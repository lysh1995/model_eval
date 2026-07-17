---
title: "Interactive Fiction Games: A Colossal Adventure (Jericho)"
url: https://arxiv.org/abs/1909.05398
authors: Matthew Hausknecht, Prithviraj Ammanabrolu, Marc-Alexandre Côté, Xingdi Yuan (Microsoft Research; Georgia Institute of Technology)
year: 2020
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# Interactive Fiction Games: A Colossal Adventure (Jericho)

**Sourcing note:** all numbers extracted from the arXiv PDF (`arxiv.org/pdf/1909.05398`, 20pp) via pypdf and **independently verified against the ar5iv HTML** — the two agree exactly on Table 1 and on the normalized progress scores. (This is worth recording because the same check *failed* for TextWorld's Table 1 and ALFWorld's Table 2, where ar5iv silently corrupted the tables.)

Published AAAI 2020. Code: https://github.com/microsoft/jericho

## Abstract (verbatim)

> A hallmark of human intelligence is the ability to understand and communicate with language. Interactive Fiction games are fully text-based simulation environments where a player issues text commands to effect change in the environment and progress through the story. We argue these games are an excellent testbed for studying language-based autonomous agents. In particular, IF games combine challenges of combinatorial action spaces, language understanding, and commonsense reasoning.

## What Jericho is

