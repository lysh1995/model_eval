---
title: "Psychometrics of rating 'in-character-ness' — standardized-patient portrayal accuracy, fictional-character personality ratings, and performance rubrics"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC4035823/
authors: Vora et al. / Wallach et al. (SP portrayal accuracy, 2014); Rasmussen (movie characters, 2005); Kowert et al. (Game of Thrones, 2022)
year: 2005-2022
type: paper / review
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Can humans reliably judge whether a performance is "in character"?

**The direct empirical test of the framework's L1 measurability claim.** The framework asserts κ ≈ 0.78–0.94 for L1 because it is "bound" to the character sheet as a referent. This file assembles the closest published analogues. Verdict: **the claim is achievable but only under conditions the framework has not specified — and it is flatly false for whole classes of character attributes.**

There are three relevant literatures. They disagree with each other in an informative way.

---

## 1. Standardized-patient portrayal accuracy — THE closest analogue, and it SUPPORTS the framework

**"Accuracy of portrayal by standardized patients: results from four OSCE stations conducted for high stakes examinations", *BMC Medical Education* (2014), 14:97.**

This is as close as medicine gets to our exact problem: **a trained human is given a written character brief (the case) and must stay in character; independent raters score whether the portrayal was faithful.** That is L1 + L2, assessed, at high stakes.

### Design
- 142 IMG candidates (68F/74M; 109 passed), **4 stations** drawn from a 10-station OSCE, videotaped.
- **4 assessment tracks × 4 SPs per case = 16 SPs total.**
- 6 SP–candidate interactions per track (3 morning, 3 afternoon).
- **Two physician assessors** scored independently; a third resolved disagreements; mode used for analysis.

### The instrument — note how concrete it is
- Case-specific items on **verbal and physical portrayal**.
- **3-point scale with explicit anchors: "yes" / "yes, but" / "not done".**
- Plus a 5-point anchored global rating: "very poor" / "poor" / "ok" / "good" / "very good".
- Items assess concrete manifestations: tone of voice, facial expressions, physical demonstrations, whether specific concerns were expressed.

### Reliability results

> Cohen's Kappa **"ranged from 0.80 to 0.89 for all the four cases"**

> **"85% agreement between the two physician assessors"**

**This is the framework's claimed band, essentially confirmed — κ 0.80–0.89 vs. our claimed 0.78–0.94.** So the claim is *not* fantasy. But look hard at what bought it:
- Behaviourally-anchored, **binary-ish** items ("did they say X?" — yes / yes-but / not done)
- **Concrete, observable** targets (verbal content, tone, physical actions)
- Trained physician raters
- Video, i.e. full information
- Case-specific checklists written alongside the script

**Every one of those is a design choice, not a property of "having a referent."**

### THE CRITICAL NUANCE — two dissociations the framework must not miss

**(a) Internal consistency was POOR even where inter-rater agreement was excellent.**

Cronbach's alpha by case: **Case A 0.744, Case B 0.40, Case C 0.41, Case D 0.56.**

**Raters agreed with each other (κ .80–.89) on items that did not hang together as a scale (α .40–.56).** These measure different things: κ says "we agree on this item"; α says "these items measure one construct." **You can have near-perfect agreement about a set of items that do not constitute a coherent construct.** If our L1 rubric reports κ but not α, we may be reporting excellent agreement about a bag of unrelated observations and calling it "comprehension."

**(b) Rater agreement was high; PERFORMER consistency was not.**

> "There was full agreement on verbal portrayal and facial expressions across all cases with the only disagreement on cases where the videos were not clear"

But:

> **"the facial expressions of the SPs differed significantly (p < .05)"**

> Case B, an emergency management station, "differed between all four SPs"; Case D showed significant differences in discussing relationship concerns (p = 0.046).

Conclusion, verbatim:

> **"Variation of trained SP portrayal of the same station across different tracks and at different times in OSCE may contribute substantial error to OSCE assessments. The training of SPs should be strengthened and constantly monitored during the exam to ensure that the examinees' scores are a true reflection of their competency and devoid of exam errors."**

**Read this carefully — it is the most important result in this file.** *Trained professional humans, given the same written character brief and explicitly paid to portray it identically, portrayed it significantly differently from one another.* The raters agreed perfectly *that* the portrayals differed. **The measurement was reliable; the character instantiation was not.**

