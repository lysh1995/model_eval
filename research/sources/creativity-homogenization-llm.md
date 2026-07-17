---
title: "LLM homogenization / mode collapse of creative output — evidence cluster"
urls:
  - https://arxiv.org/html/2402.01536v2  # Homogenization Effects of Large Language Models on Human Creative Ideation
  - https://www.sciencedirect.com/science/article/pii/S294988212500091X  # Homogenizing effect of LLMs on creative diversity
  - https://arxiv.org/abs/2410.04265  # Creativity Index (alignment -30.1%)
year: 2024-2026
type: evidence cluster
accessed: 2026-07-16
topic: creativity-measurement
---

# Homogenization / mode collapse — the population-level failure mode

## Mechanism

- Optimization for reliable adherence to human preferences forces models into **mode collapse**: the probability distribution converges on a narrow set of safe, homogenized attractor states.
- **KL-divergence regularization** in standard alignment algorithms penalizes the long tail of diverse outputs to prioritize the majority opinion.
- Reward models show inherent bias toward **verbalized confidence**, incentivizing suppression of epistemic doubt.
- Instruction tuning + RLHF produce "safe"/aligned responses; these processes "can inadvertently reduce creativity and encourage homogenized responses."

## Empirical evidence

- **Doshi & Hauser / related (arXiv 2402.01536)**: Writers exposed to GPT-4-generated ideas produced **better and more enjoyable stories** than those writing alone — **but these LLM-inspired stories were more similar to each other** than stories written by humans alone. *Per-item quality up, population diversity down.*
- Individuals using InstructGPT produced short essays "more similar in terms of lexical and content diversity" than those written without LLM support.
- **Creativity Index paper**: "Alignment reduces the Creativity Index of LLMs by an average of **30.1%**" at the verbatim level.
- General finding: "Post-training alignment actively reduces diversity, and while we lack reliable ways to push diversity up, current alignment pipelines actively push it down."

## THE key structural insight for our platform

The Doshi/Hauser result is the whole argument for a population-level metric tier:

> **Every per-response metric got BETTER while the thing we actually care about got WORSE.**

Quality per story ↑, similarity across stories ↑ (diversity ↓). No amount of per-response scoring — judge or automatic — can detect this. Homogenization is **only measurable across a set of responses**, and only when those responses come from the *same prompt* (or matched prompts).

Concretely: a model that answers every "surprise me" roleplay turn with a beautifully-written but identical trope will score well on every per-response rubric and is exactly the regression we most need to catch in a companion product, where users see many turns from the same character.

## Measurement design implied

Sample **k ≥ 10 independent generations at temperature per fixed scenario**, then measure:
- pairwise similarity across the k (compression ratio / self-repetition / self-BLEU)
- how often the same trope/entity/opening appears across the k

This is a *distributional* statistic. It has no per-response value. Budget for it explicitly — it multiplies generation cost by k while adding zero judge cost.
