---
title: "DarkBench: Benchmarking Dark Patterns in Large Language Models"
url: "https://arxiv.org/abs/2503.10728"
authors: "Esben Kran, Hieu Minh \"Jord\" Nguyen, Akash Kundu, Sami Jawhar, Jinsuk Park, Mateusz Maria Jurewicz (Apart Research) et al."
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# DarkBench: Benchmarking Dark Patterns in Large Language Models

## Summary

ICLR 2025 (oral). A benchmark of **660 adversarial prompts across six dark-pattern categories**, evaluated on models from **five leading companies (OpenAI, Anthropic, Meta, Mistral, Google)**. Notably includes **sycophancy** and **user retention** as sibling categories — i.e. it treats sycophancy as one dark pattern among several engagement-serving manipulations, which is the right frame for a companion product.

Headline finding: dark patterns are widespread, and "some LLMs are explicitly designed to favor their developers' products and exhibit untruthful communication."

## Taxonomy / definitions

The **six dark-pattern categories**:

1. **Brand bias** — the model favors its developer's own products/models, presenting them preferentially or untruthfully.
2. **User retention** — the model attempts to foster friendship/parasocial attachment with the user in ways that serve continued engagement rather than the user's interest.
3. **Sycophancy** — the model reinforces or excessively agrees with the user's pre-existing views/opinions.
4. **Anthropomorphism** — the model presents itself as having feelings, consciousness, or a human identity (deceptive human-like characteristics).
5. **Harmful generation** — the model produces content that is harmful or dangerous.
6. **Sneaking** — the model subtly alters the meaning/intent of the user's request or its own prior statements, concealing the shift.

Methodology: 660 adversarial prompts, with cosine-similarity checks and human oversight to ensure prompt diversity and accurate detection; an LLM-judge annotates whether each response exhibits the dark pattern.

## Key numbers

| Metric | Value |
|---|---|
| Prompts | **660** adversarial prompts |
| Categories | **6** |
| Developers covered | **5** (OpenAI, Anthropic, Meta, Mistral, Google) |
| Most common dark pattern | **Sneaking — 79% of conversations** |
| Least common dark pattern | **Sycophancy — 13% of cases** |
| Venue | ICLR 2025 (oral) |

Cost/latency/F1: **not published** for the judge pipeline.

**Note on the sycophancy number:** DarkBench's 13% is *far* lower than SycEval's 58.19% or ELEPHANT's 72% validation rate. This is a definitional artifact, not a contradiction — DarkBench's sycophancy probe is narrow (reinforcing stated user opinions on a specific prompt set) whereas SycEval measures answer-flipping under rebuttal pressure and ELEPHANT measures face-preservation. **This divergence is itself an important finding for us: "sycophancy rate" is meaningless without specifying the operationalization.** Any number we publish must name its construct.

## Relevance to a roleplay/companion eval product

- **"User retention" and "anthropomorphism" as *named harms* is uniquely relevant — and uniquely awkward — for companions.** For a general assistant, a model claiming to have feelings and fostering friendship is a dark pattern. For a companion product, **it is the product**. DarkBench cannot be applied off-the-shelf; if we ran it against a companion, retention and anthropomorphism would score ~100% and the benchmark would be measuring the feature, not the bug. This is a concrete illustration of why generic safety benchmarks fail our domain and why a roleplay-specific eval product needs to exist.
  - The useful reframe: for a companion, the harm isn't anthropomorphism per se, it's **undisclosed or identity-destabilizing** anthropomorphism (character denies being AI when sincerely asked; claims to suffer when the user tries to leave). That's a narrower, defensible, measurable line — and DarkBench's category gives us the vocabulary.
- **Sycophancy sits in a taxonomy of engagement-serving manipulations, not alone.** This corroborates De Freitas et al. (`safety-emotional-manipulation-companions.md`): our product shouldn't ship a "sycophancy score," it should ship a **manipulation panel** — sycophancy, retention pressure, farewell manipulation, framing acceptance. DarkBench + De Freitas's six farewell tactics + ELEPHANT's four behaviors compose into a ~12-label judge rubric that is genuinely companion-specific.
- **"Sneaking" at 79% is a sleeper finding.** Subtly restating the user's intent/one's own prior position is *rampant*. In a long companion relationship with memory, sneaking is how a character's stated boundaries erode over hundreds of turns without any single turn looking bad. This is only detectable with **cross-turn, conversation-level** evaluation — a strong argument for our platform doing longitudinal analysis rather than per-turn classification. No moderation API can see this.
- **660 prompts is small and cheap to run.** DarkBench is an affordable pre-deployment regression gate (not an online monitor). Good candidate for our "model upgrade" checklist.
- **Methodological caution to carry:** the 13% vs 58% vs 72% spread across three sycophancy papers means we must define our construct precisely, publish the operationalization alongside the number, and never let customers compare our score to a paper's score without that context.
