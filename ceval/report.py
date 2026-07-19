"""Build the dashboard from the DB — shared by `ceval dashboard` (writes files) and
`ceval serve` (serves live). One place, so the two never diverge.
"""
from __future__ import annotations
import pathlib
from typing import Tuple

from .store import Store
from .store.adapt import (offline_run_from_store, gradebook_from_store, evidence_from_store)
from .dashboard import render
from .dashboard.interactive import render_interactive
from .offline import SCHEME
from .ability import build_profiles, measure_field
from .service import _VariantShim

TITLE = "Companion variant evaluation — one platform, offline + online"


def _session_summaries(store: Store) -> dict:
    """Per-variant online drill-down straight from the persisted sessions: how many sessions,
    split by assignment arm — which surfaces the self-selection confound (heavy users over- or
    under-pick a variant), and the per-character spread."""
    out = {}
    for v in store.list_variants():
        rows = store.sessions_for(v["id"])
        if not rows:
            continue
        rnd = sum(1 for r in rows if r["arm"] == "randomized_default")
        slf = sum(1 for r in rows if r["arm"] == "self_selected")
        by_char = {}
        for r in rows:
            by_char[r["character_id"]] = by_char.get(r["character_id"], 0) + 1
        out[v["id"]] = {"total": len(rows), "randomised": rnd, "self_selected": slf,
                        "by_character": by_char}
    return out


def _prep(store: Store):
    gb = gradebook_from_store(store, TITLE)
    variants = {v["id"]: {"label": v.get("label") or v["id"], "model": v.get("model_name", ""),
                          "system_prompt": v.get("system_prompt", ""), "intent": v.get("intent", "")}
                for v in store.list_variants()}
    run = offline_run_from_store(store, "en")
    field = {}
    for vid, chars in run.dialogues.items():
        field.update(measure_field(_VariantShim(vid, chars), "en", budget=200))
    profiles = build_profiles(field, "en")
    evidence = evidence_from_store(store)
    sessions = _session_summaries(store)
    return gb, variants, profiles, evidence, sessions


def build_html(store: Store) -> Tuple[str, str]:
    """Render (static_html, interactive_html) as strings, fresh from the DB."""
    gb, variants, profiles, evidence, sessions = _prep(store)
    tmp = pathlib.Path("out/_render")
    tmp.mkdir(parents=True, exist_ok=True)
    sp = render(gb, str(tmp / "s.html"), ability_profiles=profiles, scheme=SCHEME)
    ip = render_interactive(gb, variants, profiles, str(tmp / "i.html"),
                            title=gb.title, evidence=evidence, sessions=sessions)
    return pathlib.Path(sp).read_text(), pathlib.Path(ip).read_text()


def write_files(store: Store, out_path: str) -> Tuple[str, str]:
    """Render and write both dashboards to disk. Returns (static_path, interactive_path)."""
    static_html, inter_html = build_html(store)
    sp = pathlib.Path(out_path)
    ip = pathlib.Path(out_path.replace(".html", "_interactive.html"))
    for p, h in ((sp, static_html), (ip, inter_html)):
        if "<title>" not in h:
            h = "<title>Companion Variant Evaluation</title>\n" + h
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(h)
    return str(sp), str(ip)
