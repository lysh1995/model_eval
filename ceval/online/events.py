"""The collection contract. R7: there is no app behind this, so we specify what it emits.

No existing standard is sufficient, and that is a finding rather than NIH. OpenTelemetry's
`gen_ai.evaluation.result` carries exactly SIX attributes -- evaluation.name, score.value,
score.label, explanation, response.id, error.type -- and NOT ONE identifies the evaluator
that produced the score. The spec concedes evaluation semantics are evaluator-dependent and
then provides no field for the evaluator. That is constraint C1, unmet by the standard.

So: adopt `gen_ai.*` where it exists, add `eval.*` for what nothing carries.

Two field choices are load-bearing and easy to get wrong:

  finish_reason  A REFUSAL IS A MISSING OBSERVATION, NOT A ZERO. Scoring a refusal as 0
                 silently averages a non-answer into a quality mean -- which is exactly how
                 over-refusal disappears from a dashboard.

  assignment_arm Costs nothing, and CANNOT BE RECONSTRUCTED LATER. If users self-select
                 their model, quality differences are contaminated by who chose it. Only the
                 randomised arm supports a causal claim.
"""
from __future__ import annotations
import json, time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class FinishReason(Enum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"    # NOT a zero. A missing observation.
    ERROR = "error"

    @property
    def is_observation(self) -> bool:
        """Did the model actually answer? If not, the score is MISSING, not bad."""
        return self in (FinishReason.STOP, FinishReason.LENGTH)


class AssignmentArm(Enum):
    RANDOMIZED_DEFAULT = "randomized_default"   # supports causal claims
    SELF_SELECTED = "self_selected"             # confounded by who chose it
    UNKNOWN = "unknown"                         # the field was not wired. Unrecoverable.


class DiegeticStatus(Enum):
    """FactScore explicitly disclaims deceptive text -- but FICTION IS DECEPTION.

    Characters lie, scheme, conceal. Without this distinction, contradiction precision is
    WORST ON THE BEST WRITING: a well-written liar looks exactly like an inconsistent model.
    """
    AUTHOR_ASSERTS = "author_asserts"       # the narration says X. Contradicting it is a bug.
    CHARACTER_CLAIMS = "character_claims"   # the character says X. They may be lying.
    OUT_OF_CHARACTER = "out_of_character"   # the user/model stepped outside the fiction
    UNKNOWN = "unknown"


@dataclass
class GenerationEvent:
    """One served turn. The atom of the online half."""
    # --- gen_ai.* : adopt the standard where it exists
    response_model: str                 # gen_ai.response.model -- what SERVED, not what was asked
    conversation_id: str                # gen_ai.conversation.id
    finish_reason: FinishReason
    input_tokens: int
    output_tokens: int

    # --- eval.* : ours, because no standard carries it
    variant_id: str                     # H(model, params, system_prompt_BYTES, anchoring_policy)
    character_id: str
    language: str
    turn_index: int
    distance_to_anchor: int             # THE causal variable. OTel offers only a boolean.
    latency_ms: float
    assignment_arm: AssignmentArm = AssignmentArm.UNKNOWN
    diegetic_status: DiegeticStatus = DiegeticStatus.UNKNOWN
    inclusion_prob: float = 1.0         # pi_i -- LINEAGE. Unweighted => silently biased.
    provenance: str = "production"
    evaluator_id: Optional[str] = None  # None for judge-free lanes
    lane0_verdicts: List[str] = field(default_factory=list)
    text: str = ""
    ts: float = field(default_factory=time.time)

    @property
    def cell(self) -> tuple:
        """The sampling/reporting cell. Language is ABOVE the aggregation line."""
        return (self.variant_id, self.language, self.character_id)

    def to_row(self) -> Dict[str, Any]:
        d = asdict(self)
        for k in ("finish_reason", "assignment_arm", "diegetic_status"):
            d[k] = getattr(self, k).value
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_row(), ensure_ascii=False)


class RefusalIsNotZero(Exception):
    pass


def score_or_missing(ev: GenerationEvent, score: float) -> Optional[float]:
    """Gate every score through this. A non-observation returns None, never 0.0.

    The alternative -- averaging a content_filter as 0.0 -- is how a model that refuses
    everything scores 'poor quality' instead of 'refused', and how over-refusal vanishes
    into a quality mean where nobody looks for it.
    """
    if not ev.finish_reason.is_observation:
        return None
    return score


@dataclass
class SessionEvent:
    """Session lifecycle. NO standard models a session -- gen_ai.conversation.id is a bare
    label the spec forbids you to synthesise. So we build the entity."""
    conversation_id: str
    variant_id: str
    character_id: str
    language: str
    user_id_hash: str
    started_ts: float
    ended_ts: Optional[float] = None
    end_reason: str = ""            # graceful | abandoned_mid_scene | timeout | blocked
    assignment_arm: AssignmentArm = AssignmentArm.UNKNOWN

    @property
    def duration_s(self) -> Optional[float]:
        return (self.ended_ts - self.started_ts) if self.ended_ts else None


REQUIRED_FIELDS = (
    "response_model", "conversation_id", "finish_reason", "variant_id", "character_id",
    "language", "turn_index", "distance_to_anchor", "inclusion_prob",
)


def validate(ev: GenerationEvent) -> List[str]:
    """Contract check. Returns problems; empty means the event is evaluable."""
    problems = []
    for f in REQUIRED_FIELDS:
        if getattr(ev, f, None) in (None, ""):
            problems.append(f"missing required field: {f}")
    if ev.assignment_arm is AssignmentArm.UNKNOWN:
        problems.append(
            "assignment_arm=UNKNOWN: this field costs nothing and CANNOT be reconstructed "
            "later. Without it, no online comparison supports a causal claim"
        )
    if not 0 < ev.inclusion_prob <= 1:
        problems.append(f"inclusion_prob={ev.inclusion_prob} outside (0,1]: sampled "
                        f"estimates will be unweighted and biased")
    return problems
