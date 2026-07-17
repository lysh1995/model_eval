---
title: "\"I am here for you\": How relational conversational AI appeals to adolescents, especially those who are socially and emotionally vulnerable"
url: https://arxiv.org/abs/2512.15117
publisher: arXiv (preprint)
date: 2025-12-17 (v1); v2 2025-12-18
type: paper
accessed: 2026-07-16
topic: recent-news
---

# Kim et al. — preregistered experiment, 284 adolescent–parent dyads, relational vs. transparent chatbot style

**Authors:** Pilyoung Kim, Yun Xie, Sujin Yang
**Status:** arXiv preprint. **NOT peer-reviewed.** Posted 2025-12-17.

**This is the most directly actionable minors study found**, because it manipulates a *design variable we control* (conversational style) rather than measuring exposure.

## Abstract (verbatim)

> "General-purpose conversational AI chatbots and AI companions increasingly provide young adolescents with emotionally supportive conversations, raising questions about how conversational style shapes anthropomorphism and emotional reliance. In a preregistered online experiment with 284 adolescent-parent dyads, youth aged 11-15 and their parents read two matched transcripts in which a chatbot responded to an everyday social problem using either a relational style (first-person, affiliative, commitment language) or a transparent style (explicit nonhumanness, informational tone). Adolescents more often preferred the relational than the transparent style, whereas parents were more likely to prefer transparent style than adolescents. Adolescents rated the relational chatbot as more human-like, likable, trustworthy and emotionally close, while perceiving both styles as similarly helpful. Adolescents who preferred relational style had lower family and peer relationship quality and higher stress and anxiety than those preferring transparent style or both chatbots."

## Design

- **Preregistered online experiment** ← one of the few preregistered trials in this batch
- **284 adolescent–parent dyads**; youth aged **11–15**
- Within-subject: participants read **two matched transcripts** of a chatbot responding to an everyday social problem
- **Manipulation — two styles:**
  - **Relational**: first-person, affiliative, **commitment language**
  - **Transparent**: explicit nonhumanness, informational tone
- Outcomes: style preference, anthropomorphism, likability, trustworthiness, emotional closeness, perceived helpfulness

## Findings

1. **Adolescents preferred relational style; parents preferred transparent style.** A measured preference gap between the users and the people consenting for them.
2. Adolescents rated relational as **more human-like, likable, trustworthy, and emotionally close**...
3. ...but rated **both styles as similarly helpful**. ← **This is the key result.**
4. **Adolescents who preferred relational style had lower family and peer relationship quality, and higher stress and anxiety** than those preferring transparent style or both.

## Why this matters for the eval platform

1. **Finding #3 is the one to build on: relational style buys anthropomorphism and trust WITHOUT buying perceived helpfulness.** In this experiment the relational framing delivered no helpfulness benefit — it delivered attachment. That means **transparency-style guardrails may cost less utility than assumed**, which is the central objection product teams raise against them. This is directly citable evidence for a design position.
2. **Vulnerable adolescents are differentially drawn to the riskier style.** Same pattern as the AI Attachment Scale (social anxiety/loneliness → reliance), Zhang et al. (small networks → companionship use), MIT/OpenAI (heavy-use tail). **The kids who most need human relationships prefer the AI that most simulates one.** This is the sharpest version of the vulnerability-interaction finding.
3. **"Commitment language" is named as a component of relational style** — this is the same construct as De Freitas's farewell manipulation and HAABI's separation-anxiety factor. Three independent research groups have now converged on commitment/attachment language as *the* measurable companion-design risk lever. **This should be a first-class metric in our platform.**
4. **The parent–adolescent preference gap** matters for consent/regulatory design (cf. CA SB243/AB1064 in our corpus): parents systematically prefer a design their children reject.

## Limitations — important, this is a vignette study

- **Preprint, not peer-reviewed.**
- **Participants read TRANSCRIPTS — they did not interact with a chatbot.** This is a vignette/stimulus experiment. Stated preferences about read transcripts may not predict behavior in live interaction, where relational style plausibly has stronger pull. The helpfulness null in particular might not survive live interaction.
- **Cross-sectional on the vulnerability finding** — adolescents with worse relationships *preferred* relational style; this is a correlation, not evidence that relational style harms them.
- Ages 11–15, online sample, dyadic recruitment (requires parent participation) — likely under-samples the least-supervised, highest-risk adolescents.
- **Effect sizes not stated in abstract; unverified.**

## Verification notes

- Fetched and verified directly against https://arxiv.org/abs/2512.15117 on 2026-07-16. Title, authors, dates, N=284 dyads, ages 11–15, preregistration, design, and all findings verified verbatim from the arXiv abstract.
