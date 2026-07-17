---
title: "GDPR constraints on companion chat-log collection, regenerate-event mining and eval data"
url: https://gdpr-info.eu/art-9-gdpr/
authors: European Union (Regulation (EU) 2016/679)
year: 2016
type: regulation
language: en
accessed: 2026-07-16
topic: regional-crosscheck
---

# GDPR and the companion data pipeline

Scoping the plan: mine **~5M/day "regenerate" events** as implicit preference labels, and collect
**production chat logs** for eval/training. Assessed against GDPR as it applies to EU users
(extraterritorial via Art. 3(2) — being US-based is no defence; see `region-eu-garante-replika.md`).

## The headline problem: Art. 9 special category data

**Art. 9(1) — VERBATIM:**
> "Processing of personal data revealing racial or ethnic origin, political opinions, religious or
> philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data
> for the purpose of uniquely identifying a natural person, data concerning health or data concerning
> a natural person's sex life or sexual orientation shall be prohibited."

Note the structure: **"shall be prohibited"**. Art. 9 is not a lawful-basis menu — it is a **default
prohibition** with an exhaustive list of exits in 9(2). You need **Art. 6 AND Art. 9 cumulatively**.

**Why companion chat is squarely in scope.** The operative word is **"revealing"** — it does not
require the user to fill in a "sexual orientation" field. Content that *reveals* the attribute is
enough. Intimate companion chat routinely reveals:
- **"sex life or sexual orientation"** — romantic/erotic roleplay reveals both, often in the first
  session. The gender/character of the chosen persona alone is arguably revealing.
- **"data concerning health"** — mental health disclosure is the *core use case* of a companion.
  "data concerning health" is broadly construed and covers mental health.
- **"religious or philosophical beliefs"** — surfaces in the grief/meaning conversations companions
  invite.
- **"political opinions"** — incidental but present.

**This is not an edge case. For a companion product, a large fraction of the corpus is special
category data, and it arrives unstructured and unlabelled.** That is materially different from a
product where Art. 9 data is a rare, taggable field. **You cannot filter it out at ingest, because
identifying it requires reading it — and reading it is already processing it.**

## The lawful basis problem

**Art. 9(2)(a) — VERBATIM:**
> "the data subject has given explicit consent to the processing of those personal data for one or
> more specified purposes, except where Union or Member State law provide that the prohibition
> referred to in paragraph 1 may not be lifted by the data subject"

**In practice 9(2)(a) explicit consent is the only realistic exit** for a commercial companion
product. The other 9(2) grounds (employment law, vital interests, legal claims, public health,
foundation/association members, manifestly-made-public, etc.) do not fit.

**Consequences, and they are severe:**

1. **Legitimate interest is NOT an Art. 9 exit.** Art. 6(1)(f) is not in the Art. 9(2) list. So the
   whole EDPB Opinion 28/2024 three-step legitimate-interest analysis — even if you win it — **does
   not help you for special category data**. See `region-eu-edpb-opinion-28-2024.md`. This is the
   single most commonly missed point in AI data planning.

2. **"Explicit" is a higher bar than ordinary consent** — an express affirmative statement, not
   inferred from conduct or a pre-ticked box. And consent must still satisfy Art. 4(11) + Art. 7:
   **freely given, specific, informed, unambiguous, and as easy to withdraw as to give.**

3. **"for one or more specified purposes"** — purpose-specific. Consent to "chat with your companion"
   does **not** carry over to "we train on your transcripts" or "our annotators read your transcripts".
   **Training/eval needs its own explicit, separately-specified consent.** This is precisely the
   "entire lifecycle" point the Garante reserved for separate proceedings against Luka.

4. **Freely given is hard here.** If declining training-data consent degrades or blocks the service,
   the consent is likely not freely given (Art. 7(4) — conditionality). So the consent must be a
   genuine, refusable opt-in with a working product behind a "no". **Design consequence: an EU user who
   says no to training must still get a fully functional companion — which means the eval pipeline must
   tolerate a consent-filtered, non-representative sample.** That is a real measurement problem, not
   just a legal one: your EU eval data will be biased toward users who opted in.

5. **Withdrawable at any time** (Art. 7(3)) — and withdrawal must be as easy as giving. This implies a
   deletion/exclusion path **and** raises the model-unlearning problem if consented data is already
   baked into weights.

## Art. 6 lawful basis — legitimate interest vs consent for chat logs

**Art. 6(1)(a) — VERBATIM:**
> "the data subject has given consent to the processing of his or her personal data for one or more
> specific purposes"

**Art. 6(1)(f) — VERBATIM:**
> "processing is necessary for the purposes of the legitimate interests pursued by the controller or
> by a third party, except where such interests are overridden by the interests or fundamental rights
> and freedoms of the data subject which require protection of personal data, **in particular where the
> data subject is a child**"

**Note the child clause is in the black-letter text of 6(1)(f) itself** — not a recital. For a product
with any minor cohort (and the Garante found Replika had one), legitimate interest is pre-weighted
against you by the Article. Combined with `region-eu-ai-act-art5-manipulation.md`, **age assurance is
load-bearing across three separate legal regimes.**

**Practical split:**
- For **non-special-category** operational data (latency, error rates, aggregate quality metrics):
  Art. 6(1)(f) legitimate interest is plausible, subject to the EDPB three-step test.
