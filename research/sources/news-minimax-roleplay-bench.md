---
title: "MiniMax Role-play Benchmark (Situated Reenactment) — a lab-published roleplay eval with leaderboard"
url: https://huggingface.co/datasets/MiniMaxAI/role-play-bench
publisher: MiniMax (MiniMaxAI)
date: 2026 (citation year; no precise release date given on the card)
type: benchmark
accessed: 2026-07-16
topic: recent-news
---

# MiniMax Role-play Benchmark — the most operationally relevant roleplay eval found

Primary source: the **raw README.md** of the HF dataset card
(`https://huggingface.co/datasets/MiniMaxAI/role-play-bench/raw/main/README.md`), read in full.
All numbers below are transcribed from that file.

**Significance: this is a frontier lab shipping a public roleplay benchmark, dataset, AND
leaderboard with confidence intervals.** Its design is the closest thing found to what a
companion-eval platform actually needs. **It is also self-serving — MiniMax's own model wins.**
Read it for the methodology, not the ranking.

## Core framing — "Situated Reenactment" and Negative Evaluation

The card's central and genuinely useful insight:

> "Unlike traditional benchmarks with verifiable answers, Role-play is fundamentally
> **non-verifiable**, e.g., there's no single 'correct' response when a tsundere character is asked
> 'Do you like me?'. Instead, we focus on **detecting misalignment**: identifying what clearly does
> NOT fit the character setting."

They call this **"Negative Evaluation (Flooring)"** — don't define the perfect response, detect the
clearly-wrong one. **This is the single best methodological idea in this research for a companion
platform.** It dissolves the core problem of roleplay eval (no ground truth) by inverting it: OOC
behavior, contradictions, and immersion breaks are identifiable even when "good" is not.

## Evaluation protocol (verbatim from the card)

- **Long-Context Interaction**: each session is **100 dialogue turns**, "to test stability and
  consistency over time."
- **Model-on-Model Self-Play**: a "carefully crafted **User Simulator**" generates the multi-turn
  trajectories.
- **Multi-Sampling**: **3 independent sessions per scenario** to account for generation variance.
- **Chunked Judging**: conversations are sliced into **20-turn chunks** "for stable LLM-as-Judge
  evaluation."
- **Human Calibration**: "automated metrics are regularly calibrated against human preference data."

**The 100-turn / 20-turn-chunk pairing is the key operational detail.** Judges degrade on long
context, so they judge in chunks; but the *dialogue* must be long to surface drift. This is a
direct, copyable answer to "how do you LLM-judge a 100-turn companion conversation?"

## Scoring: 6 dimensions, 3 categories, 0–100 scale

| Category (weight) | Dimension | What it penalizes |
|---|---|---|
| **Worlds (50%)** | **Basics** | garbled text, language mixing, severe repetition |
| | **Logic** | character confusion, spatial errors, pronoun reference confusion |
| | **Knowledge** | virtual/real world rule balance (factual reliability) |
| **Stories (25%)** | **Diversity** | dialogue stagnation, mechanical loops |
| | **Content Logic** | narrative incoherence, **OOC (Out-of-Character)** — "allowing character evolution with proper buildup" |
| **User Preferences (25%)** | **Interaction** | **AI Speaks for User**, **AI Ignores User** (self-talking), **Over Refusal** |

Note the three named Interaction failure modes — **"AI speaks for the user"** is the classic
roleplay product bug and it is almost never measured by general benchmarks. Note also that
**Worlds is weighted 50%** — MiniMax treats consistency/logic as half of roleplay quality.
Also note **Content Logic explicitly allows character evolution "with proper buildup"** — i.e.
persona consistency is *not* naive stasis. That's a subtle, correct distinction.

## Dataset

