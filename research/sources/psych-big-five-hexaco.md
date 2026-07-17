---
title: "Big Five and HEXACO: the lexical hypothesis, factor structure, retest reliability, and Honesty-Humility"
url: https://en.wikipedia.org/wiki/HEXACO_model_of_personality_structure
authors: Goldberg; Costa & McCrae; Michael C. Ashton & Kibeom Lee; Roberts & DelVecchio
year: 2004
type: review
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Big Five / HEXACO — structure and reliability

**Background file, not the main lead.** Included because it supplies (a) the trait taxonomy a
character sheet implicitly borrows, (b) **retest reliability numbers that set the ceiling for any
trait-matching metric**, and (c) the fact that even the *canonical* trait models keep getting
re-rotated and re-numbered — which bears on treating a trait list as a stable "specification."

Sources compiled:
- Wikipedia, "HEXACO model of personality structure" —
  https://en.wikipedia.org/wiki/HEXACO_model_of_personality_structure
- Ashton, M. C., & Lee, K. (2004/2007). The HEXACO model; *Personality and Social Psychology Review*.
- Ashton, M. C., Lee, K., & de Vries, R. E. (2014). "The HEXACO Honesty-Humility, Agreeableness, and
  Emotionality Factors: A Review of Research and Theory." *PSPR*. —
  https://journals.sagepub.com/doi/10.1177/1088868314523838
- Roberts, B. W., & DelVecchio, W. F. (2000). Rank-order consistency meta-analysis. *Psych Bulletin*.
- Costa & McCrae (1988), NEO-PI-R longitudinal retest.
- "A meta-analysis of dependability coefficients (test–retest reliabilities) for measures of the Big
  Five." *JRP* (2014). — https://www.sciencedirect.com/science/article/abs/pii/S0092656614000543

## The lexical hypothesis

The foundational assumption behind both models: personality differences that matter get encoded in
natural language, so factor-analyzing the trait adjectives of a language recovers the structure of
personality. The HEXACO literature's formulation — the approach "**uses adjectives found in language
that describe behaviours and tendencies among individuals**."

**Worth flagging for the team**: the lexical hypothesis is *why* trait vocabularies feel like natural
character-sheet primitives — they were harvested from exactly the descriptive language authors use.
But it also means the taxonomy is a **summary of how people talk about each other**, not a
specification of mechanism. It is descriptive, not generative. (Fleeson's Whole Trait Theory makes
this explicit: Big Five content gives the *descriptive* half of a trait and provides **no**
explanatory half. See `psych-fleeson-whole-trait-density.md`.)

## The Big Five

**O**penness, **C**onscientiousness, **E**xtraversion, **A**greeableness, **N**euroticism.

**Critical caveat carried in a separate file**: the Big Five are **not orthogonal in practice**,
despite being routinely presented as independent dimensions. That is the whole subject of
`psych-metatraits-trait-intercorrelation.md`, and it is the file that speaks to the team's
entanglement question.

## HEXACO — six factors, and why

Ashton & Lee (2004). Factors: **H**onesty-Humility, **E**motionality, e**X**traversion,
**A**greeableness, **C**onscientiousness, **O**penness.

> "the HEXACO model is **unique mainly due to the addition of the honesty-humility dimension**"

**Why a sixth factor:**

> "when similar lexical studies were conducted in **multiple languages rather than only English**, a
> sixth factor emerged, which was called the honesty-humility factor"

Languages in which it replicated: **"Dutch, French, Korean, Polish, Croatian, Filipino, Greek,
German, Italian, Hungarian, and Turkish."**

Per Ashton et al. (2000): a sixth lexical factor "explained antisocial traits such as
Machiavellianism and psychopathy as well as prosocial traits better than the Big Five," and "a
large-scale reanalysis of **eight lexical studies in seven languages** showed that this sixth factor
emerged consistently."

Honesty-Humility content: sincerity, fairness, greed-avoidance, modesty. It is the primary HEXACO
predictor of exploitative/antisocial behavior, and Ashton, Lee & de Vries (2014) report that
"Honesty-Humility and HEXACO Agreeableness **correlate only modestly and predict different
outcomes**," establishing H as distinct from Big Five Agreeableness.

### ⚠ HEXACO is a ROTATION, not just an addition — this matters for character sheets

> "**Agreeableness and emotionality from the HEXACO model represent rotated variants of their Big Five
> counterparts**, for example, characteristics related to **a quick temper** are associated with
> **neuroticism** ... in the Big Five framework, but with **low agreeableness** in the HEXACO
> framework"

**Read that carefully.** The *same behavior* — quick temper — loads on **Neuroticism** in one
canonical model and on **(low) Agreeableness** in the other. The behavior did not move. The axes did.

