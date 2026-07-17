---
title: "A Course Correction in Steerability Evaluation: Revealing Miscalibration and Side Effects in LLMs"
url: https://arxiv.org/abs/2505.23816
authors: Trenton Chang (University of Michigan), Tobias Schnabel (Microsoft Research), Adith Swaminathan (Netflix), Jenna Wiens (University of Michigan)
org: University of Michigan / Microsoft Research / Netflix
year: 2025
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Course Correction — steering error decomposed into MISCALIBRATION (≈ our elasticity error) and ORTHOGONALITY (≈ our crosstalk)

**Verdict up front: this paper formalizes exactly the two quantities our framework is built on — "did it move the right amount along the requested axis" (miscalibration) and "did it move axes nobody asked about" (side effects / orthogonality) — and measures both. It uses intensity adverbs ("slightly/much") in the prompt. This is a serious refutation. What saves us: the axes are rule-based TEXT ATTRIBUTES, not character traits, and no curve is fitted.**

Verification: PDF (arxiv.org/pdf/2505.23816, 34 pages, 191,904 chars) extracted with pypdf; all quotes string-matched. arXiv v2 stamped "arXiv:2505.23816v2 [cs.CL] 17 Jan 2026". AAAI. Code open-sourced (per abstract).

## Abstract (verbatim excerpt)

> "Despite advances in large language models (LLMs) on reasoning and instruction-following tasks, it is unclear whether they can reliably produce outputs aligned with a variety of user goals, a concept called **steerability**. Two gaps in current LLM evaluation impede steerability evaluation: (1) many benchmarks are built with past LLM chats and Internet-scraped text, which may skew towards common requests, and (2) **scalar measures of performance common in prior work could conceal behavioral shifts in LLM outputs in open-ended generation**. Thus, we introduce a framework based on a **multi-dimensional goal-space** that models user goals and LLM outputs as vectors with dimensions corresponding to text attributes (e.g., reading difficulty). Applied to a text-rewriting task, we find that **current LLMs induce unintended changes or side effects to text attributes, impeding steerability**."

Note gap (2) — "scalar measures could conceal behavioral shifts" — is *our* argument for why binary compliance metrics are insufficient. Someone already made it, in an abstract, at AAAI.

## The framework (verbatim)

> "We map user goals and LLM outputs into a shared, multi-dimensional **goal-space** with text-to-scalar functions, from which we sample a **steerability probe** comprised of equally-weighted goals. A multi-dimensional goal-space allows us to measure behaviors such as **miscalibration: too much/too little change along the requested direction**, or **side effects: unintended shifts in dimensions orthogonal to user goals** (Amodei et al. 2016)."

Read those two definitions against our framework:
- **"miscalibration: too much/too little change along the requested direction"** = our elasticity being wrong (slope ≠ 1; Dead if too little, Brittle if too much)
- **"side effects: unintended shifts in dimensions orthogonal to user goals"** = our off-diagonal crosstalk / Entangled mode

These are not loose analogies. They are the same two constructs.

## Metric geometry (verbatim, Figure 1 caption)

> "Figure 1: Steerability metrics in 2D goal-space (reading level & text length). A user aims to rewrite text according to some intent, expressed via a prompt (*Make this harder to read...*). The **steering error** (red dotted line) is the gap between the user's intent (blue) and the LLM's output (red). **Miscalibration (miscal.) and orthogonality (ortho.) decompose steering error into components parallel and orthogonal to user intent respectively.**"

The worked example in the figure (verbatim): source text `Cats are animals.`; user goal `Make this harder to read and a little longer.`; LLM response `Say, felines are totally like, a whole other sort of animal, you know?`; oracle response `Cats are classified as Felis catus.`

So: `z0` (source text) → `z*` (target goal) → `ẑ` (LLM output), all in goal-space. **Steering error = miscalibration ⊕ orthogonality.** Clean vector decomposition.

## THE PROMPT-INTENSITY DETAIL (verbatim) — this is the load-bearing one

> "Some residual miscalibration is expected, since **the model may not be calibrated to the magnitude of 'slightly/much' in our prompts**."

**They put intensity adverbs in the prompt and measure whether output movement tracks them.** That is a prompt-space dose. It is a 2-rung ladder ("slightly" / "much"), embedded in a target-tracking design rather than a curve-fitting design — but the construct is ours.

## Goal dimensions — deliberately rule-based, NOT traits (verbatim)

