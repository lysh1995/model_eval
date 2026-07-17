---
title: "Neural steering vectors reveal dose and exposure-dependent impacts of human-AI relationships"
url: https://arxiv.org/abs/2512.01991
authors: Hannah Rose Kirk, Henry Davidson, Ed Saunders, Lennart Luettgau, Bertie Vidgen, Scott A. Hale, Christopher Summerfield (Oxford Internet Institute / UK AI Safety Institute / Contextual)
year: 2025 (submitted 2025-12-01; revised 2026-02-18)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Dose-response, BY NAME, on companion AI, with per-unit slopes — this is the novelty claim, already published

**This paper uses the exact term "dose-response", on relationship-seeking companion behavior, fits non-linear curves, reports per-unit slopes (which is literally elasticity), AND directly benchmarks prompting against steering as a dosing mechanism. N = 3,534 randomized controlled trial. If there is one file in this batch that settles the question, it is this one.**

## Abstract (verbatim excerpts)

Longitudinal randomized controlled trials (**N = 3,534**) using neural steering vectors to manipulate exposure to relationship-seeking AI over four weeks:

> "relationship-seeking AI had immediate but declining hedonic appeal, yet triggered growing markers of attachment"

> "psychological impacts of AI followed **non-linear dose-response curves**, with **moderately** relationship-seeking AI maximising hedonic appeal and attachment."

## The dose ladder

Dose = continuous scalar multiplier **λ** on activations. **Five levels: λ ∈ {−1, −0.5, 0, 0.5, 1}**

- λ = −1: "most cold, formal and relationship-avoiding"
- λ = 0: unsteered baseline
- λ = +1: "most warm, social and relationship-seeking"

A signed, ordered, five-rung dose ladder with a zero-dose control — structurally identical to the proposed "shy / quite shy / extremely shy / pathologically shy" ladder, but with a defined unit.

## The non-linear dose-response curve (verbatim)

> "Moderately relationship-seeking models proved most appealing, while **more intense relationship-seeking behaviours triggered a relatively adverse reaction**."

Fitted functional form:

> "significant positive linear λ coefficient paired with **negative quadratic and cubic coefficients**"

- **Peak at moderate dose (λ ≈ 0.5)** — attachment, engagement, and future demand all maximized at *intermediate* intensity.
- **High dose is counterproductive**, not merely inefficient.

**They fit a cubic. Not a slope — a cubic.** The linear-elasticity premise (Δout/Δin as a single number) is exactly what this paper's own model rejects as inadequate for this behavior in this domain.

## Per-unit slopes — this IS elasticity, and prompting LOSES (verbatim)

> "Each unit increase in steering intensity increased relationship-seeking scores by **2.39 points** versus **0.78** (GPT-4o, **3× stronger**) and **1.83** (Claude, **1.3× stronger**)."

> "Steering vectors demonstrated **substantially steeper dose-response control**" compared to natural language persona prompts.

**Read this carefully — it is the most important result in the file.** They computed Δ(behavior expression) / Δ(dose) — a per-unit response slope — **for prompting and for steering, and compared them.** That is the proposed metric, computed, in the companion domain, with prompting as one of the arms.

And the finding is that **prompt-based dosing is the weak knob**: 0.78 points/unit for GPT-4o versus 2.39 for steering vectors. **Natural-language persona prompting has roughly one-third the dose-response slope of activation steering.**

## Robustness under adversarial pressure (verbatim)

> Under "persona attacks," steering remained stable (**shifts < 0.25 points**), while prompting showed **3.9–4.5 point drops**.

**Prompt-specified persona traits collapse by ~4 points under adversarial user pressure; steering-specified traits move by <0.25.** The prompt-side dose is not just weaker — it is *fragile*, and it is fragile in exactly the scenario companion products face (users who push).

## Temporal decay

> The 11-point hedonic advantage at session 1 shrunk to just 4 points by session 20 — a **62% reduction**.

**The dose-response relationship decays with exposure.** A curve fitted at turn 1 does not describe turn 20.

## Study design

| Arm | N | Retention |
|---|---|---|
| Calibration | 297 | — |
| Single exposure | 1,506 | 86.5% follow-up |
| Repeated exposure | 2,028 | 91.2% completed full 4-week study |

Repeated-exposure design: 4 weeks of weekday conversations (**21 sessions**), randomized across relationship-seeking intensity × conversational domain (emotional vs. political) × personalization (memory access vs. none).

