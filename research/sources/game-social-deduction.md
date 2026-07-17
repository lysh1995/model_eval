---
title: "Social Deduction Games with LLM Agents: Rule Adherence and Consistency (ReCon / Werewolf / AvalonBench)"
url: https://arxiv.org/abs/2310.01320
authors: "Shenzhi Wang, Chang Liu, Zilong Zheng, Siyuan Qi, Shuo Chen, Qisen Yang, Andrew Zhu, Li Kang, Yujie Qin, Wenhao Yu, Ning Ke, Bo An, Gao Huang, Junliang Xing, Yu Wang, Yuandong Tian (ReCon); Yuzhuang Xu, Shuo Wang, Peng Li, Fuwen Luo, Xiaolong Wang, Weidong Liu, Yang Liu (Werewolf); Jonathan Light, Min Cai, Sheng Shen, Ziniu Hu (AvalonBench)"
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Social deduction: rule adherence & consistency measurement

Three sources, covered because the task brief asks specifically about **whether the game engine rejects illegal moves, hallucinated actions, out-of-turn speech, or improper disclosure of hidden information**.

1. **ReCon** — "Avalon's Game of Thoughts: Battle Against Deception through Recursive Contemplation" — arXiv 2310.01320
2. **Werewolf** — "Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf" — arXiv 2309.04658
3. **AvalonBench** — "AvalonBench: Evaluating LLMs Playing the Game of Avalon" — arXiv 2310.05036

> **Headline for our purposes:** none of these three implements a rule-violation *counter*. Rule adherence is discussed qualitatively, or enforced structurally by making violations unrepresentable. This is a gap in the literature, not a source of metrics.

---

## 1. ReCon (arXiv 2310.01320)

