---
title: "Static Vs. Agentic Game Master AI for Facilitating Solo Role-Playing Experiences"
url: https://arxiv.org/abs/2502.19519
authors: Nima Ahmadzadeh Chaharlang, et al.
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Static vs. Agentic Game Master AI (2025)

**arXiv:** 2502.19519 (HTML v2: https://arxiv.org/html/2502.19519v2)

The most recent GM-evaluation study found (2025). System: **ChatRPG**. Compares a **static prompt-engineered GM (v1)** against an **agentic multi-agent GM (v2)**. Methodologically this is a **user-experience study**, and it is a useful example of the *opposite* of what our platform wants — all subjective, no state verification, no IAA.

> ⚠️ **Provenance note:** figures below come from the arXiv HTML v2 rendering. I did not independently re-extract this one from the PDF (unlike FIREBALL/CRD3/CALYPSO/Story Shaping/Skill Check, which were verified against primary PDF text). Treat the exact t/p values as needing a spot-check before external citation; the design and direction of results are consistent across sources.

## 1. Study design

**Counterbalanced within-subjects:** participants played **both** ChatRPG v1 and v2, with surveys and interviews after each version.

**Participants: N = 12** (11 male, 1 female; ages 21–30, **M = 26**). Ten reported playing **5+ hours weekly** of offline tabletop games; all claimed **6+ hours weekly** video game engagement. (A prior **pilot study had 8 participants** on v1.)

## 2. Conditions

- **Static GM (v1)**: simplified prompt engineering with **three system prompts (Do, Say, Attack)**
- **Agentic GM (v2)**: **multi-agent ReAct framework** with **Narrator** and **Archivist** agents

The **Archivist** agent is the interesting architectural piece — a dedicated agent for maintaining/retrieving game state, i.e. an explicit structural answer to world-state amnesia.

## 3. Measures

**Player Experience Inventory (PXI)** constructs: Ease of control, Goals and rules, Progress feedback, Meaning, Curiosity, Mastery, Immersion, Autonomy.

**Custom survey questions:** Story interestingness, Story coherence, Story adaptation, NPC engagement, Likelihood to replay, Overall satisfaction.

All on **Likert-type scales** (PXI uses a −3…+3 scale, consistent with the reported means below).

## 4. Results — paired-sample t-tests (α = 0.05)

| Construct | v1 Mean | v2 Mean | t | df | p | Sig. |
|---|---|---|---|---|---|---|
| Ease of control | 2.08 | 2.81 | -3.026 | 11 | 0.012 | **Yes** |
| Goals and rules | 1.35 | 2.39 | -2.786 | 11 | 0.018 | **Yes** |
| Progress feedback | 0.89 | 2.00 | -1.872 | 11 | 0.088 | No |
| Meaning | 1.36 | 1.97 | -1.677 | 11 | 0.122 | No |
| Curiosity | 1.83 | 2.57 | -2.236 | 11 | 0.047 | **Yes** |
| Mastery | 0.68 | 2.33 | -3.683 | 11 | 0.004 | **Yes** |
| Immersion | 1.64 | 2.42 | -2.420 | 11 | 0.034 | **Yes** |
| Autonomy | 2.17 | 2.67 | -1.384 | 11 | 0.194 | No |
| Story interesting | 1.17 | 2.33 | -2.755 | 11 | 0.0187 | **Yes** |
| **Coherent story** | **1.00** | **2.25** | **-2.322** | 11 | **0.040** | **Yes** |
| Story adapted | 1.42 | 2.27 | -1.449 | 11 | 0.175 | No |
| Engaging NPCs | 1.50 | 1.92 | -1.100 | 11 | 0.295 | No |
| Likely to play again | 1.58 | 2.50 | -2.2 | 11 | 0.050 | **Yes** |
| Satisfied with game | 1.08 | 2.17 | -2.238 | 11 | 0.0468 | **Yes** |

**9 of 14 constructs significant, all favoring v2 (agentic).**

**Forced-choice preference:** v2 preferred across **all** dimensions measured (Response Quality, Flexibility, Complexity/Depth, Realism, Flow, Perceived Intelligence, Control/Autonomy, Story Engagement, Overall Enjoyment).

**Qualitative:** thematic analysis → four themes: "Game Master Flexibility Dynamics," "Complex Realism and Flow," "Autonomous Intelligence Perception," "Narrative Satisfaction."

**Objective/countable metrics — essentially absent.** The only one: **task completion rates** — all 8 pilot participants (v1) and all 12 comparative-study participants completed assigned game tasks successfully. **100% vs 100% — zero discriminative power** (same failure as Story Shaping's win rate).

## 5. IAA status

**Not reported.** Thematic analysis has no stated second coder or agreement statistic.

## 6. Methodological problems (relevant to us)

- **N = 12, df = 11.** Underpowered. Several "significant" results sit right at the boundary (p = 0.050, 0.047, 0.0468, 0.040).
- **14 constructs tested with no multiple-comparisons correction.** At α = 0.05 across 14 tests, ~0.7 false positives expected by chance; **a Bonferroni correction (α = 0.0036) would leave only Mastery (0.004) and arguably Ease of control (0.012) standing.** The "9 of 14 significant" headline does not survive correction.
- **Within-subjects with both versions played** → strong demand characteristics; v2 was the authors' new system, and participants could likely tell which was which.
- **11/12 male, all heavy gamers, ages 21–30** — narrow sample.
- **No state-consistency verification whatsoever.** "Coherent story" (1.00 → 2.25) is a *self-reported Likert item*, despite coherence being exactly the property that Skill Check shows is objectively unit-testable and FIREBALL shows is checkable against structured state.

## Relevance to companion-eval-platform

1. **This is a clean illustration of the problem our platform exists to fix.** The paper's central claim — the agentic GM produces a more **coherent** story — rests on a 12-person Likert item (1.00 → 2.25, p = 0.040) with **no agreement statistic and no correction for 14 comparisons**. Coherence is *exactly* the dimension that Skill Check operationalizes as pass/fail unit tests and that FIREBALL grounds in structured state. The same claim could have been made verifiably and was not. **Use this as the canonical "before" example in our positioning.**
2. **The Archivist agent is architecturally important to us.** A dedicated state-tracking agent is the current best structural answer to world-state amnesia — and it also **creates the artifact our metrics need**: if the Archivist maintains an explicit state record, then contradictions become checkable against it, exactly like Avrae state in FIREBALL. **Architectures that externalize state are architectures we can objectively evaluate.** This is a design-influences-measurability argument worth making explicitly.
3. **Second independent case of a countable metric with zero discriminative range:** task completion 100% (v1) vs 100% (v2). Same pathology as Story Shaping's identical win rates. Reinforces the screening rule: **a countable dimension must also demonstrate variance across systems we believe differ**, or it is decoration.
4. **Useful as evidence that the field's 2025 state of the art is still all-subjective.** Despite FIREBALL (2023) demonstrating structured-state evaluation and Skill Check (2023) demonstrating unit tests, this 2025 paper evaluates a GM entirely with PXI Likert scales and thematic analysis. **The objective-evaluation gap for GM/roleplay systems is still open as of 2025** — that is the market/scientific opening for the platform.
5. **PXI is a real, validated instrument** and its construct list (Ease of control, Goals and rules, Progress feedback, Meaning, Curiosity, Mastery, Immersion, Autonomy) is a reasonable menu **if** we need a subjective battery for convergent validity against our objective dimensions. Worth noting PXI has published reliability data, unlike ad-hoc rubrics — if we must have subjective dimensions, borrowing a validated instrument is better than inventing scales.
6. **Sixth consecutive paper with no IAA.** Across this entire batch only Callison-Burch et al. (2022) reports agreement.
