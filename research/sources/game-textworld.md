---
title: "TextWorld: A Learning Environment for Text-based Games"
url: https://arxiv.org/abs/1806.11532
authors: Marc-Alexandre Côté, Ákos Kádár, Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine, James Moore, Matthew Hausknecht, Ruo Yu Tao, Layla El Asri, Mahmoud Adada, Wendy Tay, Adam Trischler (Microsoft Research; Tilburg University; McGill University)
year: 2018
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# TextWorld: A Learning Environment for Text-based Games

**Sourcing note:** all numbers below extracted from the arXiv PDF (`arxiv.org/pdf/1806.11532`, 29pp) via pypdf. **The ar5iv HTML rendering of Table 1 is corrupted** — it drops the `Avg. Steps` columns entirely and returns only 4 of 9 rows, with a fabricated column header ("BYU Score"). The real table is reproduced verbatim below. Do not cite the ar5iv version.

Workshop paper, Computer Games Workshop @ IJCAI 2018. Code: http://aka.ms/textworld

## Abstract (verbatim)

> We introduce TextWorld, a sandbox learning environment for the training and evaluation of RL agents on text-based games. TextWorld is a Python library that handles interactive playthrough of text games, as well as backend functions like state tracking and reward assignment. It comes with a curated list of games whose features and challenges we have analyzed. More significantly, it enables users to handcraft or automatically generate new games. Its generative mechanisms give precise control over the difficulty, scope, and language of constructed games, and can be used to relax challenges inherent to commercial text games like partial observability and sparse rewards. By generating sets of varied but similar games, TextWorld can also be used to study generalization and transfer learning. We cast text-based games in the Reinforcement Learning formalism, use our framework to develop a set of benchmark games, and evaluate several baseline agents on this set and the curated list.

## The state representation — this is the key contribution for our purposes

**Game state is a multiset of logical atoms in linear logic.** Verbatim (§3.1):

> Game states are defined in terms of logical predicates. Each predicate p(v1,...,vm) consists of a symbol p drawn from the alphabet of predicates Σ followed by an m-tuple of variables. These predicates define the relations between the entities (objects, player, room, etc.) present in the game. A logical atom is a predicate whose variables are all bound, i.e., free variables (placeholders) have been substituted by concrete entities. **A game state s∈S consists in a multiset of logical atoms representing the facts that are currently true about the world**, also known as "resources" in linear logic.

The worked example given (Figure 4):

```
s_t = at(fridge, kitchen) ⊗ at(table, kitchen) ⊗ in(apple, fridge)
      ⊗ open(fridge) ⊗ at(P, kitchen)
```

where `⊗` is the linear logic **multiplicative conjunction** operator.

**Winning conditions are a set of facts, checked by entailment:**

> The set of winning states G is composed of any state s for which all the winning conditions (a set of facts) hold. The winning conditions are determined during the game generation process. For instance, a winning condition could be as simple as `in(apple, I)`, i.e., the apple being in the player's inventory.

**State transition function:**

> The state transition function is defined using linear logic [Russell and Norvig, 2016, Ch. 8] and is inspired in part by Ceptre [Martens, 2015], a linear logic programming language.

Linear-logic rules *consume* the resources on the left of the `⊸` and *produce* those on the right — so state changes are resource-exact rather than monotonic, which is what makes inventory/container semantics correct by construction.

## Architecture (§3, Figure 3)

Two main components:
- **Generator** — samples a game definition (map, objects, quest, descriptions) from a knowledge base of object types (Door, Container, Supporter, Food item, ...), actions (Open, Take, Eat, Put, ...), predicates (`at`/`in`/`on`, `edible`, `north_of`, `open`/`closed`, ...), and themes (Medieval world; Home world).
- **Engine** — handles interactive play.

Pipeline (verbatim from Fig. 3 caption):

> Given some knowledge base, sampled game definitions are first converted to Inform 7 code and compiled into a Glulx executable file. Then, agents interact with the game by communicating with the Git-Glulx interpreter via TextWorld.

**Validity guarantee at generation time:**

> Game generation in TextWorld relies on a simple inference engine that ensures game validity at every step in the generation process. **A game is said to be valid if it is possible to reach the end goal from the initial state.**

This is worth pausing on: the generator *proves* winnability before emitting the game. Contrast with ByteSized32 (`game-bytesized32.md`), where an LLM authors the game and winnability drops to 30–37% and had to be checked by a human expert.

## Ground truth exposed to the researcher

TextWorld exposes, for **generated** games:

