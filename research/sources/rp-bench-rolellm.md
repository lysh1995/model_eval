---
title: "RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models (RoleBench)"
url: https://arxiv.org/abs/2310.00746
authors: Zekun Moore Wang, Zhongyuan Peng, Haoran Que, Jiaheng Liu, Wangchunshu Zhou, Yuhan Wu, Hongcheng Guo, Ruitong Gan, Zehao Ni, Jian Yang, Man Zhang, Zhaoxiang Zhang, Wanli Ouyang, Ke Xu, Stephen W. Huang, Jie Fu, Junran Peng
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# RoleLLM / RoleBench

- **arXiv:** 2310.00746 (submitted 1 Oct 2023; 30 pages)
- **Published venue:** Findings of the ACL 2024 — <https://aclanthology.org/2024.findings-acl.878/>
- **Code/data:** <https://github.com/InteractiveNLP-Team/RoleLLM-public>
- **HuggingFace dataset:** <https://huggingface.co/datasets/ZenMoore/RoleBench> (released 19 Oct 2023)

## Abstract (VERBATIM)

> The advent of Large Language Models (LLMs) has paved the way for complex tasks such as role-playing, which enhances user interactions by enabling models to imitate various characters. However, the closed-source nature of state-of-the-art LLMs and their general-purpose training limit role-playing optimization. In this paper, we introduce RoleLLM, a framework to benchmark, elicit, and enhance role-playing abilities in LLMs. RoleLLM comprises four stages: (1) Role Profile Construction for 100 roles; (2) Context-Based Instruction Generation (Context-Instruct) for role-specific knowledge extraction; (3) Role Prompting using GPT (RoleGPT) for speaking style imitation; and (4) Role-Conditioned Instruction Tuning (RoCIT) for fine-tuning open-source models along with role customization. By Context-Instruct and RoleGPT, we create RoleBench, the first systematic and fine-grained character-level benchmark dataset for role-playing with 168,093 samples. Moreover, RoCIT on RoleBench yields RoleLLaMA (English) and RoleGLM (Chinese), significantly enhancing role-playing abilities and even achieving comparable results with RoleGPT (using GPT-4).

## The four-stage RoleLLM framework

1. **Role Profile Construction** — 100 roles, profiles built from scripts/dialogue lines.
2. **Context-Instruct** — context-based instruction generation, extracting role-specific knowledge from the role's source material to produce role-specific QA.
3. **RoleGPT** — role prompting with GPT (dialogue engineering + few-shot retrieval-augmented style exemplars) to imitate speaking style. RoleGPT is the *reference system* whose outputs become ground truth for RoleBench.
4. **RoCIT** — Role-Conditioned Instruction Tuning on RoleBench, producing RoleLLaMA (English) and RoleGLM (Chinese).

Important structural note: RoleBench's "ground truths" are **RoleGPT (GPT-generated) outputs**, not human-written references. This is a key methodological caveat — the benchmark measures similarity to a GPT-4-class role-prompted system rather than to human gold standards.

## Dimensions / criteria scored

RoleBench scores **three** dimensions, each computed as a Rouge-L overlap against a different ground-truth set:

| Abbrev. | Dimension | Verbatim description |
|---|---|---|
| **CUS** | Speaking Style Imitation | "the model's ability to mimic the speaking style associated with a particular role" |
| **RAW** | Answering Accuracy | "the model's response accuracy to instructions" — measured against raw ground-truths (i.e., the original general-purpose instruction answers, *without* role-playing) |
| **SPE** | Role-Specific Knowledge | "the model's role-specific knowledge and memories" — measured against the responses to role-specific (Context-Instruct-generated) instructions |

So: **CUS** = style, **RAW** = general instruction-following correctness, **SPE** = role knowledge/memory. There is no separate safety, empathy, engagement, or morality dimension — RoleBench is deliberately narrow compared with CharacterEval/CharacterBench.

## How it scores

**1. Automatic (primary):**
> "We employ Rouge-L (Lin, 2004) to measure the overlap between model predictions and ground truths."

Rouge-L against three different reference sets yields the CUS / RAW / SPE triple. This is **reference-based n-gram overlap**, not an LLM judge and not a rubric scale — a notable weakness for open-ended roleplay where many valid responses share little lexical overlap with the reference.

**2. GPT-based (secondary):**
Following AlpacaEval, models are compared via GPT evaluators producing:
- **Win rate** — "signifying the frequency at which a model is favored over RoleGPT by GPT-3.5" (i.e., **pairwise comparison against RoleGPT as the fixed baseline opponent**, judged by GPT-3.5)
- **Average ranking** positions.

