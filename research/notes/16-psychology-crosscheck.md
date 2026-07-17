# 16 — Psychology cross-check: does the L1→L2→L3 cascade survive?

**Topic owner:** construct validity of [ABILITY-MODEL.md](../docs/ABILITY-MODEL.md)
**Date:** 2026-07-16
**Sources:** `research/sources/psych-*.md` (33 files)

**Scope:** the ability model claims roleplay quality decomposes into three causally ordered layers
(L1 comprehension → L2 application & steerability → L3 creativity), that failures cascade downward
never upward, and that L1/L2 are "bound" (→ high agreement) while L3 is perspectival. Psychology has
studied *understanding another person* and *portraying a character* for a century. This note asks
whether we are re-inventing a validated wheel, or building a square one.

---

## 0. Verdict in one page

**The framework's *shape* is right and is 30 years old. Its *content* is wrong in four specific,
fixable places. Its *strategic bet* — "measure the bound layers because they have high agreement" —
is refuted by the best available evidence, and that is the finding that matters.**

| claim | verdict | the evidence |
|---|---|---|
| Quality decomposes into ordered, necessary stages; failures cascade downward | ✅ **SUPPORTED — and not novel.** Funder's **Realistic Accuracy Model** (1995) is exactly this: relevance→availability→detection→utilization, explicitly "**necessary**" and "**multiplicative**" | [RAM](../sources/psych-funder-realistic-accuracy-model.md) |
| **"L1/L2 are bound ⇒ high agreement ⇒ they're the layers to measure"** | ❌ **REFUTED. This is the load-bearing error.** Boundedness buys **reliability**, not **validity**. The bound measure has ~0 criterion validity | [Elliott](../sources/psych-elliott-empathy-outcome-meta.md), [Ickes](../sources/psych-empathic-accuracy-ickes.md) |
| L1 "comprehension" is one measurable thing | ❌ **REFUTED — five independent literatures, all null** | [ToM convergence](../sources/psych-tom-task-convergence.md), [ERA vs EA](../sources/psych-era-vs-ea-separate-competences.md), [Ickes](../sources/psych-empathic-accuracy-ickes.md) |
| L1 gates L2 (understanding predicts portrayal) | ⚠️ **WEAK.** ToM→behaviour **r=.19** (~4% variance). Acting is neurally *not* applied ToM. Diderot, Meisner and Stanislavski's late method all invert the order | [ToM→competence](../sources/psych-tom-predicts-social-competence.md), [Brown fMRI](../sources/psych-actor-neuroscience-brown.md), [Diderot](../sources/psych-diderot-paradox-actor.md), [Meisner](../sources/psych-meisner-technique.md) |
| L2.1 "consistency of hold" is the right metric | ❌ **PSYCHOLOGICALLY WRONG as invariance.** Real people manifest *nearly all levels of all traits*. Variability is signal | [Fleeson](../sources/psych-fleeson-whole-trait-density.md), [CAPS](../sources/psych-caps-behavioral-signatures.md), [Mischel](../sources/psych-mischel-person-situation.md) |
| L2.2 trait crosstalk is "the killer" defect | ❌ **REFUTED. Crosstalk is how person perception works.** Asch (1946) is the founding finding of the field | [Asch](../sources/psych-asch-impression-formation.md) |
| L2.2 "the perturbation is ours, so the referent is known exactly" | ❌ **FALSE — but cheaply fixable.** We chose the wording, not the dose | [psychophysics](../sources/psych-psychophysics-dose-scaling.md) |
| L2.3 sheet-position effects are untested | ❌ **Tested in 1946.** Asch's primacy effect | [Asch](../sources/psych-asch-impression-formation.md) |
| "Chemistry is a user×character×model interaction" (stated as a worry) | ✅ **CONFIRMED, and worse than stated.** It is the **largest single variance component** (30–40%) and the *least stable* (r=.40) | [Kenny SRM](../sources/psych-kenny-social-relations-model.md) |
| Isolate the perspectival layer at the end, measure bound layers separately | ✅ **SUPPORTED** — target effects are stable (r=.90), relationship effects are not (r=.40). Best quantitative support for the architecture we found | [Kenny SRM](../sources/psych-kenny-social-relations-model.md) |

**The one-sentence version:** *the cascade is a real model form with a distinguished pedigree, but
the framework picked its layers by reliability and never checked whether the reliable layers predict
anything — and in the one large-scale test available, they don't.*

---

## 1. What psychology SUPPORTS

### 1.1 The cascade form is legitimate — and has a name

**Funder's Realistic Accuracy Model (Psych Review, 1995)** decomposes accurate person-judgment into
four stages, and its structural claim is *our* structural claim, stated more strongly:

> "Within the RAM, these stages are all described as **necessary**, which means that **if any stage
> is unsuccessful, an accurate judgment is not possible**."
> "The stages are also **multiplicative**, meaning that the level of accuracy of the judgment could
> theoretically be determined by **multiplying the levels of success for each stage**."

