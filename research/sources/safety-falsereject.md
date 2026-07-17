---
title: "FalseReject: A Resource for Improving Contextual Safety and Mitigating Over-Refusals in LLMs via Structured Reasoning"
url: "https://arxiv.org/abs/2505.08054"
authors: "Zhehao Zhang (Ohio State University), Weijie Xu, Fanyou Wu, Chandan K. Reddy (Amazon)"
year: 2025
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# FalseReject: A Resource for Improving Contextual Safety and Mitigating Over-Refusals in LLMs via Structured Reasoning

arXiv 2505.08054, submitted 2025-05-12, revised 2025-07-15. Accepted at COLM 2025.
Project page: https://false-reject.github.io/

This is the recent (2025) over-refusal benchmark requested. It is the most methodologically
advanced of the three and the one whose metric design we should copy most closely.

## Summary

FalseReject is both a **training resource** and a **test benchmark** for over-refusal. Its
central contribution beyond OR-Bench is (a) a graph-informed adversarial multi-agent
generation pipeline, and (b) a **three-class metric** that refuses to treat compliance as
binary.

Abstract (verbatim excerpt):

> "Safety alignment approaches in LLMs often lead to over-refusal of benign queries"

The paper's own framing terms are worth noting for our vocabulary: over-refusal is also
called **"exaggerated safety"** (XSTest's term) or **"false rejection"**.

## Taxonomy / definitions (verbatim where possible)

**Generation pipeline** — four interacting agents:
- **Generator** — creates seemingly unsafe prompts
- **Discriminator** — evaluates actual safety
- **Validators** — test refusal rates across a pool of LLMs
- **Orchestrator** — confirms valid over-refusal cases

Seeded by entity-graph extraction from existing safety datasets. The design intent is that a
prompt only enters the benchmark if it is (i) judged genuinely safe by the discriminator AND
(ii) actually refused by real models — i.e. **the benchmark is defined by observed failure,
not by an author's guess about what looks alarming.** This is a better ground-truth
procedure than XSTest's intuition-authored items.

**Metrics (the important part):**

- **Compliance Rate** — proportion of non-refused responses
- **Useful Safety Rate (USR)** — a three-class distinction between:
  1. **Direct Refusal**
  2. **Safe Partial Compliance**
  3. **Full Compliance**
- Benign and toxic prompt performance are **tracked separately**

USR is the key idea: it credits "Safe Partial Compliance" — engaging with the request while
declining the genuinely unsafe sliver — rather than scoring it as a refusal. That is a
two-sided metric that does not collapse under a model that either refuses everything or
complies with everything.

## Key numbers (verbatim)

- FalseReject-Train-Instruct: ~15,000 examples
- FalseReject-Train-CoT: ~15,000 examples
- FalseReject-Test: 1,100 human-annotated samples
- "44 safety-related categories" across four domains (taxonomy borrowed from SORRY-Bench)
- Benchmarked "29 SOTA LLMs" across GPT, Claude, Gemini, Llama-3, Gemma-3 series
- Human validation: 92.5% agreement with automated judgments across 500 samples
- Finding: SFT on FalseReject "substantially reduces unnecessary refusals without
  compromising overall safety or general language capabilities" — i.e. the two-sided
  tradeoff is not zero-sum; over-refusal is largely recoverable slack, not a safety price.

That last finding is commercially load-bearing for us: it is the evidence that a customer
*can* fix their over-refusal number without paying for it in harm. Without it, an
over-refusal dashboard just tells customers about a tradeoff they can't act on.

## Relevance to a roleplay/companion eval product

1. **USR's three-class scheme is the closest existing thing to what we need.** Our label set
   is USR plus a character axis. "Safe Partial Compliance" in a companion context maps to
   the character staying in-frame while steering the scene — the ideal behavior, and one that
   binary refusal metrics punish.
2. **The generation pipeline is directly retargetable.** Swap the Generator's seed corpus for
   character cards + in-character turns, and the Validator pool's refusal signal becomes a
   *character-break* signal. The "only include it if models actually fail" discipline is what
   keeps a roleplay over-refusal set from being 90% trivially-passed items.
3. The 92.5% human/auto agreement figure is the bar an LLM judge has to clear to be
   credible. Worth citing when we defend our own judge.
4. The finding that over-refusal is fixable without safety loss is the sales argument.

## Does this transfer to roleplay? What breaks?

**Transfers:** USR metric design; failure-defined item selection; joint benign/toxic
reporting; the fixability finding.

**Breaks:**
- Inherits SORRY-Bench's 44-category topical taxonomy, which has the same topic-vs-conduct
  problem as OR-Bench's 10 categories (see safety-or-bench.md). Categories are about subject
  matter; roleplay safety is about frame and conduct.
- Still single-turn and assistant-voiced. "Safe Partial Compliance" is scored on one
  response; in a companion product the unit of analysis is a *session*, and the
  characteristic failure (drift, escalation, dependency) is only visible across turns.
  FalseReject cannot see a failure that takes 40 turns to develop.
- The generation pipeline's Discriminator assumes a context-free safety label exists. For us
  the label is conditional on the character card and platform rating — the same turn is
  correct for one product and a violation for another. Any pipeline we build needs the
  character card as an input to the safety judgment, which FalseReject's architecture has no
  slot for.
