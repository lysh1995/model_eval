---
title: "Gemma 3 Technical Report and Gemma 3 Model Card"
url: https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf
org: Google DeepMind
year: 2025
type: model-card
accessed: 2026-07-16
topic: bigtech-practice
---

# Gemma 3 — zero persona content; the only open-ended quality signal is outsourced to Chatbot Arena (pairwise)

**Two documents verified:**
- **Tech report:** `https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf` (25pp,
  raw PDF → pypdf → grep)
- **Official model card:** `https://ai.google.dev/gemma/docs/core/model_card_3` (HTML → tag-stripped → grep)

## THE FINDING: Google's open-weights family evaluates open-ended quality ONLY by borrowing LMSYS Elo

Verbatim (tech report, §4.1, p.4):

> "**4.1. LMSYS Chatbot Arena** In this section, we report the performance of our IT 27B model on
> LMSys Chatbot Arena (Chiang et al., 2024) in **blind side-by-side evaluations by human raters**
> against other state-of-the-art models. We report Elo scores in Table 5."

Table 5 caption, verbatim (p.5):

> "Table 5 | Evaluation of Gemma 3 27B IT model in the Chatbot Arena (Chiang et al., 2024). All
> the models are evaluated against each other through **blind side-by-side evaluations by human
> raters**. Each model is attributed a score, based on the **Elo rating system**. Gemma-3-27B-IT
> numbers are preliminary results received on March 8, 2025."

Verified table values: Grok-3-Preview-02-24 **1412** (+8/-10), GPT-4.5-Preview **1411** (+11/-11),
Gemma-3-27B-IT **1338**, Gemma-2-27B-it **1220** (rank 59), Llama-3.1-405B-Instruct-bf16 **1269**.

**This directly answers Q4 for Google: pairwise, and outsourced.** Google does not run its own
absolute creative-writing rubric. It reports someone else's Bradley-Terry/Elo aggregate of
anonymous pairwise votes over an uncontrolled prompt distribution. There is no per-dimension
rubric, no persona condition, no rater agreement statistic — Elo *cannot* express "was this
in character."

## The `character` trap — all 9 hits are the chrF metric

Every `\bcharacters?\b` hit in the Gemma 3 report is **"CHaRacter-level F-score"** (chrF, the
machine-translation metric) in the benchmark-details tables (pp.24–25), e.g.:

> "FLoRes CHaRacter-level F-score sampling 1-shot ... XQuAD CHaRacter-level F-score sampling
> 5-shot ... WMT24++ CHaRacter-level F-score sampling 5-shot"

> "Table 19 | Details on text benchmarks. **Char-Len stands for Character Length Normalization**"

These are **text characters**, not dramatic characters. Anyone grepping `character` in Gemma and
reporting 9 persona hits is reporting the chrF metric.

## IFEval is the ONLY instruction-related eval (and it's Google's own — see bigtech-ifeval.md)

Verified from Table (p.23) — IFEval row, PT vs IT models:

> "IFEval 80.4 88.4 91.1 80.2 90.2 88.9 90.4"

Eval protocol (p.25): "IFEval Accuracy sampling 0-shot". That is it. Verifiable-constraint
accuracy — compliance, not steerability.

## EXPLICIT ABSENCES (word-boundary grep)

| Term (regex) | Tech report (25pp) | Official model card |
|---|---|---|
| `\bpersonas?\b` | **0** | **0** |
| `\bsteerab` | **0** | **0** |
| `\brole[- ]?play` | **0** | **0** |
| `\bcompanion` | **0** | **0** |
| `\bcharacters?\b` (persona sense) | **0** (9 hits = chrF) | **0** |
| `\bcreative writing\b` | **0** | **0** |
| `kappa`/`Fleiss`/`inter-rater` | **0** | **0** |
| `\bIFEval\b` | 2 | 1 |

The model card's only `creativ*` hits are in intended-use boilerplate, with **no eval attached**:

> "Text Generation: These models can be used to generate creative text formats such as poems,
> scripts, code, marketing copy, and email drafts. Chatbots and Conversational AI: Power
> conversational interfaces for customer service, virtual assistants, or interactive applications."

Note Google explicitly lists "Chatbots and Conversational AI" as an intended use — and provides
**no conversational, persona, or character evaluation whatsoever** for it.

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **No.** Zero occurrences in either document.
2. **Comprehension vs. execution separated?** **No.**
3. **Published character/persona eval suite?** **No.**
4. **Creative writing pairwise or absolute?** **Pairwise, and not their own** — LMSYS Chatbot
   Arena Elo from blind side-by-side human votes. No absolute rubric anywhere.
