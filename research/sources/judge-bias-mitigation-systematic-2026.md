---
title: "Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines"
url: https://arxiv.org/abs/2604.23178
authors:
  - Sadman Kabir Soumik
year: 2026
type: paper (preprint, single independent author — see credibility note)
accessed: 2026-07-16
topic: llm-judge
---

# Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines (2026)

> **Credibility note:** single-author independent preprint (April 2026), not peer-reviewed at time of access. Treat directionally, not as settled fact. **However** it is the only source found that (a) tests mitigations head-to-head on a common footing, (b) reports cross-bias interactions, and (c) uses **2025/2026-era frontier judges** (Claude Sonnet 4, Gemini 2.5 Pro, GPT-4o, Llama 3.3-70B) rather than the GPT-4-era models every other paper uses. Its most important claims **contradict the older canon**, so it should be replicated on our own data before we rely on it.

## Abstract (opening, verbatim)

> LLM-as-a-Judge has become the dominant paradigm for evaluating language model outputs, yet LLM judges exhibit systematic biases that compromise evaluation reliability.

## Methodology

Nine mitigation strategies tested, grouped by cost multiple:

**Single-call (1× cost):**
- **B0** — Baseline (minimal prompt)
- **S4** — Calibrated Rubric (5-criteria scoring)
- **S5** — Chain-of-Thought (step-by-step analysis)

**Multi-call aggregation:**
- **S1** — Position Swap (**2× cost**, reversed A/B order)
- **S2** — Same-Family Ensemble (**3× cost**, temperature variation)

**Combined:**
- **S8** — Combined Budget = position swap + CoT + rubric (**2× cost**)

Evaluated on MT-Bench (n=400, natural data) and LLMBar (adversarial data). Statistical testing with **Holm–Bonferroni correction** — notable rigor; most judge papers report uncorrected deltas.

## Key numbers

### Effects by bias type

**Style bias — the dominant finding:**
- Baseline: **0.76–0.92** across all models (very high)
- **S8 (combined)** reduces to **0.58** average (**−0.26**, from 0.84 → 0.58)
- **CoT alone: −0.14**

**Position bias:**
- **Negligible: ≤0.04 across all models**
- Position swap (S1) gains only **+4.6pp for Gemini 2.5 Pro** (p=0.012, marginal)

**This is the headline update.** In MT-Bench (2023), GPT-4 flipped verdicts on 35% of pairs from ordering. On 2025/26 frontier models, this paper measures position bias at ≤0.04. **Position bias appears to have been largely engineered out of frontier judges — while style bias has not.** If replicated, this reallocates our mitigation budget away from swap-and-average and toward style control.

**Verbosity bias:**
- Expansion pairs: **−0.20 to −0.76** — i.e. these judges show a **conciseness preference**, the *opposite* sign to the 2023 literature
- Truncation accuracy: **0.92–1.00** — judges reliably distinguish genuine quality from mere length
- Rubric reduces by **−0.11** average

**Self-preference bias:**
- **Highly model-dependent: −0.48 to +0.56.** Some models *disfavor* their own outputs. There is no universal constant to subtract.

### Cross-bias interactions (Figure 2) — the most actionable finding

| Strategy | Style bias | Verbosity bias |
|---|---|---|
| **Position swap** | **−0.12** | **+0.07 (worse!)** |
| **CoT** | **−0.14** | no increase |
| **S8 (combined)** | **−0.26** (0.84 → 0.58) | — |

> "Position swap reduces style bias but increases verbosity bias, a cross-bias interaction that single-strategy evaluations would miss."

**Mitigations are not independent and not free.** Fixing one bias can worsen another. Any paper (or engineer) that evaluates one mitigation against one bias in isolation will overstate its value. **CoT is the best single move: largest style reduction with no verbosity penalty, at 1× cost.**

### MT-Bench results (Table 1, n=400), after Holm–Bonferroni correction

**Statistically significant:**
- **Claude Sonnet 4 + S8: +11.2pp** (p<0.0001, **κ = 0.530**)
- Claude Sonnet 4 + S5 (CoT): **+7.2pp** (p=0.004)
- Gemini 2.5 Pro + S1 (swap): +4.6pp (p=0.012, marginal)

**Directional but not significant:**
- GPT-4o + S8: +2.8pp
- Llama + S8: +3.8pp
- Gemini Flash + CoT: +2.5pp

**Sign test across all 20 configurations: 18/20 positive (p<0.001).** So mitigations reliably help, but the effect is small and mostly below per-config significance — you need the aggregate to see it.

### Absolute performance — the sobering number

- **Best accuracy: Claude Sonnet 4 + S8 = 70.0% agreement, κ = 0.530**
- Budget option: **Llama 3.3-70B + S8 = 68.5% agreement, zero API cost**

**κ = 0.530 is "moderate" agreement on the Landis–Koch scale — for the best configuration of the best judge with every mitigation stacked on.** Compare to MT-Bench's advertised 85%: that was raw percent agreement on non-tie votes. When you use chance-corrected κ on realistic data, the best judge is *moderate*, not *human-equivalent*. **This is the single most important number in this file for calibrating expectations.**

## Practical recommendations (Algorithm 1)

1. **Adversarial / high-stakes:** use **CoT (S5)** for all models (+1.5 to +13.0pp on LLMBar)
2. **Natural evaluation data (MT-Bench-like):** model-specific strategy selection
3. **Budget-constrained:** Llama 3.3-70B + S8 (68.5% agreement, zero API cost)
4. **Best accuracy:** Claude Sonnet 4 + S8 (70.0%, κ=0.530)
5. **Default when unknown:** **CoT — 1× cost, universally positive**

## Implications for our platform

- **CoT is the default, cheapest, safest mitigation.** 1× cost, positive everywhere, no cross-bias penalty. (But note CALM finds CoT *itself* is a bias vector — RR 0.56–0.75. Both can be true: CoT improves agreement while making verdicts sensitive to whether CoT is used. Consistency in *always* using it is what matters.)
- **Style bias is the real enemy at 0.76–0.92 baseline**, and even the best mitigation stack only gets it to 0.58. This is the "unfixable by prompting" bias — it needs the statistical Bradley-Terry style-control treatment, not a better judge prompt.
- **Position swap may be a poor use of 2× budget on modern judges** (position bias ≤0.04) and actively worsens verbosity bias. This is the most counterintuitive result and the one we should verify on our own judges first — but if it holds, our default protocol should *not* be swap-and-average.
- **Self-preference has no universal sign** — must be measured per judge/candidate pair, cannot be assumed or subtracted with a constant.
