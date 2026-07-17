---
title: "Does Prompt Formatting Have Any Impact on LLM Performance?"
url: https://arxiv.org/abs/2411.10541
authors: Jia He*, Mukund Rungta*, David Koleczek, Arshdeep Sekhon, Franklin X Wang, Sadid Hasan (1 Microsoft; 2 MIT — Franklin X Wang is MIT, all others Microsoft; * equal contribution)
year: 2024 (arXiv preprint, 15 Nov 2024; arXiv comments state "Submitted to NAACL 2025" — NAACL 2025 Industry Track publication NOT VERIFIED, see venue note)
type: paper
accessed: 2026-07-16
topic: steerability
---

**Same content, four wrappers (plain text / Markdown / JSON / YAML), and performance moves significantly on every benchmark×model cell but one. The paper's famous "40% in a code translation task" number is the one thing in it I could NOT reconcile with its own tables — it appears exactly once, in the abstract, and nothing in the paper supports it. Its "larger models are more robust" claim is real, hedged, and directly contradicted by its own GPT-4 data point.**

> **VENUE NOTE — do not propagate unverified.** The arXiv comments field says only **"Submitted to NAACL 2025"**. Only v1 exists (no v2+). I searched the ACL Anthology NAACL 2025 proceedings index and ran a site-restricted search for an Anthology entry; **no ACL Anthology record was found**. The widely-repeated "NAACL 2025 Industry Track" attribution is **NOT VERIFIED IN TEXT**. Cite as an arXiv preprint until an Anthology ID is confirmed.

## Abstract (verbatim)

> In the realm of Large Language Models (LLMs), prompt optimization is crucial for model performance. Although previous research has explored aspects like rephrasing prompt contexts, using various prompting techniques (like in-context learning and chain-of-thought), and ordering few-shot examples, our understanding of LLM sensitivity to prompt templates remains limited. Therefore, this paper examines the impact of different prompt templates on LLM performance. We formatted the same contexts into various human-readable templates, including plain text, Markdown, JSON, and YAML, and evaluated their impact across tasks like natural language reasoning, code generation, and translation using OpenAI's GPT models. Experiments show that GPT-3.5-turbo's performance varies by up to 40% in a code translation task depending on the prompt template, while larger models like GPT-4 are more robust to these variations. Our analysis highlights the need to reconsider the use of fixed prompt templates, as different formats can significantly affect model performance.

## Method

### Formats compared (4)

**plain text, Markdown, YAML, JSON.** The design is explicitly a *semantically-null* manipulation — this matters enormously for transfer to the platform:

> "We use various input formats: plain text, markdown, YAML, and JSON. **Prompts include five components: *persona*, *task instructions*, *examples*, *output format instructions*, and *user ask*.** We ensure the content of each placeholder stays the same across different prompt formats. **The only differences are in structure and syntax.** To avoid confounding variables, we design the prompts so that the context and meaning remain consistent, regardless of the format."

(Note that **persona is one of the five prompt components** — but it is held *constant* and never manipulated. This paper does not vary persona.)

### Models (4 — all OpenAI GPT, via Azure)

> "For GPT-3.5, we used "gpt-35-turbo-0613" and "gpt-35-turbo-16k-0613" to compare context window sizes (4k vs. 16k). For GPT-4, we used "gpt-4-32k-0613" and "gpt-4-1106-preview" to test the newer, faster variant with a 128k context window."

### Benchmarks (6, in 3 families)

