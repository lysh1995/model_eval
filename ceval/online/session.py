"""The session assembler. No standard models a session, so we build the entity.

ONE RULE decides this file:

    If it stores a mean, the platform is wrong by design.

MT-Bench-101 measured it: min-over-turns beats mean-over-turns by TWELVE POINTS of human
agreement (87% vs 75%), and min-aggregation of a GPT-4 judge exceeds human experts' own
internal agreement. Their justification is ours verbatim: "a single failed response can
compromise the entire dialogue."

A mean LAUNDERS the one catastrophic turn that actually ended the session. So the session
stores `min_turn_score` and `first_failure_turn_idx` -- a score AND a location, because a
number you cannot navigate to is not actionable.

Second rule: the CONVERSATION is the sampling unit; the turn is a repeated measure. Turns
within a dialogue are autocorrelated -- 42% of turn-level findings are spurious without this.
`effective_n` returns conversations. It is a method, not a field, so nobody can accidentally
sum turns into it.
"""
from __future__ import annotations
import collections, statistics as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from .events import GenerationEvent, SessionEvent, FinishReason, score_or_missing


@dataclass
class TurnScore:
    turn_index: int
    metric: str
    value: Optional[float]      # None = MISSING (a refusal), never 0.0
    distance_to_anchor: int


@dataclass
class Session:
    """A conversation, assembled. The unit of analysis."""
    conversation_id: str
    variant_id: str
    character_id: str
    language: str
    turns: List[GenerationEvent] = field(default_factory=list)
    scores: Dict[str, List[TurnScore]] = field(default_factory=lambda: collections.defaultdict(list))
    end_reason: str = ""

    # -- the two fields that matter -------------------------------------------
    def min_turn_score(self, metric: str, lower_is_better: bool = True) -> Optional[float]:
        """The WORST turn. Not the mean. See the module docstring."""
        vals = [s.value for s in self.scores.get(metric, ()) if s.value is not None]
        if not vals:
            return None
        return max(vals) if lower_is_better else min(vals)

    def first_failure_turn_idx(self, metric: str, threshold: float,
                               lower_is_better: bool = True) -> Optional[int]:
        """WHERE it broke. Turns a score into a place to look."""
        for s in sorted(self.scores.get(metric, ()), key=lambda x: x.turn_index):
            if s.value is None:
                continue
            bad = s.value > threshold if lower_is_better else s.value < threshold
            if bad:
                return s.turn_index
        return None

    # -- deliberately absent ---------------------------------------------------
    def mean_turn_score(self, *_a, **_k):
        raise NotImplementedError(
            "Session does not expose a mean over turns. min beats mean by 12 points of "
            "human agreement (87% vs 75%) because a mean launders the one catastrophic turn "
            "that ended the session. Use min_turn_score() and first_failure_turn_idx(). "
            "If you need a distribution, ask for percentiles explicitly."
        )

    def percentile_turn_score(self, metric: str, p: float) -> Optional[float]:
        """Explicit percentiles are fine -- what is banned is the SILENT mean."""
        vals = sorted(s.value for s in self.scores.get(metric, ()) if s.value is not None)
        if not vals:
            return None
        k = min(len(vals) - 1, int(p * len(vals)))
        return vals[k]

    def missing_rate(self, metric: str) -> float:
        """Fraction of turns with no observation (refusals). NOT a quality score."""
        ss = self.scores.get(metric, ())
        return sum(1 for s in ss if s.value is None) / len(ss) if ss else 0.0

    @property
    def cell(self) -> Tuple[str, str, str]:
        return (self.variant_id, self.language, self.character_id)

    @property
    def inclusion_prob(self) -> float:
        return self.turns[0].inclusion_prob if self.turns else 1.0


class SessionAssembler:
    """Turn a stream of GenerationEvents into Sessions.

    Sampling happens at the SESSION level, not the generation level: boundary erosion,
    dependency and drift are TRAJECTORY properties. A per-generation sampler draws turn #47
    blind to turns #1-46 and is structurally blind to our worst failure modes.
    """

    def __init__(self):
        self._open: Dict[str, Session] = {}
        self.completed: List[Session] = []

    def add(self, ev: GenerationEvent) -> None:
        s = self._open.get(ev.conversation_id)
        if s is None:
            s = Session(ev.conversation_id, ev.variant_id, ev.character_id, ev.language)
            self._open[ev.conversation_id] = s
        s.turns.append(ev)

    def score(self, conversation_id: str, metric: str, values: Dict[int, float]) -> None:
        s = self._open.get(conversation_id)
        if not s:
            return
        for ev in s.turns:
            v = score_or_missing(ev, values.get(ev.turn_index, 0.0))   # None if refused
            s.scores[metric].append(TurnScore(ev.turn_index, metric, v, ev.distance_to_anchor))

    def close(self, conversation_id: str, end_reason: str = "graceful") -> Optional[Session]:
        s = self._open.pop(conversation_id, None)
        if s:
            s.end_reason = end_reason
            self.completed.append(s)
        return s

    # -- the correction that stops a 60x overstatement -------------------------
    def effective_n(self) -> int:
        """CONVERSATIONS, not turns.

        Our corpus: ~95 characters, NOT 313,500 turns. Displaying turn-pooled n overstates
        the evidence 60x and is the single most likely way this platform lies to someone.
        A method, not a field, so it cannot be accidentally summed.
        """
        return len(self.completed)

    def turn_count(self) -> int:
        """Available, but NEVER a sample size. Named so that misuse is visible in review."""
        return sum(len(s.turns) for s in self.completed)
