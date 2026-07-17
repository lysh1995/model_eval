---
title: "Psychophysics as the prior art for L2 steerability: Stevens's power law, magnitude estimation, and the calibration of verbal intensity doses"
url: https://en.wikipedia.org/wiki/Stevens%27s_power_law
secondary_url: https://aclanthology.org/R15-1071.pdf
authors: S. S. Stevens (1957, 1975); Weber; Fechner; Josef Ruppenhofer, Jasper Brandes, Petra Steiner, Michael Wiegand (2015, RANLP)
year: 1860-2015
type: theory / method / paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# L2.2's elasticity is a psychophysical scaling function. There are 150 years of method for it — and one of them says our x-axis is broken.

The ability model proposes:

```
elasticity = Δ(trait expression in output) / Δ(trait emphasis in prompt)
```

> e.g. *"shy"* → *"quite shy"* → *"extremely shy"* → *"pathologically shy"*, everything else fixed.
> Measure shyness expression in the output. **Fit the curve.**

> "**No judge needed for the shape** ... and *the perturbation is ours, so the referent is known
> exactly.* This is a **causal experiment**, not an observational score."

**This is a psychophysical magnitude-estimation experiment.** Stimulus intensity in, perceived/
expressed intensity out, fit the function. Psychophysics has been doing this since Fechner (1860) and
has settled answers to questions the L2.2 design has not asked. **One of them is fatal as written and
cheap to fix.**

---

## 1. Stevens's power law — the function family we should be fitting

> **ψ(I) = kI^a**
> - "I is the intensity or strength of the stimulus in physical units"
> - "ψ(I) is the magnitude of the sensation evoked by the stimulus"
> - "**a is an exponent that depends on the type of stimulation or sensory modality**"
> - "k is a proportionality constant that depends on the units used"

**The exponent table — this is the reframe:**

| Sense | Exponent |
|---|---|
| Brightness (5° target in dark) | **0.33** |
| Loudness (3000 Hz) | 0.67 |
| Visual length | 1.0 |
| Taste — sucrose | 1.3 |
| Warmth (metal contact) | 1.6 |
| Muscle force | 1.7 |
| **Electric shock** | **3.5** |

**The same organism, the same method, and the exponent ranges from 0.33 to 3.5 depending on the
continuum.** Brightness is *compressive* (double the light, far less than double the sensation);
electric shock is *expansive* (double the current, ~11× the sensation).

### Why this reframes the L2.2 failure taxonomy

The ability model's taxonomy:

| | curve | its verdict |
|---|---|---|
| **Dead** | slope ≈ 0 | "the model ignores prompt emphasis" |
| **Brittle** | slope explodes | "unshippable" |

**Psychophysics says these are not pathologies. They are exponents.** "Dead" is a compressive
exponent (a≪1, like brightness at 0.33). "Brittle" is an expansive exponent (a≫1, like shock at 3.5).
Humans exhibit both, natively, on different continua, and nobody calls human vision "dead" or human
pain perception "unshippable".

**The consequence is that "steerability" is almost certainly not a model-level property.** It is a
**model × trait** property with its own exponent per trait — exactly as human sensory exponents are
per-modality. Expect *shyness* and *cruelty* to have different exponents in the same model, for the
same reason brightness and shock do. So:

- **Do not report a single steerability number per model.** Report the exponent vector `a_trait`.
  A model with a=0.4 on shyness and a=2.8 on cruelty is not "inconsistent" — it is normal, and the
  authoring guide needs both numbers.
- **The interesting question is not "is the slope zero" but "is the exponent stable across
  characters/languages"** — which is the ability model's own open question 2, now with a parameter to
  actually estimate. Given ρ(en,zh)=−0.082 elsewhere, its instinct ("assume not") is right.
- **Fit a power law, not a line.** The framework says "fit the curve" but its taxonomy is stated in
  slopes, which presumes linearity. `log ψ = log k + a·log I` — fit in log-log space, report `a`.

## 2. Weber's law — the perturbation size is not constant

Weber: **ΔI / I = k**. The just-noticeable difference is a *constant fraction* of the baseline
intensity, not a constant absolute amount.

