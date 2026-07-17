---
title: "Llama Guard 3 (1B, 8B) and Llama Guard 4 (12B multimodal)"
url: "https://huggingface.co/meta-llama/Llama-Guard-3-1B , https://huggingface.co/meta-llama/Llama-Guard-3-8B , https://huggingface.co/meta-llama/Llama-Guard-4-12B"
authors: "Meta (Llama Team)"
year: 2025
type: api-doc
accessed: 2026-07-16
topic: roleplay-safety
---

# Llama Guard 3 / Llama Guard 4

## Summary

Meta's open-weight LLM-based safety classifiers, aligned to the **MLCommons hazard taxonomy**. Classifies both **prompts** (user input) and **responses** (model output) as `safe`/`unsafe` plus violated category codes. Self-hostable — which means *we control the cost curve*, unlike hosted APIs.

Three relevant variants:
- **Llama Guard 3-1B** — pruned + distilled from the 8B for **on-device** deployment. The cheapest credible option for 100% traffic.
- **Llama Guard 3-8B** — the accuracy workhorse. 8 languages.
- **Llama Guard 4-12B** — natively multimodal (text + image), pruned from Llama 4 Scout, adds S14.

## Taxonomy / definitions (verbatim)

**MLCommons-aligned hazard taxonomy.** Llama Guard 3 covers **S1–S13**; Llama Guard 4 (and Llama Guard 3-8B's card, which lists S14 for code-interpreter use) covers **S1–S14**:

| Code | Category |
|---|---|
| **S1** | Violent Crimes |
| **S2** | Non-Violent Crimes |
| **S3** | Sex-Related Crimes |
| **S4** | Child Sexual Exploitation |
| **S5** | Defamation |
| **S6** | Specialized Advice |
| **S7** | Privacy |
| **S8** | Intellectual Property |
| **S9** | Indiscriminate Weapons |
| **S10** | Hate |
| **S11** | Suicide & Self-Harm |
| **S12** | Sexual Content |
| **S13** | Elections |
| **S14** | Code Interpreter Abuse (text only; Llama Guard 3-8B and Llama Guard 4) |

Descriptions (verbatim/near-verbatim from the model cards):
- **S1 Violent Crimes** — unlawful violence toward people and animals
- **S2 Non-Violent Crimes** — incl. fraud, theft, drug crimes, hacking, cyber crimes
- **S3 Sex-Related Crimes** — trafficking, sexual assault, harassment, prostitution
- **S4 Child Sexual Exploitation** — content depicting/enabling child sexual abuse
- **S5 Defamation** — "verifiably false" statements likely to injure a living person's reputation
- **S6 Specialized Advice** — dangerous/unqualified financial, medical, legal guidance
- **S7 Privacy** — exposure of sensitive nonpublic personal information
- **S8 Intellectual Property** — violations of third-party IP rights
- **S9 Indiscriminate Weapons** — chemical, biological, radiological, nuclear, high-yield explosives
- **S10 Hate** — dehumanizing content based on protected characteristics
- **S11 Suicide & Self-Harm** — self-injury, suicide, disordered eating
- **S12 Sexual Content** — erotica / lewd content
- **S13 Elections** — factually incorrect information about electoral systems/voting
- **S14 Code Interpreter Abuse** — attempts to abuse a code interpreter (denial of service, privilege escalation)

## Key numbers (verbatim) — accuracy, size, latency

### Llama Guard 3-8B

| Metric | Value |
|---|---|
| Params | 8B (BF16) |
| **English response classification F1 / FPR** | **0.939 / 0.040** |
| Llama Guard 2 baseline | F1 **0.877** / FPR **0.081** |
| GPT-4 baseline | F1 **0.805** / FPR **0.152** |
| Languages | "English, French, German, Hindi, Italian, Portuguese, Spanish, Thai" (8) |
| INT8 quantized | checkpoint size **~40% smaller**, minimal performance impact |
| Serving | vLLM, SGLang supported |

### Llama Guard 3-1B (pruned/distilled for on-device)

| Metric | Value |
|---|---|
| Params | **1B** — pruned to **1,123 million** parameters |
| Pruning | reduced to **12 decoder layers** and **6400 MLP hidden dimension**, via block-importance metrics + layer-wise pruning calibration |
| Output layer | pruned from **262.6M → 40.96k** parameters (dropping unused token connections) |
| Distillation | "Llama Guard 3-8B as a teacher model" via **logit-level distillation** |
| **English F1 / FPR** | **0.899 / 0.090** |
| **INT4-quantized English F1 / FPR** | **0.904 / 0.084** (quantization does *not* hurt — slightly better) |
| French F1/FPR | 0.939 / 0.012 |
| German F1/FPR | 0.845 / 0.036 |
| Hindi F1/FPR | 0.680 / 0.057 |
| XSTest | **0.821 / 0.068** vs GPT-4 **0.805 / 0.152** |

**Latency/throughput: not published by Meta** in tokens/sec or ms terms. Meta describes 3-1B as suitable for on-device/mobile deployment but publishes no ms figures. **Do not assume a number — benchmark it.** See `safety-guard-model-serving-costs.md`.

### Llama Guard 4-12B

| Metric | Value |
|---|---|
| Params | **12B** — "natively multimodal safety classifier with 12 billion parameters" |
| Architecture | "early fusion transformer architecture with dense layers"; pruned from **Llama 4 Scout** pre-trained model; dense FFN (not MoE) |
| Multimodal | "mixed text-and-image prompts"; "supports safety classification when multiple images are given in the prompt as input" |
| English (output filtering) | **69% recall / 11% FPR / 61% F1** |
| Multilingual | **43% R / 3% FPR / 51% F1** |
| Single-image | **41% R / 9% FPR / 38% F1** |
| Multi-image | **61% R / 9% FPR / 52% F1** |

**Note the F1 discrepancy:** Llama Guard 4's reported F1 (61% English) is much *lower* than Llama Guard 3-8B's (0.939). These are **not comparable** — different eval sets and a stricter internal benchmark. Do not present them side-by-side as a regression. Benchmark both on our own data.

### Hosted pricing (list prices — see `safety-guard-model-serving-costs.md`)
- **Together AI: Llama Guard 4 12B — $0.20 per 1M tokens** (list price, together.ai/pricing, accessed 2026-07-16).
- Llama Guard 3-8B: **not listed** on Together's current pricing page. Not offered on Groq's pricing page (Groq lists Prompt Guard at $0.03–$0.04/1M, which is a *different* model — prompt-injection detection, not content moderation).

## Relevance to a roleplay/companion eval product

- **Llama Guard 3-1B at INT4 is the strongest candidate for a self-hosted 100%-traffic tier.** F1 0.904 at INT4 — *better* than the unquantized 1B (0.899) and comfortably above GPT-4's 0.805. A 1B INT4 model is small enough to serve at very high throughput on commodity GPUs, and quantization is free accuracy-wise. This is the "we control our own costs" answer if OpenAI's free endpoint ever becomes unavailable or rate-limits us.
- **Self-hosting is the strategic hedge.** OpenAI Moderation is free *today*. Llama Guard is free *forever* (open weights) at the cost of GPU time. For a platform selling reliability to customers, having a self-hostable path matters — especially for customers who can't send traffic to OpenAI (EU data residency, NSFW content that may violate OpenAI's usage policies). **This last point is significant: many companion products cannot legally or contractually route their spicy traffic through OpenAI at all.** For those customers Llama Guard isn't a hedge, it's the only option.
- **S12 (Sexual Content) is a false-positive machine for us — and that's fixable.** Llama Guard's prompt format lets you **select which categories to enforce**. We simply omit S12 for consensual adult roleplay while keeping **S4 (Child Sexual Exploitation)** and **S3 (Sex-Related Crimes)** as hard blocks. This category-selectivity is a real advantage over OpenAI's fixed taxonomy, and it's the single most important configuration decision for a companion deployment.
- **S11 (Suicide & Self-Harm) is the highest-value category**, same as with OpenAI Mod. Run both; agreement/disagreement between two independent classifiers is itself a useful triage signal for human review.
- **S6 (Specialized Advice) is underrated for companions.** A companion giving confident medical/financial advice to an emotionally dependent user is a real liability. This category has no equivalent in OpenAI's taxonomy — a concrete reason to run Llama Guard *alongside* rather than instead of.
- **Llama Guard 4's multi-image support matters** if the product ships character images / user selfies. But its image F1 (38% single-image) is poor — image moderation is genuinely unsolved. OpenAI's omni-moderation covers images free; prefer that for images and use Llama Guard for text.
- **Nothing in this taxonomy touches sycophancy or manipulation.** S1–S14 is a *content* taxonomy. Confirms the tier-1/tier-2 split: Llama Guard/OpenAI Mod handle content harm cheaply at 100%; our own judges handle relational harm on a sample. We should not try to fine-tune Llama Guard into a sycophancy detector as a first move — the taxonomy and training distribution are wrong for it.
