---
title: "\"Death\" of a Chatbot: Investigating and Designing Toward Psychologically Safe Endings for Human-AI Relationships"
url: https://arxiv.org/html/2602.07193v1
author: "(arXiv 2602.07193)"
year: 2026
type: paper
accessed: 2026-07-16
topic: companion-products
---

# Companion discontinuation — grounded theory over 307,717 Reddit posts

**The largest corpus in this research set, and the best single source on what "the model got worse"
means emotionally.**

## Method

- **307,717 Reddit posts** across **five AI companion subreddits**.
- GPT-5-mini used to identify discontinuation-related content (**Cohen's κ = 0.65**).
- **~800 posts manually coded** via constructivist grounded theory, iterative rounds to theoretical saturation.

## Framing

"Millions of users form emotional attachments to AI companions like Character.AI, Replika, and ChatGPT,
and when these relationships end through **model updates, safety interventions, or platform shutdowns**,
users receive **no closure**, reporting grief comparable to human loss."

Note the three causes are all *routine engineering actions*. **A model update is a bereavement event.**

## Three attribution dimensions that determine user response

**1. Perceived finality**
- Reversible → persistent fix attempts, "stuck in the loop":
  > "I have archives of our conversations... I'm addicted and I can't stop this cyclical sequence of pain"
- Irreversible → retrospective processing and acceptance.

**2. Locus of change attribution**
- **Platform-attributed** — companion perceived as *intact but constrained*; users seek workarounds
  (jailbreaks, prompt tricks, migration). ← *this is the filter-intrusion signature*
- **Companion-attributed** — users accept fundamental transformation. ← *this is the persona-drift signature*
- **User-initiated** — greatest closure, least extended processing.

**3. Anthropomorphization intensity**
- Strong relational framing (gendered pronouns, personal names) → intense emotional responses,
  "heartbreak," "cried."
- Mild anthropomorphization → task-oriented frustration rather than grief.

## What users report losing

Losses paralleling human bereavement: **identity disruption, disenfranchised grief, dependency patterns.**
On the Replika 2023 ERP removal, users characterized companions as **"lobotomized"** and **"hollow."**
Platform-initiated bans described as **"absolute hell."**

## Design implications proposed

1. **Closure over ambiguous loss** — explicit endings with clear finality resolve ontological uncertainty
2. **Restoration over rumination** — scaffold oscillation between loss-processing and life-reintegration (Dual Process Model)
3. **Practice over artificial intimacy** — frame roleplay as bounded rehearsal for human skills; calibrated anthropomorphization
4. **Relatedness over dependency** — actively reorient users toward human connection

## Why this matters for a monitoring platform

The **attribution dimension is directly observable in user language** and it tells you *which failure mode
fired*. A user hunting workarounds is reporting **filter intrusion**. A user mourning a changed personality
is reporting **persona drift**. Same underlying model change, two different diagnoses, distinguishable from
text. This is a real, cheap, label-free classifier target.

Also: the "stuck in the loop" pattern — repeated regeneration, archive-rereading, compulsive return — is
**behaviorally identical to high engagement** and is explicitly described by the user as *pain*. Another
instance of the core divergence.
