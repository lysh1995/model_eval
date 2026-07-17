---
title: "Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models"
url: https://arxiv.org/abs/2405.01535
authors:
  - Seungone Kim
  - Juyoung Suk
  - Shayne Longpre
  - Bill Yuchen Lin
  - Jamin Shin
  - Sean Welleck
  - Graham Neubig
  - Moontae Lee
  - Kyungjae Lee
  - Minjoon Seo
year: 2024
venue: EMNLP 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Prometheus 2

## Abstract (verbatim)

> Proprietary LMs such as GPT-4 are often employed to assess the quality of responses from various LMs. However, concerns including transparency, controllability, and affordability strongly motivate the development of open-source LMs specialized in evaluations. On the other hand, existing open evaluator LMs exhibit critical shortcomings: 1) they issue scores that significantly diverge from those assigned by humans, and 2) they lack the flexibility to perform both direct assessment and pairwise ranking, the two most prevalent forms of assessment. Additionally, they do not possess the ability to evaluate based on custom evaluation criteria, focusing instead on general attributes like helpfulness and harmlessness. To address these issues, we introduce Prometheus 2, a more powerful evaluator LM than its predecessor that closely mirrors human and GPT-4 judgements. Moreover, it is capable of processing both direct assessment and pairwise ranking formats grouped with a user-defined evaluation criteria.

**Why this matters for us:** Prometheus 2 is the strongest open-weights judge, which means it can be **pinned as a versioned artifact** — the single most important property for a reproducible eval platform. A GPT-4 judge is a moving endpoint; a Prometheus-2 checkpoint has a hash.

It also explicitly supports **user-defined evaluation criteria**, which is exactly what we need for character fidelity / creativity / storytelling — custom subjective rubrics rather than generic helpfulness.

## Methodology

- Two base sizes: **7B** (Mistral-7B) and **8x7B** (Mixtral MoE).
- **Weight merging** is the core trick: train one model on direct-assessment (pointwise) feedback data and another on pairwise-ranking data, then **merge the weights**:

  ```
  θ_final = α · θ_direct + (1 − α) · θ_pairwise
  ```

  with **α = 0.5** for Mistral-7B, and **DARE merging** for Mixtral-8x7B.

- The finding that merging beats joint training is notable: it means the direct-assessment and pairwise skills are somewhat separable in weight space, and a single model can hold both without the usual interference.
- Datasets: Feedback Collection + Preference Collection.

## Key numbers

### Direct assessment (pointwise) — Pearson correlation with human/GPT-4

| Benchmark | Prometheus 2-8x7B | GPT-4-1106 | Prometheus-13B (v1) |
|-----------|-------------------|-----------|----------------|
| Feedback Bench | **0.898** | 0.753 | 0.860 |
| Vicuna Bench | 0.685 | **0.694** | 0.492 |
| MT Bench | 0.665 | **0.717** | 0.404 |
| FLASK | 0.659 | **0.736** | 0.462 |

Prometheus 2-8x7B **closes most but not all of the gap to GPT-4** on independent benchmarks (0.665 vs 0.717 on MT Bench; 0.659 vs 0.736 on FLASK), while winning on its own in-domain Feedback Bench (0.898 — in-domain, so discount it). It improves on Prometheus v1 by a large margin (MT Bench 0.404 → 0.665). The paper reports at least **+0.2 units** improvement over prior open evaluators.

### Pairwise ranking — accuracy

| Benchmark | Prometheus 2-8x7B | GPT-4-1106 | Auto-J |
|-----------|-------------------|-----------|--------|
| HHH Alignment | 85.52% | **90.95%** | 75.57% |
| MT Bench Human Judgement | 71.96% | **79.90%** | 69.12% |
| Auto-J Eval | 79.98% | **83.12%** | 76.64% |
| Preference Bench | **90.65%** | 85.50% | 81.35% |

**A gap to GPT-4 remains on pairwise: ~5pp on HHH, ~8pp on MT Bench Human Judgement.** Prometheus 2 wins only on Preference Bench (in-domain).

Note the absolute numbers: **the best judge scores 79.9% on MT Bench Human Judgement.** Against a human-human ceiling around 81%, that looks near-ceiling — but see JudgeBench: on genuinely hard pairs, judges collapse toward chance.

## Implications for our platform

- **Strong candidate for a pinnable, self-hosted judge**, especially as a panel member alongside a frontier API judge.
- Supports both pointwise and pairwise with a custom rubric from one checkpoint — matches our need to score multiple subjective dimensions.
- Cost/privacy: self-hosted means no per-judgment API cost and no data egress (relevant for companion/roleplay content, which may be sensitive).
- **Caveat:** the ~5-8pp pairwise gap to GPT-4 is real. Prometheus 2 as the *sole* judge trades accuracy for reproducibility. The panel approach (PoLL) lets us have both.
- **Caveat 2:** Prometheus is trained on GPT-4-generated feedback. Its "agreement with GPT-4" is partly distillation, not independent confirmation. **A panel of {Prometheus 2, GPT-4} is less independent than it looks** — their errors are correlated by construction. This matters for the disjoint-families requirement in PoLL.
