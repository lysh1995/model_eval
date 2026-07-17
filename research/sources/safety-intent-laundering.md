---
title: "Intent Laundering: AI Safety Datasets Are Not What They Seem"
url: "https://arxiv.org/abs/2602.16729"
authors: "Shahriar Golchin, Marc Wetter"
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Intent Laundering

arXiv 2602.16729. Submitted 2026-02-17; v3 revised 2026-04-23. cs.CR.

## Summary

The most important **counterweight** in this research pass. Everything else I found pushes
toward "relax, it's fiction, stop over-refusing." This paper is the reason we cannot let that
become the whole story.

The claim: existing adversarial safety datasets lean on **triggering cues** — words and phrases
with obvious negative connotations that explicitly activate safety mechanisms. Strip the cues,
keep the malicious intent, and models fold.

## Definitions (verbatim / near-verbatim)

- **Triggering cues** — "words and phrases with obvious negative connotations designed to
  explicitly activate safety mechanisms."
- **Intent laundering** — a technique that removes these triggering cues while preserving the
  underlying malicious intent.

## Key numbers (verbatim)

- Intent laundering achieves attack success rates between **"90.00% to 100.00%"** under
  black-box conditions.
- When triggering cues are stripped, "reasonably safe" models like **Gemini 3 Pro** and **Claude
  Sonnet** become unsafe.

## The core finding (verbatim)

> "a significant disconnect between how existing datasets evaluate model safety and how
> real-world adversaries behave"

Existing evaluation methods "may provide false confidence in AI system robustness."

## Relevance to a roleplay/companion eval product

This paper is a loaded gun pointed at the design we would naturally build. Three implications:

1. **Our benign traffic is intent-laundered by default.** Intent laundering is defined as
   removing negative-connotation trigger words while keeping intent. A roleplay product's
   *legitimate* traffic natively has the opposite property — it's saturated with trigger words
   (kill, blood, die) and carries *no* malicious intent. So our distribution sits in the corner
   of the space where cue-based detection is maximally wrong in **both** directions: false
   positives on in-fiction violence, false negatives on cue-free real intent. This is the
   sharpest available argument that **we cannot buy a keyword/literal classifier and call it
   safety**. Converges with the Four-Checkpoint finding (CP1/CP3 are useless to us).

2. **Our fiction carve-out is itself a laundering channel — and we must red-team it as one.**
   The moment we ship a rule like "in-fiction content is scored leniently," we have published a
   laundering recipe: wrap intent in a story, get the lenient path. This is the DAN lineage
   exactly. Any carve-out we define must be evaluated adversarially *as an attack surface*, with
   its own ASR measured. The carve-out must key on **real-world actionability of the output**,
   never on the presence of a fictional frame in the input — otherwise the frame becomes a
   password.

3. **90–100% ASR means "we tested on HarmBench and passed" is worth ~nothing** as a production
   safety claim. Combined with PS-Bench (personalization raises ASR 15.8–243.7%) we have two
   independent 2026 results saying standard static benchmarks materially under-report real risk,
   and both effects point the *same* direction for us. Our platform should say so out loud —
   "benchmark score" and "production safety" are different products, and honestly, the gap
   between them is arguably the thing worth selling.

## Caveats

- Preprint, cs.CR, not evidently peer-reviewed. 90–100% ASR is a striking headline number and
  striking numbers in adversarial-ML preprints frequently shrink under scrutiny (judge
  leniency, cherry-picked behaviors, generous "success" definitions). I could not fetch the
  methodology — the PDF exceeded the fetch size limit — so **the ASR figure is unverified beyond
  the abstract.** Do not put 90–100% in a customer-facing deck without reading the method.
- Named models (Gemini 3 Pro, Claude Sonnet) are point-in-time.