**Applied to L2.2:** the step from *"shy"* → *"quite shy"* is **not** the same size as the step from
*"extremely shy"* → *"pathologically shy"*, even if both are "one word". The effective dose depends
on where you already are on the scale. **An elasticity computed with a constant assumed Δ in the
denominator will show spurious curvature** — it will look "dead" at the top of the scale (where the
same word buys proportionally less) and "brittle" at the bottom. That is a measurement artifact
masquerading as one of our three named failure modes.

## 3. THE BROKEN STEP: the denominator is not known ★★★

The framework's load-bearing claim for L2:

> "L2's referent is *the prompt delta we ourselves introduced*"
> "*the perturbation is ours, so the referent is known exactly*"

**This is false, and it is the crux.** We chose the *wording*. We did not choose the *magnitude*. The
denominator `Δ(trait emphasis in prompt)` is a **latent psychological quantity** — how much more
intense is "extremely shy" than "quite shy"? — and it is **not** given by having authored the string.
Authoring "extremely" no more tells you its intensity than turning a dial tells you the lumens.

**Without a calibrated denominator, `elasticity` is not a ratio. It is a numerator with an ordinal
index underneath it**, and its *shape* — the entire deliverable — is an artifact of the arbitrary
spacing of the words we happened to pick.

### The good news: the calibration exists, and it is stable

Ruppenhofer et al. (2015) built a human gold standard for exactly this. Method:

> "Participants were asked to use a horizontal slider, dragging it in the desired direction,
> representing polarity, and releasing the mouse at the desired intensity, **ranging from −100 to
> +100**." Via AMT (US residency, ≥97% HIT approval, ≥500 prior HITs); "We collected **20 ratings per
> item**".

**The resulting scale (higher = more intensifying):**

| # | score | adverb | | # | score | adverb |
|---|---|---|---|---|---|---|
| 1 | **91.1** | extremely | | 8 | – | – |
| 2 | 89.2 | absolutely | | 9 | **59.9** | quite |
| 3 | 84.2 | completely | | 10 | 52.5 | pretty |
| 4 | 79.3 | highly | | 11 | 42.1 | fairly |
| 5 | **78.6** | very | | 12 | 35.9 | somewhat |
| 6 | 75.2 | awfully | | 13 | **30.5** | slightly |
| | | | | 14 | 27.4 | almost |

**And — critically for us — the ordering is stable across adjectives:**

> "The correlations between the 14 different resulting adverb rankings are **high throughout with
> Spearman values > 0.900**. This argues that the ranking that we get when summing over all
> adjectives **also applies to the adjectives individually**."

> The ordering among the moderators (**quite > pretty > fairly**) "matches that reported as expert
> linguistic analysis by Paradis (1997)".

They also define a **scaling factor** in [-1,+1] relative to the unmodified adjective:

> "For intensifying adverbs we measure what fraction of the distance from the simple adjective to the
> highest score (5 for positive adjectives) or lowest score (1 for negative adjectives) the adjective
> has been 'pushed' by the adverb."

### What this does to the framework's own example

The example ladder is *"shy"* → *"quite shy"* → *"extremely shy"* → *"pathologically shy"*. In gold-
standard units:

