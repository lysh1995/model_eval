---
title: "Benjamini-Hochberg FDR control and multiple-testing correction for monitoring"
url: https://www.statisticshowto.com/benjamini-hochberg-procedure/
org: Benjamini & Hochberg (1995); Statsig; Statology
year: 1995 / 2024
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Benjamini-Hochberg / FDR — controlling alert fatigue across many slices

## The problem at our scale

Slicing by **~95 characters x 2 languages x N variants** means we run on the order of
**hundreds to thousands of simultaneous tests** every monitoring window. At alpha=0.05
with 1,000 independent slices and *nothing actually wrong*, you expect **50 false
alerts per window**. Run that every hour and it is 1,200 false alerts/day. The alerting
system becomes noise and gets ignored — this is the mechanism of alert fatigue, and it
is arithmetic, not bad luck.

## Benjamini-Hochberg procedure (1995)

Controls the **False Discovery Rate** — the expected *proportion* of false positives
among rejected nulls.

### Procedure
1. Put the individual p-values in **ascending order**
2. Assign **ranks** i = 1..m to the p-values
3. Compute the critical value for each: **(i/m) x Q**
   - where `m` = total number of hypotheses tested
   - `Q` = the chosen false discovery rate (e.g. 0.05, 0.10)
4. Find the **largest p-value that is smaller than its critical value**
5. That p-value **and all smaller ones** are declared significant

### Adjusted p-value formula

```
Adjusted p-value = min{ 1, min_{j>=i} { m * p_(j) / j } }
```

"For each p-value at rank i, the adjusted p-value is calculated as the minimum value
between 1 and the minimum ratio obtained by dividing m (the total number of hypotheses)
by j (the rank) for all j greater than or equal to i."

## BH vs Bonferroni

"The Benjamini-Hochberg procedure is **less strict** than a Bonferroni Correction.
A Bonferroni Correction controls the chance of **at least one** false positive (Family
Wise Error Rate). BH instead controls the **expected proportion** of false positives
when you reject the null (False Discovery Rate)."

Bonferroni (alpha/m) is far too conservative at m=1,000: it demands p < 0.00005 per
slice and will miss real regressions in low-traffic characters. FDR is the right error
notion for monitoring — we are willing to accept that ~5-10% of the alerts we page on
are false, in exchange for catching real regressions in small slices.

## Practical recommendations for alert design

Beyond BH, the literature (and the Evidently/KS discussion) converges on:
- **Pair p-values with an effect size.** From the KS search: "Pair KS p-values with an
  effect-size measure such as PSI or Wasserstein distance, and apply a Bonferroni or
  false-discovery-rate correction when running it across many features." Require *both*
  statistical significance AND a minimum practical effect size to fire. At 50M/day the
  effect size is the binding constraint, and significance is nearly free.
- **Rate-of-change alerting:** alert on the *derivative* of the metric rather than the
  level, so a slow benign drift in the baseline does not sit permanently over a static
  threshold generating a stuck alert.
- **Minimum sample floor per slice** before a slice is eligible to alert at all.
- **Hierarchical / two-stage testing:** test the global aggregate first; only descend
  into per-character slices when the parent shows movement. This cuts m by orders of
  magnitude and is more powerful than flat BH over all slices.
- **e-BH:** the e-value analogue of BH (Wang & Ramdas) controls FDR for e-values and,
  unlike BH, requires **no independence or PRDS assumption** — our slices are correlated
  (a bad model release moves all characters at once), so this matters.

## Note on the independence assumption

Standard BH requires independence or positive regression dependence (PRDS). Our slices
are **positively correlated** (shared model, shared traffic). PRDS plausibly holds for
same-direction shifts, so BH is defensible; Benjamini-Yekutieli (dividing by the
harmonic number `sum(1/i)`, ~7.5 at m=1000) is the assumption-free but much more
conservative fallback.
