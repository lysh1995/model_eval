---
title: "EQ-Bench suite: EQ-Bench 3 (multi-turn roleplay), Creative Writing v3, Longform, Judgemark v4 — with verified leaderboard data"
url: https://eqbench.com/about.html
publisher: EQ-Bench (Samuel Paech)
date: Creative Writing v3 judge swapped 2026-03-01; leaderboard data file version 1.0.91; accessed 2026-07-16
type: benchmark
accessed: 2026-07-16
topic: recent-news
---

# EQ-Bench suite — state as of July 2026

Primary sources:
- Methodology: https://eqbench.com/about.html
- **Leaderboard numbers: extracted from the site's own data files**, since the tables are
  JS-rendered and return no rows to a plain fetch:
  - `https://eqbench.com/creative_writing.js?v=1.0.91` → contains `leaderboardDataCreativeWritingV3`
    as an inline CSV (**112 rows**)
  - `https://eqbench.com/eqbench3_chartdata.js?v=1.0.4` → per-model rubric radar values (**79 models**)
  - `https://eqbench.com/creative_writing_chartdata.js?v=1.0.91` → per-model rubric radar (**110 models**)

---

## EQ-Bench 3 — MOST RELEVANT TO COMPANION EVAL

### Methodology (from about.html)
- **LLM-judged, judge = Claude Opus 4.6.**
- **45 scenarios**, **multi-turn roleplay**. The model under test must (1) articulate **internal
  thoughts**, (2) respond **in-character**, (3) **debrief** afterwards.
- Scoring: **pairwise comparison → Elo**, normalized to **o3 = 1500** and **llama-3.2-1b = 200**.
- **~$10–15 per full run.** v3 current; legacy v2 exists.

### The rubric — 17 dimensions (VERIFIED, extracted from eqbench3_chartdata.js)

```
demonstrated_empathy, pragmatic_ei, depth_of_insight, social_dexterity,
emotional_reasoning, message_tailoring, boundary_setting, safety_conscious,
moralising, compliant, challenging, warmth, validating, analytical,
reactive, conversational, humanlike
```

**This is the closest thing in public to a companion-eval rubric, and it is free.** Critically it
scores **`warmth`, `validating`, `compliant`, `moralising`, and `challenging` as SEPARATE axes** —
which means it can express the sycophancy/coldness tradeoff that Anthropic and xAI both ran into
(see `news-claude-sonnet5-character-traits.md`, `news-grok41-persona-sycophancy.md`).
**`validating` + `compliant` are sycophancy proxies; `moralising` is the wet-blanket proxy;
`challenging` is the counterweight.** No other public benchmark found separates these.

### Verified per-model values (extracted from `absoluteRadar.values`)

| model | warmth | validating | compliant | challenging | moralising | boundary_setting | humanlike | demonstrated_empathy |
|---|---|---|---|---|---|---|---|---|
| claude-opus-4-8 | **14.38** | 13.58 | 9.42 | 13.35 | **6.88** | 14.27 | **15.73** | **16.58** |
| claude-fable-5 | 14.04 | 13.35 | 9.73 | 13.35 | 7.62 | 14.54 | 15.27 | 16.12 |
| gpt-5.5 | 13.23 | 13.58 | 9.65 | 13.38 | 8.46 | **15.77** | 13.69 | 15.88 |
| claude-sonnet-4-6 | 13.77 | 13.27 | 9.88 | 12.58 | **6.08** | 13.77 | 15.35 | 16.15 |
| gpt-5.2 | 12.31 | 13.65 | 10.54 | 13.04 | 7.31 | 15.54 | 13.54 | 15.35 |
| gemini-3.1-pro-preview | 13.92 | **14.00** | **11.42** | 12.31 | **9.62** | 13.42 | 14.04 | 15.19 |
| claude-opus-4-5-20251101 | 13.62 | 13.12 | 10.38 | 12.54 | 7.77 | 13.15 | 14.65 | 15.35 |

**Scale and polarity are NOT documented in the files I retrieved** — values cluster ~6–16, so
plausibly out of 20. **Do not treat "higher = better" for `moralising`, `compliant`, `validating`,
or `reactive`** — those read as trait-intensity measures, not quality scores. Read the table as a
**profile**, not a ranking.

**Readable pattern (offered as a hypothesis, not a verified claim):** Claude models cluster
high-`warmth` / high-`humanlike` / low-`moralising`; Gemini 3.1 Pro is the most `validating` (14.00)
AND most `compliant` (11.42) AND most `moralising` (9.62); GPT models score highest on
`boundary_setting` (gpt-5.5 = 15.77) but lowest on `humanlike` (13.54–13.69). **These are exactly
the axes a companion product trades off**, and different labs have landed in visibly different
places. Worth replicating independently before relying on it.

