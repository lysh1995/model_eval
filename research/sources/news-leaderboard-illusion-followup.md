---
title: "The Leaderboard Illusion (arXiv 2504.20879) and LMArena/Arena's response — status as of July 2026"
url: https://arxiv.org/abs/2504.20879
publisher: Cohere Labs / AI2 / Princeton / Stanford / Waterloo / UW (paper); Arena (response)
date: paper v1 2025-04-29, v2 2025-05-12; Arena response ~2025-04/05 (undated page)
type: paper
accessed: 2026-07-16
topic: recent-news
---

# The Leaderboard Illusion — where it actually stands, 14 months on

## The paper — precise bibliographic status (verified on arXiv abs page)

- **arXiv 2504.20879**. **v1: 2025-04-29**. **v2 (last revised): 2025-05-12**.
- **68 pages, 18 figures, 9 tables** (arXiv comments field).
- **No venue listed in the arXiv comments field as of 2026-07-16.** An OpenReview forum exists
  (`openreview.net/forum?id=4Ae8edNqm0`) but the page is behind a bot check and **I could not
  verify the venue or decision status.** Treat it as a preprint.
- **There is no v3.** The paper has not been revised since 2025-05-12 — i.e. it has **not** been
  updated to reflect any of Arena's subsequent changes.

## The paper's claims (as reported; the PDF itself was not text-extracted)

1. **Undisclosed private testing** lets a few providers test many variants pre-release and retract
   scores, producing biased scores via **selective disclosure**. Headline example:
   **27 private LLM variants tested by Meta** ahead of Llama-4.
2. **Data access asymmetry**: **Google ~19.2%** and **OpenAI ~20.4%** of all Arena data each,
   while **83 open-weight models combined got ~29.7%**.
3. Proprietary models are sampled at higher rates and deprecated less often than open models.
4. Claimed performance gains of **up to 112%** from overfitting to Arena-specific dynamics.

## Arena's response — the rebuttal (https://arena.ai/blog/our-response/)

**The response page carries no explicit publication date**; it references stats "published
2025/4/27", so it is contemporaneous with the paper (late Apr / early May 2025).

Specific rebuttals with counter-numbers:

- **Open-model share**: paper says open source = **8.8%** of the leaderboard; Arena says official
  stats show **Open Models at 40.9%**, and that the paper's calculation **omitted open-weight
  models like Llama and Gemma**. (This is a definitional dispute — "open source" vs "open weight" —
  and both sides are arguably measuring different things.)
- **Pre-release testing boost**: paper implies **100+ Elo points**; Arena says the real effect is
  **"around +11 Elo after 50 tests and 3000 votes"**, diminishing with fresh data. Arena further
  argues the paper's headline plot **"is a simulation using Gaussians with an arbitrarily chosen
  variance"** and that "the numbers in the original plot are unrelated to Chatbot Arena."
  **If true, this is a serious methodological objection and the 112% / 100+ point figures should
  not be cited as empirical Arena measurements.**
- **Identical-checkpoint variation**: disputed scores **1069 (±27) vs 1054 (±18/22)** — Arena says
  these differences sit **within expected confidence intervals**.
- **Pointed counter**: Arena states **Cohere received 9 pre-release model evaluations
  (Jan 2025–present), "2-3x more pre-release tests than labs like xAI/OpenAI."** Cohere Labs is the
  lead author institution. Read this as adversarial framing, not neutral evidence — but it does
  undercut the "only big labs get private testing" narrative.

## Arena's committed changes — and whether they SHIPPED (cross-checked against the changelog)

| Commitment in the response | Shipped? | Evidence |
|---|---|---|
| Explicitly allow all providers to test multiple variants pre-release | Policy stated | Response page; no changelog entry |
| Increase clarity on model retirement; mark retired models explicitly | **Not verified** | No changelog entry found |
| Mark scores **"provisional"** until 2,000 additional fresh votes post-release (when 10+ models tested in parallel) | **YES — shipped** | Changelog **2025-09-18**: "preliminary" tag for anonymously-tested models later released publicly, "scores pending stabilization post-launch" |

So: **one of three commitments is verifiably shipped**, ~4.5 months after the response.
The naming drifted from "provisional" to **"preliminary"**, and I could not verify that the
2,000-fresh-votes threshold is the actual implemented rule.

## What Arena did NOT address, and what changed anyway

- **Not addressed**: the sampling-rate disparity and the deprecation-rate disparity. No changelog
  entry rebalances data allocation between proprietary and open models.
- **Changed anyway (bigger deal than the response)**: the **2026-05-12 "Battles in Direct"** update
  added **`is_direct_battle` and `same_org_indicator` features to the Bradley-Terry model**, and
  explicitly corrects **position bias favoring Model A** and **same-organization bias**.
  This is Arena conceding — in code, not in prose — that its ranking model needed bias covariates.
  See `news-lmarena-arena-ai-changelog.md`.
- **Rebrand**: LMArena → **Arena**; `news.lmarena.ai` 301s to `arena.ai/blog`.

## Bottom line for a companion-eval platform

- The **substance of the critique survives** (selective disclosure, unequal sampling), but the
  **headline numbers (112%, 100+ Elo) are contested by Arena as simulation artifacts** and should
  **not** be quoted as measured Arena effects. Anyone citing "the Arena gives a 112% boost" is
  citing a disputed simulation.
- The durable, uncontested lesson: **a leaderboard whose ranking model ignores position bias,
  same-org bias, and selective submission produces biased ranks.** Arena now models the first two.
  Selective submission is still handled by a *label* ("preliminary"), not by the statistics.
- **Design implication**: if you build a companion leaderboard with pairwise voting, you must
  (a) randomize and model position, (b) fix a submission policy and publish it, (c) publish
  per-model vote counts and CIs, and (d) have a stated retirement policy. Arena spent 14 months
  learning this in public.

## UNVERIFIED

- Venue / peer-review status of 2504.20879 (OpenReview bot-blocked).
- The paper's internal numbers — I read them via search summaries and Arena's rebuttal, **not**
  from the PDF. The 27-Meta-variants, 19.2%/20.4%/29.7% figures are second-hand here.
- Arena's response page publication date (undated).
- Whether the "2,000 fresh votes" rule is what shipped as the "preliminary" tag.
- Whether Arena ever published a *later* (2026) statement on the paper.
