---
title: "SocialBench: Sociality Evaluation of Role-Playing Conversational Agents"
url: https://arxiv.org/abs/2403.13679
authors: Hongzhan Chen, Hehong Chen, Ming Yan, Wenshen Xu, Xing Gao, Weizhou Shen, Xiaojun Quan, Chenliang Li, Ji Zhang, Fei Huang, Jingren Zhou
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# SocialBench: Sociality Evaluation of Role-Playing Conversational Agents

- **arXiv**: 2403.13679 — v1 submitted 20 March 2024; v4 last revised 5 August 2024
- **Venue**: Findings of ACL 2024
- **Code / data**: https://github.com/X-PLUG/SocialBench (Alibaba X-PLUG)

## Abstract (verbatim)

> Large language models (LLMs) have advanced the development of various AI conversational agents, including role-playing conversational agents that mimic diverse characters and human behaviors. While prior research has predominantly focused on enhancing the conversational capability, role-specific knowledge, and stylistic attributes of these agents, there has been a noticeable gap in assessing their social intelligence. In this paper, we introduce SocialBench, the first benchmark designed to systematically evaluate the sociality of role-playing conversational agents at both individual and group levels of social interactions. The benchmark is constructed from a variety of sources and covers a wide range of 500 characters and over 6,000 question prompts and 30,800 multi-turn role-playing utterances. We conduct comprehensive evaluations on this benchmark using mainstream open-source and closed-source LLMs. We find that agents excelling in individual level does not imply their proficiency in group level. Moreover, the behavior of individuals may drift as a result of the influence exerted by other agents within the group. Experimental results on SocialBench confirm its significance as a testbed for assessing the social interaction of role-playing conversational agents. The benchmark is publicly accessible at https://github.com/X-PLUG/SocialBench.

## Core idea

SocialBench is the only one of the four benchmarks organized around **social intelligence** rather than persona/personality fidelity, and the only one that evaluates **group dynamics** (multiple characters interacting) in addition to one-on-one behavior.

Two headline findings, both directly relevant to companion products:
1. **Individual-level competence does not predict group-level competence** — they are separable capabilities.
2. **Behavior drifts under group influence** — an agent's persona destabilizes when other agents exert social pressure.

## Dimensions

### Individual level (6 subcategories, grouped into 3 abilities)

**Self-Awareness (SA)**
- **Self-Awareness on Role Style (SA Style)** — understanding not only the role's knowledge but also the role's distinct behavioral style.
- **Self-Awareness on Role Knowledge (SA Know.)** — understanding character-specific facts, experiences and background.

**Emotional Perception (EP)**
- **Emotional Perception on Environment (EP Situ.)** — acquire high-level feeling perception of the situation/environment for effective social interactions.
- **Emotion Detection (EP Emo.)** — analyzing the current speaker's emotions (happiness, sadness, etc.).

**Conversation Memory (CM)**
- **Short-Term Conversation Memory (CM Short)** — recalling keywords within 40 utterances.
- **Long-Term Conversation Memory (CM Long)** — recalling keywords over 40 utterances.

### Group level (3 categories — Social Preference)

- **Positive Social Preference (Pos.)** — cooperation, coordination, teamwork behaviors.
- **Neutral Social Preference (Neu.)** — aligning with majority opinion, taking a neutral stance.
- **Negative Social Preference (Neg.)** — competition, refusal to cooperate, conflict.

The group level asks: given a group conversation, does the agent's social stance behave as the character would — and does it hold that stance under pressure from other agents?

## Methodology / how it scores

**No LLM judge. No human judge at inference.** SocialBench is deliberately **objective and reproducible** — this is its key design difference from PersonaGym and InCharacter.

**Question formats**:
- Multiple-choice questions — **single-answer** and **multiple-answer** variants
- Open-domain generation scored by **keyword matching**

**Scoring**:
- **Single-answer MC**: `Accuracy = correct choices / total questions`
- **Multiple-answer MC**: `∑ᵢ (Scoreᵢ / MaxScoreᵢ)` — partial credit applies
- **Conversation Memory**: keyword coverage rate = `matched keywords / total keywords`

This makes SocialBench cheap, deterministic, and free of judge bias — at the cost of not measuring free-form generation quality. It tests *recognition/discrimination*, not *production*.

## Dataset statistics

**Totals**: 500 characters · 6,000+ question prompts · 30,800 multi-turn role-playing utterances · ~1,000 scenarios

Per-category breakdown:

