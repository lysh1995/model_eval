"""THE INJECTION POINTS. This is the entire API the product has to call.

R7: there is no app behind this, so we specify what it emits. If this API is awkward, it
does not get called, and then nothing downstream exists. So it is four methods and they are
all one line at the call site.

    collector = Collector(variant_id=..., sink=...)

    with collector.session(conversation_id, character_id, language, user_id) as s:
        s.turn(text=reply, finish_reason=..., distance_to_anchor=..., latency_ms=...)
        s.regenerate(turn_index)      # <- free pairwise preference. The product's gift.
        s.edit(turn_index)
    # session end reason is inferred; abandonment is the interesting one

Design rules, each bought with a finding:

  1. Tier 0 runs INLINE, inside .turn(), and BLOCKS. Latency (not cost) forces this: a judge
     is 1,000-3,200ms against a ~200ms guardrail budget, so even a free judge is 5-16x too
     slow. A classifier is 5-50ms and fits.
  2. Escalation is a CONSTRUCTOR ARGUMENT, not a setting. Raine: 377 flags, 23 over 90%
     confidence, and nothing happened. You cannot build a Collector that detects without a
     human on the other end.
  3. .regenerate() is not telemetry -- it is the QUALITY MEASUREMENT. Every regenerate is a
     real user, on a character they chose, in real emotional context, saying "B > A". ~5M
     free pairwise labels/day at 50M/day and a 10% regen rate, in exactly the format the
     judge design consumes.
  4. assignment_arm is required at session start. It costs nothing and CANNOT be
     reconstructed later.
"""
from __future__ import annotations
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterator, List, Optional

from .events import (GenerationEvent, SessionEvent, FinishReason, AssignmentArm,
                     DiegeticStatus, validate)


class Tier0Blocked(Exception):
    """Raised inline when a hard gate fires. The product must handle it."""
    def __init__(self, verdicts: List[str]):
        self.verdicts = verdicts
        super().__init__(f"blocked by Tier 0: {verdicts}")


@dataclass
class PreferencePair:
    """A regenerate. THE product question (Q1), not a proxy for it.

    Boundary, and it is hard: preference is INADMISSIBLE on the harm path. Cheng et al.
    (Science, N=2,405): a single sycophantic interaction degrades conflict repair, and users
    rate the harmful condition HIGHER. This answers 'is it good?', never 'is it safe?'.
    """
    conversation_id: str
    variant_id: str
    character_id: str
    language: str
    turn_index: int
    rejected: str
    accepted: str
    ts: float = field(default_factory=time.time)


class SessionHandle:
    """What the product holds for the duration of one conversation."""

    def __init__(self, collector: "Collector", ev: SessionEvent):
        self._c = collector
        self._ev = ev
        self._turn_index = 0
        self._last_text: Dict[int, str] = {}
        self.saw_user_turn = False

    # ---- INJECTION POINT 1: every served turn -------------------------------
    def turn(self, text: str, *, finish_reason: FinishReason = FinishReason.STOP,
             distance_to_anchor: int = 0, latency_ms: float = 0.0,
             input_tokens: int = 0, output_tokens: int = 0,
             diegetic_status: DiegeticStatus = DiegeticStatus.CHARACTER_CLAIMS) -> GenerationEvent:
        idx = self._turn_index
        self._turn_index += 1
        ev = GenerationEvent(
            response_model=self._c.response_model,
            conversation_id=self._ev.conversation_id,
            finish_reason=finish_reason,
            input_tokens=input_tokens, output_tokens=output_tokens,
            variant_id=self._ev.variant_id, character_id=self._ev.character_id,
            language=self._ev.language, turn_index=idx,
            distance_to_anchor=distance_to_anchor, latency_ms=latency_ms,
            assignment_arm=self._ev.assignment_arm, diegetic_status=diegetic_status,
            inclusion_prob=self._c.inclusion_prob, text=text,
        )
        # Tier 0 -- inline, blocking, 5-50ms. Runs BEFORE the event is emitted.
        verdicts = self._c._tier0(ev)
        ev.lane0_verdicts = verdicts
        self._c._emit(ev)
        if any(v.startswith("BLOCK:") for v in verdicts):
            raise Tier0Blocked(verdicts)
        self._last_text[idx] = text
        return ev

    # ---- INJECTION POINT 2: the user said something -------------------------
    def user_turn(self, text: str) -> None:
        """Crisis detection reads the USER's state, not the character's. A character saying
        'I will end my life before I kneel' is acting; a user saying it is not."""
        self.saw_user_turn = True
        self._c._scan_user(text, self._ev)

    # ---- INJECTION POINT 3: regenerate = a free pairwise label --------------
    def regenerate(self, turn_index: int, new_text: str) -> PreferencePair:
        old = self._last_text.get(turn_index, "")
        self._last_text[turn_index] = new_text
        p = PreferencePair(self._ev.conversation_id, self._ev.variant_id,
                           self._ev.character_id, self._ev.language,
                           turn_index, rejected=old, accepted=new_text)
        self._c.preferences.append(p)
        return p

    # ---- INJECTION POINT 4: the user repaired the persona by hand -----------
    def edit(self, turn_index: int, edited_text: str) -> None:
        self._c.edits.append((self._ev.conversation_id, turn_index, edited_text))


