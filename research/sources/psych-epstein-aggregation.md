---
title: "Epstein's aggregation rebuttal: single acts are single-item tests; reliability climbs as you aggregate occasions"
url: https://library.scottbarrykaufman.com/uploads/2019/01/Temporal_Stability_and_Cross-Situational.pdf
authors: Seymour Epstein (1979, 1980, 1983); Ed Diener & Randy J. Larsen (1984, empirical test); John Kihlstrom (Berkeley, course notes)
year: 1979
type: paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Epstein's aggregation principle — and its precise limits

**This is the crucial counter-argument to Mischel, and it directly determines how many turns the
team must sample.** It is also the argument most often over-claimed, so the limits section below
matters as much as the principle.

Sources compiled (Epstein 1979 itself is paywalled; numbers below come from sources that report it
and from the direct empirical replication in Diener & Larsen 1984, full text extracted):
- Epstein, S. (1979). "The stability of behavior: I. On predicting most of the people much of the
  time." *JPSP*, 37, 1097–1126.
- Epstein, S. (1983). "Aggregation and beyond: Some basic issues on the prediction of behavior."
  *Journal of Personality*, 51. — https://onlinelibrary.wiley.com/doi/10.1111/j.1467-6494.1983.tb00338.x
- **Diener, E., & Larsen, R. J. (1984). "Temporal Stability and Cross-Situational Consistency of
  Affective, Behavioral, and Cognitive Responses." *JPSP*, 47(4), 871–883.** — full text extracted
  from https://library.scottbarrykaufman.com/uploads/2019/01/Temporal_Stability_and_Cross-Situational.pdf
- Kihlstrom, J. F., "Critique of Trait Psychology" —
  https://www.ocf.berkeley.edu/~jfkihlstrom/IntroductionWeb/resources/Ch4TraitCritique.htm

## The core insight, stated as cleanly as it has ever been stated (Kihlstrom)

> "**Single-act criteria are, in effect, single-item tests. And single-item tests are inherently
> unreliable.**"

That is the whole argument in two sentences. **Mischel's .30 was not a measurement of personality;
it was a measurement of a one-item test.** You cannot indict a construct with an instrument of
length 1.

## Epstein's claim and design

- **Epstein (1979): four studies, 131 college students.**
- The finding, as reported across sources: **"when measures of behavior were averaged over an
  increasing number of events, stability coefficients increased to high levels for all kinds of
  data, including objective behavior, self-ratings, and ratings by others"** — and once aggregated,
  "objective behavior was then reliably related to self-report measures, including standard
  personality inventories."
- Epstein (1979, 1980) "argued that **impressive stability can be demonstrated over a wide range of
  behavioral variables as long as the behavior is averaged over a sufficient number of
  occurrences.**"

A concrete single-occasion datapoint reported by Kihlstrom from Epstein's data:

> "The number of telephone calls made, and the number of letters written, over a 12-day period. **The
> correlation was .33.**"

— i.e. **.33 at the single-occasion level, the classic "personality coefficient" magnitude, from a
purely objective behavioral count.** Aggregate the same behavior over days and it climbs.

Epstein (1983) on the mechanism:

> "**appropriate aggregation can reduce error variance associated with the unrepresentativeness of
> individual stimuli, situations, occasions, judges, items of behavior, and subjects**"

> "Single items tend to be **too unreliable and too narrow in scope** to measure broad dispositions
> such as traits."

## The formula — this is the number the team needs

Aggregation follows the **Spearman-Brown prophecy formula**. Sources confirm Epstein's observed gains
track it: "When ten weights are used **the increase in validity follows that predicted by the
Brown-Spearman formula**." Fleeson (2001) independently confirms: "(Stepping up the single-state
correlations with the Spearman-Brown prophecy formula **predicted values similar to these empirically
observed values**.)"

```
ρ_k  =  k·ρ_1 / (1 + (k−1)·ρ_1)
```

where `ρ_1` = reliability of a single observation, `k` = number of aggregated observations.

**Worked, starting from Mischel's own ceiling (ρ₁ = .30):**

| k (occasions aggregated) | ρ_k |
|---|---|
| 1 | **.30** |
| 2 | .46 |
| 4 | .63 |
| 8 | .77 |
| **10** | **.81** |
| 16 | .87 |
| 20 | .90 |
| 32 | .93 |
| 50 | .96 |

**The .30 barrier and the .80 reliability are the same number.** Mischel's "personality coefficient"
of .30 *is* an aggregate reliability of ~.81 at k=10 and ~.90 at k=20. Nothing about the person
changed — only the length of the test.

Inverting, to hit a target `ρ_k` from `ρ_1`:

