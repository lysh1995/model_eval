---
title: "Can Language Models Serve as Text-Based World Simulators? (ByteSized32-State-Prediction)"
url: https://arxiv.org/abs/2406.06485
authors: Ruoyao Wang, Graham Todd, Ziang Xiao, Xingdi Yuan, Marc-Alexandre Côté, Peter Clark, Peter Jansen
year: 2024
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# ByteSized32-State-Prediction (ACL 2024)

**Venue:** ACL 2024. **arXiv:** 2406.06485. Follow-up to ByteSized32 (EMNLP 2023, arXiv 2305.14879 — see `game-bytesized32.md`).

## Relationship to the original ByteSized32

The 2023 paper asked whether an LLM can **author** a simulator (emit Python game code). This paper asks whether an LLM can **be** the simulator — predicting state transitions directly, in-context, with no code emitted. The reference game engines from the ByteSized32 corpus supply exact ground truth.

## Core claim

The authors test whether current LLMs can function as world simulators by predicting state transitions in text-based environments. Verdict: despite impressive performance, GPT-4 "is still an unreliable world simulator without further innovations."

## The formal task — LLM-Sim

> "The LLM-Sim task is defined as implementing a function ℱ:C×S×A→S×ℝ×{0,1} as a world simulator that maps from a given context, state, and action (i.e. c, s_t, a_t) to the subsequent state, reward, and game completion status"

> "Performance on LLM-Sim is determined by the model's prediction accuracy w.r.t. the ground truth labels over a dataset of test samples"

The three sub-functions, verbatim:

| Function | Predicts | Verbatim |
|---|---|---|
| **ℱ_act** | s_{t+1}^act given c, s_t, a_t | "the direct state change caused by actions" |
| **ℱ_env** | s_{t+1} given c, s_{t+1}^act | "state that results after any environment-driven transitions" |
| **ℱ_R** | r_{t+1}, d_{t+1} | reward and game completion status |

**State representation:** JSON objects encoding "all objects in the game, along with each object's properties... and relationships to other objects".

## Benchmark construction

**ByteSized32-State-Prediction (BS32-SP):** **76,369 transitions** across **31 distinct text games**. Each transition record contains state, action, and outcome information.

Full tuple: "(c,s_t,r_t,d_t,a_t,s_{t+1}^act,s_{t+1},r_{t+1},d_{t+1})".

Collection was **deterministic, not annotated**: "deterministically collect[ing] every valid transition that is at most one step away from the gold-label trajectory."

Per-game averages (Table 1): **2463.5 states**, **7.4 action verbs**, **5.5 object types**, **10.4 object instances per state**.

**No inter-annotator agreement is reported** — the human study used the paper's own authors as subjects.

## Three prediction regimes

The state transition function is decomposed into:

- **ℱ_act** — **action-driven** transitions: direct effects of the agent's action.
- **ℱ_env** — **environment-driven** transitions: time-based / background dynamics that occur regardless of the action (e.g. water heating, a fire burning down).
- **ℱ** — the **full** state transition, combining both.

Each is scored two ways:
- **Full** — predict the entire resulting state.
- **Diff** — predict only the changed portion of the state.

Conditions vary the rule supervision (human-written rules / LLM-generated rules / no rules) and whether the state is **dynamic** (non-trivial — something actually changes) or **static** (trivial — nothing changes).

## Results — GPT-4 accuracy (Table 2)

| Condition | ℱ (Full) | ℱ (Diff) | ℱ_act (Full) | ℱ_act (Diff) | ℱ_env (Full) | ℱ_env (Diff) |
|---|---|---|---|---|---|---|
| **Human rules, dynamic** | **59.9%** | 51.6% | **77.1%** | 68.4% | 38.6% | 22.2% |
| Human rules, static | 63.5% | 73.9% | 77.5% | 90.2% | 73.8% | 92.3% |
| LLM rules, dynamic | 59.0% | 59.5% | 76.1% | 75.2% | 44.1% | 49.7% |
| No rules, dynamic | 54.1% | 52.2% | 70.8% | 67.7% | 24.4% | 22.3% |

### Number verification (as requested)

- **59.9%** — CONFIRMED. GPT-4's best accuracy on **non-trivial (dynamic) full state transitions** with human-written rules.
- **76.8%** — **NOT FOUND.** No such figure appears in the paper. The nearest actual value is **77.1%** — action-driven (ℱ_act) full-state prediction, human rules, dynamic. (77.5% is the static-state counterpart.) The commonly-cited pairing should be **59.9% / 77.1%**.

### Game progress / reward prediction (ℱ_R, Table 3)

| Condition | Accuracy |
|---|---|
| With LLM rules | **92.1%** |
| Without rules | **61.5%** |

**+30.6 points from having rules in context.** Directly relevant: an explicit world-bible/state block in context should massively improve consistency. That is a *product* recommendation falling out of an eval finding, and it is testable on our grid.

### Human baseline (Table 4)
On challenging transitions, humans reached **~80%** vs. GPT-4's **~50%**.

⭐ **This is a noise floor for state prediction, and it must be read carefully.** 80% is far better than the α = 0.25–0.34 we see on aesthetics — this is the core reason to prefer world-state dimensions. But it is **not 100%**, which kills the naive claim that "world state is objective, therefore free of the ground-truth problem." Even with JSON-vs-JSON and a code oracle available, humans disagree with the oracle 20% of the time on hard cases. Our contradiction auditor will not beat this. (Caveat: small n, and the "humans" were the authors — the 80% is itself soft.)

### ⚠️ The compounding claim — an extrapolation, not a measurement

