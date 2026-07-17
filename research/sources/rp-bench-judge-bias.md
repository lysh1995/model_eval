---
title: "LLM-as-a-Judge bias: self-preference and position bias (threats to cross-model comparability)"
url: https://arxiv.org/abs/2410.21819
authors: "Koki Wataoka, Tsubasa Takahashi, Ryokan Ri (self-preference); Lin Shi et al. (position bias)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# Judge bias — why roleplay scores may not be comparable across models

Not a roleplay benchmark, but **the single biggest threat to our platform's core requirement** (scores comparable across models on the same baseline). Nearly every benchmark in this review uses an LLM judge. These papers quantify how much that judge distorts cross-model comparison.

Sources:
- Self-Preference Bias in LLM-as-a-Judge — https://arxiv.org/abs/2410.21819 (OpenReview: https://openreview.net/forum?id=Ns8zGZ0lmM)
- Judging the Judges: A Systematic Investigation of Position Bias in Pairwise Comparative LLM-as-a-Judge — https://arxiv.org/html/2406.07791v5

---

## Paper 1: Self-Preference Bias in LLM-as-a-Judge

### Abstract (verbatim)

> "Automated evaluation leveraging large language models (LLMs), commonly referred to as LLM evaluators or LLM-as-a-judge, has been widely used in measuring the performance of dialogue systems. However, the self-preference bias in LLMs has posed significant risks, including promoting specific styles or policies intrinsic to the LLMs. Despite the importance of this issue, there is a lack of established methods to measure the self-preference bias quantitatively, and its underlying causes are poorly understood. In this paper, we introduce a novel quantitative metric to measure the self-preference bias. Our experimental results demonstrate that GPT-4 exhibits a significant degree of self-preference bias. To explore the causes, we hypothesize that LLMs may favor outputs that are more familiar to them, as indicated by lower perplexity. We analyze the relationship between LLM evaluations and the perplexities of outputs. Our findings reveal that LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated. This suggests that the essence of the bias lies in perplexity and that the self-preference bias exists because LLMs prefer texts more familiar to them."

### The key mechanistic finding

The bias is **not** "the judge recognizes its own output." It is **"the judge rewards low-perplexity (familiar-to-it) text."** Self-preference is a *symptom*; perplexity affinity is the *cause*. The effect holds "regardless of whether the outputs were self-generated."

### Why this is severe for us specifically

This mechanism is uniquely destructive for **creativity** and **storytelling** scoring:

1. Creative, surprising, stylistically distinctive prose is **by construction high-perplexity**. A judge that rewards low perplexity is **systematically anti-correlated with the creativity construct we claim to measure.** Our creativity dimension may measure the opposite of creativity.
2. It biases *between model families*, not just toward the judge's own outputs. A judge shares a tokenizer/pretraining distribution more with some families than others, so the penalty is **unevenly distributed across the variants we compare**. This is exactly the "same baseline" violation we must avoid.
3. It is invisible to reliability checks. The bias is *stable* — re-running the judge reproduces it. High self-consistency, high test-retest reliability, and a clean regression signal are all fully compatible with this bias. **You cannot detect it by measuring judge agreement with itself.** Only human calibration catches it.

Caveat on sourcing: the arXiv abstract page did not expose the metric's formal definition or per-model coefficients. Those numbers are in the full paper body and were not retrieved here. What is firmly established: GPT-4 shows "a significant degree of self-preference bias," and the perplexity relationship is significant.

---

## Paper 2: Judging the Judges — Position Bias

### Abstract (verbatim, opening)

> "LLM-as-a-Judge offers a promising alternative to human judges across various tasks, yet inherent biases, particularly position bias—a consistent preference for answers based on their position in the prompt—compromise its effectiveness."

### Metric definitions (verbatim)

- **Position Bias** — tendency of LLM judges to favor certain positions within prompt components rather than evaluating content objectively.
- **Repetition Stability (RS)** — "the percentage of the most frequent selections across multiple trials for each query, aggregated from all queries within each dataset."
- **Position Consistency (PC)** — "the ratio of consistent evaluation pairs to the total number of valid evaluations, where a pair is deemed consistent if the model selects the same winner."
- **Preference Fairness (PF)** — assesses whether judges exhibit primacy (favoring first position) or recency bias (favoring last position); fair preference is at 0.

### Scale and numbers

| Quantity | Value |
|---|---|
| Evaluation instances | ~100,000 |
| Judge models | 12 commercial LLMs |
| Benchmarks | 2 (MTBench, DevBench) |
| Tasks | 22 |
| Answer-generating models | ~40 |
| **Repetition Stability (most capable models)** | **RS > 0.95** |
| **Position Consistency (across judges, MTBench)** | **0.57 – 0.82** |

### The headline number: PC 0.57–0.82

**This is the most important number in this file.** Position Consistency of 0.57 means that when you swap the order of two candidate responses, the judge picks a *different winner* up to **43% of the time**. At PC 0.57, the judge is barely above the 0.50 coin-flip floor. Even the best judges (0.82) flip on ~1 in 5 pairs.

Contrast with **RS > 0.95**: judges are highly *self-consistent* when you re-ask the identical question, but *not* consistent when you make a semantically irrelevant change (ordering). This is the trap. **Stability is not validity.** A pairwise judge can look extremely reliable on repeat-run checks and still be near-random with respect to actual content.

Direct implication: **any pairwise-comparison scoring we build must evaluate both orderings and either average or discard ties.** Single-order pairwise scoring at PC≈0.6 would produce a leaderboard substantially driven by prompt ordering. This alone may disqualify pairwise as our primary cross-variant mechanism.

### Roleplay-specific finding

Roleplay is discussed only briefly. On roleplay tasks, **o1-mini exhibited "almost fair preferences"** (PF near 0), contrasting with its primacy preference on coding/math/extraction. Weak positive signal that roleplay may be less position-biased than reasoning tasks — but roleplay results were **not isolated numerically**, so treat as suggestive only, not as license to skip order-swapping.

### Judge-human agreement

**The paper does not report direct judge-human agreement percentages.** It notes prior work claimed "high level of agreement with human judgments" but focuses on position bias rather than human alignment. Worth flagging: this is a recurring pattern across the whole roleplay-benchmark literature — reliability gets measured, validity does not.

### Stated limitations (author-identified)

1. Only pairwise comparative assessment studied; other judging types unexplored.
2. Limited to 12 commercial LLMs; larger open-source models not tested.
3. Only two benchmarks examined.
4. Could not investigate model parameter sizes/architectures directly due to proprietary restrictions.
5. Limited question quantity per task (10 per MTBench task, 8 per DevBench task).
6. Default prompt settings used; prompt variations not explored.

Note limitation 1 constrains transfer: these PC numbers are **pairwise-specific**. Absolute/rubric scoring (what MiniMax and CharacterEval use) has no position to be biased by — it trades position bias for calibration drift instead. That trade-off favors rubric scoring for our use case.

---

## Related, not yet captured

- **Preference leakage** — judges favor specific *model families*, not just themselves. Directly attacks cross-model comparability.
- UDA: Unsupervised Debiasing Alignment for Pair-wise LLM-as-a-Judge — https://arxiv.org/pdf/2508.09724
- Quantifying and Mitigating Self-Preference Bias of LLM Judges — https://arxiv.org/pdf/2604.22891
