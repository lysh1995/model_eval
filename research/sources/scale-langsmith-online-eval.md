---
title: Set up online evaluators (LangSmith)
url: https://docs.langchain.com/langsmith/online-evaluations
org: LangChain / LangSmith
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# LangSmith — Online Evaluations

## Sampling rate configuration

Verbatim: "Configure a sampling rate to control the percentage of filtered runs that trigger the automation action."

Worked example, verbatim: "to control costs, you may want to set a filter to only apply the evaluator to 10% of traces. In order to do this, you would set the sampling rate to 0.1."

- Sampling rate is expressed as a **decimal between 0 and 1** (0.1 = 10%, 0.5 = 50%).
- Sampling is a property of the **automation rule**, not of the SDK/client.
- No documented platform default sampling rate; it is set per-rule at creation.
- Sampling is applied **after** the filter — i.e. filter first, then sample the filtered subset. This is the "filter → sample" ordering that matters for cost math.

## Filters (the other half of cost control)

Docs state filters work identically to trace filtering. Documented filter targets, verbatim:
- "Runs where a user left feedback indicating the response was unsatisfactory"
- "Runs that invoke a specific tool call"
- "Runs that match a particular piece of metadata (e.g. if you log traces with a `plan_type`)"

Note the pattern: metadata-keyed filters (`plan_type`) enable **tier-differentiated eval rates** — e.g. eval 100% of enterprise traffic, 1% of free tier, without separate instrumentation.

Related doc guidance (from the LLM-as-judge online evaluator page): "evaluate only threads under N turns or sample 10% of all threads" — i.e. filters and sampling are presented as interchangeable cost levers.

## Execution model — async

Online evaluators run as **automation rules over logged runs**, not in the request path. They are triggered by runs arriving, not by the app awaiting a result. Nothing in the online-eval docs describes a blocking mode.

Backfill, verbatim: "The backfill is processed as a background job, so you will not see the results immediately."

Backfill applies rules to historical runs via a toggle + date selection, **available only at rule creation time**. Progress is tracked through evaluator logs.

## Rule ordering / composition

Verbatim: "If you also have a webhook automation rule on this project and want the webhook payload to include this evaluator's scores, add a feedback filter to the webhook rule rather than relying on rule ordering."

Architecturally important: rule execution order is **not guaranteed**. Chaining ("score, then act on score") must be expressed as a *feedback filter on the downstream rule*, not as an ordering assumption. This is a real constraint on building cascade/tiered eval in LangSmith — you cascade via feedback-predicate rules, not sequencing.

## Not documented on this page

- No blocking/inline guardrail mode.
- No latency budget numbers.
- No throughput or volume figures.
- No published cost numbers beyond the 10%/0.1 illustration.
