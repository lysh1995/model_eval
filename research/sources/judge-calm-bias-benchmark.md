---
title: "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)"
url: https://arxiv.org/abs/2410.02736
authors:
  - Jiayi Ye
  - Yanbo Wang
  - Yue Huang
  - Dongping Chen
  - Qihui Zhang
  - Nuno Moniz
  - Tian Gao
  - Werner Geyer
  - Chao Huang
  - Pin-Yu Chen
  - Nitesh V. Chawla
  - Xiangliang Zhang
year: 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)

## Abstract (verbatim)

> LLM-as-a-Judge has been widely utilized as an evaluation method in various benchmarks and served as supervised rewards in model training. However, despite their excellence in many domains, potential issues are under-explored, undermining their reliability and the scope of their utility. Therefore, we identify 12 key potential biases and propose a new automated bias quantification framework-CALM-which systematically quantifies and analyzes each type of bias in LLM-as-a-Judge by using automated and principle-guided modification. Our experiments cover multiple popular language models, and the results indicate that while advanced models have achieved commendable overall performance, significant biases persist in certain specific tasks. Empirical results suggest that there remains room for improvement in the reliability of LLM-as-a-Judge. Moreover, we also discuss the explicit and implicit influence of these biases and give some suggestions for the reliable application of LLM-as-a-Judge.

**This is the single most valuable source for our bias table** — it is the only work that quantifies 12 biases on a common scale across many judges.

## Methodology

CALM applies **principle-guided automated perturbations** to judge inputs that should not change the correct verdict, then measures whether the verdict changes.

Core metric: **Robustness Rate (RR)** — the fraction of cases where the judge's verdict is *unchanged* after a bias-inducing perturbation. **RR = 1.0 is perfect; RR = 0.5 is coin-flip on a perturbation that should have had zero effect.** Note RR measures *consistency under perturbation*, not correctness.

## The 12 bias types

| # | Bias | Definition |
|---|---|---|
| 1 | **Position** | Favoring answers based on their placement in the input |
| 2 | **Verbosity** | Preferring longer responses regardless of quality |
| 3 | **Compassion-Fade** | Judgments change when model identity is named vs anonymized |
| 4 | **Bandwagon** | Preference for the answer labeled as the majority opinion |
| 5 | **Distraction** | Susceptibility to irrelevant content inserted in responses |
| 6 | **Fallacy-Oversight** | Ignoring logical errors, focusing only on final correctness |
| 7 | **Authority** | Over-weighting answers carrying citations / authoritative references |
| 8 | **Sentiment** | Preference or aversion driven by emotional tone |
| 9 | **Diversity** | Differential treatment when identity markers are mentioned |
| 10 | **Chain-of-Thought** | Verdict varies with/without explicit reasoning steps |
| 11 | **Self-Enhancement** | Favoring one's own generated outputs |
| 12 | **Refinement-Aware** | Different scoring when told an answer is a refinement |

## Key numbers — Robustness Rate by bias and judge (Table 4)

| Bias Type | ChatGPT | GPT-4-Turbo | GPT-4o | GLM-4 | Claude-3.5 | Qwen2 |
|-----------|---------|-------------|--------|-------|-----------|-------|
| Verbosity | 0.900 | 0.915 | **0.977** | 0.887 | 0.952 | 0.884 |
| Fallacy-Oversight | 0.917 | 0.969 | **0.984** | 0.979 | 0.985 | 0.935 |
| Sentiment | 0.804 | 0.653 | 0.699 | 0.679 | 0.660 | **0.651** |
| Position | **0.566** | 0.818 | 0.776 | 0.781 | 0.832 | 0.760 |
| Compassion-Fade | 0.862 | 0.858 | 0.868 | 0.835 | 0.875 | 0.877 |
| Bandwagon | 0.688 | 0.638 | 0.791 | 0.690 | **0.610** | 0.710 |
| Authority | 0.662 | 0.846 | 0.787 | 0.796 | 0.865 | 0.779 |
| Distraction | 0.713 | 0.729 | 0.790 | 0.814 | 0.878 | 0.785 |
| Diversity | 0.679 | 0.855 | 0.814 | 0.788 | 0.914 | 0.826 |
| Chain-of-Thought | **0.560** | 0.720 | 0.700 | 0.688 | 0.745 | 0.704 |

Higher RR = more resilient.

## Findings that matter for a companion/roleplay platform

**Weakest areas across ALL models (these are the unfixable-looking ones):**

- **Sentiment bias: 0.60–0.80 RR.** Every model is badly affected. Emotional-tone modification of a response changes the verdict 20–40% of the time. **This is the most dangerous finding for our use case** — companion characters are emotionally-toned by design, and our judges will be scoring emotional content. The paper reports that sadness/anger/fear emotional modification **dropped robustness to 0.24–0.66 RR on high-quality answers** — i.e. on some emotional perturbations the judge flips its verdict up to 76% of the time.
- **Chain-of-Thought bias: 0.56–0.75 RR** — the *lowest* overall robustness. Adding/removing CoT changes verdicts. This directly undercuts the naive assumption that "just add CoT" is a free mitigation: CoT changes verdicts, and CoT itself is a bias vector.
- **Position bias: 0.566–0.832 RR**, and the paper explicitly notes it **worsens with 3–4 answer options** — a direct warning against listwise judging.
- **Bandwagon: 0.610–0.791.** Telling the judge "90% of people prefer A" flips it ~21–39% of the time. Claude-3.5 is the *most* susceptible (0.610).

**Strongest areas:**
- Fallacy-Oversight: 0.92–0.99 across all models.
- Verbosity: 0.88–0.98 — notably *better* than MT-Bench's naive attack suggested, but CALM's verbosity perturbation differs from Length-Controlled AlpacaEval's real-world length confound.

**Attack effectiveness:** Authority bias via fabricated book/quote citations degraded RR to 0.628–0.841. Inserting a fake citation flips the verdict up to ~37% of the time.

**Model-specific:**
- GPT-4o strongest overall (0.977 verbosity, 0.984 fallacy-oversight).
- Claude-3.5 best on diversity (0.914) and distraction (0.878) but worst on bandwagon (0.610).
- ChatGPT/GPT-3.5 worst on position (0.566) and CoT (0.560) — **do not use a GPT-3.5-class model as a pairwise judge.**

## Implications

1. **No judge is uniformly robust.** Each model has a different bias profile. This is an argument for a *panel of diverse judges* (see PoLL) rather than picking "the best" judge.
2. **Bias is task-dependent** — the paper stresses that advanced models have good *overall* performance but "significant biases persist in certain specific tasks." Aggregate judge quality does not transfer to our specific subjective dimensions; we must measure on our own data.
3. Sentiment and CoT biases are the two that current models have essentially not solved, and both sit directly on top of our roleplay/emotional-companion use case.
