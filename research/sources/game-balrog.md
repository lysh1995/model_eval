---
title: "BALROG: Benchmarking Agentic LLM and VLM Reasoning On Games"
url: https://arxiv.org/abs/2411.13543
authors: Davide Paglieri, Bartłomiej Cupiał, Samuel Coward, Ulyana Piterbarg, Maciej Wołczyk, Akbir Khan, Eduardo Pignatelli, Łukasz Kuciński, Lerrel Pinto, Rob Fergus, Jakob Nicolaus Foerster, Jack Parker-Holder, Tim Rocktäschel (UCL; University of Warsaw; IDEAS NCBR; NYU; Oxford; Meta)
year: 2024 (ICLR 2025)
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# BALROG: Benchmarking Agentic LLM and VLM Reasoning On Games

**Sourcing note:** all numbers extracted from the arXiv PDF (`arxiv.org/pdf/2411.13543`, 36pp) via pypdf. Tables 2 and 3 were **independently verified against the arXiv HTML v2** — both agree exactly. Published as a conference paper at **ICLR 2025**. Leaderboard: balrogai.com

## Abstract (verbatim)

> Large Language Models (LLMs) and Vision Language Models (VLMs) possess extensive knowledge and exhibit promising reasoning abilities, however, they still struggle to perform well in complex, dynamic environments. Real-world tasks require handling intricate interactions, advanced spatial reasoning, long-term planning, and continuous exploration of new strategies... we introduce BALROG, a novel benchmark designed to assess the agentic capabilities of LLMs and VLMs through a diverse set of challenging games... we find that current models achieve partial success in the easier games, they struggle significantly with more challenging tasks... several models perform worse when visual representations of the environments are provided, indicating severe deficiencies in vision-based decision-making.

## Contributions (verbatim)

> - BALROG, a suite of six reinforcement learning environments for testing the agentic capabilities of long-context LLMs. We provide a fine-grained metric for model evaluation, and we develop a novel data-informed progression system for NetHack.
> - Baseline evaluations of state-of-the-art LLMs on BALROG using zero-shot prompting, in both Language-Vision and Language-only modalities...
> - We perform a qualitative analysis of the results across capabilities such as spatial reasoning, systematic exploration, and long-term planning. **We identify an intriguing knowing-doing gap where the models cannot employ the knowledge they possess.**

## Environments (§2.1)

- **BabyAI** (Chevalier-Boisvert et al. 2019; Carta et al. 2023) — 2D grid-world, natural-language tasks (e.g. *"go to the blue ball, then pick up the grey key"*). Five navigation task types.
- **Crafter** (Hafner 2021) — Minecraft-inspired grid; explore, gather resources, craft items. Scored on milestones achieved.
- **TextWorld** (Côté et al. 2018) — text adventure. See `game-textworld.md`.
- **Baba Is AI** — puzzle game requiring manipulation of the rules themselves.
- **MiniHack** — multi-task roguelike framework.
- **NetHack (NLE)** — extreme complexity roguelike.

### Table 1: Tested skills, time horizons, complexities (VERBATIM)

| Skills | BabyAI | TextWorld | Crafter | Baba Is AI | MiniHack | NLE |
|---|---|---|---|---|---|---|
| Navigation | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Exploration | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Resource Management | ✗ | ✔ | ✔ | ✗ | ✔ | ✔ |
| Complex Credit Assignment | ✗ | ✗ | ✔ | ✔ | ✔ | ✔ |
| Deducing Env. Dynamics | ✗ | ✗ | ✗ | ✔ | ✔ | ✔ |
| Long-term Planning | ✗ | ✗ | ✗ | ✔ | ✔ | ✔ |
| **Turns to Complete** | 10¹ | 10² | 10³ | 10² | 10² | 10⁴–10⁵ |
| **Time to Master for Humans** | Seconds | Minutes | Hours | Hours | Hours | **Years** |

## Metrics (§3.1, verbatim)

