# 16 — Psychology cross-check: does the L1→L2→L3 cascade survive?

**Topic owner:** construct validity of [ABILITY-MODEL.md](../docs/ABILITY-MODEL.md)
**Date:** 2026-07-16
**Sources:** `research/sources/psych-*.md` (35 files)

**Scope:** the ability model claims roleplay quality decomposes into three causally ordered layers
(L1 comprehension → L2 application & steerability → L3 creativity), that failures cascade downward
never upward, and that L1/L2 are "bound" (→ high agreement) while L3 is perspectival. Psychology has
studied *understanding another person* and *portraying a character* for a century. This note asks
whether we are re-inventing a validated wheel, or building a square one.

---

## 0. Verdict in one page

**The cascade is a legitimate model form with a 30-year pedigree, and it is UNEXAMINED rather than
refuted — nobody has ever regressed portrayal quality on comprehension, in humans or models. What is
refuted is the framework's *justification*: "these layers are bound, therefore high-agreement,
therefore the ones to measure." Boundedness buys reliability, not validity, and the two come apart
violently. Three of the framework's specific metrics are also wrong in ways psychology can fix.**

| claim | verdict | evidence |
|---|---|---|
| Quality decomposes into ordered, **necessary**, multiplicative stages | ✅ **SUPPORTED — and not novel.** Funder's **Realistic Accuracy Model** (1995) is exactly this | [RAM](../sources/psych-funder-realistic-accuracy-model.md) |
| **"L1/L2 are bound ⇒ high agreement ⇒ they're the layers to measure"** | ❌ **REFUTED. The load-bearing error.** Faux Pas has scoring **ICC = .996** and correlates **−.029 to .135** with every other ToM task. EA has **α ≈ .90** and **r = .06** with its nearest neighbour | [ToM convergence](../sources/psych-tom-task-convergence.md), [Ickes](../sources/psych-empathic-accuracy-ickes.md) |
| The bound measure is the one worth gating on | ❌ **REFUTED where tested.** 6,138 clients: empathic accuracy "**virtually unrelated to outcomes**"; the *perspectival* measure predicts best (r=.28) | [Elliott](../sources/psych-elliott-empathy-outcome-meta.md) |
| L1 "comprehension" is one measurable thing | ❌ **REFUTED at the broad level** — parallel analysis returns a **zero-factor solution**. ✅ but **narrow constructs measure beautifully** (55% of variance within false-belief) | [ToM convergence](../sources/psych-tom-task-convergence.md) |
| **L1 gates L2 (understanding predicts portrayal)** | ⚠️ **UNEXAMINED — the study has never been run.** And **we plan to test it with the wrong statistic** (§2.3). Evidence that exists runs the *other* way: acting training → ToM gains, randomised | [acting-ToM](../sources/psych-goldstein-winner-acting-tom.md), [Meisner](../sources/psych-meisner-technique.md) |
| L2.1 "consistency of hold" | ❌ **WRONG, provably.** Signature stability is "**negatively related**" to cross-situational consistency. **The metric is anti-correlated with the construct** | [CAPS](../sources/psych-caps-behavioral-signatures.md), [Fleeson](../sources/psych-fleeson-whole-trait-density.md) |
| L2.2 trait crosstalk is "the killer" defect | ❌ **REFUTED. Crosstalk is how person perception works** (Asch 1946) — but ~half of ours will be judge halo | [Asch](../sources/psych-asch-impression-formation.md), [halo](../sources/psych-halo-effect.md) |
| "the perturbation is ours, so the referent is known exactly" | ❌ **FALSE — cheaply fixable.** We chose the wording, not the dose | [psychophysics](../sources/psych-psychophysics-dose-scaling.md) |
| The steerability **matrix** is a well-defined object | ❌ **NO.** Asch Exp. IV: centrality is **not a trait property** — re-embed "warm" elsewhere and it becomes subsidiary. **Coefficients aren't stable, so M[i,j] isn't a matrix** | [Asch](../sources/psych-asch-impression-formation.md) |
| Elasticity (a **difference score**) is estimable | ❌ **The design defeats the estimator.** `r_DD → 0` exactly as `r_xy → r_xx`. **Our controls maximize `r_xy`** | [difference scores](../sources/psych-difference-score-reliability.md) |
| L1 agreement is uniformly κ ≈ 0.78–0.94 | ❌ **Direct counterexample in our exact condition** — 8 raters × 4 **movie characters**: ICC **.88 → .05**, an **18× spread** | [rating portrayal](../sources/psych-rating-character-portrayal.md) |
| L2.3 sheet-position effects are untested | ❌ **Tested in 1946.** Asch's primacy effect — swings up to **55 points** | [Asch](../sources/psych-asch-impression-formation.md) |
| "Chemistry is a user×character×model interaction" (a worry) | ✅ **CONFIRMED, worse than stated.** The **largest** component (30–40%) and the **least stable** (r=.40) | [Kenny SRM](../sources/psych-kenny-social-relations-model.md) |
| Isolate the perspectival layer at the end | ✅ **SUPPORTED** — target effects r=.90, relationship effects r=.40 | [Kenny SRM](../sources/psych-kenny-social-relations-model.md) |

**One sentence:** *the cascade may well be true, nobody has tested it, our planned test would fail to
detect it even if it were true — and the argument we're using to justify it is the one thing here
that is definitely wrong.*

---

## 1. What psychology SUPPORTS

### 1.1 The cascade form is legitimate — and has a name

**Funder's Realistic Accuracy Model (Psych Review, 1995)** decomposes accurate person-judgment into
relevance → availability → detection → utilization, and its structural claim is ours, stated harder:

