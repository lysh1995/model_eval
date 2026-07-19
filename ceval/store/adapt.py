"""Adapters between the DB and the eval pipeline.

  offline_run_from_store  DB dialogues -> the OfflineRun the scorer consumes
  persist_gradebook       a scored GradeBook -> grades + evidence rows in the DB
  gradebook_from_store    grades rows -> a GradeBook the dashboard renders

So the pipeline is unchanged; only its input/output are the DB instead of files.
"""
from __future__ import annotations
import json
from typing import Optional

from .db import Store
from ..offline.runner import OfflineRun
from ..gradebook import Grade, GradeBook, Role, Source, Axis


def offline_run_from_store(store: Store, language: str = "en") -> OfflineRun:
    variants = [v["id"] for v in store.list_variants()]
    dialogues, cards = {}, {}
    chars = store.characters()
    for cid, c in chars.items():
        cards[cid] = c.get("card", "")
    for vid in variants:
        by_char = {}
        for d in store.dialogues_for(vid):
            by_char[d["character_id"]] = d["turns"]
        if by_char:
            dialogues[vid] = by_char
    present = [v for v in variants if v in dialogues]
    return OfflineRun(present, language, dialogues, cards)


def persist_gradebook(store: Store, gb: GradeBook, phase: str,
                      evidence: Optional[dict] = None):
    for g in gb.grades:
        ev_id = (g.provenance or {}).get("evaluator")
        eid = None
        if ev_id:
            eid = store.add_evaluator(kind=ev_id.split("/")[0], model_snapshot=ev_id)
        iv = g.interval or (None, None)
        store.add_grade({
            "variant_id": g.variant_id, "dimension": g.dimension, "value": g.value,
            "role": g.role.value, "source": g.source.value, "phase": phase,
            "language": g.language, "evaluator_id": eid,
            "interval_low": iv[0], "interval_high": iv[1], "n_effective": g.n_effective,
            "segment": g.segment, "caveats": json.dumps(g.caveats, ensure_ascii=False)})
    if evidence:
        for vid, dims in evidence.items():
            for dim, ex in dims.items():
                if "note" in ex:
                    continue
                for kind in ("good", "bad"):
                    e = ex.get(kind)
                    if e:
                        store.add_evidence({
                            "variant_id": vid, "dimension": dim, "kind": kind,
                            "character_id": e["character"], "text": e["text"],
                            "score": e["score"], "why": e["why"]})


_ROLE = {r.value: r for r in Role}
_SRC = {s.value: s for s in Source}
_AXIS = {a.value: a for a in Axis}


def gradebook_from_store(store: Store, title: str) -> GradeBook:
    variants = [v["id"] for v in store.list_variants()]
    gb = GradeBook(title=title, variant_ids=variants, dataset_id="db",
                   evaluator_ids=sorted({e["id"] for e in store._rows("SELECT id FROM evaluators")}),
                   created_iso=__import__("datetime").datetime.now(
                       __import__("datetime").timezone.utc).isoformat())
    for r in store.grades():
        iv = (r["interval_low"], r["interval_high"]) if r["interval_low"] is not None else None
        try:
            gb.add(Grade(
                dimension=r["dimension"], variant_id=r["variant_id"], language=r["language"] or "en",
                value=r["value"], role=_ROLE.get(r["role"], Role.GUIDE),
                source=_SRC.get(r["source"], Source.OFFLINE_CONTENT),
                axis=Axis.QUALITY, interval=iv, n_effective=r["n_effective"] or 0,
                n_unit="conversations", segment=r["segment"] or "all",
                caveats=r["caveats"], provenance={"evaluator": r["evaluator_id"]} if r["evaluator_id"] else {}))
        except ValueError:
            pass  # e.g. a pooled-language guard; skip rather than crash the dashboard
    return gb


def evidence_from_store(store: Store) -> dict:
    out: dict = {}
    for e in store.evidence():
        out.setdefault(e["variant_id"], {}).setdefault(e["dimension"], {})[e["kind"]] = {
            "character": e["character_id"], "text": e["text"],
            "score": e["score"], "why": e["why"]}
    return out


# ── online sessions: the behavioural analogue of an offline dialogue ─────────────────────────
# A session row is one faked user interaction; persisting it makes the online half a real
# DB-backed data flow (drill-down + traceability), and grading reads it back from the store.
_SESSION_SIGNAL_FIELDS = ("conversation_id", "n_turns", "abandoned", "follow_up_rate",
                          "regenerates", "edits", "votes_favor", "votes_defavor",
                          "total_latency_ms", "length_slope", "ended_reason", "user_cocreation")


def persist_online_sessions(store: Store, rows: list) -> int:
    """Write simulated SessionSignals rows into the DB `sessions` table. Returns the count."""
    for r in rows:
        signals = {k: getattr(r, k) for k in _SESSION_SIGNAL_FIELDS}
        store.add_session(r.variant_id, r.character_id, r.assignment_arm, signals, r.language)
    return len(rows)


def online_sessions_from_store(store: Store) -> list:
    """Read persisted sessions back out as SessionSignals — grading consumes these, proving the
    retrieve→grade pipeline runs off the store, not off in-memory simulator output."""
    from ..online.signals import SessionSignals
    out = []
    for row in store.all_sessions():
        s = row["signals"]
        out.append(SessionSignals(
            conversation_id=s.get("conversation_id", f"db_{row['id']}"),
            variant_id=row["variant_id"], character_id=row["character_id"],
            language=row.get("language", "en"), assignment_arm=row["arm"],
            n_turns=int(s["n_turns"]), abandoned=bool(s["abandoned"]),
            follow_up_rate=float(s["follow_up_rate"]), regenerates=int(s["regenerates"]),
            edits=int(s["edits"]), votes_favor=int(s["votes_favor"]),
            votes_defavor=int(s["votes_defavor"]), total_latency_ms=float(s["total_latency_ms"]),
            length_slope=s.get("length_slope"), ended_reason=s.get("ended_reason", "graceful"),
            user_cocreation=float(s.get("user_cocreation", 0.0))))
    return out
