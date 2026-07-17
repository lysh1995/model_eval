---
title: "ScienceWorld: Is your Agent Smarter than a 5th Grader?"
url: https://arxiv.org/abs/2203.07540
authors: Ruoyao Wang, Peter Jansen, Marc-Alexandre Côté, Prithviraj Ammanabrolu
year: 2022
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# ScienceWorld: Is your Agent Smarter than a 5th Grader? (EMNLP 2022, pp. 11279–11298)

ACL Anthology: https://aclanthology.org/2022.emnlp-main.775/ · Website: https://sciworld.apps.allenai.org · Code: https://github.com/allenai/ScienceWorld

**Status: the LLM is the PLAYER, not the simulator. The simulator is 40k lines of hand-written Scala. That makes ScienceWorld the *inverse* of our setting — but the environment itself is the most detailed published example of a mechanically-checkable text world, and its scoring design (required goals + 2–15 optional subgoals, normalized 0–1) is directly stealable.**

> ⚠️ **Numbers below verified against the ACL Anthology PDF text, not a summarizer.** An ar5iv-based extraction of Table 2 was independently reproduced and matched exactly. Where the paper does *not* report something (notably human performance), that is stated explicitly rather than filled in.

## Abstract (verbatim)

> "We present SCIENCEWORLD, a benchmark to test agents' scientific reasoning abilities in a new interactive text environment at the level of a standard elementary school science curriculum. Despite the transformer-based progress seen in question-answering and scientific text processing, we find that current models cannot reason about or explain learned science concepts in novel contexts. For instance, models can easily answer what the conductivity of a known material is but struggle when asked how they would conduct an experiment in a grounded environment to find the conductivity of an unknown material. This begs the question of whether current models are simply retrieving answers by way of seeing a large number of similar examples or if they have learned to reason about concepts in a reusable manner. We hypothesize that agents need to be grounded in interactive environments to achieve such reasoning capabilities. Our experiments provide empirical evidence supporting this hypothesis—showing that a 1.5 million parameter agent trained interactively for 100k steps outperforms a 11 billion parameter model statically trained for scientific question-answering and reasoning from millions of expert demonstrations."

## The environment

> "SCIENCEWORLD is a simulation of the world abstracted through a complex interactive text environment in English with many objects, actions, and simulation engines. The framework consists of **40k lines of SCALA (speed) with a PYTHON interface**."

- **10 interconnected locations**, populated with **up to 200 types of objects** — "devices, instruments, plants/animals, electrical components, substances, containers, and common environment objects such as furniture, books, and paintings."
- **25 high-level actions**, "including both science-domain actions (e.g., using thermometer) and common actions (e.g., moving, opening containers, picking up items), with **approximately 200k possible action-object combinations per step** (though only a limited subset of these will be meaningful)."

## Simulation engines (verbatim, condensed)

The environment "contains a number of elementary science-domain specific processes that either occur automatically (e.g., thermodynamics) or are coupled to actions (e.g., devices, mixing chemicals)."

| Engine | Ground-truth mechanics |
|---|---|
| **Thermodynamics** | "All objects have temperatures and other thermal properties based on their materials. All objects within a container are considered in thermal contact with each other, and transfer heat energy using a simplified conductive heat model." Heat transfer "mediated by the object's thermal conduction coefficient." "Every material has phase transition points (i.e., melting point, boiling point) and combustion points populated based on the best-known or approximate physical values." Convective transfer via heat sources (oven, stove) and sinks (fridge, freezer); rooms transfer ambient heat. |
| **Electricity** | "simple series electrical circuits" — devices (light bulb, motor) powered from sources (battery, solar panel) through conductors. "Polarized and unpolarized components are modelled, with each object having exactly two terminals." "Every non-electrical object in SCIENCEWORLD has virtual unpolarized terminals," enabling conductivity tests (metal vs plastic fork in a circuit). |
| **Devices** | Activated/deactivated by the agent; may have environment-specific activation conditions ("a solar panel will only produce power if it is outside"). |
| **Chemistry** | "mixing a set of substances together in a container will produce a resultant substance (e.g., salt and water mix to produce salt water)." Models "water reactions, rust, food reactions, paint mixing." |
| **Life Stages** | "Living things (plants and animals) progress through life stages (e.g., seed, seedling, juvenile plant, adult plant, reproducing plant, dead plant)." Progression requires meeting needs (water, soil); otherwise the organism dies. |
| **Reproduction and Genetics** | "Genes are inherited from the alleles of both parents, and **genotype is determined at the time of reproduction using a Punnett square**. Phenotype (expressed, visible traits) are determined based on which genes are dominant versus recessive." Pollination via pollinators (e.g., a bee). |
| **Friction (Inclined Plane)** | "models the forces of gravity and friction in the specific context of 1-dimensional inclined plane experiments." Objects slide "at a speed proportional to the plane's angle, and the friction coefficient of its surface material." |
| **Containers** | Always-open or closeable; contents invisible until opened. "Some effects spread beyond a container — for example, a wooden cupboard with a hot object inside may combust." |

