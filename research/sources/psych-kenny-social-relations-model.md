---
title: "The Social Relations Model (SRM) — interpersonal perception, consensus, and variance decomposition"
url: https://davidakenny.net/ip/srmip.htm
secondary_url: https://davidakenny.net/ip/consen.htm
tertiary_url: https://davidakenny.net/ip/fimp.htm
authors: David A. Kenny (SRM: Kenny & La Voie 1984; Kenny 1994; Kenny, Albright, Malloy & Kashy 1994, Psych Bulletin 116:245-258)
year: 1984-2023
type: method / theory / meta-analysis
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Kenny's Social Relations Model — the "chemistry" worry, quantified. It's worse than we said.

**The ability model worries in passing that "chemistry is a user×character×model interaction". The
SRM is a 40-year research program built to decompose exactly that variance, and it has the numbers.
The numbers say the interaction term is not a nuisance — in several constructs it is the LARGEST
component.**

---

## 1. The model

A judgment by perceiver *i* of target *j* decomposes into:

> "In the Social Relations Model, perceptions are separated into three components: **perceiver,
> target, and relationship**. The **perceiver effect** reflects how the person tends to see others;
> the **target effect** reflects how a person is seen in general by others; and the **relationship
> effect** reflects how a perceiver uniquely sees the target."

Kenny's plain-language form (iResearchNet):

> "P = constant + John's perceiver effect + Mary's target effect + relationship effect + error"

Standard notation (Kenny & La Voie 1984; the site defers the formal algebra to Appendix B of
*Interpersonal Perception: A Social Relations Analysis*):

```
X_ij = μ + α_i + β_j + γ_ij + ε_ij

  μ    grand mean
  α_i  perceiver (actor) effect     — how i sees everyone
  β_j  target (partner) effect      — how j is seen by everyone      → CONSENSUS
  γ_ij relationship effect          — how i uniquely sees j          → "CHEMISTRY"
  ε_ij error
```

**Design requirement — the round robin:**

> "Each person in the group rates or judges everyone else in the group. Most studies of interpersonal
> perception use this design"

⚠️ **Note the cost: γ_ij is only identified if you have replications** (two measures per dyad, or
multiple occasions). Otherwise relationship variance is confounded with error. **This is a hard
design constraint on us if we want to estimate the chemistry term at all.**

## 2. The variance numbers ★★★

### Consensus (= target variance / total variance)

> "Consensus ... is defined within the Social Relations Model as **the target variance divided by the
> total variance**."

> "The level of consensus is **fairly modest, ranging from about .20 at zero acquaintance to about
> .40 at long-term acquaintance**."

> Cleeton & Knight (1924): "The average level of consensus between two judges was **.20**, meaning
> that about twenty percent of variance is due to target."

**Read this against the ability model's agreement gradient.** §1 claims L1 is bound to the character
sheet ⇒ κ ≈ 0.78–0.94. **Kenny's meta-analytic answer for "how much do judges agree about what a
person is like" is 20–40% of variance — and that is the ceiling after long acquaintance.** These are
not the same statistic (κ on a discrete probe vs variance ratio on a trait rating), and our task is
easier in one specific way — our "target" is a *written sheet*, fully available to all judges, so
availability is maximal. But the direction of the discrepancy is stark and worth stating plainly:
**human beings, judging real people they know well, reach ~.40 consensus. We are projecting ~.9.**

### Which traits get consensus — the shape our κ should have

> "There is **more consensus for extraversion** than for the other Big Five factors."

> "Research has consistently shown that agreement at zero acquaintance is strongest for
> **Extroversion** ... Agreement is generally shown for ratings of **Conscientiousness**. Agreement
> for **Agreeableness, Emotional Stability, and Culture tend to be less**."

> **"traits that are more behavioral, external or observable show more consensus."**

> As for validity, "it seems to be greatest for **Conscientiousness**"

> When perceivers know targets well: "if perceivers are well acquainted with the targets, there is
> **not much difference in consensus between the Big Five traits**."

