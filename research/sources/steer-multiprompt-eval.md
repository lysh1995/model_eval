---
title: "State of What Art? A Call for Multi-Prompt LLM Evaluation"
url: https://arxiv.org/abs/2401.00595
authors: Moran Mizrahi, Guy Kaplan, Dan Malkin, Rotem Dror, Dafna Shahaf, Gabriel Stanovsky (Hebrew University of Jerusalem / University of Haifa)
year: 2024 (TACL 2024; ACL Anthology 2024.tacl-1.52)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Mizrahi et al. — paraphrase brittleness, and the single best number in this whole literature

**Why this paper matters more than FormatSpread for our purposes: FormatSpread perturbs separators and
casing. This paper perturbs INSTRUCTION WORDING — paraphrases and synonym swaps. That is one step closer to
what the platform actually does (swapping intensity words). And it contains the number that breaks the
"scale fixes it" hypothesis in the most vivid way available anywhere in the literature.**

## Abstract (verbatim, complete)

> "Recent advances in large language models (LLMs) have led to the development of various evaluation
> benchmarks. These benchmarks typically rely on a single instruction template for evaluating all LLMs on a
> specific task. In this paper, we comprehensively analyze the brittleness of results obtained via
> single-prompt evaluations across 6.5M instances, involving 20 different LLMs and 39 tasks from 3
> benchmarks. To improve robustness of the analysis, we propose to evaluate LLMs with a set of diverse
> prompts instead. We discuss tailored evaluation metrics for specific use cases (e.g., LLM developers vs.
> developers interested in a specific downstream task), ensuring a more reliable and meaningful assessment of
> LLM capabilities. We then implement these criteria and conduct evaluations of multiple models, providing
> insights into the true strengths and limitations of current LLMs."

## Method — how the paraphrases were built

**Scale:** 6.5M instances × 20 LLMs × 39 tasks × 3 benchmarks.

**Benchmarks/tasks (39 total):**
- **LMentry** — 10 tasks (Efrat et al. 2023)
- **BIG-Bench Lite (BBL)** — 14 tasks
- **BIG-Bench Hard (BBH)** — 15 tasks

**Paraphrase generation:** "more than 175 paraphrases for different tasks (**5K instruction paraphrases in
total**)", averaging "more than **200 automatically-generated instruction template paraphrases** for each of
our tasks." Three generation methods:
1. instruction template rephrasing
2. Chain-of-Thought prompting
3. gradual template generation

Generated with **GPT-3.5-Turbo**, seeded from the original instruction templates.

**Validation (this matters — the paraphrases are verified meaning-preserving, not assumed):**
> "All automatically generated paraphrases were manually verified and filtered by an annotator"

- **90%** of generated paraphrases for LMentry were correct; **~84%** for BBH.
- Inter-annotator agreement on 375 instructions: "more than **85%** were found to be correct by both
  annotators."

Models span **80M to 15B** parameters.

## THE NUMBERS

### The headline finding — absolute performance

**THE killer number (verbatim):**
> "the **Flan-T5-large** model demonstrated an average performance **degradation of 28%** when changing the
> word **'excludes' to 'lacks'**, while the **Flan-T5-XL** model showed an average performance **improvement
> of 46%** on that **same edit**"

**Read that carefully. One synonym swap. Two sizes of the same model family. Opposite directions. A 74-point
swing between them on an identical edit.** This single result does three things at once:
1. It kills "scale fixes brittleness" — the larger model isn't more stable, it's differently unstable.
2. It kills cross-model transfer of prompt choices *within a single family* — the best edit for one size is
   the worst edit for the next size up.
3. It is a **near-synonym lexical swap**, i.e. the perturbation type closest to the platform's intensity-word
   manipulation of anything in this literature. See the Relevance section — this is the strongest available
   evidence about the platform's actual construct.

### Original templates are unrepresentatively good (selection bias in benchmarks)

> "In **72.5%** of the cases, the performance of the original instructions was higher than the estimated
> average across all paraphrases. In the davinci model, the original prompts added on average **21 more
> accuracy points**"

Benchmark-authored prompts are ~21 points better than a random valid paraphrase. **Any single-prompt number
in any paper is an optimistic outlier, not a central estimate.**

> "the performance of the Alpaca-13B with the original instruction templates outperformed its average
> performance by more than one standard deviation in **7 out of 10** LMentry tasks"

### Ranking instability — how much do model rankings change across paraphrases?

**Kendall's W (agreement of rankings across paraphrases):**
> "Most W values are smaller than **0.85**, indicating weak to moderate agreement"

> "**10 of the tasks** exhibiting only slight to moderate ranking agreement, and only **two** exhibiting
> strong agreement"

**Kendall's τ:**
> "**15 tasks out of 25** have instruction template paraphrases with **negative Kendall's τ**, indicating
> mostly disagreeing LLM rankings"

**Negative τ means the ranking is more than destroyed — it is *inverted*.** In 60% of tasks there exist two
valid paraphrases of the same instruction that produce anti-correlated model leaderboards.

**Friedman test:**
> "different instructions lead to statistically significant differences in performance for **21 out of the 25
> tasks**"

