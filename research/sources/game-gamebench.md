---
title: "GAMEBENCH: Evaluating Strategic Reasoning Abilities of LLM Agents"
url: https://arxiv.org/abs/2406.06613
authors: Anthony Costarelli, Mat Allen, Roman Hauksson, Grace Sodunke, Suhas Hariharan, Carlson Cheng, Wenjie Li, Joshua Clymer, Arjun Yadav
year: 2024
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# GAMEBENCH: Evaluating Strategic Reasoning Abilities of LLM Agents

arXiv:2406.06613. HTML source consulted: https://arxiv.org/html/2406.06613v1

## Abstract (verbatim)

> "Large language models have demonstrated remarkable few-shot performance on many natural language understanding tasks. Despite several demonstrations of using large language models in complex, strategic scenarios, there lacks a comprehensive framework for evaluating agents' performance across various types of reasoning found in games. To address this gap, we introduce GameBench, a cross-domain benchmark for evaluating strategic reasoning abilities of LLM agents."

Headline findings, verbatim from the paper's own summary of results:

> "At worst GPT-4 performs worse than random action"

> "CoT and RAP both improve scores but not comparable to human levels"

None of the tested models matched human performance.

## The 9 games (Appendix F, verbatim descriptions)

1. **Air, Land, and Sea (ALS)** — "A war strategy game where players are Supreme Commanders fighting to control two of three areas (air, land, sea) by deploying limited Battle card forces each round."
2. **Arctic Scavengers (ARC)** — "A resource-management game in which players are the leader of a small tribe of survivors... pitted against each other in a fight for survival."
3. **Are You the Traitor? (AYT)** — "A social deduction game where players are secretly divided into Good and Evil teams... engaging in unstructured conversation trying to deduce the opposing team's critical roles."
4. **Codenames (CN)** — "A 2v2 cooperative game with one spymaster and one operative per team... spymasters create one-word clues that relate to multiple predetermined words from the grid."
5. **Hive (HV)** — "A strategy game occurring on a hexagonal grid... players try to coordinate their bugs in order to completely surround the enemy's queen bee."
6. **Pit (PT)** — "An every-person-for-themselves trading simulation... players must trade semi-blindly to try to obtain enough of any commodity to 'corner the market.'"
7. **Santorini (SN)** — "A strategy game in which two players take turns moving one of their two pawns on a five by five grid and building blocks on the grid."
8. **Two Rooms and a Boom (TRB)** — "A cooperative social-deduction game in which all players are split into two teams... red team's goal to end the game with the red-team bomber and blue-team president in the same room."
9. **Sea Battle (SB)** — "A 3v3 board game in which players' attempt to sink their opponents' ships and their movement and cannon-firing actions occur simultaneously."

## Strategic reasoning dimensions (Table 1, Section 3.2)

Each game covers at least one axis of a key reasoning skill identified in strategy games.

| Reasoning Category | Total | Games |
|---|---|---|
| Abstract Strategy | 6 | ALS, ARC, CN, HV, SN, SB |
| Non-Deterministic | 3 | ARC, TRB, SB |
| Hidden Information | 3 | ARC, AYT, TRB |
| Language Communication | 4 | AYT, CN, PT, TRB |
| Social Deduction | 2 | AYT, TRB |
| Cooperation | 4 | AYT, CN, SB, TRB |

## Scaffolding tested

**Chain-of-Thought (CoT)** — Appendix D. CoT-scaffolded agents are prompted, after viewing game state and available actions, with:

> "First, let's reason out loud about which action you should take to maximize your probability of winning"

**Reasoning via Planning (RAP)** — Appendix D:

> "GPT-4-RAP employs a Monte-Carlo tree search where states and actions are model predictions, and rewards are computed using next-token probabilities"

> "GPT-4-RAP was run with the default parameters from the llm-reasoners library except the Monte-Carlo tree search depth limit was set to 2 due to resource constraints."

Appendix E provides prompting templates for RAP covering action prediction, state transitions, and win-probability assessment via next-token probabilities.

Agents evaluated: `random`, `human`, `gpt-3`, `gpt-3-cot`, `gpt-4`, `gpt-4-cot`, `gpt-4-rap`.

## Results

### Table 2: Game Ratings (exponential Bradley–Terry skill ratings)

