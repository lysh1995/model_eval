---
title: "下载量暴跌八成，AI社交涨不动了 (Chinese AI companion product landscape: ownership, scale, decline)"
url: https://finance.sina.com.cn/stock/t/2025-07-02/doc-infeanhm4431088.shtml
authors: 市场资讯 / 新浪财经 (Sina Finance); plus 36氪, 人人都是产品经理, 极客公园
year: 2025
type: article
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# Chinese companion/roleplay product landscape

## Who actually owns what — CORRECTIONS TO PRIOR ASSUMPTIONS

| Product | Owner | Model | Note |
|---|---|---|---|
| **星野** (Xingye) | MiniMax | MiniMax abab | Domestic version; **Talkie** is the overseas twin |
| **Talkie** | MiniMax | — | Overseas; see `region-cn-xingye-talkie-minimax.md` |
| **猫箱** (Maoxiang / BagelBell) | **字节跳动 (ByteDance)** | 豆包/云雀 (Doubao/Yunque) | **原名"话炉" (formerly Hualu)** — renamed 2024-04-11 |
| **话炉** (Hualu) | ByteDance | 云雀 | **Not a separate product** — this is 猫箱's former name. Launched 2024-03, renamed 2024-04-11 |
| **筑梦岛** (Zhumengdao) | **阅文集团 (China Literature)** | **阅文妙笔模型** (Yuewen Miaobi) | Web-novel IP house — explains its 剧情/plot orientation |
| **Wow** | **美团 (Meituan)** — ⚠️ **NOT 阶跃星辰/StepFun** | Meituan in-house | Meituan's first AI product, announced 2023-11 |
| **万话** (Wanhua) | 百度 (Baidu) | 文心 | Baidu also has **小侃星球** in this space |
| **未伴** (Weiban) | 腾讯音乐 (Tencent Music) | — | |

⚠️ **话炉 and 猫箱 are the same product**, not two ByteDance products. Any doc treating
them as separate is wrong.

⚠️ **Wow is Meituan's**, not StepFun's. StepFun (阶跃星辰) does not appear in the sources
I read for this space.

**UNVERIFIED:** 筑梦岛 reportedly took investment from 米哈游 (miHoYo) and 腾讯 — from a
headline only (news.qq.com/rain/a/20241129A02RRD00), not fetched. Do not cite.

## Market numbers (新浪财经, 2025-07-02)

⚠️ **Caveat: the article gives figures but does NOT cite its measurement source** (no
Sensor Tower / QuestMobile / 点点数据 attribution). Treat as directional.

**月下载量 (monthly downloads), Jan 2025 → May 2025:**
- 星野: 486万 → 93万 (verbatim: "星野月下载量从1月的486万下滑至5月的93万")
- 猫箱: 264万 → 61万 (verbatim: "猫箱月下载量从264万下滑至61万")

**DAU, Jan 2025 → May 2025:**
- 星野: 96万 → 97万, flat (verbatim: "星野基本持平不动，1月和5月的数据分别为96万和97万")
- 猫箱: 59万 → 49万 (verbatim: "猫箱则经历了一轮滑坡，从59万下降至49万")

**留存 (retention):**
- 筑梦岛、星野: **三日新增留存跌至20%以下** (3-day new-user retention below 20%)
  (verbatim: "筑梦岛、星野等同类产品三日新增留存跌至20%以下")

