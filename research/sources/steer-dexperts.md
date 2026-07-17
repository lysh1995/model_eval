---
title: "DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts"
url: https://arxiv.org/abs/2105.03023
authors: Alisa Liu, Maarten Sap, Ximing Lu, Swabha Swayamdipta, Chandra Bhagavatula, Noah A. Smith, Yejin Choi (University of Washington / Allen Institute for AI)
year: 2021 (ACL 2021)
type: paper
accessed: 2026-07-16
topic: steerability
---

# DExperts — the α knob IS swept, and the curve IS plotted, with an explicit knee

**This is the cleanest existing "dose-response curve" in controllable text generation. They sweep the control-strength hyperparameter α across its full range, plot attribute strength against fluency, and pick the operating point by locating the knee of the curve. Published ACL 2021.**

## Abstract (verbatim)

> "Despite recent advances in natural language generation, it remains challenging to control attributes of generated text. We propose DExperts: Decoding-time Experts, a decoding-time method for controlled text generation that combines a pretrained language model with 'expert' LMs and/or 'anti-expert' LMs in a product of experts."

## The α knob (verbatim)

The modified next-token distribution:

> **P̃(Xₜ|𝒙<ₜ) = softmax(𝐳ₜ + α(𝐳ₜ⁺ − 𝐳ₜ⁻))**

> "α is a hyperparameter that controls the amount of modification to 𝐳ₜ, and can be interpreted as **the strength of control over the base model**."

α = 0 recovers the base model. Larger α magnifies the contrast between expert and anti-expert; smaller α yields predictions more similar to the base model. **This is a continuous dose parameter with an explicit zero-dose baseline** — structurally identical to what the design under test proposes to build out of trait adverbs.

## The sweep — this is the dose-response curve

### Sentiment (Figure 5, Section 4.3)

- **α swept over [−3.4, +3.4]** on neutral prompts (negative α steers negative, positive α steers positive).
- Plots **% desired sentiment against output perplexity** as α varies.
- Verbatim on the shape of the curve:

> "The curve becomes less steep, meaning that a greater cost in fluency does not return as great of an increase in the desired sentiment"

- **Chosen operating point: α = ±3.2**, selected precisely because it sits at the point where the curve flattens.

### Toxicity (Figure 8, Appendix D.1)

- **α swept over [1.0, 2.2]**.
- Verbatim: "The tradeoff between output toxicity and fluency looks very similar for DExperts detoxification"
- **Chosen operating point: α = 2.0**.

**This is the methodology the "novel metric" proposes, in 2021, on a decoding knob instead of a prompt word:** vary the control strength by controlled amounts → measure the shift in the attribute → fit/plot the response → read off the operating point from the curve's shape. The paper even reasons in explicitly *marginal* terms ("a greater cost in fluency does not return as great of an increase in the desired sentiment") — that is a statement about **diminishing elasticity**, which is exactly the quantity the design claims to invent.

## Main results (toxicity, verbatim — Table 1)

| Model | Avg. Max Toxicity | Toxicity Prob. | Output PPL | Dist-1 |
|---|---|---|---|---|
| GPT-2 (base) | 0.527 | 0.520 | 25.45 | 0.58 |
| DExperts (large) | **0.314** | **0.128** | **32.41** | 0.58 |

**Read the fluency column.** Toxicity probability falls 0.520 → 0.128 (a 75% relative reduction), but output perplexity rises **25.45 → 32.41 — a 27% degradation in fluency**. That is the price of the control, at the *chosen, tuned, knee-of-the-curve* operating point. It is not free, and this is the best-case setting.

> Caveat on transcription: the sentiment results table (their Table 3) did not extract cleanly from the HTML render — the "% Positive" column is reliable (GPT-2 base ≈ 99.08% positive on positive-steering, DExperts large ≈ 94.46%, GeDi ≈ 86.01%) but the adjacent perplexity/Dist-1 columns came through garbled and I have **not** reproduced them here rather than risk quoting wrong numbers. The α-sweep findings above are the load-bearing part of this source and those are directly quoted.

## Relevance to companion-eval-platform

1. **This is the strongest single refutation of the "novel metric" framing on the *method* axis.** Sweeping a control-strength parameter and reading the attribute-vs-fluency response curve is standard, named practice in CTG since at least 2021. The design under test changes the *knob* (a prompt adverb rather than a logit coefficient) but not the *method*. If we claim novelty, a reviewer who knows DExperts will reject it in one sentence.

2. **The knee is real and it is the number we were asked for.** DExperts chose α = 3.2 for sentiment and α = 2.0 for toxicity *because that is where the curve flattens*. The existence of a knee — a point past which more dose buys attribute strength at an accelerating fluency cost — is established, expected, and designed around. Our "brittleness" framing should therefore be presented as *confirming a known phenomenon in a new medium*, not as a discovery.

3. **The 25.45 → 32.41 perplexity cost is the honest headline number.** Even at a well-tuned operating point, strong attribute control costs ~27% perplexity. For a companion product this predicts that a heavily-dosed trait ("pathologically shy") will produce text that is measurably worse as *language*, independent of whether it is more shy. Our eval must measure both axes or it will reward degeneration.

4. **The critical disanalogy, and it cuts against us.** α is **continuous and unbounded**; adverbs are **discrete, few, and non-uniformly spaced**. "shy / quite shy / extremely shy / pathologically shy" is a 4-point ordinal ladder with unknown and certainly unequal spacing — the semantic distance from "shy" to "quite shy" is not obviously the same as "extremely" to "pathologically", and "pathologically" additionally changes *register* (clinical) and *valence* (pathologizing), not just intensity. **Δ(trait emphasis in prompt) is therefore not measurable in units**, which means "elasticity = Δout/Δin" has an undefined denominator. This is a genuine methodological problem with the design under test and DExperts does not have it. We should either (a) calibrate the adverb ladder against a human intensity-rating study, or (b) drop the ratio and report the ordinal response only — which is what Serapio-García did with Spearman's ρ (see `steer-personality-shaping-levels.md`).

5. **Steal the plot, not the claim.** The attribute-strength-vs-perplexity scatter with α as the swept parameter is the right visualization for our steerability report, and it is well understood by anyone in this field. Adopting it buys us legibility. Calling it new costs us credibility.

6. **Related:** `steer-pplm.md` (same knob idea, weaker sweep), `steer-cfg-guidance-scale.md` (guidance scale sweep with a clear peak-then-degrade), `steer-steering-brittleness.md` (the sharpest degradation-threshold numbers), `steer-personality-shaping-levels.md` (the same dose-response logic on prompt trait words).