**Concrete rank flips (verbatim):**
- "**T0pp** ranks **first** on the BBH task (center) according to P₁ and only **9th** according to P₂"
- "**Alpaca-13B and Alpaca-7B** are in the **top-performing** models on the LMentry task P₂, while they rank
  **last** for P₁"

**Even restricting to OpenAI models:**
> "Agreement was observed in only **5 out of 10** tasks for the average metric, and in **4 out of 10** tasks
> for the maximum metric"

### Proposed metrics (the constructive contribution)

| Metric | Definition | Intended use case (verbatim) |
|---|---|---|
| **MaxP** | `MaxP(M,T,I_T) = max_{i∈I_T} ε(M,T,i)` | "developers aiming to integrate an LLM into a specific downstream task" |
| **AvgP** | `AvgP(M,T,I_T) = 1/\|I_T\| · Σ_{i∈I_T} ε(M,T,i)` | "assessing model robustness to paraphrases" for LLM developers |
| **Sat** | `Sat(M,T,I_T) = 1 − (MaxP − AvgP)` | saturation / robustness term |
| **CPS** | `CPS(M,T,I_T) = Sat · MaxP` | "selecting a model for a suite of applications or a platform" |

The CPS construction is the key idea: **peak capability discounted by its own spread**. A model that can hit
a high score only under one lucky phrasing is penalized.

> "LLaMA-based models were competitive with T5-based models in terms of MaxP. However, in terms of AvgP, they
> tended to lag behind, due to **extremely poor performance on a large number of paraphrases**"

### Does ranking instability shrink with model size?

**No explicit quantitative claim in the paper.** The models span 80M–15B but the paper does not correlate
instability with parameter count directly. **Do not cite this paper for a scale claim.** The Flan-T5-large vs
Flan-T5-XL result above is *suggestive* evidence against scale helping (opposite-signed response to an
identical edit at two sizes), but it is a single anecdote, not a scaling analysis. The load-bearing citation
for "sensitivity does not shrink with scale" remains Sclar et al.'s abstract (`steer-formatspread.md`).

## Relevance to companion-eval-platform

**This is the most transferable paper in the steerability set, and it cuts in a genuinely uncomfortable
direction for the design.**

1. **It moves the perturbation one step toward our construct — and the brittleness does not go away.** The
   worry with FormatSpread is that separators/casing are *so* semantically empty that the result might not
   say anything about wording. Mizrahi et al. perturb **actual instruction wording** — human-verified
   meaning-preserving paraphrases (90%/84% correct) — and still find negative Kendall's τ on 15/25 tasks.
   **Paraphrase brittleness ≈ format brittleness in magnitude.** So the platform cannot assume that "wording
   changes" are a cleaner channel than "formatting changes."

2. **The 'excludes' → 'lacks' result is the closest thing in the literature to our measurement, and it is a
   warning shot.** A single-word lexical swap between near-synonyms produced −28% on one model and +46% on
   its bigger sibling. The platform's core manipulation ("shy" → "very shy") is *also* a single-word lexical
   swap. The difference is that our swap is *intended* to move behavior. But this result shows the model's
   response to a one-word swap is (a) large, (b) model-specific, and (c) **not sign-stable across model
   sizes.** If a *meaning-preserving* one-word swap can produce ±46%, then a *meaning-changing* one-word swap
   producing a large effect is **not evidence that the model understood the intensity word.** The effect size
   alone cannot distinguish "the model responded to the semantics of 'very'" from "the model twitched because
   a token changed." **This is the central measurement-validity problem for the whole design, and this paper
   is the citation for it.**

3. **Negative Kendall's τ generalizes directly to trait rankings.** If the platform ever ranks models by
   steerability, or ranks traits by how steerable they are, this paper predicts the ranking will invert under
   a different-but-equivalent phrasing of the persona prompt on ~60% of tasks. **A steerability leaderboard
   built on one phrasing per trait is not measuring steerability.** The minimum viable design is N paraphrases
   per trait per intensity level, not one.

4. **The 72.5% / 21-point result predicts our own prompts will flatter us.** The prompts a designer writes
   are original templates, and original templates beat the paraphrase average 72.5% of the time (davinci:
   +21 points). Hand-authored persona prompts will make traits look **more steerable than they are**. The
   platform needs paraphrase sampling not just for error bars but to remove an *optimistic bias* in the point
   estimate.

5. **CPS is a directly stealable design.** `CPS = (1 − (MaxP − AvgP)) · MaxP` — capability discounted by
   spread — is exactly the shape the steerability score should have: **how far can wording move this trait
   (signal), discounted by how much the wording-that-shouldn't-matter also moves it (noise).** This is the
   published precedent for the "signal ÷ noise" recommendation in `steer-formatspread.md`. Adopt the
   structure; swap MaxP for intended-effect-size and the spread term for null-perturbation spread.

6. **Honest limit:** every number here is accuracy on tasks with ground truth. None of it measures behavior
   without a right answer, and none of it touches ENTANGLED. This paper constrains how the platform must
   *sample* prompts; it does not validate what the platform *measures*.
