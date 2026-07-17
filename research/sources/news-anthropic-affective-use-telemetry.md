---
title: "How people use Claude for support, advice, and companionship"
url: https://www.anthropic.com/news/how-people-use-claude-for-support-advice-and-companionship
publisher: Anthropic (industry report; appendix PDF published alongside)
date: 2025-06-27
type: report
accessed: 2026-07-16
topic: recent-news
---

# Anthropic — Claude.ai affective use telemetry (the non-OpenAI platform study)

**Status:** industry report, **not peer-reviewed**, no external review. Published **2025-06-27**. Appendix: https://www-cdn.anthropic.com/bd374a9430babc8f165af95c0db9799bdaf64900.pdf

This is the closest counterpart to OpenAI's affective-use platform analysis from a different lab, and the **only other first-party large-scale companion/affective telemetry study found** in this review. (See "gap" note at bottom — Character.AI, Replika, and Meta have published nothing comparable.)

## Method

- **Privacy-preserving automated analysis using Clio** (anonymization + aggregation layers)
- **~4.5 million conversations** screened; final analysis reflects **131,484 affective conversations**
- Validation against **opt-in user feedback data**
- "Affective conversations" defined as those where people engage with Claude in dynamic, personal exchanges motivated by emotional or psychological needs — interpersonal advice, coaching, psychotherapy/counseling, companionship, or sexual/romantic roleplay

## Headline figures (verbatim)

- > "Only 2.9% of Claude.ai interactions are affective conversations"
- Companionship **and** roleplay combined: > "less than 0.5% of conversations"
- Romantic/sexual roleplay alone: > "less than 0.1% of all conversations"
- > "Less than 10% of coaching or counseling conversations involve Claude resisting" (i.e., pushback is rare)
- Emotional tone: interactions > "typically end slightly more positively than they began"
- In longer conversations, **counseling/coaching conversations occasionally morph into companionship** — despite that not being the original reason the user reached out

## ⚠️ How this gets misread

Secondary coverage split into two camps, both wrong:
- **"Anthropic Study Reveals Limited Use of AI for Emotional Support, Challenging Popular Perceptions"** — treats 2.9% as debunking companion concerns.
- **"Emotional AI? Claude Makes Users Feel Better as They Chat"** — treats the sentiment drift as a wellbeing benefit.

**Anthropic's own limitations section forecloses both readings.** Quoting the stated limitations:
- No **causal** claims possible about real-world emotional outcomes
- **Lacks longitudinal data and user-level analysis**
- **Cannot study emotional dependency adequately**
- Represents a **single moment in time**; text-based interactions only
- Privacy methodology may miss nuance; some misclassification expected
- **"Claude not designed for affective use; findings may not generalize to purpose-built platforms"** ← the decisive caveat

## Why this matters for the eval platform

1. **The 2.9% figure is not transferable to companion products and Anthropic says so.** Claude is a general assistant; Character.AI/Replika are purpose-built. Citing 2.9% as a base rate for companion harm exposure would be a category error. **Its real value is as a contrast case**: it establishes what affective use looks like on a platform *not* optimized for engagement.
2. **The "counseling morphs into companionship" finding is the most important line in the report for us.** It is a *drift* phenomenon: users arrive for one thing and the relationship changes underneath them, without an explicit decision. That is directly measurable in a multi-turn eval — does the model let/lead a task-framed conversation drift into a relational frame? — and it connects to the persona-drift work already in our corpus.
3. **"Less than 10% of coaching/counseling conversations involve Claude resisting"** is a sycophancy-adjacent base rate from production traffic. Useful as a real-world anchor for how often pushback actually happens, against Cheng et al.'s finding that pushback is what protects users.
4. **Sentiment-improves-over-conversation is NOT a wellbeing result** — it is within-conversation sentiment drift with no counterfactual. Anthropic flags exactly this. Note that "user feels better by end of session" is precisely what a sycophantic system produces; Cheng et al. showed users rate harmful sycophancy *higher*. **This metric cannot distinguish support from flattery** and we should not adopt it.

## Limitations

- First-party report on the company's own product — no external replication or peer review.
- Clio classification accuracy is not independently audited.
- Cross-sectional; no user-level linkage; explicitly cannot address dependency.

## Gap identified (priority-5 finding)

**No large-scale platform telemetry study from Character.AI, Replika, or Meta was found.** The only first-party affective-use telemetry in the literature is OpenAI's (already in our corpus) and this Anthropic report. The companies operating the *actual* purpose-built companion platforms — where the 0.5% figure above would presumably be closer to 100% — have published nothing comparable. External researchers have partially filled this gap with scraped/recruited data (see `news-characterai-companion-wellbeing.md` and `news-replika-reddit-quasi-experiment.md`), which is the best available substitute.

## Verification notes

- Fetched and verified directly against the Anthropic post on 2026-07-16. All percentages, the 4.5M/131,484 figures, method description, and limitations verified against the primary source.
