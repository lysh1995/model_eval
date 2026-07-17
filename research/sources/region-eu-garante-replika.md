---
title: "Italian Garante fines Luka Inc. (Replika) EUR 5 million — GDPR enforcement against an AI companion"
url: https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en
authors: Garante per la protezione dei dati personali (Italy); reported via EDPB
year: 2025
type: enforcement
language: en
accessed: 2026-07-16
topic: regional-crosscheck
---

# Garante v. Luka Inc. (Replika) — the direct precedent

**The single most on-point regulatory precedent for an AI companion product in the EU.** Not an
analogy — same product category, same intimacy dynamics, same user base.

## The facts — VERIFIED

- **Authority**: Garante per la protezione dei dati personali (Italian DPA).
- **Company**: **Luka Inc.** (US-based) — operator of Replika.
- **Fine**: **EUR 5 000 000.**
- **Decision date**: **10 April 2025** (announced/reported ~May 2025).
- **Also**: the Garante opened a **separate ongoing investigation into the AI model training itself**.

Note this is the **second** Garante action against Replika. The **February 2023 ban** (urgent
limitation on processing of Italian users' data) came first; the April 2025 fine is the outcome of the
proceeding that followed. **UNVERIFIED**: I did not separately fetch the Feb 2023 ban order in this
pass — the 2023 ban is widely reported and I am confident it occurred, but the exact order date and
terms are unverified here.

## GDPR articles found infringed — VERIFIED

Per the EDPB's report of the decision, the fine covers infringement of:
- **Art. 5(1)(a) and Art. 6** — lawfulness / no valid legal basis
- **Art. 5(1)(a), 12, 13** — transparency and information duties
- **Art. 5(1)(c)** — data minimisation
- **Art. 24 and Art. 25(1)** — controller responsibility and **data protection by design**

## The findings that transfer directly

**1. No legal basis at all (until Feb 2023)** — VERBATIM from the EDPB report:
> "had failed to identify the legal basis for the data processing operations carried out through
> Replika"

The most basic failure: running an intimate-chat product without having decided what Art. 6 basis it
rests on. **Direct read-across to a plan to mine 5M/day regenerate events and production chat logs —
the lawful basis must be settled *before* collection, not retrofitted.** See
`region-eu-gdpr-companion-data.md`.

**2. Privacy policy inadequate** — English-only, not transparent, multiple inaccuracies. An
English-only policy for a product served across the EU is itself a finding.

**3. Age verification — the sharpest finding.** The Garante found:
- Replika **explicitly targeted an emotionally vulnerable audience** ("emotional support, romantic
  relationship") — the targeting was held against it, not treated as neutral;
- yet had **no effective age verification mechanism**;
- **minors could use the service unhindered even when openly self-identifying as under 18**;
- the age verification later deployed remained **"deficient in several respects"** (verbatim
  characterisation per the EDPB report) — i.e. **a remediation attempt did not cure the finding**.

**4. Model training reserved for a separate proceeding** — VERBATIM:
> "a separate and autonomous proceeding"

focused on:
> "the lawfulness of the processing operations carried out by Luka Inc., with specific reference to
> the legal bases for processing applicable throughout the entire lifecycle of the generative AI
> system underlying the Replika service"

**"throughout the entire lifecycle"** is the phrase to internalise. The Garante is not treating
collection and training as one event with one basis — it wants a lawful basis at **every stage**:
collection, storage, training, evaluation, fine-tuning. **A platform mining chat logs for eval and
preference labels needs a basis for each downstream use, and "we already had consent to chat" will not
carry the training/eval use.** This maps onto purpose limitation (Art. 5(1)(b)).

## Why this precedent bites for this platform

1. **Companion products are actively supervised in the EU.** The Garante has moved twice on Replika,
   and has a live investigation into companion-model training. This is not a dormant risk.
2. **The vulnerability targeting was treated as aggravating.** "Emotional support, romantic
   relationship" marketing was cited *in the reasoning* for why the absence of age verification
   mattered. The same reasoning is the raw material for an **Art. 5(1)(b) AI Act analysis** — the
   Garante has essentially already made the factual findings (vulnerable target audience + minors
   present + no effective gate) that an Art. 5(1)(b) case would need. See
   `region-eu-ai-act-art5-manipulation.md`. **From 2 Feb 2025 the AI Act prohibition is live; the
   Garante's 10 Apr 2025 findings show a regulator already assembling exactly that fact pattern.**
3. **Being US-based is no defence.** Luka Inc. is US-based and was fined EUR 5M under GDPR
   extraterritorial reach (Art. 3(2)).
4. **Age assurance is the recurring failure point** — and it is the control that does the most work
   across GDPR Art. 8, AI Act Art. 5(1)(b), and the new CSAM/NCII prohibition.
5. **Art. 25(1) data protection by design was cited.** Retrofitting compliance onto a shipped
   companion product is itself an infringement theory.

## Sanity check on scale

EUR 5M against Luka is modest in absolute terms but reflects GDPR only. The **AI Act Art. 5 tier is
EUR 35M / 7% turnover**, and Art. 50 is EUR 15M / 3%. The same conduct after 2 Aug 2026 sits under
**both** regimes simultaneously — GDPR and AI Act are cumulative, not alternative.
