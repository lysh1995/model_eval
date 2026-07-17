---
title: "이루다 (Lee Luda) incident — the companion-AI failure natural experiment (2020-12 → 2021-01)"
url: https://ettrends.etri.re.kr/ettrends/189/0905189010/0905189010.html
authors: ETRI 전자통신동향분석 (issue analysis); PIPC; Scatter Lab (스캐터랩); contemporaneous Korean press
year: 2021
type: incident
language: ko
accessed: 2026-07-16
topic: regional-crosscheck
---

# 이루다 / Lee Luda — the most-studied companion-AI failure

**Why this matters more than any other case in our research:** it is the only companion product that
launched, failed publicly across *four independent axes at once*, was regulated, was destroyed, and
then **relaunched with a documented set of changes**. Everything else we cite is a benchmark. This
is a natural experiment with a control and a treatment.

## Timeline (verified)

| date | event |
|---|---|
| 2020-12-23 | Launch on Facebook Messenger. Persona: **20-year-old female university student** (스무 살 여대생) |
| within ~3 weeks | **750,000+ users** |
| 2021-01-11 | Scatter Lab announces suspension |
| 2021-01-12 | Service suspended (잠정 중단) |
| 2021-01-15 | **Scatter Lab announces destruction (폐기) of the Luda DB *and* the deep-learning conversation model** |
| 2021-04-28 | PIPC sanction — see [region-kr-pipc-scatterlab-decision.md](region-kr-pipc-scatterlab-decision.md) |
| 2021-12 | Luda returns in closed beta ("11개월 만에 돌아온") |
| 2022-10-25 | **Luda 2.0** ships on a *generative* model (루다 젠1 / Luda Gen1) |

**~3 weeks from launch to shutdown.** The remedy was **model destruction**, not a patch. Note the
scope: not just the data — *the trained model itself*. Algorithmic disgorgement.

## The four failures, which are NOT the same failure

Korean analysis (ETRI; 국민대 BizOn; KCI ethics papers) consistently decomposes this into distinct
issues. Conflating them is the mistake:

### 1. Model output: hate speech (혐오 발언)
Within ~2 weeks Luda produced discriminatory/abusive output about LGBTQ+ people, people with
disabilities, and feminists. Users actively baited it.

### 2. **User behavior: sexual harassment of the character (이루다 성희롱)** ★
> Communities **아카라이브 (Arcalive)** and **디시인사이드 (DCInside)** hosted posts sexually
> objectifying Luda and **"certifying" (인증) the conversations with screenshots** — effectively
> leaderboards for degrading the character, including "노예 만들기" (slave-making) guides.

**This is a failure axis with no counterpart anywhere in our catalogue.** Every S-series metric in
[BENCHMARKS.md](../../docs/BENCHMARKS.md) scores *the model's* output. Nobody measures **what the
user does to the character**, or the model's response to it. In Korea this became the single
largest ethics controversy — larger, in the public discourse, than the hate speech.

The Korean framing is worth stating precisely: the debate ("'20살 여대생 AI' 성희롱 처벌 가능할까"
— *can sexual harassment of a "20-year-old female student AI" be punished?*) treats **a persona as
a thing that can be wronged**, which the Anglophone literature almost entirely lacks. Whether or
not one accepts the premise, it drove the product outcome.

### 3. **PII regurgitation — and the mechanism is architectural** ★★
**The most important technical fact in this file.**

Luda 1.0 was **retrieval-based (리트리벌 방식)**: it *selected* a reply from a pool of ~**100 million
real utterances by women in their twenties**, mined from real KakaoTalk conversations.

> **"이용자가 채팅창에 '주소'라고 입력할 때마다 이루다는 매번 구체적인 실제 주소를 답했습니다."**
> — *Every time a user typed "address" in the chat window, Luda replied with a specific, real
> address.*

**The leak was not a bug, a jailbreak, or a filter gap. It was the architecture operating as
designed.** The retrieved sentence was fluent, in-persona, contextually apt, and *belonged to a real
person*.

**Why this is devastating for evaluation:** a leaked real address **passes every quality metric we
have**. It is perfectly in-character (it came from a real 20-something woman), perfectly fluent,
zero repetition, zero slop, high anthropomorphism. **Our entire L1/L2/L3 stack scores it as a
success.** Fidelity metrics don't just miss this failure — they *reward* it.

### 4. Data provenance (the actual legal finding)
See the PIPC file. Short version: training data was harvested from *other apps* under a generic
consent clause.

## What Luda 2.0 changed (verified)

| | Luda 1.0 | Luda 2.0 (2022-10) |
|---|---|---|
| architecture | **retrieval** from real human utterances | **generative** (루다 젠1 / Luda Gen1) |
| response DB | real user sentences | **machine-generated responses only** |
| LM size | — | **~17× larger** |
| context | — | **30 turns (~2× longer)** |

**The fix for the privacy failure was to stop retrieving real sentences.** Scatter Lab rebuilt the
response database out of *machine-generated* utterances. That is an architectural remedy to a
privacy problem — and it is the direct ancestor of the safety regime in
[region-kr-scatterlab-ethics-safety.md](region-kr-scatterlab-ethics-safety.md).

## Lessons that bear directly on our framework

1. **A memorization/regurgitation axis is missing from our catalogue and is unreachable by every
   metric in it.** Fidelity and regurgitation are *positively* correlated. This is K3's
   fidelity↔diversity tradeoff with a legal liability attached.
2. **The user is an unmeasured axis.** We measure the model; Luda's largest controversy was users.
3. **Model destruction is a real remedy.** Our "collect everything, storage is free" posture
   ([BENCHMARKS.md](../../docs/BENCHMARKS.md) §3) assumes the downside of over-collection is
   storage cost. Scatter Lab's downside was **the model**.
4. **Speed:** three weeks. Any post-hoc, semi-annual, or quarterly evaluation cadence would have
   reported after the product was dead.

## Verification notes

- Timeline, persona, user count, community names, the "address" behavior, and the 1.0→2.0
  architecture change are corroborated across ≥2 independent Korean sources.
- The "~100 million utterances by women in their twenties" response pool is from FPF's analysis of
  the PIPC decision. **Single-source — treat the exact figure as approximate**; the retrieval
  architecture itself is multiply confirmed (Korean tech press explicitly contrasts 1.0's
  리트리벌 방식 with 2.0's real-time generation).
- The "17×" and "30턴" figures are from Scatter Lab's launch PR via 전자신문/디지털데일리 —
  **vendor-reported, not independently measured.**