**"Failures cascade downward, never upward" is a respectable, 30-year-old model form. Cite RAM and
stop presenting it as our invention.** The "test in order, stop at the first failure" logic follows
from necessity, and it is sound *as logic*.

### 1.2 The architecture's core strategic move — isolate preference at the end — is right

Kenny's SRM decomposes any interpersonal judgment into perceiver + target + relationship. The
stability numbers are the best support the framework has:

> "strong stability for the **target effect, r = .90**, but not nearly the same degree of stability
> for the **relationship effect, r = .40**"

The consensual/bound component is a *great* regression detector (r=.90). The idiosyncratic/
preference component is large and barely replicates (r=.40). **Measuring the bound layers separately
and refusing to smear preference across every metric is the right call, and this is why.** The
framework's instinct here is correct and now has a number behind it.

### 1.3 L1.2's discrimination/generation gap is a real, named human phenomenon — twice over

- **Motivated inaccuracy** (Simpson et al. 1995): dating partners — who are normally ~50% *more*
  accurate than strangers — dropped to **"significantly worse than that of total strangers and not
  significantly greater than chance"** when accuracy was threatening. Capability intact, performance
  collapsed. That is L1.2 row 2 ("knows better than it acts") in humans.
- **Recognition vs inference are dissociable competences** with Bayesian evidence *for* the null
  (BF01 = 29.82–124.98). The authors' explanation — **"pattern matching"** vs **"perspective taking
  using context information"** — is exactly L1.2 row 4 ("mimicry without comprehension").

**L1.2 is the best-motivated single design in the ability model.** Keep it. But see §2.1 and §3.2 —
its cause is probably not "decoding, prompt, sampling", and its two probe formats won't correlate.

### 1.4 L2.2 dose-response is the oldest quantitative method in psychology

The framework calls it "the only genuinely causal thing in the whole catalogue". It's right, and it's
**psychophysics** — Fechner 1860, Stevens 1957. We should be fitting `ψ = kI^a` in log-log and
reporting the exponent. See §4.4 for what that changes.

### 1.5 Authoring is a real lever — RAM says so, structurally

RAM's first two stages, **relevance** and **availability**, are properties of the **target**, not the
judge. Applied to us: **the character sheet is the target.** If the sheet specifies nothing relevant
to a trait, no model can be accurate about it — and that is not a model defect. RAM's **"good
information"** moderator has two aspects:

> "**Information quantity** ... having more information tends to result in more accurate judgments
> ... referred to as the **acquaintanceship effect**"
> "**Information quality** ... Highly useful information includes information about **general and
> specific behaviors, and thoughts and feelings**."

**ABILITY-MODEL §5 calls this "*if the hypothesis holds*". RAM says it is not a hypothesis — it is
two of the four stages with 30 years of support.** [Note 15](15-l1-convergent-reading.md)'s
underpowered result (en +0.324, zh +0.274, n=45) is the **acquaintanceship effect**, and RAM is the
prior that makes it worth powering properly rather than dropping at p=0.07. Better: information
*quality* gives us a **pre-registered, empirically grounded prediction about what a good character
sheet contains** — behaviours, thoughts, feelings — which is the "house style guide" deliverable
handed to us for free.

---

## 2. What psychology CONTRADICTS

### 2.1 ★ THE BIG ONE: bound ⇏ valid. The framework optimizes the wrong property.

ABILITY-MODEL §1's central argument:

> "**L1 and L2 are bound.** ... So **the two layers that gate everything are exactly the two we can
> measure with high agreement** ... This is why the framework beats the defect catalogue: it doesn't
> just say what to measure, it **explains why most of it is measurable.**"

**Empathic accuracy is the 40-year refutation of the inference from "bound" to "worth measuring".**

EA is *maximally* bound — the referent is the target's own timestamped self-report of their own
thought. Its inter-rater reliability:

> "ranging from a low of **0.85** ... to a high of **0.98** ... the average interrater reliability
> has been about **0.90**"

And yet:

| | | |
|---|---|---|
| EA ↔ Costanzo & Archer's Interpersonal Perception Task (the *most similar* other measure) | **r = 0.06** | "not significantly different from zero" |
| EA ↔ emotion recognition accuracy | **BF01 = 29.82–124.98** | strong-to-extreme evidence **FOR the null** |
| EA ↔ self-report empathy dispositions | null | "generally fail to predict" |
| ToM tasks ↔ each other (adults) | all r ∈ **[−.115, +.125]** | RMET correlates *negatively* with higher-order ToM |
| Different interpersonal-sensitivity performance measures ↔ each other | null | Hall (2001) |

**α = 0.90 and r = 0.06 in the same instrument.** Boundedness buys **reliability**. It does not buy
**validity**, and it does not buy **unidimensionality**.

Note 04 §2.5 already has the attenuation ceiling `√(ρ_xx'·ρ_yy')`. **The point here is worse than
attenuation:** with ρ≈.90 on both measures the *permitted* correlation is ≈.90 and the observed one
is **.06**. That isn't noise. **That is two different constructs wearing the same name.**

