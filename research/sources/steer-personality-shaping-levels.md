---
title: "Personality Traits in Large Language Models"
url: https://arxiv.org/abs/2307.00184
authors: Gregory Serapio-García, Mustafa Safdari, Clément Crepy, Luning Sun, Sahra Ghaffari, Marwa Abdulhai, Aleksandra Faust, Maja Matarić (Google DeepMind / Google Research / Cambridge / UC Berkeley / USC)
year: 2023 (published as Nature Machine Intelligence, 2025)
type: paper
accessed: 2026-07-16
topic: steerability
---

# Personality Traits in LLMs — graded trait shaping via adverbial qualifiers, ALREADY DONE

**This is the direct prior art for "dose-response elasticity". They perturb a trait adjective with Likert-style linguistic qualifiers across NINE ordered levels, measure the shift in output, and verify monotonicity with a rank correlation. That is the proposed method, published in 2023, in Nature Machine Intelligence.**

## Abstract (verbatim excerpt)

> "The advent of large language models (LLMs) has revolutionized natural language processing, enabling the generation of coherent and contextually relevant human-like text."

The paper presents "a novel and comprehensive psychometrically valid and reliable methodology for administering and validating personality tests on widely-used LLMs, as well as for shaping personality in the generated text of such LLMs."

Headline claim: "personality in LLM outputs can be shaped along desired dimensions to mimic specific human personality profiles."

## The shaping methodology — this IS the "trait word dosing" design

- **Nine intensity levels** per trait.
- Levels are set with **Likert-type linguistic qualifiers**. Verbatim: they used "linguistic qualifiers often used in Likert-type response scales (e.g., 'a bit,' 'very,' 'extremely')" to configure target levels for each adjective.
- **104 trait adjectives**, expanding Goldberg's original 70 bipolar adjectives. Examples from their Table 3: "silent" (low extraversion) / "talkative" (high extraversion).
- Prompt structure: **Persona Instruction + Persona Description + Item Instruction**, combined with trait adjectives at specified intensity levels.
- Example shaped personas given in the paper: **"extremely extraverted"**, **"somewhat introverted"**.

Map this onto the design under test:

| Design under test | Serapio-García et al. (2023) |
|---|---|
| "shy" → "quite shy" → "extremely shy" → "pathologically shy" | trait adjective + {"a bit", "very", "extremely", …} across 9 levels |
| measure behavioral shift in output | IPIP-NEO score distributions + text-based personality classifier |
| fit a curve / check response | Spearman's ρ between targeted level and observed score |
| "elasticity" = Δoutput / Δprompt | ρ ≥ 0.90 (survey) / ρ = 0.47–0.77 (generated text) |

The perturbation ladder, the ordered levels, the adverbial intensifiers, and the monotonicity check are all present. The only thing not present is the **name** "dose-response elasticity" and the explicit **ratio** Δout/Δin.

## Monotonicity verification (verbatim)

> "We benchmarked the success of independent shaping by 1) quantifying how strongly shifts in IPIP-NEO score distributions were related to shifts in targeted trait levels embedded in our prompt sets (i.e., through Spearman's rank correlation coefficient ρ)."

Monotonicity is additionally shown visually via **ridge plots** across the nine levels. The paper reports that Flan-PaLMChilla 62B's personality scores **monotonically increased** alongside prompted levels of a given Big Five trait.

## Correlation numbers (verbatim)

### Single-trait shaping, survey-based (IPIP-NEO)

> "Across all tested models, ordinal targeted levels of personality very strongly correlated with observed IPIP-NEO scores (ρs ≥0.90)"

### Prompted level → personality expressed in GENERATED TEXT (their Table 4)

This is the closer analogue to our use case: does the prompt dose show up in free-form output, not just in a questionnaire?

| Big Five domain | Spearman ρ (prompted level → text) |
|---|---|
| Agreeableness | **0.77** |
| Extraversion | **0.74** |
| Neuroticism | **0.72** |
| Conscientiousness | **0.68** |
| Openness | **0.47** |

> All correlations "statistically significant at p<0.0001; n=450 per targeted domain."

**The Openness collapse to ρ = 0.47 is the single most important number in this file for us.** It says the elasticity of prompt-dose → observed-behavior is *trait-dependent*, and for at least one of five traits the graded control is only weakly ordered. A platform that reports one "elasticity" number per character would average over exactly this variance.

### Convergent validity, survey vs. text

- Average convergent Pearson **r = 0.55** across all five dimensions
- Exceeded the human baseline of **r = 0.38**

## Cross-trait spillover — entanglement is already documented here

> "Conscientiousness and neuroticism scores fluctuated the most in response to prompts that did not target those domains, but the fluctuations did not reach the strength and direction of the score changes observed in the ridge plots of targeted traits."

> "the medians of Flan-PaLMChilla 62B's openness scores remained near 3.00 when all other Big Five domains were shaped"

