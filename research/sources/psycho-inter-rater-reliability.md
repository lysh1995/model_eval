---
title: "Inter-rater reliability: Cohen's/Fleiss' kappa, Krippendorff's alpha, ICC — selection and thresholds"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3402032/
authors: Kevin A. Hallgren (primary); plus StatsTest, k-alpha.org, ATLAS.ti methodological notes
year: 2012
type: tutorial/review (multi-source compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Inter-rater reliability: which coefficient, and what counts as acceptable

Sources compiled:
- Hallgren, "Computing Inter-Rater Reliability for Observational Data: An Overview and Tutorial" — https://pmc.ncbi.nlm.nih.gov/articles/PMC3402032/
- StatsTest, "Inter-Rater Reliability: Cohen's Kappa and Krippendorff's Alpha" — https://www.statstest.com/inter-rater-reliability-cohen-kappa-krippendorff-alpha
- k-alpha.org methodological notes — https://www.k-alpha.org/methodological-notes
- ATLAS.ti, "why Cohen's kappa is not a good choice" — https://atlasti.com/research-hub/measuring-inter-coder-agreement-why-cohen-s-kappa-is-not-a-good-choice
- Wongpakaran et al., Cohen's kappa vs Gwet's AC1 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3643869/

## Selection rules

| Situation | Coefficient |
|---|---|
| Exactly 2 raters, nominal categories | **Cohen's kappa** |
| >2 raters, nominal, fully crossed | **Fleiss' kappa** |
| Any number of raters, any measurement level (nominal/ordinal/interval/ratio), **missing data OK** | **Krippendorff's alpha** |
| Continuous / ordinal scores, want to model rater as a variance facet | **ICC** |
| High prevalence skew (base-rate problem) | **Gwet's AC1** |

Verbatim points:
- "Cohen's Kappa works for two raters; Krippendorff's Alpha handles multiple raters and missing
  data."
- Krippendorff's alpha "is intended for addressing projects with larger numbers of coders,
  different scales of measurement, and missing data."
- "ICCs use list-wise deletion for missing data and cannot accommodate datasets in fully-crossed
  designs with large amounts of missing data" — Krippendorff's alpha "may be more suitable when
  problems are posed by missing data in fully-crossed designs."

## Thresholds

**Kappa (Landis & Koch-style bands):**
- < 0.40 — poor
- 0.40–0.60 — moderate
- 0.60–0.80 — substantial
- > 0.80 — excellent

**Krippendorff's alpha (Krippendorff's own recommendation):**
- **α ≥ 0.80** — satisfactory; "acceptable for drawing triangulated conclusions based on the rated
  data."
- **α ∈ [0.67, 0.79]** — "the lower bound for tentative conclusions," moderate agreement; "outcomes
  should be interpreted with concern."
- **α < 0.67** — do not draw conclusions.

**ICC (Koo & Li convention, widely used):**
- < 0.50 — poor
- 0.50–0.75 — moderate
- 0.75–0.90 — good
- > 0.90 — excellent

## The base-rate / prevalence problem (kappa paradox)

Kappa corrects for chance agreement using the **marginal distributions** of each rater. When one
category dominates (high prevalence skew), expected chance agreement approaches observed agreement,
so **kappa collapses toward 0 even when raw percent agreement is 95%+**. This is the "kappa
paradox" (Feinstein & Cicchetti). A second paradox: unbalanced marginals between raters can
*inflate* kappa.

Consequence: kappa is **not comparable across dimensions with different base rates**. Two dimensions
with identical rater behaviour can post wildly different kappas purely because one has a skewed
score distribution.

Gwet's AC1 was designed specifically to be stable under prevalence skew and is the recommended
alternative when categories are unbalanced.

## ICC forms (Shrout & Fleiss / McGraw & Wong)

Must specify three things or the number is uninterpretable:
1. **Model**: one-way random / two-way random / two-way mixed
2. **Type**: single rater `ICC(1)` vs average of k raters `ICC(k)`
3. **Definition**: **absolute agreement** vs **consistency**

For LLM judges: report **ICC(2,1) absolute agreement** if you care that judges give the *same
number*; **ICC(3,1) consistency** if you only care they *rank the same way*. Absolute agreement is
the stricter and more relevant one for a shared baseline across models.

## Relevance to companion-eval

- Our dimensions are ordinal (1–5) with multiple LLM judges and possible missing ratings →
  **Krippendorff's alpha with ordinal difference metric** is the default choice.
- Report **ICC(2,1) absolute agreement** alongside, since it decomposes into variance components
  and connects to generalizability theory.
- Watch the base-rate trap: "safety violation" will be ~98% one category. Use **Gwet's AC1** there,
  not kappa.
