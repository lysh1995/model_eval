---
title: "RoleEval: A Bilingual Role Evaluation Benchmark for Large Language Models"
url: https://arxiv.org/abs/2312.16132
authors: Tianhao Shen, Sun Li, Quan Tu, Deyi Xiong
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# RoleEval

- **arXiv:** 2312.16132 — [v1] 26 Dec 2023; [v2] 16 Feb 2024
- **Venue:** arXiv preprint (no conference acceptance noted in the comments field)
- **Code/data:** <https://github.com/Magnetic2014/RoleEval>
- **Note:** Quan Tu is also an author of CharacterEval — the two Chinese roleplay benchmarks share a contributor but take opposite methodological approaches (knowledge MCQ vs. generative reward model).

## Abstract (VERBATIM)

> The rapid evolution of large language models necessitates effective benchmarks for evaluating their role knowledge, which is essential for establishing connections with the real world and providing more immersive interactions. This paper introduces RoleEval, a bilingual benchmark designed to assess the memorization, utilization, and reasoning capabilities of role knowledge. RoleEval comprises RoleEval-Global (including internationally recognized characters) and RoleEval-Chinese (including characters popular in China), with 6,000 Chinese-English parallel multiple-choice questions focusing on 300 influential people and fictional characters drawn from a variety of domains including celebrities, anime, comics, movies, TV series, games, and fictions. These questions cover basic knowledge and multi-hop reasoning abilities, aiming to systematically probe various aspects such as personal information, relationships, abilities, and experiences of the characters. To maintain high standards, we perform a hybrid quality check process combining both automatic and human verification, ensuring that the questions are diverse, challenging, and discriminative. Our extensive evaluations with RoleEval across various open-source and proprietary large language models, under both the zero- and few-shot settings, reveal insightful findings. Notably, while GPT-4 outperforms other models on RoleEval-Global, Chinese large language models excel on RoleEval-Chinese, highlighting significant knowledge distribution differences. We expect that RoleEval would highlight the significance of assessing role knowledge for large language models across various languages and cultural settings.

## What RoleEval actually measures — read this first

**RoleEval is NOT a roleplay-quality benchmark.** It does not evaluate whether a model *plays* a character well. It evaluates whether a model **knows facts about** characters, via multiple-choice questions answered *out of character*.

This makes it categorically different from the other three benchmarks:

| | RoleBench | CharacterEval | CharacterBench | **RoleEval** |
|---|---|---|---|---|
| Measures | style imitation | roleplay quality | character customization | **role *knowledge*** |
| Output | generated text | generated text | generated text | **A/B/C/D** |
| In character? | yes | yes | yes | **no** |

It's best understood as the **prerequisite-knowledge probe**: a model can't stay in character about Sherlock Holmes if it doesn't know who Mycroft is. RoleEval isolates that substrate.

## Dimensions / knowledge categories probed (VERBATIM)

RoleEval probes **three fundamental knowledge types**:

| Knowledge type | Verbatim definition |
|---|---|
| **Inherent Attributes** | "fundamental characteristics intrinsic to the character, such as gender, race, personality, skills, and abilities" |
| **Social Relationships** | "relationships of the character with other individuals, which could include parents, disciples, and other significant personal or professional relationships" |
| **Experiences** | "experiences or events that the character has undergone" |

### Capability axes (from the abstract)

Three capabilities, in increasing difficulty: **memorization**, **utilization**, and **reasoning** of role knowledge.

### Basic knowledge vs. multi-hop reasoning split (VERBATIM)

Per character, **20 questions**:

> "17 questions about basic knowledge and 3 questions that inspect multi-hop reasoning"

**85% basic / 15% multi-hop.** (300 characters × 20 questions = 6,000 questions. ✅ arithmetic checks out.)

### The three multi-hop reasoning types

- **Character Relationship Reasoning**
- **Event Participant Reasoning**
- **Timeline Reasoning**

## How it scores

