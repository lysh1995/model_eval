---
title: "The Leaderboard Illusion"
url: https://arxiv.org/abs/2504.20879
authors: Shivalika Singh, Yiyang Nan, Alex Wang, Daniel D'Souza, Sayash Kapoor, Ahmet Üstün, Sanmi Koyejo, Yuntian Deng, Shayne Longpre, Noah A. Smith, Beyza Ermis, Marzieh Fadaee, Sara Hooker (et al.)
year: 2025
type: paper
accessed: 2026-07-16
topic: psychometrics
---

# The Leaderboard Illusion

Critique of Chatbot Arena / LMArena's statistical methodology. Central point: the Bradley-Terry
model is *theoretically* sound, but the **data-generating process violates its assumptions**, so the
resulting rankings are distorted.

## Best-of-N / selective disclosure bias

When a provider tests multiple **private variants** and publishes only the best-performing one
based on observed results, this violates BT's assumption of **unbiased sampling**, alters the
likelihood landscape, and causes the BT estimator to **systematically inflate** the ratings of
models submitted under a best-of-N strategy.

Concrete: Meta tested **27 private LLM variants** ahead of the Llama-4 release.

## Sampling rate asymmetry

- "Google and OpenAI have received an estimated 19.2% and 20.4% of all data on the arena,
  respectively"
- "a combined 83 open-weight models have only received an estimated 29.7%"

## Deprecation

205 models silently deprecated by reducing active sampling rates to near zero. **87.8% of open
weights** and **89% of open-source** models deprecated. Proprietary closed models face lower removal
rates.

## Data access → performance

"limited additional data can result in relative performance gains of up to **112%** on the arena
distribution" — i.e. access disparities translate directly into leaderboard position, so the
leaderboard partly measures *access*, not *quality*.

## Recommendations

Transparency in testing practices, equitable data distribution across models, clearer disclosure
policies, and limits on the number of private variants.

## Relevance to companion-eval

If we adopt pairwise/BT or Elo scoring internally, we will reproduce exactly this bug: teams will
iterate on variants and submit their best. Mitigations for us:
1. **Pre-register** which variant is the candidate before seeing arena results.
2. **Equal sampling** across variants by construction (we control the sampler — no excuse).
3. Never silently drop a variant; deprecation changes the comparison graph and shifts all ratings.
4. Report BT confidence intervals, not just point ranks.
