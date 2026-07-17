---
title: LLM Observability / Production Monitoring (Confident AI + DeepEval)
url: https://www.confident-ai.com/products/llm-observability
org: Confident AI (DeepEval)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Confident AI / DeepEval — Production Monitoring

Sources: https://www.confident-ai.com/products/llm-observability, https://deepwiki.com/confident-ai/deepeval/5.5-production-monitoring, https://deepeval.com/

## The anti-sampling position — marketed as a feature

Verbatim headline claim: "**Run eval metrics on 100% of traces — no sampling.**"

Confident AI is the second vendor (with Galileo) to market **no-sampling as the differentiator** rather than shipping sampling as a cost knob. The implicit argument: sampling is an admission that your eval stack is too expensive. Where Galileo justifies this with SLM economics, Confident AI justifies it with ingestion-priced billing (below) — if you're billed by GB rather than per-eval, full-coverage evaluation is affordable.

DeepEval nonetheless "supports **configurable sampling rates** for high-volume systems, allowing you to optimize trace collection." So sampling exists at the *trace collection* layer (like Langfuse) while eval runs at 100% of what's collected. Note the layering: **sampling moved down to ingestion, not eval.**

## Pricing — the only published $/volume figures in the survey

- **$1/GB** for ingestion and retention
- Tiered rates at scale: **$0.85/GB → $0.70/GB → $0.55/GB → $0.45/GB**

This is a structurally different cost model from the eval-rule platforms. Billing on **bytes ingested** rather than **evals executed** removes the incentive to sample evals, and relocates cost pressure onto trace *size* (payload trimming, context truncation) instead of trace *count*. If you're designing cost controls, note this changes which lever matters: with per-eval pricing you cut coverage; with per-GB pricing you cut payload.

## Execution — async, non-blocking

- Tracing via the **`@observe` decorator** and **`TraceManager`**; traces upload automatically to Confident AI.
- Verbatim: the system "automatically captures execution traces, **uploads them asynchronously**, and allows running metric evaluations on production data **without blocking application performance**."
- Verbatim: "**non-blocking trace capture with async worker threads**" and "continuous evaluation running metric collections on production traces to evaluate performance over time **without manual test case creation**."

Async worker threads = the standard telemetry pattern (buffer + background flush), so instrumentation cost is a queue push, not a network round-trip.

## Captured per trace

Verbatim: "Every LLM call is captured as a trace with full context including **inputs, outputs, tool calls, latency, token cost, and metadata**."

## Scale claims

- Built to handle "**millions of traces per month**"
- Dashboard examples (illustrative, not benchmarks): "**2.4M tokens**" across support agent sessions; "**1,247 active sessions**"; P95 endpoint latency `/chat` **1.2s–1.6s**, `/summarize` **780ms–910ms**; P50 **1.2s**
- Setup time claim: "**<2m**" for framework integration
- Model spend tracking examples: gpt-4o **$1,420+**, claude-3.5 **$890**

The P95 endpoint latencies (1.2–1.6s for `/chat`) are useful context for the guardrail-budget question: **if a typical chat endpoint is ~1.2s P95, a 152ms guardrail is ~13% overhead, while a 1s GLIDER-style judge nearly doubles it.** That ratio is the real argument for single-token evaluators inline.

## Alerting

Threshold-based alerts and quality-score filtering are configurable; a **"Sample Rate"** field appears in alert settings (i.e. sampling also exists as an *alert* throttle, distinct from eval sampling). Platform notifies "immediately when regressions or incidents occur."

## Integration

Supports "**OpenTelemetry, LangChain, or any major framework**."

## Not documented

- No guardrail latency numbers (Confident AI/DeepEval positions around observability + eval, not inline blocking).
- No explicit guardrails-vs-evaluators architectural split comparable to Weave/Arize. (DeepEval's sibling project **DeepTeam** covers guardrail deployment separately.)
