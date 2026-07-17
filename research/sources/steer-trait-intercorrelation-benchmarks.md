---
title: "Cross-trait measurement across LLM personality benchmarks — TRAIT, PsychoBench, PersonaLLM, InCharacter, Machine Mindset (survey of who measures the off-diagonal)"
url: https://arxiv.org/abs/2406.14703
authors: "Seungbeen Lee et al. (TRAIT); Jen-tse Huang et al. (PsychoBench); Hang Jiang et al. (PersonaLLM); Xintao Wang et al. (InCharacter); Jiaxi Cui et al. (Machine Mindset)"
year: 2023-2024
type: paper
accessed: 2026-07-16
topic: steerability
---

# Which personality benchmarks measure the off-diagonal? A survey — answer: almost none, and the omissions are structural

**Adversarial audit of five widely-cited LLM-personality benchmarks against one question: does it measure whether inducing trait X moves trait Y? Result: one shows the off-diagonal as an un-numbered heatmap, one measures role×trait (not trait×trait), and three measure the diagonal only — including one that built the exact factorial design needed and never analyzed it.**

Verification: compiled from a dedicated fan-out pass over the five arXiv sources listed below. TRAIT numbers cross-checked against `arxiv.org/html/2406.14703v1`. Per-cell values in TRAIT Figure 6 and PsychoBench Table 7 are read from rendered figures/tables — **the underlying coefficients are not printed in the text of either paper**, which is itself the finding.

## Scorecard

| Benchmark | arXiv | Measures "does inducing X move Y"? | What it actually reports |
|---|---|---|---|
| **The Personality Illusion** | 2509.03730 | **YES — per-cell β** | see `steer-personality-illusion-crosstalk.md` |
| **TRAIT** | 2406.14703 | **YES, heatmap only** | intercorrelation heatmap under inducing prompts; **no numeric cells** |
| **BIG5-CHAT** | 2410.16491 | **PARTIAL — one scalar** | Frobenius distance; see `steer-big5chat-trait-correlation.md` |
| **PsychoBench** | 2310.01386 | **PARTIAL — role×trait** | full BFI per assigned *role*, not per induced *trait* |
| **PersonaLLM** | 2305.02547 | **NO** | Cohen's d, same-trait high-vs-low only — **despite a 2⁵ factorial** |
| **InCharacter** | 2310.17976 | **NO** | AccDim / StdDim; within-dimension only |
| **Machine Mindset** | 2312.12999 | **NO** | 4-letter MBTI outcomes; no dimension×dimension |

## TRAIT (arXiv 2406.14703) — the off-diagonal exists as a picture

8,000-item personality test built from **BFI + Short Dark Triad (SD3)**, expanded from **71 validated human items → 1,600 personality descriptions** via GPT-4, grounded in **ATOMIC10× / commonsense knowledge graphs**, rendered as scenario-based multiple-choice with trait-aligned and trait-misaligned options.

**Section 4.4 "Intercorrelation in Traits" + Figure 6** (matrices also in Appendix G.3.2). Crucially, the correlations are computed over GPT-3.5 **under personality-inducing prompts** — so this is genuinely an induced-trait off-diagonal, not a baseline-trait correlation.

Findings (verbatim): "(1) a **high inverse correlation between Agreeableness and Dark Triad traits**, and (2) a **high correlation within the Dark Triad traits**" — and these are "**more pronounced**" in LLMs than in human studies, which the authors attribute to the **explicit inducing condition**.

**That last clause is important prior art for us**: TRAIT independently observes that *inducing* traits inflates their intercorrelation relative to humans — the same direction as `steer-structural-amplification.md`'s k = 1.42 and `steer-big5chat-trait-correlation.md`'s prompting = 2.10 (worst). **Three independent lines of evidence now say prompt-induced trait space is more correlated than human trait space.**

Induction effectiveness (Section 4.3 / Figure 5): **85.2 average across eight traits**; GPT-4 **95.2**, GPT-3.5 **88.3**. Resistance to harmful traits: high-Psychopathy **79.8**, high-Neuroticism **72.3**, both below the **85.6** high-trait average. Successfully induced: Machiavellianism **87.3**, Narcissism **85.4**. Verbatim: "**alignment-tuned models are particularly resistant to giving high-Psychopathy and high-Neuroticism responses**."

**Honest caveat: I could not extract per-cell r values. Figure 6 is a rendered heatmap and the text reports no numeric coefficients.** The off-diagonal is shown and described, never tabulated.

## PsychoBench (arXiv 2310.01386, ICLR 2024) — role×trait, which is a different matrix

Assigns holistic **roles** (not single traits), then administers the full BFI — so one manipulation visibly moves many traits at once. Table 7 (BFI, Role Play), **Default → Psychopath**:

| Trait | Default | Psychopath |
|---|---|---|
| Agreeableness | 4.4 ± 0.2 | **1.9 ± 0.6** |
| Openness | 4.2 ± 0.3 | 3.7 ± 0.5 |
| Extraversion | 3.7 ± 0.2 | 3.4 ± 0.5 |
| Neuroticism | 2.3 ± 0.4 | 1.9 ± 0.6 |
| Conscientiousness | 4.3 ± 0.3 | **4.3 ± 0.5** (unmoved) |

Hero role: OPN 4.5 ± 0.3, AGR 4.6 ± 0.2, NEU 1.8 ± 0.3.

