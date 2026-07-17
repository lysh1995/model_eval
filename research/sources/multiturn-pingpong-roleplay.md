---
title: "PingPong: A Benchmark for Role-Playing Language Models with User Emulation and Multi-Model Evaluation"
url: https://arxiv.org/abs/2409.06820
authors: Ilya Gusev
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# PingPong: A Benchmark for Role-Playing Language Models with User Emulation

arXiv:2409.06820 (v3). Code: https://github.com/IlyaGusev/ping_pong_bench

**Status: the closest existing analogue to our platform — roleplay + multi-turn + user emulation + multilingual + judge ensemble. Its limitations define our opportunity.**

## Abstract

"We introduce a benchmark for evaluating the role-playing capabilities of language models" using different models to simulate users in multi-turn conversations and assess dialogue quality through three metrics. **40+ models** evaluated in **English and Russian**, **64 conversations per model**.

## Methodology — three roles

**Player Model:** assumes a character role from a character card. temperature=0.6, top_p=0.9.

**Interrogator Model:** simulates user behavior in given situations. GPT-4o Mini in v2 (temperature=0.8, top_p=0.95). **Receives only situation information, NOT character details** — to simulate realistic asymmetric interaction.

That asymmetry is a deliberate and important design choice. If the user-simulator knows the character card, it *cooperates* with the persona and drift never surfaces. Withholding it is what makes the test adversarial. **Our replayed user turns need auditing on exactly this axis: were they generated with character-card visibility?** If yes, our user turns are collaborative and will under-detect drift — a bigger threat to validity than off-policyness.

**Judge Ensemble:** averages **Claude 3.5 Sonnet and GPT-4o**, 5-point Likert, temperature=0.1, top_p=0.95. **Per-turn scoring.**

## Three metrics (5-point Likert)

- **Character Consistency:** "answers align perfectly with the assigned character"
- **Entertainment Value:** "responses are engaging and entertaining"
- **Language Fluency:** "language used by the player is of the highest quality"

## Scale

- 40+ proprietary and open-source models
- **8 characters × 8 situations = 64 conversations per model**
- Languages: English, Russian
- 288 annotations per model

**Our dataset is ~2 orders of magnitude larger: 95 characters (vs 8), ~100 turns (vs short), 3 runs (vs 1), 11 models.** PingPong has no repeated runs at all — so it structurally *cannot* compute Laban-style unreliability, which is the dominant term in multi-turn failure.

## Correlation with human annotations (Spearman)

**English (250 samples):**
| Metric | ρ |
|---|---|
| Final score, multi-model ensemble | **0.604** |
| Claude 3.5 Sonnet alone | 0.499 |
| Character consistency (ensemble) | **0.460** |
| Entertainment | 0.646 |
| Fluency | 0.250 |

**Russian (265 samples):**
| Metric | ρ |
|---|---|
| Final score, ensemble | **0.612** |
| Claude 3.5 Sonnet alone | 0.547 |
| Character consistency | 0.435 |
| Entertainment | 0.617 |
| Fluency | 0.529 |

## Inter-annotator agreement — LOW

- Russian: **Krippendorff's α = 0.34**
- English: **Krippendorff's α = 0.25**

**These two numbers should govern our expectations.** α=0.25 is very low agreement — humans barely agree on roleplay quality at the turn level. And note character consistency has the *weakest* judge-human correlation (0.435–0.460) of the substantive metrics. **The thing we most want to measure is the thing per-turn LLM judging measures worst.** This is independent support for moving character consistency off the per-turn-judge substrate and onto deterministic probes (per Persona Drift) or geometric cohort metrics (per Chameleon's Limit).

## Ensemble vs single judge

"Multi-model setup has a higher correlation with humans" (>0.6 vs individual models at 0.3–0.6) — validates ensembles and partially addresses **self-preference bias**.

## v1 → v2 lessons (documented failure of their own first design)

Authors identified problems with the combined interrogator-judge design:
- **unrealistic user simulation** (interrogator received full character info)
- high costs
- mismatched decoding strategies

v2 **separated the interrogator and judge roles**, reducing bias from one model doing both.

**Free lesson: never let the same model drive the user turns and judge the result.** Our replay design gets this for free — our user turns are fixed data, so they cannot collude with the judge. This is an under-appreciated *advantage* of replay over live simulation.

## Relevance to companion-eval-platform

- Confirms the shape of the problem and that a market/precedent exists; also confirms nobody has done it at conversation depth with repeated runs.
- **Their unit of analysis is the turn** (per-turn judge scores, averaged). This is exactly the design our project argues against — and their own α=0.25 and ρ=0.46 on character consistency are evidence the per-turn substrate is noisy.
- **Adopt:** judge ensembling (measurable gain: 0.499 → 0.604), interrogator/judge separation, character-card asymmetry for the user side.
- **Improve on:** repeated runs (they have none), conversation-level aggregation (they average), 95 vs 8 characters (enables cohort metrics they cannot compute), and turn depth.
- The en/ru → en/zh parallel is useful: they found fluency correlation differs a lot by language (0.250 en vs 0.529 ru). **Expect our judge to behave differently in zh than en, and validate per-language rather than pooling.**
