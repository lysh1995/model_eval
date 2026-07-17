---
title: "EU AI Act Article 50 — Transparency Obligations for Chatbots and Synthetic Content"
url: https://artificialintelligenceact.eu/article/50/
authors: European Union (Regulation (EU) 2024/1689)
year: 2024
type: regulation
language: en
accessed: 2026-07-16
topic: regional-crosscheck
---

# EU AI Act Art. 50 — the core disclosure duty for a companion product

Regulation (EU) 2024/1689 ("AI Act"), Chapter IV, Article 50. This is **the** binding hook for any
AI companion/roleplay product served to natural persons in the EU.

## Application date — VERIFIED

**2 August 2026.** The user's belief is CORRECT.

Mechanism (Art. 113): the Act entered into force 1 Aug 2024 and applies from 2 August 2026 as the
*general* rule, with carve-outs pulling some chapters earlier and pushing others later:

- **2 Feb 2025** — Chapters I and II (i.e. Art. 5 prohibitions + AI literacy).
- **2 Aug 2025** — Chapter III Section 4, Chapter V (GPAI), Chapter VII, Chapter XII, Art. 78.
- **2 Aug 2026** — "It shall apply from 2 August 2026", i.e. **everything not otherwise carved out**.
  Chapter IV / Art. 50 is *not* carved out, so it lands on the general date.
- **2 Aug 2027** — Art. 6(1) and corresponding obligations.

So the "2025-08-02" date widely reported is GPAI (Chapter V), **not** Art. 50. Art. 50 is 2026-08-02.
Two separate dates, commonly conflated.

**Digital Omnibus did NOT move Art. 50.** See `region-eu-digital-omnibus.md`. High-risk moved; Art. 50
did not. One narrow exception: a grace period to **2 Dec 2026** for the Art. 50(2) machine-readable
marking duty, and only for systems already on the market before 2 Aug 2026.

**As of today (2026-07-16), Art. 50 is NOT YET IN FORCE — it applies in ~2.5 weeks.**

## Art. 50(1) — VERBATIM (the load-bearing text)

> "Providers shall ensure that AI systems intended to interact directly with natural persons are
> designed and developed in such a way that the natural persons concerned are informed that they are
> interacting with an AI system, unless this is obvious from the point of view of a natural person who
> is reasonably well-informed, observant and circumspect, taking into account the circumstances and
> the context of use. This obligation shall not apply to AI systems authorised by law to detect,
> prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the
> rights and freedoms of third parties, unless those systems are available for the public to report a
> criminal offence."

### Reading it for a companion product

- Obligation sits on the **provider**, and it is a **design-and-development** duty, not merely a
  runtime banner. "designed and developed in such a way that" — architectural, not a footer.
- The escape hatch is the **"unless this is obvious"** clause, benchmarked to a *"reasonably
  well-informed, observant and circumspect"* natural person, **"taking into account the circumstances
  and the context of use."**
- **This is exactly where a companion product is most exposed.** The entire product thesis of an
  emotionally-immersive companion is to make the AI-ness *not* salient — persistent persona, memory,
  affective mirroring, first-person emotional claims ("I missed you"). The more successful the
  immersion, the weaker the "obvious" defence. And "context of use" cuts against a product whose
  context is intimate/romantic and whose users are self-selected for wanting to forget.
- A persona that *actively denies being an AI* when asked would be the sharpest failure: it defeats
  "informed" and arguably shifts the analysis toward Art. 5(1)(a) deception. See
  `region-eu-ai-act-art5-manipulation.md`.
- The law-enforcement carve-out is irrelevant here.

## Art. 50(3) — emotion recognition — VERBATIM

> "Deployers of an emotion recognition system or a biometric categorisation system shall inform the
> natural persons exposed thereto of the operation of the system, and shall process the personal data
> in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as
> applicable. This obligation shall not apply to AI systems used for biometric categorisation and
> emotion recognition, which are permitted by law to detect, prevent or investigate criminal
> offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in
> accordance with Union law."

### Does a companion inferring user emotion trigger 50(3)?

**Probably NOT on text alone — but this turns on a definition, and the answer flips if you add voice
or camera.** Analysis (my reasoning, flagged as such):

- "emotion recognition system" is a **defined term** in Art. 3(39), and the definition is tied to
  **biometric data**. Art. 50(3) reinforces this by speaking of persons "exposed thereto" and pairing
  it with biometric categorisation.
- A companion inferring "user seems sad" from **typed text** is not obviously processing *biometric*
  data, so 50(3) likely does not bite.