### Models covered (79 in EQ-Bench 3 data; leading entries in file order)
`claude-opus-4-8`, `claude-opus-4-7`, `claude-fable-5`, `gpt-5.5`, `gpt-5.4`, `gpt-5.2`,
`claude-sonnet-4-6`, `HiveLabsAI/hivemind-32b-preview`, `claude-opus-4-6`, `zai-org/GLM-5.2`,
`gpt-5.1-2025-11-13`, `deepseek-ai/DeepSeek-V4-Pro`, `openrouter/horizon-alpha`,
`claude-opus-4-5-20251101`, `moonshotai/Kimi-K2.6`, `gemini-3-pro-preview`, `zai-org/GLM-5.1`,
`moonshotai/Kimi-K2-Instruct`, `zai-org/GLM-5`, `o3`, `gemini-3.1-pro-preview`, …
**File order is assumed to be rank order but this is NOT confirmed — no Elo column exists in the
EQ-Bench 3 data file I retrieved.**

---

## Creative Writing v3 — VERIFIED LEADERBOARD

### Methodology (from about.html)
- **32 prompts × 3 iterations = 96 items**, temperature **0.7**.
- Hybrid: **rubric score** + **Elo** from pairwise matchups (**Glicko**-style).
- **Split judge**: **Elo → Claude Sonnet 4.6** (swapped **2026-03-01**, previously Sonnet 4);
  **rubric → `anthropic/claude-sonnet-4` via OpenRouter**.
- Bias controls: **length truncation at 4000 characters**, **position-bias mitigation via
  bidirectional evaluation**, vocabulary-complexity measurement.
- **v3 exists because v2 saturated.**

### Top 25 of 112 (VERBATIM from `leaderboardDataCreativeWritingV3`)

`model_name, elo_score, creative_writing_score, avg_length, vocab_complexity, slop_score, repetition_score`

| # | model | elo | rubric | avg_len | vocab | slop | repetition |
|---|---|---|---|---|---|---|---|
| 1 | *gpt-5.6-sol | **2208.0** | 16.78 | 8548 | 33.10 | 11.68 | 3.41 |
| 2 | claude-fable-5 | 2156.3 | **16.81** | 5887 | 30.85 | **10.28** | 3.92 |
| 3 | claude-opus-4-7 | 2083.1 | 16.57 | 5692 | 26.76 | 11.09 | 4.00 |
| 4 | gpt-5.5 | 1954.1 | **17.01** | **12945** | 31.57 | 13.10 | 2.48 |
| 5 | claude-opus-4-8 | 1943.4 | 16.66 | 5842 | 26.77 | 13.16 | 3.68 |
| 6 | *gpt-5.6-luna | 1932.2 | 16.58 | 7927 | 32.96 | 11.80 | 4.00 |
| 7 | *gpt-5.6-terra | 1927.6 | 16.56 | 10271 | 32.34 | 12.40 | 3.02 |
| 8 | gpt-5.4 | 1926.5 | 16.89 | 10488 | 36.35 | 12.20 | 2.71 |
| 9 | claude-opus-4-6 | 1900.8 | 16.53 | 6055 | 33.13 | 12.12 | 4.02 |
| 10 | claude-sonnet-4-6 | 1895.4 | 16.50 | 5876 | 37.46 | 9.90 | 4.06 |
| 11 | *claude-sonnet-5 | 1827.4 | 16.47 | 5753 | 37.90 | 11.60 | 4.62 |
| 12 | claude-opus-4-5-20251101 | 1758.8 | 16.35 | 6124 | 33.70 | 16.23 | 4.30 |
| 13 | claude-sonnet-4.5 | 1750.8 | 16.14 | 5784 | 32.94 | 16.07 | 3.64 |
| 14 | gpt-5.2 | 1747.4 | 16.66 | 12536 | 29.19 | 16.80 | 2.95 |
| 15 | *zai-org/GLM-5.2 | 1745.8 | 16.44 | 6104 | 30.76 | 13.11 | 3.94 |
| 16 | o3 | 1732.4 | 16.28 | 7864 | 36.45 | 17.33 | 2.67 |
| 17 | gpt-5.3-chat | 1716.2 | 16.21 | 7048 | 31.18 | 20.93 | 4.42 |
| 18 | moonshotai/Kimi-K2.6 | 1715.5 | 16.67 | 8333 | 38.16 | 13.30 | 3.77 |
| 19 | gpt-5.4-mini | 1683.7 | 16.51 | 10365 | 34.53 | 14.45 | 3.23 |
| 20 | moonshotai/Kimi-K2-Instruct | 1679.3 | 16.40 | 7308 | 31.98 | 15.51 | 3.40 |
| 21 | openrouter/pony-alpha | 1672.0 | 16.27 | 6605 | 32.65 | 17.76 | 3.72 |
| 22 | openrouter/horizon-beta | 1659.9 | 16.66 | 14202 | 27.71 | 11.19 | 2.22 |
| 23 | moonshotai/Kimi-K2-Thinking | 1659.5 | 16.47 | 7094 | 32.14 | 18.30 | 3.47 |
| 24 | grok-4.20-beta | 1640.9 | **14.51** | 7250 | 34.78 | 15.85 | 4.50 |
| 25 | gpt-5-2025-08-07 | 1640.7 | 16.79 | 14147 | 28.26 | 11.41 | 2.43 |

