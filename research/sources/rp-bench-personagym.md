---
title: "PersonaGym: Evaluating Persona Agents and LLMs"
url: https://arxiv.org/abs/2407.18416
authors: Vinay Samuel, Henry Peng Zou, Yue Zhou, Shreyas Chaudhari, Ashwin Kalyan, Tanmay Rajpurohit, Ameet Deshpande, Karthik Narasimhan, Vishvak Murahari
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# PersonaGym: Evaluating Persona Agents and LLMs

- **arXiv**: 2407.18416 — v1 submitted 25 July 2024; v5 last revised 5 September 2025
- **Venue**: Findings of EMNLP 2025
- **Code**: https://github.com/vsamuel2003/PersonaGym
- **Project site**: https://personagym.com

## Abstract (verbatim)

> Persona agents, which are LLM agents conditioned to act according to an assigned persona, enable contextually rich and user aligned interactions across domains like education and healthcare. However, evaluating how faithfully these agents adhere to their personas remains a significant challenge, particularly in free-form settings that demand consistency across diverse, persona-relevant environments. We introduce PersonaGym, the first dynamic evaluation framework for persona agents, and PersonaScore, a human-aligned automatic metric grounded in decision theory that enables comprehensive large-scale evaluation. Our evaluation of 10 leading LLMs across 200 personas and 10,000 questions reveals significant advancement opportunities. For example, GPT-4.1 had the exact same PersonaScore as LLaMA-3-8b despite being a more recent and advanced closed source model. Importantly, increased model size and complexity do not necessarily enhance persona agent capabilities, underscoring the need for algorithmic and architectural innovation toward faithful, performant persona agents.

## The five evaluation tasks (dimensions)

PersonaScore is the aggregate of five task scores. Definitions as stated in the paper:

1. **Expected Action** — the persona takes actions within its response to the question that is logically expected of the persona in the setting of the question.
2. **Linguistic Habits** — adherence to persona-appropriate communication patterns; measures whether the agent's linguistic choices (jargon, syntax, tone, speech style) align with prescriptive expectations of the persona.
3. **Persona Consistency** — fidelity to established persona attributes when directly questioned; measures whether the agent maintains its prescribed persona characteristics rather than drifting or breaking character.
4. **Toxicity Control** — examines responses to potentially provocative prompts targeting persona-relevant sensitive topics. Scoring is inverted relative to harm: higher scores for appropriate responses, lower scores for toxic ones.
5. **Action Justification** — requires the agent to explain purported actions in specific scenarios. This reveals internal reasoning mechanisms and assesses whether the agent can generate explanations consistent with its persona.

### Decision-theoretic grounding

The task suite is organized around three branches of decision theory:

- **Normative** — what the persona *ought* to do (Expected Action, Toxicity Control).
- **Prescriptive** — how the persona ought to present/communicate given real constraints (Linguistic Habits, Persona Consistency).
- **Descriptive** — how the persona actually reasons about and explains its choices (Action Justification).

## Methodology / how it scores

**Dynamic, not static.** Given a persona, the framework selects relevant environments from a pool of **150 diverse environment options** and dynamically generates persona-and-environment-specific questions per task. This is the "dynamic" claim: the question set is a function of the persona, not a fixed list.

**Pipeline**:
1. Persona → relevant environment selection (from 150 environments).
2. Environment + task → dynamic question generation.
3. Persona agent answers free-form.
4. Rubric-based LLM-judge scoring.

**Scoring mechanics**:
- **1–5 point rubric**, with task-specific scoring guidelines.
- **LLM-generated exemplars** are produced for each score level (1 through 5) for each persona–question pair, so the judge grades against concrete anchors rather than an abstract scale. This is the key mechanism for human alignment.
- **Ensemble of 2 evaluator models**: GPT-4o and LLaMA-3-70b, at **temperature 0**.
- **Final score** = average across both evaluator models.
- **PersonaScore** = average across the five task scores.

**Judge type**: LLM-as-judge (ensemble, rubric + per-level exemplars). No human in the scoring loop at inference time; humans were used only for validation.

## Human alignment / agreement numbers

- **Spearman correlation** with human judgments: averaged **75.1%** across three models; highest observed **84.8%**.
- **Kendall-Tau correlation**: averaged **62.73%**; peak **77.2%**.
- **Inter-annotator agreement**: "we witness strong inter-annotator agreement, with a Fleiss' Kappa score of **0.71** across all annotators."

Verbatim: "Overall PersonaScore correlations averaged 75.1% (Spearman) and 62.73% (Kendall-Tau) across the three models."

## Main results table (Table 2)

Per-task scores and overall PersonaScore, 1–5 scale:

