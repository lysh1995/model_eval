---
title: "PandaLM: An Automatic Evaluation Benchmark for LLM Instruction Tuning Optimization"
url: https://arxiv.org/abs/2306.05087
authors:
  - Yidong Wang
  - Zhuohao Yu
  - Zhengran Zeng
  - Linyi Yang
  - Cunxiang Wang
  - Hao Chen
  - Chaoya Jiang
  - Rui Xie
  - Jindong Wang
  - Xing Xie
  - Wei Ye
  - Shikun Zhang
  - Yue Zhang
year: 2023
venue: ICLR 2024
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# PandaLM

## Abstract (verbatim opening)

> Instruction tuning large language models (LLMs) remains a challenging task, owing to the complexity of hyperparameter selection and the difficulty involved in evaluating the tuned models.

## Methodology

A fine-tuned **7B** judge model for pairwise comparison, positioned specifically as a tool for **hyperparameter selection during instruction tuning** — i.e. the same job our platform does for variants. PandaLM's framing is the closest in the literature to our use case: *cheap, repeatable comparison of many variants of the same model family.*

Notably, PandaLM is trained to evaluate **subjective factors**:

> "relative conciseness, clarity, adherence to instructions, comprehensiveness, and formality"

**"Adherence to instructions" is the nearest published analogue to our "character fidelity"** — does the output conform to a specification given in the prompt. This makes PandaLM's design worth studying even if we don't use the model.

## Key numbers

**PandaLM-7B evaluation capability (F1-score, relative):**

| Comparison | Relative capability |
|---|---|
| vs GPT-3.5 | **93.75%** |
| vs GPT-4 | **88.28%** |

A **7B** model reaching ~88% of GPT-4's judging F1 is the central claim, and it is the paper's argument for cheap self-hosted judges.

**Caveats on these numbers:**
- These are **relative** capability figures against LLM references, and share JudgeLM's methodological problem: **agreement with GPT-4 is not agreement with humans.** (See `judge-judgelm.md` for the full argument.)
- PandaLM **performed poorly on JudgeBench** (per Tan et al.), consistent with the pattern that distilled judges inherit their teacher's blind spots and collapse on hard pairs.
- The full paper reports a human-annotated test set; the specific inter-annotator agreement figures were not recoverable from the abstract at time of access.

## Design contributions worth borrowing

PandaLM explicitly addresses **position bias** (via order-swapped training data), **length bias**, and **formatting**, and is designed to avoid rewarding verbosity — the paper argues its judge prefers *relative conciseness*, in contrast to the verbosity bias documented in GPT-3.5/Claude-v1 judges by MT-Bench.

## Implications for our platform

- **The use case match is the reason to care**: PandaLM was built to pick among instruction-tuning variants, which is structurally identical to picking among our system-prompt/param variants. Its conclusion — that a small fine-tuned judge is adequate for *relative* comparison within a family — supports a cheap-judge tier for our inner development loop.
- **But its own JudgeBench collapse is the warning**: adequate for coarse variant selection, unreliable for the hard, subtle comparisons that matter once variants are close. Our variants will converge over time, so a PandaLM-class judge's useful life on our platform is the early, coarse phase only.
- Historical value mostly: superseded by Prometheus 2 and modern reward models. Included here for the taxonomy and the use-case parallel, not as a live candidate.
