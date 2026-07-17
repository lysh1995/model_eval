---
title: "Personality as a Probe for LLM Evaluation: Method Trade-offs and Downstream Effects"
url: https://arxiv.org/abs/2509.04794
authors: "Gunmay Handa, Zekun Wu, Adriano Koshiyama, Philip Treleaven (Holistic AI / UCL)"
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# Personality as a Probe — trait entanglement so severe that "purification" is a headline contribution

**The key datum: two Big Five traits (openness, conscientiousness) are so entangled in representation space that the authors had to invent a "trait purification" technique to separate them — and they list it as one of four headline contributions in the abstract. That is trait crosstalk, acknowledged as a first-class engineering obstacle rather than a footnote. It is also a mechanism claim: the entanglement is in the ENCODING, not the prompt.**

Verification: HTML fetched from `arxiv.org/html/2509.04794`, stripped to text; the purification and abstract quotes below string-matched against the raw extraction. Table values marked below are from extraction summary and should be re-verified before citation.

## Abstract (verbatim, relevant clauses)

> "Personality manipulation in large language models (LLMs) is increasingly applied in customer service and agentic scenarios, yet its **mechanisms and trade-offs remain unclear**. We present a systematic study of personality control using the Big Five traits, comparing **in-context learning (ICL), parameter-efficient fine-tuning (PEFT), and mechanistic steering (MS)**."

> "Third, we develop **trait purification techniques to separate openness from conscientiousness, addressing representational overlap in trait encoding.**"

> "Experiments on **Gemma-2-2B-IT and LLaMA-3-8B-Instruct** reveal clear trade-offs: **ICL achieves strong alignment with minimal capability loss, PEFT delivers the highest alignment at the cost of degraded task performance, and MS provides lightweight runtime control with competitive effectiveness.**"

## THE ENTANGLEMENT FINDING (verbatim)

> "…**trait overlap between openness and conscientiousness creates unique manipulation challenges that require targeted solutions.** When **openness alignment plateaued**, we refined the direction in two steps: (1) we **purified the openness training subset** to retain high-confidence examples; (2) we formed a new per-layer direction as the **mean activation difference between openness and conscientiousness**, normalized, and then combined it with the base openness direction into a single normalized vector. We re-calibrated l[ayers]…"

**Unpack what happened here.** They tried to steer openness. **It plateaued** — the diagonal saturated. The diagnosis was that the openness direction was contaminated by conscientiousness. The fix was to explicitly **subtract the conscientiousness direction** (contrast vector) from the openness direction.

**That is a crosstalk correction, and it was necessary to make the diagonal work at all.** The off-diagonal was not a curiosity they measured — it was an obstacle that blocked the intended manipulation until removed. This is the strongest available evidence that trait entanglement has *practical*, not merely academic, consequences for trait induction.

> "MS occupies a middle ground: it yields moderate alignment with trait-dependent Δ, which **improves with refined vector construction such as purified openness**."

## Method comparison

