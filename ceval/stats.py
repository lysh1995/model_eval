"""The stats engine. ONE model, four jobs -- this is the key build decision.

Shrinkage, variance components, clustering, and elasticity are not four features. They are
one mixed-effects model:

    score ~ 1 + (1|model) + (1|character) + (1|model:character) + (1|conversation)

  variance components  -> the G-study; the SRM chemistry term (6.7% en / 14.6% zh)
  shrunk cell means    -> drill-down that isn't a noise amplifier (19.4pp MDE at n=3)
  cluster-robust SEs   -> effective n = conversations (42% of turn-level findings are
                          spurious without this)
  random slopes        -> elasticity WITHOUT difference scores (r_DD drives per-cell
                          delta reliability toward zero -- our own control does it)

Pure stdlib: no numpy, no statsmodels. Variance components via expected mean squares
(exact for the balanced case, which our corpus is: 11 x 95 x 3, no missing cells).
Shrinkage via empirical Bayes. Everything else via permutation/bootstrap, because a
hand-rolled closed form already lied to us once (p=0.006 where the truth was 0.070).
"""
from __future__ import annotations
import collections, math, random, statistics as st
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass
class VarianceComponents:
    """A two-way random-effects decomposition with replication."""
    model: float
    character: float
    interaction: float      # CHEMISTRY: "this model suits this character"
    residual: float         # run-to-run noise
    f_interaction: float
    n_models: int
    n_characters: int
    n_runs: int

    @property
    def total(self) -> float:
        return self.model + self.character + self.interaction + self.residual

    def pct(self) -> Dict[str, float]:
        t = self.total or 1.0
        return {"model": 100*self.model/t, "character": 100*self.character/t,
                "chemistry": 100*self.interaction/t, "residual": 100*self.residual/t}

    def verdict(self) -> str:
        p = self.pct()
        out = []
        if p["residual"] > 50:
            out.append(f"noise dominates ({p['residual']:.0f}%): a SINGLE conversation is "
                       f"not evaluable -- any per-dialogue score is a coin flip with a decimal")
        if p["chemistry"] > p["model"]:
            out.append(f"chemistry ({p['chemistry']:.0f}%) EXCEEDS the model effect "
                       f"({p['model']:.0f}%): 'which model is best?' is the WRONG QUESTION "
                       f"for this dimension -- the leaderboard is actively misleading")
        if self.f_interaction < 1.5:
            out.append(f"F(interaction)={self.f_interaction:.2f}: chemistry is barely "
                       f"distinguishable from noise")
        return "; ".join(out) or "no structural warnings"


def variance_components(cells: Dict[Tuple[str, str], List[float]]) -> VarianceComponents:
    """cells: (model, character) -> [value per run]. Balanced design assumed.

    The 3 runs are what make this possible: they IDENTIFY the interaction separately from
    noise. Most designs confound the two and have to assume the interaction away.
    """
    models = sorted({m for m, _ in cells})
    chars  = sorted({c for _, c in cells})
    a, b = len(models), len(chars)
    n = min(len(v) for v in cells.values())
    cells = {k: v[:n] for k, v in cells.items()}     # balance

    allv = [x for v in cells.values() for x in v]
    grand = st.mean(allv)
    mmean = {m: st.mean(x for (mm, _), v in cells.items() if mm == m for x in v) for m in models}
    cmean = {c: st.mean(x for (_, cc), v in cells.items() if cc == c for x in v) for c in chars}
    cell_mean = {k: st.mean(v) for k, v in cells.items()}

    SS_A  = b*n*sum((mmean[m]-grand)**2 for m in models)
    SS_B  = a*n*sum((cmean[c]-grand)**2 for c in chars)
    SS_AB = n*sum((cell_mean[(m, c)]-mmean[m]-cmean[c]+grand)**2
                  for m in models for c in chars if (m, c) in cell_mean)
    SS_E  = sum((x-cell_mean[k])**2 for k, v in cells.items() for x in v)

    MS_A  = SS_A/(a-1) if a > 1 else 0.0
    MS_B  = SS_B/(b-1) if b > 1 else 0.0
    MS_AB = SS_AB/((a-1)*(b-1)) if a > 1 and b > 1 else 0.0
    MS_E  = SS_E/(a*b*(n-1)) if n > 1 else 0.0

    v_e  = MS_E
    v_ab = max(0.0, (MS_AB-MS_E)/n) if n else 0.0
    v_a  = max(0.0, (MS_A-MS_AB)/(b*n)) if b and n else 0.0
    v_b  = max(0.0, (MS_B-MS_AB)/(a*n)) if a and n else 0.0
    return VarianceComponents(v_a, v_b, v_ab, v_e,
                              (MS_AB/MS_E) if MS_E else float("inf"), a, b, n)


@dataclass
class ShrunkCell:
    key: Tuple[str, str]
    raw: float
    shrunk: float
    ci: Tuple[float, float]
    weight: float          # 0 = fully pooled to the model mean, 1 = trust the raw cell

    def label(self) -> str:
        return (f"{self.shrunk:.4f} [{self.ci[0]:.4f},{self.ci[1]:.4f}] "
                f"(raw {self.raw:.4f}, shrunk {100*(1-self.weight):.0f}% toward the mean)")