### 2.2 ★★ And the bound measure doesn't predict the outcome

**Elliott, Bohart, Watson & Murphy (2018), 82 samples, 6,138 clients** — the one profession whose
entire job is understanding another mind:

> Overall therapist empathy → outcome: **r = 0.28** (d = 0.58), "about **8%** of the difference in
> outcomes".
> "**Unlike other ways of measuring empathy, it was virtually unrelated to outcomes when measured as
> the degree to which client and therapist shared the same perceptions of what the client was feeling
> or thinking ('empathic accuracy').**"
> "**Rather than the perspectives of therapists or observers, clients' reports of therapist empathy
> best predict treatment outcome.**"

| | measure | agreement | predicts outcome? |
|---|---|---|---|
| **our L1** | empathic accuracy — bound, objective, scored against the referent | **α ≈ .90** | **≈ 0** |
| **our L3** | client-perceived empathy — perspectival, one person's opinion | low | **r = .28, the best of any measure** |

**The two properties are anti-correlated in the data.** The framework's agreement gradient sorts
measurements by exactly the wrong key: it gates on the reliable-and-inert layer and defers the
noisy-and-predictive one as "intractable".

The analogy is unusually tight — therapist:client :: companion character:user — and *"the client's
felt sense of being understood"* is close to the companion product's entire value proposition.

**The framework's best defence, and it's a real one:** Elliott's therapists are **range-restricted**
— all cleared a competence bar, so within-sample the selection variable stops predicting. Our models
are not (note 01: LifeChoice human 92.01 vs best model 67.95). **So L1 may predict in our range and
flatten later.** But notice what that concession costs: it converts L1 from *"the layer that gates
everything"* into *"a floor check that stops discriminating once models clear it."* **That is a much
weaker claim than §1 makes — and it is testable today.** See §4.1.

### 2.3 The cascade is at the wrong altitude — and understanding barely predicts portrayal

Two separate problems.

**(a) RAM's four necessary stages are all *inside* our L1.** RAM spends relevance→availability→
detection→utilization getting to "did the judge understand the target?" Our L1 is one box; RAM says
it's four, **and two of them belong to the character sheet, not the model.** Our L1 is
under-decomposed.

**(b) The L1→L2 link is weak wherever anyone has measured it:**

- **ToM → social behaviour: r = .19**, "about **4%** of the variance in peer popularity". Two
  meta-analyses converge.
- **Acting is neurally not applied ToM.** Brown et al. (2019) fMRI: responding in character produced
  "**global reductions in brain activity**" and "**deactivations in the cortical midline network**",
  "perhaps representing a '**loss of self**'". Critically, the in-character condition deactivated
  regions the third-person/ToM condition did **not**. **Portrayal ≠ mentalising-about-a-character.**
- **Acting pedagogy mostly inverts our order.** Diderot: "**in complete absence of sensibility is the
  possibility of a sublime actor**" — the great actor "must have in himself an unmoved and
  disinterested onlooker ... **penetration and no sensibility**". Meisner's whole method is
  anti-analytic ("get out of your head"). Stanislavski himself *late in life* abandoned
  emotion-memory for the **Method of Physical Actions** — action first, understanding after. Konijn's
  **task-emotion theory** finds actors run on "nervousness, concentration and excitement", which
  "**allow an actor to perform, not just feel**".

**Nobody in 250 years of acting theory believes comprehension→embodiment is the causal order, and
the one fMRI study says portrayal recruits something ToM doesn't.** The framework's "*You cannot
apply a character you didn't understand*" is defensible as *logic* but has essentially no support as
*psychology*, and several traditions actively deny it.

**⚠️ Caveat, stated honestly:** this evidence is about *humans*, whose bottleneck is embodiment
(nerves, body, stage fright, self-consciousness). An LLM has no body and no stage fright. **The human
comprehension→portrayal gap may simply not transfer**, and the framework can reasonably say so. But
then it cannot *also* claim psychological warrant for the cascade. **Pick one.**

### 2.4 ★ "Consistency" as invariance is psychologically wrong — and our metric may punish realism

This was the suspicion, and it's correct.

**Mischel (1968):** cross-situational consistency correlations sit around **r ≈ .30** — the
"personality coefficient". (Mischel did *not* say personality doesn't exist; he said trait scores
predict cross-situational behaviour weakly.)

**Fleeson (2001), experience sampling over 2–3 weeks — the devastating one:**

> "**Within-person variability was high, such that the typical individual regularly and routinely
> manifested nearly all levels of all traits in his or her everyday behavior.**"
> "individual differences in **central tendencies** of behavioral distributions were **almost
> perfectly stable**"
> "**amount of behavioral variability** (and skew and kurtosis) **were revealed as stable individual
> differences**"

**Mischel & Shoda's CAPS (1995) — behavioural signatures:**