**This is the ceiling on our L2. High inter-rater agreement at L1 does not imply low variance at L2 — and the SP literature shows the L2 variance is large enough to be the dominant error term in a high-stakes exam, even with trained humans.**

### Corroborating: SPs as raters

> "a single SP predicted to generate scores with a reliability of **0.74**, whereas a single non-SP rater's scores were predicted at a reliability of **0.40**"
> — *Interrater Reliability of Standardized Actors Versus Nonactors in a Simulation Based Assessment of Interprofessional Collaboration*, Simulation in Healthcare

**Training/role-immersion nearly doubles single-rater reliability (.40 → .74).** Consistent with the frame-of-reference training literature (`psych-trait-visibility-judgeability.md`, d ≈ .77).

---

## 2. Rating personality of FICTIONAL characters — and here the framework's claim COLLAPSES

**"Rating of personality disorder features in popular movie characters", *BMC Psychiatry* (2005), 5:45.**

### Design
- **8 psychology students** (4M/4F), University of Copenhagen, all having completed courses in personality psychology, psychiatry, and clinical psychology.
- **4 movie characters:** Sarah Morton (*Swimming Pool*), Aileen Wuornos (*Monster*), Suzanne Stone (*To Die For*), Coleman Silk (*The Human Stain*).
- **Three instruments:** global rating scales for 10 DSM-IV personality disorders (0–100); 79 DSM-IV criteria in random order (0–2); the **Ten Item Personality Inventory (TIPI)** for the Big Five.

### Results — ICC by instrument

> **"agreement for the five-factor model ranged from 0.05 to 0.88"**

**Big Five (TIPI) inter-rater ICC — verified against Table 1:**

| Trait | ICC |
|---|---|
| **Extraversion** | **0.88** |
| Conscientiousness | 0.68 |
| Agreeableness | 0.50 |
| Neuroticism | 0.37 |
| **Openness** | **0.05** |

- **Personality disorder rating scales:** range **0.04–0.54** (antisocial 0.54 highest; dependent 0.04 lowest)
- **DSM-IV criteria counts:** range **0.24–0.89** (narcissistic 0.89 highest; paranoid 0.24 lowest)

Ordering of instruments: **criteria count > TIPI > global rating scales.** Raters found "personality disorder criteria easiest and global personality disorder scales most difficult."

Abstract conclusion:

> "Psychology students with limited or no clinical experience can agree well on the personality traits of movie characters based on watching the movie. Rating movie characters may be a way to practice assessment of personality."

**Note the abstract oversells its own data.** "Can agree well" is true of Extraversion (.88) and false of Openness (.05). **An 18-fold spread on one instrument, same raters, same targets, same session.**

### Why this is the single most damaging result for the L1 claim

Every condition the framework relies on was satisfied:
- ✅ Fixed referent (the film — richer than a character sheet)
- ✅ Fictional character (our exact target class)
- ✅ Trained-ish raters
- ✅ Standard validated instrument

**And agreement still ranged 0.05 to 0.88.** The referent did not deliver uniformity. It delivered the **trait-visibility ordering** exactly as Funder/John & Robins predict: visible→high, internal→zero.

### At scale: Game of Thrones

**"Personality Perception in Game of Thrones: Character Consensus and Assumed Similarity", *Psychology of Popular Media* (2022).**

- **309 fans** recruited from 3 subreddits rated **56 characters** on Big Five + Dark Tetrad.

> "Consensus correlations were significant for all Big Five and Dark Tetrad traits, ranging from **.54 for narcissism to .83 for agreeableness (M = .66, SD = .10)**."

> "Assumed similarity slopes were positive (range: **.07–.29; M = .15, SD = .06**) and significant for all traits except conscientiousness and open-mindedness. Thus, raters reliably assumed that characters were similar to themselves on 7 of 9 traits."

Also: significant **sex-of-perceiver** effects for conscientiousness, open-mindedness, and Machiavellianism — women perceived characters as higher on these than men did.

**Three lessons:**
1. **Massive aggregation compresses the spread** (.54–.83 with N=309 vs .05–.88 with N=8) — Spearman-Brown at work. Agreement is partly a budget line.
2. **Even at N=309, the range is ~1.5× and trait-dependent.** Aggregation narrows; it does not equalize.
3. **"Assumed similarity" is a rater bias we will inherit**: raters project themselves onto characters (slopes .07–.29). Plus systematic **rater-demographic** effects. Our human L1 baseline will carry both.

