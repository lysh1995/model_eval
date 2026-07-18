"""The evaluation SERVICE — one organized platform, offline + online.

Think of it as a service with a clean shape:

    INPUT   ──▶   DOMAIN            ──▶   OUTPUT
    mock data     dimensions +            dashboard /
    (prompts,     scoring (the            pages /
     model,       grade book)             visualization
     traffic)

  INPUT   the variants under test (model + params + system prompt), exercised either
          OFFLINE (generate dialogues on a test suite) or ONLINE (served to faked user
          traffic that emits actions: response times, votes, model selection, regenerate,
          abandonment, follow-up).
  DOMAIN  the dimension catalogue (ceval/offline/scheme.py) + the scoring lanes (compute /
          psychometric / judge for offline; behavioural for online). Both phases emit the
          SAME GradeBook shape, so they are one platform, not two.
  OUTPUT  one dashboard rendering both phases for the same variants — the outcome.

The unifying story this makes visible: the variant that is worst OFFLINE (character dilution,
low fidelity, high wimp) is the one that games engagement ONLINE (votes, session depth) while
scoring worst on the one honest behavioural signal (follow-up rate). Offline and online agree,
and the platform shows it in one place.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .gradebook import Grade, GradeBook, Role, Source
from .offline import load_run, run as run_offline, make_provider, SCHEME
from .online.simulator import TrafficSimulator, VariantProfile
from .online.live_grade import LiveGrader
from .online.events import AssignmentArm
from .ability import build_profiles, measure_field


# Online behaviour profiles for the three real offline variants. These CONTINUE the offline
# story: v_assistant games engagement (votes, retention, self-selection) while starving the
# one honest signal (follow-up). Faked, but designed to be coherent with the offline finding.
ONLINE_PROFILES = {
    "v_terse":     VariantProfile("v_terse",     p_follow_up=0.45, p_abandon=0.10,
                                  p_regenerate=0.07, base_latency_ms=650,
                                  p_vote_favor=0.12, self_selection_pull=1.0),
    "v_narrator":  VariantProfile("v_narrator",  p_follow_up=0.40, p_abandon=0.08,
                                  p_regenerate=0.09, base_latency_ms=1100,
                                  p_vote_favor=0.18, self_selection_pull=1.1),
    # the engagement-gaming one: high votes + low abandon + heavy-user pull, LOW follow-up
    "v_assistant": VariantProfile("v_assistant", p_follow_up=0.18, p_abandon=0.05,
                                  p_regenerate=0.12, base_latency_ms=900,
                                  p_vote_favor=0.34, self_selection_pull=1.9),
}


@dataclass
class ServiceResult:
    offline: Optional[GradeBook]
    online: Optional[GradeBook]
    ability_profiles: list
    merged: GradeBook


class EvalService:
    """The platform facade. One object, the whole pipeline."""

    def __init__(self, language: str = "en"):
        self.language = language

    # ---- INPUT → DOMAIN: offline -------------------------------------------
    def evaluate_offline(self, gen_dir: str, tasks_path: str, created_iso: str,
                         provider_kind: str = "recorded") -> tuple:
        """Score generated variant dialogues on the offline scheme. Returns (gradebook, run)."""
        offline = load_run(gen_dir, tasks_path, self.language)
        prov = make_provider(provider_kind, judge_dir="out/judge") \
            if provider_kind == "recorded" else make_provider(provider_kind)
        gb = run_offline(offline, prov, created_iso)
        return gb, offline

    # ---- INPUT → DOMAIN: online --------------------------------------------
    def evaluate_online(self, variant_ids: List[str], created_iso: str,
                        characters: Optional[List[str]] = None,
                        n_sessions: int = 1500, seed: int = 0) -> GradeBook:
        """Serve the variants to FAKED user traffic and grade behaviour.

        The traffic emits real user-action shapes (response times, votes, model selection,
        regenerate, abandonment). Both assignment arms are simulated so the platform can
        separate the causal (randomised) arm from the confounded (self-selected) one.
        """
        profiles = [ONLINE_PROFILES[v] for v in variant_ids if v in ONLINE_PROFILES]
        chars = characters or [f"c{i}" for i in range(20)]
        sim = TrafficSimulator(profiles, chars, self.language, seed=seed)
        rows = (sim.run(n_sessions, AssignmentArm.RANDOMIZED_DEFAULT) +
                sim.run(n_sessions, AssignmentArm.SELF_SELECTED))
        return LiveGrader(self.language).grade(
            rows, [p.variant_id for p in profiles], "faked-traffic", created_iso)

    # ---- portrait (from offline generated text) ----------------------------
    def ability(self, offline_run) -> list:
        field = {}
        for vid, chars in offline_run.dialogues.items():
            field.update(measure_field(_VariantShim(vid, chars), self.language, budget=200))
        return build_profiles(field, self.language)

    # ---- DOMAIN → OUTPUT: merge both phases into one gradebook --------------
    def merge(self, offline: Optional[GradeBook], online: Optional[GradeBook],
              created_iso: str) -> GradeBook:
        variants = sorted(set(
            (offline.variant_ids if offline else []) +
            (online.variant_ids if online else [])))
        merged = GradeBook(
            title="Companion variant evaluation — offline + online",
            variant_ids=variants, dataset_id="unified",
            evaluator_ids=sorted(set(
                (offline.evaluator_ids if offline else []) +
                (online.evaluator_ids if online else []))),
            created_iso=created_iso)
        for gb in (offline, online):
            if not gb:
                continue
            for g in gb.grades:
                merged.add(g)
            merged.cannot_measure += gb.cannot_measure
        # dedupe cannot_measure preserving order
        seen = set()
        merged.cannot_measure = [c for c in merged.cannot_measure
                                 if not (c in seen or seen.add(c))]
        return merged

    # ---- the full service call ---------------------------------------------
    def evaluate(self, gen_dir: str, tasks_path: str, created_iso: str,
                 provider_kind: str = "recorded", online_sessions: int = 1500) -> ServiceResult:
        offline_gb, offline_run = self.evaluate_offline(gen_dir, tasks_path, created_iso,
                                                        provider_kind)
        profiles = self.ability(offline_run)
        online_gb = self.evaluate_online(offline_run.variant_ids, created_iso,
                                         n_sessions=online_sessions)
        merged = self.merge(offline_gb, online_gb, created_iso)
        return ServiceResult(offline_gb, online_gb, profiles, merged)


class _VariantShim:
    """Adapts a {character: turns} dict to the corpus interface measure_field expects."""
    def __init__(self, vid, chars):
        self._vid, self._chars = vid, chars
    def models(self):
        return [self._vid]
    @property
    def dialogues(self):
        vid = self._vid
        class D:
            def __init__(s, cid, turns): s.model_name = vid; s.seed_id = cid; s.turns = turns
            def ai_texts(s): return [t["text"] for t in s.turns if t["role"] == "ai"]
        return [D(c, t) for c, t in self._chars.items()]
    def character_texts(self, m):
        return {c: [t["text"] for t in ts if t["role"] == "ai"] for c, ts in self._chars.items()}