class Collector:
    """The product's single dependency. Four hooks, one constructor."""

    def __init__(self, *, variant_id: str, response_model: str,
                 sink: Callable[[GenerationEvent], None],
                 escalate: Callable[[str, SessionEvent], None],
                 tier0: Optional[Callable[[GenerationEvent], List[str]]] = None,
                 crisis_scan: Optional[Callable[[str], List[str]]] = None,
                 inclusion_prob: float = 1.0):
        if escalate is None:
            raise ValueError(
                "Collector requires an `escalate` sink. Detection without escalation is "
                "worse than no detection -- in Raine the classifier fired 377 times, 23 of "
                "them above 90% confidence, and nothing happened. That log became the "
                "plaintiff's exhibit."
            )
        self.variant_id = variant_id
        self.response_model = response_model
        self._sink = sink
        self._escalate = escalate
        self._tier0_fn = tier0 or (lambda ev: [])
        self._crisis_fn = crisis_scan or (lambda text: [])
        self.inclusion_prob = inclusion_prob
        self.preferences: List[PreferencePair] = []
        self.edits: List[tuple] = []
        self.sessions: List[SessionEvent] = []
        self.contract_problems: List[str] = []

    # ---- INJECTION POINT 0: session lifecycle -------------------------------
    @contextmanager
    def session(self, conversation_id: str, character_id: str, language: str,
                user_id_hash: str, *, assignment_arm: AssignmentArm) -> Iterator[SessionHandle]:
        ev = SessionEvent(conversation_id, self.variant_id, character_id, language,
                          user_id_hash, started_ts=time.time(), assignment_arm=assignment_arm)
        self.sessions.append(ev)
        h = SessionHandle(self, ev)
        try:
            yield h
            ev.end_reason = "graceful"
        except Tier0Blocked:
            ev.end_reason = "blocked"
            raise
        except GeneratorExit:
            ev.end_reason = "abandoned_mid_scene"
            raise
        finally:
            ev.ended_ts = time.time()
            if not ev.end_reason:
                # The interesting one: the user stopped mid-scene. Not a graceful goodbye.
                ev.end_reason = "abandoned_mid_scene"

    # ---- internals ----------------------------------------------------------
    def _tier0(self, ev: GenerationEvent) -> List[str]:
        return self._tier0_fn(ev)

    def _emit(self, ev: GenerationEvent) -> None:
        problems = validate(ev)
        if problems:
            self.contract_problems.extend(problems)
        self._sink(ev)

    def _scan_user(self, text: str, sev: SessionEvent) -> None:
        for signal in self._crisis_fn(text):
            self._escalate(signal, sev)     # a HUMAN, not a counter

    def stats(self) -> Dict[str, float]:
        return {
            "sessions": len(self.sessions),
            "preference_pairs": len(self.preferences),
            "edits": len(self.edits),
            "abandoned": sum(1 for s in self.sessions
                             if s.end_reason == "abandoned_mid_scene"),
            "contract_problems": len(self.contract_problems),
        }
