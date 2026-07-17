---
title: "Roleplay / persona-consistency benchmarks 2025-2026: RMTBench, MRBench, anonymous benchmarking, RPEval"
url: https://arxiv.org/abs/2507.20352
publisher: arXiv (multiple groups)
date: RMTBench v1 2025-07-27 / v2 2025-10-23 (EMNLP 2025 Findings); MRBench v1 2026-03-14; Anonymous benchmarking v1 2026-03-04 (SIGdial 2026); RPEval v1 2025-05-19
type: paper
accessed: 2026-07-16
topic: recent-news
---

# Roleplay & persona-consistency benchmarks — the 2025-2026 wave

Successors to CharacterEval / CharacterBench / SocialBench / RAIDEN / InCharacter. The through-line:
**the field moved from character-centric single-turn QA to user-centric, multi-turn, memory-aware,
and contamination-aware evaluation.**

---

## 1. RMTBench — the CharacterEval successor (EMNLP 2025 Findings)

- **arXiv 2507.20352**. **v1: 2025-07-27**; **v2 (latest): 2025-10-23**. cs.CL.
- **Published: ACL Anthology `2025.findings-emnlp.730`** — i.e. **EMNLP 2025 Findings**, peer-reviewed.
- Authors: Hao Xiang, Tianyi Tang, Yang Su, Bowen Yu, An Yang, Fei Huang, Yichang Zhang, Yaojie Lu,
  Hongyu Lin, Xianpei Han, Jingren Zhou, Junyang Lin, Le Sun.
  **Note the author list is substantially the Qwen/Alibaba team** (Bowen Yu, An Yang, Fei Huang,
  Jingren Zhou, Junyang Lin) + ISCAS. So this is *also* partly a lab-adjacent benchmark.
- **Scale: 80 diverse characters, 8,000+ dialogue rounds. Bilingual (English + Chinese).**
- Dataset: `huggingface.co/datasets/xiangh/RMTBENCH`.

**The core methodological shift — "user-centric" not "character-centric":**
> "existing benchmarks mostly adopt a **character-centric** approach"

RMTBench instead **constructs dialogues from explicit user motivations** rather than from character
descriptions. Named limitation of prior work (SocialBench, CharacterEval, RAIDEN): they "use
character-centric profiles to generate **static Q&A or single-turn evaluations**, neglecting
dynamic conversational aspects and the underlying user intentions."

Stated multi-turn phenomena targeted: **drift across topics, tracking of user preferences, and
testing of ethical boundaries.** Claimed contribution: "bridges the gap between academic evaluation
and practical deployment requirements."

**Why it matters:** this is the peer-reviewed articulation of the thing a companion platform cares
about — people don't talk to a companion to quiz it on its backstory (character-centric); they talk
to it because they *want something* (user-centric). Any benchmark built on "does the model know
what Sherlock would say" is measuring the wrong construct.

---

## 2. MRBench / MREval — memory-driven persona knowledge (2026-03-14)

- **arXiv 2603.19313**, **v1: 2026-03-14**. Authors: Kai Wang, Haoyang You, Yang Zhang, Zhongjie Wang.
- Title: *Memory-Driven Role-Playing: Evaluation and Enhancement of Persona Knowledge Utilization in LLMs*.
- Problem framing: models "frequently fail to **recall and accurately apply their designated persona
  knowledge without explicit cues**" over long open-ended dialogue.
- Framework inspired by **Stanislavski's acting theory**. Three artifacts:
  - **MREval** — evaluation system over **four abilities: Anchoring, Recalling, Bounding, Enacting**
  - **MRPrompt** — a prompting architecture
  - **MRBench** — a **bilingual (zh/en)** diagnostic benchmark across the four developmental stages
- **Verified finding: with MRPrompt, Qwen3-8B could match larger closed-source models
  (Qwen3-Max and GLM-4.7).** Tested across **12 LLMs**. Validates that "upstream memory gains
  directly enhance downstream response quality."

**Why it matters:** the **Anchoring / Recalling / Bounding / Enacting** decomposition is a
diagnostic ladder — it tells you *why* persona consistency failed, not just that it did. Most
persona benchmarks emit one opaque consistency score. **Bounding** (knowing what the character
does *not* know / would *not* do) is the failure mode companion products actually hit.
Also note: **an 8B model with the right prompting matched frontier models** — for a companion
platform this means persona consistency is substantially a *scaffolding* problem, not a
model-scale problem. That has direct cost implications.