So: **shaping trait X measurably moves untargeted traits Y and Z** (conscientiousness and neuroticism fluctuate most), but the leak is smaller than the intended effect. This is a partial-isolation result, not a clean-independence result.

## Multi-trait (concurrent) shaping — the capacity ceiling

| Model | Result when shaping all Big Five at once |
|---|---|
| **Flan-PaLM 540B** | "successfully shaped all Big Five personality dimensions concurrently and achieved levels of control similar to what was observed in the single trait shaping experiment", with "median differences by 2.53 on average across all dimensions" |
| **Flan-PaLM 8B** | "score ranges were more restricted, indicating lower levels of control. Flan-PaLM 8B's median scores on IPIP-NEO Agreeableness, for instance, shifted from 2.88 to only 3.52" (Δ = 0.64) vs. single-trait shaping producing differences **"173% larger"** (Δ = 1.75) |

**Δ = 0.64 concurrent vs Δ = 1.75 single-trait on the same model and same trait — a 63% loss of control range from adding competing trait objectives.** That is a quantified entanglement penalty, and it is model-capacity-dependent: the 540B model barely degrades, the 8B model degrades severely.

Note the important caveat for us: only ρ ≥ 0.90 is reported for single-trait shaping. **No Spearman correlations are reported for concurrent shaping** — only distributional distances (Δ medians). So the multi-trait *monotonicity* question is left partly open by this paper, which is a genuine gap.

## Relevance to companion-eval-platform

1. **This refutes the novelty claim as stated.** "Perturb a trait word by controlled amounts, measure behavioral shift, check the response" is Serapio-García et al. (2023), at nine levels, with the same adverbial intensifiers ("a bit"/"very"/"extremely" vs our "quite"/"extremely"/"pathologically"), validated with a rank correlation, published in Nature Machine Intelligence. We cannot claim graded trait dosing as a new method. We should cite this as the method's origin and position our work as an extension.

2. **What is genuinely left open — and it is narrow but real.** They report a *rank correlation* (is it ordered?), not a *slope with units* (how much output shift per unit prompt shift?), and not a *functional form* (linear? saturating? sigmoid?). "Elasticity" as a fitted local slope, and the shape of the curve (especially saturation and reversal at the top end), is not what ρ measures — ρ = 0.95 is compatible with a curve that is completely flat over the top three levels. **If we want a novelty claim, it has to be about curve SHAPE and SATURATION POINT, not about graded control per se.** That is a much narrower claim than "novel metric" and we should say so.

3. **The Openness ρ = 0.47 number should set our expectations, and it is bad news.** In *generated text* (not questionnaires — text, which is what our product produces), the prompt-dose→behavior ordering ranges from 0.47 to 0.77. Our companion traits ("shy", "sarcastic", "protective") are closer to text-expression than to questionnaire scores. A per-trait elasticity that varies this much means a single scalar elasticity per character is close to meaningless; we would need per-trait curves, and some traits may simply not be gradable.

4. **The survey-vs-text gap is the methodological trap we should avoid.** ρ ≥ 0.90 on the questionnaire collapses to ρ = 0.47–0.77 in free text. Any elasticity we measure via a judge scoring a rubric ("how shy is this response, 1–5?") is closer to the *questionnaire* condition and will overstate the control we actually have in production dialogue. We should measure elasticity on real dialogue outputs, not on self-report probes, and we should expect the numbers to be worse.

5. **Their entanglement finding is directionally supportive but weaker than we want.** Untargeted traits do move (conscientiousness/neuroticism fluctuate most), but "the fluctuations did not reach the strength and direction" of targeted changes. So this is evidence *for* leakage existing, and *against* leakage dominating. If our platform wants to claim entanglement is a serious failure mode, this paper is only partial support — the stronger numbers are in the multi-aspect CTG literature (`steer-multiaspect-distributional-lens.md`, `steer-tailor.md`).

6. **Model scale is a confound we must control.** The 8B vs 540B split (Δ 0.64 vs 2.53) means elasticity is a property of *the model*, not of the character sheet. Any elasticity number we publish is only meaningful per-model, and comparing elasticity across models may mostly re-measure model capacity.

7. **Honest limitation of this source.** The models tested (Flan-PaLM, Flan-PaLMChilla, PaLM 62B/8B/540B) are 2023-era and none are RLHF'd chat models of the kind our platform actually serves. Instruction-tuned modern chat models have much stronger persona-adherence priors and also much stronger "assistant" attractors that could flatten trait dosing. The ρ ≥ 0.90 figure should not be assumed to transfer. Also, IPIP-NEO administered to an LLM is a contested instrument (see `psycho-benchmark-validity-critiques.md`, `rp-bench-incharacter.md`).

8. **Related:** `steer-dexperts.md` and `steer-cfg-guidance-scale.md` (the same dose-response logic on a decoding knob, with explicit brittleness knees), `multiturn-persona-drift.md` (does the dose survive 20 turns? nobody has asked), `rp-bench-incharacter.md` (psychometric probing of roleplay agents).
