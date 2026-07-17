---
title: "Multi-IF: Benchmarking LLMs on Multi-Turn and Multilingual Instructions Following"
url: https://arxiv.org/abs/2410.15553
authors: Yun He, Di Jin, Chaoqi Wang, Chloe Bi, Karishma Mandyam, Hejia Zhang, Chen Zhu, Ning Li, Tengyu Xu, Hongjiang Lv, Shruti Bhosale, Chenguang Zhu, Karthik Abinav Sankararaman, Eryk Helenowski, Melanie Kambadur, Aditya Tayade, Hao Ma, Han Fang, Sinong Wang (Meta GenAI)
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Multi-IF: Multi-Turn and Multilingual Instruction Following

**Status: highly relevant — multi-turn AND multilingual (incl. Chinese), with a programmatic (judge-free) verifier and an explicit conversation-level aggregation rule.**

## Abstract

Expands IFEval by "incorporating multi-turn sequences and translating the English prompts into another 7 languages, resulting in a dataset of **4,501 multilingual conversations, where each has three turns**."

## Methodology — four-stage construction

1. **Multi-turn expansion:** each single-turn prompt generates two additional turns via random sampling of instruction types and LLM-based revision
2. **Conflict removal:** automatic LLM scanning + human verification eliminates contradictory instructions across turns
3. **Multilingual translation:** LLM translation into 7 languages (French, Russian, Hindi, Italian, Portuguese, Spanish, **Chinese**) with human auditor review
4. **Sensitive content filtering:** automated flagging + human review

**Verification: rule-based programmatic evaluation.** No LLM judge. This is why the numbers are trustworthy and why turn-depth curves from this paper are cleaner than PingPong's.

## Accuracy metrics (exact definitions — the aggregation lesson lives here)

- **Instruction-level strict accuracy:** "percentage of individual instructions that are accurately followed by LLMs"
- **Conversation-level strict accuracy:** "percentage of conversations whose **every instruction, from the first user turn to the current turn, is followed correctly**"
- **Instruction-level loose accuracy:** strict evaluation with first sentence removed (handles preambles like "Certainly, here is...")
- **Conversation-level loose accuracy:** conversation-level strict with loose criterion

**Conversation-level strict accuracy is an AND across all turns — a MIN-aggregation, not a mean.** This is precisely the "don't average away the one catastrophic turn" pattern we want, already validated in a major benchmark. It is also brutally strict: it is the probability that *nothing went wrong anywhere*, and it decays geometrically with turn count by construction. For 100-turn dialogues a pure AND would floor at ~0 for every model and lose all discriminative power. **We need the AND's spirit (min/first-failure) with a decay-robust formulation — i.e. survival analysis, which is exactly the AND rule re-expressed as a hazard.**

## Performance degradation: Turn 1 → Turn 3

| Model | Turn 1 | Turn 3 | Decline |
|---|---|---|---|
| **o1-preview** | 0.877 | 0.707 | **19.4%** |
| o1-mini | 0.853 | 0.681 | 20.1% |
| **GPT-4o** | 0.843 | 0.631 | **25.1%** |
| Llama 3.1 405B | 0.854 | 0.707 | 17.2% |
| Claude-3.5 Sonnet | 0.817 | 0.634 | 22.4% |

**Only three turns.** ~20% degradation over 3 turns, and our dialogues are ~100.

## Language breakdown — Chinese is measurably worse

**English (best):** o1-preview 0.773 at turn 3

**Non-Latin scripts (worst):**
- **Chinese:** o1-preview **0.703**, GPT-4o **0.631**
- Russian: o1-preview 0.531, GPT-4o 0.501
- Hindi: o1-preview 0.709, GPT-4o 0.621

> "Languages with non-Latin scripts (Hindi, Russian, and Chinese) generally exhibit higher error rates, suggesting potential limitations in the models' multilingual capabilities."

**English-to-Russian gap (o1-preview): 0.773 vs 0.531 — 31% absolute at turn 3.**

**Direct consequence for us: en/zh is NOT a free doubling of our dataset.** English→Chinese costs o1-preview 7 points at turn 3 and GPT-4o 14 points. Language must be a modeled covariate, never pooled. And any cross-model ranking may reorder between en and zh — which is itself a finding our platform can produce.

## Key degradation findings

1. **Instruction Forgetting Ratio (IFR):** Gemini models exhibit highest forgetting; **IFR from turn 1→2 generally EXCEEDS turn 2→3 rates**
2. **Error Correction Ratio (ECR):** "OpenAI's o1-preview and o1-mini models exhibit the highest ECR — correcting around **25%** of unfollowed instructions in later turns"
3. **Error distribution:** "Length_constraint and combination categories show consistently high error rates" across all languages

**Finding 1 is important and cuts against a naive monotone-decay model: the damage is FRONT-LOADED.** The biggest single drop is turn 1→2. Degradation decelerates. This matches the (H−i) weighting in the static-context theorem and argues that our instrumentation should be *densest in early turns*, not uniformly spaced.

**Finding 2 contradicts Laban et al.'s "do not recover" in a narrow sense** — o1 recovers 25% of failed instructions. Reconciliation: Laban's task is *conversational steering under ambiguity* (unrecoverable); Multi-IF's is *discrete constraint adherence* (recoverable). Different failure classes have different recoverability. **Our platform should not assume all failures are absorbing states** — "broke character once at turn 40" may or may not be terminal, and that's an empirical question we can answer with our data.

## Relevance to companion-eval-platform

- **Programmatic verification is the gold standard** where achievable. Our nearest analogue: character cards with checkable constraints (speech tics, forbidden knowledge, language, name usage, formatting). Extract a rule-checkable subset per character and get a judge-free drift signal.
- **Conversation-level strict accuracy** = the AND/min aggregation, validated at scale. Adopt the spirit, replace with survival for long horizons.
- **Chinese underperformance is measured and real** — model our en/zh split explicitly.
- IFR/ECR are two directly reusable, cheap metrics: forgetting rate and correction rate between adjacent turns.
