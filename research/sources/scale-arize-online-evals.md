---
title: Run online evals on traces / Run evaluations in the UI (Arize AX)
url: https://arize.com/docs/ax/evaluate/online-evals
org: Arize AI
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Arize AX — Online Evals

Sources: https://arize.com/docs/ax/evaluate/online-evals and .../online-evals/run-evaluations-in-the-ui

## Sampling rate — the most explicit volume-tiered guidance published

**Range: 1–100%** ("define the percentage of data the task should run on (0–100)").

Verbatim tiering by application volume:
- **100%**: "Low-volume or critical applications where you want to evaluate every trace"
- **10–50%**: "High-volume applications balancing cost and coverage"
- **1–5%**: "Very high-volume applications where representative sampling is enough"

**Rollout recommendation, verbatim: "Start at 10–20% and increase once you have validated your evaluator is working correctly."**

This is the single most actionable published default in the survey. Note the reasoning is **not** primarily cost — it's *evaluator trust*. You sample low while you don't yet know if the judge is right, then raise coverage once validated. Sampling doubles as a blast-radius limiter on a possibly-broken evaluator.

No hard platform default; 10–20% is the documented starting recommendation.

Compare to Braintrust (1-10% high volume / 50-100% critical) — Arize's bands are consistently more generous at the same volume tier, but the two agree on the shape: **coverage inversely proportional to volume, overridden upward by criticality.**

## Scope hierarchy — session > trace > span, and where sampling binds

Three evaluator levels:
- **Span-level**: single subquery filters only
- **Trace-level**: full MSQ; "one score per trace written to root span"
- **Session-level**: full MSQ; "scores written to each turn's root span"

**Critical rule, verbatim: "Sampling is applied at the highest evaluator scope in the task: session > trace > span, and lower-level evaluators will run on all matching data within that sampled set."**

And: "Sampling applies **after admission**, at the trace/session unit level" — not at individual span level.

This is the most sophisticated sampling semantics found. Two consequences worth internalizing:
1. **Sampling unit ≠ billing unit.** A 10% session sample doesn't mean 10% of spans evaluated — it means 10% of sessions, then *every* matching span inside them. For a 50-turn companion session, 10% session sampling can mean far more eval calls than naive math suggests. Cost scales with sample_rate × (spans per session), and session length is the hidden multiplier.
2. **Sampling coherence**: like Langfuse's trace-level all-or-nothing, sampling at the top scope guarantees you get *complete* sessions rather than scattered fragments. For multi-turn/conversational analysis, a complete 10% is far more useful than a random 10% of turns — you can't judge a conversation from disconnected turns.

Order of operations across the whole industry is consistent: **filter (admission) → sample → evaluate.**

## Filters

Tasks support:
- Span kind (e.g., "LLM spans only")
- Model name
- Metadata tags
- Span attributes
- **Multi-span queries (MSQ)** for trace/session evals — pattern-based filtering with operators `AND` / `OR` / `NOT`, and `=>` (direct parent-child) / `->`.

MSQ is a differentiator: filters express *structural* patterns over the trace tree (e.g., "traces where a retrieval span is the direct parent of an LLM span"), not just flat attribute predicates. Braintrust's SQL filters are flat by comparison.

## Execution — async

- Cadence options: "**Run continuously on new data**" (rolling schedule) or "**One-Time Backfill**" for historical data. No specific interval documented.
- Verbatim: tasks run asynchronously; results "attach automatically" to spans after execution completes.
- Programmatic path: `async_evaluate_dataframe()`.

## Hard limit

Verbatim: evals can be applied to spans "**up to 14 days prior to the current day**." Backfill window is bounded — a real constraint on retroactive eval of a new metric.

## Evaluator sourcing

Pre-built LLM judge templates from the **Eval Hub** for continuous runs, or custom code-based evaluators via **Phoenix Evals** for programmatic control and external data integration.
