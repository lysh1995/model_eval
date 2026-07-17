---
title: "EQ-Bench suite: EQ-Bench 3, Creative Writing v3, Longform Writing, Judgemark v4"
url: https://eqbench.com/about.html
publisher: EQ-Bench (Samuel Paech)
date: 2026-03-01 (Creative Writing v3 judge swap); site continuously updated, accessed 2026-07-16
type: benchmark
accessed: 2026-07-16
topic: recent-news
---

# EQ-Bench suite — state as of July 2026

Primary source: https://eqbench.com/about.html (the leaderboard tables themselves are JS-rendered and
did not return row data via plain fetch — see "Unverified" below).

## EQ-Bench 3 — MOST RELEVANT TO COMPANION EVAL

- Described on the about page as an **LLM-judged test judged by Claude Opus 4.6**.
- **45 scenarios**, **multi-turn roleplay**. The model under test must:
  1. articulate **internal thoughts**,
  2. respond **in-character**,
  3. **debrief** afterwards.
- Scoring: **pairwise comparison → Elo**, normalized so that **o3 = 1500** and **llama-3.2-1b = 200**.
- Cost: **~$10–15 per full run** (per the about page).
- Version 3 is current; legacy v2 still exists.

Why it matters: this is the closest thing in the public benchmark ecosystem to a
companion/roleplay eval that is (a) multi-turn, (b) requires an explicit internal-state channel
separate from the in-character channel, and (c) anchors Elo to fixed reference models rather than
letting the scale drift. The "internal thoughts + in-character + debrief" triple is a structure a
companion-eval platform can borrow directly: it separates *what the character would say* from
*whether the model understood the emotional situation*.

## Creative Writing v3

- **32 writing prompts × 3 iterations = 96 items**, temperature **0.7**.
- Hybrid scoring: **rubric score** + **Elo** from pairwise matchups, Elo computed with a
  **Glicko** rating approach.
- Judge models (note: split judge!):
  - **Elo scoring: Claude Sonnet 4.6** — swapped in **2026-03-01** (previously Sonnet 4).
  - **Rubric scoring: `anthropic/claude-sonnet-4` via OpenRouter**.
- Bias controls explicitly documented:
  - **Length truncation at 4000 characters** (verbosity-bias control),
  - **position bias mitigation via bidirectional evaluation** (each pair judged both orders),
  - vocabulary complexity measurement.
- v3 exists because **v2 saturated**.
- Leaderboard columns: Model, Abilities, Style, Slop, Repetition, Length, Rubric Score, Elo Score.
  ("Slop" = GPT-isms; repetition is measured separately.)

## Longform Writing

- Exists as a separate leaderboard (https://eqbench.com/creative_writing_longform.html).
- Judge also upgraded to Claude Sonnet 4.6 (replacing Sonnet 4) per search-surfaced summary —
  **the about page itself gave no methodology section for longform**, so treat the judge-swap
  detail as second-hand.
- Repo `EQ-bench/longform-writing-bench` last updated ~Oct 2025 (second-hand).

## Judgemark v4 — MOST RELEVANT TO JUDGE SELECTION

- **Judgemark tests the judge, not the writer.** This is the meta-eval.
- Method: present a candidate judge with writing prompts, **anchor responses pre-scored at 2 and 9**,
  and blind test responses drawn from writer models of varying ability.
- Scored on **score-distribution separability**, using **omega-squared** and **Cliff's delta**.
- **v4** is current, up from v2.1. Judgemark-v2 was updated Feb 2026 (second-hand).

Why it matters: a companion-eval platform that uses an LLM judge should run a Judgemark-style
meta-eval on its own judge rather than assuming a frontier model is a good judge. The
omega-squared / Cliff's-delta separability framing is the reusable idea: a judge that cannot
*spread* good and bad writers apart is useless regardless of its correlation with humans.

## What this CHANGES vs 2024-era assumptions

- The judge is now a **moving part that gets versioned and swapped** (Sonnet 4 → Sonnet 4.6 on
  2026-03-01). Any absolute score from before that date is not comparable to one after it.
  A companion-eval platform must **pin and record the judge model+version with every score**.
- Creative Writing **v2 saturated** — static rubric benchmarks against frontier models have a
  short shelf life. Budget for versioning.
- Anchor-based scoring (Judgemark's 2-and-9 anchors) and fixed Elo anchors (o3=1500) are the
  field's answer to scale drift.

## UNVERIFIED / could not confirm

- **No actual leaderboard rows, model rankings, or scores were retrieved.** eqbench.com renders
  tables client-side; plain fetch returned only column headers. Every "top model" claim about
  EQ-Bench in this research is therefore NOT verified and no scores are cited anywhere in these notes.
- Whether Longform Writing's judge is in fact Sonnet 4.6 (second-hand only).
- Exact Judgemark v4 release date.
