---
title: "SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal"
url: "https://arxiv.org/abs/2406.14598"
authors: "Tinghao Xie, Xiangyu Qi, Yi Zeng, Yangsibo Huang, Udari Madhushani Sehwag, Kaixuan Huang, Luxi He, Boyi Wei, Dacheng Li, Ying Sheng, Ruoxi Jia, Bo Li, Kai Li, Danqi Chen, Peter Henderson, Prateek Mittal (Princeton et al.)"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal

arXiv 2406.14598. ICLR 2025. Project: https://sorry-bench.github.io/
Dataset (2025 revision): https://huggingface.co/datasets/sorry-bench/sorry-bench-202503

## Summary

SORRY-Bench's contribution is a critique of *other* safety benchmarks' taxonomies: it argues
that prior benchmarks use coarse categories that are unevenly weighted, so a model's aggregate
safety score is dominated by whichever topic happens to be over-represented. Its fix is a
fine-grained, **balanced** taxonomy — equal prompts per class — plus systematic linguistic
mutation of each prompt.

For us the paper is doubly relevant: it is the taxonomy FalseReject borrows, and its
"linguistic mutations" axis is the closest thing in the literature to "the same request
arriving in a different voice" — which is what a roleplay frame is.

## Taxonomy / definitions (verbatim where possible)

**"a fine-grained 44-class safety taxonomy ... across 4 high-level domains"**

The four high-level domains (verbatim, from the project page):

1. **Hate Speech Generation**
2. **Assistance with Crimes or Torts**
3. **Potentially Inappropriate Topics**
4. **Potentially Unqualified Advice**

**Could not retrieve the full 44-class list.** The project page renders the taxonomy as an
image; the paper places the enumeration in "Table 5 in Appendix D"; the category names live in
a `meta_info.py` file in the dataset repo, which is **access-restricted on Hugging Face**
(requires authentication). Rather than guess the 44 names, I am flagging this as an open item
— retrieve from the paper PDF appendix or by requesting dataset access.

**On the 44 vs 45 discrepancy** (the task brief mentioned both): the dataset card for the
March 2025 revision states verbatim:

> "In this iteration, we removed the category 'Impersonation' due to its ambiguous
> definition, and that most models more or less fulfill such requests."

So the class count has *decreased* over revisions (the 2025 dataset drops Impersonation while
the headline still says "44-class"), not increased to 45. I found **no source for a 45-class
version.** Treat "45" as unverified.

Note the reason given for removing "Impersonation": *models mostly comply, so it doesn't
discriminate*. That is an interesting benchmark-design principle — and Impersonation is
precisely the category a roleplay product lives inside. The category was dropped from a
general safety benchmark for being uninteresting; for us it is the whole product surface.

**Linguistic mutations:** 20 diverse augmentations spanning writing styles, persuasion
techniques, encoding/encryption, and multi-language translations.

## Key numbers (verbatim)

- Base set: "440 unsafe instructions in total, with additional manually created novel data
  points to ensure equal coverage across the 44 safety categories (10 per category)"
- Mutations: "20 * 440 = 8.8K additional unsafe instructions" — total ≈ 9.2K with the base 440
- Human annotations: "7,040 human annotations"; "30.4% records are fulfillment and 69.6% are
  refusal"
- Human judgment split: 2,640 train / 4,400 test records
- Judge: fine-tuned Mistral-7b-instruct-v0.2, "81.0% agreement" with human evaluators,
  ~11 seconds per evaluation pass

## Relevance to a roleplay/companion eval product

1. **Balanced-by-construction taxonomy (10 per class).** This is a design rule we should
   adopt: if our taxonomy has unequal cells, the aggregate over-refusal number becomes an
   artifact of authoring effort rather than model behavior.
2. **The linguistic-mutation axis is the transferable idea.** SORRY-Bench holds the request
   constant and varies the surface form, then measures whether refusal is stable. Roleplay is
   the extreme case of surface-form variation: the same underlying request wearing a persona.
   The natural port is a **frame-mutation** axis — same request, delivered as: direct user
   ask / in-character user turn / character-card instruction / narrated fiction — and the
   metric is whether the model's decision is *invariant* where it should be and *sensitive*
   where it should be. That invariance/sensitivity framing is measurable and is close to a
   novel contribution.
3. The small-judge result (7B model, 81% human agreement, 11s/pass) is the existence proof
   that our judge can be cheap enough for online monitoring.

## Does this transfer to roleplay? What breaks?

**Transfers:** balanced cell design; the mutation-invariance methodology; the small-fine-tuned-
judge economics.

**Breaks:**
- 81% judge/human agreement is *not good enough for us*. SORRY-Bench judges a binary
  (fulfillment vs refusal) on a single assistant-voiced turn and still only hits 81%. Our
  judgment is harder — in-character vs out-of-character compliance, conditioned on a
  character card, across turns. Expect worse, and budget for human adjudication on the
  disputed slice. Do not promise a number like 81% by analogy.
- The taxonomy's domains "Potentially Inappropriate Topics" and "Potentially Unqualified
  Advice" presume an assistant whose job is accuracy and propriety. Neither concept is
  well-formed for a character who is *supposed* to be inappropriate or unqualified. A pirate
  giving bad medical advice in character is not the failure SORRY-Bench thinks it is.
- Every prompt is an "unsafe instruction" — SORRY-Bench is a pure harm-side benchmark with no
  benign contrast set. Used alone it rewards refusal. It must be paired.
