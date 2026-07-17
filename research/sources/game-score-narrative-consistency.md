---
title: "SCORE: Story Coherence and Retrieval Enhancement for AI Narratives"
url: https://arxiv.org/abs/2503.23512
authors: Qiang Yi, Yangfan He, Jianhui Wang, Xinyuan Song, Shiyao Qian, Miao Zhang, Li Sun, Tianyu Shi
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# SCORE: Story Coherence and Retrieval Enhancement for AI Narratives

Full text: https://arxiv.org/html/2503.23512v1. arXiv preprint (March 2025) — **no conference/journal venue**.

**Status: the closest published thing to the world-state auditor we want to build. Its central mechanism is worth stealing. Its numbers should not be cited — see the credibility section, which is the main reason this file exists.**

## Method

**Dynamic State Tracking** — the part worth taking:
- Monitors object/character states via **symbolic logic**.
- State space per item: **{active, lost, destroyed}**.
- "flags **continuity errors** when an item marked `lost` or `destroyed` reappears as `active` **without narrative justification**."
- State records maintained per episode using symbolic representations.

**Context-Aware Summarization:** hierarchical episode summaries capturing character actions `Ac(t)`, item interactions `Ii(t)`, relationships, emotional state changes.

**Hybrid Retrieval:** TF-IDF keyword relevance + cosine-similarity embeddings (FAISS, OpenAI embeddings), with a sentiment score `σ(e)` ∈ [0,1] in the retrieval kernel; "top N episodes with highest `S(ec,ep)` scores are retrieved."

## Taxonomy of inconsistency types

| Type | Definition |
|---|---|
| **Item Status Consistency** | object state transitions violating logical constraints |
| **Character Consistency** | actions contradicting established personality traits |
| **Plot Progression** | events lacking causal justification |
| **Emotional Consistency** | sentiment/tone shifts without explanation |
| **Continuity** | unexplained reappearances or state reversals |

⭐ **This taxonomy is the useful output of the paper**, and note the ordering: Item Status is nearly free and near-deterministic; Emotional Consistency is pure aesthetics (α=0.3 territory). **The five "consistency" types are not one dimension and must not be averaged** — they span our entire cost/reliability range. Lumping them into a "coherence" score is exactly the error note 11 warns against.

## Reported numbers

**Table 2 (GPT-4 baseline → +SCORE):**

| Metric | Baseline | SCORE | Δ |
|---|---|---|---|
| Consistency | 83.21% | 85.61% | ↑2.4% |
| Coherence | 84.32% | 86.9% | ↑2.58% |
| **Item Status** | **0%** | **98%** | ↑98% |
| Complex QA | 82.34% | 89.45% | ↑7.11% |

**Ablation (Table 3):** −Dynamic Tracking: −17.6% consistency, −37.1% item accuracy. −Context Summary: −22.5% coherence. −Hybrid Retrieval: −10.9% complex QA.

**Robustness (Table 4):** under combined noise, metrics degrade 10.6–13.3%, all stay >75%.

**Dataset:** 5,000 episodes from **1,000 GPT-generated stories** (Sci-Fi/Drama/Fantasy/Comedy, 250 each); 10–15 episodes/story (mean 12); 50% GPT-3.5 + 50% GPT-4; 15 prompt templates/genre; 30% multi-character (>4), 20% non-linear timelines, 50% symbolic objects. Cross-validation on NarrativeQA (1,567), BookCorpus (11,038), WP-STORIES.

**IAA:** "Fleiss' κ of **0.78**" — but for *quality-control filtering* across three annotators (excluding stories with <80% genre alignment), **not** for the consistency labels themselves.

## ⚠️ Credibility assessment — read before citing

**Do not cite this paper's numbers.** Multiple independent problems:

1. **The abstract contradicts the paper's own tables.** Abstract claims "**23.6% higher coherence**"; Table 2 reports coherence 84.32 → 86.9 = **+2.58%**. An order of magnitude apart. Same for "41.8% fewer hallucinations" — unlocatable in the tables.
2. **Benchmarks that appear to exist only in this paper.** "NCI-2.0 benchmark" and the "EASM metric" (89.7% emotional consistency) have no independent provenance found.
3. **Item Status baseline = 0%.** A GPT-4 baseline scoring *exactly zero* on an item-tracking metric is not a measurement; it's a metric defined so the baseline can't score. The 0→98% "improvement" is an artifact of the metric's construction.
4. **No precision/recall/F1 for inconsistency detection anywhere** — the actual thing the system does is never directly evaluated. Same sin as Zep: the detector is only assessed through downstream proxies.
5. **The corpus is GPT-generated stories.** Consistency is measured on synthetic text with synthetic "errors," which is a much easier and differently-distributed problem than real dialogue. Cross-validation sets are QA/corpora, not consistency benchmarks.
6. **No error rate reported**, self-acknowledged: "Reliance on retrieval accuracy for key-item continuity."

## Relevance to companion-eval-platform

1. **⭐ Steal the mechanism, not the results.** A typed item-state machine `{active, lost, destroyed}` with a flag on illegal transitions is *exactly* the Lane-1 world-state check we want, and it's the most concrete instantiation in the literature. The finite state space is what makes it cheap and checkable.
2. **⭐ Their taxonomy stratifies our cost tiers for us.** Item Status (deterministic, ~free) → Continuity (near-deterministic given a record) → Plot Progression (LLM) → Character Consistency (LLM, α≈0.3) → Emotional Consistency (hopeless). **Build down this list in order and stop where reliability dies.** This ordering *is* our dimension roadmap and it fell out of a bad paper.
3. **"Without narrative justification" is the whole problem, hidden in a subordinate clause.** SCORE's item checker flags `lost → active` transitions *unless justified*. Deciding "was this justified?" is an unbounded LLM judgment — the exact place the objectivity leaks out. **Every world-state auditor has this escape hatch, and its error rate lives entirely inside it.** In roleplay the equivalent is "the character found the knife again" — legitimate if the scene provided for it, a canon violation if not. **Note 13's error-rate estimate must be an estimate of *this* clause, not of the state machine.**
4. **The negative result is the useful one:** two independent systems (Zep, SCORE) built LLM-based contradiction detection and **neither measured its precision/recall.** That is either an oversight repeated twice or a tell that the number is unflattering. **If we measure it, we are publishing something the field has twice declined to.**
