---
title: "RULER: What's the Real Context Size of Your Long-Context Language Models?"
url: https://arxiv.org/abs/2404.06654
authors: Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg (NVIDIA)
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# RULER

Submitted 2024-04-09; final revision 2024-08-06. Published at COLM 2024. Full text read from https://arxiv.org/html/2404.06654v3

## Core framing — why NIAH is inadequate (VERBATIM)

> "The needle-in-a-haystack (NIAH) test, which examines the ability to retrieve a piece of information (the 'needle') from long distractor texts (the 'haystack'), has been widely adopted to evaluate long-context language models. However, this simple retrieval-based test is indicative of only a superficial form of long-context understanding."

> "Despite achieving nearly perfect accuracy in the vanilla NIAH test, almost all models exhibit large performance drops as the context length increases."

The paper argues NIAH reveals "merely the retrieval capability, failing to gauge other forms of long-context understanding."

> "While these models all claim context sizes of 32K tokens or greater, only half of them can maintain satisfactory performance at the length of 32K."

**This is the single most citable NIAH critique in the literature: models saturate vanilla NIAH (~100%) while collapsing on anything harder at the same context length. Vanilla NIAH has near-zero discriminative power.**

## Task definitions (13 tasks, 4 categories)

RULER generates synthetic examples with **configurable sequence length and task complexity**, so it is not contaminated by parametric knowledge (unlike real-document benchmarks).

### 1. Retrieval (NIAH variants)
- **Single NIAH (S-NIAH):** "a single 'needle' needs to be retrieved from the 'haystack'". Key-value pairs where query/key/value are words, numbers, or UUIDs; haystack is noise sentences or essays.
- **Multi-keys NIAH (MK-NIAH):** Multiple needles inserted; only one requires retrieval, the others serve as **hard distractors**.
- **Multi-values NIAH (MV-NIAH):** "Multiple 'needles' sharing the same key are inserted into the 'haystack'. All values associated with the same key need to be retrieved."
- **Multi-queries NIAH (MQ-NIAH):** "Multiple 'needles' are inserted into the 'haystack'. All 'needles' with distinct keys need to be retrieved."

### 2. Multi-hop Tracing
- **Variable Tracking (VT):** Chains of variable assignments (X2=X1, X3=X2, ...) are scattered through the context; the model must return all variable names pointing to the same value. Tests "track[ing] relevant co-occurrence patterns and drawing skipped connections within long input". **This is the closest synthetic analogue to tracking an evolving fact across a conversation.**

### 3. Aggregation
- **Common Words Extraction (CWE):** Identify top-K common words. Common words appear at fixed frequency; uncommon words scale with context length.
- **Frequent Words Extraction (FWE):** Return the 3 most frequent words from text sampled from a Zeta distribution, where "the frequency of the k-th ranked word is k^-a * N / zeta(a)".

### 4. Question Answering
- **QA:** "Insert the golden paragraphs (i.e., the paragraphs that contain answers) into paragraphs randomly sampled from the same dataset" — i.e. NIAH with realistic needles + realistic distractors.

## "Effective context length" — exact definition

> "We use the performance of Llama2-7b model at the 4K context length as the threshold."

Baseline threshold score: **85.6%** average accuracy across the 13 tasks.
**Effective length = the maximum sequence length at which the model still exceeds 85.6%.**

## Table 3 — main results (EXACT)

