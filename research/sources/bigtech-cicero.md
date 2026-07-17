---
title: "Human-level play in the game of Diplomacy by combining language models with strategic reasoning (CICERO)"
url: https://www.science.org/doi/10.1126/science.ade9097
org: Meta
year: 2022
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# CICERO — NO persona eval, but the best DOSE-RESPONSE architecture anyone at Meta ever shipped

**Verification:** the Science version is paywalled; I used the authors' public technical report PDF
at `https://noambrown.github.io/papers/22-Science-Diplomacy-TR.pdf` (3.3MB, 91pp), pypdf →
Python regex (NOT grep — this file contains NUL bytes; see method note). All counts Python-verified.

(Complements the existing `research/sources/game-cicero-diplomacy.md`. **This file answers only:
does CICERO contain persona eval content?** Answer: **no** — but its *architecture* is the closest
thing in either org's corpus to the elasticity/dose-response construct we need, so it is worth
having under bigtech-practice.)

## VERDICT ON THE ASSIGNED QUESTION: no persona eval content

Python-verified counts across 91 pages:

| Term (regex) | Hits |
|---|---|
| `\bpersonas?\b` | **0** |
| `\brole[- ]?play` | **0** |
| `\bsteerab` | **0** |
| `\bin[- ]character\b` | **0** |
| `\bcompanion` | **0** |
| `\bcreative writing\b` | **0** |
| `\bcharacters?\b` | 4 (none persona-sense) |
| `kappa`/`Fleiss`/`Krippendorff`/`inter-rater` | **0** |
| `intent` | **197** |

CICERO plays *seven powers* in Diplomacy (England, France, etc.) — arguably seven "characters" —
and **never once frames them as personas, never evaluates voice, and never measures in-character
consistency**. The agent is evaluated on **game score and human-likeness of play**, not portrayal.

## WHY IT STILL MATTERS: intent-controlled dialogue IS a dose-response mechanism

The one architectural idea here that our framework should steal (verbatim, p.2):

> "**Intent-controlled dialogue** Cicero generates messages through a neural generative Diplomacy
> dialogue model that was **trained to be controllable through a set of intents**."

The training/inference structure (verbatim, p.62):

> "• **Intent-controlled dialogue model** … Responsible for all dialogue generation in CICERO.
> Trained to imitate messages in human diplomacy games given the board state and history, the
> dialogue history, and **the intent for the target message**. At test time, **the intent was
> supplied from strategic planning** instead."

> "• **Intent annotation model** … Used to annotate the human dataset messages with intents, for
> training the intent-controlled dialogue model and imitation intent model. **Not used in CICERO at
> test time.**"

And (p.3), Fig. 2 caption:

> "Illustration of the training and inference process for intent-controlled dialogue. Actions are
> specified as strings of orders for units… (A) An "**intent model**" was trained to predict actions
> for a pair of players on the basis of their dialogue. Training data was restricted to a subset in
> which dialogue is d[ense]…"

**This is the structure our steerability construct needs, and Meta built it in 2022:**

1. There is an **explicit, machine-readable control variable** (the intent = a set of orders).
2. The control variable is **supplied at inference from outside the dialogue model** (from the
   strategic planner), so it can be **varied independently of the conversation**.
3. There is an **inverse model** (the intent annotation model) that reads a message and recovers
   the intent — i.e. a **decoder from output back to the control variable**.

(3) is the key. An annotation model that maps *message → intent* is exactly the instrument needed
to ask **"did the persona prompt actually land?"** Set intent to X, generate, run the annotator,
check you recover X. Vary the strength of X, and you have a **dose-response curve**. Meta had the
full apparatus — control variable, independent manipulation, and an inverse decoder — and pointed
it at **board moves** rather than **character**.

CICERO is therefore the strongest existence proof in the big-tech corpus that a
comprehension/execution split is *buildable*: the intent annotation model measures whether the
generated text *carries* the intended content (execution), separately from whether the planner
chose a good intent (comprehension/decision). **Nobody at Meta ever ran this play for persona.**

## What CICERO evaluates instead

Persuasion-adjacent framing dominates (`persuasion` = 14 hits), consistent with the rest of the
corpus: dialogue quality is instrumentally valued for *winning*, and the published metrics are game
score, ranking among human players, and human-likeness — not portrayal fidelity. There is no rubric
scoring whether CICERO "sounds like France."

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **The mechanism, yes; the measurement, no.** Intent
   is a genuine, independently-manipulable control variable with an inverse decoder — the only such
   apparatus in either org's corpus. But CICERO never reports an intent-fidelity *curve* (no
   "how often does the message actually convey the intent, as a function of X"). The word
   `steerab*` appears **0** times.
2. **Comprehension vs. execution separated?** **Architecturally yes, evaluatively no.** The planner
   (decides intent) and the dialogue model (renders intent) are separate modules, and the annotation
   model could score the rendering — but no such separation is reported as a metric.
3. **Published character/persona eval suite?** **No.**
4. **Creative writing pairwise or absolute?** **Neither** — game-outcome and human-likeness metrics.

## METHOD NOTE

`grep` returns **0 for every term** on this document's extraction because it contains NUL bytes and
macOS grep silently treats the file as binary. `grep -oi "intent"` → **0**; Python `re.findall` →
**197**. Every count above is Python-verified with NULs stripped. Do not trust a grep-derived zero
on this file.