> "Within the RAM, these stages are all described as **necessary**, which means that **if any stage
> is unsuccessful, an accurate judgment is not possible**."
> "The stages are also **multiplicative** ... the level of accuracy ... could theoretically be
> determined by **multiplying the levels of success for each stage**."

**"Failures cascade downward, never upward" is a respectable, 30-year-old model form. Cite RAM; stop
presenting it as our invention.**

### 1.2 The architecture's core move — isolate preference at the end — is right

Kenny's SRM stability numbers are the best support the framework has:

> "strong stability for the **target effect, r = .90**, but not nearly the same degree of stability
> for the **relationship effect, r = .40**"

The consensual/bound component is a great regression detector. The preference component is large and
barely replicates. **Measuring the bound layers separately and refusing to smear preference across
every metric is correct, and this is the number that justifies it.**

### 1.3 L1.2's discrimination/generation gap is real — and both off-diagonal cells are populated

- **Motivated inaccuracy** (Simpson et al. 1995): dating partners — normally ~50% *more* accurate than
  strangers — fell to "**significantly worse than that of total strangers and not significantly
  greater than chance**" when accuracy was threatening. Capability intact, performance collapsed.
  **That is L1.2 row 2 in humans.**
- **Recognition vs inference are dissociable competences**, Bayesian evidence *for* the null
  (BF01 = 29.82–124.98): "**pattern matching**" vs "**perspective taking** using context information".
  **That is L1.2 row 4.**
- **Strachan et al. (Nature Hum Behav 2024, N=1,907 humans) populated both cells in one study.**
  GPT-4's faux-pas deficit (p=5.42×10⁻⁵) **vanished to perfect performance** when asked "*is it more
  likely they knew?*" — **hyperconservatism, not failed inference** (row 2: knows better than it
  acts). LLaMA2 scored **100% via a bias toward attributing ignorance** (row 4: right answer, no
  comprehension).

**L1.2 is the best-motivated design in the ability model.** Keep it. But its causes are not the three
cheap ones listed (§3.2), and note what Strachan implies: **our probes see performance; the cascade
is a claim about competence.**

### 1.4 L2.2 dose-response is the oldest quantitative method in psychology

It's **psychophysics** — Fechner 1860, Stevens 1957. We should fit `ψ = kI^a` in log-log and report
the exponent. §4.4.

### 1.5 Authoring is a real lever — RAM says so structurally

RAM's first two stages — **relevance** and **availability** — are properties of the **target**. The
character sheet is the target. **If the sheet specifies nothing relevant to a trait, no model can be
accurate about it, and that is not a model defect.** RAM's **good information** moderator:

> "**Information quantity** ... referred to as the **acquaintanceship effect**"
> "**Information quality** ... Highly useful information includes information about **general and
> specific behaviors, and thoughts and feelings**."

**ABILITY-MODEL §5 calls this "*if the hypothesis holds*". RAM says it's two of the four stages with
30 years of support.** [Note 15](15-l1-convergent-reading.md)'s underpowered result (en +0.324,
zh +0.274) *is* the acquaintanceship effect — RAM is the prior that makes it worth powering rather
than dropping at p=0.07. And information *quality* hands us the "house style guide" deliverable as a
**pre-registered prediction**: behaviours, thoughts, feelings.

---

## 2. What psychology CONTRADICTS

### 2.1 ★ THE BIG ONE: bound ⇏ valid

ABILITY-MODEL §1:

> "**L1 and L2 are bound.** ... So **the two layers that gate everything are exactly the two we can
> measure with high agreement** ... it doesn't just say what to measure, it **explains why most of it
> is measurable.**"

**The inference from "bound" to "worth measuring" is severed at the last arrow, repeatedly:**

| measure | reliability | convergence with its nearest neighbour |
|---|---|---|
| **Faux Pas Recognition** | **scoring ICC = .996** | **−.029 to .135** with every other ToM task |
| Empathic accuracy | **α ≈ .90** | **r = .06** with the Interpersonal Perception Task |
| EA ↔ emotion recognition | both high | **BF01 = 29.82–124.98 FOR the null** |
| RMET | multiple-choice against a key | **α = .73**; ~15% shared variance with other ToM (ρ=.39) — *less than* with emotion perception (ρ=.48); correlates with **vocabulary at ρ=.32** |
| ToM tasks ↔ each other (adults, N=222) | — | all r ∈ **[−.115, +.125]**; RMET ↔ higher-order ToM = **−.069** |

**Warnell & Redcay (2019) ran parallel analysis on five ToM tasks and got a ZERO-FACTOR SOLUTION** —
the tasks share no common variance distinguishable from noise. They increased N specifically to rule
out low power; Bayesian analyses favoured the null 2–6×.

**Faux Pas is the cleanest statement available anywhere: ICC = .996 and r ≈ 0.** Perfect rater
agreement. Zero convergent validity. **Boundedness buys agreement about the scoring. It says nothing
about whether the thing scored exists.**

Note 04 §2.5 has the attenuation ceiling `√(ρ_xx'·ρ_yy')`. **This is worse than attenuation:** with
ρ≈.99 and ρ≈.90, the *permitted* correlation is ≈.94 and the observed is ≈.06. **That is two
different constructs wearing the same name.**

**⚠️ But the framework has a real escape, and it's the most useful thing in this section.**
Narrow constructs measure *beautifully*: Wellman/Cross/Watson (178 studies) explain **55% of the
variance** within false-belief; Devine & Hughes (460 children) recovered a **single latent factor**
with strong test-retest and no DIF across gender/ethnicity/SES. **Coherence is strong *within* a
paradigm (ρ > .36) and absent *between* paradigms.**

> **We can have a narrow L1 that measures well, or a broad L1 that means what we intend. Not both.**

