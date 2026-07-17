---
title: "How Is ChatGPT's Behavior Changing over Time?"
url: https://arxiv.org/abs/2307.09009
authors:
  - Lingjiao Chen
  - Matei Zaharia
  - James Zou
year: 2023
venue: Harvard Data Science Review
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# How Is ChatGPT's Behavior Changing over Time?

## Abstract (verbatim opening)

> GPT-3.5 and GPT-4 are the two most widely used large language model (LLM) services. However, when and how these models are updated over time is opaque. Here, we evaluate the March 2023 and June 2023 versions of GPT-3.5 and GPT-4 on several diverse tasks...

**Why this is in the judge corpus:** this is the empirical foundation for **judge drift**. It is not about judging per se — it is proof that a proprietary model endpoint's behavior changes substantially and without notice. If your judge is an API endpoint, your measuring instrument silently changes under you. Every eval number you have ever recorded against `gpt-4` is a measurement against an artifact you cannot reconstruct.

## Key numbers — drift over three months

**Prime vs. composite identification (GPT-4):**

| Version | Accuracy |
|---|---|
| GPT-4, **March 2023** | **84.0%** |
| GPT-4, **June 2023** | **51.4%** |

**A 32.6pp collapse in three months on the same task, same prompts, same model name.** 51% is chance on a binary task.

**Other measured changes:**
- GPT-4 became **less willing to answer sensitive questions and opinion survey questions** in June than in March.
- Both models made **more formatting mistakes in code generation** in June than in March.
- **GPT-4's instruction-following ability decreased over time** — the authors identify this as the common factor behind the drifts. **This is the mechanism that would break a judge**: judge prompts are instruction-heavy (follow this rubric, output this format, use this scale). Degraded instruction-following degrades rubric adherence directly.
- **Chain-of-thought effects changed**: prompting techniques that worked in March stopped working in June. **Our mitigation stack can silently stop working even if the judge model seems fine.**

**Contrasting trend:** GPT-3.5 *improved* on primes between March and June while GPT-4 *deteriorated*. **Drift is not a uniform "models get better" trend** — you cannot assume an update is an upgrade for your use case, and you cannot extrapolate one model's drift to another.

## Caveat / criticism

This paper drew methodological criticism (notably from Arvind Narayanan & Sayash Kapoor): the prime-number task used only prime numbers, so a model shifting toward answering "composite" more often would show a large accuracy drop reflecting a **behavior/formatting shift rather than a capability loss**. The critique is fair on the capability question.

**For our purposes the critique does not weaken the conclusion — it strengthens it.** We do not care whether the judge got "dumber"; we care whether it **behaves the same**. A behavior shift is precisely the failure mode that breaks an eval platform: if the judge's answer distribution moves, our scores move, and we will read it as a change in our variants. The critique concedes the behavior shifted, which is all we need.

## Implications for our platform — this is the core versioning source

1. **Never pin a judge to a floating alias** (`gpt-4`, `claude-sonnet-latest`). Always pin a dated/immutable snapshot ID. Even so, snapshots are eventually retired — the vendor's retirement schedule is an upper bound on the lifetime of our score comparability.
2. **Judge identity must be part of the score's primary key.** A score is meaningless without `(variant, judge_model_snapshot, judge_prompt_version, rubric_version, dataset_version)`.
3. **Scores from different judge versions are not comparable and must never be plotted on the same axis** without an explicit bridge.
4. **The bridge:** maintain a frozen **calibration set** and re-run it on every judge change. This gives the offset/rescaling between judge versions, and tells us whether a "regression" is our variant or our instrument.
5. Since even a pinned snapshot can be retired, plan for **judge migration** as a routine event, not an emergency: dual-run old and new judges on the calibration set during an overlap window (the standard instrument-changeover protocol from metrology).
6. This is the strongest argument for **open-weights judges** (Prometheus 2, Llama-based) for the *reproducible* tier of our platform: a checkpoint hash cannot drift.