This is a direct hit on the team's "trait sheet as specification" assumption: **which trait a
behavior "belongs to" is a property of the chosen rotation, not of the person.** If two respected
trait models disagree about whether temper is an N-thing or an A-thing, then "perturb *shy*, expect
only shyness to change" presupposes a privileged basis that **the field does not have**. See
`psych-metatraits-trait-intercorrelation.md` — this is the same point the rotation-artifact debate
makes formally.

The six-dimensional space "has emerged repeatedly in lexically-based studies of personality structure
conducted in diverse languages, and **supersedes the Five-Factor structure** that was observed in
early studies of the English personality lexicon."

## RETEST RELIABILITY — the numbers that cap any trait metric

These are the ceiling for how well *anything* can measure a trait, including an LLM judge.

| Source | Instrument / interval | Value |
|---|---|---|
| Meta-analysis of dependability coefficients (JRP 2014) | Big Five, short-term | **median ρ_tt = .816** |
| HEXACO-100 evaluation | humans, retest | **median .88** |
| Costa & McCrae (1988) | NEO-PI-R domains, **6-year** | **.68 – .83** |
| Roberts & DelVecchio (2000) meta-analysis | rank-order stability, plateau after age 50 | **~.70 – .75** |

Notes from the meta-analysis: "Extraversion scales resulted in the most dependable scores, whereas
**agreeableness scales exhibited slightly larger measurement error**."

Roberts & DelVecchio: "rank-order stability of personality traits **increases throughout adulthood,
reaching a plateau of approximately .70 to .75 after age 50**"; stability "coefficients increase
during transition to adulthood, start to slow down at the ages between 30 and 40 years, and reach a
peak in old age."

**The headline: even the same human, measured with the best available instrument, retests at ~.82
short-term and ~.70–.83 over years. Personality trait measurement has a hard reliability ceiling
in the .8s.**

## Implications for the team's "character consistency" metric

1. **Retest reliability caps the metric. ~.82 is the ceiling, not 1.0.** If a *human* re-measured on
   the same validated instrument correlates with themselves at **.816** (median, short-term), then a
   model scoring above ~.85 on trait-recovery is **not more faithful to the character — it is
   exceeding the reliability of the construct itself.** The team should:
   - Treat **.80–.85 as target**, not as a shortfall.
   - Treat **>.90 as a rigidity flag** — it is outside the range in which trait measurement is even
     meaningful.
   - **Correct their correlations for attenuation** if comparing against any human-rated ground
     truth, otherwise they will systematically under-credit models.

2. **Long-horizon drift has a human benchmark too — and it is not 1.0.** Costa & McCrae: **.68–.83
   over six years**. Roberts & DelVecchio: **.70–.75 plateau, and *lower* before age 50** — i.e. real
   people's traits *do* move, and younger people's move more. A character that is *perfectly*
   unchanged from turn 3 to turn 97 is more temporally invariant than a 50-year-old human is across
   a decade. **Some drift is not a bug; the question is only whether it is more than a person's.**

3. **The lexical taxonomy is descriptive, not generative — so a trait vector under-specifies a
   character.** The Big Five/HEXACO were built to *summarize how people describe each other*, not to
   *generate behavior*. A character sheet built from trait adjectives inherits that limitation: it
   pins **elevation** (mean levels) and says nothing about **shape** (if-then structure) or **spread**
   (SD). Two characters with identical sheets can be entirely different people (Wediko children 9 and
   28 — see `psych-caps-behavioral-signatures.md`). **The sheet is not a specification; it is a
   summary statistic of one.**

4. **On trait entanglement — HEXACO delivers a clean, self-contained argument the team can't wave
   away.** They assume traits are independently perturbable knobs. But:
   - The Big Five are **not orthogonal in practice** (see the metatraits file).
   - And **the assignment of behavior to trait is rotation-dependent**: quick temper = Neuroticism in
     Big Five, = low Agreeableness in HEXACO. **Same person, same behavior, different trait label.**
   Therefore "perturb *shy*, expect only shyness to change" is only well-posed **relative to a chosen
   basis** — and the field's two leading bases disagree. **If the team's model shows "shy" bleeding
   into "anxious," that may be a basis disagreement between the model's internal representation and
   the sheet's chosen axes, not a defect in either.** Before calling crosstalk a bug, the team must
   answer: *in which rotation?*

5. **Practical: add Honesty-Humility to the character-sheet vocabulary if they use Big Five.** H is
   the strongest predictor of exploitative, manipulative, and antisocial behavior, and it is
   **absent** from the Big Five. For companion characters — where sincerity, manipulation, and
   fairness are exactly the safety-relevant axes — a Big Five sheet has **no dimension on which to
   specify "this character does not manipulate the user."** That is a real gap with product and
   safety consequences, not just a taxonomic preference.
