"""The offline test runner: variant + scheme -> GradeBook. Component 3's backend.

Pipeline:
  1. reconstruct dialogues from generated replies + the replayed user turns
  2. COMPUTE dimensions (repetition, discriminability, scene-drive, over-refusal) — run on the
     REAL generated content, fully automated, no model call
  3. PSYCHOMETRIC dimensions (α, test-retest) — self-validating, via the scoring provider
  4. JUDGE dimensions (voice fidelity, wimp) — via the scoring provider
  5. emit a GradeBook, every grade stamped with its evaluator + provenance

Provenance is the firewall: compute grades are real measurements on real Claude output; judge
and psychometric grades carry the provider's evaluator_id (e.g. 'simulated/v1'), so a simulated
score can never be mistaken for a measured one.
"""
from __future__ import annotations
import json, pathlib, statistics as st
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..gradebook import Grade, GradeBook, Role, Source, Axis
from ..metrics.builtin import Repetition, Discriminability, Homogenization
from ..metrics.craft import Initiative
from ..safety.refusal import OverRefusal
from .scheme import SCHEME, Dimension, Lane, Level
from .psychometric import analyse, retest, administer_prompt, QUESTIONNAIRE
from .provider import ScoringProvider, make_provider


def reconstruct(user_turns: List[str], ai_replies: List[str], prologue: str) -> List[dict]:
    """Interleave replayed user turns with generated AI replies into the turn format."""
    turns = [{"role": "ai", "round": 0, "text": prologue}]
    rnd = 1
    for i, u in enumerate(user_turns):
        turns.append({"role": "user", "round": rnd, "text": u}); rnd += 1
        if i < len(ai_replies):
            turns.append({"role": "ai", "round": rnd, "text": ai_replies[i]}); rnd += 1
    return turns


@dataclass
class OfflineRun:
    variant_ids: List[str]
    language: str
    dialogues: Dict[str, Dict[str, List[dict]]]   # variant -> character -> turns
    cards: Dict[str, str]


def load_run(gen_dir: str, tasks_path: str, language: str = "en") -> OfflineRun:
    tasks = json.loads(pathlib.Path(tasks_path).read_text())
    cards = {cid: t["card"] for cid, t in tasks.items()}
    dialogues: Dict[str, Dict[str, List[dict]]] = {}
    for f in sorted(pathlib.Path(gen_dir).glob("v_*.json")):
        vid = f.stem
        replies = json.loads(f.read_text())
        dialogues[vid] = {}
        for cid, ai in replies.items():
            if cid not in tasks:
                continue
            dialogues[vid][cid] = reconstruct(tasks[cid]["user_turns"], ai,
                                              tasks[cid]["prologue"])
    return OfflineRun(sorted(dialogues), language, dialogues, cards)


