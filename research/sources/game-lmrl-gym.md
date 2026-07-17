---
title: "LMRL-Gym: Benchmarks for Multi-Turn Reinforcement Learning with Language Models"
url: https://arxiv.org/abs/2311.18232
authors: Marwa Abdulhai, Isadora White, Charlie Snell, Charles Sun, Joey Hong, Yuexiang Zhai, Kelvin Xu, Sergey Levine
year: 2023
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# LMRL-Gym: Benchmarks for Multi-Turn Reinforcement Learning with Language Models

arXiv:2311.18232. HTML source consulted: https://arxiv.org/html/2311.18232v1

## Abstract (verbatim)

> "Large language models (LLMs) provide excellent text-generation capabilities, but standard prompting and generation methods generally do not lead to intentional or goal-directed agents and might necessitate considerable prompt tuning. This becomes particularly apparent in multi-turn conversations: even the best current LLMs rarely ask clarifying questions, engage in explicit information gathering, or take actions now that lead to better decisions after multiple turns. Reinforcement learning has the potential to leverage the powerful modeling capabilities of LLMs, as well as their internal representation of textual interactions, to create capable goal-directed language agents. This can enable intentional and temporally extended interactions, such as with humans, through coordinated persuasion and carefully crafted questions, or in goal-directed play through text games to bring about desired final outcomes. However, enabling this requires the community to develop stable and reliable reinforcement learning algorithms that can effectively train LLMs. Developing such algorithms requires tasks that can gauge progress on algorithm design, provide accessible and reproducible evaluations for multi-turn interactions, and cover a range of task properties and challenges in improving reinforcement learning algorithms. Our paper introduces the LMRL-Gym benchmark for evaluating multi-turn RL for LLMs, together with an open-source research framework containing a basic toolkit for getting started on multi-turn RL with offline value-based and policy-based RL methods. Our benchmark consists of 8 different language tasks, which require multiple rounds of language interaction and cover a range of tasks in open-ended dialogue and text games."

## The 8 tasks

Split into **RL Capability Tests** (5 tasks, symbolic/game-engine grounded) and **Interactive Dialogue Tasks** (3 tasks, LLM-simulated). Maze and Text-Nav each have fully-observed (FO) and partially-observed (PO) variants, giving 10 evaluation rows from 8 tasks.

### RL Capability Tests (5)

1. **Maze** — Navigation task testing credit assignment and trajectory stitching. Agent receives reward of **-1 for non-goal states, 0 for goals**. Fully observed (FO) and partially observed (PO) versions.
2. **Text-based Navigation (Text-Nav)** — "text-based game based on navigation in a house environment using a modified version of the TextWorld engine." Tests credit assignment, trajectory stitching, and complex language parsing. FO/PO variants.
3. **Wordle** — "game of Wordle the agent is given at most 6 attempts to guess a hidden 5-letter word." Tests information-seeking behavior in partially observed settings with strategic decision-making.
4. **Chess** — "text-based chess task to test the strategic decision-making, credit assignment, and trajectory stitching abilities." Board states in **FEN notation**, moves in **SAN notation**. Data generated via **Stockfish** engines.
5. **Chess Endgames** — Simplified chess variant on "endgame positions where the only pieces on the board are the two kings and the queen." Tests strategy learning with reduced computational complexity.

### Interactive Dialogue Tasks (3)

6. **Twenty Questions (20Qs)** — "one player (the oracle) thinks of an object, and the agent (the guesser) tries to guess what it is by asking a series of yes-or-no questions." Tests information gathering and semantic understanding.
7. **Guess My City (Guess)** — "agent tries to guess what city the oracle is from." Extends 20Qs by allowing open-ended questions beyond yes/no format. Tests strategic decision-making and complex language handling.
8. **Car Dealer** — the paper's text-based negotiation task. Negotiation between "car buyer and a car dealer, each with different strategies for getting the best deal." Features **three buyer and three seller types** with different strategies. Tests strategic decision-making and credit assignment.

