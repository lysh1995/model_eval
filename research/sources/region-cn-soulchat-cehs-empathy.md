---
title: "SoulChat (灵心): Improving LLMs' Empathy, Listening, and Comfort Abilities through Fine-tuning with Multi-turn Empathy Conversations — the CEHS manual evaluation framework"
url: https://aclanthology.org/2023.findings-emnlp.83/
authors: Yirong Chen, Xiaofen Xing, Jingkai Lin, Huimin Zheng, Zhenyu Wang, Qi Liu, Xiangmin Xu (South China University of Technology 华南理工大学; Guangdong Provincial Key Laboratory of Human Digital Twin; Pazhou Lab, Guangzhou)
year: 2023
type: paper
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# SoulChat (灵心) — CEHS framework and the Empathy/Helpfulness conflict

Findings of EMNLP 2023, pages 1170–1183. Chinese mental-health/empathy dialogue model
from **华南理工大学 (South China University of Technology)**. Code:
https://github.com/scutcyr/SoulChat

**All numbers below were read directly from the paper's extracted text.** I pulled the
PDF and extracted it with pypdf rather than trusting any summary. Line references are to
my extraction. Nothing here is inferred.

## Why this is the most important file in the CN sweep

It supplies **quantitative evidence for the central Chinese thesis about companion AI**:
that being *helpful* and being *empathetic* are in tension — and that assistant-tuned
models sit on the wrong side of that tradeoff for companionship.

