---
title: "TALES: Text Adventure Learning Environment Suite"
url: https://arxiv.org/abs/2504.14128
authors: Christopher Zhang Cui, Xingdi Yuan, Ziang Xiao, Prithviraj Ammanabrolu, Marc-Alexandre Côté
year: 2025
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# TALES — Text Adventure Learning Environment Suite (arXiv 2504.14128, 2025)

**Affiliations:** 1 University of California, San Diego; 2 Microsoft Research Montréal; 3 Johns Hopkins University. Contact: `czcui@ucsd.edu`, `textworld@microsoft.com`

**Versions:** Submitted 19 Apr 2025 (v1), last revised 24 Apr 2025 (**v4**). Categories: cs.AI, cs.CL.
**Full text used:** https://arxiv.org/html/2504.14128v4 — verified that **Table 3 is byte-identical between v3 and v4**.
**Code / leaderboard:** https://github.com/microsoft/tale-suite • https://microsoft.github.io/tale-suite/

**Why this one was selected.** The brief asked for a 2025–26 benchmark measuring state-transition or rule-following accuracy against a ground-truth simulator. TALES is the strongest fit available: it is the first benchmark to unify Jericho, ALFWorld, ScienceWorld, TextWorld and TextWorldExpress **in their canonical forms** with **minimal scaffolding**, and every environment is a deterministic, executable simulator with mechanical scoring. A search for a more recent LLM-as-world-model / state-tracking benchmark (WorldModelBench, Word2World, R-WoM, and similar 2025–26 candidates) surfaced no unified benchmark that better matches the "ground-truth simulator + rule-following accuracy" spec. Note that the **simulator-side complement is already captured** in this repo as `game-bytesized32-state-prediction.md` (Can Language Models Serve as Text-Based World Simulators?, ACL 2024) — TALES is the **player-side** counterpart, and the two together bracket the platform's question. See Relevance section.

---

## Abstract (verbatim)

> "Reasoning is an essential skill to enable Large Language Models (LLMs) to interact with the world. As tasks become more complex, they demand increasingly sophisticated and diverse reasoning capabilities for sequential decision-making, requiring structured reasoning over the context history to determine the next best action. We introduce TALES, a diverse collection of synthetic and human-written text-adventure games designed to challenge and evaluate diverse reasoning capabilities. We present results over a range of LLMs, open- and closed-weights, performing a qualitative analysis on the top performing models. **Despite an impressive showing on synthetic games, even the top LLM-driven agents fail to achieve 15% on games designed for human enjoyment.** Code and visualization of the experiments can be found at microsoft.github.io/tale-suite."

---

## 1. What the benchmark is (verbatim)

> "To evaluate an LLM-driven agent's comprehensive reasoning capabilities, we introduce TALES, **the first benchmark that unifies Jericho, ALFWorld, ScienceWorld, TextWorld, and TextWorldExpress in their canonical forms.** Unlike other benchmarks that focus on a specific text-adventure game framework, introduce an excessive amount of expert knowledge to explicitly provide the agent the otherwise implicit constraints, or reduce the game's scope to obtain results Paglieri et al. (2024); Chang et al. (2024), **we apply minimal scaffolding.** This creates a challenging and comprehensive evaluation suite for better understanding the agent's baseline composite reasoning skills without expert knowledge."

> "We show the performance of **34 models**, open- and closed-weights, in a **zero-shot setting on a suite of 122 games.**"

> "We show that despite the impressive capabilities and **likely data contamination** of many state-of-the-art LLMs, **no agent is capable of completing the gauntlet of games in TALES in a zero-shot setting with minimal inductive bias.**"

**The mechanical substrate (verbatim, §3):**

> "All frameworks included in TALES are text-adventure game environments where the player is provided a textual observation, and sometimes an explicit goal, and are able to interact with the environment through short action phrases. **If these action phrases are invalid, the parser will typically return some error message indicative of whether the action has been understood by the environment but is unable to be done, or if the parser just does not understand the action.** Some environments use a nearest-neighbor parser which can understand similar action phrases to mean the same thing, e.g., *take lamp*, *get lamp* and *pick up lamp*. **Most environments provide the player a score as a metric of how far they have progressed through the game**, though some environments only provide a single score at the end of the game if the goal state is reached. Unless otherwise stated, **all environments have failure conditions or actions that will cause the game to reset.**"

