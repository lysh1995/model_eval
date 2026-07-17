---
title: "Rubric and anchor design: BARS, grading scales, and LLM-judge calibration"
url: https://arxiv.org/abs/2601.03444
authors: Weiyue Li, Minda Zhao, Weixuan Dong, Jiahui Cai, Yuze Wei, Michael Pocress, Yi Li, Wanyan Yuan, Xiaoyue Wang, Ruoyu Hou, Kaiyuan Lou, Wenqi Zeng, Yutong Yang, Yilun Du, Mengyu Wang; plus Liu et al. (G-Eval, 2023); Smith & Kendall (BARS, 1963)
year: 2026
type: paper (compilation)
accessed: 2026-07-16
topic: psychometrics
---

# Rubric / anchor design and why unanchored Likert fails

Sources compiled:
- Li et al., "Grading Scale Impact on LLM-as-a-Judge: Human-LLM Alignment Is Highest on 0-5 Grading Scale", arXiv 2601.03444 (Jan 2026) — https://arxiv.org/abs/2601.03444
- Masood, "Rubric-Based Evaluations & LLM-as-a-Judge — Methodologies, Biases, and Empirical Validation" — https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80
- "LLM-as-a-Judge in 2026: How It Works, When It Fails" — https://futureagi.com/blog/llm-as-a-judge/
- Smith & Kendall (1963), original BARS formulation

## Grading scale choice (Li et al. 2026)

Direct empirical finding: **"the grading scale of 0-5 yields the strongest human-LLM alignment."**

Also: "LLM judgments are **not perfectly consistent across scales** on subjective benchmarks" — the
same judge on the same content gives non-equivalent orderings depending on whether you asked for
0-5 vs 0-10 vs 0-100. And: important variations in alignment exist **across demographic groups**.

The scale is not a neutral container. It is part of the instrument.

## Why unanchored Likert collapses

"A Likert rubric **without exemplars tends to collapse toward central scores** because judges do not
share the same latent image of what a '3' versus a '5' means."

"LLM judges exhibit **central tendency bias** on broad scales, which is why practitioners are
encouraged to use narrower scales (e.g. 1-5) as opposed to broad scales (e.g. 1-10 or 1-100)."

Remedy: "The industry standard solution is the use of **anchor examples**, providing real-world,
concrete examples of exactly what a 1 looks like, what a 3 looks like, and what a 5 looks like."

## Behaviorally Anchored Rating Scales (BARS)

Origin: Smith & Kendall (1963), industrial/organizational psychology. Built to solve exactly our
problem — getting different human raters to mean the same thing by the same number.

Construction procedure (the classic five steps):
1. **Critical incident generation** — SMEs write concrete examples of actual observed behaviour,
   good and bad.
2. **Dimension definition** — cluster incidents into dimensions; define each.
3. **Retranslation** — a *second, independent* group of SMEs re-sorts the incidents back into
   dimensions blind. **Incidents that fail to sort back into their original dimension (typically
   <60-75% agreement) are discarded.** This is the step everyone skips and it is the step that does
   the work — it is an empirical test of whether your dimension is even coherent.
4. **Scaling** — surviving incidents are rated for effectiveness level; incidents with high SD across
   raters are discarded.
5. **Instrument construction** — the surviving incidents become the scale anchors.

Key property: anchors are **observable behaviours**, not adjectives. "Introduces an unprompted plot
complication that references an earlier turn" is an anchor. "Highly creative" is not.

## Known LLM-judge biases

- **Position bias** — order of presentation in pairwise comparisons.
- **Verbosity bias** — longer responses score higher independent of quality.
- **Self-enhancement bias** — judges prefer outputs from their own model family.
- **Central tendency bias** — see above.

Mitigations: structured rubrics with explicit scoring criteria; randomize/counterbalance position and
report the position-swap agreement rate; control for length.

## G-Eval

Liu et al. 2023. "chains-of-thought through the rubric then returns a score **weighted by token
probability**." Probability-weighted scoring produces a continuous score rather than a lumpy integer,
which reduces the granularity loss of a 1-5 scale and improves correlation with human judgments.

Useful for us: token-probability weighting gives finer resolution *without* widening the scale (which
we now know hurts alignment). Best of both.

## Relevance to companion-eval

The BARS retranslation step is the highest-leverage and least-glamorous thing on this whole list. If
our own team cannot blind-sort example transcripts back into "creativity" vs "character consistency"
above ~70%, those two dimensions are **not distinct constructs** and no downstream statistics will
fix it. Run retranslation before writing a line of scoring code.

Concrete rubric spec implied by this file:
- **0-5 scale** (empirically best aligned)
- **Every level has a behavioural anchor** drawn from a real transcript
- **Anchors survived retranslation**
- Judge emits CoT then score; score read via **token-probability weighting**
- Position **counterbalanced**; length logged as a covariate
