---
title: "Data drift algorithm — default test selection logic"
url: https://docs-old.evidentlyai.com/reference/data-drift-algorithm
org: Evidently AI
year: 2024
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Evidently's default drift test selection — the n=1000 switching rule

This is the concrete, published version of "what test should I use at what n." Evidently
switches from hypothesis tests to distance metrics at **1000 observations**.

## Small data: <= 1000 observations in the reference dataset

| Column type | Test |
|---|---|
| Numerical, `n_unique > 5` | **two-sample Kolmogorov-Smirnov test** |
| Categorical, or numerical with `n_unique <= 5` | **chi-squared test** |
| Binary categorical (`n_unique <= 2`) | **proportion difference test** for independent samples, based on Z-score |

**Threshold:** all small-data tests use a **0.95 confidence level** by default.
Drift score = **p-value**; **p <= 0.05 means drift**.

## Larger data: > 1000 observations in the reference dataset

| Column type | Test |
|---|---|
| Numerical, `n_unique > 5` | **Wasserstein Distance** (normalized) |
| Categorical, or numerical with `n_unique <= 5` | **Jensen-Shannon divergence** |

**Threshold:** all large-data metrics use **threshold = 0.1** by default.
Drift score = distance/divergence; **>= 0.1 means drift**.

## The headline

> "The 1000 observation threshold is the key dividing point in Evidently AI's automatic
> method selection logic."

A mature drift library abandons the KS test entirely above 1,000 rows. Our platform
operates at **50,000,000 per day** — five orders of magnitude past the point where the
vendor that publishes this stops using p-value tests. This is the single strongest
citation for not using KS.

## Cross-reference

Their empirical blog post (scale-evidently-large-dataset-drift-comparison.md) shows why:
at n=100,000 KS fires on a **0.5–1% shift**, while PSI/JS require **~10%**. The KS
p-value at n=50M is essentially a measure of sample size, not of change.
