"""The grade book — the unified artifact BOTH halves produce.

Pre-launch (content metrics on a test suite) and live (behavioural metrics on retrieved
traffic) emit the SAME shape, so one dashboard renders both and the two can be compared.

A Grade is never just a number. It carries -- in the data, not in a doc -- its role
(gate/guide), its interval, its provenance, its confounds, and WHAT IT CANNOT MEASURE.
The dashboard shows all of it, because a number without its uncertainty is a lie in this
system.

Design invariants enforced here, each bought with a finding:
  - a Grade tagged `pooled_language` raises: rho(en,zh) = -0.082, so no cross-language mean
  - a preference-derived Grade cannot carry axis=HARM: Cheng et al., preference is
    inadmissible on the harm path
  - effective_n is CONVERSATIONS; a Grade built from turns must say so
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Role(Enum):
    GATE = "gate"        # may block a ship
    GUIDE = "guide"      # informs a human; never blocks
    TRIPWIRE = "tripwire"
    TRAP = "trap"        # collect, never headline (votes, retention) -- research note 05


class Source(Enum):
    OFFLINE_CONTENT = "offline_content"    # judge-free metric on generated text
    OFFLINE_JUDGE = "offline_judge"        # pairwise judge
    LIVE_BEHAVIOR = "live_behavior"        # a retrieved production signal


class Axis(Enum):
    QUALITY = "quality"
    SAFETY_HARM = "safety_harm"            # preference is INADMISSIBLE here
    SAFETY_REFUSAL = "safety_refusal"


@dataclass
class Grade:
    dimension: str
    variant_id: str
    language: str                          # ALWAYS set; never "pooled"
    value: float
    role: Role
    source: Source
    axis: Axis = Axis.QUALITY
    interval: Optional[Tuple[float, float]] = None
    n_effective: int = 0                   # CONVERSATIONS, not turns
    n_unit: str = "conversations"
    segment: str = "all"                   # e.g. use-case cohort; "all" = un-segmented
    confounded: bool = False
    from_preference: bool = False          # regenerate/vote-derived
    caveats: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.language in ("pooled", "all", "*"):
            raise ValueError(
                f"Grade.language={self.language!r} -- language is a MEASUREMENT CONTEXT, not "
                f"a slice. rho(en,zh) = -0.082, so a pooled-language grade averages two "
                f"unrelated quantities. Emit one grade per language."
            )
        if self.from_preference and self.axis is Axis.SAFETY_HARM:
            raise ValueError(
                "a preference-derived grade cannot carry axis=SAFETY_HARM. Cheng et al. "
                "(Science, N=2,405): a single sycophantic interaction degrades conflict "
                "repair AND users rate the harmful condition higher. Preference answers "
                "'is it good?', never 'is it safe?'."
            )
        if self.n_unit == "turns":
            self.caveats.append(
                "n is TURNS: turns are autocorrelated repeated measures. Effective n is "
                "conversations (~60x smaller). This grade overstates its evidence."
            )

    def to_row(self) -> Dict[str, Any]:
        d = asdict(self)
        d["role"] = self.role.value
        d["source"] = self.source.value
        d["axis"] = self.axis.value
        return d


@dataclass
class GradeBook:
    """A versioned, self-describing bundle of grades. Feeds the dashboard as JSON."""
    title: str
    variant_ids: List[str]
    dataset_id: str
    evaluator_ids: List[str]
    created_iso: str                       # passed in from outside (scripts stamp it)
    grades: List[Grade] = field(default_factory=list)
    cannot_measure: List[str] = field(default_factory=list)

    def add(self, g: Grade) -> None:
        self.grades.append(g)

    # -- views the dashboard needs -------------------------------------------
    def languages(self) -> List[str]:
        return sorted({g.language for g in self.grades})

    def dimensions(self) -> List[str]:
        return sorted({g.dimension for g in self.grades})

    def gates(self) -> List[Grade]:
        return [g for g in self.grades if g.role is Role.GATE]

    def traps(self) -> List[Grade]:
        return [g for g in self.grades if g.role is Role.TRAP]

    def by_cell(self, dimension: str, language: str) -> List[Grade]:
        return [g for g in self.grades
                if g.dimension == dimension and g.language == language]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "variant_ids": self.variant_ids,
            "dataset_id": self.dataset_id,
            "evaluator_ids": self.evaluator_ids,
            "created_iso": self.created_iso,
            "languages": self.languages(),
            "dimensions": self.dimensions(),
            "cannot_measure": self.cannot_measure,
            "grades": [g.to_row() for g in self.grades],
            # A ledger the dashboard prints verbatim -- the platform's honesty is the product.
            "counts": {
                "gate": len(self.gates()),
                "guide": sum(1 for g in self.grades if g.role is Role.GUIDE),
                "trap": len(self.traps()),
                "total": len(self.grades),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
