---
title: "Empathic accuracy: measurement and potential clinical applications"
url: https://iris.unil.ch/bitstreams/ff2b8ba9-235e-41ea-9a1d-93ac328f65cc/download
secondary_url: https://www.researchgate.net/publication/255961565_Empathic_accuracy_Measurement_and_potential_clinical_applications
authors: Marianne Schmid Mast; William Ickes
year: 2007
type: method / book chapter (in Farrow & Woodruff, eds., Empathy in Mental Illness, CUP)
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Empathic Accuracy — the 40-year validated paradigm that IS our L1

**This is the single most directly relevant prior art for L1 (character comprehension).** Ickes'
group has been operationalizing "how accurately can one mind read another mind from a description
of behavior" since the late 1980s. We are re-inventing it. This file captures the paradigm, the
scoring formula, and — most importantly — **the reliability/validity split that should scare us.**

---

## 1. The construct

Empathic accuracy = "everyday mind reading". Ickes' framing:

> "Empathic inference, or 'everyday mind reading,' is a form of complex psychological inference in
> which observation, memory, knowledge, and reasoning are combined to yield insights into the
> subjective experience of others."

Note what this is **not**: it is not self-reported empathy, not a disposition, not a feeling. It is a
**performance measure with a scored right answer**. That is exactly the move our L1 makes.

---

## 2. The two paradigms — and they map onto our two design options

### 2.1 The (unstructured) dyadic interaction paradigm

Two people interact spontaneously while the experimenter is absent; the interaction is videotaped.
Then, separately:

> "The participants view the entire interaction and stop the tape at each of those points at which
> they distinctly remember having had a specific thought or feeling. At each of these 'tape stops',
> the participants use a coding form to record: (1) the time the thought or feeling occurred
> (available from a time-counter overlay that is superimposed on the video image), (2) whether they
> were experiencing a thought or a feeling at that time, and (3) the specific content of the thought
> or feeling, expressed in sentence form."

Then the inference pass:

> "The participants are then asked to view the tape a second time, this time for the purpose of
> inferring the specific thoughts and feelings that their interaction partner reported having had at
> each of his or her tape stops. The research assistant who is seated in the control room pauses the
> tape at each of the times the participant's interaction partner reported having had a specific
> thought or feeling."

**Crucial design property: the target generates the ground truth, not the experimenter.** The
referent is the target's own self-reported thought at a timestamp. This is the cleanest available
answer to "where does the right answer come from?" — and it is the answer we do *not* have, because
our character sheets are static and our characters cannot self-report.

### 2.2 The standard stimulus paradigm (EA-SSP)

> "In the standard stimulus paradigm, individual participants each view the same standard set of
> videotaped interactions and attempt to infer the thoughts and feelings of the same set of target
> persons."

Prototype: Marangoni et al. (1995) — three female clients each discussed "a genuine personal
problem" with a male client-centred therapist; each client then made "a complete, video-cued record
of all her thoughts and feelings during the interaction". The edited tapes became the standard
stimuli.

**This is our design.** Fixed stimulus set, many perceivers, same referent, scored against a fixed
key. **Every model sees the same character sheet** = the standard stimulus paradigm with models as
perceivers. We should say so and cite it.

---

## 3. The scoring system — steal this verbatim

> "The raters' task is to compare each actual thought or feeling with the inferred thought or
> feeling and to judge how similar they are on a scale from 0 to 2. A rating of 0 is assigned if
> there is no apparent similarity in the content of the actual thought/feeling compared to the
> inferred thought/feeling; a rating of 2 is assigned if the same content is evident (though
> paraphrased or expressed in different words); and a score of 1 is assigned to all of the 'grey
> area' cases in between."

**The 3-point 0/1/2 content-similarity scale is the whole instrument.** Note it is deliberately
*coarse*. Compare note 04's finding that 0–5 beats 1–10/1–100; Ickes goes coarser still and gets
α≈.90.

### The formula — and its built-in verbosity correction

> "For each inference, the similarity ratings of all of the independent raters are averaged. In a
> next step, those averaged ratings are summed up across all inferences to compute the 'total
> accuracy points' earned by each perceiver. **It is important to recognize that the 'total accuracy
> points' will be greater for perceivers who make many inferences than for those who make few
> inferences.** Therefore, each perceiver's 'total accuracy points' is divided by the maximum number
> of possible accuracy points (number of inferences times the maximum score per inference) and
> multiplied by 100 to obtain a percent-correct empathic accuracy measure that has a potential range
> of 0 to 100."

```
EA% = ( Σ_inferences mean_rater_similarity ) / ( n_inferences × 2 ) × 100
```

> "This percentage measure of empathic accuracy is conveniently scaled, easy to interpret and
> **corrects reasonably well for differences in the total number of inferences made**."

