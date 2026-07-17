---
title: "MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback"
url: https://arxiv.org/abs/2309.10691
authors: Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, Heng Ji
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# MINT (ICLR 2024)

Full text read from arxiv HTML: https://arxiv.org/html/2309.10691v3

## What it is

Benchmark evaluating LLMs' ability to solve tasks with multi-turn interactions by (1) using tools and (2) leveraging natural language feedback. Tools are accessed by the LLM **executing Python code**; user natural language feedback is **simulated by GPT-4**. 20 open- and closed-source LLMs evaluated.

## UNIT OF EVALUATION — per-task-instance / per-trajectory, NOT per-response

This is the single most important structural fact for our purposes. MINT does **not** score individual responses. It scores whether an entire multi-turn *trajectory* solved the task:

> "Success Rate SR measures the percentage of successful task instances."

The metric is **micro-averaged across all 586 task instances**. A trajectory is one interaction episode run from scratch under a turn budget. So the unit of evaluation = **one task instance's whole interaction trajectory**, binary success/failure.

Critically, the turn budget is a *re-run*, not a prefix:

> "For interaction limit k, we start from scratch and allow each LLM to interact up to the k-th turn and measure their corresponding SR_k."

i.e. SR_1 … SR_5 are **five independent evaluation runs at different budgets**, not five checkpoints inside one conversation. Worth internalizing before borrowing this design — it is expensive (5x rollouts) but avoids prefix-contamination across budgets.

## Dataset composition (Table 1)

| Task type | Source | Original | MINT |
|---|---|---|---|
| Code Generation | HumanEval | 164 | 45 |
| Code Generation | MBPP | 500 | 91 |
| Decision Making | ALFWorld | 134 | 134 |
| Reasoning | GSM8K | 1,319 | 48 |
| Reasoning | HotpotQA | 7,405 | 43 |
| Reasoning | MATH | 5,000 | 100 |
| Reasoning | MMLU | 13,985 | 76 |
| Reasoning | TheoremQA | 800 | 49 |
| **Total** | | **29,307** | **586** |

Three task types: **reasoning (316), code generation (136), decision-making (134)**. Curated down from 29,307 → **586 instances** "into a compact subset for efficient evaluation."

## TURN-DEPTH FINDING #1 — success rate rises with k, but with diminishing returns

Headline claim, verbatim:

> "All models benefit from tool interaction and natural language feedback, with absolute performance gains by 1–8% for each additional turn of tool use, and 2–17% with natural language feedback."

So: **+1–8% absolute per additional tool-use turn**, **+2–17% absolute from natural language feedback**.

SR by interaction limit k = 1 → 5 (micro-average, Table 2):

| Model | k=1 | k=2 | k=3 | k=4 | k=5 |
|---|---|---|---|---|---|
| gpt-3.5-turbo-0613 | 2.7% | 16.9% | 24.1% | 31.7% | 36.2% |
| claude-2 | 26.4% | 35.5% | 36.0% | 39.8% | 39.9% |
| claude-instant-1 | 12.1% | 32.2% | 39.2% | 44.4% | 45.9% |
| LLaMA-2-70B (base) | 1.9% | 19.4% | 24.6% | 26.4% | 26.4% |
| CodeLLaMA-34B (base) | 0.2% | 16.2% | 23.0% | 25.9% | 28.2% |
| Lemur-v1-70B (SIFT) | 3.8% | 27.0% | 35.7% | 37.5% | 37.0% |

gpt-4-0613 reported at **69.5% (SR_5)** — the top scorer.

Two things to note in this table:
- The **k=1 → k=2 jump is by far the largest** (gpt-3.5-turbo: 2.7 → 16.9; LLaMA-2-70B: 1.9 → 19.4). Gains then flatten hard.
- **Curves saturate or invert by k=5.** LLaMA-2-70B is flat 26.4% → 26.4% (k=4→5). Claude-2 is essentially flat 39.8% → 39.9%. **Lemur-v1-70B-SIFT actually goes DOWN, 37.5% → 37.0%.** More turns is not monotonically better.

