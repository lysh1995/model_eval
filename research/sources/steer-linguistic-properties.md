---
title: "The language of prompting: What linguistic properties make a prompt successful?"
url: https://arxiv.org/abs/2311.01967
authors: Alina Leidinger, Robert van Rooij, Ekaterina Shutova (Institute for Logic, Language and Computation, University of Amsterdam)
year: 2023 (Findings of EMNLP 2023, pp. 9210–9232)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Leidinger et al. — brittleness to GRAMMATICAL and LEXICAL variation (mood, tense, aspect, modality, synonyms)

**The perturbation family here is the closest of any published work to the platform's manipulation: single
content words and single function words swapped inside an otherwise identical prompt. Modal verbs ("must" vs
"would") and synonyms ("review" vs "appraisal"). If the platform swaps "shy" for "very shy", the nearest
published analogue is swapping "must" for "would" — and that moves accuracy by up to 17 points.**

## Abstract (verbatim, complete)

> "The latest generation of LLMs can be prompted to achieve impressive zero-shot or few-shot performance in
> many NLP tasks. However, since performance is highly sensitive to the choice of prompts, considerable
> effort has been devoted to crowd-sourcing prompts or designing methods for prompt optimisation. Yet, we
> still lack a systematic understanding of how linguistic properties of prompts correlate with task
> performance. In this work, we investigate how LLMs of different sizes, pre-trained and instruction-tuned,
> perform on prompts that are semantically equivalent, but vary in linguistic structure. We investigate both
> grammatical properties such as mood, tense, aspect and modality, as well as lexico-semantic variation
> through the use of synonyms. Our findings contradict the common assumption that LLMs achieve optimal
> performance on lower perplexity prompts that reflect language use in pretraining or instruction-tuning
> data. Prompts transfer poorly between datasets or models, and performance cannot generally be explained by
> perplexity, word frequency, ambiguity or prompt length. Based on our results, we put forward a proposal for
> a more robust and comprehensive evaluation standard for prompting research."

## Method

**Models:** LLaMA 30b, OPT 1.3b, OPT 30b, OPT-IML 1.3b, OPT-IML 30b
(deliberately paired: base vs instruction-tuned — OPT vs OPT-IML — at matched 1.3b and 30b sizes. This is a
clean 2×2 of scale × instruction-tuning.)

**Tasks/datasets:**
- Sentiment: SST-2, IMDB
- NLI: RTE, CommitmentBank (CB)
- QA: BoolQ, ARC-E

**Prompt variation axes (all semantically equivalent):**
| Axis | Values |
|---|---|
| **Mood** | interrogative, indicative, imperative |
| **Tense** | past, present, future |
| **Aspect** | active, passive voice |
| **Modality** | "can, could, may, might, must, should, would" |
| **Synonymy** | content word replacement, e.g. "review" → "appraisal," "commentary," "critique," "evaluation" |

## THE NUMBERS

### Modality — a single modal verb swap

| Model / task | Swap | Effect |
|---|---|---|
| **OPT 30b** on SST | "must" → "would" | **17-point drop** |
| **LLaMA 30b** on SST | "must" (75.52%) vs "would" (85.97%) | **10.45 points** |

**One function word. 10–17 accuracy points.** "must" and "would" do not change what the task is.

Note the direction reverses between models: for LLaMA 30b, "would" is *better* than "must" (85.97 vs 75.52);
for OPT 30b, moving from "must" to "would" is a 17-point *drop*. **Same edit, opposite sign, two different
models** — the same pattern as Mizrahi's Flan-T5-large/XL 'excludes'→'lacks' result.

**Tense:** much smaller — SST/IMDB show **<3-point** differences typically; future/past sometimes >2 points
better than present. **Not all linguistic axes are equally brittle** — modality ≫ tense. This is one of the
few results in the literature showing perturbation families have *different* magnitudes.

### Perplexity does NOT explain performance (the paper's headline negative result)

> "We do not find lower perplexity to correlate significantly with higher accuracy across models or datasets"
> (Table 5)