**Note 03 §3 A3 flags length/verbosity as "THE BIGGEST TRAP IN THIS DOC" (0.79–0.904 correlation with
word count). Ickes solved it in 1990 by making the denominator the number of inferences attempted.**
That is a real, cheap, structural fix — not a post-hoc regression control. Our L1 probes should be
scored the same way: a fixed denominator of *probe items attempted*, never a free-text volume.

---

## 4. Reliability — the numbers that make L1 look great

**Inter-rater reliability:**

> "Interrater reliability in empathic accuracy studies has consistently been quite high (Cronbach's
> alpha), ranging from a low of **0.85** in a study in which only four raters were used to a high of
> **0.98** in two studies in which either seven or eight raters were used. Across all of the studies
> conducted to date, **the average interrater reliability has been about 0.90** (Ickes, 2001)."

**Cross-target consistency** (standard stimulus paradigm only — does a perceiver who is accurate
about target A stay accurate about target B?):

> "Cross-target consistency in the first standard stimulus study conducted by Marangoni et al.
> (1995) was **0.86** (Cronbach's alpha) across the three target tapes used. In a more recent study
> using highly edited versions of the same three tapes, Gesn and Ickes (1999) reported an alpha of
> **0.91**."

> "the average inter-target correlation of the perceivers' empathic accuracy scores (**0.60**) was
> impressively high in this study" (Marangoni et al. 1995, n=80).

⚠️ **Ickes himself flags the confound, and it is exactly our confound:**

> "These high alpha values might be partly attributable to **homogeneity in the set of target
> persons** (all three were middle-class, college-educated, Anglo-American women) and in the
> problems they discussed (women's relationship issues)."

**Read that against note 15.** Our own result — cross-model agreement per character spans 0.052→0.213
(en) and 0.086→0.466 (zh), a 4–5× range — is *the same phenomenon*: agreement is a property of the
**target set**, not of the instrument. Ickes' α≈.90 is partly an artifact of picking three similar
targets. **Any L1 agreement number we publish is conditional on our character sample and must be
reported per-character, not pooled.** Our 95 characters are far more heterogeneous than Ickes' three
women, so **we should expect materially lower agreement than his α≈.90 — and lower than the
κ≈0.78–0.94 the ability model assumes.**

---

## 5. Validity — the numbers that should scare us ★★★

This is the most important section in this file.

**Predictive validity: passes.**

> "the empathic accuracy scores of close, same-sex friends were about **50% higher** than those of
> same-sex strangers – a statistically significant difference in both studies" (Stinson & Ickes 1992;
> Graham 1994).

Marangoni et al. (1995) further confirmed: accuracy rises across a tape (acquaintance), and
perceivers given **immediate feedback** mid-tape scored significantly better by the end. (→ EA is
*trainable*, which matters for the "is this a capability or a prompt problem" question.)

**Convergent/discriminant validity: FAILS.**

> "Establishing the convergent and discriminant validity of the empathic accuracy measure has proven
> to be **more difficult and complicated**. Davis and Kraus (1997) found that **self-report measures
> of empathically relevant dispositions generally fail to predict performance** on interpersonal
> accuracy/sensitivity tests."

> "Mortimer (1996) failed to find a predicted relationship between participants' scores on a
> cross-target measure of empathic accuracy ... and their scores on Costanzo and Archer's (1989)
> interpersonal perception task – the interpersonal sensitivity measure that (superficially, at
> least) most resembles the empathic accuracy measure in its stimulus materials and available
> channels of information. **The correlation that Mortimor (1996) obtained was not significantly
> different from zero (r = 0.06).**"

> "This null result is **similar to that reported by other investigators who have attempted to
> correlate different performance measures of interpersonal sensitivity with each other** (Hall,
> 2001). The explanation for these null findings is not yet clear. **It is possible that different
> types of interpersonal sensitivity exist that are not necessarily related to each other.**"

### Why this is the most important finding in this file

**α = 0.90 and r = 0.06 in the same instrument.**

The ability model's core argument is: *L1 is bound to a referent ⇒ high agreement (κ 0.78–0.94) ⇒ we
can measure it.* Empathic accuracy is the 40-year proof that **the inference does not go through.**
EA is maximally bound — the referent is the target's own timestamped self-report — and it achieves
α≈.90 *inter-rater*. And yet **two "mind-reading ability" tests that both have α≈.90 correlate r≈.06
with each other.**

High rater agreement means **raters agree about whether inference X matches thought Y**. It says
*nothing* about whether "comprehension" is one thing. **Boundedness buys reliability, not validity.**
Note 04 §2.5 already has the machinery for this (the validity ceiling `√(ρ_xx'·ρ_yy')`); the point
here is stronger and worse — the ceiling is *not* the binding constraint. With ρ≈.90 on both
measures, the permitted correlation is ≈.90, and the observed correlation is **.06**. That is not
attenuation. **That is two different constructs wearing the same name.**

**Implication for the ability model:** "L1 comprehension" is very likely **not a single ability**.
Our L1.1 probe suite (*what do they want that they'd never admit?* / *what would they do if X?* /
*which response is more in-character?* / *what's the contradiction?*) is **four plausibly unrelated
tests**. EA + Hall (2001) predict they will **not** correlate. We must run the inter-probe
correlation matrix (note 04 §4.1's discriminant matrix, pointed at L1) **before** reporting a scalar
L1 score — and be prepared for the answer that there is no such scalar.

---

## 6. Motivated inaccuracy — the human version of "knows better than it acts" ★

Simpson et al. (1995): dating partners audibly rated photos of opposite-sex others for
attractiveness in front of each other; high-threat (all attractive photos) vs low-threat (all
unattractive). Then the standard EA procedure on the covert videotape.

> "the partners in the high-threat condition ... would be less accurate in their attempts to infer
> each other's thoughts and feelings ... The results confirmed this effect, which was particularly
> evident for the insecure yet mutually dependent couples ... their average level of empathic
> accuracy was **significantly worse than that of total strangers and not significantly greater than
> chance**."

Dating partners — who by the friends-vs-strangers finding should be **~50% more accurate** — dropped
**to chance** when accuracy was threatening. Capability unchanged; performance collapsed.

**This is exactly row 2 of the L1.2 discrimination/generation table ("knows better than it acts"),
and it is a real, replicated human phenomenon with a name: `motivated inaccuracy`.** It vindicates
L1.2 as a *design* — the discrimination/generation gap is a genuine dissociation, not an artifact.
But it also warns: **the gap's cause need not be "decoding, prompt, sampling" (cheap).** In humans
the cause is an *objective function* — the perceiver is optimizing something other than accuracy.
An RLHF'd model that is being agreeable rather than in-character is doing **motivated inaccuracy**,
and that is not a sampling fix. Add a third column to the L1.2 table.

Relatedly, the gender finding (Wikipedia summary of Klein & Hodges 2001): women outperform men on EA,
but "these differences were dramatically diminished when couples received money for correct
identifications", suggesting "men and women are very similar ... in skill, but differ in
**motivation**". **Ability vs motivation is measurable by paying for accuracy.** The model analogue
is an explicit instruction/incentive condition — cheap, and it separates capability from disposition
better than our current L1.2 design does.

---

## 7. Performance levels — calibrate expectations

Typical EA scores (Ickes, *Everyday Mind Reading*): roughly **.20 for strangers, ~.30 for close
friends** on the 0–1.00 index — i.e. **20–30% correct.** Humans are *bad* at this.

**We should not expect, or demand, high absolute L1 scores**, and we should be suspicious if we get
them — it would suggest the probes are easy rather than that the model is good. Ickes' construct is
useful because it *discriminates*, not because anyone passes it.

---

## 8. What to steal, concretely

| # | Steal | Where it goes |
|---|---|---|
| 1 | **The name and the citation.** Call L1 what it is: empathic accuracy under a standard stimulus paradigm. 40 years of validation is free credibility. | ABILITY-MODEL §2 |
| 2 | **The 0/1/2 content-similarity scale.** Coarse, α≈.90, cheaper than our 0–5. | L1 rubric |
| 3 | **The denominator.** `accuracy points / (n_inferences × 2)`. Structural verbosity correction, not a covariate. | L1 scoring |
| 4 | **Cross-target consistency as a first-class stat.** Is a model that reads character A well also good at character B? α across characters. **This is the test of whether "L1 ability" exists at all**, and we can run it on the existing corpus. | note 15 follow-up |
| 5 | **The feedback manipulation.** Marangoni: mid-tape feedback improves EA. Model analogue = in-context correction. Separates "can't" from "didn't". | L1.2 |
| 6 | **Paying for accuracy.** Klein & Hodges: incentives erase the gender gap ⇒ it was motivation not skill. Model analogue = explicit accuracy instruction. | L1.2 third column |
| 7 | **Report agreement per-target, never pooled.** Ickes' own homogeneity caveat + our note 15 range (4–5×). | every L1 number |

## 9. What it breaks

- **"Bound ⇒ measurable" is half-true.** Bound ⇒ *reliable*. Bound ⇏ *valid*, and ⇏ unidimensional.
  α=.90 with r=.06 convergence is the counterexample. **The ability model's §1 agreement-gradient
  argument needs this caveat or it is overclaiming.**
- **κ≈0.78–0.94 for L1 is probably too optimistic for our corpus.** Ickes gets α≈.90 on *three
  demographically identical targets*; we have 95 heterogeneous characters in 2 languages, and note 15
  already measured a 4–5× spread in per-character agreement.
- **"L1 comprehension" may not be a scalar.** Run the inter-probe correlation matrix first.
