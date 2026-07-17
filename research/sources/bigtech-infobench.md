---
title: "InFoBench: Evaluating Instruction Following Ability in Large Language Models"
url: https://arxiv.org/abs/2401.03601
authors: Yiwei Qin, Kaiqiang Song, Yebowen Hu, Wenlin Yao, Sangwoo Cho, Xiaoyang Wang, Xuansheng Wu, Fei Liu, Pengfei Liu, Dong Yu (Tencent AI Lab; Shanghai Jiao Tong University; University of Central Florida; University of Georgia)
org: Tencent AI Lab
year: 2024
type: benchmark
accessed: 2026-07-16
topic: bigtech-practice
---

# InFoBench / DRFR — the cleanest illustration of the BINARY-COMPLIANCE crux

**Verdict up front: measures "did it comply", not "how much did it move". DRFR is a ratio of satisfied binary criteria. This is the whole instruction-following paradigm's shape, and it is orthogonal to steerability. Confirms the crux distinction with no ambiguity.**

Verification: arxiv abstract page fetched raw via curl and string-matched.

## Abstract (verbatim)

> "This paper introduces the **Decomposed Requirements Following Ratio (DRFR)**, a new metric for evaluating Large Language Models' (LLMs) ability to follow instructions. Addressing a gap in current methodologies, **DRFR breaks down complex instructions into simpler criteria**, facilitating a detailed analysis of LLMs' compliance with various aspects of tasks. Alongside this metric, we present InFoBench, a benchmark comprising **500 diverse instructions and 2,250 decomposed questions** across multiple constraint categories. Our experiments compare DRFR with traditional scoring methods and explore annotation sources, including human experts, crowd-sourced workers, and GPT-4. The findings demonstrate **DRFR's higher reliability and the effectiveness of using GPT-4 as a cost-efficient annotator**."

## The method, and why it settles KEY QUESTION 3

DRFR decomposes an instruction into atomic requirements, each answerable **Yes/No**, then reports the **ratio satisfied**.

The measurement chain is:
```
instruction → decompose into N binary criteria → judge each Yes/No → DRFR = (# Yes) / N
```

Every quantity in that chain is **binary at the atom**. The only continuity in DRFR is the continuity of *counting* — a ratio over a set of satisfied/unsatisfied predicates. It answers **"how many of the requirements did it meet?"** It cannot answer **"how much of the trait did it express?"** because there is no trait quantity anywhere in the construct; there are only predicates and their truth values.

**This is the precise crux of our KEY QUESTION 3, and InFoBench is the sharpest possible illustration because decomposition is its entire contribution.** The paper's innovation is to make compliance *more granular* — and granular is still binary. Finer atoms do not create a magnitude. You can decompose "be shy" into fifty Yes/No criteria and still have no answer to "is this response 30% shy or 80% shy?"

## The pattern across the whole instruction-following family

Assembled from this file and existing sources (`game-ifeval.md`, `game-multi-if.md`, `game-followbench.md`, `game-sysbench.md`):

| Benchmark | Atom | Aggregate | Continuous magnitude? |
|---|---|---|---|
| IFEval | deterministic program predicate | prompt-level / instruction-level accuracy | **No** — regex-checkable predicates |
| Multi-IF | IFEval predicate, across turns | 4 accuracies + IFR + ECR | **No** — IFR counts followed→unfollowed flips |
| FollowBench | constraint satisfied | HSR / SSR / CSL | **No** — see below |
| SysBench | checklist item, GPT-4o judge | CSR / ISR / SSR | **No** — "Outputs binary Yes/No per constraint" |
| InFoBench | decomposed requirement | DRFR | **No** — Yes/No per requirement |

**Every single one bottoms out in a satisfied/violated predicate.** The variation across the family is in *aggregation* (conjunctive vs. average), *granularity* (prompt vs. instruction), and *axis* (turns vs. constraint count) — never in whether the underlying quantity is binary. This is not an oversight; it is IFEval's founding design decision (`game-ifeval.md`: "verifiable instructions are instructions amenable to objective verification of compliance"), inherited by the whole lineage. **They bought reliability by narrowing the construct to one where compliance is decidable.** Magnitude was traded away on purpose, in 2023, and nobody in this family has traded back.