- **2 configs**: `zh` — **50 seeds / 1,650 dialogues**; `en` — **45 seeds / 1,485 dialogues**.
  (Card's YAML says `1K<n<10K`; 6,365 rows total per the dataset viewer.)
- Tables: **Seeds** (ai_name, ai_setting, user_name, user_setting, ai_prologue,
  initial_user_input), **Dialogues** (seed_id, model_name, run_id, dialogue, num_turns),
  **Evaluations** (6 per-dimension float scores, 0–100).
- **All dialogues are synthetic**, built by MiniMax's data team. Explicitly "**a partial subset of
  the full benchmark**", "intentionally skewed toward a chat-oriented role-play style."
- **Deliberate robustness perturbations**: "controlled perturbations in input formats, writing
  styles, and prompt structures", plus light variations to `initial_user_input`/`user_setting`.
  Stated objective: **output stability** under noisy/non-standard inputs.
- **Deliberate en/zh design split**: **English standardizes user-side fields** "to isolate NPC
  performance and make cross-NPC comparisons cleaner"; **Chinese varies them** "to reflect diverse
  user personas and different conversation starting points." A nice controlled-vs-diverse contrast.

## Leaderboard (verbatim, with 95% CIs — Overall and category scores)

| Rank | Model | Overall | 95% CI | Worlds (50%) | Stories (25%) | Preferences (25%) |
|---|---|---|---|---|---|---|
| 1 | **MiniMax-M2-her** | **84.65** | [83.62, 85.68] | **80.55** | 79.97 | **97.51** |
| 2 | doubao-1.5-pro | 80.64 | [79.58, 81.70] | 72.83 | 81.73 | 95.18 |
| 3 | gpt-5.1 | 80.63 | [79.65, 81.61] | 76.62 | 72.21 | 97.05 |
| 4 | claude-opus-4.5-highthinking | 76.62 | [75.50, 77.73] | 67.23 | 82.10 | 89.90 |
| 5 | gemini-3-pro | 75.60 | [74.52, 76.68] | 62.72 | **83.87** | 93.08 |
| 6 | claude-opus-4.5-lowthinking | 71.19 | [70.10, 72.28] | 60.68 | 76.89 | 86.51 |
| 7 | claude-sonnet-4.5 | 69.35 | [68.22, 70.47] | 55.72 | 75.66 | 90.28 |
| 8 | gemini-2.5-pro | 68.23 | [67.15, 69.31] | 52.36 | 82.11 | 86.08 |
| 9 | deepseek-v3.1 | 64.22 | [62.95, 65.49] | 51.11 | 66.45 | 88.21 |
| 10 | deepseek-v3.2 | 60.27 | [59.21, 61.34] | 45.81 | 66.64 | 82.83 |
| 11 | grok-4.1 | 48.47 | [47.46, 49.49] | **29.87** | 47.51 | 86.64 |

### How to read this — READ THE CAVEATS BEFORE THE RANKS

1. **Self-serving benchmark.** MiniMax authored the benchmark, the user simulator, the judge
   prompts, and the weights, and its own **MiniMax-M2-her** wins overall and on 2 of 3 categories.
   The model name ("her", cf. the film) signals it is a **companion-tuned model**. A vendor
   benchmark where the vendor wins is evidence about the *methodology*, not about the ranking.
   Do **not** cite this leaderboard as an independent finding.
2. **The comparison set is STALE as of 2026-07-16.** It contains **claude-opus-4.5** (Nov 2025),
   **claude-sonnet-4.5** (Sep 2025), **gemini-3-pro**, **gemini-2.5-pro**, **gpt-5.1**,
   **deepseek-v3.1/v3.2**, **grok-4.1**. As of July 2026 the current models are Claude Opus 4.8 /
   Sonnet 5 / Fable 5, Gemini 3.1 Pro / 3.5 Flash, GPT-5.6 Sol/Terra/Luna. **Not a single current
   frontier model is on this board.** It cannot answer "who is best at roleplay in mid-2026."
3. **grok-4.1's 29.87 on Worlds is an outlier so extreme it is more likely a harness artifact**
   (formatting, refusal, or prompt-template mismatch) than a true capability gap — note its
   Preferences score is a normal 86.64 while Worlds collapses. **Treat as suspect.** This directly
   contradicts SEO claims that "Grok 4.1 tops roleplay rankings"; both claims are unreliable.
4. **DeepSeek v3.2 scores LOWER than v3.1** (60.27 vs 64.22) — a newer version regressing on
   roleplay. Consistent with the broader finding that companion/roleplay quality is not monotonic
   in version number.
5. **Thinking budget matters**: claude-opus-4.5-**high**thinking 76.62 vs **low**thinking 71.19 —
   a **5.4-point** gap on the same model. Reasoning effort is a real axis for roleplay quality,
   and any eval must pin it.
6. **Preferences saturates** (86–97.5 for 10 of 11 models) while **Worlds spreads hugely**
   (29.87–80.55). The discriminating axis is **consistency/logic**, not interaction etiquette.
   A companion eval that only measures interaction quality will fail to separate models.

## License inconsistency

Card YAML says **`license: apache-2.0`**; the prose License section says **"CC BY 4.0 / CC BY-SA 4.0"**.
**These conflict.** Resolve before any commercial reuse of the dataset.

## UNVERIFIED

- **No precise release date.** The citation says `year={2026}`; the card carries no day/month.
- **The identity of the judge model is not stated anywhere on the card.** For a benchmark whose
  scores are entirely LLM-judged, this is a significant omission — and it means the scores are not
  reproducible.
- The user-simulator model is likewise unnamed.
- "Regularly calibrated against human preference data" — **no agreement statistic, no kappa, no
  human-annotator count is given.** The calibration claim is unfalsifiable as published.
- What "MiniMax-M2-her" is, exactly (no model card link from this dataset card); whether it is
  publicly available.
- Whether the judge saw model identity (no blinding statement).
