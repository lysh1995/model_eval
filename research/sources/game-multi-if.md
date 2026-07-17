---
title: "Multi-IF: Benchmarking LLMs on Multi-Turn and Multilingual Instructions Following"
url: https://arxiv.org/abs/2410.15553
authors: Yun He, Di Jin, Chaoqi Wang, Chloe Bi, Karishma Mandyam, Hejia Zhang, Chen Zhu, Ning Li, Tengyu Xu, Hongjiang Lv, Shruti Bhosale, Chenguang Zhu, Karthik Abinav Sankararaman, Eryk Helenowski, Melanie Kambadur, Aditya Tayade, Hao Ma, Han Fang, Sinong Wang (Meta GenAI)
year: 2024
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Multi-IF — IFEval's verifiable checkers, extended across turns

## Abstract (verbatim excerpt)

> "Large Language Models (LLMs) have demonstrated impressive capabilities in various tasks, including instruction following, which is crucial for aligning model outputs with user expectations."

The paper's move: existing benchmarks (IFEval) are **single-turn and monolingual**; Multi-IF extends verifiable instruction-following to multi-turn and multilingual dialogue.

## Benchmark construction

- **4,501** multilingual conversations
- **3 turns** per conversation
- **8 languages**: English, French, Russian, Hindi, Italian, Portuguese, Spanish, Chinese
- **Built by expanding the IFEval dataset** using a hybrid LLM + human annotation pipeline
- Construction stages: (1) multi-turn expansion, (2) conflict removal, (3) multilingual translation, (4) sensitive content filtering

The critical design point: **constraints accumulate**. Each turn adds a new verifiable instruction, and the instructions from prior turns *remain in force*. Turn 3 is checked against the turn-1, turn-2 and turn-3 constraints simultaneously. The "conflict removal" stage exists precisely to guarantee the accumulated constraint set stays jointly satisfiable — otherwise a failure would be ambiguous between decay and impossibility.

## Metrics

