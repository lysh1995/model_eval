---
title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
url: https://arxiv.org/abs/2306.05685
authors:
  - Lianmin Zheng
  - Wei-Lin Chiang
  - Ying Sheng
  - Siyuan Zhuang
  - Zhanghao Wu
  - Yonghao Zhuang
  - Zi Lin
  - Zhuohan Li
  - Dacheng Li
  - Eric P. Xing
  - Hao Zhang
  - Joseph E. Gonzalez
  - Ion Stoica
year: 2023
venue: NeurIPS 2023 Datasets and Benchmarks Track
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

## Abstract (verbatim)

> Evaluating large language model (LLM) based chat assistants is challenging due to their broad capabilities and the inadequacy of existing benchmarks in measuring human preferences. To address this, we explore using strong LLMs as judges to evaluate these models on more open-ended questions. We examine the usage and limitations of LLM-as-a-judge, including position, verbosity, and self-enhancement biases, as well as limited reasoning ability, and propose solutions to mitigate some of them. We then verify the agreement between LLM judges and human preferences by introducing two benchmarks: MT-bench, a multi-turn question set; and Chatbot Arena, a crowdsourced battle platform. Our results reveal that strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans. Hence, LLM-as-a-judge is a scalable and explainable way to approximate human preferences, which are otherwise very expensive to obtain. Additionally, we show our benchmark and traditional benchmarks complement each other by evaluating several variants of LLaMA and Vicuna.

This is the foundational paper for the entire LLM-as-a-judge methodology. Nearly every later paper positions itself against these numbers.

## Methodology

Two benchmarks are introduced:

- **MT-Bench** — 80 multi-turn questions across 8 categories (writing, roleplay, extraction, reasoning, math, coding, STEM, humanities). Note for our project: **roleplay is an explicit MT-Bench category**, which makes this paper directly relevant to companion-character evaluation. 3.3K expert-level pairwise human preferences collected over 6 models.
- **Chatbot Arena** — crowdsourced anonymous battle platform; ~30K votes analyzed at time of writing. Elo/Bradley-Terry rating aggregation.

Three judge setups are defined and used throughout the literature:

1. **Pairwise comparison** — judge sees two answers, picks a winner (or tie).
2. **Single answer grading (pointwise)** — judge assigns a scalar score (1–10 Likert) to one answer in isolation.
3. **Reference-guided grading** — judge is given a reference answer (e.g. a GPT-4-generated solution) before grading.

Two agreement setups are reported:

- **S1** — includes ties; agreement computed over all votes.
- **S2** — non-tie votes only (ties excluded from both judge and human). S2 numbers are the ones usually quoted.

## Key numbers

### Position bias (Table 2) — consistency when swapping answer order

| Judge | Default prompt | Renamed-assistants prompt |
|---|---|---|
| GPT-4 | **65.0%** | 66.2% |
| GPT-3.5 | **46.2%** | 51.2% |
| Claude-v1 | **23.8%** | 56.2% |

Consistency = fraction of pairs where the judge gives the same verdict under both orderings. **GPT-4 flips its verdict on ~35% of pairs purely from ordering.** Claude-v1 at 23.8% is close to worse-than-chance stability. Renaming the assistants helps Claude-v1 enormously (23.8% → 56.2%) but barely moves GPT-4 — i.e. the bias is not a single mechanism across models.

### Verbosity bias (Table 3) — "repetitive list" attack

Attack: take an answer that is a list, and rephrase it to be more verbose *without adding information* (repeating the list items). Failure rate = judge prefers the padded answer.

| Judge | Failure rate |
|---|---|
| Claude-v1 | **91.3%** |
| GPT-3.5 | **91.3%** |
| GPT-4 | **8.7%** |

n = 23 answers. GPT-4 is dramatically more robust to this specific naive attack than GPT-3.5/Claude-v1, but 8.7% is not zero, and this is the *easiest* possible verbosity attack (pure repetition, no new content). Later work (Length-Controlled AlpacaEval, Style Control) shows GPT-4 still has substantial length bias against subtler padding.

### Self-enhancement bias

- **GPT-4** favors itself with a **~10% higher win rate** than humans give it.
- **Claude-v1** favors itself with a **~25% higher win rate** than humans give it.
- GPT-3.5 does *not* favor itself.

The authors explicitly caution that the data is limited and confounded (each judge saw few models), so they **do not draw a definitive statistical conclusion**. This is important: the canonical "self-preference" cite is weaker than commonly assumed. Panickssery et al. 2024 is the stronger causal evidence.

### Judge-vs-human agreement

**MT-Bench (Table 5b), Setup S2 (non-tie votes only):**

| Comparison | Agreement |
|---|---|
| GPT-4 pairwise vs human | **85%** |
| GPT-4 single-answer grading vs human | **84%** |
| **Human vs human** | **81%** |

**Chatbot Arena (Table 6), Setup S2:**

| Comparison | Agreement |
|---|---|
| GPT-4 pairwise vs human | **87%** |
| GPT-4 single-answer vs human | **85%** |
| GPT-3.5 vs human | 83% |
| Claude vs human | 84% |

**The headline claim — "GPT-4 agrees with humans as much as humans agree with each other" — rests on 85% vs 81%.** Two critical caveats that the platform design must internalize:

1. These are **S2** numbers, with ties excluded. Including ties (S1) drops agreement substantially (~66% range). Ties are exactly where subjective dimensions live, and our roleplay/creativity dimensions will produce many near-ties.
2. 81% human-human agreement is the **ceiling**, not a floor. It means ~19% of pairwise judgments are irreducibly contested even among experts. No judge can be validated beyond this on the same distribution.

### Limited reasoning / math grading (Table 4) — and mitigation

Failure rate grading math questions (n = 20):

| Judge prompt | Failure rate |
|---|---|
| Default | **70%** (14/20) |
| Chain-of-thought | **30%** (6/20) |
| **Reference-guided** | **15%** (3/20) |

Reference-guided judging cuts the failure rate by ~4.7x vs default and ~2x vs CoT. This is the strongest single mitigation measured in the paper. CoT helps but is markedly weaker than giving the judge a reference answer.

### Few-shot judging (Table 13)

- GPT-4 zero-shot consistency: 65.0%
- GPT-4 **few-shot**: **77.5%**

Few-shot examples buy +12.5pp of position consistency. The authors note it makes the judgment more verbose/expensive and that few-shot examples can themselves introduce bias.

## Notes for our platform

- **Roleplay is a native MT-Bench category** — the reference judge prompts for roleplay are reusable as a starting point.
- The paper's own recommended defaults: pairwise for comparing two specific models; **single-answer grading when you need to scale to many models** (pairwise is O(n²)); reference-guided when a ground truth exists.
- Crucially, the paper notes single-answer grading **"may be unstable across different judges/prompt versions"** and that its scores are not necessarily comparable across separate runs — directly relevant to our cross-model comparability requirement.
- The judge model here is a moving API endpoint (`gpt-4`). None of these numbers are reproducible against a pinned artifact today — a live demonstration of why judge versioning matters.
