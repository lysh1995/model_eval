---
title: "EQ-Bench Creative Writing v3 + Slop Score"
urls:
  - https://eqbench.com/creative_writing.html
  - https://eqbench.com/slop-score.html
  - https://github.com/EQ-bench/creative-writing-bench
year: 2025-2026
type: benchmark / production system
accessed: 2026-07-16
topic: creativity-measurement
---

# EQ-Bench Creative Writing v3 — the closest production analogue to what we're building

## Judge methodology

- **32 writing prompts × 3 iterations per prompt**.
- Hybrid scoring: **rubric assessment + Elo ratings via pairwise comparisons**. (Note: they use BOTH, matching the LitBench conclusion that pairwise carries the reliable signal while rubric carries diagnostics.)
- Judge model: Claude Sonnet 4.6 recommended "for leaderboard parity" — i.e. **the judge model is pinned as part of the benchmark definition**. Changing the judge invalidates cross-run comparison. Exactly the "same baseline for each model" discipline we need.
- Prompts target humor, romance, spatial awareness, unique perspectives.

## Acknowledged uncontrolled biases (verbatim list)

- judge self-bias (judge prefers its own family's outputs)
- positivity / negativity bias
- NSFW content aversion ("smut bias") — **highly relevant to companion/roleplay eval**
- stylistic preferences
- **"slop" bias** — favoring overused tropes

That last one is the LLM-judge-prefers-generic-text failure mode, admitted by the benchmark authors themselves. It is why they built a separate mechanical Slop Score rather than trusting the judge to penalize cliché.

## Slop Score — a cheap, no-model-call metric

Measures frequency of words/phrases typically overused by LLMs ("GPT-isms"), by matching text against a master slop list.

**Weighted composite:**
- **60%** — Slop Words
- **25%** — Not-x-but-y Patterns  (e.g. "it wasn't just X, it was Y")
- **15%** — Slop Trigrams

**List construction method (this is the reusable part):** slop word and trigram lists identify words and n-grams that are **statistically over-represented in LLM outputs compared to human writing**, by analyzing outputs from 10 different language models on essay and creative writing prompts, then comparing against human-authored text.

## Why this is the best single template for us

1. It is a **frequency-ratio against a human reference distribution**, not an absolute novelty measure. Sidesteps the Death-of-Novelty precision problem: we're not claiming novel = creative, we're claiming *this specific known-cliché inventory* = uncreative. Much easier to defend.
2. Zero model calls → run on 100% of responses.
3. Directly interpretable and debuggable — you can show the engineer the exact matched phrases.
4. Fully deterministic → perfect test-retest → ideal regression detector.
5. Domain-adaptable: we should build our **own** slop list from *roleplay/companion* outputs vs human roleplay/fiction text. Generic GPT-ism lists will miss companion-specific slop ("a mischievous glint in her eye", "voice barely above a whisper", "little did they know").

**Caveat:** it's a negative metric (absence of cliché), not a positive one (presence of creativity). Low slop ≠ creative. Pair with the pairwise judge.