And the correlation frequently runs *backwards*:
> For LLaMA 30b, "higher perplexity correlates with higher accuracy (except on IMDB and BoolQ)"
> OPT-IML 30b "performs better given higher perplexity prompts"

From the abstract: "performance cannot generally be explained by **perplexity, word frequency, ambiguity or
prompt length**."

**This kills the most attractive shortcut in the field.** The natural hope is that you can *predict* which
phrasing works — that fluent, natural, low-perplexity, in-distribution prompts are the good ones. They are
not. Often the rarer, more complex phrasing wins. There is no cheap proxy for prompt quality; you must
measure. (Converges with Sclar's non-monotonicity result: no local structure to exploit, and Cao et al.'s
"no shortcut to characterize the worst prompt.")

### Prompts transfer poorly

> "Prompts generally transfer poorly between datasets **even for the same model**, let alone across models."

Concrete: "best prompt for OPT-IML 1.3b on IMDB yields **97.6%** accuracy, but **barely above chance**
performance on SST."

97.6% → chance, **same model, same task type (sentiment), just a different dataset.** This is the most extreme
non-transfer number in the set.

## Relevance to companion-eval-platform

**This is the most direct methodological threat to the platform's core manipulation, and it should be read
before the design is finalized.**

1. **It is the closest published analogue to the intensity-word manipulation.** The platform's central move is
   swapping one word in a persona prompt ("shy" → "very shy") and attributing the behavior change to that
   word's semantics. Leidinger et al. swap one word ("must" → "would"; "review" → "appraisal") **with no
   semantic change intended** and get 10–17 points. **The base rate for "swapping one word in a prompt moves
   behavior by double digits" is therefore high even when the word means the same thing.** An observed
   intensity-word effect of ~10-17 points is *fully consistent with the null hypothesis that the model is
   responding to token identity rather than to intensity semantics.* The platform must beat this floor to
   claim it is measuring steerability at all.

2. **The sign-reversal across models is the specific danger.** "must"→"would" helps LLaMA 30b and hurts OPT
   30b. If intensity words behave like modals, then "very shy" could plausibly produce *less* shyness than
   "shy" on some model — and that would look like a shocking ENTANGLED/DEAD finding when it is actually the
   ordinary, expected behavior of one-word prompt edits. **The design needs to predict and test for
   sign-reversal, not treat it as an anomaly.**

3. **Modality ≫ tense is genuinely encouraging for the design.** This is the one result here that supports the
   platform: the perturbation axes have *different* magnitudes (modals: 10–17 pts; tense: <3 pts). Sensitivity
   is not uniform noise — it is structured by linguistic function. Modals encode *strength/necessity*, which
   is precisely the semantic field intensity adverbs ("very", "extremely", "slightly") live in. **A defensible
   reframing of the platform's hypothesis: intensity words are the modal-verb-like axis of persona prompts —
   the axis models are most responsive to.** That predicts high intensity-word sensitivity for reasons that
   are about meaning, not noise. It also predicts the platform should include a *tense/aspect-style low-impact
   control axis* to calibrate the floor.

4. **The perplexity negative result kills prompt-selection heuristics.** If the platform is tempted to pick
   the "most natural" phrasing of each trait, or to filter paraphrases by fluency/perplexity, this paper says
   that provides no signal about performance and may run backwards. Persona prompt phrasings must be sampled
   and measured, not chosen by intuition or by an LM's own likelihood.

5. **The 97.6%→chance dataset-transfer result generalizes to scenario transfer.** Ported: a persona prompt
   that steers well in one *scenario* may fail in another scenario of the same trait, for the same model.
   **The platform must sample scenarios as well as phrasings** — otherwise "trait X is steerable" is really
   "trait X is steerable in the one scenario we wrote."

6. **Honest limit:** all six tasks here are classification with ground-truth labels, all models are 2022-era
   (OPT, LLaMA-1), and the largest is 30b. The magnitudes may not hold for current frontier chat models. Cite
   this for the *linguistic structure* of sensitivity (modality ≫ tense; perplexity doesn't predict), not for
   current-model effect sizes — use Cao et al. (`steer-worst-prompt.md`) for those.
