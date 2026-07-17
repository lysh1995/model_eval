---
title: "Does theory of mind predict social behavior? Two meta-analyses converging on r = .19"
url: https://pubmed.ncbi.nlm.nih.gov/25874384/
authors: Slaughter, Imuta, Peterson & Henry (2015); Imuta, Henry, Slaughter, Selcuk & Ruffman (2016)
year: 2015-2016
type: review
accessed: 2026-07-16
topic: psychology-crosscheck
---

# The comprehension → behavior link in humans is weak (r ≈ .19, ~4% of variance)

**This file is the direct test of the team's cascade claim.** If "comprehension" causally gates
"application/portrayal," then in humans, mentalizing ability should strongly predict social
performance. It doesn't.

Sources compiled:
- Slaughter, Imuta, Peterson & Henry, "Meta-Analysis of Theory of Mind and Peer Popularity in the
  Preschool and Early School Years," *Child Development* 86(4) (2015) —
  https://pubmed.ncbi.nlm.nih.gov/25874384/ / https://srcd.onlinelibrary.wiley.com/doi/10.1111/cdev.12372
- Imuta, Henry, Slaughter, Selcuk & Ruffman, "Theory of Mind and Prosocial Behavior in Childhood: A
  Meta-Analytic Review," *Developmental Psychology* (2016) —
  https://www.semanticscholar.org/paper/3ecd6af229713c767b81cff70566b7fde69a9fc2

## Meta-analysis 1 — ToM and peer popularity (Slaughter et al. 2015)

Scope: **"Meta-analysis of 20 studies including 2,096 children (aged from 2 years, 8 months to 10
years)"**

Headline result:

> "Significant overall association (r = .19) indicating that children with higher ToM scores were also
> more popular"

Moderators:

| Moderator | Effect |
|---|---|
| Boys | **r = .12** |
| Girls | **r = .30** |
| Popularity | **r = .23** |
| Rejection | **r = .13** |
| Age | "The effect did not vary with age" |

Authors' conclusion (note the framing — this is a *positive* spin on r=.19):

> "These findings confirm that ToM development has significant implications for children's peer
> relationships"

The variance interpretation, as summarized in the surrounding literature:

> "children's correct performance on ToM tasks accounts for about 4% of the variance in peer
> popularity. This small effect may be due to the presence of other factors - cognitive, personality,
> physical and behavioral – that affect children's sociometric status."

## Meta-analysis 2 — ToM and prosocial behavior (Imuta et al. 2016)

Scope: **76 studies, 6,432 children, ages 2-12.**

Headline result — **the same number, independently**:

> overall effect size r = .19, "indicating that children with higher Theory of Mind scores also
> received higher scores on concurrent measures of prosocial behavior"

Moderators:

| Moderator | Effect |
|---|---|
| Affective perspective taking | **r = .24** |
| Cognitive perspective taking | **r = .16** |
| Age 6-12 | **r = .24** (stronger than younger) |

**Two independent meta-analyses, 96 studies and ~8,500 children between them, different outcome
constructs (sociometric status vs prosocial behavior), both land on r = .19.** That convergence is
itself the finding: it is a robust, replicated, *small* effect.

## What r = .19 actually means

- **r² ≈ .036.** Knowing a child's ToM score explains **~3.6% of the variance** in their social
  behavior. ~96% is something else.
- Cohen's conventions put r = .19 just below "small" (.10) → "medium" (.30). It is a real effect and a
  weak one.
- **It's concurrent, not causal.** Imuta measures "concurrent measures of prosocial behavior" — ToM and
  behavior measured at the same time. A correlation of .19 between two things measured simultaneously
  is not evidence that one gates the other. Both plausibly load on language ability, executive
  function, and SES (recall from `psych-tom-task-convergence.md` that ToM tasks correlate rho .21-.39
  with verbal IQ — arguably *better than they correlate with each other*).