| Model | Claimed | Effective | 4K | 8K | 16K | 32K | 64K | 128K | Avg. | wAvg.(inc) | wAvg.(dec) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini-1.5-Pro | 1M | >128K | 96.7 | 95.8 | 96.0 | 95.9 | 95.9 | 94.4 | 95.8 | 95.5 (1st) | 96.1 (1st) |
| GPT-4 | 128K | 64K | 96.6 | 96.3 | 95.2 | 93.2 | 87.0 | 81.2 | 91.6 | 89.0 (2nd) | 94.1 (2nd) |
| Llama3.1 (70B) | 128K | 64K | 96.5 | 95.8 | 95.4 | 94.8 | 88.4 | 66.6 | 89.6 | 85.5 (4th) | 93.7 (3rd) |
| Qwen2 (72B) | 128K | 32K | 96.9 | 96.1 | 94.9 | 94.1 | 79.8 | 53.7 | 85.9 | 79.6 (9th) | 92.3 (4th) |
| Command-R-plus (104B) | 128K | 32K | 95.6 | 95.2 | 94.2 | 92.0 | 84.3 | 63.1 | 87.4 | 82.7 (7th) | 92.1 (5th) |
| GLM4 (9B) | 1M | 64K | 94.7 | 92.8 | 92.1 | 89.9 | 86.7 | 83.1 | 89.9 | 88.0 (3rd) | 91.7 (6th) |
| Llama3.1 (8B) | 128K | 32K | 95.5 | 93.8 | 91.6 | 87.4 | 84.7 | 77.0 | 88.3 | 85.4 (5th) | 91.3 (7th) |
| GradientAI/Llama3 (70B) | 1M | 16K | 95.1 | 94.4 | 90.8 | 85.4 | 80.9 | 72.1 | 86.5 | 82.6 (8th) | 90.3 (8th) |
| Mixtral-8x22B (39B/141B) | 64K | 32K | 95.6 | 94.9 | 93.4 | 90.9 | 84.7 | 31.7 | 81.9 | 73.5 (11th) | 90.3 (9th) |
| Yi (34B) | 200K | 32K | 93.3 | 92.2 | 91.3 | 87.5 | 83.2 | 77.3 | 87.5 | 84.8 (6th) | 90.1 (10th) |
| Phi3-medium (14B) | 128K | 32K | 93.3 | 93.2 | 91.1 | 86.8 | 78.6 | 46.1 | 81.5 | 74.8 (10th) | 88.3 (11th) |
| Mistral-v0.2 (7B) | 32K | 16K | 93.6 | 91.2 | 87.2 | 75.4 | 49.0 | 13.8 | 68.4 | 55.6 (13th) | 81.2 (12th) |
| LWM (7B) | 1M | <4K | 82.3 | 78.4 | 73.7 | 69.1 | 68.1 | 65.0 | 72.8 | 69.9 (12th) | 75.7 (13th) |
| DBRX (36B/132B) | 32K | 8K | 95.1 | 93.8 | 83.6 | 63.1 | 2.4 | 0.0 | 56.3 | 38.0 (14th) | 74.7 (14th) |
| Together (7B) | 32K | 4K | 88.2 | 81.1 | 69.4 | 63.0 | 0.0 | 0.0 | 50.3 | 33.8 (15th) | 66.7 (15th) |
| LongChat (7B) | 32K | <4K | 84.7 | 79.9 | 70.8 | 59.3 | 0.0 | 0.0 | 49.1 | 33.1 (16th) | 65.2 (16th) |
| LongAlpaca (13B) | 32K | <4K | 60.6 | 57.0 | 56.6 | 43.6 | 0.0 | 0.0 | 36.3 | 24.7 (17th) | 47.9 (17th) |

### Most damning gaps (claimed vs effective)
- **LWM (7B): claims 1M, effective <4K** — a 250x+ overstatement.
- **LongChat (7B) / LongAlpaca (13B): claim 32K, effective <4K.**
- **GradientAI/Llama3 (70B): claims 1M, effective 16K** (62x).
- **Yi (34B): claims 200K, effective 32K** (6x).
- **Mixtral-8x22B: claims 64K, holds 90.9 at 32K but collapses to 31.7 at 128K.**
- **DBRX: 95.1 at 4K → 2.4 at 64K → 0.0 at 128K.** Total collapse.
- Even **GPT-4**, the best non-Gemini model: 96.6 at 4K → 81.2 at 128K; effective length **64K vs 128K claimed** (2x overstatement).

### Note on the weighted averages
`wAvg.(inc)` weights longer sequences more heavily (increasing weight); `wAvg.(dec)` weights shorter sequences more. The rank swings between them are large — e.g. Qwen2 (72B) is 9th by wAvg.(inc) but 4th by wAvg.(dec) — showing how sensitive "which model is best at long context" is to how you weight length.

## Relevance to companion / conversational memory eval

1. **The headline transferable claim:** near-perfect vanilla NIAH is compatible with severe failure on aggregation, multi-hop, and distractor-heavy retrieval at the *same* context length. Passing a needle test says almost nothing about holding a conversation.
2. **MK-NIAH (hard distractors) is the relevant analogue for companions.** A long roleplay conversation is full of *near-miss* facts — the user mentioned three different pets, changed their job twice. That is MK-NIAH, not S-NIAH, and it is exactly where models degrade.
3. **MV-NIAH / MQ-NIAH map to "recall everything the user said about X"** — a multi-value retrieval, which is far harder than single-needle.
4. **VT maps to state tracking across a conversation** (a fact that gets updated/overwritten in later turns).
5. **CAVEAT / VALIDITY GAP:** RULER is entirely **synthetic and document-shaped**. Needles are UUIDs and word lists in essay haystacks. It has **no dialogue structure, no turn boundaries, no speaker attribution, no emotional or relational content, and no notion of a fact being *superseded* by a later turn.** RULER measures the ceiling of the substrate, not conversational memory. It tells us what a model *cannot* do; it cannot tell us that a model *can* be a good companion.
6. The "effective context length" methodology — **pick a competence threshold, then report the max length at which the model clears it** — is directly borrowable. A companion-eval analogue: define an acceptable persona-consistency/recall score, then report "effective conversation length" in turns.