- **Format:** **multiple-choice questions**, "with four options for each question" (A/B/C/D)
- **Metric:** **accuracy** — percentage of correct answers selected
- **No LLM judge, no human scoring, no reward model, no rubric.** Fully objective and deterministic. This is RoleEval's main practical advantage: zero judge cost, zero judge bias, perfectly reproducible.
- **Extraction method differs by model type:**
  - Open-source models: "probability of subsequent tokens following the initial prompt" (compare logprobs over A/B/C/D)
  - GPT models: "regular expressions to extract the preferred choice"
  - *This asymmetry is a subtle confound — logprob-based scoring and regex-extraction-from-generation are not strictly comparable, and regex extraction penalizes models that hedge or refuse to commit to a letter.*
- **Settings:** **zero-shot** and **five-shot**

## Quality check process

**Hybrid: "automatic and human verification"**

**Automatic filtering criteria (exact thresholds):**

| Parameter | Value | Meaning |
|---|---|---|
| `x_l` | **0.3** | lower accuracy threshold (GPT-4 performance) |
| `x_u` | **0.9** | upper accuracy threshold (GPT-4 performance) |
| `y_u` | **0.8** | GPT-3.5 performance upper bound |
| `d` | **0.15** | discrimination threshold |

I.e. questions are kept only if GPT-4 scores between 0.3 and 0.9 (not trivial, not impossible), GPT-3.5 scores below 0.8, and the GPT-4/GPT-3.5 gap exceeds 0.15 (discriminative).

**⚠️ Methodological criticism:** this filtering **defines question difficulty relative to GPT-4 and GPT-3.5**. The benchmark is constructed to be discriminative *for the OpenAI model family circa late 2023*. This bakes in a subtle circularity — questions GPT-4 happens to know are filtered out as "too easy," which mechanically deflates GPT-4's ceiling while questions GPT-4 uniquely fails are also removed. Cross-family comparisons (e.g., Qwen vs GPT-4) inherit this construction bias.

**Human verification:** annotators "manually check the questions and options to ensure quality" and provide "links to referenced text in online encyclopedias" as evidentiary grounding.

## Inter-annotator agreement

**Not reported.** No agreement statistics (kappa, alpha, percent agreement) are given for the human verification stage. Less damaging here than for the generative benchmarks — MCQ answers with encyclopedia citations are far more objective than 5-point Likert judgments of "empathy" — but still unquantified.

Also **no judge-human correlation applies**, since there is no judge.

## Dataset statistics

| Statistic | Value |
|---|---|
| **Total questions** | **6,000** Chinese-English **parallel** |
| **Characters** | **300** |
| **Questions per character** | **20** (17 basic + 3 multi-hop) |
| **RoleEval-Global** | **4,000** questions / **200** characters |
| **RoleEval-Chinese** | **2,000** questions / **100** characters |
| **Options per question** | **4** |

### Domain breakdown (5 domains, equal distribution)

| Domain | Global | Chinese |
|---|---|---|
| Celebrities | 40 | 20 |
| Anime and comics | 40 | 20 |
| Movies and TV series | 40 | 20 |
| Games | 40 | 20 |
| Fiction | 40 | 20 |
| **Total** | **200** | **100** |

## Models evaluated — key results

Extensive evaluation across open-source and proprietary LLMs, zero-shot and five-shot. Top performers (5-shot accuracy):

| Model | RoleEval-Global | RoleEval-Chinese |
|---|---|---|
| **GPT-4-1106** | **76.00%** | 62.75% |
| GPT-4-0613 | 72.32% | 58.75% |
| **Qwen-72B** | 67.47% | **66.20%** |
| Yi-34B | 65.83% | 64.60% |

**Headline finding:** "while GPT-4 outperforms other models on RoleEval-Global, Chinese large language models excel on RoleEval-Chinese, highlighting significant knowledge distribution differences."

Note the pattern: GPT-4-1106 leads Global by ~8.5 points over Qwen-72B, but **loses** Chinese by 3.45 points. Qwen-72B is remarkably balanced (67.47 / 66.20, a 1.27-point gap) while GPT-4-1106 drops 13.25 points crossing into Chinese characters. This mirrors CharacterEval's finding that Chinese models beat GPT-4 on Chinese roleplay — and RoleEval supplies a *mechanism*: it's a **knowledge distribution** gap, not just a style/tuning gap.