---

## 3. Theatre/performance assessment — thin evidence, be honest about it

Searches for peer-reviewed inter-rater reliability on acting/audition assessment turned up **mostly instruments, not psychometrics**: e.g. the [ChiArts theatre audition rubric](http://chiarts.org/wp-content/uploads/2016/11/Sample_ACTING_Audition_Rubric.pdf) and similar district rubrics, which rate dimensions like concentration, physical expression, and character work — but publish no reliability data.

**Assessment: there is no substantial published inter-rater reliability literature for "in character" judgments in drama/theatre.** Do not cite theatre rubrics as evidence for our κ claim; they are existence proofs that people *build* such rubrics, not that the rubrics agree. The SP/OSCE literature is the defensible analogue and should be cited instead.

---

## Implications for our framework

1. **The κ 0.78–0.94 claim is achievable — but it is a claim about the RUBRIC, not about L1.** The SP literature hits κ .80–.89 on exactly this task. But it earns that with 3-point anchored items ("yes / yes, but / not done") over **concrete verbal and physical behaviours**, with trained raters and full video. Our framework attributes its κ to L1 being "bound to the character sheet as a referent." **That attribution is wrong, and the movie-character study is the counterexample: same binding, ICC .05.** The κ comes from *item concreteness and anchoring*, not from the existence of a referent. This matters because it changes what we must do to keep the κ: we must engineer the items, not merely point at the sheet.

2. **Predicted κ profile for our L1 rubric — the uniform band will not survive.**
   - Sheet-fact recall, catchphrases, register, stated backstory, refusal boundaries → **κ .80–.90** (SP-like: concrete, verbal, anchored)
   - Sociability/extraversion-like manifestations → **κ ≈ .85**
   - Conscientiousness-like → **κ ≈ .65**
   - Agreeableness-like (evaluative) → **κ ≈ .50**
   - Neuroticism/inner states, motivation, "depth" → **κ ≈ .35**
   - Openness/curiosity/imagination → **κ ≈ .05–.30**
   
   **Recommendation: report κ per attribute class and drop the single band.** A stratified claim is both more honest and more defensible than a uniform one — and it's a stronger scientific contribution, because it tells authors which parts of a sheet are gradeable.

3. **Report α alongside κ — the SP study shows they dissociate badly.** κ .80–.89 with α .40–.56 means raters agreed about items that don't form a construct. If our L1 rubric reports only κ, we could be reporting high agreement about an incoherent bag of observations and calling it "comprehension." **Two numbers, always.**

4. **The SP portrayal-variance result caps L2 and should reframe the roadmap.** Trained professionals, paid to portray an identical brief, differed significantly from each other (p<.05; on one station, all four differed). **Human character instantiation from a written brief is itself high-variance** — this is the *human baseline* for L2 steerability, and it is not near-zero. Two consequences: (a) a model that varies across runs may be at or below human variance, so **we need the human variance baseline before calling model variance a defect**; (b) the SP conclusion — "may contribute substantial error to... assessments" — warns that *character-instantiation variance can become the dominant error term in the whole eval*, swamping the model differences we're trying to detect.

5. **Instrument format dominates — and the ordering is a free design win.** Criteria-count (.24–.89) > TIPI (.05–.88) > global scales (.04–.54). Raters found **discrete criteria easiest and global scales hardest**. This exactly parallels the SP design (concrete 3-point items) succeeding. **Design L1 as a criteria checklist, never as global Likert impressions.** This is the cheapest available κ improvement and it's supported by two independent literatures.

6. **Budget raters deliberately.** N=8 → .05–.88; N=309 → .54–.83. Spearman-Brown means our κ is partly a purchasing decision. But aggregation improves the *precision of the consensus*, not the *judgeability of the trait* — 300 raters agreeing about a character's Openness may be measuring shared stereotype rather than anything in the text. **Reliability is not validity, and on low-visibility traits, buying reliability can actively disguise a validity problem.**

7. **Expect rater-projection and rater-demographic bias in our human baseline.** GoT: assumed-similarity slopes .07–.29 on 7 of 9 traits, plus significant sex-of-perceiver effects. Our human L1 gold labels will contain both. If we then score models against those labels, **we will be scoring models on their ability to match human raters' projections of themselves onto the character** — worth naming explicitly, and worth measuring by collecting rater personality alongside ratings (a cheap addition that would let us *correct* for it).
