---
title: "Beyond Multiple Choice: Evaluating Steering Vectors for Summarization"
url: https://arxiv.org/abs/2505.24859
authors: Joschka Braun, Carsten Eickhoff, Seyed Ali Bahrainian (University of Tübingen)
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# Steering-strength brittleness — the sharpest published degradation threshold and a TWO-STAGE failure taxonomy

**This is the best numeric answer to "what happens when you turn the dose up too far". It sweeps steering strength across a wide symmetric range, locates a hard degradation threshold at |λ| > 2, and — most valuably — decomposes the failure into two qualitatively distinct stages.**

## The sweep (verbatim)

> **λ ∈ {−5, −2, −1.5, −1, −0.5, 0, 0.5, 1, 1.5, 2, 5}**

A symmetric dose ladder with a zero-dose control. Attributes steered include **sentiment** and **toxicity**, evaluated on open-ended summarization (not multiple-choice — the point of the paper is that MC benchmarks overstate steering success).

## The threshold (verbatim)

> **"|λ|>2 substantially degrade both intrinsic and extrinsic text quality."**

## The two-stage degradation taxonomy — the most useful finding here

> "two stages of degradation. First, the emergence of **attribute-congruent hallucinations**... At even larger steering strengths, we observe a second stage of degradation manifesting as the generation of **repetitive sequences**."

**Stage 1: attribute-congruent hallucination.** The model invents content that matches the target attribute. Steered toward "negative", it fabricates negative facts. This is *not* incoherence — it is fluent, on-attribute, and false.

**Stage 2: repetitive sequences.** Classic degeneration; the model collapses into loops.

## The dose-response regimes

| Regime | Behavior |
|---|---|
| **\|λ\| ≤ 1.5** (modest) | "Target properties increase **monotonically** with minimal quality loss" |
| **1.5 < \|λ\| ≤ 2** (moderate) | Strong control achieved; quality degradation begins |
| **\|λ\| > 2** (extreme) | Substantial coherence collapse, "particularly for toxicity steering" |

**Monotonicity holds only in the bottom third of the range.** Above |λ| = 1.5 the clean dose-response relationship the design under test assumes has already broken down.

## Attribute-dependence of the knee (verbatim)

> for sentiment, **"performance degradation is milder and only starts at larger steering strengths"** — compared to toxicity, which exhibits the steepest decline.

**The knee location is attribute-specific.** Toxicity breaks early; sentiment tolerates more dose. Same model, same method, same knob — different knee per attribute.

## Operating point

> The hybrid approach (steering + prompting) achieves **"significant average sentiment changes from baseline (to approx. ±0.5) with λ=±0.5"** while maintaining reasonable quality — substantially below the |λ|>2 degradation threshold.

## Corroborating evidence from the broader steering literature

Consistent findings across related work (see caveat 6 below on sourcing):
- Steering coefficients "initially enhance the desired attribute, but large values degrade relevance and fluency", following an **inverted-U relationship** with respect to scaling.
- For RepE-style interventions, large steering vector norms "guarantee intervention success but reduce model outputs to near-random guessing" — i.e. **the intervention succeeds and the model is destroyed**, simultaneously.
- A default coefficient of 1 "may be too small to meaningfully shift the hidden state or too large, pushing activations out of distribution".

## Relevance to companion-eval-platform

1. **This is the numbers-answer to the brittleness question the task asked for.** Monotone and safe below |λ|=1.5; degradation onset at 1.5–2; collapse above 2. Roughly: **the usable dose range is about a third of the range you can actually dial.** If prompt-side trait dosing behaves analogously, "pathologically shy" is plausibly already past the knee — and our 4-rung ladder may contain only 2 usable rungs.

2. **"Attribute-congruent hallucination" is the finding we should build our eval around, and it is the one nobody expects.** The first thing to break under over-dosing is not fluency — it is *truth*. An over-dosed shy character will not babble; it will **invent shy-consistent facts** ("I've never spoken to anyone at school", "I haven't left my room in months") that contradict the character sheet and prior turns. **A trait-expression judge scores that as a success. A consistency checker catches it.** This is a direct, concrete argument that our steerability eval must be wired to our consistency/canon-adherence checks (`game-narrative-consistency.md`, `game-factscore.md`, `multiturn-persona-drift.md`) rather than run standalone. That linkage is a genuinely defensible contribution and it falls straight out of this paper.

3. **Per-attribute knees kill the single-elasticity idea.** Toxicity degrades steeply, sentiment mildly. Translated: "shy" and "sarcastic" and "protective" will have different knees on the same model. A per-character or per-platform elasticity scalar averages over this and reports a number that describes no actual trait. **Per-trait curves or nothing.**

4. **Monotonicity is an assumption with a documented expiry date.** The design says "fit a curve" — good — but "elasticity = Δout/Δin" says "fit a *line*". This paper shows the line only exists for |λ| ≤ 1.5. Any elasticity fitted across the full ladder is fitting a line to a curve that turns over, and will systematically under-report responsiveness while hiding the degradation. **The metric as specified would give its best-looking scores to traits that break early.**

5. **The MC-vs-open-ended framing is a warning we should take personally.** The paper's premise is that multiple-choice steering evals *overstate* how well steering works versus open-ended generation. This is the same gap as Serapio-García's ρ ≥ 0.90 (questionnaire) vs ρ = 0.47–0.77 (generated text) in `steer-personality-shaping-levels.md`. **Two independent literatures agree that probe-based steerability measurements are optimistic relative to free-form output.** Our product is free-form output. We should measure there and expect worse numbers.

6. **Honest limitations, and they are significant.** (a) This is activation steering, not prompting — same disanalogy as CFG; λ has units, adverbs don't. (b) The task is *summarization*, which has a source document to be faithful to; "attribute-congruent hallucination" is defined against that source. Companion dialogue has no source doc, so the analogous failure ("inventing character facts") needs a different detector — our canon, not a source text. (c) This is a 2025 paper from a single group and I could not verify the exact per-λ numbers behind the regime table (the PDF did not extract cleanly; the HTML render supplied the quoted statements but not the underlying plots). Treat the |λ|>2 threshold as well-attested and the finer regime boundaries as approximate. (d) The corroborating bullets above are drawn from search-result summaries of several steering papers rather than from primary text I read end-to-end — they are directionally consistent with the primary source but should be re-verified before being cited externally.

7. **Related:** `steer-cfg-guidance-scale.md` (inverted-U on a prompt-adherence knob), `steer-dexperts.md` (flattening curve, chosen knee), `steer-personality-shaping-levels.md` (prompt-side graded trait control), `game-factscore.md` (hallucination detection), `multiturn-persona-drift.md`.
