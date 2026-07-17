---
title: Sampling (Langfuse)
url: https://langfuse.com/docs/observability/features/sampling
org: Langfuse
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Langfuse — Sampling

## The only platform with a documented DEFAULT

- Env var: `LANGFUSE_SAMPLE_RATE`
- **Default: `1`** — verbatim: "**the default value is 1, meaning that all traces are collected**"
- Range: verbatim "between 0 and 1"

This is a notable contrast with the eval-rule platforms (LangSmith/Braintrust/Weave), where sampling governs *which traces get evaluated*. **Langfuse's `LANGFUSE_SAMPLE_RATE` governs which traces get INGESTED AT ALL.** Different layer, different consequence: unsampled traces don't exist for debugging either.

## Configuration

- **Python**: constructor param `Langfuse(sample_rate=0.5)` → samples 50% of traces. Or set `LANGFUSE_SAMPLE_RATE` as a string env var.
- **JS/TS**: uses OpenTelemetry's `TraceIdRatioBasedSampler(0.2)` rather than a constructor param; also configurable via `LANGFUSE_SAMPLE_RATE`.

Caveat noted: "The Python SDK handles sampling **client-side** with straightforward rate parameters, while JS/TS implementations delegate to **OpenTelemetry's sampling infrastructure**, requiring configuration at the SDK initialization level rather than via constructor parameters."

Sampling is **client-side** — the decision happens in the SDK before data leaves the app. Consequence: it saves network/ingest/storage cost, not just eval cost. It also means the sample rate is a **deploy-time** setting, not a dashboard toggle (contrast: LangSmith/Braintrust/Weave rules are changeable server-side without redeploy).

## Sampling unit: the TRACE, and it is all-or-nothing

Verbatim: the SDK samples "**on the trace level** meaning that if a trace is sampled, **all observations and scores within that trace will be sampled as well**."

Verbatim: "**If a trace is not sampled, none of its observations (spans or generations) or associated scores will be sent to Langfuse**", which "can significantly reduce data volume for high-traffic applications."

Verbatim: "**Scores inherit the sampling decision of their parent trace to prevent 'orphaned' scores.**"

The orphaned-scores problem is the design rationale worth stealing: if sampling were per-span or per-score, you'd get scores referencing traces you never stored. Trace-level all-or-nothing sampling keeps the data model referentially closed.

## Mechanism — deterministic hash, no coordination

Verbatim: "The `TraceIdRatioBased` sampler uses a **deterministic hash of the 128-bit Trace ID**. If `hash(trace_id) < sample_rate`, the trace is marked as `RECORD_AND_SAMPLE`, ensuring that **all microservices or threads seeing the same Trace ID will reach the same sampling conclusion without communicating.**"

This is the important distributed-systems property: sampling is a **pure function of trace ID**, so a distributed multi-service agent produces complete or entirely-absent traces — never partial. No coordination, no sampling service, no shared state. Standard OTel `TraceIdRatioBased` semantics.

## LLM-as-judge evaluators

Guidance surfaced in search: for LLM-as-a-Judge evaluators, "sampling rate can be set to **5-10% initially** to control costs for evaluations." Langfuse evaluators are configured with their own sampling, layered *on top of* ingestion sampling — i.e. effective eval coverage = ingest_rate × eval_rate. Worth noting this multiplicative trap.

## Known issue

GitHub Discussion #8838, "Random Traces Appearing with 1.0 Sampling Rate" — reported inconsistency at full sampling. (Not verified in detail; flagged as a known-issues signal only.)
