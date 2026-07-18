"""Fake production traffic, so the retrieval -> grade pipeline can be built and TESTED before
a single real user exists.

The user asked for exactly this: "create fake user dialogs with response times, and inject
some favor or de-favor vote, and fake selection ... to simulate our data retrieving pipeline
and the data we retrieved."

CRITICAL DESIGN CHOICE: the simulator does not emit noise. It emits traffic with a KNOWN,
INJECTED structure -- a good variant and a bad variant with a real, specified gap -- so that
downstream we can VERIFY the live grade book recovers what we put in. A simulator that
produces plausible-looking random data would let us ship a broken grade book that looks fine.
That is this project's whole failure mode, six times over.

It also reproduces the two confounds we must design around, so we can prove the pipeline
handles them:

  SELF-SELECTION   heavy users disproportionately pick the "good" variant, so on the
                   self-selected arm the good variant looks even better than it is. The
                   randomised-default arm is clean. If the grade book cannot tell these
                   apart, it inherits the confound.

  SYCOPHANCY TRAP  the "engaging" variant earns more thumbs-up AND more abandonment-avoidance
                   while being no better on diagnostics -- so a grade book that headlines
                   votes ranks it first. It must not.
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .events import AssignmentArm
from .signals import SessionSignals, follow_up_question_rate, message_length_trajectory


@dataclass
class VariantProfile:
    """The GROUND TRUTH we inject. The grade book's job is to recover it."""
    variant_id: str
    # diagnostic truth
    p_follow_up: float          # probability a model turn asks a question
    p_abandon: float            # probability the user leaves mid-scene
    p_regenerate: float         # per-turn regenerate probability
    base_latency_ms: float
    # the trap: an "engaging" variant games votes without being better
    p_vote_favor: float
    # self-selection: how strongly heavy users prefer this variant when they choose
    self_selection_pull: float  # >1 = heavy users over-pick it


# Two variants with a KNOWN, deliberate structure:
#   GOOD  draws users out (high follow-up), rarely abandoned, low regen.
#   ENGAGING  games votes (high favor) and avoids abandonment, but LOWER follow-up
#             (it talks AT the user) -- the sycophancy signature. Heavy users over-pick it.
GOOD = VariantProfile("v_good", p_follow_up=0.55, p_abandon=0.08, p_regenerate=0.06,
                      base_latency_ms=700, p_vote_favor=0.12, self_selection_pull=1.0)
ENGAGING = VariantProfile("v_engaging", p_follow_up=0.20, p_abandon=0.05, p_regenerate=0.10,
                          base_latency_ms=900, p_vote_favor=0.30, self_selection_pull=1.8)


class TrafficSimulator:
    """Generates SessionSignals rows, the shape the retrieval pipeline stores."""

    def __init__(self, profiles: List[VariantProfile], characters: List[str],
                 language: str = "en", seed: int = 0):
        self.profiles = {p.variant_id: p for p in profiles}
        self.characters = characters
        self.language = language
        self.rng = random.Random(seed)

    def _assign(self, arm: AssignmentArm, is_heavy_user: bool) -> str:
        """Return the variant this session runs on.

        RANDOMIZED_DEFAULT: uniform, ignoring user type -> clean.
        SELF_SELECTED: heavy users pull toward the high self_selection_pull variant -> the
        confound we must handle downstream.
        """
        ids = list(self.profiles)
        if arm is AssignmentArm.RANDOMIZED_DEFAULT or not is_heavy_user:
            return self.rng.choice(ids)
        weights = [self.profiles[i].self_selection_pull for i in ids]
        return self.rng.choices(ids, weights=weights, k=1)[0]

    def _session(self, variant_id: str, character_id: str, arm: AssignmentArm,
                 is_heavy_user: bool) -> SessionSignals:
        p = self.profiles[variant_id]
        # heavy users have longer sessions regardless of variant -- this is the confound:
        # it makes session_depth (a trap) track the USER, not the variant.
        n_turns = self.rng.randint(30, 90) if is_heavy_user else self.rng.randint(4, 25)
        ai_texts, user_texts = [], []
        regen = edits = fav = defav = 0
        total_latency = 0.0
        abandoned = False
        for i in range(n_turns):
            asks = self.rng.random() < p.p_follow_up
            ai_texts.append(("How does that land for you?" if asks else "The room falls quiet.")
                            + f" turn{i}")
            # user message length DECAYS if the model doesn't draw them out (low follow-up)
            base_len = 60 if asks else 30
            user_texts.append("x" * max(3, int(base_len - i * (0.0 if asks else 0.6)
                                              + self.rng.gauss(0, 5))))
            total_latency += p.base_latency_ms + self.rng.gauss(0, 120)
            if self.rng.random() < p.p_regenerate:
                regen += 1
            if self.rng.random() < 0.02:
                edits += 1
            if self.rng.random() < p.p_vote_favor:
                fav += 1
            elif self.rng.random() < 0.05:
                defav += 1
            if self.rng.random() < p.p_abandon / n_turns:
                abandoned = True
                break
        return SessionSignals(
            conversation_id=f"sim_{self.rng.getrandbits(32):08x}",
            variant_id=variant_id, character_id=character_id, language=self.language,
            assignment_arm=arm.value, n_turns=len(ai_texts), abandoned=abandoned,
            follow_up_rate=follow_up_question_rate(ai_texts),
            regenerates=regen, edits=edits, votes_favor=fav, votes_defavor=defav,
            total_latency_ms=total_latency,
            length_slope=message_length_trajectory(user_texts),
            ended_reason="abandoned_mid_scene" if abandoned else "graceful")

    def run(self, n_sessions: int, arm: AssignmentArm,
            heavy_user_frac: float = 0.25) -> List[SessionSignals]:
        out = []
        for _ in range(n_sessions):
            heavy = self.rng.random() < heavy_user_frac
            variant = self._assign(arm, heavy)
            char = self.rng.choice(self.characters)
            out.append(self._session(variant, char, arm, heavy))
        return out
