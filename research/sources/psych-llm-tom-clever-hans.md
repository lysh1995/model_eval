---
title: "Clever Hans or Neural Theory of Mind? + Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs"
url: https://aclanthology.org/2024.eacl-long.138/
authors: Natalie Shapira, Mosh Levy, Seyed Hossein Alavi, Xuhui Zhou, Yejin Choi, Yoav Goldberg, Maarten Sap, Vered Shwartz (2024); Maarten Sap, Ronan LeBras, Daniel Fried, Yejin Choi (2022)
year: 2022-2024
type: critique
accessed: 2026-07-16
topic: psychology-crosscheck
---

# The "shallow heuristics" critique — Shapira et al. (EACL 2024) + Sap et al. (EMNLP 2022)

Sources compiled:
- Shapira, Levy, Alavi, Zhou, Choi, Goldberg, Sap & Shwartz, "Clever Hans or Neural Theory of Mind?
  Stress Testing Social Reasoning in Large Language Models," EACL 2024 —
  https://arxiv.org/abs/2305.14763 · https://aclanthology.org/2024.eacl-long.138/ ·
  https://ar5iv.labs.arxiv.org/html/2305.14763
- Sap, LeBras, Fried & Choi, "Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs,"
  EMNLP 2022 — https://aclanthology.org/2022.emnlp-main.248/ · https://arxiv.org/abs/2210.13312

## Part 1 — Sap et al. 2022: the original pessimistic result

Full abstract (verbatim):

> "Social intelligence and Theory of Mind (TOM), i.e., the ability to reason about the different mental
> states, intents, and reactions of all people involved, allows humans to effectively navigate and
> understand everyday social interactions. As NLP systems are used in increasingly complex social
> situations, their ability to grasp social dynamics becomes crucial. In this work, we examine the open
> question of social intelligence and Theory of Mind in modern NLP systems from an empirical and
> theory-based perspective. We show that one of today's largest language models (GPT-3; Brown et al.,
> 2020) lacks this kind of social intelligence out-of-the box, using two tasks: SocialIQa (Sap et al.,
> 2019), which measure models' ability to understand intents and reactions of participants of social
> interactions, and ToMi (Le, Boureau, and Nickel, 2019), which measures whether models can infer mental
> states and realities of participants of situations. Our results show that models struggle substantially
> at these Theory of Mind tasks, with well-below-human accuracies of **55% and 60% on SocialIQa and ToMi**,
> respectively. To conclude, we draw on theories from pragmatics to contextualize this shortcoming of large
> language models, by examining the limitations stemming from their data, neural architecture, and training
> paradigms. **Challenging the prevalent narrative that only scale is needed, we posit that person-centric
> NLP approaches might be more effective towards neural Theory of Mind.**"

Error analysis findings:
- **Recency bias** — "GPT-3 models exhibit a notable recency bias and participant confusion, particularly
  on ToMi questions, with GPT-3-DAVINCI often defaulting to the most recently mentioned object location."
- **In-context learning ceiling** — "For SocialIQa, performance only increased by 1% from 10 to 35
  examples, and for ToMi, improvements were not substantial beyond k=4."

Note this predates Kosinski by months and reaches the opposite conclusion on overlapping tasks. Ullman
cites it as "(14)" — "While some of these tests offer a pessimistic evaluation (14)…"

## Part 2 — Shapira et al. 2024: the systematic stress test

**Six existing tasks evaluated:**

| Task | Size |
|---|---|
| Triangle COPA | 100 problems, social reasoning with fictional characters |
| SocialIQa | 400-sample subset — motivations and emotional reactions |
| ToMi | 400-sample synthetic false-belief dataset |
| **ToMi'** | 180 questions (30 stories) **reformatted to sentence-completion format** |
| Epistemic Reasoning | 2,000 questions on mental state logic |
| FauxPas-EAI | 176 questions (44 stories), faux pas recognition |

**Plus a new adversarial set — Adv-CSFB** (183 questions, 40 stories): Kosinski's original false-belief
examples, **true-belief** variants (the control Kosinski lacked), and adversarial variations
"inspired by Ullman (2023)": transparent access, uninformative labels, trustworthy testimony, late
labels, and "in→on" relationship changes.

### Results — GPT-4 on unexpected transfer, and the inverse-scaling bombshell

| Condition | GPT-4 | (davinci-002) |
|---|---|---|
| False belief (original) | **97.5%** | — |
| Trusted testimony | 83.3% | — |
| Other person | **68.8%** | **93.8%** |
| **In→on** | **0%** | **71.4%** |
| **Transparent access** | **0%** | **66.7%** |

