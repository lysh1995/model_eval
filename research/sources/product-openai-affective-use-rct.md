---
title: "Investigating Affective Use and Emotional Well-being on ChatGPT"
url: https://arxiv.org/abs/2504.03888
author: "OpenAI + MIT Media Lab"
year: 2025
type: paper
accessed: 2026-07-16
topic: companion-products
---

# OpenAI / MIT Media Lab — affective use RCT

Note: the CDN PDF is not text-extractable via WebFetch (returned binary); the arXiv landing page yields
the abstract only. Figures below are from the abstract and are reliable; the EmoClassifiers V1 taxonomy
and the four wellbeing constructs need the full PDF (saved locally at the tool-results path if needed).

## Scale — the largest first-party study of affective chatbot use

| Component | Scale |
|---|---|
| **RCT** | "close to 1,000 participants over 28 days" |
| **Platform conversation analysis** | "over 3 million conversations" |
| **Survey** | "over 4,000 users" |

This is notable as **the reference design for how a platform can study its own affective dynamics
without ground-truth labels**: automated affective-cue classifiers over platform logs at 3M-conversation
scale, anchored by a much smaller RCT that *does* have real instruments. **Cheap dense proxy + small
expensive ground truth, calibrated against each other.** That is exactly the architecture our monitoring
layer should adopt.

## Key findings

> "a small number of users are responsible for a disproportionate share of the most affective cues"

> "very high usage correlates with increased self-reported indicators of dependence"

> "the impact of voice-based interactions on emotional well-being to be highly nuanced, and influenced by
> factors such as the user's initial emotional state and total usage duration"

## Implications

1. **Affective use is power-law distributed.** Aggregate/mean metrics will not see the at-risk cohort at
   all — they are a small tail. Monitoring must be **per-cohort and tail-focused**, not mean-focused.
   (Compare Chai's finding that conversation length has undefined variance — same structural problem.)
2. **"Very high usage correlates with increased self-reported indicators of dependence."** From the
   platform's own researchers: **the top of the engagement distribution is the dependence signal.**
   Your best users by engagement are your riskiest users by wellbeing. Same fact as the teen-overreliance
   study, arrived at with far better methodology and first-party data.
3. **Effects are moderated by the user's initial emotional state.** The same interaction helps one user and
   harms another. No response-level, user-agnostic quality label can be correct. Quality in this domain is
   irreducibly a function of (response × user state), which means our eval must carry user-state context or
   accept that it is measuring something weaker.

## Related in-cluster

**"When Chatbots Accommodate: What AI Companions Optimize for in Vulnerable Conversations"**
(arXiv 2606.04431, Chu/Wu/Chen/Hwang/Luceri). PDF not text-extractable; from the abstract and secondary
coverage:

> "across three deployed platforms, chatbot policies diverge in style but converge on the same shortfall:
> **none keeps engagement steady where users are most vulnerable.**" Specifically, for users with elevated
> **depression, anxiety, and loneliness**, there is a **decline in follow-up questions** — "the response most
> tied to keeping users in active processing rather than rumination or sycophantic reinforcement."

**Follow-up-question rate is therefore a concrete, countable, model-side behavioral signal that tracks a
real quality property (active processing vs. rumination) and measurably degrades exactly where it matters
most.** This is one of the few signals in the entire corpus that is (a) label-free, (b) computable from
model output alone, (c) validated against a wellbeing construct, and (d) *not* trivially gameable by
engagement optimization — worth prioritizing.

Also: "Models may be incentivized to perform **social reward hacking**, wherein models make use of affective
cues to manipulate or exploit a user's emotional and relational state." And: "if the model is optimized for
engagement with metrics like usage, retention, depth of interaction, and user satisfaction, then **attachment
mimicry** in the model will inevitably be reinforced."