> "It becomes more challenging with grounded environments, **where the causal constraints between actions are fixed and cannot be violated.**"

### The four reasoning skills measured (verbatim headings + definitions, §2)

- **Spatial reasoning.** "The ability to navigate the environment effectively and understand the spatial relationship among game objects, including path finding, backtracking, and locating items."
- **Deductive reasoning.** "The ability to derive valid actions through the logical application of general principles within a specific environmental context."
- **Inductive reasoning.** "The ability to draw conclusions through interactions and observations. […] The inductive reasoning skill allows the agent to **derive environment-specific rules through exploration** and act accordingly."
- **Grounded reasoning.** "The ability to make decisions based on relevant information and current context. This reasoning skill is analogous to **situational awareness** in humans. […] as agents often have access to the full interaction history at every step, **the ability to correctly identify what information is relevant to the current state and reason over said information becomes more and more important as the length of the history grows.**"

---

## 2. Table 1 — Attributes of each framework (verbatim)

Caption: "Attributes of each framework with respect to one another and the top average agent score for each framework across subsets of LLMs. Claude-3.5-Sonnet† outperforms all other zero-shot models."

| | TextWorld | TextWorldExpress | ALFWorld | ScienceWorld | Jericho |
|---|---|---|---|---|---|
| **Properties** | | | | | |
| #Games | 10 | 16 | 12 | 30 | 54 |
| Avg. walkthrough length | 13.70 | 33.06 | 5.83 | 41.67 | 87.15 |
| Informative feedback | ✓ | ✓ | ✗ | ✓ | ✓ |
| Synthetic | ✓ | ✓ | ✓ | ✓ | ✗ |
| Intermediate rewards | ✓ | ✓ | ✗ | ✓ | ✓ |
| Nearest-neighbor parser | ✓ | ✗ | ✗ | ✓ | ✓ |
| Game resets | ✓ | ✓ | ✗ | ✓ | ✓ |
| Dead state | ✓ | ✓ | ✗ | ✓ | ✓ |
| **Top Avg. agent score** | | | | | |
| Zero-shot | 95.5† | 81.6† | 75.0† | 82.3† | 9.5† |
| Reasoning | 100.0* | 91.8@* | 83.3‡ | 80.1# | 13.4@* |

Total games: **10 + 16 + 12 + 30 + 54 = 122**.

---

## 3. Evaluation protocol (verbatim)

**System prompt (verbatim, in full):**

> "You are playing a text-based game and your goal is to finish it with the highest score. Upon reading the text observation, provide a *single* short phrase to interact with the game, e.g. `get lamp` (without the backticks). When stuck, try using the `help` command to see what commands are available."

> "**We do not provide other instructions to the LLMs on how to play the game** to assess LLMs' capabilities when not directed by a human expert with domain knowledge. This differs from other benchmarks such as Chang et al. (2024); Paglieri et al. (2024); Lu et al. (2025) which introduce significant inductive bias by providing the agent important information about the environments it would need to otherwise discover on its own. When calling the LLMs, **the observation and feedback are provided as the user inputs while the LLM actions are recorded as the assistant outputs.**"

**Two baseline agents (verbatim):** "**Zero-shot:** a basic agent that uses the prompt shown below; **Reasoning agent:** an agent that uses a reasoning model as the backbone with the same minimal prompt." (Footnote: "For DeepSeek-R1, we first generate the thinking traces then use a second query to generate an action.")

**Step cap and scoring (verbatim):**

> "For our results in the initial release of TALES, **we cap the number of steps the agents can take in any environment to 100** due to compute and monetary limitations. **Even though only 57% of the total score is achievable within 100 steps in Jericho, no agent approaches this score** (as we will discuss in Section 4.1). We believe 100 steps to be adequate to demonstrate the current scope of model reasoning capabilities. This number can easily be adjusted in TALES in the future. **TALES captures the model's capability evidence by the score from each game environment, ranging from 0-100.** Although each game environment has its own customized scoring rules, **those rules mark significant milestones in solving the game.**"

