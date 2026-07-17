# The chemistry term, measured (2026-07-16)

Reproduce: [`scripts/srm_variance.py`](../../scripts/srm_variance.py). No API key, no new generations.

## Why this was possible at all

From [16](16-psychology-crosscheck.md): **our corpus is already a round-robin.** 11 models × 95
characters × 3 runs, fully crossed and balanced — the exact design Kenny's **Social Relations Model**
decomposes. The psychology stream spotted that; we'd been sitting on it.

The 3 runs matter enormously: they **identify the interaction separately from noise.** Most designs
confound the two and have to assume the interaction away.

| term | question it answers |
|---|---|
| model main effect | *"some models are just better"* — the leaderboard's premise |
| character main effect | *"some characters are just harder"* |
| **model × character** | **CHEMISTRY** — *"this model suits this character"* |
| residual | run-to-run noise |

Metric: **repetition rate** — our only fully validated judge-free measure ([09](09-offline-probes.md),
[10](10-noise-floor.md)). Two-way random-effects ANOVA via expected mean squares.

## Result

| component | en | zh |
|---|---|---|
| model | **30.3%** | **54.6%** |
| character | 1.6% | 1.0% |
| **model × character (chemistry)** | **6.7%** | **14.6%** |
| residual | **61.5%** | 29.8% |
| F(interaction) = MS_AB/MS_E | **1.33** | **2.48** |

## What this does and does not say

**It does say:**

1. **Chemistry is real but subordinate — for this metric.** 6.7% / 14.6%, well below Kenny's 30–40%
   for human interpersonal perception. **"Which model is best?" is a meaningful question here**, which
   is a genuine (if partial) point *against* the strong version of the chemistry worry in
   [BENCHMARKS §0.5](../../docs/BENCHMARKS.md).
2. **Character main effects are negligible (1–2%).** Characters barely differ in how repetition-prone
   they make a model. Note this **contradicts nothing** — it's the *interaction*, not the character
   axis, that the drill-down requirement rests on.
3. **The en residual is 61.5%** — noise is the single largest component, again
   ([10](10-noise-floor.md) found σ_within > σ_between). In en, **F(interaction) = 1.33**: the
   interaction is *barely distinguishable from noise at all.* In zh, F = 2.48 — substantive.
4. **The languages diverge again.** Model effect 30% vs 55%; chemistry 6.7% vs 14.6%; residual 62% vs
   30%. **Every single component differs by ~2×.** This is now the fifth independent confirmation
   that en and zh are not one system.

**It does NOT say chemistry is small.** This is a **weak test of the hypothesis**, and the reason is
construct, not statistics:

> **Repetition is not a chemistry construct.** There is no reason a model would loop more with *this*
> character than *that* one beyond mechanical load. Kenny's 30–40% relationship effects were measured
> on **interpersonal perception** — i.e. *liking*, *preference*, *fit*. That is **Q1**, which
> [BENCHMARKS §0.5](../../docs/BENCHMARKS.md) establishes we **cannot measure offline at all**,
> because the corpus has no users in it.

So: **7–15% is a floor from a metric where chemistry should barely appear.** The real estimate needs
preference data. Finding a *detectable* interaction (zh F=2.48) in a metric with no plausible chemistry
mechanism is arguably evidence **for** the concern, not against it.

## What to do with it

- **Run this decomposition per dimension, not once.** It's ~free, and the interaction share will vary
  by construct. Any dimension where model × character rivals the model main effect is a dimension
  where the leaderboard is actively misleading.
- **This is the same mixed-effects machinery** already required for shrinkage ([10](10-noise-floor.md)),
  the G-study ([04](04-psychometrics-measurement.md)), and the clustering correction
  ([08](08-multiturn-conversation-eval.md)). **Four problems, one model.** Build it once.
- **Kenny's other finding matters for the architecture:** target effects are stable (**r=.90**),
  relationship effects are not (**r=.40**). So the model main effect is the estimable part and the
  interaction is intrinsically noisier — which means **detecting chemistry needs far more data than
  ranking models does.** Budget accordingly, or don't promise it.

## Caveat that applies to this note specifically

One metric, one construct, and the construct is the wrong one for the question. **This is a
demonstration that the machinery works and a floor on the interaction term — not an answer.** The
honest headline is *"chemistry is at least 7–15% on a metric where it should be ~0."*
