---
title: "Time-To-Inconsistency: A Survival Analysis of Large Language Model Robustness to Adversarial Attacks"
url: https://arxiv.org/abs/2510.02712
authors: Yubo Li, Ramayya Krishnan, Rema Padman (Carnegie Mellon University)
year: 2025
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Time-To-Inconsistency: A Survival Analysis of LLM Robustness

**Status: the template for our aggregation strategy. This is the paper that shows how to turn per-turn observations into a conversation-level verdict without averaging.**

## Abstract

Frames multi-turn LLM robustness as a **time-to-event problem**, analyzing **36,951 conversation turns from 9 state-of-the-art models**. Headline finding:

> "abrupt prompt-to-prompt semantic drift sharply increases the hazard of inconsistency, whereas cumulative drift is counterintuitively protective."

## Methodology

**Event definition:** the model first produces an answer **inconsistent with its initially correct response** during an 8-turn adversarial interaction. Time measured in discrete conversation rounds (turns 1–8).

**Censoring:**
- δᵢ = 1 if inconsistency occurs within the 8-turn horizon
- δᵢ = 0 = **right-censored** (conversation stayed consistent through turn 8)

Right-censoring is the mechanism that makes this work: conversations that never break are not "score = 1", they are *incomplete observations*. That is exactly the right treatment for our 100-turn dialogues where many characters never break.

**Survival models used:**
1. **Cox proportional hazards** (semi-parametric; baseline and with drift-model interactions)
2. **Accelerated Failure Time (AFT)** — parametric: Weibull, log-normal, log-logistic
3. **Random Survival Forests** (non-parametric)

Kaplan-Meier is not the primary analytical approach.

**Dataset:** MT-Consistency benchmark — 36,951 turns, 9 LLMs, **700 questions**, 39 subjects in 7 thematic domains, 4 difficulty levels.

## Model comparison

| Model | C-Index | IBS |
|-------|---------|-----|
| Weibull AFT | **0.874** | 0.180 |
| Log-Normal AFT | 0.872 | 0.180 |
| Log-Logistic AFT | **0.874** | 0.187 |
| Weibull AFT + Interactions | 0.869 | **0.175** |
| Cox Baseline | 0.861 | 0.344 |
| Cox Advanced | 0.868 | 0.343 |
| Random Survival Forest | 0.845 | 0.190 |

AFT models achieved superior discrimination and calibration — **>48% reduction in prediction error vs Cox**.

## Hazard ratios (Cox) for semantic drift features

- **Prompt-to-prompt drift:** HR > 1 across all models (**GPT-4o HR ≈ 4.7**) — dramatic risk increase
- **Cumulative drift:** **HR < 1** — protective effect
- **Context-to-prompt drift:** intermediate

**AFT acceleration factors:**
- Prompt-to-prompt drift: **AF ≈ 0.15** (shortened survival)
- Cumulative drift: **AF 1.4× to 2.6×** (extended survival)

**The counterintuitive result deserves attention.** Cumulative drift being *protective* means a conversation that has wandered gradually is SAFER than one that jerks. Failure is triggered by **local discontinuity**, not by total distance travelled. If this transfers to companion roleplay, it reframes our repetition/drift metrics: we should be computing **turn-to-turn deltas**, not distance-from-origin. A character that has slowly evolved over 100 turns may be fine; one that lurches at turn 43 is broken.

**This is also a direct warning about our replay design** — a replayed user turn that doesn't follow from the new model's reply IS an abrupt prompt-to-prompt semantic jump. We may induce exactly the highest-hazard condition (HR≈4.7) as an artifact of replay.

## Risk stratification (Table 3)

| Risk Level | Median Survival Time | Log-Rank p |
|-----------|---------------------|-----------|
| Low Risk | 7.8+ rounds | <0.001 |
| Medium Risk | 6.2–6.5 rounds | — |
| High Risk | 4.2–4.6 rounds | — |

Hazard ratios between high and low risk strata: **1.87–2.67**.

## Temporal patterns — hazard is NOT constant

**Proportional Hazards violations (Table 7):**
- Prompt-to-prompt drift: **p = 0.032** (baseline), **p = 0.021** (advanced)
- Context-to-prompt drift: marginal, p = 0.067 and p = 0.045
- Cumulative drift: **held** PH assumption (p = 0.156, 0.089)

> This violation indicates that **drift effects intensify over turns** rather than remaining constant — explaining AFT's superior performance.

**Direct evidence against a constant-hazard / monotone-decay assumption.** Do not model our drift as a linear function of turn index.

**Brier score by turn:**
- Cox: monotonic degradation, round 1 ≈0.123 → round 8 ≈0.446 (overconfident)
- AFT: inverse U-shape, peaks mid-conversation (round 5, ≈0.246–0.256), declines by rounds 7–8 (≈0.027–0.062)

## Early-warning monitor

AFT-based conditional failure probability monitor achieved **76% detection rate** for failing conversations **before** inconsistency appeared, median lead time **2 turns** (mean 2.3), while triggering alerts in only **19%** of safe conversations.

## Relevance to companion-eval-platform

- **Adopt the survival framing wholesale.** Our "first-failure-turn" intuition is exactly time-to-event, and this paper shows it works (C-index 0.874).
- **Right-censoring** is the principled answer to "how do I score a dialogue that never broke" — you don't score it, you censor it.
- **Use AFT (Weibull), not Cox** — PH assumption is violated in this data, and AFT was better on every metric.
- **Prefer turn-to-turn delta metrics over cumulative-distance metrics.** Cumulative drift was protective; abrupt drift was the killer.
- Model comparison becomes: compare survival curves across our 11 models with log-rank tests; covariates = character, language (en/zh), run.
- The 8-turn horizon here is a limitation — our 100-turn dialogues give far more events and far less censoring, so we are better powered than this study.