def run(offline: OfflineRun, provider: ScoringProvider, created_iso: str) -> GradeBook:
    lang = offline.language
    gb = GradeBook(
        title="Offline test — Claude Sonnet variants (real generation)",
        variant_ids=offline.variant_ids, dataset_id="sonnet-gen/3char",
        evaluator_ids=["content/v1", provider.evaluator_id], created_iso=created_iso)

    rep, ini, orf = Repetition(lang), Initiative(lang), OverRefusal(lang)

    for vid in offline.variant_ids:
        chars = offline.dialogues[vid]

        # ---- COMPUTE (real measurement on real Claude output) --------------
        rep_vals, drive_vals, refusal_vals = [], [], []
        for cid, turns in chars.items():
            rep_vals.append(rep.compute({cid: turns})[cid])
            drive_vals.append(ini.compute({cid: turns})[f"{cid}::treadmill"])
            refusal_vals.append(orf.compute({cid: turns})[cid])
        _add(gb, "repetition", vid, lang, st.mean(rep_vals), Role.GATE,
             Source.OFFLINE_CONTENT, n=len(chars),
             cav=["L3 · compute · real measurement · validated 10-13× MDE"])
        _add(gb, "scene_drive_treadmill", vid, lang, st.mean(drive_vals), Role.GUIDE,
             Source.OFFLINE_CONTENT, n=len(chars),
             cav=["L3 · compute · positive = talks a lot, moves nothing"])
        _add(gb, "over_refusal", vid, lang, st.mean(refusal_vals), Role.GUIDE,
             Source.OFFLINE_CONTENT, n=len(chars), axis=Axis.SAFETY_REFUSAL,
             cav=["safety · compute · frame-breaks only; pair with harm, never average"])

        # discriminability + homogenization need text across characters
        texts = {cid: [t["text"] for t in turns if t["role"] == "ai"]
                 for cid, turns in chars.items()}
        disc = Discriminability(lang, 200).run(texts).values.get("accuracy", float("nan"))
        _add(gb, "discriminability", vid, lang, disc, Role.GUIDE, Source.OFFLINE_CONTENT,
             n=len(chars), cav=["L2 · compute · prices the catalogue; chance = 1/3"])

        # ---- PSYCHOMETRIC (self-validating; via provider) -----------------
        # Administer across MANY scene contexts (α needs a sample of administrations, not 2).
        # α across contexts = 'does the character answer a trait's items consistently?'
        alphas = []
        for cid, turns in chars.items():
            card = offline.cards.get(cid, "")
            admins = provider.questionnaire_administrations(vid, cid, card, n=8)
            if len(admins) < 2:
                continue
            res = analyse(vid, cid, admins)
            if res.mean_alpha is not None:
                alphas.append(max(0.0, res.mean_alpha))     # α<0 = no coherent trait -> floor at 0
        if alphas:
            _add(gb, "character_alpha", vid, lang, st.mean(alphas), Role.GUIDE,
                 Source.OFFLINE_JUDGE, n=len(chars), evaluator=provider.evaluator_id,
                 cav=[f"L1 · psychometric · SELF-VALIDATING (no ground truth) · "
                      f"α≈0.8 = a character is in there · provider={provider.kind}"])

        # ---- JUDGE (via provider) -----------------------------------------
        fids, wimps = [], []
        for cid, turns in chars.items():
            card = offline.cards.get(cid, "")
            replies = [t["text"] for t in turns if t["role"] == "ai" and t.get("round", 0) > 0]
            for j in provider.fidelity_scores(vid, cid, card, replies):
                fids.append(j["voice_fidelity"]); wimps.append(j["wimp"])
        if fids:
            _add(gb, "voice_fidelity", vid, lang, st.mean(fids), Role.GUIDE,
                 Source.OFFLINE_JUDGE, n=len(chars), evaluator=provider.evaluator_id,
                 cav=[f"L2 · judge · pairwise vs anchor · provider={provider.kind}"])
            _add(gb, "wimp_rate", vid, lang, st.mean(wimps), Role.GUIDE,
                 Source.OFFLINE_JUDGE, n=len(chars), axis=Axis.SAFETY_REFUSAL,
                 evaluator=provider.evaluator_id,
                 cav=[f"safety · judge · sycophancy=accept-without-add · SEGMENT before gating "
                      f"· provider={provider.kind}"])

        # ---- STORYTELLING CRAFT (the product core; the STORY side, not the persona) --------
        # Session-level: narrative craft is a property of the trajectory, not a reply (note 12).
        # Judge-free heuristics measure entity density, not craft, so this is a judge dimension.
        if hasattr(provider, "craft_scores"):
            crafts = []
            for cid in chars:
                c = provider.craft_scores(vid, cid, offline.cards.get(cid, ""))
                if c is not None and c == c:
                    crafts.append(c)
            if crafts:
                _add(gb, "narrative_craft", vid, lang, st.mean(crafts), Role.GUIDE,
                     Source.OFFLINE_JUDGE, n=len(crafts), evaluator=provider.evaluator_id,
                     cav=[f"L3 · judge · STORY craft: scene advancement + co-creation, "
                          f"SESSION-level (note 12: craft is a trajectory property) · "
                          f"provider={provider.kind}"])

    gb.cannot_measure = [
        "whether users PREFER a variant — no user touched this (needs live Q1 / regenerate data)",
        "chemistry (user × character × model) — structurally impossible offline",
        "anything cross-language — this run is en only; ρ(en,zh) = −0.082",
        f"judge & psychometric grades came from provider '{provider.kind}'"
        + (" — SIMULATED, not a measurement of the model; the pipeline is real, the numbers are not"
           if provider.kind == "simulated"
           else " — REAL Claude Sonnet judging (evaluator " + provider.evaluator_id + ")"
           if provider.kind == "recorded" else ""),
    ]
    return gb


def _add(gb, dim, vid, lang, val, role, source, n, cav, axis=Axis.QUALITY, evaluator=None):
    if val != val:      # NaN
        return
    gb.add(Grade(dimension=dim, variant_id=vid, language=lang, value=val, role=role,
                 source=source, axis=axis, n_effective=n, n_unit="conversations",
                 caveats=list(cav),
                 provenance={"evaluator": evaluator} if evaluator else {}))
