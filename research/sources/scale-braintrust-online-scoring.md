---
title: Score production traces / Online scoring (Braintrust)
url: https://www.braintrust.dev/docs/evaluate/score-online
org: Braintrust
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Braintrust — Online Scoring

## Rule model

Verbatim: online scoring rules are "defined at the project level and specify which scorers and classifiers to run, how often, and on which logs." They "automatically evaluate production traces as they arrive."

Three axes per rule: **which scorers** × **sampling rate** ("how often") × **SQL filter** ("on which logs"). Rules are configured at project level via the Configuration page. Multiple rules with different sampling rates and filters can coexist.

## Sampling rate — the most concrete published guidance found

Verbatim recommendations:
- **High-volume applications**: "use lower rates (1-10%) to manage costs"
- **Low-volume or critical applications**: "can use higher rates (50-100%) for comprehensive coverage"

Verbatim: each rule "uses a sampling rate to control the proportion of the matching traffic that is scored, with high-volume applications usually scoring a smaller percentage to manage cost, while critical workflows can use higher sampling when fuller production coverage is needed."

**No default sampling rate is specified in the documentation.** The 1-10% / 50-100% split is guidance, not a default.

## Execution model — async, explicitly zero-latency

Verbatim: the system runs "evaluations asynchronously in the background" without "adding latency to your application."

Verbatim: scoring provides "continuous quality monitoring without affecting your application's latency or performance."

Verbatim (from the related how-to-eval material): "online scoring does not add application latency because scoring runs asynchronously after traces are logged, and the agent can respond to the user without waiting for the scoring rule to finish."

This is the clearest statement of the **observability-eval vs. guardrail** split: Braintrust's online scoring is explicitly *not* a guardrail. It is post-hoc, off the request path, by design.

## SQL filters

- Filters use "a SQL filter clause" matching spans on "input, output, metadata, etc."
- Documented limitation, verbatim: "The `!=` operator is not supported in SQL filters for online scoring. Use `IS NOT` instead."
- **Trace-scoped rules**: "the filter matches if any span in the trace satisfies the condition."
- **Span-scoped rules**: "it applies to each candidate span individually."

The trace-vs-span scoping distinction is the sampling-unit question: sampling 10% of *spans* and 10% of *traces* give very different coverage for multi-step agents.

## Cost control guidance

Verbatim: "LLM-as-a-judge scorers have higher latency and costs than code-based alternatives. Factor this into your sampling rate decisions."

This is the seed of the **cascade pattern**: cheap code scorers at high/full sampling, expensive LLM judges at low sampling. Braintrust states the cost asymmetry explicitly but leaves the tiering to the user's rule configuration.

## Not documented

- No throughput or volume metrics.
- No latency numbers (only the qualitative "zero added latency" claim).
- No default sampling rate.
