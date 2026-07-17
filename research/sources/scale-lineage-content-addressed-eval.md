---
title: "Eval reproducibility & lineage: content-addressed artifacts, judge pinning, prompt/dataset versioning"
url: https://github.com/MohamedAklamaash/redharness
org: composite — redharness (GitHub), Atlan LLMOps lineage guides, Cloudsmith LLMOps artifact management
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Reproducibility / lineage for eval scores

Requirement from our brief: **keep every score traceable to (variant, evaluator
version, data).** This file collects the published patterns for that.

## The `redharness` pattern — the most directly applicable prior art found

Self-description (LLM red-teaming benchmark across jailbreak / prompt-injection /
data-leakage):

> Standardized, reproducible LLM red-teaming benchmark across three surfaces
> (jailbreak · prompt-injection · data-leakage) under one methodology — **judge-pinned
> provenance** and a **judge-sensitivity study**. **Offline-deterministic core**;
> opt-in live model eval. Standardize the evaluation, not just the attack.

The mechanics, as reported:

> uses **content-addressed datasets (hash-pinned) verified before use**, with
> **execution deterministically seeded** and **attempts cached on their fully resolved
> parameters**.

Four ideas worth stealing verbatim:

1. **Content-addressed, hash-pinned datasets, verified *before* use.** The eval refuses
   to run against a dataset whose hash doesn't match the manifest. This turns "which
   data was this scored on?" from a bookkeeping question into an enforced invariant.
2. **Judge-pinned provenance.** The judge model+prompt is pinned and recorded as part of
   the result identity — a score is meaningless without knowing which judge produced it.
3. **Judge-sensitivity study.** They explicitly measure *how much the result changes if
   you swap the judge.* This is the discipline that answers "is this regression real, or
   did our evaluator drift?" — the single most important confounder in continuous
   monitoring.
4. **Cache attempts on their fully resolved parameters.** The cache key is the complete
   resolved config, not a human-assigned version string. This means an accidental config
   change *cannot* silently reuse a stale result.

## General LLMOps lineage guidance (Atlan / Cloudsmith)

> Automating lineage tracking ensures every inference result is traceable back to the
> specific **model version, prompt, and dataset** used.

> Every evaluation run can be versioned so you can trace **which model, prompt,
> dataset, and evaluation logic produced which metrics**, ensuring perfect auditability
> and experiment reproducibility.

> Training datasets can be versioned at each stage using **content hashes**.

> For LLM workflows, versioning **prompt templates, fine-tuned adapters, and retrieval
> configurations** ensures full reproducibility and regulatory traceability.

> Connecting a specific version back to the dataset and prompts enables unambiguous
> **root-cause analysis of model drift**, accuracy and precision issues, and performance
> degradation over time.

Note the four-part tuple that recurs across every source: **model version + prompt +
dataset + evaluation logic**. Our brief's "(variant, evaluator version, data)" triple is
missing *evaluation logic* as a distinct axis — worth separating, because the rubric
prompt and the scoring/parsing code can drift independently.

## Anthropic-API-side lineage primitives available to us

(cross-referenced from `scale-anthropic-pricing-batch-caching.md`)

- **`response._request_id`** — the `request-id` header, populated on every response;
  the join key to Anthropic-side traces.
- **`response.model`** — the model that *actually* served the message. **Do not assume
  it equals the requested model.** With server-side fallbacks or sticky routing, a
  request nominally to model A can be served by model B. A lineage record that logs the
  *requested* model is wrong; log `response.model`.
- **`response.usage.iterations`** — per-attempt token accounting; the source of truth
  when a fallback fired.
- **Structured outputs schema cache** — "New schemas incur a one-time compilation cost.
  Subsequent requests with the same schema use a **24-hour cache**." Implication: the
  schema is itself a versioned artifact whose identity affects behavior and latency.

## Recommended content-addressed identity for our platform

Make an eval score's identity a hash over the **fully resolved** inputs:

```
score_id = H(
    variant_id,            # which companion variant produced the generation
    generation_id,         # content hash of the generation being judged
    evaluator_id = H(      # <- the "evaluator version", content-addressed
        rubric_prompt_text,     # NOT a version string — the actual bytes
        judge_model_id,         # e.g. claude-haiku-4-5
        judge_params,           # effort, thinking, output schema
        scoring_code_version,   # git SHA of the parse/aggregate logic
    ),
    sampling_stratum_id,   # which stratum this was drawn from
    inclusion_prob,        # pi_i — see scale-horvitz-thompson-reweighting.md
)
```

Two non-obvious points, both learned from the sources above:

- **Hash the rubric *bytes*, not a version label.** Human-assigned version strings drift
  from reality (someone edits the prompt without bumping the label). Content-addressing
  makes that impossible. This is the redharness "resolved parameters" lesson.
- **`inclusion_prob` (π_i) is lineage, not telemetry.** Sampling rates change over time;
  once they do, π_i cannot be reconstructed from a config file after the fact. If it
  isn't stored on the record at sample time, every historical global estimate becomes
  uncomputable. (See the HT source file.)

## The judge-drift problem — the thing most teams miss

`redharness`'s **judge-sensitivity study** is the important idea here. In continuous
monitoring, a "regression" has (at least) three possible causes:

1. the variant actually got worse;
2. the traffic mix shifted (a harder character got popular) — **composition drift**, not
   quality drift;
3. **the evaluator changed** (rubric edit, judge model silently upgraded, provider-side
   model update).

Cause 3 is invisible unless the evaluator is content-addressed and pinned. Cause 2 is
invisible unless scores are sliced (which is the whole point of our stratification).
**A monitoring system that cannot distinguish these three will generate confident,
wrong alerts.** Concretely, this argues for:

- **pinning the judge model to a dated/exact ID** and treating a judge-model change as a
  release requiring back-comparison;
- **maintaining a frozen golden set** re-scored on every evaluator version bump — if the
  golden-set scores move, the *evaluator* moved, and any production score delta in that
  window is confounded;
- **reporting sliced metrics by default**, so composition shifts don't masquerade as
  quality shifts.
