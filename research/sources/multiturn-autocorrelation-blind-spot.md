---
title: "The Autocorrelation Blind Spot: Why 42% of Turn-Level Findings in LLM Conversation Analysis May Be Spurious"
url: https://arxiv.org/abs/2604.14414
authors: Ferdinand M. Schessl
year: 2026
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# The Autocorrelation Blind Spot

arXiv:2604.14414v1.

**Status: a statistical-validity warning that directly constrains our platform's analysis layer. Read before writing any significance test over turns.**

## Core claim

Turn-level analyses **violate the independence assumption** in statistical testing. The **42%** figure is the estimated proportion of statistically significant turn-level findings that may be **false positives** when autocorrelation among conversational turns is not accounted for.

## The statistical problem

**Non-independence of turns:**
> Consecutive turns in conversations are not independent observations. A user's response depends on the prior AI response, and vice versa. This creates autocorrelated data structures that invalidate standard regression and significance tests.

**Pseudo-replication:**
> Researchers often treat each turn as an independent data point, effectively inflating sample size and artificially reducing standard errors. This leads to spuriously significant results.

**This is the sharpest possible statement of the unit-of-analysis problem, and it cuts against a naive version of our own thesis.** It is not enough to say "look across turns." If we pool 100 turns × 3 runs × 11 models × 95 characters and treat n = 313,500, our standard errors will be wrong by a large factor and we will ship confident nonsense. The effective n is closer to **95 characters × 11 models**, or at best the number of *conversations* (95 × 3 × 11 = 3,135), not the number of turns.

## Detection methodology

1. **Intraclass Correlation Coefficient (ICC)** — measures degree of autocorrelation within conversations
2. **Bootstrap methods** — resampling that accounts for dependency structures
3. **Effect size calculations** — adjusts effect estimates downward when autocorrelation is considered

## Recommended corrections

- **Mixed-effects models:** random intercepts/slopes **by conversation** to account for within-conversation dependencies
- **Cluster-robust standard errors:** cluster at the **conversation level**, not the turn level
- **Unit of analysis:** the appropriate unit should be the **conversation (dialogue session), not individual turns**, for hypothesis testing about effect sizes

Also references **Benjamini-Hochberg FDR control** and adjustments following **Chelton (1983)** and **Politis (1994)** for autocorrelated data in scientific inference.

## Relevance to companion-eval-platform

- **The conversation is the sampling unit; the turn is a repeated measure within it.** This is a stronger and more precise version of our project thesis, and it comes with a statistical obligation, not just an architectural one.
- Our nesting structure is deep: **turn ⊂ run ⊂ (character × model × language)**. Mixed-effects with random intercepts for character and for conversation is the minimum defensible analysis. Character is a random effect, not a fixed one — we care about generalizing to *unseen characters*, and 95 is a sample from a population.
- **Compute and report ICC per metric.** A metric with high within-conversation ICC (drift, repetition — almost certainly high) carries far less independent information per turn than its raw n suggests. This should be surfaced in the platform, not buried.
- Practical consequence for the product: **do not let the UI report per-turn n as if it were sample size.** Any confidence interval we show on a turn-pooled metric is a lie unless it is cluster-robust.
- Interacts with the survival framing: survival analysis handles this naturally, since each conversation contributes exactly ONE event time — one observation per conversation, independence restored.
