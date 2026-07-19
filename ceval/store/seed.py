"""Migrate the existing file-based data into the DB (one-time), so the service is DB-backed.

Populates: models, prompts, variants, characters, dialogues, sessions — from demo/gen/*.json,
demo/gen/tasks.json, and the variant manifest. Idempotent (content-addressed upserts).
"""
from __future__ import annotations
import json, pathlib
from .db import Store
from ..offline.variants import as_dict as variants_manifest
from ..offline.runner import reconstruct


def seed(store: Store, gen_dir: str = "demo/gen", language: str = "en") -> dict:
    gp = pathlib.Path(gen_dir)
    tasks = json.loads((gp / "tasks.json").read_text()) if (gp / "tasks.json").exists() else {}
    manifest = variants_manifest(gen_dir)

    # characters (from tasks: card + prologue + user turns)
    for cid, t in tasks.items():
        store.add_character(cid, t.get("name", cid), t.get("card", ""), language,
                            t.get("prologue", ""), t.get("initial_user_input", ""), "role-play-bench")

    # models + prompts + variants.
    # A prompt is content-addressed by its system_prompt, so the SAME prompt run on two models
    # (e.g. Terse on Sonnet vs Haiku) shares one prompt row — that IS "same baseline across models".
    # The prompt NAME must therefore be model-agnostic (`prompt`), distinct from the per-variant
    # `label` that distinguishes the two model instances in the UI.
    for vid, meta in manifest.items():
        mid = store.add_model(meta["model"], "anthropic")
        pid = store.add_prompt(meta.get("prompt", meta["label"]), meta["system_prompt"],
                               meta.get("intent", ""))
        store.add_variant(mid, pid, label=meta["label"], vid=vid)

    # dialogues (offline data points): reconstruct turns from generated replies + replayed users
    n_dlg = 0
    for f in sorted(gp.glob("v_*.json")):
        vid = f.stem
        if vid not in manifest:
            continue
        replies = json.loads(f.read_text())
        for cid, ai in replies.items():
            if cid not in tasks:
                continue
            turns = reconstruct(tasks[cid]["user_turns"], ai, tasks[cid]["prologue"])
            store.add_dialogue(vid, cid, turns, run_id="run_1", source="generated")
            n_dlg += 1

    return {"models": len(store.list_models()), "prompts": len(store.list_prompts()),
            "variants": len(store.list_variants()), "dialogues": n_dlg,
            "characters": len(store.characters())}
