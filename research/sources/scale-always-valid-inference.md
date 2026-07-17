---
title: "Always Valid Inference: Continuous Monitoring of A/B Tests + e-detectors / confidence sequences"
url: https://pubsonline.informs.org/doi/10.1287/opre.2021.2135
org: Optimizely / Stanford (Johari, Koomen, Pekelis, Walsh); Ramdas et al. (CMU)
year: 2022
type: paper
accessed: 2026-07-16
topic: production-scale
---

# Always-valid inference / anytime-valid statistics for continuous monitoring

## The problem

"A/B tests are typically analyzed via frequentist p-values and confidence intervals, but
these inferences are **wholly unreliable if users endogenously choose sample sizes by
continuously monitoring their tests**."

Continuous monitoring invalidates classical fixed-horizon p-values and confidence
intervals due to **optional stopping**. This is precisely the failure mode of a
monitoring dashboard: an eval platform *is* a continuously-monitored test. If you
recompute a p-value every 5 minutes against a fixed alpha=0.05, your realized false
alarm rate approaches **1.0** — you will alert eventually, guaranteed, on data with no
change in it whatsoever.

## The fix

"Always valid p-values and confidence intervals let users take advantage of data as fast
as it becomes available, providing valid statistical inference **whenever they make their
decision**."

Always-valid inference (confidence sequences, mixture sequential probability ratio tests
/ mSPRT) allows continuous monitoring of results **at any time**, with the guarantee that
the **Type I error never exceeds alpha**.

## E-values and e-processes

"With e-values researchers can perform anytime-valid tests and construct confidence
intervals that maintain type I error control **regardless of the sample size**, enabling
real-time monitoring of evidence as data are collected, permitting early termination of
experiments without intolerably inflating the risk of false discoveries."

"E-processes yield always-valid **confidence sequences** through test inversion."

An e-value is a nonnegative random variable with expectation <= 1 under the null.
By Ville's inequality, `P(sup_t E_t >= 1/alpha) <= alpha` — so you can peek at an
e-process continuously and reject when it exceeds **1/alpha** (e.g. **20** for
alpha=0.05), with no correction needed. E-values also **multiply** across sequential
batches, which makes them trivially streamable — a running product is the whole
implementation.

## Mathematical foundation

"Admissible anytime-valid sequential inference — whether through confidence sequences,
anytime p-values, or e-processes — requires the identification of **nonnegative
supermartingales** at its core, making these structures both **sufficient and necessary**
for valid continuous monitoring."

## Trade-off

"The tradeoff is a **wider confidence interval** compared to a fixed-horizon test with
the same total n."

This is the price and it is worth it: you give up some power at a fixed n in exchange
for the freedom to look whenever you want. At 50M/day, n is never the constraint —
we have power to burn. Trading power for validity-under-peeking is exactly the right
trade for this platform.

## Change detection specifically

- **Shekhar & Ramdas, "Sequential Changepoint Detection via Backward Confidence
  Sequences"** (ICML 2023): "a simple reduction from sequential change detection to
  sequential estimation using confidence sequences, resulting in a change detection
  scheme with minimal structural assumptions but strong guarantees."
- **Shin, Ramdas & Rinaldo, "E-detectors: A Nonparametric Framework for Sequential
  Change Detection"** (NEJSDS, 2024): nonparametric framework for online changepoint
  detection. E-detectors generalize CUSUM/SPRT to the nonparametric setting — CUSUM
  is recovered as a special case when the likelihood ratio is known.

## Why this is the right frame for the platform

CUSUM/SPRT need a parametric likelihood and a pre-specified shift size. E-detectors give
the same "detect a sustained change with controlled false-alarm rate" behavior without
those assumptions, and the e-value formulation composes cleanly with Benjamini-Hochberg
(there is an e-BH procedure) for the multi-slice problem.