**Fidelity caveat (verbatim footnote 3):**
> "For tractability, simulation engines are implemented with fidelity at the level of elementary science. Thermal transfer uses a simplified equation, biological changes happen in stages rather than gradually, only simple series circuits are simulated (no resistance, inductance, or any advanced topics), etc."

## Task structure: 30 tasks / 10 topics

> "we identified a candidate set of **10 broad science exam topics** from the list of 400 fine-grained science curriculum topics of Xu et al. (2020). Topics were chosen that would be amenable to text-based simulation, and that did not have critical fine-grained spatial reasoning requirements, and include: changes of state, temperature measurement, electrical circuits, friction, object classification, chemical mixtures, plants and pollinators, life spans, life stages, and Mendelian genetics. Each topic was further divided into between **2 and 4 specific tasks** for agents to perform, producing a total of **30 science-domain tasks**."

> "To prevent overfitting and encourage generalization, each subtask contains between **10 and 1400 parametric variations** (with **7200 total variations across all 30 subtasks**). Variations change critical task objects (e.g., the specific substance to be melted), the agent's starting location in the environment, as well as randomly vary the contents of the environment itself."

**Splits:** "For a given subtask, variations are split into 50% training, 25% development, and 25% test sets. Variations are sorted such that critical unseen variations (e.g., substances, animals, or plants unseen during training) are found in development and test sets."

## Scoring (verbatim) — the part worth stealing

> "To reduce reward sparsity, each task includes between **2 and 15 optional subgoals** (such as turning on the stove, or the substance increasing in temperature by 10C) that help nudge agents in the direction of canonical solutions, if desired. Meeting required and optional subgoals increases the agent's score on a given subtask. **Scores for all tasks are normalized to between 0 and 1.**"

Each subtask also has "a small number of method-agnostic required goals to be met" — i.e. the goal check does not prescribe *how*, only *what state must hold*.

**Oracle agents (the label source):**
> "To support imitation learning, we provide gold trajectories from **30 hand-coded oracles** on all subtasks and variations. For tractability these solutions represent **canonical solution methods** (e.g., using a stove to boil water), rather than all possible solution methods that lead to the goal state (e.g., building a campfire to boil water)."

⇒ Note the asymmetry: **scoring is method-agnostic (state-based), but the demonstrations are canonical-method-only.** The scorer is more permissive than the expert. That's the right way round, and it's a design point for us.

## Results — Table 2 (verbatim, zero-shot on test variations)

"Rely on Test Time Valid Action Detection Aid": ✓ for Random-Valid, DRRN, KG-A2C, CALM (not BC / TDT).

