---
title: "Does style matter? Disentangling style and substance in Chatbot Arena"
url: https://www.lmsys.org/blog/2024-08-28-style-control/
authors:
  - Tianle Li
  - Anastasios Angelopoulos
  - Wei-Lin Chiang
  - LMSYS / LMArena team
year: 2024
type: blog / methodology writeup
accessed: 2026-07-16
topic: llm-judge
---

# Does style matter? Disentangling style and substance in Chatbot Arena (Style Control)

## Summary

LMArena's response to the criticism that Chatbot Arena rankings reward verbose, heavily-formatted answers rather than better ones. The fix — **Style Control** — adds style features as *independent variables* in the Bradley-Terry regression, so the model coefficient estimates quality **conditional on style** rather than confounded with it.

Note this measures bias in **human** voters, not an LLM judge. That is precisely why it matters for us: it proves the length/formatting confound is not an LLM artifact that a better judge will fix. It is present in the human preference signal that judges are trained and validated against. **A judge perfectly aligned to human preference would inherit this bias.**

## Methodology

Style features controlled for:

1. Answer token length
2. Markdown header count
3. Markdown bold element count
4. Markdown list element count

**Normalization:** each style feature is normalized as

```
normalize( (featureA - featureB) / (featureA + featureB) )
```

making the difference proportional to the baseline magnitude rather than absolute. These become additional regressors in the BT model alongside the model-identity indicators.

The key statistical idea: BT with style covariates estimates each model's strength **holding style constant** — a deconfounding regression, not a filter or a penalty.

## Key numbers — style coefficients

| Feature | Control Both | Control Markdown Only | Control Length Only |
|---------|-------------|----------------------|-------------------|
| **Length** | **0.249** | — | 0.267 |
| Markdown List | 0.031 | 0.111 | — |
| Markdown Header | 0.024 | 0.044 | — |
| Markdown Bold | 0.019 | 0.056 | — |

> "Length is the dominant style factor. All other markdown effects are second order."

Length's coefficient (0.249) is **~8x** the largest markdown coefficient (list, 0.031) when both are controlled. Note also that markdown coefficients *inflate* (0.031 → 0.111) when length is not controlled — markdown correlates with length, so uncontrolled markdown effects are largely length in disguise.

## Key numbers — ranking changes after style control

**Overall rankings (before → after controlling for both length and markdown):**

| Model | Before | After |
|---|---|---|
| GPT-4o-mini | 6 | **11** |
| Grok-2-mini | 6 | **18** |
| Claude 3.5 Sonnet | 6 | **4** |
| Llama-3.1-405B | 6 | 6 |

**Hard prompts:**

| Model | Before | After |
|---|---|---|
| Claude 3.5 Sonnet | 2 | **1** (ties for #1) |
| Llama-3.1-405B | 4 | 3 |

**Grok-2-mini moves 12 ranks (6 → 18) purely from removing the style confound.** This is the headline number: on an uncontrolled leaderboard, a model can sit 12 positions above its style-adjusted position. If our platform ranks variants without style control, a variant that merely tuned its system prompt toward longer, listier output would climb the board without any improvement in character fidelity.

## Implications for our platform

- **Style control is not optional for cross-model comparability.** Different base models have very different default verbosity and formatting habits; that difference alone will dominate our leaderboard unless regressed out.
- The **BT-with-covariates** approach is directly portable: our variant scores should be fit as a BT model over pairwise judgments with length/formatting covariates included.
- For roleplay/companion specifically, we should consider extending the covariate set beyond length/markdown — e.g. dialogue-vs-narration ratio, emoji/asterisk-action density, average turn length. These are style choices in companion output that a judge will confound with quality.
- **Caution:** style control removes style from the *score*, it does not stop the judge from *seeing* style. It corrects the aggregate estimate, not the individual judgment. And if style genuinely correlates with quality on a dimension (e.g. "storytelling" plausibly *should* reward vivid longer prose), controlling for length may over-correct and remove real signal. The covariate set must be chosen per-dimension, deliberately.