- **Attenuation cuts both ways, and honesty requires saying so.** Per `psycho-classical-test-theory.md`,
  observed r is capped at √(ρ_xx'·ρ_yy'). ToM measures are unreliable (RMET α ≈ .73 at best, often
  ~.60), and sociometric measures are noisy too. Disattenuating .19 by, say, √(.70 × .70) = .70 gives
  a true correlation nearer **.27** — still small, ~7% of variance. So measurement error does *not*
  rescue the cascade. The honest statement is: the true comprehension→behavior link in humans is
  somewhere in the .19-.30 band, i.e. small.
- **The moderator pattern is bad news for a clean cascade.** If ToM gated social performance, the gate
  shouldn't be twice as strong for girls (.30) as for boys (.12). Sex moderating a *causal capacity
  gate* by 2.5× in variance terms suggests we're looking at a correlate embedded in a web of other
  causes, not a bottleneck.

## Why this matters for the L1/L2/L3 framework

**This is the cleanest available falsification test of the cascade claim, and the framework fails it.**

1. **The cascade's core premise is that comprehension gates downstream performance.** L1 → L2 → L3,
   "failures cascade downward never upward." The human analogue of L1→(social performance) has been
   measured 96 times across 8,500 children. The answer is **r = .19**. If human mentalizing barely
   predicts human social behavior, the prior that model "character comprehension" predicts model
   "character portrayal" should be correspondingly weak. **The team is asserting a strong causal chain
   where the closest measured analogue is a weak correlation.**

2. **A cascade predicts an asymmetric, thresholded pattern — not a linear correlation.** Note what the
   cascade claim would actually look like in data. It's not "L1 correlates with L3." It's: **low L1
   ⇒ low L3 (near-deterministic), but high L1 ⇒ L3 anything.** That is a *triangular scatterplot*, and
   it produces a modest Pearson r even when the cascade is real. So r = .19 does not by itself refute
   the cascade — and this is the strongest defense available to the team, worth stating plainly. **But
   it does mean the cascade must be tested as a necessity claim, not a correlation.** The right test is
   : are there zero cases of (L1 fail, L3 success)? Count the empty cell, don't compute a correlation.
   If the empty cell isn't empty, the cascade is dead regardless of r.

3. **The framework's real vulnerability is that comprehension may be necessary but almost free.** A
   plausible reading of r = .19 that *preserves* the cascade: comprehension is a low threshold that
   nearly everyone clears, so it has almost no variance left to explain downstream outcomes. Under this
   reading L1 is real, causally upstream, and **useless as an evaluation target** — it would be a
   ceiling-effect metric that never discriminates between the frontier models we actually care about.
   This is arguably the most likely outcome for L1 in practice, and it argues for measuring L1 only as
   a **gate** (pass/fail, run once) rather than as a **score** (a dimension you track and optimize).
   The framework currently treats it as a score.

4. **The mediation finding tells us where to look instead.** One of the retrieved sources is titled
   "Theory of Mind and Sociometric Peer Status: The Mediating Role of Social Conduct" — the ToM→status
   link runs *through behavior*. Comprehension doesn't cause outcomes; it enables conduct that causes
   outcomes, and the conduct step is where the variance lives. Translated: **the interesting variance
   is in the L2/L3 layer, not L1.** Effort spent building precise comprehension probes is effort spent
   on the layer with the least explanatory power.

5. **Affective > cognitive perspective taking (.24 vs .16) is a hint about what to measure.** The
   "warmer" construct predicted behavior *better* than the crisp cognitive one. This inverts the
   framework's implicit hierarchy, which treats the bound/cognitive layers as the trustworthy
   foundation and the perspectival layer as the soft one. In the human data, the softer construct is
   the more predictive one. If that transfers, our fuzzy L3 judgments may carry more signal about
   actual roleplay quality than our crisp L1 probes — the exact opposite of the framework's confidence
   ordering.

**Caveat, stated honestly**: these are developmental samples (ages 2-12) and correlational designs.
Adult effects could differ, and no one has run the model analogue. But it is the best evidence
available, it replicates across two independent meta-analyses with different outcomes, and it is
evidence the framework should be required to engage with rather than assume away. The burden is on the
cascade claim to produce its empty cell.
