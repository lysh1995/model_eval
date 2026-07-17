---
title: Set up guardrails (W&B Weave)
url: https://docs.wandb.ai/weave/guides/evaluation/guardrails
org: Weights & Biases (Weave)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# W&B Weave — Guardrails (inline/blocking path)

Source of truth: `wandb/docs` repo, `weave/guides/evaluation/guardrails.mdx` (raw fetched; docs.wandb.ai renders it).

## Definition — the clearest guardrail/monitor split found across all platforms

Verbatim: "Guardrails intervene in your LLM application's behavior based on scores from LLM judges. **They run in real time before outputs reach users and can block or modify responses when scores exceed thresholds.** You can use guardrails to block toxic content, filter responses for personally identifiable information (PII), or block abusive input from users."

Verbatim: "Weave guardrails use **inline** Weave Scorers to assess the input from a user or the output from an LLM and adjust the LLM's responses **in real time**."

Verbatim: "If you want to **passively** score production traffic without modifying your application's control flow, use **monitors** instead."

Verbatim: "Unlike monitors, **guardrails require code changes because they affect your application's control flow.** However, **every scorer result from guardrails is automatically stored in Weave's database, so your guardrails also function as monitors without any extra configuration.** You can analyze historical scorer results regardless of how they were originally used."

**Key architectural insight**: same primitive (Scorer) serves both roles. The *call site* determines blocking vs. passive — `await call.apply_scorer(...)` in the request path = guardrail; UI-configured monitor = async. Guardrail results are free monitoring data.

## Latency budget guidance (qualitative — no published ms numbers)

Verbatim: "Because guardrails can **interrupt your application's control flow and change the course of its responses, they can impact performance if they're too complex.** For best performance, follow these recommendations:
* Keep guardrail logic minimal and fast.
* Cache common results.
* Avoid heavy external API calls.
* Initialize guardrails outside of your main functions to avoid repeated initialization costs."

Verbatim, on when init-outside-function matters most:
"* Your scorers load ML models.
* You're using local LLMs where **latency is critical**.
* Your scorers maintain network connections.
* You have **high-traffic applications**."

**No ms latency budget is published.** Guidance is qualitative: minimal logic, cache, avoid external calls, hoist initialization.

## Sampling

**Guardrails have no sampling rate.** Sampling is a monitor-only concept. This is logically necessary — a guardrail sampled at 10% blocks only 10% of bad content, which defeats the purpose. Confirms the cross-platform rule: **guardrails run at 100% or not at all; sampling belongs to the async tier.**

## Code pattern — the two-call structure

```python
result, call = generate_response.call(prompt)   # get result AND Call handle
score = await call.apply_scorer(moderation_scorer)  # blocking scorer
if not score.result.get("passed", True):
    return "I'm sorry, I can't provide that response due to content policy restrictions."
return result
```

The `.call()` variant (vs plain invocation) returns `(result, call)` so the scorer can attach to the trace. Scorer returns `passed` boolean → app branches.

Built-in scorer example: `OpenAIModerationScorer` (delegates to OpenAI moderation API — cheap/fast classifier, not an LLM judge). Custom example: `PIIDetectionScorer` = pure regex (email/phone/SSN patterns), `passed = len(detected_types) == 0`. **Note the tiering instinct: the guardrail examples are regex and moderation-API classifiers, not LLM judges** — cheap detectors inline.

AWS Bedrock integration: `BedrockGuardrailScorer(guardrail_id=..., guardrail_version="DRAFT", source="INPUT", bedrock_runtime_kwargs={"region_name": "us-east-1"})`. Supports **modify** as well as block: `score.result.metadata.get("modified_output")` returns rewritten content.

## Constraint

Verbatim: "The Weave TypeScript SDK doesn't support the tools required to set up guardrails." (Python-only for inline guardrails.)
