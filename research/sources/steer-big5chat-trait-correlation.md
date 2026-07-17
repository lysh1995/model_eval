---
title: "BIG5-CHAT: Shaping LLM Personalities Through Training on Human-Grounded Data"
url: https://arxiv.org/abs/2410.16491
authors: Wenkai Li, Jiarui Liu, Andy Liu, Xuhui Zhou, Mona Diab, Maarten Sap (CMU LTI)
year: 2024 (ACL 2025)
type: paper
accessed: 2026-07-16
topic: steerability
---

# BIG5-CHAT — the trait × trait correlation matrix, reduced to one number, and PROMPTING IS THE WORST METHOD

**This paper computes the full induced trait×trait correlation matrix for three induction methods, compares each against a 619K-person human matrix, and reports the matrix distance. Prompting scores 2.10; SFT scores 1.55; human is 0. That is a quantified statement that PROMPT-INDUCED personality has a MORE distorted correlation structure than trained personality. It is the aggregate version of the steerability matrix's off-diagonal.**

Verification: HTML fetched from `arxiv.org/html/2410.16491v1`, stripped to text, all quotes below string-matched against the raw extraction. The Frobenius passage was located by direct grep.

## Abstract (verbatim)

> "In this work, we tackle the challenge of embedding realistic human personality traits into LLMs. **Previous approaches have primarily focused on prompt-based methods that describe the behavior associated with the desired personality traits, suffering from realism and validity issues.**"

> "…we explore Supervised Fine-Tuning and Direct Preference Optimization as training-based methods to align LLMs more naturally with human personality patterns. **Our methods outperform prompting on personality assessments such as BFI and IPIP-NEO, with trait correlations more closely matching human data.** Furthermore, our experiments reveal that models trained to exhibit **higher conscientiousness, higher agreeableness, lower extraversion, and lower neuroticism display better performance on reasoning tasks**, aligning with psychological findings on how these traits impact human cognitive performance."

## THE MATRIX COMPARISON — method (verbatim)

> "…we first calculated the **intra-trait correlations from real human distributions** using the IPIP-NEO questionnaire, based on the **PAPI-120-600K dataset** from Zhu et al. (2024), which includes **619K human responses** to the IPIP-NEO. Next, we computed the intra-trait correlations for the **prompting, SFT, and DPO** methods using the results from Table 2. These correlations are visualized in **Figure 2**, showing that **most traits are positively correlated, with the exception of neuroticism**. To quantify the similarity between the method-generated and human correlation matrices, we calculated the matrix distance using the Frob[enius norm]…"

## THE NUMBER (verbatim)

> "Frobenius norm, where **0 represents perfect similarity and 10 indicates maximum dissimilarity**. The matrix distances were **2.10 for prompting, 1.55 for SFT, and 2.06 for DPO**. These results suggest that the trained models, particularly SFT, **more accurately capture the trait correlations seen in natural human data compared to the prompting-based methods**."

| Induction method | Frobenius distance from the 619K-human trait correlation matrix |
|---|---|
| Human ground truth | **0** (by definition) |
| **SFT** | **1.55** |
| **DPO** | **2.06** |
| **Prompting** | **2.10** (worst) |

**This is the headline for us. The induction method our platform actually uses — prompting — produces the trait correlation structure FURTHEST from human.** The off-diagonal of a prompt-induced trait matrix is not merely non-zero; it is *more wrong* than the off-diagonal you get from fine-tuning.

Note the honest reading: 2.10 vs 2.06 (DPO) is a negligible gap; the real contrast is **SFT (1.55) vs everything else**. The claim "prompting is worst" is true but the margin over DPO is within noise as reported (no CI is given).

## The limitation that is our opening (verbatim)

> "**Our current approach isolates individual traits for steering, but personality traits are rarely exhibited in isolation**"

> "we **deliberately focus on single traits in this study** to enhance clarity, interpretability, and replicability."

