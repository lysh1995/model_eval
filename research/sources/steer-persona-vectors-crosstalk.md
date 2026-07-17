---
title: "Persona Vectors: Monitoring and Controlling Character Traits in Language Models — trait-crosstalk evidence (Appendix G.2)"
url: https://arxiv.org/abs/2507.21509
authors: Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey (Anthropic Fellows Program / UT Austin / Constellation / Truthful AI / Anthropic)
year: 2025
type: paper
accessed: 2026-07-16
topic: steerability
---

# Persona Vectors — the trait × trait entanglement matrices, extracted in full

**Companion file to `bigtech-persona-vectors.md`, which covers the dose-response/steering-coefficient story. This file exists to hold the CROSSTALK evidence at full numeric resolution: both 7×7 cosine-similarity matrices, the cross-trait predictive-power matrix, and — critically — the fact that Anthropic explicitly leaves steered co-expression as an OPEN QUESTION.**

Verification: extracted from the **v3 PDF** (63 pages, `arxiv.org/pdf/2507.21509v3`). **No HTML exists** — ar5iv reports a fatal conversion error and all `/html/` versions 404. The PDF is the only full-text source. Matrix values read from Figure 20.

## The word "entanglement" appears EXACTLY ONCE in the paper (verbatim)

> "Aggregating these results across all trait pairs yields a 'persona correlation' heatmap shown in Figure 20 (left), which visualizes the degree of alignment or **entanglement** among different trait directions."

The strongest concession is **footnote 6, p. 7** (verbatim):

> "However, it is worth noting that **persona shifts are rather correlated between seemingly different traits**. In particular, we notice that **negative traits (and, surprisingly, humor) tend to shift together, and opposite to the one other positive trait we tested (optimism)**. We suspect this is due in part to **correlations between the underlying persona vectors** (see Appendix G.2), and in part due to **correlations in the data**."

Note it is a **footnote**. The entanglement result is real, numeric, and published — and it is editorially buried.

## Figure 20 caption (verbatim)

> "Figure 20: Top: Llama; Bottom: Qwen. Left: **Pearson correlation between projected finetuning shifts and behavioral changes across different traits.** Each trait's own direction yields the highest predictive accuracy for its behavior. Right: **Cosine similarity between persona vectors.**"

## COSINE SIMILARITY BETWEEN PERSONA VECTORS — full matrices, both models

Trait order: **Evil / Sycophantic / Hallucinating / Impolite / Apathetic / Humorous / Optimistic**

**Llama-3.1-8B-Instruct (Layer 16):**
```
        Evil   Syco   Hall   Impo   Apat   Humo   Opti
Evil    1.000  0.412  0.233  0.440  0.331  0.369 -0.469
Syco    0.412  1.000  0.252  0.294  0.082  0.351 -0.112
Hall    0.233  0.252  1.000 -0.032 -0.108  0.127  0.042
Impo    0.440  0.294 -0.032  1.000  0.734  0.435 -0.484
Apat    0.331  0.082 -0.108  0.734  1.000  0.226 -0.435
Humo    0.369  0.351  0.127  0.435  0.226  1.000 -0.237
Opti   -0.469 -0.112  0.042 -0.484 -0.435 -0.237  1.000
```

**Qwen2.5-7B-Instruct (Layer 20):**
```
        Evil   Syco   Hall   Impo   Apat   Humo   Opti
Evil    1.000  0.368  0.192  0.552  0.390  0.478 -0.472
Syco    0.368  1.000  0.162  0.386  0.072  0.440  0.178
Hall    0.192  0.162  1.000  0.000 -0.013  0.134  0.026
Impo    0.552  0.386  0.000  1.000  0.542  0.594 -0.327
Apat    0.390  0.072 -0.013  0.542  1.000  0.043 -0.336
Humo    0.478  0.440  0.134  0.594  0.043  1.000 -0.144
Opti   -0.472  0.178  0.026 -0.327 -0.336 -0.144  1.000
```

