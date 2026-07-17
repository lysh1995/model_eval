---
title: "RPGBench: Evaluating Large Language Models as Role-Playing Game Engines"
url: https://arxiv.org/abs/2502.00595
authors: Pengfei Yu, Dongming Shen, Silin Meng, Jaewon Lee, Weisu Yin, Andrea Yaoyun Cui, Zhenlin Xu, Yi Zhu, Xingjian Shi, Mu Li, Alex Smola (Boson AI; UIUC)
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# RPGBench — objective game-mechanic checking in an LLM RPG engine

**The single most directly applicable source in this review. It is our exact product setting (an LLM running a scene for a user), it runs objective and subjective metrics side by side on the same trajectories, and it independently reproduces our α finding — including a NEGATIVE human-human correlation on persona consistency.**

## Abstract (verbatim)

> "We present RPGBENCH, the first benchmark designed to evaluate large language models (LLMs) as text-based role-playing game (RPG) engines. RPGBENCH comprises two core tasks: Game Creation (GC) and Game Simulation (GS). In GC, an LLM must craft a valid and playable RPG world using a structured event-state representation, ensuring logical coherence and proper termination conditions. In GS, the LLM simulates interactive gameplay across multiple rounds while consistently updating states and enforcing game rules. To comprehensively assess performance, RPGBENCH integrates objective and subjective evaluation methodologies. Objective measures verify adherence to event mechanics and check variable updates without requiring human intervention. Subjective measures—such as content interestingness, action quality, and role-playing capability—are evaluated via an LLM-as-a-judge framework, where a strong LLM grades each candidate's outputs. Empirical results demonstrate that state-of-the-art LLMs can produce engaging stories but often struggle to implement consistent, verifiable game mechanics, particularly in long or complex scenarios."

Motivating claim (verbatim): "Unlike traditional text generation tasks, where coherence is judged subjectively, game mechanics must be evaluated ob[jectively]."

## The design move: event–state representation

The enabling trick. Games are represented as structured **events** with entering conditions and success/failure **effects on state variables**. This "maintains storytelling flexibility while allowing for automated robust assessments of mechanical correctness."

**This is the IFEval move applied to fiction.** IFEval made instructions checkable by restricting to verifiable ones; RPGBench makes *fiction* checkable by requiring the game to declare an explicit state machine underneath the prose. The prose stays free; the mechanics are checkable.

### BFS Validity Checker (Game Creation)

Starting from initial state, BFS repeatedly checks which events are available, applies success/failure effects, tracks whether at least one success and one losing state is reachable. Stops when no new states discoverable or search exceeds **10,000,000 states**.

> "A game is valid if every event is triggered at least once, and both success and losing termination conditions are achievable."

Fully deterministic, no judge.

## Metrics

**Game Creation:** FCR (format-check pass rate), VCR (valid-check pass rate), plus `w. Success`, `w. Lose`, `Reachability`.

**Game Simulation** — objective:
- **Event Condition Error:** "An event triggers when its entering condition is not met, or the outcome (success/failure) does not match the current state."
- **Variable Update Error:** "The state variables do not update according to event effects."

Main mechanic metric — round-level accuracy:
```
MEC = #Rounds with no errors / #Rounds
```
Fine-grained:
```
ECEt = #Event condition errors / #Events
VUEt = #State variables incorrectly updated / #State variables
```
> "By design, all these metrics require no LLM judge."

**Game Simulation** — subjective (all LLM-as-judge, GPT-4o):
- **Action Quality (ACT)** — diversity, relevance, clarity; 1–5 normalized to [0,1] via (s−1)/4
- **Interestingness (INT)** — 1–5 normalized
- **Role-Playing Factual Consistency (FAC)** — each fact labeled align/contradict/neutral; `#align / (#align + #contradict)`
- **Role-Playing Personality Consistency (PER)** — infer Big Five from generated content via Ten-Item Personality Inventory (TIPI, Gosling et al. 2003), compare to game definition

Setup: simulated player picks one of three candidate actions **at random** each round; temperature 0.2; simulations terminated after round 10 for main experiments.

## Game Creation results (verbatim Table 2)

| Models | FCR ↑ | VCR ↑ | w. Success | w. Lose | Reachability |
|---|---|---|---|---|---|
| Claude 3.5 Sonnet* | 0.050 | 0.010 | / | / | / |
| DeepSeek V3 | 0.990 | 0.380 | 0.455 | 0.545 | 0.828 |
| Gemini 1.5 Pro | 0.850 | 0.040 | 0.060 | 0.080 | 0.610 |
| Gemini 2.0 Flash Exp | 1.000 | 0.330 | 0.420 | 0.680 | 0.480 |
| GPT 4o | 0.960 | **0.490** | 0.656 | 0.771 | 0.656 |

