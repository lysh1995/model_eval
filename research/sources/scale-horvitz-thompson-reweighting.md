---
title: "Horvitz–Thompson estimator / inverse-probability weighting for stratified sampling"
url: https://en.wikipedia.org/wiki/Horvitz%E2%80%93Thompson_estimator
org: Wikipedia / ScienceDirect / EmergentMind (composite reference)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Horvitz–Thompson (HT) estimator — the correction that makes stratified judging honest

**Why this matters:** the moment we stop sampling uniformly (which we must, to keep
rare characters visible), our raw judged sample **stops being representative of
production traffic**. Any naive average over the judged set is then a *biased* estimate
of the true production quality. HT is the standard fix, and it is cheap. Getting this
wrong is the single most likely way our dashboard silently lies.

## Definition

> The Horvitz–Thompson estimator is a method for estimating the total and mean of a
> pseudo-population in a stratified sample by applying **inverse probability weighting**
> to account for the difference in the sampling distribution between the collected data
> and the target population.

> The HT Estimator considers the design probabilities directly, using **the inverse of
> the inclusion probabilities** for each sampled unit to estimate population totals.

Formally, for a population total with inclusion probability `π_i` for unit `i`:

```
  T̂_HT = Σ_{i ∈ sample}  y_i / π_i
```

and for a mean, divide by the population size N (or use the Hájek variant, dividing by
`Σ 1/π_i`, which is biased but usually lower-variance and is generally preferred when N
is not known exactly — for us N *is* known exactly, since we count every generation, so
plain HT is available).

## Key properties

> The Horvitz-Thompson estimator is able to produce **unbiased estimates even when the
> sampling design is complex**, and it accommodates varying probabilities, thereby
> reflecting the true characteristics of the population more accurately.

> This feature is particularly beneficial in **stratified sampling, cluster sampling,
> and other designs where selection probabilities differ significantly among units.**

> It can be recognized as an **inverse probability weighted (IPW) estimator.**

> It is widely applied in complex survey designs, network inference, and machine
> learning, remaining a cornerstone for robust estimation **despite its variance
> challenges.**

## The variance caveat — read this before shipping

That last clause is the trap. **HT is unbiased but its variance blows up when
inclusion probabilities are very small.** A tail cell sampled at π = 0.0001 contributes
each judged item with weight 10,000. One bad score in that cell swings the global
estimate hard. This is the classic inverse-propensity-weighting variance problem.

Consequences for our design:
- **Do not compute the global quality number by HT-reweighting a heavily stratified
  sample.** The variance will make the top-line metric jitter.
- **Instead, run two samples with different jobs:**
  - a **uniform** (or lightly-stratified) sample → powers the *global* top-line metric,
    where weights are near-constant and variance is well-behaved;
  - an **oversampled tail** stratum → powers *per-slice* metrics, which are reported
    **within-slice** and therefore need no reweighting at all.
- Reweighting is only needed when **aggregating across strata**. A per-character
  dashboard reading "character X failure rate = 4.2%" is computed only from character
  X's own sample and is unbiased with no weights. This is the cleanest way to sidestep
  the variance problem entirely: **report per-slice metrics per-slice, and keep a
  separate uniform sample for the global roll-up.**
- If we must aggregate across strata, **stabilize the weights** (clip/winsorize extreme
  weights, or use the Hájek ratio estimator) and report a variance estimate alongside
  the point estimate.

## Practical rule for the platform

Every judged record must persist its **inclusion probability `π_i`** (or equivalently
its stratum ID + that stratum's sampling rate) **at the time of sampling**, alongside
the score. Without `π_i` stored per record, the sample is uninterpretable after the
fact and no correct global estimate can ever be reconstructed — and because sampling
rates will change over time (we will re-tune strata), `π_i` cannot be recovered later
from a config file. **`π_i` is lineage data and belongs in the event schema.**
