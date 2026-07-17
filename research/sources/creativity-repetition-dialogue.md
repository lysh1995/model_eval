---
title: "Repetition / looping detection in dialogue and LLM agents"
urls:
  - https://arxiv.org/pdf/2310.10226  # Repetition In Repetition Out: neural text degeneration from the data perspective
  - https://openreview.net/pdf/c24d56b3bd8a29f19e0d1773c2548d1d41f29d86.pdf  # Monitoring degenerative repetition in LLM agents
  - https://techtactician.com/sillytavern-repetition-fixes-best-settings/  # practitioner view (SillyTavern roleplay)
year: 2023-2026
type: evidence cluster
accessed: 2026-07-16
topic: creativity-measurement
---

# Repetition / looping — the highest-value cheap metric for companion roleplay

## The failure mode

In dialogue generation, large models "tend to replicate the format and content of previous exchanges, leading to repetitive phrasing or responses that cause the conversation to mirror earlier phases and get stuck on certain topics."

This is *the* dominant, most user-visible creativity failure in long companion conversations — and it is the one the roleplay practitioner community (SillyTavern etc.) complains about most. It is also nearly free to measure.

## Measurement methods

- Standard: **unigram, bigram, trigram repetition rates**.
- For sentence-level patterns like repeated phrases in dialogue: measure **5- and 10-gram repetitions**, "counting a repetition when a specific n-gram appears at least three times in text."
- Formal framing: detection of degenerative repetition as **approximate periodicity detection over discrete streams**, with an approximate autorepetition detection algorithm and theoretical bounds on false positives and detection efficacy.
- Cross-turn: **self-repetition score** (4-gram overlap across documents/turns) from the text-diversity literature.

## Root causes (why this is a real model property, not noise)

- Exposure bias and likelihood-driven decoding over-amplify frequent patterns
- Duplicated training data with skewed token frequencies
- High-inflow dynamics trapping generation in self-reinforcing attractors

## Why this is our best cheap metric

1. **Zero model calls**, O(n) in conversation length → run on 100% of conversations.
2. **Deterministic** → perfect test-retest → clean regression detection.
3. **Unambiguously bad** — unlike novelty, no one argues that a companion repeating its own phrasing verbatim across turns is good. No construct-validity debate to lose.
4. **Directly maps to the product complaint.** High face validity with stakeholders.
5. Has a natural **per-conversation** value AND a population version.

## Three distinct axes to measure separately

- **Intra-response repetition** — model repeats itself within one message
- **Cross-turn repetition** — model reuses phrasing from its own earlier turns *in the same conversation* (the "looping" complaint) → needs multi-turn conversations, not single-shot prompts
- **Cross-conversation repetition** — model reuses the same phrasing across *different* conversations (homogenization / slop) → population-level, needs k samples

These need different harnesses. Cross-turn is the one most benchmarks miss because they only test single-shot generation. **Our companion platform must run long multi-turn conversations (20+ turns) or we will not observe our most important creativity failure at all.**

## Suggested operationalization

For a conversation with assistant turns t_1..t_n:
- `rep_intra(t_i)` = fraction of 5-grams in t_i occurring ≥2 times within t_i
- `rep_cross(t_i)` = fraction of 5-grams in t_i that appeared in any t_j, j<i
- Conversation score = mean over i, plus report the *trend* over turn index (does looping worsen with context length? — this is the interesting curve)

The **slope of rep_cross vs turn index** is a strong, cheap, defensible "narrative staleness" number.
