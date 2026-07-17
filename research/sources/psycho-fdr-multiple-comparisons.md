---
title: "Benjamini-Hochberg FDR control and multiple comparisons"
url: https://www.jstor.org/stable/2346101
authors: Yoav Benjamini, Yosef Hochberg (1995); Benjamini & Yekutieli (2001)
year: 1995
type: paper (compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Multiple comparisons and false discovery rate control

Sources compiled:
- Benjamini & Hochberg, "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing", JRSS-B 1995 — https://www.jstor.org/stable/2346101
- Benjamini & Yekutieli, "The control of the false discovery rate in multiple testing under dependency", Annals of Statistics 29(4), 2001 — https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-4/The-control-of-the-false-discovery-rate-in-multiple-testing/10.1214/aos/1013699998.full
- Statsig docs, Benjamini-Hochberg procedure — https://docs.statsig.com/experiments/statistical-methods/methodologies/benjamini-hochberg-procedure

## FDR vs FWER

- **Bonferroni** controls the **Family-Wise Error Rate (FWER)** — "the chance of at least one false
  positive". Threshold `α/m`. Very conservative; with `m` = 190 slices, `α = 0.05` becomes
  `0.00026`, and we will never detect anything.
- **Benjamini-Hochberg** controls the **False Discovery Rate (FDR)** — "the expected proportion of
  false positives when you reject the null hypothesis". "Controlling the FDR instead of the FWER is
  **less stringent and increases the method's power**."

Formal definition: `FDR = E(V/R)` where `V` = number of rejected true null hypotheses and `R` =
total number of rejected null hypotheses.

## The BH procedure

1. Conduct `m` tests, obtain p-values `p_1 … p_m`.
2. **Sort ascending**: `p_(1) ≤ p_(2) ≤ … ≤ p_(m)`.
3. Find the **largest** `k` such that:
   ```
   p_(k) ≤ (k / m) · q
   ```
   where `q` is the target FDR (e.g. 0.10).
4. **Reject all hypotheses `H_(1) … H_(k)`** — including any with p-values larger than their own
   individual threshold. (This step-up behaviour is what people implement wrong.)

Equivalently, BH-adjusted p-values: `p_adj(k) = min_{j≥k} ( m/j · p_(j) )`, capped at 1.

## Validity conditions

- BH "controls the FDR when the null p-values are **independent** of each other."
- It also controls FDR "when the test statistics have **positive regression dependency** (PRDS)" on
  the true-null test statistics.
- Under **arbitrary dependence**, use **Benjamini-Yekutieli**: divide `q` by the harmonic number
  `H_m = Σ_{i=1}^{m} 1/i`. This is much more conservative (for m=190, `H_m ≈ 5.9`, so effectively
  `q/5.9`).

## Choosing q

FDR is a *decision*, not a constant. `q = 0.05` for shipping decisions; `q = 0.10`–`0.20` is normal
and defensible for **screening / exploratory** slice analysis, where the cost of a false alarm is a
wasted investigation rather than a bad launch.

## Relevance to companion-eval

We have **95 characters × 2 languages = 190 slices**, times however many dimensions. At `α = 0.05`
uncorrected, we expect **~9.5 false "regressions" per dimension per release** from pure noise. A
team chasing those will lose trust in the platform within two releases.

Design implication — a **two-tier testing policy**:
- **Tier 1 (gate)**: one pre-registered pooled test per dimension. This is the ship/no-ship
  decision. No correction needed — it is one test.
- **Tier 2 (screen)**: per-slice tests, BH-corrected at `q = 0.10`, reported as *investigate*, never
  as *block*.

Slices are **positively correlated** (same model, same judge, overlapping scenarios), so plain BH
under PRDS is defensible; BY is the conservative fallback if we ever need airtight guarantees.
