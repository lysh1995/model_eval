---
title: "Data Flywheels for LLM Applications"
url: https://www.sh-reya.com/blog/ai-engineering-flywheel/
org: Shreya Shankar (UC Berkeley EPIC Lab)
year: 2024
type: research-blog
accessed: 2026-07-16
topic: eval-lifecycle
---

# The data flywheel — Shankar

The canonical writeup. Companion piece to "Who Validates the Validators?" (UIST 2024).

## The loop

"automatically and dynamically improve LLM applications using production data" —
production outputs → evaluation → monitoring → improvement → feeds back into future runs.

## Stage 1 — Evaluation: defining success metrics

- Identify metrics **specific to your use case by examining actual LLM outputs**
- Implement via code-based heuristics **or** LLM-as-judge
- **"Start with binary metrics (True/False) for easier alignment"**
- Validate inputs and outputs; validate **intermediate steps** in multi-step pipelines
- **"Use multiple granular metrics rather than holistic quality judgment"**

> "Multiple granular metrics rather than holistic quality judgment" is note 11's organizing
> principle arrived at independently: *decompose every soft dimension until the objective
> part falls out.*
>
> "Start with binary" also aligns — note 11's Lane 1 fields are **violation rates**:
> countable events with a real denominator, bounded [0,1], comparable by construction.

## Stage 2 — Monitoring: operationalizing metrics

- **"Automatically reassess if your chosen metrics still align with your goals"** as
  production data evolves
- Keep LLM-based validators aligned via **dynamic few-shot example retrieval**
- Maintain labeled production data in a DB **with timestamps for recency tracking**
- **"Next-token probabilities from instruction-tuned models are uncalibrated and unhelpful
  when analyzing outputs at scale"**

> ⚠️ **The uncalibrated-logprobs finding is a direct hit on a tempting shortcut.** Note 06's
> Tier 1 lists "logprobs" among cheap 100%-coverage signals, and note 11's judge protocol
> needs a **confidence** signal to drive abstention (§6) and the Trust-or-Escalate cascade
> (note 06 §4). **Shankar's finding says the free confidence signal doesn't work.** That is
> why Trust-or-Escalate uses N=5 *Simulated Annotators* for calibration instead of reading
> logprobs — and why that paper reconciles to ">40% cost reduction" rather than 78.5%
> (note 06 §4's warning). **Confidence must be purchased, not read off.** Budget for it.

## Stage 3 — Continual improvement: closing the loop

- Manually review metric score distributions and patterns in low-performing instances
- **Automatically retrieve similar "fixed" traces as few-shot demonstrations for future
  inference**
- **Prioritize low-scoring traces for human review** on "a daily or weekly cadence,
  depending on your application's scale"
- **Active learning: "prioritize retrieving examples where human labels differed from what
  an LLM would predict"**
- Retrieve examples considering **both semantic similarity AND recency weighting**
- Set minimum semantic-similarity thresholds (example: **0.7**) for input relevance

> **"Prioritize examples where human labels differed from what an LLM would predict"** is
> the sharpest sampling rule in the source and it maps onto machinery we already have:
> note 11 §6's **abstentions route to humans → a free calibration set on exactly the hard
> cases**. The judge's abstention set *is* the active-learning query set. Two independent
> motivations, one queue.
>
> ⚠️ **But note the danger, which Shankar doesn't flag:** if human labels are collected
> *only* where the judge is uncertain, the resulting calibration set is **non-random by
> construction** and κ measured on it is **not** κ on production. It is κ on the hard tail —
> a *lower bound*, and a biased one. We need **two human queues**: (a) a uniform-random
> audit sample for unbiased κ and Tier-2 FP-rate estimation (note 06 §1: "the gold tier is
> the instrument that measures Tier 2's FP rate"), and (b) an uncertainty-sampled queue for
> cheap improvement. **Conflating them silently corrupts the headline reliability number.**
> This is the same Horvitz–Thompson lesson as note 06 §3: once selection is non-uniform, the
> naive average is biased — and it applies to *human labels* exactly as it does to judge
> samples.

## Failure modes identified

- Errors in early nodes of multi-step pipelines **amplify** through subsequent steps
- LLM-as-judge misaligns with human preferences without proper few-shot examples
- Uncalibrated next-token probabilities (above)
- **"Metric implementations drift over time as LLM APIs change and user preferences evolve"**
- **"Regular human labeling creates significant operational burden"**

Human remains essential: **"an AI engineer actually verifies new metric sets before
implementation."**

## Criteria drift (from "Who Validates the Validators?", UIST 2024)

> "**users need criteria to grade outputs, but grading outputs helps users define
> criteria**" — some criteria "appear dependent on the specific LLM outputs observed
> (rather than independent and definable a priori), raising serious questions for
> approaches that assume the independence of evaluation from observation of model outputs."

> **This is the deepest finding in the flywheel literature and it undermines a premise our
> design leans on.** Note 11 assumes a **frozen** rubric, a **frozen** anchor set, and
> content-addressed evaluator versions — i.e. that the criteria are definable a priori and
> held still while variants move. Criteria drift says **the rubric is itself a moving
> object that only stabilizes by looking at outputs**, which are produced by the variants
> we're grading. The eval and the thing evaluated are not independent.
>
> We can't dissolve this, but we can **contain** it: the rubric is *allowed* to change, but
> a rubric change is a **versioned, content-addressed release requiring re-baseline on the
> frozen golden set** (note 06 §7) — never a silent edit. Criteria drift then becomes a
> visible, dated event in the lineage rather than an invisible confound. **The honest
> framing: our eval doesn't measure a fixed construct over time; it measures a construct we
> re-ratify at each rubric version, and the golden set is what makes the re-ratification
> auditable.**
