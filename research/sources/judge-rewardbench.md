---
title: "RewardBench: Evaluating Reward Models for Language Modeling"
url: https://arxiv.org/abs/2403.13787
authors:
  - Nathan Lambert
  - Valentina Pyatkin
  - Jacob Morrison
  - LJ Miranda
  - Bill Yuchen Lin
  - Khyathi Chandu
  - Nouha Dziri
  - Sachin Kumar
  - Tom Zick
  - Yejin Choi
  - Noah A. Smith
  - Hannaneh Hajishirzi
year: 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# RewardBench: Evaluating Reward Models for Language Modeling

## Abstract (verbatim opening)

> Reward models (RMs) are at the crux of successfully using RLHF to align pretrained models to human preferences, yet there has been relatively little study that focuses on evaluation of those models.

## Methodology

A benchmark of **prompt–chosen–rejected trios** across categories:

- **Chat** — general conversational preference
- **Chat Hard** — subtle distinctions, adversarial/trick pairs
- **Safety** — refusal behavior and safe completions
- **Reasoning** — code and math correctness

Evaluates reward models trained by different methods: **direct MLE training of classifiers**, and **implicit reward modeling via DPO**. LLM-as-a-judge models are also scored on the same trios, making it one of the few places where **generative judges and trained reward models are compared head-to-head on identical data**.

## Key findings

- Documents **"propensity for refusals, reasoning limitations, and instruction following shortcomings"** of various reward models.
- Reward models score high on **Chat** and much lower on **Chat Hard** and **Reasoning** — the same pattern JudgeBench found for LLM judges. **Easy preference is solved; hard discrimination is not.**
- The **Chat Hard** category is the informative one and the one that most resembles our problem: distinguishing two responses that are both fluent and plausible. Companion variants of the same character will differ *subtly*, not obviously — every comparison we run is a "Chat Hard" comparison.

## Relationship to our platform

- **RewardBench is the standard shopping catalogue for picking a reward model** as a cheap panel member or first-stage cascade judge. Skywork-Reward (Gemma-2-27B) — top-tier on RewardBench — also **beat GPT-4o-as-judge by 13.4pp on JudgeBench** (64.3% vs 50.9%). Small trained RMs are competitive with frontier judges at a fraction of the cost/latency.
- **Important caveat, later established by JudgeBench:** RewardBench performance **does not predict JudgeBench performance well**. RewardBench's pairs are largely distinguishable by *preference/style*; JudgeBench's require *correctness*. A model can top RewardBench by learning style preferences. **So: do not select our judge on RewardBench alone.** It measures preference alignment, which is only one of our dimensions — and it is the dimension most contaminated by style bias.
- RMs are **pointwise scorers by construction** (they emit a scalar), which makes them naturally suited to our cross-model comparability requirement — a scalar on a fixed scale from a frozen checkpoint is exactly the comparable, traceable artifact we want. Their weakness is that they give **no rationale**, so they cannot be audited or debugged, and they cannot be pointed at a *custom* rubric (character fidelity) without retraining.

## Practical role in our stack

Best used as:
1. A **cheap first-stage judge** in a Trust-or-Escalate cascade.
2. A **family-disjoint panel member** — an RM's "own generations" never appear among our variants, so it is structurally immune to self-preference (see Panickssery).
3. A **fast regression tripwire** — cheap enough to run on every commit, with the expensive generative judge reserved for confirming a flagged regression.

Not suitable as the *sole* judge: no rationale, no custom rubric, and RewardBench-topping RMs are known to be style-confounded.
