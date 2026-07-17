---
title: "When Attention Closes: How LLMs Lose the Thread in Multi-Turn Interaction"
url: https://arxiv.org/abs/2605.12922
authors: Vardhan Dongre, Joseph Hsieh, Viet Dac Lai, Seunghyun Yoon, Trung Bui, Dilek Hakkani-Tür
year: 2026
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# When Attention Closes: How LLMs Lose the Thread in Multi-Turn Interaction

arXiv:2605.12922v1. 34 pages with appendices A–I.

**Status: partial extraction — the PDF is 8.5MB and the detailed per-turn tables did not extract cleanly. Flagged for manual follow-up. The headline structural claim is captured and is directly relevant to our "position of failure" question.**

## Abstract

Investigates performance degradation in LLMs during multi-turn conversations, examining how **attention mechanisms** contribute to context loss.

## Key finding on the SHAPE of degradation

> Performance does **not** degrade uniformly across conversation turns. The degradation curve exhibits **non-linear behavior rather than a monotonic decline**, suggesting specific architectural vulnerabilities at certain interaction stages.

**This is the direct answer to our "does quality degrade monotonically with turn index?" question: NO.** It converges with:
- Multi-IF's IFR (turn 1→2 drop > turn 2→3 drop — decelerating, not linear)
- Time-To-Inconsistency's PH violation (hazard is non-constant over turns)
- Laban et al.'s "loss-of-middle-turns" (middle turns specifically neglected)
- Lost-in-the-Middle's U-shape (positional, not monotone)

**Four independent literatures agree that turn-index effects are non-monotone.** Any platform that models drift as a linear function of turn index — or that reports a single "degradation slope" — is fitting the wrong functional form.

## Attention findings

Analyzes how attention patterns shift across turns: the model's ability to **attend to earlier context diminishes**, examining which **attention heads and layers** show the most significant drift from optimal allocation patterns.

Converges with the Persona Drift paper's π(t) attention-decay analysis — same mechanism, independently observed.

## Methodology

Combines **probing techniques** (citing Alain & Bengio; Belinkov & Finkelstein) with architectural analysis to isolate when and why contextual coherence fails in extended dialogues.

## Extraction caveat

Specific numerical thresholds for performance loss by turn index are embedded in tables/figures across the appendices and were not recoverable via automated extraction. **The qualitative claim (non-monotone degradation) is solid; the exact curve shape needs a manual read of the appendices before we cite any number from this paper.**

## Relevance to companion-eval-platform

- **Do not assume monotone decay.** Instrument turn index as a non-parametric / spline term or as binned strata, not a linear covariate.
- Supports probing *at multiple depths* rather than only endpoint comparison — if the curve is non-monotone, endpoint-only measurement (turn 1 vs turn 100) can miss a mid-conversation trough entirely.
- Mechanistically consistent with attention decay ⇒ expect the effect in all 11 models, differing in rate.
