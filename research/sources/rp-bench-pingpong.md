---
title: "PingPong: A Benchmark for Role-Playing Language Models with User Emulation and Multi-Model Evaluation"
url: https://arxiv.org/abs/2409.06820
authors: Ilya Gusev
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# PingPong (arXiv 2409.06820)

Submitted 10 Sep 2024. Single author (Ilya Gusev). Live leaderboard: https://ilyagusev.github.io/ping_pong_bench/ · Code: https://github.com/IlyaGusev/ping_pong_bench

**The closest of the five to a production companion-eval harness.** It is the only source that (a) simulates the *user* rather than replaying fixed prompts, (b) validates its judges against multiple human annotators with a published agreement statistic, (c) reports confidence intervals, and (d) grounds its test situations in *real* companion-app usage data (the Chai dataset). It costs **<$3 per model** to run.

## Abstract (VERBATIM)

> We introduce a benchmark for evaluating the role-playing capabilities of language models. Our approach leverages different language models to simulate users in dynamic, multi-turn conversations and assess the resulting dialogues. Our methodology involves three main components: a player model that adopts a specific character role, an interrogator model that simulates user behavior in a specific situation, and a judge model ensemble that evaluates conversation quality with 3 metrics: character consistency, entertainment value, and language fluency. We evaluated more than 40 models in both English and Russian, with each model participating in 64 conversations with 8 characters and 8 situations. We conducted experiments comparing automated evaluations with human annotations to validate our approach, demonstrating strong correlations across multiple criteria. This work provides a foundation for a robust and dynamic evaluation of different model capabilities in interactive scenarios.

## Architecture: player / interrogator / judge

Three separated roles:
- **Player** — the model under test; adopts a character card.
- **Interrogator** — simulates the user in a given situation. **Deliberately does not receive the full character profile:** *"In many real-world use cases, users lack complete information about character profiles, and to correctly simulate it, we should not provide complete character information to the interrogator."*
- **Judge ensemble** — scores every turn.

## The three criteria (VERBATIM)

> The scoring is single-point, with no reference examples or pairs. The judge used three main evaluation criteria:
>
> • **Character consistency**: The player's answers align perfectly with the assigned character; they correspond to the character's description.
>
> • **Entertainment value**: The player's responses are engaging and entertaining.
>
> • **Language fluency**: The language used by the player is of the highest quality and is free of errors. The player is perfectly fluent.
>
> These criteria reflect the main things we expect from the model during role-playing. We also ask whether the player refused to answer.

Note these are phrased as the **top-of-scale anchor** ("perfectly", "highest quality"), not neutral dimension names. A **refusal** flag is tracked separately and reported as "the proportion of conversations with refusals" — valuable for companion products where over-refusal is a primary failure mode.

Judge protocol: *"We prompt a model to explain itself before giving a score, using quotes from the conversation. It must also return a set of scores for every turn of the conversation."* (Reason-then-score, quote-grounded, per-turn.)

## Version 1 → Version 2 (the design lesson)

**Version 1** merged interrogator and judge into one Claude 3.5 Sonnet call, 10-point scale. Selected via Judgemark results, *"hypothesizing a correlation between creative writing and role-playing capabilities."* Three stated failures:

> • **Unrealistic user simulation**: In many real-world use cases, users lack complete information about character profiles, and to correctly simulate it, we should not provide complete character information to the interrogator.
> • **High costs**: The choice of the interrogator influences the final scores less than the choice of the judge (see Appendix D), so it does not make sense to use the same expensive model for both.
> • **Non-optimal decoding strategies**: Some decoding strategies are suitable for judgment but not for interrogation. For example, a higher temperature benefits the interrogator but not the judge.

**Version 2** separates roles and adds **multi-model judging**:
- Judges: **Claude 3.5 Sonnet + GPT-4o**, *"the top two models, by correlation with manual annotations"* — scores **averaged**. *"We tried several more sophisticated approaches, but the average worked best."*
- Interrogator: **GPT-4o Mini** (*"it has the same generation quality as GPT-4o but is cheaper"*).
- **5-point Likert scale**, down from 10-point, justified explicitly:

> The Likert scale (Likert, 1932) has its roots in sociology, and 5-7 scale points typically maximize both reliability and validity while minimizing the cognitive load on human raters (Cox III, 1980), so we decided to use it instead of the 10-point scale. We also used the same scale for human annotations.

**Judge choice dominates interrogator choice** (Appendix D, Kendall τ over 6 judges × 6 interrogators):

> The average Kendall τ for a group with different interrogators is 0.58, and the minimum Kendall τ is 0.43. The average Kendall τ for a group with different [judges] is 0.5, and the minimum Kendall τ is 0.14.
> From this we conclude that a choice of an judges influences the final scores more than a choice of an interrogator.