Headline cells:
- **Evil ↔ Sycophantic: 0.412 (Llama) / 0.368 (Qwen)** — the two traits the design-under-test would most want to treat as independent share a substantial direction.
- **Impolite ↔ Apathetic: 0.734 (Llama) / 0.542 (Qwen)** — the strongest positive off-diagonal.
- **Evil ↔ Hallucinating: 0.233 / 0.192** — the *least* coupled pair; hallucination is close to orthogonal to everything (row is ~0.0 to 0.25).
- **Evil ↔ Optimistic: −0.469 / −0.472** — strong negative, i.e. a single evaluative axis.

**The traits are NOT orthogonal by construction.** Off-diagonal cosines of 0.4–0.73 mean a "dial" for one trait is partly a dial for another, mechanically, before any behavior is measured.

## CROSS-TRAIT PREDICTIVE POWER — and the off-diagonal sometimes WINS

Figure 20 (left) is **finetuning-shift → behavior**, not steering. Full matrices (rows = Persona Score /
behavior *B*; columns = Finetuning Shift / direction *A*), extracted verbatim from the v3 PDF text layer:

**Llama-3.1-8B-Instruct:**
```
              Evil   Syco   Hall   Impo   Apat   Humo   Opti   <- direction (finetuning shift)
Evil         0.930  0.645  0.813  0.974  0.951  0.946 -0.907
Sycophantic  0.701  0.893  0.753  0.800  0.800  0.834 -0.724
Hallucinating 0.672 0.646  0.967  0.768  0.871  0.779 -0.703
Impolite     0.881  0.666  0.677  0.944  0.908  0.893 -0.894
Apathetic    0.882  0.553  0.699  0.958  0.936  0.864 -0.945
Humorous     0.844  0.755  0.729  0.916  0.902  0.908 -0.842
Optimistic  -0.924 -0.599 -0.773 -0.985 -0.963 -0.928  0.961
```

**Qwen2.5-7B-Instruct:**
```
              Evil   Syco   Hall   Impo   Apat   Humo   Opti
Evil         0.826  0.600  0.861  0.810  0.814  0.777 -0.734
Sycophantic  0.344  0.758  0.724  0.397  0.425  0.493 -0.234
Hallucinating 0.733 0.728  0.916  0.774  0.829  0.807 -0.713
Impolite     0.855  0.639  0.814  0.862  0.836  0.797 -0.785
Apathetic    0.804  0.465  0.803  0.813  0.839  0.701 -0.782
Humorous     0.793  0.724  0.856  0.808  0.810  0.811 -0.720
Optimistic  -0.867 -0.472 -0.706 -0.870 -0.877 -0.776  0.865
```

### ★ THE CAPTION IS CONTRADICTED BY ITS OWN FIGURE — verified by direct arithmetic

Caption: "**Each trait's own direction yields the highest predictive accuracy for its behavior.**"
Body: "As expected, each trait direction is most predictive of its corresponding behavior change."

**This is false in 7 of 14 trait×model rows.** Recomputed from the values above (|r|):

| model | rows where an off-diagonal ≥ diagonal | worst case |
|---|---|---|
| **Llama** | **4/7** (Evil, Apathetic, Humorous, Optimistic) | Evil behavior: own dir **0.930** < Impolite dir **0.974** |
| **Qwen** | **3/7** (Evil, Humorous, Optimistic) | Evil behavior: own dir **0.826** < Hallucinating dir **0.861** |

It also fails **column-wise** (3/7 in both models), so the result is robust to matrix-orientation ambiguity:
the **Impolite direction predicts Optimistic behavior (−0.985) better than it predicts Impolite behavior
(0.944)**. In Llama the *Impolite* column is the single best predictor of *four* other traits' behavior.

Aggregate margins — the diagonal wins **on average**, but barely:

| model | diag mean \|r\| | off-diag mean \|r\| | margin | off-diag max |
|---|---|---|---|---|
| Llama | 0.934 | **0.816** | **+0.118** | **0.985** |
| Qwen | 0.840 | **0.718** | **+0.122** | 0.877 |

### ★★ THE HEADLINE SEPARABILITY CLAIM IS COMPUTED ON THE 3 LEAST-ENTANGLED TRAITS

