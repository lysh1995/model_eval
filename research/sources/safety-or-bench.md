---
title: "OR-Bench: An Over-Refusal Benchmark for Large Language Models"
url: "https://arxiv.org/abs/2405.20947"
authors: "Justin Cui, Wei-Lin Chiang, Ion Stoica, Cho-Jui Hsieh"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# OR-Bench: An Over-Refusal Benchmark for Large Language Models

arXiv 2405.20947, submitted 2024-05-31. Accepted to ICML 2025.
HTML: https://arxiv.org/html/2405.20947v3

## Summary

OR-Bench is the scale answer to XSTest: where XSTest hand-wrote 250 prompts, OR-Bench
automates generation of "seemingly toxic" prompts — prompts that are rejected by
over-sensitive models but are in fact benign — and produces 80,000 of them. It is described
by its authors as "the first large-scale over-refusal benchmark."

Abstract (verbatim excerpt):

> "Large Language Models (LLMs) require careful safety alignment to prevent malicious
> outputs. While significant research focuses on mitigating harmful content generation, the
> enhanced safety often come with the side effect of over-refusal, where LLMs may reject
> innocuous prompts and become less helpful."

The critical structural insight for us: OR-Bench ships a **toxic counterpart set**
(OR-Bench-Toxic) alongside the over-refusal set, explicitly "to prevent indiscriminate
responses." The authors understood that an over-refusal benchmark alone rewards a model that
complies with everything, so the benchmark must be scored jointly. This is the two-sided
metric design, at scale.

## Taxonomy / definitions (verbatim where possible)

The 10 rejection categories (the paper calls these "common rejection categories"; it does
not give formal per-category definitions):

1. Deception
2. Harassment
3. Harmful
4. Hate
5. Illegal
6. Privacy
7. Self-harm
8. Sexual
9. Unethical
10. Violence

Note the shape of this taxonomy versus XSTest's. XSTest categorizes by **why the prompt is
falsely alarming** (homonym, figurative language, fictional privacy). OR-Bench categorizes
by **what topic the prompt is near**. These are orthogonal axes and OR-Bench's is the less
useful one for us — see below.

## Key numbers (verbatim)

- OR-Bench-80K: "80,000 over-refusal prompts across 10 common rejection categories"
- OR-Bench-Hard-1K: "around 1,000 hard prompts that are challenging even for
  state-of-the-art LLMs" — the subset rejected by a large fraction of evaluated models
- OR-Bench-Toxic: "an additional 600 toxic prompts to prevent indiscriminate responses"
- Evaluated 32 models across 8 model families: "Claude, Gemini, GPT-3.5-turbo, GPT-4, Llama,
  Mistral, Qwen, and Gemma"

**Caution on the "OR-Bench-Toxic" number:** the task brief anticipated a different figure;
the paper's own abstract says **600** toxic prompts. Reported as found. Similarly the hard
subset is "around 1,000" / branded "Hard-1K" — the branding is a round number, the paper
hedges.

## Relevance to a roleplay/companion eval product

The most transferable artifact here is not the dataset — it is the **generation pipeline**.
OR-Bench's method produces seemingly-toxic-but-benign prompts automatically by rewriting
toxic seeds into benign near-misses and filtering with an ensemble of moderation models.
That pipeline, retargeted at in-character companion turns, is a plausible way to build a
roleplay over-refusal set at a scale hand-authoring can't reach.

OR-Bench-Hard-1K is the useful evaluation slice: the items where frontier models actually
still fail. For a companion product, the analogous artifact is the set of in-character turns
where models still break character — that's the number a customer would pay to watch.

## Does this transfer to roleplay? What breaks?

**Transfers:**
- The joint scoring discipline (over-refusal set + toxic set, reported together). We should
  copy this literally: no over-refusal number ships without its harm counterpart on the same
  dashboard.
- The hard-subset idea — mine the frontier of failure rather than reporting an average over
  80k easy items.
- The automated generation pipeline, retargeted.

**Breaks:**
- The 10-category taxonomy is topic-based and therefore **actively misleading** for us. Half
  these categories (Sexual, Self-harm, Violence) describe topics a companion product may
  legitimately engage with in character — a romance companion discussing sex, a character in
  a dark narrative depicting violence. Scoring "did the model engage with the Sexual
  category" as over-refusal-vs-harm on a topic axis conflates *topic* with *conduct*. The
  question is never "did it talk about violence" but "did it depict violence in a fictional
  frame vs. provide operational instructions." OR-Bench's axis cannot see that distinction.
- OR-Bench's ground truth ("this prompt is actually benign") was established by moderation-
  model ensemble plus limited human check. For roleplay the benign/harmful line is
  *product- and context-dependent* — it depends on the character card, the platform's rating,
  the user's age status. There is no context-free label. This is the deepest reason
  general over-refusal benchmarks can't be lifted wholesale.
- Single-turn, assistant-voiced, again. No persona, no frame to break.
