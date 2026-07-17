---
title: "LitBench: A Benchmark and Dataset for Reliable Evaluation of Creative Writing"
url: https://arxiv.org/abs/2507.00769
acl_url: https://aclanthology.org/2026.eacl-long.362/
year: 2025
venue: EACL 2026
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# LitBench — the best evidence that judges CAN work, if you validate them

Counterweight to the TTCW pessimism. The difference is **pairwise preference** rather than absolute rubric scoring.

## Dataset

- Held-out test set: **2,480 debiased, human-labeled story comparisons** from Reddit (r/WritingPrompts)
- Training corpus: **43,827 pairs** of human preference labels
- Explicitly **debiased** against **length, temporal, and popularity effects** — note they had to actively remove length bias, echoing the diversity-metric length confound.

## Method

Benchmark zero-shot LLM judges; train Bradley-Terry and generative reward models; run an online human study to validate reward model rankings on newly LLM-generated stories.

## Validation numbers

| Judge | Agreement with human preference |
|---|---|
| Claude-3.7-Sonnet (best off-the-shelf zero-shot) | **73%** |
| Bradley-Terry trained reward model | **78%** |
| Generative reward model | **78%** |

Trained reward models outperform all off-the-shelf judges.

## Why this reconciles with the TTCW null result

- TTCW: absolute, 14-way binary, expert-defined, story-level → LLM judges ≈ 0 correlation.
- LitBench: **pairwise A-vs-B preference** → 73–78% agreement.

**The task format is doing the work.** LLM judges are far better at "which of these two is better" than at "is this story original, yes/no." This is the strongest argument for making our creativity scoring **comparative** rather than absolute.

## Direct implication for the platform

Pairwise-with-anchors gives us the "same baseline for each model" property the user asked for: hold a **fixed anchor set** of reference responses per scenario, score every model's response against the same anchors, convert wins to a Bradley-Terry / Elo scalar. The number is then comparable across models *by construction* and stable enough for regression detection, without requiring absolute calibration of a judge that demonstrably cannot do absolute calibration.

Ceiling to remember: ~73–78% agreement means ~1 in 4 pairwise calls disagrees with a human. Need many comparisons to average this down.