---

## 3. Anonymous benchmarking — the contamination result (2026-03-04, SIGdial 2026)

- **arXiv 2603.03915**, **v1: 2026-03-04**. Authors: **Ji-Lun Peng, Yun-Nung Chen**.
- Title: *Rethinking Role-Playing Evaluation: Anonymous Benchmarking and A Systematic Study of
  Personality Effects*. **Venue: SIGdial 2026.**

**The finding that invalidates a lot of prior work:**
> models perform better when character names are revealed because they rely on **"their internal
> training memory of these characters rather than demonstrating role-playing capabilities."**
> When character identities were **anonymized, performance substantially declined** — "name exposure
> provides implicit cues that **mask a model's true capability**."

Second finding: **personality augmentation consistently improves** RPA performance in the anonymous
setting.

**Why it matters — this is the most important negative result for benchmark design here.**
Every roleplay benchmark built on **famous fictional characters** (CharacterEval, InCharacter,
Character Profiling, and most of the 2023-2024 lineage) is substantially **measuring memorized
trivia about Sherlock Holmes / Harry Potter, not roleplay ability**. A companion platform's
characters are **original** — nothing is memorized about them. **So public roleplay leaderboard
ranks systematically fail to transfer to original-character products, and will overestimate models
that memorized the canon.** Any companion eval must use **anonymized or original** characters. This
is a hard requirement, not a nicety.

---

## 4. RPEval (2025-05-19)

- **arXiv 2505.13157**, *Role-Playing Evaluation for Large Language Models*. v1 **2025-05-19**.
- Four dimensions: **emotional understanding, decision-making, moral alignment, in-character
  consistency**.
- Not fetched beyond the abs listing; treat details as low-confidence.

---

## 5. Also surfaced (NOT verified — listed only so they can be checked later)

These appeared in arXiv search listings. **I did not fetch their abs pages. Titles/IDs may be
imprecise; do not cite without verification.**

- **2605.17044** — *PersonaArena: Dynamic Simulation for Evaluating and Enhancing Persona-Level
  Role-Playing in LLMs*
- **2606.25632** — *Staying In Character: Perspective-Bounded Memory For Book-Based Role-Playing Agents*
- **2512.17270** — *Understanding Generalization in Role-Playing Models via Information Theory*
- **2507.03543** — *H2HTalk: Evaluating Large Language Models as Emotional Companion*
- **2606.23380** — *Affective AI Safety: The Missing Piece in LLM Safety*
- **2601.13188** — *Large Language Lovers: Lived Experiences of Negotiating Agency and Platform
  Control in AI Companionship*
- **PERSIST** — claimed to measure "personality stability across model sizes and conversation
  histories" (from a search summary; **no arXiv ID recovered; existence unverified**)

---

## Synthesis — what changed in roleplay eval since mid-2025

| Axis | 2024 / early-2025 state | 2025-2026 state |
|---|---|---|
| Turn structure | single-turn / static QA (CharacterEval, SocialBench) | **multi-turn, 100-turn sessions** (MiniMax), 8k rounds (RMTBench) |
| Framing | **character**-centric ("would Sherlock say this?") | **user**-centric (what does the user want?) — RMTBench |
| Characters | famous fictional | **anonymized / original required** — 2603.03915 |
| Consistency | one opaque score | **decomposed**: Anchoring/Recalling/Bounding/Enacting (MREval); Worlds/Stories/Preferences (MiniMax) |
| Ground truth | implicit "correct" response | **non-verifiable → detect misalignment** (MiniMax "Negative Evaluation") |
| Memory | not measured | **first-class** (MRBench, perspective-bounded memory) |
| Language | mostly zh or mostly en | **bilingual standard** (RMTBench, MRBench, MiniMax) |

## UNVERIFIED across this file

- All papers read at **abstract level only**. No PDFs read. No per-model score tables verified for
  RMTBench, MRBench, or 2603.03915.
- Whether RMTBench/MRBench leaderboards exist publicly with current (mid-2026) models on them.
  **Almost certainly they do not** — RMTBench's data predates the current model generation.
- The magnitude of the anonymization effect ("substantially declined" is the abstract's word; **no
  number verified**).
- Whether `xiangh/RMTBENCH` is the official RMTBench dataset (name matches first author Hao Xiang;
  not confirmed).