Four accuracy scores (inherited directly from IFEval's strict/loose × granularity design), averaged for the final metric:
1. Instruction-level strict accuracy
2. Conversation-level strict accuracy
3. Instruction-level loose accuracy
4. Conversation-level loose accuracy

Note IFEval's "prompt-level" becomes **"conversation-level"** — the conjunction now runs over the whole dialogue.

Two novel horizon-specific metrics:
- **Instruction Forgetting Ratio (IFR)** — the percentage of instructions that were *successfully followed in a previous turn* and are *no longer followed* in a subsequent turn. This isolates decay from incapacity: the model demonstrably could do it, then stopped.
- **Error Correction Ratio (ECR)** — the percentage of previously *unfollowed* instructions that get corrected in later turns.

IFR is the single most important metric in this paper for our purposes. It is a **clean, objective, deterministic measure of instruction decay over a horizon**, and it is only definable because the underlying checkers are programmatic.

## Results — average accuracy by turn (verbatim tables)

### Turn 1

| Model | Average | English | French | Russian | Hindi | Italian | Portuguese | Spanish | Chinese |
|-------|---------|---------|--------|---------|-------|---------|------------|---------|---------|
| o1-preview | 0.877 | 0.856 | 0.898 | 0.835 | 0.871 | 0.891 | 0.895 | 0.912 | 0.858 |
| o1-mini | 0.853 | 0.836 | 0.882 | 0.815 | 0.842 | 0.873 | 0.868 | 0.886 | 0.824 |
| GPT-4o | 0.843 | 0.874 | 0.853 | 0.789 | 0.812 | 0.878 | 0.858 | 0.876 | 0.805 |
| GPT-4 | 0.815 | 0.860 | 0.842 | 0.789 | 0.718 | 0.840 | 0.832 | 0.850 | 0.786 |
| Llama 3.1 405B | 0.854 | 0.907 | 0.868 | 0.801 | 0.825 | 0.864 | 0.876 | 0.871 | 0.817 |
| Llama 3.1 70B | 0.826 | 0.890 | 0.837 | 0.783 | 0.759 | 0.862 | 0.847 | 0.847 | 0.783 |
| Qwen-2.5 72B | 0.837 | 0.881 | 0.869 | 0.822 | 0.681 | 0.865 | 0.867 | 0.882 | 0.831 |

### Turn 2

| Model | Average | English | French | Russian | Hindi | Italian | Portuguese | Spanish | Chinese |
|-------|---------|---------|--------|---------|-------|---------|------------|---------|---------|
| o1-preview | 0.783 | 0.834 | 0.820 | 0.633 | 0.775 | 0.819 | 0.811 | 0.804 | 0.766 |
| o1-mini | 0.772 | 0.802 | 0.800 | 0.684 | 0.763 | 0.812 | 0.782 | 0.809 | 0.728 |
| GPT-4o | 0.724 | 0.784 | 0.745 | 0.601 | 0.708 | 0.760 | 0.740 | 0.749 | 0.705 |
| GPT-4 | 0.705 | 0.756 | 0.752 | 0.619 | 0.634 | 0.731 | 0.734 | 0.729 | 0.685 |
| Llama 3.1 405B | 0.782 | 0.843 | 0.822 | 0.692 | 0.754 | 0.793 | 0.801 | 0.800 | 0.748 |
| Llama 3.1 70B | 0.742 | 0.814 | 0.774 | 0.629 | 0.707 | 0.781 | 0.778 | 0.757 | 0.697 |
| Qwen-2.5 72B | 0.715 | 0.764 | 0.769 | 0.664 | 0.582 | 0.753 | 0.738 | 0.747 | 0.700 |

### Turn 3

| Model | Average | English | French | Russian | Hindi | Italian | Portuguese | Spanish | Chinese |
|-------|---------|---------|--------|---------|-------|---------|------------|---------|---------|
| o1-preview | 0.707 | 0.773 | 0.738 | 0.531 | 0.709 | 0.759 | 0.714 | 0.733 | 0.703 |
| o1-mini | 0.681 | 0.742 | 0.716 | 0.576 | 0.668 | 0.701 | 0.708 | 0.714 | 0.627 |
| GPT-4o | 0.631 | 0.701 | 0.653 | 0.501 | 0.621 | 0.647 | 0.645 | 0.645 | 0.631 |
| GPT-4 | 0.609 | 0.678 | 0.653 | 0.490 | 0.537 | 0.633 | 0.639 | 0.634 | 0.608 |
| Llama 3.1 405B | 0.707 | 0.786 | 0.753 | 0.587 | 0.677 | 0.740 | 0.727 | 0.716 | 0.670 |
| Llama 3.1 70B | 0.668 | 0.749 | 0.718 | 0.519 | 0.640 | 0.710 | 0.696 | 0.689 | 0.622 |
| Qwen-2.5 72B | 0.609 | 0.672 | 0.645 | 0.527 | 0.497 | 0.648 | 0.645 | 0.626 | 0.608 |

### Derived degradation (turn 1 → turn 3, average column)

| Model | T1 | T2 | T3 | Absolute drop | Relative drop |
|---|---|---|---|---|---|
| o1-preview | 0.877 | 0.783 | 0.707 | **−0.170** | −19.4% |
| o1-mini | 0.853 | 0.772 | 0.681 | −0.172 | −20.2% |
| GPT-4o | 0.843 | 0.724 | 0.631 | −0.212 | −25.1% |
| GPT-4 | 0.815 | 0.705 | 0.609 | −0.206 | −25.3% |
| Llama 3.1 405B | 0.854 | 0.782 | 0.707 | −0.147 | −17.2% |
| Llama 3.1 70B | 0.826 | 0.742 | 0.668 | −0.158 | −19.1% |
| Qwen-2.5 72B | 0.837 | 0.715 | 0.609 | **−0.228** | −27.2% |

## Degradation analysis (verbatim)

> "All models tested showed a higher rate of failure in executing instructions correctly with each additional turn. For example, o1-preview drops from 0.877 at the first turn to 0.707 at the third turn in terms of average accuracy over all languages."

> As the number of turns increases, LLMs "increasingly forget to adhere to instructions that were successfully executed in previous turns," which contributes to the performance degradation.

**IFR:** high-performing models (o1-preview, o1-mini, Llama 3.1) demonstrated *lower* forgetting rates than others. Turn-1 accuracy and forgetting rate are **partially decoupled** — the paper notes Qwen-2.5 72B "may achieve higher accuracy than other models, but degrades much faster than the others in later turns" (T1 0.837, above GPT-4o's 0.843's peer group, but T3 0.609, tied for last). Conversely o1-preview, o1-mini and Llama 3.1 405B "suffer less degradation."

**ECR (verbatim):** "OpenAI's o1-preview and o1-mini models exhibit the highest ECR—correcting around 25% of unfollowed instructions in later turns—suggesting that their incorporation of a hidden chain of thought is especially helpful in error correction."

## Relevance to companion-eval-platform

**This is the closest existing analogue to the rule-adherence dimension we want to ship, and it validates the whole approach.**

1. **It proves the construct is real and objectively measurable.** Rule adherence decays over turns, the decay is large (−0.15 to −0.23 absolute, 17–27% relative over just **three** turns), it is measured with zero human raters and zero LLM judges, and it cleanly separates models. This is the polar opposite of our α = 0.25–0.34 aesthetic-quality situation. Reliability here is a checker bug, not a rater disagreement.

2. **IFR is the metric to steal outright.** "Followed at turn *k*, not followed at turn *k+n*" is exactly what a scene-rule violation is on our platform. It is a within-conversation, within-model comparison, so it controls for capability entirely: the model *proved* it could satisfy the constraint, then stopped. For us: the AI honored "the tavern keeper is mute" at turn 4 and had him speak at turn 47. That is a countable event with an unambiguous ground truth.

3. **Three turns is nothing — this is a floor, not a ceiling.** Multi-IF's horizon is 3 turns and o1-preview already loses 17 points. Companion/roleplay sessions run 50–500 turns. The honest extrapolation is that unmeasured rule decay on our platform is severe. We should expect our numbers to look much worse than Multi-IF's and should *not* treat that as a bug in our harness. Building the longer-horizon version of this curve is a genuine contribution — nobody in this line has run verifiable-constraint checking out to a realistic companion-session length.

4. **The "conflict removal" stage is a requirement we must copy.** Their pipeline guarantees the accumulated constraint set is jointly satisfiable. If our scene rules can contradict each other (or contradict a user request), a violation is ambiguous between decay and impossibility, and the metric silently becomes meaningless. Any scene-rule authoring tool we build needs a satisfiability check before the scene is admissible to eval.

5. **Direction of travel confirmed:** this paper *is* the Multi-IF-shaped hole we identified. It inherits IFEval's four metrics verbatim, renames prompt-level → conversation-level, and adds two horizon metrics. Our design should be: IFEval taxonomy (`game-ifeval.md`) → Multi-IF accumulation + IFR → our extension to long horizons and in-fiction constraints.

6. **ECR is a second free metric with product meaning.** Self-correction ("the AI noticed it broke the rule and recovered") is separately countable and is arguably a *feature* users feel. 25% for reasoning models is the number to beat.

7. **Caveat:** Multi-IF's constraints are still IFEval-style *surface* constraints (word counts, formats, keywords) carried across turns, not *semantic world-state* constraints ("the door stays locked"). The gap between "checkable string predicate" and "checkable fiction predicate" is the real engineering work for us, and it is where our checkers will start to need something more than regex. See `game-llm-sim-state-prediction.md` — tracking world state is itself a task models are bad at, which means our checker may need a symbolic state model rather than a model-based one.
