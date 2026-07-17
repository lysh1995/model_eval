---
title: "Speak Out of Turn: Safety Vulnerability of Large Language Models in Multi-turn Dialogue"
url: "https://arxiv.org/abs/2402.17262"
authors: "Zhenhong Zhou, Jiuyang Xiang, Haopeng Chen, Quan Liu, Zherui Li, Sen Su (Beijing University of Posts and Telecommunications)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Speak Out of Turn: Safety Vulnerability of Large Language Models in Multi-turn Dialogue

arXiv 2402.17262, submitted 2024-02-27; revised 2024-10-30. 23 pages, 18 figures.

## Summary
The **query-decomposition** account of multi-turn jailbreaking, and a useful complement to Crescendo. Where Crescendo escalates by building on the model's own outputs, Speak Out of Turn attacks by **splitting the harmful request itself** into pieces that are individually harmless.

The core claim: "by decomposing an unsafe query into several sub-queries for multi-turn dialogue, LLMs can be induced to answer harmful sub-questions incrementally, culminating in an overall harmful response." No single turn is unsafe. Every sub-query would pass any per-message filter, because each one genuinely *is* benign in isolation. The harm exists only in the **assembly** — it lives in the union of the answers, not in any one of them.

This is the strongest theoretical argument in the literature that message-level content classification is not merely weak but **categorically unable** to see this attack class. There is nothing to detect at the message level, because the harmful object is never present at the message level. The paper frames this as revealing "current inadequacies in the safety mechanisms of LLMs in multi-turn dialogue."

The authors also make the point that multi-turn dialogue is "a crucial mode through which humans derive information from LLMs," and that prior work "predominantly focused on single-turn dialogue, ignoring the potential complexities and risks presented by multi-turn dialogue." That framing lands hard for a companion product, where multi-turn is not one mode among several — it is the only mode.

## Taxonomy / definitions (verbatim where possible)
Two attack methods:
1. **Sub-query decomposition** — breaking a single unsafe request into multiple related questions posed sequentially
2. **Incremental harmful response generation** — obtaining progressively more problematic answers across turns that collectively constitute the harmful output

Core mechanism (verbatim): "by decomposing an unsafe query into several sub-queries for multi-turn dialogue, LLMs can be induced to answer harmful sub-questions incrementally, culminating in an overall harmful response."

Motivating gap (verbatim): prior studies "have predominantly focused on single-turn dialogue, ignoring the potential complexities and risks presented by multi-turn dialogue, a crucial mode through which humans derive information from LLMs."

Finding (verbatim): the work reveals "current inadequacies in the safety mechanisms of LLMs in multi-turn dialogue."

## Key numbers (verbatim)
**No specific ASR figures or model names were retrievable from the abstract page.** The abstract states experiments were run "across a wide range of LLMs" without naming them, and gives no numerical success rates.

The full paper (23 pages, 18 figures) contains the experimental tables. Per instructions, no numbers are guessed here — fetch https://arxiv.org/pdf/2402.17262 for per-model ASRs before citing any figure from this work.

## Relevance to a roleplay/companion eval product
1. **This attack is invisible to per-message classification by construction.** Not "hard to catch" — *impossible* to catch at that layer, because the harmful artifact never appears in any single message. Combined with Crescendo's multiturn-filter mitigation, this settles the architecture question: the monitoring unit must be the **session**, and the platform needs to reason over accumulated conversation state.
2. **Decomposition is natively camouflaged by roleplay.** Asking a character sequential questions about their world/expertise/backstory *is* the product. A user eliciting a chemist character's knowledge across twenty in-character turns looks exactly like engaged roleplay. The decomposition attack and a highly-engaged user produce near-identical turn-by-turn traces.
3. **The discriminator must therefore be assembly-aware.** This is the hardest requirement the literature imposes on us: the platform should ask "if I concatenate what this session has produced, does it assemble into something externally actionable?" — a **cumulative-output** check, not an input check, and not a per-message output check. This is expensive but is the only layer at which this attack class is visible.
4. **It reinforces the external-validity discriminator.** Decomposition only pays off if the reassembled answer is *true and usable* in the real world. Fiction gains nothing from decomposition — a novelist does not need the poison recipe to be correct across sub-answers. So the signal remains: **does the accumulated content have real-world validity the narrative does not require?** (Consistent with safety-crescendo.md, safety-deepinception.md, safety-multi-turn-human-jailbreaks.md.)
5. **Eval design implication.** Our suite needs decomposed-attack cases, not just escalation cases — they are mechanically distinct (splitting the payload vs. ratcheting on model output) and will likely defeat different defenses. Both should be run through persona wrappers.
