---
title: "CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation"
url: https://arxiv.org/abs/2401.01275
authors: Quan Tu, Shilong Fan, Zihang Tian, Rui Yan
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# CharacterEval

- **arXiv:** 2401.01275 — [v1] 2 Jan 2024 16:20:40 UTC; [v2] 9 Jan 2024 18:54:05 UTC
- **Published venue:** ACL 2024 **main conference**, Long Papers — <https://aclanthology.org/2024.acl-long.638/>
- **License:** CC BY-NC-SA 4.0
- **Code/data/reward model:** <https://github.com/morecry/CharacterEval>

## Abstract (VERBATIM)

> Recently, the advent of large language models (LLMs) has revolutionized generative agents. Among them, Role-Playing Conversational Agents (RPCAs) attract considerable attention due to their ability to emotionally engage users. However, the absence of a comprehensive benchmark impedes progress in this field. To bridge this gap, we introduce CharacterEval, a Chinese benchmark for comprehensive RPCA assessment, complemented by a tailored high-quality dataset. The dataset comprises 1,785 multi-turn role-playing dialogues, encompassing 23,020 examples and featuring 77 characters derived from Chinese novels and scripts. It was carefully constructed, beginning with initial dialogue extraction via GPT-4, followed by rigorous human-led quality control, and enhanced with in-depth character profiles sourced from Baidu Baike. CharacterEval employs a multifaceted evaluation approach, encompassing thirteen targeted metrics on four dimensions. Comprehensive experiments on CharacterEval demonstrate that Chinese LLMs exhibit more promising capabilities than GPT-4 in Chinese role-playing conversation. Source code, data source and reward model will be publicly accessible at this https URL.

## The 13 metrics across 4 dimensions (VERBATIM definitions)

### Dimension 1 — Conversational Ability (3 metrics)

| Metric | Verbatim definition |
|---|---|
| **Fluency (Flu.)** | "measures the grammatical correctness of a response, indicating whether a response is readable and free from obvious grammatical errors." |
| **Coherency (Coh.)** | "evaluates the topic relevance between the response and the context." |
| **Consistency (Cons.)** | "assesses the stability of RPCAs during a conversation. Responses of an RPCA should not contradict their own responses in previous turns." |

### Dimension 2 — Character Consistency (5 metrics)

| Metric | Verbatim definition |
|---|---|
| **Knowledge-Exposure (KE)** | "assessing the informativeness of a response, it's crucial for an RPCA to reflect knowledge in its responses." |
| **Knowledge-Accuracy (KA)** | "assess whether this knowledge aligns with the character. The goal is for the RPCA to accurately generate response based on the knowledge from character's profile." |
| **Knowledge-Hallucination (KH)** | "the RPCA should maintain consistency with the character's identity and avoid responding to queries involving unknown knowledge." |
| **Persona-Behavior (PB)** | "A character's behaviors, typically described within brackets, improve the embodied feeling of users by portraying fine-grained actions, expressions, and tones." |
| **Persona-Utterance (PU)** | "a character's speaking style is also important. Each character has unique expression habits. Therefore, the RPCA's utterances should align with these habits." |

