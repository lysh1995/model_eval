---
title: "Inspect AI — eval log format and reproducibility model"
url: https://inspect.aisi.org.uk/eval-logs.html
org: UK AI Security Institute (AISI)
year: 2026
type: framework-docs
accessed: 2026-07-16
topic: eval-lifecycle
---

# Inspect (UK AISI) — the reproducibility bar

Framework home: https://inspect.aisi.org.uk/

The one eval framework in this survey built by a government safety institute rather than a
vendor, and the only one whose **stated primary goal is reproducibility**:

> "The motivation behind Inspect is to **improve the reproducibility of evals**, especially
> for large-scale evaluations of frontier models."
> "Inspect captures **all the context required to debug, analyze, and, most importantly,
> reproduce an evaluation**."

## Primitives

```
dataset -> Task -> Solver -> Scorer
```

- **Dataset**: "your set of test cases, each with an **input** (the prompt for the model)
  and a **target** (the correct answer or grading guidance)"
- **Task**: "combines a dataset of samples, one or more **solvers** that determine how the
  model is prompted (including multi-step agents and tool use), and a **scorer** that grades
  the model's answers"
- Multi-turn/agent workflows with tools; sandboxed execution (Docker built-in, optional
  Kubernetes/Proxmox); VS Code log viewer + web Inspect View

> **`target` = "the correct answer OR grading guidance"** — the second disjunct is the
> escape hatch we need. Inspect is the only framework surveyed that explicitly admits a
> dataset item may carry *rubric guidance* instead of a gold answer. For us the "target" is
> the **character card + frozen anchor exemplar** (note 11 §4: reference-anchor every
> judgment). **Inspect's data model accommodates our no-gold-answer problem; Braintrust's
> `expected` and LangSmith's "reference outputs" do not.**
>
> **The Solver abstraction also matters more for us than for anyone else.** Our "variant"
> = (model + params + system prompt), which is exactly a Solver + generation config — and
> note 11 §9 wants **re-anchoring frequency as a first-class variant parameter**. That is a
> *solver* property, not a model property. A framework where the prompting strategy is a
> versioned, composable object is the right shape for our variant axis.

## The EvalLog format — top-level fields (verbatim)

| Field | Type | Contents |
|---|---|---|
| `version` | int | File format version (currently **2**) |
| `status` | str | `"started"` / `"success"` / `"error"` |
| `eval` | EvalSpec | "Top level eval details including task, model, creation time, etc." |
| `plan` | EvalPlan | "List of solvers and model generation config used for the eval" |
| `results` | EvalResults | "Aggregate results computed by scorer metrics" |
| `stats` | EvalStats | "Model usage statistics (input and output tokens)" |
| `error` | EvalError | Error details if status is "error" |
| `tags` | list[str] | Current tags with post-eval edits merged |
| `metadata` | dict | Current metadata with post-eval edits merged |
| `log_updates` | list | "Post-eval edits to tags and metadata (**with provenance tracking**)" |
| `samples` | list[EvalSample] | Individual sample data: input, output, target, scores |
| `reductions` | list[EvalSampleReduction] | Sample reductions for **multi-epoch** evaluations |

The `eval` (EvalSpec) field captures:
- **task name and version**
- **model specification**
- **dataset configuration**
- **creation timestamp**
- **git revision and package versions**
- **generation parameters and solver configuration**

## File formats

| Format | Description |
|---|---|
| `.eval` | "Binary file format optimised for size and speed. Typically **1/8 the size** of `.json` files" |
| `.json` | "Text file format with native JSON representation" |

Interchangeable via the Log File API; can coexist in the same directory.

## Why this is the reproducibility reference

`EvalSpec` records **git revision + package versions + model spec + generation params +
solver config + dataset config**, all in the log itself. **The log is self-describing: you
can reconstruct the run from the artifact alone**, with no external config lookup.

> This is note 06 §7's four-part lineage tuple (**model + prompt + dataset + evaluation
> logic**) implemented, plus the environment (`git revision`, `packages`) that note 06 does
> **not** list — and which is a real gap: a metric's *scoring code* drifts with its
> dependencies. `scoring_code_git_sha` in note 06's `evaluator_id` covers our own code but
> not the tokenizer/regex library under it. **Inspect logs both. We should too.**
>
> Two more things worth stealing:
> - **`log_updates` — "post-eval edits to tags and metadata (with provenance tracking)"**.
>   Inspect assumes the log will be **annotated after the fact** (by a human, later) and
>   makes that an **append-only, attributed** operation rather than a mutation. That is
>   exactly what our human-in-the-loop does to a production trace, and it is the difference
>   between an auditable label history and a spreadsheet.
> - **`reductions` / multi-epoch** — first-class support for **running the same sample N
>   times and reducing**. Note 10's noise floor work *is* a multi-epoch reduction (σ_within
>   across n=3 runs), and note 11 §6 needs min-over-turns rather than mean. **A framework
>   with a pluggable reducer can express "min, not mean"; one that assumes one-run-per-item
>   cannot.** Most can't.
