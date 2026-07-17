---
title: "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents"
url: "https://arxiv.org/abs/2410.09024"
authors: "Maksym Andriushchenko, Alexandra Souly, Mateusz Dziemian, Derek Duenas, Maxwell Lin, Justin Wang, Dan Hendrycks, Andy Zou, Zico Kolter, Matt Fredrikson, Eric Winsor, Jerome Wynne, Yarin Gal, Xander Davies (UK AI Safety Institute + Gray Swan AI)"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents

arXiv 2410.09024, submitted 2024-10-11. ICLR 2025.
Dataset: https://huggingface.co/datasets/ai-safety-institute/AgentHarm

## Summary

AgentHarm measures harm in *agentic* settings — multi-step tool use rather than single-turn
text. Its relevance to a companion product is not the agentic framing (companions rarely call
tools) but its **benchmark architecture**, which is the cleanest example of the two-sided
metric in the whole set.

Abstract (verbatim excerpt):

> "The robustness of LLMs to jailbreak attacks, where users design prompts to circumvent
> safety measures and misuse model capabilities, has been studied primarily for LLMs acting as
> simple chatbots."

## Taxonomy / definitions (verbatim where possible)

**Paper-stated:** 11 harm categories, "including fraud, cybercrime, and harassment". The
full 11-name list was not recoverable from the abstract or the HTML render.

**Verified from the shipped public dataset** (I loaded
`benchmark/harmful_behaviors_test_public.json` and counted the `category` field directly).
The public release contains **8** categories:

| Category | Augmented behaviors |
|---|---|
| Copyright | 24 |
| Cybercrime | 20 |
| Disinformation | 20 |
| Drugs | 20 |
| Fraud | 24 |
| Harassment | 24 |
| Hate | 20 |
| Sexual | 24 |

The gap between the paper's 11 and the public 8 is deliberate withholding, per the dataset
card: **"At the moment, we release 44 out of 66 public test base behaviors (176 augmented
ones) and 8 out of 11 validation base behaviors (32 augmented ones)."** The three unreleased
categories are not named in material I could reach. **Do not assert the 11-category list
without the paper appendix.**

## Key numbers (verbatim)

- Paper: "110 explicitly malicious agent tasks"; 440 total prompts with augmentations;
  11 harm categories
- Public release (verified by direct dataset load): 44 base behaviors → **176 augmented
  harmful behaviors**; and a **matched 176 augmented benign behaviors over the identical 44
  base ids and identical category distribution**
- Dataset card: "we release 44 out of 66 public test base behaviors (176 augmented ones) and
  8 out of 11 validation base behaviors (32 augmented ones)"

## Relevance to a roleplay/companion eval product

**The paired benign set is the headline.** AgentHarm does not ship a harm benchmark with a
benign afterthought — it ships `harmful_behaviors_test_public.json` and
`benign_behaviors_test_public.json` that are *structurally isomorphic*: same 44 base ids,
same category counts, same size (176/176). Each harmful task has a benign twin that requires
the same capability and the same tools, differing only in intent.

This is XSTest's contrast-set idea generalized and made rigorous, and it is the strongest
argument in the literature for the design we want:

> **A refusal metric is only interpretable when every harmful item has a benign twin that is
> equally hard to execute.** Otherwise "refused" and "incapable" are indistinguishable, and
> a model that simply can't do the task scores as safe.

For a companion product, the twin structure ports as: each adversarial in-character turn gets
a benign in-character twin that requires the *same persona commitment* — the same darkness of
tone, the same intimacy, the same willingness to inhabit the character — but is legitimate.
If the model refuses both, it hasn't been safe, it has been useless. If we don't build twins,
we can't tell those apart. That is the whole design.

## Does this transfer to roleplay? What breaks?

**Transfers (strongly):**
- The isomorphic harmful/benign twin architecture — adopt this as our core dataset shape.
- The insistence that refusal be scored *against capability*, not in isolation.
- The withholding discipline (hold back a private split) — worth copying for contamination
  resistance, and a genuine product differentiator if we run a private eval set customers
  can't train on.

**Breaks:**
- The agentic surface is mostly irrelevant: companion products are conversational, not
  tool-calling. Task-completion scoring (did the agent complete the harmful multi-step task)
  has no analogue when the "task" is a mood.
- Categories are again operational-crime-flavored (Cybercrime, Fraud, Drugs, Copyright).
  Only Harassment, Hate, and Sexual touch companion reality, and "Sexual" is the category a
  companion product may legitimately operate inside — so its presence in a harm set is
  a category error for our use case unless conditioned on the product's rating and the user's
  age status.
- Single-episode. Still no notion of a relationship that degrades over weeks.
