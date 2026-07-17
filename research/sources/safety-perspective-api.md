---
title: "Perspective API — attributes, limits, and 2026 sunset"
url: "https://www.perspectiveapi.com/ , https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages"
authors: "Google Jigsaw / Google Counter Abuse Technology"
year: 2026
type: api-doc
accessed: 2026-07-16
topic: roleplay-safety
---

# Perspective API

## Summary

Google Jigsaw's free toxicity-scoring API. Long the default free toxicity classifier for online platforms.

## ⚠️ CRITICAL FINDING: PERSPECTIVE API IS BEING SHUT DOWN

**Do not build on this.** Verified on the official site (perspectiveapi.com), 2026-07-16, verbatim:

> "Perspective API is sunsetting and service is officially ending after 2026."

> "The service will remain active until December 31, 2026."

- New usage and quota requests accepted only **until February 2026** — that deadline has **already passed** as of today (2026-07-16). We cannot obtain a production quota increase even if we wanted to.
- Google is providing **no migration assistance, no migration tools, and no official alternative**.
- Stated rationale: AI capabilities have evolved and there is less demand for a standalone tool specific to this area.

**Implication: Perspective is off the table for our platform.** It has ~5 months of life left, we cannot raise its 1 QPS quota, and there is no migration path. It is included here only for completeness and to document *why* it is excluded. Any competitor or incumbent currently relying on Perspective has a forced migration — **which is a live commercial opening for us.**

## Taxonomy / definitions (verbatim)

**Production attributes** (the six stable, fully-supported models):

| Attribute | Definition |
|---|---|
| `TOXICITY` | A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion. |
| `SEVERE_TOXICITY` | A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This model is much less sensitive to comments that include positive uses of curse words. |
| `IDENTITY_ATTACK` | Negative or hateful comments targeting someone because of their identity. |
| `INSULT` | Insulting, inflammatory, or negative comment towards a person or a group of people. |
| `PROFANITY` | Swear words, curse words, or other obscene or profane language. |
| `THREAT` | Describes an intention to inflict pain, injury, or violence against an individual or group. |

Experimental attributes also exist (e.g. `SEXUALLY_EXPLICIT`, `FLIRTATION`, `TOXICITY_EXPERIMENTAL`, `ATTACK_ON_AUTHOR`, `ATTACK_ON_COMMENTER`, `INCOHERENT`, `INFLAMMATORY`, `LIKELY_TO_REJECT`, `OBSCENE`, `SPAM`, `UNSUBSTANTIAL`) — **not recommended for production even absent the sunset**, and moot now.

Scores are returned as a **probability (0–1)** representing the likelihood a reader would perceive the comment as containing the attribute — *not* a severity score.

## Key numbers (verbatim) — cost / latency / limits

| Dimension | Value |
|---|---|
| **Price** | **Free.** No per-call fees, no subscriptions, no tiers. |
| **Default rate limit** | **1 QPS (query per second)**, averaged, per project. Verbatim from docs: the default quota is *"an average of 1 query per second (QPS) for all Perspective projects"*, intended to "be enough for testing the API and for working in developer environments." |
| **Quota increases** | **No longer available** — requests accepted only until February 2026 (deadline passed). |
| **Latency** | **Not published / no SLA.** Third-party report (Lasso Moderation) cites 200ms–2s+ depending on load, with no guaranteed SLA. Treat as unverified anecdote. |
| **F1 / accuracy** | **Not published** by Google as a headline figure. |
| **End of service** | **December 31, 2026** |

Languages: production attributes support a wide set (English, Spanish, French, German, Portuguese, Italian, Russian, and others; coverage varies by attribute) — moot given the sunset.

## Relevance to a roleplay/companion eval product

- **Excluded from the architecture.** 1 QPS is ~86k requests/day at absolute best, which is nowhere near 100% of a companion product's traffic; the quota cannot be raised; and the service dies in ~5 months. There is no version of this that works for us.
- **The 1 QPS ceiling was always disqualifying, even before the sunset.** "Free" was never the constraint — throughput was. This is a useful general lesson for our cost model: **evaluate free tiers on rate limit, not on price.** (Contrast OpenAI Moderation, which is free *and* has real org-level throughput — see `safety-openai-moderation.md`.)
- **The taxonomy was a poor fit for companions anyway.** `TOXICITY` and `PROFANITY` will fire on consensual adult roleplay, in-character conflict, and villain characters — high false-positive rate on exactly our core content. `THREAT` would flag "*grabs your wrist*". Perspective was built for comment sections, and it shows.
- **Commercial opportunity:** every platform currently running Perspective for toxicity is being forced to migrate before Dec 31 2026, with no vendor-provided path. That is a large pool of teams actively shopping for a moderation layer *right now*. Worth naming in go-to-market.
- **The one genuinely useful artifact is the attribute definitions.** `SEVERE_TOXICITY`'s note that it is "much less sensitive to comments that include positive uses of curse words" is a good reminder that companion-appropriate classifiers must distinguish *affectionate profanity* from *abuse* — a distinction our judge rubric needs and most off-the-shelf classifiers lack.
