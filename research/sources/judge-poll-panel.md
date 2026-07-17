---
title: "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models (PoLL)"
url: https://arxiv.org/abs/2404.18796
authors:
  - Pat Verga
  - Sebastian Hofstatter
  - Sophia Althammer
  - Yixuan Su
  - Aleksandra Piktus
  - Arkady Arkhangorodsky
  - Minjie Xu
  - Naomi White
  - Patrick Lewis
year: 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Replacing Judges with Juries (PoLL)

## Abstract (verbatim)

> As Large Language Models (LLMs) have become more advanced, they have outpaced our abilities to accurately evaluate their quality. Not only is finding data to adequately probe particular model properties difficult, but evaluating the correctness of a model's freeform generation alone is a challenge. To address this, many evaluations now rely on using LLMs themselves as judges to score the quality of outputs from other LLMs. Evaluations most commonly use a single large model like GPT4. While this method has grown in popularity, it is costly, has been shown to introduce intramodel bias, and in this work, we find that very large models are often unnecessary. We propose instead to evaluate models using a Panel of LLm evaluators (PoLL). Across three distinct judge settings and spanning six different datasets, we find that using a PoLL composed of a larger number of smaller models outperforms a single large judge, exhibits less intra-model bias due to its composition of disjoint model families, and does so while being over seven times less expensive.

**This is the key source for the ensembling mitigation, and it is unusually strong: the panel is simultaneously better AND ~7-8x cheaper.**

## Methodology

**Panel composition — three models from deliberately disjoint families:**
- **Command R** (35B, Cohere)
- **Claude-3 Haiku** (Anthropic)
- **GPT-3.5** (OpenAI)

The disjointness is the point: self-preference/intra-model bias cannot be shared by models from different families, so it partially cancels in aggregate.

**Aggregation methods:**
- **Max voting** for QA tasks (binary correct/incorrect judgments)
- **Average pooling** for Chatbot Arena (1–5 scale scores)

Three judge settings across six datasets.

## Key numbers

### Correlation with human judgments — single-hop QA (KILT), Cohen's κ

| Dataset | PoLL | GPT-4 | Δ |
|---------|------|-------|---|
| Natural Questions | **0.763** | 0.627 | **+0.136** |
| TriviaQA | **0.906** | 0.841 | +0.065 |
| HotpotQA | **0.867** | 0.830 | +0.037 |

The panel of three *small* models beats a single GPT-4 judge on every dataset — by a large margin on NQ.

### Chatbot Arena Hard — rank correlation

| Metric | PoLL | GPT-4 |
|--------|------|-------|
| Pearson | **0.917** | 0.817 |
| Kendall Tau | **0.778** | 0.667 |

This is the most relevant setting for us: **PoLL reproduces the human-derived model ranking better than GPT-4 does (Kendall τ 0.778 vs 0.667).** Ranking fidelity is exactly what our cross-model comparability requirement needs.

### Cost

> "running the entire three model PoLL is seven to eight times less expensive than running a single GPT-4 judge"

Rates cited (per million tokens):
- **PoLL (all three combined): $1.25 input / $4.25 output**
- **GPT-4 Turbo (single judge): $10 input / $30 output**

So the panel is both better *and* ~7–8x cheaper. This is a rare strict dominance — there is no quality/cost tradeoff to argue about.

### Intra-model / self-preference bias

Figure 2: GPT-4 ranked **another GPT-4 variant in position 2 when its true position was 4** — a 2-rank self-promotion.

Variance across judges: PoLL's ranking had a **standard deviation of 2.2** vs **6.1 for GPT-3.5** as a single judge. The panel is roughly **2.8x more stable** in the ranks it produces.

## Notes for our platform

- The cost argument means a panel is affordable at our scale; a 3-model panel of mid-tier models costs less than one frontier judge.
- The disjoint-families requirement is a **hard design constraint**: a panel of GPT-4o + GPT-4o-mini + GPT-4-turbo would share self-preference bias and defeat the purpose. Our panel must span vendors (e.g. one OpenAI, one Anthropic, one open-weights).
- **Critical caveat for us:** if the panel includes a model from the same family as a variant *under test*, that panel member's self-preference contaminates that variant's score. Since we are evaluating variants across many base models, we need either (a) judges from families disjoint from all candidates — increasingly hard, or (b) to measure and subtract the self-preference offset per judge/candidate family pair.
- Aggregation choice matters and should match the output type: max-voting for discrete verdicts, average-pooling for scales.
