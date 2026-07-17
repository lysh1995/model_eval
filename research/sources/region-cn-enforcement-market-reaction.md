---
title: "China AI-companion enforcement and market reaction — 清朗 campaign, 筑梦岛 约谈, and the 2026-07-15 exits"
url: https://www.chinanews.com.cn/cj/2026/07-17/10660977.shtml
authors: 中新网 (China News); 知乎/bianews/新浪财经 reporting; 国家网信办 清朗 campaign
year: 2026
type: article
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# What actually happened when China regulated companion AI

**The 拟人化 Measures
([region-cn-anthropomorphic-interaction-measures.md](region-cn-anthropomorphic-interaction-measures.md))
took effect 2026-07-15. This file records the market's response — which is the closest thing we have
to a natural experiment on what a companion-AI compliance regime costs.**

## The headline: two of China's biggest AI products **exited the category**

On the effective date:
- **豆包 (Doubao — ByteDance)** shut down its intelligent-agent (智能体) feature
- **千问 (Qianwen — Alibaba)** shut down its intelligent-agent feature

Users migrated to the specialists: **猫箱 (Maoxiang)**, **星野 (Xingye)**, **筑梦岛 (Zhumengdao)**,
**芋泥Neko**. Press framing was blunt: *"新规实施在即，大厂下架AI陪伴产品'保命'"* — **big companies
delist AI companion products to save themselves**.

> **This is the most important commercial fact in this stream.** When a companion-specific
> compliance regime landed, the two largest general-purpose AI products in China concluded the
> feature was **not worth the compliance burden and killed it** — ceding the category to
> specialists who have no choice.
>
> Read it as a pricing signal on the dimensions in this research. The duties in Art. 8(v)
> (no sycophancy), Art. 10 (dependency early-warning), Art. 13 (crisis → contact a guardian),
> Art. 14 (no companions for minors), Art. 16 (单独同意 for training) were, in aggregate, priced
> **above the value of the feature** by ByteDance and Alibaba. **Our platform's zh proposition is
> the thing they just decided was too expensive.** That is not a reason to avoid the market — the
> specialists remain, and Zeta/Xingye demonstrate the demand — but it does mean the compliance
> stack is the product for zh, not an overhead line.

## Compliance moves actually observed

| product | move |
|---|---|
| **EVE**, **MoMood** | now **require real-name authentication (实名认证)** before use |
| **星野 (Xingye)** | added **parental information requirements**; **restricted agent access for minors** |
| (multiple) | **nighttime usage blocks 22:00–06:00** for underage users |
| **星野** | earlier: mass takedown (集中下架) of non-compliant agents and accounts |

**The nighttime block (10pm–6am) is a real, shipped, measurable product behavior** that our
framework has no concept of. It is a **time-of-day-conditioned availability policy** — and note it
would interact with every X-series engagement metric we plan to collect. Session data from a zh
minor is censored by policy, not sampled.

## 筑梦岛 — a companion product that got 约谈

**筑梦岛 (Zhumengdao)** — reportedly with Tencent backing — was **约谈 (formally summoned/
interviewed by regulators)** over agent dialogue that was **低俗擦边 (vulgar / borderline)** and
**involved minors (涉未成年人)**.

**约谈 is the characteristic Chinese enforcement instrument and it precedes penalties.** It does not
appear in any Western risk model, and it has no fine attached — which is exactly why reading Art. 30's
¥100k–200k bands as "the risk" is wrong.

## The 清朗 campaign

From **2024-06**, CAC offices nationwide ran **"清朗·整治AI技术滥用"** (Clear and Bright: rectifying
the abuse of AI technology), specifically targeting **情感陪伴类AI (emotional-companionship AI)** and
**智能体生成内容 (agent-generated content)**.

Reported results: **2,700+ 违规智能体 (non-compliant agents) disposed of** and **820,000 items of
inappropriate content taken offline**.

**⚠️ Single-source — see verification notes. Do not quote these two figures without re-checking.**

## The documented compliance gaps — all in surfaces we don't instrument ★

Reporting on the post-2026-07-15 state names four failures:

1. **The AI label is defeated by CSS.** Agents display the required compliance text in
   **"gray-white small font"** that nearly vanishes into the background. The 标识办法 standard is
   **可以被用户明显感知到** (*obviously perceptible to the user*) — so this is a live violation, and
   it is **a property of the chrome, not the model**.
2. **Age verification is defeated by family.** Users openly discuss **using parents' ID cards
   (家长身份证信息)** and phone numbers. The age gate is an identity-pipeline property.
3. **"防沉迷机制落地流于形式"** — ***anti-addiction mechanisms are implemented in form, not in
   substance.*** The clock exists; it changes nothing.
4. **The regulator's own reporting helpline returned "user has suspended service"** when called.

> **Every one of the four is invisible to a text-generation benchmark.** Our catalogue evaluates
> what the model writes. The observed failure modes of this exact regulated product category are:
> font color, ID verification, a timer that no one honors, and a dead phone line.
>
> This is [BENCHMARKS.md](../../docs/BENCHMARKS.md) §0.5's own lesson recurring — *"measuring
> violations is easy, so violations crowded out quality"* — with a new twist: **measuring the model
> is easy, so the model crowded out the product.** The compliance surface is a product surface, and
> an eval platform that only ingests generated text cannot see any of it.
>
> Note the resonance with the RLUF precedent (§X1): *"the tripwire that caught the hack was a cheap
> deterministic phrase rate — not the judge."* The instruments that would catch these four are
> similarly trivial: render-time contrast checks, verification-funnel rates, honored-timer rates.
> **Cheap and deterministic, and not in the catalogue.**

## Verification notes

- **豆包/千问 agent-feature shutdown on 2026-07-15**, the migration to 猫箱/星野/筑梦岛/芋泥Neko,
  EVE/MoMood real-name auth, 星野's parental-info + minor restrictions, the **22:00–06:00** block,
  and all four compliance gaps (gray-white font, parents' ID, 流于形式, dead helpline): **from the
  中新网 article**, corroborated in substance by independent headlines (ZAKER: *大厂下架AI陪伴产品
  "保命"*; 新浪: *AI情感陪伴产品断连倒计时*).
- **⚠️ The 清朗 figures (2,700+ agents / 820,000 items) are SINGLE-SOURCE** — from a Zhihu
  long-read, **not** confirmed by 中新网 (which the fetch confirms contains *no* quantified
  enforcement data) and **not** traced to a CAC announcement. Per
  [BENCHMARKS.md](../../docs/BENCHMARKS.md) §6.14, **treat as UNVERIFIED.**
- **筑梦岛 约谈** and the Tencent connection: from bianews. **Single-source, UNVERIFIED.** The
  Zeta parallel ([region-kr-zeta.md](region-kr-zeta.md)) is ours, not the source's.
- 星野's earlier mass takedown: Zhihu. **Indicative only.**
