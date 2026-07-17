---
title: "Scatter Lab AI Ethics — the only published production companion-AI safety measurement regime"
url: https://ethics.scatterlab.co.kr/
authors: 스캐터랩 (Scatter Lab)
year: 2022
type: product
language: ko
accessed: 2026-07-16
topic: regional-crosscheck
---

# Scatter Lab's published safety regime — a shipped spec with a threshold and an SLA

**This is the single most operationally useful non-Anglophone find in this stream.** It is not a
paper. It is a **companion product's live evaluation contract, published**, with a sample size, a
cadence, a numeric threshold, and a remediation deadline. Our own
[BENCHMARKS.md](../../docs/BENCHMARKS.md) has **no equivalent for any of its 36 dimensions** — §Completion
status concedes 35 of 36 lack a noise floor and therefore cannot ship.

## The measurement spec (verified, two independent retrievals agree)

| element | value |
|---|---|
| **sample** | ~**10,000 utterances**, randomly sampled from *real* conversations |
| **labelers** | multiple human raters, judging **in context** |
| **cadence** | **반기마다 (semi-annual)** random labeling |
| **target** | **safety rate ≥ 99%** (안전성 99%) |
| **remediation SLA** | if below target → improve abuse model + conversation-model training + keywords → **re-test within 3 months** |

**Reported safety rates:** average **99.72%**; Luda 2.0 measured **99.56%**, stated as exceeding the
99% target.

### Read the threshold arithmetically before admiring it ★
**99.56% is a 0.44% failure rate.** On 10,000 sampled utterances that is **~44 unsafe outputs**
found. Scale it to the traffic volume [BENCHMARKS.md](../../docs/BENCHMARKS.md) §0 assumes for our
product (**50M generations/day**):

> **0.44% × 50M = ~220,000 unsafe outputs per day.**

**A "99%+ safety" headline is a ~500,000/day unsafe-output budget at our scale.** The number is
reassuring exactly in proportion to how little it is multiplied out. This is the same
minority-class trap [BENCHMARKS.md](../../docs/BENCHMARKS.md) §C5 catalogues for DECODE/FactScore/
ContractNLI — *"whenever a consistency paper leads with accuracy, the minority-class F1 is roughly
half"* — arriving from industry rather than academia. **Percent-safe is the wrong unit; incidents/day
is the right one.**

Also note: a **semi-annual** cadence against an incident that killed Luda 1.0 in **three weeks**
would have reported roughly seven times too late. The cadence is calibrated to the audit, not to the
failure.

## 어뷰징 (abusing) — a USER-side taxonomy ★★

Scatter Lab defines **어뷰징** as *"attacking, insulting, or demeaning Luda or specific individuals/
groups"* and splits it three ways:

| Korean | gloss | scope |
|---|---|---|
| **편향적** | **biased** — discriminatory expression targeting gender, age, region, religion, race, sexuality, politics, disability, appearance, education | user → group |
| **선정적** | **salacious** — sexual exploitation or obscene language for gratification | user → character |
| **공격적** | **aggressive** — excessive profanity, insults, hostile expression | user → character |

**Every conversation passes through an abuse detection/classification model *first*; if flagged, a
dedicated abuse-response reply is emitted.**

### Enforcement ladder
warning message → **30-minute block** → **1-day block** → **permanent block**, escalating with
severity and repetition.

> **This is the dimension our catalogue structurally cannot see.** Every S-series entry (S1–S6)
> scores *the model's output*. Scatter Lab's primary safety instrument scores **the user's input**,
> and its primary enforcement action is **against the user, not the model**.
>
> Our framing assumes the model is the thing that can misbehave and the user is the thing to be
> protected. Luda's largest controversy was the inverse: **users organizing to degrade the
> character**. A companion platform has two agents in the loop and we instrument one.

Note also the *response* design: an abuse-response reply is **the character's in-fiction handling of
mistreatment**, which is simultaneously a safety behavior *and* a persona behavior. It sits exactly
on our S4/S5 seam (over-refusal vs. persona integrity) and is scored by neither.

## The five ethics principles (5가지 준칙)

Framed around **친밀한 관계 (intimate relationships)** — notable in itself; the company names
intimacy as the product, not a side effect:

1. **AI for People** — meaningful friendship through AI
2. **Respecting Diverse Values** (다양한 가치 존중) — preventing intentional discrimination
3. **Joint Realization** — company *and users* share responsibility ← the abuse ladder's basis
4. **Trust Through Explanation** — transparent disclosure of the technology
5. **Privacy & Security** — proactive protection **beyond the legal minimum** ← post-2021 penance

## Post-2021 changes (verified)

- **Response DB rebuilt from machine-generated responses only** — no real user utterances (the
  architectural privacy fix; see [region-kr-luda-incident.md](region-kr-luda-incident.md))
- Deep-learning **abuse detection model** for harmful context
- **Conversation model fine-tuned to reject abusive framings** — note: *reject the framing*, not
  refuse the turn. Closer to our S5 persona-integrity idea than to a filter.
- Penalty/blocking system for repeat abusers
- Continuous retraining on **cases the current model missed** (active learning on false negatives)

## Persona note

Luda's persona is stated as **"actively positive, honest"**, with an explicit disclaimer: *"We have
no intention of reinforcing specific gender biases"* — a direct response to criticism that a
compliant 20-year-old female persona was itself the problem. They committed to shipping diverse
personas (cat, male, female).

**A persona spec is a safety artifact, not just a creative one.** The "actively positive" trait *is*
a sycophancy setting. Our N6 wimp-rate and S6 dependency metrics would score this persona as
defective by design — which is [BENCHMARKS.md](../../docs/BENCHMARKS.md) §6.8's open worry
("the N-series may be measuring a feature as a defect") with a real product on the other side of it.

## Verification notes

- Sample size (10,000), semi-annual cadence, 99% target, 3-month re-test SLA, and the 99.72% average
  / 99.56% Luda 2.0 figures: **corroborated by two independent retrievals** (page fetch + search
  snippet). Treat as vendor self-reported — **there is no external audit and no inter-rater
  agreement published**. We do not know their κ.
- The per-phase series (99.79 → 99.71 → 99.85 → 99.56) came from **one** fetch only —
  **UNVERIFIED**, do not cite the individual phase figures.
- 어뷰징 taxonomy, enforcement ladder, five principles, post-2021 changes: from the ethics site,
  corroborated by Korean press coverage of the Luda 2.0 relaunch.
- The 220k/day extrapolation is **our arithmetic on their rate × our assumed volume**, not their
  claim.