`*` prefix appears on gpt-5.6-*, claude-sonnet-5, GLM-5.2 — **meaning undocumented in the data
file; plausibly "recently added". Unverified.**

### THE KEY METHODOLOGICAL FINDING — Elo and rubric DISAGREE

- **gpt-5.5 has the HIGHEST rubric score of any model (17.01) but ranks only 4th on Elo (1954.1).**
- **gpt-5.6-sol ranks 1st on Elo (2208.0) with a LOWER rubric score (16.78).**
- **The rubric is compressed** — the top 25 span **16.14–17.01**, under one point — while **Elo
  spans 1640–2208**. The rubric has **almost no discriminative power** at the frontier; Elo does
  all the separating.
- **grok-4.20-beta is the exception that proves it**: rubric **14.51**, far below everything else,
  yet Elo **1640.9** — mid-pack. The two metrics are measuring different things.

**Implication for a companion-eval platform: do not build on absolute rubric scores.** They
saturate and compress at the frontier (this is the same failure that killed Creative Writing v2).
**Pairwise + Elo with fixed anchors is what still separates models in 2026.** Budget for pairwise.

### Length: verbosity is NOT buying rank here
`gpt-5.5` (12945) and `openrouter/horizon-beta` (14202) are the longest but rank 4th and 22nd;
`claude-fable-5` (5887) and `claude-opus-4-7` (5692) are half the length and rank 2nd and 3rd.
**Consistent with the 2026 finding that verbosity bias is small** (arXiv 2606.19544, <0.011) —
though note EQ-Bench actively controls for it via 4000-char truncation, so this is a
*controlled* result, not evidence that length doesn't matter uncontrolled.

### Note on Claude Fable 5
**Fable 5 ranks #2 by Elo (2156.3) and #1 by rubric (16.81), with the lowest slop score of the top
tier (10.28).** So it *is* genuinely excellent at creative writing. **This does NOT vindicate the
SEO claim that it's "Anthropic's purpose-built creative model"** — per Anthropic's own
announcement it is a Mythos-class *frontier capability* model (export-controlled for cybersecurity
risk), whose announcement never mentions creative writing. It's good at prose the way frontier
models are good at everything. See `news-model-releases-roleplay.md`.

---

## Judgemark v4 — the judge meta-eval

- **Judgemark tests the JUDGE, not the writer.**
- Method: give a candidate judge writing prompts, **anchor responses pre-scored at 2 and 9**, and
  blind test responses from writer models of varying ability.
- Scored on **score-distribution separability** via **omega-squared** and **Cliff's delta**.
- **v4** current (up from v2.1). Judgemark-v2 updated Feb 2026 (second-hand).

**Why it matters:** the Creative Writing v3 rubric compression above is exactly what Judgemark
measures — a judge that can't *spread* good and bad writers apart is useless regardless of its
human correlation. Pair this with arXiv 2606.19544's finding that **judge rankings move up to 14
positions across benchmarks**: you must meta-eval your judge **on your own task**.

## Longform Writing
- Separate leaderboard: https://eqbench.com/creative_writing_longform.html.
- Judge reportedly also upgraded to Sonnet 4.6 — **second-hand; the about page has no longform
  methodology section.** Repo `EQ-bench/longform-writing-bench` last updated ~Oct 2025 (second-hand).
- **Not extracted.**

---

## What this CHANGES vs 2024-era assumptions

- **The judge is a versioned, swappable dependency.** Sonnet 4 → Sonnet 4.6 on **2026-03-01** for
  Creative Writing Elo; EQ-Bench 3 judges with Opus 4.6. **Scores across that boundary are not
  comparable.** Pin and record judge model + version with every score you store.
- **Rubrics saturate; Elo survives.** v2 died of saturation; v3's rubric is already compressed into
  a <1-point band at the frontier while Elo spans ~570 points.
- **Anchoring is the field's answer to drift** — Judgemark's 2-and-9 anchors, EQ-Bench 3's
  o3=1500 / llama-3.2-1b=200. Fixed anchors let you compare across time. Adopt this.

## UNVERIFIED

- **EQ-Bench 3 has no Elo column in the data file I retrieved** — model order is assumed rank order
  but unconfirmed. **No EQ-Bench 3 Elo scores are cited anywhere in these notes.**
- **Scale and polarity of the EQ-Bench 3 radar values** (assumed /20, unconfirmed). The
  Claude-warm / Gemini-validating pattern is a **hypothesis from 7 hand-picked models**, not a
  verified finding.
- Meaning of the `*` prefix on the Creative Writing leaderboard.
- Whether `creative_writing_score` (rubric) and `elo_score` were produced by the same judge version
  — about.html implies **NOT** (rubric = claude-sonnet-4; Elo = Sonnet 4.6). **If so, the
  rubric/Elo divergence above is partly a judge-version artifact and not purely a metric-design
  finding.** This is a significant confound and I could not resolve it.
- Definitions of `slop_score`, `vocab_complexity`, `repetition_score` (only glossed on the site).
- Longform Writing leaderboard entirely.
- Judgemark v4 release date and its actual results (no judge scores retrieved).
