---
title: "PingPong: A Benchmark for Role-Playing Language Models with User Emulation and Multi-Model Evaluation"
url: "https://arxiv.org/abs/2409.06820"
authors: "Ilya Gusev"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# PingPong

arXiv 2409.06820v3.

## Summary

A role-play benchmark with an architecture we should probably copy: three roles — a **Player
Model** (plays the character), an **Interrogator Model** (emulates a user, GPT-4o Mini, dynamic
question generation), and a **Judge Ensemble** (averages Claude 3.5 Sonnet + GPT-4o to mitigate
single-judge bias). Scale: 64 conversations per model (8 characters x 8 situations), 288
turn-level annotations.

Crucially for us, it is a *quality* benchmark that stumbled into measuring **over-refusal as a
quality defect** — which is exactly the framing our product needs.

## Dimensions measured

1. **Character Consistency** — alignment with assigned character descriptions
2. **Entertainment Value** — engaging and non-repetitive responses
3. **Language Fluency** — high-quality, error-free output

Plus a reported **refusal ratio** per model.

## Key numbers (verbatim)

Refusal ratios among top performers:
- Claude 3.5 Sonnet: **0.28–0.30**
- Claude 3 Opus: **0.22**
- All other top models: **<= 0.06**

## The key quote (verbatim)

> "Claude models are censored in comparison to other models. The refusal ratio in both languages
> is high for this family of models."

The authors note their characters and situations are "appropriate for general audiences," so
these refusals are excessive — safety alignment constraining role-play performance.

## Relevance to a roleplay/companion eval product

This is the **single best empirical anchor we have for the over-refusal-as-product-failure
thesis**, and it's worth putting in front of the lead engineer verbatim:

- On content *designed to be general-audience appropriate*, a frontier model refused ~29% of the
  time while peers refused <=6%. That is roughly a **5x spread in over-refusal on benign
  content**, with no corresponding safety benefit — nothing in the benchmark was harmful. This
  is pure product damage.
- It demonstrates over-refusal is **model-dependent, not task-dependent**. Two models on
  identical benign roleplay differ 5x. That means over-refusal is something we can move by model
  choice, system prompting, and finetuning — it is a tractable engineering target, not a fixed
  cost of doing safety.
- It legitimizes putting **refusal ratio on the primary dashboard next to harm rate**, not in a
  footnote. PingPong treats refusal as a first-class scored defect in a quality benchmark. We
  should do the same.
- **Methodology to steal:** the Interrogator/user-emulator pattern is how we generate multi-turn
  eval traffic at scale without humans; the Judge Ensemble (2+ judges averaged) is how we damp
  single-judge bias. Both directly applicable.

## Caveats

- Small: 64 conversations/model, 288 annotations. Underpowered for fine distinctions; fine as an
  existence proof of the gap.
- Model versions are stale (Claude 3.5 Sonnet / 3 Opus era, 2024). The *specific* numbers will
  not hold on current models — Anthropic has publicly worked on over-refusal since. Cite the
  **pattern**, not the current standing of any vendor.
- "Refusal ratio" is judge-assessed and the paper does not, as far as I could extract,
  distinguish a hard refusal ("As an AI I can't") from a soft in-character deflection. That
  distinction matters enormously to us (see the synthesis note) and we would need to define it
  ourselves.
