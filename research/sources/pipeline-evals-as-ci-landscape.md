---
title: "Evals as CI — the tooling landscape (DeepEval, Vercel agent-eval, OpenAI Evals, W&B Weave)"
url: https://deepeval.com/guides/guides-regression-testing-in-cicd
org: Confident AI / Vercel / OpenAI / W&B (composite)
year: 2026
type: product-docs-composite
accessed: 2026-07-16
topic: eval-lifecycle
---

# "Evals as CI" — the tooling landscape

Composite of:
- https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd + /guides/guides-regression-testing-in-cicd
- https://github.com/vercel-labs/agent-eval
- https://evals.openai.com/
- https://docs.wandb.ai/weave/guides/evaluation/guardrails_and_monitors

## DeepEval — evals as pytest

> "simple-to-use, open-source LLM evaluation framework that is **similar to pytest but
> specialized for unit testing LLM apps**"

- Write evals as pytest tests using **`assert_test()`**, run with **`deepeval test run`** as
  a pipeline step
- **"Failing metrics fail the build, so regressions get caught before they ship"**
- **`--regression` flag compares to the previous run and fails if any metric regresses**
- "For CI, **save the baseline once on main and compare PRs against it**"
- Confident AI: designate a run as the **"official test run"** — "the marked good run that
  future runs are compared against for regressions"
- 30+ metrics, most using an **LLM judge** (G-Eval, DAG, QAG) rather than string matching

> **The "official test run" / baseline-on-main pattern is the right primitive and it is
> underrated.** It reframes the CI gate from *absolute threshold* ("score > 0.95") to
> *delta against a named, pinned baseline* — which is what promptfoo's before/after does
> too, and what note 11 §1 forces for the judge (pairwise, never absolute).
>
> ⚠️ **But `--regression` "fails if any metric regresses" is a noise machine at our σ.**
> Note 10: at n=3 runs a single (model, character) cell resolves only **19.4pp**; 2pp needs
> **281 runs**. A gate that fires on *any* downward movement of *any* metric will fire on
> essentially every PR, and the team will disable it in a fortnight. **This is the single
> most common way an eval-gate program dies**, and it is a statistics failure, not a tooling
> failure.
>
> Our gate must be: **fail if the shrunk estimate's confidence interval excludes the
> baseline by more than the dimension's declared MDE** (note 11's pre-registration gate).
> That is buildable on any of these tools, but **none of them ship it** — every framework
> surveyed compares point estimates.

## Vercel agent-eval

- `npx @vercel/agent-eval init`; experiments live in an `experiments/` directory
- "running controlled experiments, measuring **pass rates**, and comparing techniques"
- **"Automatic result reuse for matching fingerprints"**
- **Failure classification using Claude Sonnet 4.5** via the Vercel AI Gateway with
  sandboxed read-only tools
- Docker sandbox option

> **"Automatic result reuse for matching fingerprints"** = content-addressed eval results,
> again (cf. promptfoo's `hashFiles()` cache key, note 06 §7's `evaluator_id`). **Four
> independent tools have now converged on hashing the eval's resolved inputs.** For us the
> payoff is bigger than cache hits: if a variant's fingerprint is unchanged, **we must not
> re-run and must not re-score** — otherwise the same variant gets two different scores from
> judge stochasticity, and someone will notice and lose trust in the platform. **The
> fingerprint is what makes a score idempotent.**

## OpenAI Evals

Hosted at https://evals.openai.com/ — the API-side evals product (distinct from the old
`openai/evals` OSS registry repo, which was a static benchmark collection).

## W&B Weave — guardrails and monitors

- Pre-built scorers: **safety** (toxicity, bias, PII, hallucination) and **quality**
  (coherence, fluency, context relevance)
- **"Scorers can be used as Guardrails to block or modify unsafe content before it reaches
  users, or as Monitors to track quality metrics over time"**
- "A Weave evaluation **runs a function over a dataset and applies scorers**, with the result
  logged with **per-example scores and aggregate metrics**"
- **"A lower sampling rate is useful for controlling costs, as each scoring call has a cost"**
- **"test new LLMs and custom models against production traces"**

> Weave's guardrail/monitor duality and the "guardrails have no sampling rate" rule are
> already load-bearing in note 06 §1 — not repeated here. The addition relevant to
> *lifecycle*: **"test new LLMs against production traces"** is replay-based shadow eval as
> a product feature. See `pipeline-shadow-canary-rollout.md` for why replay is unsound for
> multi-turn companion traffic (the candidate is scored on a trajectory it did not generate).

## The cross-tool pattern

| Tool | CI entry point | Baseline | Gate |
|---|---|---|---|
| promptfoo | `promptfoo eval` + GH Action | before/after on changed prompt | pass-rate threshold / `--fail-on-error` |
| DeepEval | `deepeval test run` (pytest) | "official test run" on main | any metric regresses |
| Braintrust | `braintrustdata/eval-action@v1` | dataset + scorer thresholds | `__pass_threshold` |
| Vercel agent-eval | `npx @vercel/agent-eval` | fingerprint reuse | pass rates |
| Inspect | `inspect eval` | EvalLog comparison | scorer metrics |

**Every tool: (1) a CLI that runs a dataset through a config and emits structured results,
(2) a CI action that runs it on PR, (3) a comparison against a named baseline, (4) a
threshold that fails the build.** This is settled architecture — **we should not invent a
new one, we should supply a better statistic into it.**

> **The gap across all five is identical and it is ours to fill: none of them models
> measurement error.** They compare point estimates and fail on deltas. Notes 10 and 11
> exist precisely because that is invalid at our noise level. **Our differentiator is not a
> better harness — it's that our gate knows its own MDE.**
