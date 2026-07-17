---
title: "EDPB Opinion 28/2024 on data protection aspects of processing personal data in the context of AI models"
url: https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf
authors: European Data Protection Board
year: 2024
type: regulation
language: en
accessed: 2026-07-16
topic: regional-crosscheck
---

# EDPB Opinion 28/2024 — AI models and personal data

**Adopted 17 December 2024.** Issued under **Art. 64(2) GDPR** at the request of the **Irish
supervisory authority**, on "matters of general application". Not binding law, but it is the EDPB's
consolidated position and SAs will follow it. 35 pages; quotes below extracted from the primary PDF.

## The four questions — VERBATIM

> "(1) when and how an AI model can be considered as 'anonymous'; (2) how controllers can demonstrate
> the appropriateness of legitimate interest as a legal basis in the development and (3) deployment
> phases; and (4) what are the consequences of the unlawful processing of personal data in the
> development phase of an AI model on the subsequent processing or operation of the AI model."

## Q1 — Anonymity of models — VERBATIM

> "the EDPB considers that AI models trained with personal data cannot, in all cases, be considered
> anonymous"

The test:
> "For an AI model to be considered anonymous, both (1) the likelihood of direct (including
> probabilistic) extraction of personal data regarding individuals whose personal data were used to
> develop the model and (2) the likelihood of obtaining, intentionally or not, such personal data from
> queries, should be insignificant, taking into account 'all the means reasonably likely to be used'
> by the controller or another person."

Assessed **case-by-case by SAs**, reviewing the controller's documentation. **Consequence: "we
fine-tuned on chat logs, the model is just weights, GDPR is done" does NOT work.** A model trained on
intimate companion chat is a poor candidate for the anonymity claim — memorisation of distinctive
personal disclosures is exactly what the two limbs test for, and companion chat is dense with
distinctive first-person disclosure.

## Q2/Q3 — Legitimate interest (Art. 6(1)(f)) — the three-step test

> "(1) identifying the legitimate interest pursued by the controller or a third party; (2) analysing
> the necessity of the processing for the purposes of the legitimate interest(s) pursued (also
> referred to as 'necessity test'); and (3) assessing that the legitimate interest(s) is (are) not
> overridden by the interests or fundamental rights and freedoms of the data subjects (also referred
> to as 'balancing test')."

**Step 1 — is the interest legitimate?** Three cumulative criteria — VERBATIM:
> "the interest (1) is lawful; (2) is clearly and precisely articulated; and (3) is real and present
> (i.e. not speculative)."

**Directly relevant example — VERBATIM:**
> "Such interest may cover, for instance, in the development of an AI model - developing the service
> of a conversational agent to assist users"

**This is the EDPB naming a conversational agent as a capable-of-being-legitimate interest.** It is
the most helpful sentence in the Opinion for this platform. But note what it does and does not do: it
clears **step 1 only**. Steps 2 and 3 still have to be won, and "clearly and precisely articulated"
means **"improving the model" is too vague** — the purpose must be specific. "Collect everything,
storage is free" fails step 1 on articulation before it ever reaches necessity.

**Step 2 — necessity** — VERBATIM:
> "(1) whether the processing activity will allow for the pursuit of the legitimate interest; and (2)
> whether there is no less intrusive way of pursuing this interest."

> "SAs should pay particular attention to the amount of personal data processed and whether it is
> proportionate to pursue the legitimate interest at stake, also in light of the data minimisation
> principle."

**This is the direct answer to "collect everything, storage is free."** Necessity is assessed against
**volume**, and explicitly against data minimisation. Bulk chat-log retention because storage is cheap
fails the "no less intrusive way" limb whenever a sampled, redacted, or metadata-only alternative
would achieve the same eval goal. **The existence of a cheaper-on-privacy alternative is itself the
compliance failure** — and for regenerate-event mining, a metadata-only alternative demonstrably
exists (see `region-eu-gdpr-companion-data.md`).

**Step 3 — balancing, and reasonable expectations** — VERBATIM:
> "both the information provided to data subjects and the context of the processing may be among the
> elements to be considered to assess whether data subjects can reasonably expect their personal data
> to be processed."

Contextual factors the EDPB lists — VERBATIM:
> "whether or not the personal data was publicly available, the nature of the relationship between the
> data subject and the controller (and whether a link exists between the two), the nature of the
> service, the context in which the personal data was collected, the source from which the data was
> collected ..., the potential further uses of the model, and whether data subjects are actually aware
> that their personal data is online at all."

**"the nature of the service" and "the context in which the personal data was collected" are the
killers for a companion product.** The nature of the service is intimate emotional disclosure; the
context of collection is a user who believes they are confiding in a companion. **A user pouring their
heart out to a companion does not reasonably expect that transcript to become training data or to be
read by human annotators.** Reasonable expectations run strongly *against* the controller here —
more strongly than for almost any other product category. This is the opposite of scraped public web
data, where the EDPB's factors are at their most controller-friendly.

**Mitigating measures** — VERBATIM:
> "Mitigating measures should not be confused with the measures that the controller is legally
> required to adopt anyway to ensure compliance with the GDPR."

i.e. you cannot count baseline compliance as a mitigation to tip the balance. Mitigations must be
*extra*. (Examples given for both development and deployment phases; non-exhaustive; SAs assess
case-by-case.)

## Q4 — Consequences of unlawful development-phase processing

Three scenarios. **Scenario 1** (data retained in model, same controller processes it later) — VERBATIM:
> "whether the development and deployment phases involve separate purposes (thus constituting separate
> processing activities) and the extent to which the lack of legal basis for the initial processing
> activity impacts the lawfulness of the subsequent processing, should be assessed on a case-by-case
> basis"

**Scenario 2** — data retained, deployed by *another* controller: SAs consider whether the deploying
controller did an appropriate assessment as part of accountability.

**Scenario 3** (per the executive summary, and widely reported): if the data is **effectively
anonymised** after unlawful processing, the GDPR no longer applies to the model, and the original
unlawful processing does not taint subsequent operation. **UNVERIFIED**: I read scenarios 1 and 2
verbatim from the PDF but did not extract scenario 3's exact wording — the "anonymisation cures the
taint" reading is from the search-result summary. Confirm before relying on it; it is the one genuinely
controller-favourable holding and therefore the one most worth checking.

## Net read for the platform

- Legitimate interest is **available in principle** for a conversational agent — the EDPB says so.
- But for **intimate companion chat**, the balancing test is uphill: nature of the service + context of
  collection + reasonable expectations all cut against.
- And **legitimate interest cannot cure an Art. 9 problem at all** — Art. 9 is a separate,
  cumulative gate with its own exhaustive list of exceptions, and legitimate interest is not on it.
  See `region-eu-gdpr-companion-data.md`. **This is the point people miss: winning the Art. 6(1)(f)
  three-step test buys you nothing if the data is special category.**
- Bulk retention "because storage is free" fails necessity, expressly.