| Model | Action Just. | Expected Action | Ling. Habits | Persona Cons. | Toxicity Ctrl. | **PersonaScore** |
|---|---|---|---|---|---|---|
| LLaMA-2-13b | 3.96 | 3.87 | 3.77 | 4.12 | 4.18 | **3.98** |
| GPT-3.5 | 4.31 | 4.28 | 3.63 | 4.70 | 4.96 | **4.38** |
| LLaMA-2-70b | 4.44 | 4.32 | 3.85 | 4.67 | 4.68 | **4.39** |
| LLaMA-3-8b | 4.55 | 4.43 | 3.97 | 4.77 | 4.74 | **4.49** |
| Claude 3 Haiku | 2.47 | 4.28 | 3.04 | 3.47 | 4.94 | **3.64** |
| Claude 3.5 Sonnet | 4.52 | 4.37 | 3.98 | 4.81 | 4.88 | **4.51** |
| GPT-4.1 | 4.51 | 4.20 | 4.10 | 4.67 | 4.96 | **4.49** |
| Deepseek-V3 | 4.54 | 4.20 | 4.26 | 4.66 | 4.74 | **4.48** |
| LLaMA-3.3-70b | 4.34 | 4.12 | 3.92 | 4.56 | 4.86 | **4.36** |
| GPT-4.5 | 4.57 | 4.21 | 4.14 | 4.70 | 4.96 | **4.51** |

**Headline finding**: GPT-4.1 ties LLaMA-3-8b at exactly **4.49** — the abstract's central claim. Top score is 4.51 (Claude 3.5 Sonnet and GPT-4.5, tied). Claude 3 Haiku is a notable outlier at 3.64, dragged down almost entirely by Action Justification (2.47) and Linguistic Habits (3.04) while scoring 4.94 on Toxicity Control.

**Scale compression is worth noting for platform design**: 8 of 10 models fall in a 4.36–4.51 band (0.15 points). The metric discriminates poorly at the top end. Linguistic Habits is the most discriminative task (3.63–4.26 spread); Toxicity Control is the least (most models ≥4.7, ceiling effect).

## Dataset size and scale

- **200 personas**
- **10,000 questions** total (dynamically generated)
- **150 environments** in the selection pool
- **10 LLMs** evaluated (see table above)
- Repo ships a pre-built benchmark via `--benchmark benchmark-v1`

## Limitations (verbatim)

> Although we firmly believe that the 200 personas included in our current benchmark are sufficient for justifying our findings, we acknowledge that these personas do not provide equal representation of all socio-demographic groups. Future versions of PersonaGym benchmark will be aimed at improving the distribution of represented socio-demographic groups.

### Additional limitations / criticisms (our assessment)

- **Judge-family contamination**: GPT-4o is in the evaluator ensemble while GPT-family models are among the evaluated systems — a self-preference risk the paper does not control for.
- **Ceiling / compression**: as above, near-saturation on several tasks limits headroom and makes rank ordering fragile.
- **Persona type**: personas are demographic/occupational descriptors, *not* established fictional characters with canon. This is a meaningful difference from InCharacter and SocialBench, and matters for a companion platform where characters have backstory.

## Multilingual and multi-turn support

- **Multilingual/Chinese**: **No mention.** English-only by construction.
- **Multi-turn**: **No mention.** Evaluation is single-turn question → response. Each question is answered independently; there is no dialogue history, no conversation state, and no drift-over-time measurement.

This is the single largest gap for a companion/roleplay platform: PersonaGym measures persona fidelity in isolated one-shot responses, not sustained conversational consistency.

## Repository notes

- Supports OpenAI, Anthropic, and TogetherAI API providers.
- Python 3.9 / Conda; `pip install -r requirements.txt`; keys in `api_keys.py`; entry point `run.py`.
- Structure: `code/` (personas + static environments), `evaluations/`, `prompts/`, `questions/benchmark-v1/`, `rubrics/`.
- Supports checkpointing — pre-generated questions and responses can be reloaded to resume an evaluation.

## Relevance to companion-eval-platform

- The **rubric + per-score-level exemplar** technique is the most directly reusable idea here: it is what buys the 0.71 Fleiss Kappa / 75.1% Spearman alignment, and it transfers to any 1–5 LLM-judge dimension we define.
- The **dynamic question generation** (persona → environment → question) is reusable for generating character-specific eval sets rather than a fixed battery.
- The **five tasks map cleanly onto companion concerns**, but Toxicity Control needs inverting for our purposes and Persona Consistency needs extending to multi-turn.
- **Do not** adopt PersonaScore as-is: single-turn and English-only.