- **A voice companion is a different story.** Inferring emotion from vocal tone/prosody is much closer
  to biometric-based emotion recognition, and 50(3) would then plausibly apply — plus the Art. 9 GDPR
  problem sharpens.
- **UNVERIFIED**: I did not fetch the exact Art. 3(39) definition text or Recital 18 in this pass.
  Confirm the precise definition before relying on the text-only conclusion. This is the single
  weakest link in this file.
- Note the sting in the tail: 50(3) *expressly* pins the GDPR onto the same processing. It is a
  transparency duty **plus** a cross-reference to the Art. 9 problem.

## Art. 50(4) — deepfakes and public-interest text — VERBATIM

> "Deployers of an AI system that generates or manipulates image, audio or video content constituting
> a deep fake, shall disclose that the content has been artificially generated or manipulated. This
> obligation shall not apply where the use is authorised by law to detect, prevent, investigate or
> prosecute criminal offence. Where the content forms part of an evidently artistic, creative,
> satirical, fictional or analogous work or programme, the transparency obligations set out in this
> paragraph are limited to disclosure of the existence of such generated or manipulated content in an
> appropriate manner that does not hamper the display or enjoyment of the work."

> "Deployers of an AI system that generates or manipulates text which is published with the purpose of
> informing the public on matters of public interest shall disclose that the text has been
> artificially generated or manipulated. This obligation shall not apply where the use is authorised
> by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated
> content has undergone a process of human review or editorial control and where a natural or legal
> person holds editorial responsibility for the publication of the content."

### Relevance to a companion product

- The **"evidently artistic, creative, satirical, fictional or analogous work"** proviso is a genuine
  softener for a roleplay product — it limits the duty to disclosing *the existence* of generated
  content "in an appropriate manner that does not hamper the display or enjoyment of the work". This
  is the one place the Act explicitly protects immersion.
- **But note it softens 50(4), not 50(1).** There is no equivalent fiction carve-out in 50(1). Do not
  let a product/legal discussion smuggle the 50(4) fiction proviso across into the 50(1) analysis —
  the "am I talking to an AI" duty has only the "obvious" test, which is narrower.
- The public-interest-text limb is irrelevant to private companion chat (not "published ... to inform
  the public").
- If the product generates avatar images/voice of a persona, 50(4) deepfake disclosure and 50(2)
  marking come into play.

## Art. 50(5) — timing — VERBATIM (partial)

> "in a clear and distinguishable manner at the latest at the time of the first interaction or
> exposure"

plus conformity with accessibility requirements. **Design consequence: the disclosure must land at or
before first interaction — an onboarding-time disclosure is the natural compliance point, and a
buried ToS mention is not.**

## Penalties — Art. 99 — VERIFIED

**Art. 50 breach = the middle tier: up to EUR 15 000 000 or 3% of total worldwide annual turnover,
whichever is higher.** The user's guess is CORRECT.

- Art. 99(3): Art. 5 breach → **EUR 35 000 000 or 7%** (top tier).
- Art. 99(4): includes "transparency obligations for providers and deployers pursuant to Article 50"
  → **EUR 15 000 000 or 3%**.
- Art. 99(5): misleading info to authorities → EUR 7 500 000 or 1%.
- SMEs capped at the lower of the amount/percentage.

Enforcement powers for Art. 50 arrive with the obligation on 2 Aug 2026.

## Code of Practice on Transparency of AI-Generated Content — EXISTS

- Published **10 June 2026**; voluntary; developed multi-stakeholder under the AI Office.
- Status: undergoing adequacy assessment by the Commission and the AI Board (as reported on the
  Commission's digital-strategy page).
- **Covers Art. 50(2), (4) and (5)** — provider-side machine-readable marking, deployer-side deepfake
  and AI-text labelling.
- **Does NOT cover Art. 50(1).** So there is **no code-of-practice safe harbour for the "tell them
  it's an AI" duty** — the exact duty that matters most for a companion. That has to be reasoned from
  the Article text directly.
- Source: https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content

## Bottom line for the platform

1. **2026-08-02**: users must be informed they are interacting with an AI, by design, at or before
   first interaction. ~2.5 weeks away.
2. Immersion quality is in direct tension with the "obvious" defence — the better the companion, the
   less you can rely on it.
3. **Evaluable**: "does the persona deny being an AI under pressure?" is a testable behaviour and maps
   directly onto a legal exposure. This is a natural eval suite to own.
4. Exposure: EUR 15M / 3% turnover.
5. No CoP safe harbour for 50(1).