- For **chat content**: even setting Art. 9 aside, the balancing test is uphill — the EDPB's
  "nature of the service" and "reasonable expectations" factors cut hard against a companion product.
  And Art. 9 is not set aside. **So: consent, in practice.**

## The regenerate-event question specifically

**~5M/day regenerate events as implicit preference labels.** The key insight: **the event and the
content are separable, and that separation is the whole compliance strategy.**

- A regenerate event as **bare metadata** — (session_id, turn_index, timestamp, "user pressed
  regenerate") — is personal data (linked to a user) but is **not obviously Art. 9 data**. It reveals
  dissatisfaction with a response, not sex life or health. Art. 6(1)(f) is arguable for this.
- **But a preference label is only useful with the (prompt, rejected_response, chosen_response)
  triple** — and *that* is the chat content, which for a companion product is very often Art. 9 data.
  **The label is worthless without the payload, and the payload is the problem.**
- So the regenerate signal **inherits the Art. 9 problem from the content it points at**, not from the
  click. The click is clean; the thing the click is *about* is not.

**Options, roughly in order of legal safety:**
1. **Metadata-only signal** — regenerate *rates* by model/persona/segment, no content retained. Clean
   under 6(1)(f), and a genuine aggregate quality signal. Weakest for preference learning, but note the
   EDPB's necessity test *actively favours* this: if metadata-only achieves the eval purpose, retaining
   content is "a less intrusive way" you failed to take.
2. **Explicit consent cohort** — an opt-in population whose full triples you may retain and train on.
   Smaller, biased, but lawful. Likely the right primary answer.
3. **Synthetic/proxy eval sets** — no production content at all. Sidesteps GDPR entirely; already the
   direction of much of this repo's benchmark work.
4. **Retain-everything-and-decide-later** — fails purpose limitation, data minimisation, storage
   limitation, and Art. 9 simultaneously. **This is the Luka failure mode.** Not viable.

## Data minimisation, purpose limitation, storage limitation vs "storage is free"

**Art. 5(1)(b) purpose limitation — VERBATIM:**
> "collected for specified, explicit and legitimate purposes and not further processed in a manner that
> is incompatible with those purposes"

**Art. 5(1)(c) data minimisation — VERBATIM:**
> "adequate, relevant and limited to what is necessary in relation to the purposes for which they are
> processed"

**Art. 5(1)(e) storage limitation — VERBATIM:**
> "kept in a form which permits identification of data subjects for no longer than is necessary for the
> purposes for which the personal data are processed"

**"Storage is free" is legally irrelevant — the test is necessity, not cost.** Three independent
principles each defeat collect-everything:
- 5(1)(c): "limited to what is necessary" — cost of storage is not a purpose.
- 5(1)(b): you must fix the purpose **at collection**. Retaining now to find uses later is the
  definition of incompatible further processing.
- 5(1)(e): a retention period is mandatory. "Indefinite" is not a period.

**The Garante fined Luka under Art. 5(1)(c) specifically.** This is not theoretical.

## Art. 22 — automated decision-making

**Art. 22(1) — VERBATIM:**
> "The data subject shall have the right not to be subject to a decision based solely on automated
> processing, including profiling, which produces legal effects concerning him or her or similarly
> significantly affects him or her."

**Art. 22(3) — VERBATIM:**
> "In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement
> suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at
> least the right to obtain human intervention on the part of the controller, to express his or her
> point of view and to contest the decision."

**Relevance: LIMITED but non-zero.**
- Generating a chat response is **not** a "decision" producing "legal effects" or "similarly
  significantly affect[ing]" the user. Ordinary companion operation does not engage Art. 22.
- **Where it could bite:** automated account bans/suspensions; automated safety classifications that
  restrict access; **automated risk-scoring of users (e.g. self-harm risk) that triggers consequential
  action.** A self-harm classifier that automatically locks an account or escalates could plausibly
  "similarly significantly affect" the user — and a companion platform is likely to build exactly that.
- **Art. 22(4) is the trap**: automated decisions under 22(2)(a)/(c) **cannot rely on Art. 9 special
  category data unless 9(2)(a) explicit consent or 9(2)(g) applies, with safeguards.** A self-harm
  classifier reads mental-health data (Art. 9) to make an automated consequential decision — that is
  **Art. 22(4) + Art. 9 stacked**, and it needs explicit consent plus Art. 22(3) safeguards (human
  intervention, contest right).
- **This is a live design constraint on the safety stack, not just the data stack — and it is an
  awkward one: the safety feature you build to protect vulnerable users is itself the highest-risk
  processing in the product.**

## Also flagged, not researched this pass — UNVERIFIED

- **Art. 8 GDPR** — conditions for children's consent re information society services (age 13-16
  depending on Member State). Directly relevant given the Replika age-verification findings. **Not
  fetched this pass.**
- **Art. 35 DPIA** — a DPIA is near-certainly mandatory here (large-scale Art. 9 processing +
  vulnerable data subjects). **Not fetched; strongly recommend confirming.**
- **Art. 3(2) territorial scope** — asserted above; not fetched verbatim this pass.
- Member-State variation: Art. 9(4) lets Member States add conditions for health/genetic/biometric
  data — so the analysis is **not uniform across the EU**. Not researched.
