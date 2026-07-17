---
title: "Langfuse Data Model — traces, observations, sessions, scores, datasets"
url: https://langfuse.com/docs/observability/data-model
org: Langfuse
year: 2026
type: product-docs
accessed: 2026-07-16
topic: eval-lifecycle
---

# Langfuse data model

Also covers https://langfuse.com/docs/evaluation/data-model and
https://langfuse.com/docs/evaluation/scores/data-model

## Core hierarchy — three levels

> "Langfuse organizes an application's data into three core concepts: observations,
> traces, and sessions."

**Trace** — "A trace typically represents a single request or operation. For example,
when a user asks a question to a chatbot, that interaction, from the user's question to
the bot's response, is captured as one trace." It is a **container of observations**.

**Observation** — "the individual steps within a trace", nestable. Typed:
- `span` — generic step
- `generation` — "a special span representing a single LLM call, carrying the model name,
  prompt, completion, token usage, and cost"
- `event` — point-in-time
- plus tool calls, retrieval steps

**Session** — "Optionally, traces can be grouped into sessions. Sessions are used to group
traces that are part of the same user interaction." / "A session groups multiple traces
that belong to one conversation or user journey — for example, every turn of a multi-message
chat."

Attribute propagation: traces propagate `user_id`, `session_id`, `tags`, `metadata` to
child observations.

Built on OpenTelemetry: *"Langfuse is built on OpenTelemetry, an open standard for
collecting telemetry data from applications."*

> **The mapping that matters for a roleplay product:**
> `session` = the whole roleplay conversation (our 102-turn dialogue)
> `trace`   = one user turn → one AI reply
> `generation` = one model call inside that turn
>
> This is a **three-level** model. OTel GenAI is effectively **two-level** (span +
> conversation.id label). Note 06 §2 concluded the **session is the sampling unit**;
> Langfuse is the only mainstream schema that gives the session an ID *and* lets a score
> attach to it directly.

## Scores — the evaluation object

> "Scores are the data object to store evaluation results. They are used to assign
> evaluation scores to **traces, observations, sessions, or dataset runs**."

Four data types: **Numeric, Categorical, Boolean, Text**.

Score object fields: `name`, `value`, `comment` (+ target id, source).

**Score configs:**
> "Score configs are used to ensure that your scores follow a specific schema. Using score
> configs allows you to standardize your scoring schema across your team and ensure that
> scores are consistent and comparable for future analysis."

> **Two things to steal:**
> 1. **A score can attach to a SESSION.** This is the thing OTel cannot express and the
>    thing note 11 §6–7 requires (min-over-turns is a session-level score; the conversation
>    is the sampling unit). In OTel we would have to invent it.
> 2. **Score configs = a registered schema per metric.** This is the enforcement point for
>    note 11's "no dimension ships without its noise floor" gate — the config is where a
>    dimension is declared before it can be written.
>
> ⚠️ But note the **Text** score type and free `comment` field: Langfuse's score is
> still a *scalar + note*. **No pairwise comparison primitive, and no evaluator-version
> field.** Same gap as OTel and OpenInference. Every platform surveyed stores
> `(name, value)` and leaves "which judge, which rubric" to `metadata`.

## Datasets / experiments

**DatasetItem** fields:
```
id, datasetId, input, expectedOutput, metadata,
sourceTraceId, sourceObservationId,
status  (ACTIVE | ARCHIVED),
mediaReferences
```

> **`sourceTraceId` / `sourceObservationId` are the flywheel primitive.** They are a
> **permanent back-pointer from a benchmark item to the production trace it was mined
> from.** This is what makes "promote a production failure into the regression suite"
> auditable rather than a copy-paste. Adopt this field verbatim.
>
> **`status: ACTIVE | ARCHIVED`** — dataset items are *retired, never deleted*. That is
> the mechanism for eval-set drift management (see `pipeline-eval-set-drift.md`): you can
> re-run a historical benchmark exactly as it was by filtering on status-at-a-timestamp.

**DatasetRun** (= experiment run) contains **DatasetRunItems** linking:
```
datasetItemId  -> the input
traceId        -> execution result (primary)
observationId  -> optional
```

Scores connect to: traces (1 trace → n scores), observations (1 observation → n scores),
dataset runs (aggregate metrics via run evaluators).

## Function definitions

- **Task**: "Takes dataset item input, returns application output during experiment execution"
- **Evaluator**: "function that scores the output of a task for a single dataset item" —
  receives input, output, expected output, metadata; returns an Evaluation → becomes a Score
- **Run Evaluator**: "Assesses complete experiment results, computing aggregate metrics
  attached to dataset runs"

> **The Run Evaluator is the primitive our design needs and most platforms lack.** Note 11
> §4 (shrinkage), §7 (mixed-effects on ~95 characters), and note 06 §3 (Horvitz–Thompson
> reweighting) are all **aggregate-level computations that cannot be expressed as a
> per-item scorer.** A platform that only supports per-item evaluators structurally cannot
> host our statistics. Langfuse's run-evaluator is the right shape; whether it is powerful
> enough to fit a BT model is another question.

## Sampling

`LANGFUSE_SAMPLE_RATE` defaults to `1`. Governs **ingestion**, not evaluation. Trace-level
all-or-nothing via deterministic trace-id hash; *"Scores inherit the sampling decision of
their parent trace to prevent 'orphaned' scores."* (see note 06 §1)

## Known limitation (verbatim)

> "Local dataset experiments create traces only; no dataset runs or comparison views are
> generated currently."