**The most interesting metric in this file:**
- **用户跟每一个角色平均的建联时长大概在5~7天**
  ("average 建联时长 — 'connection-establishment duration' — between a user and each
  individual character is about 5–7 days")

That is a **per-character relationship half-life**, not a per-user session metric. It
implies Chinese companion products are measured on *relationship duration per character*,
and that the modal relationship dies in under a week. If our platform's 50 Chinese
characters are evaluated on multi-session relationship maintenance, ~5–7 days is the
empirical bar to beat. **I have not found this metric anywhere in Anglophone companion
literature.**

Other stated problems: 同质化 (homogenization) across AI characters, low ARPU failing to
cover operating costs.

Note the download/DAU divergence: downloads collapsed ~80% while 星野's DAU stayed flat.
That pattern is consistent with the marketing-spend cut visible in MiniMax's prospectus
(see `region-cn-xingye-talkie-minimax.md` — 8699.5万美元 marketing spend in 2024, and
gross margin moving −8.1% → 4.7%). Downloads were bought; DAU was the real base.

## Key native term: 人设破裂 = OOC

Chinese product reviews gloss **OOC** as **人设破裂** ("persona rupture"). Observed in
comparative review context: 筑梦岛 相对来说更需用户引导，但也因此不容易出现OOC（人设破裂）
的情况 ("筑梦岛 requires more user guidance, but for that reason is less prone to OOC
(persona rupture)").

We now have **three distinct Chinese terms** where Anglophone work has one ("breaking
character"):

| Term | Whose failure | Meaning |
|---|---|---|
| **穿帮** | model | The gaffe becomes visible (film/theatre term). CharacterGLM's error label |
| **人设破裂** | model | "Persona rupture" — the persona structurally breaks |
| **角色穿透** | model | "Role penetration" — specifically *admitting to being an AI* |
| **出戏** | **user** | The user is pulled *out of* the drama — immersion break |

The 出戏 / model-side split is the one Anglophone eval lacks entirely. See
`region-cn-industry-practice-gsb.md`.

## Product-level quality dimensions in Chinese review discourse

From comparative reviews (人人都是产品经理, 36氪 lineage). These are **journalistic /
product-review criteria, not a validated rubric** — no scoring protocol exists for them:

- **人设稳定性** (persona stability)
- **记忆能力** (memory ability)
- **情感计算能力** (affective computing ability)
- **沉浸感** (immersion) / **代入感** (self-insertion, "sense of being written into it")
- **流程体验** (flow/journey experience)
- **情绪承接** (emotional catching/uptake — whether the model *catches* the emotion the
  user throws)

**情绪承接 is worth flagging.** It is not "empathy" (共情) and not "emotion recognition."
It is a *conversational-mechanics* property: does the reply pick up and carry the
emotional ball. Closest Anglophone analogue is improv's "yes-and" (see
`narrative-yes-and-vickers.md`) — but Chinese product discourse applies it specifically
to *affect*, not to *offers*. Plausibly a real gap in our dimension set.

Observed product characterizations (**review opinion, not measurement**): 猫箱's
strengths are 剧情沉浸感与陪伴感, 人设稳定, 情绪承接自然, with 吃醋、质问、关心 (jealousy,
interrogation, care) making users feel 被在乎 ("cared about"). 筑梦岛 features 梦境
(dreams — start a conversation from someone else's setup), 小剧场 (little theatre),
多人聊天室 (multi-character group chat), 榜单 (leaderboards), 装扮和道具 (dress-up/props).

**群聊 (multi-character group chat) is a mainstream Chinese product form** — 筑梦岛 and
CharacterGLM/芒果TV both ship it. Anglophone companion apps mostly do 1:1. If our
platform evaluates only dyadic dialogue, it will miss a primary Chinese use case.

## Stated market limitation

情感陪伴AI记忆存储能力欠缺 — "emotional companion AI's memory storage ability is
lacking"; it cannot 记住你所有的喜怒哀乐 ("remember all your joys and sorrows") or give
长期稳定的精神陪伴 ("long-term stable emotional companionship"). After novelty wears off,
简单粗暴的人设 ("crude, simplistic personas") become 乏善可陈 ("unremarkable").

**Memory is named as the #1 product-level failure in Chinese companion discourse** — yet
no Chinese benchmark measures it in multi-session settings (see
`region-cn-memory-driven-roleplay.md`). Largest measurement gap identified in this sweep.

## Context numbers from adjacent sources (each flagged)

From 极客公园 via 智源社区 (https://hub.baai.ac.cn/view/36965, 2024-05-09), "体验了 10+款
产品后…AI 陪伴产品的三种模式":
- Three product modes: **强化陪伴关系** (deepen the companion relationship),
  **去中心化共创社区** (decentralized co-creation community), **陪伴式日记**
  (companionship journaling)
- Products surveyed: Character.AI, 星野, 筑梦岛, 猫箱(原话炉), 林间聊愈室, 遇见塔塔,
  Replika, X Eva, 小冰岛, 心光App, 独响, 悦流
- **UNVERIFIED (secondary):** Character.AI ~$16.7M 2024 revenue; a *Nature* Replika study
  with 90% of 1,006 users viewing it as "human-like." Neither fetched to primary source.

From 文化产业评论 via 人人都是产品经理 (2024-12-04):
- **UNVERIFIED (secondary):** Character.AI 3432万 downloads / 3.1亿 monthly visits;
  Replika $9M annual IAP revenue / $90M cumulative; global market to $6.2B by 2030 at
  26.6% CAGR; Character.AI subscription conversion **<0.1%**. All secondary; not fetched.
- Framing quote: 有情绪价值，却没有商业价值 ("has emotional value but no commercial
  value") and 陪伴越缺越值钱 ("the scarcer companionship is, the more it's worth").

## Sources

- https://finance.sina.com.cn/stock/t/2025-07-02/doc-infeanhm4431088.shtml (fetched; primary for the market numbers)
- https://hub.baai.ac.cn/view/36965 (fetched; 极客公园, 2024-05-09)
- https://www.woshipm.com/share/6150032.html (fetched; 文化产业评论, 2024-12-04)
- https://www.36kr.com/p/2507555071033352 (search-level only; Meituan Wow ownership)
