---
title: "Tailor: A Soft-Prompt-Based Approach to Attribute-Based Controlled Text Generation"
url: https://arxiv.org/abs/2204.13362
authors: Kexin Yang, Dayiheng Liu, Wenqiang Lei, Baosong Yang, Mingfeng Xue, Boxing Chen, Jun Xie (Alibaba DAMO Academy / Sichuan University)
year: 2022 (ACL 2023)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Tailor — multi-attribute PROMPT concatenation degrades fluency AND is position-sensitive

**The closest thing in the CTG literature to our actual situation: attributes specified as prompts, combined by concatenation. Two documented failure modes — fluency decrease and position sensitivity. The second one is the scarier one for character sheets.**

## The setup

Tailor represents each attribute as a **pre-trained continuous prefix** (a soft prompt). Multi-attribute generation is attempted by **simply concatenating** the single-attribute prompts, with no re-training.

> these prompts "can be simply concatenated as a whole to multi-attribute CTG without any re-training, yet **raises problems of fluency decrease and position sensitivity**"

## Failure mode 1 — fluency decrease (verbatim)

> "this straightforward method **suffers from notably decreasing fluency of final text** compared with single-attribute CTG."

## Failure mode 2 — position sensitivity (verbatim) — THIS IS THE IMPORTANT ONE

> "the PLM tends to **focus more on the single-attribute prompt that is closer to the input prefix**."

Quantified: swapping attribute order between the NE-AM and AM-NE combinations shifts performance on the Negative Emotion attribute by **3.14%**.

**Attribute ORDER in the prompt changes attribute EXPRESSION in the output.** The same two attributes, the same model, the same everything — reorder them and the trait strength moves 3.14 points.

## Main results — six attribute combinations (2 sentiments × 3 food types), their Table 2

| Method | Correctness (%) | Grammar | Perplexity | Distinctness |
|---|---|---|---|---|
| CONCAT (naive) | 76.20 | 0.63 | 55.02 | 0.05/0.33/0.68 |
| Tailor-C | 78.82 | 0.63 | 52.76 | 0.05/0.32/0.68 |
| Tailor-W | 83.98 | 0.68 | 51.41 | 0.05/0.33/0.69 |
| Tailor-A | **87.15** | **0.69** | 52.73 | 0.05/0.33/0.69 |

## Single-attribute vs multi-attribute degradation

Tailor-S (single-attribute) achieves **~90%** correctness; the best multi-attribute approach reaches **87.15%** — a **~3-point decline** from handling multiple constraints simultaneously, and that is *after* their fixes (multi-attribute prompt mask, re-indexed position sequence, trainable prompt connector). **Naive concatenation sits at 76.20% — a ~14-point drop from single-attribute.**

Efficiency note: Tailor requires only **0.08% extra training parameters** of GPT-2, across eleven attribute-specific generation tasks.

## Relevance to companion-eval-platform

1. **Position sensitivity is the finding that should change how we write character sheets.** 3.14% attribute shift from reordering alone. Our character sheets are ordered lists of traits — and if the model over-weights whatever is nearest the input, then **trait order is an uncontrolled variable in every eval we run**. Any dose-response curve measured without randomizing or fixing trait position has this confound baked in. **Concretely: our elasticity measurement must randomize trait order across samples, or the elasticity of "shy" will depend on whether shy is listed first or fifth.** This is the most actionable item in this file and it is cheap to implement.

2. **Naive concatenation costs ~14 points (90% → 76.20%).** This is prompt-space, not logit-space — the closest analogue to stacking traits in a character sheet. It corroborates the Distributional Lens −18.7pt figure (`steer-multiaspect-distributional-lens.md`) from a different method family. Two prompt/prefix-based results agreeing that combining attributes costs 14–19 points is a reasonably robust signal that the entanglement claim is *true* — and simultaneously that it is *already known*, which is the point of this research.

3. **The ~3pt residual after their fixes is the optimistic bound.** Even with engineered mitigations, multi-attribute control does not fully recover single-attribute performance. There is an irreducible interference floor. For our product this means: a multi-trait character will always express each trait somewhat less than a single-trait character would. Worth quantifying for our own models, but not worth claiming as a discovery.

4. **Grammar 0.63 → 0.69 tracks correctness 76.20 → 87.15.** Note these move *together* here, which cuts against the simple "control costs fluency" story — better attribute fusion improved *both*. The tradeoff is not inescapable; it is a property of *bad* fusion. That is a genuinely important nuance for our writeup: **the knee is not a law of nature, it is a symptom of a crude control mechanism.** Prompt-side adverb dosing is a crude control mechanism.

5. **Honest limitations.** (a) GPT-2 + soft prefixes, 2022 — soft prompts are continuous vectors, not natural-language adverbs, so the position-sensitivity mechanism (attention distance to the input prefix) may or may not transfer to modern long-context chat models with strong system-prompt handling. Modern models are explicitly trained to attend to system prompts holistically, which could eliminate the effect — or not, and nobody has checked for trait words. **That check is cheap and would be a real contribution.** (b) The attribute set (sentiment × food type) is trivially separable compared to companion traits like "shy" and "guarded", which are semantically overlapping — real trait pairs should interfere *more*, not less. (c) 3.14% is a single number from one attribute pair; I would not treat it as an effect-size estimate, only as an existence proof.

6. **Related:** `steer-multiaspect-distributional-lens.md` (the same interference from the decoder side, bigger numbers), `steer-personality-shaping-levels.md` (cross-trait spillover), `game-followbench.md` (constraint count vs adherence; CSL ≈ 3.3 rule budget), `game-sysbench.md`, `multiturn-lost-in-middle.md` (position effects in long contexts — directly relevant to trait position in long character sheets).