> "After 10 steps, average simulation accuracy would reduce to 0.599^10 ... or less than 1%"

**0.599^10 = 0.6% assumes each step's error is independent and that any single error is fatal.** Neither holds cleanly: errors concentrate on specific hard properties (a model that gets `temperature` wrong at step 1 likely gets it wrong at step 2 — positively correlated, making the true curve *less* steep than the product rule), while error propagation through an already-corrupted state pushes the other way. **The paper never measures the actual 10-step rollout curve.**

**Do not cite the <1% figure as an empirical result.** Cite 59.9% single-step, and cite the compounding as the authors' own argument, flagged as an assumption. Measuring the *real* decay curve is a genuine, cheap contribution available to us.

## Key findings

- **Environment-driven transitions are the failure mode.** ℱ_env collapses to **38.6%** (full) / **22.2%** (diff) on dynamic states — far below the 77.1% on action-driven transitions. Modeling what happens *on its own*, independent of the agent's action, is dramatically harder than modeling the direct consequences of an action.
- **Static vs. dynamic gap.** Static (nothing-changes) transitions score much higher — e.g. ℱ_env diff 92.3% static vs. 22.2% dynamic. Aggregate accuracy is inflated by trivial cases; only the dynamic slice is diagnostic.
- **Rules help, modestly.** Human rules 59.9% vs. no rules 54.1% on ℱ (full). LLM-generated rules (59.0%) are nearly as good as human-written ones. But on ℱ_R the rules effect is large (+30.6pp) — so "rules help modestly" is true for state, false for reward.

## Failure modes (qualitative only)

> "GPT-4 is more likely to make an error when arithmetic, common-sense, or scientific knowledge is needed"

> "Errors are concentrated on non-trivial properties that requires arithmetic (e.g., temperature, timeAboveMaxTemp), common-sense (e.g., current_aperture, current_focus), or scientific knowledge"

> "When predicting action-driven and environment-driven transitions in a single step, GPT-4 tends to focus more on action-driven transitions, resulting in more **unaltered value errors**"

**No quantified error counts beyond the accuracy percentages** — the failure taxonomy is qualitative. A gap we could fill.

Authors' interpretation: LLMs learn **correlational rather than causal** models of world dynamics.

## Limitations (verbatim)

> "This work considers two strong in-context learning LLMs, GPT-3.5 and GPT-4, in their ability to act as explicit formal simulators. We adopt these models because they are generally the most performant off-the-shelf models across a variety of benchmarks. While we observe that even GPT-3.5 and GPT-4 achieve a modest score at the proposed task, we acknowledge that we did not exhaustively evaluate a large selection of large language models, and other models may perform better."

> "The state spaces produced in this work are focused around the domain of common-sense and early (elementary) scientific reasoning... it does not address using LLMs as simulators for highly domain-specific areas, such as physical or medical simulation."

---

## Relevance to companion-eval-platform

### (a) Is the LLM PLAYER or SIMULATOR/GAME MASTER?

**SIMULATOR — the LLM *is* the game engine.** This is the purest simulator framing in the literature. The model is not authoring code (as in ByteSized32 2023) and not playing (as in the social deduction work); it is being asked to *be* the state transition function. Given state + action, emit the next state. There is no player role anywhere in the evaluation loop.

Read the two papers as a pair: 2023 = LLM as **simulator author** (artifact is code, checked by the interpreter); 2024 = LLM as **simulator itself** (artifact is a predicted state, checked against the reference engine). Both keep ground truth external and mechanical — that's the family resemblance that makes this line of work valuable to us.

### (b) Is ground-truth state available and mechanically checkable?

**Yes — this is the strongest case in the entire source set.** The properties:

- **Ground truth is exact and free.** Each of the 76,369 transitions has a correct next state produced by the reference Python game engine. Not a rater's opinion, not an LLM judge — the actual output of the actual simulator.
- **Scoring is string/structure comparison.** Predicted state vs. true state. No judge model, no annotator, no κ to report — inter-annotator reliability is *not a coherent question* here, because there are no annotators. This sits at the absolute objective end of our dimension ladder, above even ByteSized32's "does it compile" gate.
- **Scale is 3 orders of magnitude past human rating.** 76,369 items. No aesthetic-rating protocol reaches that; our roleplay-quality ratings (α = 0.25–0.34) can't even reach stability at N in the hundreds.

**The most transferable idea: the dynamic/static split.** The paper's own numbers show aggregate accuracy is badly inflated by trivial transitions where nothing changes (ℱ_env: 92.3% static vs. 22.2% dynamic — a 70-point gap on the same metric). This generalizes directly to us: **any objective metric must be reported on the non-trivial slice**, or the no-op cases will manufacture a flattering headline number. If we adopt countable dimensions, we need the equivalent of a "dynamic" filter, or we'll be measuring how often nothing was supposed to happen.

**Second transferable idea: decompose the transition by *cause*.** Splitting ℱ into ℱ_act (agent-caused) and ℱ_env (world-caused) is what surfaces the real finding — the 77.1% vs. 38.6% gap. A single aggregate would have hidden it. For a companion, the analogue is separating what changes *because the user did something* from what should change *on its own* (elapsed time, prior commitments, persistent state). The ByteSized32-SP result predicts that the second category is where models fail, and it is exactly the category that mechanically-checkable state tracking would catch and aesthetic rating would not.

**Caveat:** the state here is a small, closed, typed object graph — dishes, water temperature, container open/closed. Companion state is not so tidy. The lesson to port is the *methodology* (external engine as ground truth; report the dynamic slice; decompose by causal source), not the assumption that companion state reduces this cleanly.
