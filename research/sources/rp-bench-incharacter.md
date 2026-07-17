---
title: "InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews"
url: https://arxiv.org/abs/2310.17976
authors: Xintao Wang, Yunze Xiao, Jen-tse Huang, Siyu Yuan, Rui Xu, Haoran Guo, Quan Tu, Yaying Fei, Ziang Leng, Wei Wang, Jiangjie Chen, Cheng Li, Yanghua Xiao
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews

- **arXiv**: 2310.17976 — v1 submitted 27 October 2023; v4 last revised 7 June 2024
- **Venue**: ACL 2024
- **Note**: earlier versions circulated under a different title (the "Does Role-Playing Chatbots Capture the Character Personalities?" line of work)

## Abstract (verbatim)

> Role-playing agents (RPAs), powered by large language models, have emerged as a flourishing field of applications. However, a key challenge lies in assessing whether RPAs accurately reproduce the personas of target characters, namely their character fidelity. Existing methods mainly focus on the knowledge and linguistic patterns of characters. This paper, instead, introduces a novel perspective to evaluate the personality fidelity of RPAs with psychological scales. Overcoming drawbacks of previous self-report assessments on RPAs, we propose InCharacter, namely Interviewing Character agents for personality tests. Experiments include various types of RPAs and LLMs, covering 32 distinct characters on 14 widely used psychological scales. The results validate the effectiveness of InCharacter in measuring RPA personalities. Then, with InCharacter, we show that state-of-the-art RPAs exhibit personalities highly aligned with the human-perceived personalities of the characters, achieving an accuracy up to 80.7%.

## Core idea

Rather than asking an RPA to fill in a Likert questionnaire directly (**self-report**, which the paper argues is invalid for RPAs — characters would not answer a psychometric survey in character, and the format breaks immersion), InCharacter **interviews** the character with open-ended questions converted from scale items, then has a judge LLM infer the personality scores from the interview transcript.

The central methodological claim: **self-report on RPAs is unreliable; interview-then-infer is better aligned with human perception of the character.**

## The 14 psychological scales and their dimensions

| Scale | Dimensions |
|---|---|
| **Big Five Inventory (BFI)** | Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism |
| **Eysenck Personality Questionnaire-R (EPQ-R)** | Extraversion, Neuroticism, Psychoticism, Lying |
| **16 Personalities (16P)** — MBTI-based | Five independent spectrums (E/I, S/N, T/F, J/P, plus assertive/turbulent) |
| **Dark Triad Dirty Dozen (DTDD)** | Narcissism, Machiavellianism, Psychopathy |
| **Bem's Sex Role Inventory (BSRI)** | Masculinity, Femininity |
| **Comprehensive Assessment of Basic Interests (CABIN)** | Health Science, Creative Expression, Technology, People, Organization, Influence, Nature, Things |
| **Implicit Culture Belief (ICB)** | Single dimension — beliefs about cultural influence on character |
| **Experiences in Close Relationships-R (ECR-R)** | Attachment Anxiety, Attachment Avoidance |
| **General Self-Efficacy (GSE)** | Single dimension — confidence in own capability |
| **Life Orientation Test-R (LOT-R)** | Optimism orientation |
| **Love of Money Scale (LMS)** | Monetary value orientation |
| **Emotional Intelligence Scale (EIS)** | Emotional awareness / regulation |
| **Wong & Law Emotional Intelligence Scale (WLEIS)** | Self-emotion appraisal, others' emotion appraisal, emotion regulation, use of emotion |
| **Empathy Scale** | Empathetic tendency |

BFI and 16P are the two scales with external ground truth (see below) and are therefore the ones used for the headline accuracy numbers. The other 12 are reported for breadth/consistency analysis.

## Methodology

### Interview construction

- Scale items are converted into **open-ended interview questions** by LLMs, with **manual verification**.
- Critically: "each question is posed in an isolated context, thereby avoiding potential interference among the questions." Each item is its own independent single-turn exchange — this prevents earlier answers from contaminating later ones.

### Assessment — two families of method

**Option Conversion (OC)**
- A judge LLM converts the RPA's free-text response back into a Likert-scale option.
- **d-OC** (dimension-specific variant): uses descriptive anchor terms ("Extroverted" vs. "Introverted") instead of generic agreement terms ("Agree" / "Disagree"). Improves accuracy.

**Expert Rating (ER)**
- A judge LLM directly assigns personality scores across dimensions, reasoning over question–response pairs.
- **ER_all**: all question-response pairs considered simultaneously.
- **ER_batch**: batched processing. **This is the best-performing variant.**

**Baselines**
- **Self-Report (SR)**: RPA directly picks scale options. The thing InCharacter argues against.
- **SR-CoT**: self-report plus chain-of-thought reasoning.

### Judge / interviewer LLMs

GPT-3.5, GPT-4, Gemini, Qwen1.5-110B. So: **LLM-as-judge over an interview transcript**, with the psychological scale supplying the construct definitions.

## Metrics

- **Acc_dim** (a.k.a. single/dimension accuracy) — per-dimension agreement with ground-truth label.
- **Acc_full** — all dimensions of the scale correct simultaneously for a character (strict, full-profile match).
- **MSE / MAE** — error against ground-truth continuous scores.
- **StdScore** — consistency/stability measure across repeated runs.

## Results (Table 2 — BFI & 16P, averaged over three runs)

