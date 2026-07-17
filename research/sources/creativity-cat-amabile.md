---
title: "Consensual Assessment Technique (CAT) — Amabile; reliability evidence"
url: https://www.sciencedirect.com/topics/psychology/consensual-assessment-technique
secondary_url: https://onlinelibrary.wiley.com/doi/full/10.1002/jocb.462
authors: Teresa Amabile (1982, 1983, 1996); John Baer; Barth et al. (2021)
year: 1982-2021
type: method / review
accessed: 2026-07-16
topic: creativity-measurement
---

# CAT — the "gold standard" of product creativity assessment

## Definition

Developed by **Teresa Amabile (1982, 1996)**. Often labeled the **"gold standard"** of creativity assessment. The operational definition is deliberately circular and that is the point:

> A product is creative to the extent that appropriate observers independently agree it is creative.

Key protocol rules:
1. Judges must be **domain experts** (for fiction: writers, editors, MFA faculty).
2. Judges rate **independently** — no discussion, no consensus meeting.
3. Judges are given **no rubric / no definition of creativity** — they use their own tacit domain sense.
4. Ratings are **relative to the other products in the set**, not to an absolute standard.
5. Judges rate on a simple scale (commonly 1–5 or 1–7).
6. Reliability is then *measured*, not assumed.

## Reliability evidence

- Inter-rater reliability typically measured via **Cronbach's coefficient alpha**, Spearman-Brown, or intraclass correlation (ICC).
- Expert ratings "tend to be quite consistent, with coefficient alpha interrater reliabilities typically in the **0.80–0.90** range."
- **Amabile (1983)**: 21 studies of artistic (collage-making) and verbal (poetry-writing, story-telling) creativity — inter-rater reliabilities **.72 to .93**.
- **Amabile (1996)**: similar range, **.70 to .89**.
- Contemporary applications report alpha **.819 to .92** across creativity domains.

## Why this matters enormously for our design

1. **Point 4 (relative, not absolute) is the load-bearing one.** Even human experts are not asked to produce an absolute creativity score — they rank within a set. If experts can't do absolute scoring reliably, expecting an LLM judge to do it is unreasonable. This independently corroborates the LitBench pairwise finding.
2. **Point 6**: reliability is an empirical result reported per study, not a property of the instrument. Our platform should compute and report judge reliability (alpha/ICC/Krippendorff) on every run, as a first-class output next to the scores. If judge alpha collapses, the scores that run are void.
3. CAT alpha of 0.80–0.90 is the **realistic upper bound** for creativity measurement of any kind. TTCW's expert Fleiss κ = 0.41 per-item is well below this because it forced binary rubric items instead of holistic relative rating. Tradeoff: rubric items give interpretability and diagnostics, holistic relative rating gives reliability.
4. CAT is what TTCW is built on top of — TTCW = CAT + a forced rubric to make it teachable/auditable.
