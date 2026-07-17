---
title: Set up custom monitors + Signals (W&B Weave)
url: https://docs.wandb.ai/weave/guides/evaluation/custom-monitors
org: Weights & Biases (Weave)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# W&B Weave — Monitors & Signals (async tier)

Sources: `wandb/docs` repo `weave/guides/evaluation/custom-monitors.mdx` and `monitors.mdx`; plus https://wandb.ai/site/online-evaluations/.

## Monitors = passive/async, no code changes

Verbatim: "Monitors use LLM judges to **passively** score production traffic to surface trends and issues in your LLM applications... Monitors automatically store all scoring results in Weave's database, so you can analyze historical trends and patterns."

Verbatim: "**Monitors require no code changes to your application. Set them up using the Weave UI.**"

Verbatim: "If you need to **actively intervene** in your application's behavior based on scores, use **guardrails** instead."

Verbatim (marketing page): "Weave's Online Evaluations **reside and run on the Weights & Biases environment, eliminating code dependencies, blocking, and extra latency.**"

Verbatim: "Choose precisely which traces your online evaluations run on with **random sampling and custom filters.**" / "Score only the calls that matter. Fully control sampling to keep your evaluations focused and efficient."

## Sampling rate — exact config

From the monitor creation modal, verbatim:
- "**Sampling rate**: The percentage of calls to score (**0% to 100%**)."
- Tip, verbatim: "**A lower sampling rate reduces costs, since each scoring call has an associated cost.**"

Worked example in docs sets "**Sampling rate**: Set to `100%` to score every call" (a demo/tutorial setting, not a production default).

**No documented production default.** Range is 0–100%, expressed as a percentage (contrast: LangSmith/Langfuse use 0–1 decimals).

## Selection axes (three, same as Braintrust)

- **Operations**: "Choose one or more `@weave.op`s to monitor. You must log at least one trace that uses the op before it appears in the list." — selection is **op-scoped**, a dimension Braintrust/LangSmith lack; you target a specific function, not a SQL predicate.
- **Filter** (optional): "Narrow which calls are eligible (for example, by `max_tokens` or `top_p`)."
- **Sampling rate**: 0–100%.

## Signals vs. custom monitors — the built-in tiering table (verbatim)

| | Signals | Custom monitors |
|---|---------|----------------|
| **Configuration** | One-click enable, no prompt writing | Full control over scoring prompt, model, and parameters |
| **Scope** | Preset quality and error classifiers | Any evaluation criteria you define |
| **Trace selection** | Automatic (successful root traces for quality, failed traces for errors) | Configurable operations, filters, and sampling rate |
| **Model** | Serverless Inference (preset) | Any commercial or Serverless Inference model |
| **Use case** | Quick production monitoring with proven classifiers | Custom evaluation criteria specific to your application |

**Signals have no user-facing sampling rate** — trace selection is automatic and *predicate-based*: quality signals run on **successful root traces**, error signals on **failed traces**. This is routing-by-outcome rather than random sampling — a distinct cost-control strategy: you don't sample randomly, you sample the *interesting* population.

Docs note: "Custom monitors are the previous approach to monitoring production traffic. For new implementations, use **Signals**." — W&B is moving from user-configured sampling toward preset, outcome-routed classifiers.

## Signals — 13 presets, batched into ONE LLM call

Verbatim: "13 preset signals organized into two groups."
- **Quality (7)**: "Hallucination," "Low quality," "User frustration," "Jailbreaking," "NSFW," "Lazy," "Forgetful."
- **Error (6)**: "Network Error," "Ratelimited," "Request Too Large," "Bad Request," "Bad Response," "Bug."

Verbatim mechanism: Weave uses an "LLM-as-a-judge approach to classify traces." The system "constructs a prompt that includes the trace metadata, inputs, outputs, exception details (if any), and the operation's source code."

**Critical cost-architecture detail, verbatim: "For multiple active signals, Weave batches the signals into a single LLM call."**

This is the key cost lever besides sampling: **N classifiers cost 1 LLM call, not N.** Amortizing judges across a shared prompt is an alternative to reducing sampling rate — you cut the constant, not the coverage. Note it also feeds the op's *source code* into the judge prompt.

## Storage

Verbatim: "Weave automatically stores all scorer results in the Call object's `feedback` field." Same sink for guardrail and monitor results.

Judge model selection: any commercial LLM configured in the W&B account, or W&B **Serverless Inference** models (preset default for Signals). Docs example uses `o3-mini-2025-01-31` as judge. Supports audio- and image-enabled judges via Media Scoring JSON Paths (RFC 9535 JSONPath).
