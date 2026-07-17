---
title: "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting"
url: https://arxiv.org/abs/2310.11324
authors: Melanie Sclar, Yejin Choi, Yulia Tsvetkov, Alane Suhr (University of Washington / Allen Institute for AI / UC Berkeley)
year: 2023 (ICLR 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# FormatSpread — the load-bearing number for "BRITTLE is the default"

**This is the single most important prior-art paper for the BRITTLE failure mode. Its headline result is that
a 76-accuracy-point swing is achievable from formatting alone — changes that carry ZERO semantic content.
If a semantically-null perturbation moves behavior by 76 points, then BRITTLE is not an edge case a design
can flag; it is the measured baseline condition of every model tested.**

## Abstract (verbatim, complete)

> "As large language models (LLMs) are adopted as a fundamental component of language technologies, it is
> crucial to accurately characterize their performance. Because choices in prompt design can strongly
> influence model behavior, this design process is critical in effectively using any modern pre-trained
> generative language model. In this work, we focus on LLM sensitivity to a quintessential class of
> meaning-preserving design choices: prompt formatting. We find that several widely used open-source LLMs
> are extremely sensitive to subtle changes in prompt formatting in few-shot settings, with performance
> differences of up to 76 accuracy points when evaluated using LLaMA-2-13B. Sensitivity remains even when
> increasing model size, the number of few-shot examples, or performing instruction tuning. Our analysis
> suggests that work evaluating LLMs with prompting-based methods would benefit from reporting a range of
> performance across plausible prompt formats, instead of the currently-standard practice of reporting
> performance on a single format. We also show that format performance only weakly correlates between
> models, which puts into question the methodological validity of comparing models with an arbitrarily
> chosen, fixed prompt format. To facilitate systematic analysis we propose FormatSpread, an algorithm that
> rapidly evaluates a sampled set of plausible prompt formats for a given task, and reports the interval of
> expected performance without accessing model weights. Furthermore, we present a suite of analyses that
> characterize the nature of this sensitivity, including exploring the influence of particular atomic
> perturbations and the internal representation of particular formats."

Note the framing the authors themselves choose: formatting is "a quintessential class of **meaning-preserving**
design choices." The perturbation is defined as semantically null *by construction*. Hold onto this — it is
exactly the axis on which this paper does NOT match a steerability design (see Relevance below).

## Method — how "plausible formats" are defined

Formats are not arbitrary strings. The authors define a **formal grammar** over plausible formats, so that
every sampled format is one a competent prompt engineer might plausibly have written. Building blocks:

- `B1(d,s,f) := f(d) s <text>` — a basic field: a descriptor `d` (e.g. "Passage"), a separator `s`, and a
  casing function `f`.
- `B2` — joins n fields with a spacing constant `c`.
- `B3` — enumerations (for multiple-choice items).

Constant sets instantiated (meaning-preserving transformations only):

- **S1** separators between descriptor and text: `":"`, `"::"`, `"||"`, `"-"`, etc.
- **S2** item separators: space, double-space, tab, etc.
- **C** spacing between fields: newline, tab, `":"`, `"-"`, etc.
- **F_casing**: identity, `.title()`, `.upper()`, `.lower()`
- **F_item**: number/letter format (`A/a/I/i/1`) crossed with wrappers (`(x)`, `[x]`, `<x>`, …)

**Equivalence definition:** two formats are equivalent if they apply the same rule with identical descriptors,
differing *only* in meaning-preserving transformations (casing, spacing, separators). The whole space is by
construction semantically constant.

**Scale:** 53 tasks from Super-NaturalInstructions. Early sensitivity analysis uses **10 randomly sampled
formats** per task; the comprehensive analysis evaluates **320 formats** per task. 1-shot and 5-shot settings.

## The "spread" metric

**Performance spread** = `max_i m(p_i, D) − min_i m(p_i, D)` — i.e. best-format accuracy minus worst-format
accuracy over the plausible format set `{p_1 … p_n}`. It is a *range*, not a variance.

Two evaluation metrics are used:
1. **Probability ranking** — the highest-ranked valid option matches the expected answer.
2. **Exact prefix matching** — the output's prefix matches the answer after normalization.

(Exact prefix matching yields substantially larger spreads — see below. There is no "weighted spread" metric.)

## Thompson sampling (the budget algorithm)

FormatSpread searches the format space under a user-specified compute budget using **Thompson sampling for
Bernoulli bandits with Beta priors** (each format = one arm).

- Budget `E` split: `E/2` to find the maximum-performing format, `E/2` for the minimum; phase 1 supplies
  informative priors to phase 2.
- Priors: `Beta(α, β)` with `β = 5`, `α = max(β·x/(1−x), 1.1)`, where `x` is the original format's accuracy.
- Mini-batch size `B = 20` samples per arm evaluation.
- Reported efficiency, verbatim:

> "With a budget of 51,200 evaluations, Thompson sampling results in a spread within 1 accuracy point of the
> true spread, while naive sampling finds a spread within 4 points, and UCB within 11."

Crucially: FormatSpread does **not** require model weights — it works on API-only models.

## THE NUMBERS (all verbatim)

### Headline
> "performance differences of up to **76 accuracy points** when evaluated using LLaMA-2-13B"

### Median spreads (probability ranking, 53 tasks)
| Setting | Verbatim number |
|---|---|
| LLaMA-2 (across model choice + n-shot) | "median spread of **7.5 accuracy points**" |
| 1-shot LLaMA-2-70B | "yields a median spread of **0.171** (mean=0.221, std=0.200)" |
| 5-shot LLaMA-2-70B | "still shows high spreads, with **25% of tasks having a spread of 0.310**" |
| GPT-3.5 | "yields a median spread of **0.064** (mean=0.110, std=0.115, across 53 tasks)" |

### Exact prefix matching (the more realistic generative setting)
> "median spread ranging from **12 to 28 accuracy points** depending on the model"

**This is the number to quote for generative/free-text behavior** — the ~7.5-point median is the
constrained-ranking setting. When the model actually *generates*, the median semantically-null spread is
12–28 points.

### Task-level persistence
> "**20% of tasks** consistently result in a spread of **at least 15 accuracy points** for **all** LLaMA-2
> settings"

That "all settings" is doing real work: for a fifth of tasks, no choice of size or shot-count rescues you.

## Does spread shrink with scale / instruction tuning / more few-shot examples? NO.

Verbatim from the abstract:

> "Sensitivity remains even when increasing model size, the number of few-shot examples, or performing
> instruction tuning."

Supporting structure:
- **Model size:** spread persists across LLaMA-2-7B → 13B → 70B. 1-shot 70B still has median spread 0.171;
  5-shot 70B still has 25% of tasks at spread 0.310. The largest model in the study is *not* meaningfully
  more format-robust.
- **Instruction tuning:** Falcon-7B vs Falcon-7B-Instruct compared directly; sensitivity remains.
- **Few-shot examples:** 1-shot vs 5-shot compared directly; sensitivity remains.

**CONFIRMED: the user's prior is correct.** Format brittleness does not wash out with scale, instruction
tuning, or more demonstrations. This is stated in the abstract of an ICLR 2024 paper and is not a contested
claim.

Related: more sampling only *finds* more spread — "about 17% of tasks are expected to increase their spread
by at least 5 accuracy points when increasing from 10 to 20 sampled formats." The spread you measure is a
lower bound on the spread that exists.

## Do format rankings transfer across models? NO — and there is NO Spearman number.

**Correction to a common assumption: this paper does not report a Spearman correlation for cross-model format
transfer.** I checked the full text specifically for this. The transfer result is reported as a **pairwise
ordering-preservation ratio** in Table 2.

> **Table 2 caption (verbatim):** "Ratio of prompt format pairs (p1,p2) such that if p1 is worse than p2
> using model M1, then the same trend holds for M2."

| Model pair | Ratio |
|---|---|
| Llama-2-7b → Llama-2-13b | **57.46%** |
| Llama-2-7b → Falcon-7b | **55.91%** |
| Falcon-7b → Falcon-7b-Inst | **61.11%** |

**Chance is 50%.** So format rankings transfer at 6–11 percentage points above coin-flip — even between two
sizes of the *same model family* (57.46%), and even between a base model and its own instruction-tuned
version (61.11%). This is the strongest available evidence that "the good format" is not a property of the
task; it is a property of the (model × task) pair.

The abstract's own summary: "format performance only weakly correlates between models, which puts into
question the methodological validity of comparing models with an arbitrarily chosen, fixed prompt format."

> **Figure 4 caption (verbatim):** "Probability that model M performs worse than M′ by at least d when using
> format p′, given that M performed better than M′ by at least d using format p. 53 tasks, 1- and 5-shot."

i.e. **model A-beats-B conclusions reverse under format change.** "LLaMA-2-13B and -70B reverse trend by at
least d=0.02 with probability 0.141" — a ~14% chance of flipping the sign of a model comparison purely by
reformatting.

## The space is non-monotonic and unpredictable

> "32.4 and 33.6% of triples were monotonic for multiple-choice and non-multiple-choice tasks respectively.
> Given that random shuffling ... will result in monotonicity 33.3% of the time, this suggests that local
> search mechanisms like simulated annealing may not be effective."

**Monotonicity is at chance (33.3%).** The format-performance surface has no exploitable local structure —
you cannot hill-climb to a good format, you can only search.

> "24% of atomic changes have an associated accuracy change of at least 5 points when using exact prefix
> matching" (11% with probability ranking).

A quarter of *single* atomic edits (one separator, one casing change) move accuracy ≥5 points.

**Formats are highly identifiable internally:** using the top 100 principal components of prompt embeddings
yields ≥0.98 format classification accuracy for all 31 tasks analyzed — the model represents format
distinctly even though format is semantically empty. Classifier accuracy from just the top two components
"correlates moderately with the spread of performance in the prompts they represent (0.424, p=8.04⋅10⁻⁶;
0.555 for the 5-shot setting)."

