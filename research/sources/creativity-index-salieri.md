---
title: "AI as Humanity's Salieri: Quantifying Linguistic Creativity of Language Models via Systematic Attribution of Machine Text against Web Text"
url: https://arxiv.org/abs/2410.04265
html_url: https://arxiv.org/html/2410.04265v1
authors: Ximing Lu et al.
year: 2024
type: paper
code: https://github.com/GXimingLu/creativity_index
accessed: 2026-07-16
topic: creativity-measurement
---

# Creativity Index / DJ Search

## Definition (verbatim)

**L-uniqueness**: the proportion of words in text **x** where none of the n-grams (n ≥ L) containing that word appear in reference corpus C.

> uniq(x,L) = ∑[k=1 to ||x||] 𝟙{f(x[i:i+n],C)=0 ∀i∈(k-n,k], n≥L} / ||x||

**Creativity Index** = ∑[n≥L] uniq(x,n) — uniqueness aggregated across varying n-gram lengths.

Intuition: quantify creativity by how hard it is to *reconstruct* a text from existing web snippets. Low reconstructability = high creativity.

## DJ Search algorithm

> "DJ Search, a dynamic programming algorithm"

Two-pointer method reducing complexity from quadratic to linear:
- Identifies the longest n-gram at each position matching corpus C
- Reuses prior computations: if f(x[i:i+n],C)=1 then f(x[i+1:i+n],C)=1
- Limits function evaluations to 2||x|| calls

## Headline numbers

- "The Creativity Index of professional human authors is on average **66.2% higher** than that of LLMs."
- By domain: **52.2%** for novels, **31.1%** for poetry, **115.3%** for speeches (verbatim matches only).
- **"Alignment reduces the Creativity Index of LLMs by an average of 30.1%"** at the verbatim level. → RLHF measurably destroys linguistic novelty. Direct evidence for the homogenization concern.
- As a machine-text detector: beats DetectGPT (strongest zero-shot baseline) "by a significant margin of 30.2%"; outperforms supervised Ghostbuster in 5 of 6 domains, AUROC +3.5% on average.

## Validation gap

**Human creativity judgments validation is not explicitly addressed with formal metrics** in this paper. The Creativity Index is validated as a *detector* and as a *human-vs-LLM discriminator*, NOT as a correlate of human creativity ratings. See `creativity-death-of-novelty.md` — when someone did validate it against expert judgment, precision was ~9%.

## Practical caveat

Requires a reference corpus / web index to search against. For roleplay dialogue this is expensive and the "reference corpus" is ill-defined. A tractable substitute for us: measure overlap against **our own corpus of prior responses** rather than the web — that turns it into a homogenization/self-repetition measure, which is what we actually care about.
