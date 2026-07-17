---
title: "MiniMaxAI/role-play-bench — Role-play Benchmark (Situated Reenactment)"
url: https://huggingface.co/datasets/MiniMaxAI/role-play-bench
authors: MiniMax AI
year: 2025
type: repo
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# MiniMax role-play-bench

**Primary sources:**
- Dataset card: https://huggingface.co/datasets/MiniMaxAI/role-play-bench
- Methodology deep dive: https://www.minimax.io/news/a-deep-dive-into-the-minimax-m2-her-2
- Applied write-up: https://www.talkie-ai.com/blog/m2-role-play

This is our **reference dataset**. It is the closest existing artifact to what our platform needs: session-level, multi-turn, cross-model, bilingual, with a fixed rubric applied identically to every model.

---

## Core framing (verbatim / near-verbatim)

The benchmark's central design claim is what it calls the **"Ground Truth Paradox"**: role-play is inherently subjective, so the benchmark refuses to define perfect responses and instead detects deviation. The stated pivot:

> "misalignment is surprisingly objective."

Methodology name: **Situated Reenactment**. On multi-turn generation:

> "Instead of evaluating static, single-turn responses, we generate multi-turn dialogue trajectories via self-play simulation."

**This is the single most transferable idea for our platform.** Do not score "is this a good response" (unanswerable, model-relative, judge-biased). Score "did this response violate a stated constraint" (checkable, model-agnostic, comparable). See synthesis note for why this resolves the cross-model comparability requirement.

---

## Dimension tree

Three pillars → six scored dimensions. Session-level scores on a **0–100 scale**.

### Pillar 1: Worlds — weight 50%

Highest weight. This pillar is the immersion substrate: violations here are catastrophic and objectively detectable.

| Dimension | Definition |
|---|---|
| **Basics** | Text quality. Surface-level errors: language mixing, repetition, formatting issues, garbled text. |
| **Logic** | Consistency of character behavior and spatial references. Catastrophic forgetting, character relationship confusion, pronoun reference errors, setting contradictions. Special emphasis on **"Reference Confusion"** — whether models remember *user-constructed* character relationships (as opposed to canon ones). |
| **Knowledge** | Factual reliability across virtual/real world boundaries. Adherence to world-specific physical and magical laws; prevents lore violations. |

### Pillar 2: Stories — weight 25%

| Dimension | Definition |
|---|---|
| **Diversity** | Expression variety and narrative momentum. Explicitly **semantic** progression, not merely lexical variety. Detects negative patterns: monotonous phrasing, repetitive plot beats, stagnation, low-information filler. |
| **Content Logic** | Narrative coherence and out-of-character (OOC) detection. Measures **"motivated character evolution"** rather than static adherence — i.e. characters are allowed to change, but the change must be motivated. |

### Pillar 3: User Preferences — weight 25%

| Dimension | Definition |
|---|---|
| **Interaction** | Quality of user engagement. Penalizes the AI speaking for the user. |

The Interaction dimension decomposes into four named failure metrics:

- **AI Speaks for User** — whether the model oversteps boundaries by acting or speaking on behalf of the user.
- **AI Ignores User** — captures whether the model talks to itself; judges whether it specifically responds to user behavior and context.
- **AI Silence** — judges whether the model provides "hooks" that invite a reply; penalizes purely descriptive narration that gives the user nothing to respond to.
- **Interaction Boundary** — balances safety compliance against emotional engagement.

**Note the asymmetry:** "Diversity" is the only dimension in the whole tree that rewards a positive quality rather than penalizing a failure. Everything else is deviation-detection. This is deliberate and is why the scores are comparable across models.

---

## Scoring methodology

- **LLM-as-Judge** with **chunked judging**: 100-turn conversations are sliced into 20-turn segments and judged per-chunk, then aggregated. This bounds judge context length and prevents late-conversation errors from being diluted by early good turns.
- **3 independent sampling runs** per scenario (`run_id` in the schema).
- **Human calibration** to align automated metrics against human preferences.
- The deep-dive describes a "rigorous scoring stack: text chunking, consistency checks across multiple samples, and manual calibration."
- Evaluation records carry **95% confidence intervals** per score field — the benchmark treats each score as an estimate with uncertainty, not a point value. Directly relevant to our regression-detection requirement.

**Not disclosed publicly:** exact numeric rubric / point scales per dimension, the precise weight arithmetic within pillars, the judge model identity and prompt, pass/fail thresholds, and the human-calibration correlation numbers. **No inter-annotator agreement or judge-human correlation coefficient is published.** This is the benchmark's biggest transparency gap and we cannot reproduce its calibration from public materials.

---

## Dataset composition

- **95 seeds total**, bilingual:
  - **English (en):** 45 seeds, 1,485 dialogues, standardized user fields
  - **Chinese (zh):** 50 seeds, 1,650 dialogues, scenario-dependent variations
- Dialogues are **synthetically constructed** via self-play simulation.
- 3,135 dialogues total across 11 models.

### Schema

**Seeds:** `id`, `ai_name`, `ai_setting`, `user_name`, `user_setting`, `ai_prologue`, `initial_user_input`

**Dialogues:** `seed_id`, `model_name`, `run_id`, `dialogue` (list of turn objects), `num_turns`

**Evaluations:** `seed_id`, `model_name`, `run_id`, plus six score fields each with 95% confidence intervals

The seed schema is worth copying near-verbatim for our variant harness: it separates `ai_setting` (character description) from `user_setting` (who the user is playing), and pins `ai_prologue` + `initial_user_input` so every model starts from a byte-identical state. **That pinning is what makes the cross-model comparison valid** — it is the "same baseline" property our platform requires.

---

## Leaderboard (11 models)

| Rank | Model | Score |
|---|---|---|
| 1 | MiniMax-M2-her | 84.65 |
| 2 | Doubao-1.5-pro | 80.64 |
| 3 | GPT-5.1 | 80.63 |
| 4 | Claude-opus-4.5-highthinking | 76.62 |
| 5 | Gemini-3-pro | 75.60 |
| 6 | Claude-opus-4.5-lowthinking | 71.19 |
| 7 | Claude-sonnet-4.5 | 69.35 |
| 8 | Gemini-2.5-pro | 68.23 |
| 9 | Deepseek-v3.1 | 64.22 |
| 10 | Deepseek-v3.2 | 60.27 |
| 11 | Grok-4.1 | 48.47 |

**Read this table with suspicion.** The benchmark's author's own model ranks #1 by a 4-point margin. There is no published judge-human correlation to rule out self-preference (see `rp-bench-judge-bias.md` — LLM judges systematically reward low-perplexity, i.e. familiar, text). The opus-4.5-high vs opus-4.5-low gap (76.62 vs 71.19) is the most useful signal in the table for us: it shows the metric is sensitive to a *known* capability delta within a fixed model family, which is exactly the sensitivity a regression detector needs. The absolute cross-family ordering is much weaker evidence.

## License

CC BY 4.0 / CC BY-SA 4.0 — permissive enough to reuse the seeds and rubric structure directly.
