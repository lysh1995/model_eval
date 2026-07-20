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

from .core.gradebook import Grade, GradeBook, Role, Source
from .offline import load_run, run as run_offline, make_provider, SCHEME
from .online.simulator import TrafficSimulator, VariantProfile
from .online.live_grade import LiveGrader
from .online.events import AssignmentArm
from .ability import build_profiles, measure_field


# Online behaviour profiles for all six variants. These are FAKED but designed to CONTINUE the
# offline story coherently — each variant's online signature matches how it failed (or didn't)
# offline. Three distinct shapes:
#   healthy   (terse, narrator)      — draw the user out (high follow-up), few votes, no pull.
#   gaming    (assistant, ·Haiku)    — the sycophancy trap: high votes + low abandon + heavy-user
#                                      pull, but STARVED follow-up. Looks best on votes, worst on
#                                      the one honest signal. This is what must not headline.
#   friction  (hostile)              — the opposite failure: users bounce off the prickliness →
#                                      HIGH abandonment, LOW votes, heavy users AVOID it (pull<1).
# The Haiku twins mirror their Sonnet twin's SHAPE with a small model delta: faster latency,
# slightly weaker engagement — consistent with their lower offline voice_fidelity.
ONLINE_PROFILES = {
    # craft= is the offline JUDGE narrative_craft score, injected as ground truth: the simulated
    # user co-creates in proportion to it — DECOUPLED from p_vote_favor, so the sycophant shows
    # high votes + LOW co-creation (the divergence the online craft proxy must recover).
    "v_terse":     VariantProfile("v_terse",     p_follow_up=0.45, p_abandon=0.10,
                                  p_regenerate=0.07, base_latency_ms=650,
                                  p_vote_favor=0.12, self_selection_pull=1.0,  craft=0.64),
    "v_narrator":  VariantProfile("v_narrator",  p_follow_up=0.40, p_abandon=0.08,
                                  p_regenerate=0.09, base_latency_ms=1100,
                                  p_vote_favor=0.18, self_selection_pull=1.1,  craft=0.82),
    # engagement-gaming: high votes + low abandon + heavy-user pull, LOW follow-up, LOW craft
    "v_assistant": VariantProfile("v_assistant", p_follow_up=0.18, p_abandon=0.05,
                                  p_regenerate=0.12, base_latency_ms=900,
                                  p_vote_favor=0.34, self_selection_pull=1.9,  craft=0.25),
    # friction failure: users leave (high abandon), rarely vote it up — but craft is HIGH (0.81)
    "v_hostile":   VariantProfile("v_hostile",   p_follow_up=0.30, p_abandon=0.24,
                                  p_regenerate=0.15, base_latency_ms=780,
                                  p_vote_favor=0.07, self_selection_pull=0.6,  craft=0.81),
    # Haiku twins: same shape as the Sonnet twin, faster, engagement a touch weaker
    "v_terse_haiku":     VariantProfile("v_terse_haiku",     p_follow_up=0.41, p_abandon=0.12,
                                  p_regenerate=0.08, base_latency_ms=470,
                                  p_vote_favor=0.11, self_selection_pull=0.95, craft=0.69),
    "v_assistant_haiku": VariantProfile("v_assistant_haiku", p_follow_up=0.18, p_abandon=0.06,
                                  p_regenerate=0.13, base_latency_ms=610,
                                  p_vote_favor=0.33, self_selection_pull=1.8,  craft=0.40),
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
        prov = make_provider(provider_kind, judge_dir="demo/judge") \
            if provider_kind == "recorded" else make_provider(provider_kind)
        gb = run_offline(offline, prov, created_iso)
        return gb, offline

    # ---- INPUT → DOMAIN: online --------------------------------------------
    def simulate_online(self, variant_ids: List[str],
                        characters: Optional[List[str]] = None,
                        n_sessions: int = 1500, seed: int = 0) -> list:
        """Serve the variants to FAKED user traffic and RETURN the session rows (data points).

        The traffic emits real user-action shapes (response times, votes, model selection,
        regenerate, abandonment). Both assignment arms are simulated so the platform can separate
        the causal (randomised) arm from the confounded (self-selected) one. These rows are the
        online analogue of an offline dialogue — persist them, then grade from the store.
        """
        profiles = [self.online_profile(v) for v in variant_ids]
        chars = characters or [f"c{i}" for i in range(20)]
        sim = TrafficSimulator(profiles, chars, self.language, seed=seed)
        return (sim.run(n_sessions, AssignmentArm.RANDOMIZED_DEFAULT) +
                sim.run(n_sessions, AssignmentArm.SELF_SELECTED))

    def grade_online(self, rows: list, variant_ids: List[str], created_iso: str,
                     dataset_id: str = "faked-traffic") -> GradeBook:
        """Grade a stream of session rows (from the simulator or read back from the DB)."""
        return LiveGrader(self.language).grade(rows, variant_ids, dataset_id, created_iso)

    def evaluate_online(self, variant_ids: List[str], created_iso: str,
                        characters: Optional[List[str]] = None,
                        n_sessions: int = 1500, seed: int = 0) -> GradeBook:
        """Simulate traffic and grade it in one call (in-memory; no persistence)."""
        rows = self.simulate_online(variant_ids, characters, n_sessions, seed)
        return self.grade_online(rows, variant_ids, created_iso)

    @staticmethod
    def online_profile(v: str) -> VariantProfile:
        """The injected ground-truth behaviour for a variant; a neutral default if unknown."""
        return ONLINE_PROFILES.get(v, VariantProfile(
            v, p_follow_up=0.35, p_abandon=0.09, p_regenerate=0.09,
            base_latency_ms=800, p_vote_favor=0.18, self_selection_pull=1.0, craft=0.5))

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
