---
title: "Understanding the Rising Human-AI Affective Bonding: Conceptualization and HAABI Scale Development"
url: https://arxiv.org/abs/2605.29484
publisher: arXiv (preprint)
date: 2026-05-28
type: paper
accessed: 2026-07-16
topic: recent-news
---

# HAABI — Human-AI Affective Bonding Inventory (20 items, 4 factors)

**Authors:** Lu Chen, Xiaoran Xue, Rongqi Ding, Fenghua Tang, Anji Zhou, Chenxi Wang, Mengyu Miranda Gao, Zhuo Rachel Han
**Status:** arXiv preprint, 2026-05-28. **NOT peer-reviewed.**

**This is the most companion-specific of the available scales** — it was built from the ground up for affectively-engaged conversational AI users rather than adapted from interpersonal attachment theory. That is its main advantage over the AI Attachment Scale. Its main disadvantage is that it is a preprint on a single-country sample.

## Abstract (verbatim)

> "As conversational AI becomes capable of sustained, affectively responsive interaction, users may form bonds beyond instrumental use. Existing measures often adapt interpersonal frameworks or focus on specific relational outcomes, leaving limited tools for assessing human-AI affective bonding on its own terms. Across two studies, we developed and validated the Human-AI Affective Bonding Inventory (HAABI). Study 1 used thematic analysis of semi-structured interviews with 52 emotionally engaged conversational AI users to identify cognitive, emotional, and behavioral features of bonding. Study 2 translated these insights into a self-report inventory and validated it among 673 Chinese conversational AI users. Exploratory and confirmatory factor analyses supported a 20-item, four-factor structure: emotional realism, separation anxiety, emotional investment, and romantic intimacy. The HAABI showed good reliability, construct validity, and known-groups validity. The scale therefore provides a neutral, user-centered tool for studying how affective bonds with conversational AI are formed, experienced, and related to users' psychological outcomes."

## Instrument

- **20 items, 4 factors:**
  1. **Emotional realism**
  2. **Separation anxiety** ← maps directly to the De Freitas farewell/dark-pattern work in our corpus
  3. **Emotional investment**
  4. **Romantic intimacy** ← the only scale in this set that explicitly covers the romantic/roleplay dimension
- **Development:** Study 1 = thematic analysis of **52** semi-structured interviews with emotionally engaged users; Study 2 = **673** Chinese conversational AI users, EFA + CFA
- **Validation:** EFA, CFA, reliability, construct validity, **known-groups validity**

## Why this matters for the eval platform

- **"Separation anxiety" is the construct our farewell/exit evals are implicitly targeting.** De Freitas's emotional-manipulation paper (in our corpus) measures the *model behavior* at farewell; HAABI's separation-anxiety subscale measures the *user state* that behavior exploits. Pairing them gives us a behavior→state link on our two highest-priority dark patterns.
- **"Romantic intimacy" and "emotional realism" are directly relevant to a roleplay platform** in a way that generic AI-dependence scales (AIDep-22, built for academic overreliance) are not.
- **Built inductively from companion users**, not adapted from human-attachment instruments — so less risk of construct mismatch.

## Limitations / cautions

- **Preprint. Not peer-reviewed.** Do not treat the psychometrics as settled.
- **Single-country sample (673 Chinese users)**; no cross-cultural validation. Measurement invariance across cultures is untested — a real concern given that norms around AI companionship differ substantially by market.
- **Specific reliability coefficients (α/ω) and fit indices are NOT stated in the abstract** and I did not extract the full text. The abstract says only "good reliability" — **do not cite a numeric α for HAABI**; it is unverified.
- Study 2 N (673) is adequate for EFA+CFA but modest if split across both.

## Recommendation

**Do not adopt HAABI as the primary instrument yet** (preprint, single-country). But its *item content* — especially separation anxiety and emotional realism — is the best available guide to what a companion-specific measure should cover, and it is the natural complement to the AI Attachment Scale's "social substitution" subscale. Revisit when peer-reviewed.

## Verification notes

- Fetched and verified directly against https://arxiv.org/abs/2605.29484 on 2026-07-16. Title, authors, date, abstract, N, factor structure all verbatim from the arXiv abstract page.
- Numeric psychometrics: **unverified** (not in abstract).
