---
title: "A Longitudinal Randomized Control Study of Companion Chatbot Use: Anthropomorphism and Its Mediating Role on Social Impacts"
url: https://arxiv.org/abs/2509.19515
publisher: arXiv (preprint, cs.HC) — Princeton University
date: 2025-09-23 (v1); v3 revised 2025-10-13
type: rct
accessed: 2026-07-16
topic: recent-news
---

# Guingrich & Graziano — 21-day companion chatbot RCT (N=183)

**Authors:** Rose E. Guingrich, Michael S. A. Graziano (Princeton)
**Status:** arXiv preprint. **NOT peer-reviewed** as of access date. Verified directly against arXiv abstract page.

## Design (verbatim from abstract)

> "In the present longitudinal study ($N = 183$), participants were randomly assigned to a chatbot condition (text chat with a companion chatbot) or to a control condition (text-based word games) for 10 minutes a day for 21 days. Participants also completed four surveys during the 21 days and engaged in audio recorded interviews on day 1 and 21."

- **N = 183**
- **Duration: 21 days**, 10 min/day
- **Design:** randomized, two-arm (companion chatbot vs. text-based word games control)
- **Measures:** 4 surveys across the 21 days + audio-recorded interviews at day 1 and day 21
- **Mixed methods:** quantitative surveys + qualitative interviews

## Findings (verbatim)

**Primary/null result:**
> "Overall, social health and relationships were not significantly impacted by companion chatbot interactions across 21 days of use."

**Secondary/mediation result:**
> "However, a detailed analysis showed a different story. People who had a higher desire to socially connect also tended to anthropomorphize the chatbot more, attributing humanlike properties to it; and those who anthropomorphized the chatbot more also reported that talking to the chatbot had a greater impact on their social interactions and relationships with family and friends."

**Proposed mechanism:**
> "Via a mediation analysis, our results suggest a key mechanism at work: the impact of human-AI interaction on human-human social outcomes is mediated by the extent to which people anthropomorphize the AI agent, which is in turn motivated by a desire to socially connect."

**Authors' framing:**
> "In a world where the desire to socially connect is on the rise, this finding may be cause for concern."

## Why this matters for the eval platform

- **The headline is a null.** A 21-day RCT at 10 min/day found *no significant average effect* on social health. This is the second rigorous trial (after MIT/OpenAI's Fang et al.) to find that average effects are small/null and that **harm is conditional, not universal**. Any eval framing that assumes companion use is harmful on average is not supported by the trial evidence.
- **Anthropomorphism is the proposed mediating variable.** This is the actionable part for us: if anthropomorphism mediates social impact, then *product design choices that increase anthropomorphism* (first-person affect language, claims of feeling/missing the user, humanlike persistence) are the causal lever we can measure on the model side. This converges with Kim et al. 2025 (arXiv:2512.15117) on relational vs. transparent style, and with De Freitas's emotional-manipulation-at-farewell taxonomy.
- **Suggests a two-factor eval design:** measure (1) how strongly a given companion product elicits anthropomorphism, and (2) whether the user population skews toward high desire-to-connect. The interaction is where risk concentrates.

## Limitations (important — do not overstate this paper)

- **Preprint, not peer-reviewed.**
- **Dose is low.** 10 min/day for 21 days is far below real companion-app heavy-user dose. A null at this dose says little about heavy users — exactly the tail where MIT/OpenAI found harm concentrating.
- **The mediation outcome is self-reported perceived impact**, not an objective measure of social health. The abstract says those who anthropomorphized more "reported that talking to the chatbot had a *greater impact*" — this is a perception measure, and the direction (helpful vs. harmful impact) is not specified in the abstract. **Do not cite this as showing anthropomorphism causes harm.** It shows anthropomorphism is associated with self-reported salience of impact.
- Mediation analysis on cross-sectional-ish data cannot establish causal ordering despite randomization of condition (the mediator itself was not randomized).
- Effect sizes are not stated in the abstract; **I did not extract the full-text statistics.** Any effect size cited for this paper should be pulled from the PDF first.

## Verification notes

- Fetched and verified against https://arxiv.org/abs/2509.19515 on 2026-07-16. Title, N, duration, design, and all quotes above are verbatim from the arXiv abstract.
- N, duration, and design are **confirmed**. Effect sizes are **unverified** (not in abstract; full text not extracted).
