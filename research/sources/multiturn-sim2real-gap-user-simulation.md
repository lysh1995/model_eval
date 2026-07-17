---
title: "Mind the Sim2Real Gap in User Simulation for Agentic Tasks"
url: https://arxiv.org/abs/2603.11245
authors: Xuhui Zhou, Weiwei Sun, Qianou Ma, Yiqing Xie, Jiarui Liu, Weihua Du, Sean Welleck, Yiming Yang, Graham Neubig, Sherry Tongshuang Wu, Maarten Sap
year: 2026
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Mind the Sim2Real Gap in User Simulation for Agentic Tasks

arXiv:2603.11245v1.

**Status: the empirical case AGAINST live LLM user simulators — and therefore, indirectly, part of the case FOR our replayed human-ish user turns.**

## Abstract / setup

Formalizes the **"Sim2Real gap"** by comparing **31 LLM simulators** against **451 real human participants** across **165 τ-bench tasks**. The best simulator achieved a **User-Sim Index (USI) of 76.0, "far below human scores of 92.9."**

## Methodology

Researchers **replaced τ-bench's LLM user simulator with real humans** role-playing customer service tasks. Measured:
- **Four behavioral dimensions (D1–D4):** communication style, information patterns, clarification behavior, error reaction
- **Two evaluative dimensions:** outcome calibration (ECE) and quality judgments across eight dimensions
- **USI metric:** composite 0–100 score aggregating all dimensions
- Alignment measured with **Sørensen–Dice coefficients** comparing behavioral features

## Behavioral gaps — the specific biases (all verbatim)

**Communication Style (D1):**
> "1.0% of GPT-4o turns are short vs. 29.0% for humans"
> "49.0% of GPT-4o turns are polite vs. 15.3% for humans"

LLM simulators exhibit "excessive cooperativeness, stylistically uniform."

**Information Patterns (D2):**
> "UserLM-8b includes nearly twice as many identifier-like tokens per turn (4.8 vs. 2.6)"

Simulators **front-load complete information; humans reveal incrementally.** (Note the direct tie-in to Laban et al.: front-loading is exactly the `Concat` condition, which is 95% of `Full` — i.e. a simulator that front-loads *hides* the multi-turn failure mode entirely.)

**Clarification (D3):**
> "GPT-4o expressing uncertainty in 14.6% of turns, which is twice the human rate (7.3%)"

**Error Reaction (D4):**
> "Simulators pivot strategy far more than humans (19.1% and 16.5% vs. 8.4%)"

Humans show "more accusatory behavior" while simulators "quietly pivot."

## Evaluation gap

**LLM evaluator bias:**
- LLM evaluators **inflated human-likeness ratings by "+1.11"** on quality scales
- Simultaneously conservative on task completion (**"Δ = −0.15"**)

**Binary reward orthogonality:**
> "70.6% of reward=0 interactions are actually judged as successful by humans"
> "33% of reward=1 interactions are judged as unsuccessful or only partially successful"

The binary reward was **"largely orthogonal to human-perceived quality."**

## Agent success-rate inflation — the headline risk

> "Most general-purpose LLM simulators yield higher agent success rates than the human baseline (63.6%), with top models reaching 77.8%."

> Simulators create an **"easy mode" that systematically inflates perceived agent competence.**

## Relevance to companion-eval-platform — this one cuts in our favor

- **The live-simulator alternative is badly broken.** Anyone who objects "replayed turns are off-policy, just use a live simulator" is proposing to trade a *known, bounded, characterizable* bias for a *large, measured, direction-known* one: +14pp inflated success, 49% vs 15% politeness, 1% vs 29% short turns.
- **Simulator uniformity is fatal specifically for OUR use case.** "Stylistically uniform" simulators would *manufacture* the homogenization we are trying to detect. If the user turns are all the same, the character responses converge, and we'd measure the simulator's collapse, not the model's.
- **The incremental-reveal finding is the strongest single argument for replay.** Humans reveal incrementally; simulators front-load. Laban et al. show front-loading (`Concat`) recovers 95% of single-turn performance — i.e. a front-loading simulator *erases the multi-turn penalty we exist to measure*. Our replayed turns, if originally produced by or against realistic human-like distribution, preserve incremental reveal. **Replay is off-policy but keeps the failure mode; live simulation is on-policy but destroys it.**
- Their USI/D1–D4 framework is a ready-made instrument for auditing our own dataset's user turns: we can score our replayed user turns on D1–D4 against human reference distributions and *quantify* how human-like our fixed turns are. That's a concrete, high-value work item.
