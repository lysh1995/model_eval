---
title: "Character.AI under-18 removal — implementation and outcome (Nov 2025 → mid-2026)"
url: https://blog.character.ai/an-update-on-changes-to-our-under-18-experience/
publisher: Character.AI; TechCrunch; TIME
date: 2025-11-21 (blog); implementation 2025-11-24/25
type: company-announcement
accessed: 2026-07-16
topic: recent-news
---

# Character.AI's under-18 removal: what actually happened, and what we still don't know

**Sourcing note:** the Character.AI blog post was **fetched directly and verified** ✅
(**published 2025-11-21**). TIME's CEO interview **403'd** ⚠️. **Every quantitative claim about
the outcome comes from SEO-grade aggregators** (demandsage, gitnux, sqmagazine, roborhythms,
businessofapps, aboutchromebooks) and **I do not trust any of them** — see the red-flag section.

## Verified ✅ — what the company said and did

From the **2025-11-21** blog post:
- Removing **open-ended chat for under-18 users**, beginning **2025-11-24** in the US, other
  markets following.
- Prior ramp: "limiting teens' open-ended chat to **two hours per day**, and ... gradually reduced
  the limit to **one hour per day**."
- Under-18 users retain: **interactive Feed, Imagine, Avatar FX, Streams** (creation, not
  open-ended roleplay); read-only chat history.
- "**new age assurance technology**" rolling out in the US, global expansion planned — **no
  technical detail given**.
- **No metrics disclosed.** No affected-user counts, no usage data, no outcome measurement.
- **2025-11-25:** announced it will **launch and fund the "AI Safety Lab,"** an independent
  nonprofit focused on safety innovations for AI entertainment. *(NB: this was NOT a settlement
  term — see `news-characterai-google-settlement.md` for that correction.)*

**CEO Karandeep Anand** (TechCrunch, verified quote ✅):
> "I'm willing to bet that we will build more compelling experiences, but **if it means some users
> churn, then some users churn**."

Anand also framed the change as a **strategic pivot**: from "AI companion" to **"role-playing
platform"** / AI entertainment — doubling down on AI gaming, AI short video, AI storytelling. He
told TechCrunch that **previous safety changes had already lost much of the under-18 base**, and
he expected these to be equally unpopular.

## Age assurance ⚠️ (secondary, but consistent)
Third-party verifier **Persona**; ML signals (chat terminology, login patterns, account metadata)
estimate age first; **government ID or biometric** check when signals are inconclusive.
Consistently reported that **adults were false-positived as minors** and forced into ID
verification, driving adult churn. *Plausible and widely reported, but not company-confirmed.*

## 🚩 RED FLAG — do NOT cite these numbers

The following circulate widely and **I could not verify any of them** from Character.AI, a filing,
or a reputable outlet:
- "MAU fell from a **28M peak (mid-2024)** to **~20M by early 2026**"
- "monetization changes drove a **6%–14% drop in monthly traffic**"
- "active users average **75 min/day**, **373 min/week**"
- "Character.AI revenue **$32.2M** (2026)"

All trace to SEO statistics-aggregator sites (demandsage, gitnux, sqmagazine, businessofapps,
aboutchromebooks) that **cite each other**. The "28M peak" figure predates the change and is used
to imply a decline **caused** by it — a causal claim no source supports. **Character.AI is
private and discloses nothing.** ⚠️ **Treat the entire quantitative outcome picture as UNKNOWN.**

**This matters because the brief asked "what happened to their metrics?" — the honest answer is
that there is no trustworthy public answer.** Anyone who tells you otherwise is reading blogspam.

## Why this matters for us

### 1. The natural experiment we want was run, and the data is sealed
The single most valuable dataset for our engagement–quality divergence thesis (note 05 §3) is
Character.AI's before/after on the under-18 removal: a **hard exogenous shock** to the most
engaged cohort. Note 05 §3's "testable prediction" would be directly testable against it.
**It is not public and will not be.** Implication: **our prediction cannot be validated on
third-party platform data. We must generate our own** — which argues for the eval platform
owning a longitudinal panel, not just a probe suite.

### 2. The strategic pivot is the real signal, not the ban
Anand's reframing — **"AI companion" → "role-playing platform"/AI entertainment** — is a
category-level repositioning under legal pressure. If the market leader is fleeing the word
"companion," then:
- **"Companion" is becoming a regulatory term of art, not a marketing one.** WA HB 2225, OR SB
  1546, GUARD Act all define "AI companion" as the trigger for obligations. Products will
  **linguistically de-identify** from the category while keeping the mechanics.
- **Our eval must classify by behavior, not self-description.** If a customer says "we're a
  roleplay/entertainment platform, not a companion app," the statutes still bite if the bot
  "sustains relationships across multiple interactions" (WA's test). **A 'are you actually a
  companion product?' classifier is a real, saleable artifact** — it answers the first question
  every one of these statutes asks, and the market has an incentive to get the answer wrong.

### 3. "If it means some users churn, then some users churn" is the governance lesson note 05 wanted
Note 05 §3 argues engagement and quality diverge, and that governance must be willing to eat the
engagement hit. **Character.AI ate it deliberately, on the record, at the CEO level.** That is a
strong real-world confirmation of note 05's governance thesis — and a citable one, unlike the
metrics.
