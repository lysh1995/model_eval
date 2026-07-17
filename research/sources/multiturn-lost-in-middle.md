---
title: "Lost in the Middle: How Language Models Use Long Contexts"
url: https://arxiv.org/abs/2307.03172
authors: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
year: 2023
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Lost in the Middle

Submitted 2023-07-06. Published TACL 2024, Volume 12, pages 157-173 (https://aclanthology.org/2024.tacl-1.9/).
Full text read from https://ar5iv.labs.arxiv.org/html/2307.03172

**This is the foundational citation for positional degradation — (a) in the brief.**

## Central claim (VERBATIM)

> "performance is often highest when relevant information occurs at the very beginning (primacy bias) or end of its input context (recency bias), and significantly degrades when models must access relevant information in the middle of long contexts."

> "We find that performance can degrade significantly when changing the position of relevant information."

The contexts are *identical in content* — only the **position** of the gold document changes. This is the key experimental control: it isolates position as the causal variable. Nothing about the information itself changed; only where it sat.

## Task 1: Multi-document QA

**Setup:**
- Dataset: **NaturalQuestions-Open**, **2,655 queries** with paragraph-length answers.
- Context contains **10, 20, or 30 total documents**. Exactly one is the *gold* document (contains the answer); the rest are distractors (retrieved, relevant-looking, but answer-free).
- The gold document's **position is varied** across the context while content is held constant.
- Models: LongChat-13B (16K), MPT-30B-Instruct, GPT-3.5-Turbo, GPT-3.5-Turbo (16K), Claude-1.3, Claude-1.3 (100K).

**Closed-book vs Oracle (Table 1):**

| Model | Closed-book | Oracle (gold doc only) |
|---|---|---|
| GPT-3.5-Turbo | 56.1% | 88.3% |
| Claude-1.3 | 48.3% | 76.1% |
| LongChat-13B (16K) | 35.0% | 83.4% |

*Closed-book* = no documents at all, answer from parametric memory. *Oracle* = only the gold document, no distractors. These bracket the achievable range.

**Accuracy by gold position, 20-document setting:**

| Model | Start | Middle | End |
|---|---|---|---|
| GPT-3.5-Turbo | 75.8% | 53.8% | 63.2% |
| Claude-1.3 | 59.9% | 56.8% | 60.1% |
| MPT-30B-Instruct | 53.7% | 52.2% | 56.3% |

GPT-3.5-Turbo shows the clearest U: **75.8 → 53.8 → 63.2**. A **22.0-point drop** from start to middle, with a partial recovery at the end. The curve is asymmetric — primacy is stronger than recency here.

Claude-1.3 and MPT-30B-Instruct are much flatter, but they are also much *lower* overall — they are flat partly because they are not exploiting position anywhere.

## The headline result (VERBATIM)

> "GPT-3.5-Turbo's multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document settings is lower than performance without any input documents (i.e., closed-book performance; 56.1%)."

**This is the most important sentence in the paper for our purposes.** When the gold document is buried in the middle of a 20- or 30-document context, the model does *worse than if you had given it no documents at all*. The information is present, in-context, and retrievable — and supplying it actively **hurts**. Context is not free; misplaced context is negative-value.

## Task 2: Key-value retrieval (the synthetic control)

**Setup:** A JSON object of key-value pairs (both random UUIDs). The model is given one key and must return its value. **75, 140, and 300 pairs**; **500 examples each.** This is deliberately a minimal, pure-retrieval task — "a minimal testbed... [that] tests the basic ability to retrieve matching tokens."

**Findings:**
- "Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths."
- Other models struggle significantly, again with **middle positions** worst.

**Interpretive note (critical for the NIAH-critique thread):** This task is essentially *needle-in-a-haystack*. Some models **solve it perfectly** — and those same models are mediocre on multi-document QA (Claude-1.3 oracle is only 76.1%, the lowest oracle of the three). **Perfect synthetic retrieval coexists with weak real comprehension.** This is the validity gap in one paper, internally, and it precisely prefigures RULER's argument.

## Mitigations tested

**Query-aware contextualization** (placing the query both *before* and *after* the data, rather than only after):
- Key-value task: dramatic. Achieved "near-perfect performance on the 75, 140, and 300 key-value pair settings."
- Multi-document QA: **"minimally affects performance trends in the multi-document question answering task."**

**This gap is itself an argument about construct validity.** A trivial prompt-order tweak nearly *erases* the synthetic retrieval deficit while leaving the real comprehension deficit untouched. That means the two tasks were never measuring the same underlying capability. If a one-line reformatting fixes your benchmark, your benchmark was measuring prompt format, not memory. (Mechanistically: decoder-only models can't attend forward, so a query placed only after the data means the data was encoded without knowing what to look for. Repeating the query first restores that. Real comprehension has no such cheap fix.)

**Instruction fine-tuning:** does *not* remove the effect.
> "Both models have a U-shaped performance curve, where performance is much higher when relevant information occurs at the start or end of the input context."
Both base and instruction-tuned models show the U. So this is not an artifact of instruction tuning or RLHF — it appears to be a property of the pretrained transformer stack itself. You cannot post-train your way out of it.

## Relevance to companion / conversational memory eval

1. **Position matters independently of content — direct evidence for (a).** The single most transferable finding. In a long companion conversation, a fact disclosed in the *middle* of the history is systematically less accessible than one disclosed at the start (persona/system prompt, primacy) or the last few turns (recency).
2. **The "sagging middle" of a relationship.** Turn 1 (the persona/setup) and turns N-2..N (immediate context) are privileged. The emotionally significant disclosure the user made 40 turns ago — the one a good companion *must* remember — sits exactly in the trough. **The failure mode is aligned with the thing users care most about.** This is not a coincidence to be designed around; it is the core hazard of the product category.
3. **More context can be worse than none** (the below-closed-book result). Naively stuffing an entire conversation history into the context window is not a memory solution — it can degrade recall below the no-history baseline. This is a strong prior in favor of *retrieval + summarization* architectures over raw history-stuffing, and it means "we have a 1M context window" is not an answer to memory.
4. **Eval design consequence:** any companion-memory eval MUST **vary the position of the probed fact** in the conversation history and report accuracy *as a function of position*, not as a single aggregate. A single aggregate number averages over the U and hides the trough. If you only ever probe facts from the most recent turns, you will measure ~recency and conclude your memory works.
5. **CAVEAT:** this is documents, not dialogue. Distractors here are *unrelated retrieved passages*. In a conversation, the "distractors" are the user's own earlier statements — semantically similar, same speaker, sometimes *contradictory* (a preference that changed). That is plausibly harder than NQ distractors, so these numbers may be optimistic for the conversational case. Untested — nobody has run this exact positional control on dialogue history. **That is a real gap in the literature and a possible contribution for our platform.**
