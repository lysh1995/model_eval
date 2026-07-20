"""Content-addressed identity. Constraint C1 lives here.

Every score must trace to (variant, evaluator, data). No standard gives us this:
OpenTelemetry's gen_ai.evaluation.result has six attributes and NONE identifies the
evaluator that produced the score. So we build it.

Rules enforced here, each bought with a research finding:
  1. variant_id hashes system_prompt BYTES, not a name. A variant IS a prompt.
  2. simulator_id is first-class -- the user simulator is part of the instrument,
     and must be card_blind (note 21: the dataset's simulator probably was not).
  3. A judge bump is a breaking change. rebaseline_required() refuses to rescale.
  4. inclusion_prob is lineage, not telemetry -- without it sampled estimates are
     silently biased.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


def _h(*parts: Any) -> str:
    b = json.dumps(parts, sort_keys=True, ensure_ascii=False, default=str).encode()
    return hashlib.sha256(b).hexdigest()[:16]


@dataclass(frozen=True)
class Variant:
    """model + params + system prompt + anchoring policy. THE unit under test."""
    model: str
    params: Dict[str, Any]
    system_prompt: str
    anchoring_policy: str = "once_at_start"   # a first-class parameter (MT-Eval: the
                                              # causal variable is distance-to-anchor)
    label: str = ""

    @property
    def id(self) -> str:
        # system_prompt BYTES, not a name: a renamed prompt is a new variant
        return "v_" + _h(self.model, self.params, self.system_prompt, self.anchoring_policy)


@dataclass(frozen=True)
class Evaluator:
    """A judge, pinned. Never a floating alias -- GPT-4 went 84%->51.4% in 3 months."""
    model_snapshot: str
    prompt_hash: str
    rubric_version: str
    decoding: Dict[str, Any]
    seed: Optional[int] = None

    @property
    def id(self) -> str:
        return "e_" + _h(self.model_snapshot, self.prompt_hash, self.rubric_version,
                         self.decoding, self.seed)


@dataclass(frozen=True)
class Simulator:
    """The user simulator is PART OF THE MEASURING INSTRUMENT, not a fixture.

    card_blind must be True. Note 21 found the dataset's simulator probably saw the
    character card (own-card term leak 1.59x/1.48x over a topic-matched control,
    p<0.0001) -- which makes it a COLLABORATOR, not a user. Collaborators do not probe
    the seams, so they systematically UNDER-detect drift.
    """
    kind: str                      # "replay" | "live"
    source: str                    # corpus id, or a model snapshot
    card_blind: bool = True

    def __post_init__(self):
        if not self.card_blind:
            raise ValueError(
                "A card-aware simulator is a collaborator, not a user. It under-detects "
                "drift and quietly destroys every consistency metric. If you genuinely "
                "need this, construct with card_blind=True and document why."
            )

    @property
    def id(self) -> str:
        return "s_" + _h(self.kind, self.source, self.card_blind)


@dataclass(frozen=True)
class Dataset:
    name: str
    content_hash: str
    n_characters: int
    languages: tuple

    @property
    def id(self) -> str:
        return "d_" + _h(self.name, self.content_hash)


@dataclass
class Provenance:
    """Stamped on every score row. This IS constraint C1."""
    variant_id: str
    dataset_id: str
    simulator_id: str
    metric_name: str
    metric_version: str
    evaluator_id: Optional[str] = None      # None for judge-free lanes
    inclusion_prob: float = 1.0             # pi_i -- LINEAGE. Unweighted => biased.
    provenance: str = "human-authored"      # human-authored | mined | synthetic
    code_ref: str = ""

    def to_row(self) -> Dict[str, Any]:
        return asdict(self)


class RebaselineRequired(Exception):
    """Raised when someone tries to compare across evaluator versions."""


def assert_comparable(a: Provenance, b: Provenance) -> None:
    """A judge bump is a BREAKING CHANGE. The system refuses to silently rescale.

    This is the concrete form of constraint C1 -- and the reason it is a hard error
    rather than a warning is that the alternative (a quiet rescale) produces a number
    that looks exactly like a valid one.
    """
    if a.metric_name != b.metric_name:
        raise ValueError(f"different metrics: {a.metric_name} vs {b.metric_name}")
    if a.evaluator_id != b.evaluator_id:
        raise RebaselineRequired(
            f"evaluator changed ({a.evaluator_id} -> {b.evaluator_id}). Old scores are "
            f"NOT comparable to new ones and will not be rescaled. Dual-run the frozen "
            f"calibration set and re-baseline."
        )
    if a.metric_version != b.metric_version:
        raise RebaselineRequired(
            f"metric version changed ({a.metric_version} -> {b.metric_version}). "
            f"Re-run the baseline."
        )
