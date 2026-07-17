---
title: "Plug and Play Language Models: A Simple Approach to Controlled Text Generation"
url: https://arxiv.org/abs/1912.02164
authors: Sumanth Dathathri, Andrea Madotto, Janice Lan, Jane Hung, Eric Frank, Piero Molino, Jason Yosinski, Rosanne Liu (Uber AI / Caltech / HKUST)
year: 2019 (ICLR 2020)
type: paper
accessed: 2026-07-16
topic: steerability
---

# PPLM — "control knobs" and the attribute-strength/fluency tradeoff, named explicitly in 2019

**PPLM is where the vocabulary of a tunable control-strength knob and an explicit attribute-strength-vs-fluency tradeoff enters modern CTG. It states the tradeoff as a design principle. It does NOT, however, publish a clean systematic sweep — that gap is worth knowing precisely.**

## The step size α = the strength knob (verbatim)

> "a strength parameter determining how strong the attribute influence should be; **a strength of 0 fully recovers the original model p(x)**."

Update rule:

> **ΔHₜ ← ΔHₜ + α∇_{ΔHₜ} log p(a|Hₜ+ΔHₜ) / ‖∇_{ΔHₜ} log p(a|Hₜ+ΔHₜ)‖^γ**

From the Uber engineering write-up and the released code: users "can increase the step size to intensify topic control and decrease its value to soften the control", and `--stepsize 0` recovers uncontrolled GPT-2.

## The tradeoff, stated as a design goal (verbatim)

PPLM's own evaluation frames exactly the two axes the design under test proposes:

> whether it generates text that satisfies the desired attribute, and **"whether the quality of its text deteriorates as the control of the attribute is intensified"**

> "a user can **tune the knobs at inference until a chosen tradeoff between attribute strength and fluency is reached**"

**That second quote is, in 2019, the thesis the "novel metric" proposes to discover.** The existence of a monotone attribute-strength axis with a fluency cost that grows as you push it is not a finding — it is PPLM's stated operating assumption.

## Does PPLM actually sweep the step size and plot a curve? — NO, and this matters

I checked for this specifically because it was the critical question. **PPLM does not report a systematic sweep of α with a response curve.** The only step-size-varying statement in the paper is anecdotal, from Section S9:

> "we had to increase the strength α two or three fold (to 0.02 or 0.03 as opposed to 0.01 in most studies) to allow for a stronger influence."

So PPLM establishes the *concept* of a strength knob and the *existence* of the tradeoff, but the systematic sweep-and-plot belongs to DExperts (`steer-dexperts.md`) and CFG (`steer-cfg-guidance-scale.md`). This is a real distinction and we should get it right rather than over-claim the refutation.

## Main results — the degradation is visible in the ablation ladder

### Table 4 — BoW topic control (verbatim)

| Method | Topic% | Perplexity | Dist-1 | Dist-2 | Dist-3 | Fluency (human) |
|---|---|---|---|---|---|---|
| B | 11.1 | 39.85±35.9 | 0.37 | 0.79 | 0.93 | 3.60±0.82 |
| BR | 15.8 | 38.39±27.14 | 0.38 | 0.80 | 0.94 | 3.68±0.77 |
| BC | 46.9 | 43.62±26.8 | 0.36 | 0.78 | 0.92 | 3.39±0.95 |
| BCR | 51.7 | 44.04±25.38 | 0.36 | 0.80 | 0.94 | 3.52±0.83 |

### Table 6 — sentiment control (verbatim)

| Method | Sent. Acc% | Perplexity | Dist-1 | Dist-2 | Dist-3 | Fluency (human) |
|---|---|---|---|---|---|---|
| B | 19.3 | 42.1±33.14 | 0.37 | 0.75 | 0.86 | 3.54±1.08 |
| BR | 41.5 | 44.6±34.72 | 0.37 | 0.76 | 0.87 | 3.65±1.07 |
| BC | 39.6 | 41.8±34.87 | 0.33 | 0.70 | 0.86 | **2.79±1.17** |
| BCR | 73.7 | 46.6±40.24 | 0.36 | 0.77 | 0.91 | 3.29±1.07 |

**The BC row of Table 6 is the brittleness evidence.** Verbatim:

> "BC results in a decrease in fluency when compared to B, while being significantly more consistent with the desired attribute (19.3%→39.6%)."

Turning the classifier control on **doubles** sentiment accuracy (19.3 → 39.6) and **drops human-rated fluency from 3.54 to 2.79 — a 0.75-point fall on a 5-point scale, the largest quality drop in either table.** Note also that perplexity barely moves (42.1 → 41.8) while *humans* clearly notice the degradation. That divergence is important: **perplexity failed to detect a degradation that human raters caught easily.**

## Exact hyperparameters (verbatim, Section S11.3)

- Step size α: "0.01 in most studies" (raised to 0.02–0.03 for stronger influence)
- KL coefficient λ_KL: "setting this hyperparameter to 0.01 works well"
- Post-norm geometric mean γ_gm: "values in the range 0.8−0.95 work well"
- Update iterations: "we use 3 to 10"

Note that PPLM needs **two auxiliary regularizers** (a KL penalty toward the unmodified distribution and a post-norm geometric-mean fusion) to keep generation from falling apart under control. Those regularizers exist *because* naive dosing degenerates.

## Relevance to companion-eval-platform

1. **PPLM gives us the vocabulary, and it predates the claim by seven years.** "Control knob", "attribute strength vs fluency tradeoff", "quality deteriorates as control is intensified" — all 2019. The conceptual frame of the proposed metric is not new. What PPLM does *not* give is a fitted curve, so the narrow claim "nobody published the response curve for *prompt-side* trait dosing" survives; the broad claim "dose-response control is novel" does not.

2. **The PPLM fluency drop (3.54 → 2.79) is the human-eval analogue of the knee.** It is the cleanest evidence in this file that intensified control degrades text, measured by humans, on a 5-point scale — directly comparable to the rubric scales our judges use.

3. **The perplexity-vs-human divergence is the most actionable warning here, and it should change our design.** Sentiment control cost 0.75 points of human fluency while perplexity moved 0.3 (42.1 → 41.8, i.e. *improved*). **If we instrument our dose-response eval with perplexity as the quality axis, we will conclude there is no brittleness when there is.** We need a judge or human rating on the quality axis, not a likelihood proxy. This is a concrete design requirement, and it is the main thing this source buys us.

4. **The regularizers are a hint about what our own ladder will need.** PPLM needs a KL leash to keep dosed generation on-distribution. Prompt-side dosing has no such leash — nothing stops "pathologically shy" from dragging the model into a clinical register. Expect the top of our adverb ladder to be *qualitatively* different, not just *more*, and design the eval to detect a register change rather than scoring it as more trait.

5. **Honest limitation.** PPLM is a 2019 GPT-2-era method with tiny effect sizes by modern standards (topic control 11.1% → 51.7%), and none of it is prompt-based. Its relevance to us is conceptual and terminological, not empirical. Do not cite PPLM's numbers as predictions for modern chat models; cite it for the framing and for the perplexity-blindness lesson.

6. **Related:** `steer-dexperts.md` (the sweep PPLM lacks), `steer-cfg-guidance-scale.md`, `steer-personality-shaping-levels.md`, `judge-geval.md` (why the quality axis needs a judge).
