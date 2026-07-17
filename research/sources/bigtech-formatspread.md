---
title: "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting (FormatSpread)"
url: https://arxiv.org/abs/2310.11324
authors: Melanie Sclar, Yejin Choi, Yulia Tsvetkov, Alane Suhr (University of Washington; Allen Institute for AI; UC Berkeley)
org: University of Washington / AI2 / UC Berkeley
year: 2023
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# FormatSpread — the NOISE FLOOR any elasticity estimate must clear

**Verdict up front: this does NOT measure dose-response. It measures the opposite and that is why it matters: how much behavior moves when the prompt changes in ways that should move it ZERO. It is the denominator sanity check for our entire framework. Evidence for the Brittle mode, and a methodological threat to every slope we will ever report.**

Verification: arxiv abstract page fetched raw via curl; PDF (arxiv.org/pdf/2310.11324, 98,322 chars) extracted with pypdf. The string "76 accuracy points" appears exactly once and was matched in context. ICLR 2024.

## Abstract (verbatim)

> "As large language models (LLMs) are adopted as a fundamental component of language technologies, it is crucial to accurately characterize their performance. Because choices in prompt design can strongly influence model behavior, this design process is critical in effectively using any modern pre-trained generative language model. In this work, we focus on LLM sensitivity to a quintessential class of **meaning-preserving design choices: prompt formatting**. We find that several widely used open-source LLMs are **extremely sensitive to subtle changes in prompt formatting in few-shot settings, with performance differences of up to 76 accuracy points when evaluated using LLaMA-2-13B**. **Sensitivity remains even when increasing model size, the number of few-shot examples, or performing instruction tuning.** Our analysis suggests that work evaluating LLMs with prompting-based methods would benefit from **reporting a range of performance across plausible prompt formats**, instead of the currently-standard practice of reporting performance on a single format."

## Why this is load-bearing for a steerability framework

Our elasticity is `Δ(trait expression) / Δ(trait emphasis)`. FormatSpread establishes the **null-dose variance**: change the prompt in a way that carries **zero** semantic dose — separators, casing, spacing, punctuation — and behavior still swings by **up to 76 accuracy points**.

This creates an unavoidable methodological obligation:

**A dose-response slope is only interpretable relative to the spread induced by zero-dose perturbations.** If upgrading "shy" → "extremely shy" moves trait expression by 8 points, but swapping `Q:`/`A:` for `Question:`/`Answer:` also moves it by 8 points, then our elasticity has measured nothing but noise wearing a lab coat. We would have a number, a curve, and no signal.

**Consequence for our design: every dose rung must be run over a distribution of semantically-null format variants, and we must report the elasticity against that spread.** This is not optional rigor; it is the difference between a real result and a fabricated one. Our project has a documented incident about exactly this class of error.

`meaning-preserving` appears once, `semantically equivalent` 4 times, `spread` 132 times.

## Relation to the Brittle failure mode

Our Brittle mode is "slope explodes". FormatSpread is the pathological limit: **infinite slope at zero dose** — behavior moves with no semantic input at all. It shows Brittle is not a hypothetical corner of our taxonomy; it is the documented default behavior of LLMs under prompt perturbation, and it is scale-resistant: "Sensitivity remains even when increasing model size, the number of few-shot examples, or performing instruction tuning."

Note the convergence with `bigtech-steerability-course-correction.md`, which found scaling reduces miscalibration but **not** orthogonality. Two papers, two constructs: **the pathologies of prompt-space control do not scale away.**

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**NO. It measures the noise floor beneath any dose-response.**

- Prompt-space perturbation → behavior change: **YES**
- **Semantic dose axis: NO** — perturbations are explicitly meaning-*preserving*; there is no "more" or "less" of anything, so no dose ordering exists and no slope can be defined
- Trait expression: **NO** — task accuracy on benchmarks
- Curve fitted: **NO** — reports spread/range across a format distribution

## Companion: "State of What Art? A Call for Multi-Prompt LLM Evaluation"

Verified raw (arxiv.org/abs/2401.00595). Abstract (verbatim excerpt):

> "These benchmarks typically rely on a **single instruction template** for evaluating all LLMs on a specific task. In this paper, we comprehensively analyze the **brittleness of results obtained via single-prompt evaluations across 6.5M instances, involving 20 different LLMs and 39 tasks from 3 benchmarks**. To improve robustness of the analysis, we propose to **evaluate LLMs with a set of diverse prompts** instead."

Same lesson at larger scale (6.5M instances, 20 LLMs, 39 tasks): single-prompt evaluation is brittle; report distributions over prompts. **Our steerability harness is a prompt-based evaluation and inherits this entire critique.** Each rung of our intensity ladder is a single template unless we deliberately make it a distribution.

## Relevance to companion-eval-platform

1. **This paper sets a hard precondition on our headline result.** Before reporting any elasticity, run the null-dose control: fix the trait word, vary only formatting, measure trait-expression spread. **That spread is our noise floor.** Report elasticity as signal-to-noise against it, not in raw points. If our slopes sit inside the format spread, the honest finding is "prompt-space trait control is indistinguishable from formatting noise" — which, given PsySET's flat result, is a live possibility and would itself be a publishable, product-critical finding.
2. **It makes the "Dead" diagnosis much harder than we assumed.** Dead = slope ≈ 0. But a small slope buried in large format variance is *unidentifiable*, not *dead*. Distinguishing them requires enough samples per rung to resolve a slope against the noise — a power calculation, which our project has a source for (`psycho-power-sample-size.md`). **We should do that power analysis before running the experiment, not after.**
3. **Each ladder rung must be a distribution, not a string.** Sample paraphrases and formats per rung; the rung's trait expression is a distribution with a mean and a spread. This also gives us error bars on the slope for free, which is what makes a fitted elasticity defensible.
4. **It is a genuine intellectual contribution to our framing.** Nobody in the steerability literature we found (IBM, PsySET, Course Correction, Oxford/AISI) reports their steering effect against a format-noise baseline. **Combining the elasticity construct with the FormatSpread control is a real methodological improvement over all four**, and it is cheap. If PsySET's "all levels give about the same emotion transfer" is measured without a noise floor, we cannot tell whether prompt-space control is *dead* or merely *drowned*. That question is open and we are well-placed to answer it.
5. **Related:** `bigtech-psyset.md`, `bigtech-prompt-steerability.md` (IBM flags "specific phrasing or word choice in the persona statements" as a limitation — the same worry), `bigtech-steerability-course-correction.md`, `psycho-variance-in-benchmarks.md`, `psycho-power-sample-size.md`, `judge-style-control-arena.md`.