That is a *choosable* trade-off, not a defeat — and choosing it explicitly is the fix (§5.2).

### 2.2 ★★ Where the bound measure has been checked against an outcome, it lost

**Elliott, Bohart, Watson & Murphy (2018), 82 samples, 6,138 clients** — the profession whose entire
job is understanding another mind:

> Overall empathy → outcome: **r = 0.28** (d = 0.58), "about **8%** of the difference in outcomes".
> "**Unlike other ways of measuring empathy, it was virtually unrelated to outcomes when measured as
> the degree to which client and therapist shared the same perceptions of what the client was feeling
> or thinking ('empathic accuracy').**"
> "**Rather than the perspectives of therapists or observers, clients' reports of therapist empathy
> best predict treatment outcome.**"

| | measure | agreement | predicts outcome? |
|---|---|---|---|
| **our L1** | empathic accuracy — bound, scored against the referent | **α ≈ .90** | **≈ 0** |
| **our L3** | client-perceived empathy — perspectival | low | **r = .28, best of any measure** |

**The framework's gradient sorts measurements by exactly the wrong key.** The analogy is tight —
therapist:client :: companion character:user — and "*the client's felt sense of being understood*" is
close to the companion product's whole value proposition.

**The framework's best defence is real:** Elliott's therapists are **range-restricted** (all cleared
a competence bar), and within a selected sample the selection variable stops predicting. Our models
are not range-restricted (note 01: LifeChoice human 92.01 vs best model 67.95). **So L1 may predict
in our range and flatten later.** But that concession converts L1 from *"the layer that gates
everything"* into *"a floor check that stops discriminating once models clear it."* **Much weaker —
and testable today** (§4.1).

### 2.3 ★★★ The cascade is UNEXAMINED — and our planned test would miss it even if it's true

**This is the most important methodological finding in the note, and it partly rescues the framework
from my own first draft.**

**(a) Nobody has ever run the study.** Goldstein & Winner, Brown, Konijn, and Dumas all measure
comprehension, brain activity, or personality *in actors*. **Not one regresses portrayal quality on
comprehension.** Dumas et al. — the largest actor study ever — used *union membership* as its skill
proxy and disclaims measuring ability. **The cascade's core claim is unexamined, not refuted.** If we
ran it, it would be a novel contribution.

**(b) ⚠️ A cascade predicts a TRIANGULAR SCATTERPLOT, so correlation is the wrong statistic.**

A necessity claim — *you cannot apply a character you didn't understand* — predicts:

```
   L2 ▲
      │            ·  ·  ·   ·      ← high L1 ⇒ ANYTHING (necessary ≠ sufficient)
      │         ·  ·   ·  ·
      │      ·  ·  ·
      │   ·  ·                       ← the cascade forbids ONLY this cell:
      │ ·                                high L2 with low L1  (upper-left)
      └──────────────────────► L1
```

**A true cascade produces a low r.** So **r = .19 for ToM→social behaviour does NOT refute the
cascade** — it is exactly what a true necessity claim looks like under a correlational test. My
first draft got this wrong and the correction matters:

> **Test the cascade as a NECESSITY claim — count the empty cell — not as a correlation.**
> The prediction is: *the upper-left quadrant (high L2, low L1) is empty.* That's a one-sided test on
> a scatterplot, and it is cheap. If that cell is populated, the cascade is dead. If it's empty, the
> cascade lives regardless of r.

**This is the single most valuable methodological import in this note.** It also means the framework's
own §5 "Honest status" and open question 1 are asking the right thing in the wrong units.

**(c) The evidence that does exist runs the other way — and one arm is randomised.**

- **The tested arrow is L2→L1:** acting training → ToM/empathy gains (Goldstein & Winner 2012;
  Schellenberg 2004; **Goldstein & Lerner 2018, randomised**). Portrayal practice *produces*
  understanding.
- **Meisner says so explicitly:** "*a better understanding of others is the natural result of this
  acting training method, **not its goal**.*"
- **Stanislavski — the framework's natural patron — ran an L1-first pipeline for 25 years and then
  deleted it.** He spent 1911–1936 on "long months around the table… analyzing the text," then:
  "*Later he changed this practice because he felt it led to a **separation of emotion and
  behavior**,*" replacing it with rehearsal "almost immediately" — analysis *through* action. His
  diagnosis is a cascade failure: sequencing inner work first meant "by that time it was too late for
  organic physical work." His mature claim — the layers "*needed to be explored **simultaneously**,
  because they were **interdependent**"* — **is the direct denial of "failures cascade downward,
  never upward."** He also *forbids comprehension-shaped units*: "to think" and "to remember" are
  invalid objectives. **Anyone citing Stanislavski for L1→L2 is citing the model its author
  discarded.** (The American comprehension-first intuition is partly a publication accident: *An
  Actor Prepares* (1936) preceded *Building a Character* (1949) by 13 years.)
- **Diderot** is the cascade's best card — "*he must have a deal of judgment… **penetration and no
  sensibility***" — dissociating comprehension from feeling and putting quality on the comprehension
  side. But his own argument ("one cannot do two things at a time") is an **interference model, not a
  cascade**. **Stella Adler is the only real pro-cascade ancestor**, and her L1 is *world-research*,
  not introspection.
- **Portrayal is neurally not applied ToM.** Brown et al. (2019): responding in character produced
  "**global reductions in brain activity**" and "**deactivations in the cortical midline network**",
  "perhaps representing a '**loss of self**'" — deactivating regions the third-person/ToM condition
  did **not**. The paper explicitly distinguishes the actor from "*a theatre professor… recount[ing]
  details*". **Our L1.1 probe — interrogating the model out of character, in assistant mode, about
  the sheet — is the theatre professor task.**
