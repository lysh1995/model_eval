---
title: "Generalizability theory: facets, variance components, G-studies and D-studies"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6699529/
authors: Bloch & Norman (primer); Brennan (NCME Module 14); Cogn-IQ Encyclopedia
year: 2019
type: tutorial/review (multi-source compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Generalizability theory (G-theory)

Sources compiled:
- Bloch & Norman, "Generalizability Theory Made Simple(r): An Introductory Primer to G-Studies" — https://pmc.ncbi.nlm.nih.gov/articles/PMC6699529/
- Brennan, "Generalizability Theory", NCME Module 14 — https://ncme.org/wp-content/uploads/2025/10/Module-14-Generalizability-Theory-Brennan-Winter-1.pdf
- Cogn-IQ, Generalizability Theory — https://www.cogn-iq.org/learn/theory/generalizability-theory/

## Why it exists

"Unlike classical test theory, which aggregates all error into a single component, G-theory
**decomposes observed-score variance into discrete variance components** attributable to multiple
facets — such as raters, items, sessions, or other design elements — and their interactions."

CTT gives you one number (reliability) and no diagnosis. G-theory tells you **where the noise is**,
and therefore what to spend money on.

## Facets

A **facet** is a source of measurement error you deliberately model: raters, items, occasions,
prompts. G-theory "offers a way to quantify the variance contributed by factors such as rater bias,
relative difficulty of items or stations, and other influences."

**Object of measurement** (usually persons; **for us, models**) is not a facet — its variance is the
signal, not the error.

## G-study vs D-study

**G-study**: run first. "Its purpose is to estimate, from data collected under a chosen design, the
magnitude of every variance component — to find out how much each facet and interaction contributes
to error." Estimated by ANOVA-based methods (or REML). Answers: *how much of the total variability
is due to each facet?*

**D-study**: "translates the variance components of a G-study into actionable design
recommendations ... project how reliability would change under different measurement conditions —
for example, with more items, more raters, or more occasions."

## The design for our platform

Crossed design `m × i × j` — models (m) × items/scenarios (i) × judges (j). Total variance
decomposes into 7 components:

```
σ²_total = σ²_m + σ²_i + σ²_j + σ²_mi + σ²_mj + σ²_ij + σ²_mij,e
```

Interpretation for us:
- `σ²_m` — **signal**. Real differences between model variants.
- `σ²_i` — some scenarios are just harder. Harmless for ranking (constant across models).
- `σ²_j` — judge severity/leniency. Harmless for *ranking* if fully crossed, fatal for *absolute*
  scores.
- `σ²_mi` — **model × scenario interaction**. Different models win on different scenarios → this is
  the "benchmark lottery" showing up as a variance component.
- `σ²_mj` — **model × judge interaction**. A judge systematically favours a particular model. This
  is the dangerous one (self-enhancement bias for a judge from the same family).
- `σ²_ij` — scenario × judge.
- `σ²_mij,e` — residual + run-to-run sampling noise (temperature).

## Coefficients

**Generalizability coefficient** `Eρ²` — for **relative** decisions (ranking):
```
Eρ² = σ²_m / (σ²_m + σ²_rel)     where σ²_rel = σ²_mi/n_i + σ²_mj/n_j + σ²_mij,e/(n_i·n_j)
```

**Dependability coefficient** `Φ` — for **absolute** decisions (does this model clear a bar of 4.0?):
```
Φ = σ²_m / (σ²_m + σ²_abs)
σ²_abs = σ²_rel + σ²_i/n_i + σ²_j/n_j + σ²_ij/(n_i·n_j)
```

`Φ ≤ Eρ²` always — absolute decisions are strictly harder, because now judge severity and scenario
difficulty count against you.

**Our platform needs Φ, not Eρ²**, because the user's requirement is a "SAME BASELINE" — an
absolute, cross-model, cross-release comparable score, not just a within-batch ranking.

## D-study levers

The D-study formulas above show `n_i` and `n_j` in the denominators. Whichever variance component is
largest tells you where to spend:
- Large `σ²_mi` → add **scenarios** (adding judges won't help)
- Large `σ²_mj` or `σ²_j` → add **judges** / fix the rubric
- Large residual → add **runs** per cell (or lower temperature)

## Relevance to companion-eval

This is arguably the single highest-value framework on the list. One crossed G-study
(models × scenarios × judges, a few runs each) yields a numeric answer to "should we buy more
scenarios or more judges", and yields `Φ` per dimension, which is exactly the "is this dimension
trustworthy" number.
