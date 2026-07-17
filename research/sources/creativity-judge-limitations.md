---
title: "Can LLM judges assess creativity? — consolidated evidence for and against"
urls:
  - https://arxiv.org/abs/2309.14556  # TTCW: judges ~zero correlation
  - https://arxiv.org/abs/2508.05470  # Rethinking Creativity Evaluation: r=0.159, 40% consistency
  - https://arxiv.org/abs/2507.00769  # LitBench: 73-78% pairwise agreement
  - https://arxiv.org/abs/2509.22641  # Death of Novelty: judges > n-gram at expression level
  - https://eqbench.com/creative_writing.html  # admitted slop bias
year: 2024-2026
type: evidence cluster
accessed: 2026-07-16
topic: creativity-measurement
---

# The judge question — the decisive evidence table

This is the crux for the platform. The literature looks contradictory until you sort by **task format**.

## Evidence AGAINST (absolute / rubric scoring)

| Source | Finding |
|---|---|
| TTCW (Chakrabarty et al., CHI 2024) | "none of the LLMs positively correlate with the expert assessments"; correlations "close to zero" on 14 binary creativity tests |
| Rethinking Creativity Evaluation (2025) | LLM-judge vs human: **Pearson r = 0.159**; only **40% consistency across three runs**; **~20% contradictory judgments** under minor prompt variation; "bias towards particular labels" |
| Literary translation creativity study | LLM-as-judge "shows a systematic bias in favour of machine-translated texts and penalises creative and culturally appropriate solutions" |
| EQ-Bench (authors' own admission) | uncontrolled **"slop" bias (favoring overused tropes)**, self-bias, positivity bias, NSFW aversion |
| General | Judge "defaults to assessing whether the response sounds plausible"; "confident, fluent hallucinations often receive high scores"; perplexity/judge signals reflect **fluency rather than novelty** |
| General | LLMs prefer their own generations |

## Evidence FOR (pairwise / narrow-scope)

| Source | Finding |
|---|---|
| LitBench (EACL 2026) | Claude-3.7-Sonnet best off-the-shelf judge: **73% agreement** with human preference on pairwise story comparison; trained Bradley-Terry / generative reward models: **78%** |
| Death of the Novel(ty) (ICLR 2026) | "LLM-as-a-Judge novelty scores align with expert writer preferences more so than an n-gram based metric" — at the **expression level** |

## The reconciliation — it's the task format, not the model

- **Absolute, holistic, story-level creativity verdict** → r ≈ 0.16, ~0 correlation with experts. **Do not do this.**
- **Pairwise A-vs-B preference** → 73–78% human agreement. **Do this.**
- **Narrow, localized, single-attribute call** ("is this specific phrase novel?") → beats n-gram baselines. **Do this.**

Corroborating theory: **Amabile's CAT itself never asks experts for absolute scores** — it asks for *relative* ratings within a set, and that is where its 0.80–0.90 reliability comes from. The instrument that humans need in order to be reliable is the same instrument LLM judges need. This is a consistent, principled story, not a coincidence.

Also note TTCW's own internal evidence: expert per-item Fleiss κ = 0.41, but aggregate correlation 0.69. **Aggregation rescues noisy items.** Applies to judges too — many noisy narrow calls, summed, beats one holistic call.

## The specific "fluent-but-generic" bias

This is the most dangerous bias for a *companion* product, because it is **correlated with the thing we're trying to measure**, not random. A judge that rewards fluent generic prose will:
- systematically **overrate** the exact mode-collapsed, sloppy, trope-heavy output we most want to catch
- systematically **underrate** a model taking a genuine creative risk

Random noise averages out with more samples. **This bias does not** — more samples give you a more precise wrong answer. Mitigations must be structural, not statistical:
1. Use a **mechanical, judge-independent slop/cliché metric** as a cross-check (EQ-Bench does exactly this — they didn't trust the judge to penalize slop either).
2. Use **pairwise against fixed anchors**, so absolute fluency preference partially cancels.
3. **Validate against a human-labeled calibration set** and report the agreement number as a first-class platform output.
4. **Pin the judge model+version+prompt** as part of the benchmark definition (EQ-Bench: "for leaderboard parity").

## The non-negotiable conclusion

An LLM judge's creativity scores are **not valid on their own** and must never be shipped as "the creativity number" without a measured human-agreement statistic attached. Any judge we deploy needs a periodically-refreshed human calibration set, and its agreement rate is the honest confidence interval on every number it produces.
