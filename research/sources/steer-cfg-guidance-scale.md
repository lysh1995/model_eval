---
title: "Stay on topic with Classifier-Free Guidance"
url: https://arxiv.org/abs/2306.17806
authors: Guillaume V. Sanchez, Honglu Fan, Alexander Spangher, Elad Levi, Pawan Sasanka Ammanamanchi, Stella Biderman (EleutherAI et al.)
year: 2023 (ICML 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Classifier-Free Guidance for LMs — a guidance-scale sweep with an explicit PEAK-THEN-DEGRADE curve

**This is the source with the clearest published brittleness knee on a prompt-adherence knob: sweep γ, performance rises, peaks at a specific value, then falls. The inverted-U is documented, not hypothesized.**

## The guidance equation (verbatim)

> **log P̂θ(wᵢ|wⱼ<ᵢ,c) = log Pθ(wᵢ|wⱼ<ᵢ) + γ(log Pθ(wᵢ|wᵢ<ⱼ,c) − log Pθ(wᵢ|wⱼ<ᵢ))**

γ is the **guidance strength**. γ = 1 is the ordinary conditional model (no guidance); γ > 1 over-weights the prompt/condition c relative to the unconditional distribution. **γ is a continuous dose on "how much the prompt matters"** — which is conceptually the closest existing knob to "how much does the trait word in the character sheet matter".

## The sweeps — dose-response curves with knees

### Assistant / system-prompt following (GPT4All)

- **γ ∈ {1, 2, 3, 4, 5, 6}**
- **"Clear peak at γ=3 with 75% of system-prompt following preference"**
- Human evaluation: **75% preference** for CFG-guided generation over baseline.

**This is the single most relevant number in the file: prompt-adherence peaks at γ=3 and declines at γ=4,5,6.** Pushing the "obey the system prompt" dial past the knee makes the model *worse at obeying the system prompt*. That is the brittleness result, on the system-prompt axis, which is exactly the axis a character sheet lives on.

### Code generation (HumanEval)

- **γ tested at 1.0, 1.1, 1.25, 1.5, 1.75, 2.0**
- Peak performance at lower values (γ ≤ 1.5) for pass@1
- Verbatim: **"Low CFG increases the pass@1 rate uniformly"** while **"high CFG leads to deterioration"**
- Verbatim: **"High CFG decreases performance on pass@k for large k values"**

### Chain-of-Thought (GSM8K) — the sharpest statement of the tradeoff

> "For small CFG values, using CFG increases the percentage of chains which end in a valid answer structure while increasing the model accuracy. **For large values the invalid percentage remains small but the accuracy drop.**"

Read carefully: at high γ the model still produces well-*formed* output (valid structure), but the output is *wrong*. **Surface compliance is retained while substance degrades.** For us: at a high trait dose, the character may still "sound shy" while the response stops being a good response.

### Diversity

The paper documents that excessive guidance reduces **diversity** and **creativity** (this is why pass@k falls at large k while pass@1 holds — the model collapses onto a single mode).

## Headline results (verbatim)

- LLaMA-7B achieved **81% on LAMBADA at γ=1.5**, outperforming PaLM-540B's **77.9%**
- **"A model using CFG can generally perform just as well as a model twice as large"**
- The authors note CFG requires **"tweaking and exploration"** as optimal γ varies by task

## Relevance to companion-eval-platform

1. **This is the numeric answer to "is there a known 'turn it up too far and it degenerates' result?" — yes, with a location.** γ peaks at **3** for system-prompt following and degrades above it; **γ ≤ 1.5** for code, deteriorating above. The knee exists, it is measurable, it has been published, and — critically — **it moves depending on the task** ("optimal values vary by task", requiring "tweaking and exploration"). That last point is the real finding for us: **there is no universal knee.** Which means a single "elasticity" number for a platform, or even for a model, is not a stable quantity.

2. **The inverted-U refutes the linear-elasticity premise directly.** "elasticity = Δ(trait expression)/Δ(trait emphasis)" presupposes a slope that is meaningful — but if the true curve is inverted-U, the slope is **positive, then zero, then negative**, and a single fitted elasticity is an average over a sign change. It would report ≈0 for a strongly-but-non-monotonically-responsive trait. **If we keep the metric, it must be a fitted curve with a reported peak location, not a scalar ratio.** This is the most important design consequence in this file.

3. **The GSM8K finding is the failure mode our judges will miss.** "Valid structure, wrong answer" at high dose = "still sounds shy, but the reply is bad". A rubric judge asked "how shy is this response?" will score the over-dosed response *high* and miss the degradation entirely. We need an independent quality/appropriateness axis scored by a different judge, and the trait-expression judge must not be allowed to double as the quality judge. (Compare `steer-pplm.md`, where perplexity missed a degradation humans caught — same lesson, different instrument.)

4. **The 75%-preference peak at γ=3 is a useful sanity anchor for effect sizes.** It tells us a well-tuned prompt-adherence intervention produces a large, human-visible effect. If our trait-dosing ladder produces effects much smaller than this, the likely explanation is that prompt-side adverbs are a *weak* knob compared to logit-space guidance — which would itself be a legitimate, publishable finding, and a more defensible one than "novel metric".

5. **Honest limitation — this is the big one for this source.** CFG is a **logit-space** intervention with a continuous, unbounded, well-defined scalar. Our proposal is a **prompt-space** intervention with ~4 discrete adverbs of unknown spacing. The mapping is analogical, not formal: there is no reason to expect "pathologically" ≈ some particular γ. So CFG cannot tell us *where* our knee is, only that knees are the norm and that we must look for one rather than assume monotonicity. Claiming CFG's numbers predict prompt-side behavior would be unsupported.

6. **Related:** `steer-dexperts.md` (α sweep, flattening curve), `steer-steering-brittleness.md` (|λ|>2 threshold, two-stage degradation), `steer-personality-shaping-levels.md` (prompt-side graded control), `game-sysbench.md` / `game-followbench.md` (system-prompt adherence under load).
