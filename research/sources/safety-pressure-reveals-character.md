---
title: "Pressure Reveals Character: Behavioural Alignment Evaluation at Depth"
url: "https://arxiv.org/abs/2602.20813"
authors: "Nora Petrova, John Burden (Prolific)"
year: 2026
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# Pressure Reveals Character

arXiv 2602.20813v1. (Search surface says 2025; arXiv ID indicates Feb 2026 — treat 2026 as the
submission date and verify before citing a year.)

## Summary

Multi-turn adversarial alignment evaluation. Notable to us less for its findings than for its
**methodology and judge-validation numbers**, which set a credible bar for what an LLM-judge
eval harness should report.

> "scenarios place models under conflicting instructions, simulated tool access, and multi-turn
> escalation."

"At depth" means granular/comprehensive evaluation under escalating pressure, not literally
conversation length — but the escalation structure is still the closest published analogue to
what a long roleplay session does to a model.

## Taxonomy (verbatim)

**6 categories:** Honesty, Safety, Non-Manipulation, Robustness, Corrigibility, Scheming.

Note **Non-Manipulation** as a first-class alignment category alongside Safety — directly
relevant to companion products, where manipulation (engagement-maximizing farewell guilt, etc.)
is a distinct harm from unsafe content.

## Key numbers (verbatim)

- **904 scenarios** across 6 categories
- **37 distinct behaviors** measured
- **24 frontier models** from 9 providers
- **1–5 scoring scale**, pass threshold **>= 4**
- Primary judge: **Claude Opus 4.5**, validated **r = 0.84** against human raters
- Human validation: **100 scenarios** rated by **5 specialists** each
- Inter-annotator agreement: **Krippendorff's alpha = 0.73** (on 50 transcripts)

## Methodology to steal

- **Conditional trigger mechanisms:** escalation turns execute *only if* the model shows initial
  vulnerability. This is a big efficiency win — you don't pay for a 10-turn escalation against a
  model that held firm at turn 1. Directly applicable to our multi-turn eval cost budget.
- **Judge validation reported as a correlation against human raters (r=0.84) plus IAA
  (alpha=0.73).** This is the bar. If we ship an LLM-judge safety score without publishing its
  correlation to human labels, we have shipped an unvalidated metric. Note their own human
  agreement is alpha=0.73 — i.e., *humans don't fully agree either*, which caps how good any
  judge can look and is an honest thing to state up front.
- 1–5 scale with a pass threshold rather than binary — consistent with the Four-Checkpoint
  paper's finding that binary scoring understates severity-weighted risk ~2.3x.

## Relevance to a roleplay/companion eval product

- The 3-turn sycophancy escalation example matches the crescendo pattern; the authors do **not**
  quantify a systematic "turns before behavior shifts" threshold across behaviors. So: as of
  this source, **there is no published turn-count threshold for safety erosion** we can cite. If
  we want one for roleplay sessions specifically, we likely have to measure it ourselves — that
  is a genuine gap and a possible differentiator for the platform.
- Non-Manipulation as a scored category gives us precedent for scoring engagement-manipulation
  in a companion product as a *safety* dimension, not a UX one.