**Best InCharacter configuration (ER_batch + GPT-4):**

| Scale | Acc_dim | Acc_full | MAE |
|---|---|---|---|
| BFI | **76.6%** | 31.2% | 18.2 |
| 16P | **80.7%** | 44.8% | 20.5 |

**Self-Report baseline (GPT-4):**

| Scale | Acc_dim | Acc_full | MAE |
|---|---|---|---|
| BFI | 63.3% | 7.3% | 23.2 |
| 16P | 65.6% | 21.9% | 26.5 |

The **80.7%** in the abstract is Acc_dim on 16P with ER_batch + GPT-4.

**Interpretation**: the interview method beats self-report by ~13–15 points on Acc_dim, and by a far wider *relative* margin on Acc_full (31.2% vs 7.3% on BFI — a 4.3x improvement). The Acc_full gap is the strongest evidence for the paper's thesis: self-report almost never gets a character's whole profile right.

**Consistency (StdScore)**
- InCharacter: 2.7–5.9 across settings
- Self-report: 1.5–2.1

**Across all 14 scales**: average Acc_dim of **78.9%** with ER_batch + GPT-3.5.

## Ground truth and inter-annotator agreement

**Two ground-truth sources:**

1. **Personality Database (PDb)** — a crowd-sourced database of community-voted personality typings for fictional characters. BFI and 16P labels derived from "label percentage (e.g., 60% Extroverted)".
2. **Human annotators** — "two to three annotators for each character (**93 in total for 32 characters**)".

**Label categorization rule**: above 60% → positive; below 40% → negative; otherwise → **marginal** (marginal cases are excluded/handled separately).

**Inter-annotator agreement**: **Cohen's Kappa, average coefficient across 14 scales = 60.9%.**

> Note this is *moderate* agreement — humans themselves only agree ~61% on what a fictional character's personality is. This is an important ceiling: an RPA scoring 80.7% Acc_dim is being measured against a target that human raters only reproduce among themselves at 60.9% Kappa. Any platform reusing this method inherits that noise floor.

## Characters and models

**32 characters:**
- **16 from ChatHaruhi** — of which **6 are Chinese-language**
- **16 from RoleLLM**
- "mainly from popular fictional works, such as Harry Potter, The Big Bang Theory and Genshin Impact"

**Foundation models / RPAs tested:**
- **Closed-source**: GPT-3.5, GPT-4, character.ai
- **General open-source**: Qwen-7B, OpenChat-3.5, Mistral-2, LLaMA-2-Chat, Mixtral-8x7B
- **Role-play specialized**: CharacterGLM-6B, RP-Qwen-7B, RP-Mistral-2-7B

**Released artifact**: **18,304 interview dialogues** released for future research.

## Limitations (verbatim)

> First, the personality measurement in this paper relies on the interviewer LLMs. Consequently, the accuracy of the measured results may be compromised by potential errors or biases inherent in LLMs, potentially leading to an underestimation of the personality fidelity in RPAs. Second, the personalities of humans or fictional characters can change over time.

> the progressive changes in RPA personalities remain unexplored within existing literature. We leave the study of RPA personality dynamics for future research.

### Additional criticisms (our assessment)

- **Ground-truth validity**: PDb is crowd-voted internet opinion, not clinical assessment. "Human-perceived personality" is the honest framing the paper uses, but it is a soft target.
- **Psychometric validity on non-humans**: administering instruments validated on humans to LLMs is contested — the scales' norms, reliability, and factor structure are not established for model outputs.
- **Marginal-case exclusion** inflates accuracy by removing the hardest characters (those without clear consensus typings).
- **Judge-family effects**: GPT-4 as both judge and evaluated system.
- **Acc_full is low in absolute terms** (31.2% BFI): even the best method gets a character's complete Big Five profile right less than a third of the time.

## Multilingual and multi-turn support

- **Multilingual / Chinese**: **YES — genuine bilingual support.** "Six RPAs from ChatHaruhi are based on Chinese data, and we conduct the interview with them in Chinese." English + Chinese. This is the strongest Chinese support of the four benchmarks reviewed alongside SocialBench.
- **Multi-turn**: **Deliberately NOT multi-turn.** Questions are posed individually in isolated contexts by design — this mitigates cross-question contamination but means it does not implement or test multi-turn dialogue chains. The paper explicitly flags personality *dynamics over time* as unexplored future work.

## Relevance to companion-eval-platform

- **Most reusable asset**: the interview-then-infer pattern. For a companion product, "does this character *behave* like the persona" is better probed by naturalistic conversation than by asking the character to self-assess — and the SR vs. InCharacter gap (esp. Acc_full 7.3% → 31.2%) quantifies exactly how much self-report misleads. **Do not build self-report probes.**
- **d-OC finding** (descriptive anchors beat generic agree/disagree anchors) is a cheap, directly portable prompt-design win for any rubric we write.
- **ER_batch > ER_all** suggests judges degrade when given too much transcript at once — relevant to how we chunk long companion conversations for judging.
- **The 60.9% Cohen's Kappa is the number to internalize**: it sets a realistic expectation for what agreement we can expect from our own human raters on character-fidelity labels, and argues against over-engineering precision above that floor.
- **Bilingual (EN/ZH) design is directly applicable** if the platform targets Chinese characters.
- **Gap to fill**: no multi-turn drift measurement — which is arguably the core companion-product risk.