**Seeds / temperature / inclusion criterion (verbatim):**

> "For each game, **we repeat the experiment 5 times** due to the stochastic nature of LLMs, but find minimal changes in performance. When available, **we set the temperature equal to 0** and run multiple seeds to account for randomness within the environment. Per Section 3.1, **we only include models that could achieve at least 90% of the total score in the 100 step version of Simon Says with Memory.**"

### Simon Says — the gating unit test (verbatim, §3.1)

> "With the release of TALES, we also introduce a new TextWorldExpress game in the form of "**Simon Says**". […] The basic *Simon Says* simply provides the agent an action to repeat while *Simon Says With Memory* provides a list of actions to follow at the start of the game. **Both versions award a point for every correct action. The game restarts if any action is performed out of order or is wrong.** While outwardly trivial, we believe *Simon Says With Memory* serves as a good unit test for if an agent possesses sufficiently advanced reasoning to make meaningful progress through TALES. **A prerequisite to success in TALES is the ability to at least follow instructions over a long horizon task.**"

> "In this classic children's game, players must follow instructions only when prefaced with "Simon says" - making it fundamentally an **instruction-following task**. The simplest formulation of our text-adventure implementation gives the player a direct walkthrough of required actions, similar to the iconic copy task Graves et al. (2014) where models must reproduce given sequences. **Despite this programmatic simplicity, we find that even advanced models struggle with this straightforward instruction-following challenge. We discover that success in this elementary task strongly predicts (Pearson r = 0.83) a model's ability to make meaningful progress in the more complex environments of TALES.**"

★ **This is a load-bearing number for the platform: a pure, mechanically-scored instruction-following task correlates at r = 0.83 with downstream competence across 122 games.**

---

## 4. ★ MAIN RESULTS — Table 3 (verbatim, all 34 models)

Caption (verbatim): "Average scores per framework and average-per-game score. * Indicates LLM has only been run on one seed. We will update the paper once all run seeds have been completed."