> "We choose a **small number of rule-based goal dimensions to disentangle the accuracy of goal measurement from steerability**, and to aid in interpretation of results."

Dimensions used: **reading difficulty (Flesch-Kincaid grade), formality (Heylighen-Dewaele score), text length.**

This is the key scoping decision and the reason the paper does not close our gap. They explicitly traded construct richness for measurement validity — the same trade IFEval made (`game-ifeval.md`). Character traits ("shy", "cruel") have no Flesch-Kincaid equivalent; measuring them requires a judge, which reintroduces the reliability problem their design was built to avoid.

## Results (verbatim)

> "**Even strong LLMs induce side effects.** Neither larger nor newer models meaningfully improve steering error. Median steering error remains high, **0.452 for the largest model (Llama-3.3**; Figure 2, left), far from ideal despite outperforming a random baseline (**0.770**; sampling random goal levels in each dimension). Miscalibration improves (Figure 2, center) with model size (e.g., **Llama3.1-8B vs. 70B: 0.667→0.455**)."

> "Median **orthogonality remains high and skewed towards 1** even as model size increases (Figure 2, right) with **Llama3.3-70B performing best with an orthogonality of 0.718**. While several pairwise differences are statistically significant, models remain in a **high-orthogonality regime** on average."

> "larger/newer models **reduce miscalibration but have little effect on orthogonality**"

**That last sentence is the most important empirical result in this paper for us: scaling fixes the gain error but NOT the crosstalk.** Entanglement is not a small-model problem. It does not wash out. If it held for character traits, it would mean crosstalk is a permanent property of prompt-space control and therefore a permanent product risk — exactly the kind of durable finding worth building an eval around.

## THE ENTANGLEMENT EVIDENCE (verbatim)

> "**Goal dimensions may be entangled.** We investigate side effects in a 2D (reading difficulty, formality) subspace using a **vector flow diagram** of goal-space movement (Figure 3, Llama3.3-70B, blue vectors). We include instructions requesting changes to reading difficulty (x-axis) but not formality (y-axis), such that **vertical movement is a side effect**. Figure 3 shows a 'current' from the lower left (informal & easy to read) to the top right, suggesting that, **when asked to increase reading difficulty without direction on formality, LLMs still increase formality**."

> "We also conduct a preliminary study of coupling between goal dimensions, which suggests that **the entanglement is LLM-induced**. While harder-to-read texts are often more formal, **they need not be under our chosen measurement functions** (Flesch-Kincaid grade, reading difficulty; Heylighen-Dewaele score, formality). LLM behavior appears to reflect this correlation: when stratifying steerability probe results based on whether the prompt requested **correlated** (e.g., make it harder to read and more formal) vs. **anti-correlated** changes (e.g., make it harder to read and *less* formal), **Llama3.3-70B is less steerable** [on anti-correlated requests]."

> "Figure 4: Median and IQR steerability, Llama3.3-70B, in correlated (darker) vs. anti-correlated (lighter) requests for change in reading difficulty and formality... **Llama3.3-70B struggles more with anti-correlated changes.**"

**This is our "changing shy also changes cruel" experiment, run on (reading difficulty, formality), with a control that establishes the entanglement is model-induced rather than definitional.** The correlated/anti-correlated stratification is a genuinely clever identification strategy and we should copy it wholesale: to prove trait entanglement is the *model's* and not the *concept's*, request anti-correlated trait pairs and show steerability drops.

## Interventions tried (verbatim)

> "As candidate interventions, we try **prompt engineering, which is ineffective**, and **best-of-N sampling, which requires extensive sampling** (Section 4.2). We then try **RL fine-tuning in 2D goal-space, which rivals best-of-128 and disentangles goals, but side effects remain** (Section 4.3)."

RL fine-tuning objective (verbatim, Eq. 6): `min_f E_(z0,z*)∼D E_ẑ∼f(·|z0,z*)[ŵ(z0,z*)·‖z*−ẑ‖²₂]`, optimized with leave-one-out PPO (LOOP), Llama3.1-8B via rank-stabilized LoRA.

**"Prompt engineering is ineffective" is the same null PsySET reports.** Two independent papers, two different constructs, same conclusion: you cannot fix prompt-space steerability with better prompts.

Models evaluated: GPT (3.5-turbo, 4-turbo, 4o, 4.1), Llama3–3.3 (8B/70B), DeepSeek-R1 distills (8B/70B), Qwen3 (4B/32B/30B-A3B), o1/o3-mini (appendix, "due to high response refusal/truncation rates").

