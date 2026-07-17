---
title: "Benchmark validity critiques: The Benchmark Lottery; AI and the Everything in the Whole Wide World Benchmark; leaderboard sensitivity"
url: https://arxiv.org/abs/2111.15366
authors: Raji, Bender, Paullada, Denton, Hanna (2021); Dehghani, Tay, Gritsenko, Zhao, Houlsby, Diaz, Metzler, Vinyals (2021); Alzahrani et al. (2024)
year: 2021
type: paper (compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Benchmark validity critiques

## 1. AI and the Everything in the Whole Wide World Benchmark

Raji, Bender, Paullada, Denton, Hanna — NeurIPS Datasets & Benchmarks 2021.
https://arxiv.org/abs/2111.15366

Explores "the limits of influential benchmarks in order to reveal the **construct validity issues**
in their framing as the functionally 'general' broad measures of progress they are set up to be."

Core claim: "the reality of benchmark development, use and adoption indicates a construct validity
issue, where the involved benchmarks — due to their instantiation in particular data, metrics and
practice — **cannot possibly capture anything representative of the claims to general applicability
being made about them**."

Two named failure modes:
- **Decontextualization**: "Just because a task is unpinned to a specific context does not make it
  general."
- **Scale ≠ generality**: "simply scaling the dataset to make it very large does not make a
  benchmark open-ended, neutral or accurate — **a large closed problem is not an open problem, it is
  still of limited scope**."

Title alludes to the Grover book "The Monster at the End of This Book" / Sesame Street's "Everything
in the Whole Wide World Museum" — a museum claiming to contain everything, which in fact contains an
arbitrary handful of objects.

## 2. The Benchmark Lottery

Dehghani, Tay, Gritsenko, Zhao, Houlsby, Diaz, Metzler, Vinyals — 2021.
https://arxiv.org/abs/2107.07002

"Relative model performance is **highly sensitive to the choice of tasks and datasets** it is
measured on." "The random nature of task selection can become a **lottery that algorithms need to
win**."

Key mechanism: "Tasks within the same benchmark frequently **share design choices, data sources, or
evaluation protocols that induce high correlation**. This lack of independence is critical —
different subsets of tasks produce different winners, and **if tasks were truly independent, the
aggregate ranking should remain stable regardless of the specific subset examined**."

That last sentence is a **testable diagnostic** we can run on our own suite: bootstrap-resample the
scenario set, re-rank, and measure rank stability. If our ranking flips under resampling, our
scenario set is doing the deciding, not the models.

Also notes rankings are sensitive to **prompt formatting**, "often reversing leadership based on
minor perturbations."

## 3. When Benchmarks are Targets: Revealing the Sensitivity of LLM Leaderboards

Alzahrani et al., 2024. https://arxiv.org/html/2402.01781v2

Leaderboard rankings shift substantially under trivially innocuous perturbations — changing the
order of multiple-choice options, changing the answer-extraction method. Demonstrates that
leaderboard position can be an artifact of evaluation implementation details rather than model
capability.

## Relevance to companion-eval

Concrete practices these three imply for us:
1. **Do not claim generality.** Name the construct narrowly and state the population of scenarios it
   generalizes to. "Creativity" is a claim we cannot support; "lexical novelty and plot-initiative in
   3-turn open roleplay, en, fantasy characters" is.
2. **Test rank stability under scenario resampling** (bootstrap over items). This directly
   operationalizes the benchmark-lottery critique and is cheap — it reuses existing runs.
3. **Test rank stability under prompt-format perturbation.** If our ranking moves when we reorder
   rubric dimensions in the judge prompt, we are measuring the judge harness.
4. Correlated scenarios inflate our effective N. Report an **effective sample size**, not a raw
   count of 95 characters × 2 languages.
