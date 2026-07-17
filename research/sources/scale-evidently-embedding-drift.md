---
title: "5 methods to detect drift in ML embeddings"
url: https://www.evidentlyai.com/blog/embedding-drift-detection
org: Evidently AI
year: 2023
type: blog
accessed: 2026-07-16
topic: production-scale
---

# Embedding drift detection — 5 methods compared

Directly applicable to LLM output/prompt embedding monitoring.

## 1. Euclidean distance

- **How:** "average all embeddings in the 'current' and 'reference' data to get a single
  representative embedding for each dataset. Then, we measure the distance between the
  embeddings" (i.e. centroid shift)
- **Score range:** 0 to infinity
- **Threshold:** requires experimentation; absolute distances difficult to calibrate universally
- **PCA impact:** consistent results with/without dimensionality reduction
- **Performance:** less sensitive to subtle shifts in noisy datasets; inconsistent across
  embedding models (BERT vs FastText)
- **Speed:** fast without PCA; slows with PCA applied

## 2. Cosine distance (centroid shift)

- **Formula:** `Cosine distance = 1 - Cosine similarity`
- **Score range:** 0 to 2
- **Threshold:** thresholds start very low (**0.001+**) and lack intuitive interpretation
- **PCA impact:** "very inconsistent: likely because the angle between the vectors is not
  'preserved' during the transformation"
- **Performance:** fast computation but problematic with dimensionality reduction

## 3. Model-based drift detection (domain classifier) — RECOMMENDED DEFAULT

- **How:** "train a binary classification model to discriminate between data from reference
  and current distributions"
- **Score:** ROC AUC, range 0 to 1
- **Recommended threshold: 0.55 or higher**
- **Interpretation:** "Everything over 0.5 is better than random. 1 is an 'absolute drift'"
- **PCA impact:** consistent results with and without PCA
- **Performance:** "consistent behavior for different pre-trained embeddings" (BERT and
  FastText); reasonable computation speed; highly interpretable thresholds
- **Assessment:** authors recommend as **"good default"**

## 4. Share of drifted components

- **How:** treat embeddings as tabular; check drift per component
- **Per-component method:** Wasserstein distance with **0.1** threshold
- **Score range:** 0 to 1 (fraction of components drifting)
- **Threshold example: 20% of components drifting** triggers alert
- **Performance:** less effective on noisy datasets; consistent across embedding models;
  "fairly interpretable threshold"

## 5. Maximum Mean Discrepancy (MMD)

- **How:** "measures the distance between the means of the vectors. This multi-dimensional
  distance is calculated using a kernel function" (mean embeddings in RKHS)
- **Score range:** values above zero; **0** for identical distributions
- **Threshold:** "quite hard to set"; values as low as **0.001** when drift introduced
- **Statistical testing:** recommended for datasets **under 1000 objects**; direct threshold
  setting for larger datasets
- **PCA impact:** "slightly more sensitive when PCA is applied"
- **Performance:** consistent across embedding models; poor interpretability;
  **slowest computation** of all methods

## General findings

- **Best default:** model-based drift detection (domain classifier) — interpretable
  threshold (ROC AUC > 0.55), consistent behavior, reasonable speed
- **Sample size:** statistical hypothesis testing beneficial only for datasets
  **under 1000 objects**
- MMD's O(n^2) kernel computation makes it impractical at 50M/day without aggressive
  sampling — the domain classifier scales far better and gives a bounded, interpretable score.

## Note on MMD complexity

Naive MMD is **O(n^2)** in the batch size (pairwise kernel matrix). At any meaningful
batch size this must be subsampled (typical practice: 1k–10k vectors per window) or
replaced with a linear-time estimator.
