---
title: "Is 'steerability' an operationalized term of art? — Vafa et al. steerability gap, the goal-space projection metric, and HELM's silence"
url: https://arxiv.org/abs/2503.17482
authors: Keyon Vafa, Sarah Bentley, Jon Kleinberg, Sendhil Mullainathan (Harvard / Cornell)
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# "Steerability" is an operationalized term of art with published formulas — verdict and the strongest formalization we had missed

**Direct answer to the question "is the WORD 'steerability' already an operationalized term of art with a published metric?" — YES, decisively, and by more than one research group with more than one formula.** Anyone claiming to introduce steerability as a new construct will be corrected in review. This file records the formalization we had **not** covered (Vafa et al.'s producibility/steerability decomposition — which owns the literal phrase **"steerability gap"**), plus the HELM negative result, and cross-references the rest rather than restating it.

## Prior state of our sweep (do not duplicate these)

| Formalization | Where it lives | Status |
|---|---|---|
| Goal-space projection; miscalibration + orthogonality decomposition | `bigtech-steerability-course-correction.md` (Chang et al., AAAI, arXiv 2505.23816) | covered, verified from PDF |
| Prompt steerability profiles / curves | `bigtech-prompt-steerability.md` (IBM, arXiv 2411.12405, NAACL 2025) | covered |
| Community-persona steerability (accuracy framing) | `bigtech-steerability-other-benchmarks.md` (Steer-Bench) | covered |
| Activation steerability prediction | `bigtech-steerability-other-benchmarks.md` (ASTEER) | covered |
| Meta's definition + training, never evaluated | `bigtech-llama3-steerability.md` (Llama 3 §4.3.7) | covered |

**This file adds:** Vafa et al. (new — and the biggest name on the list), the workshop precursor to Chang et al., HELM's axis list, and the open-source framework.

---

## 1. Vafa, Bentley, Kleinberg & Mullainathan — "What's Producible May Not Be Reachable: Measuring the Steerability of Generative Models" (2025)

**URL:** https://arxiv.org/abs/2503.17482 · arXiv only (cs.LG/AI/CV/HC), submitted 2025-03-21. **Authors are heavyweight** (Kleinberg and Mullainathan are among the most-cited people in the field) — this paper will be known to reviewers.

### Abstract (verbatim)

> "How should we evaluate the quality of generative models? Many existing metrics focus on a model's **producibility**, i.e. the quality and breadth of outputs it can generate. However, the actual value from using a generative model stems not just from what it can produce but **whether a user with a specific goal can produce an output that satisfies that goal. We refer to this property as steerability.** In this paper, we first introduce a **mathematical decomposition for quantifying steerability independently from producibility**. Steerability is more challenging to evaluate than producibility because it requires knowing a user's goals. We address this issue by creating a benchmark task that relies on one key idea: **sample an output from a generative model and ask users to reproduce it**. We implement this benchmark in user studies of text-to-image and large language models. **Despite the ability of these models to produce high-quality outputs, they all perform poorly on steerability.** These results suggest that we need to focus on improving the steerability of generative models. We show such improvements are indeed possible: **simple image-based steering mechanisms achieve more than 2x improvement on this benchmark.**"

### The formal decomposition (verbatim, Equation 2)

> "r(X∗) − r(h(m,r)) = [r(X∗) − r(S∗m)] ⏞ **producibility gap** + [r(S∗m) − r(h(m,r))] ⏞ **steerability gap**"

- **Producibility gap** — how well the model's producible set aligns with all possible instances (*can it make the thing at all?*)
- **Steerability gap** — how well humans can steer toward **the best output the model can already produce** (*can a user get it out?*)
- Ideal-point reward: **`r(x) = −d(x_g, x)`**, where `d` is human-judged distance between goal and generated output

**The "sample and reproduce" trick is the elegant part and worth understanding.** Steerability needs a known user goal, which is normally unobtainable. Their fix: **sample the goal from the model's own output distribution**, guaranteeing the target is producible **by construction**. The producibility gap is then zero *a priori*, so anything that goes wrong is **pure steerability**. That is a genuinely clever identification strategy.

### Method

1. Sample a goal image from the model's producible set
2. Show it to a human
3. Human prompts the model to reproduce it — **up to 5 attempts**
4. Separate annotators rate similarity between attempts and goal

### Numbers

- **554 goal images**, **2,770 (goal, generated) pairs**, **277 participants**, **18,550 ratings** across four metrics
- **"Annotators rate the attempted reproductions as unsatisfactory 60% of the time"**
- **"only 62% of the time are images generated by a human's 5th attempt ranked as more similar to the goal image than images generated by a human's 1st attempt (compared to a baseline of 50%)"** — i.e. **five iterations of prompting barely beats a coin flip.** This is the most damning steerability number in the literature.
- Professionals only marginally better: "final similarity scores **10% higher**" than non-experts
- **Text steering: 54.7% improve rate → Image steering (learned proposals): 74.2%** — the ">2x improvement" over text steering

### Verdict against our design

| Our construct | Vafa et al.? |
|---|---|
| The word "steerability", formally defined | **YES — with an equation and a named "steerability gap"** |
| Dose axis (graded intensity of one trait) | **NO** — goals are target points, not magnitudes on a dial |
| Continuous response | **PARTIAL** — human-judged distance `d`, continuous, but no dose to regress on |
| Curve / slope | **NO** |
| Crosstalk / entanglement | **NO** |
| Primary modality | **text-to-image** (+ LLM study); not traits, not companions |

**Why it does not close our gap:** this is *target-hitting under iterative human prompting* — reachability of a point in output space. It measures **whether a user can arrive**, not **whether the model's response scales with the strength of the ask**. No dose, no curve, no trait.

---

## 2. The workshop precursor — "Measuring Steerability in Large Language Models" (NeurIPS SafeGenAI 2024)

**URL:** https://openreview.net/forum?id=y2J5dAqcJW · same group as `bigtech-steerability-course-correction.md` (Chang et al.).

Reported definition:

> Steerability is "the magnitude of the **vector projection** of the LLM's goal-space movement onto the **user request vector**, normalized by the magnitude of the request vector — quantifying the LLM's progress in goal-space **as a proportion of the user's request**."

**⚠️ VERIFICATION STATUS: UNVERIFIED. OpenReview returned a browser-verification wall on both the forum and PDF endpoints; this wording comes from a search-result snippet, not from the paper.** Do not quote it as verbatim in any writeup without retrieving the PDF. It is recorded here because of what it implies, not as citable text.

**What it implies is the single most important line in this file.** "Movement along the requested direction **as a proportion of the request**" is **output change ÷ requested change** — a **normalized gain**. That is, up to naming, **our elasticity**. The AAAI version's *miscalibration* is the same quantity re-expressed as an error. So the construct "how much did it move relative to how much I asked" is **published, named, and formalized** — as a **scalar at a single operating point**, not as a curve over a dose ladder.

**Our defensible residual, stated precisely:** they measure gain **at one point**; we measure the **function** — slope across a dose ladder, plus saturation, monotonicity, and the off-diagonal crosstalk matrix. **"They took one derivative sample; we characterize the transfer function."** That is a real but *narrow* contribution, and we should size our claims to it. It is emphatically **not** "we introduce steerability."

---

## 3. HELM has NO steerability axis — clean negative

**URL:** https://arxiv.org/abs/2211.09110 · https://crfm.stanford.edu/helm/

HELM's core: **7 metric categories** — **accuracy, calibration, robustness, fairness, bias, toxicity, efficiency** — across **16 core scenarios** (triples of task, domain, language) spanning 6 user-facing tasks.

**"Steerability" is not among them.** The most prominent holistic evaluation suite in the field, explicitly designed for *breadth* and named for *holism*, does not have a steerability axis.

**Note the near-miss that we should preempt:** HELM's **calibration** is *confidence calibration* (do predicted probabilities match empirical accuracy?) — **totally unrelated** to Chang et al.'s **miscalibration** (did the output move the requested amount?). **Same word, unrelated constructs, both in our neighbourhood.** If we use "calibration" unqualified in a writeup, half the audience will hear the HELM sense. **Say "elasticity" or "gain", never bare "calibration".**

**This is a genuinely useful positive for us:** the field's flagship holistic suite covering 7 axes has no steerability axis, while at least five separate papers argue steerability is under-evaluated (Steer-Bench: "remains under-evaluated"; Llama 3 defines and trains it but never evaluates it; Chang et al.: "two gaps ... impede steerability evaluation"). **The construct is formalized in the literature but absent from the evaluation infrastructure.** That is exactly the gap a *platform* fills — and it reframes our contribution from "new metric" (contestable, and probably losable) to **"the missing evaluation axis, operationalized into infrastructure"** (defensible, and true).

---

## 4. Open-source framework: `github.com/MLD3/steerability`

"An open-source evaluation framework for measuring LLM steerability" — the Chang et al. (Michigan MLD3) codebase. **Actionable: their goal-space probe is runnable code.** We should run it against our trait dimensions before building our own harness — either it works and we save weeks, or it breaks on non-rule-based traits and **that failure is itself our motivating result** ("existing steerability tooling cannot measure character traits because it requires text-to-scalar rule functions"). Either outcome is a win; this is the highest-leverage next action from this sweep.

---

## Bottom line

**"Steerability" is a term of art with at least three published operationalizations** — Chang et al.'s goal-space projection/miscalibration, Vafa et al.'s producibility/steerability-gap decomposition, and IBM's prompt-steerability profiles — **plus a public benchmark (Steer-Bench), a public codebase (MLD3), and a Meta model-card section.** The word is taken. The formulas exist. **What does not exist is: (a) a dose ladder on a single trait, (b) a fitted response curve, (c) crosstalk between character traits, and (d) any of it in an evaluation suite.**

**Framing recommendation: never write "we propose steerability." Write "we operationalize steerability as a *response function* rather than a *scalar gap*, on character traits rather than rule-based text attributes, and ship it as infrastructure."** Every clause there survives contact with this literature; "we propose steerability" does not survive one reviewer.

**Related:** `bigtech-steerability-course-correction.md` (the goal-space formalization — the serious threat), `bigtech-prompt-steerability.md`, `bigtech-steerability-other-benchmarks.md`, `bigtech-llama3-steerability.md`, `bigtech-neural-steering-dose.md`, `steer-followbench-levels.md`.