| # | Topic | Task | Random-Valid | DRRN | KG-A2C | CALM | BC | TDT |
|---|---|---|---|---|---|---|---|---|
| 1-1 | Matter | Changes of State (Boiling) | 0.00 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1-2 | Matter | Changes of State (Melting) | 0.00 | 0.04 | 0.00 | 0.00 | 0.00 | 0.01 |
| 1-3 | Matter | Changes of State (Freezing) | 0.00 | 0.01 | 0.04 | 0.00 | 0.01 | 0.00 |
| 1-4 | Matter | Changes of State (Any) | 0.00 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2-1 | Measurement | Use Thermometer | 0.00 | 0.10 | 0.06 | 0.01 | 0.04 | 0.04 |
| 2-2 | Measurement | Measuring Boiling Point (known) | 0.00 | 0.08 | 0.11 | 0.01 | 0.01 | 0.02 |
| 2-3 | Measurement | Measuring Boiling Point (unknown) | 0.00 | 0.06 | 0.04 | 0.01 | 0.01 | 0.02 |
| 3-1 | Electricity | Create a circuit | 0.01 | 0.13 | 0.07 | 0.05 | 0.03 | 0.07 |
| 3-2 | Electricity | Renewable vs Non-renewable Energy | 0.01 | 0.10 | 0.04 | 0.07 | 0.02 | 0.05 |
| 3-3 | Electricity | Test Conductivity (known) | 0.01 | 0.07 | 0.04 | 0.02 | 0.05 | 0.05 |
| 3-4 | Electricity | Test Conductivity (unknown) | 0.00 | 0.20 | 0.04 | 0.02 | 0.04 | 0.05 |
| 4-1 | Classification | Find a living thing | 0.03 | 0.26 | 0.18 | 0.10 | 0.29 | 0.16 |
| 4-2 | Classification | Find a non-living thing | 0.63 | 0.56 | 0.44 | 0.54 | 0.19 | 0.17 |
| 4-3 | Classification | Find a plant | 0.01 | 0.19 | 0.16 | 0.10 | 0.17 | 0.19 |
| 4-4 | Classification | Find an animal | 0.01 | 0.19 | 0.15 | 0.08 | 0.21 | 0.19 |
| 5-1 | Biology | Grow a plant | 0.07 | 0.09 | 0.06 | 0.02 | 0.08 | 0.03 |
| 5-2 | Biology | Grow a fruit | 0.02 | 0.16 | 0.11 | 0.04 | 0.03 | 0.05 |
| 6-1 | Chemistry | Mixing (generic) | 0.01 | 0.20 | 0.17 | 0.03 | 0.06 | 0.10 |
| 6-2 | Chemistry | Mixing paints (secondary colours) | 0.01 | 0.29 | 0.19 | 0.06 | 0.16 | 0.20 |
| 6-3 | Chemistry | Mixing paints (tertiary colours) | 0.00 | 0.11 | 0.04 | 0.03 | 0.05 | 0.07 |
| 7-1 | Biology | Identify longest-lived animal | 0.02 | 0.48 | 0.43 | 0.06 | 0.26 | 0.20 |
| 7-2 | Biology | Identify shortest-lived animal | 0.03 | 0.47 | 0.32 | 0.10 | 0.14 | 0.16 |
| 7-3 | Biology | Identify longest-then-shortest-lived animal | 0.01 | 0.31 | 0.23 | 0.04 | 0.02 | 0.20 |
| 8-1 | Biology | Identify life stages (plant) | 0.00 | 0.09 | 0.05 | 0.04 | 0.04 | 0.02 |
| 8-2 | Biology | Identify life stages (animal) | 0.00 | 0.10 | 0.10 | 0.00 | 0.02 | 0.07 |
| 9-1 | Forces | Inclined Planes (determine angle) | 0.01 | 0.13 | 0.04 | 0.00 | 0.05 | 0.04 |
| 9-2 | Forces | Friction (known surfaces) | 0.00 | 0.13 | 0.04 | 0.03 | 0.05 | 0.04 |
| 9-3 | Forces | Friction (unknown surfaces) | 0.01 | 0.13 | 0.04 | 0.02 | 0.04 | 0.04 |
| 10-1 | Biology | Mendelian Genetics (known plants) | 0.01 | 0.19 | 0.11 | 0.02 | 0.06 | 0.06 |
| 10-2 | Biology | Mendelian Genetics (unknown plants) | 0.01 | 0.17 | 0.11 | 0.02 | 0.13 | 0.05 |
| | | **Average** | **0.03** | **0.17** | **0.11** | **0.05** | **0.08** | **0.08** |
| | | **Param. Count ×10⁶** | – | **1.5** | **5.5** | **131*** | **11,000** | **11,000** |

