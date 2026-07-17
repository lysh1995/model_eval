---
title: "Guard model serving costs and latency — list prices and published benchmarks"
url: "https://www.together.ai/pricing , https://groq.com/pricing , https://aws.amazon.com/bedrock/pricing/ , https://developers.openai.com/api/docs/guides/moderation"
authors: "Various (Together AI, Groq, AWS, OpenAI; compiled)"
year: 2026
type: api-doc
accessed: 2026-07-16
topic: roleplay-safety
---

# Guard Model Serving Costs & Latency

## Summary

**Headline finding: essentially nobody publishes latency or throughput numbers for guard models.** Not Meta (Llama Guard 3/4), not Google (ShieldGemma), not AI2 (WildGuard), not OpenAI (Moderation API). The academic papers report F1 and nothing else; the inference providers report $/token and nothing model-specific for guards.

**Everything below is either a LIST PRICE or explicitly marked "not published." No latency number in this file is a measurement of a guard model.** Per the brief, nothing is invented or approximated. **We must run our own benchmark before any capacity plan is finalized.**

## Key numbers (verbatim) — cost

### Hosted moderation endpoints

| Service | Price | Source | Confidence |
|---|---|---|---|
| **OpenAI Moderation** (`omni-moderation-latest`) | **FREE** — "The moderation endpoint is free to use" | developers.openai.com moderation guide | ✅ Verbatim from docs |
| **Perspective API** | **FREE**, but **1 QPS** default quota, quota increases closed since Feb 2026, **service ends Dec 31 2026** | perspectiveapi.com | ✅ Verbatim; see `safety-perspective-api.md` |
| **Together AI — Llama Guard 4 12B** | **$0.20 per 1M tokens** | together.ai/pricing, accessed 2026-07-16 | ✅ List price |
| **AWS Bedrock Guardrails** — content filters / denied topics | **$0.15 per 1,000 text units** | aws.amazon.com/bedrock/pricing | ✅ List price |
| AWS Bedrock Guardrails — sensitive information filters | **$0.10 per 1,000 text units** | AWS | ✅ List price |
| AWS Bedrock Guardrails — contextual grounding checks | **$0.10 per 1,000 text units** | AWS | ✅ List price |
| AWS Bedrock Guardrails — automated reasoning checks | **$0.17 per 1,000 text units** | AWS | ✅ List price |
| AWS Bedrock Guardrails — word filters, regex filters | **No charge** | AWS | ✅ List price |
| **AWS Bedrock — Llama Guard 3 8B** | **NOT PUBLISHED / not listed** as a standalone Bedrock model | — | ❌ Not found |
| **Groq — Llama Guard (any variant)** | **NOT OFFERED / not listed** on Groq's pricing page | groq.com/pricing | ❌ Not found |
| **Together AI — Llama Guard 3 8B** | **NOT LISTED** on current pricing page (only Llama Guard 4 12B appears) | together.ai/pricing | ❌ Not found |
| **Fireworks — Llama Guard** | **NOT FOUND** in published pricing | — | ❌ Not found |

### Adjacent / proxy prices (NOT guard models — use only as order-of-magnitude proxies for self-hosted small models)

| Model | Price | Source | Note |
|---|---|---|---|
| Groq — **Prompt Guard** | **$0.03–$0.04 per 1M tokens** | Groq (via aipricing.guru) | ⚠️ **Different model** — prompt-injection/jailbreak detection, *not* content moderation. Useful as evidence of what a small guard-class model costs to serve. |
| Groq — Llama 3.1 8B Instant | **$0.05 per 1M input tokens** | groq.com/pricing | ⚠️ Proxy for 8B-class serving cost |
| Together AI — Llama 3.1 8B | **$0.18 per 1M** | via aipricing.guru | ⚠️ Proxy |
| Fireworks — Llama 3.1 8B | **$0.20 per 1M** | via aipricing.guru | ⚠️ Proxy |
| Groq — Llama 3.3 70B | **$0.59 input / $0.79 output per 1M**, reported at **394 tok/s** | morphllm comparison | ⚠️ Proxy; the 394 tok/s is a *generation* throughput for a 70B chat model, **not** a guard-model classification latency |
| Fireworks — Llama 70B | **$0.90 per 1M** | tokenmix | ⚠️ Proxy |

**Note:** Llama Guard 3-1B is not offered by any major hosted inference provider found. It is designed for on-device/self-hosted deployment. **If we want 1B guard economics, we must self-host it.**

## Key numbers — latency / throughput

