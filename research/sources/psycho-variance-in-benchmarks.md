---
title: "Quantifying Variance in Evaluation Benchmarks"
url: https://arxiv.org/abs/2406.10229
authors: Lovish Madaan, Aaditya K. Singh, Rylan Schaeffer, Andrew Poulton, Sanmi Koyejo, Pontus Stenetorp, Sharan Narang, Dieuwke Hupkes
year: 2024
type: paper
accessed: 2026-07-16
topic: psychometrics
---

# Quantifying Variance in Evaluation Benchmarks

## Core framing

Verbatim: "we rarely quantify the variance in our evaluation benchmarks, **which dictates whether
differences in performance are meaningful**."

## Variance metrics examined

1. **Seed variance** — performance fluctuations "across initialisations" (retraining with different
   random seeds).
2. **Monotonicity** — how consistently model performance improves over the course of training. A
   non-monotonic benchmark is a noisy benchmark.

## Findings

- **Task formatting matters**: "framing choice tasks (like MMLU) as completion tasks, can often
  reduce variance for smaller scale (~7B) models."
- **Psychometric methods disappointed**: approaches borrowed from psychometrics — "item analysis and
  item response theory" — "struggle to meaningfully reduce variance."
- **Practical recommendation**: practitioners should "carefully factor in variance when comparing
  models" rather than assuming observed performance differences are meaningful.

## The caveat worth carrying

This is the most important **counterweight** to the tinyBenchmarks / IRT enthusiasm. IRT is good at
*efficiency* (estimating the same score with fewer items) but this paper finds it does **not** fix
*variance*. Seed/run variance is irreducible by item selection — you reduce it by running more
seeds, not by picking cleverer items.

Implication for us: IRT helps us shrink the scenario bank; it does **not** license us to skip
multiple runs per cell. These are orthogonal budget lines.

## Relevance to companion-eval

Direct analogue of seed variance for us is **run-to-run sampling noise at temperature > 0**. Before
any leaderboard ships we must measure: re-run the *same* model on the *same* scenarios with
different sampling seeds, and compute the spread. That spread is the **noise floor** — no score
difference smaller than it is reportable, regardless of how many scenarios we have.

Monotonicity has an analogue too: score across a known-ordered set of model variants (e.g. a
deliberately degraded model, base, and a known-better model). If our dimension does not order those
correctly, the dimension is broken — this is a cheap **criterion-validity** check.
