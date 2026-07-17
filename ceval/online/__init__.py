"""The online half. R3/R7/R11.

The collection contract (no standard carries evaluator identity), the session assembler
(if it stores a mean, the platform is wrong by design), and the injection points -- four
hooks the product calls, with Tier 0 inline and escalation as a constructor argument.
"""
from .events import (GenerationEvent, SessionEvent, FinishReason, AssignmentArm,
                     DiegeticStatus, validate, score_or_missing)
from .session import Session, SessionAssembler, TurnScore
from .collector import Collector, SessionHandle, PreferencePair, Tier0Blocked