| Model | TextWorld | TextWorldExpress | ALFWorld | ScienceWorld | Jericho | Average Score |
|---|---|---|---|---|---|---|
| claude-3.7-sonnet | 97.3 | 91.3 | 83.3 | 76.5 | 12.5 | **52.5** |
| claude-3.5-sonnet-latest | 95.5 | 81.6 | 75.0 | 82.3 | 9.6 | **50.4** |
| gemini-2.5-pro-preview* | 100.0 | 91.8 | 75.0 | 64.2 | 13.4 | **49.3** |
| o1 | 97.8 | 70.2 | 28.3 | 80.1 | 10.3 | **44.2** |
| gpt-4o | 83.6 | 80.6 | 56.7 | 61.4 | 5.6 | **40.6** |
| claude-3.5-haiku | 94.9 | 79.8 | 26.7 | 67.3 | 5.0 | **39.6** |
| Llama-3.1-405B-Instruct | 90.9 | 79.2 | 31.7 | 51.8 | 6.1 | **36.4** |
| gemini-2.0-flash* | 70.6 | 74.5 | 20.0 | 57.6 | 5.1 | **34.0** |
| Llama-3.3-70B-Instruct | 69.6 | 77.2 | 15.0 | 55.1 | 4.5 | **32.8** |
| Llama-3.1-70B-Instruct | 65.6 | 81.9 | 8.3 | 51.9 | 5.3 | **32.0** |
| Qwen2.5-72B-Instruct | 76.5 | 83.8 | 36.7 | 35.0 | 2.9 | **30.7** |
| Mistral-Large-Instruct-2407 | 82.4 | 68.3 | 6.7 | 46.1 | 5.8 | **30.3** |
| o3-mini | 83.2 | 61.1 | 11.7 | 48.4 | 4.5 | **29.9** |
| gpt-4o-mini | 56.5 | 73.6 | 0.0 | 27.2 | 1.8 | **21.8** |
| Llama-4-Scout-17B-16E-Instruct | 41.1 | 68.4 | 0.0 | 27.0 | 1.8 | **19.8** |
| Llama-4-Maverick-17B-128E-Instruct | 43.5 | 56.1 | 8.3 | 11.5 | 2.0 | **15.5** |
| Mistral-Small-Instruct-2409 | 56.1 | 27.3 | 0.0 | 24.4 | 1.4 | **14.8** |
| Llama-3.1-8B-Instruct | 29.7 | 50.3 | 0.0 | 15.7 | 2.3 | **13.9** |
| DeepSeek-R1 | 37.1 | 38.6 | 0.0 | 15.8 | 1.0 | **12.4** |
| Qwen2.5-7B-Instruct | 27.7 | 45.6 | 0.0 | 12.6 | 0.7 | **11.7** |
| Llama-3.2-3B-Instruct | 21.4 | 42.0 | 0.0 | 10.0 | 1.5 | **10.4** |
| phi-4 | 20.8 | 43.8 | 0.0 | 8.9 | 1.6 | **10.3** |
| Mistral-Small-24B-Instruct-2501 | 15.8 | 23.0 | 0.0 | 15.8 | 1.4 | **8.8** |
| DeepSeek-R1-Distill-Llama-70B | 8.7 | 39.8 | 0.0 | 7.7 | 1.3 | **8.4** |
| Ministral-8B-Instruct-2410 | 10.9 | 22.8 | 0.0 | 2.3 | 0.4 | **4.6** |
| Mistral-Small-3.1-24B-Instruct-2503 | 2.5 | 10.3 | 0.0 | 10.5 | 0.8 | **4.5** |
| Mixtral-8x22B-Instruct-v0.1 | 17.1 | 8.4 | 0.0 | 4.0 | 0.4 | **3.7** |
| Llama-3.2-1B-Instruct | 0.0 | 19.0 | 0.0 | 2.4 | 0.6 | **3.3** |
| Phi-3-mini-128k-instruct | 2.7 | 9.4 | 0.0 | 2.4 | 0.3 | **2.2** |
| Phi-3.5-MoE-instruct | 0.0 | 7.0 | 0.0 | 2.3 | 0.4 | **1.7** |
| Phi-4-mini-instruct | 0.0 | 5.5 | 0.0 | 2.3 | 0.5 | **1.5** |
| Mixtral-8x7B-Instruct-v0.1 | 0.0 | 1.6 | 0.0 | 4.0 | 0.3 | **1.3** |
| Phi-3.5-mini-instruct | 0.0 | 2.0 | 0.0 | 2.4 | 0.5 | **1.0** |
| Phi-3-medium-128k-instruct | 0.0 | 0.0 | 0.0 | 2.3 | 0.3 | **0.7** |

### Key structural facts in this table

- **Jericho (human-written games) collapses.** Best Jericho score across all 34 models is **13.4** (gemini-2.5-pro-preview, one seed) and **12.5** (claude-3.7-sonnet, full seeds). Every model is below 15 — hence the abstract's headline claim. Meanwhile the same models hit **97.3–100.0** on TextWorld.
- **The synthetic/human gap for claude-3.7-sonnet is 97.3 → 12.5**, a ~7.8× drop, on the *same* agent with the *same* prompt.
- **ALFWorld is bimodal:** 17 of 34 models score exactly **0.0**. Its terminal-only reward and uninformative feedback ("Nothing happens") make it all-or-nothing.
- **Reasoning models do not dominate.** DeepSeek-R1 averages **12.4**, below Llama-3.1-8B-Instruct (13.9) and far below claude-3.5-haiku (39.6). o3-mini (29.9) sits below gpt-4o (40.6).
- Other tables in the paper (not reproduced in full here): **Table 2** (max score % reached by following the walkthrough for each Jericho game), **Table 4** (avg final tokens used per LLM per game per framework), **Table 5** (standard deviation statistics per LLM), **Table 6** (games organized by framework), **Tables 7–12** (per-game breakdowns for TextWorld / TextWorldExpress / ALFWorld / ScienceWorld / Jericho parts 1–2). Per-game data for ScienceWorld (30 tasks) and Jericho (54 games) is available in the HTML full text and in the repo's leaderboard.