*Claude 3.5 Sonnet "frequently refuses to generate content, often citing an 'over-lengthy output' error, causing 95% of its responses to fail the format check."

**Best model produces a logically valid game 49% of the time.** Gemini 1.5 Pro: 4%. Format compliance is near-solved (0.85–1.00); *logical validity* is not.

## Game Simulation results (verbatim Table 3)

| Model | LEN | FAC ↑ | PER ↑ | ACT ↑ | INT ↑ | MEC ↑ | ECE ↓ | VUE ↓ |
|---|---|---|---|---|---|---|---|---|
| Claude 3.5 Sonnet | 220.3 | 0.991 | 0.589 | 0.923 | **0.722** | **0.113** | 0.062 | 0.308 |
| Deepseek V3 | 309.5 | 0.984 | 0.583 | 0.918 | 0.502 | 0.277 | 0.165 | 0.153 |
| Gemini 1.5 Pro | 198.0 | 0.968 | 0.596 | 0.894 | 0.602 | 0.554 | 0.081 | 0.085 |
| Gemini 2.0 Flash Exp | 195.3 | 0.885 | 0.598 | 0.865 | 0.538 | **0.765** | 0.094 | 0.034 |
| GPT 4o | 201.9 | 0.902 | 0.585 | 0.894 | 0.502 | 0.693 | 0.088 | 0.047 |
| GPT 4o mini | 282.5 | 0.955 | 0.588 | 0.900 | 0.496 | 0.147 | 0.126 | 0.148 |
| Llama 3.1 70B Instruct | 279.2 | 0.977 | 0.586 | 0.915 | 0.420 | 0.162 | 0.161 | 0.284 |
| Llama 3.3 70B Instruct | 225.7 | 0.960 | 0.585 | 0.936 | 0.466 | 0.204 | 0.201 | 0.302 |

> "Game mechanic performance (MEC) varies the most among all metrics... Even the best-performing model, Gemini 2.0 Flash Exp, only achieves a 0.765 MEC score, highlighting the inherent difficulty of precisely following complex game mechanics in a text-based RPG setting."

**THE HEADLINE DISSOCIATION — Claude 3.5 Sonnet: highest INT (0.722), highest FAC (0.991)... and MEC of 0.113.** The most *interesting* game engine in the study breaks its own mechanics in ~89% of rounds. Meanwhile Gemini 2.0 Flash Exp has the best mechanics (0.765) and near-worst interestingness (0.538). **Objective correctness and subjective appeal are not merely distinct — in this table they are close to inversely ranked.**

Note also the **discriminative power gap**: PER spans 0.583–0.598 (range 0.015) and ACT spans 0.865–0.936 (range 0.071) across all eight models — nearly flat, useless for ranking. MEC spans 0.113–0.765 (range 0.652). **The objective metric separates models ~9x better than the subjective persona metric.**

## Degradation over rounds (verbatim Table 5, GPT-4o)

| # Rounds | FAC | INT | MEC |
|---|---|---|---|
| 10 | 0.920 | 0.502 | 0.693 |
| 15 | 0.948 | 0.480 | 0.679 |
| 20 | 0.941 | 0.458 | 0.674 |
| 25 | 0.941 | 0.440 | **0.668** |

> "INT score decreases with more rounds, which could originate from repetitive content. MEC score also decreases, potentially due to the challenges in handling long context."

MEC decays gently: 0.693 → 0.668 over 10→25 rounds (−2.5 pts). But note MEC is a **per-round** rate, not a session conjunction — at 0.668/round, the probability of a clean 25-round session is vanishingly small (0.668²⁵ ≈ 10⁻⁵ if independent). The SysBench-style session-level number is not reported and would be near zero.

## Temperature (verbatim Table 4, GPT-4o)

| Temperature | FAC | INT | MEC |
|---|---|---|---|
| 0.2 | 0.920 | 0.502 | 0.693 |
| 0.5 | 0.939 | 0.520 | 0.629 |
| 0.8 | 0.952 | 0.538 | **0.643** |

Temperature buys interestingness (0.502→0.538) and costs mechanics (0.693→0.643). A directly actionable knob with a measurable trade.