**Table 2 caption (verbatim):** "Zero-shot performance of the agents on test variations of across all tasks. All online RL-trained agent performances are averaged over 5 independent random seeds. **Results across seeds tend to have low variance, with 80% of standard deviations below 0.05, and 95% of standard deviations below 0.10.** Performance for RL agents is averaged over the last 10% of evaluation episodes, while T5 performance represents average task score across all test variations of a task. * signifies that the value of 131M parameters includes the number of the parameters of the pre-trained GPT-2 action generator model. **Only 6.9 million policy parameters are updated in RL training.**"

**Baselines, in brief:**
- **DRRN** (He et al., 2016) — learns separate observation/action representations, selects from the valid-action set `A_t`. "a strong baseline with near state-of-the-art performance on many medium-to-hard interactive text environments."
- **KG-A2C** (Ammanabrolu & Hausknecht, 2020) — knowledge graph from OpenIE triples; selects action templates then fills them from the KG.
- **CALM (GPT2)** (Yao et al., 2020) — GPT-2 fine-tuned on oracle transcripts generates a shortlist of 30 candidate actions; a DRRN-like model re-ranks.
- **Behavior Cloning (BC-T5)** — T5 initialized from **Macaw-11b**; **211,092 training examples** with `(d, o_{t-1}, a_{t-1}, o_t)` → `a_t`.
- **Text Decision Transformer (TDT-T5)** — novel here; models the whole POMDP trajectory as a sequence with returns-to-go `R̂`; **224,902 training examples** with `(d, o_{t-1}, R̂_{t-1}, a_{t-1}, o_t, R̂_t)` → `a_t`.

### The 1.5M vs 11B claim, precisely

> "Our best-performing model, the **DRRN, has only 1.5 million parameters – four orders of magnitude less than the T5 models**. Both models also receive the same number of gradient updates (10⁶) with respect to SCIENCEWORLD training tasks—though the T5 models have the added benefit of pre-training both from science exam QA and a large number of expert demonstrations. This underscores that **how a model approaches modeling state spaces and action sequences may be more important than the scope of its pre-training.**"

⇒ Concretely: **DRRN 1.5M params → 0.17** vs **BC-T5 / TDT-T5 11,000M params → 0.08 each**. Roughly **2× the score at ~1/7300 the parameters.** Caveat the paper itself concedes: DRRN uses the **valid-action detection aid** at test time and the T5 agents do not — the comparison is not apples-to-apples on affordances.

> "**all but two agents benchmarked here depend on SCIENCEWORLD's valid action detection aid at test time, substantially simplifying their search problem in the action space.**"

## ⚠️ Human performance: NOT REPORTED

**Despite the title "Is your Agent Smarter than a 5th Grader?", the paper contains no human study and no human performance number.** The full text was searched; the only comparison baselines are computational (Random-Valid, DRRN, KG-A2C, CALM, BC, TDT). The title is rhetorical framing, not a measured comparison.