### Method
Two-stage contemplation framework for navigating deceptive information:
1. **Formulation contemplation** — generates initial thought and speech using **first-order perspective transition** (inferring others' mental states from the agent's own perspective).
2. **Refinement contemplation** — polishes the output using **second-order perspective transition** (how others perceive the agent's mental state).

The key structural move: contemplation happens *internally, before public speech*, so the agent can catch itself before leaking.

### Game setup
6-player Avalon with hidden roles:
- **Good:** Merlin, Percival, 2 Loyal Servants
- **Evil:** Morgana, Assassin
- **Victory:** Good wins with 3+ successful quests; Evil wins with 3 failed quests **or** by assassinating Merlin.

### Results (end-to-end, Figure 4)
| Agent | Side | Success rate |
|---|---|---|
| ReCon + ChatGPT | Good | ~83.3% |
| ReCon + Claude | Good | ~75% |
| Baseline CoT | Good | ~15–40% |
| ReCon | Evil | ~70.6% |

### Multi-dimensional metrics (Figure 5) — GPT-4 as judge, six dimensions
Concealment (CCL), Logic (LG), Contribution (CTR), Persuasiveness (PRS), Information (INF), Creativity (CRT). ReCon exceeded baseline across all six.

> Note: these six are **LLM-judged subjective dimensions**. The paper reports no inter-rater reliability for them.

### Rule adherence & information leakage — what's actually measured

- **Information leakage is identified as a central failure.** The paper states LLM agents "struggle to maintain confidential information securely" in deceptive environments, and shows a worked example of an agent **exposing its secret Merlin role**, leading to assassination. ReCon partially mitigates via internal contemplation before public speech. This is presented as a **qualitative case study — no leak-rate count is reported.**
- **Format compliance (the one countable adherence number):** ChatGPT and Claude achieve **>90%** adherence to required response formats; **LLaMA-2 "consistently fails."**
- **No engine-level rejection of invalid moves** is described.
- **No hallucination-detection system** for illegal actions.
- **No consistency checker** for contradictory statements across rounds.
- Humans must **manually review gameplay logs** to spot inconsistencies or deceptive intent.

---

## 2. Werewolf (arXiv 2309.04658)

### Framework
Tuning-free — frozen LLMs play via prompt engineering. Four components:
1. **Game context** (rules, roles, strategy priors)
2. **Historical information retrieval**, three dimensions:
   - *Freshness* — most recent K=15 messages
   - *Informativeness* — rule-matched critical messages (top N)
   - *Completeness* — reflection via Q&A over full history
3. **Experience-based suggestions** from cross-round gameplay pools
4. **Chain-of-thought reasoning** prompts

### Setup
- Model: **GPT-3.5-turbo-0301**
- 7 players: 2 werewolves, 2 villagers, 1 witch, 1 guard, 1 seer
- Experience pools of 10 / 20 / 30 / 40 rounds evaluated separately
- 50 test rounds per configuration
- Window K=15, predefined questions L=5, free questions M=2

### Results
**Learning from experience (Figure 3):**
- 10–20 round pools: "notable positive effect on both winning rate and game duration"
- 30 round pool: "average duration obviously longer"
- 40 round pool: mixed — "slightly promising" win rates but shorter duration

**Ablation (Figure 4):** all components necessary; the complete approach achieves the highest **"percentage of reasonable outputs"** vs. variants.

> "Percentage of reasonable outputs" is the closest thing to a rule-adherence metric in this paper, but it is a soft/aggregate judgment, not a violation count. Exact values are presented in figures rather than a numeric table.

### Emergent strategic behaviors (unprogrammed)
1. **Trust** — players "proactively share information detrimental to themselves"; bidirectional trust increases with experience pools.
2. **Confrontation** — implicit disagreement; defenders "chose to protect...in countering attacks."
3. **Camouflage** — role deception and fabricated events.
4. **Leadership** — influential suggestions like "Can the seer tell us more" to steer the group.

### Rule adherence — the key conceptual contribution

The paper explicitly **separates strategic deception from hallucination**, and this distinction is the most useful thing in it for us:

- Deceptive utterances and false accusations are **rational gameplay, not hallucinations**. "Camouflage...should not be considered hallucinations" — agents "convey information about werewolves while not revealing roles," and the authors give evidence agents comprehend deception's strategic value.
- **True hallucinations are logical contradictions** — the canonical example: *"As villager, I verified Player 1"* (villagers cannot verify; only the seer can). This is a **role-capability violation** and it is mechanically checkable: the claimed action is not in the claimed role's action set.
- **Non-constant baseline caveat:** werewolf performance was not constant; "capability of LLMs might also change in response" to opponent strategies, explaining outcome variability.

---

## 3. AvalonBench (arXiv 2310.05036)

### Environment design
Comprehensive multi-agent game environment: Avalon engine + **rule-based bots as deterministic baseline opponents** + ReAct-style LLM agents with role-tailored prompts.

**How actions reach the engine:** the LLM emits natural language; "the output is then fed to a separate LLM model that parses the output...into a format readable by the game engine." A parsing layer sits between free text and the engine.

**Discrete action spaces, enforced structurally per role:**
- **Team selection** — leader picks a subset of fixed team size
- **Voting** — binary approve/reject, all players
- **Quest** — binary pass/fail, selected team members only
- **Assassination** — single target from player pool

**Information hiding** is enforced by **role-based disclosure at prompt-construction time**: Evil players receive complete identity information; Servants receive none.

### Results

**Table 2 — Assassin role (LLM Evil vs. Good baseline bots):**
| Model | Setting | Total Winrate | Mission Winrate | Assassination Winrate | Assassination Accuracy |
|---|---|---|---|---|---|
| Baseline Bot | — | 61.8 | 42.7 | 19.1 | 33.3 |
| GPT-3.5 | w/o discussion | 26.7 | 20.0 | 6.7 | 8.0 |
| GPT-3.5 | w/ discussion | 66.7 | 0.0 | 66.7 | 66.7 |
| Llama2-7B | w/ discussion | 30.0 | 0.0 | 30.0 | 30.0 |

**Table 3 — Servant role (LLM Good vs. Evil baseline bots):**
| Model | Setting | Total Winrate | Deduction Accuracy |
|---|---|---|---|
| Baseline Bot | — | 38.2 | 71.8 |
| GPT-3.5 | w/o discussion | 11.1 | 60.7 |
| GPT-3.5 | w/ discussion | 22.2 | 76.0 |
| Llama2-7B | w/ discussion | 13.3 | 68.0 |

**Headline:** ChatGPT playing Good wins **22.2%** vs. rule-based Evil bots, where the *rule-based* Good bot achieves **38.2%** in the same setting — LLMs underperform scripted baselines. Conclusion: current LLM agents "do not possess the deduction, persuasion, negotiation, and deception capabilities yet to play Avalon well."

### Rule violations & information handling
- **Evil players "frequently reveal their identity"** during discussion despite explicit instructions not to — e.g. stating preferences from an evil perspective, directly acknowledging team membership goals. Documented as an observed pattern; **no leak rate is quantified.**
- **No engine-level rejection of illegal actions** is described; no information isolation beyond role-based prompting.
- The system "appears to rely on LLM compliance rather than hard constraints" for discussion-phase behavior.

---

## Cross-source synthesis on rule adherence

| Violation type | Measured anywhere? | How handled |
|---|---|---|
| Illegal *mechanical* move (bad team size, voting twice) | **Not measured — made impossible.** AvalonBench's discrete action space + parser means the engine never sees a malformed move. | Structural prevention |
| Hallucinated role capability ("As villager, I verified X") | **Identified qualitatively** (Werewolf paper). Mechanically checkable in principle — claimed action vs. role's action set. **No count reported.** | Manual log review |
| Hidden-information leakage | **Identified as a major failure** (ReCon: Merlin self-exposure; AvalonBench: Evil "frequently reveal their identity"). **No leak rate in any of the three.** | Case studies |
| Speaking out of turn | **Not addressed.** Turn order is imposed by the scaffold. | Structural prevention |
| Output format compliance | **Yes — the one hard number.** ReCon: >90% for ChatGPT/Claude; LLaMA-2 "consistently fails." | Reported |

**The central observation:** these frameworks achieve rule adherence by **making violations structurally unrepresentable** rather than by detecting and counting them. The parser collapses free text into a legal action; the scheduler enforces turn order; the prompt builder enforces information access. What escapes this net is exactly what is *expressed in natural language* — leaked identities and hallucinated role claims — and that is precisely what none of the three papers counts.

---

## Relevance to companion-eval-platform

### (a) Is the LLM PLAYER or SIMULATOR/GAME MASTER?

**PLAYER — unambiguously, in all three.** This is the direct inverse of ByteSized32. The simulator is a **hand-written, human-authored game engine** (AvalonBench's Avalon environment; the Werewolf framework's game loop). The LLM occupies a **seat at the table** and is scored on outcomes it achieves *within* a world it did not create and cannot alter.

Consequence: the engine is trusted infrastructure, so **no one evaluates the simulator**. All measurement points at the player. For a platform where the model must *be* the world (companion as game master), this literature offers strategy and social-reasoning results but almost nothing about simulator fidelity. ByteSized32 is the relevant lineage for that; this is the contrast case that shows why.

### (b) Is ground-truth state available and mechanically checkable?

**Ground truth: yes. Mechanically checkable: yes — but almost entirely unexploited for rule adherence.**

The engine holds exact hidden state — every role assignment, every quest outcome, every private vote. Everything needed to compute a rule-violation rate is *already in memory*. The papers just don't compute it.

**What is objective and countable here:**
- **Win rate** — perfectly objective, the engine declares the winner. AvalonBench 22.2% (ChatGPT Good) vs. 38.2% (rule-based Good). ReCon ~83.3% Good / ~70.6% Evil.
- **Deduction accuracy** — 76.0% (GPT-3.5 w/ discussion) vs. 71.8% (bot). Checked against true role assignments the engine knows.
- **Assassination accuracy** — 66.7% (GPT-3.5 w/ discussion) vs. 33.3% (bot). Did it name the actual Merlin? Engine knows.
- **Format compliance** — >90% ChatGPT/Claude. Parseable or not; deterministic.

These are all genuinely alpha-free — no rater, no judge, no aesthetic call. They clear the α = 0.25–0.34 roleplay-quality bar trivially, in the same way ByteSized32's "does it compile" does.

**What is subjective and should be treated with suspicion:**
- ReCon's six GPT-4-judged dimensions (Concealment, Logic, Contribution, Persuasiveness, Creativity, Information) are **exactly the class of aesthetic construct our α = 0.25–0.34 finding indicts** — "Persuasiveness" and "Creativity" are roleplay-quality ratings wearing a game-theory costume. **No inter-rater reliability is reported for them.** Note the irony: *Concealment* is judged subjectively by GPT-4, when the engine knows the true role and every public utterance — it could be counted exactly.

**The actionable gap — and the best opportunity in this source set.** The two violation types that survive structural prevention are both countable with information the engine already has:

1. **Hidden-information leakage rate.** Engine knows agent *i*'s true role. Scan agent *i*'s public utterances for disclosure of information available only to that role. Report leaks per game. ReCon and AvalonBench both narrate this failure at length (Merlin self-exposure; Evil "frequently reveal their identity") and **neither reports a number.** This maps cleanly onto companion evaluation: *did the companion reveal something it should not know or should not say?* — persona-breaking disclosure, out-of-character knowledge, leaking system-prompt content. Objective, countable, engine-checkable.

2. **Role-capability violation rate.** The Werewolf paper's *"As villager, I verified Player 1"* is the template. Each role has a closed action set; a claimed action either is or isn't in it. This is a **set membership test**, not a judgment — the same shape as ByteSized32's spec-compliance object-presence check that scored **κ = 0.96**, our highest-reliability data point across all sources. The companion analogue: the character claims a capability, memory, or history the persona doesn't have.

**Design lesson for the platform.** These papers reveal an important asymmetry: **structural prevention destroys measurement.** By parsing free text into a legal action, AvalonBench guarantees rule-compliant moves — and simultaneously guarantees it can never measure rule-following, because the model was never able to fail. If we want rule adherence as a *dimension*, we must leave a channel where violation is possible and then count violations. A companion architecture that silently repairs or constrains model output will look perfectly compliant while telling us nothing. **Preserve the failure mode, or forfeit the metric.**
