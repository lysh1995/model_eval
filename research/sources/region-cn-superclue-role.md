---
title: "SuperCLUE-Role：中文原生角色扮演测评基准 (Chinese-native roleplay evaluation benchmark)"
url: https://github.com/CLUEbenchmark/SuperCLUE-Role
authors: CLUEbenchmark (中文语言理解测评基准组织)
year: 2024
type: leaderboard
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# SuperCLUE-Role

Chinese-native roleplay leaderboard from CLUEbenchmark, the org behind the SuperCLUE
family of Chinese LLM benchmarks. Self-describes as **中文原生** ("Chinese-native") —
i.e. explicitly not a translation of an English benchmark. Released ~2024-04-01
(inferred from leaderboard image filename `SuperCLUE-Role20240401.png`).

## Why it matters for us

This is the clearest example of a Chinese eval taxonomy that **treats 情感陪伴
(emotional companionship) as a first-class scored scenario**, not a safety edge case.
Anglophone roleplay benchmarks generally do not carve out companionship as a scored
application category.

## Dimension taxonomy (verified — two independent sources agree)

**3 一级维度 (first-level) / 10 二级维度 (second-level).** The 2+3+5 = 10 arithmetic
matches the benchmark's own "三个一级维度和十个二级维度" claim.

### 1. 角色基础 (Role Fundamentals)
Tests dialogue ability and knowledge mastery — the substrate, not the performance.
- **对话能力** (dialogue ability)
- **知识掌握** (knowledge mastery)

### 2. 角色演绎力 (Role Interpretation / Portrayal Ability)
Per the benchmark: tests whether the model 遵循角色的性格、语言风格、行为习惯和三观
("follows the character's personality, language style, behavioral habits, and 三观").
- **语言风格** (language style)
- **行为习惯** (behavioral habits)
- **角色背景** (character background)

> **三观 (sān guān)** — literally "the three views": 世界观/人生观/价值观 (worldview /
> outlook on life / values). This is a load-bearing Chinese concept with **no clean
> Anglophone benchmark equivalent**. Anglophone persona-consistency work checks facts
> and style; 三观 asks whether the character's *value judgments* stay in character.
> Worth considering as a distinct sub-dimension for our platform.

### 3. 场景应用 (Scenario Application)
Application-context evaluation — the part Anglophone benchmarks mostly lack.
- **情感陪伴** (emotional companionship)
- **游戏NPC** (game NPC)
- **直播营销** (livestream marketing / livestream selling)
- **社交场景** (social scenarios)
- **影音名人** (entertainment / media celebrities)

## Methodology

- Model-based evaluation (LLM-as-judge), **5级评分** (5-point scale) applied across
  multiple dimensions per second-level task.
- Final score aggregates second-level dimension averages.
- Stated motivation: existing benchmarks (CharacterEval, RoleBench named explicitly)
  have 评估标准和方法不一致 ("inconsistent evaluation standards and methods") and lack
  assessment of **应用潜力** (application potential) in common deployment scenarios.

## Numbers — DELIBERATELY NOT RECORDED

**UNVERIFIED / NOT CAPTURED:** The leaderboard scores are published **only as embedded
images** on both the GitHub README and the mirror article. Text extraction returns model
names but no scores. Models named at the top of the ranking: **GPT-4-Turbo-0125**,
**Qwen1.5-72B-Chat**, **文心一言4.0 (Ernie 4.0)**. Both sources state Qwen1.5-72B-Chat
and Ernie 4.0 perform strongly in Chinese contexts.

I did **not** record any numeric scores because I could not read them. Do not let anyone
fill these in from memory — read the images directly if scores are needed.

**UNVERIFIED:** Total count of roles (角色) and test questions is not stated in the
extracted text of either source.

## Sources cross-checked

- Primary: https://github.com/CLUEbenchmark/SuperCLUE-Role
- Mirror/commentary (independent extraction, same taxonomy): https://www.53ai.com/news/qianyanjishu/587.html
  — "SuperCLUE-Role：重新定义中文角色大模型测评基准"

Both extractions independently produced the identical 3/10 taxonomy, which is why the
taxonomy above is marked verified.
