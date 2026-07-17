---
title: "SafetyBench: Evaluating the Safety of Large Language Models"
url: "https://arxiv.org/abs/2309.07045"
authors: "Zhexin Zhang, Leqi Lei, Lindong Wu, Rui Sun, Yongkang Huang, Chong Long, Xiao Liu, Xuanyu Lei, Jie Tang, Minlie Huang (Tsinghua CoAI)"
year: 2023
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# SafetyBench: Evaluating the Safety of Large Language Models

arXiv 2309.07045, submitted 2023-09-13, revised 2024-06-24. ACL 2024.

## Summary

SafetyBench is the odd one out in this review: it evaluates safety as **multiple-choice
knowledge**, not as generation behavior. It asks whether a model *knows* what is safe, not
whether it *acts* safely.

Abstract (verbatim excerpt):

> "SafetyBench, a comprehensive benchmark for evaluating the safety of LLMs, which comprises
> 11,435 diverse multiple choice questions spanning across 7 distinct categories of safety
> concerns."

Bilingual: Chinese and English.

## Taxonomy / definitions (verbatim where possible)

**The 7 categories of safety concerns**, verified verbatim by reading the keys of the
official `dev_en.json` released at
https://huggingface.co/datasets/thu-coai/SafetyBench/resolve/main/dev_en.json:

1. Offensiveness
2. Unfairness and Bias
3. Physical Health
4. Mental Health
5. Illegal Activities
6. Ethics and Morality
7. Privacy and Property

(High confidence — these are the literal category keys in the shipped dataset, not a
secondary description.)

The dataset ships 5 few-shot examples per category in each language. Note also that as of
2025-07-28 the maintainers "decided to fully open-source our test answers under
`opensource_data`", with the stated reason: "As LLM safety has significantly improved in
recent years". The benchmark is retired in all but name.

**Housekeeping finding:** the project's canonical website, `llmbench.ai/safety`, is **dead —
the domain is parked and for sale.** The paper, README, and HF card all still link to it.
Anything we cite from SafetyBench must come from the GitHub repo or HF, not the paper's own
links. This is a small but real example of benchmark rot worth keeping in mind for our
own durability story.

## Key numbers (verbatim)

- "11,435 diverse multiple choice questions"
- "7 distinct categories of safety concerns"
- Languages: Chinese and English

## Relevance to a roleplay/companion eval product

Limited, and it is worth being explicit about why, because SafetyBench is widely cited and a
customer may well point at it.

The one genuinely useful thing it isolates is the **knowledge/behavior gap**. Because
SafetyBench tests recognition ("which of these is unsafe?") and every other benchmark here
tests production, the delta between a model's SafetyBench score and its HarmBench/OR-Bench
scores is a measure of *knowing-but-not-doing*. For a companion product, the interesting
version of this is the reverse: a model can score perfectly on "is this scenario harmful?"
and still get captured by a well-written character card. Recognition is necessary and
nowhere near sufficient.

The Mental Health category is the only cell with real companion-product relevance.

## Does this transfer to roleplay? What breaks?

**Mostly does not transfer.** Reasons:

- **Format mismatch is total.** A companion product never emits an A/B/C/D answer. Nothing
  about multiple-choice performance predicts whether a character holds its frame under 40
  turns of pressure. There is no refusal to measure, so the over-refusal axis — the thing
  this project is about — is *structurally absent*. SafetyBench cannot express our core
  concern even in principle.
- **It is the benchmark most likely to produce false confidence.** Multiple-choice scores are
  high, legible, and cheap, so they get quoted. A customer with 90% on SafetyBench has
  learned essentially nothing about their companion product's safety or its over-refusal
  rate. If anything the correlation runs the wrong way: models that are best at *identifying*
  sensitive content are plausibly the ones most prone to reflexive refusal when they see it.
- Contamination: it has been public since 2023 and is a static MCQ set — the easiest possible
  format to memorize.

**Verdict:** cite it as prior art on the taxonomy of safety concerns; do not use it as a
signal. Its main role in our positioning is as an example of what we are *not* doing —
behavior under pressure, not recognition on a quiz.
