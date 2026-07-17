---
title: "From Static Context to Calibrated Interactive RL: Mitigating Distribution Shift in Multi-turn Dialogue with Aligned Simulator"
url: https://arxiv.org/abs/2605.26403
authors: Xiaohua Wang, Jiakang Yuan, Zisu Huang, Muzhao Tian, Changze Lv, Kaitao Song, Chen Tao, Xiaoqing Zheng (Fudan University)
year: 2026
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# From Static Context to Calibrated Interactive RL

arXiv:2605.26403v1, posted May 26, 2026.

**Status: this is the formal backbone of the off-policy argument for replaying user turns.** The paper is about *training*, but its Theorem 3.1 is a statement about any use of static/replayed dialogue context, evaluation included.

## Abstract (as extracted)

The authors propose Calibrated Interactive RL to address limitations in multi-turn dialogue training. They theoretically demonstrate that **both static context and uncalibrated interactive approaches suffer from context distribution misalignment**, where discrepancies between training and real conversation histories accumulate. Their framework couples interactive policy optimization with simulator alignment via supervised fine-tuning.

## The two error sources (both relevant to us)

### 1. Policy-Induced Shift (the static/replay problem)

Training on fixed offline histories creates mismatch between observed and self-generated trajectories.

> "errors compound quadratically over turns and severely degrades dialogue quality."

This is *our* problem: our user turns were produced against a different model. Replaying them onto a new variant means the new model is conditioned on a history it would never have generated.

### 2. Simulator-Induced Shift (the live-simulation problem)

Uncalibrated simulators exhibit artifacts like **sycophancy**, causing the learned policy to exploit simulator weaknesses rather than solve actual tasks.

This matters because it blocks the naive fix. "Just use a live LLM user simulator instead of replaying" trades one bias for another.

## Theorem 3.1 (verbatim form)

Performance degradation is bounded by:

> |J(π) − J(π′)| ≤ R_max · Σ(H−i)·ε_i

This establishes **quadratic error accumulation**: small per-step deviations (ε_t) compound to **O(H²)** total error across horizon H.

The recurrence relation: **Δ_{t+1} ≤ Δ_t + ε_t**, which telescopes into quadratic growth.

**Read the (H−i) weight carefully — it is the single most actionable thing in this paper for us.** A deviation at step `i` is weighted by how many turns remain. An early-turn mismatch is weighted ~H; a late-turn mismatch is weighted ~1. So the off-policy penalty of replaying is **concentrated in early turns** and decays linearly. For our H≈100 dialogues, a divergence at turn 5 is ~20× more damaging to validity than one at turn 95.

## Off-policy problem articulation

The authors emphasize that static methods **ignore how policy π influences future histories**, optimizing under data distribution `d^data_t` rather than the on-policy distribution `d^π_t`, creating systematic bias in sequential decision-making.

## Quantitative findings

| Method | MATH-Chat accuracy | Doc editing (BLEU) |
|---|---|---|
| Static Context | 85.0% | 33.8 |
| Naive Interactive (uncalibrated simulator) | — | **26.1** (severe reward hacking) |
| Calibrated Interactive (theirs) | **91.5%** (+6.5pp) | 34.6 |

The Naive Interactive → 26.1 BLEU collapse is the evidence that an unaligned user simulator is *worse than replay*, not better. Replay is a biased-but-bounded estimator; a bad simulator is an unbounded one because the policy can actively exploit it.

## Relevance to companion-eval-platform

- Gives us the formal vocabulary: replaying user turns = evaluating under `d^data` not `d^π`. This is textbook **off-policy evaluation** and is *biased*, with bias growing in horizon.
- **O(H²) with (H−i) weighting** ⇒ the bias is real but front-loaded. Our 100-turn dialogues are deep in the regime where the bound is loose.
- Crucially: the bound is on *policy value* J(π), i.e. on **task success**. It does not say replay is invalid for every measurement — it says replay mis-estimates the quantity that depends on the model steering the conversation. Measurements of *properties of the model's own output given a fixed context* (persona adherence, repetition, style) are far less exposed to this bias than measurements of *conversational outcome*.
- The sycophancy/reward-hacking result warns us off "just swap in a live simulator" as a clean fix.
