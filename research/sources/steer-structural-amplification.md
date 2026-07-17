---
title: "From Five Dimensions to Many: Large Language Models as Precise and Interpretable Psychological Profilers"
url: https://arxiv.org/abs/2511.03235
authors: Liu et al.
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# Structural amplification — LLM trait space is MORE correlated than human trait space, and the slope is measured

**This is the answer to "is the induced-trait space low-rank?" The answer is: it is not literally rank-1, but LLMs systematically reproduce the human trait-correlation network with the correlations INFLATED by a measured factor. Slope k = 1.42 for Gemini 2.5 where human data is 1.0 by definition. Every model tested had k > 1.0. This means the off-diagonal of any trait matrix is LARGE BY DEFAULT — not as an artifact of a bad prompt, but as a general property of modern LLMs.**

Verification: HTML fetched from `arxiv.org/html/2511.03235`, stripped to text, all quotes below string-matched against the raw extraction.

## Abstract (verbatim opening)

> "Psychological constructs within individuals are widely believed to be interconnected. We investigated whether and how Large Language Models (LLMs) can model the correlational structure of human psychological traits from minimal quantitative inputs… LLMs demonstrated remarkable accuracy in capturing human psychological structure, with the **inter-scale correlation patterns from LLM-generated responses strongly aligning with those from human data (R² > 0.88)**."

## The method

> "For each of the **816 individuals** in our dataset, we tasked the LLM with a role-playing prediction… the individual's **20 item-level scores from the Big Five inventory**… predict that same person's responses on **all items across the nine other psychological scales**."

Two phases: (1) per-individual prediction from 20 Big Five items; (2) compute Pearson correlation matrices for all psychological scale pairs, comparing LLM-generated vs human ground-truth correlations. The regression of *LLM correlations* on *human correlations* has slope **k**; k = 1.0 would mean perfect structural fidelity.

## THE HEADLINE NUMBER (verbatim)

> "Gemini 2.5 demonstrates an exceptionally strong linear relationship (**R² = 0.92, p < .001**) with a **regression slope (k) of 1.42, significantly greater than 1.0**. This indicates that **LLMs systematically overestimate the strength of correlations between psychological traits—a phenomenon we term structural amplification.**"

> "Bottom-left panel: **All tested LLMs exhibit an amplification coefficient k > 1.0**, consis[tent]…"

> "model-generated correlations… **consistently match the sign of human data but are more saturated (further from zero) than their human counterparts**"

Models tested: **Gemini 2.5, DeepSeek V3.1, Claude 3.7 Sonnet, GPT-5, GLM-4.5, Qwen3-235B, Kimi K2.** All k > 1.0.

The authors distinguish this from the familiar "bias amplification" (verbatim):

> "This should be distinguished from 'bias amplification'… which typically describes a **first-order effect** where models exaggerate specific, pre-existing societal biases from training data (e.g., gender stereotypes). In contrast, the structural amplification we identify is a **se[cond-order effect]**" — i.e. it concerns the **entire relational network of traits**, not one association.

## The causal evidence — a dose-response on NOISE

This is the part that makes the finding hard to dismiss as an artifact. They manipulate noise in both directions:

**Human side** — using less-noisy human data (filtered by response times):

> "This less-noisy human data produced an inherently **stronger correlation structure** that was significantly **closer to the LLM's output (k = 1.08** when compared to the full sample)."

**Model side** — injecting noise into model predictions:

> "By systematically **injecting increasing levels of Gaussian noise** into a baseline model's predictions, we observed a clear **dose-response relationship**: as noise increased, the structural amplification effect was **progressively attenuated (k decreased from 1.55 to 1.12)**."

> "This convergence of evidence—where **removing noise from human data and adding it to model predictions produce opposite, predictable effects**—provides robust empirical support for interpreting structural amplification as a process of **idealized abstraction**"