**3. Human evaluation (data-quality check only, not model scoring):**
Sampling 100 instances each from the general and role-specific subsets, expert annotators confirmed:
- **100%** — can the generated response answer the instruction?
- **84%** — does the response reflect the character's speaking style?
- **77%** — is the response correct?

## Inter-annotator agreement / judge-human correlation

**None reported.** The paper reports no inter-annotator agreement statistics (no kappa, alpha, Pearson, Spearman, or Kendall), and no correlation between the GPT-3.5 judge and human raters. The human evaluation above is a one-off data-quality audit with three binary questions, not a validated judge calibration.

This is a significant gap: RoleBench's Rouge-L metrics and its GPT-3.5 pairwise judge are both **unvalidated against human judgment**.

## Dataset size and composition

- **168,093 samples** total, across **23,463 instructions**, **100 roles**.
- **Role split:** 95 English roles / 5 Chinese roles.
- **General-purpose data:** 147,609 samples (140,225 English; 7,384 Chinese)
- **Role-specific data:** 20,484 samples (18,949 English; 1,535 Chinese)

Roles span fictional characters (Jack Sparrow, Sherlock Holmes), historical figures (Abraham Lincoln, Malcolm X), and Chinese literary characters (孙悟空, 李白). English roles are drawn primarily from movie/TV scripts.

## Models evaluated

- **English:** RoleGPT, LLaMA, Alpaca-7B, Vicuna-13B, RoleLLaMA
- **Chinese:** RoleGPT, ChatGLM2, RoleGLM

A small evaluation set (~8 systems) compared with CharacterBench (18) or RoleEval (many). RoleLLM is framed as much as a *training* contribution as an evaluation one.

## Multilingual coverage and multi-turn support

- **Bilingual but heavily English-skewed:** 95/100 roles English, 5 Chinese. Chinese coverage is a small annex (7,384 general + 1,535 role-specific samples), not a peer of the English set.
- **Multi-turn: NO.** RoleBench is **single-turn instruction→response**. There is no multi-turn dialogue evaluation, no context accumulation, no memory-over-turns testing. This is the single biggest limitation for companion/roleplay use cases, where degradation over long conversations is the central failure mode.

## Stated limitations and known criticisms

**No dedicated Limitations section** in the paper. Acknowledged constraints in-text:
- RoleLLaMA trails RoleGPT on speaking style and accuracy metrics.
- Role-specific knowledge (SPE) scores for **unseen roles** show minimal improvement — i.e., generalization to new characters is weak.

**Criticisms (from the broader literature and structural analysis):**
1. **GPT-4 outputs as ground truth** — the benchmark rewards imitating RoleGPT, capping the measurable ceiling at RoleGPT's own behavior and baking in GPT-4's stylistic biases.
2. **Rouge-L is a poor proxy for roleplay quality** — lexical overlap penalizes valid diverse responses and rewards surface mimicry. Later benchmarks (CharacterEval, CharacterBench) explicitly move to generative/rubric evaluation partly in reaction to this.
3. **Single-turn only** — cannot detect persona drift, memory failure, or long-conversation degradation.
4. **No judge validation** — no human-correlation numbers for the GPT-3.5 pairwise judge.
5. **Thin Chinese coverage** despite the bilingual framing.
6. **Narrow dimension set** (3) — no safety, morality, empathy, or engagement axes.

## Relevance to a companion-eval platform

- Useful as a **style-imitation** and **role-knowledge** signal source, and its 100-role profile set is a reusable asset.
- **Not** usable as-is for companion evaluation: single-turn, Rouge-L-based, no emotional/safety dimensions, no judge validation.
- The CUS/RAW/SPE decomposition is worth borrowing conceptually — separating *style*, *task correctness*, and *character knowledge* is a clean factorization, even if the measurement instrument is dated.

## Citation

```bibtex
@article{wang2023rolellm,
  title   = {RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models},
  author  = {Wang, Zekun Moore and Peng, Zhongyuan and Que, Haoran and Liu, Jiaheng and Zhou, Wangchunshu and Wu, Yuhan and Guo, Hongcheng and Gan, Ruitong and Ni, Zehao and Yang, Jian and Zhang, Man and Zhang, Zhaoxiang and Ouyang, Wanli and Xu, Ke and Huang, Stephen W. and Fu, Jie and Peng, Junran},
  year    = {2023},
  journal = {arXiv preprint arXiv:2310.00746}
}
```