**Why this is not our matrix:** the manipulation is a *character* ("Psychopath"), not a *trait dial*. It cannot separate "the psychopath role moved agreeableness because of crosstalk" from "the psychopath role is *defined* as low-agreeableness." Still, the Conscientiousness cell is instructive: a maximally disruptive persona moved AGR by **−2.5** and CON by **0.0**. **Some traits are simply not reachable from some personas** — the matrix is sparse, not uniformly hot. No inter-scale correlation matrix is reported.

## PersonaLLM (arXiv 2305.02547) — THE most striking omission in the literature

**320 personas: 10 per each of 32 = 2⁵ high/low Big Five combinations** (160 ChatGPT + 160 GPT-4). Cohen's d is reported **high-vs-low on the same trait only**:

| Trait | ChatGPT d | GPT-4 d |
|---|---|---|
| Extraversion | **7.81** | 5.47 |
| Agreeableness | 5.93 | 4.22 |
| Conscientiousness | 1.56 | 4.39 |
| Neuroticism | 1.83 | 5.17 |
| Openness | 2.90 | **6.30** |

One-way ANOVA: "statistically significant differences across all five personality traits" (no p-values printed).

**This is the cleanest example of the field's blind spot. A full 2⁵ factorial over five traits, 320 personas, with all five traits scored on every persona, IS a complete steerability matrix — the off-diagonal is a marginal-means calculation away.** They report only the five diagonal effect sizes. **The data to compute what the design-under-test calls novel was collected in 2023 and never analyzed.**

Note also the wild instability of the *diagonal* across models: Conscientiousness d = 1.56 (ChatGPT) vs 4.39 (GPT-4); Neuroticism 1.83 vs 5.17. **Even the diagonal is not a stable property of a trait — it is a property of trait×model.**

## InCharacter (arXiv 2310.17976) — no

Metric is Measured Alignment / **AccDim = 80.7%** best (Expert Rating + GPT-4 on 16Personalities), avg **78.9%**. `StdDim` measures *within*-dimension consistency across runs only. **No trait×trait matrix.**

## Machine Mindset (arXiv 2312.12999) — no

MBTI dimensions trained **independently** (verbatim: "we utilized four datasets corresponding to 'I,' 'N,' 'F,' and 'P'"). Appendix reports full 4-letter type outcomes but **no per-dimension numbers, no dimension×dimension matrix, and no discussion of spillover** — despite training four supposedly-orthogonal axes into one model, which is precisely the setting where interference would show.

## Relevance to companion-eval-platform

1. **The honest headline: the off-diagonal is under-measured, not un-measured, and the pattern of omission is the story.** Of seven benchmarks, one reports per-cell coefficients (`2509.03730`), one shows a heatmap without numbers (TRAIT), one reports a single scalar (BIG5-CHAT). Four report nothing. **We cannot claim novelty for the concept. We can claim it for the resolution: nobody has published the CELLS of a prompt-induction trait×trait matrix.** That claim is narrow, true, and checkable — and this file is the evidence base for it.

2. **PersonaLLM is our best rhetorical asset and our best reality check.** "A 2⁵ factorial with all five traits scored on 320 personas has existed since 2023 and the off-diagonal was never computed" is a compelling framing of the gap. **It is also a warning: if the analysis were valuable and easy, someone would likely have done it.** We should ask honestly why they didn't — plausibly because per-cell estimates from 10 samples/cell are too noisy to publish. **Our design must budget enough samples per cell to beat that, or we will rediscover why the cells went unreported.** This is the main statistical-power risk in the project.

3. **TRAIT independently corroborates trait-space inflation under induction.** "More pronounced [correlations] in LLMs than humans… attributed to the explicit inducing condition" converges with k = 1.42 (`steer-structural-amplification.md`) and prompting-worst Frobenius 2.10 (`steer-big5chat-trait-correlation.md`). **Three methods, three groups, one direction. This is now a well-supported prior: induction inflates the off-diagonal.** Our experiment should be framed as *quantifying a known effect at per-cell resolution*, not discovering one.

4. **PsychoBench's Conscientiousness-unmoved cell (4.3 → 4.3 under a Psychopath role) argues the matrix is SPARSE.** Not every trait is reachable from every perturbation. If true for companion traits, the useful product output is not "here is your crosstalk score" but "**here are the 3 trait pairs in YOUR character sheet that are physically coupled**" — a sparse, actionable list. That is a better product than a dense heatmap nobody reads.

5. **The diagonal itself is model-dependent (PersonaLLM d: CON 1.56 → 4.39 across two models).** Reinforces `steer-personality-shaping-independence.md` point 5: **normalize the off-diagonal by the diagonal per model**, or cross-model comparisons measure capacity, not entanglement.

6. **Alignment tuning resists specific traits (TRAIT: Psychopathy 79.8, Neuroticism 72.3 vs 85.6 avg).** Our companion traits include some RLHF-disfavored directions (cruel, manipulative, cold). **The diagonal will be compressed exactly where the product's dramatic range needs it most**, and a compressed diagonal inflates the off-diagonal/diagonal ratio artifactually. This is a confound we must handle explicitly, not a finding.

7. **Related:** `steer-personality-illusion-crosstalk.md` (the one paper with cells), `steer-big5chat-trait-correlation.md`, `steer-structural-amplification.md`, `steer-personality-shaping-independence.md`, `rp-bench-personallm.md` and `rp-bench-personagym.md` (existing coverage of these benchmarks from the role-play angle — this file is the crosstalk-specific audit; do not duplicate).