### Which are text games with programmatic ground-truth simulators (verbatim distinction)

**Maze, Text-Nav, Wordle, Chess, and Endgames** use symbolic engines or game simulators. The three dialogue tasks (20Qs, Guess My City, Car Dealer) instead use **"LLMs as 'simulators' for the task."**

This split is the most important structural fact in the paper for our purposes — see Relevance below.

## Task properties / capabilities (Figure 2)

| Task | Strategic Decision Making | Complex Language | Credit Assignment | Partial Observability | Trajectory Stitching |
|------|---|---|---|---|---|
| Maze (FO) | ✗ | ✗ | ✓ | ✗ | ✓ |
| Maze (PO) | ✗ | ✗ | ✓ | ✓ | ✓ |
| Text-Nav (FO) | ✗ | ✓ | ✓ | ✗ | ✓ |
| Text-Nav (PO) | ✗ | ✓ | ✓ | ✓ | ✓ |
| Wordle | ✓ | ✗ | ✗ | ✓ | ✗ |
| Chess | ✓ | ✗ | ✓ | ✗ | ✓ |
| Endgames | ✓ | ✗ | ✓ | ✗ | ✓ |
| 20Qs | ✓ | ✓ | ✓ | ✓ | ✓ |
| Guess | ✓ | ✓ | ✓ | ✓ | ✓ |
| Car Dealer | ✓ | ✓ | ✓ | ✓ | ✓ |

## RL algorithms benchmarked

1. **BC** (Behavioral Cloning) — supervised fine-tuning baseline
2. **Filtered BC** (**%BC**) — BC using only successful trajectories
3. **MC Returns** (Monte-Carlo returns) — value-based method predicting reward-to-go
4. **ILQL** (Implicit Language Q-Learning) — value-based with Q-function Bellman backups
5. **Online PPO** — policy gradient online RL algorithm
6. **Online Filtered BC** — online variant collecting and filtering data
7. **GPT-4** — few-shot prompting baseline (no RL)

## Results

### Table 2: Normalized reward (primary results table)

Normalization, verbatim: **0 = minimum possible return, 50 = dataset average, 100 = maximum return per task.**

| Task | BC | Filtered BC | MC Returns | ILQL | Online PPO | Online Filtered BC | GPT-4 |
|------|---|---|---|---|---|---|---|
| FO Maze | 58.2 | 68.9 | 75.0 | **99.9** | 79.7 | 57.4 | 78.2 |
| PO Maze | 53.1 | 50.1 | 52.4 | **76.3** | 42.4 | 53.1 | 60.4 |
| FO Text-Nav | 53.7 | 65.1 | 71.9 | **91.8** | 87.1 | 74.5 | 67.5 |
| PO Text-Nav | 49.7 | 60.5 | 71.6 | 83.7 | **85.5** | 68.4 | 40.2 |
| Wordle | 79.9 | 79.1 | 94.9 | **97.7** | 84.2 | 95.2 | **15.4** |
| Chess | 47.2 | 42.9 | 46.5 | 47.3 | **48.0** | 47.2 | **0** |
| Endgames | 35.1 | 17.7 | 50.2 | 45.8 | **77.5** | 36.2 | **0** |
| 20Qs | 57.1 | 77.1 | 87.1 | 82.9 | 72.9 | 55.2 | **95.7** |
| Guess | 30.0 | 48.0 | 88.0 | 75.0 | 49.9 | 31.6 | **92.3** |
| Car Dealer | 44.5 | 54.8 | 57.2 | 46.3 | 50.5 | 40.4 | 53.5 |

The single most striking pattern, and it maps exactly onto the simulator split:

- On the **programmatic-simulator tasks**, GPT-4 few-shot is **catastrophic**: Wordle 15.4, Chess **0**, Endgames **0** — i.e. at or below the minimum-return floor, worse than the dataset average (50) and worse than plain BC. Trained RL methods dominate (ILQL 97.7 on Wordle; Online PPO 77.5 on Endgames).
- On the **LLM-simulated dialogue tasks**, GPT-4 few-shot is the **best method on the board**: 20Qs **95.7**, Guess **92.3**, beating every RL algorithm.
- Car Dealer, the negotiation task, is the flat one: everything sits in a 40.4–57.2 band. Nothing separates.

