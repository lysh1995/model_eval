"""The 50M/day cost model. Every input carries its provenance; the report prints it.

The tiering claim under test:

    Lane 0  100% inline, blocking       regex + classifier
    Lane 1  100% async                  pure computation, no model call
    Lane 2  100% batch                  corpus statistics
    Lane 3  ~1% stratified              judge panel

If Lanes 0-2 are genuinely cheap enough to run on 100% of 50M/day, the design holds and only
the ~1% judge sample costs money. THAT IS A CHECKABLE CLAIM, and this module checks it
against measured throughput rather than asserting it.

Latency, not cost, is what forces the tiering: a judge takes 1,000-3,200ms against a ~200ms
guardrail budget, so even a FREE judge is 5-16x too slow to sit inline. Cost is why we cannot
judge everything ASYNCHRONOUSLY either -- two separate arguments, often conflated.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .units import Provenance, Quantity, TokenProfile, Price, Benchmark


@dataclass
class Workload:
    generations_per_day: float = 50_000_000
    turns_per_generation: float = 1.0
    languages: int = 2
    characters: int = 95
    variants: int = 5

    @property
    def cells(self) -> int:
        return self.characters * self.languages * self.variants

    @property
    def per_sec(self) -> float:
        return self.generations_per_day / 86_400


@dataclass
class TierPlan:
    lane0_coverage: float = 1.0
    lane1_coverage: float = 1.0
    lane2_coverage: float = 1.0
    lane3_coverage: float = 0.01
    lane3_escalation: float = 0.0001     # to a strong "gold" judge


@dataclass
class CostLine:
    lane: str
    coverage: float
    items_per_day: float
    unit_cost_usd: float
    per_day_usd: float
    provenance: Provenance
    note: str = ""


class CostModel:
    def __init__(self, workload: Workload, plan: TierPlan,
                 cheap_judge: Price, gold_judge: Price,
                 token_profile: TokenProfile,
                 lane1_throughput: Optional[Benchmark] = None,
                 bytes_per_event: Optional[float] = None):
        self.w, self.p = workload, plan
        self.cheap, self.gold, self.tp = cheap_judge, gold_judge, token_profile
        self.lane1 = lane1_throughput
        self.bytes_per_event = bytes_per_event

    # -------------------------------------------------- the checkable claim
    def lane1_cores_needed(self) -> Optional[Quantity]:
        """Is 'Lanes 0-2 are free' true? Convert MEASURED throughput into cores at 50M/day.

        This is the load-bearing check. If it comes back needing a fleet, the tiering
        argument is wrong and the $/day headline is fiction.
        """
        if not self.lane1:
            return None
        cores = self.w.generations_per_day / (self.lane1.per_sec * 86_400)
        return Quantity(cores, "cores", Provenance.MEASURED,
                        f"{self.lane1.per_sec:,.0f} dialogues/sec/core measured on the real corpus",
                        "single-threaded, pure stdlib, no numpy")

    def lane1_cost_per_day(self, usd_per_core_hour: float = 0.04) -> CostLine:
        c = self.lane1_cores_needed()
        cores = c.value if c else float("nan")
        cost = cores * 24 * usd_per_core_hour
        return CostLine("1 (computation)", self.p.lane1_coverage,
                        self.w.generations_per_day, 0.0, cost,
                        Provenance.MEASURED,
                        f"{cores:,.1f} cores @ ${usd_per_core_hour}/core-hr (price BORROWED)")

    def lane3_cost_per_day(self) -> List[CostLine]:
        n_cheap = self.w.generations_per_day * self.p.lane3_coverage
        n_gold = self.w.generations_per_day * self.p.lane3_escalation
        uc = self.cheap.judgment_cost(self.tp, cached=True, batch=True)
        ug = self.gold.judgment_cost(self.tp, cached=True, batch=False)
        return [
            CostLine(f"3 ({self.cheap.name})", self.p.lane3_coverage, n_cheap, uc,
                     n_cheap * uc, Provenance.BORROWED,
                     f"our {self.tp.per_judgment_input:,}-token prompt (MEASURED) "
                     f"x published price (BORROWED)"),
            CostLine(f"3-gold ({self.gold.name})", self.p.lane3_escalation, n_gold, ug,
                     n_gold * ug, Provenance.BORROWED, "escalation tier"),
        ]

    def counterfactual_100pct(self) -> Dict[str, float]:
        """What the brief's volume costs WITHOUT tiering. The number that justifies the design."""
        uc = self.cheap.judgment_cost(self.tp, cached=True, batch=True)
        ug = self.gold.judgment_cost(self.tp, cached=False, batch=False)
        return {
            f"100% {self.cheap.name} (batch+cached)": self.w.generations_per_day * uc * 365,
            f"100% {self.gold.name} (live)": self.w.generations_per_day * ug * 365,
        }

    def cache_saving_per_year(self) -> float:
        n = self.w.generations_per_day * self.p.lane3_coverage
        with_c = self.cheap.judgment_cost(self.tp, cached=True, batch=True)
        without = self.cheap.judgment_cost(self.tp, cached=False, batch=True)
        return (without - with_c) * n * 365

    def storage_per_year_tb(self) -> Optional[Quantity]:
        if self.bytes_per_event is None:
            return None
        tb = self.w.generations_per_day * 365 * self.bytes_per_event / 1e12
        return Quantity(tb, "TB/yr", Provenance.MEASURED,
                        f"{self.bytes_per_event:.0f} bytes/event measured on real dialogues",
                        "uncompressed; a columnar store typically gets 5-10x")

    # -------------------------------------------------- sampling
    def uniform_sampling_gap(self) -> Dict[str, float]:
        """Uniform 1% starves the tail. The floor fixes it at the SAME budget.

        ASSUMED: a head/tail traffic shape we do not have. Labelled, not hidden -- the real
        distribution changes these numbers and it is the first thing to measure in production.
        """
        per_cell_uniform = self.w.generations_per_day * self.p.lane3_coverage / self.w.cells
        return {"cells": self.w.cells,
                "judged_per_cell_per_day_if_uniform_and_flat": per_cell_uniform}

    def floor_plan(self, floor_per_cell: int = 500) -> Dict[str, float]:
        total = floor_per_cell * self.w.cells
        return {"floor_per_cell_per_day": floor_per_cell,
                "total_judged_per_day": total,
                "as_frac_of_traffic": total / self.w.generations_per_day}
