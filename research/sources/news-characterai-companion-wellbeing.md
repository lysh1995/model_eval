---
title: "The Rise of AI Companions: Interaction with AI Companions and Psychological Well-being"
url: https://arxiv.org/abs/2506.12605
publisher: arXiv (preprint) — Stanford / Carnegie Mellon
date: 2025-06-14 (v1); v5 revised 2026-05-04
type: paper
accessed: 2026-07-16
topic: recent-news
---

# Zhang et al. — Character.AI users, surveys + 464,687 real messages

**Authors:** Yutong Zhang, Dora Zhao, Jeffrey T. Hancock, Robert Kraut, Diyi Yang
**Status:** arXiv preprint. **NOT peer-reviewed** as of access. v1 2025-06-14, **v5 2026-05-04** (actively revised — check for a published version).

**This is the best available substitute for Character.AI first-party telemetry** (which does not exist publicly). It pairs self-report with *actual chat logs* — rare in this literature.

## Design

- **1,131 U.S. adults** who use Character.AI — survey responses
- **4,664 chat sessions / 464,687 messages** donated by **237** of those participants
- **Observational/correlational.** Not an experiment. No randomization.

## Findings

- **Smaller social networks** → more likely to report **companionship as primary chatbot use** → associated with **lower well-being**
- The negative association was **stronger when interactions were intensive and highly disclosive**
- Authors' conclusion: the association between AI companionship and well-being **is not uniform** and **depends on how chatbots are used and users' offline social environments**

## Why this matters for the eval platform

1. **Converges with the whole batch on the same conclusion: harm is conditional, concentrated, and dose/mode-dependent — not universal.** This now holds across MIT/OpenAI (heavy-use tail), Guingrich & Graziano (null on average), the AI Attachment Scale (vulnerability → reliance), Kim et al. (vulnerable adolescents prefer relational style), and this paper (small networks + intensive/disclosive use). **Five independent studies, same shape.** That is the most robust finding in the field and should be the organizing assumption of our platform.
2. **"Intensive and highly disclosive" is a two-dimensional risk marker computable from logs** — volume × self-disclosure depth. Both are measurable server-side without a survey. This is a strong candidate for a production telemetry signal.
3. **Offline social network size is the moderator** — and it is *not* observable from logs. This is an argument that log-only evaluation is structurally insufficient: the same conversation is higher-risk for a socially isolated user. Either we accept that limitation explicitly or we pair telemetry with periodic survey instrumentation (see the scales files).
4. Direction of causation is **not** established — small networks may cause companion reliance, companion reliance may shrink networks, or both. **Do not cite this as evidence that companion use lowers wellbeing.**

## Limitations

- **Preprint, not peer-reviewed**; 5 revisions suggests substantive change — verify current version before citing.
- **Cross-sectional and correlational.** No causal claim supported.
- Self-selected participants who consented to donate chat logs — the 237 log-donors are a subset of the 1,131 and likely non-representative even of Character.AI users.
- U.S. adults only; Character.AI's user base skews young, so adult-only sampling may miss the highest-risk population.
- Well-being measure not specified in the abstract; **unverified** which instrument was used.

## Verification notes

- Fetched and verified directly against https://arxiv.org/abs/2506.12605 on 2026-07-16. Title, authors, dates/versions, N=1,131, 237 log-donors, 4,664 sessions, 464,687 messages, and the findings verified against the arXiv abstract page.
- Effect sizes and the well-being instrument: **not in abstract, unverified.**
