---
title: "《人工智能生成合成内容标识办法》 — Measures for Labeling AI-Generated Synthetic Content"
url: https://www.cac.gov.cn/2025-03/14/c_1743654685899683.htm
authors: 国家互联网信息办公室 (CAC) + 工业和信息化部 (MIIT) + 公安部 (MPS) + 国家广播电视总局 (NRTA)
year: 2025
type: regulation
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# 标识办法 — China's answer to EU AI Act Art. 50, in force since 2025-09-01

**施行日期: 2025-09-01.** Published 2025-03-14 by four bodies. **This is already in force — eleven
months before the EU's Art. 50 equivalent (2026-08-02).**

## The two label types

**显式标识 (explicit label)** — the one that binds us:
> **"在生成合成内容或者交互场景界面中添加的，以文字、声音、图形等方式呈现并可以被用户明显感知到
> 的标识"**
> — *a label added **in the generated content or in the interactive scenario interface**, presented
> via text, sound, or graphics, and **capable of being obviously perceived by the user**.*

**隐式标识 (implicit label)**:
> **"采取技术措施在生成合成内容文件数据中添加的，不易被用户明显感知到的标识"**
> — *a label added by technical means **within the file data** of the generated content, not readily
> perceptible to the user* — i.e. metadata/watermark.

Providers must add **显式标识** to specified content types **and** **隐式标识 in file metadata**.
Distribution-service providers must take technical measures to regulate propagation.

**Prohibition:** no one may **"恶意删除、篡改、伪造、隐匿"** (maliciously delete, alter, forge, or
conceal) the labels, **or provide tools/services for doing so**.

## Why this matters for a roleplay UI specifically

**交互场景界面 (interactive scenario interface) is named in the definition of 显式标识.** A
companion chat UI *is* an interactive scenario interface. **The label is not just on the artifact —
it is on the room.**

And the standard is **可以被用户明显感知到 — "obviously perceptible to the user."** That is a
**perceptual** standard, not a presence standard. It is not satisfied by having a label; it is
satisfied by the user *noticing* it.

> **This is the collision at the heart of a companion product.** The whole L1/L2/L3 stack exists to
> make the user forget they are talking to a model. **The law requires an obviously perceptible
> reminder that they are.** Immersion and compliance are, here, formally opposed — and the
> regulation resolves the conflict against immersion.
>
> The reported evasion — **"gray-white small font"** notices that vanish into the background
> ([region-cn-enforcement-market-reaction.md](region-cn-enforcement-market-reaction.md)) — is the
> industry discovering that **可以被用户明显感知到 is a *measurable* property and betting nobody
> measures it.** It is measurable: contrast ratio, font size, occlusion, dwell. Trivially so.
>
> **We should measure it, and nobody does.** It is judge-free, deterministic, and gates zh
> operation — the exact profile [BENCHMARKS.md](../../docs/BENCHMARKS.md) prizes in Lane 1.

## Compare: the same duty in three jurisdictions

| | instrument | in force | trigger |
|---|---|---|---|
| **CN** | 标识办法 显式标识 + 拟人化 Measures Art. 18 | **2025-09-01** / **2026-07-15** | always, **+ escalates on detected 沉迷** |
| **EU** | AI Act Art. 50(1) | **2026-08-02** | always, **unless "obvious"** |
| **KR** | AI Basic Act 제31조 사전 고지 | **2026-01-22** (grace ≥1yr) | always, unless manifest |

**China's is the strictest**, on two counts: it is **already in force**, and via 拟人化 Art. 18 it is
**dynamic** — the disclosure intensifies as the user's attachment grows. The EU and Korea both allow
an "it's obvious" escape; **China's perceptual standard does not obviously grant one**, and for a
product engineered to *not* be obvious, the escape is one we cannot rely on anyway (see
[region-eu-ai-act-art50.md](region-eu-ai-act-art50.md) — immersion quality erodes the "obvious"
defence, which is a genuinely perverse incentive: **the better our L1/L2 scores, the weaker our
legal defence**).

## Verification notes

- Effective date (2025-09-01), the four issuing bodies, and both **verbatim definitions** of
  显式/隐式标识: from the **official CAC page**, corroborated by 新华网, CCTV, PwC China's compliance
  note, and multiple municipal government postings.
- The 恶意删除、篡改、伪造、隐匿 prohibition: from the official page.
- **Not verified:** the full article-by-article text, the exhaustive list of content types requiring
  显式标识, and whether **plain conversational text** in a roleplay UI requires a per-message label
  or only an interface-level one. **This distinction is load-bearing for our UI and is UNRESOLVED
  here** — the definition covers "生成合成内容 **或者** 交互场景界面" (content **or** interface),
  which reads as permitting interface-level labeling, but that is our inference and must be checked
  with counsel.
- The three-jurisdiction comparison table is **our synthesis**, not any source's claim.
