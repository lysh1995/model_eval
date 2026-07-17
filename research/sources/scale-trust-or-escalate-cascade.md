---
title: "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement (Cascaded Selective Evaluation)"
url: https://arxiv.org/html/2407.18370v1
org: ICLR 2025 (conference paper)
year: 2025
type: paper
accessed: 2026-07-16
topic: production-scale
---

# Cascaded Selective Evaluation

**Why this matters for us:** this is the canonical, peer-reviewed formulation of the
tiered-judge idea our brief needs. It gives a *provable* human-agreement guarantee
rather than a hand-tuned "escalate if unsure" heuristic — which is what makes a tiered
design defensible when someone asks "how do you know the cheap tier isn't lying to you?"

## Core framework — Selective Evaluation

The principle: **LLM judges should abstain when uncertain.** Given a confidence measure
`c_LM` and threshold `λ`, the system evaluates only when:

> `c_LM(x) ≥ λ, otherwise abstain`

The guarantee provided:

> `P(LLM preference agrees with human | LLM evaluates x) ≥ 1−α` with probability at least `1−δ`

This is a **conditional** guarantee — it holds over the subset the judge chose to score,
not the whole population. That is the key trade: you buy agreement with **coverage**.

## Confidence calibration — "Simulated Annotators"

Rather than using predictive probability or verbalized confidence (both poorly
calibrated), the paper simulates N diverse annotators via K-shot prompting:

> `c_LM(x) = max_y (1/N) Σ p_LM(y|x; in-context examples from annotator j)`

**Calibration results (Table 1, GPT-4-turbo on AlpacaEval):**

| Metric | Simulated Annotators | Baseline |
|---|---|---|
| Expected Calibration Error | **0.106** | 0.217 |
| AUROC | **0.718** | 0.642 |

> Reduces calibration error by 50%.

Notably: **for weaker models (Mistral-7B), Simulated Annotators achieves better
calibration than GPT-4 using standard methods.** This is the load-bearing result for a
cheap-tier judge — a small model with good calibration can be trusted to know when to
escalate.

## Threshold selection — fixed-sequence testing

The algorithm searches for `λ̂` satisfying:

> `R̂⁺(λ) = sup{R: P(Bin(n(λ),R) ≤ ⌈n(λ)R̂(λ)⌉) ≥ δ} ≤ α`

Testing proceeds **from highest to lowest λ** until the upper confidence bound of the
disagreement risk falls below target `α`. (Binomial tail bound — statistically rigorous,
cheap to compute, and re-runnable per evaluator version.)

## Cascade architecture

**Models used, in escalation order:**
1. Mistral-7B-instruct-v0.2 (base tier)
2. GPT-3.5-turbo (escalation 1)
3. GPT-4-turbo (escalation 2)

**Algorithm:** For each instance, attempt evaluation starting with Mistral-7B. If
`c_M1(x) < λ₁`, escalate to GPT-3.5. If `c_M2(x) < λ₂`, escalate to GPT-4.

## Headline results

**ChatArena (target agreement 85%):**

| Metric | Value |
|---|---|
| Human agreement achieved | **85.8%** (empirical) |
| Guarantee success rate | 91.0% (across 1000 runs) |
| Coverage | **63.2%** of test set |
| Evaluator composition | 23.7% Mistral-7B / 58.8% GPT-3.5 / **17.5% GPT-4** |
| **Cost savings** | **78.5% reduction vs. GPT-4 baseline** |

**TL;DR dataset (target agreement 90%):**
- Coverage: 55.7%
- Guarantee success rate: 90.8%
- Majority of evaluations: Mistral-7B (28.3%) or GPT-3.5 (28.2%)

**Auto-J (target agreement 80%):**
- GPT-4 alone: **63.2%** human agreement *without* guarantees
- Cascaded method: **80%** guaranteed agreement
- Coverage: 42.9%

> This last row is the most striking result: the cascade is not just cheaper than
> GPT-4 — on Auto-J it is substantially *more accurate* (80% vs 63.2%), because
> abstention removes the cases where the judge is unreliable.

## Abstention policy is meaningful, not a surface heuristic

The method abstains based on human-perceived subjectivity:

| Subset | Inter-annotator agreement |
|---|---|
| Abstained samples | 81.5% |
| Evaluated samples | 90.2% |

Difference statistically significant (**p < 1e-8**). Critically:

> No reliance on length ratio or token overlap.

The judge abstains exactly where *humans also disagree with each other* — i.e. the
abstention set is genuinely ambiguous, not just "long" or "weird".

## Cost caveat — read this carefully

Relative API costs (Table 5, ChatArena):

| Configuration | Relative cost |
|---|---|
| GPT-4 only (N=1) | 1.000 |
| Cascaded Selective Evaluation (N=5) | **2.849** |

**This looks contradictory against the 78.5% figure and must not be misquoted.** The
78.5% saving is the cascade *routing* benefit (only 17.5% of items reach GPT-4). The
2.849 figure is the cost when running **N=5 simulated annotators** for calibration — the
confidence-estimation step multiplies calls by N. The paper's own reconciliation:

> Despite higher simulations, cascaded method achieves "over 40% cost reduction vs.
> GPT-4" while guaranteeing 85% agreement with higher coverage.

**Practical takeaway for our design:** the honest, defensible number is **~40–78% cost
reduction depending on how many simulated annotators you run.** Budget the cascade at
**~40% saving** if we adopt Simulated Annotators for calibration; the 78.5% figure
assumes calibration is free. Do not put 78.5% in a cost model that also uses N=5.

## Applicability to our platform

- **Fits:** the tiered judge (Haiku → Sonnet → Opus) maps directly onto the
  Mistral → GPT-3.5 → GPT-4 cascade. The escalation rate (17.5% to the top tier) is a
  reasonable planning prior for our Opus tier.
- **Caution 1 — coverage:** 42–63% coverage means the cascade *declines to score* a
  large share of traffic. For monitoring, abstention is not free: an abstained item is
  a missing data point. We must either (a) treat abstention rate as a monitored metric
  in its own right (a spike in abstention IS a regression signal), or (b) route
  abstentions to human review. Do not silently drop them.
- **Caution 2 — pairwise preference:** the paper's task is *pairwise preference
  agreement* (which of two responses is better). Our roleplay quality scoring may be
  pointwise/rubric-scored, where "human agreement" is a weaker notion. The calibration
  machinery transfers; the specific numbers may not.
- **Caution 3 — model generation:** results are on Mistral-7B / GPT-3.5 / GPT-4.
  Modern Haiku 4.5 is far stronger than Mistral-7B-instruct-v0.2, so our base tier
  should have *higher* coverage and a *lower* escalation rate than 17.5% — the paper's
  numbers are a conservative floor for us.
