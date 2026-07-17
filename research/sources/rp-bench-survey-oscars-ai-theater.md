---
title: "The Oscars of AI Theater: A Survey on Role-Playing with Language Models"
url: https://arxiv.org/abs/2407.11484
authors: Nuo Chen, Yan Wang, Yang Deng, Jia Li (HKUST-GZ, Tencent AI Lab, SMU)
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# Survey — The Oscars of AI Theater

**arXiv:** 2407.11484 (submitted 16 Jul 2024; latest revision 10 Jan 2025). HTML: https://arxiv.org/html/2407.11484v3
**Companion repo:** https://github.com/nuochenpku/Awesome-Role-Play-Papers

> **HIGHEST-VALUE ITEM IN THE SET.** This survey contains the cleanest, most complete, explicitly-defined **4×N evaluation dimension taxonomy** in the role-play literature. It maps almost 1:1 onto RAIDEN's 11 dimensions and is the natural spine for a companion-eval rubric.

## Abstract (VERBATIM)

> This survey explores the burgeoning field of role-playing with language models, focusing on their development from early persona-based models to advanced character-driven simulations facilitated by Large Language Models (LLMs). Initially confined to simple persona consistency due to limited model capabilities, role-playing tasks have now expanded to embrace complex character portrayals involving character consistency, behavioral alignment, and overall attractiveness. We provide a comprehensive taxonomy of the critical components in designing these systems, including data, models and alignment, agent architecture and evaluation. This survey not only outlines the current methodologies and challenges, such as managing dynamic personal profiles and achieving high-level persona consistency but also suggests avenues for future research in improving the depth and realism of role-playing applications.

## TOP-LEVEL TAXONOMY — 4 critical components

1. **Data**
2. **Models and Alignment**
3. **Agent Architecture**
4. **Evaluation**

---

## ⭐ THE EVALUATION DIMENSION TAXONOMY (Section 6.1) — VERBATIM

**Four top-level dimensions, each with named sub-dimensions and definitions.** This is the item to reuse.

### 6.1.1 Conversation Ability

- **Linguistic Quality** — encompasses **"fluency and diversity."**
  - *Fluency* ensures **"grammatical correctness of responses, ensuring they are readable and free from obvious errors"**
  - *Diversity* evaluates **"the richness of vocabulary used in responses"**
- **Coherence** — evaluates how **"relevant and logically consistent responses are with the ongoing conversation context"**