**Interpretation the authors defend: the LLM is not wrong about the structure — it is modeling the *idealized, measurement-error-free* version of it.** Human trait correlations are attenuated by measurement noise; the LLM reproduces the disattenuated (true-score) structure. k = 1.08 against clean human data is close to 1.0.

Other reported fits: inter-scale correlations R² = 0.92; target scales alone R² = 0.91; SummaryOnly condition R² = 0.91. And notably:

> "**The greater a model amplifies the underlying structure, the better it predicts human traits**" (R² = 0.95 across models)

## Relevance to companion-eval-platform

1. **This is the strongest available answer to "is the trait space low-rank?" — and the honest answer is NO, but the off-diagonal is inflated by a measured factor.** The design's hoped-for finding ("steerability matrix is near-rank-1") is **not** supported: LLMs reproduce the *full* human correlation network with high fidelity (R² > 0.88), including its sign structure. They do not collapse it to one evaluative factor. What they do is **saturate** it: k ≈ 1.4. So the correct claim is "**off-diagonal ≈ 1.4× the human off-diagonal**," not "the matrix is rank-1." We should not overclaim a collapse that the best-measured evidence contradicts.

2. **But 1.4× is still decisive for the platform's purpose.** If a character author assumes traits are independent dials, they are wrong by roughly the human intercorrelation *times 1.4*. The Big Five are already meaningfully intercorrelated in humans (see `psych-metatraits-trait-intercorrelation.md`); amplifying that by 40% means "shy" and "agreeable" and "unconfident" are substantially one dial. **This gives us a quantitative expectation for our own off-diagonal — a prediction to test, not just a hope.**

3. **The noise dose-response is the mechanism we should adopt as the null hypothesis, and it is inconvenient for us.** If amplification is "idealized abstraction" — the LLM rendering the disattenuated true-score structure — then a large off-diagonal in *our* matrix is **not a defect of the model and not a controllability failure.** It is the model correctly representing that shy people *are* somewhat less cruel. **We must not report crosstalk as a bug without first checking it against the human correlation.** The right statistic is the *residual* off-diagonal after regressing out the human trait correlation, not the raw off-diagonal. **This should change our metric definition.** A platform that flags "shy→agreeable spillover" as an entanglement failure would be flagging the model for being psychologically realistic.

4. **k > 1.0 across all seven frontier models is a strong generalization.** This is not a Llama-8B curiosity. Claude, GPT-5, Gemini, DeepSeek, Qwen, GLM, Kimi all amplify. Whatever we measure on our serving model, we should expect the same sign.

5. **"The greater a model amplifies, the better it predicts human traits" (R² = 0.95) is a genuine tension for the product.** Amplification *helps* accuracy. If we build a platform that penalizes trait entanglement, we may be penalizing exactly the property that makes a companion feel like a coherent person rather than a bag of independent sliders. **The product question "do we want a low off-diagonal?" is not obviously yes**, and this paper is the reason. That belongs in the design doc, not buried.

6. **Honest limitation.** This paper measures the LLM *predicting other people's* trait profiles from Big Five inputs — a role-playing *inference* task. It is **not** trait *induction* on the assistant persona. The correlation structure it recovers is the model's *model of human personality*, which is related to, but not the same as, the structure of *its own* induced persona. **Do not cite this as direct evidence about induced-trait crosstalk** — cite it as evidence that the model's internal representation of trait space is a saturated copy of the human one, which is a *mechanism* for why induced traits would entangle. The direct induced-trait evidence is `steer-personality-illusion-crosstalk.md` and `steer-big5chat-trait-correlation.md`.

7. **Related:** `steer-big5chat-trait-correlation.md` (prompting produces a trait correlation matrix *further* from human than SFT: Frobenius 2.10 vs 1.55 — the induction-side counterpart to this finding), `psych-metatraits-trait-intercorrelation.md` (the human baseline being amplified), `steer-personality-illusion-crosstalk.md` (per-cell induced crosstalk).
