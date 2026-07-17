---
title: "Standardizing the Measurement of Text Diversity: A Tool and a Comparative Analysis of Scores"
url: https://arxiv.org/abs/2403.00553
html_url: https://arxiv.org/html/2403.00553v1
year: 2024
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# Which diversity score to actually use — with runtime numbers

The single most operationally useful source for our cheap-metrics tier. Compares **nine** diversity measures.

## The nine scores

1. **Self-BLEU** — "measures similarity between all text pairs in D using BLEU as the similarity score"
2. **Homogenization Score (ROUGE-L)** — pairwise ROUGE-L
3. **Homogenization Score (BERTScore)** — pairwise BERT embedding similarity
4. **Self-repetition Score** — 4-gram repetition ACROSS documents
5. **MATTR** (Moving Average Token-Type Ratio) — lexical diversity within segments
6. **N-gram Diversity Score (NGD)** — "ratio of the unique n-gram counts to all n-gram counts"
7. **HD-D** (Hypergeometric Distribution D) — lexical diversity
8. **Compression Ratio (CR)** — "ratio between the size of the compressed file to that of the original file"
9. **CR:POS** — compression applied to POS tag sequences

## Formulas (verbatim)

**Homogenization Score:**
```
hom(D) = 1/(|D|-1) Σ sim(d,d')
```

**Self-repetition Score:**
```
SRS(d) = log(Σ N_i + 1)
```
where N_i is the count of documents containing 4-gram i.

**N-gram Diversity:**
```
NGD(D) = Σ(n=1 to 4) [# unique n-grams / # n-grams]
```

**Compression Ratio:**
```
CR(D) = size of D⊕ / compressed size of D⊕
```

## Correlations between scores

- **Compression ratio** — "strong" correlation with most n-gram-based measures (it's a cheap proxy for all of them)
- **Self-BLEU and BERTScore** — only "weak correlations" with compression approaches
- **Self-repetition** — "moderate" correlation with other scores, therefore informative (adds independent signal)
- **BERTScore homogenization** — minimal variation across text sources
- Cross-dataset correlations range 0.654 to 0.991; Self-BLEU shows 0.991 consistency between datasets

## Recommendation — report these four

1. **Compression Ratio** — computationally efficient, captures redundancy
2. **CR:POS** — identifies syntactic repetition patterns *distinguishing human from machine text*
3. **Self-repetition** — long n-gram reuse, intuitive interpretation
4. **Self-BLEU** — weakly correlated with the others → provides an independent perspective

Explicitly **rejects** BERTScore homogenization: "There is no good justification to report it" — it fails to detect human-machine differences.

## Runtime (500 texts, CNN/DailyMail)

| Method | Cost |
|---|---|
| Compression-based | seconds to minutes |
| Self-repetition | "acceptable time" |
| Self-BLEU, BERTScore | **"prohibitively slow"** — est. 48–800 hours for 50k samples |

Self-BLEU is O(n²) in corpus size. At our scale, compression ratio is the only free lunch.

## THE CRITICAL CONSTRAINT

> All scores correlate significantly with text length (correlations **0.79–0.904** with word count). "scores are not meaningfully comparable" across varying text lengths.

**This is a trap for our platform.** If model A writes longer replies than model B, every diversity score will differ for reasons that have nothing to do with creativity. We MUST either (a) control response length in the harness, (b) truncate to a fixed token budget before scoring, or (c) report length alongside and regress it out. Otherwise our "creativity" leaderboard is a verbosity leaderboard.
