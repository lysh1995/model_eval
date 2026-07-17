---
title: "Guardrail latency budgets: inline blocking vs async sampled judging"
url: https://modelmetry.com/blog/latency-of-llm-guardrails
org: Modelmetry (plus cross-referenced vendor figures from Galileo/LangWatch surveys)
year: 2026
type: blog
accessed: 2026-07-16
topic: production-scale
---

# Guardrail latency

## The core distinction (from LangWatch's "LLM Evaluations Explained", 2026)

> A guardrail blocks a specific failure mode inline, with millisecond latency
> requirements. However, building an async evaluator when you need an inline guardrail
> means harmful outputs reach users; building a synchronous guardrail when you need an
> async evaluator means unacceptable p99 latency.

This is the cleanest statement of the two-lane architecture our brief needs: the
choice is not "which is better" but "which failure mode are you buying".

## Latency by guardrail complexity (Modelmetry)

**Caveat, stated plainly: the article presents these as illustrative/hypothetical
scenarios, NOT measured production data.** Treat as order-of-magnitude planning
figures, not benchmarks.

| Guardrail class | Latency overhead |
|---|---|
| **Basic** — keyword filters, regex checks | **5–10 ms** |
| **Moderate** — rule-based + ML combined | **20–50 ms** |
| **Comprehensive** — LLM-as-Judge evaluators, external APIs | **1–5 s** |

## Evaluator type comparison (qualitative, Modelmetry)

- **Rule-based**: "Generally very fast and predictable in terms of latency"
- **ML-based**: "More computationally intensive than rule-based evaluators, leading to
  higher latency"
- **LLM-as-Judge**: introduces "the highest latency as they require an additional LLM
  inference" call per evaluation

## Percentile framing

The article discusses p95/p99 as the metrics to track but gives **no measured values**.
Its worked illustration: "p95 latency is 200ms...p99 latency is 500ms".

## Vendor-published inline guardrail latencies (via Galileo's low-latency eval survey, 2026)

These are vendor self-reported marketing figures — directionally useful, independently
unverified:

| Product | Claimed latency |
|---|---|
| Galileo **Luna-2** | **< 200 ms** |
| **Lakera Guard** | **< 150 ms** |
| Azure AI Content Safety | ~1 s (near-real-time) |
| Patronus **Glider** | ~1 s (near-real-time) |
| LLM-as-judge (DeepEval / TruLens / Confident AI) | **1,000 ms+** — "best for CI/CD pipelines" |

## The key architectural trick: run guardrails in PARALLEL with the LLM call

> Run the guardrail check in parallel with your LLM call — fire both off, wait for both
> to return, then decide. Since LLM calls take way longer than ML-based guardrail checks
> (jailbreak detection, PII detection typically run in milliseconds), the guardrail
> finishes first and you're just waiting on the LLM anyway.

**This makes an input-side guardrail effectively free in wall-clock terms.** The
generation call dominates. An input guardrail at 10–50ms hides entirely inside a
multi-second generation.

**But note the asymmetry our design must respect:** this trick works for **input**
guardrails (you can start both at t=0). An **output** guardrail cannot run in parallel
with the generation that produces its input — it is strictly serial and its latency
adds to the user-visible total. Output-side checks must therefore be *much* cheaper
than input-side ones, or must operate on streaming chunks.

## The organizational constraint (worth quoting to the team)

> Above 200ms p50, the rail loses political support inside the product team.

This is a soft but real number: **~200ms p50 is the practical budget ceiling for
anything inline.** It rules out any LLM-as-judge on the inline path (1,000ms+) and
confirms guardrails must be classifiers/regex, not judges.

## Platform selection criteria (2026)

> Evaluator coverage across the seven metric categories, p95 latency under your
> real-time budget, span-level observability, and policy-as-code determine platform
> selection in 2026.

## Synthesis for our design

| Lane | Coverage | Mechanism | Budget |
|---|---|---|---|
| Inline guardrail | 100% | regex + small classifier, parallel w/ generation on input side | 5–50 ms; hard ceiling ~200 ms p50 |
| Async sampled judge | ~1% | LLM-as-judge, off the request path | seconds — irrelevant to user |
| Deep/gold judge | ~0.01% | strong model, batch | hours — irrelevant |

The 1,000ms+ LLM-judge figure is the quantitative proof that **judging cannot be
inline at 50M/day** — independent of cost, it would blow the latency budget by 5–10x.
Cost is the *second* reason; latency is the first.
