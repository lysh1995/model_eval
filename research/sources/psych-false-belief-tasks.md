---
title: "The classic ToM paradigms: Sally-Anne, Smarties, Faux Pas, Strange Stories — paradigms and psychometrics"
url: https://srcd.onlinelibrary.wiley.com/doi/10.1111/1467-8624.00304
authors: Wimmer & Perner (1983); Baron-Cohen, Leslie & Frith (1985); Perner, Leekam & Wimmer (1987); Happé (1994); Baron-Cohen et al. (1999); Wellman, Cross & Watson (2001); Devine & Hughes (2016)
year: 1983-2016
type: method
accessed: 2026-07-16
topic: psychology-crosscheck
---

# The classic paradigms — and the one place where ToM measurement actually works

**Read this file alongside `psych-tom-task-convergence.md`. This one contains the counter-evidence to
the "ToM doesn't converge" story, and it is the framework's strongest defense.**

## The paradigms

### Unexpected Transfer (Sally-Anne) — Wimmer & Perner 1983; Baron-Cohen, Leslie & Frith 1985

Ullman's description:

> "a participant sees or is told of a person who observes a particular state of affairs. The state of
> affairs then changes, without the person being aware. The participant is then asked what action the
> person will take. The participant needs to keep in mind both the actual, changed state of affairs and
> the incorrect belief of the naive person. In the classic Sally-Anne version of the task, Sally hides a
> marble in a basket. Anne then moves the marble to a box, without Sally's knowledge. A participant is
> then asked where Sally will look for her marble."

Warnell & Redcay's administration: "False belief location: an object was moved unbeknownst to a
character, and children were asked where the character would look (2 trials presented)"; "Second-order
false belief: Children had to predict where a third character thought the protagonist would look for an
object that was moved unbeknownst to the protagonist (2 trials presented)"

### Unexpected Contents (Smarties) — Perner, Leekam & Wimmer 1987

Ullman's description:

> "this assessment of ToM shows a participant a container (e.g. a crayon box). The container typically
> contains some item (e.g. crayons), but in this particular case it contains an unexpected item (e.g.,
> smarties). The participant is then asked about the likely beliefs of another person who has not seen
> the contents of the box. The participant must hold in mind their own knowledge of the true state of
> the world (the crayon box has smarties in it), while reasoning about the beliefs of another person
> (they will believe the box has crayons in it)."

Warnell & Redcay: "False belief content: a box contained an object different from that on the label,
and children were asked what a character would think was in the box (2 trials presented)"

**Note the structural feature both paradigms share**: a *self/other* split plus a *time* split. The
participant knows X; the character knows ¬X; the participant must suppress their own knowledge. This
is the "curse of knowledge" architecture, and it is what makes the task hard.

### Faux Pas Recognition Test — Baron-Cohen et al. 1999

> "Children listened to four short vignettes that each presented a social scenario and had to identify
> whether a faux pas was committed and, if so, why it was a faux pas." (six-year-olds; eight vignettes
> for ages 7-12)

Requires **two** mental states simultaneously: the speaker doesn't know they've caused offense
(ignorance), and the listener is hurt (affect). This is why Strachan et al. found it uniquely hard for
GPT-4 (see `psych-competence-performance-tom.md`).

### Strange Stories — Happé 1994; White et al. 2009

> "children were presented vignettes containing mental states (e.g., white lie, double cross) and had to
> identify the motivation behind characters' statements" — open-ended justification, scored by rubric.

> "Children listened to eight stories involving mental states (e.g., double crossing, white lie) and
> were asked to explain the motivation behind a character's statement."

Key design feature: Strange Stories includes **matched physical-control stories** with equivalent
narrative complexity but no mental-state content. The score of interest is mental minus physical. Same
subtract-a-matched-control logic as Warnell & Redcay's adult composites.

## Psychometrics — the good news

### Wellman, Cross & Watson 2001 — the false-belief meta-analysis (Child Development 72(3):655-684)

**178 separate studies.** https://home.cs.colorado.edu/~mozer/Teaching/syllabi/3702/readings/WellmanCrossWatson2001.pdf

> "A combined model including age, country of origin, and four task factors accounted for **55 percent
> of the variance** in false-belief performance."

> "false-belief results cluster systematically with the exception of only a few outliers"

Age effect: "correct responses increasing from below chance at 3 years to above chance by 5 years."

Conclusion: findings are "consistent with theoretical accounts proposing that understanding of belief
exhibit conceptual change in the preschool years" — refuting early-competence accounts.

**55% of variance explained is a genuinely strong result.** Within the false-belief paradigm, performance
is lawful, developmentally ordered, and cross-culturally robust. This is what a real construct looks
like.

### Devine & Hughes 2016 — the best psychometric case in the ToM literature

"Measuring theory of mind across middle childhood: Reliability and validity of the Silent Films and
Strange Stories tasks," *J Experimental Child Psychology* 149:23-40 —
https://pubmed.ncbi.nlm.nih.gov/26255713/

Design: **"460 ethnically and socially diverse children (211 boys) between 7 and 13 years of age"** tested
**"at two time points separated by 1 month."**

Findings (verbatim):

> "all items loaded onto a **single theory-of-mind latent factor**."

