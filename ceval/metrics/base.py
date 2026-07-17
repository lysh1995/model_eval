"""The metric framework. Two rules, one per job.

GATE  -- blocks a ship. If wrong: you ship something bad, or block something good, and
         false alarms teach the team to ignore the platform. Needs a noise floor.
GUIDE -- tells a human what to change. If wrong: someone loses an afternoon. Recoverable
         IF labeled honestly. Needs an honest interval, not an MDE.

The cut criterion is NOT "unproven" -- it is "directionally wrong".

ONE rule does not relax for guides: registered confound tests. A confounded metric isn't
fuzzy, it is WRONG IN A SPECIFIC DIRECTION and the reader cannot tell. A length confound
doesn't blur the answer; it makes the answer "verbosity" while the label says "voice".

We shipped two invisible confounds in one afternoon (length rho=+0.73, then survivorship).
Neither looked like a failure. Hence: a metric without a registered confound test does not
load. Not a review step -- an import error.
"""
from __future__ import annotations
import statistics as st
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence


class Role(Enum):
    GATE = "gate"      # may block a ship
    GUIDE = "guide"    # informs a human; never blocks
    TRIPWIRE = "tripwire"  # zero-tolerance event; no statistics needed


class Unit(Enum):
    """The unit of analysis. Getting this wrong is how you overstate evidence 60x."""
    CONVERSATION = "conversation"   # the sampling unit. Turns are repeated measures.
    CORPUS = "corpus"               # only defined ACROSS responses (homogenization)
    TURN = "turn"                   # almost always wrong -- FED: per-response scoring is
                                    # DIRECTIONALLY wrong (ranks Meena above Human, then
                                    # flips at dialogue level)


@dataclass
class ConfoundTest:
    """A registered confound with a measured ceiling. CI fails if the residual exceeds it."""
    name: str
    covariate: Callable[[Any], float]     # extract the confounding variable from an item
    max_abs_rho: float
    note: str = ""


@dataclass
class NoiseFloor:
    """Required to GATE, optional to GUIDE."""
    sigma_within: float
    mde: float
    n_planned: int
    source: str          # a script path. If you can't point at code, you don't have one.


@dataclass
class ConfoundResult:
    name: str
    rho: float
    ceiling: float
    @property
    def passed(self) -> bool:
        return abs(self.rho) <= self.ceiling


@dataclass
class MetricResult:
    metric: str
    version: str
    role: Role
    unit: Unit
    values: Dict[Any, float]                      # key -> value
    confounds: List[ConfoundResult] = field(default_factory=list)
    interval: Optional[tuple] = None
    caveats: List[str] = field(default_factory=list)

    @property
    def confounded(self) -> bool:
        return any(not c.passed for c in self.confounds)

    def label(self) -> str:
        """The number, with its uncertainty printed ON it -- not in a footnote."""
        bits = []
        if self.confounded:
            bad = [f"{c.name} rho={c.rho:+.3f} > {c.ceiling}" for c in self.confounds if not c.passed]
            bits.append("CONFOUNDED: " + "; ".join(bad))
        bits.extend(self.caveats)
        return " | ".join(bits)


_REGISTRY: Dict[str, "Metric"] = {}