| Agent | Overall | ALS | ARC | AYT | CN | HV | PT | SN | TRB | SB |
|---|---|---|---|---|---|---|---|---|---|---|
| random | -0.50 | 1.07 | 0.48 | -2.52 | -2.67 | -1.15 | 0.63 | 0.37 | -0.79 | 0.05 |
| human | 1.76 | 1.49 | 0.45 | 1.92 | 1.26 | 3.63 | 1.29 | -0.89 | 1.70 | 1.25 |
| gpt-3 | -0.48 | 1.26 | -0.05 | -1.84 | -2.06 | 1.27 | 0.63 | -0.01 | -2.51 | -0.41 |
| gpt-3-cot | 0.06 | 0.03 | 0.22 | 2.42 | 0.45 | -0.44 | 0.63 | 0.53 | -2.76 | 0.26 |
| gpt-4 | -0.89 | -7.38 | -0.12 | -2.73 | -0.65 | -1.31 | -4.42 | -0.08 | 0.62 | -1.40 |
| gpt-4-cot | 0.16 | 2.13 | 0.27 | -0.19 | 2.41 | -1.13 | 0.63 | -0.53 | 1.22 | 0.62 |
| gpt-4-rap | -0.10 | 1.41 | -1.25 | 2.94 | 1.26 | -0.86 | 0.63 | 0.62 | 2.51 | -0.37 |

Key readings: `human` overall 1.76 is the top rating. Bare `gpt-4` overall -0.89 is **below** `random` at -0.50 — this is the "worse than random action" result. Scaffolding recovers it: `gpt-4-cot` 0.16, `gpt-4-rap` -0.10, `gpt-3-cot` 0.06 — all above random, all far below human.

### Table 3: Average Score (win rate / match score, 0–1)

| Agent | Overall | ALS | ARC | AYT | CN | HV | PT | SN | TRB | SB |
|---|---|---|---|---|---|---|---|---|---|---|
| random | 0.49 | 0.72 | 0.60 | 0.25 | 0.18 | 0.41 | 0.50 | 0.56 | 0.52 | 0.58 |
| human | 0.85 | 1.00 | NaN | NaN | NaN | 1.00 | 1.00 | 0.43 | NaN | 0.78 |
| gpt-3 | 0.48 | 0.64 | 0.43 | 0.43 | 0.63 | 0.80 | 0.50 | 0.47 | 0.27 | 0.40 |
| gpt-3-cot | 0.60 | 0.43 | 0.50 | 0.93 | 0.89 | 0.60 | 0.50 | 0.61 | 0.33 | 0.55 |
| gpt-4 | 0.31 | 0.00 | 0.42 | 0.33 | 0.83 | 0.33 | 0.31 | 0.42 | 0.71 | 0.20 |
| gpt-4-cot | 0.60 | 0.81 | 0.50 | 1.00 | 1.00 | 0.50 | 0.50 | 0.37 | 0.75 | 0.51 |
| gpt-4-rap | 0.62 | NaN | 0.33 | 1.00 | NaN | 0.50 | NaN | 0.58 | 1.00 | 0.26 |

Note the `NaN` cells: coverage is not uniform. Human data in particular is missing for ARC, AYT, CN, and TRB, and `gpt-4-rap` is missing ALS, CN, PT. Overall human average of 0.85 is therefore computed over a *different, easier* subset of games than the model averages. This is a real comparability defect in the headline "no model matches human" claim.

## Rating methodology (verbatim)

The benchmark employs:

> "the exponential Bradley–Terry model"

chosen over Elo because it "assumes model skill does not change over time and it does not need to be calculated in a decentralized manner."

Bootstrapping:

> "we perform bootstrapping on the sample S for B=10,000 times"

with weighted sampling inversely proportional to match counts per game.

Match volume (verbatim):

> "not uniform across games nor against agent-pairs due to resource constraints. In general, we preferred playing agents against the random baseline and preferred games that didn't take too long to complete."

## RULES ENFORCED BY A GAME ENGINE — explicit note

**Yes, rules are enforced by a programmatic game engine.** Verbatim from the implementation section:

> "Each environment, implemented in Python, describes a Game object with methods for initializing, retrieving the game's current state and available actions, updating the state with an action, and executing a full match between two agents."

> "Agents are objects that describe a method for choosing an action conditioned on the rules, state, and available actions retrieved from a Game instance."

> "Agents are instantiated at the beginning of a match and destroyed at the end, so agents may maintain persistent state between moves to choose an action."

**Are illegal/invalid moves counted or filtered? — FILTERED BY CONSTRUCTION, AND NOT MEASURED.**

This is the single most important methodological fact for our purposes, and it must be stated precisely:

