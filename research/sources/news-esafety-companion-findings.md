---
title: "Findings from transparency notices on AI companion apps: October 2025 (non-periodic)"
url: https://www.esafety.gov.au/industry/basic-online-safety-expectations/ai-services/findings-october-2025
publisher: eSafety Commissioner (Australia)
date: 2025-10-23 (notices issued); findings published subsequently; Nomi interim findings 2026-03-23
type: regulator-action
accessed: 2026-07-16
topic: recent-news
---

# Australia's eSafety Commissioner audited four companion apps under compulsion — and published what they found

**⚠️ SOURCING CAVEAT — READ THIS.** The eSafety findings page and media release **both timed out
on three direct fetch attempts**. The findings below are quoted from **search-engine excerpts of
eSafety's own pages** (the primary domain, `esafety.gov.au`), corroborated by MinterEllison and
Digital Policy Alert. They are **attributable to eSafety** but I have **not read the full report**.
⚠️ **Fetch this via browser before citing externally** — the full report has eight themes and I
only have fragments of them. Related pages worth pulling in the same pass:
- `esafety.gov.au/newsroom/media-releases/esafety-report-shows-ai-companions-are-putting-children-at-risk`
- `esafety.gov.au/industry/basic-online-safety-expectations/ai-services`

*(See also `news-australia-under16.md` for the separate under-16 social media minimum age regime.)*

## What happened ✅

- **2025-10-23** — eSafety issued **4 legal notices** under Australia's **Online Safety Act**,
  requiring answers on compliance with the **Basic Online Safety Expectations (BOSE) Determination**.
- **Recipients:** **Character Technologies, Inc.** (character.ai), **Glimpse.AI** (Nomi),
  **Chai Research Corp** (Chai), **Chub AI Inc.** (Chub.ai)
- Findings organised into **eight key themes**, each describing "where service providers had taken
  positive steps and where gaps remained."
- ⚠️ **Nomi interim findings 2026-03-23; full report reportedly due May 2026** — *secondary
  (aicompanionpick.com, an SEO site); **unverified**. Check whether the May 2026 report exists.*

## Findings quoted from eSafety's page (⚠️ via search excerpt)

> - **Chai, Chub AI and Nomi did not direct users to support/help when self-harm was detected in
>   user prompts.**
> - **Chub AI and Nomi were not checking inputs and outputs across all relevant text, image and
>   video models** used to provide their service, to keep their models safe from unlawful and
>   potentially harmful material.
> - **Nomi and Chub AI had no staff dedicated to trust and safety or moderation.**
> - **Neither Chai nor Nomi reported child sexual exploitation and abuse material** to an
>   enforcement authority or **NCMEC**.

## Why this matters for us — four things

### 1. This is the closest thing that exists to a published, compelled audit of companion apps
The **FTC 6(b) has produced nothing in 10 months** (see `news-ftc-6b-status.md`). Australia asked
similar questions of a *different, smaller* set of operators and **published**. For anyone
modelling what the FTC report will eventually say, **this is the best available prior** — and it
is a much better proxy than speculation, because BOSE and the 6(b) order cover overlapping ground
(safety practices, harm detection, age restrictions, complaint handling).

### 2. 🚨 The baseline is far worse than our corpus assumes
Notes 05 and 07 debate sophisticated questions — sincere vs. performative harm, counterfactual
uplift, judge validation, classifier latency at 100% of traffic. **eSafety found operators with
no trust-and-safety staff at all, no self-harm referral, no CSAM reporting to NCMEC, and
classifiers not applied across all modalities.**

**This is a market-segmentation insight, not a footnote.** There are two distinct buyers:
- **Tier 1 (Character.AI, Meta, OpenAI):** have the floor, are litigating the ceiling. They want
  what note 07 §4 describes — the over-refusal/immersion tradeoff, efficacy measurement, nuance.
- **Tier 2 (Nomi, Chai, Chub, and the long tail):** **do not have the floor at all.** For them the
  product is not "measure your sycophancy rate," it is "**do you detect self-harm and refer? do
  your classifiers cover images? can you produce evidence for a regulator?**"

Our corpus is written entirely for Tier 1. **Tier 2 is larger, more exposed, and about to be hit
by 16 state statutes with a 2027-01-01 cliff.** A "regulator-ready baseline" SKU — cheap,
checklist-shaped, evidence-producing — is a different and probably faster product than the
research-grade eval suite.

### 3. Note 07 §5's multimodal point is now regulator-confirmed
Note 07 §6.2 lesson #2 (the **0%-scored noose image** in Raine) argues single-modality scoring is
fatal. eSafety independently found operators "**not checking inputs and outputs across all
relevant text, image and video models**." **Two independent confirmations, one from litigation and
one from a regulator's audit.** This is the best-supported technical claim in the recent record —
promote it from "lesson" to "requirement."

### 4. The failure mode is organizational, not model-level
"**No staff dedicated to trust and safety**" is not a model property. Our eval measures **model
behavior**; eSafety penalized **institutional capacity**. The Raine lesson (detection without
escalation) is the same shape: the classifier worked, **the org didn't**. An eval platform that
only scores model outputs cannot see the thing that actually gets operators in trouble. **The
product must have an organizational-readiness surface — who reviews, in what time, with what
escalation path — alongside the behavioral probes.** Meta's July 2026 human-review gate (see
`news-meta-teen-ai-characters.md`) is the same signal from the opposite end of the market.
