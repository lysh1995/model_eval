---
title: "Emotion recognition accuracy only weakly predicts empathic accuracy in a standard paradigm and in real life interactions"
url: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1154236/full
secondary_url: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10232734/
authors: (Frontiers in Psychology, 2023)
year: 2023
type: paper (empirical, Bayesian)
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Two "read the other mind" tests. Bayesian evidence FOR the null. They are separate competences.

**This is the fifth independent line of evidence that "understanding another mind" is not one
construct** — and it's the strongest methodologically, because it reports *Bayesian evidence for the
null* rather than a failure to reject.

## The design

- **N = 101** (diary subsample N = 61).
- **ERA test (ERAM)** — emotion recognition: "24 video recordings of emotional facial expressions
  without audio track, 24 emotional expressions with audio track only, and 24 audio-video
  recordings" — 12 emotion labels, **forced-choice**.
- **EA test** — Ickes-style empathic accuracy: "Video clips (2.5–3 min long each) of individuals
  narrating ... a negative event" — **open-ended** inference of thoughts and feelings.
- Plus a **diary** component for real-life interactions.

Both tasks are "infer what's going on in this person". One is recognition/forced-choice; one is
open-ended generation of an inference.

## The result

> "**No correlation** between variables obtained from the empathic accuracy test scores and the
> variables obtained from Emotion recognition test scores **had a Bayesian support against the null
> hypothesis**."

> "**strong evidence for the null hypothesis** for all EA scores both with and without group included
> in the model (**BF01 from 29.82 to 124.98** ... except for the EA score for Feeling audio only where
> only weak evidence in favor of the null hypothesis emerged (BF01 = 2.75, R² = 0.15)"

**BF01 of 29.82–124.98 is "strong" to "extreme" evidence FOR the null.** This is not an underpowered
null. This is a positive demonstration of independence.

Real-life diary data agrees:

> "only significant relationship was for the EA scores for feelings when both video and audio were
> shown, F(1,356) = 4.49, p < 0.04, **ηp² = 0.01**"

(η² = 0.01 — 1% of variance. The one "significant" effect is negligible.)

## The authors' conclusion

> "**skill in decoding prototypical facial emotion expressions ... does not predict a skill in
> discerning the unspoken thought and feelings of others.**"

> "suggesting that they are **separate competences** ... the ability to use **context information to
> correctly infer others' emotions via perspective taking** should [not] be correlated with the
> ability to use **pattern matching** for the same task."

## Why this matters for the ability model — the mechanism is named ★

The authors' explanation is the important part for us: **perspective-taking from context** and
**pattern matching** are different competences that happen to be measured by superficially similar
tasks.

**That distinction maps precisely onto the L1.2 discrimination/generation table's row 4:**

| discriminate | generate | ability model's diagnosis |
|---|---|---|
| ❌ | ✅ | "**mimicry without comprehension** — brittle; will fail off-distribution" |

The ability model already suspects that **pattern matching can masquerade as comprehension**. This
paper is the human-subjects evidence that these are dissociable competences *in people*, with
BF01 up to 124.98. **The L1.2 design is well-motivated.** But note what it implies about the probe
suite: a **forced-choice** probe (*"which of these two responses is more in-character?"* — the
ability model's "key one") measures **pattern matching**, and an **open-ended** probe (*"what does
this character want that they'd never admit?"*) measures **perspective-taking from context**.

> **The ability model's own L1.1 probe list mixes both formats and expects them to produce one L1
> score. This paper says they will not correlate — and gives the theoretical reason why.**

## Convergence — the tally now stands at five

Independent literatures finding that "understanding another mind" does not cohere as one measurable
ability:

| # | finding | statistic | source |
|---|---|---|---|
| 1 | ToM tasks don't intercorrelate (adults) | all r between **−.115 and +.125** | `psych-tom-task-convergence.md` |
| 2 | EA ↔ Interpersonal Perception Task | **r = 0.06** (ns) | `psych-empathic-accuracy-ickes.md` (Mortimer 1996) |
| 3 | Different interpersonal-sensitivity performance measures ↔ each other | null | Hall (2001), via ibid. |
| 4 | Self-report empathy ↔ EA performance | "generally fail to predict" | Davis & Kraus (1997), via ibid. |
| 5 | **ERA ↔ EA** | **BF01 = 29.82–124.98 for the null** | *this file* |

**Five independent lines. All null. None of them is a power failure — #5 is positive evidence for
independence.**

**Conclusion for L1: there is no such thing as "comprehension ability" as a scalar.** There are
specific competences measured by specific probe formats, and they do not converge. Any single "L1
score" we compute is an arbitrary weighted average over non-converging subtests — its value will be
determined by our probe mix, not by the model.

## What to steal

1. **Bayesian null testing.** When we run the L1 inter-probe correlation matrix (which we must), use
   Bayes factors. "We found no correlation" is unpersuasive; **BF01 > 10 is a result.** This is a free
   upgrade to note 04 §4.1's discriminant matrix and lets us make a *positive* claim about
   dimensionality instead of a hedge.
2. **The format confound as a design variable.** Cross forced-choice × open-ended probes deliberately
   and report them separately. If they don't correlate — and five literatures say they won't —
   **report two L1 numbers, not one.** Name them: `L1-recognition` and `L1-inference`.
3. **η² alongside p.** Their one "significant" real-life effect is η²=0.01. Note 04's SEM/noise-floor
   discipline, restated: significance without effect size is theatre.
