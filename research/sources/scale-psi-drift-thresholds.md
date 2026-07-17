---
title: "Measuring Data Drift with the Population Stability Index (PSI)"
url: https://www.fiddler.ai/blog/measuring-data-drift-population-stability-index
org: Fiddler AI
year: 2023
type: blog
accessed: 2026-07-16
topic: production-scale
---

# PSI — formula, thresholds, binning, zero handling

## Formula (verbatim)

```
PSI = Σ_b (ActualProp(b) - ExpectedProp(b)) × ln( ActualProp(b) / ExpectedProp(b) )
```

Where:
- `B` = total number of bins
- `ActualProp(b)` = proportion of counts in bin b from the **target** (current) distribution
- `ExpectedProp(b)` = proportion of counts in bin b from the **reference** (baseline) distribution

Note the term is a product of a difference and a log-ratio, summed over bins — this
is what makes PSI symmetric.

## Thresholds (the "0.1 / 0.2 rule")

- **PSI < 0.1** — distributions are considered similar (no significant change)
- **PSI 0.1 – 0.2** — target distribution is *moderately* different from reference
- **PSI > 0.2** — significant shift; recommendation to develop a new model using recent data

(Some sources, e.g. Minitab / credit-risk practice, use 0.25 rather than 0.2 as the
upper band: <0.1 stable, 0.1–0.25 moderate/investigate, >0.25 significant drift →
retrain. Both conventions are in wide use; 0.1/0.2 is the more conservative.)

## Binning strategies

Two approaches:
1. **Equi-width bins** — equal intervals across the variable range
2. **Equi-quantile / equi-depth bins** — each bin contains the same proportion of
   samples from the *reference* distribution

"Choice of strategy is context-specific and requires domain knowledge." Credit
scoring is given as an example where existing binning conventions should be maintained.

Critical practice note: **the same bin edges must be used for both samples**. Bin
edges are computed once on the reference and then frozen; recomputing edges per
batch destroys comparability.

Common industry default: **10 bins** (deciles) of the reference distribution.

## Handling zero / empty bins

PSI is undefined (or unbounded) when a bin proportion is zero. Guidance:
- add "a small value such as **0.01**" to each bin proportion, **or**
- add "a base count of **1**" to each bin

## Relationship to KL divergence

PSI is mathematically equivalent to the **symmetrized Kullback-Leibler divergence**:

```
PSI = KL(Expected || Actual) + KL(Actual || Expected)
```

This is why PSI is symmetric while KL is not. (The article does not discuss
Jensen-Shannon divergence.)

## Why PSI matters at 50M/day

PSI is an *effect size*, not a hypothesis test. It has no n in it — the bin
proportions are normalized. So its value does not inflate with sample size, and a
fixed 0.1/0.2 threshold remains meaningful whether the batch is 10k or 10M. That is
exactly the property KS lacks.
