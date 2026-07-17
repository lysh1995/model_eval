---
title: "Persona Vectors: Monitoring and Controlling Character Traits in Language Models"
url: https://arxiv.org/abs/2507.21509
authors: Runjin Chen (Anthropic Fellows Program / UT Austin), Andy Arditi (Anthropic Fellows Program), Henry Sleight (Constellation), Owain Evans (Truthful AI / UC Berkeley), Jack Lindsey (Anthropic)
org: Anthropic
year: 2025
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Anthropic's Persona Vectors — activation-space dose-response, PLUS a prompt ladder used as an instrument rather than as an object of study

**Verdict up front: this does NOT refute our prompt-space novelty claim, but it comes closer than expected and for a reason we had not anticipated. It contains (a) an 8-rung prompt-intensity ladder, (b) a many-shot dose ladder with a numeric axis, and (c) a 7×7 trait entanglement heatmap. None of these are prompt-space dose-response CURVES. The distinction is real but narrower than we assumed — and it is NOT the distinction we thought we would be making.**

Verification: PDF (arxiv.org/pdf/2507.21509, 23 pages, 203,839 chars) downloaded and extracted with pypdf; every quote below string-matched against the raw extraction. Blog: https://www.anthropic.com/research/persona-vectors

## Abstract (verbatim)

> "Large language models interact with users through a simulated 'Assistant' persona. While the Assistant is typically trained to be helpful, harmless, and honest, it sometimes deviates from these ideals. In this paper, we identify **directions in the model's activation space—persona vectors—underlying several traits, such as evil, sycophancy, and propensity to hallucinate**. We confirm that these vectors can be used to **monitor** fluctuations in the Assistant's personality at deployment time. We then apply persona vectors to predict and control personality shifts that occur during training... Our method for extracting persona vectors is automated and can be applied to any personality trait of interest, given only a natural-language description."

## The activation-space dose-response (verbatim)

> "Given a persona vector v_ℓ extracted from layer ℓ, we can steer the model's activations toward this direction at each decoding step: **h_ℓ ← h_ℓ + α·v_ℓ** ... where **α is a scalar steering coefficient**, and h_ℓ is the residual stream activation at layer ℓ. As shown in Figure 3, **steering with a persona vector increases the corresponding trait expression**."

> "Figure 3: **Steering with persona vectors.** Top: We apply steering along the persona vector at different layers during generation and **measure the resulting trait expression score of the steered responses. Each line represents a different steering coefficient.**"

Steering coefficients visible in the Figure 3 axis labels: **2.50, 2.00, 1.50, 1.00, 0.50**, swept across layers 5–25. Trait expression scored **0–100** by an LLM judge. Traits: **evil, sycophancy, hallucination** (plus optimism, humor, impoliteness, apathy in Appendix G).

**This IS a dose-response curve: trait expression vs steering coefficient. It is in activation space. `dose` appears 0 times and `intensity` 0 times in the paper — the concept is present, the vocabulary is not.**

## THE PART WE DID NOT EXPECT — a prompt-intensity ladder (verbatim)

> "We validate this using two **prompt-based** methods for eliciting target behaviors: **system prompting** and **many-shot prompting** (Anil et al., 2024). To construct sequences of system prompts, we use Claude 4.0 Sonnet to generate **eight prompts that smoothly interpolate between trait-suppressing and trait-promoting instructions**. For many-shot prompting, we use a set of **0, 5, 10, 15, or 20 examples** that demonstrate the target trait. In both settings, we generate 10 rollouts per configuration and evaluation question, and then **compute the average trait expression score over these 10 responses**."

> "Figure 4: **Monitoring prompt-induced behavioral shifts.** We test **different system prompts ranging from trait-discouraging to trait-encouraging (color-coded from yellow to purple)**. Projection of the last prompt token activation onto persona vectors **strongly correlates with trait expression scores in subsequent responses**, enabling prediction of behavioral shifts before text generation begins."

**Read this carefully, because it is the crux of our whole novelty claim.**

Anthropic **does** construct a monotone prompt-intensity ladder — eight system prompts interpolating from trait-suppressing to trait-promoting — and **does** measure trait expression (0–100) at each rung. The many-shot ladder (0/5/10/15/20 examples) even has a *numeric* dose axis. The raw ingredients of a prompt-space dose-response curve are all present in this paper.

**But the plotted relationship is `projection onto persona vector` (x-axis) vs `trait expression score` (y-axis). The prompt rung is neither axis — it is only a color.**

That is the precise distinction, and it is a distinction of *research question*, not of missing data:
- **Anthropic's question:** "does an internal activation reading predict the behavior that follows?" The prompt ladder is an **instrument** — a convenient way to manufacture spread in trait expression so the projection↔behavior correlation can be tested across a range. Any other source of variation would have served.
- **Our question:** "does the prompt knob move the behavior, and by how much per unit?" The prompt ladder is the **independent variable**.