**Two things here, and the second is the more interesting one.**

First: GPT-4 scores **97.5%** on the canonical task and **0%** on two perturbations. This is a systematic,
peer-reviewed replication of Ullman at scale — his hand-built counterexamples were not cherry-picked.

Second, and under-appreciated: **GPT-4 is dramatically WORSE than the older, smaller davinci-002 on the
perturbed variants** — 0% vs 71.4% on in→on, 0% vs 66.7% on transparent access, 68.8% vs 93.8% on other-
person. That is **inverse scaling**. The newer model got better at the canonical form and *lost* the
ability to handle variants. This is the signature of a model that has fit the benchmark's template harder,
not understood the domain better. Kosinski's beautiful 40→70→90→95 emergence curve
(`psych-llm-tom-kosinski.md`) **runs backwards** once you leave the template.

### The ToMi' result — reformatting destroys performance

> "GPT-3.5 … achieves 81% accuracy" overall but "only 46%" on the "false belief" subset — "close to random
> performance."

ToMi' is *the same task* as ToMi, reformatted from QA to sentence completion. **The format, not the
content, carries most of the score.**

### Conclusions (verbatim)

> "models do not have _robust_ N-ToM abilities"

> "performance gaps between different question types suggests that LLMs rely on shortcuts, heuristics, and
> spurious correlations"

> "we caution readers to interpret 'neural ToM' carefully and without aiming to make claims about 'AI
> cognition.'"

> "it is important to be cautious when drawing conclusions about ToM in models based on their performance on
> a few tasks"

> "**when a system succeeds on an instrument designed for humans, we can't draw the same conclusions as we
> would for humans.**"

The paper's overall caution: "against drawing conclusions from anecdotal examples, limited benchmark
testing, and using human-designed psychological tests to evaluate models."

## Why this matters for the L1/L2/L3 framework

1. **"Performance gaps between question types ⇒ shortcuts" is a diagnostic we can run tomorrow.** This is
   the same logic as FANToM's ALL* (`psych-fantom-benchmark.md`) and Warnell & Redcay's inter-task
   correlations (`psych-tom-task-convergence.md`), stated as a *method*: **variance across framings of one
   construct is the measurement of shallowness.** Our version: probe each character fact in several
   formats and treat the *spread* as the primary statistic. Under this view, the framework has it exactly
   backwards — cross-framing disagreement isn't noise to average away en route to an L1 score, it **is**
   the L1 finding.

2. **Inverse scaling is the strongest argument against a cascade.** A cascade says L1 is foundational: fix
   comprehension and downstream layers improve. But GPT-4 *regressed to 0%* on perturbations its
   predecessor handled at ~70%, while improving on the canonical task. Capability at the layer moved in
   **two directions at once** depending on surface form. A variable that can go up and down simultaneously
   depending on how you ask is not a foundation — it isn't a scalar at all. **You cannot build a causal
   ordering on top of a quantity that has no consistent value.**

3. **ToMi' is the direct warning about our harness design.** Same content, different format, 81% → 46%
   (chance). If our L1 probe is multiple-choice and our L2 probe is free-form roleplay, then **any L1→L2
   "cascade" we observe is confounded with format**. We'd be measuring the MC-to-free-form drop and calling
   it a layer transition. Controlling format across layers isn't a refinement — without it the cascade is
   untestable in principle.

4. **The "Clever Hans" framing names our actual risk.** Clever Hans really did produce correct answers; the
   mechanism was just not arithmetic. A companion model that passes every character-comprehension probe may
   be reading the shape of the probe. And per Ullman, **publishing the probe generator guarantees this** —
   the next model trains on it. Keep a held-out perturbation set; never ship it.

5. **The instrument-transfer warning applies to this entire research effort — including these files.** "When
   a system succeeds on an instrument designed for humans, we can't draw the same conclusions as we would
   for humans." Every psychometric tool we're importing (alpha, IRT, factor analysis, inter-rater
   agreement) was built for human respondents, whose errors are noisy-but-unbiased around a stable trait.
   Model errors are **systematic and prompt-dependent** — a double space flips them. That breaks the CTT
   assumption `X = T + E` with E mean-zero and independent of T (`psycho-classical-test-theory.md`). For a
   model, "E" is a deterministic function of prompt surface form, which means **there may be no T at all.**
   This is the deepest problem with the framework: it assumes each layer names a true score the model
   possesses. The evidence says a model has *responses*, not *traits*.
