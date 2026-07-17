---
title: "Of Human Criteria and Automatic Metrics: A Benchmark of the Evaluation of Story Generation (HANNA)"
url: https://arxiv.org/abs/2208.11646
acl_url: https://aclanthology.org/2022.coling-1.509/
code: https://github.com/dig-team/hanna-benchmark-asg
authors: Cyril Chhun, Pierre Colombo, Fabian Suchanek, Chloé Clavel
year: 2022
venue: COLING 2022
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# HANNA — Human-ANnotated NArratives for ASG evaluation

## The 6 orthogonal human criteria

"6 orthogonal and comprehensive human criteria, carefully motivated by the social sciences literature":

| Criterion | Definition |
|---|---|
| **Relevance** | Extent to which the story is relevant to the writing prompt |
| **Coherence** | Extent to which the story is logically consistent and coherent |
| **Empathy** | How well the story conveys/evokes the characters' emotions |
| **Surprise** | Extent to which the story is surprising (unexpected turns) |
| **Engagement** | Extent to which the story is engaging and interesting to the reader |
| **Complexity** | How elaborate / richly developed the story is |

**Scale: 5-point Likert scales.** Rated by crowd workers (not experts — contrast with TTCW).

## Dataset

- 1,056 stories from 96 prompts (WritingPrompts dataset), 10 different ASG systems.
- 3 raters per story × 6 criteria = **19,008 annotations**.
- 72 automatic metrics evaluated for correlation against these criteria.

## Key findings

- The analysis "highlight[s] weaknesses of current metrics for ASG" — n-gram overlap metrics (BLEU, ROUGE) correlate poorly with all six human criteria.
- Model-based / embedding metrics outperform n-gram metrics but remain weak.
- Practical recommendation: report multiple complementary metrics; do not rely on single-reference n-gram overlap for open-ended narrative.

## Why this matters for us

The 6-criterion decomposition is directly reusable as a **rubric skeleton for roleplay**. Note especially:
- **Surprise** and **Engagement** are separated from **Coherence** — meaning our "creativity" construct should not be one number.
- **Empathy** is treated as a first-class narrative criterion; for companion characters this is arguably the highest-weight dimension.
- Crowd workers (not experts) produced usable signal at 5-point Likert — cheaper than TTCW's MFA-expert protocol, but with a coarser construct.

## Related: OpenMEVA (arXiv 2105.08920, ACL 2021)

Companion benchmark for open-ended story generation metrics. Test suite assesses: (a) correlation with human judgments, (b) generalization to different model outputs/datasets, (c) ability to judge story coherence, (d) robustness to perturbations.

Finding: existing metrics "have poor correlation with human judgments, fail to recognize discourse-level incoherence, and lack inferential knowledge (e.g., causal order between events)."

**The (d) robustness-to-perturbations idea is directly stealable**: build adversarial checks — shuffle events, inject a contradiction, swap a character name — and verify our metric's score DROPS. A metric that doesn't move under a deliberately injected plot hole is not measuring coherence.
