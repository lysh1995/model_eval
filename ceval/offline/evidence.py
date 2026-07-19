"""Good & bad examples per dimension — make each grade explainable.

A grade is only trustworthy if you can see WHY. For the dimensions where a per-reply score
exists, this pulls the best and worst actual reply so the user reads the evidence behind the
number:

  voice_fidelity  real Claude judged each sampled reply -> show the most / least in-character
  wimp_rate       real Claude scored each reply -> show the least / most sycophantic
  repetition      computed per reply -> show the cleanest / most looping turn

Dimensions without a single-reply basis (character_alpha across a questionnaire,
discriminability across the corpus, online behavioural signals) get an honest note instead of
a fabricated example. Better to say 'aggregate, no single example' than to invent one.
"""
from __future__ import annotations
import json, pathlib, re
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class Example:
    kind: str            # "good" | "bad"
    text: str
    score: float
    character: str
    why: str


def _rep_rate(text: str) -> float:
    """Per-reply self-repetition proxy: fraction of 5-grams that repeat within the reply."""
    w = text.split()
    if len(w) < 6:
        return 0.0
    grams = [tuple(w[i:i+5]) for i in range(len(w) - 4)]
    seen, dup = set(), 0
    for g in grams:
        if g in seen:
            dup += 1
        seen.add(g)
    return dup / len(grams)


def extract(gen_dir: str = "demo/gen", judge_dir: str = "demo/judge") -> Dict[str, Dict[str, dict]]:
    """Returns evidence[variant][dimension] = {"good": {...}, "bad": {...}} or {"note": ...}."""
    gen = {f.stem: json.loads(f.read_text())
           for f in pathlib.Path(gen_dir).glob("v_*.json")}
    out: Dict[str, Dict[str, dict]] = {}

    for vid, chars in gen.items():
        ev: Dict[str, dict] = {}

        # ---- judge dimensions: per-reply scores from the recordings -------
        fpath = pathlib.Path(judge_dir) / f"fidelity_{vid}.json"
        ipath = pathlib.Path(judge_dir) / f"input_{vid}.json"
        if fpath.exists() and ipath.exists():
            fid = json.loads(fpath.read_text())
            inp = json.loads(ipath.read_text())
            pool = []   # (character, reply_text, fidelity, wimp)
            for cid, scores in fid.items():
                replies = inp.get(cid, {}).get("sampled_replies", [])
                for r, s in zip(replies, scores):
                    pool.append((cid, r, float(s.get("voice_fidelity", 0)), float(s.get("wimp", 0))))
            if pool:
                hi = max(pool, key=lambda x: x[2]); lo = min(pool, key=lambda x: x[2])
                ev["voice_fidelity"] = {
                    "good": asdict(Example("good", hi[1], hi[2], hi[0],
                        f"real Claude judge scored this {hi[2]:.2f} — most in-character")),
                    "bad": asdict(Example("bad", lo[1], lo[2], lo[0],
                        f"judge scored this {lo[2]:.2f} — least in-character"))}
                # wimp: LOW is good
                lw = min(pool, key=lambda x: x[3]); hw = max(pool, key=lambda x: x[3])
                ev["wimp_rate"] = {
                    "good": asdict(Example("good", lw[1], lw[3], lw[0],
                        f"wimp {lw[3]:.2f} — stays true to character, doesn't just agree")),
                    "bad": asdict(Example("bad", hw[1], hw[3], hw[0],
                        f"wimp {hw[3]:.2f} — warm agreement that dodges the character's edge"))}

        # ---- compute dimension: repetition per reply ---------------------
        rep_pool = []
        for cid, replies in chars.items():
            for r in replies:
                rep_pool.append((cid, r, _rep_rate(r)))
        if rep_pool:
            worst = max(rep_pool, key=lambda x: x[2]); clean = min(rep_pool, key=lambda x: x[2])
            ev["repetition"] = {
                "good": asdict(Example("good", clean[1], clean[2], clean[0],
                    f"{clean[2]:.0%} internal 5-gram recurrence — fresh")),
                "bad": asdict(Example("bad", worst[1], worst[2], worst[0],
                    f"{worst[2]:.0%} recurrence — the most repetitive turn"))}

        # ---- honest notes for dimensions with no single-reply basis ------
        ev["character_alpha"] = {"note":
            "aggregate over a 12-item questionnaire across 6 scene moments — no single reply. "
            "α measures whether the answers hang together, not one line."}
        ev["discriminability"] = {"note":
            "corpus-level: whether characters are separable across the whole set — undefined "
            "for one reply."}
        out[vid] = ev
    return out
