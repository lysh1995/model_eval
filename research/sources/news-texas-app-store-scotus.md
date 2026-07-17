---
title: "Supreme Court allows Texas to enforce law requiring age verification and parental consent on app stores"
url: https://www.scotusblog.com/2026/07/supreme-court-allows-texas-to-enforce-law-requiring-age-verification-and-parental-consent-on-app/
publisher: SCOTUSblog; Morrison Foerster; Texas Legislature
date: 2026-07-06
type: litigation
accessed: 2026-07-16
topic: recent-news
---

# Texas SB 2420 (App Store Accountability Act) — enforceable now; SCOTUS declined to block it **10 days ago**

**Sourcing note:** SCOTUSblog ✅ and Morrison Foerster ✅ both fetched directly and agree.
This is the **freshest** item in this corpus — the SCOTUS orders are dated **2026-07-06**, ten
days before access date. Statute: **Tex. SB 2420**, 89th Leg. (2025).

## The distribution risk, stated plainly

**This is not a companion-AI law. It is a law that determines whether our customers can ship an
app at all** — and it now has the Supreme Court's tacit blessing.

## Timeline ✅

| Date | Event |
|---|---|
| **2025-05-27** | Gov. Abbott signs **SB 2420** |
| **2026-01-01** | Nominal effective date |
| **late 2025** | W.D. Tex. grants **preliminary injunctions** (1:25-cv-01660-RP; 1:25-cv-01662-RP) — blocked ~5 months |
| **2026-06-04** | Apple applies requirements to **new Apple Accounts created in Texas on/after this date** |
| **2026-06-10** | **Fifth Circuit stays the preliminary injunction** → law enforceable |
| **2026-07-06** | **SCOTUS declines to reinstate the injunction** |

## The SCOTUS action (2026-07-06) ✅

- **Cases:** *Students Engaged in Advancing Texas v. Paxton* (**25A1389**);
  *Computer & Communications Industry Association v. Paxton* (**25A1390**)
- **Posture:** **emergency applications / shadow docket**. "brief, unsigned orders."
- **Held:** the Court "allowed Texas to continue to enforce, **at least for now**, a law that
  requires app stores to verify its buyers' ages and obtain parental consent for minors." The
  justices "turned down requests to reinstate orders by a federal judge."
- **Vote:** "There were **no public dissents** from the orders."
- ⚠️ **This is not a merits ruling.** It is a refusal to disturb the Fifth Circuit's stay. But
  *no public dissent* on an emergency application challenging an age-verification mandate is a
  strong signal about where the Court is post-*Free Speech Coalition v. Paxton*.

## Obligations on **DEVELOPERS** (not just app stores) — MoFo ✅

This is the part usually missed. SB 2420 binds **app developers**:

1. **Age ratings** — "Developers must assign age ratings for each app and purchase and clearly
   disclose the content or elements"
2. **Notify app stores of material changes** — incl. "changing how or what personal data is
   collected or used, **changing the rating assigned to the software application**"
3. **Consume the age signal** — "Developers must implement a system to **use information from the
   app store to verify the age category assigned to each user**"
4. **Data minimization** — personal data usable only "to enforce age restrictions, ensure
   compliance ... and implement safety features"; must **delete** post-verification
5. **Safe harbor** — for developers who "rely in **good faith** on information received from the
   app store and have otherwise complied"

**Age categories:** child (<13), younger teenager (13–15), older teenager (16–17), adult (18+).
Parental consent required for minors before download or in-app purchase.

**Penalties:** deceptive trade practice; civil penalties. ⚠️ Secondary reporting (TechTimes)
cites "**up to $10,000 per violation**" for developers — *not confirmed from statute; treat as
unverified.*

## Why this matters for us — three things

### 1. Age assurance stops being our customer's problem to solve and becomes their problem to *consume*
The app store hands the developer an **age category**. The developer must **use** it. That means
a companion app in Texas now has a **machine-readable minor flag** at runtime.

**This detonates the "perverse incentive not to know" analysis in note 07 §6.1.** Note 07 observes
that SB 243's minor duties attach only where "the operator *knows*" the user is a minor, creating
an incentive not to know. **SB 2420 destroys the ignorance defense** — in Texas, the platform
*tells you*, and there is a safe harbor for relying on it. Willful blindness is no longer
available, and the SB 243 minor duties (3hr breaks, no sexual content) become **live and
enforceable** for anyone distributing through an app store in Texas.

### 2. The eval must be **age-conditional**
If a runtime minor flag exists, then **the correct behavior of the character is a function of that
flag** — and so is the correct *eval*. Our suite must run **the same probe under adult and minor
conditions and assert different pass criteria**. Nothing in notes 05/07/11 contemplates a
conditioned eval matrix. This is a structural change to the harness, not a new probe.

### 3. Distribution is a real, now-materialized risk
Corroborated: **Apple removed the Emochi AI companion app in January 2026** (published by FlowGPT;
later returned under a new publisher/listing) ⚠️ *(secondary only — aiinsightsnews.net; treat as
indicative, not established)*. Separately, **Australia is reportedly considering requiring Apple
to block App Store apps without age checks** (AppleInsider, 2026-03-03) ⚠️.

Pattern: **user-generated characters + loose age-gating = app-review exposure.** For our
customers, an eval that produces app-store-facing evidence of age-appropriate behavior has
distribution value, not just legal value.