def shrink(cells: Dict[Tuple[str, str], List[float]],
           vc: Optional[VarianceComponents] = None) -> Dict[Tuple[str, str], ShrunkCell]:
    """Empirical-Bayes partial pooling. THE fix for the drill-down requirement.

    At n=3 a single (model, character) cell resolves only a ~19.4pp difference; resolving
    2pp would need ~281 runs. So the naive drill-down -- score each cell, rank, surface the
    worst -- is a NOISE AMPLIFIER that manufactures a story about some character every
    release. Someone burns a day investigating. That is how teams learn to ignore an eval
    platform.

    Shrinkage pulls each cell toward its model mean in proportion to its own noise. Cells
    with real signal survive; the rest go quiet.

    THE PLATFORM MUST NEVER DISPLAY A RAW PER-CELL SCORE. A number without its uncertainty
    is a lie in this system, and per-cell is where the lie is largest.
    """
    vc = vc or variance_components(cells)
    tau2 = vc.interaction                       # between-cell (real) variance
    models = collections.defaultdict(list)
    for (m, c), v in cells.items():
        models[m].append(st.mean(v))
    mmean = {m: st.mean(v) for m, v in models.items()}

    out = {}
    for (m, c), runs in cells.items():
        n = len(runs)
        raw = st.mean(runs)
        se2 = (vc.residual / n) if n else vc.residual     # within-cell sampling variance
        w = tau2 / (tau2 + se2) if (tau2 + se2) > 0 else 0.0
        shr = w * raw + (1 - w) * mmean[m]
        half = 1.96 * math.sqrt(max(se2 * (1 - w), 1e-12))
        out[(m, c)] = ShrunkCell((m, c), raw, shr, (shr - half, shr + half), w)
    return out


@dataclass
class Comparison:
    a: str
    b: str
    delta: float
    ci: Tuple[float, float]
    mde: Optional[float]
    n_effective: int

    @property
    def detectable(self) -> bool:
        return self.mde is None or abs(self.delta) >= self.mde

    def verdict(self) -> str:
        """The gate compares INTERVALS, never point estimates.

        Every CI tool surveyed fails a PR 'if any metric regresses'. At our noise floor
        that fires on every PR and gets disabled inside a fortnight. A gate that doesn't
        know its own MDE is theatre.
        """
        if self.mde is not None and abs(self.delta) < self.mde:
            return (f"NO DETECTABLE CHANGE (delta={self.delta:+.4f}, below MDE={self.mde:.4f}). "
                    f"This is not 'no regression' -- a change smaller than {self.mde:.4f} is "
                    f"INVISIBLE to this benchmark, not absent.")
        lo, hi = self.ci
        if lo <= 0 <= hi:
            return f"delta={self.delta:+.4f}, CI [{lo:+.4f},{hi:+.4f}] spans zero: not significant"
        return f"delta={self.delta:+.4f}, CI [{lo:+.4f},{hi:+.4f}] excludes zero: REAL"


def compare(cells: Dict[Tuple[str, str], List[float]], a: str, b: str,
            mde: Optional[float] = None, seed: int = 0) -> Comparison:
    """Paired at the CHARACTER level -- the only clean comparison unit.

    The dataset is paired at the seed level and independent below it. Never pair or diff
    individual turns across models: user turns diverge at the SECOND user turn in 100% of
    cases (note 00).

    Effective n = characters, NOT turns. Turns are autocorrelated repeated measures; 42% of
    turn-level findings are spurious without this.
    """
    chars = sorted({c for (m, c) in cells if m in (a, b)})
    pairs = []
    for c in chars:
        ka, kb = (a, c), (b, c)
        if ka in cells and kb in cells:
            pairs.append(st.mean(cells[ka]) - st.mean(cells[kb]))
    if not pairs:
        raise ValueError(f"no shared characters between {a} and {b}")
    delta = st.mean(pairs)
    rng = random.Random(seed); k = len(pairs)
    reps = sorted(st.mean([pairs[rng.randrange(k)] for _ in range(k)]) for _ in range(5000))
    ci = (reps[125], reps[-126])
    return Comparison(a, b, delta, ci, mde, k)


class PooledCrossLanguageRefused(Exception):
    """The platform REFUSES to emit a pooled cross-language number."""


def pool_across_languages(*_args, **_kw):
    """Deliberately not implemented. This is a feature.

    Spearman(en rank, zh rank) = -0.082 on homogenization -- statistically indistinguishable
    from zero. grok-4.1 swings 1.4% -> 29.6% on repetition (21x). Every SRM variance
    component differs ~2x between languages.

    A pooled cross-language score is not a summary. It is an average of two unrelated
    quantities, and it is wrong about both. Language is a separate MEASUREMENT CONTEXT in
    which the instrument must be independently validated -- not a slice you may collapse.

    This is measurement non-invariance: a Chinese "4" is not an English "4", a property of
    the SCALE, not the content, so better translation cannot fix it.
    """
    raise PooledCrossLanguageRefused(
        "Refusing to pool across languages. rho(en,zh) = -0.082: the ranking in one "
        "language carries no information about the other. Report per language. If you "
        "genuinely need a single number, you must first establish scalar invariance via "
        "a versioned anchoring-vignette set rated by every judge in every language."
    )