---

## 5. Qualitative failure analysis (verbatim) — these are state-tracking failures

The paper's analysis section is unusually explicit that the dominant failure mode is **failure to track state from environment feedback** — i.e. exactly the machine-checkable dimension.

**On compositional cascade (§2, verbatim):**

> "Within longer contexts, these reasoning skills often become compositional with a failure in one skill leading to failures in the others later on. […] the agent **not realizing it failed to pick up lead in one step leads to further failures later on** when attempting to use the object the agent had previously failed to pick up."

> "Lacking a specific reasoning skill would lead to task failure as **the error will cascade and be difficult to recover.**"

**On ALFWorld — inability to infer rules from feedback (verbatim, §4.2):**

> "**LLMs often fail to discover implicit game dynamics through inductive reasoning.** We find **even the top agents are unable to infer environment rules that are not explicitly provided.** When the agent is holding an object and tries to pick up another object, rather than an informative error message that explains that the player can only hold one object at a time, the ALFWorld environments simply reply with *nothing happened*. ALFWorld returns this feedback if the action fails for any reason, including the case when the action fails to be parsed, and when the action is not possible in the current state. **The most common failure mode resulting from this is when an agent picks up an object tangentially related to the task but fails to realize it must put the original object down before picking up another one**, often the actual object needed for the task."

> "**Distractor objects significantly hinder LLMs with weaker deductive reasoning.** […] In any ALFWorld game, there are a large enough number of distractor receptacles and objects that if the agent attempts to interact with every distractor, it will quickly hit the maximum number of steps."

**On ScienceWorld — failure to process feedback in long contexts (verbatim, §4.3):**

> "**Increased environmental complexity severely degrades agent reasoning capabilities beyond what performance metrics alone indicate.** We find the increase in environment complexity from ALFWorld to ScienceWorld to result in a significant drop in reasoning ability across all models. **This is not obvious from the scores alone.** […] For example, ScienceWorld provides **26 possible commands templates** when the help command is called where ALFWorld only has **13**. ALFWorld has an average gold trajectory length of **5.83** where ScienceWorld has an average gold trajectory length of **41.67**."

> "**LLM agents struggle with processing feedback in longer contexts.** The most common inductive reasoning failure mode we found in ScienceWorld were **agents not accounting for the feedback from their action.** We see this across all agents in ScienceWorld as a result of the previously discussed degradation in reasoning across the board. For example, **an agent failing to pick up an object due to a syntactically incorrect action phrase but then leaving the location without any additional attempts.**"

**Ambiguity of failure attribution (verbatim, §4.1)** — relevant caveat:

> "**Failures in grounded reasoning are more ambiguous to classify** versus the other types of reasoning as it is a reasoning mode that is typically done compounded with or alongside another reasoning skill. For example, a failure to navigate from one location to another could be a spatial reasoning failure in planning out an incorrect route, or it could be a grounding reason failure in attempting to traverse from one location to another, not-connected location."

**Conclusion (verbatim, §6):**

> "The game transcripts from leading LLMs reveal that, despite their impressive language capabilities, **these models still struggle with core reasoning challenges inherent to text-adventure games.** The difficulty stems not only from long-horizon dependencies and implicit environmental cues but also from the need for sequential, exploratory, and commonsense reasoning—skills that remain a bottleneck for even state-of-the-art LLMs."

> "Overall, while progress has been made on synthetic text-adventure games, **LLM-driven agents are still far from being able to complete games meant to be played for simple, human enjoyment.**"

---

## 6. Framework notes worth carrying (verbatim)

