---
title: "Benchmarking Complex Instruction-Following with Multiple Constraints Composition (ComplexBench)"
url: https://arxiv.org/abs/2407.03978
authors: Bosi Wen, Pei Ke, Xiaotao Gu, Lindong Wu, Hao Huang, Jinfeng Zhou, Wenchuang Li, Binxin Hu, Wendy Gao, Jiaxing Zhang, Yuxiao Dong, Jie Tang, Hongning Wang, Minlie Huang (Tsinghua CoAI / Zhipu AI)
year: 2024 (NeurIPS 2024 Datasets & Benchmarks Track)
type: benchmark
accessed: 2026-07-16
topic: steerability
---

# ComplexBench — constraint COMPOSITION with real dependency structure; the closest thing to entanglement, but it isn't entanglement

**Why this file matters:** ComplexBench is the single strongest "someone already did constraint interaction" threat in the instruction-following literature, because it explicitly models **dependencies between constraints** rather than treating them as an unordered bag. This file adjudicates how close that is to our entanglement/crosstalk construct. **Answer: structurally adjacent, semantically different — their dependency is a *scoring* dependency declared by annotators, not a *behavioural* interference discovered by measurement.**

## Taxonomy (verbatim definitions)

**4 constraint types:**

1. **Lexical Constraint** — "output specific keywords or phrases or precisely generate texts that are related to specific keywords"
2. **Format Constraint** — "requirements on the output structure (such as JSON, Markdown, and bullet points), length, and patterns"
3. **Semantic Constraint** — "topic, language style, personality, and sentiment of the output"
4. **Utility Constraint** — "language, helpfulness, supportiveness, consistency, and factuality of generated texts"

**19 constraint dimensions:**

- **Lexical (2):** Word Matching, Keywords
- **Format (8):** JSON Format, Markdown Format, Bullets Format, Length, Start with, End with, Punctuation, Template
- **Semantic (4):** Language Style, Personalization, Topic, Sentiment
- **Utility (5):** Helpfulness, Target Language, Supportiveness, Consistency, Factuality

Note **Semantic → Language Style / Personalization** is where a companion character sheet lives. It is one dimension of nineteen, scored binary.

## The 4 composition types — this is the novel contribution

- **Single** — one constraint only
- **And** — "multiple constraints simultaneously"
- **Chain** — "multiple tasks sequentially, each of which may contain several constraints"
- **Selection** — "select different branches according to certain conditions"

These "can be nested to form complex structures."

## Dependency-based scoring (the mechanism to understand precisely)

Each instruction is decomposed into scoring questions. Aggregation respects a **dependency graph**:

> "all the scoring questions of the subsequent task depend on the answers to those of the preceding task" (Chain)

For **Selection**, the branch's questions depend on the model having selected the correct branch. **If a prerequisite question fails, its dependent questions automatically fail.**

**Read this carefully — it is the crux.** The dependency is a **logical/evaluative gate authored into the benchmark**: annotators declare "Q3 only counts if Q1 passed." It propagates *scoring* failure downstream. It is *not* a measurement of one constraint degrading the model's ability to satisfy another. ComplexBench never asks "does adding constraint B make constraint A less well satisfied than it was alone?" — the counterfactual (A alone vs A+B) is not run.

## Scale and metrics

- **1,150 instructions**, **5,306 scoring questions**
- Evaluation: LLM-based evaluators **augmented with rules** — "to effectively verify whether generated texts can satisfy each constraint and composition"
- Metric: **DRFR (Decomposed Requirements Following Ratio)** — imported directly from InFoBench

## Results (verbatim/derived)

- **GPT-4-1106: 0.800 DRFR** overall
- Performance drops on complex compositions: **Selection averages 0.765**, **Chain averages 0.725**
- Headline finding: ComplexBench "identifies significant deficiencies in existing LLMs when dealing with complex instructions with multiple constraints composition"

The Chain < Selection < And < Single ordering is the same story as FollowBench's L1→L5: **more structure, worse adherence.**

## Verdict against our design

| Our construct | ComplexBench? |
|---|---|
| Dose axis (intensity of one trait) | **NO** — constraints are present/absent; no magnitude knob |
| Continuous response variable | **NO** — DRFR is a ratio over **binary** atoms |
| Fitted curve / slope | **NO** |
| Constraint interaction | **PARTIAL — and not the kind we mean.** Declared scoring dependency, not measured behavioural interference |
| Monotonicity / saturation | **NO** |

## Relevance to companion-eval-platform

1. **This is the paper to cite when we say "the field composes constraints but never doses them."** ComplexBench is the most sophisticated compositional taxonomy in the literature — 19 dimensions, 4 composition types, nesting, a dependency graph — and there is still **no magnitude knob anywhere in it**. A constraint is present or absent. That is a strong, specific novelty argument: the field's most advanced work on constraint *structure* has zero work on constraint *degree*.

2. **The entanglement distinction we must be able to state in one sentence.** ComplexBench's dependency is **declared a priori by annotators and gates scoring**. Our entanglement is **discovered empirically and describes behaviour**: dialing "shy" up unintentionally moves "formal" or "verbose". Theirs is a DAG in the rubric; ours is an off-diagonal term in a measured response matrix. If a reviewer says "ComplexBench already does constraint interaction," the reply is: *they encode which constraints logically presuppose which; they never measure whether satisfying one costs you another.* The A-alone vs A+B counterfactual is absent.

3. **But do not overclaim — Chain/Selection is real prior art on structure.** If we describe our platform as "the first to consider that constraints relate to each other," ComplexBench refutes us instantly and embarrassingly. Scope our claim to **magnitude and crosstalk**, never to "constraints interact" in general.

4. **DRFR is now the field's default response variable, and that is our wedge.** InFoBench invented it (`bigtech-infobench.md`), ComplexBench adopted it wholesale, CFBench's CSR/ISR are the same shape, FollowBench's HSR/SSR likewise. **Four independent benchmark teams converged on binary-atom satisfaction.** That convergence is why nobody has a curve to fit: you cannot regress a slope on {0,1} atoms. Our continuous trait-magnitude measurement is not a small metric tweak — it is a departure from the field's shared evaluation substrate, and we should frame it that way.

5. **Their rules-augmented LLM evaluator is the right engineering pattern to copy.** Semantic constraints (Language Style, Personalization) cannot be regexed, so they back the judge with rules where rules apply. Our trait-magnitude judge needs the same hybrid, and we should expect judge noise on exactly the Semantic dimensions we care most about.

6. **Nesting is a warning about our own scope.** ComplexBench needed 5,306 scoring questions for 1,150 instructions (~4.6 per instruction) once compositions nest. If we cross dose levels × traits × scenes, our grid explodes the same way. Budget for it or restrict to a small trait set.

**Related:** `bigtech-infobench.md` (DRFR origin), `steer-followbench-levels.md` (count axis), `steer-cfbench.md`, `bigtech-steerability-course-correction.md` (orthogonality/side-effects — the *actual* crosstalk prior art, and a far bigger threat than ComplexBench).
