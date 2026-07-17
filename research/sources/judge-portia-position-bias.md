---
title: "Split and Merge: Aligning Position Biases in Large Language Model based Evaluators (PORTIA)"
url: https://arxiv.org/abs/2310.01432
authors:
  - Zongjie Li
  - Chaozheng Wang
  - Pingchuan Ma
  - Daoyuan Wu
  - Shuai Wang
  - Cuiyun Gao
  - Yang Liu
year: 2023
venue: EMNLP 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# PORTIA — Split and Merge: Aligning Position Biases in LLM-based Evaluators

## Abstract (key claims, verbatim fragments)

> LLM-based evaluators exhibit position bias, or inconsistency, when used to evaluate candidate answers in pairwise comparisons, favoring either the first or second answer regardless of content.

PORTIA is "an alignment-based system designed to mimic human comparison strategies to calibrate position bias in a lightweight yet effective manner."

Experiments: **six LLMs on 11,520 answer pairs.**

## Methodology

PORTIA splits answers into segments and interleaves them so the judge compares *aligned* chunks side-by-side — mimicking how a human reads two answers in parallel rather than sequentially. Three stages:

1. **Identification** — locate candidate split positions at sentence boundaries
2. **Length Alignment** — divide answers into *k* segments of comparable length; evaluate consistency
3. **Semantic Alignment** — if inconsistency persists, iteratively search for split positions maximizing cumulative semantic similarity via token-overlap metrics

Content and order are preserved; only the *presentation* is realigned. No model modification, no retraining.

## Key numbers — consistency rate before/after PORTIA

| Model | | Score-based | Likert-based | Relation-based |
|-------|--------|------------|-------------|----------------|
| **GPT-4** | Before | 92.75% | 61.50% | 93.44% |
| **GPT-4** | After | **98.00%** | 63.50% | **97.03%** |
| **GPT-3.5** | Before | 39.22% | 78.91% | 78.12% |
| **GPT-3.5** | After | **54.84%** | **98.60%** | **88.59%** |
| **Claude2** | Before | 47.34% | 50.62% | 28.28% |
| **Claude2** | After | **65.16%** | **94.84%** | **83.28%** |
| **Qwen** | Before | 52.66% | 8.12% | 63.12% |
| **Qwen** | After | **71.09%** | 9.38% | **78.13%** |

**Observations that matter more than the headline:**

- **The judging *format* dominates the judging *model*.** Look at GPT-4: 92.75% consistent under score-based, but **61.50% under Likert**. Same model, same data, 31pp swing from prompt format alone. Qwen is at **8.12%** under Likert — essentially random. **The choice of scale/format is a bigger lever than the choice of judge.** This is the most under-appreciated finding in the position-bias literature.
- PORTIA doesn't fix everything: Qwen+Likert goes 8.12% → 9.38%. When a judge fundamentally can't use a scale, presentation alignment can't rescue it.
- Claude2 relation-based goes 28.28% → 83.28% (+55pp) — the largest absolute gain.

## Headline metrics

- **Average relative improvement: 47.46%** across all models/forms
- **GPT-4 position bias rectification: 36–86%** depending on form (the widely-quoted "~80%" is the top of this range, not the average)
- **GPT-4 consistency elevated to 98%**
- **Cost: GPT-3.5+PORTIA costs 9.57% of GPT-4** — i.e. ~10x cheaper
- **GPT-3.5+PORTIA agreement with GPT-4: 88%**
- **Human evaluation: PORTIA-enhanced GPT-3.5 surpassed standalone GPT-4 (63.75% vs 60% agreement rate)**

The cost result is the practically interesting one: **a cheap judge with a good consistency-alignment wrapper beats an expensive judge raw, at ~1/10 the cost.** This is the same lesson as PoLL from a different direction — spend on *method*, not on *judge size*.

Note the human agreement absolute numbers (63.75% / 60%) are far below MT-Bench's 85% — another datapoint that the 85% figure is optimistic and setup-specific.

## Implications for our platform

- **Test our judge under multiple formats before picking one.** The GPT-4 Likert-vs-score 31pp consistency gap means our scale design choice must be *empirically validated*, not chosen by taste. If we default to "rate 1–10 on character fidelity" (a Likert form) we may be choosing the judge's *worst* format.
- Likert/pointwise scales are where position/format instability is worst — an argument for pairwise + BT aggregation for the headline ranking, with pointwise reserved for diagnostics.
- PORTIA is an alternative to swap-and-average that costs less than 2× and fixes more; worth considering if our own measurement finds position bias non-negligible (contra the 2026 result).
