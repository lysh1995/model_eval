---
title: "A psychometric framework for evaluating and shaping personality traits in large language models (Nature Machine Intelligence version of arXiv 2307.00184)"
url: https://www.nature.com/articles/s42256-025-01115-6
authors: Gregory Serapio-García, Mustafa Safdari, Clément Crepy, Luning Sun, Stephen Fitz, Peter Romero, Marwa Abdulhai, Aleksandra Faust, Maja Matarić (Google DeepMind / Google Research / Cambridge / UC Berkeley / USC)
year: 2025 (arXiv preprint 2023)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Serapio-García et al. — the INDEPENDENCE claim, and why it is weaker than it looks

**Companion to `steer-personality-shaping-levels.md`, which covers the 9-level adverbial dosing ladder. This file is specifically about the INDEPENDENCE / DISCRIMINANT VALIDITY analysis — i.e. their answer to "does shaping trait X move traits Y, Z?" — read from the peer-reviewed Nature Machine Intelligence version (12 models incl. GPT-4o), which supersedes the 2023 arXiv numbers in the companion file.**

Verification: full text read from the open-access PMC mirror (`pmc.ncbi.nlm.nih.gov/articles/PMC12719228/`) and cross-checked against `arxiv.org/html/2307.00184v4`. Quotes below are as returned by extraction of those two sources; where the two versions differ I flag it.

## THE CRITICAL FINDING — they claim independence, and the evidence is a MEDIAN and a RIDGE PLOT

This is their answer to the off-diagonal question, verbatim:

> "Notably, **levels of unprompted traits remained relatively stable in response to shaping.** For instance, **the medians of Flan-PaLMChilla 62B's openness scores remained near 3.00 when all other Big Five domains were shaped.**"

> "**Conscientiousness and neuroticism scores fluctuated the most in response to prompts that did not target those domains**, but **these fluctuations did not reach the strength and direction of the score changes observed in the ridge plots of targeted traits.**"

**Parse this carefully — it is the crux of whether the design's novelty claim survives.**

They DID look at the off-diagonal. They report it as **small but non-zero**: untargeted conscientiousness and neuroticism *do* move. So:
- The claim "**nobody has looked at whether shaping X moves Y**" is **FALSE**. They looked.
- The claim "**the off-diagonal has been quantified per cell**" is **also FALSE**. It has not.

What they actually report is: (a) one median for one trait on one model ("openness stayed near 3.00"), and (b) a **qualitative visual comparison** of ridge plots ("did not reach the strength and direction"). **There is no cross-trait correlation matrix, no per-cell spillover coefficient, no significance test on the off-diagonal, and no effect size for the untargeted movement.** The independence conclusion rests on eyeballing ridge plots plus a single median.

Confirmed by direct extraction: "**The paper does not provide an explicit cross-trait correlation matrix.** Figure 4's ridge plots visually show independence but no numerical intercorrelation table appears in main text or extended data tables."

**This is the single most important methodological point in this file. The most-cited prior art for trait shaping asserts independence WITHOUT MEASURING IT.** That is our opening, and it is a legitimate one.

## How they benchmarked "independent shaping" (verbatim)

Two criteria, neither of which is a crosstalk metric:

> "quantifying how strongly shifts in IPIP-NEO score distributions were related to shifts in **targeted trait levels** embedded in our prompt sets (i.e., through **Spearman's rank correlation coefficient ρ**)"

Plus a distributional-distance check: whether extreme prompt sets (lowest vs highest levels) produced sufficiently separated score distributions.

**Both criteria are about the DIAGONAL.** "Independent shaping" in their usage means "**we shaped each trait one at a time**" (a description of the experimental *design*), **not** "**we verified the other traits did not move**" (a *result*). This is an easy and consequential misreading — the word "independent" refers to the manipulation, not to the outcome.

## Spearman ρ — the diagonal (verbatim, Nature MI version)

> "For **11 out of 12 models tested**, ordinal targeted levels of personality very strongly correlated with observed IPIP-NEO scores. Namely, **the average Spearman correlation (ρ) for these models was ≥ 0.80**." (Extended Data Table 6)

> "On average per model, prompted trait levels correlated strongly to very strongly with personality observed in **LLM-generated social media updates (average ρ ranged from 0.68 to 0.82)**." (Extended Data Table 5)

Note the NMI version's numbers are **more conservative** than the 2023 arXiv figures in the companion file (which cite ρ ≥ 0.90 survey / 0.47–0.77 text). The peer-reviewed generated-text range **0.68–0.82** is a per-model average, whereas the companion file's 0.47–0.77 is per-domain. **Both are true of different aggregations — do not mix them.**

## Control range Δ — capacity dependence (verbatim)

> **Smallest models** (Flan-PaLM 8B, Llama 2-Chat 7B, Mistral 7B Instruct): "struggled to reach **Δs ≥ 2.00**"
> **Larger models** (>62B, GPT-4o): "achieved average **Δs ≥ 3.00**"
> **Best**: "**Flan-PaLM 540B achieving the largest Δ of 3.67**"

## Concurrent (multi-trait) shaping — the closest thing to a crosstalk measurement

