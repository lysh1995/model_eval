---
title: "Optimizing AI Inference at Character.AI / Inside Kaiju: building conversational models at scale"
url: https://blog.character.ai/optimizing-ai-inference-at-character-ai-2/
author: Character.AI
year: 2024
type: engineering-blog
accessed: 2026-07-16
topic: companion-products
---

# Character.AI engineering — serving, memory, and what they optimize for

Two posts: the inference-optimization post (2024) and the Kaiju model post. Both fetched successfully.

## Serving scale and cost

| Metric | Value |
|---|---|
| Inference throughput | "more than 20,000 inference queries per second" (~20% of Google Search's ~105k QPS) |
| Serving cost reduction since late 2022 | **33x** |
| Cost vs. using a commercial API | commercial API would cost "13.5X more than with our systems" |
| **Average dialogue history** | **180 messages per chat** |
| **Prefix cache hit rate** | **95%** |
| KV cache reduction from architecture | "more than 20X without regressing quality" |

**The 180-messages-per-chat figure is the important product number here.** It tells you the real
workload: companion conversations are long, and the memory/context problem is the product, not a
side quest. It also explains why "memory loss" is the #1 user complaint — 180 messages is well past
a 1024-token sliding window.

## Techniques

- **Multi-Query Attention (MQA)** — 8x KV cache reduction vs. the GQA used in most open-source models
- **Hybrid/sliding-window attention** — 1024-token local window, O(length) not O(length²); production
  model uses global attention on **1 of every 6 layers** (Kaiju post says ~"5:1 ratio of sliding to global")
- **Cross-layer KV sharing** — a further 2–3x; "generally, 2-3 layers share a KV cache"
- **Int8 quantization** on weights, activations, *and* KV cache — natively trained in int8 (QAT), not
  post-training quantized. QAT gives "bf16-level model accuracy while training 20–30% faster."
- **Stateful inter-turn caching** — host-memory LRU tree enabling prefix reuse across partial matches

## Kaiju models

Sizes: **Small 13B / Medium 34B / Large 110B**. Trained on H100s. Gradient compression via "Squinch"
(6-bit comms); "Ternary Weight Updates" at 1.6 bits/parameter for smaller models.

## The single most revealing detail: their two data mixes

Character.AI explicitly maintains **two named data mixes**:

- **"MMLU Max"** — optimizes AGI/academic benchmarks
- **"Production Max"** — creates "highly engaging" conversational models

They "explicitly avoid optimizing for standard academic metrics, instead targeting production
performance." They also concede MQA "is known to have a measurable, negative impact on some AGI
benchmarks like MMLU" and shipped it anyway.

**Read that as a thesis statement: the company that runs the largest companion product in the world
states that benchmark quality and companion quality are different axes, and deliberately trades the
former for the latter.** This is direct validation that an eval platform for this domain cannot be
built out of academic benchmarks. It is also an unguarded admission that the production objective is
literally named "engaging."

## The conspicuous gap

The Kaiju post "provides no quantitative engagement metrics, user satisfaction scores, or comparative
evaluation results" and "notably omits human evaluation results or preference testing data for
conversational quality." Safety work is described (SFT, "modified online DPO", classifiers with
"token-level metrics about safety") but conversational quality evaluation is essentially unaddressed
in public. The infra is world-class and publicly documented; the eval methodology is not documented
at all. That gap is the market for this platform.

## Published engagement figures (third-party, treat as soft)

Widely reported but not first-party-confirmed, and estimates vary a lot — cite with care:
- Session duration: reported anywhere from ~12m33s to ~16m to ~18m15s to "25–45 minutes" depending on source
- "two hours per user per day on average" for engaged users (frequently cited, poorly sourced)
- ~20M MAU confirmed early 2025 (upper estimates 28M); ~200M+ monthly visits in Q3 2024
- Reportedly fell from ~28M to ~20M MAU between mid-2025 and early 2026 amid filter tightening
