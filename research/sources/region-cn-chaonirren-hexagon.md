---
title: "AI大模型怎么"走心"？聆心智能CharacterGLM交卷！六边形能力加持 (超拟人 'super-anthropomorphic' model category and the 六边形能力 framework)"
url: https://zhidx.com/p/388605.html
authors: 智东西 (Zhidx) reporting on 聆心智能 (Lingxin Intelligence) / 智谱AI / 清华大学 COAI
year: 2023
type: article
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# 超拟人 (super-anthropomorphic) as a Chinese product category + the 六边形能力 framework

Published **2023-07-25** by 智东西, covering the CharacterGLM product launch.

**Distinct from our existing `rp-bench-characterglm.md`**, which covers the CharacterGLM
*paper* and its 6 *evaluation* dimensions (一致性/人性化/参与度/质量/安全性/正确性). This
file covers the *product-level capability taxonomy* and the **超拟人 category concept** —
which is the Chinese-specific material.

Orgs: **聆心智能** (Lingxin Intelligence, spun out of Tsinghua CS), **智谱AI** (provides
the GLM base model), **清华大学交互式人工智能课题组 (COAI)**.

## 超拟人 (chāo nǐrén) — "super-anthropomorphic"

**This is the headline answer to the East/West divergence question.** In China,
"anthropomorphic" is not a research construct buried in a rubric — **it is the name of
the product category**. Vendors ship "超拟人大模型" (super-anthropomorphic large models)
as a marketing category.

There is no Anglophone equivalent. No US vendor markets a "super-human-like model";
Character.AI/Replika market *characters* and *relationships*, not human-likeness as a
model property. The Chinese framing makes 拟人度 a **first-class, named, competed-on
axis**.

> **Decisive corroboration:** 拟人化 is not merely a marketing or benchmark term in China
> — it is a **legal category**. See `region-cn-anthropomorphic-interaction-measures.md`:
> the CAC's 《人工智能拟人化互动服务管理暂行办法》 ("Interim Measures for the
> Administration of AI **Anthropomorphic Interactive Services**", Decree No. 21)
> regulates 拟人化互动服务 as a named service class. So the concept runs the full stack:
> **product category (超拟人) → benchmark dimension (人性化/拟人度) → regulated legal
> category (拟人化互动服务)**. No Anglophone jurisdiction or vendor treats
> "anthropomorphism" as a named object at any of those three levels. This is the
> strongest evidence for a genuine East–West conceptual divergence found in this sweep.