Because the ladder is an instrument, the paper never reports the one number we care about: **trait expression per unit of prompt emphasis.** The eight rungs are unordered colors in a scatter, not an x-axis. No slope, no fit, no elasticity. The data almost certainly exists in their artifacts; the analysis was never the point.

**This is a genuinely narrow gap and we should be honest that it is narrow.** It is not "Anthropic works in activation space and we work in prompt space" — that framing is wrong and a reviewer will catch it, because Anthropic *did* run the prompt ladder. It is: "Anthropic used a prompt ladder as a nuisance instrument to validate a monitor; nobody turned the ladder into the x-axis and fitted it."

## Brittleness in activation space (verbatim)

> "Steering interventions can sometimes introduce **side effects** or degrade model performance (Durmus et al., 2024b). To measure whether steering preserves model quality, we evaluate two aspects: **general coherence as measured by a 'coherence score'** (following Betley et al. (2025), where each response is **rated 0–100 by GPT-4.1-mini** based on its coherence), and general capability as measured by **MMLU accuracy**. For all results presented, **average response coherence is above 75**."

> "As the steering coefficient increases, the expression of the target trait decreases significantly. However, similar to findings in Durmus et al. (2024b), we observe that applying inference-time steering can introduce side effects: when evaluating on MMLU (gray line), **large steering coefficients tend to degrade** [performance]"

> "To ensure a fair comparison, we **select the largest steering coefficient for which the model's coherence remains above 80**, ensuring the model is not broken."

**This is our "Brittle" mode, in activation space: crank the dose and the model degrades.** The coherence-above-80 dose ceiling is a methodological device we should copy directly — an elasticity measured past the point where the model stops being coherent is meaningless.

## THE TRAIT ENTANGLEMENT HEATMAP — we must not claim nobody measures crosstalk (verbatim)

> "However, it is worth noting that **persona shifts are rather correlated between seemingly different traits**. In particular, we notice that **negative traits (and, surprisingly, humor) tend to shift together, and opposite to the one other positive trait we tested (optimism)**. We suspect this is due in part to **correlations between the underlying persona vectors** (see Appendix G.2), and in part due to correlations in the data."

Appendix G.2 method (verbatim):

> "**G.2 CROSS-TRAIT PREDICTIVE POWER AND VECTOR SIMILARITY ANALYSIS.** To further investigate the generalizability and relationships among trait directions, we evaluate how well each trait vector predicts behavioral changes across different traits. Concretely, for a given trait A, we first measure the finetuning-induced activation shift by projecting the model's last-prompt-token activation on evaluation questions targeting trait A onto the trait-A direction... For another trait B, we independently measure the observed change in behavior by evaluating the model on trait-B specific questions and computing its trait expression score before and after finetuning. We then compute the **Pearson correlation** between these two quantities... This correlation **quantifies the extent to which movement along one trait direction is predictive of behavioral expression in another trait**. Aggregating these results across all trait pairs yields a **'persona correlation' heatmap** shown in Figure 20 (left), which visualizes the **degree of alignment or entanglement among different** [traits]"

**They use the word "entanglement". They build a 7×7 trait matrix. It has off-diagonal entries.**

Traits on both axes: **Evil, Sycophantic, Hallucinating, Impolite, Apathetic, Humorous, Optimistic.**

Persona Vector **Cosine Similarity** (Llama, Layer 16) — verbatim off-diagonals worth noting: Evil↔Sycophantic **0.412**, Evil↔Impolite **0.440**, Evil↔Optimistic **−0.469**, **Impolite↔Apathetic 0.734** (the strongest positive off-diagonal), Impolite↔Optimistic **−0.484**, Hallucinating↔Impolite **−0.032** (essentially orthogonal).

Finetuning-Shift vs Persona-Behavior correlations (Llama) are uniformly high (e.g. Evil-shift→Evil-score **0.930**, Evil-shift→Impolite-score **0.974**, Evil-shift→Optimistic-score **−0.907**), which is the quantitative form of "negative traits tend to shift together."

**So: a trait × trait entanglement matrix EXISTS, at Anthropic, published.** Our claim "nobody measures trait-trait crosstalk" is false as stated and must be narrowed.

What the matrix is *not*: its cells are **(finetuning-induced activation shift along A) × (behavioral change in B)** and **cosine similarity between persona vectors**. Both axes live in activation/finetuning space. There is no cell anywhere in this paper of the form **(prompt emphasis on trait A) × (expression of trait B)**. Zero occurrences of `off-diagonal` in the text.

## Other findings worth carrying

> "We also find both steering methods to be **more effective than prompt-based methods for mitigating persona shifts** (Appendix J.2 and J.7.2)."

