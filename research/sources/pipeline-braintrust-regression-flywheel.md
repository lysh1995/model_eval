---
title: "How to turn LLM production failures into regression tests"
url: https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests
org: Braintrust
year: 2026
type: vendor-engineering-guide
accessed: 2026-07-16
topic: eval-lifecycle
---

# Braintrust: production failures → regression tests

The most concrete published description of the flywheel's back-half. Five steps:

> **capture failed traces → diagnose failure mode → promote to dataset → write scorer → gate releases**

## 1. Capture the failed trace

Trace must include: original input, model output, intermediate tool calls, retrieved
context, runtime metadata. *"The trace becomes the reproducible source of truth for the
failure."*

> This is a **schema requirement stated as a workflow requirement**: if the generation
> event doesn't carry enough to *replay* the failure, the failure can never become a test.
> Anything not logged at generation time is permanently unavailable to the benchmark.

## 2. Diagnose failure mode — a fixed taxonomy of five

- **Hallucination** — unsupported claims without source backing
- **Retrieval miss** — right source exists but wasn't surfaced
- **Tool argument error** — wrong format or omitted required fields
- **Instruction-follow failure** — ignored system/user constraints
- **Format violation** — mismatched schema or data types

> **This taxonomy is a RAG/agent taxonomy and only ~2 of 5 transfer to us.** We have no
> retrieval and no tools. Ours are instruction-follow failure and format violation (both
> already in note 11's Lane 1), plus companion-specific modes with no analogue here:
> persona drift, repetition/looping, voice homogenization, sycophancy, boundary erosion.
> **The *practice* of a closed failure-mode enum transfers; the enum does not.** Worth
> noting that every published flywheel writeup assumes a RAG/agent app — nobody has
> published a companion/roleplay flywheel taxonomy. Ours must come from note 07/11.

## 3. Promote to regression dataset

```typescript
const dataset = initDataset("My App", { dataset: "Customer Support" });
dataset.insert({
  input: { question: "How do I reset my password?" },
  expected: { answer: "Click 'Forgot Password' on the login page." },
  metadata: { category: "authentication", difficulty: "easy" },
});
await dataset.flush();
```

Alternatives: manual promotion from Logs UI (select traces → **+ Dataset**); BTQL backfill
using the **`origin`** field linking to the source span.

Dataset row fields: `input`, `expected`, `metadata`, `origin`.

> **`origin`** = the same back-pointer idea as Langfuse's `sourceTraceId`. Two independent
> vendors converged on "a benchmark item must remember which production trace it came
> from." Treat as settled practice.
>
> ⚠️ **`expected` is a problem for us.** This whole workflow assumes a *reference answer*
> exists. Note 11's entire premise is that "is this good?" has no stable answer
> (α=0.25–0.34) and that we must judge **pairwise against a frozen anchor**, not against
> a gold response. **Our dataset item cannot have an `expected` field in this sense** — it
> has a character card, a conversation prefix, and an anchor set. The industry-standard
> dataset shape does not fit a creative-generation product, and we should not contort
> ourselves into it.

## 4. Write scorers

- **Semantic failures** → LLM-as-a-judge; scorer prompt references `{{output}}`, returns
  configurable choice scores (e.g. A=1, B=0.5, C=0)
- **Deterministic failures** → custom code; schema compliance, exact match, field presence;
  returns `score` (0 or 1) + optional `metadata`

Both use a **`__pass_threshold`** metadata field to mark passing/failing scores.

Scorer primitives: `name`, `slug`, `handler`, `__pass_threshold`.

## 5. Gate releases in CI

```yaml
uses: braintrustdata/eval-action@v1
with:
  api_key: ${{ secrets.BRAINTRUST_API_KEY }}
  runtime: node
```

Runs on pull requests, posts results back to PR, blocks merges if scorer thresholds fail.

## The closed loop

Same dataset + scorer runs **in CI** (`eval-action`) and **on live traffic** via **online
scoring rules**:

> production failures → datasets → scorers → CI gates → production monitoring

> **"One scorer, two call sites" again** — same primitive as W&B Weave's guardrail/monitor
> duality (note 06 §1). Three vendors independently converged. **The scorer must be a
> deployable artifact runnable in both CI and streaming context.** That is an architectural
> constraint on how we write Lane 1/2 code: no notebook-only metrics.

## Gating advice (verbatim-ish, and unusually good)

- **Schema validators: require perfect scores (1.0)** to catch breaking changes
- **LLM-as-a-judge: calibrate the threshold BELOW measured human-scorer agreement** to
  account for judge variance
- **Start in shadow mode before making scorers blocking CI checks**
- **Revalidate judge scorers against human labels when prompt or model version changes**

> These four map 1:1 onto our design and independently confirm it:
> - "calibrate below human agreement" — our κ≈0.53 ceiling (note 11 §7) *is* that bound.
>   A gate stricter than the instrument's reliability is a coin flip with a changelog.
> - "start scorers in shadow mode" — **the evaluator itself gets a rollout**, not just the
>   variant. Note 11 §deployment gate ("no dimension ships without its noise floor") is the
>   same rule stated statistically. **A new metric is a change that needs a canary.**
> - "revalidate when prompt or model version changes" — note 11 §8: a judge bump is a
>   breaking change requiring re-baseline.
