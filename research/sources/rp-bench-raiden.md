---
title: "RAIDEN Benchmark: Evaluating Role-playing Conversational Agents with Measurement-Driven Custom Dialogues"
url: https://aclanthology.org/2025.coling-main.735/
authors: Bowen Wu, Kaili Sun, Ziwei Bai, Ying Li, Baoxun Wang (Platform and Content Group, Tencent)
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# RAIDEN Benchmark

**Venue:** Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025), pages 11086–11106.
**PDF:** https://aclanthology.org/2025.coling-main.735.pdf
**No arXiv version found.** Discovered via ACL Anthology.

> **Relevance to a companion-eval platform: HIGHEST of the six.** This is the only source that is natively Chinese, natively multi-turn, natively dialogue-based, includes an *Emotional Companionship* role category, and ships a trained open judge model. Its design (one dimension per turn, pairwise comparison, API-free judge) is close to a blueprint.

## Abstract (VERBATIM)

> As Large-scale Language Models (LLMs) advance, the development of engaging Role-Playing Conversational Agents (RPCAs) has gained prominence. Despite this progress, there is a notable absence of benchmarks designed around dialogues, rather than question-answering formats, to assess the effectiveness of RPCA interactions. This paper introduces the RAIDEN benchmark, containing a comprehensive dataset specifically developed for RPCA evaluation, comprising over 40,000 multi-turn utterances across 135 characters. The benchmark focuses on assessing particular dimensions at different stages of a conversation, facilitated through interactions conducted by annotators. This approach allows the evaluation phase to concentrate on specific response dimensions, and thus subjectivity in dialogue evaluation is reduced. To further enhance objectivity, evaluators compare responses from two different models rather than assessing a single response in isolation. Besides, we introduce RPCAJudger, a specialized judging LLM tailored for automatic RPCA evaluation. The evaluations conducted by RPCAJudger closely mirror human judgments, and its API-free methodology serves to prevent potential data leakage. All the models and all non-private leaderboard data will be made publicly available.

## The 11 Dimensions (VERBATIM definitions)

RAIDEN refines "self-awareness and conversational ability into 11 dimensions." Two top-level groups:

### Group 1 — Self-Awareness (5 dimensions)

Framing (verbatim):
> Previous studies have typically assessed self-awareness through knowledge consistency and persona consistency (Tu et al., 2024; Chen et al., 2024). In this work, we further refine these aspects. Specifically, knowledge consistency requires agents to possess both in-script knowledge and out-of-script knowledge, and to understand the boundaries of their identity (Wang et al., 2023b). Persona consistency demands the language style aligning with the character's traits.

- **Script-Based Knowledge (SBK)** — "examines the model's ability to follow the knowledge explicitly provided in the profile (Zhou et al., 2023), such as identity, interests, experiences, social relations, etc."
- **Script-Agnostic Knowledge (SAK)** — "requires the agent to understand knowledge inherent to the character but not shown in the provided materials. For example, a Harry Potter agent should comprehend that Hermione founded the Society for the Promotion of Elfish Welfare."
- **Script-Contradictory Knowledge (SCK)** — "assesses the model's ability to correct users' inaccurate and misleading questions, a common phenomenon in user-agent dialogues."
- **Role-Cognition Boundary (RCB)** — "implies that the model should decline to answer questions that fall outside the character's scope, such as a historical figure facing questions about modern society."
- **Persona Language Style (PLS)** — "needs RPCAs to use the same language style as the acted roles, such as catchphrases, speaking styles, and classic quotes, which can establish more realistic characters and improve user immersion."

### Group 2 — Conversational Ability (6 dimensions)

Framing (verbatim):
> Conversation ability is essential for a role-playing agent, as it determines its capacity to engage users in prolonged conversations (Zhou et al., 2023). Specifically, fluent conversations and precise memories are fundamental requirements. In addition, the ability to actively steer conversations, vividly describe behaviors and psychological states, and provide emotional value can significantly enhance the engagement and appeal of interactions.

