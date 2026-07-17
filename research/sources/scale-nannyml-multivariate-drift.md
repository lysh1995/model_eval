---
title: "Multivariate Drift Detection — PCA reconstruction error and domain classifier"
url: https://nannyml.readthedocs.io/en/stable/how_it_works/multivariate_drift.html
org: NannyML
year: 2024
type: docs
accessed: 2026-07-16
topic: production-scale
---

# NannyML — multivariate drift detection

## Why univariate methods are insufficient

"Univariate data drift methods often **fail to detect when joint data distributions
change in the absence of individual feature shifts**, and they lack the data
relationship context between different input variables."

"Multivariate drift detection can identify changes that may **not be seen using solely
univariate methods**."

Concretely: each feature's marginal can be unchanged while their *correlation* flips
entirely. For an LLM eval platform this is real — e.g. response length and judge score
individually stable, but the relationship between them inverts after a model change.

Corollary: multivariate methods also **collapse many tests into one**, which directly
addresses the multiple-testing/alert-fatigue problem. One drift signal per slice instead
of one per feature per slice.

## NannyML's two multivariate options

"To address univariate data drift methods' shortfalls, NannyML offers **2 options**:
**Data Reconstruction with PCA** and a **Domain Classifier**."

## Data Reconstruction with PCA

Mechanism:
- "The PCA algorithm is **fitted on the reference dataset** and learns a transformation
  from the pre-processed model input space to a **latent space**, which is then applied
  to compress the data being analyzed."
- "When there is data drift, the principal components the PCA method has learnt become
  **suboptimal**, resulting in **worse reconstruction** of the new data and therefore a
  **different reconstruction error**."

The signal is a single scalar per chunk: **reconstruction error**. Note it alerts on
error moving in *either* direction — an unusually *low* reconstruction error is also
drift (the data got more concentrated than reference).

## Thresholds

> "A threshold for significant change in NannyML is defined as values that are more than
> **three standard deviations** away from the mean of the reference data."

"NannyML computes the **mean and standard deviation of the reconstruction error with PCA
on the reference dataset based on different results for each Data Chunk**, establishing
a range of expected values of reconstruction error. If the reconstruction error crosses
the upper or lower threshold an alert is raised."

This is a **3-sigma control chart on a chunk-level statistic** — the same structural
idea as EWMA/SPC, applied to a learned multivariate summary. Crucially, the sigma is
estimated from **chunk-to-chunk variation in the reference period**, not from the raw
per-row variance. That is the trick that makes it scale-stable: it calibrates against
"how much does this statistic normally bounce around between hours," which is the
operationally meaningful null.

## Why the chunk-level calibration matters at 50M/day

This is the deep lesson and it generalizes beyond NannyML. A KS test asks "could these
two samples come from the same distribution?" — an answer that becomes trivially "no" as
n grows. NannyML instead asks **"is this chunk's statistic outside the range this
statistic normally occupies?"** — calibrated empirically on reference chunks. That
question stays meaningful at any n, because the reference variability is measured at the
same chunk size as the thing being tested.

**Any statistic can be made scale-stable this way**: compute it per chunk over the
reference period, take mean +/- 3 sd of the chunk-level values, alert on excursion. This
is the recommended meta-pattern for the platform — it turns arbitrary metrics (judge
score, refusal rate, PSI itself) into calibrated alerts with an interpretable false-alarm
rate, without ever computing a p-value against a raw-sample null.
