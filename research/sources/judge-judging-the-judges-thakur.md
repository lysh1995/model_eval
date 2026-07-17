---
title: "Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges"
url: https://arxiv.org/abs/2406.12624
authors:
  - Aman Singh Thakur
  - Kartik Choudhary
  - Venkat Srinik Ramayapally
  - Sankaran Vaidyanathan
  - Dieuwke Hupkes
year: 2024
venue: GEM 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges

## Abstract (opening, verbatim)

> Offering a promising solution to the scalability challenges associated with human evaluation, the LLM-as-a-judge paradigm is rapidly gaining traction as an approach to evaluating large language models (LLMs).

## Methodology

**Thirteen judge models** evaluating **nine exam-taker models**. The study deliberately uses a setup with objectively checkable answers (TriviaQA), so "correct" is known and judge alignment can be measured against ground truth rather than only against other humans.

## Key findings and numbers

### Percent agreement is a misleading metric — use Cohen's κ

**This is the paper's most important methodological contribution and the one most relevant to us.**

> "judges with high percent agreement can still assign vastly different scores"

Percent agreement is inflated by the base rate. If 80% of answers are good, a judge that says "good" unconditionally scores 80% agreement while carrying zero information. **Cohen's κ corrects for chance agreement and reveals gaps that percent-agreement masks.**

This directly undercuts the famous MT-Bench "80%+ agreement = human-level" claim: that number is raw percent agreement on a distribution with a strong base rate. The paper explicitly frames this as "rediscovering the importance of using sophisticated metrics beyond percent alignment."

**Implication for us: we must report Cohen's κ (or Krippendorff's α for >2 raters), never raw percent agreement, when validating our judge.**

### Alignment is weak except at the very top

- Only the **largest models** achieved reasonable human alignment.
- Even for those, **assigned scores may still differ by up to 5 points from human-assigned scores** (on the paper's scale). A 5-point divergence on a Likert scale is enormous — it means absolute scores are essentially uninterpretable even when the *ranking* is roughly right.

### Vulnerabilities

Judges exhibited:
- **Sensitivity to prompt complexity and length**
- **A tendency toward leniency** (systematic upward bias in scoring)

The authors caution these vulnerabilities appear even in **"comparatively simple setups"** — i.e. the failures are not exotic edge cases; they show up in the easy case, which implies they are worse in the hard, subjective case (like ours).

### Scoring scale sensitivity

The paper demonstrates that the choice of scoring scale materially changes results — judges do not use scales uniformly, and the same underlying quality maps to different numbers under different rubric designs.

## Implications for our platform

1. **Report κ, not percent agreement.** Any validation dashboard reporting "our judge agrees with humans 85% of the time" is self-deception. Compute chance-corrected agreement.
2. **Absolute pointwise scores are not trustworthy** — up to 5 points of drift vs humans. Use them for ranking/regression detection, never as an absolute quality claim ("our character scores 8.2/10 on fidelity" is not a defensible statement).
3. **Leniency bias means score compression at the top.** If judges are lenient, good variants bunch near the ceiling and we lose the resolution we need to detect regressions among strong variants.
4. Scale/rubric design is a first-class versioned artifact, not a prompt detail.
