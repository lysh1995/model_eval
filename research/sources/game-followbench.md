---
title: "FollowBench: A Multi-level Fine-grained Constraints Following Benchmark for Large Language Models"
url: https://arxiv.org/abs/2310.20410
authors: Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin Jiang, Qun Liu, Wei Wang (HKUST / Huawei Noah's Ark Lab)
year: 2023 (ACL 2024)
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# FollowBench — how adherence scales with the NUMBER of simultaneous constraints

**The axis this paper isolates: not turns, but constraint count. It answers "how many rules can a model hold at once?" — the orthogonal question to Multi-IF's "how long can it hold them?"**

## Abstract (verbatim excerpt)

> "a Multi-level Fine-grained Constraints Following Benchmark for LLMs"

820 curated instructions from 50+ NLP tasks, evaluated with **both rule-based and model-based** evaluation methods.

## Five constraint types

1. **Content** — explicit restrictions on response scope/depth
2. **Situation** — implicit contextual/background information guiding appropriate answers
3. **Style** — stylistic variations (tone, sentiment, formality, empathy)
4. **Format** — structural/presentation requirements for outputs
5. **Example** — pattern recognition from few-shot examples with potential noise

**Situation** and **Style** are the interesting ones for us — they are the two categories that resist regex and force model-based evaluation. Note this taxonomy overlaps heavily with SysBench's six (Role, Background, Action, Style, Content, Format); "Situation" ≈ "Background".

## Multi-level construction — the key design

Instructions run from **level 1 to level 5**, and the benchmark "incrementally adds a single constraint to straightforward instructions at each increased level."

This is a **controlled ablation**: same base instruction, +1 constraint per level. Any performance drop from L1→L5 is attributable to constraint load, not to task difficulty. This design is what lets them "pinpoint the difficulty level at which LLMs fail to follow instructions."

**Benchmark size:** 820 total instructions across constraint categories with multi-level variants.

## Metrics

- **HSR (Hard Satisfaction Rate)** — average rate at which *all* constraints of an instruction are simultaneously satisfied (conjunctive; = IFEval's prompt-level, SysBench's ISR)
- **SSR (Soft Satisfaction Rate)** — average satisfaction rate of *individual* constraints across instructions (= IFEval's instruction-level, SysBench's CSR)
- **CSL (Consistent Satisfaction Levels)** — **maximum consecutive levels satisfied starting from level 1**

CSL is the novel one and the conceptual cousin of SysBench's SSR: instead of "how many consecutive *turns* do you hold?", it is "how many consecutive *constraint loads* do you hold?" Reported as a mean over instruction groups, so it reads as "this model reliably handles ~N simultaneous constraints."

Note the vocabulary collision to watch for: **FollowBench's SSR (Soft Satisfaction Rate) is a per-constraint average; SysBench's SSR (Session Stability Rate) is a session-level conjunction.** Same acronym, near-opposite strictness. Do not mix these up in our docs.

## Main results (verbatim table, HSR by level)

| Model | L1 | L2 | L3 | L4 | L5 | Avg. | CSL |
|-------|----|----|----|----|----|----|-----|
| GPT-4-Preview | 84.7% | 75.6% | 70.8% | 73.9% | 61.9% | 73.4% | **3.3** |
| GPT-3.5-Turbo | 80.3% | 68.0% | 68.6% | 61.1% | 53.2% | 66.2% | **2.9** |
| Qwen-Chat-72B | 73.8% | 63.3% | 54.3% | 45.2% | 39.9% | 55.3% | **2.4** |
| LLaMA2-Chat-70B | 59.9% | 53.3% | 46.0% | 40.2% | 37.9% | 47.5% | **2.1** |

> "Performance consistently declined across all models from L1→L5, with GPT models substantially outperforming open-source alternatives."

Additionally reported: GPT-4 achieves **HSR and SSR of 84.70% at level 1**, and at level 5, **HSR 62.42% / SSR 73.27%** — the HSR/SSR gap widens with load (individual constraints still mostly satisfied at 73%, but holding *all* of them drops to 62%). That gap *is* the conjunction penalty, and it grows with constraint count.

### Derived degradation (L1 → L5, HSR)

| Model | L1 | L5 | Absolute drop | Relative drop |
|---|---|---|---|---|
| GPT-4-Preview | 84.7% | 61.9% | −22.8 | −26.9% |
| GPT-3.5-Turbo | 80.3% | 53.2% | −27.1 | −33.7% |
| Qwen-Chat-72B | 73.8% | 39.9% | −33.9 | −45.9% |
| LLaMA2-Chat-70B | 59.9% | 37.9% | −22.0 | −36.7% |

**The CSL numbers are the punchline: the best model in the study reliably holds ~3.3 simultaneous constraints.** Not thirty. Three.

## Relevance to companion-eval-platform

1. **CSL ≈ 3.3 is a hard budget number, and it should scare us.** A realistic roleplay system prompt contains *far* more than three constraints: character voice, backstory facts, world rules, forbidden topics, format conventions, tone, relationship state. FollowBench says GPT-4-class models reliably hold about three. This directly predicts that a rich scene definition is **already over budget at turn 1**, before any multi-turn decay. Combine with SysBench (33.7% five-turn session stability) and Multi-IF (−17 pts over three turns) and the composite picture is: our platform's scenes are probably being violated constantly and invisibly.

2. **Two independent axes of decay, and we need both.** FollowBench: adherence falls with **constraint count** (L1→L5). Multi-IF/SysBench: adherence falls with **turn count**. Our product has *both* simultaneously — many rules, held for many turns. Nobody in this literature has measured the interaction. **The 2D grid (rules × turns) is an obvious and genuinely novel contribution** and it is cheap to run because the checkers are the same ones.

3. **The controlled-ablation design is the methodological lesson.** Same base instruction, +1 constraint per level, so the drop is attributable. Our analogue: hold the scene fixed, vary the number of active rules. That gives us a defensible causal claim ("rule N+1 costs X% adherence") instead of a correlational one, and it yields a directly actionable product output: **a recommended rule budget for scene authors.** That is a feature, not just a metric.

4. **CSL is the metric shape to steal for authoring guidance.** "How many rules can this model hold before it starts dropping them" is exactly what a scene author needs to know, and it is a single interpretable number. A scene-authoring UI that says "this scene has 11 rules; models reliably hold ~3" would be the most useful thing our eval produces.

5. **Honest caveat on the numbers.** FollowBench uses "both rule-based and model-based" evaluation — Content/Format are checkable, Situation/Style/Example need a judge. So these figures are not purely deterministic and inherit some judge noise. Also note L4 (73.9%) > L3 (70.8%) for GPT-4-Preview: the level ordering is not perfectly monotonic, which suggests the added constraints are not uniformly difficult and the "level" abstraction is a bit leaky. Treat CSL 3.3 as an order-of-magnitude signal ("a few, not dozens"), not a precise budget.

6. **Naming hazard flagged above:** FollowBench SSR ≠ SysBench SSR. If we adopt terms from both papers we must rename. Suggest: `per-rule adherence` (soft/CSR), `per-turn all-rules` (hard/ISR), `session stability` (SysBench SSR), `rule budget` (CSL).

7. **Related:** `game-ifeval.md`, `game-multi-if.md`, `game-sysbench.md`. FollowBench is the constraint-count axis; the others are the horizon axis.
