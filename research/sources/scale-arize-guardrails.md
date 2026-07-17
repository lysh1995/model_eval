---
title: Guardrails (Arize AX)
url: https://arize.com/docs/ax/security-and-settings/llm-security/guardrails
org: Arize AI
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Arize AX — Guardrails (inline tier)

## Definition

Verbatim: "**Guardrails correct undesirable outputs at run-time, ensuring real-time safety and compliance.**"

Guardrails intercept LLM inputs or outputs **at runtime**, evaluate messages, and trigger corrective actions on validation failure. Same architectural split as W&B Weave: guardrails are inline and act on control flow; online evals are async and observational.

## Two guard types — and this IS the cascade

1. **Dataset Embeddings Guard**: compares message embeddings against a dataset of problematic examples using **cosine distance thresholds (default: 0.2)**.
2. **RAG LLM Guard**: for retrieval-augmented generation — Context Relevancy, QA Correctness, Hallucination detection.

The embeddings guard is the cheap tier made explicit: **no LLM call at all — just an embedding + a cosine distance compare against known-bad examples.** Default threshold **0.2**. This is the cheapest possible "evaluator": vector lookup, sub-10ms, deterministic, no judge. The RAG LLM Guard is the expensive tier for cases where semantic similarity to known-bad examples is insufficient.

Note this mirrors Galileo's argument from a different direction: Galileo makes the *model* cheap (SLM); Arize makes the *method* cheap (embedding distance, no generation).

## Published latency + accuracy numbers (Dataset Embeddings Guard, jailbreak detection)

- "**1.41 median latency** for end-to-end LLM call on GPT-3.5" (units almost certainly seconds — this is the *guarded end-to-end* figure, i.e. the guard's overhead is folded into a full LLM call)
- **Detection rate: 86.43% true positives** on **656 jailbreak prompts**
- **False positive rate: 13.95%** on **2000 regular prompts**

The FP rate is the load-bearing number: **~14% of legitimate prompts get flagged.** At 100% inline enforcement that is a serious UX tax — 1 in 7 normal users hitting a refusal. This quantifies why embedding guards are usually paired with a second-stage check rather than trusted alone to block, and it echoes the Phoenix hallucination-eval FP figure (12%) from the same vendor family.

## Corrective actions — block is not the only option

- `on_fail="fix"` → **Default response**: returns a hard-coded response
- `on_fail="reask"` → **LLM reask**: regenerates the response

`reask` is a meaningfully different design from binary block: on failure, re-generate rather than refuse. Costs a second LLM call on the failure path only, and preserves UX. The latency budget for a guard with `reask` must therefore include a potential full second generation — worst-case latency is roughly 2x the unguarded path, not guard_overhead + 1x.

## Models

Documentation demonstrates with OpenAI models but states: "**any model provider can be used with a Guard.**"

## Not documented

- No cost figures.
- No throughput metrics.
- No sampling strategy for guardrails (consistent with the cross-platform pattern: **guardrails don't sample**).
