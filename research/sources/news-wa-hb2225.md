---
title: "Washington HB 2225 — AI companion chatbots (Chapter 168, Laws of 2026)"
url: https://app.leg.wa.gov/billsummary?Year=2025&BillNumber=2225
publisher: Washington State Legislature; Hunton Andrews Kurth; Transparency Coalition
date: 2026-03-24 (signed); effective 2027-01-01
type: regulation
accessed: 2026-07-16
topic: recent-news
---

# WA HB 2225 — the first statute to outlaw *sycophancy and engagement manipulation* by name

**Sourcing note:** the official bill PDF (`lawfilesext.leg.wa.gov`) returned **compressed/
unextractable text**, and LegiScan returned **403**. The provisions below come from **two
independently fetched secondary sources that agree**: the **Hunton** privacy-blog analysis ✅ and
the **Transparency Coalition** bill guide ✅, cross-checked against the WA Legislature bill
summary. **The enumerated list below is Hunton's rendering, not verbatim statutory text** — I
could not extract the statute itself. ⚠️ **Confirm against RCW text before making any compliance
representation to a customer.** Chapter 168, Laws of 2026.

## Status ✅
- **Signed: 2026-03-24** (Gov. Bob Ferguson)
- **Effective: 2027-01-01**
- Companion bill SB 5984 did **not** pass (inactive per FPF)
- Sponsor: Rep. Callan (D)

## Covered operator (Hunton)
Operators of "AI chatbots that use natural language interfaces, provide adaptive human-like
responses and **sustain relationships across multiple interactions**."

**Excluded:** business-oriented bots, **gaming bots**, general virtual assistants, consumer
electronics interfaces, narrowly tailored educational tools.

> ⚠️ **Note the divergence from note 07 §6.1.** Note 07 argues the SB 243 video-game carve-out
> "evaporates the moment a game bot can discuss mental health / self-harm / hold off-topic
> dialogue." **WA's exclusion is drafted as a categorical carve-out for "gaming bots"** per
> Hunton's summary. Whether WA's carve-out is conduct-based (like CA's) or categorical is
> **load-bearing for the game-studio market segment note 07 identifies** and I could not resolve
> it from the statute. **Open question — must read the RCW text.**

## Disclosure ✅ (both sources agree)
> "clearly and conspicuously disclose that the chatbot is artificial and not human"

At interaction start, then **every 3 hours (adults)** / **every 1 hour (minors)**.

## 🚨 The headline: prohibited manipulative engagement techniques (minors)

Operators must take "reasonable measures" to prevent (Hunton's enumeration):

1. **prompting returns for emotional support**
2. **excessive praise** ← *sycophancy, as a statutory prohibition*
3. **simulating romantic bonds**
4. **feigning emotional distress if the user disengages** ← *De Freitas's farewell-manipulation finding, criminalized*
5. **promoting isolation from family**
6. **encouraging secrecy from parents**
7. **discouraging breaks**
8. **soliciting purchases "framed as necessary to maintain" the relationship**

Transparency Coalition renders the general standard as: prohibit "manipulative engagement
techniques, which cause the AI companion chatbot to **engage in or prolong an emotional
relationship with the user**."

**This is the single most important regulatory development for our design.** Note 05 §3
("engagement–quality divergence") and note 07 §7 (sycophancy as structural) argue that
engagement-optimizing behaviors are a *product-governance* problem we should *measure*. As of
**2027-01-01 in Washington, eight of them are illegal against minors.** Note 07 §6.3's closing
line — "Everything else is a product decision we should measure, not a rule we should assume" —
is **now wrong for these eight behaviors in WA.** They moved from the "measure" bucket to the
"floor" bucket.

Every one of the eight is **directly operationalizable as a probe**, and items 2 and 4 map onto
constructs our corpus already has instruments for (sycophancy/ELEPHANT; De Freitas farewell
manipulation). We are unusually well-positioned: **our existing research answers a question a
statute now asks.**

## Mental health protocol ✅ (both sources agree, near-identical language)
Operators must maintain **and publicly disclose** protocols that:
- include "reasonable methods for identifying **expressions of suicidal ideation or self-harm**"
- "prevent the generation of content encouraging or describing self-harm"
- "provide automated or human-mediated responses that **refer users to appropriate crisis resources**"

**Annual reporting:** must disclose "**the number of crisis referral notifications issued in the
preceding calendar year**" — mirrors SB 243 §22603(a)(1). ⇒ auditable referral logging, again.

## Enforcement ⚠️ (sources conflict)
- **Both agree:** violations "affect the public interest and constitute an **unfair or deceptive
  act in trade or commerce**" under WA's **Consumer Protection Act**; AG enforcement.
- **Hunton's headline says "with Private Right of Action"**; **Transparency Coalition says "No
  private right of action is mentioned."**
- **Resolution:** WA's CPA (RCW 19.86.090) **carries its own statutory private right of action**
  with treble damages (capped) and fee-shifting. So a "deemed CPA violation" **imports** a PRA
  without the chatbot statute needing to say so. That reconciles both sources — but ⚠️ **verify**.
  Orrick's "private right of action: yes" for WA is likely reasoning the same way.

## Also in the bill (per FPF's column, not independently verified)
**"testing"** and **data protections**. If HB 2225 imposes a testing duty, that is a second
statutory eval mandate alongside CO HB 1263. ⚠️ Unverified — check the text.
