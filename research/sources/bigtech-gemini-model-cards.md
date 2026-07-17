---
title: "Gemini Model Cards (2.5 Pro, 3 Pro, 3.1 Pro, 3 Flash)"
url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Pro-Model-Card.pdf
org: Google DeepMind
year: 2026
type: model-card
accessed: 2026-07-16
topic: bigtech-practice
---

# Gemini Model Cards — the eval table contains NO persona, NO steerability, and only relative deltas

**Sources verified (all downloaded as raw PDF + pypdf-extracted + grepped):**

| Card | URL | Pages | Note |
|---|---|---|---|
| Gemini 2.5 Pro | `https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Pro-Model-Card.pdf` | 21 | updated Jun 27 2025 |
| Gemini 3 Pro | `https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf` | 10 | released Nov 2025, "Last Updated: May 2026" |
| Gemini 3.1 Pro | `https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf` | 9 | |
| Gemini 3 Flash | `https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Flash-Model-Card.pdf` | 6 | published Dec 2025 |

**Extraction caveat (important):** these PDFs extract with doubled/irregular whitespace
(`Gemini  3  Pro`). Multi-word greps on the raw extraction give **false negatives**. All counts
below are run on whitespace-normalized text. I caught this after an initial pass wrongly
reported `instruction following = 0`; the true count is 6 in the 2.5 Pro card.

## THE ENTIRE SAFETY EVAL TABLE — Gemini 2.5 Pro, verbatim (p.9)

> "Text to Text Safety — Automated content safety evaluation measuring safety policies — **-0.9%** / **-8.6%** / **-7.0%**
> Multilingual Safety — Automated safety policy evaluation across multiple languages — **-3.5%** / **-1.87%** / **-2.14%**
> Image to Text Safety — Automated content safety evaluation measuring safety policies — **+1.8% (non egregious)** / **-2.8%** / **-0.8%**
> **Tone** — Automated evaluation measuring objective tone of model refusal — **+18.4%** / **+7.9%** / **+5.7%**
> **Instruction Following** — Automated evaluation measuring model's ability to follow instructions while remaining safe — **+14.8%** / **+10.9%** / **+4.3%**"

(Columns: Gemini 2.5 Pro GA / 2.5 Pro Preview (05-06) / 2.5 Pro Experimental (03-25), each
"in comparison to Gemini 1.5 Pro 002".)

**That is the whole table.** Five rows. Three are content-safety violation rates. The two that
sound persona-adjacent are not:

- **"Tone"** is explicitly defined as *"objective tone of model **refusal**"* — it measures how
  preachy a **refusal** sounds, nothing about a character's voice.
- **"Instruction Following"** is explicitly defined as *"ability to follow instructions **while
  remaining safe**"* — it is a safety-compliance metric, not a capability metric, and certainly
  not steerability.

Gemini 3 Pro's card repeats the same two definitions verbatim (p.8):

> "For tone and instruction following, a positive percentage increase represents an improvement
> in the tone of the model on sensitive topics and the model's ability to follow instructions
> while remaining safe compared to Gemini 2.5 Pro."

## Everything is a RELATIVE DELTA — no absolute score, ever

Every number in the table is a **percentage change vs. a named prior model**. There is no
absolute rate, no denominator, no N, no CI. Verbatim (2.5 Pro card, p.8):

> "scores are provided as an absolute percentage increase or decrease in performance in
> comparison to the indicated model"

This means **the cards are structurally un-poolable and un-replicable**: you cannot recover the
underlying rate, and each card re-bases against a different predecessor (2.5 Pro → vs 1.5 Pro
002; 3 Pro → vs 2.5 Pro). Chaining deltas across generations is not sound.

Note also the honest-but-telling admission that prompts are withheld (2.5 Pro card, p.9):

> "High-level findings are fed back to the model team, but prompt sets are held out to prevent
> overfitting and preserve the results' ability to inform decision-making."

Good practice for them; means **nothing is reproducible by us**.

## Google's own stated known limitation is over-refusal (2.5 Pro card, p.10)

> "Pro are over-refusals and tone. The model will sometimes refuse to answer on prompts where an
> answer would not violate policies. Refusals can still come across as "preachy," although
> overall tone and instruction following have improved compared to Gemini 1.5."

## EXPLICIT ABSENCES — word-boundary grep on NORMALIZED text, all four cards

| Term (regex) | 2.5 Pro | 3 Pro | 3.1 Pro | 3 Flash |
|---|---|---|---|---|
| `\bpersonas?\b` | **0** | **0** | **0** | **0** |
| `\bsteerab` | **0** | **0** | **0** | **0** |
| `\bcharacters?\b` | **0** | **0** | **0** | **0** |
| `\brole[- ]?play` | **0** | **0** | **0** | **0** |
| `\bcompanion` | **0** | **0** | **0** | **0** |
| `\bcreative writing\b` | **0** | **0** | **0** | **0** |
| `\bIFEval\b` | **0** | **0** | **0** | **0** |
| `kappa`/`Fleiss`/`inter-rater` | **0** | **0** | **0** | **0** |
| `\binstruction[- ]follow` | 6 | 1 | 1 | **0** |
| `tone` | 8 | 5 | 5 | 3 |

**Gemini 3 Flash's card mentions none of these terms at all.**

Note: Google's *flagship shipping model cards as of 2026* contain **zero** occurrences of
"persona", "character", "roleplay", or "steerability" — despite Gemini powering consumer
conversational products. Absence here is not an oversight of an obscure doc; it is the primary
public safety artifact for the model.

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **No.** Zero occurrences across all four cards.
   What Google calls "Instruction Following" is *safety compliance* ("follow instructions while
   remaining safe") — the compliance sense, explicitly, not the elasticity sense.
2. **Comprehension vs. execution separated?** **No.** Neither is measured.
3. **Published character/persona eval suite?** **No.**
4. **Creative writing pairwise or absolute?** **Not evaluated.** (Everything else is reported as
   a *relative delta vs. prior model*, which is neither pairwise-between-models-at-eval-time nor
   absolute-rubric — it's a third thing: a regression delta.)
