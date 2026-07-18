"""Live behavioural signals: what we retrieve, and which ones are TRAPS.

The single most important distinction in the online half. From research note 05 (companion
products in practice), corroborated across a 307k-post grounded theory, a 318-post teen
study, and 413k donated messages:

  DIAGNOSTIC   points at a NAMED failure, hard to game. Safe to act on.
  TRAP         summarises approval. Collect it (storage is free) -- NEVER headline it,
               NEVER optimise it. This is not caution; it is the mechanism of two shipped
               disasters.

Why the traps are traps, with receipts:

  Chai got +30.3% D30 / +50.87% MCL from RLHF on pure continuation+retry labels.
  OpenAI added a thumbs-up signal to a reward; it "weakened the influence of our primary
  reward signal, which had been holding sycophancy in check" -- rollback in 4 days. THEIR
  A/B TESTS APPROVED OF IT. You cannot detect reward hacking with the metric being hacked.

So votes, retention, MCL, and time-to-next-session are TRAPS. Model SELECTION is worse than
a trap on the self-selected arm -- it is a CONFOUND: a model that attracts heavy roleplayers
looks better on every behavioural metric while being no better, and the difference is
unrecoverable unless the assignment was randomised.

The one signal that earns its keep: FOLLOW-UP QUESTION RATE. Best-validated in the corpus --
tracks wellbeing, degrades exactly for depressed/anxious/lonely users, and points AGAINST
engagement. It can dissent from the retention numbers, which is precisely why we need it.
"""
from __future__ import annotations
import re, statistics as st
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Sequence


class SignalClass(Enum):
    DIAGNOSTIC = "diagnostic"   # act on it
    TRAP = "trap"               # collect, never headline, never optimise
    CONFOUND = "confound"       # only interpretable on the randomised arm


@dataclass(frozen=True)
class SignalDef:
    name: str
    signal_class: SignalClass
    proxies_for: str
    gameable_by: str            # the model that would win by gaming it
    note: str = ""


# The catalogue. This IS the answer to "define more user behavior data points".
SIGNALS: Dict[str, SignalDef] = {
    "follow_up_question_rate": SignalDef(
        "follow_up_question_rate", SignalClass.DIAGNOSTIC,
        "conversational health; the model drawing the user out",
        "hard to game -- degrades for at-risk users, points against engagement",
        "THE headline diagnostic. It can dissent from retention."),
    "regenerate_rate": SignalDef(
        "regenerate_rate", SignalClass.DIAGNOSTIC,
        "dissatisfaction with a specific reply (= a pairwise 'B > A')",
        "a model producing addictive variance would win -- so it is a YARDSTICK, not a target",
        "each regenerate is free Q1 preference data; never optimise it"),
    "edit_rate": SignalDef(
        "edit_rate", SignalClass.DIAGNOSTIC,
        "the user repairing the persona by hand -- a drift leading indicator",
        "hard to game", ""),
    "abandonment_rate": SignalDef(
        "abandonment_rate", SignalClass.DIAGNOSTIC,
        "the user left mid-scene rather than said goodbye",
        "a clingy 'don't go!' bot lowers it while harming -- read with manipulation metrics",
        ""),
    "response_latency_ms": SignalDef(
        "response_latency_ms", SignalClass.DIAGNOSTIC,
        "serving health. +1s -> -3.01% MCL, so it CONTAMINATES every engagement metric",
        "not a quality signal -- a covariate to control for", ""),
    "session_depth": SignalDef(
        "session_depth", SignalClass.TRAP,
        "engagement", "the mechanism of the Chai result", "collect, never headline"),
    "vote_favor": SignalDef(
        "vote_favor", SignalClass.TRAP,
        "explicit approval (thumbs up)",
        "THE April-2025 sycophancy mechanism -- a thumbs-up in the reward broke sycophancy control",
        "collect, never optimise, never headline"),
    "vote_defavor": SignalDef(
        "vote_defavor", SignalClass.TRAP,
        "explicit disapproval (thumbs down)",
        "asymmetric with favor; still a trap", ""),
    "retention_d7": SignalDef(
        "retention_d7", SignalClass.TRAP,
        "return behaviour", "+30.3% D30 was ACHIEVED by engagement-hacking", ""),
    "model_selection": SignalDef(
        "model_selection", SignalClass.CONFOUND,
        "which variant the user chose when offered a choice",
        "self-selection contaminates every downstream metric -- a model that attracts heavy "
        "users looks better while being no better",
        "interpretable ONLY on the randomised-default arm"),
}


# ---------------------------------------------------------------- computed signals
_Q = re.compile(r"\?")

def follow_up_question_rate(ai_turns: Sequence[str]) -> float:
    """Fraction of model turns that ask the user a question. DIAGNOSTIC (the good one)."""
    if not ai_turns:
        return 0.0
    return sum(1 for t in ai_turns if _Q.search(t)) / len(ai_turns)


def message_length_trajectory(user_turns: Sequence[str]) -> Optional[float]:
    """Slope of user message length over the session. Falling = disengaging.

    Returns per-turn slope (chars/turn). None if too short. A DIAGNOSTIC, and one of the few
    that reads the USER rather than the model.
    """
    lens = [len(t) for t in user_turns]
    n = len(lens)
    if n < 4:
        return None
    xs = list(range(n))
    mx, my = st.mean(xs), st.mean(lens)
    denom = sum((x - mx) ** 2 for x in xs)
    return sum((xs[i] - mx) * (lens[i] - my) for i in range(n)) / denom if denom else None


@dataclass
class SessionSignals:
    """Everything we retrieve from one session. The row the pipeline stores."""
    conversation_id: str
    variant_id: str
    character_id: str
    language: str
    assignment_arm: str
    n_turns: int
    abandoned: bool
    follow_up_rate: float
    regenerates: int
    edits: int
    votes_favor: int
    votes_defavor: int
    total_latency_ms: float
    length_slope: Optional[float]
    ended_reason: str

    def as_diagnostics(self) -> Dict[str, float]:
        """Only the signals safe to grade on. Traps and confounds are excluded by design."""
        return {
            "follow_up_question_rate": self.follow_up_rate,
            "regenerate_rate": self.regenerates / max(1, self.n_turns),
            "edit_rate": self.edits / max(1, self.n_turns),
            "abandonment": 1.0 if self.abandoned else 0.0,
            "mean_latency_ms": self.total_latency_ms / max(1, self.n_turns),
        }

    def as_traps(self) -> Dict[str, float]:
        """Collected, reportable ONLY behind a 'do not optimise' label."""
        return {
            "session_depth": float(self.n_turns),
            "vote_favor": float(self.votes_favor),
            "vote_defavor": float(self.votes_defavor),
        }