## Relevance to companion-eval-platform

**This paper is simultaneously the strongest support for and the strongest threat to the three-failure-mode
design. Read carefully, it is mostly a threat to the *interpretation*, not the *measurement*.**

**Where it supports the design:**
- BRITTLE is real and enormous. 76 points max, 12–28 median under generative decoding. Any steerability
  metric that does not report a *range* over nuisance variation is reporting noise with a decimal point.
- It validates spread-as-range (max − min) as the field-standard framing, and Thompson sampling as the
  budget-respecting way to estimate it. If the platform needs a brittleness estimator, this is the reference
  implementation to copy, and it works API-only (no weights).
- It kills the "just use a bigger/instruction-tuned model" objection dead, from the abstract.

**Where it threatens the design — this is the important part:**
1. **If BRITTLE is the default state of every model, "BRITTLE" is not a diagnostic verdict.** A test whose
   positive class is ~100% prevalent has no discriminative value. FormatSpread's 20%-of-tasks-≥15-points and
   12–28-point median mean the platform will label essentially every (model, trait) cell BRITTLE unless the
   threshold is calibrated against a *measured null distribution* rather than set a priori. **Recommendation:
   the BRITTLE threshold must be defined relative to a same-model, same-trait, semantically-null perturbation
   baseline — i.e. measure this model's format spread on this trait first, and only call BRITTLE when
   intensity-word variation exceeds that floor.** Without that, BRITTLE measures "is this an LLM?"
