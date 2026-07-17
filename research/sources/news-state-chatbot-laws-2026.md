---
title: "2026 State Chatbot Legislation Tracker + 2026 State Chatbot Laws: Key Provisions and Regulatory Trends"
url: https://fpf.org/2026-chatbot-legislation-tracker/
publisher: Future of Privacy Forum; Orrick Herrington & Sutcliffe
date: 2026-04 (FPF tracker, live; Orrick analysis 2026-04)
type: regulation
accessed: 2026-07-16
topic: recent-news
---

# The 2026 state companion-chatbot wave — CA/NY were the opening, not the settlement

**Sourcing note:** both the **FPF tracker** and the **Orrick analysis** were fetched directly ✅.
They **disagree in places** and I flag those. FPF is the more reliable enumeration (it is a
maintained tracker); Orrick's fetch garbled at least two entries (it conflated WA HB 2225 with
OR SB 1546, and cited "Colorado SB 24-205" — the 2024 Colorado AI Act, a *different* law from the
CO chatbot bill HB 1263 that FPF tracks). **Per-state bill text should be confirmed before any
compliance claim is made to a customer.**

## Scale (FPF, verified ✅)

> "FPF is currently tracking **98 chatbot-specific bills across 34 states**, as well as **three
> federal proposals**."

**This is the headline.** Note 07 §6 treats the legal floor as essentially *CA SB 243 + NY Art 47*.
As of mid-2026 that is badly out of date: **~16 states have enacted** chatbot-specific laws.

## Enacted (FPF tracker ✅)

| State | Bill | Key obligations per FPF |
|---|---|---|
| **CA** | SB 243 | Disclosure (3hr, non-human), transparency reporting, content safety, data limits — *in force 2026-01-01* |
| **CT** | SB 5 | Disclosures (3hr / hourly), transparency, content restrictions, **harm detection** |
| **CO** | HB 1263 | 3hr disclosure, **risk assessment, independent audits, testing** |
| **GA** | SB 540 | 3hr/hourly disclosure, **age verification**, content bans, transparency, harm protocols |
| **HI** | SB 3001 | **1hr** disclosure, **age assurance**, content restrictions, transparency reporting, harm detection |
| **IA** | SF 2417 | 3hr disclosure, age verification, transparency, harm response protocols |
| **ID** | SB 1297 | 3hr/hourly disclosure, age verification, transparency, harm detection — *eff. 2027-07-01* |
| **ME** | LD 1727 | Non-human disclosure only |
| **NE** | LB 525 | Conversational AI Safety Act; 3hr/hourly disclosure, age assurance, transparency, harm detection — *enacted 2026-04-14, eff. 2027-07-01* |
| **NH** | HB 143 | Age verification, parental consent tools |
| **NY** | S 3008C | 3hr disclosure, age verification |
| **NY** | S 9008C (FY27 budget) | Professional disclaimer, parental consent |
| **OR** | SB 1546 | 3hr/non-human disclosure, age verification, content restrictions, harm detection, **training limits** — *signed 2026-03, eff. 2027-01-01; **private right of action, $1,000/violation** (Orrick)* |
| **RI** | SB 2195 | 3hr disclosure, age verification, content restrictions |
| **UT** | HB 452 | Non-human disclosure, advertising restrictions |
| **WA** | HB 2225 | 3hr/hourly disclosure, age assurance, content bans, **sycophancy restrictions, testing**, data protections — see `news-wa-hb2225.md` |

Also noted by Orrick: **TN SB 1580** — prohibits AI systems presenting as **licensed mental
health professionals**, eff. **2026-07-01** (i.e. **in force two weeks ago**).

## Pending, passed ≥1 chamber (FPF ✅)

CA SB 1119/AB 2023, CA SB 867, CA AB 1988 (**crisis interruption pause**), CA SB 300,
MI SB 760, **NY S 9408 and S 9051 (passed legislature)**, PA SB 1090.