## Is FollowBench a dose-response design? — the honest assessment

The task specifically flags FollowBench's "multi-level fine-grained constraints" as a possible dose-response design. Per `game-followbench.md`, it "incrementally adds a single constraint to straightforward instructions at each increased level", L1→L5.

**It is a controlled ablation with an ordered load axis, but it is NOT a dose-response curve of trait expression, for three reasons:**

1. **The x-axis is constraint COUNT, not intensity of one trait.** L1→L5 adds *different* constraints. It is "how many rules can you hold?", not "how much shyness do you express per unit of shy-emphasis?" Adding a constraint about tone and then a constraint about length does not constitute a dose of anything.
2. **The y-axis is binary satisfaction rate, not magnitude.** HSR (all constraints satisfied) and SSR (fraction satisfied) are conjunctions and averages over **binary** predicates. As load rises, compliance *probability* falls — a psychometric-style curve over pass/fail events, not a magnitude response.
3. **The direction of the construct is inverted.** FollowBench's curve descends: more constraints → *worse* adherence. It measures **capacity degradation under load**. A dose-response curve ascends: more emphasis → *more* trait. FollowBench answers "when does it break?"; steerability answers "does it move?" These are different questions with different failure modes.

**The closest FollowBench comes is CSL** (max consecutive levels satisfied from L1), which reads like a saturation point — but it is a saturation point of *capacity*, not of *gain*. **Verdict: not a dose-response design.** The FollowBench-shaped analogy is a trap and we should say so explicitly rather than let a reviewer say it for us. Its real value to us is orthogonal and already captured in `game-followbench.md` (the ~3.3 rule budget).

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**NO — and not close. Nothing in the instruction-following family does.**

- Prompt-space dose axis: **NO** — instructions are present or absent, never graded
- Continuous trait magnitude in output: **NO** — Yes/No per decomposed requirement
- Curve: **NO**
- Crosstalk: **NO** — requirements are scored independently; no analysis of whether satisfying one perturbs another

**This is the one part of our claim that survives fully intact.** Instruction-following benchmarks measure compliance, not movement. The distinction is not a quibble — it is a different construct with a different mathematical type (predicate vs. magnitude). Anyone who says "isn't this just IFEval?" is wrong, and this file is the citation for why.

## Relevance to companion-eval-platform

1. **This is the clean half of our argument. Lead with it.** "Instruction-following benchmarks are binary-compliance; steerability is continuous-magnitude" is TRUE, defensible across the entire family (IFEval → Multi-IF → FollowBench → SysBench → InFoBench), and the family's own founding paper says why. The refutations we found (`bigtech-psyset.md`, `bigtech-prompt-steerability.md`, `bigtech-neural-steering-dose.md`) come from the *steerability* literature, not the *instruction-following* literature — a completely separate research community. Our framing error was searching the wrong shelf.
2. **DRFR's reliability finding is a warning about our own judge.** The paper reports "DRFR's higher reliability and the effectiveness of using GPT-4 as a cost-efficient annotator" — reliability was won *by decomposing into binary atoms*. **We are proposing to go the other way: a continuous 0–100 trait score.** We should expect *worse* judge reliability than DRFR, not better, and we must measure it rather than assume it. Cf. our α = 0.25–0.34 on aesthetic quality, and the unreported judge reliability in SysBench and persona vectors.
3. **A hybrid is available and may be the honest design.** Decompose "shy" into binary behavioral indicators (avoids eye contact in narration? deflects direct questions? hedges? initiates topics?) and let the **count** be the magnitude. That is DRFR-with-a-dose-axis: binary atoms (reliable) aggregated into a continuous score (magnitude), swept across an intensity ladder. **This may be the single most valuable design idea in this research pass** — it converts our unreliable continuous judgment into a reliable countable one while preserving the dose-response construct, and it is a genuine synthesis of the two literatures rather than a borrowing from either.
4. **Related:** `game-ifeval.md` (the founding trade), `game-multi-if.md`, `game-followbench.md` (assessed above — not dose-response), `game-sysbench.md`, `judge-inter-rater-reliability` / `psycho-inter-rater-reliability.md`, `bigtech-psyset.md`.
