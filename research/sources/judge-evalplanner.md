---
title: "Learning to Plan and Reason for Evaluation with Thinking-LLM-as-a-Judge (EvalPlanner)"
url: https://arxiv.org/abs/2501.18099
authors:
  - Swarnadeep Saha
  - Xian Li
  - Marjan Ghazvininejad
  - Jason Weston
  - Tianlu Wang
year: 2025
venue: ICML 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# EvalPlanner: Learning to Plan and Reason for Evaluation

## Abstract (verbatim opening)

> LLM-as-a-Judge models generate chain-of-thought (CoT) sequences intended to capture the step-by-step reasoning process that underlies the final evaluation of a response.

The paper's diagnosis: existing judge approaches either **constrain reasoning to hand-designed components** (rigid rubrics that can't adapt to the instance) or **intertwine planning with evaluation** (the judge decides *how* to judge while judging, contaminating both).

## Methodology — three-stage separation

1. **Plan** — generate an *unconstrained* evaluation plan for this instance (what criteria matter here, in what order, what to check).
2. **Execute** — carry out the plan against the responses.
3. **Judge** — render the final verdict.

Trained via **iterative self-training on synthetically constructed preference pairs** — no human preference data required, and it achieves its results with **fewer training examples than comparable methods**.

**The key insight for us: separating "how should this be evaluated" from "what is the verdict."** The plan is a reusable, inspectable, *auditable* artifact. This is architecturally significant — it means the evaluation criteria become a first-class object that can be versioned, diffed, and reviewed by a human, rather than being implicit in a wall of CoT.

## Key numbers

- **RewardBench: 93.9** — state-of-the-art for generative reward models at time of publication.
- Also demonstrated on **RM-Bench, JudgeBench, FollowBenchEval**.

Achieved with **fewer training examples** than comparable methods, via self-training on synthetic pairs.

## Implications for our platform

- **The plan/execute split maps well onto our rubric problem.** Rather than hand-writing one rigid rubric for "character fidelity" that must cover every character and scenario, EvalPlanner suggests generating an **instance-specific evaluation plan** from the character card, then executing it. A goth vampire character and a cheerful barista character need different fidelity checks; a fixed rubric serves neither well.
- **The generated plan is a traceability artifact** — it can be logged with the judgment, giving an auditable record of *why* a variant scored as it did. This directly serves our "traceable to (variant, evaluator version, data)" requirement, in a way that a bare scalar from a reward model cannot.
- **Tension to be aware of:** the plan is generated per-instance, so it varies across instances. That is good for fidelity and **bad for comparability** — if the plan differs between two variants' evaluations, we are not measuring them with the same instrument. **Mitigation: generate the plan once per (character, scenario) and freeze it, reusing the identical plan across all variants for that item.** This keeps the instrument fixed across the comparison, which is what comparability requires, while still adapting it to the content. The frozen plan then becomes part of the versioned evaluator artifact.
- Converges with the JudgeBench finding that **reasoning at inference time is the biggest available lever** (o1-preview: +24.5pp). EvalPlanner is a cheaper way to buy structured reasoning than paying for a frontier reasoning model on every judgment.
- Self-training on synthetic pairs means we could potentially **train a companion-specific judge without a large human preference dataset** — attractive given how expensive expert character-designer annotation will be.
