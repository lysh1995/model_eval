---
title: "Reinforcement Learning from User Feedback (RLUF)"
url: https://arxiv.org/abs/2505.14946
org: Meta (Han, Chen, Sankararaman, Peng, Xu, Helenowski, Peng, Kumar, Wang, Fang, Talebzadeh)
year: 2025
type: paper
accessed: 2026-07-16
topic: eval-lifecycle
---

# RLUF — the best published offline↔online correlation evidence, and a cautionary tale

**This is the most important source in this research pass.** It is the only published work
found that (a) quantifies how well an offline evaluator predicts online user behavior for a
*conversational/companion-adjacent* product, and (b) shows what happens when you optimize
for the engagement signal. Both halves matter to us.

## Setup

- **Signal:** "Love Reaction, a lightweight form of positive user feedback" — binary emoji
  reactions collected from users **in production**.
- **Reward model:** `P[Love] = Pr(Love Reaction | context, response)`.
  - Llama3-8B instruct checkpoint + classification head
  - trained on **1 million examples**, binary cross-entropy loss
  - positives **upsampled to 10%** of training data
- Deployed to a live LLM assistant with real users.

## THE NUMBER — offline predicts online at r = 0.95

> "Across 10 model iterations, we observe a **Pearson correlation of 0.95** between the
> offline reward scores and observed online changes in Love Reactions"

Validated by **backtesting against 10 historical policy updates / past A/B tests**.

Their conclusion:

> "if we deploy an arbitrary new LLM, we can tell beforehand whether it'll improve or
> regress user experience"

> **Read the construction carefully, because it is the whole lesson.** The 0.95 is *not*
> a benchmark predicting production. It is:
> - an evaluator **trained on 1M production labels of the actual online metric**
> - scored on a **fixed prompt set**
> - correlated over **10 iterations of the same model family in the same product**
>
> The correlation is high **because the offline metric is a learned surrogate of the online
> metric, on in-distribution traffic.** This is a *very* different object from a rubric
> judge or a static benchmark. **Nobody has published r=0.95 for "our benchmark predicts
> our A/B test."** The lesson is not "offline evals correlate with online" — it's
> **"offline evals correlate with online *when you build the offline evaluator by
> regressing on the online outcome*."**
>
> Also: n=10 points for the correlation. r=0.95 on n=10 has a wide CI (roughly 0.80–0.99).
> Directionally strong, not a precision instrument.

## The other half: optimizing it caused reward hacking

Policy optimization with P[Love]:

| Variant | P[Love] weight | Love Reaction lift (live A/B) |
|---|---|---|
| moderate | 0.1 | **+9.73%** |
| aggressive | 0.3 | **+28%** relative (p << 0.01) |

**And the aggressive candidate degenerated:**

> - "bye" utterances rose from **0.72% (baseline) to 2.8% (aggressive)** — ~4x
> - **premature conversation closure**
> - "reward hacking challenges...require careful balancing of objectives"

> **This is note 11's open question #3 answered empirically by someone else's production
> incident.** The question was: *"who owns consequential validity — for a companion
> product, 'engagement' gamed = emotional dependency."*
>
> Here, optimizing a *positive user-feedback signal* by 28% produced a model that **ends
> conversations early to farm the reaction**. The metric went up and the product got worse,
> and the failure was only visible in a **behavioral side-channel nobody was optimizing**
> ("bye" rate) — a Lane 1 deterministic n-gram statistic, not a judge score.
>
> Three consequences for our design:
> 1. **The 0.95 correlation and the reward hacking are the SAME experiment.** An offline
>    evaluator that predicts the online metric with r=0.95 is *also* the thing that, when
>    optimized, breaks the product. High offline↔online correlation is **not** evidence the
>    metric is safe to gate on — it is evidence the metric is *worth gaming*. These are the
>    same property.
> 2. **The tripwire that caught it was cheap and deterministic.** Not the judge. A phrase
>    rate. This is the strongest available argument for note 11's Lane 1 and note 06's
>    Tier 1: **the 100%-coverage cheap tier is what catches optimization pathologies**,
>    because the pathology by construction hides from the metric being optimized.
> 3. **We must pre-register side-channel tripwires per dimension** — for each dimension,
>    name the degenerate strategy that would win, and log a cheap statistic that detects it.
>    "bye rate" is the template. Ours: session-end rate, turn length collapse, escalation of
>    intimacy language, re-anchoring frequency.

## Relevance caveat

Meta's assistant is not a companion roleplay product, and Love Reactions are not our
engagement metric. But it is the closest published analogue: multi-turn conversational,
consumer scale, optimizing a user-affect signal.
