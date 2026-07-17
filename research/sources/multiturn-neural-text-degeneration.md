---
title: "The Curious Case of Neural Text Degeneration"
url: https://arxiv.org/abs/1904.09751
authors: Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi
year: 2019
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# The Curious Case of Neural Text Degeneration

ICLR 2020. arXiv:1904.09751.

**Status: the origin of the repetition/diversity metric vocabulary we will reuse. Old, but every repetition metric in the field descends from it.**

## Abstract

Likelihood maximization in decoding produces bland, repetitive text. Proposes **Nucleus Sampling**, which "truncates the unreliable tail of the probability distribution, sampling from the dynamic nucleus of tokens containing the vast majority of the probability mass."

## Metric definitions (exact — these are what we reuse)

**Repetition Metric:** a phrase with **minimum length 2 tokens** counts as repetition when it appears **at least three times at the generation's end**, within 200 tokens.

**Self-BLEU:** computed by calculating BLEU for each generated document **against all other generations as references**; **lower = more diverse**.

**Zipf Coefficient:** vocabulary distribution against theoretical exponential curve; **s=1 = perfect Zipfian**.

**HUSE:** "Human Unified with Statistical Evaluation" — combines model likelihood with human typicality judgments using KNN classification (**k=13**).

## Results table

| Method | Perplexity | Self-BLEU4 | Zipf | Repetition % |
|--------|-----------|-----------|------|------------|
| **Human** | 12.38 | 0.31 | 0.93 | **0.28** |
| Beam (b=16) | 1.48 | 0.44 | 0.94 | **28.94** |
| Pure Sampling | 22.73 | 0.28 | 0.93 | 0.22 |
| Top-k (k=640) | 13.82 | 0.32 | 0.96 | 0.28 |
| Nucleus (p=0.95) | 13.13 | 0.32 | 0.95 | 0.36 |

**Human text: 0.28% repetition. Beam search: 28.94%** — a ~100× gap.

Note the perplexity inversion: beam search has the BEST perplexity (1.48) and the WORST repetition (28.94%). **Likelihood and quality are anti-correlated in generation.** This is the 2019 ancestor of the modern point that a metric optimized per-token can be maximally wrong at the sequence level — structurally the same argument as ours one level up (per-turn vs per-conversation).

## Relevance to companion-eval-platform

- **The metric definitions transplant directly, but the UNIT must be lifted.** Self-BLEU was defined *across independent generations*; we need **Self-BLEU across TURNS within one conversation** — that is the computable form of "the character keeps saying the same thing." This is a genuine re-definition, not a reuse, and should be documented as such.
- Three distinct repetition units we should separate:
  1. **Intra-response** repetition (classic degeneration; Holtzman's metric as-is) — rare in modern RLHF'd models, low value
  2. **Inter-turn repetition within a conversation** (self-BLEU / n-gram recurrence across turns; "looping") — **this is the companion failure mode**, and it is invisible per-response
  3. **Cross-conversation / cross-character repetition** (same catchphrase for every character) — the corpus/cohort unit, ties into homogenization
- **Zipf coefficient per character over the whole conversation** is a cheap, judge-free drift/vocabulary-collapse signal.
- Caveat for our platform: this paper predates RLHF and instruction tuning. Modern models rarely produce the classic degenerate loop; they produce *semantic* repetition (restating the same sentiment in fresh words), which n-gram methods will MISS. We likely need **embedding-based** inter-turn similarity, not just n-gram self-BLEU. Holtzman gives us the framework and the human baselines, not a drop-in detector.
