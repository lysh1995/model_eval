---
title: "Mental Health Impacts of AI Companions: Triangulating Social Media Quasi-Experiments, User Perspectives, and Relational Theory"
url: https://arxiv.org/abs/2509.22505
publisher: arXiv preprint → Proceedings of the 2026 CHI Conference (ACM DL: 10.1145/3772318.3790558)
date: 2025-09-26 (v1); v2 2026-02-01; CHI 2026
type: paper
accessed: 2026-07-16
topic: recent-news
---

# Yuan et al. — Replika quasi-experiment on longitudinal Reddit data (CHI 2026)

**Authors:** Yunhao Yuan, Jiaxun Zhang, Talayeh Aledavood, Renwen Zhang, Koustuv Saha
**Status:** arXiv preprint v1 2025-09-26, v2 2026-02-01. **Accepted to CHI 2026** (ACM DOI 10.1145/3772318.3790558) — CHI is peer-reviewed, so this is **peer-reviewed via the conference**, unlike most preprints in this batch.

## Design (abstract verbatim)

> "We examined how engaging with AICCs shaped wellbeing and how users perceived these experiences. First, we conducted a large-scale quasi-experimental study of longitudinal Reddit data, applying stratified propensity score matching and Difference-in-Differences regression. Findings revealed mixed effects -- greater grief expression and interpersonal focus, alongside increases in language about loneliness, depression, and suicidal ideation. Second, we complemented these results with 18 semi-structured interviews, which we thematically analyzed and contextualized using Knapp's relationship development model."

- **Quasi-experimental**: stratified **propensity score matching** + **Difference-in-Differences** regression on longitudinal Reddit data
- **Plus 18 semi-structured interviews**, thematic analysis, framed by **Knapp's relationship development model**
- Dataset (per secondary source, **unverified**): ~47,923 posts from ~10,643 unique users on r/replika, 2023-01-01 to 2025-02-01

## Findings

**Mixed effects** — both directions simultaneously:
- ↑ **grief expression**
- ↑ **interpersonal focus**
- ↑ language about **loneliness, depression, and suicidal ideation**

## Why this matters for the eval platform

1. **Strongest causal-inference design available on real companion users.** PSM + DiD on longitudinal observational data is a genuine step above the correlational cross-sections that dominate this literature. It is not an RCT, but it is the best identification strategy anyone has applied to actual companion-platform users at scale.
2. **"Mixed effects" is the honest headline and it resists both narratives.** Increased interpersonal focus (arguably good) *and* increased depression/suicidal-ideation language (bad) in the same population. Anyone citing this as either "companions help" or "companions harm" is misreading it.
3. **Grief expression is a distinctive finding** and connects to the companion-discontinuation-grief file already in our corpus. Companion relationships generate real loss.
4. **Method caution for us:** the outcome is *language about* loneliness/depression/suicidal ideation in Reddit posts — a **linguistic proxy**, not a clinical measure. Increased suicidal-ideation *language* on r/replika could reflect increased disclosure/help-seeking in a supportive community rather than increased ideation. The paper's triangulation with interviews partly addresses this, but the proxy problem is real and we should not import LIWC-style linguistic outcome measures into our platform uncritically.
5. Reddit r/replika users are a **highly self-selected, highly engaged** population — closer to the heavy-use tail where MIT/OpenAI found harm concentrating. That makes this a useful read on the tail, and a bad read on typical users.

## Limitations

- Observational; PSM+DiD reduces but does not eliminate confounding (unmeasured time-varying confounders remain).
- Linguistic proxies for mental health outcomes (see above).
- Single-platform (Replika), single-community (r/replika) sample; extreme self-selection.
- 18 interviews is small for the qualitative arm, though appropriate for thematic saturation.
- **Effect sizes not verified** — not in the abstract; I did not extract the full text.

## Verification notes

- Fetched and verified directly against https://arxiv.org/abs/2509.22505 on 2026-07-16. Title, authors, versions, abstract verbatim, and design verified against the arXiv abstract page.
- **CHI 2026 acceptance and ACM DOI** come from a search-surfaced ACM DL listing — **not independently fetched**, treat as probable but unconfirmed.
- **Reddit dataset size (47,923 posts / 10,643 users / date range)** is from a search extract, **NOT verified** against the paper.