```
k  =  ρ_k·(1 − ρ_1) / (ρ_1·(1 − ρ_k))
```

**For the team: from ρ₁ = .30, reaching ρ_k = .80 requires k ≈ 9.3 → 10 observations; ρ_k = .90
requires k ≈ 21.** This is the direct answer to "how many turns must we sample."

## The empirical replication with real numbers — Diener & Larsen (1984)

The best-documented test of the principle, and it also delivers the **decomposition** the team needs.

**Design** (pp. 872–874):
- **42 subjects**, sampled on **3,512 occasions** "randomly sampled from the lives of 42 subjects."
- Signalled at random times, **twice daily for a six-week period**, via preset alarm watch; "The
  random times, which were based on sampling without replacement, were generated so that **every
  10-min period during the waking day was covered over the six weeks**."
- Reliability of measures: internal consistency **α = .89 (positive affect), .84 (negative affect)**.

**Abstract, verbatim** (p. 871):

> "Consistency and stability of feelings were examined in reports that were completed on **3,512
> occasions randomly sampled from the lives of 42 subjects**. The stability and consistency of
> responses depended on the situations, individuals, and responses involved. **High degrees of
> consistency were unusual for single responses, although mean levels of responding tended to be both
> highly stable and consistent.** ... The results indicate that **the question of whether personality
> consistency exists does not have a simple answer, and requires knowledge of the persons,
> situations, responses, and level of analysis involved.**"

**The aggregation finding, verbatim** (p. 881, conclusion 3):

> "**Aggregating data across occasions resulted in much higher stability and consistency estimates
> than those based on disaggregated estimates.** Such aggregation is analogous to randomization and
> experimental control in laboratory research because aggregation helps reduce the influence of
> uncontrolled factors. **There were striking differences between the correlations for aggregated data
> and those disaggregated to single occasions. This indicates that there are consistent and stable
> long-term trends in mean levels of responding for individuals, but in general single responses will
> show very low levels of consistency and stability.**"

> "The **low estimated single occasion correlations** suggest **short-term fluctuations or variability
> in the responses of our subjects, even though there is a long-term trend in the mean level of their
> responses.**"

Observed aggregate-level numbers in the paper: three-week stability coefficients of **.79 (positive
affect)** and **.81 (negative affect)** (robust to partialling out response artifacts: .76 / .77);
odd/even-day reliability correlations across the table running **.74 – .97**.

**Stability > consistency, verbatim** (p. 881, conclusion 4):

> "It appeared that **most variables tended to show somewhat greater stability than consistency**. This
> difference was most pronounced for affect, arousal, and the cognitive variables. However, each of
> these also showed strong consistency when aggregated data were analyzed."

Why rater-based studies look more consistent than behavior-based ones (p. 873) — **directly relevant
to an LLM-judge pipeline**:

> "Note that findings of higher cross-situational consistencies such as those based on peer ratings
> **are usually based on data that are implicitly averaged across occasions**. One reason that rater
> judgments may show relatively high cross-situational consistency ... **is that raters base their
> judgments on a number of occasions.**"

## ⚠ THE LIMIT OF AGGREGATION — the team must not over-apply this

Aggregation is **not** a general-purpose rescue of cross-situational consistency. It fixes
**unreliability**; it does not fix **situational variance**, because situational variance is not
error.

**The decisive evidence** — Mischel & Peake (1982), Carleton College (via Kihlstrom):

> "The average correlation across the 19 different behavioral variables was **a mere .08**."
> "**Even when the variables were aggregated over time, so that 2-12 different observations went into
> the measurement, the average cross-situation correlation was only 0.13.**"

**Aggregating over time moved cross-situational consistency from .08 to .13. That is all.** Compare
against the Spearman-Brown prediction for k≈7 from ρ₁=.08 → ρ_k ≈ .38. **It massively underperformed
the formula.** Why? Because Spearman-Brown only applies when the thing being averaged out is
**random error**. The cross-situational variance is **systematic** — it is the if-then signature (see
`psych-caps-behavioral-signatures.md`). You cannot average away signal.

Diener & Larsen make the same caution explicit (p. 881):

> "**The high correlations obtained in this study and by Epstein (1979, 1982) for aggregates do not
> mean that personality is any stronger in its ability to explain individual responses.** However, if
> one is interested in long-term mean levels of behavior, there may be person effects that are
> strong..."

> "**Which level of analysis a scientist chooses to study will [determine what they find]**" —
> i.e. aggregation changes *the question*, not just the precision of the answer.

And critically (p. 881):

> "**Nevertheless, even after aggregation some responses were very consistent and others were not.
> Thus person effects can be weak in some cases even if long-term trends are examined.**"

