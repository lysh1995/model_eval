---
title: "Statistical power and sample size for detecting eval regressions"
url: https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc
authors: Various practitioner sources; Cohen (1988) conventions
year: 2025
type: blog/practitioner (compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Power and sample size for eval regressions

Sources compiled:
- "Eval Set Sizing: The Statistical Power Math Behind LLM A/B Tests" — https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc
- "How Sample Size Affects LLM Prompt Testing" — https://latitude.so/blog/sample-size-affects-llm-prompt-testing/
- "A/B Testing LLM Prompts: The Statistical Playbook (2026)" — https://futureagi.com/blog/ab-testing-llm-prompts-best-practices-2026/
- MEERA, Power Analysis, Statistical Significance & Effect Size — https://meera.seas.umich.edu/power-analysis-statistical-significance-effect-size.html

## Working formula (continuous scores, two independent arms)

```
n_per_arm = 16 · σ² / MDE²
```
at `α = 0.05`, **80% power**, two-sided. (The 16 comes from `2(z_{1-α/2} + z_{1-β})² ≈ 2(1.96+0.84)² ≈ 15.7`.)

General form:
```
n_per_arm = 2 · (z_{1-α/2} + z_{1-β})² · σ² / Δ²
```
- 80% power, α=0.05 → constant ≈ **15.7**
- 90% power, α=0.05 → constant ≈ **21.0**

## Paired designs — the big win

"The **paired** McNemar test should be used when both prompts run on the same questions, and it
**frees up an order of magnitude of compute**."

"Paired tests can have significantly more statistical power, allowing detection of effects with much
smaller sample sizes, which is especially useful for LLM experiments that have increased time and
financial costs."

Paired formula — the relevant variance is the variance of the **difference**, not the raw score:
```
n_pairs = (z_{1-α/2} + z_{1-β})² · σ²_d / Δ²
where σ²_d = σ²_A + σ²_B − 2ρ·σ_A·σ_B
```
When scenario difficulty dominates (large `σ²_i`, which is exactly our situation), `ρ` between arms
is high, `σ²_d` collapses, and `n_pairs` drops dramatically. **Run every model variant on the
identical scenario set and pair the analysis.** This is the cheapest power win available to us and
it costs nothing but discipline.

## Rules of thumb quoted

- "If you only care about catching regressions of **10 points or more, 250 examples** is sufficient."
- "If you want to catch a **2-point lift, you need thousands of examples per arm** or you are
  guessing."

## The correlation trap

"since LLM outputs are often **correlated** and produce similar responses, misjudging sample sizes
can shift performance metrics by up to **10%** and rankings by **5 positions**, so statistical
methods should be used to calculate the right sample size **while adjusting for correlations**."

Our observations are nested (turns within conversation, conversations within character, characters
within language). Treating 190 slices × k scenarios as independent samples **overstates N**. Use a
**design effect** correction:
```
DEFF = 1 + (m − 1)·ICC        n_effective = n_raw / DEFF
```
where `m` = average cluster size and `ICC` = intra-cluster correlation. With `m = 10` scenarios per
character and `ICC = 0.2`, `DEFF = 2.8` — we have **~1/3 the sample size we think we have**.

Alternative and better: fit a **mixed-effects model** with random intercepts for character and
scenario, which handles the nesting directly.

## Relevance to companion-eval

Two numbers must be decided *before* building: (1) the **MDE** — the smallest score regression we
actually care about catching; (2) `σ`, measured from a pilot. Everything else follows. Without a
declared MDE, "how many scenarios do we need" is unanswerable and any answer is arbitrary.