Chess is worth pausing on: every trained method clusters at 42.9–48.0, i.e. all approximately at or just below the dataset average of 50. No method learns chess. The task discriminates GPT-4 (0) from fine-tuned models, but does not discriminate among the RL algorithms.

### Table 1: Dataset statistics

| Task | Size | Avg Length | Std Length | Success Rate | Avg Return | Std Return |
|------|---|---|---|---|---|---|
| Maze | 1.24k | 19.7 | 24.5 | 0.11 | -19.7 | 24.5 |
| Text-Nav | 2.5k | 12.2 | 8.77 | 0.26 | 0.258 | 0.424 |
| Wordle | 1m | 4.82 | 1.27 | 0.70 | -4.12 | 1.59 |
| Chess | 625k | 46.7 | 18.16 | 0.60 | 0.210 | 0.970 |
| Endgames | 97.756k | 11.9 | 12.0 | 0.59 | 0.586 | 0.492 |
| 20Qs | 100k | -14.9 | 4.38 | 0.31 | -17.3 | 2.56 |
| Guess | 100k | -18.8 | 4.57 | 0.53 | -18.8 | 4.12 |
| Car Dealer | 19k | 16.5 | 3.61 | 0.53 | 0.562 | 0.422 |

Sourcing caveat: the negative "Avg Length" values for 20Qs (-14.9) and Guess (-18.8) are almost certainly a column-alignment artifact of my extraction, not the paper's actual figures — a length cannot be negative, and the Guess row repeats -18.8 in both Avg Length and Avg Return. Treat Table 1's dialogue-task rows as unreliable and re-verify against the PDF before citing any of these numbers. Table 2 (the primary results table) showed no such anomalies and is the one to rely on.

## Deterministic simulator / verifier — explicit note

**Tasks with a deterministic, programmatic ground-truth simulator/verifier:**

- **Maze (FO and PO)** — symbolic engine; reward is mechanically defined (-1 non-goal, 0 goal). Fully deterministic, fully verifiable.
- **Text-Nav (FO and PO)** — TextWorld engine (modified). Deterministic state transitions and goal checking.
- **Wordle** — deterministic verifier. The hidden word is known; the letter-match feedback and the win/lose outcome are computed by rule with zero ambiguity. Legality of a guess (is it a real 5-letter word) is dictionary-checkable.
- **Chess** — deterministic. FEN/SAN with a real chess engine; **legal-move checking is exact and free**, and Stockfish supplies both data generation and an objective position evaluation.
- **Endgames** — same as Chess, restricted to two kings and a queen. Deterministic and, at this piece count, tablebase-exact.

**Tasks with NO deterministic simulator — the environment is itself an LLM:**

- **20Qs**, **Guess My City**, **Car Dealer** — verbatim, these use "LLMs as 'simulators' for the task." The oracle/counterparty is a language model. Ground truth for the *target* (the object, the city) is known and the final guess is exactly checkable, but the **environment dynamics — what the oracle answers on each turn — are model-generated and not mechanically verifiable.** An oracle can answer inconsistently or wrongly and nothing in the harness catches it. Car Dealer is the weakest of the three: its "reward" depends on a simulated negotiation outcome with no external arbiter at all, which is very likely why every method scores 40–57 on it.

The clean generalization: **the five game tasks have mechanical ground truth; the three dialogue tasks have mechanical ground truth only on the terminal answer, and none on the trajectory.**

## Relevance to companion-eval-platform

Our core finding is that aesthetic judgments of roleplay quality are unstable — human Krippendorff alpha 0.25–0.34 — so we prefer dimensions with objective, countable, verifiable correlates. LMRL-Gym is the most directly relevant source in this corpus, because it is the one paper that puts LLM-as-player and LLM-as-simulator side by side in the same benchmark and lets us read the difference off a single results table.