**This independently replicates Funder's "good trait" moderator and Connelly & Ones' trait×
relationship interaction** (see `psych-funder-realistic-accuracy-model.md`). Three separate
literatures agree: **agreement is a function of trait observability.** A single pooled L1 κ is
therefore a weighted average over a strongly heterogeneous set, and its value is an artifact of how
many observable vs internal traits we happened to probe. **Stratify or don't report it.**

Note the second quote is a genuine mitigation for us: with *full* acquaintance the trait differences
shrink. A character sheet is arguably "full acquaintance" — everything knowable is on the page. This
is the strongest argument that our situation is better than Kenny's. It's worth making, but it
predicts we land near **.40**, not .90.

### Relationship variance — the chemistry term

> "In the case of **liking**, about **10%–20%** of the variance can be attributed to **perceivers**,
> about the same amount to **targets**, and about **30%–40% to the unique perception**."

> "For trait ratings of the Big Five, about **40% of variance is due to relationship effects**."

> "previous SRM research has shown that **the variance of the individual level effects is lower than
> the variance of the dyad level effects**, and that **the perceiver variance is higher than the
> target variance**."

> "**Strong relationship effects make the case for uniqueness: A given person's perception of another
> person is idiosyncratic.**"

**Both of the ability model's fears are confirmed, and they compound:**

1. **The relationship (chemistry) term is the largest single component for liking (30–40%) and is
   ~40% for Big Five trait ratings.** It is not noise to be averaged away — it is the plurality of
   the variance. For a *companion* product, where "liking" is close to the actual outcome variable
   (Q1 real user preference), **SRM says ~30–40% of user preference is irreducibly dyad-specific.**
   No model-level scalar can capture it. That is a ceiling on the entire leaderboard concept, and it
   should be stated in BENCHMARKS.md as a structural limit, not a caveat.
2. **The perceiver term dominates the target term.** The ability model's open question 3 asks whether
   steerability predicts Q1. SRM's answer-shape: **a large share of Q1 is about the user, not the
   model.** Our "same baseline across models" is well-defined; "same baseline across *users*" is not
   achievable even in principle without a round-robin design.

### Metaperception — the perceiver term is overwhelming

> "The dominant SRM variance component in metaperception is the **perceiver effect**, usually
> accounting for **over 52 percent** of the total variance for **traits** and **35 percent** for
> **liking**."

(Metaperception = "how do I think you see me". Less directly relevant, but it's the extreme case of
perceiver dominance and worth knowing the number.)

### Stability — the chemistry term is large AND unstable ★

> "strong stability for the **target effect, r = .90**, but not nearly the same degree of stability
> for the **relationship effect, r = .40**"

**This is the most operationally important number in the file.** The consensual component is highly
stable (r=.90 — a great regression detector). The idiosyncratic component is **large (30–40% of
variance) and only r=.40 stable**. So the biggest chunk of preference variance is also the part that
*doesn't replicate*.

**Directly translated: any A/B test whose outcome is user preference is fighting a 30–40% variance
component with test-retest r≈.40.** That is a brutal power problem and it is *exactly* what note 04
§7 (sample sizing) and note 10 (noise floor) need to hear. It also independently justifies the
ability model's core strategic move — **isolate L3/preference at the end and measure the bound layers
separately** — because the bound layers live in the r=.90 target component and preference lives in
the r=.40 relationship component. **This is the best quantitative support for the framework's
architecture found anywhere in this cross-check.**

### One more useful number

> "making perceivers dependent on a target did in fact lead to **over 25% more relative target
> variance**"

Outcome dependence increases consensus. Model analogue: *give the judge a stake / a task that
requires getting the character right* and agreement rises. Cheap thing to try in probe design.

> "an average correlation of target effects between perceivers of two different classes is **.73**"

