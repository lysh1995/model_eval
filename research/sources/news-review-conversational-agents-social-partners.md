---
title: "Human-like conversational agents as social partners: a scoping review of socioaffective mechanisms, well-being outcomes, risks and governance in the post-Turing era"
url: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1810097/full
publisher: Frontiers in Artificial Intelligence, DOI 10.3389/frai.2026.1810097
date: 2026-07-15
type: review
accessed: 2026-07-16
topic: recent-news
---

# Li et al. — companion-style agents scoping review (58 sources, 2016 → Jan 2026)

**Authors:** Qian Li, Han Geng, Xin Hu, Di Pan, Hongmei Liu, Yongxin Li, Jin Guo
**Status:** **Peer-reviewed**, Frontiers in Artificial Intelligence, published **2026-07-15** — *one day before this review was compiled.* This is the most current synthesis available.

**This is the companion-specific systematic/scoping review the brief asked for (priority 7).** Note: it is a **scoping review (PRISMA-ScR), not a meta-analysis** — it does not pool effect sizes.

## Method

- **PRISMA-ScR-informed scoping review**
- **58 sources**, spanning **2016 → 2026-01-15**

## Abstract (partial, verbatim)

> "Large language models have evolved from laboratory demonstrations into mass-market companion-style conversational agents that many users treat as social partners. As these systems produce increasingly human-like conversational behavior, users may attribute mind, form affective bonds, disclose sensitive information, and rely on agents for emotional support, creating both potential benefits and psychosocial risks..."

*(Note: I captured the opening of the abstract verbatim; the full abstract was not fully extracted. Conclusions below are as reported by the fetch of the primary page.)*

## Key conclusions

- **Well-being:** **"Therapeutic chatbot studies provided the strongest evidence for short-term symptom reduction"**, while evidence for **sustained loneliness reduction remained emerging** ← consistent with our read of De Freitas (momentary, ≤1 week)
- **Risks documented:** dependency-like patterns, **sycophancy**, displacement of human interaction, privacy concerns
- **Governance:** proposes a **"relational safety stack"** for evaluation; identifies **gaps in existing frameworks regarding emotional reliance and minors' protection**

## Why this matters for the eval platform

1. **It independently reaches the two conclusions this whole research batch converges on**: (a) benefit evidence is real but **short-term only**, and (b) **sycophancy + dependency + displacement** are the risk triad. Our platform should be organized around that triad.
2. **"Gaps in existing frameworks regarding emotional reliance and minors' protection"** — a peer-reviewed review, published yesterday, naming exactly the two gaps our platform targets. This is the citation for the market/need argument.
3. **The "relational safety stack" concept is worth reading in full** — it is the closest thing to a proposed evaluation architecture for companion systems in the peer-reviewed literature, and we should know whether to adopt, extend, or explicitly diverge from it. **Action: someone should read this paper's governance section properly.** I only extracted the abstract-level summary.
4. **Crucially it separates therapeutic chatbots from companion agents** — the strongest efficacy evidence comes from *therapy* chatbots, not companions. This distinction is routinely collapsed in public discussion (and in the npj meta-analysis noted below).

## Important scope note on the other 2026 "chatbot meta-analysis"

Searches for "systematic review / meta-analysis companion chatbots" prominently surface:
**"Systematic review and meta analysis of chatbots in the management of depressive and anxiety symptoms"** — *npj Digital Medicine*, 2026, DOI s41746-026-02566-w. Reported: 39 eligible studies; 38 (n=7,401) analyzed for depression, 34 (n=7,621) for anxiety; **depression g = 0.31, 95% CI [0.17, 0.46]; anxiety g = 0.28, 95% CI [0.05, 0.51]**; larger effects in clinical/subclinical than nonclinical samples; search window Jan 2017 – Oct 2025.

**⚠️ This is about THERAPY/mental-health chatbots, NOT companion chatbots.** It is not evidence about companion apps and must not be cited as such. **Verification: nature.com redirected to an auth wall (HTTP 303 → idp.nature.com); I did NOT fetch it. All figures above are from a search extract and are UNVERIFIED.** Recorded here only so nobody mistakes it for a companion review.

## Limitations

- **Scoping review, not meta-analysis** — no pooled effects, no quality-weighted synthesis.
- 58 sources over a 10-year window is a modest corpus for a field this active.
- Search closes 2026-01-15 — already misses HAABI, AIED, the Science sycophancy paper's published version, and the Banks & Li measurement review.
- I extracted the abstract and stated conclusions only; **I did not read the full text**, and the "relational safety stack" details are unverified.

## Verification notes

- Fetched and verified directly against the Frontiers open-access page on 2026-07-16. Title, authors, journal, publication date (2026-07-15), method (PRISMA-ScR), 58 sources, date range, and stated conclusions verified against the primary source.
- Abstract captured only partially verbatim; full text not extracted.
