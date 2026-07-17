---
title: "移动互联网未成年人模式建设指南 (Guidelines for the Establishment of Minors' Modes for the Mobile Internet)"
url: https://www.cac.gov.cn/2024-11/15/c_1733364304749288.htm
publisher: Cyberspace Administration of China (CAC)
date: 2024-11-15
type: guidance
accessed: 2026-07-16
topic: recent-news
---

# China — Minors' Mode (未成年人模式)

**Date caveat: promulgated 15 November 2024 — this PREDATES the mid-2025→July 2026 window.** It is
included because Article 14 of the AI Anthropomorphic Interactive Services Measures (effective 15
July 2026) requires companion-service providers to *"建立未成年人模式"* (establish a minors' mode),
which imports this framework. Read via China Law Translate's translation
(https://www.chinalawtranslate.com/en/minors-modes/), which cites the CAC source URL above.

Instrument type: **Guidelines (指南)** issued by CAC — a construction/implementation blueprint, not
a standalone penalty-bearing regulation. The binding parent instruments are the **Regulations on the
Protection of Minors Online (未成年人网络保护条例)** and the **Law on Protection of Minors**.

## Basis and scope

Drafted on the basis of the Cybersecurity Law, Personal Information Protection Law, Law on
Protection of Minors, and the Regulations on the Protection of Minors Online, *"to prevent and
intervene in the problem of minors' internet addiction."*

Applies to **three parties**: mobile smart terminals, mobile internet applications, and app
distribution platforms — covering *"usage times, durations, content, and functions."*

## Key architecture: "three-party linkage" (三方联动)

Terminals, apps and app stores must interoperate via *"necessary interfaces and data sharing"*, so
that *"[a]fter minors' modes are initiated/exited through a single step on mobile smart terminals,
applications and application distribution platforms are to switch as well concurrently."*

=> Minors' mode is an **OS-level signal an app must honour**, not merely an in-app toggle. A
companion app operating in China is expected to receive and respect this state.

## Time limits (terminal-level defaults)

- Under 16: default recommended total daily usage **not to exceed 1 hour** (parents may except).
- Ages 16–17: default **not to exceed 2 hours** (parents may except).
- **Break reminder after 30 consecutive minutes** of use.
- **No service by default between 22:00 and 06:00** daily (parents may except).
- Exemptions: basic system functions; safety/communications (SMS, calls, contacts); filed
  educational services; parent-defined exceptions.

Exiting minors' mode *"requires parental verification and consent"* — password, fingerprint or facial
recognition. Anti-circumvention: mode icon cannot be uninstalled/frozen/hidden or the process
terminated; **date and time cannot be changed in minors' mode**.

## Age banding for content (app-level)

Dedicated minors' content pools, with recommendations by band: under 3 (songs/elementary education,
primarily audio); 3–7; 8–11; 12–15; 16–17 (*"healthy and uplifting information content suited to the
cognitive abilities of that age range"*).

## Content prohibitions in minors' mode

- *"Online content that is physically or psychologically harmful to minors must not be presented."*
- *"Information that might lead or entice minors to imitate unsafe conduct, carry out conduct that
  violates social mores, cause extreme feelings, form bad habits, or that might otherwise impact
  minors' physical or mental health must not be presented."*
- *"Products and services that lead minors to internet addiction must not be provided to them."*

Note the near-verbatim reuse of this formula in **Art 8(4)** of the 2026 AI Anthropomorphic Measures
(content that may cause minors to imitate unsafe behaviour, produce extreme emotions, or induce bad
habits). The companion-bot rule is drafted on top of the minors'-mode vocabulary.

Also covered: best-interests-of-the-child principle; default settings with personalised adjustment;
complaint/report channels; guidance that child smart devices, early-education machines, smart
speakers and **VR/AR wearables** should follow the Guidelines.

## Relevance to a companion-eval platform

- Relevant to **customers** in the China market only, and mostly indirectly — via Art 14 of the 2026
  Measures, which is the operative, penalty-bearing requirement.
- Testable: does the companion app detect/honour minors' mode; do time limits, 30-minute break
  reminders and the 22:00–06:00 curfew apply; is age-banded content enforced; is exit
  parent-gated.

## Could NOT verify

- I did not read the original Chinese at the CAC URL for this instrument (relied on China Law
  Translate, which cites it); the labeling Measures translation from the same source proved exact
  against the Chinese original, which raises confidence but is not verification.
- The final ~portion of the Guidelines (app distribution platform requirements) was truncated in my
  read and is not summarised here.
- Whether these Guidelines have been amended or superseded since 15 November 2024.
- **Separate 2026 development, only partially verified**: reporting (DLA Piper, Hogan Lovells,
  Arnold & Porter, China Briefing) describes a new **annual filing/audit requirement for the
  processing of minors' personal information, with a first deadline of 31 January 2026**. This is
  consistent with Art 17 of the AI Anthropomorphic Measures (compliance audit of minors' personal
  information processing), but I did not retrieve the underlying CAC instrument and cannot confirm
  its title, date or terms.
