---
title: "The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs"
url: https://arxiv.org/abs/2509.03730
authors: Pengrui Han, Rafal Kocielnik, Peiyang Song, Ramit Debnath, Dean Mobbs, Anima Anandkumar, R. Michael Alvarez (Caltech / Cambridge / NVIDIA)
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# The Personality Illusion — THE off-diagonal, measured, with per-cell coefficients

**Verdict up front: this is the closest thing to the "steerability matrix" that exists. They inject ONE trait persona and regress ALL SIX traits on the injection. That is a diagonal AND an off-diagonal, with signed coefficients and significance levels. The claim "nobody has measured trait-induction crosstalk" is FALSE, and this is the paper that falsifies it most directly.**

Verification: HTML fetched from `arxiv.org/html/2509.03730`, stripped to text, every quote below string-matched against the raw extraction. Numbers independently re-derived by a second agent reading the same source and they agree.

## The design — this IS a steerability matrix row

Inject a trait-specific persona (Agreeableness, or Self-Regulation), then run **logistic regression predicting the persona condition** from either (a) six self-reported traits or (b) one behavioral measure. Scales: **BFI** + **Self-Regulation Questionnaire (SRQ)**. Three prompting strategies. Coefficients reported as **β with 95% CI**.

Figure 5 caption (verbatim):

> "Figure 5: **Trait-Specific Personas Are Detectable via Self-Reports but Not Behavior.** Coefficient estimates (95% CI) from logistic regressions predict persona condition (Agreeableness or Self-Regulation vs. Default) using either six self-reported traits or one behavioral measure (sycophancy or risk-taking). Results are shown across three prompting strategies... Across strategies, self-reports reliably reveal persona presence, whereas behavioral measures do not, indicating limited transfer of persona effects to downstream behavior."

## THE DIAGONAL (verbatim)

> "Trait-specific personas lead to strong alignment on their target traits. When injecting the agreeableness persona, logistic regression reveals a significant increase in self-reported agreeableness (β≈3.6 to 4.4, p<.001). Similarly, injecting the self-regulation persona results in a significant increase in self-reported self-regulation (β≈2.2 to 2.9, p<.05)."

| Injected persona | Target trait | β | p |
|---|---|---|---|
| Agreeableness | Agreeableness | **3.6 to 4.4** | <.001 |
| Self-Regulation | Self-Regulation | **2.2 to 2.9** | <.05 |

## THE OFF-DIAGONAL (verbatim) — and it is LARGER than the diagonal

> "However, **the inter-trait relationships do not fully align with the patterns observed in RQ1** (Figure 2), where extraversion, openness, conscientiousness, and agreeableness were meaningfully positively correlated, and neuroticism was negatively associated. In contrast, we find that **injecting agreeableness produces an inconsistent effect on self-regulation (β≈−0.44 to 0.50, some n.s., up to p<.05)**, while **injecting self-regulation reduces agreeableness (β≈−1.1 to −1.8, p<.05) and openness (β≈−2.2 to −2.8, p<.001)**. Additionally, the self-regulation persona has little and often non-significant effect on neuroticism or extraversion. Notably, **conscientiousness shows a strong and significant increase when the self-regulation persona is applied (β≈4.2 to 4.8, p<.001), exceeding even the effect on self-regulation itself.**"

Assembled into the matrix form the design-under-test proposes:

| Injected ↓ / Measured → | Agreeableness | Self-Regulation | Openness | Conscientiousness | Neuroticism | Extraversion |
|---|---|---|---|---|---|---|
| **Agreeableness** | **3.6 – 4.4*** | −0.44 – 0.50 (n.s.–*) | — | — | — | — |
| **Self-Regulation** | **−1.1 – −1.8*** | **2.2 – 2.9*** | **−2.2 – −2.8*** | **4.2 – 4.8*** | ~0 n.s. | ~0 n.s. |

**Read the Self-Regulation row. The largest coefficient in the entire row is an OFF-DIAGONAL cell (conscientiousness, β≈4.2–4.8) — nearly double the diagonal cell (β≈2.2–2.9). The paper says this in as many words: "exceeding even the effect on self-regulation itself."**

That is the single most important number in this file. **A trait perturbation's largest measured effect was on a trait it was not targeting.** If the steerability matrix is real, this is a published instance of it being off-diagonal-dominant for at least one row.

Also note the **asymmetry**: SelfReg→Agreeableness is a clean negative (β≈−1.1 to −1.8, p<.05), but Agreeableness→SelfReg is noise (β≈−0.44 to 0.50, n.s.). **The matrix is not symmetric.** Crosstalk in one direction does not imply crosstalk in the reverse. Any design that assumes a symmetric matrix (or that estimates only the upper triangle) is wrong.