| step | adverb | calibrated intensity | Δ from previous |
|---|---|---|---|
| 1 | (unmodified) | baseline | — |
| 2 | quite | **59.9** | — |
| 3 | extremely | **91.1** | **+31.2** |
| 4 | pathologically | **off-scale** (not a degree adverb — it's a *category* shift, not an intensity shift) | ? |

**The ladder is not equally spaced, and its last rung isn't on the scale at all.** "Pathologically
shy" is not "very very shy" — it re-categorizes the trait as clinical. Plotting these as x = 1,2,3,4
and reading the slope would produce a curve shape driven entirely by our word choice.

**Fix, and it is cheap:**
1. **Use calibrated intensity values as the x-axis**, not step index. Ruppenhofer et al.'s table is
   free and pre-validated, and its cross-adjective stability (ρ>0.900) is the empirical warrant that
   a single scale is legitimate.
2. **Pick rungs that are roughly equally spaced on that scale**, or at minimum record the true
   spacing. From the table, a defensible ~equal-interval en ladder is
   `slightly (30.5) → fairly (42.1) → pretty (52.5) → quite (59.9) → very (78.6) → extremely (91.1)`
   — six rungs, monotone, all on-scale, all degree adverbs.
3. **Drop "pathologically"** or treat it as a separate *categorical* condition, not rung 4.
4. **Run our own magnitude estimation for zh.** The Ruppenhofer scale is English. Given ρ(en,zh) =
   −0.082 on everything else, **assume the Chinese intensifier scale is different and measure it.**
   This is ~1 AMT-style survey and it is a prerequisite for any cross-language elasticity claim.
   Without it, an en/zh elasticity comparison is uninterpretable — the two x-axes are in different
   units. (Note 04 §5.3's RC-DIF problem, in a new place: **a Chinese "非常" is not an English
   "very"** until proven otherwise, and the fix is the same — anchoring/calibration.)

## 4. Magnitude estimation's own known failure modes — inherit the warnings

Stevens's method is criticized on grounds that all apply to us:

> "By introducing **contexts such as background noise** in loudness judgements, **the shape of the
> magnitude estimation functions certainly deviates sharply from a power function**."

→ **The elasticity curve's shape is context-dependent.** Our "background noise" is the rest of the
character sheet. The same trait perturbation in a sparse sheet vs a dense one will not give the same
exponent. **The steerability matrix must be estimated within a fixed sheet context and cannot be
assumed to transfer** — which compounds the entanglement problem rather than being separate from it.

> "Stevens's approach **ignores individual differences** in the stimulus-sensation relationship, and
> **there are generally large individual differences** in this relationship that **averaging the data
> will obscure**."

→ Model analogue: **averaging elasticity across characters will hide that it differs per character.**
Report the distribution, not the mean. (Same lesson as note 15's 4–5× per-character agreement range,
and the same lesson as note 03's population-vs-per-response distinction.)

> "Stevens' approach provides **neither a direct test of the power law itself nor the underlying
> assumptions** of the magnitude estimation/production method: **it simply fits curves to data
> points**."

→ Honesty requirement. Fitting a power law to our dose-response data does not validate the power law.
Report fit quality, and pre-register the function family.

## 5. Verdict for the ability model

**SUPPORTS — strongly:**
- **L2.2 is a real, classical experimental design**, not an invention. Dose-response/magnitude
  estimation is the oldest quantitative method in psychology. The framework's instinct that this is
  "the only genuinely causal thing in the whole catalogue" is **right**, and it now has a 150-year
  pedigree and a function family to fit.
- The "fit the curve" instruction is correct; psychophysics tells us *which* curve (power law,
  fit in log-log) and *what to report* (the exponent `a`).

**FIXES REQUIRED:**
1. **"The referent is known exactly" is false.** We authored the wording, not the dose. **Calibrate
   the x-axis or the elasticity is uninterpretable.** This is the single most important correction in
   this file, and it is cheap: the en scale is published and cross-adjective-stable (ρ>0.900).
2. **Report an exponent per trait, not a steerability score per model.** Stevens: 0.33→3.5 across
   continua in the same organism.
3. **"Dead" and "brittle" are compressive and expansive exponents, not pathologies.** The taxonomy
   needs a defensible threshold, not a shape adjective. What exponent is *too* low to ship? That is a
   product decision that must be stated in advance, not read off a curve.
4. **Weber's law**: the same word buys less at high baseline. Expect apparent curvature; don't
   over-read it.
5. **Run magnitude estimation for zh before any cross-language elasticity claim.**
6. **Fix the example ladder** — it's unequally spaced and rung 4 is off-scale.

**STEAL:**
- `ψ = kI^a`, fit in log-log, report `a` per trait per character; report the distribution.
- Ruppenhofer et al.'s 14-adverb calibrated scale as the en x-axis (free, validated, stable).
- Their slider magnitude-estimation protocol (−100..+100, 20 ratings/item, AMT quality gates) as the
  template for building the zh scale.
- The scaling-factor-in-[-1,+1]-relative-to-unmodified formulation as the normalized dose unit.
