---
title: "Story Shaping: Teaching Agents Human-like Behavior with Stories"
url: https://arxiv.org/abs/2301.10107
authors: Xiangyu Peng, Christopher Cui, Wei Zhou, Renee Jia, Mark Riedl (Georgia Tech)
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Story Shaping (AIIDE 2023)

**arXiv:** 2301.10107 | **Published:** Proc. AAAI AIIDE vol. 19 (2023)

RL-agent paper, not a GM paper. Relevant to us for one specific reason: it operationalizes **"human-like / commonsense-appropriate behavior" as a countable knowledge-graph-triple match against a reference**, converting a normally-subjective judgment into an automatic number. It is also a **cautionary case** about circular metrics.

## 1. Method

"Story Shaping [is] a technique in which a reinforcement learning agent **infers tacit knowledge from an exemplar story** of how to accomplish a task and **intrinsically rewards itself for performing actions that make its current environment adhere to that of the inferred story world**."

Two knowledge graphs are built and compared:

**Story KG** — extracted from the exemplar narrative via **Semantic Role Labeling trained on VerbAtlas** (Di Fabio et al., 2019) to get ⟨subject, relation, object⟩ triples. "VerbAtlas is a linguistic resource that provides semantic [frames]... entities and VerbAtlas frames are used as edges, such as ⟨You, DRINK, coffee⟩." Incorporating the VerbAtlas frame name of the verb normalizes surface variation.

**World KG** — built during agent interaction using **ALBERT-QA** (Lan et al., 2019) fine-tuned on the **JerichoQA** dataset, by answering questions such as "What am I carrying?" to construct the state representation.

## 2. Intrinsic reward (verbatim formula)

> **r't = rt + α × rts + β × rte**

- **rts** (KG intrinsic reward) = **n × ρ** for matching triples between World KG and Story KG (n = number of matched triples)
- **rte** (exploration reward) = **Δ(G_global − G_t)**, encouraging state discovery
- **rt** = base game score
- **α, β** = scaling factors

The commonsense signal is literally **a count of matched graph triples**. That is the whole idea.

## 3. Environments

- **Jericho**: `9:05` — "a game in which the agent must successfully nav[igate a morning routine]"
- **TextWorld**: `Shopping` and `See Doctor`
- **LIGHT**: fantasy role-playing sandbox (KG-A2C used for LIGHT experiments)

Agents: **Q\*BERT-S** (Story-Shaped) vs baseline **Q\*BERT**. All results over **20 random seeds / 20 independent runs**. Games auto-terminate after **50 steps**.

## 4. Automatic metrics (verbatim definitions)

- **Win rate**: "the winning rate of trained agents on test games over 20 random seeds."
- **Avg steps**: "the average number of steps that each agent takes to win the game. The game will automatically end over 50 steps."
- **Avg Commonsense score**: "the total intrinsic reward accrued over a testing trial; a higher score indicates the agent takes more actions that express commonsense and social norm knowledge."
- **Avg game score**: "the average score of each agent on the test games, which reflects **how far toward the win condition** the agent made it, **irrespective of how** the agent reached the farthest point."

## 5. Results — Table 2 (20 independent runs)

| Game | Agent | Win Rate % | Avg Steps | Avg CS Score | Max CS Score | Avg Game Score | Max Game Score |
|---|---|---|---|---|---|---|---|
| 9:05 | Q*BERT-S | 100 | 16.30 | **3.90** | 4 | 5.00 | 5 |
| 9:05 | Q*BERT | 100 | 7.25 | 0.40 | | 5.00 | 5 |
| Shopping | Q*BERT-S | 100 | 12.35 | **3.70** | 4 | 5.00 | 5 |
| Shopping | Q*BERT | 100 | 6.30 | 0.90 | | 5.00 | 5 |
| Doctor | Q*BERT-S | 95 | 19.15 | **6.70** | 8 | 4.75 | 5 |
| Doctor | Q*BERT | 95 | 14.30 | 0.70 | | 4.75 | 5 |

**CRITICAL, verbatim:** "The win rates and the average game scores are **identical** between agents with and without Story Shaping. However, our agent's 'Avg Commonsense Score' is significantly higher than the baseline agent's... The larger 'Avg Steps' value for our agent also suggests that it takes more actions before winning the game, which further highlights that it is **not seeking the shortest possible trajectory**."

