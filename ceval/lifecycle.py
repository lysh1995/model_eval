"""The end-to-end flow. R1 + R2 + R11: create -> dry-run -> gate -> ship -> monitor -> loop.

    Variant ──> DryRun ──fail fast, free──> reject
              └─> Benchmark ──> ShipDecision ──> Live(Collector) ──> Curation ──> Benchmark
                                                                                     ^
                                                                                     └ accumulates,
                                                                                       never replaces

Two stages are deliberately NOT here:

  SHADOW as a quality gate. It cannot work: the candidate's turn-2 is conditioned on the
  INCUMBENT's turn-1, so by turn 3 you are scoring a conversation the candidate would never
  have produced. The industry pattern is borrowed from single-turn RAG and does not transfer.
  Shadow survives only as a turn-1 smoke test.

  A TRAINING LOOP. Findings feed humans, not a reward model. RLUF is the precedent: the only
  published offline<->online correlation (r=0.95) was achieved by training the evaluator on
  1M production labels -- and optimising it +28% produced a model that ends conversations
  early to farm the signal. The correlation and the pathology are the same property.
"""
from __future__ import annotations
import statistics as st
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple

from .registry import Variant, Dataset, Simulator, Provenance
from .metrics.base import Metric, Role, MetricResult
from .stats import variance_components, shrink, compare, Comparison, VarianceComponents


class Stage(Enum):
    DRAFT = "draft"
    DRY_RUN = "dry_run"
    BENCHMARK = "benchmark"
    SHIP_REVIEW = "ship_review"
    CANARY = "canary"
    LIVE = "live"
    REJECTED = "rejected"


@dataclass
class DryRunResult:
    """A FILTER, not a measurement. Deliberately underpowered.

    Catches the 90% of bad variants that don't deserve a judge: violates its own length cap,
    loops, leaks assistant-voice. It must never emit a ship recommendation -- it is a smoke
    test on a stratified subset and it knows it.
    """
    passed: bool
    autofails: List[str] = field(default_factory=list)
    n_dialogues: int = 0

    def verdict(self) -> str:
        if self.passed:
            return f"PROMOTE to benchmark ({self.n_dialogues} dialogues, no autofail)"
        return f"REJECT before spending a cent on judging: {'; '.join(self.autofails)}"


@dataclass
class SliceFinding:
    key: Tuple[str, str]
    shrunk: float
    ci: Tuple[float, float]
    pulled_pct: float


@dataclass
class ShipDecision:
    """R2: a recommendation backed by evidence. NOT a number.

    States: the delta, its interval, THE MDE, which slices moved after shrinkage, what
    abstained, and WHAT IT COULD NOT MEASURE. The last one is not a footnote -- 'no
    regression' is meaningless without the detectable effect.
    """
    candidate: str
    baseline: str
    language: str
    comparisons: Dict[str, Comparison]
    variance: Dict[str, VarianceComponents]
    slices: List[SliceFinding]
    safety_blocks: List[str]
    cannot_measure: List[str]
    human_veto: Optional[str] = None

    @property
    def blocked(self) -> bool:
        return bool(self.safety_blocks) or self.human_veto is not None

    @property
    def any_detectable_regression(self) -> bool:
        return any(c.detectable and c.delta > 0 for c in self.comparisons.values())

    def recommendation(self) -> str:
        if self.human_veto:
            return f"NO-SHIP — human veto: {self.human_veto}"
        if self.safety_blocks:
            return f"NO-SHIP — safety: {'; '.join(self.safety_blocks)}"
        if self.any_detectable_regression:
            return "NO-SHIP — a detectable regression on a gate metric"
        return "SHIP — no detectable regression on any gate metric"

    def render(self) -> str:
        L = ["─" * 78,
             f"SHIP DECISION — {self.candidate}  vs  {self.baseline}   [{self.language}]",
             "─" * 78, "", f"  {self.recommendation()}", ""]
        L.append("  EVIDENCE")
        for name, c in self.comparisons.items():
            L.append(f"    {name:22s} {c.verdict()}")
            L.append(f"    {'':22s} effective n = {c.n_effective} conversations "
                     f"(NOT turns — turns are repeated measures)")
        if self.slices:
            L += ["", "  SLICES THAT MOVED (shrunk; raw cells are noise amplifiers)"]
            for s in self.slices[:5]:
                L.append(f"    {s.key[1]:24s} {s.shrunk:.4f} "
                         f"[{s.ci[0]:.4f},{s.ci[1]:.4f}]  pulled {s.pulled_pct:.0f}% to the mean")
            L.append("    (informational only — slices never block; BH q=0.10)")
        L += ["", "  WHAT THIS COULD NOT MEASURE"]
        for c in self.cannot_measure:
            L.append(f"    · {c}")
        L += ["", "  A qualitative signal may block this ship with no statistical",
              "  justification. OpenAI's April 2025 rollback happened BECAUSE the A/B",
              "  tests approved the model and expert dissent was overruled.", ""]
        return "\n".join(L)


