---
title: "Steering Llama 2 via Contrastive Activation Addition"
url: https://arxiv.org/abs/2312.06681
authors: Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, Alexander Matt Turner (Anthropic / MATS)
year: 2023 (ACL 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# CAA — "precise control over the DEGREE of the targeted behavior" via a signed multiplier

**CAA's abstract literally claims graded degree-control of a behavioral trait via a scalar coefficient. Relevant here mostly as (a) further evidence that degree-control is standard, and (b) an honest counterweight: CAA did NOT find the degradation the brittleness story wants.**

## Abstract (verbatim)

> "We introduce Contrastive Activation Addition (CAA), an innovative method for steering language models by modifying their activations during forward passes. CAA computes 'steering vectors' by averaging the difference in residual stream activations between pairs of positive and negative examples of a particular behavior, such as factual versus hallucinatory responses. During inference, these steering vectors are added at all token positions after the user's prompt with either a positive or negative coefficient, **allowing precise control over the degree of the targeted behavior**."

**"Precise control over the degree of the targeted behavior"** — that is the design under test's goal statement, from a 2023 abstract, on behavioral traits (sycophancy, refusal, hallucination) that are close cousins of companion character traits.

## The multiplier

The steering vector is added to the residual stream with a scalar coefficient. The paper sweeps multipliers of **−1 and +1** across all layers to locate the best steering layer; open-ended generation experiments use **±2**. Signed dosing means **negative doses are available** — you can steer *away* from a trait, not just toward it.

## Dose-response numbers (Figure 4, layer 13, multiple-choice)

| Behavior (Llama 2 7B) | mult = −1 | mult = 0 | mult = +1 |
|---|---|---|---|
| Refusal | ~0.56 | ~0.78 | ~0.86 |
| Hallucination | ~0.42 | ~0.54 | ~0.78 |

Monotone in the multiplier, with an asymmetry worth noting: for refusal, the negative dose moves the behavior **more** (−0.22 from baseline) than the positive dose (+0.08). **Dose-response is not symmetric around zero** — suppressing a trait and amplifying it are not mirror operations. If that holds prompt-side, "not at all shy" and "extremely shy" will not have equal and opposite effects, and a curve fitted symmetrically will be wrong.

## MMLU vs multiplier (Table 5, Llama 2 13B Chat, layer 14)

| Multiplier | MMLU |
|---|---|
| 0 | 0.63 |
| +1 | 0.59–0.65 |
| −1 | 0.57–0.64 |

**No systematic capability degradation at |mult| ≤ 1.** No perplexity measurements reported.

## What CAA does NOT show — and I checked specifically

**The paper does not report output degradation at large multipliers.** There is no explicit discussion of coherence loss, and no sweep past ±2. This is a genuine limitation of CAA as brittleness evidence, and I want to flag it rather than paper over it: the "residual-stream steering degrades quality at high strength" claim comes from *later* work critiquing or extending CAA (see `steer-steering-brittleness.md`), **not from CAA itself**. CAA's own multiplier range (±1, ±2) sits comfortably inside the regime that later work found safe (|λ| ≤ 1.5 monotone, degradation onset 1.5–2). **CAA never turned the dial far enough to break anything.**

That is itself a useful observation: the brittleness knee is invisible if you only sweep the range you already expect to work.

## Relevance to companion-eval-platform

1. **Corroborates that degree-control is standard vocabulary, on behavioral traits specifically.** CTG papers control *sentiment/topic/toxicity*; CAA controls *sycophancy/refusal/hallucination* — dispositional traits much closer to "shy" or "protective". "Precise control over the degree of the targeted behavior" is the claim, in 2023, from a paper with an Anthropic byline. This is directly on-point prior art for trait-degree control and hard to argue around.

2. **The asymmetry (−1 moves refusal by −0.22, +1 by +0.08) is a design warning.** If our ladder is meant to include de-emphasis ("not at all shy") as well as amplification, we cannot assume a single slope covers both directions. Report the two halves separately or the fit is meaningless. This also suggests baseline placement matters enormously: if Llama-2-chat is already at 0.78 refusal, there is a **ceiling** limiting how much the positive dose can show. **Traits the model already exhibits by default will look inelastic purely from ceiling effects, not from genuine unresponsiveness** — and companion models are RLHF'd to be agreeable, warm, and helpful by default, meaning exactly the traits our characters most often specify are the ones most likely to be ceilinged. This is a serious confound for any cross-trait elasticity comparison and I have not seen it addressed anywhere in this literature.

3. **The flat MMLU is a genuine counterweight to the brittleness narrative and I should say so plainly.** Within |mult| ≤ 1, CAA steers behavior meaningfully with **no measurable capability cost** (MMLU 0.63 → 0.59–0.65, within noise). The honest reading across sources is not "dosing always degrades" — it is **"dosing is free in the low range and destructive past a knee"**, which is exactly the DExperts/CFG/brittleness picture. Our writeup should not overstate brittleness; the interesting question is *where the knee is*, not *whether degradation exists*. If we cherry-pick only the degradation results we will be making the same mistake in the other direction that the novelty claim makes.

4. **Method-transfer caveat, same as CFG/DExperts.** Activation-space multiplier ≠ prompt-space adverb. CAA also requires white-box access to the residual stream, which our platform may not have for hosted models. The relevance is conceptual (degree-control is prior art; asymmetry and ceilings are real hazards) rather than a source of numbers we can port.

5. **Honest limitation on this source.** Llama 2 (7B/13B), 2023. The Figure 4 values above are **read off a plot and are approximate** (the paper's own presentation is a figure, not a table) — I have marked them with "~" and they should not be quoted as precise. Table 5's MMLU ranges are reported as ranges in the paper across system-prompt conditions. Also note CAA's behaviors are measured largely on **multiple-choice** probes, which `steer-steering-brittleness.md` argues systematically overstates steering success relative to open-ended generation — so even CAA's clean monotone curves are probably optimistic.

6. **Related:** `steer-steering-brittleness.md` (what happens when you sweep past CAA's range), `steer-personality-shaping-levels.md` (the prompt-side equivalent, with ceiling effects visible), `steer-cfg-guidance-scale.md`, `safety-sycophancy-anthropic.md`, `safety-persona-modulation.md`.