- **ICL**: full context prompting with few-shot examples
- **PEFT**: trait-specific **LoRA adapters (rank-64)**
- **MS**: calibrated steering vectors at post-attention layers, from a contrastive high/low-trait dataset
- Evaluation: **within-run Δ analysis** (relative change within each method's own run, to control for baseline variation) across **MMLU** (reasoning), **GAIA** (agentic), **BBQ** (demographic bias)

## Downstream/collateral effects — crosstalk into CAPABILITY space

Values below are from extraction and **should be re-verified against the PDF before citation**:

| Measure | Finding |
|---|---|
| MMLU, Gemma-2 ICL | −0.06 to −0.08 across traits |
| MMLU, Gemma-2 MS | up to **−0.45** for agreeableness |
| MMLU, LLaMA-3 | small within-run Δ across all methods |
| BBQ (SAMB bias), Gemma-2 MS | **±29.7** shifts |
| BBQ, Gemma-2 PEFT | −14.3 to +22.3 |
| Stability | ICL 0.0366, PEFT 0.0363, Steering 0.0326 |
| Agreeableness via ICL | **+0.50** — "most difficult for ICL… suggesting trait-specific representational complexity" |

> "indicating that **embedding personality in parameters competes with general representational resources**"

**BBQ shifts of ±29.7 from a personality manipulation is the number to remember.** Inducing a Big Five trait moves *demographic bias* by up to ~30 points. **The off-diagonal is not confined to trait space — it leaks into safety-relevant behavior.**

No explicit trait×trait correlation matrix is provided.

## Relevance to companion-eval-platform

1. **"Purification" is the most compelling single piece of evidence in this entire research pass that the off-diagonal is REAL and CONSEQUENTIAL.** Not "we measured a correlation" but "**we could not steer openness until we subtracted conscientiousness.**" A published paper lists de-entangling two Big Five traits among four headline contributions. If traits were separable dials, this contribution would not exist. **Lead with this when arguing the problem is real** — it is a concrete engineering failure, which is far more persuasive to a skeptical reader than a heatmap.

2. **It supplies the mechanism that `steer-persona-vectors-crosstalk.md` predicts.** Anthropic: impolite↔apathetic cos = 0.734, evil↔sycophancy = 0.412 — trait directions are non-orthogonal. This paper: openness and conscientiousness overlap so much in encoding that steering one plateaus. **Geometry (Anthropic) → engineering failure (here).** Two independent groups, two model families, same conclusion: **trait directions are not orthogonal, and this bites.**

3. **The plateau is the crucial detail for our dose-response work, and it links two of our claims.** "Openness alignment **plateaued**" — the diagonal saturated. Note `steer-personality-shaping-levels.md` found **openness had the WORST prompt→text ordering (ρ = 0.47)**, the weakest of the Big Five. **Two unrelated papers, two methods (prompting, steering), both find OPENNESS is the hardest trait to control.** That is a convergent, pre-registerable prediction: openness-like traits (curiosity, imaginativeness — very common in companion characters) will have the flattest dose-response curve and the muddiest attribution. **And the saturation may be caused by the entanglement** — which would mean *the diagonal and the off-diagonal are not independent measurements*. A flat diagonal may be a *symptom* of a hot off-diagonal. **If true, this is the most important structural insight in the whole research pass**: the steerability matrix's two halves are coupled, and reporting "elasticity" separately from "crosstalk" would be measuring one thing twice.

4. **BBQ ±29.7 forces the scope question.** Trait induction moved demographic bias by up to ~30 points. Our matrix is trait×trait — but the *dangerous* off-diagonal may be **trait×safety**, not trait×trait. For a companion product, "making her more submissive increased demographic bias by 30 points" is a materially worse finding than "it also made her less confident." **We should include at least one safety axis as a column in the matrix.** This is a cheap addition (BBQ is off-the-shelf) with a high chance of being the most citable result we produce.

5. **ICL (prompting) preserves capability best (MMLU Δ −0.06 to −0.08) — a point IN FAVOR of prompt-space work.** Contrast with MS at −0.45 and PEFT's "degraded task performance." This partially offsets the "prompting is weaker control" prior from `bigtech-persona-vectors.md`/PsySET/Course Correction. **Prompting is weaker but cheaper in collateral damage.** That tradeoff — control strength vs capability cost — is a legitimate axis our platform could own, and it is a better product story than "prompting is worse at everything."

6. **Steal the within-run Δ design.** "Relative change within each method's own run" controls for baseline variation — the same problem that floor effects (evil = 0, sycophancy = 4.4 in persona vectors) create for slope estimates. Our matrix cells must be baseline-normalized or the off-diagonal will be dominated by whichever traits started near the middle of the scale.

7. **Honest limitations.** Small models only (**Gemma-2-2B-IT, LLaMA-3-8B-Instruct**) — the 2B model in particular may entangle traits far more than a frontier model, and `steer-personality-shaping-independence.md` shows control is strongly capacity-dependent (8B: Δ<2.00 vs 540B: Δ=3.67). **The openness/conscientiousness overlap may be partly a small-model artifact and should not be assumed to transfer to our serving model.** Also: no trait×trait matrix here — the entanglement is documented via an engineering workaround and a plateau, not a measurement. It is compelling evidence *that* the off-diagonal is real; it is not an estimate *of* it.

8. **Related:** `steer-persona-vectors-crosstalk.md` (the geometry: cos 0.41–0.73), `steer-personality-shaping-levels.md` (openness ρ = 0.47 — the convergent openness result), `steer-structural-amplification.md` (k = 1.42), `steer-personality-illusion-crosstalk.md` (per-cell off-diagonal), `bigtech-neural-steering-dose.md` and `steer-psyset.md` (prompt-vs-activation control strength).