**They state plainly that single-trait steering is a simplification and that the joint/interaction case is out of scope.** Combined with Anthropic's open question in `steer-persona-vectors-crosstalk.md` ("Do correlations between persona vectors predict co-expression of the corresponding traits?"), that is **two independent research groups explicitly flagging the joint-trait case as unaddressed.** That is a far stronger novelty argument than claiming crosstalk is unmeasured.

## What it does NOT do

It reports a **single scalar distance** for the whole matrix. It never reports "**inducing trait X moved trait Y by Z**" — there is no per-cell spillover coefficient, no signed off-diagonal, no asymmetry analysis. Figure 2 visualizes the matrices but the text gives no per-cell values.

So: the off-diagonal is **measured in aggregate** and **collapsed to one number**. The per-cell structure — which pairs entangle, in which direction, how much — is discarded.

## Evaluation apparatus

- **BFI** (44 items, 1–5) and **IPIP-NEO** (120 items).
- Personality classifier: **RoBERTa-Large + 5 regression heads** (MSE) trained on **PsychGenerator**.
- Expert generator achieved **80.4** average classifier accuracy vs **59.2** baseline.
- Training-vs-prompting difference (verbatim): training methods produced "**lower scores for low levels of personality traits** when compared to prompting-based methods" — i.e. prompting struggles to push a trait *down*, a floor-effect asymmetry.

## Relevance to companion-eval-platform

1. **The single most useful number in this file: prompting = 2.10, SFT = 1.55.** If we want to argue the off-diagonal matters, this is the cleanest published evidence that **prompt-induced trait structure is measurably distorted relative to humans**, on a 619K-person baseline, using a standard matrix norm. It is directly about the induction method our product uses.

2. **They computed our matrix and threw away the interesting part.** They built the trait×trait correlation matrix for prompt-induced personality — then reduced it to ‖·‖_F. **Every per-cell number the steerability matrix wants already existed in their pipeline and was summarized away.** This is the same shape of gap as PersonaLLM's unused 2⁵ factorial (see `steer-trait-intercorrelation-benchmarks.md`). **Our defensible novelty is not "nobody measured it" — it is "everybody who measured it reported a scalar or a heatmap, and nobody reported the cells."** That is a real, checkable, and much more modest claim.

3. **Frobenius distance is the right aggregate metric and we should adopt it as a summary statistic** — but as a *complement* to per-cell reporting, not a replacement. It gives us a one-number comparison against a human baseline that reviewers already accept, and it lets us compare induction methods (prompt vs. fine-tune vs. steer) on one axis.

4. **The human baseline is the move we should copy.** They do not ask "is the off-diagonal zero?" (a naive and wrong question — human traits are correlated). They ask "**is the off-diagonal the same as humans'?**" That is the correct null, and it aligns with the warning in `steer-structural-amplification.md`: raw crosstalk is not a defect; *deviation from the human correlation* is. **We should define our metric as distance-from-human-structure, not distance-from-identity.** PAPI-120-600K (619K responses) is a usable public baseline.

5. **The "lower scores for low levels" asymmetry is a floor effect we will hit.** Prompting cannot push traits down as well as it pushes them up. Our intensity ladder ("shy" → "extremely shy") mostly tests the *up* direction; the down direction ("not at all shy") may be nearly inert. **The matrix may be asymmetric in dose direction as well as in trait pair** — cf. the A→B ≠ B→A asymmetry in `steer-personality-illusion-crosstalk.md`.

6. **Honest limitation of this source.** The correlations are computed **across trait conditions from Table 2 aggregates**, not from a within-subject perturbation design — so this is a correlation *between induced trait scores across conditions*, which is not identical to "perturbing X causes Y to move." It is suggestive of entanglement, not a causal crosstalk estimate. The causal per-cell evidence remains `steer-personality-illusion-crosstalk.md`.

7. **Related:** `steer-structural-amplification.md` (k = 1.42 — why prompt-induced correlations inflate), `steer-personality-illusion-crosstalk.md` (per-cell causal off-diagonal), `steer-personality-shaping-independence.md` (Google's contrary "unprompted traits remain stable" claim), `steer-trait-intercorrelation-benchmarks.md` (who else has the data and didn't use it).