> To ensure a fair and interpretable evaluation, we introduce a standardized metric, scoring performance on each task within a range of 0 to 100. For environments like **MiniHack, BabyAI, and Baba Is AI, each episode is scored as either 0 or 100 based on task completion.** For **TextWorld, Crafter, and NetHack** we use as the score a real number between 0 and 100, representing the **proportion of achievements toward the maximum score.** For NetHack, as the game scoring system does not adequately reflect actual progression (Wołczyk et al., 2024), we propose a novel, data-informed progression metric, described in Appendix F.2.

## ★ Invalid-action handling — the rule-adherence hook (§3.1, VERBATIM)

This is the passage most directly relevant to us, and it is easy to miss:

> To address cases where the LLMs/VLMs output **hallucinated or invalid actions**, BALROG provides feedback to the agent indicating the action's invalidity, it then **executes a default fallback action** (such as a "do-nothing" action or a standard move like "north"), and **logs the occurrence for trajectory statistics**. This ensures that the interaction remains continuous and robust while **enabling users to analyze the context and frequency of such errors in post-evaluation analysis.**

**BALROG counts invalid actions.** It does not enumerate a legal action list and force a choice from it — the agent emits a free-form natural language string and the harness detects invalidity, logs it, and continues. This is the opposite design choice from GAMEBENCH (see `game-gamebench.md`), which hands the agent an enumerated `available actions` list so illegal moves are *structurally impossible* and therefore *unmeasurable*. **BALROG is the better citation for rule-adherence-as-measured-quantity.** Caveat for honesty: the paper *provides the logging affordance* but does **not report an invalid-action rate table** in the results — the instrumentation exists, the published metric does not.

Also from §3.1:

> To perform successfully in BALROG, models must demonstrate robust instruction-following capabilities, including reading and interpreting game rules, understanding the action space, and producing valid actions to complete tasks effectively.

## Evaluation protocol (§3)

Zero-shot prompting only. History length **16 observations** across all tasks. Initial prompt introduces game rules and a list of available actions with brief descriptions; subsequent prompts present observation-action history in chat format (game rules and observations as "user", prior actions as "assistant"/"model"). A general prompt not tuned to any specific LLM. Multiple seeds per environment; standard error obtained from replicate seeds.

Models: Gemini-1.5-Flash, Gemini-1.5-Pro, GPT-4o-mini (2024-07-18), GPT-4o (2024-05-13), Claude 3.5 Sonnet, Claude 3.5 Haiku (2024-10-22 releases), Llama 3.1 instruct (8B, 70B), Llama 3.2 instruct (1B, 3B, 11B, 90B). **o1-preview (2024-09-12) tested exclusively on NetHack due to budget constraints.**

## RESULTS

### Table 2: Language-Only Performance (VERBATIM)

| Model | Average Progress (%) |
|---|---|
| claude-3.5-sonnet | **32.64 ± 1.93** |
| gpt-4o | 32.34 ± 1.49 |
| llama-3.1-70b-it | 27.88 ± 1.43 |
| llama-3.2-90B-it | 27.29 ± 1.44 |
| gemini-1.5-pro | 21.00 ± 1.18 |
| claude-3.5-haiku | 19.32 ± 1.83 |
| gpt-4o-mini | 17.36 ± 1.35 |
| llama-3.2-11B-it | 16.82 ± 1.47 |
| llama-3.1-8b-it | 15.14 ± 1.55 |
| gemini-1.5-flash | 14.63 ± 1.37 |
| llama-3.2-3B-it | 10.13 ± 1.28 |
| llama-3.2-1B-it | 6.65 ± 1.04 |

### Table 3: Vision-Language Performance (VERBATIM)

| Model | Average Progress (%) |
|---|---|
| claude-3.5-sonnet | **35.48 ± 2.02** |
| gemini-1.5-pro | 25.76 ± 1.36 |
| gpt-4o | 22.56 ± 1.44 |
| llama-3.2-90B-it | 20.99 ± 1.58 |
| gpt-4o-mini | 15.36 ± 1.29 |
| gemini-1.5-flash | 14.94 ± 1.40 |
| llama-3.2-11B-it | 8.43 ± 1.26 |