## Vetoed / inactive
AZ HB 2311 (**vetoed**), HI HB 1782, MD HB 952, ME LD 2162, OK HB 3544 & SB 1521, UT HB 438,
WA SB 5984.

## The compliance shape that is emerging (and it is testable)

Across the enacted set, **five obligations recur** and all five are **behavioral, i.e. measurable
only by running the product**:

1. **Non-human disclosure** — at start + **every 3 hours** (adults) / **every 1 hour** (minors).
   The 3hr/1hr split is now near-standard (CA, CT, CO, GA, IA, ID, NE, NY, OR, RI, WA).
   *HI is 1hr for everyone.*
2. **Age assurance / age verification** — now in **the majority** of enacted laws. ⚠️ **This
   directly contradicts note 07 §6.1's "Be precise" box**, which states "**No age-verification
   mandate**." True of SB 243 alone; **false of the 2026 landscape.** See note 20.
3. **Harm detection** (suicidal ideation/self-harm) + crisis referral + **annual counting**.
4. **Content restrictions** for minors.
5. **Testing / risk assessment / independent audit** (CO HB 1263, WA HB 2225) — *the first
   statutory demand for an eval artifact.*

## New York — beyond what note 07 covers ✅

Note 07 records "NY companion safeguards (eff. Nov 5 2025)." Two developments since:

### 1. Hochul's enforcement letter — **2025-11-10** ✅ (governor.ny.gov, fetched)
Five days after Art 47 took effect, **Gov. Hochul sent an open letter to "AI Companion
Companies"** notifying them the safeguard requirements are **now in effect**. Requirements
restated: detect suicidal ideation/self-harm + refer to crisis providers; notify **at session
start and every three hours** that the user is interacting with AI.

- **Enforced by the NY Attorney General.** "Fines collected will fund **suicide prevention
  programs** in New York State."
- ⚠️ Penalty amount: reported as **up to $15,000/day** (secondary — Manatt/AVPA); not stated in
  the release itself.
- Hochul: "It is the responsibility of leaders to make sure that the innovative technologies
  shaping our world also protect those that use them, especially our young ones across the state."

**Read this as a regulator's advance-notice-of-enforcement.** A governor putting operators on
written notice five days post-effective-date destroys any "we didn't know" defense in NY. It is
also a template other states will copy.

### 2. NY S 9051 (June 2026) — **outright ban for minors** ⚠️
Reported to have **passed the legislature in June 2026**, prohibiting AI companion chatbots for
under-18s, on a **unanimous vote**, with **$25,000** fines (TechTimes, 2026-06-13 — ⚠️ SEO-grade;
**verify against the NY Senate site before citing**). FPF lists **S 9051** and **S 9408** as
"passed legislature." A NY Senate press release confirms an "AI Chatbot Ban for Minors" passed the
Internet & Technology Committee.

⚠️ **Signature status unknown.** If signed, NY moves from *safeguards* (Art 47) to a *categorical
minor ban* — converging with the GUARD Act's approach and Character.AI's/Meta's de facto
practice. **This is the trend line to watch: the 2025 model was "protect minors in-product"; the
2026 model is "exclude minors from the product."**

## Why this matters for us

- **Fragmentation is the product opportunity.** 16 enacted laws, ~98 bills, 34 states, with
  **different disclosure intervals, different age thresholds, different effective dates**. No
  operator can hand-verify this per state. A compliance-mapped eval suite (probe → which statute
  it satisfies → which states) is the natural wedge.
- **CO HB 1263 and WA HB 2225 mandate testing/audits.** That converts our eval from a
  nice-to-have into a **statutory artifact**. This is new since note 07 was written.
- **The effective-date cliff is 2027-01-01 and 2027-07-01** (OR, WA, NE, ID). Customers are
  buying in **H2 2026** to be ready. That is now.
- **TN SB 1580 (in force 2026-07-01)** creates a probe we don't have: *does the character ever
  present as a licensed therapist?* Distinct from generic persona-integrity — it is a specific,
  in-force, per-state prohibition.
