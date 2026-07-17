---
title: "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 (AI Basic Act) — Korea, in force 2026-01-22"
url: https://www.law.go.kr/lsInfoP.do?lsiSeq=268543
authors: 대한민국 국회 / 과학기술정보통신부 (MSIT); analysis via 신·김 (Shin & Kim) newsletter
year: 2026
type: regulation
language: ko
accessed: 2026-07-16
topic: regional-crosscheck
---

# Korea AI Basic Act — the world's second comprehensive AI law, already in force

Passed **2024-12-26** (260 for / 264 present). **시행일: 2026-01-22.** Second only to the EU.

## What actually binds a companion product

### 사전 고지 의무 (prior notification) — 법 제31조, 영 제23조
> **"제품·서비스가 고영향 AI나 생성형 AI에 기반하여 운용된다는 사실을 이용자에게 사전에 고지"**
> — *inform the user **in advance** that the product/service operates on the basis of high-impact or
> generative AI*

Permitted methods: on the product/service directly, in the **terms of service**, or a website
notice.

**This is a weaker duty than it first appears.** Disclosure **in the 이용약관 (ToS)** is expressly
allowed. Compare China's 标识办法, whose 显式标识 must be **可以被用户明显感知到** (obviously
perceptible) **in the interactive interface** — a ToS burial would fail there. **Korea's transparency
bar is the lowest of the three regimes.**

### 표시 의무 (marking)
> **"결과물이 생성형 인공지능에 의하여 생성되었다는 사실 표시"**

General generative output: **human-readable labels OR machine-readable watermarks** (either).
Deepfakes: **conspicuous, user-perceivable marking only** (watermark alone insufficient).

### 고영향 AI (high-impact AI) — 제2조 제4호
> **"생명, 신체의 안전 및 기본권에 중대한 영향을 미치거나 위험 초래할 우려가 있는 AI"**

Enumerated domains are employment, lending, and similar consequential decisions.

**A companion chatbot almost certainly does NOT qualify as 고영향.** It makes no decision about
employment, credit, or core rights. So the heavy 고영향 obligations do not attach — **only the
generative-AI transparency duties do.**

> **This is the sharpest regulatory contrast in the whole cross-check.** Korea — the country that
> produced the Luda incident — classifies a companion service as **low-risk**, subject only to
> "tell them it's AI." China wrote it **its own dedicated statute** with dependency, crisis,
> minors, elderly, and training-data duties.
>
> **Same product, same region, opposite regulatory theory.** Korea regulates AI by *decisional
> consequence*; China regulates it by *relational intimacy*. A framework built for one is blind to
> the other — and note which theory the Luda facts actually support. Luda harmed nobody's credit
> score.

### Penalties
| violation | 과태료 |
|---|---|
| 사전 고지 failure | **≤ ₩30,000,000** |
| 국내 대리인 미지정 (no domestic representative) | **≤ ₩30,000,000** |

Plus 시정명령 (corrective orders) for marking violations. **₩30M ≈ US$22k. Immaterial.**

### 계도기간 (grace period) — **the operative fact today**
**Minimum 1 year.** Investigations and 과태료 during the grace period are limited to grave cases
(fatalities, serious rights violations).

> **Today is 2026-07-16. The Act is in force but inside its grace period; full enforcement is
> deferred to at least 2027-01.** So Korea is, right now, the *permissive* jurisdiction — while
> China's 拟人화 Measures went live **2026-07-15 with no grace period**.

### 역외적용 (extraterritorial application) — 법 제36조, 영 제29조
Foreign AI operators must designate a **국내 대리인 (domestic representative)** if they meet any of:
- prior-year revenue **≥ ₩1 trillion**, **OR**
- prior-year **AI service** revenue **≥ ₩10 billion**, **OR**
- **≥ 1,000,000 daily Korean users** (averaged over the prior 3 months)

**Worth sizing against reality:** Zeta is at **>1.1M MAU**
([region-kr-zeta.md](region-kr-zeta.md)) — the threshold is **1M *daily* users**, so even Korea's
category leader plausibly sits under it. **These thresholds exempt almost everyone.** Unless we are
very large in Korea, the extraterritorial hook does not catch us.

## Net assessment for our platform

**Korea is the least binding of the three regimes**, which is counterintuitive given it hosts both
the field's landmark failure (Luda) and its most successful roleplay product (Zeta).

**The real Korean constraints are not in this Act:**
- **PIPA** — the instrument that actually punished Scatter Lab
  ([region-kr-pipc-scatterlab-decision.md](region-kr-pipc-scatterlab-decision.md)). Data protection,
  not AI law, did the work.
- **Copyright** — the webtoon platforms' criminal complaints against Zeta
  ([region-kr-zeta.md](region-kr-zeta.md)).
- **국정감사** — parliamentary pressure on minors, which moves products without moving law.

> **The lesson for our regulatory posture:** in Korea, **the AI-specific statute is the least of it.**
> The general-purpose laws (privacy, copyright) and the political process did the actual damage. Any
> compliance model that reads only the AI Act misses every mechanism that has ever actually hurt a
> companion product in Korea.

## Verification notes

- 시행일 (2026-01-22), passage (2024-12-26), the 제31조 고지/표시 duties, the 고영향 definition and
  scope, ₩30M 과태료, the ≥1-year 계도기간, and the 제36조 extraterritorial thresholds: from the
  **Shin & Kim law-firm newsletter**, corroborated on the headline items (시행일, ₩30M, generative
  notification duty, 계도기간, 10^26 FLOP high-impact compute threshold) by independent Korean press
  and explainers.
- **The statute text at law.go.kr was NOT fetched directly.** Article numbers (제31조, 제36조, 제2조
  제4호) and 시행령 references (영 제23조, 영 제29조) rest on the law firm's summary. **Solid
  secondary, not primary.**
- The **10^26 FLOP** compute criterion for 고영향/특수 obligations appears in press coverage; it is
  **not** what would capture a companion product and is not load-bearing here. **Not verified.**
- The assessment that a companion chatbot is **not** 고영향 is the law firm's reading plus **our
  inference**. It is a legal conclusion and should be confirmed with counsel before relied upon.
