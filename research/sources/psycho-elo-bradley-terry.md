---
title: "Elo, Bradley-Terry, TrueSkill: assumptions and failure modes"
url: https://arxiv.org/html/2502.10985v1
authors: "Is Elo Rating Reliable? A Study Under Model Misspecification"; Bertrand et al. "Elo Ratings in the Presence of Intransitivity" (2412.14427); Balduzzi et al. "Re-evaluating Evaluation" (2019)
year: 2025
type: paper (compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Ranking and aggregation models: Elo, Bradley-Terry, TrueSkill

Sources compiled:
- "Is Elo Rating Reliable? A Study Under Model Misspecification" — https://arxiv.org/html/2502.10985v1
- "Elo Ratings in the Presence of Intransitivity" — https://arxiv.org/abs/2412.14427
- "The impact of intransitivity on the Elo rating system", PLOS ONE — https://pmc.ncbi.nlm.nih.gov/articles/PMC12742789/
- Balduzzi et al., "Re-evaluating Evaluation", NeurIPS 2019
- Elo vs Bradley-Terry practical comparison — https://hippocampus-garden.com/elo_vs_bt/

## Bradley-Terry

Probability model for pairwise comparison:
```
P(i beats j) = exp(β_i) / (exp(β_i) + exp(β_j)) = σ(β_i − β_j)
```
Fit by maximum likelihood over all observed comparisons. **Static** — it fits one strength parameter
per model over the whole dataset.

## Elo

An **online / incremental** update rule:
```
R_i ← R_i + K · (S_ij − E_ij)
E_ij = 1 / (1 + 10^((R_j − R_i)/400))
```
"Elo rating is usually interpreted as an **incremental update algorithm for estimating an underlying
stationary Bradley-Terry model**, though in practice, model assumptions may be violated."

Critical consequence: **Elo is order-dependent.** Shuffle the match history, get different ratings.
BT is not order-dependent. For a static pool of LLM variants where all comparisons are available at
once, **BT (fit by MLE) is strictly the better choice than Elo** — Elo's incrementality is a feature
for chess (where players genuinely change over time) and a bug for us.

## TrueSkill

Bayesian, models each player's skill as a Gaussian `N(μ, σ²)` and updates by message passing.
Advantages over Elo: handles multiplayer/teams, gives **explicit uncertainty** (`σ`), converges
faster. Assumes transitivity like BT.

## Failure modes

### 1. Intransitivity
The big one. Rock-paper-scissors preferences (A>B, B>C, C>A) genuinely occur among LLMs because
quality is **multi-dimensional** — model A wins on warmth, B on coherence, C on creativity, and
pairwise judges weight them differently per matchup.

"Once the assumption of transitivity is relaxed, Elo ratings exhibit the undesirable property that
**estimated ratings are dependent on who plays who**."

So under intransitivity your rating depends on the **schedule**, not just on quality. A scalar rating
is a lossy projection of an inherently non-transitive relation. Balduzzi et al. ("Re-evaluating
Evaluation") make this argument formally and propose Nash-averaging as an alternative.

**Actionable**: "**preference cycles should be monitored as indicators of diverse model
specializations**" — count 3-cycles in the empirical preference graph. A high cycle rate means the
scalar leaderboard is hiding a real trade-off and should be replaced by per-dimension reporting.

### 2. Non-stationarity
Judges drift (model updates), the scenario pool changes, raters learn. BT assumes one fixed strength
per model for all time. Ratings from different eras are not comparable.

### 3. Model misspecification / judge systematic error
"LLM-as-a-judge offers systematic errors — such as **position bias, self-preference, or
intransitivity** — that can strongly **miscalibrate the resulting rankings**."

### 4. Best-of-N selection bias
See `psycho-leaderboard-illusion.md`. Violates the unbiased-sampling assumption, inflates ratings of
whoever submits the most variants.

## Uncertainty quantification

"**Bootstrap resampling** gives a more reliable variance estimate, especially when the Bradley-Terry
assumptions are violated (e.g. due to intransitive preferences or context effects)." This is what
Chatbot Arena itself does — bootstrap the comparison set, refit BT, take percentiles.

Scale reality check: "**rating differences smaller than 30 Elo points typically require hundreds of
comparisons to validate**."

Refinement worth adopting: propagate **calibrated win probabilities rather than hard labels** into
the BT fit, estimating per-battle uncertainty from the judge's own score differences. A 5-vs-4.9
judgment should not count the same as 5-vs-1.

## Relevance to companion-eval

- Use **BT with bootstrap CIs**, not Elo — our comparisons are batch, not streaming.
- **Report CIs, never bare ranks.** Ranks without CIs are the single biggest source of false
  confidence in a leaderboard.
- **Monitor 3-cycles.** If cycles are common in a dimension, that dimension should not have a scalar
  leaderboard.
- Pairwise BT and absolute rubric scoring answer **different questions**. BT gives relative ranking
  only and cannot answer "did we regress vs last release" across a changing pool. Our "SAME
  BASELINE" requirement points to **anchored absolute rubric scores** as the primary metric, with BT
  as a secondary cross-check.
