---
title: Patronus Evaluators — GLIDER, Lynx, Judge (small vs large evaluator tiering)
url: https://www.patronus.ai/blog/patronus-evaluators
org: Patronus AI
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Patronus AI — Evaluator Tiering

Sources: https://www.patronus.ai/blog/patronus-evaluators, https://docs.patronus.ai/docs/research_and_differentiators/Glider, https://arxiv.org/abs/2412.14140, https://www.patronus.ai/announcements/patronus-ai-launches-industry-first-self-serve-api-for-ai-evaluation-and-guardrails

## The tiering is the product — explicit small/large split

Verbatim: Patronus "offers **Small and Large Evaluators tailored for both real-time and offline use cases**."

Verbatim: Patronus "provides small and large LM-as-judge models: **one for quick, real-time guardrails and another for longer, more accurate analysis**."

This is the **cleanest articulation of the cascade pattern** in the survey. Where LangSmith/Braintrust/Weave leave tiering to user configuration, Patronus ships two *model classes* mapped to the two latency regimes:
- **Small → real-time guardrails** (inline, ~1s budget)
- **Large → offline / deeper analysis** (async, accuracy-maximizing)

Evaluator families on the platform:
- **Glider** — "quick guardrails and checks, fast and accurate", in-house model
- **Judge** — "powerful and customizable LLMs-as-a-Judge"
- **Judge MM** — "based on Gemini", multimodal

Evaluators are defined over "**four components: input, output, retrieved context, and gold answer**."

## GLIDER — the real-time tier

- **3.8B parameters** (docs also say "3B parameter custom evaluator model trained by Patronus AI"; the paper says 3.8B — recorded as published)
- **Base model: `phi-3.5-mini-instruct`**
- Latency: "**approximately 1-second eval latency**, making it suitable for **near-real-time** applications"
- Training data: "synthetic data that spans **183 different research and industrial evaluation metrics** from **685 relevant domains** of application"
- Output scales: "**0-1, 1-3, and 1-5 Likert scale** rankings"
- Paper: GLIDER: Grading LLM Interactions and Decisions using Explainable Ranking, arXiv 2412.14140

Performance:
- "outperforms GPT-4o on the FLASK dataset" — **FLASK: 0.615 ±0.01 Pearson correlation vs GPT-4o's 0.610**
- "competes with open source models **17x its size**" on pairwise and pointwise ranking tasks

## The explainability contrast with Galileo — a genuine fork in the design space

GLIDER, verbatim: "For every evaluation, GLIDER outputs a **list of detailed reasons behind the score, highlighting the most critical phrases from the input** that influenced the result." Produces "**high quality reasoning chains and text highlight spans**" plus multilingual reasoning.

**This is the direct opposite bet from Galileo's Luna-2.** Both use SLMs to cut judge cost, but:
- **Luna-2**: single-token verdict → ~152ms, deterministic, **no rationale**
- **GLIDER**: full reasoning chain + span highlights → **~1s**, non-deterministic decode, **fully explainable**

The ~6x latency gap is precisely the cost of generating the explanation. The tradeoff to internalize: **reasoning chains cost you an order of magnitude in latency and forfeit determinism.** For an inline blocking guardrail, Luna-2's bet is right. For triage/analysis of *why* something failed — where a human reads the output — GLIDER's bet is right. Span highlights are especially valuable for human review queues.

This maps onto the tiering cleanly: **fast opaque verdict inline; slow explainable verdict async.** Explainability is an async-tier luxury.

## Lynx — hallucination detection

Verbatim: "Lynx is Patronus AI's flagship hallucination detection model that **outperforms GPT-4o at detecting inaccuracies in retrieval-augmented generation (RAG) systems**." Platform "enables the use of **Lynx, GLIDER, and many other judge LLMs** for evaluation tasks."

## API / pricing

Patronus launched an "**industry-first self-serve API for AI evaluation and guardrails**" (Nov 2024). The API "offers the flexibility to configure LLM judges that evaluate custom criteria across capabilities, safety, and alignment, with a **flexible, usage-based pricing model**." No published per-call rates or sampling configuration found.

## Not documented

- No sampling rate configuration found (Patronus is evaluator-API-shaped rather than trace-rule-shaped; sampling is the caller's responsibility).
- No throughput numbers.
- No explicit ms latency budget beyond GLIDER's "~1 second."