**Absolute ceiling is low:** the best score anywhere is 76%, and on Chinese nothing clears 67%. Role knowledge is genuinely unsolved — models hallucinate character facts routinely.

## Multilingual coverage and multi-turn support

- **Bilingual — and the cleanest bilingual design of the four.** 6,000 **Chinese-English parallel** questions: every question exists in both languages, enabling true controlled cross-lingual comparison (same content, different language).
- **Two culture-specific splits:** RoleEval-Global (internationally recognized characters) vs. RoleEval-Chinese (characters popular in China). This *cultural* split — not just linguistic — is the design feature that surfaces the knowledge-distribution finding. CharacterBench, by contrast, translates Chinese-native data into English and so cannot make this comparison.
- **Multi-turn: NO.** Single-turn multiple-choice questions. No dialogue, no context accumulation, no persona maintenance.

## Stated limitations (VERBATIM)

> "Firstly, the aspect of timeliness is crucial; the knowledge regarding real-world characters may change over time, making the benchmark outdated or irrelevant."

> "Secondly, the current format of benchmarks often restricts questions to having only one correct answer. This approach fails to adequately test scenarios where multiple answers could be correct, thus limiting the benchmark's ability to evaluate complex decision-making skills."

## Known criticisms / gaps

1. **Does not measure roleplay at all** — only knowledge *about* roles, answered out of character. A model can ace RoleEval and be a terrible companion; the converse is also possible. Never present RoleEval scores as roleplay quality.
2. **MCQ ≠ generation.** Four-option recognition is far easier than free-form recall, and logprob-ranked selection doesn't test whether the model would *volunteer* correct facts in dialogue.
3. **Construction is GPT-4/GPT-3.5-relative** (thresholds x_l=0.3, x_u=0.9, y_u=0.8, d=0.15) — difficulty is calibrated to one model family, creating cross-family comparison bias.
4. **Scoring asymmetry** — logprobs for open models vs. regex extraction for GPT models are not strictly comparable protocols.
5. **Timeliness decay** (author-acknowledged) — real-world celebrity facts rot; a 2023 benchmark evaluated in 2026 has stale ground truth for the "celebrities" domain (60 of 300 characters).
6. **Single-correct-answer format** (author-acknowledged) — can't handle genuine ambiguity or multi-valid-answer scenarios.
7. **No inter-annotator agreement reported.**
8. **Contamination risk** — characters are drawn from encyclopedias; questions built from Baike/Wikipedia-type sources are plausibly in pretraining data. The x_u=0.9 filter partially mitigates by removing questions GPT-4 aces, but doesn't address contamination in other model families.
9. **Not peer-reviewed** — arXiv preprint only, unlike the other three (ACL Findings / ACL main / AAAI).

## Relevance to a companion-eval platform

- **Use it as a cheap, deterministic knowledge substrate check**, not as a roleplay metric. Zero judge cost, fully reproducible, no annotation needed — it's the one benchmark of the four you can run continuously in CI without a judge budget.
- **The parallel ZH/EN design is the best template of the four** for measuring cultural/knowledge coverage gaps in a bilingual product. If we want to answer "does our model know Chinese-canon characters as well as Western ones?", RoleEval's Global-vs-Chinese split is the right instrument.
- **The knowledge-distribution finding is strategically important:** GPT-4-1106 drops 13.25 points crossing into Chinese characters while Qwen-72B stays flat. For a bilingual companion product, base-model choice is partly a *character-knowledge coverage* decision, not just a capability decision.
- **Do not** use it for persona fidelity, safety, empathy, engagement, or multi-turn stability — it measures none of these.
- **Refresh caution:** the celebrities domain (60/300 characters) has stale-ground-truth risk as of 2026.

## Citation

```bibtex
@article{shen2023roleeval,
  title   = {RoleEval: A Bilingual Role Evaluation Benchmark for Large Language Models},
  author  = {Shen, Tianhao and Li, Sun and Tu, Quan and Xiong, Deyi},
  year    = {2023},
  journal = {arXiv preprint arXiv:2312.16132}
}
```
