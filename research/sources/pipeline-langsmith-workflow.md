---
title: "LangSmith evaluation concepts — offline/online evals, annotation queues, datasets, experiments"
url: https://docs.langchain.com/langsmith/evaluation-concepts
org: LangChain
year: 2026
type: product-docs
accessed: 2026-07-16
topic: eval-lifecycle
---

# LangSmith: the offline/online split and the annotation queue

## The core distinction (verbatim)

**Offline evaluation** — "target **examples** from **datasets**: curated test cases **with
reference outputs** that define what 'good' looks like."

**Online evaluation** — "target **runs** and **threads** from tracing: real production
traces **without reference outputs**. Without reference outputs, evaluators focus on
**detecting issues, anomalies, and quality degradation** in real-time." "Online evaluation
scores real-world production traffic in real-time to detect quality drift."

> **This is the cleanest statement of why offline and online evals are different
> instruments, not the same instrument at different times.** The presence or absence of a
> **reference output** changes what questions are answerable:
> - offline: "is this *right*?" (comparison to a target)
> - online: "is this *anomalous*?" (comparison to a distribution)
>
> **Our platform is unusual in that even the OFFLINE side has no reference output.** Note 11
> establishes there is no gold answer for roleplay (human α=0.25–0.34). So we are in the
> "online" epistemic regime **in both places** — everything is distributional or pairwise,
> nothing is right/wrong. That's a real constraint on tool choice: **the entire industry's
> offline-eval tooling is built around `expected`/`reference`, and we have none.**
>
> What we substitute: the **frozen anchor set** plays the structural role of the reference —
> not "the right answer" but "a fixed thing to compare against." That preserves
> comparability without claiming correctness. It's the only move available.

## Runs vs examples

> "A **run** is a single execution trace from your deployed application. Each run contains:
> **Inputs**: The actual user inputs your application received. **Outputs**: What your
> application actually returned. **Intermediate steps**: All the child runs (tool calls, LLM
> calls, and so on). **Metadata**: Tags, user feedback, latency metrics, etc. **Unlike
> examples in datasets, runs do not include reference outputs.**"

**Threads** — the multi-turn grouping (LangSmith's session analogue). Online evals can
target threads, not just runs.

> Another vendor with a first-class multi-turn object that can be *evaluated as a unit*
> (Langfuse: session; LangSmith: thread; OTel: nothing but a label). **Three of four
> platforms model the conversation; the open standard does not.**

## Annotation queues (verbatim)

> "Annotation queues **streamline structured collection of human feedback on runs**. They
> complement inline annotation by providing organized workflows with **prescribed rubrics**,
> **team collaboration features**, and **progress tracking**."

Two queue types:
- **Single-run queues** — "Review one run at a time against custom rubric items. Useful for
  **triaging issues or building datasets from production traces**."
- (multi-run/comparison queues)

> "**Building datasets from production traces**" — the annotation queue is explicitly the
> **on-ramp of the flywheel**, not just a labeling tool. The queue is where a production
> trace becomes a dataset item, and where the human decides *whether* it should.
>
> **This is where our human-in-the-loop attaches**, and it is a single component serving
> four distinct jobs that we should keep explicitly separated (they have different sampling
> and different consumers):
> 1. **judge abstentions** (note 11 §6) — ~19% contested items, routed automatically
> 2. **uniform-random audit** — unbiased κ + Tier-2 FP rate (note 06 §1)
> 3. **uncertainty/active sampling** — cheap improvement (see `pipeline-shreya-data-flywheel.md`)
> 4. **curation decisions** — promote/reject a mined case into the rolling set
>
> Same UI, four queues, **four different inclusion probabilities** — and π must be recorded
> per item (note 06 §3: "π_i is lineage, not telemetry") or the κ computed from the pooled
> labels is uninterpretable.

## Datasets & experiments

> "Multiple experiments typically run on a given dataset to test different application
> configurations (e.g., different prompts or LLMs). LangSmith displays all experiments
> associated with a dataset and supports **comparing multiple experiments side-by-side**."

The dataset-driven workflow "allows you to measure your application's quality, compare
prompt/model versions, and **detect regressions before you release any changes to
production**."

> **`dataset × experiment` is the industry's universal shape** for the pre-launch gate
> (Braintrust: dataset/experiment; Langfuse: dataset/dataset-run; W&B Weave:
> Evaluation/Model; Inspect: Task/EvalLog). Our "variant" = their "experiment
> configuration". This is settled and we should not invent a fifth vocabulary.

## Rule ordering caveat (from note 06 §1, restated here for the record)

⚠️ **LangSmith rule ordering is *not* guaranteed** — a cascade cannot be expressed as rule
sequencing; it must be expressed as **feedback-predicate filters** (rule B filters on the
feedback key rule A wrote). Relevant if we build the Tier2→Tier3 cascade on their primitives.