**The vision drop:** GPT-4o falls **32.34 → 22.56** (−9.78) when given images alongside text. Llama-3.2-90B falls **27.29 → 20.99** (−6.30). Claude 3.5 Sonnet *rises* 32.64 → 35.48 and Gemini-1.5-Pro rises 21.00 → 25.76. So "models perform worse with vision" is true of GPT-4o and Llama, not universally. TextWorld has no visual component and is excluded from the vision format — which partly explains Gemini's rise (its 0% TextWorld score drops out of the average).

### Per-environment findings (§4, verbatim)

> Most leading models demonstrate fair average progression on **BabyAI, Crafter, and Baba Is AI**, with GPT-4o and Claude 3.5 Sonnet performing best. Interestingly, the open-source Llama 3.1 70B and Llama 3.2 90B models achieve the highest results on the **Baba Is AI** language-only format, narrowly surpassing GPT-4o and Claude 3.5 Sonnet.

> In **TextWorld**, GPT-4o and Claude 3.5 Sonnet lead, while **Gemini models fail to complete any tasks, being flagged as 'unsafe' by the Google Gemini API, despite the prompts containing no actual safety concerns.**

> The **MiniHack** suite proves very challenging for all models, especially the quest and boxoban tasks, **which were never solved by any model.**

> Finally, all models flat line with **NetHack**, with the best-performing model, **o1-preview, achieving a meager 1.5% average game progression.** [elsewhere given as **1.57%**]

> Gemini-1.5-Pro lags behind the other large models, partly due to its **0% performance on TextWorld.**

**Note the Gemini-TextWorld artifact.** A model scores 0 on an entire environment because of a *safety filter false positive*, and that 0 propagates into its headline average and its published rank. The benchmark is mechanically objective and the number is still an artifact of infrastructure, not capability. Directly relevant to us: a refusal-shaped failure and an incapability-shaped failure are indistinguishable in the aggregate score.

## ★ Qualitative analysis (§4.1) — the knowing-doing gap

**Spatial Reasoning:**
> While language models demonstrate some proficiency in basic navigation, they exhibit significant limitations in more complex spatial reasoning tasks. In the BabyAI suite, we observed **significant shortcomings in the agents' ability to place objects adjacent to other objects**... In NetHack and MiniHack CorridorBattle, good spatial reasoning is crucial during combat... **the agents frequently ended up cornered.**

**Systematic Exploration:**
> In TextWorld's Coin Collector, where agents must explore a house to locate a coin, **agents often wander aimlessly, revisiting rooms they've already explored while missing important areas entirely.** An efficient agent would behave in DFS-like manner, methodically searching each room, keeping track of visited areas and prioritizing unexplored spaces.

**Long-term planning:**
> We observe **near-zero performance on MiniHack, and NLE**, which both require careful planning. In particular, **we do not observe a single successful trajectory in the Boxoban logical puzzles in MiniHack**, which requires careful planning at every step in order to avoid irreversible failures. LLMs, with the finite amount of compute available to them in a single forward pass, are necessarily confined to solving some subset of reasoning problems... We see a notable improvement with OpenAI o1's chain of thought capabilities on NetHack, **performing close to three times better than its closest competitor in language-only mode Claude-3.5-Sonnet. However, its average progression of 1.57% is still far from satisfactory.**

**Knowing-Doing Gap (the headline qualitative finding), verbatim:**

> a pronounced "knowing-doing" gap, where **models execute undesirable actions during gameplay despite knowledge of their negative consequences.**

> In NetHack, models often **exit the dungeon shortly after starting the game, resulting in an instant game termination.** When queried in a separate thread about the consequences of exiting the first level in NetHack, **they correctly identify that it results in an instant death.**

> although the models correctly identify that **eating rotten food** in NetHack can result in death, this remains a **common cause of failure**, underscoring a disconnect between knowledge and decision-making.

From the intro, same finding:
> Some of the models exhibit knowledge about the game from pre-training but fail to use it in practice. For example, in NetHack, **GPT-4o often dies from the consumption of rotten food, even though, when prompted, it correctly identifies it as very dangerous.**

**Discovering and Leveraging Environment Dynamics:**
> Some games require inferring non-trivial causal structure through experimentation... a player might identify a potion of paralysis by drinking it, and then realize they can use this strategically by throwing such potions at enemies to incapacitate them... **current models struggle to formulate and execute such context-dependent strategies.**

