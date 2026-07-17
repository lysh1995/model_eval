---
title: "JudgeBench: A Benchmark for Evaluating LLM-based Judges"
url: https://arxiv.org/abs/2410.12784
authors:
  - Sijun Tan
  - Siyuan Zhuang
  - Kyle Montgomery
  - William Y. Tang
  - Alejandro Cuadron
  - Chenguang Wang
  - Raluca Ada Popa
  - Ion Stoica
year: 2024
venue: ICLR 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# JudgeBench: A Benchmark for Evaluating LLM-based Judges

## Abstract (verbatim opening)

> LLM-based judges have emerged as a scalable alternative to human evaluation and are increasingly used to assess, compare, and improve models. However, the reliability of LLM-based judges themselves is rarely scrutinized.

Note the author overlap with MT-Bench (Zhuang, Stoica) — **this is partly the MT-Bench team walking back the optimism of their own 2023 paper.** That provenance makes the negative result more credible, not less.

## Methodology

The key design move: build response pairs where **correctness is objectively known**, rather than relying on crowdsourced preference. Pairs are drawn from datasets with objective ground truth (MMLU-Pro, LiveBench, LiveCodeBench and similar) spanning **knowledge, reasoning, math, and coding**. One response is factually/logically correct, the other is not.

This decouples **"which answer does a human prefer"** from **"which answer is actually right."** Prior benchmarks (MT-Bench, RewardBench Chat) conflate them, and a judge can score well by matching human preference for style while being wrong on substance.

## Key numbers

**GPT-4o (vanilla prompt):**

| Category | Accuracy |
|---|---|
| Knowledge | **44.2%** |
| Reasoning | 48.0% |
| Math | 66.1% |
| Coding | 61.9% |
| **Overall** | **50.9%** |

**GPT-4o scores 50.9% overall — random chance is 50%.** On knowledge pairs it scores **44.2%, i.e. worse than a coin flip.** One of the strongest available models, used as a judge, carries essentially zero information about which of two answers is factually correct.

**Arena-Hard prompt (GPT-4o):**

| Category | Accuracy |
|---|---|
| Knowledge | 50.7% |
| Reasoning | 54.1% |
| Math | 75.0% |
| Coding | 59.5% |
| **Overall** | **56.6%** |

Better prompting buys **+5.7pp** (50.9 → 56.6). Prompt engineering does not rescue the judge; it moves it from "chance" to "barely above chance."

**Skywork Reward (Gemma-2-27B) — a trained reward model:**

| Category | Accuracy |
|---|---|
| Knowledge | 59.7% |
| Reasoning | 66.3% |
| Math | 83.9% |
| Coding | 50.0% |
| **Overall** | **64.3%** |

A small trained reward model **beats GPT-4o-as-judge by 13.4pp overall**. Judge quality is not a function of general model capability.

**o1-preview (reasoning model):**

| Category | Accuracy |
|---|---|
| Math | 85.7% |
| Coding | 85.7% |
| **Overall** | **75.4%** |

**Inference-time reasoning is the biggest single lever found: 50.9% → 75.4% (+24.5pp).** Far larger than any prompt-level mitigation in the literature. This is the strongest argument for spending latency/cost on a reasoning judge rather than on more samples from a cheap one.

**PandaLM (LLaMA-7B)** performed poorly (specific figure not captured).

**Self-judging collapse:** Claude-3.5-Sonnet achieves **64.3%** accuracy judging GPT-4o-generated pairs, but drops to **44.8%** when judging **its own** generated pairs — a **−19.5pp collapse**, to below chance. This is a much sharper self-preference result than MT-Bench's soft ~10%: when a model is wrong, it is wrong *confidently and consistently* about its own output, because the same blind spot produced and evaluated the answer. **A judge cannot catch an error it would itself make.** This is the cleanest available statement of the fundamental ceiling on self-evaluation.

## Implications for our platform

- **The judge is not a truth oracle.** For anything with a fact of the matter, an LLM judge near chance. Our subjective dimensions (creativity, storytelling) don't have a ground truth, so this benchmark doesn't directly bound them — **but character fidelity partly does.** "Did the character contradict its established backstory?" is a factual consistency question, and JudgeBench says a judge will be near-chance at catching it. **Character fidelity should be decomposed: the factual-consistency part needs programmatic checks or a reasoning judge; only the stylistic part should be left to a preference judge.**
- **Errors correlate with the candidate model.** The 64.3% → 44.8% self-judging collapse means judge reliability depends on *which model produced the response*. This breaks cross-model comparability directly — the judge is a *different instrument* for each candidate family. **This is the deepest threat to our core requirement**, and it cannot be fixed by averaging: it is a per-candidate-family bias, not noise.
- Strong argument for **reasoning judges** (o1-class) on fidelity, and for **excluding judges from the same family as the candidate** wherever possible.
- Trained reward models beat frontier LLM judges here and are far cheaper — worth benchmarking as panel members.