A lightweight Python interface connecting learning agents to **Z-Machine story files** (.z3/.z5) through a Gym-like API. **32 human-made IF games** spanning dungeon crawl, science fiction, mystery, comedy, and horror — including classic Infocom titles (Zork, Hitchhiker's Guide to the Galaxy) and community-created games (Anchorhead, Afflicted).

Contrast with TextWorld (`game-textworld.md`): these are games *written by humans for humans*, not generated. Vastly more linguistic variety and a much larger action space — but correspondingly less introspectable state.

## The handicaps — this is the mechanically-checkable part

Jericho provides five handicaps:

1. **Fixed random seed** — enforces determinism
2. **Load/Save functionality** — enables state restoration
3. **Game-specific templates and vocabulary** extraction
4. **World object tree** — auxiliary state representation showing possession relationships and object nesting
5. **World-change detection** (Algorithm 1) — systematically tests template+vocabulary combinations against the world object tree to identify valid actions

Verbatim, what these amount to:

> ground-truth identification of player location, ground-truth detection of the objects present at the player's location, and world-change-detection.

**Note precisely what this is and is not.** It is *not* TextWorld's full logical state. It is a set of extractions from the Z-Machine's memory: the object tree, the player's location, and a diff-based test for whether a candidate action changed anything. Valid-action identification works by *executing* candidate template+vocab combinations against a saved state and checking whether the object tree changed — i.e. ground truth by brute-force simulation and rollback, not by reading a declarative state. This is a genuinely different (and cheaper to retrofit) technique than TextWorld's, and it is the one that ports to an environment you did not author.

## Experiments (§6)

Agents evaluated:
- **RAND** — uniformly samples from canonical actions: `{north, south, east, west, up, down, look, inventory, take all, drop, yes}`
- **NAIL** — general IF agent, uses **no handicaps, no training period, plays each game for a single episode**
- **TDQN** — template-based DQN, estimates Q-values over full space of templates × vocabulary words
- **DRRN** — choice-based, estimates Q-values only over pre-identified valid actions

Protocol (verbatim):

> Five separate DRRN and TDQN agents were trained for each game. No environment seeds were set so environments remained stochastic throughout. We compute the score for each agent by averaging return over the last hundred episodes of learning. Hyperparameters for TDQN and DRRN were optimized on Zork1 then held fixed across games.

### Table 1: Raw scores across Jericho supported games (VERBATIM)

`|T|` = number of templates, `|V|` = size of parser's vocabulary. †Advent starts with a score of 36.

| Game | \|T\| | \|V\| | RAND | NAIL | TDQN | DRRN | MaxScore |
|---|---|---|---|---|---|---|---|
| 905 | 82 | 296 | 0 | 0 | 0 | 0 | 1 |
| acorncourt | 151 | 343 | 0 | 0 | 1.6 | 10 | 30 |
| advent† | 189 | 786 | 36 | 36 | 36 | 36 | 350 |
| adventureland | 156 | 398 | 0 | 0 | 0 | 20.6 | 100 |
| afflicted | 146 | 762 | 0 | 0 | 1.3 | 2.6 | 75 |
| anchor | 260 | 2257 | 0 | 0 | 0 | 0 | 100 |
| awaken | 159 | 505 | 0 | 0 | 0 | 0 | 50 |
| balances | 156 | 452 | 0 | 10 | 4.8 | 10 | 51 |
| deephome | 173 | 760 | 1 | 13.3 | 1 | 1 | 300 |
| detective | 197 | 344 | 113.7 | 136.9 | 169 | 197.8 | 360 |
| dragon | 177 | 1049 | 0 | 0.6 | -5.3 | -3.5 | 25 |
| enchanter | 290 | 722 | 0 | 0 | 8.6 | 20.0 | 400 |
| gold | 200 | 728 | 0 | 3 | 4.1 | 0 | 100 |
| inhumane | 141 | 409 | 0 | 0.6 | 0.7 | 0 | 90 |
| jewel | 161 | 657 | 0 | 1.6 | 0 | 1.6 | 90 |
| karn | 178 | 615 | 0 | 1.2 | 0.7 | 2.1 | 170 |
| library | 173 | 510 | 0 | 0.9 | 6.3 | 17 | 30 |
| ludicorp | 187 | 503 | 13.2 | 8.4 | 6 | 13.8 | 150 |
| moonlit | 166 | 669 | 0 | 0 | 0 | 0 | 1 |
| omniquest | 207 | 460 | 0 | 5.6 | 16.8 | 5 | 50 |
| pentari | 155 | 472 | 0 | 0 | 17.4 | 27.2 | 70 |
| reverb | 183 | 526 | 0 | 0 | 0.3 | 8.2 | 50 |
| snacktime | 201 | 468 | 0 | 0 | 9.7 | 0 | 50 |
| sorcerer | 288 | 1013 | 5 | 5 | 5 | 20.8 | 400 |
| spellbrkr | 333 | 844 | 25 | 40 | 18.7 | 37.8 | 600 |
| spirit | 169 | 1112 | 2.4 | 1 | 0.6 | 0.8 | 250 |
| temple | 175 | 622 | 0 | 7.3 | 7.9 | 7.4 | 35 |
| tryst205 | 197 | 871 | 0 | 2 | 0 | 9.6 | 350 |
| yomomma | 141 | 619 | 0 | 0 | 0 | 0.4 | 35 |
| zenon | 149 | 401 | 0 | 0 | 0 | 0 | 20 |
| zork1 | 237 | 697 | 0 | 10.3 | 9.9 | 32.6 | 350 |
| zork3 | 214 | 564 | 0.2 | 1.8 | 0 | 0.5 | 7 |
| ztuu | 186 | 607 | 0 | 0 | 4.9 | 21.6 | 100 |

### Normalized progress scores (VERBATIM)

> In order to quantify overall progress towards story completion, we normalize agent score by maximum possible game score and average across all games. The resulting progress scores are as follows: **RANDOM 1.8%, NAIL 4.9%, TDQN 6.1%, and DRRN 10.7% completion.**

**The headline number is 10.7%.** After training five agents per game, the best method completes about a tenth of the average game.

### Author analysis (verbatim)

> Comparing the different agents, the random agent shows that more than simple navigation and take actions are needed to succeed at the vast majority of games. Comparing DRRN to TDQN highlights the utility of choice-based game playing agents who need only estimate Q-Values over pre-identified valid-actions. In contrast, TDQN needs to estimate Q-Values over the full space of templates and vocabulary words. As a result, we observed that TDQN was more prone to over-estimating Q-Values due to the Q-Learning update computing a max over a much larger number of possible actions.

> NAIL performs surprisingly well considering it uses no handicaps, no training period, and plays the game for only a single episode. It should be noted that NAIL was developed on many of the games used in this evaluation, but contains no game-specific information.

> All algorithms have a ways to go before they are solving games of even average difficulty. **None of the agents were able to get any score on five of the games.** Games like Anchorhead are highly complex and others pose difficult exploration problems like 9:05 which features only a single terminal reward indicating success or failure at the end of the episode.

## Difficulty tiers (§7, Table 2)

Three tiers:
- **Possible Games** — *"games that learning agents have a credible chance to solve in the near future... feature frequent rewards, are solvable by basic navigation and interaction actions, and are largely devoid of the complexities like dialog and inventory limits."* Detective is one of the easiest; Acorncourt is a sanity check.
- **Difficult Games** — *"feature sparser rewards, more complex puzzles and interactions, and require more steps to solve."*
- **Extreme Games** — highly complex, beyond current agent capabilities.

Table 2 annotates each game with: Template Space (×10⁶), Action Space, Solution Length, Avg. Steps Per Reward, and boolean flags for **Stochastic, Dialog, Darkness, Nonstandard Actions, Inventory Limit**. Selected rows:

| Game | Template Space ×10⁶ | Action Space | Solution Length | Avg. Steps Per Reward |
|---|---|---|---|---|
| detective | 19 | 51 | 2 | — |
| library | 37 | 52 | 5 | — |
| pentari | 32 | 34 | 5 | — |
| ztuu | 64 | 84 | 5 | — |
| acorncourt | 17 | 17 | 8 | — |
| dragon | 182 | 101 | 9 | — |
| omniquest | 37 | 78 | 13 | — |
| ludicorp | 45 | 364 | 4 | — |
| advent | 107 | 277 | 7 | — |
| zork1 | 114 | 400 | 9 | — |
| anchor (anchorhead) | — | — | — | — |

(Table 2 is wide and partially garbled in PDF extraction; the columns above are the reliably-recovered ones. The **flag columns** are the interesting part conceptually — the paper explicitly factors game difficulty into named, countable structural properties rather than a holistic "hardness" rating.)

## Relevance to companion-eval-platform

### Is the LLM the PLAYER or the SIMULATOR/GAME MASTER?

**PLAYER — and in the original paper, not even an LLM.** Jericho (2020) predates LLM agents; RAND/NAIL/TDQN/DRRN are hand-engineered or DQN-based. **The simulator is the Z-Machine interpreter running a human-authored story file** — a 1980s virtual machine, fully deterministic, with no model in it anywhere.

Jericho is now most relevant to us **through TALES** (see `game-tales.md`), where modern LLMs play these same 32 games zero-shot. That result is the one to quote: **every model scores under 15 on Jericho**, ceiling 13.4, and claude-3.7-sonnet drops from **97.3 on TextWorld to 12.5 on Jericho** with the same agent and prompt. Jericho is where LLM agents visibly fall off a cliff.

### Is ground-truth state available and mechanically checkable?

**Partially — and the *manner* is the transferable idea.** Jericho does not expose a declarative logical state the way TextWorld does. It gives you:
- ground-truth player location ✓
- ground-truth objects at player's location ✓
- the world object tree (possession/nesting) ✓
- world-change detection via save → execute candidate → diff object tree → rollback ✓
- full fact-level semantics ✗

The scores themselves are emitted by the game engine and are exactly checkable; MaxScore is known per game, so normalization is principled.

### Why this matters given α = 0.25–0.34 on roleplay quality

Three imports, in descending order of usefulness:

**1. The save/execute/diff trick is the one to steal.** Jericho gets ground truth out of a black-box binary it did not write, by checkpointing state, speculatively executing a candidate action, diffing the object tree, and rolling back. We are in the analogous position: we did not author the "world" a companion narrates, and we cannot read its state declaratively. But if we maintain *any* extracted state representation, the same pattern — checkpoint, apply the model's claimed change, diff, roll back — turns "is this consistent?" into a diff over a tree. This is the cheapest path from an unauthored world to a countable signal, and it is why Jericho matters more to us than TextWorld does despite having a weaker state model.

**2. Structural difficulty factors instead of a hardness score.** Table 2 does not rate games as "hard." It counts: template space, action space, solution length, steps-per-reward, and flags Stochastic / Dialog / Darkness / Nonstandard Actions / Inventory Limit. Each is countable; difficulty is their conjunction. If we need a scenario-difficulty axis, this is the model — enumerate the structural properties, count them, and let difficulty be derived rather than rated.

**3. The normalization is honest and we should copy the honesty.** RANDOM 1.8% is reported alongside DRRN 10.7%. The random baseline is *in the headline*. Note that on **advent** all four agents score exactly 36 because *the player starts with 36 points* — an objective metric that carries zero information about the agent. Same failure as TextWorld's Advent note and ScienceWorld's Task 4-2. Third independent instance in this lineage. The rule for us: **every countable dimension ships with its random-baseline value next to it**, or the number is not interpretable.

### The caution

Jericho's ground truth is *thinner* than TextWorld's, and that thinness is not incidental — it is the price of using worlds you did not author. TextWorld has perfect state because it generates the world from predicates. Jericho has partial state because it reverse-engineers a compiled binary. **A companion product is in Jericho's position, not TextWorld's**, and should expect Jericho's grade of ground truth: location-like facts, possession-like facts, and change-detection — not full semantics. Plan the metric suite around what is recoverable, not around what would be ideal.
