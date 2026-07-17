---
title: "The reliability of difference/change scores — Cronbach & Furby (1970), Lord's paradox, and why Δoutput/Δprompt may be unmeasurable"
url: https://www.semanticscholar.org/paper/How-we-should-measure-%22change%22:-Or-should-we-Cronbach-Furby/fd841428d711c44b950f1e1c2c19b1441da99571
authors: Lee J. Cronbach & Lita Furby (1970); Frederic Lord (1956, 1963); Rogosa, Brandt & Zimowski (1982)
year: 1970
type: theory / paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Cronbach & Furby (1970), "How we should measure 'change' — or should we?", *Psychological Bulletin*, 74(1), 68–80

**Read this file before finalizing the steerability metric.** Our steerability score is a **difference score**: behaviour under prompt A minus behaviour under prompt B (Δoutput per Δprompt). Difference scores have a known, closed-form, ~70-year-old pathology: **the more reliable each measurement is, and the more the two conditions resemble each other, the LESS reliable their difference becomes.** This is not a small correction. Under plausible values for our setup, the reliability of the difference goes to **zero** while each individual measurement remains excellent.

This is the most concretely damaging item in the psychology cross-check, because it is arithmetic, not interpretation.

## THE FORMULA

For a difference score `D = X − Y` where X and Y are standardized (equal variances), the reliability of D is:

```
                r_xx + r_yy − 2·r_xy
    r_DD  =  ─────────────────────────
                    2·(1 − r_xy)
```

General form (unequal variances):

```
              σ²_x·r_xx + σ²_y·r_yy − 2·r_xy·σ_x·σ_y
    r_DD  =  ─────────────────────────────────────────
                  σ²_x + σ²_y − 2·r_xy·σ_x·σ_y
```

Where:
- **r_xx** = reliability of measure X (behaviour under prompt A)
- **r_yy** = reliability of measure Y (behaviour under prompt B)
- **r_xy** = **correlation between the two measures** ← the killer term
- σ_x, σ_y = standard deviations

The canonical statement of the problem:

> "It is widely believed that measures of gain, growth, or change, expressed as simple differences between pretest and posttest scores, are inherently unreliable. **The difference between two measures is generally less reliable than the individual measures themselves when the measures are highly correlated and have similar variance.**"

> "when dealing with differences observed between 2 scores, we are dealing with a variable of much lower reliability than we might guess."

## The arithmetic — why this is fatal, not annoying

The numerator subtracts `2·r_xy` (shared true variance cancels out of a difference). The denominator subtracts `2·r_xy` too, but the **error variance does not cancel — errors are independent, so they ADD.** As X and Y become more similar, you subtract away all the signal and keep all the noise.

**Worked table (computed, r_xx = r_yy):**

| r_xy (corr. between conditions) | r_DD @ rel=.80 | r_DD @ rel=.90 | r_DD @ rel=.95 |
|---|---|---|---|
| 0.00 | 0.800 | 0.900 | — |
| 0.30 | 0.714 | 0.857 | — |
| 0.50 | **0.600** | 0.800 | 0.900 |
| 0.60 | 0.500 | 0.750 | — |
| 0.70 | **0.333** | 0.667 | 0.833 |
| 0.80 | **0.000** | 0.500 | 0.750 |
| 0.85 | — | 0.333 | — |
| 0.90 | — | **0.000** | 0.500 |
| 0.95 | — | — | **0.000** |

**Read the diagonal. When `r_xy = r_xx = r_yy`, the reliability of the difference is EXACTLY ZERO.** Both measurements are individually excellent (.90!) and their difference is pure noise.

This is the trap in its purest form: **you cannot escape by measuring better.** Improving r_xx from .80 to .90 helps only if r_xy stays put — but in our design, making the measurement better and making the two prompt conditions more comparable tend to *both* push r_xy up. The metric fights itself.

### Why this bites us specifically and hard

A steerability perturbation is, by design, a **small, controlled edit to a prompt**. That is the *definition* of a high-r_xy manipulation:
- Same character sheet, same scenario, same model, same seed.
- One trait word swapped, or one instruction reworded.
- Output measured on the same rubric.

**Everything about good experimental control drives r_xy toward 1.0** — and the better our control, the closer r_DD gets to zero. The design virtue *is* the psychometric vice. A sloppier experiment (different scenarios, different characters) would have lower r_xy and a more "reliable" difference — for entirely the wrong reasons.

And note the interaction with our L1 claim: if L1 comprehension really is measurable at κ ≈ 0.78–0.94, **that high reliability does not buy us a reliable Δ.** It's the r_xy term that governs, and we haven't estimated it.

## Cronbach & Furby's actual conclusion — stronger than "be careful"

Their recommendation was not "adjust for it." It was closer to **abandon the difference score as a construct**:

> Cronbach "is widely recognized for describing raw score problems measuring change but abandoned this challenge to improve social research methodology by advising researchers to **'frame their questions in other ways'**."