(Different *classes* of perceiver still agree about targets at .73. Encouraging for cross-model
agreement: **different model families should still converge on the target component** — which is
exactly what note 15 measures. Note 15's observed cross-model agreement of 0.052–0.466 is *far* below
.73, which suggests our characters are much harder targets than real people, or that our agreement
metric isn't measuring the target component cleanly.)

## 3. Consensus ≠ accuracy — the distinction we are eliding ★

SRM is careful about something the ability model currently is not. **Consensus (do judges agree?) and
accuracy (are they right?) are different parameters.** Kenny's PERSON model decomposes consensus
further:

> "consensus starts out at **.20 at zero acquaintance, all of which is due to S** and asymptotes at
> **.40, all of which is due to P**." (S = Stereotype; P = Personality)

**At zero acquaintance, 100% of the agreement between judges is driven by shared STEREOTYPE, not by
the target's actual personality.** Judges agree because they share priors, not because they're
reading the target.

**This is the sharpest single threat to the ability model's foundational argument.** Note 15's design
— all 11 models got identical character sheets, so cross-model divergence is "L1 variance made
visible for free" — **has this confound in it directly.** Cross-model *agreement* on a character
could be:
- (a) the models converging on what the sheet actually says ← what we want to conclude (P)
- (b) the models sharing a training-data stereotype about tsundere/goth/mentor archetypes ← **(S)**

**These are indistinguishable in note 15's current design**, and Kenny's number says that for
*unacquainted* judges the answer was **100% (b)**. Models are the most stereotype-saturated judges
imaginable — shared pretraining is literally shared priors. **The null hypothesis for note 15 should
be stereotype convergence, and it currently isn't.**

**Concrete fix, cheap:** score a *scrambled* or *archetype-only* sheet (strip the specifics, keep the
archetype label). If cross-model agreement barely drops, we were measuring S, not P. That is the
stereotype/personality separation, it costs one extra generation condition, and **it should gate the
note-15 line of work.** (This is the same instinct as `rp-bench-anonymous-benchmarking.md`'s finding
that anonymization degrades every model — note 01 §3 already flags canon-knowledge as a confound;
Kenny says the confound generalizes to *archetypes*, not just named characters.)

## 4. Verdict for the ability model

**CONFIRMS OUR FEARS, with numbers:**
- Relationship/chemistry variance is **30–40%** (liking; Big Five traits ≈40%) — **the largest single
  component**, not a nuisance term.
- **Perceiver variance > target variance.** The user matters more than the character. For
  metaperception the perceiver effect is **>52%**.
- Relationship effects are **unstable (r=.40)** while target effects are **stable (r=.90)** — the big
  component is the unreplicable one.

**SUPPORTS THE ARCHITECTURE:**
- The r=.90 target vs r=.40 relationship split is a strong quantitative argument for **measuring the
  bound/consensual layers separately and isolating preference at the end.** The framework's core
  strategic move is right, and this is the best evidence for it we found.
- .73 cross-class target agreement says cross-*model* convergence on the target component is a
  reasonable thing to expect and measure.

**BREAKS:**
- **κ ≈ 0.78–0.94 for L1 is not consistent with 40 years of consensus research** (.20→.40 variance).
  Different statistic, easier task (sheet is fully available) — but the gap needs an argument, not an
  assumption.
- **Consensus ≠ accuracy, and at low acquaintance consensus is 100% stereotype.** Note 15's
  cross-model agreement is confounded with shared pretraining priors. **Needs the archetype-only
  control condition before it can claim to measure L1.**
- Agreement varies by trait observability (replicating Funder). **A pooled L1 κ is an artifact of
  probe mix.**

**STEAL:**
1. **The variance decomposition itself.** `model` / `character` / `model×character` is a
   round-robin. We can fit an SRM *today* on the existing 11-model × 95-character corpus and get the
   actual size of our interaction term instead of worrying about it. **This is a zero-new-generation
   experiment and it directly answers the chemistry question.** Highest-value item here.
2. **Report consensus as target-variance/total-variance**, the SRM way, rather than as a κ. It's the
   right statistic for "do judges agree about this character", it's already what note 15 gestures at,
   and it makes our numbers comparable to a 40-year literature.
3. **The stereotype control** (archetype-only sheet) as a gate on note 15.
4. `TripleR` (R) / `srm` packages exist — don't hand-roll the estimator.
