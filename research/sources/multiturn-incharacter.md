---
title: "InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews"
url: https://arxiv.org/abs/2310.17976
authors: Xintao Wang, Yunze Xiao, Jen-tse Huang, Siyu Yuan, Rui Xu, Haoran Guo, Quan Tu, Yaying Fei, Ziang Leng, Wei Wang, Jiangjie Chen, Cheng Li, Yanghua Xiao
year: 2023
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews

**Status: the key prior art for measuring character identity as a latent construct rather than a per-response property.**

## Abstract

Methodology for assessing whether role-playing agents (RPAs) accurately reproduce character personalities using psychological assessment tools. "InCharacter" is an **"interview-based approach"** that surpasses **"self-report scales"** in measuring RPA personalities. Testing involved **32 characters across 14 psychological instruments**, achieving **"an accuracy up to 80.7%"** against human-annotated character traits.

## Methodology — two stages

1. **Interview Phase:** RPAs receive **"open-ended questions derived from psychological scales"**, posed **individually to avoid context interference**. Questions transform scale items into conversational prompts.
2. **Assessment Phase:** two conversion methods:
   - **Option Conversion (OC):** LLMs map responses to Likert-scale options
   - **Expert Rating (ER):** LLMs directly evaluate personality dimensions from all responses **collectively**

Note the unit of analysis: **ER scores the SET of responses, not each response.** Personality is explicitly treated as only estimable from an aggregate of probes. This is the same architectural claim our platform is making.

## Psychological scales (14 instruments)

BFI, 16Personalities (16P), Dark Triad Dirty Dozen (DTDD), EPQ-R, Bem's Sex Role Inventory (BSRI), CABIN, Implicit Culture Belief (ICB), ECR-R, General Self-Efficacy (GSE), LOT-R, Love of Money Scale (LMS), Emotional Intelligence Scale (EIS), WLEIS, Empathy Scale.

## Scope

**32 widely-recognized fictional characters** from ChatHaruhi (16) and RoleLLM (16) — Harry Potter, The Big Bang Theory, Genshin Impact, etc.

Scale items were "transformed into open-ended questions via LLMs and manually checked." Each question is asked **individually to prevent cross-item interference.**

## Key numbers

- **80.7%** accuracy (AccFull) on 16Personalities, GPT-4, Expert Rating, batch mode
- **76.6%** on BFI with GPT-4 using ER
- Interview-based methods outperform self-report by **8–15 percentage points** across metrics
- **Consistency**: self-report produced inconsistent item-level responses (**StdItem ~10–13%**); interview-based achieved **~3–5%**
- **Human inter-rater reliability**: "average coefficient across 14 scales **60.9%**" (Cohen's kappa) — "suggesting some subjectivity in personality assessment itself"

**That last number is a ceiling, and we should treat it as one.** If humans only agree 60.9% on what a character's personality *is*, any automated persona-fidelity metric that claims higher agreement is measuring something narrower than "personality."

## Why self-report / single-response evaluation fails for RPAs

- **Instruction Conflict:** directly prompting for scale responses "contradicts role-playing instructions, leading to RPAs' reluctance or inability to engage"
- **Behavioral Misalignment:** "Selected options may conflict with the actual behaviors of RPAs," rendering results unindicative of genuine personalities
- **Training Data Bias:** RPAs "might underperform owing to inadequate understanding of scale instructions and the biases inherent in the training data"

## Relevance to companion-eval-platform

- **Direct support for "the unit of evaluation is not the response."** Personality is a construct recovered from a *battery* of probes; no single response identifies it.
- **Probe batteries are compatible with replayed dialogues** and are our best lever against the off-policy problem: a probe's answer depends on the character card + accumulated context, not on the user turn being on-policy. We can inject the same probe battery at turns 10/30/50/70/90 across all 11 models and get a drift curve that is *immune to replay incoherence* because the probe is our text, not the dataset's.
- **StdItem (variance across runs of the same item)** is a directly reusable metric and maps onto our 3-runs design.
- Caveat: InCharacter is **static/one-shot** — questions asked individually with no accumulated dialogue context. It measures persona fidelity *at rest*, not persona *stability under conversational load*. Our contribution is exactly the composition of InCharacter-style probing with Persona-Drift-style turn-depth measurement.