Definition per coverage: models with 更多的人情味儿 ("more human flavor/warmth"),
offering 千人千面的AI形象 ("a thousand faces for a thousand people" — i.e. per-user
persona differentiation), meeting 聊天、陪伴的情感需求 ("emotional needs for chat and
companionship"), breaking through AI大模型与人类的情感交流困难.

The 超拟人 label is also applied to voice — MiniMax markets 超拟人、多情感 speech models
(speech-01). So 超拟人 spans text and speech as an industry-wide category term.

### 情商 (EQ) vs 智商 (IQ) framing

Chinese industry explicitly frames companion models as **EQ-optimized** in contrast to
mainstream **IQ-optimized** models. Search-level sourcing states current LLM evaluation
focuses on 智商 ("IQ") dimensions while 超拟人 models enhance 情商 ("EQ"). This
IQ/EQ split is a standard Chinese industry rhetorical frame with no direct Anglophone
counterpart (the nearest is "EQ-Bench", which is a benchmark, not a category).

## 六边形能力 (hexagonal capability) — the product taxonomy

Six named dimensions. Note this is a **capability/design taxonomy, not a scored rubric** —
no scoring protocol is published for it.

| # | Dimension | Description (from source) |
|---|---|---|
| 1 | **人格** (personality) | 通过拟人化提示词实现角色、风格设定 — attitude, 性格 (disposition), 观点 (viewpoints), 语言风格 (language style) |
| 2 | **知识** (knowledge) | Internet retrieval + private DB forming 角色记忆 ("character memory"); explicitly framed as avoiding 灾难性遗忘 ("catastrophic forgetting") |
| 3 | **能力** (ability) | Human-logical reasoning **and 非语言信息表达能力** — non-verbal expression (动作表情 / actions and expressions) |
| 4 | **社会化** (socialization) | 基于共情对话经验 (empathetic dialogue experience) → 千人千面; generates 恰当共情回复 ("appropriate empathetic replies") keyed to 实时情绪 (real-time emotion) |
| 5 | **成长性** (growth / developmental capacity) | 让AI角色得到迭代成长 — "letting the AI character grow iteratively" |
| 6 | **价值观** (values) | Replies conform to human 价值观 and 道德伦理 (ethics) |

### The two genuinely novel dimensions

**成长性 (growth)** — the character *changes over time*. I found **no Anglophone
roleplay benchmark that scores this**. Anglophone persona work treats drift as pure
failure (persona drift, persona collapse — see our `multiturn-persona-drift.md`,
`multiturn-persona-collapse-homogenization.md`). Chinese product framing treats
*directed* change as a **feature**.

This is a sharp conceptual distinction our platform may need: **drift (bad) vs. growth
(good)** are both "the character is different than before." Any metric that penalizes
all change cannot express 成长性. Distinguishing them likely requires knowing whether
the change is (a) consistent with prior state as a *development* and (b) responsive to
relationship history. Flagging as an open design question — I found **no published
operationalization** of 成长性 by anyone. **UNVERIFIED that anyone actually measures it.**

**价值观 (values)** — pairs with SuperCLUE-Role's **三观** (worldview/life-view/
values). Two independent Chinese frameworks make character *values* a named dimension.
Anglophone benchmarks fold this into either "safety" (does it say bad things) or
"persona consistency" (does it contradict the card). Neither captures "does this
character reason from the right value system."

## Numbers — VENDOR CLAIMS, NOT INDEPENDENTLY VERIFIED

⚠️ Everything below is **a vendor claim reported in launch coverage**, not an
independent evaluation. 智东西 is a tech-media outlet reporting a product launch.

- **UNVERIFIED VENDOR CLAIM:** "ELO测评排名：CharacterGLM超越Claude、GPT-4成为积分榜第一名"
  (CharacterGLM tops an ELO leaderboard above Claude and GPT-4). **No leaderboard
  identity, rater pool, sample size, or CI given. Do not cite this as a result.**
- **UNVERIFIED VENDOR CLAIM:** 角色一致性、趣味性 rank first; 安全性 second to GPT-4;
  生成质量 comparable to GPT-4. No numbers attached to any of these.
- Stated specs (vendor-reported): 参数量 数百亿 ("tens of billions"); 上下文长度 最大32K
  (~4–5万汉字); **情绪识别粒度 32种情绪 (32-emotion recognition granularity)**.

The **32种情绪** spec is notable regardless of verification: Anglophone companion work
typically uses coarse affect (valence/arousal, or Ekman-6). A 32-category emotion
taxonomy as a *product spec* signals how central fine-grained affect recognition is to
the Chinese companion stack. **I did not find the taxonomy's contents** — worth chasing.

Related model per search-level sourcing (**UNVERIFIED**): **Emohaa** (~66B params,
psychological support/companionship) and CharacterGLM (~6.3B) described as 聆心智能's
超拟人 line alongside OPD-2. Parameter counts are from a search summary, not a primary
source — do not cite.

## Commercial deployments named

- **芒果TV** (Mango TV) — recreated 6 characters from 《大宋少年志》 as a group chat
  (群聊), characters interact freely per 剧情和人设 (plot and persona)
- 数字栩生 — digital-human interaction system
- 洪恩 — 洪恩AI问答2.0 (children's education, shipped)
- Own product: **AiU** (AI interest community, in closed beta at time of writing)

The 芒果TV case is notable: **IP-licensed character replication for a streaming
platform**, plus multi-character group chat. Group-chat roleplay (群聊) is a much more
prominent product form in China than in Anglophone companion apps.

## Sources

- https://zhidx.com/p/388605.html (智东西, 2023-07-25)
- Corroborating (search-level only, not fetched): 中国日报网
  https://tech.chinadaily.com.cn/a/202307/31/WS64c77b4ca3109d7585e47509.html