| Family | Benchmarks |
|---|---|
| NL2NL | MMLU, NER Finance (OpenAI Evals) |
| NL2Code | HumanEval, FIND |
| Code2Code | CODEXGLUE (Java↔C#), HumanEval-X (Java→Python) |

### Metrics

- **Sensitivity** — one-sided matched-pair t-test between best and worst format per model×benchmark.
- **Consistency** (from Shu et al. 2023) — "the proportion of test samples that yield identical responses for two prompt templates."
- **Coefficient of Mean Deviation (CMD)** — `CMD = Σ|s(pᵢ) − s̄| / (n · s̄)`. > "A lower CMD indicates that the model's performance is less affected by prompt format changes, showing greater robustness."

## THE NUMBERS

### The "40%" claim — UNVERIFIABLE IN TEXT

The requested claim is verbatim, in the abstract:

> "Experiments show that **GPT-3.5-turbo's performance varies by up to 40% in a code translation task depending on the prompt template**, while larger models like GPT-4 are more robust to these variations."

**"40%" appears exactly ONCE in the entire paper — that abstract sentence.** It is never repeated, derived, or cited in the body, results, or appendices. I checked every occurrence of the string "40" in the full text.

The paper's two code-translation benchmarks are CODEXGLUE (Java↔C#, Table 8) and HumanEval-X (Java→Python, Table 7). Computed from the paper's own tables, **no GPT-3.5 code-translation cell approaches 40% on any reading**:

| Code translation task | GPT-35-turbo-0613 min → max | Absolute | Relative to min | Relative to max |
|---|---|---|---|---|
| CODEXGLUE Java→C# | 66.46 (plaintext) → 78.37 (JSON) | **11.91 pt** | **17.9%** | 15.2% |
| CODEXGLUE C#→Java | 68.81 (plaintext) → 77.49 (JSON) | 8.68 pt | 12.6% | 11.2% |
| HumanEval-X Java→Python | 62.95 (plaintext) → 69.82 (Markdown) | 6.87 pt | 10.9% | 9.8% |

The largest GPT-3.5 swing anywhere near 40% is on **HumanEval — which is code *generation*, not translation**: 40.24 (plaintext) → 59.76 (JSON) = **19.52 pt absolute / 48.5% relative**. Whether the abstract garbled this (note the coincidental "40.24") is **speculation and should not be asserted**.

**Verdict: the "up to 40% in a code translation task" figure is NOT VERIFIED IN TEXT.** Do not repeat it. If a headline number is needed for GPT-3.5 format sensitivity on code translation, use **11.91 points absolute / 17.9% relative on CODEXGLUE Java→C#**, and cite Table 8 directly.

### Sensitivity: best vs. worst format, per model (Table 1, verbatim values)

> "Table 1: Sensitivity of model performance to prompt format assessed using one-sided matched pair t-tests. Table displays metrics for top and bottom formats (Max/Min) and p-values for each dataset/model."

| Benchmark | GPT-35-turbo-0613 | GPT-35-turbo-16k-0613 | GPT-4-1106-preview | GPT-4-32k-0613 |
|---|---|---|---|---|
| MMLU | 59.7 (JSON) / 50.0 (Markdown) *p<0.001* | 59.4 (JSON) / 50.7 (Markdown) *p<0.001* | 81.2 (Markdown) / 73.9 (JSON) *p<0.001* | 81.3 (Markdown) / 77.8 (JSON) *p<0.001* |
| HumanEval | 59.8 (JSON) / 40.2 (Plain text) *p<0.001* | 57.9 (JSON) / 37.20 (Plain text) *p<0.001* | 86.6 (Markdown) / 82.9 (Plain text) *p=0.055* | **76.2 (Plain text) / 21.95 (JSON)** *p<0.001* |
| NER Finance | 37.2 (Plain text) / 24.6 (YAML) *p<0.001* | 36.80 (Plain text) / 21.8 (YAML) *p<0.001* | 53.8 (YAML) / 49.3 (Plain text) *p=0.001* | 53.2 (YAML) / 47.2 (Plain text) *p<0.001* |
| CODEXGLUE (Java2CS) | 78.4 (JSON) / 66.5 (Plain text) *p<0.001* | 78.4 (JSON) / 66.5 (Plain text) *p<0.001* | 77.0 (Markdown) / 68.2 (Plain text) *p<0.001* | 74.2 (Markdown) / 67.2 (Plain text) *p<0.001* |
| CODEXGLUE (Cs2Java) | 77.5 (JSON) / 68.8 (Plain text) *p<0.001* | 77.5 (JSON) / 68.9 (Plain text) *p<0.001* | 83.1 (JSON) / 68.1 (Plain text) *p<0.001* | 75.0 (JSON) / 67.9 (Plain text) *p<0.001* |
| HumanEval-X | 69.8 (YAML) / 63.0 (Plain text) *p<0.001* | 69.8 (YAML) / 62.9 (Plain text) *p<0.001* | 72.4 (JSON) / 63.9 (Plain text) *p<0.001* | 72.3 (JSON) / 65.0 (Plain text) *p<0.001* |
| FIND | 15.9 (Plain text) / 5.2 (Markdown) *p<0.001* | 15.8 (Plain text) / 5.0 (Markdown) *p<0.001* | 20.7 (Markdown) / 20.08 (Plain text) *p<0.0269* | 21.9 (plaintext) / 17.4 (markdown) *p<0.001* |

**Every cell is significant at p<0.05 except GPT-4-1106-preview on HumanEval (p=0.055).** 27 of 28 model×benchmark cells show statistically significant format sensitivity. **No format wins universally** — the best format flips across both benchmark and model.

The paper's own dramatic framing:

> "For instance, in the FIND dataset, both GPT-35-turbo-0613 and GPT-35-turbo-16k-0613 show a dramatic **200% improvement** when prompts are switched from Markdown to plain text. Similarly, for the HumanEval benchmark, the GPT-4 model with a 32k-0613 configuration exhibits an impressive performance boost of **over 300%** when the prompt format is changed from JSON to plain text. This suggests, LLM performance may not be robust to the choice of prompt format."

### GPT-4 vs GPT-3.5 format sensitivity — the CMD numbers (Appendix D.2, Figure 6)

> "The results indicate that the **GPT-4-1106-preview model exhibits superior robustness to format changes, maintaining a performance dispersion consistently below 0.036 across all benchmarks.** In contrast, the **GPT-4-32k-0613 model demonstrates less robustness relative to the GPT-4-1106-preview, yet it outperforms the GPT-3.5 series, with CMDs not exceeding 0.043.** The **GPT-3.5 series displays a broader range of CMDs, from 0.035 to 0.176**, signifying a higher degree of performance variability under different prompt formats."

| Model | CMD (lower = more format-robust) |
|---|---|
| GPT-4-1106-preview | **< 0.036** across all benchmarks |
| GPT-4-32k-0613 | **≤ 0.043** |
| GPT-3.5 series | **0.035 – 0.176** |

**The ranges overlap.** GPT-3.5's *best* CMD (0.035) is better than GPT-4-32k's *worst* (0.043) and essentially ties GPT-4-1106's bound (0.036). The separation is real on average but is **not** a clean split.

MMLU spread, from Table 3 (verbatim cell values, spreads computed):

| Model | Plaintext | Markdown | YAML | JSON | Spread |
|---|---|---|---|---|---|
| GPT-35-turbo-0613 | 54.464 ± 18.300 | 50.021 ± 17.144 | 56.355 ± 16.792 | 59.705 ± 16.594 | **9.68 pt** (19.4% rel.) |
| GPT-35-turbo-16k-0613 | 54.184 ± 19.066 | 50.686 ± 17.436 | 55.901 ± 16.347 | 59.405 ± 17.092 | 8.72 pt |
| GPT-4-1106-preview | 81.005 ± 12.979 | 81.252 ± 12.932 | 80.758 ± 13.000 | 73.918 ± 13.580 | 7.33 pt (9.9% rel.) |
| GPT-4-32k-0613 | 80.638 ± 13.172 | 81.349 ± 13.158 | 81.162 ± 13.110 | 77.800 ± 13.725 | **3.55 pt** (4.6% rel.) |

CODEXGLUE Java→C#, from Table 8:

| Model | Plaintext | Markdown | YAML | JSON | Spread |
|---|---|---|---|---|---|
| GPT-35-turbo-0613 | 66.46 ± 16.04 | 78.10 ± 18.75 | 78.28 ± 18.92 | 78.37 ± 18.93 | **11.91 pt** (17.9% rel.) |
| GPT-35-turbo-16k-0613 | 66.46 ± 16.04 | 78.10 ± 18.75 | 78.30 ± 18.92 | 78.40 ± 18.93 | 11.94 pt |
| GPT-4-1106-preview | 67.16 ± 16.77 | 74.16 ± 16.77 | 70.75 ± 16.08 | 74.16 ± 16.77 | 7.00 pt (10.4% rel.) |
| GPT-4-32k-0613 | 68.19 ± 13.14 | 76.95 ± 18.33 | 76.41 ± 18.00 | 76.86 ± 18.31 | 8.76 pt (12.8% rel.) |

### The GPT-4 counterexample the abstract omits (Table 4, HumanEval)

| Model | Plaintext | Markdown | YAML | JSON |
|---|---|---|---|---|
| GPT-35-turbo-0613 | 40.24 ± 3.98 | 54.27 ± 4.70 | 42.68 ± 4.14 | 59.76 ± 4.85 |
| GPT-35-turbo-16k-0613 | 37.20 ± 3.77 | 48.17 ± 4.44 | 37.20 ± 3.77 | 57.93 ± 4.81 |
| GPT-4-1106-preview | 82.93 ± 4.39 | 86.59 ± 4.06 | 85.37 ± 4.18 | 86.59 ± 4.06 |
| **GPT-4-32k-0613** | **76.22 ± 4.76** | 75.61 ± 4.78 | 68.29 ± 4.92 | **21.95 ± 2.48** |

**GPT-4-32k-0613 collapses from 76.22 (plaintext) to 21.95 (JSON) — a 54.27-point absolute / 71.2% relative wipeout**, far larger than *any* GPT-3.5 format effect in the paper. The larger model is the most format-brittle single cell in the entire study. The paper explains it as a behavioral failure, not a capability one:

> "Further examining GPT-4-32k-0613's performance, we notice the CMD on HumanEval benchmark is extremely high, this is due the extremely low score using JSON format [...] Analyzing the model outputs, we find the poor performance is because **most of the time the model would generate chain of thought in plain text, but did not continue with actually generating the code.** The other models did not exhibit this behavior for the JSON template. We hypothesize that this may be related to the OpenAI's claim about fixing laziness in task completion in the 0125 version of GPT-4-turbo."

### Cross-format consistency (Section 4.2, MMLU + FIND, temperature = 0)

> "For MMLU, we set the temperature to zero to eliminate response variability. The **GPT-3.5-turbo series displayed low consistency, with scores below 0.5, and only 16% identical responses between Markdown and JSON formats.** In contrast, **GPT-4's consistency scores surpassed 0.5**, indicating better reliability across different prompts. For the FIND dataset [...] GPT-4 again outperformed the GPT-3.5-turbo series in consistency. These findings suggest that larger models like GPT-4 are more consistent, **but there is still a need for model improvements to achieve reliable performance across various formats.**"

| Model family | MMLU consistency | Notable |
|---|---|---|
| GPT-3.5-turbo series | **< 0.5** | **only 16%** identical responses Markdown vs JSON |
| GPT-4 | **> 0.5** | still means **up to ~half** of answers change with format |

> "Figure 2: Consistency comparison for MMLU dataset: GPT-3.5 models show consistency scores below 0.5 across format pairs, whereas GPT-4 consistently exceeds 0.5, indicating greater reliability."

**Even the "robust" model changes a large fraction of its answers when only the syntax changes.** Note the deep tension: GPT-4's *accuracy* barely moves (MMLU spread 3.55 pt for GPT-4-32k) while its *answers* churn on ~half the items. **Aggregate scores mask per-item instability.** This is the most important finding in the paper for the platform.

### The scale claim — exact statements and scope

Three statements, escalating in confidence, all in this paper:

1. Abstract: > "while **larger models like GPT-4 are more robust to these variations**"
2. Appendix D.2 conclusion: > "**In summary, larger models are more robust to template variation.**"
3. Conclusion §6 (hedged): > "Regarding explainability, we observe that model size affects model's responses to prompt variations. For instance, GPT-4's performance is less influenced by prompt changes compared to GPT-3.5, **suggesting that larger models may process prompts more consistently.**"

**Scope and confounds, in the paper's own words:**

- Size is *assumed*, not known: > "**While the architectural details and exact size of GPT-4 are not published, it is assumed that** GPT-4 contains significantly more parameters, was trained on more data than GPT-3.5, and is clearly the overall more capable model."
- Recency, not size, is the better-supported explanation: > "Notably, the **GPT-4-1106-preview model achieves greater robustness compared to the GPT-4-32k-0613**, corroborating existing evidence that suggests **the former has a heightened proficiency in comprehending and generating content in specific formats as instructed**." Both are "GPT-4"; size is held roughly constant and robustness still differs — so the *within-GPT-4* variation is a **recency/training effect, not a scale effect**.
- The alternative mechanism the paper itself floats: > "GPT-4's observed improvements **may be attributed to its enhanced ability to process data in diverse formats.**" That is *format-following skill*, which is a trained capability, not a parameter count.
- Family scope: > "This study was focused on GPT-based models, however, we plan to examine the impact of prompt formats on other models, such as LLaMA, Gemini, PaLM, or smaller models like Phi in the future."

**Assessment of the claimed contradiction with Sclar et al. (FormatSpread):** this paper **cites Sclar et al. (2023)** in its own intro ("one study showed that LLMs are sensitive to minor fine-grained prompt modifications, such as separators or capitalization changes"). The tension is **real but much weaker than a clean contradiction**, and the platform should not present it as one:

- **n = 4 models, all OpenAI GPT, with unpublished parameter counts.** This cannot support a scaling law. It is a 2-family comparison with size, recency, training data, and format-following ability all confounded.
- **The CMD ranges overlap** (GPT-3.5 best 0.035 vs GPT-4-32k worst 0.043).
- **Its own largest format effect is on a GPT-4 model** (HumanEval JSON, 76.22 → 21.95).
- The mechanism the paper endorses for its *cleanest* comparison (1106-preview > 32k-0613) is **recency/instruction-following, not scale**.
- **PromptRobust (`steer-promptbench.md`) finds the opposite on 9 models across 6 families**: > "there seems to be no clear correlation between model robustness and size [...] despite being the smallest, T5-large demonstrates robustness on par with larger models such as ChatGPT."

**Net: the honest reading is "the newer, better instruction-following GPT-4 is less format-sensitive than GPT-3.5 on 6 benchmarks, on aggregate scores, with overlapping ranges and one severe counterexample." That is not "sensitivity shrinks with scale," and it does not overturn FormatSpread.**

## Relevance to companion-eval-platform

### Where it transfers

1. **The consistency-vs-accuracy gap is the single most valuable result here, and it is a warning aimed squarely at the platform.** GPT-4's MMLU accuracy moves only 3.55 points across formats while >40% of its individual answers flip. **A stable aggregate is not a stable model.** The platform's persona metrics are aggregates (mean shyness score over N responses). If it measures only aggregate trait scores, it will report "not BRITTLE" for models whose per-response behavior is churning violently. **The platform should adopt a consistency metric — paired, per-item, temperature-0, same content — alongside its trait deltas, or it will systematically under-detect BRITTLE.** This paper is the proof that the two come apart, and the method (Shu et al.'s identical-response proportion) is trivially portable.
2. **It establishes that a semantically-null wrapper change is enough to move behavior** — 27/28 cells significant at p<0.05, with a fixed, non-adversarial, 4-item format set. Unlike PromptRobust, **there is no adversarial search here**, so these effects are much closer to an "expected effect of an innocuous edit" than PromptRobust's worst-case-under-search. **For a brittleness prior, this paper's effect sizes are the more honest reference class**, and they are far smaller than 33%: mostly 4–20% relative on aggregate scores.
3. **Format is a confound the platform must control.** If persona prompts are rendered in different structures across conditions (or if the trait-intensity manipulation incidentally changes prompt structure/length), format variance will leak into the trait deltas. The platform should **fix one format across all persona conditions and report it**, and ideally replicate its headline result under a second format. This paper shows the best format is model-dependent, so there is no safe universal default.
4. **The prompt decomposition is directly reusable**: persona / task instructions / examples / output format instructions / user ask. That is a sane schema for the platform's system prompts, and it isolates *persona* as one manipulable slot with the rest held fixed.

### Where it does NOT transfer — the crux, stated honestly

**This paper is the purest possible example of the mismatch, and the platform must not launder it into a claim about persona steering.**

| | This paper | companion-eval-platform |
|---|---|---|
| Perturbation | **semantically-null by construction** ("The only differences are in structure and syntax") | **semantically-meaningful** ("shy" → "very shy") |
| Correct response | **none** — identical output | **a change, monotone in intensity** |
| Outcome | **accuracy** on labelled tasks (+ answer identity) | **behavior**, no ground truth |
| Failure = | any sensitivity | *insensitivity* (DEAD) or *erratic* sensitivity (BRITTLE) |

- **Its perturbation is null *by explicit design*.** The authors state they engineered the meaning to be constant "to avoid confounding variables." Their whole result is "the model reacts to something that carries no information." The platform's intensity words **carry information** and the model **is supposed to react**. **A model could be maximally format-sensitive and still perfectly, monotonically steerable by intensity words — the two are orthogonal constructs.** Nothing here bounds persona-steering brittleness.
- **It never varies persona.** Persona is one of its five prompt slots and is deliberately held **constant**. Despite the surface-level appeal of "a Microsoft paper with `persona` in the prompt schema," **this paper contains zero evidence about persona-trait steerability.** Do not cite it as if it does.
- **All findings are OpenAI-GPT-only, on 2023-era models (0613 / 1106-preview).** The limitations section concedes the family restriction. For a 2026 platform these models are three generations stale, and the "GPT-4 is more format-robust" result is precisely the kind of claim most likely to have been overtaken by later instruction-tuning.
- **The "40%" is unsupported by the paper's own tables** (see above). If the platform's design doc cites this paper's headline to argue "brittleness is huge," it will be citing a number the paper never demonstrates — and the numbers it *does* demonstrate (mostly single-digit to ~20% relative on aggregate scores) argue for a **much more modest** brittleness prior than "BRITTLE is the default."
- **ENTANGLED gets nothing here.** Single-outcome-per-task design; no cross-trait or cross-construct measurement of any kind.

### The bearing on "is BRITTLE the default?"

**This paper, read carefully, weakens rather than strengthens that claim** — which is the opposite of how it is usually deployed.

- Its aggregate effects under *benign, non-adversarial, semantically-null* edits are **mostly modest** (GPT-4-32k MMLU: 3.55 points across all four formats).
- Its large effects are either **adversarially-flavored outliers** (GPT-4-32k HumanEval JSON, a specific parse/laziness pathology) or **low-baseline benchmarks where relative percentages explode** (FIND's "200%" is 5.2 → 15.9).
- Its own framing is **"reconsider fixed prompt templates,"** not "models are chaos."

**The defensible synthesis across this paper and PromptRobust:** prompt sensitivity is **real, statistically robust, model-dependent, and largely orthogonal to scale** — but the headline percentages come from adversarial search (PromptRobust) or low-baseline relative arithmetic (FIND), and the *typical* benign effect on aggregate scores is far smaller. **The platform should therefore treat BRITTLE as a hypothesis to be measured per-model, not a foregone conclusion to be assumed — and should expect its strongest BRITTLE signal to show up in per-item consistency, not in aggregate trait means.** That last point is this paper's real gift to the project.