| Category | Questions | Avg Utterances | Avg Tokens/Utterance |
|---|---|---|---|
| SA Style | 1,063 | 17.9 | 32.6 |
| SA Know. | 1,408 | 9.4 | 66.7 |
| EP Situ. | 193 | 1.0 | 286.3 |
| EP Emo. | 1,016 | 6.4 | 23.0 |
| CM Short | 773 | 23.9 | 37.6 |
| CM Long | 1,348 | 76.7 | 41.2 |
| Pos./Neu./Neg. (group) | 1,916 total | ~16 avg | ~40 avg |

Note the shape: **CM Long is the largest single category (1,348 q, avg 76.7 utterances)** — long-context memory is heavily weighted. **EP Situ. is tiny (193 q)** but has by far the longest context per item (286.3 tokens/utterance, single utterance = a situation description).

## Results

**Open-source models** (average score):
- LLaMA-2 (7B / 13B / 70B Chat): 48.76% – 67.61%
- Mistral-7B: 50.12%
- Qwen (7B / 14B / 72B Chat): 66.44% – 83.87%

**Closed-source / specialized**:
- **Xingchen-Plus** (specialized role-playing): **85.43%** — top performer
- **GPT-4-Turbo**: **84.57%**
- Qwen-Max: 82.04%
- GPT-3.5-Turbo: 73.17%

**Key finding (verbatim from abstract)**: "agents excelling in individual level does not imply their proficiency in group level."

Notable: a **role-play-specialized model (Xingchen-Plus) beats GPT-4-Turbo**, and Qwen-72B (83.87%) is competitive with GPT-4-Turbo — strong evidence that domain specialization and Chinese-centric training matter more than raw scale for this task. Contrast with PersonaGym, where scale/recency also failed to predict performance.

## Limitations (verbatim)

> 1) Social interactions, particularly within group settings, are inherently complex and nuanced... 2) The number of role-playing agents in group scenarios is relatively limited... 3) Our dataset may contain some biased content, posing a risk of improper use.

### Additional criticisms (our assessment)

- **Multiple-choice ≠ roleplay.** The format measures whether a model can *pick* the in-character option, not whether it can *generate* in-character dialogue. A model can ace discrimination and still produce flat roleplay. This is the fundamental validity gap.
- **Keyword matching for memory** is brittle — it rewards lexical recall over semantic recall; a correct paraphrase scores zero.
- **Group size capped** at 2–10 characters (acknowledged in limitations).
- **Ceiling approaching**: top models at 84–85% leaves limited headroom.

## Human annotation and agreement

**Protocol**: "three different annotators to label each question. If all three annotators deem the question valid and agree on the answer, it is considered valid."

**Disagreement resolution**:
- Two or more annotators disagreeing → **discard the question**
- One annotator disagrees → **secondary review by a fourth annotator**

**Annotators**: recruited from crowdsourcing companies, "mainly consist of undergraduate students."

Note: this is a **unanimity-based data-cleaning protocol, not a reported agreement coefficient.** SocialBench does not publish a Kappa. The benchmark is constructed so that surviving items have unanimous (or 3-of-4 adjudicated) agreement by design — meaning reported difficulty is on pre-filtered, high-consensus items only. Ambiguous social situations — arguably the interesting ones — are filtered out.

## Multilingual and multi-turn support

- **Multilingual / Chinese**: **YES — genuinely bilingual.** "constructed from diverse English and Chinese books, movies, and novels." From Alibaba, Chinese-first orientation; Qwen and Xingchen-Plus results reflect this.
- **Multi-turn**: **YES — the strongest multi-turn support of the four.** 30,800 multi-turn utterances. Group dialogues consist of **2 to 10 characters**. Conversation memory is explicitly tested at short (<40 utterances) and long (>40, avg 76.7) horizons. The **behavioral-drift-under-group-influence** finding is a genuine multi-turn, multi-agent result.

This is the only benchmark of the four that measures **long-horizon consistency and drift**, which is the central failure mode of companion products.

## Relevance to companion-eval-platform

- **The most relevant of the four for companion-specific risk.** Long-term memory (CM Long) and behavioral drift are exactly what breaks long-running companion relationships, and this is the only source that instruments them.
- **The drift-under-group-influence finding** is a direct product warning: personas destabilize under social pressure. If our platform supports group chat or multi-character scenes, this needs a dedicated eval dimension.
- **Cheap deterministic scoring** (MC + keyword match) is attractive for CI/regression testing — run it on every model update, no judge cost, no judge variance. Good complement to expensive LLM-judge rubrics.
- **Bilingual EN/ZH** out of the box.
- **Main caveat**: multiple-choice recognition does not validate generation quality. Use SocialBench as a *regression gate*, not as the primary quality measure. Pair with a PersonaGym-style generative rubric.
- **Reusable structure**: the individual-vs-group split, and the Pos./Neu./Neg. social-preference taxonomy, are both directly adoptable dimension sets.
