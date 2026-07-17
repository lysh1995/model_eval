---
title: "Which test is the best? We compared 5 methods to detect data drift on large datasets"
url: https://www.evidentlyai.com/blog/data-drift-detection-large-datasets
org: Evidently AI
year: 2023
type: blog
accessed: 2026-07-16
topic: production-scale
---

# Evidently AI — comparing 5 drift detection methods on large datasets

THE single most load-bearing source for the large-n over-triggering question.

## Methods compared

Five methods evaluated:
1. **Kolmogorov-Smirnov (KS)** test
2. **Population Stability Index (PSI)**
3. **Kullback-Leibler divergence (KL)**
4. **Jensen-Shannon distance (JS)**
5. **Wasserstein distance (WD)**

(Chi-square not included in this comparison.)

## Sample sizes used in experiments

- Artificial drift experiments: **1,000 to 1,000,000 objects**
- Fixed sample size comparisons: **100,000 observations**
- Real-world examples: **10,000 to 200,000** per dataset

## Per-method thresholds (verbatim)

**KS test**
- "p-value is < 0.05, we'll alert on the drift"
- Detects **0.5% drift** at 100,000+ samples
- Recommendation: use "under 1000" observations; "you might want to take a sample"

**PSI**
- Threshold: "PSI > 0.1"
- Interpretation bands: "<0.1: no change; 0.1-0.2: moderate; >=0.2: significant"
- Detects drift only above **10% magnitude** at 100,000 samples

**KL divergence**
- Behaves "almost identical to the PSI"
- Asymmetric (unlike PSI)

**Jensen-Shannon distance**
- Threshold: "0.1 means drift"
- Bounded: **0 to 1** scale
- Slightly more sensitive than PSI/KL

**Wasserstein distance (normalized)**
- Threshold: "0.1 value as drift"
- Interpreted in units of **standard deviations**
- Overestimation on small samples is "less than Kolmogorov-Smirnov"

## Drift magnitude detection at 100,000 observations (whole dataset)

| Method | Minimum drift magnitude detected |
|---|---|
| KS | ~1% drift |
| WD | moderate sensitivity above ~5% |
| PSI / KL / JS | require >=10% drift |

This table is the crux: at n=100k the KS test fires on a 1% shift — operationally
meaningless — while the distance metrics require a 10% shift. At 50M/day the KS
test's power is far higher still.

## Segment drift (drift confined to 20% of data)

All tests show weak sensitivity. PSI detects only a "100%-shift in the data segment."

## Evidently's own default behavior

Evidently "selects a suitable drift test based on the feature type, number of
observations, and unique values" with "reasonable defaults." Specific switching
thresholds not disclosed in this article (see the Evidently docs capture for the
actual n<=1000 / n>1000 rule).

## Takeaway for a 50M/day platform

Statistical *significance* tests (KS, chi-square) are the wrong tool at this volume;
they measure "do I have enough data" more than "did anything change." Effect-size
/ distance metrics (PSI, JS, Wasserstein) with fixed thresholds are scale-stable.