- **Goldstein 2009 dissociates the layer:** actors **+0.55 SD on ToM, baseline on empathy**. → **L1
  must be defined cognitively, or it's false as a prerequisite.**

**⚠️ Honest caveat, stated twice because it matters:** this evidence is about *humans*, whose
portrayal bottleneck (body, nerves, stage fright, self-consciousness) an LLM does not have. **The
human comprehension→portrayal dissociation may simply not transfer.** But then the framework cannot
*also* claim psychological warrant for the cascade. **Pick one.**

### 2.4 ⚠️ Our L1.1 probes may be scoring novice behaviour

A Meisner-training study (Frontiers 2022; utterance coding at **κ = 0.86–0.88**) found:

> "**Novice actor observers made significantly more Feeling (p=0.001) and Speculation utterances
> (p<0.001) than professional observers**"
> Study 1, novices *over the course of training*: "Speculation utterances **increased**"
> Study 2: "**professional actors devoted themselves more to the connection with their partner**…
> while **novice actors relied on general inference to speculate about others' affective states**"

**Explicit speculation about another's inner state is a NOVICE signature.** Professionals do less of
it. L1.1's probe list — "*What does this character want that they'd never admit?*", "*What's the
contradiction in this character?*" — asks the model to do exactly the thing novices do more of.

**Hedge this properly:** the study codes *utterances during training exercises between actors*, not
answers to an examiner's questions. **It is an analogy, not a direct refutation** — being *able* to
articulate an inner state on demand is not the same as *spontaneously volunteering* speculation
instead of attending to your partner. But it is a real warning that **fluency at inner-state
articulation is not obviously the same thing as skill**, and it converges with Brown's
professor-vs-actor distinction. **At minimum, do not assume more articulate = better.**

### 2.5 ★★ "Consistency" is not just wrong — it is provably anti-correlated with what we want

This was the suspicion. It's worse than suspected.

**Mischel & Shoda (1995, p.250), quoting Shoda (1990):**

> "**the degree that an individual is characterized by stable patterns of situation-behavior relations
> is negatively related to the level of overall cross-situational consistency that can be
> expected.**"

**Strong behavioural signatures provably LOWER cross-situational consistency scores. The metric is
anti-correlated with the construct.** Optimizing L2.1 as written actively selects *against* characters
with vivid if-then structure.

**And it fires hardest on its best case.** CAPS's exemplar of coherence — Wediko summer-camp Child
#9, **profile stability r = .89**, aggression **z > 2.0 when warned by an adult** and **z < 0 when
approached by a peer** — is a textbook vivid character, and **would trigger our loudest drift
alarm.**

**The validity kill:** Mischel & Peake's reanalysis found that *perceived* consistency — what makes
observers say "same person" — tracked **profile stability (~.5)**, and showed **no relationship** to
cross-situational consistency. **The thing that makes humans say "that's the same person" is not what
we measure.**

**Fleeson (2001)**, experience sampling over 2–3 weeks:

> "**Within-person variability was high, such that the typical individual regularly and routinely
> manifested nearly all levels of all traits in his or her everyday behavior.**"
> "individual differences in **central tendencies** ... were **almost perfectly stable**"
> "**amount of behavioral variability** (and skew and kurtosis) **were revealed as stable individual
> differences**"

Within-person SD (**1.08**) *exceeds* between-person SD (**0.75**): "*individuals differ from
themselves over time at least as much as they differ from each other.*"

**Get Mischel right:** he attacked "personality traits as broad dispositions" (1968, p.146) —
**precisely the character-sheet-as-spec model** — not personality's existence, which he spent 30
years theorizing.

**The clean diagnosis of our metric:** L2.1 asks "*same person in turn 3 and turn 97, across many
contexts*". That **multiplies a should-be-high axis (temporal stability: real, .79–.94) by a
should-be-low-in-a-patterned-way axis (cross-situational invariance: ceiling ~.20–.30)**. It cannot
distinguish "*the model forgot who it was*" from "*the model noticed it was at a funeral*". **Both
score as defects.** A perfectly consistent character is not a realistic character; it is a cardboard
one. Fix in §4.3 — and the fix has human benchmark numbers.

### 2.6 ★ Trait crosstalk is not a defect — it's the founding finding of the field

L2.2 calls entanglement "**the killer** ... the character sheet stops being a specification."

**Asch's paradigm IS our L1 task**: subjects read a 7-word trait list describing a nonexistent person
and form an impression. He found the opposite of what we assume:

- **Warm/cold (N=90 vs 76): swapping one word moved `generous` from 91% → 8%, while `honest` moved
  98% → 94%.** That **selectivity** is the whole finding. An additive model predicts ~0 crosstalk
  everywhere; a halo model predicts uniform positive crosstalk. **Neither fits.**
- **Configural, not additive:** "the general impression is **not a factor added to the particular
  traits**, but rather the perception of **a particular form of relation between the traits**".
- **Asch explicitly named and rejected the position our matrix encodes:** the "halo effect" doctrine
  that configural influence "is **a source of error** which should be supplanted by the attitude of
  judging each trait in isolation". He argues *against* it — and warns that his additive Proposition
  I "controls in considerable degree many of the procedures for arriving at a scientific, objective
  view of a person (e.g., by means of questionnaires, **rating scales**)." **Our instrument assumes
  the model he wrote the paper to refute.**

**★ And Experiment IV is worse for us than the warm/cold result: centrality is not a trait
property.** Re-embed "warm" in `obedient—weak—shallow—warm—unambitious—vain` and it becomes
subsidiary — "'**warm' does not control the meaning of 'weak,' but is controlled by it**."

