---
title: "Naming unrelated words predicts creativity"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8237676/
authors: Jay A. Olson, Johnny Nahas, Denis Chmoulevitch, Simon J. Cropper, Margaret E. Webb
year: 2021
venue: PNAS
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# Divergent Association Task (DAT)

The cleanest existing example of a **fully computable, model-free creativity score with published human validation**. Worth studying as a template even though the task itself doesn't transfer directly to roleplay.

## Task instructions (verbatim)

Participants "generate 10 unrelated nouns" with constraints:
- "Use only single words"
- "Use only nouns (e.g., things, objects, concepts)"
- "Avoid proper nouns (e.g., no specific people or places)"
- "Avoid specialized vocabulary (e.g., no technical terms)"
- "Think of the words on your own (e.g., do not just look at objects in your surroundings)"
- "You will have 4 min to complete this task"

## Score formula (verbatim)

> "we compute the semantic distance (i.e., cosine distance) between all 21 possible pairs of the seven words, take the average, and then multiply it by 100."

- Only the **first seven valid words** of the ten are used (robustness to invalid entries).
- Embeddings: **GloVe**, pretrained on Common Crawl.
- Theoretical range 0–200; practical range typically **65–90**.

## Validation evidence

**Study 1A (manually screened, n=57):**
- vs Alternative Uses Task *flexibility*: r(55) = 0.51, P < 0.001
- vs Alternative Uses Task *originality*: r(55) = 0.50, P < 0.001
- vs Bridge-the-Associative-Gap *appropriateness*: r(54) = 0.34, P = 0.006

**Study 1B (full dataset, n=285):**
- vs AUT flexibility: r(223) = 0.35, P < 0.001
- vs AUT originality: r(223) = 0.32, P < 0.001
- vs BAG appropriateness: r(203) = 0.23, P < 0.001

**Test-retest reliability (Study 1C, n=50, 2-week interval):** r(48) = **0.73** [0.57, 0.84], P < 0.001

**Study 2:** 8,572 participants, 98 countries.

## Lessons for our platform

1. Even a *gold-standard* automated divergent-thinking measure only reaches **r ≈ 0.3–0.5** against other creativity measures. That is the realistic ceiling for any cheap automatic creativity proxy. Do not expect r > 0.6.
2. **Test-retest r = 0.73 > its validity correlations.** A metric can be very stable (good for regression detection) while only moderately valid (bad for absolute claims). This is exactly the tradeoff our platform needs: *stability for regression detection is a separate property from validity*.
3. Design pattern worth stealing: fixed truncation (first 7 valid), all-pairs mean cosine distance, ×100 scaling. Deterministic, cheap, no model call, no judge.
