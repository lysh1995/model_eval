---
title: "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"
url: https://arxiv.org/abs/2410.10813
authors: Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, Dong Yu
year: 2024
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# LongMemEval (ICLR 2025)

**Status: contains the single most important calibration number in this whole review — an LLM grader at >97% agreement with human experts — and it partially closes a gap note 08 claims is open.**

Full text: https://arxiv.org/html/2410.10813v2

## What it is

**500 meticulously curated questions** embedded in "freely scalable user-assistant chat histories." Evaluates **five core long-term memory abilities**: information extraction, multi-session reasoning, temporal reasoning, **knowledge updates**, and abstention.

## Question types

| Type | Definition (verbatim/near) |
|---|---|
| **Single-session-user** | memorizing information mentioned by the user within one session |
| **Single-session-assistant** | recalling details provided by the assistant in a single session |
| **Single-session-preference** | utilizing user information to generate personalized responses |
| **Multi-session (MR)** | aggregating user information across multiple sessions |
| **⭐ Knowledge-update (KU)** | "the ability to recognize the **changes in the user's personal information** and **update the knowledge of the user dynamically over time**" |
| **Temporal-reasoning (TR)** | reasoning with both metadata timestamps and explicit time references |
| **Abstention (ABS)** | **30** modified "false premise" questions testing correct refusal to answer |

Per-category counts are not broken out in the paper beyond ABS=30; total is 500.

## ⭐ Correction to note 08

Note 08 §3.2 states: *"Nothing in the long-context/memory literature evaluates facts that were later changed... Every benchmark tests static recall."*

**This is not quite right — LongMemEval's Knowledge-Update category is exactly that construct**, and it is an ICLR 2025 paper. The gap should be restated more narrowly and it survives in the restated form:

- LongMemEval KU tests **the user's** facts changing in **assistant chat** (life states, preferences) — factual, retrieval-shaped, single-correct-answer.
- Our gap is **the character's / world's** facts changing in **roleplay**, where supersession is often *narrative* (a relationship evolves, a secret is revealed recontextualizing earlier events) and where the correct behavior isn't answering a question but *not contradicting yourself while continuing to improvise*.
- LongMemEval also can't distinguish **licensed revision** from **unlicensed retcon**, because in assistant chat only the user asserts facts. In roleplay the *model* asserts facts too, and that asymmetry is the whole problem.

**Net: the contribution is still real, but the note must cite LongMemEval as prior art and claim the narrower delta, or a reviewer will find it in ten seconds.** Update note 08 §3.2.

## Scale

- **LongMemEval_S**: ~**115,000 tokens** per question
- **LongMemEval_M**: **500 sessions** per question, ~**1.5 million tokens**
- Most questions require evidence from **multiple sessions (up to six)**

## Results

**Commercial systems:**

| System | Accuracy |
|---|---|
| Offline Reading (GPT-4o) | **91.84%** |
| ChatGPT (GPT-4o) | 57.73% |
| Coze (GPT-4o) | 32.99% |

The Offline-Reading vs ChatGPT gap (91.84 → 57.73) is the "it's not the model, it's the memory system" result — **34 points** from architecture, not capability. Consistent with note 08's MemGPT +60.4 finding.

**Long-context LLMs on LongMemEval_S — performance drop vs oracle (Figure 3b):**

| Model | Drop |
|---|---|
| GPT-4o | **30.3%** |
| Llama 3.1 70B Instruct | **55.1%** |
| Llama 3.1 8B Instruct | 36.1% |
| Phi-3 128k | 45.9% |
| Phi-3.5 Mini | 48.1% |

Note Llama-3.1-**70B** drops *more* than **8B** (55.1% vs 36.1%) — another instance of note 08's orthogonality thesis: **the bigger model is the worse model on conversational memory.** Add this as a fourth independent vote alongside MemGPT DMR's GPT-4 32.1% < GPT-3.5 38.7%.

## ⭐ Grading — the number that matters

> employs "a LLM to assess response quality" using "prompt-engineer[ing] the **gpt-4o-2024-08-06** model via the OpenAI API"

> "A meta-evaluation study demonstrates that the evaluator achieves **more than 97% agreement with human experts**."

Human experts manually evaluated **97 questions** for the commercial-systems arm.

**This is the central argument for the entire world-state thesis, and it should be quoted in the pitch.** Put it next to our own numbers:

| Construct | Instrument | Agreement |
|---|---|---|
| Roleplay aesthetic quality | 5 human annotators | **Krippendorff α = 0.25–0.34** |
| Character consistency | LLM judge vs human | **Spearman 0.435–0.460** |
| **Factual memory correctness** | **LLM judge vs human experts** | **>97%** |

**Same technology. Same judge family. Radically different reliability — because the construct changed.** The instability is not in the LLM; it is in the question. Ask "is this good?" and you get α=0.3. Ask "does this contradict that?" and you get 97%. **This is the empirical foundation for preferring world-state dimensions, and it is not our claim — it is ICLR 2025's.**

⚠️ **Caveats, stated so we don't oversell it:**
- 97% is agreement on **grading answers to closed questions with a known gold answer**, not on **detecting contradictions in open-ended prose**. Our task is strictly harder: the gold answer isn't given, the auditor must *find* the conflicting pair. Do not transfer 97% to our setting — transfer the *direction*, not the magnitude.
- n=97 questions for the meta-eval. A 97% agreement on n=97 has a 95% CI of roughly [91%, 99%] — fine, but not the "97.0%" precision the phrasing implies.
- "Agreement with human experts" ≠ Krippendorff α; it's raw agreement, which ignores chance. On a task with a skewed label prior, raw agreement flatters. The α-equivalent would be lower. **We are comparing a raw-agreement number to an α number in the table above — that comparison is directionally right but technically apples-to-oranges, and someone will catch it.** Get the chance-corrected figure before putting that table in a deck.

## Relevance to companion-eval-platform

1. **⭐ The 97% vs α=0.3 contrast is the thesis.** But cite it carefully (see caveats) — it justifies the *direction* of the bet, not a specific expected accuracy.
2. **Knowledge-update is prior art for our superseded-facts claim.** Restate the claim narrowly (§ above) and update note 08.
3. **Abstention (30 false-premise questions) is a design we should copy.** Our analogue: the user asserts a "fact" that was never established, and the correct behavior is to *not* accept it. This is RAIDEN's Script-Contradictory Knowledge (note 01 §4) arrived at independently from the memory literature. **Two independent votes for the same probe — build it.**
4. **The 115k-token / 6-session evidence structure matches our 100-turn dialogues** far better than DMR's 60 messages. If we need an external validity check for a memory metric, LongMemEval is the benchmark to port to, not DMR.
5. **Llama 70B < 8B** — a fourth vote for the orthogonality thesis. Feed to note 08 §1.0.
