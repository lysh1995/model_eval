---
title: "Inside the LLM Call: GenAI Observability with OpenTelemetry — GenAI semantic conventions"
url: https://opentelemetry.io/blog/2026/genai-observability/
org: OpenTelemetry / CNCF (GenAI SIG)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Event schema design for LLM traces — OTel GenAI semantic conventions

The emerging standard. Developed by the OpenTelemetry **GenAI SIG since April 2024**;
OpenTelemetry graduated CNCF and these are the standardized conventions. As of
**March 2026**, most GenAI semantic conventions are still in **experimental** status.

## Span attributes (verbatim names)

Core:
- `gen_ai.request.model` — the model used
- `gen_ai.usage.input_tokens` — input token count
- `gen_ai.usage.output_tokens` — output token count
- `gen_ai.response.finish_reasons` — why the model stopped generating

Content (structured):
- `gen_ai.system_instructions` — system prompt content
- `gen_ai.input.messages` — user messages
- `gen_ai.output.messages` — assistant responses

Tool calls: tool call arguments and results are recorded as span attributes when content
capture is enabled.

Note: `gen_ai.prompt` and `gen_ai.completion` are **deprecated** in favor of
`gen_ai.input.messages` / `gen_ai.output.messages`.

## Metrics

- `gen_ai.client.operation.duration` — histogram measuring LLM call latencies
- `gen_ai.client.token.usage` — histogram tracking token consumption
  - filterable by `gen_ai.token.type` to distinguish input from output tokens

## Content capture guidance — important for sizing

> "**By default, no prompt content or tool arguments are captured** with GenAI
> telemetry, as these can contain sensitive data."

Only metadata (model names, token counts, durations) is included by default. Content
capture must be **explicitly enabled** via configuration.

This is the single most important schema decision for storage sizing, and the standard's
default is instructive: metadata-only spans are small and cheap; content capture is what
blows up the byte budget.

## Compatibility

`OTEL_SEMCONV_STABILITY_OPT_IN` environment variable allows **dual-emission** of both
legacy and new attribute names, maintaining compatibility during version transitions.

## Bytes-per-event sizing for our platform

Two tiers, and the split matters enormously:

**Tier 1 — metadata-only event** (model, character_id, language, variant, token counts,
latency, finish_reason, judge scores, timestamps, user_id, session_id):
~20-30 columns, mostly LowCardinality enums and small ints.
Comparable to the Tinybird telemetry schema at **~126 bytes/row uncompressed**.
At 5-10x compression → **~15-25 bytes/row on disk**.

50M/day x ~20 bytes = **~1 GB/day compressed** = **~365 GB/year**. Trivial.

**Tier 2 — with prompt/completion text:**
A companion-chat turn is realistically ~200-800 tokens in + ~100-300 tokens out
→ roughly **1-4 KB of UTF-8 text per generation**. Say **~2 KB/generation** uncompressed.
50M/day x 2 KB = **100 GB/day raw**. With ZSTD at ~3-5x on text (and Character.AI's
reported **15-20x** average across columns, which includes their enum columns) →
**~20-35 GB/day** = **7-13 TB/year**.

**Conclusion:** text payloads are **~100x** the storage of metadata. The architecture
should split them: metadata in a hot, heavily-indexed MergeTree with long retention;
raw text in a separate table with short TTL (30-90 days) and `CODEC(ZSTD)`, or sampled,
or offloaded to object storage / S3-backed MergeTree. All drift statistics run off the
metadata + precomputed embeddings/scores, never off the raw text.