> "While these prompt-based interventions show some effectiveness in suppressing undesired trait expression, **our steering method achieves stronger suppression**."

**A third independent finding that prompt-space control is weaker than activation-space control** (cf. PsySET's "limited in intensity control", Course Correction's "prompt engineering ineffective"). Three papers, three methods, same direction. This is now a well-supported prior, not a hypothesis.

Baseline trait expression scores prior to finetuning (verbatim): **0 (evil), 4.4 (sycophancy), 20.1 (hallucination)** — note the floor effects, which matter for any slope estimate.

Extraction method (verbatim): "For each question in the extraction set, we generate responses using both **positive and negative system prompts** (10 rollouts each)... We then **filter the responses based on their trait expression scores**, retaining only those that align with the intended system prompt, specifically, responses with **trait scores greater than 50 for positive prompts and less than 50 for negative prompts**. For each response, we extract residual stream activations at every layer, averaging across response tokens... We then compute the persona vector as the difference in mean activations"

Models: **Qwen2.5-7B-Instruct** and **Llama-3.1-8B-Instruct**.

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**NO — but for a subtler reason than "it's activation-space work." It ran the prompt ladder and declined to fit it.**

| Component | Present? | Space |
|---|---|---|
| Dose-response curve (trait expr. vs coefficient) | **YES** | activation |
| Monotone prompt-intensity ladder (8 rungs) | **YES** | prompt |
| Numeric prompt dose axis (many-shot 0/5/10/15/20) | **YES** | prompt |
| Trait expression measured at each prompt rung | **YES** | prompt |
| **Trait expr. plotted/fitted AS A FUNCTION OF prompt rung** | **NO** | — |
| Elasticity / slope in prompt units | **NO** | — |
| Brittle mode (dose → incoherence) | **YES** | activation |
| Trait × trait entanglement matrix | **YES** | activation / finetuning |
| **Trait × trait crosstalk from PROMPT perturbation** | **NO** | — |

Keyword census (verified counts): `steering coefficient` **34**, `trait expression` **96**, `system prompt` **38**, `dose` **0**, `intensity` **0**, `monotonic` **0**, `off-diagonal` **0**.

## Relevance to companion-eval-platform

1. **Do not say "Anthropic works in activation space, we work in prompt space."** It is the obvious framing and it is wrong. Anthropic built an 8-rung prompt ladder and a 0/5/10/15/20 many-shot dose. The correct, defensible sentence is: *"Persona vectors uses a prompt-intensity ladder as an instrument to validate an activation-space monitor; the prompt rung never becomes an x-axis, so no prompt-space gain is ever estimated."* That is true, checkable, and survives contact with a reviewer who has read the paper.
2. **Narrow the crosstalk claim too.** Figure 20 is a 7×7 entanglement heatmap using the word "entanglement". Our claim must become: *"trait × trait entanglement is measured for finetuning-induced activation shifts; the prompt-space crosstalk matrix — does emphasizing 'shy' in the prompt move 'cruel' in the output — is not."* Still novel. Much less grand.
3. **Impolite↔Apathetic = 0.734 is a warning shot for companion character design.** If two traits a scene author would treat as independent share a 0.73-cosine direction, then "authoring a character" is not selecting independent dials. Our trait × trait matrix has a plausible mechanism (shared directions) and a published precedent for the *shape* of the result. That is a strong argument the experiment is worth running.
4. **Steal the coherence-gated dose ceiling.** "Select the largest steering coefficient for which the model's coherence remains above 80" — our prompt-space analogue: report elasticity only over the dose range where coherence holds, and report the dose at which it breaks as a separate Brittle statistic. Without this, "extremely pathologically shy" produces degenerate output and inflates the apparent slope.
5. **Trait expression score (0–100, LLM judge) is the measurement primitive**, and its reliability is unreported here — same gap as SysBench (`game-sysbench.md`). Given our own α = 0.25–0.34 on aesthetic quality, we cannot assume a trait-expression judge is reliable just because Anthropic used one. **Validating the trait scorer is prerequisite work, not a detail.**
6. **The floor effects matter.** Baseline evil = 0, sycophancy = 4.4. A trait at 0 has no downward range; an elasticity computed across a floor is not a slope. Cf. IBM's capacity normalization and PsySET's openness ceiling — three papers now converge on "baseline position determines measurable steerability."
7. **Related:** `bigtech-psyset.md` (the closest work — prompt lexical intensity ladder, finds prompt response flat), `bigtech-prompt-steerability.md` (IBM — prompt-space curves; disclaims joint steerability), `bigtech-steerability-course-correction.md` (miscalibration + orthogonality), `bigtech-neural-steering-dose.md` (Oxford/AISI — actually fits a prompt-space slope: the real refutation).
