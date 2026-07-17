---
title: "Measuring and Controlling Persona Drift in Language Model Dialogs (a.k.a. Measuring and Controlling Instruction (In)Stability in Language Model Dialogs)"
url: https://arxiv.org/abs/2402.10962
authors: Kenneth Li, Tianle Liu, Naomi Saphra, Jiawei Zhou, Martin Wattenberg (Harvard VCG)
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Measuring and Controlling Persona Drift in Language Model Dialogs

Code: https://github.com/likenneth/persona_drift
OpenReview (COLM version, retitled "Instruction (In)Stability"): https://openreview.net/forum?id=60a1SAtH4e

**Status: the most directly on-topic prior work for our persona-consistency axis.**

## Core claim (abstract)

Prompting is the standard tool for customizing chatbots to a persona, with "an implicit assumption that prompts will be stable" so the chatbot keeps the persona for the duration of the conversation. The authors propose a quantitative benchmark to test this assumption and find **significant persona drift within eight rounds of conversation** in LLaMA2-chat-70B.

## Benchmark methodology: LTM (self-chat) protocol

**Self-chat protocol:**
- Two personalized chatbots converse. One (the *agent*) is tested for persona adherence; a *user* chatbot initiates with "a randomly selected conversation starter."
- Conversation runs to a preset length (**8 rounds**).
- **Probe questions are injected at each turn** to measure persona stability — this is the key mechanic: the persona is measured by an out-of-band probe, not by judging the conversational reply itself.

**Dataset:**
- **100 persona system prompts** across **5 categories**
- each with corresponding **probe questions** and a **persona measure function**
- results averaged across **200 conversations** using random persona pairs

## Metric definition (verbatim)

Persona stability is quantified as:

> fB(bi'|ai=pB)

where `fB` returns a score between **0 and 1 deterministically** based on adherence to the specified persona.

**Note the design choice: the persona measure is a DETERMINISTIC FUNCTION, not an LLM judge.** Personas are chosen so that adherence is programmatically checkable (e.g. "always answer in French", "always respond in rhyme"). This removes judge noise from the drift measurement — an important trick if we want drift curves we can trust.

## Drift magnitude and shape

- **LLaMA2-chat-70B: persona consistency degrades by more than 30% after just 8–12 dialogue turns.**
- Across 200 conversations, the agent "gradually loses its original persona over dialogue turns."
- **Bidirectional drift / persona contagion**: the model "gradually adopts the persona of the user LM over extended rounds of conversation." The agent does not merely decay toward a neutral default — it is *pulled toward its interlocutor*.

The contagion finding is significant for us: in companion roleplay, the user turns are themselves in-character, so drift may be *toward the user's implied persona*, not just toward assistant-default. And it predicts **homogenization**: two characters conversing (or two characters driven by similar user turns) converge.

## Mechanism: attention decay

Researchers tracked **π(t)** = "the sum of the attention weights allocated to" system prompt tokens throughout generation.

Findings:
- **Within** a single turn: attention to the system prompt remains "almost constant"
- **Across** conversation turns: "significant decreases" occur
- By **turn 8**: substantial attention decay to early prompt tokens is observable

Theoretical framing: the system prompt's efficacy decreases as attention to initial tokens wanes — the prompt is progressively diluted by accumulating dialogue history.

**Implication: drift is a structural consequence of the architecture, not a model-quality defect.** It should be expected to appear in every model we test, differing in rate rather than kind. And it predicts drift is a function of *context tokens accumulated*, not *turn count per se* — which is testable on our data (do verbose models drift faster per turn?).

## Mitigation: split-softmax

**Mechanism:** reweights attention distributions using power-law scaling:

> αt,i' = (πk(t)/π(t)) · αt,i

for system prompt tokens, where **k (0≤k≤1)** controls intervention strength. Training-free and parameter-free, applied at inference time.

**Results:** compared against two baselines — **System Prompt Repetition** and **Classifier-Free Guidance** — split-softmax "provides a better trade-off between persona stability and performance" across hyperparameter sweeps on MMLU, achieving equivalent stability with less context-window consumption.

That System Prompt Repetition is a *baseline that works* is notable: it means any product that re-injects the character card each turn will show less drift, so our eval must record whether re-injection is happening or we'll be measuring the harness, not the model.

## Relevance to companion-eval-platform

- Validates our central premise with hard numbers: **>30% persona degradation by turn 8–12**. Our dialogues are ~100 turns — an order of magnitude past where drift is already documented as severe.
- **Probe-injection is a directly adoptable method**: interleave out-of-band probes into our replayed dialogues at fixed turn indices and measure a deterministic persona function. Gives a clean drift curve vs. turn index, free of judge noise.
- **Persona contagion → homogenization** is the mechanistic link between our "personality drift" and "homogenization across characters" failure modes. They may be the same phenomenon measured at different units of analysis (single character over turns vs. character cohort at fixed turn).
- **Attention decay** predicts drift correlates with cumulative context length; our en/zh split is a natural experiment here (different tokenization → different token counts for same turn count).
