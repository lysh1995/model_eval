---
title: "Skill Check: Some Considerations on the Evaluation of Gamemastering Models for Role-playing Games"
url: https://arxiv.org/abs/2309.13702
authors: Santiago Gómez-Rosero, Jose María Alonso-Moral, et al. (GALA 2023)
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Skill Check: Evaluation of Gamemastering Models for RPGs

**arXiv:** 2309.13702 | Published: Games and Learning Alliance (GALA) 2023, Springer LNCS, doi 10.1007/978-3-031-49065-1_27

This is the closest thing in the literature to a **GM evaluation rubric**, and crucially it is built as **objective pass/fail unit tests**, not Likert ratings. Directly relevant to our objective-dimension preference.

> ⚠️ **Provenance note.** An automated extraction of the arXiv PDF for this paper produced fabricated content (claiming "50+ sessions", GPT-3.5 and rule-based baselines, 1–5 rubrics, means of 3.8/5.0, and **Fleiss' kappa = 0.73**). **None of that exists in the paper.** All figures below are from the ar5iv HTML rendering and are consistent with the published abstract. Do not propagate the fabricated numbers if they appear elsewhere in our notes.

## 1. Framing

The paper identifies the core GM modeling challenges as: **creating and managing a fictional world, tracking the game state, and understanding the players' actions.** It proposes three test categories and runs preliminary experiments on three out-of-the-box chat models as GMs.

## 2. The three test categories — WHAT EACH CHECKS

### (1) GM-P-GM Pattern
Checks "the model's ability to judge the **feasibility of a player's action**" — i.e. whether a proposed action is possible given the narrative context, and whether the model explains the contradiction when it is not. Named for the Game Master → Player → Game Master turn pattern.

### (2) Item Tracking
Checks whether the system **maintains accurate inventory state** when players add/remove objects from backpacks or locations across dialogue turns.

### (3) Map Design
Checks whether **accessible locations remain coherent** when players navigate between areas and return to an original location.

All three are **world-state consistency** tests. Each is checkable against a record of what the model itself previously asserted.

## 3. Models tested

- **ChatGPT** (Mar 14 Version)
- **Google Bard** (experimental version, accessed July 17, 2023)
- **OpenAssistant** / `oasst-sft-6-llama-30b` (accessed July 14, 2023)

## 4. Protocol

**Five unit tests per category, in both Spanish and English → 90 total tests** (3 categories × 5 tests × 2 languages × 3 models). **The authors manually examined outputs and determined pass/fail results.**

## 5. Results — pass/fail counts

| Category | OA [ES] | Bard [ES] | ChatGPT [ES] | OA [EN] | Bard [EN] | ChatGPT [EN] |
|---|---|---|---|---|---|---|
| GM-P-GM | 0/5 | 1/5 | 1/5 | 1/5 | 1/5 | 0/5 |
| Item Tracking | 0/5 | 0/5 | 2/5 | 0/5 | 3/5 | 1/5 |
| Map Design | 0/5 | 3/5 | 3/5 | 0/5 | 2/5 | 3/5 |
| **Total** | **0/15** | **4/15** | **6/15** | **1/15** | **6/15** | **4/15** |

**Best score across all conditions: 6/15 (40%).** OpenAssistant scored 0/15 [ES] and 1/15 [EN] — it "was unable to maintain the GM role during most of the tests."

**GM-P-GM (action feasibility) is the hardest category: max 1/5 for every model in every language.** No system exceeded 20% on judging whether a player's action is even possible.

Qualitative finding from the abstract: ChatGPT and Bard "can provide a satisfying gaming experience" but **struggle with commonsense reasoning** and **exhibit flaws in updating the world state after player actions.**

## 6. Evaluation type and IAA

**Quantitative pass/fail scoring** with qualitative observations. **No rubrics, no inter-annotator agreement scores, and no numeric confidence measures are reported.** Pass/fail was adjudicated by the authors themselves (n unclear, no second rater, no agreement statistic).

## Relevance to companion-eval-platform

1. **Direct precedent for the design we want: a GM/world-consistency benchmark built entirely from binary unit tests, not Likert scales.** The paper never asks "how good was this narration?" — it asks "did the sword the player dropped three turns ago reappear?" That is countable, verifiable, and adjudicable against the transcript.
2. **The three categories map cleanly onto companion-eval dimensions:**
   - *Item Tracking* → **entity/commitment persistence** (does the companion remember a fact it asserted and not contradict it?)
   - *Map Design* → **world/context coherence on revisit** (return to a previously established topic/state and check consistency)
   - *GM-P-GM* → **feasibility/refusal grounding** (does the system correctly reject actions incompatible with established state, and explain why?)
3. **The headroom is enormous and that is a feature.** Best total 6/15 (40%), and 1/5 max on action feasibility. Objective consistency tests are *not* saturated by frontier-adjacent models — an objective dimension only earns its place if it discriminates, and this one does. (Caveat: 2023-era models; needs re-running on current models to confirm headroom persists.)
4. **Methodological caution — this is a small, weak study.** n=5 tests per cell means each cell's resolution is 20%, differences of 1–2 tests are noise, authors self-adjudicated with no second rater, and no IAA is reported. **Cite it for the test-design taxonomy, not for the model rankings.** Our version needs many more items per dimension and a genuine second adjudicator — but note that even a *binary, record-checkable* judgment deserves an agreement statistic, and this paper (like FIREBALL) doesn't provide one.
5. **Reinforces the central pattern across this whole literature:** every GM paper that reports objective metrics reports *state-consistency* metrics, and every paper that reports aesthetic metrics either finds them flat/inverted (FIREBALL) or measurably less reliable than binary ones (Callison-Burch et al., τ=0.46 vs κ=0.6). Nobody has made an aesthetic GM metric work.
