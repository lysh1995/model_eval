---
title: "PromptRobust: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts"
url: https://arxiv.org/abs/2306.04528
authors: Kaijie Zhu, Jindong Wang, Jiaheng Zhou, Zichen Wang, Hao Chen, Yidong Wang, Linyi Yang, Wei Ye, Yue Zhang, Neil Zhenqiang Gong, Xing Xie (1 Microsoft Research; 2 Institute of Automation, CAS; 3 Carnegie Mellon University; 4 Peking University; 5 Westlake University; 6 Duke University)
year: 2023 (arXiv v1 Jun 2023; v5 Jul 2024; published as LAMPS '24 @ ACM CCS 2024, pp. 57-68, DOI 10.1145/3689217.3690621)
type: paper
accessed: 2026-07-16
topic: steerability
---

**The canonical evidence that semantically-preserving prompt perturbations wreck task accuracy — word-level attacks cost 33% of relative performance on average. But the metric is a *relative* drop rate, not the "33% absolute" it is usually cited as, and the paper's own data shows brittleness varies ~8.6x across models, which cuts against "BRITTLE is universal."**

> NAMING NOTE: this paper was originally titled **"PromptBench: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts"** (arXiv v1, Jun 2023) and was **renamed to "PromptRobust"** by v5 (Jul 2024), because "PromptBench" was reused for the authors' separate unified evaluation *library* (arXiv 2312.07910). Same paper, same numbers. Cite as PromptRobust; note the alias so the reference resolves.

## Abstract (verbatim, v5)

> The increasing reliance on Large Language Models (LLMs) across academia and industry necessitates a comprehensive understanding of their robustness to prompts. In response to this vital need, we introduce PromptRobust, a robustness benchmark designed to measure LLMs' resilience to adversarial prompts. This study uses a plethora of adversarial textual attacks targeting prompts across multiple levels: character, word, sentence, and semantic. The adversarial prompts, crafted to mimic plausible user errors like typos or synonyms, aim to evaluate how slight deviations can affect LLM outcomes while maintaining semantic integrity. These prompts are then employed in diverse tasks including sentiment analysis, natural language inference, reading comprehension, machine translation, and math problem-solving. Our study generates 4,788 adversarial prompts, meticulously evaluated over 8 tasks and 13 datasets. Our findings demonstrate that contemporary LLMs are not robust to adversarial prompts. Furthermore, we present a comprehensive analysis to understand the mystery behind prompt robustness and its transferability. We then offer insightful robustness analysis and pragmatic recommendations for prompt composition, beneficial to both researchers and everyday users.

(v1's abstract is identical except "PromptBench" for "PromptRobust" and "we present comprehensive analysis" for "we present a comprehensive analysis".)

## Method

### The attack taxonomy (4 levels, 7 attacks)

> "We create 4 types of attacks (called *prompt attacks*) to craft adversarial prompts: *character-level*, *word-level*, *sentence-level*, and *semantic-level* attacks by extending 7 adversarial attacks [...] that were originally designed to generate adversarial samples."

| Level | Attacks | What it does |
|---|---|---|
| Character-level | **TextBugger**, **DeepWordBug** | typo-style character manipulation |
| Word-level | **TextFooler**, **BertAttack** | synonym / contextual word substitution |
| Sentence-level | **StressTest**, **CheckList** | appends irrelevant/distractor sentences |
| Semantic-level | **Semantic** | 6-language translationese |

Semantic-level, verbatim:

> "Semantic-level: We simulate the linguistic behavior of people from different countries by choosing 6 common languages (Chinese, French, Arabic, Spanish, Japanese, and Korean) and constructing 10 prompts for each language per dataset. These prompts are then translated into English, introducing linguistic nuances and variations that could potentially impact LLMs."

Attacks are importance-guided, and task-essential words are protected:

> "We determine a word's importance by removing it and observing how much the prediction accuracy drops. A substantial drop in the score signifies the word's criticality to the prompt."

> "We impose additional restrictions on the perturbations, prohibiting alterations to certain task-essential words. For instance, in translation tasks, the word 'translation' is preserved [...]"

### Scale

| Quantity | Value |
|---|---|
| Adversarial prompts generated | **4,788** |
| Attacks | **7** (across 4 levels) |
| Datasets | **13** |
| Tasks | **8** |
| LLMs considered | **9** |
| LLMs actually used in the attack results | **6** |
| Prompt types | **4** (ZS-task, ZS-role, FS-task, FS-role) |
| Prompts per category | "We generate 10 distinct prompts for both role-oriented and task-oriented categories." |

- **8 tasks / 13 datasets:** sentiment analysis (SST-2), grammar correctness (CoLA), duplicate sentence detection (QQP, MRPC), natural language inference (MNLI, QNLI, RTE, WNLI), multi-task knowledge (MMLU), reading comprehension (SQuAD V2), translation (UN Multi, IWSLT 2017), math problem-solving (Mathematics).
- **9 LLMs considered:** Flan-T5-large (0.8B), Dolly-6B, Vicuna-13B, Llama2-13b-chat, Cerebras-GPT-13B, GPT-NEOX-20B, Flan-UL2 (20B), ChatGPT, GPT-4.
- **Narrowed to 6** for results: > "We find that certain LLMs even do not demonstrate satisfactory performance with clean prompts, narrowing our selection to 6 LLMs: Flan-T5-large, Vicuna-13B, Llama2-13B-chat, UL2, ChatGPT, and GPT-4."

### The metric: PDR is RELATIVE, not absolute

This is the single most misquoted thing about this paper.

> "Considering the diverse evaluation metrics across tasks and varying baseline performances across models and datasets, **the absolute performance drop may not provide a meaningful comparison.** Thus, we introduce a unified metric, the Performance Drop Rate (PDR). **PDR quantifies the relative performance decline** following a prompt attack, offering a contextually normalized measure for comparing different attacks, datasets, and models."

`PDR(A,P,f,D) = 1 - [ Σ M(f([A(P),x]), y) ] / [ Σ M(f([P,x]), y) ]`

i.e. **1 − (adversarial score / clean score)**. A PDR of 0.33 means the model retained 67% *of its own clean score* — **not** a 33-percentage-point absolute drop. APDR = PDR averaged over prompts/models/attacks as indicated.

## THE NUMBERS

### The headline — and a caveat: the paper prints TWO different headline numbers

The requested "~33%" is real and verbatim, in Sec. 4.1:

> "Firstly, attack effectiveness is highly variable, with word-level attacks proving the most potent, leading to an **average performance decline of 33%** across all datasets."

But the Introduction of the *same version* states a different number for the same claim:

> "The results highlight a prevailing lack of robustness to adversarial prompts among current LLMs, with word-level attacks proving the most effective (**39% average performance drop in all tasks**)."

Both quotes are present and unchanged in **both** v1 (ar5iv, as "PromptBench") and v5 (arXiv HTML, as "PromptRobust") — this is a durable internal inconsistency, not a version artifact. The **33%** is the one traceable to a table: it is BertAttack's Avg APDR of **0.33** in the attacks×datasets table. I could not locate any table that yields **39%**; scope differs ("across all datasets" vs "in all tasks"). **Use 33%, cite Sec. 4.1, and expect the 39% to show up in others' citations.**

### APDR by attack, averaged over all 13 datasets (v5 Table 2 = v1 Table 4, "Avg" row)

Verified identical in both versions.

| Level | Attack | Avg APDR |
|---|---|---|
| Word | **BertAttack** | **0.33 ± 0.34** |
| Word | TextFooler | 0.31 ± 0.33 |
| Semantic | Semantic | 0.22 ± 0.26 |
| Character | TextBugger | 0.21 ± 0.30 |
| Character | DeepWordBug | 0.17 ± 0.26 |
| Sentence | CheckList | 0.12 ± 0.23 |
| Sentence | StressTest | 0.11 ± 0.23 |

### Which level is most destructive — verbatim ordering

> "Firstly, attack effectiveness is highly variable, with word-level attacks proving the most potent, leading to an average performance decline of 33% across all datasets. **Character-level attacks rank the second, inducing a 20% performance drop across most datasets.** Notably, **semantic-level attacks exhibit potency nearly commensurate with character-level attacks**, emphasizing the profound impact of nuanced linguistic variations on LLMs' performance. **Conversely, sentence-level attacks pose less of a threat**, suggesting adversarial interventions at this level have a diminished effect."

Ranking: **word > character ≈ semantic > sentence.**

> "Generally, word-level attacks emerge as the most potent, and **BertAttack consistently outperforms others across all models**. However, no discernible pattern emerges for the efficacy of the other attacks."

Effect size is wildly dataset-dependent, and attacks can even *help*:

> "For instance, StressTest attacks on SQUAD V2 yield a mere 2% performance drop, while inflicting a 25% drop on MRPC. Furthermore, we observe that **StressTest attack paradoxically bolsters model's performance in some datasets** [...]"

### Does robustness differ across models? Enormously. (v5 Table 3 = v1 Table 6, "Avg" row)

| Model | Avg APDR | Interpretation |
|---|---|---|
| **UL2** | **0.08 ± 0.14** | most robust |
| **GPT-4** | **0.08 ± 0.21** | most robust (**but see caveat below**) |
| T5-large (0.8B) | 0.13 ± 0.19 | |
| ChatGPT | 0.18 ± 0.26 | |
| Llama2-13B-chat | 0.51 ± 0.39 | |
| **Vicuna-13B** | **0.69 ± 0.34** | **least robust — loses ~69% of clean score** |

> "Our analysis reveals that **GPT-4 and UL2 significantly outperform other models in terms of robustness, followed by T5-large, ChatGPT, and Llama2, with Vicuna presenting the least robustness.** [...] **Vicuna, however, exhibits consistently high susceptibility to attacks across all tasks.**"

**The spread is ~8.6x (0.08 → 0.69).** Brittleness is a *model property*, not a constant of nature. GPT-4 even goes *negative* on two datasets (MNLI −0.03, UN Multi −0.02) — attacked prompts scored slightly *better* than clean.

**CRITICAL CAVEAT on GPT-4's 0.08 — it was never actually attacked:**

> "We did not perform prompt attacks on GPT-4 by optimizing the adversarial algorithms since it requires massive rounds of communications and is too costly. **We used the adversarial prompts generated by ChatGPT to evaluate GPT-4** since the adversarial prompts can be transferred (Sec. 4.4)."

GPT-4's number is a *transfer* result. Every other model faced a white-box-ish search optimized against itself; GPT-4 faced ChatGPT's leftovers. **GPT-4's apparent robustness is at least partly an artifact of never being directly optimized against, and is not comparable to the others.** Do not cite "GPT-4 is robust" from this paper without this caveat.

### Robustness does NOT track model size — the paper's own words

> "As shown in Table 10 and 4, there seems to be **no clear correlation between model robustness and size**, for example, despite being the smallest, **T5-large demonstrates robustness on par with larger models such as ChatGPT** on our evaluated datasets."

(0.8B T5-large at 0.13 beats 13B Vicuna at 0.69 by ~5x.) Attributed instead to training/tuning:

> "The observed differences in model robustness might stem from two aspects: 1) the specific fine-tuning techniques employed. For example, both UL2 and T5-large, fine-tuned on large datasets, and ChatGPT, fine-tuned via RLHF, exhibit better robustness than Vicuna."

**This aligns with Sclar et al. (FormatSpread) and cuts against the Microsoft format paper's "larger models are more robust" — see `steer-format-impact-microsoft.md`.**

### Prompt type matters: few-shot ~35% less brittle than zero-shot (v1 Table 7, "Avg" row)

| Prompt type | Avg APDR |
|---|---|
| ZS-task | 0.33 ± 0.36 |
| ZS-role | 0.34 ± 0.37 |
| FS-task | **0.21 ± 0.31** |
| FS-role | **0.21 ± 0.31** |

> "In our analysis, **few-shot prompts consistently demonstrate superior robustness compared to zero-shot prompts across all datasets.** Furthermore, while **task-oriented prompts marginally outperform role-oriented prompts** in overall robustness, both of them show varying strengths across different datasets and tasks."

### Perturbations were validated as semantics-preserving

> "The results in Figure 3 demonstrate that these adversarial prompts generated by character-level, word-level and semantic-level attacks are **at least 85% acceptable by humans**, indicating that our attack is realistic and meaningful."

### Minor arithmetic flag (low stakes)

The footnote deriving 4,788 renders as `4,788 = 3×4×5×13×7 − 336×3×2`, which evaluates to **3,444**, not 4,788. `3×4×5×13×7 − 336×2 = 5,460 − 672 = 4,788` reconciles exactly, so the `×3` looks like a typo. The **4,788** figure itself is stated in the abstract and body and is what to cite.

## Relevance to companion-eval-platform

### Where it transfers

1. **It kills the null hypothesis that prompt wording is inert.** Semantically-preserving edits to the *instruction* — not the data — move task accuracy by 33% relative on average, with p-values not even needed given effect sizes. If the platform's DEAD failure mode were the norm, PromptRobust would not exist. Prompts are a live causal channel; measuring their sensitivity is legitimate.
2. **It gives BRITTLE a validated methodological skeleton.** PDR is the right shape for the platform's brittleness metric: *normalize the perturbed score by the entity's own unperturbed baseline*, because raw deltas aren't comparable across models/traits with different baselines. A trait-level analogue — `1 − (trait_score_perturbed / trait_score_baseline)` — inherits PromptRobust's rationale directly. Steal the metric design, and steal the "protect task-essential words" constraint (the platform's analogue: never perturb the trait noun itself, only the intensity modifier).
3. **It disciplines the platform's per-model claims.** The ~8.6x spread (UL2/GPT-4 0.08 vs Vicuna 0.69) is the paper's most useful result for this project and it is *underrated*: brittleness is a property of a specific model's tuning, not of prompting per se. A steerability platform that reports a single "models are brittle" verdict is throwing away the signal that actually matters.
4. **The few-shot result is directly actionable.** Few-shot prompts were ~35% less brittle than zero-shot (0.21 vs 0.33). If the platform's persona prompts are zero-shot system prompts, it is measuring the *most* brittle configuration, and should say so rather than generalizing.

### Where it does NOT transfer — the crux, stated honestly

**This paper cannot tell you that BRITTLE is the default state for persona steering. The perturbation semantics are inverted.**

| | PromptRobust | companion-eval-platform |
|---|---|---|
| Perturbation | **semantically-null** (typo, synonym, translationese) | **semantically-meaningful** ("shy" → "very shy") |
| Correct response to perturbation | **no change** (any change = failure) | **a change, monotone in intensity** (no change = DEAD) |
| Outcome measured | **accuracy** vs. ground truth | **behavior**, no ground truth |
| Failure = | sensitivity | *insensitivity*, or *non-monotone* sensitivity |

The consequences are sharp:

- **The 33% cannot be imported as a brittleness prior.** PromptRobust's number is the answer to "how much does the model move when it *should not move at all*?" The platform's BRITTLE asks "does the model move *erratically* when it *should* move a little?" A model with PDR 0.33 under null perturbations could be perfectly, smoothly monotone under intensity perturbations. **These are different quantities and one does not bound the other.** Asserting "prompt brittleness is known to be huge, therefore BRITTLE is the default" is an equivocation on "brittleness" and the platform should not make it.
- **Worse, the sign flips.** PromptRobust's attacks are *adversarially optimized* — an importance-guided search over substitutions run until performance breaks. It reports something close to a **worst case under search**, not the expected effect of an average paraphrase. The platform's intensity edits are a small, fixed, *non-adversarial* set. Comparing an adversarial max to a benign average will overstate expected brittleness by an unknown but large factor. PromptRobust's own between-dataset variance (StressTest: 2% on SQuAD V2 vs 25% on MRPC) shows how unstable even its own numbers are across conditions.
- **The ground-truth dependency is load-bearing.** PDR's denominator is a *clean accuracy*. Personas have no accuracy. The platform must define trait measurement (judge? classifier? behavioral probe?) before any PDR-analogue means anything, and that measurement's own noise floor will sit *inside* the brittleness estimate. PromptRobust never had to solve this because SST-2 has labels. **This is the platform's hardest unsolved problem and this paper offers no help with it.**
- **ENTANGLED gets nothing here.** PromptRobust perturbs one prompt and measures one task. It has no cross-trait construct, no notion of perturbing X and watching Y move. The nearest cousin is transferability (Sec. 4.4) — adversarial prompts moving *across models* — which is a different axis entirely. **Do not cite this paper for ENTANGLED.**

### The honest one-liner

Cite PromptRobust for: *prompt wording demonstrably and largely controls task outcomes even when meaning is held fixed (33% relative, word-level, adversarially optimized); brittleness varies ~8.6x across models and does not track scale.* Do **not** cite it for: *persona steering is brittle by default*, *33% is an absolute drop*, *GPT-4 is robust* (transfer-only artifact), or anything about trait entanglement.
