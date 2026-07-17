---
title: "tinyBenchmarks: evaluating LLMs with fewer examples"
url: https://arxiv.org/html/2402.14992v1
authors: Felipe Maia Polo, Lucas Weber, Leshem Choshen, Yuekai Sun, Gongjun Xu, Mikhail Yurochkin
year: 2024
venue: ICML 2024
type: paper
accessed: 2026-07-16
topic: psychometrics
---

# tinyBenchmarks: evaluating LLMs with fewer examples

## IRT model formulation

Two-parameter **multidimensional** IRT model. Probability that LLM `l` answers example `i`
correctly:

```
p_{il} = 1 / (1 + exp(−α_i^⊤ θ_l + β_i))
```

- `θ_l` — latent **ability** vector of model `l`
- `α_i` — **discrimination** vector; indicates which ability dimensions item `i` requires
- `β_i` — **difficulty** / bias term for item `i`

## gp-IRT estimator

Generalized performance-IRT combines a direct sampling estimate with the IRT model prediction via
convex weighting:

```
Z^{gp-IRT}_{jl} ≜ λ · Σ_{i∈Î_j} w_i Y_{il} + (1−λ) · Ẑ^{p-IRT}_{jl}
```

Weight `λ` depends on IRT model bias `b̂` and the variance `σ̂²` of the first estimator:

```
λ = b̂² / (σ̂²/|Î_j| + b̂²)
```

Intuition: trust the raw sample more when you have many items (`|Î_j|` large) or when the IRT model
is biased; trust IRT more when items are scarce.

## Anchor point selection

- Cluster examples with **K-Means on embeddings derived from model correctness patterns** across a
  set of training LLMs (i.e. items are represented by *which models get them right*).
- Pick the representative example nearest each centroid to compose the evaluation subset.
- Assign each anchor a weight = "the fraction of points in the full scenario assigned to each
  cluster."

Alternative strategies compared: stratified random sampling, correctness-based clustering,
IRT-based clustering of example representations. IRT-based anchors were the most robust /
generalizable.

## Results / thresholds

- **100 curated examples per scenario** achieves approximately **2% average performance estimation
  error** across benchmarks.
- **MMLU**: 14,000 → 100 examples (**140× reduction**) at that error level.
- **Open LLM Leaderboard**: target error at just **30 examples per scenario** (**160× reduction**).

## Estimation details

IRT parameters estimated via **variational inference** using hierarchical Bayesian models with
standard normal and gamma priors. Latent dimension selected by validation over {2, 5, 10, 15}.

## Relevance to companion-eval

Directly applicable: our scenarios/prompts are "items". Fitting IRT over a bank of scenarios gives
us (a) item difficulty and discrimination, letting us drop items that discriminate nothing, and
(b) a principled way to shrink the eval set without losing the ability to rank models. Item
discrimination `α_i` is the single most useful diagnostic for "is this prompt earning its place".
