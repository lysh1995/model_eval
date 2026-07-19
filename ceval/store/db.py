"""Storage layer for the evaluation service. One schema, two drivers.

  MySQL   the designed production DB (schema in schema.sql; driver via pymysql if installed)
  SQLite  the runnable local backend (stdlib, zero dependencies) — the default

Same table definitions emit driver-appropriate DDL, so nothing diverges. Models, prompts,
variants, dialogues (offline data points), sessions (online data points), grades, evidence,
and evaluator versions are all first-class rows with ids, so a user can keep injecting models,
prompts, and data and submit for eval.

Connection strings:
  sqlite:///out/ceval.db           (default)
  mysql://user:pass@host:3306/db   (uses pymysql when available)
"""
from __future__ import annotations
import hashlib, json, pathlib, re, time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ── dialect type map: (sqlite, mysql) ────────────────────────────────────────
_T = {
    "IDSTR": ("TEXT PRIMARY KEY", "VARCHAR(80) PRIMARY KEY"),
    "IDINT": ("INTEGER PRIMARY KEY AUTOINCREMENT", "BIGINT AUTO_INCREMENT PRIMARY KEY"),
    "STR":   ("TEXT", "VARCHAR(255)"),
    "TEXT":  ("TEXT", "LONGTEXT"),
    "REAL":  ("REAL", "DOUBLE"),
    "INT":   ("INTEGER", "INT"),
    "JSON":  ("TEXT", "JSON"),
    "TS":    ("TEXT DEFAULT CURRENT_TIMESTAMP", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
    "FK":    ("TEXT", "VARCHAR(80)"),
}

# ── the schema: source of truth for both dialects ───────────────────────────
# each table: (name, [(col, type_key, extra)])
TABLES: List[Tuple[str, List[Tuple[str, str, str]]]] = [
    ("models", [
        ("id", "IDSTR", ""), ("name", "STR", ""), ("provider", "STR", ""),
        ("params", "JSON", ""), ("created_at", "TS", "")]),
    ("prompts", [
        ("id", "IDSTR", ""), ("name", "STR", ""), ("system_prompt", "TEXT", ""),
        ("intent", "STR", ""), ("created_at", "TS", "")]),
    ("variants", [
        ("id", "IDSTR", ""), ("model_id", "FK", ""), ("prompt_id", "FK", ""),
        ("anchoring_policy", "STR", ""), ("label", "STR", ""), ("created_at", "TS", "")]),
    ("characters", [
        ("id", "IDSTR", ""), ("name", "STR", ""), ("card", "TEXT", ""),
        ("language", "STR", ""), ("prologue", "TEXT", ""),
        ("initial_user_input", "TEXT", ""), ("source", "STR", "")]),
    ("dialogues", [   # offline data points: a variant playing a character
        ("id", "IDINT", ""), ("variant_id", "FK", ""), ("character_id", "FK", ""),
        ("run_id", "STR", ""), ("turns", "JSON", ""), ("source", "STR", ""),
        ("created_at", "TS", "")]),
    ("sessions", [    # online data points: faked/real user traffic signals
        ("id", "IDINT", ""), ("variant_id", "FK", ""), ("character_id", "FK", ""),
        ("arm", "STR", ""), ("language", "STR", ""), ("signals", "JSON", ""),
        ("created_at", "TS", "")]),
    ("evaluators", [
        ("id", "IDSTR", ""), ("kind", "STR", ""), ("model_snapshot", "STR", ""),
        ("prompt_hash", "STR", ""), ("rubric_version", "STR", ""), ("created_at", "TS", "")]),
    ("grades", [
        ("id", "IDINT", ""), ("variant_id", "FK", ""), ("dimension", "STR", ""),
        ("value", "REAL", ""), ("role", "STR", ""), ("source", "STR", ""),
        ("phase", "STR", ""), ("language", "STR", ""), ("evaluator_id", "FK", ""),
        ("interval_low", "REAL", ""), ("interval_high", "REAL", ""),
        ("n_effective", "INT", ""), ("segment", "STR", ""), ("caveats", "JSON", ""),
        ("created_at", "TS", "")]),
    ("evidence", [
        ("id", "IDINT", ""), ("variant_id", "FK", ""), ("dimension", "STR", ""),
        ("kind", "STR", ""), ("character_id", "FK", ""), ("text", "TEXT", ""),
        ("score", "REAL", ""), ("why", "STR", ""), ("created_at", "TS", "")]),
]


def ddl(dialect: str) -> str:
    i = 0 if dialect == "sqlite" else 1
    out = []
    for name, cols in TABLES:
        lines = [f"  {c} {_T[t][i]}{(' ' + e) if e else ''}" for c, t, e in cols]
        suffix = "" if dialect == "sqlite" else " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        out.append(f"CREATE TABLE IF NOT EXISTS {name} (\n" + ",\n".join(lines) + f"\n){suffix};")
    return "\n\n".join(out)


def _hash(*parts) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str,
                                     ensure_ascii=False).encode()).hexdigest()[:12]


