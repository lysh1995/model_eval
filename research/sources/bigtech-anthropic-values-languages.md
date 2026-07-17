---
title: "Claude's values across models and languages"
url: https://www.anthropic.com/research/claude-values-models-languages
org: Anthropic
year: 2026
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Anthropic, "Claude's values across models and languages" (Jul 13, 2026)

**Published three days before this research was conducted.** The closest thing any lab has published
to a **Lane-2 corpus-statistic instrument for character**, and it independently corroborates our
language finding (`ρ(en,zh) = −0.082`, note 09) at n = 309,815.

Verified by `curl` + tag-strip (27,280 chars); all quotes regex-matched against raw text. Term
counts: `language` 59 · `axes` 25 · `axis` 19 · `warmth` 27 · **`persona` 0 · `steer` 3**.

## Method — a Lane-2 instrument for character, and it controls our exact confound

> "To build the value axes, we began with the **3,307 values identified in Values in the Wild** and
> manually clustered those with similar meanings, producing a shorter list of **339 high-level values**.
> Next, with our privacy-preserving analysis tool, we sampled **309,815 Claude.ai conversations in which
> the user gave Claude a subjective task.** Our sample drew equally from **three models (Sonnet 4.6, Opus
> 4.6, Opus 4.7) and the 20 most common languages** used on Claude.ai, giving us roughly **5,000
> conversations per model-language pair**. For every conversation, the tool used Claude to label each of
> the 339 high-level values as present or absent. … We then applied **dimensionality reduction**, a
> technique that compresses the labeled values into axes based on which ones Claude tends to express
> together."

**The confound control is the part to steal.** Compare BENCHMARKS.md §2 (K2): *"topic leakage (a chef
discusses food regardless of voice)"*:

> "**To make sure we measured the values Claude expressed—rather than differences in what users were
> asking about or how they asked—we controlled for each conversation's task, topic, and user-expressed
> values.**"

This is a published precedent for exactly the K2 ablation we specced. It also confirms the confound
is real enough that a lab with 300k conversations bothered to control for it.

## The four axes — and the honest variance number

> "**Four key axes capture 15% of the variation in Claude's values:**
> **Deference vs. Caution:** Whether Claude leans toward accommodating what someone wants or guarding
> against possible risk and harm.
> **Warmth vs. Rigor:** Whether Claude leans toward expressing positivity and care for the person or
> emphasizing accuracy and precision.
> **Depth vs. Brevity:** Whether Claude leans toward explaining in depth or doing only what was asked.
> **Candor vs. Execution:** Whether Claude leans toward foregrounding its own uncertainty or producing a
> more polished and confident answer."

**15%.** Four axes over 339 values across 309,815 conversations explain **fifteen percent** of the
variance. That number is worth carrying: a lab with production-scale data, reducing character to a
small number of interpretable axes, captures 15% of it. **Anyone promising that a handful of
character dimensions covers the construct is overclaiming**, and this is the citation that says so.
Directly relevant to BENCHMARKS.md §6.6 (BARS retranslation — expect "creativity"/"engagement" to
collapse) and to any temptation to ship a tidy 5-dimension character rubric.

Note also the axes are **bipolar and anti-correlated by construction**:

> "This doesn't mean the value groups on either end are mutually exclusive—Claude can express warmth and
> rigor in the same conversation. **But in practice, the more Claude expresses values on one side of an
> axis, the less it tends to express values on the other.**"

That is an empirical **entanglement** finding at corpus scale: warmth trades against rigor in
practice. Cf. the Sonnet 5 system card's sycophancy↔"wet blanket" link
(`bigtech-anthropic-sonnet5-system-card.md`) and our K3 fidelity↔diversity tradeoff. **Three
independent instances of the same structural fact: character traits are not independently
addressable.** This is the strongest cumulative support for L2.2's steerability *matrix* (as opposed
to per-trait slopes).

## ✅ Corroborates our language finding at n = 309,815

> "**The values Claude expresses vary across languages.** When Claude speaks in English, it emphasizes
> different values than when it speaks in Portuguese, Indonesian, or Chinese. **The largest variation is
> in the Warmth vs. Rigor axis, with Claude leaning toward expressing warmth-related values most in
> Arabic and Hindi and rigor-related values most in English and Russian.**"

> "In English, Claude leans toward expressing values related to caution, rigor, depth, and candor, while
> **in Arabic it leans toward deference, warmth, brevity, and execution.**"

> "Our previous research has shown that **Claude behaves somewhat differently in different languages.**"

**This validates ABILITY-MODEL §2.3 (L1.3's "zh vs en") and §5 open question 2** ("Is the
steerability matrix stable across characters and languages? … **assume not** until shown
otherwise"). Anthropic finds the *same model* expresses materially different values by language,
with task/topic/user-values controlled out — so the difference is the model's, not the users'.

**Consequence for our corpus:** our `ρ(en,zh) = −0.082` is no longer an anomaly to explain away; it
is consistent with a lab result at ~7,000× our n. **Language is a separate measurement context, and
every L1/L2/L3 number must be reported per-language.** Pooling en and zh is now affirmatively
contraindicated by external evidence.

## The validation move is ours (convergent validity against human perception)

> "**Value profiles across these axes match perceptions of model character.** Sonnet 4.6 is regarded as
> particularly warm, while Opus 4.7 is known for rigor. We find that each model's value profile mirrors
> these subjective assessments: Sonnet 4.6 leans toward expressing more deference to the user and
> emotional warmth while Opus 4.7 leans toward expressing a focus on accuracy and precision as well as
> guarding against misuse."

> "These findings line up with how people perceive these models, both within Anthropic and online.
> Claude.ai users have commented that Opus 4.7 hedges its answers more often than other models. …
> **The fact that our axes recover these impressions suggests our method for labeling and comparing the
> values Claude expresses is tracking something real about how the mo[dels differ]**"

This is BENCHMARKS.md §4's bridge argument, run by Anthropic: validate the cheap automated
instrument against an independent human-perception signal. Note it is validated against
**aggregate reputation**, not against per-conversation labels — a weaker check than our X1
(κ vs. revealed preference) or X6 (author labels) designs. **Our validation design is stronger than
the published one**, if we ever get the data.

## Steerability, again as a future hope

> "Each Claude model reflects a slightly different approach to character training as well as many other
> fine-tuning decisions. Because our value axis approach quantifies key differences between models, **it
> may ultimately allow us to connect variation in the values Claude expresses to different training
> decisions.**"

**"May ultimately allow us to connect"** — i.e. connecting a character-shaping intervention to a
measured behavioral outcome is stated as **not yet achieved**, in July 2026, by the lab that invented
character training. This is the training-space analogue of ABILITY-MODEL §3.2's prompt-space
steerability gap, and it is the third independent statement of it (cf. "Claude's Character": *"relying
on human researchers closely checking how each trait changes the model's behavior"*).

## What this does NOT contain

- ❌ **`persona`: 0 occurrences.** No authored-character work; the unit is Claude's own expressed values.
- ❌ No prompt-perturbation / dose-response; the variation is *observational* across models and
  languages, not *causal* from a manipulated prompt. (ABILITY-MODEL §3.2's point that L2.2 would be
  *"a causal experiment, not an observational score"* survives intact — this is an observational study.)
- ❌ No comprehension/execution distinction.
- ❌ No inter-rater agreement for the Claude-based value labeller.
