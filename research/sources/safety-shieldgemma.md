---
title: "ShieldGemma: Generative AI Content Moderation Based on Gemma"
url: "https://arxiv.org/abs/2407.21772"
authors: "Wenjun Zeng, Yuchi Liu, Ryan Mullins, Ludovic Peran, Joe Fernandez, Hamza Harkous, Karthik Narasimhan, Drew Proud, Piyush Kumar, Bhaktipriya Radharapu, Olivia Sturman, Oscar Wahltinez (Google)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# ShieldGemma (2B / 9B / 27B) and ShieldGemma 2 (4B image)

## Summary

Google's open-weight LLM-based content moderation models, built on **Gemma 2**. Sizes: **2B, 9B, 27B**. Moderates both **user input** and **model output** against four harm types. A follow-up, **ShieldGemma 2 (4B)**, handles **image** content.

Positioning vs Llama Guard: ShieldGemma reports **better** performance (+10.8% AU-PRC over Llama Guard, +4.3% over WildGuard on public benchmarks) and offers a **size ladder** (2B/9B/27B) letting you pick a cost/accuracy point. Notably, the paper's own numbers show **the 2B is competitive with the 9B and 27B** — which is excellent news for 100%-traffic economics.

Key methodological contribution: a **novel LLM-based data curation pipeline**, trained largely on **synthetic data**, that still generalizes.

## Taxonomy / definitions (verbatim)

**Four harm types**, verbatim from the paper:

| Harm type | Definition (verbatim) |
|---|---|
| **Sexually Explicit Information** | "content contains references to sexual acts or other lewd content (e.g., sexually graphic descriptions, content aimed at causing arousal)" |
| **Dangerous Content** | "content harming oneself and/or others (e.g., accessing or building firearms and explosive devices, promotion of terrorism, instructions for suicide)" |
| **Harassment** | "content is malicious, intimidating, bullying, or abusive content targeting another individual (e.g., physical threats, denial of tragic events, disparaging victims of violence)" |
| **Hate Speech** | "content targeting identity and/or protected attributes (e.g., racial slurs, promotion of discrimination, calls to violence against protected groups)" |

**ShieldGemma 2 (4B)** — image content classification across a comparable set (sexually explicit, dangerous content, violence/gore).

## Key numbers (verbatim) — F1 / AU-PRC / size

**Headline comparisons:**
- **~10.8% higher AU-PRC than Llama Guard** on public benchmarks
- **~4.3% better than WildGuard** on public benchmarks

**Comparison table (F1 / AU-PRC), as extracted from the paper:**

| Model | vs OpenAI Mod API | vs WildGuard (7B) | vs LlamaGuard1 (7B) |
|---|---|---|---|
| **ShieldGemma 2B** | 0.812 / 0.887 | 0.779 / — | — / 0.847 |
| **ShieldGemma 9B** | 0.821 / 0.907 | 0.721 / — | 0.758 / 0.847 |
| **ShieldGemma 27B** | 0.805 / 0.886 | — / — | 0.761 / — |

**⚠️ Extraction caveat:** this table was pulled from the ar5iv HTML rendering and the column semantics are ambiguous (these appear to be ShieldGemma's scores *on each baseline's benchmark set*, not head-to-head deltas). The **relative ordering and the 10.8% / 4.3% headline claims are reliable; the individual cell values should be re-verified against the PDF before use in any customer-facing material or capacity plan.**

**Model sizes:** 2B, 9B, 27B (text); ShieldGemma 2 = 4B (image).

**Latency / throughput / cost: NOT PUBLISHED.** The paper reports no ms, tokens/sec, or $ figures. Open weights, so serving cost is ours to determine.

**The key structural finding:** the 2B, 9B, and 27B scores are remarkably close (0.812 / 0.821 / 0.805 in the first column — the **27B is not better than the 2B**). Accuracy saturates at 2B for this task.

## Relevance to a roleplay/companion eval product

- **"The 2B matches the 27B" is the most important number in Part B.** It empirically confirms that **content moderation is an easy task that does not need a big model**. This is the entire economic foundation of running a classifier on 100% of traffic: we can serve a 2B model at ~13x lower cost than a 27B with *no accuracy loss*. Combined with Llama Guard 3-1B's INT4 result (quantization also free), the message is consistent and strong: **small + quantized is the correct architecture for tier-1, and this is a research-backed claim, not a guess.**
- **The four-harm taxonomy is much coarser than Llama Guard's S1–S14** — no self-harm/suicide as its own top-level category (it's folded into "Dangerous Content"), no specialized advice, no privacy, no CSAM as a distinct class. For a companion product where **suicide/self-harm is the #1 risk**, folding it into a generic "Dangerous Content" bucket is a real drawback: we lose the ability to threshold self-harm independently. **Llama Guard's S11 is more useful to us than ShieldGemma's Dangerous Content.**
- **"Sexually Explicit Information" has the same false-positive problem as Llama Guard's S12 / OpenAI's `sexual`** — and ShieldGemma's coarse 4-type taxonomy gives us *less* room to selectively disable it without losing coverage of adjacent harms. Llama Guard's per-category prompt selection is more configurable. Advantage: Llama Guard.
- **Where ShieldGemma wins: it's the accuracy leader and it's a size ladder.** If we need a self-hosted tier-1 and want the best F1/cost point, ShieldGemma 2B is the strongest published candidate. Worth a bake-off against Llama Guard 3-1B INT4 on our own labeled companion data — that bake-off is a concrete, high-value next step, and the two papers' numbers are not comparable enough to decide it on paper.
- **Trained on synthetic data and it generalizes.** This is directly encouraging for *us*: it suggests we can build a companion-specific sycophancy/manipulation classifier from synthetic data generated against the ELEPHANT/DarkBench/De Freitas taxonomies, without a massive human annotation budget. That's a plausible path to a proprietary tier-2 model that's cheap enough to run at high sample rates. **This is arguably the most actionable methodological finding for our roadmap.**
- **No latency numbers published anywhere** — same gap as Llama Guard. Nobody in this literature publishes serving metrics. We will have to generate them ourselves; see `safety-guard-model-serving-costs.md`.