> "The theory accounts for individual differences in **predictable patterns of variability across
> situations** (e.g., **if A then she X, but if B then she Y**), as well as for overall average levels
> of behavior, as essential expressions or **behavioral signatures** of the same underlying
> personality system."
> "**this variability reflects some of the essence of personality coherence**"
> "patterns of variability are seen **not as mere 'error' but also as reflecting essential
> expressions of the same underlying stable personality system**"

**Read L2.1 against that.** "*Same character, many contexts: is it the same person in turn 3 and turn
97?*" — as literally specified, a model that is *identically* shy at a funeral and a party scores
**better** than one that modulates. **A perfectly consistent character is not a realistic character;
it is a cardboard one.** Our metric, as written, rewards flatness and calls it fidelity.

This is not a quibble — it is the difference between measuring *invariance* (wrong) and *coherence*
(right). And **the fix is concrete and uses infrastructure we already planned** (§4.3).

### 2.5 ★ Trait crosstalk is not a defect. It's the founding finding of person perception.

ABILITY-MODEL L2.2 calls entanglement "**the killer** ... Authors cannot compose traits; the
character sheet stops being a specification."

**Asch (1946), "Forming Impressions of Personality"** — the paper that founded the field — found the
exact opposite of what we assume:

- **The warm/cold manipulation:** change *one word* in an otherwise identical trait list and the
  entire impression transforms. "**There are extreme reversals between Groups A and B in the choice
  of fitting characteristics.**"
- **Impressions are configural, not additive:** "the general impression is **not a factor added to
  the particular traits**, but rather the perception of **a particular form of relation between the
  traits**".
- **Asch explicitly rejected the framing that this is error:** "It has been asserted that the general
  impression 'colors' the particular characteristics ... In consequence the conclusion is drawn that
  the general impression is **a source of error** which should be supplanted by the attitude of
  judging each trait in isolation ... **This is the doctrine of the 'halo effect'.**" Asch argues
  *against* that doctrine.
- **And he found crosstalk is selective, not uniform:** "There is another group of qualities which is
  **not affected** by the transition from 'warm' to 'cold', or only slightly affected."

**Three consequences:**

1. **A model with zero off-diagonal crosstalk would be an inhuman model.** Perturbing "shy" *should*
   move "confident". If our model has a perfectly clean diagonal, that is evidence it is treating the
   sheet as a bag of independent switches — which is exactly the "pastiche without comprehension"
   failure the framework worries about elsewhere. **The clean diagonal we want may be the defect.**
2. **The right question is not "is there crosstalk" but "is the crosstalk the RIGHT crosstalk"** —
   does perturbing *warm* move the traits Asch's subjects moved, and leave alone the ones they left
   alone? **Asch gives us a human-agreement ground truth for the off-diagonal.** That converts the
   steerability matrix from an unbounded engineering complaint into a *bound* comparison against
   human data. This is the single best "steal" in the whole cross-check (§4.5).
3. **Asch's primacy effect answers L2.3's open question.** L2.3 asks whether position in the sheet
   matters and says "**Lost in the Middle**" says yes; **nobody has checked it for character sheets**.
   Asch checked it in 1946 with the intelligent–industrious–impulsive–critical–stubborn–envious list
   read forwards vs backwards. Position matters, in humans, for exactly the stimulus type we use.

**Note the tension with note 04 §4.1, and resolve it explicitly.** Note 04 wants discriminant
validity (inter-dimension r < 0.7) and warns "if creativity and engagement correlate at r=0.9 we
have one dimension with two names". **That is about our *rubric's* dimensions.** Asch is about the
*character's* traits. **These are different objects and the same statistic means opposite things:**
correlated rubric dimensions = our instrument is redundant (bad); correlated character traits =
the model perceives configurally (realistic). Don't let one policy govern both.

### 2.6 The elasticity denominator is uncalibrated

> "*the perturbation is ours, so the referent is known exactly*"

**False.** We chose the *wording*; we did not choose the *magnitude*. `Δ(trait emphasis in prompt)`
is a latent psychological quantity. Authoring "extremely" no more tells you its intensity than
turning a dial tells you the lumens. **Without a calibrated denominator, elasticity is not a ratio —
it's a numerator over an arbitrary ordinal index, and the curve *shape* (our entire deliverable) is
an artifact of the words we happened to pick.**

The framework's own example ladder, priced against Ruppenhofer et al.'s (2015) human gold standard
(slider −100..+100, 20 ratings/item):

| rung | word | calibrated intensity |
|---|---|---|
| "shy" | (unmodified) | baseline |
| "quite shy" | quite | **59.9** |
| "extremely shy" | extremely | **91.1** (Δ = **+31.2**) |
| "pathologically shy" | pathologically | **off-scale** — not a degree adverb; it's a *category* shift |

**Unequally spaced, and rung 4 isn't on the scale.** Good news: the calibration exists and is stable
across adjectives (**Spearman ρ > 0.900**). Fix in §4.4.

### 2.7 Chemistry: confirmed, and it's the largest term

The framework mentions the user×character×model interaction as a worry. **Kenny's SRM has measured
it for 40 years and the answer is worse than the worry:**