Main text §4.2 (verbatim): "We observe strong positive correlations (**r = 0.76–0.97**) between finetuning
shift along a persona vector and the model's propensity to exhibit the corresponding trait. Notably, these
correlations are **higher than cross-trait baselines (r = 0.34–0.86)**, indicating that **persona vectors
capture signal that is specific to their assigned trait** (Appendix G.2)."

**I reconstructed where those two ranges come from.** Restricting Figure 20 to the 3×3 submatrix of the
headline traits (**Evil, Sycophantic, Hallucinating**) over both models:

- diagonal → **0.758–0.967** = the quoted "**0.76–0.97**" ✓ exact match
- off-diagonal → **0.344–0.861** = the quoted "**0.34–0.86**" ✓ exact match

**The separability claim is computed only over the three traits it happens to hold for** — and hallucination
is the near-orthogonal outlier (cosine **0.19–0.25** to everything else). Over **all 7 traits**, in the very
appendix the sentence cites:

- off-diagonal range becomes **0.234–0.985**, and **23/84 off-diagonal cells exceed the quoted 0.86 ceiling**
  (19/42 in Llama alone)
- the diagonal range (0.758–0.967) and the off-diagonal range (0.234–0.985) **overlap across [0.758, 0.985]**

**"Persona vectors capture signal that is specific to their assigned trait" is a claim that survives on a
hand-picked 3-trait subset and fails on the paper's own full 7-trait matrix.** Their own footnote 6 concedes
the mechanism; the main text's framing does not carry it.

*Verification note: matrix values are the PDF text-layer annotations of the Figure 20 heatmaps (matplotlib
renders cell labels as selectable text), not pixel estimates. The 3-trait reconstruction matching both quoted
ranges to the digit is independent confirmation that the extraction is faithful and correctly oriented.*

Appendix G.2 (verbatim):

> "we also observe **strong cross-trait predictive signals** for several traits. For example, the directions for **evil, impolite, apathetic, and humorous exhibit relatively high correlations with each other's behavior changes**, despite having **moderate pairwise cosine similarities**."

And on training data (verbatim):

> "datasets targeting one trait (e.g., evil) can **inadvertently amplify other traits** (e.g., sycophancy or hallucination)."

## THE OPEN QUESTION — Anthropic says the steered off-diagonal is UNMEASURED

In the Discussion / future work, verbatim:

> "**Do correlations between persona vectors predict co-expression of the corresponding traits?**"

**This is the single most valuable sentence in the paper for us.** Anthropic has the vectors, has the cosine matrix, has the steering apparatus — and explicitly flags "does steering evil also raise sycophancy?" as **not answered**. The entanglement matrix they publish is over **finetuning-induced shifts** and **vector geometry**, never over **steering-induced or prompt-induced behavioral co-expression**.

## Prompted vs. steered induction — partial, and NO direction comparison

§3.3: **8 system prompts** interpolating suppress→promote; many-shot at **0/5/10/15/20** examples.

> "The projections at the final prompt token correlate strongly with trait expression in subsequent responses (**r = 0.75–0.83**)"

Table 2 (overall / within-condition):

| Trait | System prompt | Many-shot |
|---|---|---|
| Evil | 0.747 / 0.511 | 0.755 / 0.735 |
| Sycophancy | 0.798 / 0.669 | 0.817 / 0.813 |
| Hallucination | 0.830 / **0.245** | 0.634 / 0.400 |

Caveat (verbatim): "These correlations arise primarily from **distinguishing between different prompt types**… may be **less reliable for more subtle behavioral changes**."

**Hallucination's within-condition r collapses to 0.245.** The monitor works across coarse prompt types and largely fails within them.

**No cosine similarity between the prompt-induced activation shift and the persona vector is reported** — only a scalar projection. So the question "does prompting move activations along the *same direction* as steering?" is **not answered**. Projection is a shadow, not an alignment: a shift could project strongly while pointing substantially elsewhere.

## Coherence degradation at high coefficient

> "a 'coherence score' (following Betley et al. (2025), where each response is **rated 0–100 by GPT-4.1-mini** based on its coherence)… **For all results presented, average response coherence is above 75.**"

