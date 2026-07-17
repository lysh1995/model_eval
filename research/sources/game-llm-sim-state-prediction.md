---
title: "Can Language Models Serve as Text-Based World Simulators?"
url: https://arxiv.org/abs/2406.06485
authors: Ruoyao Wang, Graham Todd, Ziang Xiao, Xingdi Yuan, Marc-Alexandre Côté, Peter Clark, Peter Jansen
year: 2024
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Can Language Models Serve as Text-Based World Simulators? (ACL 2024 Short, pp. 1–17)

**Status: the single most important paper for our world-state dimension. It is the only work that turns "does the model track world state" into a scalar with a mechanically-checkable ground truth, and the answer is brutal.**

Also at https://aclanthology.org/2024.acl-short.1/ and https://arxiv.org/html/2406.06485v1. Benchmark: **BYTESIZED32-State-Prediction (BYTESIZED32-SP)**.

## The task: LLM-Sim

> "The LLM-Sim task is defined as implementing a function ℱ:C×S×A→S×ℝ×{0,1} as a world simulator that maps from a given context, state, and action (i.e. c, s_t, a_t) to the subsequent state, reward, and game completion status"

**The decomposition is the reusable idea.** Rather than one blob, ℱ is split into three functions that fail for different reasons:

| Function | Predicts | Meaning |
|---|---|---|
| **ℱ_act** | s_{t+1}^act given c, s_t, a_t | "the direct state change caused by actions" |
| **ℱ_env** | s_{t+1} given c, s_{t+1}^act | "state that results after any environment-driven transitions" |
| **ℱ_R** | r_{t+1}, d_{t+1} | reward and game completion status |

⇒ **Action-driven** (the user did something, world responds) vs **environment-driven** (the world changes on its own — fire spreads, time passes, NPC acts). This split is directly portable to roleplay and I think it is the highest-value structural import in this review. See note 13 for why.

**State representation:** JSON objects encoding "all objects in the game, along with each object's properties... and relationships to other objects".

**Two prediction formalisms** (both tested):
- **Full State** — model emits the complete output state
- **State Difference** — model emits only the changes

**Two rule conditions:** *human-written* rules vs *LLM-generated* rules provided in context.

## Dataset

> "76,369 transitions represented as (c,s_t,r_t,d_t,a_t,s_{t+1}^act,s_{t+1},r_{t+1},d_{t+1}) tuples collected from **31 distinct text games**"

Built on the ByteSized32 corpus. Collection was **deterministic, not annotated**: "deterministically collect[ing] every valid transition that is at most one step away from the gold-label trajectory."

Per-game averages (Table 1): **2463.5 states**, **7.4 action verbs**, **5.5 object types**, **10.4 object instances per state**.

> ⭐ **The ground truth is free because the games are code.** The simulator *is* the label. No annotators, no IAA problem, no aesthetic judgment. This is exactly the property we want and exactly the property open-ended roleplay lacks — the central tension for us.

**No inter-annotator agreement reported** — the human study used the paper's own authors.

## Results

**Table 2 — Dynamic transition accuracy (best condition per function):**

| Function | Accuracy | Condition |
|---|---|---|
| **ℱ_act** (action-driven) | **77.1%** | human rules |
| **ℱ_env** (environment-driven) | **49.7%** | LLM rules, state difference |
| **Full ℱ** | **59.9%** | human rules, full state |

**Static transitions are substantially easier: 73.9%** for full ℱ (human rules, full state) vs 59.9% dynamic.

**Table 3 — Game progress (ℱ_R):** **92.1%** with LLM rules; **61.5%** without rules in context.

**Table 4 — Human comparison on sampled difficult cases: humans 80% vs GPT-4 50%.**

### The headline number, stated honestly

> "After 10 steps, average simulation accuracy would reduce to 0.599^10 ... or less than 1%"