The closest thing to a ceiling is the **hand-coded oracle agents**, which by construction score ~1.0 — that is a *program's* ceiling, not a human's. **Do not cite a "human baseline" for ScienceWorld.** If a downstream doc needs a human anchor for interactive text agents, it must come from elsewhere (e.g. ReAct's ALFWorld numbers, or Jericho human walkthroughs).

The authors' own framing of the difficulty anchor is a *model* comparison, not a human one:
> "With top-performing agents reaching normalized average scores of 0.17 across tasks, performance on SCIENCEWORLD is comparable to the current best-performing agents on medium-difficulty interactive fiction games such as Zork."

## Other findings worth keeping

**Retrieval vs procedure — the paired-task design (a genuinely clever eval idea):**
> "SCIENCEWORLD includes **pairs of identical tasks where one can be solved by retrieving some critical component of the answer, while the other requires conducting the experimental procedure successfully.**"

Tasks 3-3 (conductivity, *known* material — lookupable) vs 3-4 (conductivity, *unknown* material — must run the experiment). Same for 2-2/2-3 (boiling point) and 10-1/10-2 (genetics). This isolates *retrieval* from *procedure* within a matched pair.

**Failure is at the commonsense layer, not the science layer:**
> "while agents appear to struggle with science-domain inference procedures such as how to heat a substance or how to grow a seed, they also currently lack a fluency with commonsense skills such as navigating the environment or storing liquids in containers."

> "All models relying on large language model for action selection (CALM, BC-T5, TDT-T5) generally achieve low performance as **they tend to generate few valid actions in their candidate action lists.**"

**Description fidelity is capped by context length (relevant to us):**
> "while SCIENCEWORLD achieves a high environment fidelity for a text simulation, this is still tempered by pragmatic concerns, such as **generating comparatively short descriptions of environments that can fit into the sequence lengths of most transformer models**. As such, even environments with complex physical, chemical, and biological processes underlying their simulations (such as SCIENCEWORLD) still ultimately must limit the vividness of their descriptions."

**The paper explicitly points at ALFWorld as the hybrid-environment precedent:**
> "Hybrid environments (e.g., Shridhar et al., 2020) that concurrently model the same environment as both a high-fidelity 3D world and comparatively low-fidelity text-based simulation have shown that text environments can be used to provide useful task pre-training that can transfer back to the 3D environment with relatively low simulation compute cost."

**Compute (Table 4):** DRRN 4gb/12h; KG-A2C 16gb/20h; CALM-GPT2 16gb/40h (up to 6000 GPU hours for full CALM experiments); T5 pre-training 60h on a v3-32 TPU pod. "Runtime estimates should be multiplied by the number of tasks (30) and number of random seeds (5)."

## Relevance to companion-eval-platform

### (a) Is the LLM the PLAYER or the SIMULATOR/GAME MASTER?

**The LLM is unambiguously the PLAYER. The simulator is hand-written Scala — 40k lines of it — and no learned model touches it.** ScienceWorld is the mirror image of our setting: they hold the world fixed and measure the agent; we hold the user fixed and measure the world-keeper. **Nothing about the DRRN/CALM/T5 result table transfers to us as a baseline.** Its value to us is entirely in the *environment and scoring design*, not the agent results.

This is the same axis on which `game-llm-sim-state-prediction.md` (LLM-Sim) sits on the *other* side — and notably it's the **same first author (Wang) and same senior authors (Côté, Jansen)**. LLM-Sim is literally the ScienceWorld team later asking "what if the LLM were the simulator instead?" ⇒ **ScienceWorld is the prequel to our closest analogue.** Read the pair together; the 59.9% in LLM-Sim is what happens when you try to replace exactly the Scala engine described here.

### (b) Is ground-truth simulator state available and mechanically checkable?

**Yes — maximally so, and this is the cleanest case in the corpus.** Every property that matters is a typed field in a Scala object with a known update rule:

- Temperature is a **float** with a phase-transition threshold ⇒ "did the water boil" is `temp >= boilingPoint`, not a judgment.
- Circuit closure is a **graph reachability check** over explicit anode/cathode terminals.
- Life stage is an **enum** (seed → seedling → juvenile → adult → reproducing → dead).
- Genotype is computed by a **Punnett square** — deterministic given parents.
- Inclined-plane position is a **percentage** driven by angle × friction coefficient.

There is no annotator anywhere in the loop, and therefore **no inter-rater reliability to worry about — α is undefined because there are no raters.** Contrast our α = 0.25–0.34 on roleplay aesthetics. This is the property we want and the reason this file exists.

**What to actually take:**

1. **⭐ The scoring architecture is the import, and it is directly portable.** "A small number of **method-agnostic required goals**" + "**between 2 and 15 optional subgoals**" + "**normalized to between 0 and 1**". Three properties we should copy verbatim: (i) **method-agnostic** — score the resulting *state*, never the path, so we don't punish a model for a creative-but-valid route; (ii) **dense subgoals** — a scene where the model achieves 4 of 7 tracked state changes scores 0.57, not "fail", which gives us gradient instead of a near-binary metric; (iii) **normalized** — makes heterogeneous scenarios averageable. This is a fully worked answer to "how do you build a countable score over an open-ended interaction," from a benchmark that shipped.

2. **⭐ The retrieval-vs-procedure paired tasks are the single best methodological idea here.** 3-3 (known material — answer is memorizable) vs 3-4 (unknown material — must actually run the experiment) is a **matched-pair design that isolates memorization from mechanism** while holding everything else constant. The empirical payoff is real: DRRN gets **0.07 on known vs 0.20 on unknown** — the *unknown* variant scored *higher*, which is only interpretable because the pair is matched. Our analogue: a scenario whose outcome is inferable from the character card vs one that requires tracking what happened *in this conversation*. If a model does well on the first and badly on the second, it's reciting the persona rather than simulating it — and the paired design makes that a **difference score**, which is far more robust than either absolute number. **This is cheap to build and I think it's the highest-value transferable idea in the paper.**

3. **⭐ Ground-truth availability does not make the task easy — 0.17 is the SOTA.** Worth internalizing before we oversell mechanical checkability as a panacea. A perfectly checkable, fully observable, deterministic world still yields **0.17/1.0 for the best agent, and 0.00 on nine of thirty tasks**. Objectivity buys us *trustworthy* numbers, not *good* ones, and we should expect our world-state numbers to be similarly ugly. That's a feature (headroom, discriminative power) but it must be framed before a reader reads 0.17-equivalents as a broken metric.

4. **Objective ≠ meaningful: watch Task 4-2.** Random-Valid scores **0.63** on "find a non-living thing" — higher than every learned agent except DRRN (0.56), which it *beats*. A fully mechanical scorer produced a task where **random action is the second-best policy**, purely because the subgoal decomposition hands out most of its credit for trivially-satisfied conditions. **Countability does not confer validity.** Any subgoal-decomposed score we ship needs a random-policy baseline computed per-scenario, or we will publish a dimension that random text passes. This is the direct rebuttal to a naive reading of our own "prefer objective correlates" thesis, and we should own it rather than have it pointed out.

5. **The valid-action aid is a confound, and it is our confound too.** DRRN's win depends on the simulator handing it the enumerated legal-action set; the 11B models get no such list and mostly emit invalid actions. Their "generate few valid actions in their candidate action lists" failure is not a reasoning failure — it's an **affordance-formatting failure being scored as reasoning**. Directly analogous to grading a roleplay model down for not emitting our state-block schema. **Separate "knows what to do" from "can express it in our format," or we'll publish a schema-compliance metric mislabelled as world-modelling.**

6. **Failures cluster at the commonsense layer, not the domain layer** — agents fail at "navigating the environment or storing liquids in containers" before they ever reach the science. Our analogue: models will break on *who is in the room* and *what time it is* long before they break on subtle characterization. **Instrument the boring state first**; it is where the variance is, and it is the most countable part.

7. **The context-length caveat is a limitation we inherit, stated better than we'd state it.** Even a 40k-line simulator "must limit the vividness of their descriptions" to fit transformer sequence lengths. Rich state and renderable state are in tension — the more we track, the less of it fits in the prompt. Quote this when justifying why our state block is a compressed projection rather than the full world.

8. **Reuse note — variance discipline:** "80% of standard deviations below 0.05, and 95% below 0.10" over **5 seeds**. They report the *distribution of seed variance* rather than a single ± and average RL performance "over the last 10% of evaluation episodes" rather than at a cherry-picked peak. Cheap, honest reporting conventions worth matching (cf. `psycho-variance-in-benchmarks.md`).

9. **⚠️ Citation hygiene — the human comparison does not exist.** The title invites "5th grader" comparisons and secondary sources sometimes repeat one, but **the paper reports no human performance**. If our writeup wants a human anchor for interactive text agents, use ReAct's ALFWorld figures (Human expert **59.6 SR** on WebShop; see `game-alfworld.md`) or Jericho walkthroughs, and never attribute a human number to ScienceWorld. The oracle agents score ~1.0 by construction and are **not** a human proxy.