> **The perturbation coefficient of trait *i* depends on which other traits are present. So M[i,j] is
> not stable across sheets — which means the steerability matrix is not a matrix.** It's a
> sheet-specific local linearization of a configural process. That doesn't make it useless, but it
> does mean **it cannot be a model-level property**, and "entanglement" cannot be a model-level
> defect. Asch found this in 1946.

**Consequences:**

1. **A model with zero off-diagonal crosstalk would be an inhuman model** treating the sheet as a bag
   of independent switches — the "pastiche without comprehension" failure the framework worries about
   elsewhere. **The clean diagonal we want may be the defect.**
2. **The right question is whether the crosstalk is the RIGHT crosstalk** — does perturbing *warm*
   move `generous` 91→8 and leave `honest` at ~96? **Asch gives us a quantitative human ground truth
   for the off-diagonal**, converting an unbounded engineering complaint into a *bound* comparison.
   §4.5.
3. **Asch answers L2.3's "nobody has checked it".** He tested exact permutation in 1946 —
   intelligent→envious vs reversed (N=34/24), **identical tokens, swings up to 55 points**. And
   **footnote 5 pre-empts "Lost in the Middle"**: a *central* trait in the *middle* still dominated.
   He even specifies the discriminating ablation (list-framing vs person-framing) we could run
   tomorrow. Kelley (1950) replicated the selectivity on a live guest lecturer.

**⚠️ But don't overclaim realism — ~half our crosstalk will be judge halo.** Big Five are
non-orthogonal (E–O = .22–.39 even per skeptics; orthogonality is a *varimax convention*), but
general-factor saturation drops **50% → 26%** across inventories — **about half of observed trait
intercorrelation is rater halo, not structure.** Thorndike (1920): rating-based intelligence↔teaching
correlated **.95** vs **≤.30** test-based.

**So the off-diagonal has a three-way diagnosis, and our current metric distinguishes none of them:**

| off-diagonal pattern | meaning |
|---|---|
| matches metatrait/Asch structure | **realism** — leave it alone |
| flat, "too high and too even" | **judge halo** — fix the instrument, not the model |
| structured but *wrong* | **a real bug** — the thing we actually wanted to find |

### 2.7 The elasticity denominator is uncalibrated

> "*the perturbation is ours, so the referent is known exactly*"

**False.** We chose the *wording*, not the *magnitude*. `Δ(trait emphasis)` is a latent psychological
quantity; authoring "extremely" no more tells you its intensity than turning a dial tells you the
lumens. **Without a calibrated denominator, elasticity isn't a ratio — it's a numerator over an
arbitrary ordinal index, and the curve *shape* (our whole deliverable) is an artifact of our word
choice.**

The framework's own ladder, priced against Ruppenhofer et al. (2015) (slider −100..+100, 20
ratings/item):

| rung | word | calibrated intensity |
|---|---|---|
| "shy" | (unmodified) | baseline |
| "quite shy" | quite | **59.9** |
| "extremely shy" | extremely | **91.1** (Δ = **+31.2**) |
| "pathologically shy" | pathologically | **off-scale** — not a degree adverb; a *category* shift |

**Unequally spaced; rung 4 isn't on the scale.** Good news: the calibration exists and is stable
across adjectives (**ρ > 0.900**). §4.4.

### 2.8 Chemistry: confirmed, and it's the largest term

> Liking: "about **10%–20%** ... to **perceivers**, about the same amount to **targets**, and about
> **30%–40% to the unique perception**."
> "For trait ratings of the Big Five, about **40% of variance is due to relationship effects**."
> "**the variance of the individual level effects is lower than the variance of the dyad level
> effects**, and ... **the perceiver variance is higher than the target variance**."

**The chemistry term is the plurality of the variance, the perceiver beats the target, and chemistry
is the least stable component (r=.40 vs .90).** For a companion product where liking ≈ Q1, **~30–40%
of user preference is irreducibly dyad-specific and no model-level scalar can capture it.** That is a
structural ceiling on the leaderboard and belongs in BENCHMARKS.md as a limit, not a footnote.

Funder named the same thing (**relationship moderator**), and Connelly & Ones (2010) measured its
shape:

> "**Accuracy for judgments of extraversion differed little across relationships, but accuracy for
> judgments of emotional stability, openness, and agreeableness varied quite a bit.**"

**≈0 interaction for observable traits, large for internal ones.** Ironically, **L1.1's flagship probe
— "*what does this character want that they'd never admit?*" — targets precisely the trait class with
the worst cross-judge agreement.**

### 2.9 κ ≈ 0.78–0.94 for L1 is not plausible as stated

Three literatures agree agreement is a function of **trait observability**:

- **Kenny:** consensus "ranging from about **.20 at zero acquaintance to about .40 at long-term
  acquaintance**"; "**traits that are more behavioral, external or observable show more consensus.**"
- **Funder:** "good traits are **easily observable in most situations**."
- **Connelly & Ones:** above.

Different statistic (κ on a discrete probe vs a variance ratio), and our task *is* easier in one real
way — the sheet is fully available, so RAM's *availability* stage is maximal, and Kenny notes trait
differences shrink at full acquaintance. **Worth arguing. But it predicts ~.40, not ~.90.** And
**note 15 already measured our own spread: 0.052→0.213 (en), 0.086→0.466 (zh) — topping out at
.466.** Our own data sides with Kenny.

### 2.10 Steerability is an ATI, and Cronbach recanted the program

> "An ATI result can be taken as a general conclusion only if it is not in turn moderated by further
> variables. ... **Once we attend to interactions, we enter a hall of mirrors that extends to
> infinity. However far we carry our analysis — to third order or fifth order or any other —
> untested interactions of a still higher order can be envisioned.**"

