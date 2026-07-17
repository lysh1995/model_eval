---
title: "Death of the Novel(ty): Beyond n-Gram Novelty as a Metric for Textual Creativity"
url: https://arxiv.org/abs/2509.22641
html_url: https://arxiv.org/html/2509.22641v2
authors: (ICLR 2026 conference paper)
year: 2025
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# The most important negative result for cheap novelty metrics

This paper is the direct rebuttal to using n-gram novelty / Creativity Index as a creativity score. Read it before committing to any novelty-based metric.

## Operational definition of creativity used

Creativity is decomposed into **three simultaneous judgments** at the expression level:
- **sensicality** — makes sense standalone
- **pragmaticality** — fits contextually
- **perceived novelty** — unusual/surprising

> "Creative expressions are those that are simultaneously judged by a human as sensical, pragmatic, and novel."

This is a directly usable operationalization: novelty alone is NOT creativity; novelty ∧ sensical ∧ pragmatic is.

## Methodology

- n-gram novelty measured via the **infinigram** package's ∞-probability metric (backoff to the longest n-gram present in reference corpora); perplexity computed as a novelty proxy against OLMo / OLMo-2 training corpora.
- **26 professional writers** recruited via listservs of top US MFA writing programs, plus published writers.
- Close-reading annotations on **100 fiction passages**: 50 human-written (The New Yorker), 50 AI-generated.

## Validation numbers (verbatim)

- n-gram novelty IS positively associated with creativity: **OR ≈ 1.96 per SD, p < 0.001**.
- BUT: "Approximately 91% of top-quartile n-gram novel expressions are not judged as creative" (95% CI: [0.90, 0.92]).
- "approximately 79% of unique such expressions not judged as creative by any of the annotators."
- False negatives too: "approximately 25% of unique creative expressions fall below the mean perplexity," with "8% in the lowest quartile."

**Interpretation:** n-gram novelty has a real but weak signal, catastrophic precision (~9%), and meaningful recall loss. Usable as a *population-level* directional indicator; unusable as a per-response creativity score.

## LLM vs human novelty findings

- Frontier models (GPT-5, Claude-4.1) showed "significantly higher probability of expressions judged creative" for humans compared to AI.
- Open-source LLMs: "higher n-gram novelty negatively affects pragmaticality of AI-generated text" (**OLMo-2: β = -0.48, p < 0.001**), while human text showed **no such effect**.
- **Critical for us:** for weaker models, pushing novelty up actively breaks coherence. Novelty and pragmaticality trade off in models but not in humans. A novelty metric alone can be gamed by turning up temperature and producing incoherent text that *scores better*.

## Recommendation from the authors

> "LLM-as-a-Judge novelty scores align with expert writer preferences more so than an n-gram based metric"

i.e. frontier LLMs beat n-gram approaches at *expression-level* creativity evaluation. Note the tension with the TTCW result (LLM judges ~zero correlation at *story level*). Reconciliation: judges may be better at localized, narrow expression-level novelty calls than at holistic story-level creativity verdicts.
