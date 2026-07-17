---
title: "PIPC sanction against Scatter Lab (스캐터랩) — first application of Korea's PIPA to an AI system"
url: https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&mCode=C020010000&nttId=7298
authors: 개인정보보호위원회 (Personal Information Protection Commission, PIPC), Republic of Korea
year: 2021
type: regulation
language: ko
accessed: 2026-07-16
topic: regional-crosscheck
---

# PIPC v. Scatter Lab, 2021-04-28 — the training-data consent precedent

**The first case anywhere applying a general data-protection law to AI training data.** It is a
direct precedent for the production-data collection contract in
[BENCHMARKS.md](../../docs/BENCHMARKS.md) §4.

## The sanction (verified, arithmetic-checked)

| item | amount |
|---|---|
| 과징금 (penalty surcharge) | **5,550만원** (₩55.5M) |
| 과태료 (administrative fine) | **4,780만원** (₩47.8M) |
| **total** | **1억 330만원** (₩103.3M ≈ **US$92,900**) |

Verbatim (ZDNet, 2021-04-28):
> "인공지능(AI) 챗봇 '이루다' 개발사인 스캐터랩에 대해 개인정보보호법 위반에 따른 **과징금
> 5천550만원, 과태료 4천780만원**이 부과됐다."

**Arithmetic check: 5,550 + 4,780 = 10,330만원 = 1억 330만원 ✓** — reconciles with the total in the
PIPC release and all press. (Noted because one fetch rendered the surcharge as "5,555만원", which
does *not* reconcile. Per [BENCHMARKS.md](../../docs/BENCHMARKS.md) §6.14, numbers were re-checked.)

Plus **시정조치 명령** (corrective order). **8 separate PIPA violations** (총 8가지 개인정보
보호법 위반행위).

## What they actually did wrong

Scatter Lab operated two other apps — **텍스트앳 (Text At)** and **연애의 과학 (Science of Love)** —
which ingested users' KakaoTalk conversation logs to analyze their romantic relationships. It then
used that corpus to build Luda.

| | |
|---|---|
| KakaoTalk messages used | **~9.4 billion** (94억여건) |
| users whose data was used | **~600,000** |
| period of use for Luda | **2020-02 → 2021-01** |
| PII stripped | **none** — names, phone numbers, addresses were left in |

### The consent finding — this is the load-bearing part
The privacy policy contained a **"신규 서비스 개발" ("new service development")** clause. PIPC held
this **did not amount to explicit consent**, because users could not reasonably have anticipated
that their private KakaoTalk messages would be reused to build a different product.

> **A generic "we may use your data to improve/develop services" clause does not authorize training
> a new model on intimate conversation logs.**

### Children
**200,000+ children under 14** had data collected without parental consent — the apps performed
**no age verification** at signup.

### The GitHub disclosure
2019-10 → 2021-01, Scatter Lab published a dataset to GitHub containing **1,431 KakaoTalk messages**
including **22 real names** and **34 locations**, plus gender and relationship status. Held to
violate **PIPA Art. 28-2(2)**:
> "A personal information controller shall not include information that may be used to identify a
> certain individual when providing pseudonymized information to a third party."

**Pseudonymization was attempted and was held insufficient.** Surnames and district names were
stripped; it still identified people.

## Direct read-across to our platform

[BENCHMARKS.md](../../docs/BENCHMARKS.md) proposes mining **~5M regenerate events/day** plus
production chat logs as our primary quality signal (X1/Q1), and §6.4 notes "the collection contract
must ship before any of §4 is real."

**Scatter Lab is precisely the failure mode of getting that contract wrong**, and every element
rhymes:

| Scatter Lab | us |
|---|---|
| data collected for app A, used to build product B | data collected to *serve chat*, used to *evaluate/train* |
| generic "new service development" consent | a consent clause not yet written |
| no age verification | our minors posture undefined |
| intimate conversation logs | **companion chat is the most intimate log category there is** |
| pseudonymization held insufficient | our anonymization plan unspecified |

**The collection contract must name evaluation and model development as specific, separately
consented purposes, at collection time.** Retrofitting consent is what got fined.

## Verification notes

- Fine breakdown: verbatim from ZDNet, arithmetic-reconciled against the PIPC release total.
- The PIPC press release page confirms the ₩103.3M total and the "first enforcement against an AI
  company" framing, but the itemized decision is in an .hwp/.pdf attachment **not retrieved**.
  The full 8-violation list is therefore **UNVERIFIED**; only Art. 28-2(2) is confirmed by name.
- 9.4B messages / 600k users / 200k children / 1,431-message GitHub leak: corroborated across FPF,
  The Register, and Korean press.