## Metric definitions (verbatim)

> "quantify LLMs' tool-augmented task-solving capability by (1) absolute performance SR_5 and (2) improvement per additional interaction turn Δ_tools estimated as the slope b from least-square regression"

- **Δ_tools** = slope *b* from least-squares regression of SR over k. Per-turn improvement rate.
- **Δ_feedback** = `SR⁵_feedback − SR_5` — the SR delta at budget 5 when GPT-4-simulated language feedback is provided vs not.

Example Δ_feedback values (Table 3):
- gpt-3.5-turbo: **+15.2%**
- CodeLLaMA-13B (base): **+13.5%**
- LLaMA-2-70B (base): **+8.9%**

## TURN-DEPTH FINDING #2 — SIFT/RLHF models can get WORSE with more turns

> "Surprisingly, on the LLMs evaluated, supervised instruction-finetuning (SIFT) and reinforcement learning from human feedback (RLHF) generally hurt multi-turn capabilities."

Exact deltas:

> "SIFT hurts Codellama-34B's multi-turn performance by 11.1% and 15.4% (w/ feedback), and RLHF negatively affects LLaMA-2-70B by 8.5% and 8.7%, respectively."

- **SIFT on CodeLLaMA-34B: −11.1%** (no feedback), **−15.4%** (with feedback)
- **RLHF on LLaMA-2-70B: −8.5%** (no feedback), **−8.7%** (with feedback)

On the improvement *rate* (Δ_tools slope), RLHF alignment on the LLaMA-2 series costs **−0.7% to −2.6%**.

This is the alignment-tax-on-multi-turn result. The models most tuned to produce a good *single* reply are measurably worse at *using* additional turns. Directly relevant to companion characters, where the whole product is turn 20, not turn 1.

## SINGLE-TURN vs MULTI-TURN GAP — explicit finding

> "Better single-turn performance does not necessarily entail better multi-turn performance. For example, while Claude-2 outperforms its predecessor Claude-1 in single-turn evaluation, the latter benefit more from interaction and performs better with >2 turns."

Confirmed in the SR table: **model ranking reorders as k grows.** At k=1 claude-2 leads claude-instant-1 by a wide margin (26.4% vs 12.1%); by k=5 the ordering has **flipped** (39.9% vs 45.9%). A single-turn leaderboard would have ranked these two backwards for any multi-turn use case.

Same pattern gpt-3.5-turbo vs LLaMA-2-70B: near-identical at k=1 (2.7% vs 1.9%), 10 points apart by k=5 (36.2% vs 26.4%).

## Takeaways for a companion/roleplay eval platform

- Turn-budget sweeps (k=1..5, each a fresh rollout) surface rank inversions that single-turn evals structurally cannot see. This is the strongest published evidence that we cannot infer multi-turn quality from single-turn scores.
- Per-trajectory binary success is a clean unit but assumes a *task* with a verifiable goal. Companion dialogue has no task oracle — MINT's metric shape does **not** port directly; the turn-budget *experimental design* does.
- The SIFT/RLHF regression predicts that heavily-RLHF'd base models may underperform on our long-conversation evals despite strong single-response benchmarks.

## Verification notes

- Abstract, Table 1 (dataset composition), the 1–8% / 2–17% claim, the SIFT/RLHF percentages, the Claude-1/Claude-2 single-vs-multi-turn quote, and the SR_k / Δ_tools / Δ_feedback definitions were all read directly from the arxiv HTML full text and are quoted verbatim above.
- Table 2 SR values are transcribed for a representative subset of models, not all 20. The gpt-4-0613 value (69.5%) was captured at SR_5 only; its k=1..4 values are not recorded here.
- Δ_feedback examples are a subset of Table 3, not the full table.