- **Exact state tracking** — the full multiset of true facts at every turn (not an approximation; it is the engine's own representation).
- **Admissible commands** — verbatim: *"commands that actually change the underlying state s_t"*; elsewhere defined as a list of commands guaranteed (i) to be understood by the interpreter and (ii) to affect the game state.
- **Ground truth winning policy** — a command sequence guaranteed to win from the current state.
- **Intermediate rewards** — verbatim: *"instead of earning rewards only at the end of a game if the agent is successful, one can also provide intermediate rewards during training based on environment state transitions and the ground truth winning policy."*
- **Quest objectives** as natural language.

**Critical caveat, verbatim (§3):**

> TextWorld can also be used to play existing text-based games (see a curated list of games in Section 5.1) but **provides more limited information from the internal states of such games.**

So the full ground-truth story holds for *generated* games only. For the 50 hand-authored curated games, TextWorld is closer to Jericho (see `game-jericho.md`).

## Difficulty / curriculum control

Generation is parameterized by: *"the map size, the number of objects, quest length and complexity, richness of text descriptions, and more."* Also available: restricting agent vocabulary to in-game words only; restricting verbs to those the parser understands; a simplified grammar replacing object names with symbolic tokens (e.g. *"You see container1 and container2."*); and converting any generated game into a **choice-based** game where the agent outputs an index into the admissible-command set rather than a word sequence.

## Benchmark 1: Curated List (§5.1)

50 hand-authored text games, adapted from Fulda et al. (2017) — 20 of the original 50 were replaced *"which were either parodies of text-based games or did not provide scores."*

Three baselines: **BYU** (Fulda et al. 2017), **Golovin** (Kostka et al. 2017), both submitted to the Text-Based Adventure AI Competition; and **Simple**, which samples uniformly from a predefined command set at every step. The exact Simple set (footnote 7): `north, south, east, west, up, down, look, inventory, take all, drop, YES`.

Protocol: 1000 steps per agent per game; losing resets the game and play resumes until the step budget is exhausted.

Results (Figure 9, normalized score = max score achieved / game's max possible score). The paper reports these as a figure, not a table; the verbatim characterization is:

> Unsurprisingly, agents achieve a rather low score on a few games and zero on many.

Two diagnostic notes the authors give, both of which are cautions about score-as-signal:

> For instance, in **Advent** the player starts with 36 points, which explains why all three baselines have the same score.

> As another example, the **Detective** game can be solved with mostly navigational commands. This explains why the **Simple** agent performs relatively well, since the commands it samples from are mostly navigational.

## Benchmark 2: Treasure Hunter (§5.2)

Adapted from Parisotto & Salakhutdinov (2017). Agent spawns in a randomly generated maze, an "indicator" object near the start determines which of two objects it must retrieve. Positive reward for the correct object, negative for the wrong one.

Stated aims: *"affordance extraction (agents should determine verb-noun pairs that change the environment state); efficient navigation (agents should avoid revisiting irrelevant rooms); and memory (agents should remember which object to retrieve)."*

Difficulty levels:
- **1 to 10:** Mode easy, #rooms = 5, quest length linearly increasing from 1 to 5
- **11 to 20:** Mode medium, #rooms = 10, quest length linearly increasing from 2 to 10
- **21 to 30:** Mode hard, #rooms = 20, quest length linearly increasing from 3 to 20

Modes:
- **Easy:** Rooms all empty except where the two objects are placed; connections between rooms have no door.
- **Medium:** Rooms may be connected by closed doors. Container objects added, might need to be opened to find the object.
- **Hard:** Locked doors and containers added which may need to be unlocked (and opened) to reach the object.

### Table 1: Model performance on one-life treasure hunter tasks (VERBATIM)

| | Random Avg. Score | Random Avg. Steps | BYU Avg. Score | BYU Avg. Steps | Golovin Avg. Score | Golovin Avg. Steps |
|---|---|---|---|---|---|---|
| level 1 | 0.35 | 9.85 | 0.75 | 85.18 | 0.78 | 18.16 |
| level 5 | -0.16 | 19.43 | -0.33 | 988.72 | -0.35 | 135.67 |
| level 10 | -0.14 | 20.74 | -0.04 | 1000 | -0.05 | 609.16 |
| level 11 | 0.30 | 43.75 | 0.02 | 992.10 | 0.04 | 830.45 |
| level 15 | 0.27 | 63.78 | 0.01 | 998 | 0.03 | 874.32 |
| level 20 | 0.21 | 74.80 | 0.02 | 962.27 | 0.04 | 907.67 |
| level 21 | 0.39 | 91.15 | 0.04 | 952.78 | 0.09 | 928.83 |
| level 25 | 0.26 | 101.67 | 0.00 | 974.14 | 0.04 | 931.57 |
| level 30 | 0.26 | 108.38 | 0.04 | 927.37 | 0.04 | 918.88 |

**Read this table carefully — it is a cautionary result, not a success story.** Random beats both engineered agents on *every level except level 1*. At levels 5 and 10 both BYU and Golovin score *negative* (they fetch the wrong object) while burning ~1000 steps (the full budget) versus Random's ~20. Random scores high partly because it dies fast and the one-life scoring rewards that.

The paper's own framing: beyond the predefined difficulty levels, the benchmark *"can be simplified by letting the agent directly tap into the game state information (e.g., feedback, description, inventory and objective) or using a simpler grammar."*

## Relevance to companion-eval-platform

### Is the LLM the PLAYER or the SIMULATOR/GAME MASTER?

**Neither, in the original paper — and that is exactly why TextWorld matters to us.** The 2018 paper predates LLM agents; the agents evaluated (BYU, Golovin, Simple) are hand-engineered RL/heuristic systems. **TextWorld itself is the simulator**, and it is a *non-learned* one: a linear-logic inference engine plus Inform 7 compiled to Glulx. No model is anywhere near the world state.

What TextWorld provides is therefore not a benchmark result we care about — it is **an existence proof of the artifact we would need to build**: a text-mediated interactive fiction whose entire world state is a machine-readable set of logical atoms, where "did the narration contradict the world" is a set-membership test rather than a judgment call.

TextWorld later appears *as an environment inside* LLM benchmarks — see `game-balrog.md` (where it is one of six environments; GPT-4o and Claude 3.5 Sonnet lead, Gemini scores 0% because the API flags the prompts as unsafe) and `game-tales.md` (where claude-3.7-sonnet reaches 97.3 on TextWorld and 12.5 on Jericho). In those, the LLM is the **PLAYER**.

### Is ground-truth state available and mechanically checkable?

**Yes — the strongest form in the corpus, for generated games.** The state *is* a set of logical atoms; the goal *is* a conjunction of facts; goal satisfaction *is* entailment. There is no rater, no rubric, no sampling. For **curated/existing** games, no — the paper says explicitly that TextWorld "provides more limited information from the internal states of such games."

### Why this matters given α = 0.25–0.34 on roleplay quality

The direct import is the **fact-multiset as the ground-truth substrate**. If a companion's world state (what the character knows, holds, has been told, has promised) is maintained as a multiset of atoms, then:
- "the character claimed to hold X" → `in(X, I)` ∈ s? — a set-membership test, α is undefined because there are no raters
- "the character referenced a room it never entered" → `at(P, room)` ever true? — a trace query
- "the character contradicted an earlier established fact" → `p` and `¬p` both derivable? — a consistency check

These are the countable correlates the platform wants. The catch, and it is the honest one: TextWorld gets this **only because it generates the world first and narrates it second.** The predicates are primary; the prose is a rendering of them via context-free grammar. A companion product does the reverse — prose is primary and any state model is a post-hoc extraction, which reintroduces exactly the extraction error that the logical representation was supposed to eliminate. The lesson to carry is architectural (author the state, render the text) rather than metric.

### Two cautions this paper hands us

1. **Advent gives all three agents 36 points because the player *starts* with 36.** A score that is objective can still be entirely uninformative. Objectivity is necessary, not sufficient — we need the metric to *move* with the thing we care about.
2. **Random beats both engineered agents at 8 of 9 Treasure Hunter levels**, because dying fast is rewarded under one-life scoring. This is the same failure ScienceWorld shows on Task 4-2 (Random 0.63 > DRRN 0.56, see `game-scienceworld.md`). Two independent papers in this lineage produced a mechanically-checkable metric that a random agent tops. **Before we ship any countable dimension, the required sanity check is: what does a null/random/trivial companion score on it?** If a degenerate baseline scores well, the metric is measuring an artifact of the protocol, not the construct.

### Lineage note

Côté is the common author across TextWorld, ALFWorld, ScienceWorld, ByteSized32, ByteSized32-State-Prediction, and TALES. This is one research program, and its arc is worth noting: it starts (2018) with *the simulator is a logic engine and the agent is dumb*, and arrives (2024) at *the LLM is asked to be the simulator and gets 59.9%* (`game-bytesized32-state-prediction.md`). That trajectory is the argument for why simulator-side evaluation is the open problem.