Hygiene worth copying (verbatim): "we post-process responses to remove boilerplate text (e.g., 'Sure, here's...') and reasoning tokens (e.g., `<think>` blocks). We also filter refusals, degenerate behavior (e.g., repetitive looping), or rewrites unrelated to the source using LLM-as-judge and manual review" — with the filtering impact quantified: "rejected responses comprise ≤6 (≈0.29%) of outputs in any probe."

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**PARTIALLY — and it fully measures prompt-space crosstalk, which is the more damaging half.**

- Prompt-space dose axis: **WEAK YES** — "slightly/much" adverbs, 2 rungs, inside a target-tracking design
- Gain/elasticity error measured: **YES** — miscalibration = parallel component of steering error
- Off-diagonal crosstalk measured: **YES** — orthogonality metric + 2D vector flow + correlated/anti-correlated stratification
- Curve fitted over ≥3 dose rungs: **NO**
- Character traits: **NO** — rule-based text attributes only

## The surviving gap, stated honestly

Keyword census on raw extraction (verified counts): `slope` **0**, `dose` **0**, `intensity` **0**, `crosstalk` **0**, `off-diagonal` **0**, `matrix` **0**, `undershoot` **0**, `overshoot` **0**. `side effect` 34, `miscalibrat` 24, `steerability` 99, `entangl` 11.

1. **No dose-response curve.** This is a **single-shot target-tracking** design: one prompt, one target z*, measure the gap. It is not "sweep the dose over k rungs and fit the response." Zero occurrences of "dose", "slope", "intensity". Miscalibration is an *error magnitude*, not a *gain estimate*: it says the model missed, not how much output moves per unit of prompt emphasis.
2. **Two rungs is not a ladder.** "slightly/much" cannot identify curve shape.
3. **No trait × trait matrix.** Zero occurrences of "matrix" or "off-diagonal". Entanglement is studied in a **2D subspace** (reading difficulty × formality), not as an N×N steerability matrix over named traits. The flow diagram is a beautiful 2-D visualization that does not generalize to a matrix as-is.
4. **Text attributes, not persona traits** — and this is a *deliberate* scoping choice, which means the authors would likely regard the trait version as the harder open problem rather than as already-done.
5. **Single-turn text rewriting**, not multi-turn roleplay.

## Relevance to companion-eval-platform

1. **This is the closest formal framework to ours and we should adopt its geometry rather than reinvent it.** `steering error = miscalibration ⊕ orthogonality` is a cleaner decomposition than our informal "slope + crosstalk" and it is already peer-reviewed. Our trait-space version: goal-space dims = trait scores from a judge; miscalibration = did shyness move as much as the adverb asked; orthogonality = did cruelty move when nobody asked.
2. **"Scaling fixes gain, not crosstalk" is the finding to try to replicate.** If entanglement is scale-invariant on text attributes, the prior should be that it is scale-invariant on traits. That makes the trait × trait matrix a *durable* product artifact rather than something the next model release erases — which matters a lot for whether this eval is worth building.
3. **Copy the correlated/anti-correlated identification strategy.** It is the rigorous answer to the obvious reviewer objection "shy and timid are *supposed* to move together, that's semantics not entanglement." Request anti-correlated trait pairs (e.g., "more shy AND more aggressive"); if steerability collapses, the coupling is in the model.
4. **The measurement-validity trade is our central design problem, and this paper shows both horns.** They chose rule-based dims to "disentangle the accuracy of goal measurement from steerability" — i.e., so that a bad number means bad steering, not a bad judge. We cannot do that for "shy". **Therefore the first thing our project must produce is not an elasticity curve but a validated trait-scorer with a known reliability.** Without it, every slope we report is confounded with judge noise and unfalsifiable. This reorders our roadmap.
5. **Two independent nulls on prompt engineering** (this paper + PsySET) mean "just write a better system prompt" is a dead intervention. Best-of-N works but is costly; RL works but side effects persist. For a companion product, best-of-N against a trait scorer may be the *only* shippable lever — and that is a concrete, testable product hypothesis.
6. **Related:** `bigtech-psyset.md` (trait/emotion intensity ladder; also finds prompting flat), `bigtech-prompt-steerability.md` (IBM; disclaims exactly the joint steerability this paper does), `bigtech-persona-vectors.md` (activation-space equivalents), `game-ifeval.md` (the same verifiability-vs-richness trade).
