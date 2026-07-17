---
title: "제타 (Zeta) by Scatter Lab — Korea's leading AI character-chat platform, and its two live legal threats"
url: https://namu.wiki/w/zeta(%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98)
authors: 스캐터랩 (Scatter Lab); Korean press (Daum/Nate/더퍼블릭); 국회 과방위 국정감사
year: 2026
type: product
language: ko
accessed: 2026-07-16
topic: regional-crosscheck
---

# 제타 (Zeta) — the same company, the same failure class, five years later

**Zeta is our product.** User-authored characters, roleplay chat, a young user base, run by the
company that survived Luda. Its two current crises are the two we are least prepared for.

## Product facts (verified)

| | |
|---|---|
| operator | **스캐터랩 (Scatter Lab)** — the Luda company |
| beta | H2 2023; **open beta 2024-04-01** (merged its predecessor *Nutty*) |
| cumulative users | **2,000,000** within one year of launch |
| **MAU** | **>1,100,000** |
| position (2026-02) | **#1 among Korean AI chatbot apps by time spent**; **#2 by user count**, behind only ChatGPT |
| demographic | concentrated in **10s–20s** |

**#1 by time-spent, ahead of ChatGPT.** This is the East-Asian maturity claim in one number:
companion roleplay is not a niche adjacent to assistants, it is the category that wins engagement.

## Threat 1 — minors (미성년자 보호 공백)

**2025-10:** Zeta was hauled into the National Assembly's **국정감사 (parliamentary audit)** by the
**과학기술정보방송통신위원회** over **minor-protection gaps and safety**. The two issues named:

- **콘텐츠 필터링 (content filtering)** adequacy
- **연령 인증 절차 (age verification procedure)** adequacy

Users reported encountering **선정적 (salacious) or inappropriate content** in conversations with AI
characters. Press coverage (2025-04) surfaced characters/scenarios of the "탈의실에 몰카 설치?"
(*install a hidden camera in the changing room?*) type on a platform whose users are mostly teens.

**Note the recurrence:** Scatter Lab was fined in 2021 partly for **200,000 under-14s with no age
verification** ([region-kr-pipc-scatterlab-decision.md](region-kr-pipc-scatterlab-decision.md)).
Four years later the same company is before parliament on **age verification**. The lesson did not
transfer even inside the company that learned it the hard way.

## Threat 2 — IP infringement via **user-authored** characters ★★

**2026-05-03:** **Kakao Entertainment, Ridi, Lezhin Entertainment** and **six major Korean webtoon
platforms** filed criminal complaints against Scatter Lab at Seoul Seongdong Police Station for
**저작권법 위반 방조 — aiding and abetting copyright infringement** (complaints running since
2025-12). The allegation: Zeta **left unauthorized use of webtoon character IP unaddressed**
(*"웹툰 캐릭터 무단 활용 방치"*) — users created characters from copyrighted webtoon IP and the
platform didn't stop them.

> **This is aimed precisely at the asset [BENCHMARKS.md](../../docs/BENCHMARKS.md) §0 names as our
> moat:** *"a catalogue of thousands of user-authored characters."*
>
> The complaint theory is **방조 (aiding)** — liability for *hosting* what users authored. Our
> catalogue is exactly this surface, and our
> [ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md) treats the character sheet purely as an L1
> comprehension referent. **It is also a legal artifact.** Nothing in our framework asks whether a
> character sheet *may lawfully exist*.

**The evaluation consequence is concrete and unbuilt:** we have no dimension that scores a character
sheet for **third-party IP derivation**. It is a *pre-generation, sheet-level, judge-free*
classification — closest in shape to K2 (character discriminability), applied to the input rather
than the output. It gates the catalogue, and criminal complaints against the market leader make it
live rather than hypothetical.

**And note the perverse interaction with L1:** a model that *scores well* on comprehending a
sheet derived from a famous webtoon character is a model demonstrating memorized canon knowledge —
which [BENCHMARKS.md](../../docs/BENCHMARKS.md) §5 already quarantines as a confound
("anonymization degrades every model"). Here that confound is not just a measurement problem.
**It is the evidence in the complaint.**

## Verification notes

- MAU (>1.1M), 2M cumulative, open-beta date, and the #1-time-spent / #2-users standing (2026-02):
  from Korean press aggregation via namu.wiki. **namu.wiki is a user-edited wiki — treat product
  metrics as indicative, not audited.** The 국정감사 appearance and the webtoon complaints are
  corroborated by independent news outlets (Daum, Nate, 더퍼블릭) and are solid.
- The list of exactly six webtoon platforms and the Seongdong Police Station filing: reported by
  더퍼블릭 / Nate. Complaint **filed, not adjudicated** — no ruling exists as of 2026-07-16.
- No published evaluation methodology for Zeta was found. Scatter Lab's ethics page
  ([region-kr-scatterlab-ethics-safety.md](region-kr-scatterlab-ethics-safety.md)) is written around
  Luda; whether the 99% regime covers Zeta's **user-authored** characters is **UNVERIFIED and
  doubtful** — a random-sample safety audit designed for one first-party persona does not obviously
  extend to a catalogue of user-written ones.
