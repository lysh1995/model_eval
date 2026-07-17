---
title: "The Chameleon's Limit: Investigating Persona Collapse and Homogenization in Large Language Models"
url: https://arxiv.org/abs/2604.24698
authors: Yunze Xiao, Vivienne J. Zhang, Chenghao Yang, Ningshan Ma, Weihao Xuan, Jen-tse Huang
year: 2026
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# The Chameleon's Limit: Persona Collapse and Homogenization

arXiv:2604.24698v1.

**Status: the direct prior art for our "homogenization across characters" failure mode, and the strongest evidence that CHARACTER-COHORT is a mandatory unit of analysis.**

## Abstract

Identifies **"Persona Collapse"**: LLM agents assigned distinct profiles converge into narrow behavioral modes. Proposes a **geometric framework** measuring **Coverage**, **Uniformity**, and **Complexity**. Evaluates 10 LLMs on personality simulation, moral reasoning, and self-introduction. Collapse occurs across two axes: dimensions and domains.

> **"Surprisingly, models with highest per-persona fidelity produce the most stereotyped populations."**

**That sentence is the entire argument for our platform in one line.** A model can win every per-character evaluation and still be the worst model in the cohort, because per-character fidelity and cross-character diversity are *anti-correlated*. No amount of per-response or even per-conversation evaluation can detect this. It is only visible at the population level.

## Metric definitions

**Coverage:** "The fraction of human reference neighborhoods reached by at least one model-generated point via k-nearest-neighbor hyperspheres" (human baseline from Twin-2K-500, n=2,058).

**Uniformity (Hopkins Statistic):** compares nearest-neighbor distances of personas against random samples. **~0.5 = uniform; →1.0 = clustering; →0 = over-regular spacing.**

**Complexity (Local Intrinsic Dimensionality, LID):** whether variation is genuinely high-dimensional.
> LID = −(1/k Σ log(rᵢ/r_k))⁻¹, where rᵢ = distances to nearest neighbors.

## Models (10)

**General-purpose:** Llama-3.1-8B-Instruct, Qwen3-4B, Qwen3-30B-A3B, Qwen3-32B, Claude-Haiku-4.5, MiniMax-M2
**Role-play optimized:** CoSER-Llama-8B, CoSER-Qwen-32B, HER-32B, MiniMax-M2-Her

## Tasks

- **BFI-44:** 44 personality items (5-point Likert)
- **Moral Reasoning:** 131 ethical scenarios (5-point)
- **Self-Introduction:** open-ended generation (3 samples per persona)

## KEY NUMBERS

### Higher fidelity → greater stereotyping

Models achieving ρ > 0.9 produced **Cohen's d > 6** between High/Low target groups — far exceeding the **d = 2 "very large"** threshold in human research:

| Model | ρ (fidelity) | d (polarization) |
|-------|--------------|------------------|
| MiniMax-M2 | 0.95 | **15.7** |
| Qwen3-32B | 0.94 | 13.7 |
| Claude-Haiku-4.5 | 0.95 | 13.7 |

The models aren't playing characters; they're playing *caricatures*. d=15.7 means the "high extraversion" and "low extraversion" personas are separated by 15 standard deviations — no human population looks like this.

### Coverage vs Complexity gap — no model approaches humans (Coverage=1.0, LID=14.4)

| Model | Coverage | LID |
|-------|----------|-----|
| Qwen3-4B | 0.80 | 7.3 |
| Claude-Haiku-4.5 | 0.71 | 5.4 |
| CoSER-Llama-8B | 0.16 | 4.6 |
| MiniMax-M2-Her | 0.06 | 22.3 |

### Response vocabulary collapse (effective Likert scores, inverse Simpson, max=5)

| Model | BFI EffL | Moral EffL |
|-------|----------|------------|
| CoSER-Llama-8B | 1.36 | 4.27 |
| HER-32B | 2.52 | 1.27 |

### Attribute mention rates (self-introduction) — universal truncation hierarchy

Gender **91%** · Country **90%** · Political ideology **62%** · Age **36%** · Social class **27%**

### Demographic stereotyping (moral reasoning) — incremental R², dominant attribute compression

| Model | Dominant Attribute | Dom% |
|-------|-------------------|------|
| Claude-Haiku-4.5 | Gender | 57% |
| Qwen3-4B | Social Class | 59% |
| MiniMax-M2 | Balanced | 25% |

### Template homogenization

- **Claude-Haiku-4.5: 29% of self-introductions shared an identical template skeleton** despite 73% attribute mention rate (highest among models).
- **MiniMax-M2-Her: 83% of linguistic variation was stochastic noise**; intra-persona similarity (0.75) **below** inter-persona random pairs.

That last one is a devastating and very reusable diagnostic: **if intra-persona similarity < inter-persona similarity, the persona is doing no work at all.** This is a cheap, computable check we should run on our 95 characters immediately.

## Cross-domain reversal — collapse is domain-specific

**CoSER-Llama-8B:** BFI-44 most degenerate (Coverage=0.16, Hopkins=0.91); Moral Reasoning most diverse (LID=45.3, Hopkins=0.48).
**Qwen3-4B:** BFI-44 highest Coverage (0.80); Moral Reasoning collapsed (EffL=1.20, **17/131 zero-variance items**).

⇒ You cannot measure homogenization on one axis and generalize. Our eval must probe multiple behavioral domains per character.

## Training pipeline effects — RLHF/roleplay-tuning makes it WORSE

**Qwen3-32B → CoSER-Qwen-32B (SFT) → HER-32B (RL):**

| Stage | Coverage | LID | Cohen's d |
|-------|----------|-----|-----------|
| Base | 0.64 | 5.1 | 13.7 |
| +SFT | 0.56 | 4.6 | 9.6 |
| +RL | **0.49** | 6.9 | 6.7 |

**MiniMax-M2 → MiniMax-M2-Her (RL):**
- Coverage: **0.55 → 0.06**
- LID: 6.5 → 22.3
- Persona fidelity (ρ): **0.95 → 0.41**

> RL increased geometric complexity but pushed population away from human behavioral space.

**Roleplay-tuned models get monotonically worse at cohort diversity.** This is precisely the model class our platform exists to evaluate, and precisely the failure their own per-character benchmarks won't show.

## Extended reasoning is ineffective

Qwen3-32B thinking vs non-thinking produced **"identical item-level metrics and fidelity"** across both BFI and moral reasoning — "suggesting collapse is **weight-encoded rather than reasoning-recoverable**."

## Relevance to companion-eval-platform

- **Mandates the character-cohort unit of analysis.** Coverage/Uniformity/Complexity are computed over the *population of 95 characters*, and are undefined for a single character. Our 95-character × 11-model grid is exactly the right shape to compute these.
- **Directly reusable metrics**: Hopkins statistic, LID, Coverage vs a human reference, effective-Likert (inverse Simpson), template-skeleton overlap %, and the intra- vs inter-persona similarity check.
- **The fidelity/diversity anti-correlation is the headline finding to replicate.** If it holds on our data, it's a strong argument for the platform's existence: single-character leaderboards actively mislead.
- Their study is **static/one-shot** (questionnaires, self-intros). **Our 100-turn dialogues let us ask a question they cannot: does the cohort collapse FURTHER with turn depth?** Compute Coverage/Hopkins at turn 10 vs 50 vs 90. If characters converge as conversations lengthen, that is a novel result and it unifies persona drift (within-character, over turns) with homogenization (across-character, at a turn) as two projections of one phenomenon.
