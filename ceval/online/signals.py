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
    MONITOR = "monitor"         # collect + watch for drift, but NEVER a grade/target (note 05 Tier 2)
    TRAP = "trap"               # collect, never headline, never optimise
    CONFOUND = "confound"       # only interpretable on the randomised arm


class FeedbackKind(Enum):
    """How the user's opinion reaches us. The online half's whole job is to estimate that opinion
    from BOTH kinds — but they are not equally trustworthy (see below)."""
    DIRECT = "direct"       # the user explicitly signals: vote, rating, regenerate, edit
    INDIRECT = "indirect"   # inferred from behaviour: follow-up, abandonment, message-length decay
    SYSTEM = "system"       # not the user's opinion at all — a covariate to control for (latency)


@dataclass(frozen=True)
class SignalDef:
    name: str
    signal_class: SignalClass
    feedback: FeedbackKind
    proxies_for: str
    gameable_by: str            # the model that would win by gaming it
    note: str = ""


# The catalogue: each user-behaviour data point, tagged by (1) how the feedback reaches us
# — DIRECT (explicit) vs INDIRECT (implicit) — and (2) whether it is safe to act on.
#
# The load-bearing asymmetry, and the reason "just aggregate the votes" is wrong:
#   DIRECT APPROVAL (vote_favor) is a TRAP. Optimising explicit thumbs-up is precisely the
#   Chai / OpenAI-April-2025 mechanism — their A/B tests approved the sycophantic model.
#   DIRECT REJECTION (regenerate, edit) is far more trustworthy: the user actively fixing/redoing
#   a reply is hard to fake and points at a real defect.
#   INDIRECT HEALTH (follow-up, non-decaying engagement) can DISSENT from approval — which is
#   exactly why we infer the user's opinion from these, not from the votes.
SIGNALS: Dict[str, SignalDef] = {
    "story_cocreation": SignalDef(
        "story_cocreation", SignalClass.DIAGNOSTIC, FeedbackKind.INDIRECT,
        "STORYTELLING-CRAFT proxy -- does the user get pulled into co-creating the story "
        "(introducing entities, taking in-fiction actions, growing investment)",
        "hard to game by sycophancy: a people-pleaser earns votes but LOW co-creation. Must be "
        "VALIDATED against the offline judge craft (the anchor) and pass the acid test",
        "the online read of the headline narrative_craft. A PROXY, not the truth -- the judge on "
        "a ~1% sample anchors it. Offline REPLAY freezes the user half, so it needs real traffic."),
    "follow_up_question_rate": SignalDef(
        "follow_up_question_rate", SignalClass.DIAGNOSTIC, FeedbackKind.INDIRECT,
        "conversational health; the model drawing the user out",
        "hard to game -- degrades for at-risk users, points against engagement",
        "THE headline diagnostic. It can dissent from retention."),
    "regenerate_rate": SignalDef(
        "regenerate_rate", SignalClass.DIAGNOSTIC, FeedbackKind.DIRECT,
        "direct REJECTION of a specific reply (= a pairwise 'B > A')",
        "a model producing addictive variance would win -- so it is a YARDSTICK, not a target",
        "explicit dissatisfaction; free Q1 preference data. Never optimise it."),
    "edit_rate": SignalDef(
        "edit_rate", SignalClass.DIAGNOSTIC, FeedbackKind.DIRECT,
        "direct CORRECTION -- the user repairing the persona by hand (a drift leading indicator)",
        "hard to game", "explicit dissatisfaction, harder to fake than a vote."),
    "abandonment_rate": SignalDef(
        "abandonment_rate", SignalClass.MONITOR, FeedbackKind.INDIRECT,
        "the user left mid-scene rather than said goodbye",
        "a clingy 'don't go!' bot LOWERS it while harming -- low abandonment can be the gaming",
        "note 05 Tier 2: monitor for drift, do NOT reward low abandonment as satisfaction."),
    "response_latency_ms": SignalDef(
        "response_latency_ms", SignalClass.DIAGNOSTIC, FeedbackKind.SYSTEM,
        "serving health. +1s -> -3.01% MCL, so it CONTAMINATES every engagement metric",
        "not a quality signal -- a covariate to control for", ""),
    "session_depth": SignalDef(
        "session_depth", SignalClass.TRAP, FeedbackKind.INDIRECT,
        "engagement", "the mechanism of the Chai result", "collect, never headline"),
    "vote_favor": SignalDef(
        "vote_favor", SignalClass.TRAP, FeedbackKind.DIRECT,
        "direct APPROVAL (thumbs up)",
        "THE April-2025 sycophancy mechanism -- a thumbs-up in the reward broke sycophancy control",
        "the trap. Approval feedback ranks the sycophant first; collect, never optimise/headline."),
    "vote_defavor": SignalDef(
        "vote_defavor", SignalClass.TRAP, FeedbackKind.DIRECT,
        "direct disapproval (thumbs down)",
        "asymmetric with favor; still a trap", ""),
    "retention_d7": SignalDef(
        "retention_d7", SignalClass.TRAP, FeedbackKind.INDIRECT,
        "return behaviour", "+30.3% D30 was ACHIEVED by engagement-hacking", ""),
    "model_selection": SignalDef(
        "model_selection", SignalClass.CONFOUND, FeedbackKind.INDIRECT,
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
    user_cocreation: float = 0.0    # STORYTELLING-CRAFT proxy: did the user co-create the story?

    def as_diagnostics(self) -> Dict[str, float]:
        """Only the signals safe to grade on. Traps and confounds are excluded by design."""
        return {
            "story_cocreation": self.user_cocreation,     # the storytelling-craft proxy
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