- **TextWorld:** "CookingWorld" games from the NeurIPS 2018 Competition. "We selected one game per difficulty ranging from level 1 (with one location and a recipe of 1 ingredient) to level 10 (having 12 locations and a recipe with 3 ingredients). For all difficulties, the player receive 1 point after completing sub-goals related to the task in the game. **Difficulty level 1 can be solved in 7 moves with a max score of 3, while level 10 requires 44 moves with a max score of 11.**"
- **TextWorldExpress:** "runs approximately **three orders of magnitudes faster** compared to the TextWorld counterparts." Drawback: "**stricter parser** […] does not allow for nearest-neighbor action phrases."
- **ALFWorld:** "All tasks provide only a **terminal reward of 1** upon task completion." "The ALFWorld environments are unique in their **lack of informative feedback** […] ALFWorld has only one error message in the form of *Nothing happens*." "an agent in ALFWorld can only hold one object at a time."
- **ScienceWorld:** "**emulates an open-world setting where the player can complete the task in different ways that do not follow one expected trajectory.**" "ScienceWorld also allows the player the freedom to reset the game on command. This is especially important as a number of ScienceWorld games have **dead states** where it is no longer possible to complete the assigned task in that play-through."
- **Jericho:** "a suite of **54** […] human-written, interactive fiction games." Footnote: "**We exclude hollywood.z3 because of segfault errors and threatre.z5 due to game engine errors.**" "We consider Jericho to be the most difficult framework due to the length and complexity of many of the games. **Some can be completed within 17 steps while some others require over 500 steps.** These games also cover an extremely wide range of genres and styles and **lack the consistency** of many other text-game environment suites designed for evaluating agents. For example, *9:05* follows the morning of an ordinary office worker where *Anchorhead* is a Lovecraftian Horror Story."

---

## Relevance to companion-eval-platform

### (a) Is the LLM a PLAYER or a SIMULATOR/GAME MASTER?

**The LLM is a PLAYER.** Unambiguously and by design.

- The **simulator is the game engine** — TextWorld, TextWorldExpress, ALFWorld, ScienceWorld, and Jericho's Z-machine interpreter. These are deterministic, executable programs that own the state, adjudicate every action, and emit the score. The LLM never touches state.
- The LLM's entire contribution is one string per turn: "provide a *single* short phrase to interact with the game." The engine parses it, accepts or rejects it, transitions state, and returns feedback plus score. This is a **pure actor** setup.
- The paper is explicit that the constraints are external and inviolable: "grounded environments, **where the causal constraints between actions are fixed and cannot be violated.**"

**This makes TALES the exact mirror-image of `game-bytesized32-state-prediction.md`** (LLM *as* simulator, predicting state transitions) — and the pair is more useful than either alone. Together they bracket the platform's design space:

| | LLM's role | Who owns state | What's measured |
|---|---|---|---|
| **ByteSized32-SP** (2024) | **SIMULATOR** | the LLM | does the LLM's predicted next state match the engine's? |
| **TALES** (2025) | **PLAYER** | the engine | does the LLM's action sequence reach engine-scored milestones? |

A companion/roleplay system is neither cleanly — it is a **game master**: it must voice characters (player-like) *and* own the world state (simulator-like). TALES supplies the sobering player-side prior; ByteSized32-SP supplies the simulator-side prior. Both are bad news, and both are **countable**.

### (b) Is ground-truth state available and mechanically checkable?

**YES — total, deterministic, and free.** This is TALES's whole value proposition to the platform.

- **The engine is the oracle.** Every one of the 122 games is an executable simulator with an internal state the agent cannot corrupt. Score is emitted by the engine, not inferred: "TALES captures the model's capability evidence by the score from each game environment, ranging from 0-100." No rubric, no rater, no judge, no drift.
- **Rule-following is checked by the parser**, not by opinion. Invalid action phrases are rejected mechanically, and the environment distinguishes "parser didn't understand" from "understood but impossible" — a **free, automatic, per-turn legality signal**. (ALFWorld deliberately collapses this distinction to "Nothing happens", and that single design choice is why 17/34 models score 0.0 on it — a beautifully clean demonstration that *feedback informativeness* is itself a measurable independent variable.)
- **Reliability is engineered in:** temperature 0, **5 repeats per game**, multiple seeds, and a published per-model **standard deviation table (Table 5)**. Contrast with human roleplay-quality α = 0.25–0.34: here the measurement instrument has essentially zero rater variance, and the paper still bothers to quantify the residual stochasticity.
- **Ground truth extends to the optimal path.** Every game ships a **walkthrough** (gold trajectory), which the authors use to compute both `Avg. walkthrough length` (Table 1) and the fraction of max score reachable in N steps (Table 2: "only 57% of the total score is achievable within 100 steps in Jericho"). This means **partial credit is principled**, not vibes — you can measure how far along a known-correct path an agent got.