> "the Strange Stories and Silent Film tasks were **strongly correlated even when verbal ability and
> narrative comprehension were taken into account**"

> the latent factor "exhibited **strong 1-month test-retest reliability**, and this stability did not
> vary as a function of child characteristics."

> "showed **no evidence of differential item functioning** across gender, ethnicity, or socioeconomic
> status."

> "provide evidence for the validity and reliability of the Strange Stories and Silent Film task battery
> as a measure of individual differences in theory of mind suitable for use across middle childhood."

**This is a fully successful measurement instrument**: unidimensional, reliable over time, discriminant
against verbal ability, and fair across demographics (cf. `psycho-measurement-invariance-dif.md`). It
is everything RMET is not.

### Faux Pas / Strange Stories inter-rater reliability

From the Swedish population-based psychometric study: "The intraclass correlation coefficient of the
faux pas stories of the Faux Pas Recognition test was **0.996**, and that of the Strange Stories test was
**0.911**."

These are *scoring* reliabilities (rater agreement on open-ended responses) — near-perfect. Note this is
the "bound ⇒ high agreement" claim being **fully vindicated**, and note equally that it says nothing
about convergent validity, which is where these same tasks fail.

## The reconciliation — why this file and `psych-tom-task-convergence.md` are both right

The two literatures are not in conflict once you see the boundary:

| Scope | Coherence | Evidence |
|---|---|---|
| **Within one paradigm** (false-belief location/contents/2nd-order) | **Strong** | Warnell & Redcay: "rhos > 0.36, ps < 0.001"; Wellman et al.: 55% variance explained |
| **Within conceptually-similar paradigms** (Strange Stories ↔ Silent Films — both "explain the mental motive in a narrative") | **Strong** | Devine & Hughes: single latent factor, strong test-retest, no DIF |
| **Across diverse paradigms** (RMET ↔ faux pas ↔ spontaneous ToM ↔ belief RT ↔ pragmatics) | **Absent** | Warnell & Redcay: adult rs all in [-.115, +.125], **zero-factor solution** |

Warnell & Redcay anticipated exactly this objection and pre-empted it:

> "such studies often use measures which assess conceptually-similar aspects of ToM (e.g., all false
> belief tasks or all tasks that involve explicitly inferring complex emotional states). Thus, coherence
> among tasks may be driven not by a common component underlying all mental state reasoning, but rather a
> conceptual commonality to one particular aspect of ToM. Second, the tasks used in existing studies often
> have very similar non-ToM cognitive demands (e.g., processing facial information)."

**So: "theory of mind" is not one construct. But "false-belief reasoning" is, and "explaining mental
motives in narrative" is.** Narrow, well-specified constructs measure beautifully. The broad umbrella
does not exist.

## Why this matters for the L1/L2/L3 framework

**This is the framework's best defense, and it is a real one — but it costs the framework the thing it
most wants.**

1. **A narrowly-scoped comprehension layer CAN be measured well.** Devine & Hughes is an existence proof:
   single factor, reliable at one month, no DIF, discriminant against verbal ability. If we define L1 as
   something as tight as "explains a character's motive in a narrative vignette," we can plausibly build a
   psychometrically sound instrument. **The pessimism in the other files is about the umbrella, not about
   all possible comprehension measures.** This should be said plainly to the team rather than buried.

2. **But the price is that L1 stops being "comprehension."** It becomes "false-belief-style reasoning about
   this character in this vignette format." The framework's L1 — "can it understand a character from a
   description?" — is umbrella-scoped. At that width, the evidence says it isn't one thing (zero factors in
   adults). **The team must choose**: a narrow L1 that measures well but doesn't cover what they mean, or a
   broad L1 that covers what they mean but isn't a construct. The framework currently assumes it can have
   both, and that is the specific thing psychology says is unavailable.

3. **Wellman's 55% is the honest counterweight to the whole cascade critique.** Within the false-belief
   paradigm, performance is lawful and developmentally ordered — a real capability that really does emerge
   and really does gate downstream reasoning about beliefs. If the team wants a cascade, **this is where to
   look for it**: within a tightly-specified paradigm, not across the umbrella. A defensible reformulation
   of the framework would be "per-paradigm cascades" rather than one global L1→L2→L3.

4. **Steal the matched-control design.** Strange Stories pairs every mental-state story with a physical
   story of equivalent narrative complexity; Devine & Hughes controlled for verbal ability *and* narrative
   comprehension and the correlation survived. That survival is what licenses their construct claim. Our
   analogue: every character-comprehension probe needs a matched non-character probe of equal linguistic
   difficulty, and L1 must show **incremental validity over general reading comprehension**. Devine & Hughes
   ran that test and passed. Until we run it, our L1 has no claim to be a distinct layer at all.

5. **Note what the ICC = 0.996 actually proves — and doesn't.** Faux Pas scoring agreement is essentially
   perfect, and the Faux Pas task *still* correlates -.029 to .135 with every other ToM task in Warnell &
   Redcay's six-year-olds. **Here, in one instrument, is the framework's central conflation refuted with a
   number**: perfect boundedness, perfect rater agreement, zero convergent validity. The framework's
   inference chain — bound → referent → agreement → trustworthy layer — breaks at the last arrow, and the
   Faux Pas test is the counterexample that proves it breaks.