> Preventative steering: "maintaining an average coherence score across all models **above 80**."

> Appendix J.2: "we **select the largest steering coefficient for which the model's coherence remains above 80**, ensuring the model is not broken."

> "large steering coefficients tend to **degrade accuracy**, indicating a **loss in general capability**" / "inference-time steering tends to **break the model**"

**No exact MMLU numbers appear in the text — they exist only as unlabeled gray plot lines.** Honest limitation: the "coherence collapse" is qualitative in the prose and only visual in the figures.

Coefficients swept: **0.50–2.50** (Qwen layer sweep), **0.4–1.2** (Llama), **0.00–2.00** (Fig. 30). SAE steering α=2.5 (evil/sycophancy), α=1.5 (hallucination); human eval at 1.5; preventative at 0.5 and 1.25.

Baseline trait expression pre-finetuning: **0 (evil), 4.4 (sycophancy), 20.1 (hallucination)**.

## Relevance to companion-eval-platform

1. **The strongest single argument FOR running the experiment is Anthropic's own open question.** "Do correlations between persona vectors predict co-expression of the corresponding traits?" is, verbatim, our research question — asked by Anthropic and left unanswered. That is a far better framing than "nobody has measured crosstalk" (false). **Lead with this.**

2. **We have a published mechanism AND a published prior for the effect size.** Cosine 0.41 (evil↔sycophancy) and 0.73 (impolite↔apathetic) predict *which* off-diagonal cells should be hot. If our prompt-space matrix's off-diagonal correlates with Anthropic's cosine matrix, that is a real result: **prompt-space crosstalk is explained by activation-space geometry.** If it does *not* correlate, that is a *more* interesting result. Either outcome is publishable — a rare property, and the reason this experiment is worth funding.

3. **Cosine similarity is the theoretical floor on achievable independence.** If two trait directions have cos = 0.73, no prompt can move one without moving the other by ~0.73× the projection. **Our matrix's off-diagonal is lower-bounded by geometry we did not choose.** This reframes the platform's value: not "detect crosstalk" but "**tell an author which trait pairs are physically un-composable**."

4. **Hallucination's near-orthogonality (0.19–0.25 to everything) is the control condition.** It gives us a trait pair that *should* show ~0 crosstalk. If our method reports crosstalk between orthogonal traits, our method is broken. **Build this in as a negative control** — without one, a large off-diagonal is indistinguishable from judge noise or a bad rubric.

5. **★ The strongest argument for our platform is that the field's flagship trait-separability claim does not
   replicate on its own data.** The diagonal fails to dominate in **7/14 trait×model rows**, the margin is only
   **+0.12** mean |r|, and the published "specific to their assigned trait" sentence is computed on a 3-trait
   subset chosen from a 7-trait matrix in which it fails. Together with
   `steer-personality-illusion-crosstalk.md` (SelfReg→Conscientiousness β≈4.2–4.8 **>** SelfReg→SelfReg
   β≈2.2–2.9), **two independent papers show off-diagonal-dominant cells, and both bury it.** "Diagonal ≫
   off-diagonal" is not a safe prior — it is the thing to test. **This is our single best citation: not "nobody
   measured crosstalk" (false) but "the two teams that measured it both found the off-diagonal can win, and
   neither made it the headline."**

6. **The within-condition r = 0.245 for hallucination is a warning about our own instrument.** Their monitor mostly discriminates *between prompt types*, not *within* them. Our intensity ladder lives entirely *within* a prompt type. **The regime where their method is weakest is exactly the regime we propose to operate in.**

7. **Copy the coherence gate; don't copy their reporting of it.** "Largest coefficient where coherence > 80" is the right methodology. But note they never publish the MMLU curve numerically — we should, or we inherit the same unfalsifiable claim.

8. **Related:** `bigtech-persona-vectors.md` (dose-response/steering-coefficient story; do not duplicate), `steer-personality-illusion-crosstalk.md` (the prompt-space off-diagonal, with coefficients), `steer-structural-amplification.md` (why trait space is low-rank), `steer-personality-probe-tradeoffs.md` (openness/conscientiousness representational overlap requiring "purification").