So: **the task-success metrics (win rate 100/100/95, game score 5.00/5.00/4.75) do not discriminate AT ALL.** They are identical across conditions. The only automatic metric that moves is the intrinsic reward — **which is the objective the agent was trained to maximize.** That is circular, and the paper does not flag it as such.

## 6. Human evaluation

"We recruited **30 participants** using the **Cloud Research** platform and **Amazon Mechanical Turk** (Litman et al., 2017). **We screened for participants that were generally not familiar with text games.**" Each participant reads the winning goal of a randomly chosen game, then reads **a pair of game transcripts** (Q\*BERT-S vs Q\*BERT), each including game observations and corresponding actions, then chooses which transcript they prefer per metric.

**The two forced-choice questions (verbatim):**
- "This sequence of actions expresses more common sense thinking (with social norm knowledge) on the action choice."
- "This sequence of actions makes you understand why the agent takes these actions given what you know about the goal."

"Participants had to provide **detailed explanations** for their choices in each comparison, **using at least 50 characters**."

### Table 3 — % of participants preferring each system

| Game | **Commonsense** Shaped % | Base % | Tie % | **Understanding** Shaped % | Base % | Tie % |
|---|---|---|---|---|---|---|
| 9:05 | **63.63*** | 9.09 | 27.27 | 36.36 | **45.45** | 18.18 |
| Shopping | **66.67**** | 8.33 | 25.00 | 41.67 | 33.33 | 25.00 |
| Doctor | 53.85 | 23.08 | 23.08 | 46.15 | 38.46 | 15.38 |

`*` p < 0.05, `**` p < 0.01, **Wilcoxon signed-rank test on win-lose pairs.**

**Note the split:** Story Shaping wins **Commonsense** on 2 of 3 games significantly (Doctor: 53.85 vs 23.08, NOT significant). But on **Understanding** it wins **zero** of 3 — and actually **loses** on 9:05 (36.36 vs 45.45). The paper's own second human metric fails to support it.

## 7. IAA status

**NO inter-annotator agreement reported.** Verified by grep for `krippendorff|kappa|inter-rater|inter-annotator|agreement` over the full PDF — **0 matches.** With n=30 MTurk workers doing forced-choice preference, agreement is computable but is not computed. The **≥50-character explanation requirement** is an attention/quality control, not an agreement measure.

## Relevance to companion-eval-platform

1. **The core transferable trick: score "appropriate/human-like behavior" as COUNTED TRIPLE MATCHES against a reference graph, not as a rating.** `rts = n × ρ` where n = matching ⟨subject, relation, object⟩ triples between the agent's world state and a reference story world. This is fully automatic, deterministic, and has **no annotator and therefore no alpha**. A companion analog: extract triples from an ideal/reference response or from an established persona/relationship record, count matches against the actual response. Note that VerbAtlas frames as edge labels are what make matching robust to paraphrase — plain string matching would fail.
2. **STRONGEST CAUTION IN THIS FILE — beware circular objective metrics.** The only automatic metric that discriminates is **the training objective itself**. Win rate and game score are *identical* across conditions (100 vs 100, 5.00 vs 5.00). "Our agent scores higher on the reward it was trained to maximize" is not evidence of quality. **If we build a countable dimension and then optimize against it, it stops being evidence.** Objective ≠ valid. Our objective dimensions must be (a) not directly optimized against, or (b) held out, or (c) validated against an independent signal.
3. **Corollary: objective metrics can be objectively USELESS.** Win rate here is perfectly reliable, perfectly countable, and completely non-discriminative (zero variance between conditions). Countability is necessary but not sufficient — a dimension must also have **discriminative range**. Add this as an explicit screening criterion alongside verifiability: *does it separate systems we believe differ?*
4. **Forced-choice A/B with a mandatory written justification (≥50 chars) is a cheap protocol worth copying** — pairwise preference is more stable than absolute Likert (relevant to our 0.25–0.34 problem), and the justification requirement gives an auditable trace. But they still reported no agreement, so we have no evidence on how stable it actually was.
5. **Honest-reporting model:** their own "Understanding" metric wins 0 of 3 games and loses one outright, and the Doctor commonsense result (53.85 vs 23.08) is non-significant. Two of six human-eval cells support the method. Useful precedent for reporting dimensions that don't work rather than dropping them.
6. **Fifth consecutive paper in this batch with no IAA.** Running tally across the game-simulation literature: only Callison-Burch et al. (2022) reports any agreement statistic.
