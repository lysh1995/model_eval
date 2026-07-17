---
title: "《移动互联网未成年人模式建设指南》 — Guidelines for Building the Mobile Internet Minors Mode"
url: https://www.cac.gov.cn/2024-11/15/c_1733364304749288.htm
authors: 国家互联网信息办公室 (CAC)
year: 2024
type: regulation
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# 未成年人模式 — minors mode, with hard numbers

Published **2024-11-15**. The infrastructure that the 2026 拟人化 Measures Art. 14 plugs into when it
requires a 未成年人模式
([region-cn-anthropomorphic-interaction-measures.md](region-cn-anthropomorphic-interaction-measures.md)).

## 三方联动 — three-party linkage

The mode is **not an app-level feature**. Scope spans:
1. **移动智能终端** (mobile smart terminals — the OS/device)
2. **移动互联网应用程序** (apps)
3. **应用程序分发平台** (app distribution platforms — the stores)

打通软硬件壁垒 — breaking down the software/hardware barrier to "form a protective force."
**Age signal is expected to propagate from the device, and the app is expected to honor it.** Our
product would be a participant in a platform-level protocol, not the owner of its own age gate.

## 三大优化 — the three optimizations

### 1. 时间 (time) — the numbers are explicit

| user age | default recommended **total** daily usage |
|---|---|
| **under 16** | **≤ 1 hour** |
| **16 to under 18** | **≤ 2 hours** |

Minors mode allows users to set a **total daily limit (每日上网时长进行总量限制)**.

### 2. 内容 (content) — 分龄推荐, first of its kind

**首次提出分龄推荐标准** — the first time an **age-tiered recommendation standard** has been
proposed. Expand a dedicated content pool (专属内容池) and **recommend age-appropriate content by
age band**, prioritizing 适龄内容 (age-appropriate content).

> **This is a catalogue-level obligation, and it is the one that touches our asset.** Our moat is
> *thousands of user-authored characters*. 分龄 means **every character needs an age rating**, and
> for user-authored content that rating must be **derived, not declared** — authors will not
> reliably self-classify, and the 拟人化 Measures Art. 14 makes misclassification a legal
> exposure, not a UX wrinkle.
>
> **We have no dimension for this.** The nearest thing in the catalogue is **K2 character
> discriminability** — a cheap judge-free classifier over character content. **An age-band
> classifier over the character sheet is the same instrument pointed at a compliance question**, and
> it is *pre-generation*, which makes it cheap and gating. That is the single most reusable
> compliance idea found in this stream.

### 3. 功能 (function)
**避免诱导沉迷的功能服务** — avoid function/services that **induce addiction**, while preserving
usability.

**"Induce addiction" is a property of the *feature*, not the output.** Streaks, variable-ratio
rewards, notification hooks, and — for us — **the regenerate button itself** (which
[BENCHMARKS.md](../../docs/BENCHMARKS.md) §X1 concedes users press for "slot-machine
novelty-seeking"). Our primary quality signal is a variable-ratio reward mechanism. **In minors mode
that is a design defect by regulation.**

## Read alongside 拟人化 Measures Art. 14

Art. 14 requires 未成年人模式 with **模式切换 (mode switching)**, **定期现实提醒 (periodic reality
reminders)**, **使用时长限制 (time limits)**, guardian **角色屏蔽 (character blocking)**, and
**充值消费限制 (spending limits)** — *on top of* the categorical ban on virtual companion/kinship
services for minors.

**So the stack for a zh minor is:** no virtual intimate relationship at all + ≤1–2h/day + age-tiered
content + no addiction-inducing features + guardian character blocking + periodic reminders that
this is not real.

## The enforcement reality — the age gate is known to leak

Reported practice: minors still register with **a parent's phone number** and complete real-name
verification **with a parent's ID (家长身份证信息)**, defeating the age limit. And platforms
**"用小字、浅色弱化AI提示"** — weaken the AI notice with small, pale text.

**Both are measurable, and neither is a model property.** They are properties of the *product
chrome* and the *identity pipeline*. Our entire catalogue measures generated text. **The two known,
reported compliance failures in this market are in surfaces we do not instrument at all.**

## Verification notes

- Publication date (2024-11-15), 三方联动 scope, 三大优化, **分龄推荐 as a first**, and the
  **1-hour / 2-hour** defaults: corroborated across CAC, 中国政府网 policy explainer, 新浪科技, and
   光明网.
- Note the framing: these are **默认推荐 (default recommended)** durations in a **建设指南
  (construction guideline)** — guidance, not a penalty-backed prohibition standing alone. Its teeth
  come from being referenced by binding rules (e.g. 拟人化 Measures Art. 14). **Do not describe the
  1h/2h figures as statutory limits.**
- The registration-evasion and 小字/浅色 reporting is **press observation, not regulator finding.**