> Liking: "about **10%–20%** of the variance ... to **perceivers**, about the same amount to
> **targets**, and about **30%–40% to the unique perception**."
> "For trait ratings of the Big Five, about **40% of variance is due to relationship effects**."
> "**the variance of the individual level effects is lower than the variance of the dyad level
> effects**, and ... **the perceiver variance is higher than the target variance**."
> "**Strong relationship effects make the case for uniqueness: A given person's perception of another
> person is idiosyncratic.**"

**The relationship (chemistry) term is the plurality of the variance, the perceiver term beats the
target term, and the relationship term is the *least stable* (r=.40 vs .90).** For a companion
product where "liking" ≈ Q1, **SRM says ~30–40% of user preference is irreducibly dyad-specific and
no model-level scalar can capture it.** That is a structural ceiling on the leaderboard concept and
belongs in BENCHMARKS.md as a limit, not a footnote.

Funder independently named the same thing — the **relationship** moderator — and Connelly & Ones
(2010) measured its shape:

> "**Accuracy for judgments of extraversion differed little across relationships, but accuracy for
> judgments of emotional stability, openness, and agreeableness varied quite a bit across
> relationships.**"

**The interaction is ≈0 for observable traits and large for internal ones.** So our numbers will be
stable for speech style and overt behaviour, and interaction-dominated for motivations and "what they
never admit". **Ironically, L1.1's flagship probe — "*What does this character want that they'd never
admit?*" — targets precisely the trait class with the worst cross-judge agreement.**

### 2.8 κ ≈ 0.78–0.94 for L1 is not plausible as stated

Three independent literatures say agreement is a function of **trait observability**, and that the
ceiling is far below 0.9:

- **Kenny:** "The level of consensus is fairly modest, ranging from about **.20 at zero acquaintance
  to about .40 at long-term acquaintance**." "**traits that are more behavioral, external or
  observable show more consensus.**" More consensus for extraversion than any other Big Five factor.
- **Funder:** "good traits are **easily observable in most situations**."
- **Connelly & Ones:** as above.

Different statistic (κ on a discrete probe vs a variance ratio), and our task *is* easier in one real
way — the sheet is fully available to every judge, so RAM's *availability* stage is maximal, and
Kenny notes trait differences shrink at full acquaintance. **That argument is worth making. But it
predicts we land near .40, not .90.** And **note 15 already measured our own spread: 0.052→0.213 (en)
and 0.086→0.466 (zh) — a 4–5× range, topping out at .466.** Our own data agrees with Kenny and
disagrees with the framework.

**A single pooled L1 κ is an artifact of probe mix.** Stratify by trait observability or don't report
it.

### 2.9 Steerability is an ATI, and Cronbach recanted the whole program

Our steerability construct is an **aptitude × treatment interaction**: aptitude = model, treatment =
prompt perturbation, outcome = behaviour change. Cronbach founded ATI in 1957, spent 18 years and a
600-page book on it with Snow, then publicly recanted:

> "An ATI result can be taken as a general conclusion only if it is not in turn moderated by further
> variables. If Aptitude × Treatment × Sex interact, for example, then the Aptitude × Treatment
> effect does not tell the story. **Once we attend to interactions, we enter a hall of mirrors that
> extends to infinity. However far we carry our analysis — to third order or fifth order or any other
> — untested interactions of a still higher order can be envisioned.**"

