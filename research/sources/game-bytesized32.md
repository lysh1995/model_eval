---
title: "ByteSized32: A Corpus and Challenge Task for Generating Task-Specific World Models Expressed as Text Games"
url: https://arxiv.org/abs/2305.14879
authors: Ruoyao Wang, Graham Todd, Eric (Xingdi) Yuan, Ziang Xiao, Marc-Alexandre Côté, Peter Jansen
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# ByteSized32 (EMNLP 2023)

**Venue:** EMNLP 2023. **arXiv:** 2305.14879 (cs.CL, cs.AI).

> **Disambiguation.** This is the **code-generation** paper: the LLM *writes the text game* — it is the **simulator author**. It is distinct from the follow-up *ByteSized32-State-Prediction* (ACL 2024, arXiv 2406.06485), where the LLM *is* the simulator at inference time, predicting state transitions. See `game-bytesized32-state-prediction.md`.

## Core framing

The paper examines "the capacity of language models to generate explicit, interpretable, and interactive world models," operationalized as **text game generation in Python**. The world model is not latent inside the network — it is emitted as source code, which makes it inspectable, executable, and mechanically testable.

## 1. The corpus

**ByteSized32** = 32 text-based reasoning games written in Python, ~20,000 lines of code including comments.

Per-game statistics:

| Statistic | Mean per game |
|---|---|
| Lines of Python code | 618.1 |
| Lines of comments | 198.1 |
| Tokens | 6,792 |
| Action verbs | 9.8 |
| Valid actions | 306.6 |
| Object classes | 5.4 |
| Object instances | 7.4 |
| Expert path length | 12.8 |

**Themes.** Common-sense and scientific reasoning tasks, e.g.: boiling water; washing dishes with a dishwasher; building a campfire; applying bandages; making ice cubes; heating milk for a baby; protecting from mosquitoes; planting trees.

Each game contains task-critical objects, task-critical actions, **distractors**, and high-level solution procedures documented in structured comments.

## 2. Challenge task setup

The model must generate **complete Python source code** (hundreds of lines) for an interactive text game via **single-shot in-context learning**. The model receives:

- one templated example game from the training set (the reference game), and
- a task specification for an **unseen** evaluation game.

Evaluation set: **16 additional task specifications**, deliberately crafted to minimize similarity with training games. Paired with **6 reference games** → **96 total test cases** (16 × 6).

Core question: can LLMs generate simulations that are syntactically valid, specification-compliant, physically realistic, and winnable?

## 3. Evaluation metrics (definitions)

### A. Technical validity
Does the code actually run? Checked by executing against the Python interpreter:
- **Game initialization** — environment sets up without crashing.
- **Valid action generation** — system returns possible actions for the current state.
- **Step function** — actions modify the environment without error.
- **Runnable game** — the conjunction; tested by exhaustive trajectory crawling (max 3 steps; up to 100 actions per verb group).

### B. Specification compliance
Automated assessment (GPT-4 as judge) of presence of required components:
- task-critical objects
- task-critical actions
- distractor items and behaviors

Validated against human expert ratings via Cohen's κ.

### C. Physical reality alignment
Whether game actions respect real-world constraints (GPT-4 judge):
- samples 100 trajectories from a breadth-first game crawl (max 3 steps)
- paths distributed equally across action types
- assesses whether observations are physically plausible
- example violation: *taking items from closed containers without opening them first*

Scope note: only evaluates *implemented* game actions, not hypothetical scenarios.

### D. Winnability
Does a sequence exist that reaches a winning game state?
- **Automatic:** GPT-4 agent using ReAct + Reflexion prompting.
- **Manual:** a single human expert attempting to reach the winning state.
- The paper notes automatic evaluation **significantly underestimates** winnability; **manual results are reported as the headline**.

## 4. Results

### Table 2 — Technical validity, by number of self-reflection rounds (GPT-4)

| Measurement | 0 Reflections | 1 Reflection | 2 Reflections | 3 Reflections |
|---|---|---|---|---|
| Game Initialization | 85.4% | 85.4% | 89.6% | 88.5% |
| Valid Actions | 80.2% | 83.3% | 87.5% | 88.5% |
| **Runnable Game** | **28.1%** | **42.7%** | **51.0%** | **57.3%** |

**Headline:** GPT-4 produces runnable games on unseen topics in **28%** of cases single-shot; **57%** when allowed to self-reflect on errors (+29.2 points absolute).

### Table 3 — Specification compliance & winnability, before/after reflection

| Measurement | Before | After | Δ |
|---|---|---|---|
| Task-critical objects | 100.0% | 100.0% | 0.0% |
| Task-critical actions | 93.8% | 93.8% | 0.0% |
| Distractors | 21.9% | 18.8% | −3.1% |
| Winnability | 30.2% | 37.5% | +7.3% |

### Physical reality alignment
- Before reflection: **43%** average alignment.
- After reflection: **51%** average alignment (+8 points).
- Excluding zero scores: pre-reflection **58%** (N=71), post-reflection **62%** (N=80) — reducing the effect to **4 points**.

### Table 4 — Manual (human) vs. automatic (GPT-4) evaluation, best games post-reflection