### 6.1.2 Role-Persona Consistency
*(Does the agent's stated self match the assigned persona?)*

- **Attributes** — provides **"essential background information for language models to play as a specific role"**, including **"experiences, identities, interests, viewpoints, age, gender, achievements, and titles"**
- **Relations** — involves **"relationships between the speaker and others within the dialogue context"**, considering **"familiarity, intimacy, animosity, or respect"**

### 6.1.3 Role-Behavior Consistency
*(Does the agent **act** like the persona?)*

- **Conversational Style** — **"The style of conversation should reflect the role's typical manner of speech."**
- **Personality** — **"Consistency in personality helps in forming a solid, believable character."**
- **Linguistic Features** — include **"specific language use patterns, such as vocabulary, syntax, and register appropriate to the role."**

### 6.1.4 Role-Playing Attractiveness
*(Is it actually enjoyable? — the dimension unique to entertainment/companion use)*

- **Human Likeness** — models should **"exhibit the naturalness of human interaction."**
- **Engagement** — models should **"actively keep the user interested and involved in the conversation."**
- **Proactivity** — agents should **"actively initiate and drive conversations."**
- **Empathy** — (named in the figure caption; definition not given in prose)

> **The Persona/Behavior split (6.1.2 vs 6.1.3) is the key conceptual move:** an agent can *know* its persona (attributes, relations) while failing to *behave* as it (style, personality, register). These are separately measurable and separately fixable.

---

## EVALUATION METHODS TAXONOMY (Section 6.2)

Three families:

### Reference-based Evaluation
Compares generated outputs against gold-standard responses.
- **Absolute Metrics** — pass/fail judgments; also multi-choice formats
- **Relative Metrics** — ranking comparisons

### Human-based Evaluation
Trained annotators assess outputs.
- **Scoring-based** — numerical ratings
- **Ranking-based** — relative ordering of model outputs

### LLM-based Evaluation
Language models serve as evaluators, assessing consistency and quality without human intermediaries.

**Composite requirement (VERBATIM):**
> no single metric suffices to fully assess their performance. Thus, a composite approach, utilizing multiple metrics in tandem, is essential.

---

## ⭐ WHERE THE SURVEY CRITICIZES THE FIELD

### On LLM-based evaluation — judge sensitivity
> **Sensitivity in LLM-Based Evaluation**

Flagged as a named challenge in Section 7: LLM-based approaches demonstrate **inconsistency and dependence on model selection** — i.e., your reported result depends on which judge you happened to pick, which destroys cross-paper comparability.

*(Corroborated independently by RAIDEN, which found GPT-4 judges flip their verdict when response order is reversed — see `rp-bench-raiden.md`.)*

### On human evaluation — imbalance, bias, cost
> **Imbalance, Bias and Cost in Human-based Evaluation**

Three interconnected problems: **uneven annotator expertise, subjective interpretation variations, and prohibitive labor expenses** for comprehensive assessment.

On why role-play annotation is uniquely hard (VERBATIM):
> the task of annotating high-quality preference data for role-playing is significantly more challenging than for a generic assistant, as it necessitates a deep understanding of the specific character

→ **This is the crux for a companion platform.** You cannot crowdsource role-play preference labels the way you crowdsource helpfulness labels — the annotator must know the character. (ECHO's acquaintance-evaluator design is one answer to exactly this; RAIDEN's answer is expert annotators + 91.4% triple-agreement.)

### On missing metrics
> **More Reference-based Metrics for evaluating Role-Playing**

The survey emphasizes the **absence of standardized comparison benchmarks** comparable to those established in traditional NLP tasks — current metrics remain insufficient.

### Other named challenges (from abstract + Section 7)
- **Managing dynamic personal profiles**
- **Achieving high-level persona consistency**

### ⚠️ Extraction caveat — contamination & non-comparability
An automated fetch returned a claim that the survey notes challenges including "data contamination" and "non-comparability across models." **This phrasing could not be confirmed verbatim in the retrieved text and may be a paraphrase artifact of the extraction model.** The *substance* — that judge choice drives results (sensitivity) and that no standardized reference metrics exist — IS confirmed and independently supports the non-comparability point. **Do not quote "data contamination" as verbatim from this survey without re-checking the PDF.** RAIDEN, by contrast, addresses contamination explicitly and verifiably (API-free judge + private test split "serves to prevent potential data leakage").

---

## ⭐ CROSSWALK — Oscars taxonomy ↔ RAIDEN's 11 dimensions

The two independently-developed schemes converge, which is a strong signal the taxonomy is real and not arbitrary:

| Oscars dimension | Sub-dimension | RAIDEN equivalent |
|---|---|---|
| Conversation Ability | Linguistic Quality (fluency, diversity) | Chit-Chat (CC) |
| Conversation Ability | Coherence | Chit-Chat (CC), Conversation Memory (CM) |
| Role-Persona Consistency | Attributes | Script-Based Knowledge (SBK), Script-Agnostic Knowledge (SAK) |
| Role-Persona Consistency | Relations | Script-Based Knowledge (SBK) |
| Role-Behavior Consistency | Conversational Style | Persona Language Style (PLS) |
| Role-Behavior Consistency | Personality | Persona Language Style (PLS), Persona-Behavior (PB) |
| Role-Behavior Consistency | Linguistic Features | Persona Language Style (PLS) |
| Role-Playing Attractiveness | Human Likeness | *(ECHO's whole benchmark)* |
| Role-Playing Attractiveness | Engagement | Topic Advancement (TA) |
| Role-Playing Attractiveness | Proactivity | Topic Shift (TS), Topic Advancement (TA) |
| Role-Playing Attractiveness | Empathy | Emotional Resonance (ER) |
| *(not covered)* | — | Script-Contradictory Knowledge (SCK) — correcting user errors |
| *(not covered)* | — | Role-Cognition Boundary (RCB) — refusing out-of-scope questions |

**Two gaps in the Oscars taxonomy that RAIDEN covers and a companion platform needs:**
- **SCK** — does the agent push back when the user asserts something false about the character?
- **RCB** — does the agent refuse questions outside the character's knowledge horizon? (This is also TimeChara's entire concern, generalized.)

Conversely, **TimeChara's time-dependent axis is absent from both surveys** — the Persona-to-Personalization survey explicitly flags "Point-in-time role-playing... presents an area for further study."