The paper examines "procedures previously recommended by various authors for the estimation of 'change' scores, 'residual,' or 'basefree' measures of change, and other kinds of difference scores" — and finds the proposed fixes (residualized gain, base-free change) mostly don't rescue the situation; they change what's being measured. Cronbach & Furby's advice: **if you find yourself needing a change score, you have probably asked the wrong question.**

## The rebuttal — Rogosa et al. (this is a genuine, live defence)

We should not overstate the case. The Cronbach/Lord position has been substantially contested:

> "the arguments by psychometric authorities Lord and Cronbach and Furby that gain scores are unreliable **have been called into question** by more recent researchers like Rogosa, Brandt, & Zimowski and others, suggesting this remains an area of ongoing debate."

Rogosa, Brandt & Zimowski (1982), "A growth curve approach to the measurement of change," *Psychological Bulletin* — the key counterarguments:

1. **Low reliability ≠ bias.** The difference score is an *unbiased* estimator of true change. Unreliability attenuates correlations *involving* the difference; it does not make the mean difference wrong. **If we only want "does prompt A move the model more than prompt B on average?" — a group-mean comparison — the reliability of the individual difference score is largely irrelevant.** Statistical power for the mean effect depends on N and error variance, not on r_DD.
2. **r_DD is low precisely when true individual differences in change are small.** The formula isn't "punishing" you; it's correctly reporting that there is little between-unit variance in change to detect. If everything changes by the same amount, there *are* no reliable individual differences in change — and that's a true fact about the world, not an artifact.
3. **The "paradox" is partly an artifact of the reliability framework itself** (a ratio of true to observed variance), which behaves badly when true variance is near zero. Growth-curve / multilevel models sidestep it.

Also relevant: "On the relation between power and reliability of difference scores" (2004) — a low r_DD does **not** automatically mean low power to detect a mean change.

**The synthesis that actually applies to us:**

| What we want to claim | Is r_DD a threat? |
|---|---|
| "Prompt style A moves models more than style B, on average" | **No** — mean difference is unbiased; power depends on N. |
| "Model M is *more steerable than* model N" | **YES** — this is a correlate of a difference score. |
| "Character C is harder to steer than character D" | **YES** — same problem. |
| "Steerability predicts downstream quality" | **YES, badly** — correlating a difference score with anything is exactly the attenuated case. |
| "Here is a steerability matrix M[i,j] with interpretable cells" | **YES** — every cell is an individual-level difference score. |

**Our framework wants the bottom four.** That is precisely the set the formula attacks.

## Implications for our framework

1. **The steerability matrix is a matrix of difference scores, and we have never estimated r_xy.** Every cell M[i,j] = (behaviour with trait i perturbed) − (behaviour baseline). Before building anything: **empirically estimate r_xy between the paired conditions.** This is one cheap experiment. If r_xy ≈ 0.85 and our rubric reliability is ≈ 0.85, then **r_DD ≈ 0 and the matrix is a noise generator** — every cell, every model, permanently. That is a go/no-go gate and it costs one afternoon. Run it before writing the harness, not after.

2. **The cruel irony: our control is the problem.** Same seed, same scenario, same character, one word changed — that is an r_xy-maximizing design. We are being punished *for* good experimental hygiene. This is not a reason to loosen control (that would trade a known problem for a worse one); it's a reason to **stop treating per-cell differences as the unit of analysis.**

3. **Reframe the claims to the ones that survive.** Rogosa's defence is real and it points somewhere specific: **mean-level claims are fine; individual-difference-in-change claims are not.** So:
   - ✅ Keep: "averaged over characters, perturbation class P produces larger behavioural shifts than class Q" (N is our friend; we can run thousands).
   - ❌ Drop or heavily caveat: per-model steerability *rankings*, per-character steerability *scores*, and any correlation of steerability with anything else.
   - This is a real narrowing of the framework's promise, and it should be written into the spec explicitly.

4. **Use the modeling escape hatch, not the difference score.** Rogosa's constructive answer is growth-curve/multilevel modelling. Ours is the analogue: **fit a hierarchical model with prompt-condition as a fixed effect and character/model as random effects, and read the variance components** — rather than computing Δ per cell and treating the Δs as data. This also directly serves the Cronbach variance-decomposition gate in `psych-cronbach-ati.md`. **One model, two problems solved.** Strong recommendation: this should be the default analysis, and the "steerability matrix" should be a *derived visualization* of a fitted model, not a table of raw differences.

5. **Cronbach's advice, taken seriously: "frame their questions in other ways."** Note that Cronbach is the author of *both* the ATI hall-of-mirrors retraction and the change-score critique. Our steerability construct manages to be a difference score **and** an ATI simultaneously. It is standing in the exact intersection of the two things Cronbach spent his late career warning about. If there is a way to specify what we care about that is not "Δoutput/Δprompt" — e.g. *absolute* in-character adherence under each prompt condition scored on a common instrument, compared as levels rather than differences — that formulation dodges both problems at once and should be seriously costed before we commit to the difference.
