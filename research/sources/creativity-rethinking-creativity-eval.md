---
title: "Rethinking Creativity Evaluation: A Critical Analysis of Existing Creativity Evaluations"
url: https://arxiv.org/abs/2508.05470
html_url: https://arxiv.org/html/2508.05470v3
year: 2025
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# Critical survey — the metrics disagree with each other

Surveys **four representative creativity measures** across granularity levels ("token level, n-gram patterns, part-of-speech and syntactic structures, as well as semantic and holistic evaluation dimensions"):

1. **Creativity Index (CI)** — phrase-level originality via n-gram overlap with web corpora
2. **Perplexity (PPL)** — token-level unexpectedness from LM probabilities
3. **Syntactic Templates** — structure-level novelty via common POS patterns
4. **LLM-as-a-Judge** — holistic, chain-of-thought + rubric prompting

## Criticisms (verbatim)

**Creativity Index:**
- "Reflects primarily lexical diversity" rather than conceptual originality
- "strong sensitivity" to parameter choices — L-uniqueness ranges 5–7 vs 5–11 produce substantial score variations
- Highly dependent on reference corpus selection

**Perplexity:**
- Score distributions for creative and uncreative texts "overlap substantially across all domains"
- Reflects "fluency rather than novelty"

**Syntactic Templates:**
- "Ineffective in settings dominated by formulaic language"
- Identifies stylistic patterns but misses conceptual creativity

**LLM-as-a-Judge:**
- "bias towards particular labels" and "one-sided predictions"
- only **"40% consistency across three runs"** for repeated evaluations
- **"weak correlation with human evaluators" (Pearson r = 0.159)**
- unstable under minor prompt variations — **~20% contradictory judgments**

## The headline problem

> "Different metrics often disagree on the same data points" — e.g. CI suggests one dataset is more creative while perplexity indicates the opposite.
> "metrics that distinguish creativity in one domain fail in others."

**No convergent validity.** Four metrics that all claim to measure "creativity" do not agree. This means: pick metrics for a *specific declared sub-construct*, define that construct in the spec, and never average them into one "creativity score" and claim it's meaningful.

## Numbers to hold onto for judge design

- LLM judge repeat-run consistency: **40%** across 3 runs
- LLM judge vs human: **Pearson r = 0.159**
- Prompt-variation flip rate: **~20%**

These are the numbers that justify: fixed seeds, fixed judge model version, N≥3 repeats with median aggregation, and treating any judge delta below the noise floor as non-significant.