Note the deliberate KE/KA/KH triad: **exposure** (does it surface knowledge at all), **accuracy** (is the surfaced knowledge right), **hallucination** (does it refuse/deflect on knowledge the character shouldn't have). This decomposition is one of CharacterEval's more transferable ideas — it separates *informativeness* from *correctness* from *boundary discipline*.

### Dimension 3 — Role-playing Attractiveness (4 metrics)

| Metric | Verbatim definition |
|---|---|
| **Human-Likeness (HL)** | "it is crucial for the RPCA to exhibit a more human-like persona to minimize user resistance." |
| **Communication Skills (CS)** | "users are more likely to engage with an RPCA that demonstrates higher EQ, mirroring the popularity of individuals with strong communication skills." |
| **Expression Diversity (ED)** | "an RPCA should strive to express this diversity in conversation to provide users with a more immersive experience." |
| **Empathy (Emp.)** | "its ability to express empathy can significantly impact its favorability of users." |

### Dimension 4 — Personality Back-Testing (1 metric)

- **MBTI Accuracy.** "we evaluated the accuracy of the MBTI assessment of RPCAs", using "MBTIs of characters featured in CharacterEval from an archive website" as ground truth. The RPCA answers an MBTI questionnaire **in character**; accuracy is computed against the archived character MBTI label.

This is the only dimension not scored by the reward model — it's an objective classification accuracy against an external label.

## How it scores

**Primary: a trained reward model (CharacterRM).**

- **Rating scale:** **five-point scale** for all 12 subjective metrics.
- **Human annotation:** "we recruited 12 annotators to score responses generated by different models."
- **Reward model:** "The human judgements are used to develop a role-playing reward model (CharacterRM), with **Baichuan2-13B-base** as the backbone."
- **Sparse metric assignment:** "each example in CharacterEval is assessed using a subset of these subjective metrics, leading to more differentiated evaluation results." Not every metric applies to every example — metrics are selectively assigned per example (e.g., Empathy is only scored where the context calls for it). This anticipates CharacterBench's sparse/dense distinction.
- **MBTI dimension:** objective accuracy vs. archived ground-truth labels, not reward-model scored.

So CharacterEval is a **trained-reward-model** benchmark, explicitly positioned as an alternative to GPT-4-as-judge — and the correlation table below is the paper's argument for why.

## Judge–human correlation (Pearson) — CharacterRM vs GPT-4

From **Table 2**. These are the paper's headline methodological result: a small fine-tuned reward model substantially outperforms GPT-4 as a judge on Chinese roleplay.

| Metric | CharacterRM (Pearson) |
|---|---|
| Fluency | **0.613** |
| Coherency | **0.607** |
| Consistency | **0.573** |
| Knowledge-Exposure | **0.509** |
| Knowledge-Accuracy | **0.336** |
| Knowledge-Hallucination | **0.411** |
| Persona-Behavior | **0.879** |
| Persona-Utterance | **0.472** |
| Human-Likeness | **0.497** |
| Communication Skills | **0.686** |
| Expression Diversity | **0.765** |
| Empathy | **0.385** |
| **Overall** | **0.631** |

**GPT-4 baselines (overall Pearson):**

| Judge | Overall Pearson |
|---|---|
| GPT-4, 1-shot | **0.362** |
| GPT-4, 2-shot | **0.385** |
| GPT-4, 3-shot | **0.375** |
| **CharacterRM** | **0.631** |

**Only Pearson is reported — no Spearman, no Kendall.**

**Reading the numbers critically:**
- CharacterRM ≈ **1.6–1.7×** GPT-4's correlation overall. Adding shots to GPT-4 barely helps (0.362→0.385→0.375, non-monotonic).
- **Persona-Behavior (0.879)** is by far the strongest — unsurprising, since behaviors are bracketed and thus structurally detectable; this is close to a surface-form cue.
- **Knowledge-Accuracy (0.336)** and **Empathy (0.385)** are weak — the two arguably most important axes for a companion product are the two the reward model is worst at. KA at 0.336 means factual character-consistency scoring is barely better than GPT-4's overall.
- Overall 0.631 is a **moderate** correlation. This is presented as a win, and relatively it is, but it should not be read as "solved" — ~60% of variance is unexplained.
- Independent corroboration is unfavorable: **CharacterBench reports that CharacterJudge achieves only Spearman 21.4 / Kendall 14.3 on CharacterEval data**, the lowest of the three benchmarks it cross-tested, suggesting CharacterEval's labels may be noisy or idiosyncratic.

## Inter-annotator agreement

**Not reported.** Despite recruiting 12 annotators, the paper gives **no** inter-annotator agreement statistic (no Fleiss' kappa, Krippendorff's alpha, or pairwise agreement). This is a real gap — the reward model's ceiling is the annotation quality, and that quality is unquantified. If human–human agreement on Empathy is itself low, CharacterRM's 0.385 may be near-ceiling rather than a model failure.

## Dataset statistics

From **Table 1**:

| Statistic | Value |
|---|---|
| Characters | **77** |
| Conversations (multi-turn dialogues) | **1,785** |
| Avg. turns per conversation | **9.28** |
| Avg. tokens per conversation | **369.69** |
| Training examples | **6,811** |
| Test examples | **4,564** |
| Total (train+test) | **11,376** |

**⚠️ Discrepancy to note:** the **abstract (v2) claims 23,020 examples**, while **Table 1 sums to 11,376** (6,811 + 4,564). The ar5iv-rendered body text also states "11,376 examples." The v1 abstract reportedly used 23,020 as well. Most likely reading: 23,020 counts *(example × applicable metric)* annotation instances or counts both speaker sides, while 11,376 counts response examples. **Cite 1,785 dialogues / 77 characters with confidence; flag the example count as ambiguous (11,376 response-level vs 23,020 abstract-level).**

**Source construction pipeline:** GPT-4 initial dialogue extraction from Chinese novels and scripts → rigorous human-led quality control → character profiles from **Baidu Baike**.

## Models evaluated (Table 3) — 14 systems

**Open-source, general (non-specialized):**
- ChatGLM3 (6B)
- XVERSE (7B, 13B)
- Qwen (7B, 14B)
- InternLM (7B, 20B)
- Baichuan2 (7B, 13B)

**Closed-source, specialized for role-playing:**
- CharacterGLM
- Xingchen (阿里星辰)
- MiniMax
- BC-NPC-Turbo (Baichuan NPC)

**Closed-source, general:**
- GPT-3.5
- GPT-4

**Headline finding:** "Chinese LLMs exhibit more promising capabilities than GPT-4 in Chinese role-playing conversation." Roleplay-specialized Chinese closed-source models (esp. BC-NPC-Turbo, MiniMax) beat GPT-4 on Chinese roleplay — a result about *cultural/linguistic fit and roleplay-specific tuning*, not raw capability.

## Multilingual coverage and multi-turn support

- **Language: Chinese only.** Monolingual by design. Characters come from Chinese novels and scripts; profiles from Baidu Baike. Not usable for English evaluation without full reconstruction.
- **Multi-turn: YES — and this is CharacterEval's main structural advantage** over RoleBench and RoleEval. 1,785 multi-turn dialogues at **9.28 turns average**. Evaluation is per-response *within* accumulated dialogue context, so persona drift and self-contradiction (the Consistency metric) are actually measurable.

## Stated limitations and known criticisms

**No dedicated Limitations section** in the paper.

**Stated in-text (§6.6 robustness analysis):**
- "most models demonstrate a decline in performance as conversations progress"
- "future advancements in RPCA development should focus on enhancing capabilities for longer conversational scenarios"

This is an important empirical finding in its own right: **roleplay quality degrades monotonically with conversation length across nearly all models** — directly relevant to companion products where sessions run long.

**Criticisms / gaps:**
1. **No inter-annotator agreement reported** — annotation quality unquantified, so CharacterRM's ceiling is unknown.
2. **Only Pearson reported** — no rank correlations (Spearman/Kendall), which are more appropriate for ordinal 5-point scales. Pearson on ordinal data overstates agreement when score distributions are skewed.
3. **Example-count discrepancy** between abstract (23,020) and Table 1 (11,376).
4. **Chinese-only** — no English or cross-lingual transfer.
5. **CharacterRM is a 13B model gated behind release** — reproducibility and drift over time are concerns; a fixed reward model also becomes a stale target that models can overfit.
6. **Externally validated as noisy:** CharacterBench's cross-benchmark test found the lowest human-consistency on CharacterEval (Spearman 21.4 / Kendall 14.3) of the three benchmarks it evaluated.
7. **MBTI back-testing is methodologically contested** — MBTI has poor psychometric validity, and "archive website" ground truth for fictional characters' MBTI is fan-assigned, not authoritative.
8. **GPT-4-extracted dialogues** — even with human QC, initial extraction via GPT-4 risks importing GPT-4 stylistic bias into the reference data.

## Relevance to a companion-eval platform

- **Strongest available model** for multi-turn Chinese roleplay evaluation; the 13-metric taxonomy is the most product-relevant of the four benchmarks (empathy, communication skills, expression diversity, human-likeness map directly onto companion UX concerns).
- The **KE/KA/KH decomposition** and the **sparse per-example metric assignment** are both directly borrowable design patterns.
- The **trained-reward-model-beats-GPT-4** result (0.631 vs 0.385) is a strong argument for investing in a fine-tuned judge rather than prompting a frontier model — but note CharacterBench later beat these numbers again (Pearson 68/64).
- **Caveats before adopting:** Chinese-only; unvalidated annotation agreement; weak correlation exactly on Empathy (0.385) and Knowledge-Accuracy (0.336).

## Citation

```bibtex
@inproceedings{tu-etal-2024-charactereval,
  title     = {{CharacterEval}: A {C}hinese Benchmark for Role-Playing Conversational Agent Evaluation},
  author    = {Tu, Quan and Fan, Shilong and Tian, Zihang and Yan, Rui},
  booktitle = {Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2024},
  url       = {https://aclanthology.org/2024.acl-long.638/}
}
```
