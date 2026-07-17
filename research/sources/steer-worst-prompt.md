---
title: "On the Worst Prompt Performance of Large Language Models"
url: https://arxiv.org/abs/2406.10248
authors: Bowen Cao, Deng Cai, Zhisong Zhang, Yuexian Zou, Wai Lam (CUHK / Tencent AI Lab / Peking University)
year: 2024 (NeurIPS 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Worst-case prompt performance — brittleness measured on OPEN-ENDED generation, not multiple choice

**This is the most important paper in the set after FormatSpread, for one reason: it is the only one that
measures paraphrase brittleness on FREE-FORM, OPEN-ENDED responses judged for quality, rather than accuracy
on items with a ground-truth label. That is much closer to what a companion/persona platform actually does.
And the gaps are ENORMOUS — 34 to 54 points.**

## Abstract (opening, verbatim)

> "The performance of large language models (LLMs) is acutely sensitive to the phrasing of prompts, which
> raises significant concerns about their reliability in real-world scenarios."

The paper introduces **RobustAlpacaEval** to assess worst-case prompt performance across diverse queries,
arguing for the **worst prompt performance as the lower bound / reliability floor** rather than the average.

## Method — RobustAlpacaEval

- **Source:** built on **TinyAlpacaEval**, a condensed subset of the AlpacaEval benchmark. **Case-level**
  (per-query) paraphrases — this is the key design: paraphrases of *individual queries*, not of a task-level
  instruction template.
- **Paraphrases:** "**ten paraphrases for each query** within TinyAlpacaEval."
- **Validation (semantic equivalence is human-checked, not assumed):** paraphrasing was "first accomplished
  automatically through GPT4. Subsequently, **each paraphrase is manually reviewed and revised to ensure
  semantic integrity and human-like fluency**."
- **Diversity check:** average length-normalized edit distance between paraphrase pairs = **0.7234** at word
  level. (i.e. the paraphrases are genuinely lexically distant, not trivial rewrites.)
- Scoring is **open-ended response quality** (AlpacaEval-style judged win-rate), not classification accuracy.

## THE NUMBERS — best vs worst prompt gap

| Model | Worst | Best | **Gap** |
|---|---|---|---|
| Gemma-1.1-7B-it | 8.73% | 62.38% | **53.65** |
| Llama-2-13B-chat | 4.83% | 52.05% | **47.22** |
| **Llama-2-70B-chat** | **9.38%** | **54.86%** | **45.48** |
| Mistral-7B-instruct | 4.22% | 45.26% | **41.04** |
| Llama-2-7B-chat | 5.42% | 43.54% | **38.12** |
| ChatGPT (gpt-3.5-turbo) | 5.44% | 39.88% | **34.44** |
| Gemma-1.1-2B-it | 4.42% | 36.60% | **32.18** |

**The headline (verbatim framing):** a **45.48**-point difference between worst and best performance for
**Llama-2-70B-chat**, with worst performance "dipping as low as **9.38%**."

**Critical observations:**
- **Every single model has a gap above 32 points.** There is no robust model in this table.
- **Scale does not help.** Llama-2-7B → 13B → 70B gaps are 38.12 → 47.22 → 45.48. The 70B model is *worse*
  than the 7B model. The largest model has the *second-worst* gap in its family.
- **Instruction tuning does not help** — every model here is already an instruct/chat model.
- These are **semantically-equivalent, human-verified paraphrases**. The user asked the same question.

## Do worst prompts transfer across models? NO.

- "the overlap rate of the **worst-k prompts** for Llama family models is only **2%** (**13%** for Gemma)"
  when k=1.
- **Kendall's W** concordance across all models: **0.238** — weak agreement.
- Intersection-over-Union for sensitive cases **dropped below 0.2** across models.
- Verbatim conclusion: "It is unlikely to characterize the worst prompts using **model-independent
  features**."
- "Different models are more sensitive in different cases, which further underscores the complexity involved
  in tackling the issue of worst prompt performance."

**2% overlap within the same model family.** This is an even harsher non-transfer result than FormatSpread's
57.46%. You cannot precompute a "bad prompt" blocklist; badness is (model × query)-specific.

## Can prompt engineering fix worst-case performance? Mostly NO.

| Method | Effect |
|---|---|
| **Self-refinement** | **Degraded** performance — Llama-2-70B average dropped **13.53%** |
| **Voting** | Improved worst performance by **+21.98** pts for Llama-2-70B, **but reduced best performance by −23.50** pts; cost increased severalfold |
| **Swarm Distillation** | Enhanced consistency but **decreased overall performance** via "over-fitting to self-generated outputs" |

**Voting is the honest result: it does not fix brittleness, it trades the ceiling for the floor.** You buy
+21.98 on the worst case by paying −23.50 on the best case. This is variance reduction, not capability gain —
the model is not becoming more robust, you are just averaging over its noise.

Also relevant: the paper reports the difficulty of identifying the worst prompt from **both model-agnostic
and model-dependent** perspectives, emphasizing "the absence of a shortcut to characterize the worst prompt."

## Relevance to companion-eval-platform

**This is the closest analogue to the platform's measurement setting in the entire literature, and it is the
paper I would put in front of anyone defending the BRITTLE mode.**

1. **It removes the "but that's just multiple-choice" escape hatch.** The standard rebuttal to FormatSpread
   and the MCQ-order papers is that log-prob ranking over A/B/C/D is a brittle readout, not a brittle model —
   a real chat model generating real text would be fine. **This paper tests exactly that and finds 32–54
   point gaps on open-ended, judge-scored generation.** Free-form generation is *not* more robust. If the
   platform's traits are measured by judging free-text companion responses, this is the applicable prior, and
   it says the noise floor is enormous.

2. **The scale result is cleaner here than anywhere else.** Llama-2 7B/13B/70B → 38.12/47.22/45.48. The
   biggest model is not the most robust. Combined with Sclar's abstract and Mizrahi's Flan-T5-large-vs-XL
   result, **the "scale fixes brittleness" hypothesis is dead across three independent papers.** (The one
   dissent, ProSA, is discussed in `steer-prosa-sensitivity.md` — and its own within-family Qwen data agrees
   with this paper.)

3. **The 2% worst-prompt overlap is the strongest non-transfer number in the literature.** Ported to the
   platform: **the persona phrasing that fails for model A will not be the one that fails for model B** — and
   not even for the next size of the same family. Any curated set of "known-bad trait phrasings" is a
   per-model artifact with a ~2–13% hit rate elsewhere. Prompt tuning does not port; steerability scores do
   not port.

4. **Worst-case, not average-case, is the right frame for a companion product — and the platform should
   adopt it.** This paper's central methodological argument is that the average over paraphrases hides an
   unacceptable floor. A companion product is judged on its worst turns, not its mean turn: one cruel reply
   from a "shy, kind" persona is the whole story, regardless of the mean. **The platform should report
   min-over-paraphrases for safety-relevant traits, following this paper, rather than a mean with error
   bars.** Mizrahi's CPS (`steer-multiprompt-eval.md`) discounts the max by the spread; this paper argues you
   should just report the min. For safety traits, the min is the product-relevant quantity.

5. **Voting's −23.50/+21.98 tradeoff is a direct warning about mitigation.** If the platform is tempted to
   recommend "sample k paraphrases and aggregate" as the fix for BRITTLE, this paper shows what that actually
   buys: a compressed distribution, not a better model, at several-fold cost. Worth quoting to anyone who
   proposes ensembling as a steerability fix. Self-refinement actively *hurts* (−13.53%).

**Honest limits:** the perturbation is still semantically-null-by-construction (human-verified paraphrases of
the *same question*), so this measures the **noise floor**, not intended sensitivity. It says nothing about
whether "very shy" moves shyness more than "shy" does. It bounds how much of an observed intensity-word
effect could be explained by phrasing noise alone — and the answer, 32–54 points, is large enough to swallow
most plausible intended effects. **That is the number that should scare the design.** See
`steer-spurious-vs-intended.md`.