**The rule the team should internalize:**
- **Aggregate over occasions *within* a situation type** → reliability rises per Spearman-Brown.
  ✅ Legitimate, and mandatory.
- **Aggregate over *different situation types*** → you destroy the if-then signature and gain almost
  nothing (.08 → .13). ❌ This is what the team's current metric does.

## Implications for the team's "character consistency" metric

1. **Any single-turn character-consistency judgment is a one-item test, and its ceiling is ~.30.**
   Epstein's core point applies with full force: "Single-act criteria are, in effect, single-item
   tests. And single-item tests are inherently unreliable." **If the team scores per-turn deviation
   from the character sheet and treats each score as meaningful, they are measuring noise.** A turn-97
   "character break" flagged from one turn is, statistically, indistinguishable from nothing.

2. **The direct answer to "how many turns must we sample": k ≈ 10 for ρ ≈ .80, k ≈ 20 for ρ ≈ .90,
   assuming a single-turn reliability of ρ₁ ≈ .30.** They should **measure their own ρ₁** (correlate
   character-consistency scores across two randomly chosen, well-separated single turns — exactly
   Fleeson's method, which returned .28–.48) and then use the inverted formula
   `k = ρ_k(1−ρ₁) / (ρ₁(1−ρ_k))` to set the sample size **per situation type, per character**. This is
   a concrete, defensible number to put in the eval spec, and it replaces a guess.

3. **But aggregate over occasions *within* situation type — never across situation types.** This is
   the trap. The Mischel & Peake result (.08 → .13 despite 2–12 observations) proves that averaging
   across heterogeneous situations does **not** buy reliability, because the between-situation
   variance is signal, not error. **The team's metric currently aggregates across "many different
   contexts" — which is precisely the aggregation that does not work, and which simultaneously
   destroys the if-then profile.** It is the worst of both: statistically inert *and* it deletes the
   construct.
   - **Correct design**: `situation_type × occasion` panel. Aggregate down the *occasion* axis
     (k≈10–20 per cell). **Keep the situation axis intact** — that axis *is* the behavioral signature.

4. **Epstein rehabilitates "turn 3 vs turn 97" as a legitimate question — properly framed.**
   Diener & Larsen: aggregated three-week stability of **.79–.81**. Temporal stability of the *mean*
   is genuinely high in humans and *should* be high in a model. So: compare the **aggregate mean of
   turns 1–20 within situation type S** against the **aggregate mean of turns 78–97 within situation
   type S**. **That** comparison is a real drift metric with a real human benchmark (~.80). Comparing
   *turn 3* to *turn 97* directly is comparing two single-item tests and will return noise at ρ≈.30
   regardless of whether drift occurred.

5. **Their judge is already doing implicit aggregation — and that is why judge scores may look
   deceptively consistent.** Diener & Larsen (p. 873): rater judgments show higher cross-situational
   consistency "because raters base their judgments on a number of occasions." An LLM judge reading a
   whole transcript is **implicitly aggregating**, and will therefore report *higher* consistency
   than the turn-level behavior actually supports. **Judge-level consistency scores are not
   behavior-level consistency scores**, and the team should not treat them as interchangeable. (This
   compounds with halo — see `psych-halo-effect.md`.)

6. **Report what level of analysis each number lives at.** Diener & Larsen's central conclusion is
   that consistency "does not have a simple answer, and requires knowledge of the persons,
   situations, responses, and **level of analysis** involved." A single scalar called "character
   consistency" hides the level of analysis and is therefore uninterpretable. Minimum honest
   reporting: **(a) single-turn reliability ρ₁, (b) k used, (c) aggregated within-situation
   stability, (d) cross-situational consistency, (e) if-then profile stability** — five numbers, not
   one.

7. **On trait entanglement:** aggregation speaks to this only indirectly, but usefully. Epstein's
   mechanism — aggregation "can reduce error variance associated with the unrepresentativeness of
   individual stimuli, situations, occasions, **judges**, items of behavior, and subjects" — means
   that **if the team's observed crosstalk is judge noise, aggregating over judges/occasions will
   shrink it toward zero.** If the crosstalk **survives** aggregation, it is systematic, and then the
   question becomes whether it is *realistic* systematic covariance (see
   `psych-metatraits-trait-intercorrelation.md`) or halo (see `psych-halo-effect.md`).
   **Aggregation is thus a free first-pass diagnostic**: run the perturbation many times and see
   whether the crosstalk is stable. Unstable crosstalk = noise. Stable crosstalk = a real structural
   claim that must then be evaluated against human trait covariance, not against an assumption of
   orthogonality.