*(sic: the paper's text says "different interrogators" twice; the second is clearly judges, per the stated conclusion and Tables 8/9.)* Practical implication: **spend budget on the judge, economize on the user-simulator.**

## Judge–human correlation (Spearman) — VERBATIM TABLES

Rank correlation chosen *"because the scales differed in versions 1 and 2."*

**Table 1 — English, 250 samples.** *"P-values are less than 0.0001, except those marked with an asterisk."*

| Model | In-character v1 | v2 | Entertaining v1 | v2 | Fluency v1 | v2 | Final v1 | v2 |
|---|---|---|---|---|---|---|---|---|
| Claude 3.5 Sonnet | 0.433 | 0.448 | 0.582 | 0.616 | 0.182* | 0.115* | 0.499 | 0.554 |
| Llama 3.1 70B | – | 0.403 | – | 0.573 | – | 0.116* | – | 0.546 |
| GPT-4o | – | 0.396 | – | 0.541 | – | 0.283 | – | 0.517 |
| GPT-4o Mini | – | 0.348 | – | 0.514 | – | 0.019* | – | 0.467 |
| Claude 3 Haiku | – | 0.251 | – | 0.406 | – | -0.069* | – | 0.349 |
| **Avg(Sonnet, 4o)** | – | **0.460** | – | **0.646** | – | **0.250** | – | **0.604** |

**Table 2 — Russian, 265 samples.**

| Model | In-character v1 | v2 | Entertaining v1 | v2 | Fluency v1 | v2 | Final v1 | v2 |
|---|---|---|---|---|---|---|---|---|
| Claude 3.5 Sonnet | 0.291 | 0.374 | 0.497 | 0.553 | 0.210* | 0.548 | 0.379 | 0.547 |
| GPT-4o | – | 0.424 | – | 0.553 | – | 0.413 | – | 0.550 |
| GPT-4o Mini | – | 0.166* | – | 0.393 | – | 0.225* | – | 0.344 |
| Claude 3 Haiku | – | 0.141* | – | 0.265 | – | 0.021* | – | 0.157 |
| Llama 3.1 70B | – | 0.319 | – | 0.367 | – | 0.031* | – | 0.253 |
| **Avg(Sonnet, 4o)** | – | **0.435** | – | **0.617** | – | **0.529** | – | **0.612** |

**Key reads:**
- The **2-judge average beats every single judge** on every metric — the ensemble is doing real work.
- **English Fluency correlation collapses (0.250, and 0.115 / 0.019 / −0.069 not significant).** The paper explains: models rarely make English errors, so the metric carries almost no signal. Russian Fluency is healthy (0.529) because errors actually occur.
- **Entertainment correlates best** (0.646 / 0.617) — the most subjective-sounding criterion is the most reliably judged.
- Judge quality tracks model quality: Claude 3 Haiku is a poor judge (Final 0.349 / 0.157).

## Inter-annotator agreement (VERBATIM)

Reported in Appendix A — **five annotators, not one.**

> Table 6: Pair-wise Spearman correlation of final scores, Russian samples, **Krippendorff's α is 0.34**.
>
> Table 7: Pair-wise Spearman correlation of final scores, English samples, **Krippendorff's α is 0.25**.

Pairwise annotator Spearman (final scores):

| | Russian (Table 6) | English (Table 7) |
|---|---|---|
| Pairwise range | 0.329 – 0.555 | 0.216 – 0.546 |
| Aggregated-vs-annotator | 0.701 – 0.784 | 0.607 – 0.779 |

> Russian annotations showed higher Krippendorff's α value and more consistent pairwise correlations than English. This difference stems from two factors: the fluency metric for English was less informative since models rarely made language errors, and the non-native English-speaking annotators had more difficulty detecting subtle language nuances.

**⚠️ Critical context: α = 0.25 (English) and α = 0.34 (Russian) are LOW.** Conventional thresholds treat α < 0.667 as insufficient for even tentative conclusions. This reframes the whole benchmark: the judge–human Spearman of ~0.60 is measured against a human ground truth whose own raters agree only weakly. **The judges arguably agree with the aggregated human panel about as well as the humans agree with each other** — which is a defensible ceiling claim, not a failure, but it means ~0.6 is near the practical maximum, not a shortfall to be engineered away. Any companion-eval platform should expect the same: subjective role-play quality has low human ceiling agreement, so ensemble-aggregate targets, not individual-rater targets.

**Annotator panel:** five native Russian speakers proficient in English, diverse backgrounds (a manager, an ML engineer, a bioinformatician, a computational linguist), *"young professionals in their 20s (with one participant in their late teens)."* Notably: *"Each annotator had prior experience interacting with role-playing language models, making them representative users of such systems."* Paid **$15/hour**, ~4 hours per language. Platform: **LabelStudio**; guidelines and UI configs released.

*(Note: some secondary summaries of this paper claim "a single human annotator" — that is wrong for the current arXiv version, which uses five. Earlier drafts differed.)*

## Setup / scale

- **8 characters × 8 situations = 64 conversations per model**
- Judge scores **every turn** → **288 total annotations** per model (not 64)
- Human-validation samples: **250 English / 265 Russian**, from 64 conversations each across **13+ models**
- **>40 models** on the leaderboards
- **<$3 per model** to evaluate
- Reported per model: mean score per metric, **proportion of conversations with refusals**, overall average, and **bootstrapped confidence intervals**
- Character sources: *"computer games, TV shows, movies, books, and anime"*
- Situations: *"Situations fall into two categories: common user patterns and attempts to break model behavior."*

### Length penalty

> Both language models and humans exhibit verbosity bias (Dubois et al., 2024). The longer the output, the higher the chance of being positively evaluated. To account for this, we used a length penalty similar to the Creative Writing benchmark. We calculated length-normalized scores for all models, penalizing models with a median length of player messages greater than a global median length.

(Same problem CoSER solves with its λ|M̄| correction — independent convergence on verbosity bias as a core LLM-judge threat.)

### Situations grounded in real companion-app data

Situations were derived from the **Chai dataset** (`ChaiML/20231206_chai_prize_rew`) — real user interactions with role-playing models in a mobile app — via **BERTopic**, then turned into interrogator prompts with GPT-4o. Published topic distribution:

| # | Topic | Fraction |
|---|---|---|
| 1 | Friendly Interactions | 11.1% |
| 2 | Casual Greetings | 10.6% |
| 3 | Interpersonal Interaction | 8.9% |
| 4 | Casual Fun and Games | 8.4% |
| 5 | **Affection and Comfort** | 8.0% |
| 6 | **Relationships** | 7.7% |
| 7 | Introductions | 7.3% |
| 8 | Sleeping Situations | 6.7% |
| 9 | School Life | 6.0% |
| 10 | Food and Drink | 6.0% |

**This table is the single most directly useful artifact across all five sources for a companion platform** — it is an empirical prior on what users actually do with companion characters. Note that affection/comfort + relationships ≈ 15.7% of real traffic, and that greetings/small talk dominate. Appendix C estimates the fraction of real user situations covered by the benchmark's 8 situations.

## Multilingual & multi-turn

- **Multi-turn: YES — and dynamically generated, not scripted.** This is PingPong's defining contribution: the interrogator *improvises* the user side, so conversations are not fixed transcripts. Scores are per-turn with "varying conversation lengths."
- **Multilingual: English + Russian only. NO Chinese.** The bilingual design is nonetheless the most methodologically informative of the five, because the En/Ru contrast *demonstrates* that metric validity is language-dependent (Fluency is informative in Russian, dead in English). **Direct lesson for a Chinese-language platform: do not assume a dimension that works in English carries over — re-validate agreement per language.** The harness itself is language-agnostic and adding Chinese is straightforward.

## Limitations (VERBATIM)

> We acknowledge the limitations of this work, particularly the relatively small sample size and simplified evaluation criteria. First, the sample size of 64 conversations per model, while computationally efficient, may limit the statistical robustness of our findings. Second, the simplicity of our evaluation criteria may not fully capture the nuanced aspects of role-playing abilities.

The author is explicit that the sample size is a budget decision: *"We do not want to make this sample bigger since it will increase the runtime and costs, and we have budget constraints."*

## Ethics statement (VERBATIM, partial)

> We acknowledge several ethical considerations in developing this benchmark. Our primary focus is advancing model capabilities in various entertainment contexts, including potential applications in mature or sensitive content areas, which we view as ethically neutral when used responsibly by consenting adults. However, all characters and situations used in the benchmark are designed to be appropriate for general audiences to minimize rejections from judge models, which often have strict content filters. We have strived for diversity in our character design and situation design to mitigate bias, though we recognize the inherent limitations in achieving full representation. Using language models to evaluate language models' performance presents potential concerns regarding echo chambers or bias amplification, which we have addressed through multi-model evaluation.

Directly relevant: the author concedes the benchmark **deliberately avoids mature content specifically because judge models refuse to score it** — a real, unsolved obstacle for any companion platform whose actual traffic includes such content. The judge-filter problem means the benchmark cannot measure the segment that may matter most commercially.

## Criticisms / notes for platform design

- **Low human agreement (α = 0.25 / 0.34)** undercuts the "strong correlations" claim in the abstract; ~0.6 Spearman looks strong only relative to a noisy ceiling. The abstract oversells this.
- **English Fluency is a dead metric** (r ≈ 0.1–0.25, mostly insignificant) yet still contributes to the Final average — a known weak component left in the aggregate.
- **64 conversations / 288 turn annotations** per model is small; CIs are reported, which is honest, but fine-grained leaderboard ranks between adjacent models are not meaningful.
- **Judge-refusal ceiling:** content the judges won't score can't be benchmarked.
- **Single-author, no peer review listed** on the arXiv version.
- **Adopt-worthy, in priority order:** (1) the user-simulator/interrogator pattern with *withheld* character profile; (2) **multi-judge averaging** — cheap, and beat every single judge; (3) the **Chai topic distribution** as a situation sampler; (4) per-turn scoring + refusal rate + bootstrapped CIs; (5) 5-point Likert matched between judge and human scales; (6) length normalization; (7) **validating judges per-language before trusting any dimension.**
