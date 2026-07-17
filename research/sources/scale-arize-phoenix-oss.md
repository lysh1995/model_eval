---
title: Phoenix User Guide — OSS eval framework and the Phoenix/Arize production split
url: https://arize.com/docs/phoenix/user-guide
org: Arize AI (Phoenix, open source)
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Arize Phoenix (OSS) — Production Positioning

Sources: https://arize.com/docs/phoenix/user-guide, https://github.com/Arize-ai/phoenix, https://phoenix.arize.com/integration/guardrails-ai/

## Phoenix is deliberately NOT the online-eval tier

Verbatim: "Phoenix's evaluation framework can be used to **generate ongoing assessments of LLM performance in production**."

But the online-eval capability is positioned as the commercial upsell. Verbatim: "**Phoenix and Arize use the same collector frameworks in development and production.**" Arize enhances Phoenix by enabling "**online evaluations**, allowing teams to set up **alerts if evaluation metrics...go beyond acceptable thresholds**." Arize focuses "on the production side" while Phoenix handles **development and staging**.

The product boundary is instructive for anyone building this in-house: **tracing/instrumentation is commoditized and open-source; the scheduled online-eval runner, sampling rules, and alerting are the commercial layer.** Phoenix gives you the collector and the eval *library* (you call evaluators yourself, typically batch over exported dataframes); Arize AX adds the *managed continuous runner* with sampling rates, task scheduling, and thresholds. Notably, the hard part being sold is not the evaluators — it's the orchestration around when/how often/on-what they run.

Phoenix Evals remains usable from Arize AX as the custom code-evaluator path (see scale-arize-online-evals.md), so the library/runner split is explicit in both directions.

## Sampling — the "evaluators are a sampling tool" framing

Guidance surfaced via secondary sources on Phoenix evaluators (notably regarding the hallucination evaluator):

Verbatim: "For most teams, evaluators are most useful as a **sampling tool** — **run them on a fraction of production traffic and use aggregate trends, not individual scores.**"

Context, verbatim: this is "particularly relevant for hallucination detection, where the **12% false positive rate** is significant for high-volume production use, making the evaluator most useful as a sampling tool."

**This is the most important epistemics point in the entire survey.** The argument is not primarily about cost — it's about **statistical validity**:
- At a ~12% FP rate, an *individual* score is unreliable (roughly 1 in 8 flags is wrong).
- But the *aggregate rate* across a sample is a stable, useful signal — errors average out.
- Therefore: sample, aggregate, watch trends. Do **not** act on individual scores, and do **not** put a 12%-FP evaluator inline as a blocking guardrail.

This reframes sampling from "a cost compromise that degrades your data" to "**the statistically appropriate use of a noisy instrument.**" Full coverage does not fix a 12% FP rate — it just gives you 8x more wrong individual verdicts at 8x the price. Aggregation, not coverage, is what makes a noisy evaluator useful.

Pairs directly with:
- **Arize AX's** "start at 10–20% and increase once you have validated your evaluator is working correctly" — sampling as evaluator-trust management.
- **Arize's Dataset Embeddings Guard**: 13.95% FP on 2000 regular prompts — nearly identical error profile, and the reason guards need `reask`/second-stage rather than hard block.
- **Humanloop's** human-calibration loop — sample to *measure* the autorater's error.

The through-line across all four: **the sampling rate is a function of evaluator reliability, not just traffic volume.** A noisy evaluator should be sampled and aggregated; only a validated, low-FP evaluator earns 100% coverage or a place inline.

## Guardrails

Verbatim: "**Add guardrails to your application to prevent malicious and erroneous inputs and outputs. Guardrails will be visualized in Phoenix.**" Guardrails are "attachable to spans and traces in the same fashion as evaluation metrics."

Phoenix integrates with **Guardrails AI** (third-party) rather than shipping its own inline enforcement — consistent with Phoenix being the observability/visualization layer. The unifying idea: **a guardrail result is just another span annotation.** Whatever produced it (inline guard, async evaluator, human), it lands in the same trace data model — the same convergence seen in Weave (`Call.feedback`).

Phoenix "includes patterns for RAG systems, production guardrails, and continuous monitoring."