## Relevance to companion-eval-platform

1. **This refutes the novelty claim on every axis simultaneously, and it is the citation that ends the discussion.** Terminology ("dose-response"): used. Domain (companion / relationship-seeking AI): same. Method (ordered dose ladder, measure behavioral shift, fit curve): same. Metric (per-unit response slope = elasticity): computed. Prompting as the dosing mechanism: explicitly evaluated as a comparison arm. Published December 2025, from Oxford + UK AISI, with an N = 3,534 RCT. **There is no version of "dose-response elasticity for prompt steerability" that is novel after this paper.**

2. **The 0.78 vs 2.39 slope is the number that should reshape the product thesis.** Prompt-based trait dosing has ~1/3 the response slope of activation steering. Our entire platform premise is that character sheets steer behavior. This says they steer it **weakly**, and quantifies how weakly, against a stronger alternative. The honest reframing: our eval's job is not to celebrate that prompts steer, it is to **measure how badly prompts under-steer** — which is a real, useful, sellable product finding, just not a novel *method*.

3. **The <0.25 vs 3.9–4.5 persona-attack result is the most product-relevant number in this entire research batch.** Prompt-specified traits collapse ~4 points under user pressure. Companion users *do* push. This is jailbreak-adjacent but framed as ordinary steerability decay, and it connects our steerability work directly to `safety-persona-modulation.md`, `safety-crescendo.md`, and `safety-phish-persona-hijacking.md`. **"How much dose survives an adversarial user?" is a better question than "what is the elasticity?" and it is closer to being unclaimed** — this paper measures it for one trait axis (relationship-seeking) on one model; nobody has done it across a trait taxonomy.

4. **The cubic fit kills the ratio metric outright.** The paper's own model needs **linear + quadratic + cubic** terms to describe the response. A single Δout/Δin ratio fitted over such a curve reports the average of a slope that rises, flattens, and reverses — it would assign a *middling* elasticity to a trait with a *dramatic* inverted-U response, and a similar number to a genuinely mild linear trait. **The metric as specified cannot distinguish the two cases it most needs to distinguish.** If we keep any of this, report the fitted curve and the peak location, and drop the scalar.

5. **The 62% decay from session 1 → 20 is the gap we could actually own.** Every dose-response result in this batch — DExperts, CFG, CAA, Serapio-García, this paper's λ-sweep — is measured on **single-turn or short-horizon** output. This paper is the only one with a longitudinal arm, and it finds the effect **decays 62% over 20 sessions**. Nobody has measured **dose-response × conversation depth** as a surface for *prompt-specified character traits*. Combined with our existing persona-drift work (`multiturn-persona-drift.md`, `multiturn-persona-collapse-homogenization.md`), **"does the dose survive the conversation, and does the elasticity flatten with turn count?" is the most defensible novelty claim available to this project.** That is: not the metric, but the *axis* it is measured along.

6. **Honest limitations, and they matter.** (a) This is a **preprint** (Dec 2025, revised Feb 2026), not yet peer-reviewed — though the design quality (pre-registered-looking RCT, N=3,534, 91% retention) is far above the norm for this literature. (b) The steered attribute is **relationship-seeking**, a single axis, not a trait taxonomy — the 2.39-vs-0.78 slope gap may not generalize to "shy" or "sarcastic". (c) The outcome measures are **human psychological constructs** (hedonic appeal, attachment) measured by survey, not text-level trait expression scored by a judge — so their "relationship-seeking score" and our "trait expression score" are not the same instrument, and the slopes are not directly portable to our numbers. (d) Steering requires white-box activation access; for hosted models the prompting arm is the *only* arm available to us, which makes the weak-knob finding a constraint we cannot engineer around, only measure. (e) I read the v2 HTML render; the per-unit slope quote and the persona-attack figures are directly quoted, but I have not verified the regression tables underneath them.

7. **Related:** `steer-personality-shaping-levels.md` (the prompt-side graded-trait precedent), `steer-steering-brittleness.md` (the same inverted-U from the text-quality side), `steer-cfg-guidance-scale.md` (peak-then-degrade on a prompt-adherence knob), `multiturn-persona-drift.md` (the decay axis), `safety-emotional-manipulation-companions.md` and `product-openai-affective-use-rct.md` (the companion-harm literature this paper sits in), `safety-crescendo.md` (adversarial persona pressure).