- **Emotional Resonance (ER)** — "refers to the ability of an agent to identify and respond to a user's emotional state in a manner that makes the user feel understood and supported. Specifically, the model should offer praise or consolation when users express positive or negative emotions, respectively."
- **Persona-Behavior (PB)** — "pertains to the requirements for a character's actions, which are typically described within brackets. This encompasses two specific requirements: 1) following the user's specified actions and maintaining the fluency with which it executes them; 2) the consistency between the actions and the accompanying language."
- **Conversation Memory (CM)** — "means that the model should retain the content of previous conversations and utilize it to advance the current dialogue."
- **Topic Shift (TS)** — "assesses the model's capability of initiating new topics. When the user explicitly or implicitly indicates a desire to discontinue the current topic, the model should proactively introduce a new one appropriately."
- **Topic Advancement (TA)** — "measures whether the model can progress the conversation topic. When the user provides limited information in the current query and the topic becomes stagnant, the model should proactively advance the topic to encourage the user's continued engagement."
- **Chit-Chat (CC)** — "refers to situations where the user does not have a strong conversational objective in the current dialogue turn. The response from the role-playing agent should be evaluated based on logical coherence, fluidity of dialogue, and adherence to natural human communication patterns."

## Dataset statistics

Role profiles (Table 1) — 4 role types, "135 roles with wide Chinese audiences":

| Category | # role | # token / profile |
|---|---|---|
| Celebrities | 35 | 852.2 |
| Fictional Characters | 70 | 1268.8 |
| Daily Life | 17 | 688.9 |
| **Emotional Companionship** | **13** | **664.7** |
| Total | 135 | 1029.6 |

Dialogues (Table 2):

| Category | Short | Long | Total |
|---|---|---|---|
| # dialogue | 1080 | 270 | 1350 |
| # utterance | 22920 | 17598 | 40518 |
| # utterance / dialogue | 21.22 | 65.18 | — |
| # token / utterance | 46.68 | 38.14 | 42.97 |

Short dialogues ≈10 turns, long ≈30 turns. 7 dialogue-level dimension combinations (Table 5) — 5 short, 2 long — each tagged as primarily inspecting Self-Awareness or Conversational Ability.

## How it scores

**Data construction pipeline** (Figure 2): Step I Profile Collecting → Step II Auxiliary Production (a: Character-Specific Component; b: General Component; c: Dimensional Query; d: Dialogue Base) → Step III Manual Annotation and Dimensioning.

Key design — **one dimension per turn, human-in-the-loop dialogue**:
> Before starting the conversation, the annotator, acting as the user, must review the entire dialogue draft and design queries relevant to the CM dimension. Once prepared, the conversation can begin. While dialogue drafts are provided, annotators have considerable freedom to guide the conversation. They can omit unsuitable queries, introduce new questions, correct factual inaccuracies, improve language style, etc. Directly copying utterances from the draft is prohibited, and annotators must vary the language used in evaluation dimensions, with strict automated screening in place. Additionally, during the conversation, annotators must mark the evaluation dimensions corresponding to each turn.

**Dataset validation** — manual inspection removes: "1) typographical errors; 2) awkward or ungrammatical sentences; 3) mismatches between queries and labeled evaluation dimensions; 4) queries that do not clearly reflect the evaluation dimension requirements; 5) responses with knowledge inconsistent with the character profile; 6) responses with language style misaligned with the character profile."

**Scoring = pairwise win-rate, not absolute scoring**:
> Annotators provide pairwise comparisons between diverse models and substantiate their judgments with reasons. To enable broader model comparisons, we introduce win-rate, defined as the proportion of instances in which a model outperforms all others, calculated by dividing its winning counts by the total number of comparisons.

> Given a fixed role profile and dialogue context in the RAIDEN benchmark, models under evaluation generate their responses. Any two of them combined with the golden reference and corresponding evaluation criteria construct a pairwise sample.

## Judge bias finding (important) + agreement numbers

**They tried GPT-4 as judge and rejected it** (VERBATIM):
> We attempted to use GPT-4 to produce ranking results and reasons for specific evaluation dimensions but found it could not replace human evaluation accurately (as shown in Table 6 in Appendixes). A typical issue was that reversing the order of responses led to different results. Therefore, we introduced manual annotation to provide results and reasons, using GPT-4 predictions as a reference.

→ This is a direct, citable **position-bias** finding in an LLM judge.

**Inter-annotator agreement (VERBATIM):**
> We randomly selected three response pairs from each instance for manual annotation. To ensure objectivity and high-quality data, each sample was annotated by three experts simultaneously. Our statistical analysis revealed that **91.4% of the samples received fully consistent annotations from all three experts.**

**RPCAJudger** — trained judge, base model BC2-13B-Chat (Baichuan2-13B). Train/test split by role: **105 roles training (private set), 30 roles test (public set)**. API-free by design to prevent data leakage.