class Metric:
    """Base class. Subclass, set the class attrs, implement compute()."""
    name: str = ""
    version: str = "0"
    role: Role = Role.GUIDE
    unit: Unit = Unit.CONVERSATION
    languages: Sequence[str] = ("en", "zh")
    validity: str = ""                        # what does this PREDICT? Not "is it stable?"
    confounds: Sequence[ConfoundTest] = ()
    noise_floor: Optional[NoiseFloor] = None
    caveats: Sequence[str] = ()
    comparable_across_languages: bool = False  # rho(en,zh) = -0.082. Default: NO.

    def compute(self, items) -> Dict[Any, float]:
        raise NotImplementedError

    # -- registration is where the rules bite ------------------------------------
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        if not cls.name:
            return                                    # abstract intermediate
        if not cls.confounds:
            raise TypeError(
                f"{cls.__name__}: no registered confound tests. A metric's confound tests "
                f"are part of its definition, not a review step. If you truly believe there "
                f"are none, declare confounds=(NO_CONFOUNDS,) and say why in `caveats`."
            )
        if not cls.validity:
            raise TypeError(
                f"{cls.__name__}: no validity claim. 'Can we measure it consistently?' is "
                f"the wrong question -- reliable is not valid (Faux Pas: ICC=.996, r=-.029 "
                f"to .135 with every other ToM task). State what this PREDICTS."
            )
        if cls.role is Role.GATE and cls.noise_floor is None:
            raise TypeError(
                f"{cls.__name__}: role=GATE requires a measured noise_floor. Without an MDE "
                f"the gate fires on every PR and gets disabled inside a fortnight. "
                f"Use role=GUIDE if you haven't measured one."
            )
        _REGISTRY[cls.name] = cls

    # -- running -----------------------------------------------------------------
    def run(self, items, covariate_values=None) -> MetricResult:
        vals = self.compute(items)
        confs = []
        for ct in self.confounds:
            if ct.name == "__none__":
                continue
            try:
                xs, ys = [], []
                for k, v in vals.items():
                    c = ct.covariate((k, items))
                    if c is not None:
                        xs.append(c); ys.append(v)
                if len(xs) >= 4:
                    confs.append(ConfoundResult(ct.name, spearman(xs, ys), ct.max_abs_rho))
            except Exception as e:                    # a confound test that errors is a
                confs.append(ConfoundResult(ct.name+"(ERROR)", 1.0, ct.max_abs_rho))  # failure
        return MetricResult(self.name, self.version, self.role, self.unit, vals,
                            confs, caveats=list(self.caveats))


NO_CONFOUNDS = ConfoundTest("__none__", lambda x: None, 1.0,
                            "explicitly declared: no plausible confound")


# -- statistics: stdlib only, and never hand-rolled where a permutation test will do ----
def spearman(a: Sequence[float], b: Sequence[float]) -> float:
    def rank(x):
        s = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x)
        for p, i in enumerate(s): r[i] = p + 1
        return r
    ra, rb = rank(a), rank(b); n = len(a)
    ma = mb = (n + 1) / 2
    num = sum((ra[i]-ma)*(rb[i]-mb) for i in range(n))
    den = (sum((r-ma)**2 for r in ra) * sum((r-mb)**2 for r in rb)) ** .5
    return num/den if den else 0.0


def perm_p(a: Sequence[float], b: Sequence[float], trials: int = 20000, seed: int = 0) -> float:
    """Permutation test. NEVER hand-roll a closed form.

    Earned the hard way: a hand-rolled betainc reported p=0.006 where the true value was
    0.070 -- wrong by 10x, caught only because the same output printed a critical value
    that contradicted it. Permutation tests are slower, assumption-free, and nearly
    impossible to get subtly wrong. 'Subtly wrong but plausible' is this platform's
    entire failure mode.
    """
    import random
    rng = random.Random(seed)
    obs = abs(spearman(a, b))
    bb = list(b); hits = 0
    for _ in range(trials):
        rng.shuffle(bb)
        if abs(spearman(a, bb)) >= obs: hits += 1
    return (hits + 1) / (trials + 1)


def bootstrap_ci(xs: Sequence[float], stat=st.mean, n: int = 5000,
                 alpha: float = 0.05, seed: int = 0) -> tuple:
    import random
    rng = random.Random(seed); k = len(xs)
    if k < 2: return (float("nan"), float("nan"))
    reps = sorted(stat([xs[rng.randrange(k)] for _ in range(k)]) for _ in range(n))
    lo = reps[int(alpha/2 * n)]; hi = reps[int((1-alpha/2) * n) - 1]
    return (lo, hi)


def registry() -> Dict[str, "Metric"]:
    return dict(_REGISTRY)
