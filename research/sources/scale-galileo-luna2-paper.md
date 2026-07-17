---
title: "Luna-2: Scalable Single-Token Evaluation with Small Language Models"
url: https://arxiv.org/abs/2602.18583
org: Galileo
year: 2026
type: paper
accessed: 2026-07-16
topic: production-scale
---

# Luna-2 (Galileo) — arXiv 2602.18583

**Submitted:** February 20, 2026
**Authors:** Vatsal Goel, Rishon Dsouza, Nikhil Ega, Amey Ramesh Rambatla, Rob Friel, Shuai Shao, Yash Sheth

## The problem statement — verbatim, and it is the thesis of the whole space

"**Real-time guardrails require evaluation that is accurate, cheap, and fast — yet today's default, LLM-as-a-judge (LLMAJ), is slow, expensive, and operationally non-deterministic due to multi-token generation.**"

Three named defects of LLM-as-judge for the *inline* path:
1. slow
2. expensive
3. **operationally non-deterministic due to multi-token generation** ← the subtle one. Sampling from a multi-token decode means the same input can yield different verdicts. A guardrail must be deterministic to be auditable/testable.

## Headline numbers (abstract)

- **Accuracy**: "Matches state-of-the-art LLM-based evaluators across content safety and hallucination benchmarks"
- **Cost**: "**over 80x reduction** in inference expenses"
- **Latency**: "**over 20x reduction**"
- **Production scale**: "currently protecting **100M+ AI sessions** and processing **100B+ tokens monthly**"
- **Annual savings**: "over **$30M** in evaluation costs"

These are the only published hard production-scale numbers found across all nine platforms surveyed.

## Architecture — single-token evaluation

Core innovation: models "provide evaluation scores using **just one token output**" rather than generating extended reasoning or multiple tokens.

Mechanism (per Galileo docs): classification via "**normalized log-probabilities of True/False tokens**." The verdict is read directly off the logits of a single forward pass — no decoding loop. This is what buys determinism *and* the 20x latency cut simultaneously: one forward pass, argmax/logprob read, done. The score is a continuous probability, so thresholds are tunable without retraining.

**Trade-off**: no chain-of-thought, so no free-text rationale for the verdict. Buying speed/determinism costs explainability — relevant if you need to show users *why* something was blocked.

## Multi-metric serving — LoRA adapters on a shared backbone

Verbatim: "The system uses **lightweight LoRA/PEFT heads on a shared backbone**, enabling **hundreds of specialized metrics** to operate **concurrently on single GPU** infrastructure with local deployment capabilities."

This is the structural answer to "how do you run 20 checks without 20x the cost": the backbone forward pass is shared; each metric is a cheap adapter head. Cost is roughly O(1) in the backbone + O(n) in tiny heads, not O(n) full models. Compare with W&B Weave's software-level analogue (batch N signals into 1 LLM call) — same amortization instinct, different layer.

Baselines referenced in the paper: Llama 3, Mistral 7B, Qwen3, DeBERTa, DistilBERT. Comparisons against GPT-4 and other LLM judges across Tables 3, 5, 6, 7, 8 (table values not extractable from the PDF text layer).

## Why this matters for the tiering question

The paper's implicit argument: **if your evaluator is fast and cheap enough, you don't need to sample at all.** Galileo's marketing states this directly — sub-200ms latency makes "100% traffic monitoring economically feasible." Sampling is a workaround for expensive evaluators; a purpose-built SLM evaluator dissolves the tradeoff rather than managing it.