- The engine **hands the agent a list of `available actions`** retrieved from the `Game` instance. The agent selects from that enumerated legal set rather than emitting a free-form move that the engine then validates. Illegal moves are therefore **structurally prevented, not detected**.
- **The paper does not report an invalid-action rate, an illegal-move count, or a parse-failure rate anywhere.** It does not document move validation, filtering, retry, random fallback, or forfeit penalties for rule violations. I checked the implementation section, the results tables, and the limitations section specifically for this; it is absent.
- Consequence: **rule adherence is not a measured dimension in GAMEBENCH.** The benchmark measures *choice quality within a pre-validated legal action set*, not *ability to stay inside the rules*. A model that would constantly attempt illegal moves in a free-generation setting would look identical to a compliant one here.
- This design choice is why bare `gpt-4` can score 0.00 on ALS (Table 3) without that being an illegality artifact — it lost legally.

Caveat on sourcing: the available-actions quote is verbatim from the paper; the inference that this structurally prevents illegal moves is mine, and the paper's silence on invalid-action handling means I cannot rule out an undocumented fallback in the released code. Treat "filtered by construction" as a strong reading of the architecture, not a claim the authors make.

## Limitations (verbatim)

> "We find it especially important to know how well these models fair compared to humans, but collecting comprehensive human data was out of our means"

> "Our benchmark has a respectable number of games and agents compared to other benchmarks... but the addition of more games and agents would provide a richer picture."

## Relevance to companion-eval-platform

Our core finding is that aesthetic judgments of roleplay quality are unstable — human Krippendorff alpha of 0.25–0.34 — so we prefer dimensions with objective, countable, verifiable correlates. GAMEBENCH is instructive both for what it offers and for what it conspicuously does not.

**(a) Is the LLM a PLAYER or a SIMULATOR / GAME MASTER? — PLAYER, unambiguously.**

The LLM is a competitor inside an environment it does not author. The `Game` object owns initialization, state, legal-action enumeration, state transition, and match execution; the `Agent` object only implements "a method for choosing an action." The game master role is played entirely by deterministic Python. This is the **inverse** of our setting, where the LLM *is* the game master — it narrates world state, adjudicates what the user can do, and maintains character and continuity. GAMEBENCH tells us nothing directly about simulator fidelity, because it never asks a model to hold a world together. Its social-deduction and language-communication games (AYT, CN, PT, TRB) are the closest analogues — they involve unstructured conversation and cooperation — but even there the LLM is a participant in the fiction, not its custodian.

**(b) Is ground-truth state available and mechanically checkable? — YES, completely, and this is the transferable lesson.**

Every game has full programmatic ground truth: the Python `Game` object holds authoritative state, and win/loss is decided by the engine, not by a judge. Outcome is countable with zero rater involvement, which is exactly the property our alpha 0.25–0.34 problem demands. The Bradley–Terry + 10,000-sample bootstrap rating machinery is a directly reusable pattern for turning pairwise outcomes into scores with uncertainty intervals — and it pairs with `psycho-elo-bradley-terry.md` in this corpus.

**What to take, and what to be careful about:**

1. **The strongest signal here is a negative result we can exploit.** Bare `gpt-4` scoring *below random* (rating -0.89 vs -0.50; average score 0.31 vs 0.49) is only legible because the outcome was mechanically decided. No panel of judges would have produced that finding cleanly. This is the argument for objective correlates in miniature: mechanical ground truth surfaces failures that aesthetic judgment smooths over.
2. **Do not cite GAMEBENCH as evidence for rule-adherence measurement.** It is tempting — games have rules, an engine enforces them — but the enumerated-action-list design means the benchmark never observes a rule violation. If we want to measure whether our game-master model keeps its own world's rules, GAMEBENCH offers the *engine* pattern but not the *measurement* pattern. The measurement design (free generation + engine validation + counted violation rate) is something we would have to add ourselves, and it is arguably the more valuable half.
3. **Treat the human comparison as weak.** The `NaN` coverage gaps mean human 0.85 and model overalls are not computed over the same games. We should not reuse the "models don't match humans" framing without that caveat; it would import exactly the kind of unrigorous comparison our platform exists to avoid.
4. **Scaffolding sensitivity is a confound worth internalizing.** CoT moves gpt-4 from -0.89 to 0.16 and gpt-3 from -0.48 to 0.06. If a single prompt line reorders models this dramatically on an *objective* metric, our own objective metrics need scaffolding held fixed and reported, or we will measure prompt engineering and call it capability.

**Net verdict for our design:** GAMEBENCH is a strong precedent for *outcome-as-ground-truth* and a good citation for "mechanical adjudication surfaces what judges miss." It is a poor precedent for *rule-adherence-as-metric*, and citing it that way would be a misread. Our closest structural need — LLM-as-simulator with checkable state — is better served by `game-llm-sim-state-prediction.md` and by LMRL-Gym's programmatic-simulator tasks (`game-lmrl-gym.md`).