## The baseline trait structure it is measured against (RQ1)

Big Five predicting self-regulation, all p<.001 (per the second agent's extraction of the RQ1 section):

| Trait | β |
|---|---|
| Extraversion | **23.33** |
| Openness | **15.23** |
| Neuroticism | **−16.27** |
| Conscientiousness | **12.32** |
| Agreeableness | **11.36** |

The paper's point: the *natural* correlational structure (RQ1) and the *induced* structure (RQ3) **disagree**. Injection does not move the model along its own trait manifold — it produces a configuration that is internally incoherent relative to its baseline structure.

## The other headline: injection is visible in self-report, invisible in behavior

> "In contrast to the strong alignment observed in self-reports, **behavioral measures show limited sensitivity to persona injection.** When using downstream behavior to predict whether a persona was applied, logistic regression models yield **mostly non-significant results for both cases.** Specifically, sycophantic responses provide weak and inconsistent evidence for predicting whether the agreeableness persona was used (β≈−0.05 to 0.32, n.s. to p<.001), and risk-taking behavior similarly fails to reliably distinguish the self-regulation condition (β≈−0.14 to 0.20…)"

Models tested: **LLaMA-3.2 3B, LLaMA-3 8B, LLaMA-3.3 70B, Qwen2.5, Qwen3 235B, Mistral-7B-v0.1, OLMo2 7B, Claude 3.7 Sonnet, GPT-4o.**

Overall RQ2 result: only **~24%** of trait-task associations reached statistical significance, and of those only **~52%** matched human psychological patterns — **chance is 50%.**

## Relevance to companion-eval-platform

1. **The novelty claim "nobody has measured trait-induction crosstalk" is dead as stated.** This paper injects one trait and reads out six, with signed coefficients and p-values, on nine models including Claude 3.7 Sonnet and GPT-4o. We must cite it. Any framing that says the off-diagonal is unmeasured will be caught by the first reviewer who knows this literature.

2. **But the scope is narrow, and that is our opening.** They inject **two** personas (agreeableness, self-regulation) — that is a **2×6 slice**, not a matrix. There is no N×N sweep, no intensity ladder crossed with crosstalk (they inject at one level, not nine), and the traits are psychometric constructs, not companion-character traits ("shy", "sarcastic", "protective"). The defensible claim is: *"per-cell crosstalk coefficients exist for a 2×6 slice at a single induction strength; the full N×N matrix as a function of induction intensity does not exist."* That is narrow, real, and checkable.

3. **The off-diagonal is LARGE — plan for it, don't discover it.** SelfReg→Conscientiousness (β≈4.2–4.8) beat SelfReg→SelfReg (β≈2.2–2.9). If our matrix comes back off-diagonal-dominant we are *replicating*, not discovering. The interesting question is no longer "is there crosstalk" (yes) but "**is the crosstalk structured and predictable enough to correct for**" — that is unanswered and worth answering.

4. **Asymmetry kills the cheap version of the experiment.** A→B ≠ B→A here. We cannot estimate half the matrix and mirror it. Full N×N means N² perturbation conditions, and with an intensity ladder it is N²×L. **Budget accordingly — this is the main cost driver of the design and it should be in the proposal up front.**

5. **The self-report/behavior dissociation is an existential threat to our measurement plan.** Personas were detectable in questionnaires but NOT in behavior (mostly n.s.). If we measure the steerability matrix by asking a judge to rate traits from a rubric, we are in the self-report condition and will measure a matrix that **does not exist in actual dialogue behavior**. This is the same trap as `steer-personality-shaping-levels.md`'s ρ≥0.90 (survey) vs 0.47–0.77 (text) gap — now with a *stronger* result: not attenuated, but absent. **We must measure the matrix on behavioral outputs, and we should expect much of the effect to evaporate.**

6. **Honest caveat.** β ranges are reported as intervals across three prompting strategies, not point estimates with SEs per cell — so the "off-diagonal exceeds diagonal" claim rests on non-overlapping ranges, which is weaker than a formal contrast test. The paper asserts the comparison in prose; it does not test it. We should report it as the authors' claim, not as an established inequality.

7. **Related:** `steer-personality-shaping-independence.md` (Google's independence analysis — the opposite conclusion), `steer-big5chat-trait-correlation.md` (matrix-level distance, prompting is worst), `steer-structural-amplification.md` (why the off-diagonal is large by construction), `bigtech-persona-vectors.md` (entanglement in activation space).
