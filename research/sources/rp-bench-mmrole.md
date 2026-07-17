---
title: "MMRole: A Comprehensive Framework for Developing and Evaluating Multimodal Role-Playing Agents"
url: https://arxiv.org/abs/2408.04203
authors: Yanqi Dai, Huanran Hu, Lei Wang, Shengjie Jin, Xu Chen, Zhiwu Lu
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# MMRole (arXiv 2408.04203)

Submitted 8 Aug 2024 (v1); revised 17 Feb 2025 (v2). Renmin University of China (Gaoling School of AI). Code: https://github.com/YanqiDai/MMRole

Introduces the concept of **Multimodal Role-Playing Agents (MRPAs)**. Three artifacts: **MMRole-Data** (dataset), **MMRole-Eval** (evaluation framework with a trained reward model), **MMRole-Agent** (the first specialized MRPA).

## Abstract (VERBATIM)

> Recently, Role-Playing Agents (RPAs) have garnered increasing attention for their potential to deliver emotional value and facilitate sociological research. However, existing studies are primarily confined to the textual modality, unable to simulate humans' multimodal perceptual capabilities. To bridge this gap, we introduce the concept of Multimodal Role-Playing Agents (MRPAs), and propose a comprehensive framework, MMRole, for their development and evaluation, which comprises a personalized multimodal dataset and a robust evaluation approach. Specifically, we construct a large-scale, high-quality dataset, MMRole-Data, consisting of 85 characters, 11K images, and 14K single or multi-turn dialogues. Additionally, we present a robust evaluation approach, MMRole-Eval, encompassing eight metrics across three dimensions, where a reward model is designed to score MRPAs with the constructed ground-truth data for comparison. Moreover, we develop the first specialized MRPA, MMRole-Agent. Extensive evaluation results demonstrate the improved performance of MMRole-Agent and highlight the primary challenges in developing MRPAs, emphasizing the need for enhanced multimodal understanding and role-playing consistency.

## MMRole-Eval: eight metrics across three dimensions (VERBATIM)

Each metric is phrased as a question in the paper.

### Dimension 1 — Fundamental Conversational Skills

1. **Instruction Adherence (IA)**: "Do the responses accurately adhere to the task instruction"
2. **Fluency (Flu)**: "Are the responses grammatically correct and articulated smoothly?"
3. **Coherency (Coh)**: "Do the responses maintain a coherent thread of dialogue"

### Dimension 2 — Multimodal Understanding Abilities

4. **Image-Text Relevance (ITR)**: "Do the responses exhibit a close correlation with the visual content"
5. **Response Accuracy (RA)**: "Do the responses accurately answer the words of the human user"

### Dimension 3 — Role-Playing Qualities

6. **Personality Consistency (PC)**: "Do the responses accurately and deeply reflect the personality"
7. **Knowledge Consistency (KC)**: "Do the responses accurately reflect the knowledge of the character"
8. **Tone Consistency (TC)**: "Do the responses align with the typical speech patterns"

This 3-dimension decomposition is the most directly reusable part of MMRole for a companion platform: it cleanly separates *baseline conversational competence* from *grounding* from *character adherence*. Most text-only benchmarks conflate the first and third.

## Scoring methodology — reward model, relative/paired

MMRole-Eval's distinguishing move is **relative scoring against ground truth via a trained reward model**, not absolute LLM-judge scoring. Verbatim:

> conducts a brief qualitative assessment of the relative performance between the evaluated MRPA and the constructed ground-truth data for each metric, followed by assigning a quantitative score pair. The final score of the MRPA is the ratio of the two scores within the score pair.

Mechanics:
- For each metric, the reward model sees the evaluated MRPA's response **and** the ground-truth (GPT-4-constructed) response.
- It first emits a short **qualitative** comparison, then a **quantitative score pair** (score_MRPA, score_GT).
- Final metric score = **ratio** score_MRPA / score_GT.

The ratio formulation normalizes away per-sample difficulty — a score >1 means the MRPA beat the GPT-4 reference on that metric. The reward model is trained to distill GPT-4's comparative judgments, making evaluation cheap and reproducible without API calls.

## Reward-model correlation numbers

| Comparison | Overall MAE | Pearson |
|---|---|---|
| Reward model vs **GPT-4** (its training target) | 0.0738 | **0.8129** |
| Reward model vs **humans** | 0.1258 | **0.6502** |

**Read this carefully:** the reward model tracks GPT-4 (r = 0.8129) substantially better than it tracks humans (r = 0.6502). It is a faithful GPT-4 distillation, and inherits GPT-4's disagreements with human raters. No inter-annotator agreement (kappa/alpha) is reported.

## Dataset — MMRole-Data

- **85 characters** total: **72 in-distribution (training)** + **13 out-of-distribution (test)**
- **11,032 images** total; 10,975 in-distribution
- **14,346 dialogues** (single- **and** multi-turn)
- **85,750 training samples**; **294 test samples**
- Character types span three categories: fictional characters, historical/public figures, and hypothetical real-life personas
- Ground-truth dialogues synthesized by **GPT-4**

The **in-distribution vs out-of-distribution split by character** (not just by sample) is a design worth copying — it tests whether an agent generalizes role-playing *as a skill* versus memorizing the 72 training characters.

## Models evaluated

Ten models total.

- **Closed-source (4):** GPT-4 Turbo, Gemini, Claude 3 Opus, Qwen-VL-Max
- **Open-source (6):** LLaVA variants, Yi-VL, InternVL, Qwen-VL-Chat variants
- Plus **MMRole-Agent** (the paper's own fine-tune)

Headline finding: the primary challenges are **multimodal understanding** and **role-playing consistency** — i.e., open models do fine on Dimension 1 (fluency/coherency) and fail on Dimensions 2 and 3.

## Multilingual & multi-turn

- **Multi-turn: yes** — dataset explicitly contains "single or multi-turn dialogues."
- **Multilingual / Chinese: not a stated feature.** Authors are at Renmin University and Qwen-VL models are evaluated, but the paper does not claim or report a Chinese-language split. Treat as English-primary; no verified Chinese support.
- **Multimodal: yes** — the only one of the five sources here covering image grounding. Relevant if the companion platform has avatars, photo-sharing, or visual context.

## Limitations (VERBATIM)

> The training data for MMRole-Agent is primarily synthesized by GPT-4, which constrains its performance from surpassing GPT-4 itself.

## Criticisms / notes for platform design

- **Circular supervision.** Ground truth is GPT-4-generated; the reward model is trained on GPT-4 comparisons; the ceiling is therefore GPT-4 by construction — which the authors concede. The reward-model-vs-human Pearson of 0.6502 quantifies the leak: ~42% of variance in human judgment is unexplained.
- **Small test set.** 294 test samples across 13 OOD characters is thin for per-metric claims.
- **Ratio scoring has an edge case.** If the GPT-4 ground-truth response is itself poor on a metric, the denominator shrinks and the MRPA's ratio inflates. The paper does not discuss variance in the reference.
- **Reusable idea:** the trained-reward-model approach (vs. API judge) is the cheapest path to high-volume continuous eval, provided you accept it as a frozen snapshot of the teacher judge's preferences and periodically re-validate against humans.