| Model | Latency | Throughput | Source |
|---|---|---|---|
| **Llama Guard 3-1B** | **NOT PUBLISHED** | **NOT PUBLISHED** | Meta publishes no ms or tok/s; describes it only as suitable for on-device deployment |
| **Llama Guard 3-8B** | **NOT PUBLISHED** | **NOT PUBLISHED** | Model card notes vLLM/SGLang support, INT8 checkpoint ~40% smaller, no perf numbers |
| **Llama Guard 4-12B** | **NOT PUBLISHED** | **NOT PUBLISHED** | — |
| **ShieldGemma 2B/9B/27B** | **NOT PUBLISHED** | **NOT PUBLISHED** | Paper reports F1/AU-PRC only |
| **WildGuard 7B** | **NOT PUBLISHED** | **NOT PUBLISHED** | Paper reports F1 only |
| **OpenAI Moderation API** | **NOT PUBLISHED** by OpenAI. Third-party anecdote: ~1–1.5s at scale (Lasso Moderation blog) | — | ⚠️ Unverified third-party claim; **benchmark before relying on it** |
| **Perspective API** | **NOT PUBLISHED / no SLA.** Third-party: 200ms–2s+ under load (Lasso) | 1 QPS default | ⚠️ Unverified third-party claim |

**General vLLM context (NOT guard-specific, do not use for planning):** published Llama 3.1 8B vLLM benchmarks on H100 vs A100 show A100 taking ~6x longer to first token on average (up to 16x at 16 concurrent requests). H200 > H100 > A100. This tells us GPU choice matters a lot; it tells us nothing about Llama Guard 3-1B specifically.

## Cost model for 100% traffic coverage (derived — arithmetic on list prices only)

**Critical modeling insight: guard models are classifiers. Output is ~3–10 tokens (`safe` / `unsafe\nS11`). Cost is ~entirely INPUT tokens.** This makes them dramatically cheaper than chat models at the same $/M rate, and it means output pricing is irrelevant.

Assume a companion turn requires classifying ~500 input tokens (recent context + current message).

| Option | $/1M tokens | Cost per turn | Cost per 1M turns | Cost per 100M turns/mo |
|---|---|---|---|---|
| **OpenAI Moderation** | **$0** | **$0** | **$0** | **$0** |
| **Together Llama Guard 4 12B** | $0.20 | $0.0001 | **$100** | **$10,000** |
| **Bedrock Guardrails** (content filter) | $0.15 / 1k text units | depends on text-unit definition* | — | — |
| Self-hosted Llama Guard 3-1B INT4 | GPU-hour cost | **unknown — must benchmark** | — | — |

\* A Bedrock "text unit" is up to 1,000 characters. A ~500-token turn ≈ ~2,000 chars ≈ 2 text units ≈ **$0.0003/turn ≈ $300 per 1M turns** — **3x more expensive than Together's Llama Guard 4** and infinitely more than free. *This arithmetic is derived, not quoted; verify the text-unit definition against AWS docs.*

**Conclusion from the arithmetic: at 100M turns/month, tier-1 moderation costs either $0 (OpenAI) or ~$10k/mo (Together Llama Guard 4). Both are affordable. The 100%-coverage question is settled on cost — it comes down to latency and policy fit, which is exactly what nobody publishes.**

## Relevance to a roleplay/companion eval product

- **Cost is not the binding constraint for tier-1. Latency is — and it is completely unmeasured in the public literature.** This is the biggest gap in the whole research set and the clearest reason to spend a week on an internal benchmark. Our capacity plan cannot be built on published numbers because they do not exist.
- **Recommended benchmark (concrete next step):** serve Llama Guard 3-1B INT4 and ShieldGemma 2B on vLLM on one A10G/L4 and one H100, at 500-token inputs, measuring p50/p95/p99 **time-to-first-token** (not generation throughput — we only need ~5 output tokens, so TTFT ≈ total latency). Report $/1M turns at realistic utilization. This is a small, well-defined experiment that would produce numbers **that do not currently exist publicly** — which is a mild content-marketing asset in its own right.
- **The free OpenAI endpoint makes the build/buy call easy to start:** ship on OpenAI Moderation (free, 13 categories, multimodal, covers CSAM + self-harm), and treat self-hosted Llama Guard/ShieldGemma as (a) a hedge, and (b) the **only** option for customers whose NSFW content can't be routed to OpenAI or who need EU data residency. That second group is a large share of the companion market — so self-hosting is a real product requirement, not just a hedge, and it's why the latency benchmark matters.
- **Budget the tier-2 judge, not tier-1.** Since tier-1 is $0–$10k/mo, essentially our whole moderation budget is free for the sycophancy/manipulation judges that actually differentiate us. Those use frontier models and are 100–1000x the per-call cost, so they must be **sampled**. Concentrate the sample where the research says value is: **farewell turns** (37% manipulation rate — De Freitas), flagged turns, and a random baseline slice for drift.
- **Don't pay for Bedrock Guardrails.** Derived arithmetic puts it ~3x Together's Llama Guard 4 and it's a closed taxonomy we can't tune for roleplay (no ability to disable a sexual-content category the way Llama Guard's prompt allows). Its only draw is AWS-native compliance.
- **Llama Guard 3-1B being unavailable on every hosted provider is a real signal:** the market serves 8B+ guards, so the cheap on-device tier only exists if we build it. That's friction, but also a moat — a well-benchmarked, roleplay-tuned 1B guard is something no vendor currently sells.
