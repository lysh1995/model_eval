---
title: "聊一聊做角色扮演大模型的经验 (Experience building roleplay LLMs — Chinese industry practice)"
url: https://developer.volcengine.com/articles/7439940856175394853
authors: 何先生 (originally a 知乎 column post; mirrored on 火山引擎开发者社区 / ByteDance Volcano Engine)
year: 2024
type: article
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# Chinese industry practice for roleplay LLM evaluation

Practitioner post. **The most operationally useful Chinese source I found** — it
describes what a Chinese roleplay-model team actually does to evaluate, as opposed to
what a benchmark paper proposes.

**Date: not stated on page. UNVERIFIED.**

## The actual evaluation loop (this is the finding)

> 自己熟悉的 case 评估集，200个左右就可以，熟悉到可以背下来
> ("your own familiar case eval set, ~200 is enough, familiar enough that you can
> recite them from memory")

Then two production metrics:

- **上线前的 GSB** (pre-launch GSB)
- **上线后的人均对话轮数** (post-launch average dialogue turns per user)

### GSB (Good / Same / Bad)

A pairwise side-by-side human comparison protocol — for each prompt, a rater marks the
new model as Good (better), Same, or Bad (worse) vs. baseline. Reported as a GSB ratio
or (G−B)/total. Originates in Chinese search/ranking evaluation (Baidu-lineage) and is
the **default pre-launch gate across Chinese LLM teams**.

Functionally close to Anglophone side-by-side/Arena preference testing, but note the
difference: GSB has an **explicit "Same" bucket** as a first-class outcome. Arena-style
Elo mostly forces a winner or treats ties as a nuisance. For companion products where
most changes are neutral, an explicit tie bucket is arguably better instrumentation —
it separates "no regression" from "no signal."

### 人均对话轮数 (average dialogue turns per user)

The single post-launch north-star quality proxy named. Note what this implies: Chinese
practice treats **engagement depth as the online proxy for roleplay quality**. This
should raise an obvious flag for a companion product — it is the same metric whose
optimization drives the engagement/wellbeing concerns documented in our
`product-chai-rlhf-engagement.md` and `safety-*` files. Worth naming explicitly as a
tension in the platform design.

## Quality dimensions named (original Chinese)

1. **角色一致性** (character consistency) — 模型有角色一致性，甚至要有「自我意识」
   ("the model has character consistency, and should even have 'self-awareness'")
2. **沉浸感** (immersion) — 更优秀的角色扮演模型应当让用户有强烈的沉浸感
   ("a better roleplay model should give the user a strong sense of immersion")
3. **人设完整度** (persona completeness) — 不仅仅是不脱离人设，甚至是主动引导用户去演绎
   ("not merely *not departing* from the persona, but actively **guiding the user** to
   perform") — note this is a *proactivity* requirement folded into persona quality
4. **对话质量** (dialogue quality) — 如果模型聊的内容枯燥重复，经常把天聊死
   ("if the model's content is dull and repetitive, it often **把天聊死**")
5. **用词水平** (word-choice level) — 角色扮演不仅要求模型表达正确，还需要用词「高级」
   ("roleplay requires not just correct expression but **'高级' (sophisticated/elevated)
   word choice**")

## Native vocabulary worth adopting

| Term | Literal | Meaning |
|---|---|---|
| **AI感** | "AI-feel" | The perceptible flavor of assistant-ness. 如果让它们来直接演戏，往往会表现出「AI感」 |
| **老好人助手** | "nice-guy assistant" | The over-aligned, agreeable default persona to be trained away |
| **机械感** | "mechanical feel" | Robotic quality from 简单重复的高频词 (repeated high-frequency words) |
| **出戏** | "exit the drama" | **The USER being pulled out of immersion** |
| **入戏** | "enter the drama" | The user/actor being absorbed into the role |
| **把天聊死** | "chat the sky to death" | Killing the conversation dead — a reply that leaves nowhere to go |
| **高级 (用词)** | "elevated" | Sophisticated diction; explicitly a scored quality |

### The 出戏 insight — a real East/West divergence

Chinese discourse has a distinct term for the **user's** immersion breaking (出戏),
separate from the **model** breaking character (穿帮 / 角色穿透).

Anglophone roleplay benchmarks almost exclusively measure the model-side property
(consistency, OOC rate). Chinese product discourse centers the **user-side experiential
state** — 沉浸感 (immersion), 代入感 (self-insertion), 出戏 (immersion break).

These come apart: a model can be perfectly persona-consistent and still cause 出戏 via
机械感 or 把天聊死. A consistency-only metric cannot see that failure. **This argues for
a user-side immersion-break dimension that our platform should score independently of
consistency.**

## Numbers stated in the post

- 单角色专有模型 (single-character dedicated model): 不到一千条高质量数据 ("fewer than
  1,000 high-quality examples") sufficient for good results
- Self-built eval set: 约200个案例 (~200 cases)
- 通用数据集配比 (general-data mix ratio): 30% — explicitly noted as the **author's
  personal preference**, not a validated finding

All three are practitioner rules of thumb from a single post, **not measured results**.
Treat as UNVERIFIED folklore, useful as a prior only.

## Source

- https://developer.volcengine.com/articles/7439940856175394853
