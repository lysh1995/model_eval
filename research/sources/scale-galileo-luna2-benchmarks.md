---
title: Luna-2 product page + docs (latency/cost benchmark tables)
url: https://galileo.ai/luna-2
org: Galileo
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Galileo Luna-2 — Published Benchmark Numbers

Sources: https://galileo.ai/luna-2 and https://docs.galileo.ai/concepts/luna/luna

## Head-to-head comparison table (verbatim values from galileo.ai/luna-2)

| | Luna-2 | GPT 5.4 | GPT 5.4 mini | Azure Content Safety |
|---|---|---|---|---|
| **Avg latency** | **152ms** | 3200ms | 2600ms | 312ms |
| **Cost / M tokens** | **$0.12** | $5.00 | $0.15 | $1.52 |
| **Max tokens** | 128k | 128k | 128k | 3k |
| **Accuracy** | **0.95** | 0.94 | 0.90 | 0.62 |

Reading: Luna-2 is **~21x faster than GPT 5.4** (152ms vs 3200ms) at **~42x lower cost** ($0.12 vs $5.00) with **equal-or-better accuracy** (0.95 vs 0.94). Consistent with the paper's "20x latency / 80x cost" claims. Against Azure Content Safety — the closest dedicated-guardrail comparable — Luna-2 is 2x faster, 12x cheaper, and dramatically more accurate (0.95 vs 0.62); note ACS's 3k max-token limit makes it unusable for long-context agent traces.

## Latency budget statements

- "**sub-200 ms**" for multi-metric scoring on **L4 GPUs**
- Verbatim: "even when running **10–20 checks at once**, Luna stays under **sub-200 ms on L4 GPUs**"
- Verbatim: "score AI outputs across **20+ metrics simultaneously**, running at **sub-200ms latency** so they can operate as **real-time guardrails without adding noticeable delay**"
- Verbatim: "Luna-2 small language models run evaluations at **sub-200ms latency**, making **100% traffic monitoring economically feasible**"

**~200ms is the de facto guardrail latency budget** — the only explicit number in the industry. Note it holds for 10–20 concurrent checks, not one; the adapter architecture means check count is nearly free.

## Latency by request size (from docs.galileo.ai, 3B model on H100/H200)

| Input size | Latency |
|---|---|
| 500 tokens (small) | **15ms** |
| 2K tokens (medium) | **15ms** |
| 15K tokens | **141ms** |
| 100K tokens | **2.8s** |

Highly informative shape: **latency is flat (~15ms) up to ~2K tokens, then scales with context.** Prefill-dominated — the single-token decode is free, so cost is entirely in reading the input. Implication for design: **guardrail latency is a function of how much context you feed the judge, not of the judge's verdict complexity.** Trimming judge input is the highest-leverage latency optimization. At 100K tokens (2.8s) an inline guardrail is no longer viable — long-context eval must be async regardless of model speed.

Note the discrepancy vs. the marketing table: docs quote **$0.02/M tokens** ("an order of magnitude cheaper" than GPT-4o at $2.50/M), while the product page quotes **$0.12/M**. Different configs/generations or list-vs-effective pricing; both recorded as published.

## Model specs

- **Fine-tuned Llama models, 3B and 8B variants** (decoder-only SLMs)
- Classification via "**normalized log-probabilities of True/False tokens**"
- "**Lightweight adapters on a shared base model**" supporting "**hundreds of metrics**"
- 128k max context
- Local/on-prem deployment supported (matters for data-residency-constrained guardrails)

## Fine-tuning

Verbatim: "**Approximately 4,000 samples**" needed for effective fine-tuning to a specific use case. Useful calibration for "how much labeled data before a custom evaluator beats a general judge."

## Production scale (repeated across sources)

- "protecting **100M+ AI sessions**"
- "processing over **100B tokens per month**"
- "eval cost savings of over **$30M annually**"

## Positioning statement

Verbatim: "Luna's fine-tuned SLMs deliver **millisecond-level verdicts** while staying **pennies-per-million-tokens** — perfect for **always-on evaluation pipelines**." / "low-cost production monitoring and real-time guardrailing for every AI system — **without the GPT-sized bill**."

"Always-on" is the explicit anti-sampling pitch: Galileo's product thesis is that sampling is a tax you pay for using the wrong evaluator.