2. **Construct mismatch (the crux the user flagged).** FormatSpread perturbs `separator/casing/spacing` —
   defined as meaning-preserving. The design perturbs *intensity words* ("shy" → "very shy"), which are
   meaning-**changing**. Sensitivity to the former is a defect; sensitivity to the latter is *the product
   working*. These are opposite-signed constructs that happen to share the word "sensitivity." FormatSpread's
   76 points is therefore NOT a direct upper bound on, or baseline for, intensity-word sensitivity — it is
   the **noise floor against which intended sensitivity must be contrasted**. See `steer-spurious-vs-intended.md`.
3. **The 57.46% transfer number is the real design constraint.** Format rankings barely transfer between 7B
   and 13B of the same family. Any per-model prompt tuning the platform does is non-portable; a "steerability
   score" measured on model A says almost nothing about model B, and cross-model steerability leaderboards
   are methodologically unsound for the same reason FormatSpread says fixed-format model comparison is
   unsound.
4. **Non-monotonicity (32.4% ≈ chance) predicts ENTANGLED will be hard to attribute.** If the prompt-response
   surface has no local structure for null perturbations, then observing that "shy" moves "cruel" may be a
   surface artifact rather than genuine trait entanglement. The design needs a null model for ENTANGLED too.
5. **DEAD is the mode this paper makes *least* likely to be observed.** Given that meaningless changes move
   things by 12–28 points, a trait whose *meaningful* wording moves nothing would be genuinely surprising and
   informative. DEAD is arguably the highest-information verdict of the three.

**Actionable takeaway:** the three modes are not symmetric. DEAD is rare and informative. BRITTLE is
near-universal and needs a null-calibrated threshold or it is vacuous. ENTANGLED needs a null model. The
design should measure **intensity-word effect size ÷ format-noise floor** (a signal-to-noise ratio), not raw
intensity-word sensitivity.
