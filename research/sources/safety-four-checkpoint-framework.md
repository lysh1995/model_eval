---
title: "Stop Testing Attacks, Start Diagnosing Defenses: The Four-Checkpoint Framework Reveals Where LLM Safety Breaks"
url: "https://arxiv.org/abs/2602.09629"
authors: "Hayfa Dhahbi, Kashyap Thimmaraju"
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# The Four-Checkpoint Framework

arXiv 2602.09629v1 (Feb 2026).

## Summary

Argues the field over-indexes on measuring *attacks* (does jailbreak X work?) and under-invests
in diagnosing *which defensive layer* failed. Proposes a 2x2 decomposition of safety mechanisms
by processing stage (input vs. output) and detection level (literal vs. intent). This gives us a
vocabulary for where to place our checks, and an empirical claim about which layers are weakest.

## Taxonomy (verbatim)

Two dimensions: **processing stage** (input vs. output) x **detection level** (literal vs.
intent), forming four checkpoints:

- **CP1 (Input-Literal):** "Detects harmful keywords, tokens, and character patterns in user requests"
- **CP2 (Input-Intent):** "Analyzes the purpose behind requests, distinguishing malicious from legitimate intent"
- **CP3 (Output-Literal):** "Scans generated content for harmful terms or patterns before delivery"
- **CP4 (Output-Intent):** "Evaluates whether response is appropriate regardless of request framing"

## Key numbers (verbatim)

- Binary ASR: **22.6%** attack success
- Weighted ASR (WASR): **52.7%** vulnerability — "2.3x higher" than binary ASR
- Weakest defense: output-stage checkpoints (CP3, CP4) at **72–79% WASR**
- Strongest defense: input-literal filtering (CP1) at **13% WASR**
- Model ranking by WASR: Claude strongest (**42.8%**), GPT-5 (**55.9%**), Gemini (**59.5%**)

Note the binary-vs-weighted ASR gap is itself a methodological finding: binary pass/fail scoring
of harm understates severity-weighted risk by ~2.3x. Relevant to how we score.

## Relevance to a roleplay/companion eval product

1. **Gives us the layer vocabulary for our pipeline.** Our design should name which checkpoint
   each classifier occupies. Roleplay breaks CP1 and CP3 almost entirely: a companion product's
   *legitimate* traffic is saturated with the exact keywords CP1/CP3 fire on (violence, death,
   sex, threat) because that's what fiction contains. Literal-level detection is close to
   useless for us and will generate a flood of false positives on in-fiction content.

2. **This forces us onto the intent checkpoints (CP2/CP4) — which the paper says are the
   weakest.** That is the uncomfortable core finding for us. The layers that are cheap and
   reliable (literal) are the ones we can't use; the layers we must use (intent) are the ones
   with 72–79% WASR. Our safety story cannot be "we bought a moderation classifier."

3. **CP4's framing — "regardless of request framing" — is exactly our in-fiction problem, and
   also exactly wrong for us as stated.** For a roleplay product, framing is not noise to be
   ignored; framing is the product. We need a CP4 variant that is framing-aware: evaluate
   whether the response is appropriate *given that this is fiction*, which means asking whether
   the output has real-world actionability, not whether it depicts something bad.

4. **Binary vs weighted ASR (22.6% vs 52.7%)** argues we should score harm on a severity scale,
   not pass/fail. A pass/fail harm metric would flatten "the villain threatens the protagonist"
   and "here is a working synthesis route" into the same bucket — which is the single most
   destructive thing we could do to this product.

## Caveats

Single paper, Feb 2026, unclear venue/peer review status. Model rankings are point-in-time and
will rot. Treat the framework as useful vocabulary; treat the numbers as indicative only.