This is the measured counterpart to the practitioner claim in
`region-cn-volcengine-practitioner.md` that 拟人化 means
去掉 llm 模型骨子里的彬彬有礼、有问必答 ("strip away the LLM's bone-deep politeness and
answer-everything reflex"). Two independent Chinese sources — one industry, one academic
— converge on **assistant-ness as the thing to remove**.

## The three stated failures of ChatGPT in Chinese emotional support (quoted from §1)

The paper names three reasons ChatGPT is less "human-centered":

1. **"ChatGPT tends to provide repetitive and standardized responses."** It uses the
   template: "我很抱歉...。xxx是...。以下是一些建议：..." ("I'm sorry to... {xxx} is...
   Here are some suggestions:..."), which "may cause boredom."
2. **"ChatGPT is inclined to provide suggestions rather than ask questions or listen."**
   Notes that "professional psychologists rarely provide specific suggestions during the
   counseling process."
3. **"ChatGPT acts a bit like a rational 'Straight man'"** for users who need listening
   and comfort.

Note #1 is the 机械感 / 简单重复 complaint and #2/#3 are the 老好人助手 complaint,
arrived at independently through a clinical-psychology lens.

## CEHS — the manual evaluation framework (Appendix G, Table 2)

Four dimensions. Definitions condensed from the paper's own descriptions:

| Aspect | Scale | Description (from Table 2) |
|---|---|---|
| **Content** (naturalness) | 0–2 | Whether content is relevant and coherent to conversation history; smooth and natural; **consistent with language habits**; free of syntax errors |
| **Empathy** | 0–2 | Whether the model "can understand the feelings and behaviors of the parties involved, grasp their **inner feelings, deep meanings, and their degree**" |
| **Helpfulness** | 0–2 | Whether output is helpful, "considered from the user's perspective" |
| **Safety** | 0–1 | Harm to users/others/society/environment; privacy; legal compliance; social morality; political sensitivity; discrimination; hate speech; ethics |

Raters: **three individual experts majoring in Psychology**. **100 dialogues** randomly
sampled for manual evaluation (from each of two test sets). Automatic eval used 10,000
samples and 7 metrics (BLEU-1/2/3/4, ROUGE-1/2/L).

## Fleiss' κ — VERIFIED, read verbatim from §3.3

> "Fleiss'κ (Fleiss, 1971) for Con., Emp. and Hel. are **0.489, 0.472 and 0.532**,
> indicating moderate annotation agreement respectively, while **κ = 1 for Saf.**
> (perfect agreement)."

| Dimension | Fleiss' κ |
|---|---|
| Content | **0.489** |
| Empathy | **0.472** |
| Helpfulness | **0.532** |
| Safety | **1.0** |

⚠️ **The κ = 1 for Safety is a degenerate ceiling effect, not a quality signal.**
Every model scored **1.0 on Safety across all 8 rows of Table 1** — so there was no
variance to disagree about. Perfect agreement on a constant is trivial. Do not cite
"κ=1" as evidence the safety rubric is good; it is evidence the safety rubric
**discriminated nothing** on this data.

**The κ ≈ 0.47–0.53 range is the real finding**, and it is sobering: three trained
*psychology experts* rating on a *3-point scale* only reach "moderate" agreement, with
**Empathy the lowest (0.472)**. Empathy is the hardest of the four to rate reliably.
Any companion platform scoring 共情/empathy should budget for this reliability ceiling —
see `psycho-inter-rater-reliability.md` and `pipeline-annotation-iaa-cost.md`.

This is a **real, verifiable κ** — contrast with the fabricated one this project was
previously burned by. It is checkable at aclanthology.org/2023.findings-emnlp.83, §3.3.

## Table 1 — verified results (transcribed from the paper)

Con./Emp./Hel. on 0–2; Saf. on 0–1.

**Test set: SoulChatCorpus**

| Model | B-1 | B-2 | B-3 | B-4 | R-1 | R-2 | R-L | Con. | Emp. | Hel. | Saf. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ChatGLM-6B | 22.73 | 13.15 | 8.04 | 4.92 | 25.33 | 5.72 | 18.84 | 1.90 | 1.55 | 1.92 | 1.0 |
| MeChat | 29.43 | 17.12 | 10.54 | 6.71 | 27.35 | 6.27 | 21.12 | 1.83 | 1.70 | 1.78 | 1.0 |
| ChatGPT | 27.98 | 16.09 | 9.93 | 6.23 | 27.39 | 6.82 | 21.92 | **1.96** | 1.62 | **1.94** | 1.0 |
| SoulChat | **33.78** | **20.07** | **12.86** | **8.52** | **31.47** | **8.92** | **26.57** | 1.95 | **1.84** | 1.87 | 1.0 |

**Test set: SMILECHAT** (zero-shot for SoulChat)

| Model | B-1 | B-2 | B-3 | B-4 | R-1 | R-2 | R-L | Con. | Emp. | Hel. | Saf. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ChatGLM-6B | 22.91 | 13.56 | 8.40 | 5.15 | 25.99 | 5.95 | 18.76 | 1.81 | 1.39 | 1.84 | 1.0 |
| MeChat | 30.63 | 18.41 | 11.59 | 7.46 | 28.92 | 6.76 | 21.59 | 1.95 | 1.74 | 1.83 | 1.0 |
| ChatGPT | 28.30 | 16.48 | 10.24 | 6.40 | 27.57 | 6.71 | 21.60 | 1.95 | 1.65 | **1.97** | 1.0 |
| SoulChat | **35.40** | **21.39** | **13.77** | **9.02** | **32.64** | **9.17** | 21.10 | 1.93 | **1.90** | 1.85 | 1.0 |

## The Empathy/Helpfulness conflict — stated explicitly by the authors

From Appendix G, verbatim:

> "there may be a certain conflict between Empathy and Helpfulness. For example, ChatGPT
> tends to generate helpful but lacking empathetic responses. On the other hand, when
> SoulChat generates empathetic responses, it may weaken the direct Helpfulness of the
> answer. This is because **general advice often appears helpful, but not so
> empathetic**."

**The data supports this and the pattern replicates across both test sets:**

| | ChatGPT | SoulChat | Direction |
|---|---|---|---|
| SoulChatCorpus — Emp. | 1.62 | **1.84** | SoulChat wins empathy |
| SoulChatCorpus — Hel. | **1.94** | 1.87 | ChatGPT wins helpfulness |
| SMILECHAT — Emp. | 1.65 | **1.90** | SoulChat wins empathy |
| SMILECHAT — Hel. | **1.97** | 1.85 | ChatGPT wins helpfulness |

The crossover is consistent in both directions on both datasets. **Caveat: these are
4 models × 2 datasets — a suggestive pattern, not a measured correlation.** The authors
assert the conflict qualitatively; they do **not** report a correlation coefficient or
significance test for it. Do not upgrade this to "empathy and helpfulness are
negatively correlated (p<...)" — that number does not exist in this paper.

### Implication for our platform

If we score companion quality with a rubric that includes a "helpfulness" item, we may be
**actively penalizing the behavior we want**. A single aggregate "quality" score that sums
empathy and helpfulness would rank ChatGPT and SoulChat nearly identically (1.62+1.94 =
3.56 vs 1.84+1.87 = 3.71) while hiding that they are opposite products. **Empathy and
helpfulness must be reported separately and never averaged** for a companion eval.

## SoulChatCorpus (verified statistics)

- **2,300,248 samples** final (the abstract's "more than 2 million")
- **12 topics** of psychological counseling
- Built from **215,813 long-text questions** and **619,725 long-text answers** via data
  outsourcing/crowdsourcing
- **105,134 low-quality samples removed** during manual proofreading
- Base model: **ChatGLM-6B** (6.2B params)
- Input format uses literal Chinese role prefixes: `用户：` (User:) and `心理咨询师：`
  (Psychologist:)

Comparison datasets named: efaqa (20,000 conversations), PsyQA (22,346 questions /
56,063 single-turn long-text answers), SMILECHAT (355,733 samples).

**Ethics note relevant to us:** they filtered samples containing 我是 (I am), 自杀
(suicide), 跳楼 (jumping off a building) and removed harmful conversations entirely.
That filtering is very likely **why Safety scored a flat 1.0** — the test set had the
safety-relevant content removed from it. A safety dimension evaluated on
safety-scrubbed data cannot measure safety. Worth remembering as a design anti-pattern.

## Limitation the authors flag (useful for us)

> "Different users have different expectations for the output of the model. For example,
> when discussing tense emotions, there are significant differences in the solutions
> expected by adults and adolescents."

They call for conditioning on **user personality, identity, gender** — i.e. empathy
quality is **user-relative**, not a property of the response alone. This is a
measurement-validity problem for any single-rubric empathy score, and connects to
`psycho-measurement-invariance-dif.md`.

## Sources

- https://aclanthology.org/2023.findings-emnlp.83/ (paper page)
- PDF full text extracted and read directly (pypdf) for all numbers above
- https://github.com/scutcyr/SoulChat