| Measurement | Manual (Human) | Automatic (GPT-4) | Δ |
|---|---|---|---|
| Task-critical objects | 97.2% | 100.0% | +2.8% |
| Task-critical actions | 87.5% | 93.8% | +6.3% |
| Distractors | 37.5% | 18.8% | −18.7% |
| Winnability | 37.5% | 17.8% | −19.7% |

## 5. Human evaluation & LLM-judge agreement (Cohen's κ)

**Specification compliance** (GPT-4 judge vs. human experts):
- Average **κ = 0.74**
- Object presence: **κ = 0.96**
- Action compliance: **κ = 0.75**
- Distractor compliance: **κ = 0.50**

**Physical reality alignment** (GPT-4 vs. human raters):
- **κ = 0.89**, from 200 sampled judgments — high LLM–human alignment on binary physical-plausibility calls.

**Winnability** (GPT-4 vs. human evaluator):
- **κ = 0.43** — modest. Reflects GPT-4's difficulty solving arbitrary text games zero-shot. Manual human evaluation adopted as ground truth for reported winnability.

## Summary of core findings

- 28% runnable without reflection → 57% with 3 rounds of self-reflection
- 37.5% winnable (manual evaluation)
- Strong specification compliance on task-critical objects (100%)
- Moderate physical reality modeling (51% post-reflection)
- **Weak distractor inclusion (18.8%)** — models under-generate the affordances that make a world non-trivial
- Automated LLM-based evaluation agrees strongly with humans on technical validity and physical reasoning (κ = 0.74–0.89), but degrades on task-solving metrics like winnability (κ = 0.43)

---

## Relevance to companion-eval-platform

### (a) Is the LLM PLAYER or SIMULATOR/GAME MASTER?

**SIMULATOR — and specifically, *simulator author*.** This is the sharpest available instance of the simulator role in the literature, and it is worth being precise about the two-step:

1. The LLM **authors the world model** by emitting Python source. The simulator is the *artifact*, not the model's forward pass.
2. A *separate* agent (GPT-4 with ReAct/Reflexion, or a human expert) then **plays** the authored game.

This split is the whole reason the paper is useful to us. Because the simulator is externalized as code, every property we care about becomes a property of an object we can execute, crawl, and diff — rather than a property of a transcript we have to have someone rate. The follow-up paper (2406.06485) collapses this: there the LLM *is* the simulator in-context, and ground truth comes from the reference game engine instead of the interpreter.

### (b) Is ground-truth state available and mechanically checkable?

**Yes — and the metric ladder here is a near-perfect illustration of our core finding.** The four metrics fall into a clean gradient from fully-objective to judgment-laden, and *measurement reliability tracks that gradient exactly*:

| Metric | Ground truth source | Checkable? | Reliability |
|---|---|---|---|
| **Technical validity** (runnable) | Python interpreter | **Fully mechanical.** No judge, no rater. The code runs or it raises. Crawled exhaustively to 3 steps. | Deterministic — κ is not even a meaningful question |
| **Specification compliance** | Reference spec + LLM judge, validated vs. humans | Countable (is object X present? is action Y implemented?) | κ = 0.74 avg; **κ = 0.96** on the most concrete sub-item (object presence) |
| **Physical reality alignment** | LLM judge over sampled trajectories | Binary plausibility calls on discrete observations | κ = 0.89 |
| **Winnability** | Human expert play (auto eval unreliable) | In principle mechanical (does a winning path exist?) but search is intractable → falls back to a human | **κ = 0.43** — the softest metric, the worst agreement |

The through-line: **the more the metric reduces to "count a discrete thing" or "run the code," the higher the agreement.** Object presence — the most trivially countable item — hits κ = 0.96. Winnability, which requires open-ended search and expert judgment, drops to κ = 0.43. Even so, *every* metric here clears our roleplay-quality baseline (human Krippendorff α = 0.25–0.34) by a wide margin. The floor of this paper's reliability is above the ceiling of aesthetic roleplay rating.

**Directly transferable dimensions:**
- **Compile/run as a hard gate.** "Does it execute" is free, exact, and non-negotiable. If any companion artifact can be expressed as executable structure, that structure is checkable at zero rater cost.
- **Presence-of-required-element counting.** The spec-compliance pattern (enumerate required objects/actions up front, then check presence) is a template for any "did the response contain the required components" dimension — and it's the sub-metric that scored κ = 0.96.
- **Distractors as a difficulty signal.** The 18.8% distractor rate is the most interesting negative result: models satisfy the *literal* spec (100% on task-critical objects) while failing to populate the world with plausible-but-irrelevant affordances. Analogously, a companion may hit every checklist item and still produce a thin, checklist-shaped world. Distractor count is an objective, countable proxy for a quality that otherwise only surfaces as an aesthetic complaint.
- **Self-reflection as a measured intervention.** 28% → 57% is a clean, large effect measured on a fully objective metric. Contrast with the physical-alignment gain (43% → 51%, shrinking to 4 points once zero-scores are excluded) — softer metric, softer and more fragile effect.

**Caveat for us:** winnability is the cautionary tale. It is *nominally* mechanically checkable — a winning path either exists or doesn't — but the search space defeats automation, so the authors fell back to a single human expert and got κ = 0.43. "Objective in principle" is not the same as "cheaply checkable in practice." When we select dimensions, we should demand a *tractable decision procedure*, not just a well-defined ground truth.