class Store:
    def __init__(self, url: str = "sqlite:///out/ceval.db"):
        self.url = url
        self.dialect = "mysql" if url.startswith("mysql") else "sqlite"
        self._conn = self._connect()

    def _connect(self):
        if self.dialect == "sqlite":
            import sqlite3
            path = self.url.replace("sqlite:///", "") or ":memory:"
            if path != ":memory:":
                pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
            c = sqlite3.connect(path)
            c.row_factory = sqlite3.Row
            c.execute("PRAGMA foreign_keys=ON")
            return c
        # mysql via pymysql
        try:
            import pymysql
        except ImportError:
            raise RuntimeError(
                "mysql:// requested but pymysql is not installed. Install pymysql, or use "
                "the default sqlite:///out/ceval.db backend (zero dependencies).")
        m = re.match(r"mysql://([^:]+):([^@]*)@([^:/]+):?(\d+)?/(.+)", self.url)
        if not m:
            raise ValueError("mysql url must be mysql://user:pass@host:port/db")
        user, pw, host, port, db = m.groups()
        return pymysql.connect(host=host, port=int(port or 3306), user=user, password=pw,
                               database=db, charset="utf8mb4", autocommit=True)

    # -- ddl -----------------------------------------------------------------
    def init(self):
        cur = self._conn.cursor()
        for stmt in ddl(self.dialect).split(";"):
            if stmt.strip():
                cur.execute(stmt)
        self._commit()

    def _ph(self):
        return "?" if self.dialect == "sqlite" else "%s"

    def _commit(self):
        if self.dialect == "sqlite":
            self._conn.commit()

    def _exec(self, sql: str, params: tuple = ()):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        self._commit()
        return cur

    def _rows(self, sql: str, params: tuple = ()) -> List[dict]:
        cur = self._conn.cursor()
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

    def _upsert(self, table: str, row: dict):
        ph = self._ph()
        cols = list(row)
        placeholders = ", ".join(ph for _ in cols)
        verb = "INSERT OR REPLACE" if self.dialect == "sqlite" else "REPLACE"
        self._exec(f"{verb} INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
                   tuple(row[c] for c in cols))

    def _insert(self, table: str, row: dict) -> int:
        ph = self._ph()
        cols = list(row)
        cur = self._exec(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(ph for _ in cols)})",
            tuple(row[c] for c in cols))
        return cur.lastrowid

    # -- domain: create -----------------------------------------------------
    def add_model(self, name: str, provider: str = "anthropic", params: dict = None) -> str:
        mid = "m_" + _hash(name, provider, params or {})
        self._upsert("models", {"id": mid, "name": name, "provider": provider,
                                "params": json.dumps(params or {})})
        return mid

    def add_prompt(self, name: str, system_prompt: str, intent: str = "") -> str:
        pid = "p_" + _hash(system_prompt)
        self._upsert("prompts", {"id": pid, "name": name, "system_prompt": system_prompt,
                                 "intent": intent})
        return pid

    def add_variant(self, model_id: str, prompt_id: str, label: str = "",
                    anchoring_policy: str = "once_at_start", vid: str = None) -> str:
        vid = vid or ("v_" + _hash(model_id, prompt_id, anchoring_policy))
        self._upsert("variants", {"id": vid, "model_id": model_id, "prompt_id": prompt_id,
                                  "anchoring_policy": anchoring_policy, "label": label})
        return vid

    def add_character(self, cid: str, name: str, card: str, language: str = "en",
                      prologue: str = "", initial_user_input: str = "", source: str = "") -> str:
        self._upsert("characters", {"id": cid, "name": name, "card": card, "language": language,
                                    "prologue": prologue, "initial_user_input": initial_user_input,
                                    "source": source})
        return cid

    def add_dialogue(self, variant_id: str, character_id: str, turns: list,
                     run_id: str = "run_1", source: str = "generated") -> int:
        return self._insert("dialogues", {
            "variant_id": variant_id, "character_id": character_id, "run_id": run_id,
            "turns": json.dumps(turns, ensure_ascii=False), "source": source})

    def add_session(self, variant_id: str, character_id: str, arm: str, signals: dict,
                    language: str = "en") -> int:
        return self._insert("sessions", {
            "variant_id": variant_id, "character_id": character_id, "arm": arm,
            "language": language, "signals": json.dumps(signals, ensure_ascii=False)})

    def add_evaluator(self, kind: str, model_snapshot: str = "", prompt_hash: str = "",
                      rubric_version: str = "1") -> str:
        eid = "e_" + _hash(kind, model_snapshot, prompt_hash, rubric_version)
        self._upsert("evaluators", {"id": eid, "kind": kind, "model_snapshot": model_snapshot,
                                    "prompt_hash": prompt_hash, "rubric_version": rubric_version})
        return eid

    def add_grade(self, g: dict):
        self._insert("grades", g)

    def add_evidence(self, e: dict):
        self._insert("evidence", e)

    def clear_grades(self, variant_ids: List[str] = None):
        if variant_ids:
            ph = self._ph()
            self._exec(f"DELETE FROM grades WHERE variant_id IN ({', '.join(ph for _ in variant_ids)})",
                       tuple(variant_ids))
            self._exec(f"DELETE FROM evidence WHERE variant_id IN ({', '.join(ph for _ in variant_ids)})",
                       tuple(variant_ids))
        else:
            self._exec("DELETE FROM grades"); self._exec("DELETE FROM evidence")

    def clear_sessions(self, variant_ids: List[str] = None):
        if variant_ids:
            ph = self._ph()
            self._exec(f"DELETE FROM sessions WHERE variant_id IN ({', '.join(ph for _ in variant_ids)})",
                       tuple(variant_ids))
        else:
            self._exec("DELETE FROM sessions")

    # -- domain: read -------------------------------------------------------
    def list_models(self): return self._rows("SELECT * FROM models ORDER BY created_at")
    def list_prompts(self): return self._rows("SELECT * FROM prompts ORDER BY created_at")
    def list_variants(self):
        return self._rows(
            "SELECT v.*, m.name AS model_name, p.name AS prompt_name, p.system_prompt, p.intent "
            "FROM variants v LEFT JOIN models m ON v.model_id=m.id "
            "LEFT JOIN prompts p ON v.prompt_id=p.id ORDER BY v.created_at")

    def variant(self, vid: str) -> Optional[dict]:
        r = self._rows(f"SELECT v.*, m.name AS model_name, p.system_prompt, p.intent "
                       f"FROM variants v LEFT JOIN models m ON v.model_id=m.id "
                       f"LEFT JOIN prompts p ON v.prompt_id=p.id WHERE v.id={self._ph()}", (vid,))
        return r[0] if r else None

    def dialogues_for(self, variant_id: str) -> List[dict]:
        rows = self._rows(f"SELECT * FROM dialogues WHERE variant_id={self._ph()} ORDER BY id",
                          (variant_id,))
        for r in rows:
            r["turns"] = json.loads(r["turns"])
        return rows

    def sessions_for(self, variant_id: str) -> List[dict]:
        rows = self._rows(f"SELECT * FROM sessions WHERE variant_id={self._ph()}", (variant_id,))
        for r in rows:
            r["signals"] = json.loads(r["signals"])
        return rows

    def all_sessions(self) -> List[dict]:
        rows = self._rows("SELECT * FROM sessions ORDER BY id")
        for r in rows:
            r["signals"] = json.loads(r["signals"])
        return rows

    def characters(self) -> Dict[str, dict]:
        return {r["id"]: r for r in self._rows("SELECT * FROM characters")}

    def grades(self) -> List[dict]:
        rows = self._rows("SELECT * FROM grades")
        for r in rows:
            r["caveats"] = json.loads(r["caveats"]) if r.get("caveats") else []
        return rows

    def evidence(self) -> List[dict]:
        return self._rows("SELECT * FROM evidence")

    def counts(self) -> dict:
        return {t: self._rows(f"SELECT COUNT(*) AS n FROM {t}")[0]["n"]
                for t, _ in TABLES}
