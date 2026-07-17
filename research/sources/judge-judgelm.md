---
title: "JudgeLM: Fine-tuned Large Language Models are Scalable Judges"
url: https://arxiv.org/abs/2310.17631
authors:
  - Lianghui Zhu
  - Xinggang Wang
  - Xinlong Wang
year: 2023
venue: ICLR 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# JudgeLM: Fine-tuned Large Language Models are Scalable Judges

## Abstract (verbatim opening)

> Evaluating Large Language Models (LLMs) in open-ended scenarios is challenging because existing benchmarks and metrics can not measure them comprehensively. To address this problem, we propose to fine-tune LLMs as scalable judges (JudgeLM) to evaluate LLMs efficiently and effectively in open-ended benchmarks.

## Methodology

- Fine-tune Vicuna-based models at **7B / 13B / 33B** on **100K samples with GPT-4-generated judgments**.
- Identifies **three biases** and proposes a targeted mitigation for each — this taxonomy is the paper's most reusable contribution:

| Bias | Definition | Mitigation |
|---|---|---|
| **Position bias** | Favoring an answer by its slot | **Swap augmentation** — train on both orderings |
| **Knowledge bias** | Judge lacks the facts to judge | **Reference support** — provide a reference answer |
| **Format bias** | Judge degrades when the prompt format at inference differs from training (e.g. reference present/absent) | **Reference drop** — randomly drop references during training |

**Format bias is a genuinely novel finding and it is the one most relevant to a fine-tuned judge in production.** A judge trained *with* references degrades when run *without* them. For us: **if we fine-tune or few-shot a judge in one prompt configuration and then change the configuration (add a reference, drop the persona card, change the rubric), performance degrades in ways unrelated to the change's merit.** This is an argument for treating the entire judge prompt template as an immutable, versioned unit.

## Key numbers

### Agreement with GPT-4 teacher

| Model | Agreement (w/o reference) | Agreement (w/ reference) |
|-------|---------------------------|-------------------------|
| JudgeLM-7B | 81.11% | 84.08% |
| JudgeLM-13B | 84.33% | 85.47% |
| JudgeLM-33B | **89.03%** | **89.32%** |

### Mitigation effects (measured)

**Swap augmentation (position bias):**
- Baseline consistency: **73.45%**
- With swap augmentation: **78.89%**
- **+5.44pp**

**Reference support (knowledge bias):**
- Baseline agreement: 75.87% → **80.15%** (**+4.28pp**)
- Consistency: 73.45% → **81.23%** (**+7.78pp**)

**Reference drop (format bias):** eliminates the degradation when format mismatches occur at inference.

### Efficiency

- **JudgeLM-7B judges 5K samples in 3 minutes on 8× A100.**

That is **~36ms/sample wall-clock** on 8 GPUs (~0.29 GPU-seconds/sample). Compare to a frontier API judge at ~2–10s/judgment plus rate limits. **This is a ~2 order-of-magnitude latency difference** and is what makes judging every variant on every commit feasible rather than a nightly batch job.

## The claim to be careful about

The paper reports agreement **"exceeding 90%"** with the GPT-4 teacher and notes this **"even surpasses human-to-human agreement"** (citing MT-Bench's 81–82% human-human ceiling).

**This comparison is invalid and it is the single most instructive error in the judge literature.** Agreement with *GPT-4* is not agreement with *humans*. JudgeLM is distilled from GPT-4, so high agreement with GPT-4 measures **distillation fidelity, not judgment quality**. A perfect JudgeLM would reproduce GPT-4's judgments *including all of GPT-4's biases* — position bias, self-preference toward the GPT family, verbosity preference, and its 50.9% near-chance accuracy on JudgeBench.

Comparing "89% agreement with GPT-4" against "81% human-human agreement" puts two different quantities on the same axis and concludes the wrong thing. **A distilled judge's agreement with its teacher is an upper bound on nothing except how well it copies.**

This is the trap our platform must not fall into: **our judge validation must be against human labels on our own data, never against a stronger LLM's labels.** If we validate judge-vs-GPT-5, we learn only how well we imitate GPT-5.

## Implications

- **Swap augmentation at training time is cheaper than swap-and-average at inference time** (+5.44pp consistency, no 2× inference cost) — if we fine-tune our own judge, bake the swap in.
- **Reference support gives the biggest single gain** (+7.78pp consistency, +4.28pp agreement) — converges with MT-Bench's reference-guided result (70% → 15% failure). **Reference anchoring is the most consistently validated mitigation across the entire literature.** For companion characters, the "reference" is the character card + exemplar in-character dialogue.
- **Reference drop** matters if we sometimes have references and sometimes don't — train/prompt for both.
- Self-hosted judges make per-judgment cost effectively zero and enable judging at commit granularity.
