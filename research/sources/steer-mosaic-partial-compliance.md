---
title: "Deconstructing Instruction-Following: A New Benchmark for Granular Evaluation of Large Language Model Instruction Compliance Abilities (MOSAIC)"
url: https://arxiv.org/abs/2601.18554
authors: (see arXiv listing — 2026 preprint)
year: 2026
type: benchmark
accessed: 2026-07-16
topic: steerability
---

# MOSAIC — the ONE benchmark that keeps a continuous compliance score. It grades the ANSWER, not the ASK.

**Why this file exists:** MOSAIC is the closest hit in the entire instruction-following literature to "graded compliance," and the most likely paper for a reviewer to throw at us. It scores compliance on a **continuous 0.0–1.0 scale** and explicitly reasons about **degree of adherence**. This file establishes precisely where it stops — and it stops exactly one step short of dose-response, in an instructive way.

**Verdict: MOSAIC has our y-axis but not our x-axis.** It grades the *response* continuously while holding the *instruction* fixed and binary. That is half of dose-response — the half nobody else has — and it makes MOSAIC both the most relevant prior art and the strongest evidence that the missing half is the graded *instruction*.

## Abstract (verbatim)

> "Reliably ensuring Large Language Models (LLMs) follow complex instructions is a critical challenge, as existing benchmarks often fail to reflect real-world use or isolate compliance from task success. We introduce MOSAIC (MOdular Synthetic Assessment of Instruction Compliance), a modular framework that uses a dynamically generated dataset with up to 20 application-oriented generation constraints to enable a granular and independent analysis of this capability."

Note the framing "**isolate compliance from task success**" — MOSAIC shares our instinct that adherence must be measured separately from whether the answer is good. That is the same move our design makes.

## Scoring: continuous where it can be, binary where it can't

Two regimes, and the split is the tell:

- **Formatting / Lexical / Syntactic constraints** → **rule-based functions returning continuous values in [0.0, 1.0]**, computing "the rate of compliance" or "proportion of lines" meeting criteria.
- **Semantic / Business / Legal constraints** → **LLM-as-a-judge scores 0–10, then converted to BINARY (0 or 1) via a 0.5 threshold.**

**This asymmetry is the crux, and it is the same asymmetry as CFBench's Numerical-vs-Stylistic split.** Where compliance is mechanically countable (what proportion of lines are under 80 chars?), MOSAIC keeps the fraction. Where compliance is **semantic** — the category our companion traits live in — it **has a 0–10 judge score in hand and throws it away at a 0.5 threshold.**

Read that again: the continuous signal for semantic constraints **already exists in their pipeline** and is deliberately discarded. **Our design's core methodological bet is simply: don't discard it.** That is a smaller, more credible, more defensible claim than "we invented graded evaluation," and MOSAIC is the evidence that the field's binarisation is a *choice*, not a technical necessity.

## What the partial score measures (the decisive limitation)

Partial scores are computed by measuring **adherence degree** — e.g. percentage of sentences meeting a length requirement, standard deviation of sentence lengths. Explicitly:

- **The instruction is NOT varied by intensity.** No "somewhat formal" vs. "very formal". Instructions "remain fixed and binary; only the response quality is graded on its adherence to those fixed directives."
- **The instruction IS varied by count: 1 → 20 constraints per prompt.**

So MOSAIC's x-axis is *constraint count* — FollowBench's axis (`steer-followbench-levels.md`), pushed from 5 to 20. Its y-axis is *fractional adherence to a fixed demand*. Neither axis is trait intensity.

**The distinction in one line:** MOSAIC asks *"you said 'use short sentences' — what fraction of sentences are short?"* We ask *"as I turn 'shy' from 0 to 1, how much does shyness move?"* Theirs is a compliance fraction against a fixed bar. Ours is a transfer function.

## Scale and setup

- **4,000 prompts**, stratified from **765,472** generated (synthetic, modular, dynamically generated)
- **21 constraints across 5 categories**; **1–20 constraints per prompt**
- **7 models:** Llama 3.1-8B / 70B, Qwen3 8B, Mixtral-8x-7B, DeepSeek-R1 8B, Gemini 2.5 Flash, Claude 3.7 Sonnet