## Relevance to companion-eval-platform

### Is the LLM the PLAYER or the SIMULATOR/GAME MASTER?

**PLAYER, unambiguously, in all six environments.** The LLM/VLM emits a natural-language action string each timestep; six pre-existing, hand-built RL simulators (BabyAI, Crafter, TextWorld, Baba Is AI, MiniHack, NetHack) own the state and the transitions. No model touches the world model. BALROG explicitly *"decouples inference-time prompting strategies from underlying models"* — the agent is conceptualized as (model × prompting strategy), and everything else is fixed infrastructure.

### Is ground-truth state available and mechanically checkable?

**Yes, totally and deterministically.** Every environment is an executable RL simulator emitting its own reward/progress signal. Scores are 0/100 completion (MiniHack, BabyAI, Baba Is AI) or a fraction of achievements toward a known maximum (TextWorld, Crafter, NetHack). Zero raters, zero rubrics, zero LLM judges anywhere in the scoring path. Standard errors come from replicate seeds, and they are published — every number in Tables 2 and 3 carries a ±.

### Why this matters given α = 0.25–0.34 on roleplay quality

**1. The invalid-action logger is the single most portable thing here.** BALROG's design — let the model emit free-form text, detect invalidity, log it, fall back, continue — is the exact shape of the rule-adherence measurement we want, and it is the *opposite* of GAMEBENCH's enumerate-and-choose design that makes violations unrepresentable. The generalizable principle: **you can only count violations you allow to occur.** Any companion harness that constrains the model into a legal action set (function calling with enum args, constrained decoding, retry-until-valid) has destroyed the measurement it was trying to make. If we want a rule-adherence number, the model must be free to break the rule and the harness must count it. BALROG built the counter and then, tellingly, didn't publish the number — we should publish it.

**2. The knowing-doing gap is our most important borrowed construct.** BALROG measures it by *asking the model in a separate thread* what happens if you eat rotten food, getting the right answer, and then observing the model eat rotten food in play. That is a **two-condition design: elicited knowledge vs. enacted behavior, same model, same fact.** The gap between them is a difference score over two objective measurements — no aesthetic judgment anywhere.

This maps onto companion evaluation almost directly. Ask the model out-of-band: *"Does Ana know that the user's brother died?"* → it answers correctly from the transcript. Then observe whether Ana, in play, references the brother as living. The discrepancy is countable, per-turn, and requires no rater. **This is the single best template in the game-benchmark literature for a companion dimension with an objective correlate**, because it sidesteps the whole problem of defining "good" — it only requires that the model be *self-consistent* between what it can state and what it does, and both halves are checkable.

**3. Fine-grained progress beats binary success, and they say why.** BALROG's stated design goal is a benchmark *"that still allows us to observe fine-grained progress"* — because binary completion on hard tasks is all zeros and yields no gradient. NetHack at 1.57% would be 0% under binary scoring, and o1's genuine 3× advantage over Claude 3.5 Sonnet would be invisible. For us: on any dimension where companions mostly fail or mostly succeed, a binary metric will have near-zero variance and near-zero discriminative power regardless of how objective it is.

### The cautions

- **The Gemini 0%-on-TextWorld artifact.** A safety-filter false positive produced a 0 that propagated into headline rank. Objectivity does not protect against infrastructure artifacts, and refusal is indistinguishable from incapacity in an aggregate score. If our companion eval has a refusal-prone dimension, refusals must be a *separate reported category*, not folded into the score.
- **The instrumentation-vs-metric gap.** BALROG *logs* invalid actions and does not *report* them. The affordance existing is not the same as the metric existing. If we cite BALROG for rule adherence, cite it for the **design**, not for a number — there isn't one.
- **o1-preview is NetHack-only** (budget constraints), so it is absent from Tables 2 and 3. Its 1.57% is not comparable to the 32.64% averages — different environment set entirely. Easy number to misquote.
- **Claude 3.5 Sonnet (32.64) and GPT-4o (32.34) are within overlapping error bars** (±1.93, ±1.49). "Claude is best" is not supported at that margin; the paper says *"followed closely by."*