**Judge–human correlation (VERBATIM):**
> the overall assessment of model performance on the test set by RPCAJudger is entirely consistent with the conclusions drawn from manual evaluations that are shown in Table 3. Secondly, except for the Conversation Memory (CM) and Persona Language Style (PLS) dimensions, RPCAJudger and manual cross-evaluation identify the same optimal models. For CM and PLS, the divergence occurred only in selecting the optimal and second-best models when the scores were close. **The average absolute difference in overall scores for the ten evaluated models between the automatic and manual evaluations is merely 2.46%.**

**Table 6 — judge accuracy vs. human labels, per dimension:**

| Models | SBK | RCB | SCK | SAK | PLS | SA Avg | ER | TS | TA | PB | CM | CC | CA Avg | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BC2-13B-Chat | 50.7 | 45.7 | 45.7 | 42.9 | 50.6 | 47.1 | 52.2 | 39.6 | 53.3 | 35.5 | 51.0 | 48.5 | 46.7 | 46.9 |
| RPCAJudger-13B | 85.0 | 77.2 | 77.7 | 79.3 | 84.1 | 80.7 | 88.2 | 80.5 | 82.3 | 68.6 | 80.3 | 81.7 | 80.2 | 80.4 |
| GPT-4 | 92.5 | 74.1 | 86.5 | 87.7 | 92.7 | 86.7 | 94.1 | 89.7 | 93.3 | 60.1 | 87.7 | 92.4 | 86.2 | 86.4 |

Note: GPT-4 is the stronger judge overall (86.4 vs 80.4), but **RPCAJudger-13B beats GPT-4 on the two hardest dimensions: RCB (77.2 vs 74.1) and PB (68.6 vs 60.1)** — "surpasses the GPT4 model in the two most challenging dimensions." PB is the weakest dimension for every judge.

## Models evaluated (10 total)

- **Open-source (4):** Llama2-Chinese-7B-Chat, Llama2-Chinese-13B-Chat, Atom-7B-Chat, Baichuan2-13B-Chat (BC2-13B-Chat)
- **Closed-source general (3):** GPT-3.5, GPT-4, Qwen-turbo
- **Closed-source RPCA products (3):** CharacterGLM, BC-NPC-Turbo, minimax-abab6-chat

**Human-annotated win-rate ranking (overall):**
> minimax-abab6-chat > GPT-4 > Qwen-turbo > GPT-3.5 > BC-NPC-Turbo > BC2-13B-Chat > CharacterGLM > Atom-7B-Chat > Llama2-Chinese-13B-Chat > Llama2-Chinese-7B-Chat

Selected win-rates (human eval): GPT-4 Conversation Ability avg 60.47%, Self-Awareness avg ~64.54%.

## Key findings

- "minimax-abab6-chat and GPT-4 emerge as the top-performing models across both conversation ability and self-awareness dimensions. Minimax-abab6-chat demonstrates exceptional performance in emotional resonance, topic progression, and chit-chat... GPT-4 excels in conversation memory and overall self-awareness."
- **Language-match matters:** "the importance of Chinese language comprehension for Chinese RPCAs. Baichuan2, specifically optimized for Chinese, outperforms Atom, which in turn surpasses Llama2-Chinese, which only underwent supervised fine-tuning with Chinese data."
- **Role-type effects (first study of its kind):** "minimax-abab6-chat, optimized for emotional interactions, shows a significant advantage in the Emotional Companionship category. In contrast, GPT-4 excels in the Daily Life category, which requires less Chinese language understanding and knowledge." → *Directly relevant: companion-tuned models beat frontier general models on companionship roles.*

## Limitations (Section 7, VERBATIM)

> The RAIDEN benchmark is currently limited to Chinese, excluding other languages. Additionally, while pairwise evaluation reduces subjectivity compared to absolute scoring, it still does not provide an absolute measure of performance. Furthermore, the automatic evaluation model employed in this study has only 13 billion parameters. Utilizing state-of-the-art or larger-scale LLMs could potentially enhance performance, yielding scores that more closely align with human judgments and providing more precise reasoning.

## Multilingual / multi-turn

- **Chinese: native and exclusive.** Profiles, dialogues, and roles are all Chinese ("135 roles with wide Chinese audiences"). Example role: 贾宝玉 (Jia Baoyu) from Dream of the Red Chamber.
- **Multi-turn: yes, core design.** 21.22 utterances/dialogue short, 65.18 long. Multi-turn is the point — explicitly positioned against QA-format benchmarks.

## Ethics / licensing

Annotators recruited from college campuses, voluntary, paid above local minimum wage. No personal information retained. **Dataset licensed CC BY-NC 4.0** (non-commercial — note for a commercial platform).