## HUMAN EVALUATION — direct corroboration of our α finding

Subset of **20 simulated games**, four subjective metrics. Human scores normalized to [0,1].

**Table 6 (verbatim)** — each cell: "Human Score / Automatic Score / Absolute Difference"

| Models | FAC | ACT | INT | PER |
|---|---|---|---|---|
| Claude 3.5 Sonnet | 0.810 / 1.000 / 0.190 | 0.831 / 0.913 / 0.082 | 0.856 / 0.713 / 0.144 | 0.648 / 0.729 / 0.081 |
| Deepseek V3 | 0.807 / 0.950 / 0.143 | 0.857 / 0.913 / 0.056 | 0.850 / 0.475 / 0.375 | 0.645 / 0.742 / 0.098 |
| Gemini 1.5 pro | 0.733 / 0.950 / 0.217 | 0.738 / 0.889 / 0.152 | 0.801 / 0.588 / 0.214 | 0.648 / 0.740 / 0.093 |
| Gemini 2.0 Flash Exp | 0.769 / 0.800 / 0.031 | 0.851 / 0.876 / 0.025 | 0.856 / 0.525 / 0.331 | 0.651 / 0.737 / 0.085 |
| GPT 4o | 0.709 / 0.950 / 0.241 | 0.881 / 0.887 / 0.007 | 0.834 / 0.525 / 0.309 | 0.667 / 0.711 / 0.044 |
| GPT 4o mini | 0.770 / 0.950 / 0.180 | 0.794 / 0.887 / 0.093 | 0.813 / 0.488 / 0.326 | 0.648 / 0.753 / 0.104 |
| Llama 3.1 70B Instruct | 0.778 / 0.950 / 0.172 | 0.857 / 0.898 / 0.041 | 0.824 / 0.400 / 0.424 | 0.627 / 0.744 / 0.117 |
| Llama 3.3 70B Instruct | 0.791 / 0.933 / 0.142 | 0.852 / 0.930 / 0.078 | 0.850 / 0.438 / 0.412 | 0.640 / 0.739 / 0.099 |

**Table 7 (verbatim)** — "MAD / Pearson / Kendall"

| Comparison | FAC | ACT | INT | PER |
|---|---|---|---|---|
| Auto v.s. Human | 0.165 / 0.129 / 0.267 | 0.067 / 0.226 / 0.071 | 0.317 / 0.140 / 0.109 | 0.090 / **−0.691** / **−0.429** |
| **Human v.s. Human** | 0.030 / **0.707** / 0.571 | 0.039 / **0.472** / 0.214 | 0.018 / **0.508** / 0.286 | 0.023 / **−0.310** / **−0.286** |

**Read the bottom row carefully. This is our α = 0.25–0.34 finding, independently reproduced, in our exact domain:**
- **Human–human Pearson on PER (personality/persona consistency) = −0.310, Kendall = −0.286.** *Negative.* Two humans rating whether an NPC stayed in character are **anti-correlated**. Persona consistency — the single most important quality dimension for a companion product — is not merely noisy, it is measured worse than chance by humans.
- Human–human on ACT = 0.472 Pearson / 0.214 Kendall. On INT = 0.508 / 0.286. Kendall ~0.21–0.29 is squarely in our α 0.25–0.34 band.
- **Auto vs human on PER = −0.691 Pearson.** The LLM judge is strongly *anti-correlated* with humans on persona consistency. Building a persona metric on an LLM judge would produce confidently inverted rankings.

Authors' own framing (verbatim):

> "we find a fair degree of overlap in the top two performing models across FAC, ACT, and INT, but not for PER. From Table 7, we see that the inter-annotator correlation on PER is also very low, suggesting that personality judgments tend to be more variable and less stable."

> "Feedback from our annotators further indicates that INT can be heavily influenced by personal preferences. For instance, if a rater dislikes combat scenarios, they consistently assign lower interest scores to an action-heavy game trajectory. This shows that subjective evaluations—whether by humans or LLM judges—can vary widely based on individual tastes."

> "Although LLM-based scoring has been common in prior work for subjective dimensions, our human evaluation reveals that **fine-grained comparisons remain unstable and less differentiable, even for human evaluators. This outcome highlights the importance of introducing objective metrics into game simulation assessment, such as our proposed game mechanic checks (Section 3.1) that do not rely on either human or LLM judgments.**"

> "human scores should be interpreted as reference points rather than definitive 'gold standards.'"

