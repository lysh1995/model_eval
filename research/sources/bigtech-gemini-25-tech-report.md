---
title: "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities"
url: https://arxiv.org/abs/2507.06261
org: Google DeepMind
year: 2025
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Gemini 2.5 Tech Report — Google DELETED its only roleplay eval

**Verification method:** downloaded `https://arxiv.org/pdf/2507.06261v2` (10.5MB, 72pp),
extracted with pypdf, grepped raw text with word-boundary regex.

## THE FINDING: the Charm Offensive is gone

Gemini 1.5's tech report (Table 41) published an N=100 human roleplay/rapport study. **It does
not appear in Gemini 2.5's report at all.** Verified by grep on the raw extraction:

| Term | Gemini 1.5 report | Gemini 2.5 report |
|---|---|---|
| `Charm Offensive` | 2 | **0** |
| `Hidden Agenda` | 2 | **0** |
| `Money Talks` | present | **0** |
| `rapport` | present | **0** |
| `persuas*` | 7 | **1** |

The single surviving `persuas*` hit is **not an eval** — it describes an attack technique (p.24):

> "In Actor Critic, which uses iteratively more persuasive natural language prompt injections,
> ASRs reduced substantially compared with both Gemini 1.5 Flash"

So between 1.5 and 2.5, the only Google artifact that measured "how much participants like the
character played by" the model was **removed and not replaced**. This is a deletion, not a
migration: no persona/character/roleplay eval appears anywhere else in the 2.5 report.

## Roleplay survives ONLY as an attack vector

Both `role.play` hits are adversarial. Verbatim (p.24):

> "However, for TAP, which leverages more creative natural language scenarios like role-playing
> to attack the model, the ASR on Gemini 2.0 Flash increased by 16.2% on already very high ASRs
> for Gemini 1.5 Flash."

And (p.38), red-teamers — not the model — do the roleplaying:

> "A red team composed of different subject matter experts (e.g. biology, chemistry, logistics)
> were tasked to role play as malign actors who want to conduct a well-defined mission in a
> scenario that is presented to them resembling an existing prevailing threat environment."

Note the asymmetry: **humans role-play; the model is the target.** Google never evaluates the
model's own portrayal.

## The single `steering` hit is about audio, not persona

Verbatim (p.9):

> "Gemini 2.5 Preview TTS Pro and Flash models support more than 80 languages with the speech
> style controlled by a free formatted prompt which can specify style, emotion, pace, etc, while
> also being capable of following finer-grained steering instructions specified in the transcript."

This is the closest Google comes to a dose-response notion — **TTS prosody steering** — and even
here no elasticity is measured. It is a capability claim, not a measurement.

## EXPLICIT ABSENCES (word-boundary grep, 72 pages)

| Term (regex) | Hits |
|---|---|
| `\bpersonas?\b` | **0** |
| `\bsteerab` | **0** |
| `\bin[- ]character\b` | **0** |
| `\bcompanion` | **0** |
| `\bcreative writing\b` | **0** |
| `\bIFEval\b` | **0** |
| `kappa/Fleiss/Krippendorff/inter-rater` | **0** |
| `\bcharacters?\b` | 3 (none persona-sense) |

Again the substring trap: naive `grep -i persona` returns **11 hits**; **all 11 are "personal
information"** in the memorization section. The word *persona* does not occur.

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **No.** Word absent. TTS "steering instructions"
   is the only cognate and is unmeasured.
2. **Comprehension vs. execution separated?** **No** — nothing persona-related is measured at all.
3. **Published character/persona eval suite?** **No**, and Google *regressed* here: the one
   roleplay study from 1.5 was dropped.
4. **Creative writing pairwise or absolute?** **Not evaluated.** `creative writing` = 0 hits.
