---
title: "Measurement invariance and differential item functioning: configural, metric, scalar, strict"
url: https://www.cogn-iq.org/learn/theory/measurement-invariance/
authors: Cogn-IQ Encyclopedia; Lesa Hoffman (CLP948 Lecture 07); Berkeley D-Lab
year: 2024
type: reference (multi-source compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Measurement invariance / DIF — the cross-language comparability question

Sources compiled:
- Measurement Invariance reference — https://www.cogn-iq.org/learn/theory/measurement-invariance/
- Hoffman, "Measurement Invariance (MI) in CFA and Differential Item Functioning" — https://www.lesahoffman.com/CLP948/CLP948_Lecture07_Invariance.pdf
- Berkeley D-Lab, "Testing for Measurement Invariance using Lavaan (in R)" — https://dlab.berkeley.edu/news/testing-measurement-invariance-using-lavaan-r
- Anchoring vignettes for cross-cultural comparability — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10536699/

## The core idea

"Measurement invariance is the scale-level counterpart of item-level differential item functioning
... They address the same question — **whether an instrument means the same thing across groups** —
at different resolutions."

Without invariance, **a mean difference between groups is uninterpretable**: you cannot tell whether
group A truly scores higher or whether the instrument simply behaves differently in group A. This
is exactly our en/zh and cross-character problem.

## The nested hierarchy (multi-group CFA)

Fit in sequence; at each step ask whether the added equality constraints worsen fit.

| Level | Constrained equal across groups | Licenses you to compare |
|---|---|---|
| **Configural** | same factor structure / pattern only | nothing — just "same shape" |
| **Metric** (weak) | + factor **loadings** | **associations / correlations** between constructs |
| **Scalar** (strong) | + **intercepts** | **latent means** ← what a leaderboard needs |
| **Strict** | + **residual variances** | observed means, sum scores |

**Ranking models across languages requires at least scalar invariance.** This is the single most
load-bearing fact for our platform.

## Testing criteria

- The traditional **chi-square difference test** is "sensitive to sample size and flags trivial
  differences in large samples."
- The field relies on **changes in approximate fit indices**:
  - **ΔCFI > 0.01** ⇒ evidence of **non-invariance** (the most commonly used rule)
  - complementary **ΔRMSEA** (> 0.015) and **ΔSRMR** (> 0.030 for metric, > 0.010 for scalar)

## Partial invariance

If full scalar invariance fails, you can free the intercepts of the offending items and retain
**partial scalar invariance** — comparisons remain defensible provided a majority of items (a common
rule of thumb: at least two per factor, ideally >50%) remain invariant. Practically: identify the
offending items, free or drop them.

## DIF specifically

An item shows DIF when respondents of **equal latent ability** but different group membership have
different probabilities of a given response.
- **Uniform DIF** — constant offset across the ability range (item is just harder for one group).
- **Non-uniform DIF** — the gap varies with ability (item *discriminates* differently).

Detection methods: Mantel-Haenszel, logistic regression (nested models: ability → +group →
+ability×group), IRT likelihood-ratio tests, and multi-group IRT.

## Cross-language specifics

"Low comparability of translated questionnaires or the different understanding of response formats
by respondents might lead to rejection of measurement invariance and point to **comparability bias
in multi-language surveys**."

**RC-DIF** (response-category DIF / rating-scale DIF): respondents in different languages interpret
the *response categories* differently — a Chinese "4" is not an English "4" — even when they
understand the item identically. **Anchoring vignettes** are the standard remedy: have every group
rate the same fixed set of vignettes, then use their ratings to rescale the response categories per
group.

This is directly transplantable: give every judge (en and zh) the same anchor transcripts with known
"true" scores, and use their ratings on those anchors to calibrate the scale.

## Relevance to companion-eval

Our claim "model A beats model B, in both en and zh" is a **latent mean comparison across groups**
and is only valid under scalar invariance. Groups = language, and arguably character. Concretely we
must test invariance across en/zh, and either establish it, establish partial invariance, or stop
reporting a pooled cross-language score.
