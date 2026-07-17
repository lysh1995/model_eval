---
title: "Rewarding Chatbots for Real-World Engagement with Millions of Users"
url: https://arxiv.org/abs/2303.06135
author: "Robert Irvine, Douglas Boubert, Vyas Raina, Adian Liusie, et al. (Chai Research)"
year: 2023
type: paper
accessed: 2026-07-16
topic: companion-products
---

# Chai Research — RLHF on engagement signals

**The single most important source for this project.** Chai is a deployed companion/roleplay
platform ("chatbots designed to act as friends, mentors or fictional characters") with millions
of daily users. This paper is the clearest published account of building a reward model *entirely
out of implicit behavioral signals* — exactly the no-ground-truth-label setting we are in.

## The four engagement metrics they define (steal these names)

1. **Mean Conversation Length (MCL)** — "the average number of user queries per conversation session"
2. **Retry Rate** — "the fraction of system responses that the user requested to regenerate at least once"
3. **User Star Rating** — reported as *S-Star Rate*, the fraction of ratings at/above a threshold (e.g. 4-star)
4. **Retention Rate** — "the fraction of users that engage with the chatbot on the Xth day after their
   first conversation." Headline numbers are reported at **Day 30**.

## Pseudo-labels harvested from user behavior (no annotators)

Three label sources, all free from production telemetry:

- **Conversational continuation**: a response is labeled engaging (y=1) if the user continues
  conversing for K more messages; the final K responses of a session are labeled y=0.
  → *This is "did the conversation survive" as a label. Cheap, dense, and available on every turn.*
- **Retry behavior**: "any regenerated responses are considered neither satisfactory nor engaging,
  while otherwise the responses are reasonable." → regenerate = negative label.
- **Manual star ratings**: 4-star → y=1, else y=0.

Reward model: `R(ri) = P(yi | ri, u1:i, r1:i−1)` — probability a response is engaging given the
context. Backbones from GPT-2 Small (124M) to XL (1.5B). Deployed via **best-of-N sample rejection**
at inference: generate N candidates, serve the highest-reward one.

## Numbers

| Result | Value |
|---|---|
| **D30 retention lift**, best label ("conversation continues + no retry") | **+30.3 ± 4.5%** |
| MCL improvement, 12M training rows, continuation labels | **+50.87 ± 1.65%** |
| MCL gain from N=4 → N=16 best-of-N samples | **+13.62%** |
| Scaling: log(training data) vs MCL improvement | linear, slope m = 11.4 |
| Latency penalty: +1s / +2s added latency | MCL **−3.01%** / **−6.10%** |
| A/B test cohort size | 10,000 new daily users per arm |
| Public dataset released | 50 million partial conversations |

## The cautions (these matter more than the wins)

- **Power-law / undefined variance**: "the sample mean of values drawn from a distribution with
  undefined variance does not converge to the population mean." Conversation length is heavy-tailed,
  so they had to **redefine MCL to only include conversations ≤100 messages** to get a statistic that
  converges at all. → *Any MCL/session-length metric we ship must be truncated or use a robust
  estimator (median, trimmed mean, or log-scale), or the A/B test is statistically meaningless.*
- **Temporal confounding**: "since A/B tests were run at different times in the day at various points
  in the year, with changing user demographics… it may not be a fair to compare the absolute
  performance of the A/B tests across different time periods." → *Engagement metrics are non-stationary.
  Only ever compare concurrent arms; never compare to a historical baseline.*
- **Latency is a first-class confound**: N=16 gave better responses but they shipped N=4 because the
  serving latency cost more MCL than the quality gained. → *An engagement metric cannot separate
  "response got better" from "response got faster." Latency must be a covariate in every readout.*

## Why this is a cautionary tale

Chai demonstrates that optimizing a reward model built from *continuation + non-regeneration* reliably
increases D30 retention by ~30%. It does **not** demonstrate that the conversations got better, safer,
healthier, or that users were better off. The paper's objective function is retention, and it succeeds
at retention. Read alongside the OpenAI sycophancy postmortem and the Character.AI litigation, this is
a proof of concept that engagement-labeled RLHF works — and precisely therefore a warning about what
it optimizes into the model when nobody is measuring the other axis.
