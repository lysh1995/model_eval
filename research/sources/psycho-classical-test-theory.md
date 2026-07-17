---
title: "Classical test theory: Cronbach's alpha, standard error of measurement, correction for attenuation"
url: https://www.cogn-iq.org/learn/theory/cronbachs-alpha/
authors: Cogn-IQ Encyclopedia; Schmitt (1996); McManus (2010); Moss (2019)
year: 2024
type: reference (multi-source compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Classical test theory essentials

Sources compiled:
- Cronbach's alpha reference — https://www.cogn-iq.org/learn/theory/cronbachs-alpha/
- Schmitt, "Uses and Abuses of Coefficient Alpha" (1996) — https://dosen.perbanas.id/wp-content/uploads/2017/05/Schmitt-1996-Uses-and-abuses-of-coefficient-alpha.pdf
- McManus, "The standard error of measurement is a more appropriate measure of quality for postgraduate medical assessments than is reliability" — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2893515/
- Moss, "Correcting for attenuation due to measurement error" — https://www.mn.uio.no/math/english/research/projects/focustat/publications_2/jonasmoss_oct2019.pdf

## The CTT decomposition

```
X = T + E
```
Observed score = True score + Error. Errors assumed mean-zero and uncorrelated with true score.

**Reliability** is defined as the proportion of observed variance that is true variance:

```
ρ_XX' = σ²_T / σ²_X = σ²_T / (σ²_T + σ²_E)
```

## Cronbach's alpha

```
α = (k / (k − 1)) · (1 − Σσ²_i / σ²_t)
```
- `k` = number of items
- `σ²_i` = variance of item `i`
- `σ²_t` = variance of the total score

Conventional guidelines: **.70 is the minimum threshold**; **.90 is the standard for high-stakes
decisions**.

**Schmitt's caveat (important)**: alpha is *not* a measure of unidimensionality. A scale can have
high alpha and still be multidimensional. Alpha rises mechanically with `k` — a long scale of
mediocre items can clear .70 without measuring one coherent thing. Schmitt argues there is "no
sacred level" of alpha.

## Standard error of measurement (SEM)

```
SEM = SD · √(1 − ρ_XX')
```
- `SD` = standard deviation of observed scores
- `ρ_XX'` = reliability (often Cronbach's alpha)

"The standard error of measurement is inversely related to reliability — the greater the
reliability, the smaller the SEM and the more accurate the examination."

95% confidence interval on an individual's true score: `X ± 1.96 · SEM`.

**McManus's argument**: SEM is a *better* quality report than reliability, because reliability
depends on the variance of the population you happened to sample (a homogeneous cohort deflates
reliability without the instrument getting worse), whereas SEM is in the units of the score itself
and is population-independent.

This matters enormously for us: if we evaluate 5 near-identical model variants, between-model
variance `σ²_T` is small, so **reliability will look terrible even with a perfect rubric**. Report
SEM.

## Correction for attenuation (Spearman)

Measurement error biases observed correlations **toward zero**. The disattenuated correlation
between constructs `x` and `y`:

```
r_{x'y'} = r_{xy} / √(ρ_xx' · ρ_yy')
```

Use: estimating the *true* relationship between two constructs given unreliable measures of each.
Caveats — the correction can produce estimates > 1.0 when reliabilities are underestimated, and it
amplifies sampling error; report both the raw and disattenuated values.

**Ceiling on validity**: the observed correlation between two measures cannot exceed
`√(ρ_xx' · ρ_yy')`. So the reliability of our judge caps how well our scores can *possibly*
correlate with human preference. If judge reliability is 0.6, a validity correlation of 0.77 is the
mathematical maximum.

## Spearman-Brown prophecy formula

Predicts reliability if the test is lengthened by a factor of `n`:

```
ρ_new = (n · ρ_XX') / (1 + (n − 1) · ρ_XX')
```

Use: "how many more items/judges do I need to reach α = 0.80?" Solve for `n`.

## Relevance to companion-eval

Report **SEM per dimension**, not just alpha — it's the number that tells an engineer whether a
2-point score gap is real. Spearman-Brown tells us the cheapest lever: adding judges vs adding
scenarios.