From the man who invented coefficient alpha and construct validity, after 18 years and a 600-page
book. **Our steerability matrix is a model × trait × character × language × sheet-context
interaction** — a fourth-order ATI. The framework's open question 2 already suspects it won't
generalize (ρ(en,zh) = −0.082 → "assume not"). **Cronbach says that's the default, not the edge
case.** Funder walked into the same lattice ("each moderator could interact with every other
moderator") and concedes these "have not been tested as systematically".

**This doesn't kill L2.2.** It means: **pre-declare the cells you'll generalize over; treat the matrix
as a per-character diagnostic until stability is shown.**

### 2.11 RAM couldn't put numbers on its stages in 30 years

> "success is **not measured in a way that is objective and quantitative enough to actually assign a
> number to each stage** ... Rather, **this is a conceptual idea**."

The framework's headline promise is "*It converts a score into a diagnosis*". **That requires
attributing a failure to a layer.** RAM has had 30 years and can't. **Taxonomy is cheap; attribution
is the product.**

---

## 3. What we're MISSING

### 3.1 A criterion. Nothing in the framework is validated against an outcome.
Every layer is justified by *measurability*, none by *predicting anything*. Elliott is what happens
when someone checks. **Open question 3 must be asked of every layer, not just steerability.**

### 3.2 The "motivation" column
L1.2's fixes are decoding / prompt / sampling — all cheap. **Motivated inaccuracy and Strachan's
hyperconservatism say there's a fourth: the model is optimizing something else.** An RLHF'd model
being agreeable rather than in-character is doing motivated inaccuracy; that is not a sampling fix.
The human version is separable **by paying for accuracy** (Klein & Hodges: the gender gap in EA
vanished when correct inferences were paid). **Model analogue: an explicit accuracy-incentive
condition.**

### 3.3 ★ The stereotype/personality confound in note 15
Kenny's PERSON model:

> "consensus starts out at **.20 at zero acquaintance, all of which is due to S** and asymptotes at
> **.40, all of which is due to P**." (S = Stereotype, P = Personality)

**At zero acquaintance, 100% of inter-judge agreement is shared *stereotype*.** [Note
15](15-l1-convergent-reading.md) has this confound directly: cross-model agreement could be models
converging on the sheet (P), or **sharing a pretraining stereotype about tsundere/goth/mentor
archetypes (S)** — and models are the most stereotype-saturated judges imaginable, since shared
pretraining *is* shared priors.

**Fix (one extra condition): score an archetype-only sheet.** Strip specifics, keep the archetype
label. If agreement barely drops, we measured S. **This should gate the note-15 line of work.**

### 3.4 Consensus ≠ accuracy
Judges agreeing about a character doesn't make them right. The sheet **underdetermines** most
interesting questions — which is why L1.1's probes are interesting *and* why they won't have κ=.9.

### 3.5 Difference-score reliability
Elasticity is a **difference score**. The reliability of a difference between two correlated measures
is **low when the measures are highly correlated** — and our two conditions are designed to be one
word apart. **Elasticity may be near-unmeasurable at small doses** because the *estimator* is dead,
not the model. → large doses, many rungs, report elasticity's own SEM.

### 3.6 Nobody has shown "in-character-ness" is a reliably rateable construct
Searched; the literature is thin to nonexistent. **That is itself a finding** — we are about to assume
something no one has established. Note the contrast: the Meisner study got **κ=0.86–0.88 coding
utterance *types***, while holistic quality judgement gets α=0.25–0.34 (note 01). **Same lesson as
everywhere in this repo: code events, not vibes.**

---

## 4. What to STEAL instead of inventing

### 4.1 ★★ Test the cascade as a NECESSITY claim, not a correlation
**The single most valuable import here.** A cascade predicts a **triangular scatterplot** — the
upper-left cell (**high L2, low L1**) should be **empty**. Count that cell. A low r is *consistent
with* a true cascade and must not be read as refutation.

Pair with:
- **Elliott's measurement-mode design:** measure comprehension **three ways** — L1 probe accuracy /
  observer-rated in-character-ness / **user reports the character "gets" them** — all against
  retention/Q1. Elliott says the third wins.
- **The range-restriction test:** plot L1 vs Q1 across the model quality range. If L1 predicts among
  weak models and flattens among frontier ones, **say so and demote L1 to a floor check.** Cheap,
  decisive, and it's the framework's own best defence.
- **The incremental-validity check:** **if L1 rank ≈ MMLU rank, L1 is a proxy, not a layer.** One
  correlation, potentially fatal, run it first.

### 4.2 ★ Fit an SRM on the corpus we already have — zero new generations
11 models × 95 characters **is a round-robin.** Fit it today:

```
σ²_model        ← is there a general "roleplay ability"?
σ²_character    ← character difficulty (note 15's finding, properly modelled)
σ²_model×char   ← THE CHEMISTRY TERM. Kenny predicts it's the biggest.
```

**Directly answers the loudest open worry, costs nothing, and reuses note 04 §3/§7.4/§8.4's
mixed-effects infrastructure.** ⚠️ γ_ij needs replications per cell → **generate ≥2 samples per
model×character**, which note 03's population tier wants anyway. One design, three notes.

Report consensus as **target variance / total variance** rather than κ — comparable to a 40-year
literature.

### 4.3 ★★ Replace "consistency" with three separated measures — with human benchmarks
Fleeson and CAPS give not just the critique but the metric *and* the target numbers:

```
1. TEMPORAL STABILITY  (should be HIGH)     — same situation type, turn 3 vs turn 97
2. IF-THEN PROFILE STABILITY (the real one) — ipsatize behaviour within situation type,
                                              split session halves, correlate profiles
                                              TARGET .41–.48   FLOOR .20
3. DISTRIBUTION RECOVERY                    — mean AND SD (and skew)
                                              SD ≈ 0 is BROKEN and currently scores PERFECT
```

- **Band cross-situational consistency at .20–.40. `>.90` should flag RIGIDITY, not excellence.**
- **Elevation vs shape fail differently** — mean-match (~.90) and pattern-stability (~.45) are
  separate numbers; report both.
- **Aggregate k≈10–20 occasions *within* situation type** (Spearman-Brown from ρ₁≈.30) — Epstein's
  aggregation rebuttal. **Never aggregate across types**: Mischel & Peake got .08→.13 doing that.
- **This reuses note 03's population tier (k≥10 samples/scenario) exactly** — same generations, new
  statistics. Cheapest high-value change in the note.

### 4.4 ★ Calibrate the elasticity x-axis; fit a power law; report an exponent per trait
1. **Calibrated intensity as x**, not step index. Ruppenhofer et al.'s 14-adverb scale is published,
   free, and cross-adjective-stable (ρ > 0.900).
2. **Re-space the ladder:** `slightly (30.5) → fairly (42.1) → pretty (52.5) → quite (59.9) → very
   (78.6) → extremely (91.1)`. **Drop "pathologically"** or run it as a separate *categorical*
   condition.
3. **Fit `ψ = kI^a` in log-log; report `a` per trait.** Stevens' exponents run **0.33 (brightness) to
   3.5 (electric shock)** in the *same organism*. **"Dead" and "brittle" are not pathologies — they
   are compressive and expansive exponents.** Steerability is a **model × trait** property; report the
   exponent vector and state in advance what exponent is too low to ship.
4. **Weber's law (ΔI/I = k):** the same word buys less at high baseline → expect apparent curvature;
   don't over-read it.
5. **Run magnitude estimation for zh before any cross-language elasticity claim.** A Chinese *非常* is
   not an English *very* until measured. Note 04 §5.3's RC-DIF problem in a new place, same fix.

### 4.5 ★ Asch's warm/cold as ground truth for the off-diagonal
Replicate warm/cold on a character sheet; compare the model's off-diagonal to **Asch's human
off-diagonal**, which is selective and has 80 years of replication.

```
diagonal      → does the perturbed trait move?                    (steerability)
off-diagonal  → does it move the traits Asch's subjects moved,
                and leave alone the ones they left alone?          (FIDELITY, not crosstalk)
                + is it flat and even?  → that's OUR judge's halo, not the model
```

**Converts the biggest unbounded engineering complaint into a bound comparison.** A model with zero
crosstalk fails this test — correctly.

### 4.6 Ickes' scoring, verbatim
- **The 0/1/2 content-similarity scale.** Coarse, α≈.90. (Note 04 §1.3 chose 0–5 from a single
  unreplicated 2026 paper; Ickes goes coarser on 40 years of data. Worth a bake-off.)
- **The denominator:** `accuracy points / (n_inferences × 2) × 100` — **a structural verbosity
  correction, not a covariate.** Note 03 calls length "THE BIGGEST TRAP IN THIS DOC" (r=0.79–0.904
  with word count); **Ickes solved it in 1990** by making the denominator *items attempted*.
- **Cross-target consistency as a first-class stat** — is a model good at character A also good at
  character B? **This is the test of whether "L1 ability" exists at all**, and it runs on the existing
  corpus. Ickes gets .86–.91; note 15's analogue tops out at .466.
- **Report agreement per-character, never pooled** (Ickes' own homogeneity caveat + our 4–5× range).

### 4.7 FANToM's conjunctive scoring, and worst-case over perturbations
- **FANToM's ALL* metric**: score the model correct only if it holds across **≥3 framings** of the
  same question. Humans **87.5%**, GPT-4 **4.1%** — while GPT-4 scores 68–73% on any *single*
  framing. **Single-framing L1 scores are ~17× too generous.**
- **Report worst-case over perturbations, not mean.** Shapira: GPT-4 scored **0%** on in→on and
  transparent-access perturbations where **davinci-002 scored 71.4% and 66.7%** — *inverse scaling*.
  Ullman's "double space" flipped a belief attribution ~50 points.
- **Matched non-character control probes** (Strange Stories logic) — is the failure about *character*
  or about *reasoning*?
- **Elicit likelihoods, not binary commitments** — Strachan's faux-pas deficit vanished under "*is it
  more likely they knew?*". A binary probe measures a decision threshold, not comprehension.
- Note 03 already reached "**gate, don't mean**" for creativity. **Same rule, now for L1.**

### 4.8 Bayesian nulls for the L1 dimensionality question
Use **Bayes factors** on the L1 inter-probe matrix. "We found no correlation" is unpersuasive;
**BF01 > 10 is a result.** Free upgrade to note 04 §4.1's discriminant matrix.

### 4.9 Names and citations we should be using

| ours | theirs | why |
|---|---|---|
| L1 | **Empathic accuracy, standard stimulus paradigm** (Ickes) | our design *is* EA-SSP; 40 years of validation |
| the cascade | **Realistic Accuracy Model** (Funder 1995) | necessary + multiplicative stages |
| chemistry | **relationship variance** (Kenny) / **relationship moderator** (Funder) | measurable — and it's 30–40% |
| character difficulty | **good target** / **judgeability** | studied moderator |
| sheet quality | **good information** (quantity × quality) | gives the style-guide hypothesis free |
| consistency | **personality coherence** / **if-then signatures** (Mischel & Shoda) | the construct we actually want |
| L2.2 | **magnitude estimation** / **Stevens' power law** | 150 years of method |
| steerability | **aptitude-treatment interaction** (Cronbach) | including its cautionary tale |

---

## 5. The rewrite this implies

**The framework survives — re-argued, demoted, and with three metrics replaced.**

1. **Delete the agreement-gradient argument as a *justification*.** §1's "*the two layers that gate
   everything are exactly the two we can measure with high agreement*" is the load-bearing error.
   Replace with:

   > L1 and L2 are **cheap, reliable, diagnostic instruments for debugging a failure.** They are
   > **not** proxies for quality and must never become ship gates or optimization targets. What
   > predicts whether the product works is perspectival, expensive, needs real users, and cannot be
   > subtracted away.

   **This is compatible with nearly everything else the document says.** §5's "Deliverable: a
   diagnosis + a character-sheet style guide" is *exactly right* and already there. What must go is
   the claim that boundedness makes L1/L2 the layers that **matter**. **They are the layers we can
   afford.** Different property.

2. **Choose narrow-L1 explicitly.** We can have a narrow L1 that measures well or a broad L1 that
   means what we intend — **not both**. Report `L1-recognition` (forced-choice) and `L1-inference`
   (open-ended) **separately**; five literatures say they won't correlate and one gives the mechanism
   (pattern-matching vs perspective-taking-from-context). Run the inter-probe matrix with Bayes
   factors **before** publishing any pooled L1 number.

3. **Define L1 cognitively, not affectively** (Goldstein: actors +0.55 SD ToM, **baseline empathy**).
   Otherwise it's false as a prerequisite on its face.

4. **Report L1 as `model × sheet`**, sheet-side variance broken out (RAM's relevance/availability are
   the sheet's, not the model's).

5. **Stratify every L1/L2 number by trait observability.** Never pool observable and internal traits.

6. **Rewrite L2.1** into the three separated measures with human benchmark bands (§4.3). Flag `>.90`
   as rigidity.

7. **Rewrite L2.2's off-diagonal** to the three-way diagnosis (realism / halo / bug) against Asch
   (§4.5). Calibrate the x-axis and report an exponent per trait (§4.4).

8. **Delete "nobody has checked it for character sheets"** from L2.3. Asch, 1946.

9. **Promote chemistry from a worry to a reported quantity** (§4.2). If σ²_model×char dominates — and
   Kenny predicts it will — that's a structural ceiling on the leaderboard, and it belongs in
   BENCHMARKS.md.

10. **Add the motivation column to L1.2** plus the accuracy-incentive condition.

11. **Gate note 15 on the archetype-only control** (§3.3).

12. **Reframe open question 1 as a necessity test** (count the empty cell), not a correlation — and
    run the MMLU incremental-validity check first, because it's one correlation and potentially
    fatal.

**Two experiments the literature says are novel contributions, not just internal hygiene:**
- **Regress portrayal quality on comprehension.** Nobody has ever done it, in humans or models.
- **The forced-pre-analysis ablation** both Stanislavski and Meisner predict: **does forcing L1-style
  analysis before roleplay *degrade* it?** If yes, the cascade is not just unsupported — it's
  backwards, and our probe design is iatrogenic.

---

## 6. Honest limitations

- **My first draft got the cascade verdict wrong**, reading r=.19 (ToM→behaviour) as refutation. **A
  necessity claim predicts a low r.** Corrected in §2.3; the fix (count the empty cell) is now the
  top recommendation. Flagging because the same error is easy to repeat.
- **The strongest counter-evidence (Elliott) is range-restricted.** Trained therapists all cleared a
  competence bar; our models have not. §4.1's range test is the honest way to settle it, **and it may
  well vindicate L1.** Not settled here.
- **⚠️ Ceiling-effect trap, both directions.** Ligthelm's null (η²=0.05, p=0.96, n=20) is a warning:
  **if L1 items are easy for frontier models, zero variance will produce a *spurious* refutation of
  the cascade for purely psychometric reasons.** Check L1 item variance *before* concluding anything
  from our own data. A flat L1 might mean "L1 doesn't matter" or "our probes are too easy" — and
  those recommend opposite actions.
- **The acting/actor evidence is about humans**, whose portrayal bottleneck (body, nerves,
  self-consciousness) an LLM lacks. The dissociation may not transfer — but the framework can't
  dismiss it *and* claim psychological warrant for the cascade.
- **§2.4's novice-signature finding is an analogy, not a direct hit** — it codes utterances between
  actors in training, not answers to an examiner. Hedged in place.
- **κ vs variance-ratio is a real apples/oranges problem.** Kenny's .20–.40 is a variance ratio on
  real people; our κ is on discrete probes against a fully-available written sheet. Our task is
  genuinely easier on RAM's availability stage. **Directional, not exact** — but note 15's own max of
  .466 sides with Kenny.
- **Brown et al. (2019) is n=15, one fMRI study, one play.** Suggestive, not established.
- **Ruppenhofer et al.'s adverb scale is English, crowd-sourced, 2015.** Best available calibration,
  not a law. The zh scale does not exist; we'd have to build it.
- **RAM assumes traits are real**; Mischel/CAPS/Fleeson are the other side. **I cite both as support
  for different parts of our framework, which is slightly opportunistic.** The tension is unresolved
  in psychology itself; "coherence, not invariance" (§4.3) is the operational resolution.
- **Verification debt (flagged in-file by the acting research):** Konijn (403 on every mirror —
  highest-value unverified source), Burgoyne 1999, and the Brecht wording need manual retrieval.
- **Not covered:** HEXACO specifics; Adler/Strasberg in depth; difference-score reliability worked
  through with the actual formula (§3.5 is qualitative).