### Why this matters for the platform's core thesis

**1. TALES is proof that a mechanically-scored dimension still discriminates sharply — and doesn't saturate.** The 34-model spread runs 0.7 → 52.5 with clean, monotone, reproducible ordering. Nobody had to agree on what "good" means. Compare the aesthetic dimensions where α = 0.25–0.34 and rankings are unstable: here, the ranking *is* the arithmetic.

**2. Simon Says (r = 0.83) is the single most actionable finding for the platform.** A trivially simple, fully-mechanical, instruction-following unit test — *echo this action sequence in order; you restart if you get one wrong* — predicts downstream competence across 122 complex games at **Pearson r = 0.83**. And the authors use it as a **gate**, not just a metric: "we only include models that could achieve at least 90% of the total score in the 100 step version of Simon Says with Memory." This is a direct template for the platform: **a cheap, countable, objective screen can be both a strong proxy for expensive competence and an admission criterion.** A companion-eval analogue — does the model honor N committed constraints over a long horizon without violating one — would be equally cheap, equally objective, and worth validating against the same r. (Cross-ref: `game-ifeval.md`, `multiturn-multi-if.md`, `game-multi-if.md`.)

**3. The failure modes named in the qualitative analysis are precisely the platform's dimensions — and they are state-tracking failures, not taste failures.** "Agents **not accounting for the feedback from their action**"; "the agent **not realizing it failed to pick up lead** in one step leads to further failures later on"; "**fails to realize it must put the original object down** before picking up another one"; "**unable to infer environment rules that are not explicitly provided**." Every one of these is a *contradiction between the model's implicit world-state and the engine's actual world-state* — detectable by diffing against the oracle, with no aesthetic judgment involved. This is the companion-platform problem in a domain where you can *see* the answer. (Cross-ref: `game-entity-tracking.md`, `game-narrative-consistency.md`, `multiturn-time-to-inconsistency-survival.md`.)

**4. The Jericho cliff is the long-horizon warning.** Top models: 97.3 on synthetic TextWorld → **12.5** on human-written Jericho. The authors attribute this to long, sparse context: "all models struggle to reason across **extremely long-horizon contexts where important information is sparsely scattered throughout**." Jericho games are the closest thing in the suite to a companion session — long, human-authored, idiosyncratic, inconsistent in style, "meant to be played by humans, slowly and iteratively over extended periods of time." **The environments that most resemble open-ended human-authored interaction are exactly where LLMs fall off a cliff**, and the benchmark can prove it because the score is mechanical. (Cross-ref: `multiturn-lost-in-middle.md`, `multiturn-lost-in-conversation.md`, `multiturn-when-attention-closes.md`.)

**5. Two caveats to carry.** (i) The authors flag **"likely data contamination"** for Jericho/Zork-class games — canonical IF games and their walkthroughs are all over the pretraining corpus, so scores are, if anything, *optimistic*, which makes 12.5 worse than it looks. (ii) `gemini-2.5-pro-preview` and `gemini-2.0-flash` are **single-seed** (marked `*`), so their table entries carry more variance than the rest; the paper says it will update. Don't over-read gemini-2.5-pro's 13.4 Jericho or 100.0 TextWorld.

**6. Contrast with CICERO (`game-cicero-diplomacy.md`).** Both papers rest on the same load-bearing asymmetry: **the game side is mechanical, so only the language is in question.** CICERO exploited that asymmetry constructively — it computed a legal, machine-checkable plan outside the LM and then filtered the LM's natural language for consistency with it (rejecting ~53% of generations). TALES runs the experiment *without* that scaffolding ("minimal scaffolding", "no expert knowledge") and shows what a bare LLM does when nothing pins it to the state: **it loses track, and the engine notices.** Read together, they make the platform's argument end-to-end — the verifiable dimensions are the ones that discriminate, the ones you can filter on, and the ones that predict everything else.