> "**Flan-PaLM 540B**… and **GPT-4o** showed the best overall control concurrently shaping multiple Big Five traits. For these models, a given Big Five trait score **shifted by 2.525 points on average**" (Extended Data Table 7)

> Flan-PaLM 8B's agreeableness under concurrent shaping shifted only **0.64** points (**2.88 → 3.52**) versus **1.75** points (**2.37 → 4.12**) in single-trait mode.

**Δ = 0.64 concurrent vs Δ = 1.75 single-trait on the same model and trait — a ~63% loss of control range purely from adding competing trait objectives.** That IS an entanglement penalty, quantified. But note what it is *not*: it measures **how much control you lose when shaping five traits at once**, not **how much trait Y moves when you shape only trait X**. It is an interference measure, not an off-diagonal.

And it is strongly capacity-dependent: 540B barely degrades (2.525 avg shift), 8B degrades severely.

## Convergent / discriminant validity (verbatim)

> Flan-PaLM 540B and GPT-4o: "average **r_conv = 0.90**"; Llama 2-Chat 70B: "**r_conv = 0.80**"; base (non-instruction-tuned) models: "**all non-significant and close to zero**"

> "**Discriminant validity is evidenced when the average difference (Δ) between a model's convergent (r_conv) and respective discriminant (r_discr) correlations between personality tests is at least moderate (avg. Δ ≥ 0.40).**"

**Important: their "discriminant validity" is NOT a trait-crosstalk metric.** It asks whether *two different instruments measuring the same trait* agree more than *two instruments measuring different traits* — a psychometric property of the **measurement**, not of the **manipulation**. A design that cites this as prior art for the steerability matrix's off-diagonal would be misreading it. (It is, however, exactly the right check on whether our *trait scorer* is measuring what it claims — see below.)

## Relevance to companion-eval-platform

1. **This is the most-cited prior art, and it ASSERTS independence rather than measuring it. That is the strongest honest version of our novelty claim.** They report the off-diagonal qualitatively ("fluctuated the most", "did not reach the strength and direction") and quantitatively with exactly **one** number (openness median ≈ 3.00, one model). **We can say, accurately and checkably: "the field's canonical trait-shaping result claims untargeted traits are stable, on the basis of ridge-plot inspection and a single median; the per-cell off-diagonal has never been estimated for prompt-based shaping."** That survives a reviewer who has read the paper. "Nobody has measured crosstalk" does not.

2. **Their own data contradicts clean independence, and they say so.** "Conscientiousness and neuroticism **fluctuated the most** in response to prompts that did not target those domains." That is an admission of crosstalk with a named direction — C and N are the leaky traits — and no magnitude. **We have a published prediction for which rows of our matrix should be hot, from the field's canonical paper.** That is a gift: a pre-registered expectation, not a fishing expedition.

3. **Beware the word "independent" — it describes their design, not their finding.** "Independent shaping" = shaping one trait at a time. Anyone (including us) who cites this as evidence that trait shaping *is* independent is misreading it. Worth stating explicitly in the related-work section, because the misreading is common and a reviewer may hold it.

4. **The concurrent-shaping penalty (Δ 0.64 vs 1.75, −63%) is real prior art for trait interference and we must cite it.** It establishes that trait objectives compete. But it answers a different question than the steerability matrix: it is "control degrades when you shape many," not "shaping one moves another." **Both are worth having; do not conflate them.**

5. **Capacity dependence means our matrix is a property of the model, not the character.** 8B: Δ < 2.00; 540B/GPT-4o: Δ ≥ 3.00. Any steerability matrix we publish is per-model. Comparing matrices across models may mostly re-measure model capacity, not trait structure. **Normalize by the diagonal** (i.e. report off-diagonal / diagonal per model) or the comparison is meaningless.

6. **Steal their discriminant-validity criterion for our JUDGE, not for our matrix.** "avg Δ ≥ 0.40 between convergent and discriminant correlations" is exactly the check we need on our trait scorer: does our "shyness" rubric correlate more with other shyness measures than with our "cruelty" rubric? **If our judge fails this, our entire off-diagonal is judge crosstalk, not model crosstalk.** This is the most important prerequisite in the whole project: **a rubric-based judge that cannot discriminate traits will manufacture a large off-diagonal out of nothing.** Given the α = 0.25–0.34 reliability we've seen on our own aesthetic judgments, this is a live risk, not a formality.

7. **Honest limitation.** IPIP-NEO administered to an LLM is a contested instrument, and the survey-vs-text gap is large (ρ ≥ 0.80 survey vs 0.68–0.82 text per-model average, and 0.47–0.77 per-domain in the arXiv version). `steer-personality-illusion-crosstalk.md` goes further: persona injection was detectable in **self-report but NOT in behavior**. Their independence claim is established on **questionnaire** scores; whether untargeted traits stay stable **in dialogue behavior** is untested by this paper.

8. **Related:** `steer-personality-shaping-levels.md` (same paper, the dosing-ladder story and 2023 arXiv numbers — do not duplicate), `steer-personality-illusion-crosstalk.md` (the contrary result: per-cell off-diagonal, sometimes off-diagonal-dominant), `steer-big5chat-trait-correlation.md` (prompting's matrix is furthest from human), `steer-persona-vectors-crosstalk.md` (entanglement in activation space).