From the man who invented coefficient alpha and construct validity. **Our steerability matrix is a
model × trait × character × language × sheet-context interaction.** That is a fourth-order ATI, and
the framework's own open question 2 already suspects it won't generalize (ρ(en,zh) = −0.082 → "assume
not"). **Cronbach says that suspicion is the default, not the edge case.**

Funder walked into the same lattice: "**each moderator could interact with every other moderator**"
(relationship, expertise, sensitivity, palpability, divulgence, diagnosticity) — and concedes these
"**have not been tested as systematically**".

**This does not kill L2.2.** It means: **pre-declare the cells you will generalize over, and treat
the matrix as a per-character diagnostic rather than a model property** until stability is *shown*.

### 2.10 RAM couldn't put numbers on its stages in 30 years

> "success is **not measured in a way that is objective and quantitative enough to actually assign a
> number to each stage**, so levels of accuracy are not really determined in this way. Rather, **this
> is a conceptual idea**."

The framework's headline promise is §1's *"It converts a score into a diagnosis"* — L1 fine, L2
elasticity ≈ 0, therefore fix X. **That promise requires attributing a failure to a layer.** RAM has
had 30 years, a research program, and dozens of labs, and still cannot. **Taxonomy is cheap;
attribution is the product.** The §5 "Honest status" table should say so.

---

## 3. What psychology says we're MISSING

### 3.1 A criterion. Nothing in the framework is validated against an outcome.

Every layer is justified by *measurability*. None is justified by *predicting anything*. Elliott et
al. is what happens when someone finally checks: **the reliable measure predicted nothing and the
noisy one predicted everything.** The framework's own open question 3 asks this of steerability
only — **it must be asked of every layer.**

### 3.2 The "motivation" column

L1.2's table has three fix-columns: decoding, prompt, sampling — all "cheap". **Motivated inaccuracy
says there's a fourth: the model is optimizing something else.** An RLHF'd model being agreeable
rather than in-character is doing motivated inaccuracy, and that is not a sampling fix. Klein &
Hodges showed the human version is separable **by paying for accuracy** — the gender gap in EA
vanished when correct inferences were paid. **Model analogue: an explicit accuracy-incentive
condition.** Cheap, and it cleanly separates capability from disposition. Add the column.

### 3.3 The stereotype/personality confound in note 15 ★

Kenny's PERSON model:

> "consensus starts out at **.20 at zero acquaintance, all of which is due to S** and asymptotes at
> **.40, all of which is due to P**." (S = Stereotype, P = Personality)

**At zero acquaintance, 100% of inter-judge agreement is shared *stereotype*, not the target's actual
personality.** Judges agree because they share priors.

**[Note 15](15-l1-convergent-reading.md) has this confound directly.** Cross-model agreement on a
character could be (a) models converging on what the sheet says ← what we conclude, or (b) models
sharing a training-data stereotype about tsundere/goth/mentor archetypes. **These are currently
indistinguishable, and models are the most stereotype-saturated judges imaginable — shared
pretraining *is* shared priors.**

**Fix (cheap, one extra condition): score an archetype-only sheet** — strip the specifics, keep the
archetype label. If agreement barely drops, we were measuring S, not P. **This should gate the note-15
line of work.** (Same instinct as `rp-bench-anonymous-benchmarking.md`, generalized from *named
characters* to *archetypes*.)

### 3.4 Consensus ≠ accuracy

The framework uses "agreement" and "measurability" interchangeably. SRM keeps them separate and so
should we. Judges agreeing about a character does not make them right about it. For original
characters the sheet is the only ground truth — but note the sheet **underdetermines** most
interesting questions, which is precisely why L1.1's probes are interesting and precisely why they
won't have κ=.9.

### 3.5 Reliability of a difference score

L2.2's elasticity is a **difference score** (Δoutput/Δprompt). Classical result: **the reliability of
a difference between two correlated measures is low when the two measures are highly correlated** —
and our two conditions are *designed* to be nearly identical (one word apart). **Elasticity may be
close to unmeasurable at small doses**, not because the model is dead but because the estimator is.
This argues for **large doses and many rungs**, and for reporting the elasticity's own SEM. (Note 04
§2.4's "reliability is population-dependent" trap, in a new place.)

---

## 4. What to STEAL instead of inventing

Ordered by value.

### 4.1 ★ The measurement-mode study (Elliott's design) — the one study that decides L1's fate

Elliott's decisive move: measure the **same construct four ways** and correlate each with a real
outcome. **Do exactly this for character comprehension:**

| mode | our version |
|---|---|
| accuracy | L1 probe score vs the sheet |
| observer-rated | judge-rated in-character-ness |
| **client-rated** | **user reports the character "gets" them** ← Elliott says this one wins |

→ all against retention / thumbs-up / Q1.

**And test the range-restriction escape hatch** (§2.2): plot L1 vs Q1 across the model quality range.
If L1 predicts among weak models and flattens among frontier models, **say so and demote L1 to a
floor check.** That is cheap, decisive, publishable, and it is the framework's own best defence —
worth running rather than assuming.

### 4.2 ★ Fit an SRM on the corpus we already have — zero new generations

`model × character` with 11 models × 95 characters **is a round-robin.** Fit an SRM today and get the
actual size of our model×character interaction instead of worrying about it. Report:

```
σ²_model        ← is there a general "roleplay ability"?      (target-ish)
σ²_character    ← character difficulty                        (note 15's finding, properly modelled)
σ²_model×char   ← THE CHEMISTRY TERM. Kenny predicts it's the biggest.
```

**This directly answers the framework's loudest open worry, it costs nothing, and it slots into the
same mixed-effects infrastructure note 04 §3/§7.4/§8.4 already wants.** ⚠️ Caveat: γ_ij is only
identified with replications per cell — so **generate ≥2 samples per model×character**, which we
should be doing anyway for note 03's population tier. One design serves three notes.

Report consensus the SRM way — **target variance / total variance** — rather than as a κ. It's the
right statistic for "do judges agree about this character", it's what note 15 is groping toward, and
it makes our numbers comparable to a 40-year literature.

### 4.3 ★ Replace "consistency" with distributional fidelity — Fleeson gives us the metric

**Don't measure invariance. Measure whether the model reproduces the character's trait-state
*distribution*.** Fleeson found the stable things are the **central tendency** ("almost perfectly
stable") *and* the **amount of variability** ("stable individual differences" — including skew and
kurtosis).

```
L2.1 (rewritten):
  sample the character's trait-state across k situations
  compare the DISTRIBUTION (mean, SD, skew) to the sheet's implied distribution
  drift = distance between distributions, not deviation of any single act
```

**A character who is always 0.9 shy is broken. A character whose shyness has the right *mean and
spread* is alive.** This is strictly more informative than anchor-distance and it **reuses note 03's
population tier (k≥10 samples/scenario) exactly** — same generations, new statistic. Cheapest
high-value change in this note.

**And add CAPS's if-then profile stability as the real consistency metric:**

```
for each situation type s: profile[s] = trait expression
consistency := stability of the PROFILE across sessions   (not flatness of the profile)
```

Mischel & Shoda's summer-camp work shows *human* if-then profiles are stable and are "the essence of
personality coherence". **A character SHOULD be inconsistent across situations in a patterned way,
and the pattern is the thing to measure.** This also gives L2.1 a bound referent it currently lacks —
the profile is stable even though the behaviour isn't.

### 4.4 ★ Calibrate the elasticity x-axis; fit a power law; report an exponent per trait

1. **Use calibrated intensity as x**, not step index. Ruppenhofer et al.'s 14-adverb scale is
   published, free, and cross-adjective-stable (ρ > 0.900).
2. **Re-space the ladder.** A defensible ~equal-interval en ladder from that table:
   `slightly (30.5) → fairly (42.1) → pretty (52.5) → quite (59.9) → very (78.6) → extremely (91.1)`.
   **Drop "pathologically"** or run it as a separate *categorical* condition.
3. **Fit `ψ = kI^a` in log-log; report `a` per trait.** Stevens' exponents run **0.33 (brightness) to
   3.5 (electric shock)** in the *same organism*. **"Dead" and "brittle" are not pathologies — they
   are compressive and expansive exponents.** So steerability is a **model × trait** property, not a
   model score. Report the exponent vector; state in advance what exponent is too low to ship.
4. **Weber's law (ΔI/I = k):** the same word buys less at high baseline. Expect apparent curvature;
   don't over-read it.
5. **Run magnitude estimation for zh before any cross-language elasticity claim** — the Ruppenhofer
   scale is English. A Chinese *非常* is not an English *very* until measured. This is note 04 §5.3's
   RC-DIF problem in a new place, with the same fix (anchoring/calibration), and it's ~1 survey.

### 4.5 ★ Asch's warm/cold as ground truth for the off-diagonal

Stop treating crosstalk as a defect to minimize. **Replicate Asch's warm/cold manipulation on a
character sheet and compare the model's off-diagonal to Asch's human off-diagonal.** Asch found
crosstalk is **selective** — some traits moved, "another group of qualities ... not affected". That
selectivity pattern *is* a bound referent with 80 years of replication.

```
steerability matrix (rewritten):
  diagonal   → does the perturbed trait move?          (steerability)
  off-diagonal → does it move the traits Asch's subjects moved,
                 and leave alone the ones they left alone?   ← FIDELITY, not crosstalk
```

**This converts the framework's biggest unbounded engineering complaint into a bound comparison
against human data.** A model with zero crosstalk fails this test — correctly.

### 4.6 Ickes' scoring, verbatim

- **The 0/1/2 content-similarity scale.** Coarse, α≈.90. (Note 04 §1.3 settled on 0–5 from Li et al.
  2026 — a single unreplicated paper. Ickes goes coarser, on 40 years of data. Worth a bake-off.)
- **The denominator:** `accuracy points / (n_inferences × 2) × 100`. **A structural verbosity
  correction, not a covariate.** Note 03 calls length "THE BIGGEST TRAP IN THIS DOC" (r = 0.79–0.904
  with word count); Ickes solved it in 1990 by making the denominator *items attempted*.
- **Cross-target consistency as a first-class stat** — is a model good at character A also good at
  character B? **This is the test of whether "L1 ability" exists at all**, it's α across characters,
  and we can run it on the existing corpus. Ickes gets .86–.91; note 15's analogue tops out at .466.
- **Report agreement per-character, never pooled** — Ickes' own caveat ("homogeneity in the set of
  target persons") + our 4–5× range.

### 4.7 Bayesian nulls for the L1 dimensionality question

When we run the L1 inter-probe matrix (§5, item 2), **use Bayes factors.** "We found no correlation"
is unpersuasive; **BF01 > 10 is a result** and lets us make a positive claim about dimensionality.
Free upgrade to note 04 §4.1's discriminant matrix.

### 4.8 Names and citations we should be using

| ours | theirs | why it matters |
|---|---|---|
| L1 | **Empathic accuracy, standard stimulus paradigm** (Ickes) | 40 years of validation; our design *is* EA-SSP |
| the cascade | **Realistic Accuracy Model** (Funder 1995) | necessary + multiplicative stages |
| chemistry | **relationship variance** (Kenny) / **relationship moderator** (Funder) | measurable, and it's 30–40% |
| character difficulty | **good target** / **judgeability** | studied moderator |
| sheet quality | **good information** (quantity × quality) | gives us the style-guide hypothesis free |
| consistency | **personality coherence** / **if-then signatures** (Mischel & Shoda) | the construct we actually want |
| L2.2 | **magnitude estimation** / **Stevens' power law** | 150 years of method |
| steerability | **aptitude-treatment interaction** (Cronbach) | including its cautionary tale |

---

## 5. The rewrite this implies

**The framework survives, demoted and re-argued.** Concretely:

1. **Delete the agreement-gradient argument as a justification.** §1's "*the two layers that gate
   everything are exactly the two we can measure with high agreement*" is the load-bearing error.
   Replace with the honest version:

   > L1 and L2 are **cheap, reliable, diagnostic instruments for debugging a failure.** They are
   > **not** proxies for quality and must never become ship gates or optimization targets. The thing
   > that predicts whether the product works is perspectival, expensive, needs real users, and cannot
   > be subtracted away.

   **This is compatible with almost everything else the document says.** §5's "Deliverable: a
   diagnosis + a character-sheet style guide" is *exactly* right and already there. What must go is
   the claim that boundedness makes L1/L2 the layers that *matter*. **They are the layers we can
   afford.** Different property.

2. **Split L1, and expect it not to be a scalar.** Report `L1-recognition` (forced-choice: *"which
   response is more in-character?"*) and `L1-inference` (open-ended: *"what would they never
   admit?"*) **separately**. Five literatures say they won't correlate; one gives the mechanism
   (pattern-matching vs perspective-taking-from-context). **Run the inter-probe matrix with Bayes
   factors before publishing any pooled L1 number.**

3. **Report L1 as `model × sheet`**, with sheet-side variance broken out. RAM's relevance and
   availability are the sheet's, not the model's.

4. **Stratify every L1/L2 number by trait observability.** Behavioural/external traits → expect
   agreement and stability. Internal traits → expect interaction dominance. Never pool.

5. **Rewrite L2.1** from invariance to distributional fidelity + if-then profile stability (§4.3).

6. **Rewrite L2.2's off-diagonal** from "crosstalk = defect" to "crosstalk vs Asch's human
   off-diagonal = fidelity" (§4.5). Calibrate the x-axis (§4.4). Report an exponent per trait.

7. **Delete "nobody has checked it for character sheets"** from L2.3. Asch checked position effects
   in 1946.

8. **Promote chemistry from a worry to a reported quantity.** Fit the SRM (§4.2). If σ²_model×char
   dominates — and Kenny predicts it will — that is a structural ceiling on the leaderboard and it
   belongs in BENCHMARKS.md.

9. **Add the motivation column to L1.2**, and the accuracy-incentive condition that separates it.

10. **Gate note 15 on the archetype-only control** (§3.3). Right now its agreement may be shared
    pretraining stereotype, and Kenny says at low acquaintance that's 100% of the effect.

---

## 6. Honest limitations of this note

- **The strongest counter-evidence (Elliott) is range-restricted** and I've flagged it in-line rather
  than buried it. Trained therapists all cleared a competence bar; our models have not. **§4.1's
  range test is the honest way to settle it, and it may well vindicate L1.** I have not settled it
  here.
- **The acting/actor evidence is about humans**, whose portrayal bottleneck (body, nerves, stage
  fright, self-consciousness) an LLM does not have. The comprehension→portrayal dissociation may not
  transfer. **But the framework cannot both dismiss this and claim psychological warrant for the
  cascade.**
- **κ vs variance-ratio is a real apples/oranges problem.** Kenny's .20–.40 consensus is a variance
  ratio on trait ratings of *real people*; our κ is on discrete probes against a *written sheet*
  that is fully available to every judge. Our task genuinely is easier on RAM's availability stage.
  **The comparison is directional, not exact** — but note 15's own numbers (max .466) side with Kenny.
- **Brown et al. (2019) is n=15, one fMRI study, one play.** The "acting ≠ ToM" dissociation is
  suggestive, not established. Don't over-lean on it.
- **Ruppenhofer et al.'s adverb scale is English, crowd-sourced, and 2015.** It's the best available
  calibration, not a law. The zh scale genuinely does not exist and we would have to build it.
- **RAM assumes traits are real** ("RAM begins with the assumption that personality traits are real
  attributes of individuals"). Mischel/CAPS/Fleeson are the other side. **I have cited both as
  support for different parts of our framework, which is slightly opportunistic.** The tension is
  real and unresolved in psychology itself; the resolution (coherence, not invariance) is what §4.3
  operationalizes.
- **Not covered:** HEXACO specifics; the Adler/Strasberg split in depth; Goldstein & Winner's
  acting-training→ToM causal work (the reverse-causation lead — *does portrayal training produce
  understanding?* — which if true inverts our arrow and is the most interesting untested thing here);
  difference-score reliability worked through with the actual formula (§3.5 states it qualitatively);
  psychometrics of rating "in-character-ness" (searched; the literature is thin to nonexistent —
  **which is itself a finding: nobody has established that "in-character" is a reliably rateable
  construct, and we are about to assume it is**).
