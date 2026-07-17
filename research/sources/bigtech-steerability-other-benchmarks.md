---
title: "Other benchmarks using the word 'steerability': Steer-Bench and ASTEER / 'When is Your LLM Steerable?'"
url: https://arxiv.org/abs/2505.20645
org: various (Steer-Bench: academic; ASTEER: academic)
year: 2025
type: benchmark
accessed: 2026-07-16
topic: bigtech-practice
---

# Two more benchmarks that use the word "steerability" — and why NEITHER measures our construct

This file exists to close out the "search for the actual word 'steerability'" sweep and record two **negative results**. Reporting that these do *not* refute us is as valuable as the refutations, because it bounds the threat: only three of the six steerability papers found are dangerous to our claim.

Verification: both arxiv abstract pages fetched raw via curl and string-matched. Neither PDF was fully extracted — assessments below are based on **verified abstracts only** and are marked accordingly.

---

## 1. Steer-Bench: A Benchmark for Evaluating the Steerability of Large Language Models

**URL:** https://arxiv.org/abs/2505.20645

Abstract (verbatim excerpt):

> "**Steerability**, or the ability of large language models (LLMs) to adapt outputs to align with diverse community-specific norms, perspectives, and communication styles, is critical for real-world applications but remains **under-evaluated**. We introduce Steer-Bench, a benchmark for assessing **population-specific steering using contrasting Reddit communities**. Covering **30 contrasting subreddit pairs across 19 domains**, Steer-Bench includes over **10,000 instruction-response pairs** and validated **5,500 multiple-choice question** with corresponding silver labels to test alignment with diverse community norms. Our evaluation of 13 popular LLMs using Steer-Bench reveals that while **human experts achieve an accuracy of 81% with silver labels, the best-performing models reach only around 65% accuracy** depending on the domain and configuration. Some models lag behind human-level alignment by over 15 percentage points, highlighting significant gaps in community-sensitive steerability."

### Verdict: does it measure prompt-space dose-response? **NO.**

- Dose axis: **NO** — a community persona is applied or not; there is no "more r/conservative" knob and no ordering over doses
- Response variable: **multiple-choice accuracy against silver labels** — binary-correct at the atom, exactly the InFoBench/IFEval shape (`bigtech-infobench.md`)
- Curve: **NO**
- Crosstalk: **NO**

**"Steerability" here means "can it hit the target persona at all" — a *classification accuracy* framing.** It is a target-hitting benchmark, not a gain measurement. Same word, different construct. Note it independently calls steerability "under-evaluated", which is mild support for our general framing even as three other papers undercut the specific claim.

---

## 2. When is Your LLM Steerable? (ASTEER)

**URL:** https://arxiv.org/abs/2606.11599

Abstract (verbatim excerpt):

> "**Activation steering** offers a lightweight approach to control language models' behavior at inference time, but **whether it succeeds or fails heavily depends on the prompt, concept, model, and steering configuration**. Finding the regime and boundaries of successful steering typically requires expensive grid searches and post-hoc evaluation of full autoregressive rollouts. In this work, we investigate whether **steerability can be predicted from the model's internal states at the beginning of the generation process**... To this end, we first introduce **ASTEER, a testbed including 1.4M steered generations, spanning 150 concepts with each steering success/failure labeled**... We then train a **Gradient Boosting Decision Trees (GBDT) classifier** on these features to predict whether an intervention will **under-steer, succeed, or over-steer** without requiring full rollout. Our predictor achieves around **0.7 macro-F1** score on unseen concep[ts]"

### Verdict: does it measure prompt-space dose-response? **NO — it is activation-space, and it discretizes the dose response into three classes.**

- Dose axis: **activation steering configuration**, not prompt
- Response variable: **a 3-way label — under-steer / succeed / over-steer**. This is the *categorical* version of our continuous elasticity: under-steer ≈ Dead, over-steer ≈ Brittle, succeed ≈ the usable band. **They classify the failure modes rather than fitting the function that produces them.**
- Curve: **NO** — the continuous response is collapsed to 3 labels and predicted, not fitted
- Crosstalk: **NO** (not evident from abstract — **UNVERIFIED**, PDF not extracted)

### Why this one is interesting anyway

**Our Dead/Brittle taxonomy has independent empirical support as a real trichotomy.** A 1.4M-generation testbed across 150 concepts labels every steering attempt as exactly under-steer / succeed / over-steer. That is our failure-mode taxonomy, arrived at independently, at scale — in activation space. It is evidence the taxonomy carves reality at the joints rather than being a framework we imposed.

The line **"whether it succeeds or fails heavily depends on the prompt, concept, model, and steering configuration"** also matters: steerability is **concept-dependent** (some traits steer, others don't) and **prompt-dependent even under activation steering**. Both are consistent with IBM's "each model favors a subset of persona dimensions on which it is more steerable" and PsySET's construct-specific findings. **Three independent papers agree steerability is not a scalar property of a model — it is a property of (model, trait, direction, context).** Any single "steerability score" for a model is therefore meaningless, which is a real design constraint on what our platform should report: a matrix or a profile, never a number.

**Caveat on this paper: arXiv ID 2606.11599 implies June 2026 — very recent as of our 2026-07-16 access date. Only the abstract is verified. Do not cite specifics beyond the quoted text without extracting the PDF.**

---

## Net effect on our novelty claim

| Paper | Threat level | Why |
|---|---|---|
| `bigtech-neural-steering-dose.md` (Oxford/AISI) | **FATAL** | fits a regression, reports prompt-space slope, companion trait |
| `bigtech-psyset.md` (USC) | **SEVERE** | prompt lexical intensity ladder on traits, free-form output, finds flat |
| `bigtech-prompt-steerability.md` (IBM) | **SEVERE** | prompt-space steerability curves by name; but disclaims crosstalk + multi-turn |
| `bigtech-steerability-course-correction.md` (Michigan/MSR/Netflix) | **SEVERE (crosstalk)** | miscalibration + orthogonality; but text attributes, no curve |
| `bigtech-persona-vectors.md` (Anthropic) | **MODERATE** | activation-space curve; prompt ladder present but unfitted; trait entanglement matrix in activation space |
| **Steer-Bench** | **NONE** | accuracy-based target-hitting, no dose |
| **ASTEER** | **NONE (supportive)** | activation-space; independently validates the Dead/Brittle trichotomy |

**Related:** `bigtech-psyset.md`, `bigtech-prompt-steerability.md`, `bigtech-neural-steering-dose.md`, `bigtech-persona-vectors.md`, `bigtech-steerability-course-correction.md`, `bigtech-infobench.md`.
