---
title: "Large Language Models Are Not Robust Multiple Choice Selectors (Zheng et al.) + Large Language Models Sensitivity to The Order of Options in Multiple-Choice Questions (Pezeshkpour & Hruschka)"
url: https://arxiv.org/abs/2309.03882
authors: "Zheng et al.: Chujie Zheng, Hao Zhou, Fandong Meng, Jie Zhou, Minlie Huang (Tsinghua CoAI / WeChat AI). Pezeshkpour & Hruschka: Pouya Pezeshkpour, Estevam Hruschka (Megagon Labs)"
year: 2023 (Zheng: ICLR 2024 Spotlight; Pezeshkpour: Findings of NAACL 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Option-order sensitivity — the purest semantically-null perturbation in the literature

**Two papers, one construct. Reordering the options of a multiple-choice question changes NOTHING about its
meaning — the same facts, the same correct answer, the same wording. It is the cleanest possible null
perturbation. Yet it moves accuracy by up to 75 points. This is the strongest evidence that BRITTLE-to-null-
perturbation is the universal default state of LLMs, not a property of any particular model or prompt.**

Companion papers to `steer-formatspread.md`. Where FormatSpread perturbs separators and casing, these perturb
*ordering*. Same conclusion, independent evidence.

---

## Paper A — Zheng et al., "Large Language Models Are Not Robust Multiple Choice Selectors" (ICLR 2024 Spotlight)

**arXiv:** https://arxiv.org/abs/2309.03882

### Abstract (verbatim, complete)

> "Multiple choice questions (MCQs) serve as a common yet important task format in the research of large
> language models (LLMs). This work shows that LLMs are vulnerable to option position changes in MCQs due to
> their inherent "selection bias", namely, they prefer to select specific option IDs as answers (like "Option
> A"). Through extensive empirical analyses with 20 LLMs on three benchmarks, we pinpoint that this
> behavioral bias primarily stems from LLMs' token bias, where the model a priori assigns more probabilistic
> mass to specific option ID tokens (e.g., A/B/C/D) when predicting answers from the option IDs. To mitigate
> selection bias, we propose a label-free, inference-time debiasing method, called PriDe, which separates the
> model's prior bias for option IDs from the overall prediction distribution. PriDe first estimates the prior
> by permutating option contents on a small number of test samples, which is then applied to debias the
> subsequent samples. We demonstrate that PriDe achieves superior debiasing effectiveness and computational
> efficiency to strong baselines. Furthermore, the prior estimated by PriDe is interpretable and can
> generalize well across different domains, highlighting its practical potential in broader scenarios."

### Method

- **20 LLMs**, three benchmarks: **MMLU** (Hendrycks et al. 2020), **ARC-Challenge** (Clark et al. 2018),
  **CommonsenseQA (CSQA)** (Talmor et al. 2019).
- Diagnosis: move the *correct answer* to a fixed position and measure accuracy change; permute option
  *contents* while holding IDs fixed to separate **token bias** (prior mass on the literal tokens "A"/"B"/…)
  from **position bias**.
- **RStd** (recall standard deviation across option positions) is the bias metric; accuracy is reported
  alongside.

### THE NUMBERS (verbatim)

**Selection bias is a real prior over option ID tokens.** llama-30B selects
> "A/B/C/D **34.6% / 27.3% / 22.3% / 15.8%** of the time, while gpt-3.5-turbo for **22.5% / 25.6% / 32.3% /
> 19.6%**, respectively (averaged over 10 runs)"

A uniform model would be 25/25/25/25. llama-30B over-picks "A" by ~10 points and under-picks "D" by ~9.
**Note the models are biased in *different directions*** — llama-30B is an A-preferrer, gpt-3.5-turbo is a
C-preferrer. This is the same non-transfer result as FormatSpread Table 2, in a different guise.

**Accuracy swings from moving the correct answer (0-shot MMLU):**

| Model | Manipulation | Accuracy | Δ |
|---|---|---|---|
| gpt-3.5-turbo | correct answer → position D | 67.2 → 60.9 | **−6.3 pts** |
| llama-30b | correct answer → position A | 53.1 → 68.2 | **+15.2 pts** |

**PriDe** (debiasing with 5% of samples used for prior estimation, 0-shot MMLU, averaged across models):
**−8.9 RStd** and **+2.6 accuracy**.

**Cross-domain consistency (verbatim):**
> "Selection bias within the same LLM displays a moderate similarity across different domains"

and it
> "varies with models but manifests a cross-domain similarity within the same model"

**This is a genuinely important nuance:** the bias is *model-idiosyncratic but within-model stable*. It does
not transfer across models, but it does transfer across domains within a model. That means it is estimable
and correctable per-model — which is exactly why PriDe works.

---

## Paper B — Pezeshkpour & Hruschka, "LLMs Sensitivity to The Order of Options in MCQs" (Findings of NAACL 2024)

**arXiv:** https://arxiv.org/abs/2308.11483

### Abstract (verbatim, complete)

> "Large Language Models (LLMs) have demonstrated remarkable capabilities in various NLP tasks. However,
> previous works have shown these models are sensitive towards prompt wording, and few-shot demonstrations
> and their order, posing challenges to fair assessment of these models. As these models become more
> powerful, it becomes imperative to understand and address these limitations. In this paper, we focus on
> LLMs robustness on the task of multiple-choice questions -- commonly adopted task to study reasoning and
> fact-retrieving capability of LLMs. Investigating the sensitivity of LLMs towards the order of options in
> multiple-choice questions, we demonstrate a considerable performance gap of approximately 13% to 75% in
> LLMs on different benchmarks, when answer options are reordered, even when using demonstrations in a
> few-shot setting. Through a detailed analysis, we conjecture that this sensitivity arises when LLMs are
> uncertain about the prediction between the top-2/3 choices, and specific options placements may favor
> certain prediction between those top choices depending on the question caused by positional bias. We also
> identify patterns in top-2 choices that amplify or mitigate the model's bias toward option placement. We
> found that for amplifying bias, the optimal strategy involves positioning the top two choices as the first
> and last options. Conversely, to mitigate bias, we recommend placing these choices among the adjacent
> options. To validate our conjecture, we conduct various experiments and adopt two approaches to calibrate
> LLMs' predictions, leading to up to 8 percentage points improvement across different models and benchmarks."

### THE NUMBER

> "a considerable performance gap of approximately **13% to 75%** in LLMs on different benchmarks, when answer
> options are reordered, **even when using demonstrations in a few-shot setting**"

**CONFIRMED: the user's recalled "~75% gap" is correct** — it is the top of a stated 13%–75% range across
benchmarks, not a single headline figure. Quote it as "13% to 75%" to stay accurate.

Two mechanistic findings worth carrying:
1. **Sensitivity concentrates where the model is uncertain** — the swing arises "when LLMs are uncertain about
   the prediction between the top-2/3 choices." Order-brittleness is not uniform; it lives in the model's
   indifference zone. **This is the most design-relevant finding in this file.**
2. **Position of the top-2 choices is the lever:** first-and-last placement *amplifies* bias; adjacent
   placement *mitigates* it.
3. Calibration recovers **up to 8 percentage points**.

Also note: "even when using demonstrations in a few-shot setting" — few-shot does not fix it, converging with
FormatSpread's finding that shot-count does not shrink spread.

---

## Relevance to companion-eval-platform

**What these papers settle:**

1. **The null-perturbation brittleness result is not an artifact of one paper or one perturbation type.**
   FormatSpread (separators/casing) → 76 pts. Option reordering → up to 75 pts. Two independent research
   groups, two unrelated perturbation families, same order of magnitude. Combined with PromptBench's 33%
   relative drop (`steer-promptbench.md`), the "models are wildly sensitive to meaningless changes" finding is
   about as replicated as anything in the LLM literature. **The design cannot treat BRITTLE as a surprising
   discovery — it is the field's consensus baseline.**

2. **The non-transfer result replicates too, and it is arguably the more actionable one.** llama-30B prefers A,
   gpt-3.5-turbo prefers C. FormatSpread: format rankings transfer at 57.46% (chance=50%). Leidinger: "Prompts
   transfer poorly between datasets or models." Any per-model prompt calibration the platform performs is
   **non-portable by default**, and a cross-model steerability leaderboard inherits this problem directly.

**What these papers do NOT settle — and where the platform's construct actually differs:**

3. These measure **accuracy on items with a ground-truth answer**, under perturbations that are null **by
   construction** (reordering cannot change which answer is correct). The platform measures **behavior with no
   ground truth**, under perturbations that are **meaningful by construction** ("shy" → "very shy" *should*
   move shyness). The sign of the desired effect is **opposite**: here any movement = failure; there,
   movement = the product working. **Neither the 76-point nor the 75-point figure is an upper bound on, or a
   prediction of, intensity-word sensitivity.** They bound the *noise floor*, not the signal. See
   `steer-spurious-vs-intended.md`.

**The one finding here that transfers most directly, and it is a warning:**

4. **Pezeshkpour & Hruschka's uncertainty result predicts *where* the platform will see BRITTLE.** Order
   sensitivity concentrates where the model is torn between top-2/3 choices — i.e. brittleness is highest in
   the model's *indifference zone*. Ported to persona traits: the platform should expect maximal BRITTLE
   exactly on traits where the model has **no strong prior** — ambiguous, weakly-represented, or
   context-dependent traits. A trait that reads BRITTLE may simply be a trait the model has no settled
   representation of. **That is a substantive, testable prediction and a candidate confound**: BRITTLE may be
   measuring trait-prior-strength rather than steerability failure. Well-represented traits ("cheerful")
   should be more stable than contested ones ("authentic") for reasons that have nothing to do with the
   steering mechanism.

5. **PriDe shows null-sensitivity is estimable and subtractable.** Bias is model-idiosyncratic but
   within-model stable across domains, so 5% of samples suffices to estimate and remove it (−8.9 RStd). This
   is the methodological template the platform should steal: **estimate the model's null-perturbation floor
   from a small probe set, then report intensity-word effects net of that floor.** Zheng et al. demonstrate
   the correction is cheap. This makes the "measure the null, divide by it" recommendation in
   `steer-formatspread.md` practically feasible rather than aspirational.
