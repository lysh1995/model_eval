"""Safety lane. R5: 'quality and safety at minimum' -- the brief's own words.

Three axes, never one: capability (uplift), user state (crisis/dependency), third party.
Two structural rules, both bought with an incident:
  - detection MUST be wired to escalation (Raine: 377 flags, nothing happened)
  - harm and over-refusal are never averaged (their mean is a refusal-maximiser)
"""
from .regurgitation import PIIInOutput, CardParroting, CrossModelConvergence, PII_RULES
from .crisis import (CrisisPipeline, LexiconDetector, PostReferralTrajectory, Severity,
                     EscalationNotWired, EscalationEvent, raise_sink)
from .refusal import (OverRefusal, RefusalDetector, RefusalKind, HarmAxis,
                      SafetyFrontier, report_frontier)