## Findings

- **"Compliance is not a monolithic capability"** — it varies significantly by constraint type.
- **Primacy/recency positional biases identified** — constraints at the start and end of a prompt are followed better than those in the middle.

Both findings are directly load-bearing for us (see below).

## Verdict against our design

| Our construct | MOSAIC? |
|---|---|
| Dose axis (intensity of one trait) | **NO** — instructions fixed and binary; count varies 1–20 |
| **Continuous response variable** | **PARTIAL — YES for rule-checkable constraints, NO for semantic ones (thresholded at 0.5)** |
| Fitted curve / slope | **NO** — no dose to regress against |
| Constraint interaction | **PARTIAL** — positional effects and per-type variation, not trait crosstalk |
| Isolating compliance from task success | **YES** — shared instinct |

## Relevance to companion-eval-platform

1. **This is the paper most likely to be used against us, so we should cite it first and precisely.** A reviewer skimming for "graded instruction following" lands here. Our answer must be crisp: **MOSAIC grades the response, not the ask. Without a graded ask there is no dose, and without a dose there is no curve — only a compliance percentage against a fixed bar.** Elasticity is a *derivative*; you cannot take one with a single x-value.

2. **MOSAIC proves the y-axis is tractable, which de-risks our design.** The most common objection to our platform is "you can't put a continuous number on how shy a response is." MOSAIC (rule-based side) and the existence of their discarded 0–10 semantic judge scores show continuous adherence scoring is already engineering practice. **We are not inventing a measurement; we are declining to throw one away and adding an x-axis to it.** That reframing makes the project far easier to defend.

3. **Their 0.5 threshold on semantic constraints is our single best piece of evidence for the field-wide blind spot.** CFBench computes `0.5 + 0.5×avg(secondary)` and re-thresholds at 0.8. MOSAIC gets 0–10 judge scores and thresholds at 0.5. **Two independent teams generated continuous compliance signal and binarised it on purpose.** That is not an oversight — it is a convention. Naming that convention, and breaking it, is a legitimate contribution and a much sharper story than "nobody measured intensity."

4. **"Compliance is not a monolithic capability" independently corroborates our trait-specificity claim.** It matches IBM's "each model favours a subset of persona dimensions", ASTEER's "depends on prompt, concept, model", and PsySET's construct-specific findings (`bigtech-prompt-steerability.md`, `bigtech-steerability-other-benchmarks.md`, `bigtech-psyset.md`). **Four independent papers now agree steerability/compliance is a property of (model, constraint-type), not a scalar.** Our platform must report a profile or matrix per trait, never one "steerability score" — this is now over-determined by the evidence.

5. **The primacy/recency finding is an immediate confound for our experiments.** If constraints mid-prompt are followed worse, then **where the dosed trait sits in the character sheet changes its measured elasticity.** A curve measured with "shy" at the top of the sheet will differ from one measured with it buried in paragraph three. **We must randomise or fix trait position across dose levels, or our slopes are contaminated by position.** This is a concrete, cheap methodological fix that we would likely have missed — arguably the most actionable single item from this whole sweep.

6. **1→20 constraints extends FollowBench's count axis 4×, and it is free ammunition.** FollowBench stops at 5 and reports CSL ≈ 3.3. MOSAIC goes to 20. If we want the "rules × turns" 2D grid from `game-followbench.md`, MOSAIC's range is the better precedent for the rules axis and shows the count axis is thoroughly worked. **Do not re-do the count axis — it is crowded. Own the intensity axis, which is empty.**

7. **Caveat: 2026 preprint (arXiv 2601.18554), very recent as of our 2026-07-16 access.** Details above come from an HTML extraction pass, not a full read. The **0.5 binarisation threshold for semantic constraints** is the load-bearing claim in this file — **verify it directly in the paper before citing it in writing**, because our "the field binarises on purpose" argument leans on it.

**Related:** `steer-followbench-levels.md` (count axis, L1–L5), `steer-cfbench.md` (PSR's 0.8 re-threshold — the twin of MOSAIC's 0.5), `bigtech-infobench.md` (DRFR binary-atom origin), `steer-complexbench.md`.
