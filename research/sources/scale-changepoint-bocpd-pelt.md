---
title: "Changepoint detection — BOCPD (Adams & MacKay) and PELT"
url: https://arxiv.org/abs/0710.3742
org: Adams & MacKay (Cambridge); Killick, Fearnhead & Eckley (Lancaster)
year: 2007, 2012
type: paper
accessed: 2026-07-16
topic: production-scale
---

# Changepoint detection algorithms

## BOCPD — Bayesian Online Changepoint Detection (Adams & MacKay, 2007)

**Core idea:** "maintain a posterior distribution over the current **run length**,
meaning the number of observations since the most recent change-point."

BOCPD "recursively computes the posterior probability of a change point occurring after
each new data point, making it particularly suitable for small samples or scenarios
requiring probabilistic interpretation."

### Complexity
- Space and time complexity: **O(T^2)** naive
- "Practical implementations **prune negligible posteriors** and thus achieve
  **amortized near-linear time**"

### Key parameter
The **hazard rate (lambda)** — the prior probability of a changepoint at each step.
A constant hazard `H = 1/lambda` corresponds to a geometric prior on run length; e.g.
lambda = 250 means "expect a changepoint every 250 observations."

### Output
A full posterior over run length, not a binary alarm. This is genuinely useful for a
monitoring UI: you can render "probability a changepoint occurred at time t" as a
heatmap rather than a threshold crossing, which is much better for triage.

## PELT — Pruned Exact Linear Time (Killick et al., 2012)

"The pruning strategy, known as the **penalised exact linear time (PELT)** algorithm,
introduced in **2012**, is a popular method of reducing the computational cost in
changepoint detection problems solved via dynamic programming."

- "PELT controls overfitting by introducing a **penalty term** (e.g. **Bayesian
  Information Criterion / BIC**) and achieves **linear time complexity** through
  dynamic programming with pruning."
- **O(n)** expected under the assumption that the number of changepoints grows linearly
  with n; exact (finds the global optimum of the penalized cost), unlike binary segmentation.
- Standard penalty choices: **BIC/SIC = log(n)** per changepoint, **AIC = 2**, or MBIC.
  The penalty is the sole knob controlling how many changepoints you get — too low and
  you segment noise.

## Relationship between the two

"In BOCPD, the **hazard rate parameter (lambda)** plays a role analogous to the
**penalty parameter in PELT**. The penalty term balances model complexity against
goodness of fit to prevent overfitting."

## Fit for a 50M/day eval platform

Both are **retrospective/online segmentation on an aggregate time series**, not on raw
events. The natural application:
- Run PELT **offline/nightly** over hourly aggregate series (mean judge score per
  character per language) to produce "here is when the regression started" for incident
  review. This is a *post-hoc explanation* tool — answering "when did this break?" after
  an alert, which is the question on-call actually asks.
- BOCPD **online** as an alternative to EWMA/CUSUM when you want a probabilistic
  changepoint readout rather than a threshold crossing.

Neither is a good primary alerting primitive at this scale (PELT is batch; BOCPD needs
a per-series model and careful hazard tuning across thousands of series), but PELT for
incident forensics is high-value and cheap — it runs on ~24-8760 points per series.
