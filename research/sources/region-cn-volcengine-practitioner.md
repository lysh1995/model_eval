---
title: "浅谈大模型角色扮演：从当红炸子鸡到无人问津 (On roleplay LLMs: from hot property to abandoned)"
url: https://developer.volcengine.com/articles/7413673458418548747
authors: 刘聪NLP / @ybq (practitioner post, hosted on 火山引擎开发者社区 / ByteDance Volcano Engine developer community)
year: 2024
type: article
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# Chinese practitioner view of roleplay LLM evaluation (ByteDance dev community)

Practitioner blog post, not a paper. Value here is **native industry vocabulary** that
does not appear in Anglophone benchmark literature. Hosted on ByteDance's Volcano Engine
developer community — this is the closest thing I found to a Chinese *product* team
writing about roleplay quality criteria, though it is an individual's post rather than
official ByteDance methodology.

**Publication date: not stated on page. UNVERIFIED** (article ID suggests 2024).

## Evaluation dimensions named (original Chinese)

1. **安全性** (safety) — with the specific observation that
   通用模型的安全能力，很容易在 role_play 时所忘记
   ("a general model's safety ability is easily forgotten during role_play").
2. **角色相似度** (character similarity) — whether speech tone/manner matches the character.
3. **角色穿透** (*"role penetration"*) — **whether the model admits to being an AI model.**
4. **角色知识掌握度** (character knowledge mastery) — accuracy of knowledge the character
   should possess.
5. **聊天常用指标** (standard chat metrics) — 逻辑性 (logicality), 连贯性 (coherence),
   流畅性 (fluency).

## Key term: 角色穿透 (role penetration)

This is a **distinct native term** worth adopting. It is narrower and more operational
than the Anglophone "breaking character":

- **角色穿透** = the specific failure of the model conceding it is an AI/LLM — the mask
  being *penetrated*, i.e. the user seeing through to the assistant underneath.
- Compare **穿帮** (chuāngbāng) — a film/theatre term for "the gaffe is visible", used in
  CharacterGLM's error analysis as the label for OOC generally.

Anglophone work folds both into "OOC" / "breaking character". Chinese practice
distinguishes *generic* OOC from *specifically admitting AI-ness*. For a companion
product, these are very different severities — 角色穿透 is the one that destroys the
illusion permanently. **Recommend treating as a separate scored failure mode.**

## The most useful line in the post — how 拟人化 is actually defined

The stated training objective is to make the model:

> 去掉 llm 模型骨子里的彬彬有礼、有问必答
> ("strip away the LLM's bone-deep politeness and its answer-everything reflex")

— and *that* is what the author calls achieving 拟人化 (anthropomorphization).

This is a **negative definition**: anthropomorphism is not "add human traits", it is
**"subtract assistant traits"**. That framing is much more operationalizable than the
Anglophone "human-likeness" construct, which is usually a vague Likert item. It suggests
measurable proxies: refusal-to-answer rate, unsolicited-helpfulness rate, politeness
markers, sycophancy — all *inverted* (lower = more human).

This is arguably the single most transferable idea in this file for our platform.

## Data construction insight

Emphasizes diversity of user queries as critical — explicitly wanting
各种诡异的、奇葩的 query ("all kinds of bizarre, freakish queries") and
各种应变场景 ("various contingency scenarios"), naming: 用户不聊 (user goes silent),
发火 (user gets angry), 复读 (user repeats themselves).

These are **adversarial-user scenarios framed as quality tests, not safety tests** — a
useful distinction. Anglophone eval tends to test hostile users only under a safety lens.

## Author's market claim — flagged as questionable

The post attributes declining roleplay interest to 非刚需属性 ("not a rigid/essential
need") and states **Character.ai 倒闭** ("Character.AI collapsed") caused related product
traffic to decline.

**This claim is FALSE as literally stated** — Character.AI did not shut down; its
founders left for Google in Aug 2024 in a licensing/acqui-hire deal. Recorded here only
to document that the source contains an inaccuracy, which is a reason to treat its
market commentary (not its vocabulary) with caution.

No specific numbers are given in the post. No Chinese products (猫箱/星野/筑梦岛)
are analyzed by name.

## Source

- https://developer.volcengine.com/articles/7413673458418548747