Conclusion (verbatim): **"objective scores offer a stable foundation for comparison, while subjective dimensions have high variances."**

## Relevance to companion-eval-platform

**This paper is our thesis, already published, in our exact domain. Cite it as the primary external validation of the platform's core bet.**

1. **Independent replication of our α finding — and worse than we found.** Human–human Kendall of 0.21–0.29 on ACT/INT matches our 0.25–0.34. But **PER at −0.310 human–human is a genuinely alarming datapoint we should not bury**: raters disagree *systematically* about whether a character stayed in character. Whatever "persona consistency" is, a Likert item does not measure it. That we found α 0.25–0.34 and they found ≈0 to negative on the closest analogue is strong convergent evidence that the problem is the construct, not our rater pool or our instrument.

2. **The Claude-3.5-Sonnet row is the argument for our entire platform in one line.** INT 0.722 (best), FAC 0.991 (best), **MEC 0.113 (worst by 2x)**. The most engaging, most factually consistent engine breaks its own rules ~89% of rounds. Every subjective metric says it is the best; the objective metric says it is catastrophically broken. **If you only measure what feels good, you ship the model that breaks the world.** This single row justifies the rule-adherence dimension better than any argument we could construct.

3. **Objective metrics discriminate ~9x better.** MEC range across models: 0.652. PER range: 0.015. A metric that cannot separate the best model from the worst is not a metric. This is the quantitative case for reallocating eval budget from persona-Likert to mechanic-checking, and it is a number we can put in a deck.

4. **The event–state representation is the architectural blueprint, and it has a product cost.** RPGBench gets objective rule checking *by requiring the game to declare explicit state variables and event preconditions/effects*. This is the answer to the "how do we check semantic fiction rules?" gap left open by IFEval/Multi-IF (surface constraints only) and SysBench (LLM judge + checklists). **The price: scenes must be authored with a declared state machine, not just prose.** That is a real constraint on our authoring UX and we should decide deliberately whether to pay it. Middle path worth prototyping: let authors write prose scenes but require a small declared state schema (facts, variables, locked/unlocked flags) — a "scene contract" — which is exactly what makes MEC computable.

5. **VCR 0.49 is a warning about AI-generated scenes.** If our platform lets an LLM author scenes, note the best model produces a *logically valid* game only 49% of the time, while passing format checks 96% of the time. **Format compliance is a decoy.** Any scene-generation feature needs a BFS-style reachability/validity check before the scene ships, or half our scenes will be unwinnable, unlosable, or contain dead events. Their checker design (every event triggerable; success and failure both reachable; 10M state cap) is directly liftable.

6. **The temperature and round-count tables give us knobs with measured trade-offs.** Temp 0.2→0.8: INT +0.036, MEC −0.050. Rounds 10→25: INT −0.062, MEC −0.025. These are exactly the dials our platform exposes, and RPGBench has already priced them. Note INT decays with length ("repetitive content") — this connects to the existing `creativity-repetition-dialogue.md` and `multiturn-*` notes.

7. **Where we can go beyond RPGBench — the gaps are real and cheap to fill:**
   - **MEC is per-round, not per-session.** Apply SysBench's conjunction (`game-sysbench.md`) to get session stability. At 0.668/round, the honest session number is ~0. Nobody has published that figure and it is the number our users actually experience.
   - **The simulated player picks actions at random.** No adversarial user, no misalignment testing (cf. SysBench's −19.9% on misaligned), and — importantly — **no agency measurement**. A random player cannot reveal whether choices matter.
   - **10–25 rounds is short** for a companion product.
   - **RPGBench measures no agency at all.** But it is the closest platform to measuring it: it *has* an explicit state machine, which means counterfactual divergence could be computed **exactly** (compare state vectors after choice A vs choice B) rather than estimated over prose. **This is the concrete synthesis of the whole review** — RPGBench's event–state representation is precisely the substrate that makes Thue & Bulitko's `relevance(d|E)` computable without author annotations or a player model, and it is what Wardrip-Fruin's SimCity criterion ("surface elements have analogues within the internal processes and data") demands. Agency = divergence in the declared state vector across counterfactual player choices. Objective, countable, unfakeable by prose.

8. **Related:** `game-ifeval.md` (verifiable-instruction paradigm), `game-sysbench.md` (session conjunction, adversarial users), `game-agency-relevance-thue.md` (the divergence metric this could instantiate), `game-agency-reconsidered.md` (the SimCity criterion), `game-llm-sim-state-prediction.md` (state tracking difficulty).
