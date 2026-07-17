---
title: "ProSA: Assessing and Understanding the Prompt Sensitivity of LLMs"
url: https://arxiv.org/abs/2410.12405
authors: Jingming Zhuo, Songyang Zhang, Xinyu Fang, Haodong Duan, Dahua Lin, Kai Chen (Shanghai AI Laboratory / OpenCompass)
year: 2024 (Findings of EMNLP 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# ProSA / PromptSensiScore — the DISSENT on scale, and the source of the "prompt sensitivity index"

**Read this one adversarially. Its abstract makes the two claims that would most undermine the "brittleness is
permanent" story — that larger models are more robust and that few-shot fixes sensitivity. Both claims are
weaker than the abstract implies, and the paper's OWN within-family data contradicts the first one. This file
documents the tension honestly rather than resolving it in the convenient direction.**

This is also the source the user was reaching for with "prompt sensitivity index / PromptSensiScore."

## Abstract (verbatim, complete)

> "Large language models (LLMs) have demonstrated impressive capabilities across various tasks, but their
> performance is highly sensitive to the prompts utilized. This variability poses challenges for accurate
> assessment and user satisfaction. Current research frequently overlooks instance-level prompt variations
> and their implications on subjective evaluations. To address these shortcomings, we introduce ProSA, a
> framework designed to evaluate and comprehend prompt sensitivity in LLMs. ProSA incorporates a novel
> sensitivity metric, PromptSensiScore, and leverages decoding confidence to elucidate underlying mechanisms.
> Our extensive study, spanning multiple tasks, uncovers that prompt sensitivity fluctuates across datasets
> and models, with larger models exhibiting enhanced robustness. We observe that few-shot examples can
> alleviate this sensitivity issue, and subjective evaluations are also susceptible to prompt sensitivities,
> particularly in complex, reasoning-oriented tasks. Furthermore, our findings indicate that higher model
> confidence correlates with increased prompt robustness. We believe this work will serve as a helpful tool
> in studying prompt sensitivity of LLMs."

Project: https://github.com/open-compass/ProSA

## PromptSensiScore (PSS) — the metric

**Definition (verbatim):** "the average discrepancy in the LLM's responses when confronted with different
semantic variants of the same instruction"

**Formula:**
```
S    = Σ_{p_i,p_j ∈ P} |Y(P_i) − Y(P_j)| / C(|P|, 2)
PSS  = (1/N) Σ_{i=1..N} S_i
```
where `Y(p)` = performance under prompt p, and `C(|P|,2)` = number of prompt pairs.

**PSS is a mean pairwise absolute difference, not a range.** This is a meaningful contrast with Sclar's
*spread* (max − min): PSS is robust to outlier prompts and will report much smaller numbers on the same data.
**Do not compare a PSS value to a FormatSpread spread value — they are different statistics.** PSS ≈ mean
|Δ| over pairs; spread = max − min. Spread grows with sample size; PSS does not. This partly explains why
this paper sounds less alarming than the others.

**Instance-level, not just task-level** — this is the paper's genuine novelty. Prior work (Sclar, Mizrahi)
varies the *task template*; ProSA varies prompts per *instance*.

## Method

**Prompt variants:** **12 prompt variants** per instance, built from "four constructive aspects, including
**Simple Inputs, Role Player, Emotional Support, and Output Requirement**. For each aspect, we have 3 manually
constructed prompts."

**NOTE — this is important for us: "Role Player" and "Emotional Support" are among the four aspects.** These
are *persona-flavored* prompt manipulations, making this the only paper in the set whose perturbation space
overlaps the companion domain at all.

**Semantic equivalence validation:** for subjective evaluation "we used LLMs to rewrite all the prompts";
verification gives **BERTScore 0.93–0.95** and **Human-labeled Similarity 0.88–0.92**.

**Models:** Llama3 series, Qwen1.5 series, InternLM2 series, Mistral-7B-Instruct (objective); five advanced
models plus Claude-3.5-sonnet and GPT-4o (subjective).

**Datasets:** CommonsenseQA, ARC-Challenge, MATH, HumanEval (objective); **LC AlpacaEval 2.0, Arena Hard
Auto** (subjective).

## THE NUMBERS

### Subjective evaluation (the setting closest to a companion product)

| Benchmark | Model PSS range | Reference PSS |
|---|---|---|
| LC AlpacaEval 2.0 | **0.013–0.036** | 0.167 |
| Arena Hard Auto | **0.249–0.266** | 0.275 |

> "all LLMs have significantly lower PSS on LC AlpacaEval 2.0 compared to the Reference, demonstrating a
> certain degree of prompt robustness on this benchmark. However, on **Arena Hard Auto**, LLMs have
> demonstrated **higher sensitivity**"

**The 20× gap between the two subjective benchmarks (0.013–0.036 vs 0.249–0.266) is the most useful number in
this paper.** Same models, same metric, same kind of judged open-ended task — and sensitivity differs by an
order of magnitude depending on the *benchmark*. Sensitivity is a property of the **(model × task ×
prompt-space)** triple, not of the model. **You cannot quote a single "prompt sensitivity" number for a model
and have it mean anything.**

### The scale claim — WEAKER THAN THE ABSTRACT SAYS

The abstract says "larger models exhibiting enhanced robustness." What the body actually supports:

> "**Llama3-70B-Instruct** demonstrates exceptional robustness to prompts." (Figure 4: lowest PSS across
> datasets.)

But — and this is the part that matters —

> "The three models in the same series, **Qwen1.5-7B-Chat, Qwen1.5-20B-Chat, and Qwen1.5-72B-Chat, maintain
> relatively similar prompt sensitivities**"

**The paper's own controlled within-family scaling comparison — 7B → 20B → 72B, same series, same training —
shows NO reduction in sensitivity.** The "larger is more robust" claim rests on Llama3-70B-Instruct being good
in a *cross-family* comparison, which confounds scale with training recipe, data, and recency.

Similarly, the "larger models are more robust" phrasing in context attaches specifically to few-shot gains:
> "with larger models exhibiting greater robustness improvements" — applies to **few-shot learning benefits**,
> not a universal size advantage.

### The few-shot claim — this one is real and DOES contradict Sclar

> "the introduction of few-shot learning **enhances the robustness of the model's prompts for all models**"
> "This reduction in sensitivity is **most pronounced when transitioning from the 0-shot setting to the 1-shot
> setting**"
> "with the increase in few-shot examples, larger LLMs exhibit more robust behavior to prompts"

**This is a genuine, unresolved conflict with Sclar et al.**, whose abstract states sensitivity "remains even
when increasing... the number of few-shot examples" (they compare 1-shot vs 5-shot). Note the two studies may
not actually disagree: ProSA's effect is "most pronounced when transitioning from **0-shot to 1-shot**" — a
comparison Sclar never makes, since Sclar's *minimum* is 1-shot. **The reconciliation is likely: 0→1 shot
helps a lot; 1→5 shots does not.** Both can be true. I flag this as a plausible reconciliation, not an
established one — neither paper tests the other's exact contrast.

## Relevance to companion-eval-platform

1. **This is the strongest available counter-evidence to "BRITTLE is universal", and it does not survive
   scrutiny as such.** Anyone challenging the brittleness story will cite this abstract. The rebuttal is in the
   paper's own text: the controlled within-family comparison (Qwen1.5 7B/20B/72B) shows **no scale benefit**,
   matching Sclar (LLaMA-2 7B/13B/70B), Cao et al. (Llama-2 7B/13B/70B gaps of 38/47/45), and Mizrahi
   (Flan-T5-large vs XL, opposite signs). **Four papers with within-family controls all find scale does not
   fix sensitivity; the one paper claiming otherwise does so from a cross-family comparison.** That is the
   honest state of the evidence, and it favors the user's prior — but for a more specific reason than "Sclar
   said so."

2. **PSS vs spread is a real methodological choice the platform must make, and it changes the answer.**
   Spread (max−min) is alarmist and sample-size-dependent; PSS (mean pairwise |Δ|) is conservative and stable.
   The literature's scariest numbers (76, 45.48, 75) are all *ranges*; the calmest (PSS 0.013–0.036) is a
   *mean*. **The platform should report both**, and should never compare its own metric to a published number
   computed differently. If the platform reports a range, it is on the 76-point scale; if a mean, the
   0.03 scale. Same underlying reality.

3. **The 20× cross-benchmark PSS gap is a direct warning about generalizing from one eval suite.**
   0.013–0.036 on LC AlpacaEval vs 0.249–0.266 on Arena Hard. **A steerability platform measuring on one
   scenario suite will produce a number that does not transfer to another suite** — even for the same model
   and the same trait. Scenario sampling is not optional.

4. **"Role Player" and "Emotional Support" as perturbation aspects make this the nearest domain neighbor.**
   ProSA is the only paper here that perturbs persona-flavored framings. Its PSS machinery — instance-level
   variants, BERTScore+human validation of semantic equivalence (0.93–0.95 / 0.88–0.92) — is a **directly
   reusable protocol** for validating that the platform's trait paraphrases really are equivalent. Steal the
   validation design.

5. **"Higher model confidence correlates with increased prompt robustness"** converges with Pezeshkpour &
   Hruschka's finding that order-sensitivity concentrates where the model is uncertain
   (`steer-mcq-order-bias.md`). **Two independent papers: brittleness lives in the model's low-confidence
   region.** Ported to traits, this predicts BRITTLE will track *trait-prior-strength*, and that decoding
   confidence is an available, cheap **predictor** of which traits will read BRITTLE. That is a testable
   hypothesis and a potential confound to control for — arguably the most actionable idea in this file.

6. **Honest limit:** PSS still measures accuracy/quality under *meaning-preserving* variants (BERTScore
   0.93–0.95 confirms they are equivalent by design). It is a noise-floor metric. It does not measure intended
   sensitivity, and the paper never contemplates a perturbation that *should* change the output.