class Lifecycle:
    """Orchestrates the flow. Each stage is independently testable and swappable."""

    def __init__(self, dataset: Dataset, simulator: Simulator):
        self.dataset, self.simulator = dataset, simulator
        self.stage: Dict[str, Stage] = {}

    # ---- stage 1: dry-run --------------------------------------------------
    def dry_run(self, variant: Variant, dialogues: Dict[str, list],
                autofail_checks: List[Tuple[str, Callable[[Dict[str, list]], bool]]]
                ) -> DryRunResult:
        self.stage[variant.id] = Stage.DRY_RUN
        fails = [name for name, check in autofail_checks if check(dialogues)]
        r = DryRunResult(passed=not fails, autofails=fails, n_dialogues=len(dialogues))
        if not r.passed:
            self.stage[variant.id] = Stage.REJECTED
        return r

    # ---- stage 2: benchmark ------------------------------------------------
    def benchmark(self, cells: Dict[Tuple[str, str], List[float]],
                  metric: Metric) -> Tuple[VarianceComponents, Dict]:
        vc = variance_components(cells)
        return vc, shrink(cells, vc)

    # ---- stage 3: the decision ---------------------------------------------
    def decide(self, candidate: str, baseline: str, language: str,
               cells_by_metric: Dict[str, Dict[Tuple[str, str], List[float]]],
               metrics: Dict[str, Metric],
               safety_blocks: Optional[List[str]] = None,
               human_veto: Optional[str] = None) -> ShipDecision:
        comps, vars_, slices = {}, {}, []
        for name, cells in cells_by_metric.items():
            m = metrics[name]
            if m.role is not Role.GATE:
                continue                      # only gates gate. Guides inform.
            mde = m.noise_floor.mde if m.noise_floor else None
            comps[name] = compare(cells, candidate, baseline, mde=mde)
            vc = variance_components(cells)
            vars_[name] = vc
            for k, sc in shrink(cells, vc).items():
                if k[0] == candidate and not (sc.ci[0] <= 0 <= sc.ci[1]):
                    slices.append(SliceFinding(k, sc.shrunk, sc.ci, 100*(1-sc.weight)))
        slices.sort(key=lambda s: -s.shrunk)

        cannot = [
            f"anything about the other language — rho(en,zh) = -0.082, so this says "
            f"nothing about the {'zh' if language == 'en' else 'en'} corpus",
            "whether users prefer it — no user has ever touched this corpus",
            "chemistry (user x character x model) — structurally impossible offline",
        ]
        for name, c in comps.items():
            if c.mde:
                cannot.append(f"{name}: a change smaller than {100*c.mde:.2f}pp — "
                              f"invisible, not absent")
        self.stage[candidate] = Stage.SHIP_REVIEW
        return ShipDecision(candidate, baseline, language, comps, vars_, slices,
                            safety_blocks or [], cannot, human_veto)

    # ---- stage 4: live -----------------------------------------------------
    def promote(self, variant_id: str, to: Stage) -> None:
        if to is Stage.LIVE and self.stage.get(variant_id) is not Stage.CANARY:
            raise ValueError(
                "LIVE requires CANARY first. There is no user-safe on-policy middle: "
                "shadow cannot work for multi-turn (the candidate's turn-2 is conditioned "
                "on the incumbent's turn-1), so the only honest signal is offline self-play "
                "or real users."
            )
        self.stage[variant_id] = to

    # ---- stage 5: the loop -------------------------------------------------
    def curate(self, mined_cases: List[dict], existing_provenance: List[str]) -> List[dict]:
        """The benchmark ACCUMULATES, never replaces.

        Mined cases are our own models' output. Curation that replaces human-authored anchors
        runs the model-collapse experiment on our eval set, after which it reports
        improvement forever BY CONSTRUCTION. Enforced here, not monitored.
        """
        n_human = sum(1 for p in existing_provenance if p == "human-authored")
        n_total = len(existing_provenance) + len(mined_cases)
        if n_total and n_human / n_total < 0.5:
            raise ValueError(
                f"provenance cap breached: human-authored would fall to "
                f"{n_human/n_total:.0%} of the suite. Mined cases are our own models' "
                f"output; letting them dominate runs model collapse on the eval set, and "
                f"the benchmark then reports improvement forever by construction."
            )
        return mined_cases