⚠️ **This is an extrapolation, not a measurement.** 0.599^10 = 0.6% assumes each step's error is *independent* and that any single error is fatal. Neither holds cleanly: errors are concentrated on specific hard properties (so a model that gets `temperature` wrong at step 1 will likely get it wrong at step 2 — positively correlated, making the true curve *less* steep than the product rule), while error *propagation* through a corrupted state pushes the other way. The paper does not measure the actual 10-step rollout curve. **Do not cite the <1% figure as an empirical result** — cite 59.9% single-step, and cite the compounding as the paper's own argument, flagged as an assumption. If we build a rollout metric, measuring the *real* decay curve is a genuine contribution, and cheap.

## Failure modes

> "GPT-4 is more likely to make an error when arithmetic, common-sense, or scientific knowledge is needed"

> "Errors are concentrated on non-trivial properties that requires arithmetic (e.g., temperature, timeAboveMaxTemp), common-sense (e.g., current_aperture, current_focus), or scientific knowledge"

> "When predicting action-driven and environment-driven transitions in a single step, GPT-4 tends to focus more on action-driven transitions, resulting in more **unaltered value errors**"

**No quantified error counts beyond the accuracy percentages** — the failure taxonomy is qualitative. A gap we could fill.

The authors' read: LLMs learn **correlational rather than causal** models of world dynamics.

## Limitations (verbatim)

> "This work considers two strong in-context learning LLMs, GPT-3.5 and GPT-4, in their ability to act as explicit formal simulators. We adopt these models because they are generally the most performant off-the-shelf models across a variety of benchmarks. While we observe that even GPT-3.5 and GPT-4 achieve a modest score at the proposed task, we acknowledge that we did not exhaustively evaluate a large selection of large language models, and other models may perform better."

> "The state spaces produced in this work are focused around the domain of common-sense and early (elementary) scientific reasoning... it does not address using LLMs as simulators for highly domain-specific areas, such as physical or medical simulation."

## Relevance to companion-eval-platform

**The LLM is the SIMULATOR here, not the player.** That makes this the closest published analogue to our "AI runs a scene" setting — most of the game-benchmark literature (BALROG, Jericho, ALFWorld) puts the LLM in the player seat and is therefore about a different capability.

1. **⭐ The ℱ_act / ℱ_env split is the import.** Our roleplay analogue: does the model correctly update the world in response to what the *user* did (ℱ_act), and does it keep the world alive/consistent when nobody touched it (ℱ_env)? The 77.1% vs 49.7% gap says these are **different difficulties by ~27 points** and must not be averaged into one "world consistency" score. This is a dimension-separation argument of exactly the kind note 11 demands.
2. **⭐ Environment-driven is where models fail.** ℱ_env at 49.7% ≈ coin flip. In roleplay this is the "world is a backdrop that only reacts, never acts" failure — an established NPC who should have arrived doesn't, weather that never changes, a deadline that never comes due. **This is a named, countable, product-visible failure mode and nobody is measuring it in roleplay.**
3. **⭐ Humans get 80%, not 100%.** This is a *noise floor for state prediction* and it is far better than the α=0.25–0.34 we see on aesthetics — but it is **not 1.0**, which kills the naive "world state is objective so it's free of the ground-truth problem" claim. Even on JSON-vs-JSON with a code oracle available, humans disagree with the oracle 20% of the time on hard cases. Our contradiction auditor will not beat this. Budget for it. (Caveat: n is small and the "humans" were the authors — this 80% is itself soft.)
4. **Rules in context are worth +30.6 points on ℱ_R** (92.1 vs 61.5). Analogue: an explicit world-bible/state block in context should massively improve consistency. That is a *product* recommendation falling out of an eval finding, and it's testable on our grid.
5. **Static 73.9% vs dynamic 59.9%** — 14pt gap. Most of a companion conversation's world state is static (hair colour, sister's name). The consistency problem gets much harder exactly when the world is *supposed* to move, which is what a "game" mode does.
6. **The generalization caveat that matters:** their state space is elementary-science objects with typed properties. Roleplay world state is open-vocabulary, ambiguous, and not enumerable. **Their 59.9% is an upper bound for a much easier problem than ours.** Any number we produce will be worse, and we should say so before a reader says it for us.