**(a) Is the LLM a PLAYER or a SIMULATOR / GAME MASTER? — BOTH, and the paper splits cleanly on exactly that axis.**

- On all 8 tasks, the **evaluated agent is a PLAYER** — it acts to maximize return in an environment it does not control.
- But on **20Qs, Guess My City, and Car Dealer, a second LLM is the SIMULATOR / GAME MASTER** — the oracle, the counterparty. This is our role. LMRL-Gym is, to my knowledge, unusual in that it *deploys* an LLM game master without ever *evaluating* it. The oracle's consistency is assumed, never measured. That unmeasured assumption is precisely the gap our platform exists to fill, and this paper is the cleanest citation for the gap existing.
- Compare `game-llm-sim-state-prediction.md` in this corpus, which attacks the simulator side directly.

**(b) Is ground-truth state available and mechanically checkable? — SPLIT, and the split is the finding.**

Five tasks: yes, completely (chess legality, Wordle feedback, maze position, TextWorld state). Three tasks: only the terminal answer is checkable; the turn-by-turn dynamics are LLM-generated and unverifiable.

**What to take from this:**

1. **The GPT-4 column is the argument for objective correlates, in one row.** GPT-4 scores **95.7 / 92.3** on the tasks where an LLM judges the environment, and **15.4 / 0 / 0** on the tasks where a program does. Same model. The gap is not capability — it is that a language-model environment is *permissive* in a way a chess engine is not. When the thing checking you is made of the same stuff as you, scores go up. This is a mechanistic, numeric version of our alpha 0.25–0.34 problem, and it is the strongest single piece of evidence in the corpus for insisting on mechanically-checkable dimensions. If we cite one number from this paper, cite GPT-4's 0 on Chess against its 95.7 on 20Qs.
2. **Rule adherence here is genuinely measurable, unlike in GAMEBENCH.** Chess in LMRL-Gym is free-form SAN generation against a real engine — illegal moves are exactly detectable, for free, with no rater. This is the design GAMEBENCH lacks (it hands agents an enumerated legal-action list, so it never observes a violation). If we want a rule-adherence metric for our game master, **the LMRL-Gym chess setup is the pattern to copy, not GAMEBENCH's**. Caveat: the paper does not itself report an illegal-move *rate* — it reports normalized reward. The affordance is there; the metric would be ours to add.
3. **Car Dealer is a cautionary tale, and the closest task to our product.** It is our shape almost exactly: open-ended, multi-turn, persona-driven (three buyer types, three seller types), no external arbiter. And it produces **no signal** — 40.4 to 57.2 across seven methods, i.e. everything within noise of the dataset average. A task with our structure and no mechanical ground truth failed to discriminate anything. That is a warning about naive "negotiation success" or "persuasion" metrics for companion eval: without an arbiter, the measurement collapses. It also suggests the Car Dealer flatness and our alpha 0.25–0.34 are the same disease.
4. **The FO/PO contrast is a reusable design lever.** Holding the task fixed and varying only observability (Maze 99.9 FO → 76.3 PO for ILQL; Text-Nav GPT-4 67.5 FO → 40.2 PO) is a clean way to isolate one dimension with objective outcomes. If we want to test whether our game master tracks hidden state, this ablation transfers.
5. **The normalization scheme is worth borrowing.** "0 = min possible, 50 = dataset average, 100 = max" makes heterogeneous tasks comparable on one axis and, critically, makes "worse than the data you trained on" legible as a number below 50. Several of our candidate metrics have no natural scale; this gives one.

**Net verdict for our design:** the highest-value source of the two. Take (i) the GPT-4 programmatic-vs-LLM-simulator gap as the headline evidence for objective correlates, (ii) the chess free-generation-plus-engine-validation setup as the rule-adherence measurement pattern, and (iii) Car Dealer as the documented failure mode we must design around. The one thing LMRL-Gym does *not* give us is any evaluation of the game master itself — it uses LLM simulators and never checks them.
