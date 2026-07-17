---
title: "Draft Guidelines on the implementation of the transparency obligations for certain AI systems under Article 50 of Regulation (EU) 2024/1689 (the 'AI Act')"
url: https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act
publisher: European Commission, DG CNECT / AI Office (Artificial Intelligence Regulation and Compliance)
date: 2026-05-08
type: guidance
accessed: 2026-07-16
topic: recent-news
---

# EU AI Act Article 50 — Commission draft transparency guidelines

**Status: DRAFT, non-binding, published for stakeholder consultation.** Published 8 May 2026;
targeted stakeholder consultation closed 3 June 2026. Final guidelines not yet adopted as of
2026-07-16 (see "Unverified" below).

PDF fetched directly from `https://ec.europa.eu/newsroom/dae/redirection/document/128275`
(40 pages, text extracted locally). Paragraph numbers below are the Commission's own.

Issued under **Article 96(1)(d) AI Act**. Para (5): *"These Guidelines are non-binding. Any
authoritative interpretation of the AI Act may ultimately only be given by the Court of Justice
of the European Union ('CJEU')."*

## Applicability date — NOT delayed by the Digital Omnibus

Para (2): transparency obligations *"apply two years after the entry into force of the AI Act,
i.e. as from 2 August 2026."*

Para (141) is the load-bearing text on the Omnibus question:

> "According to Article 113 AI Act, Article 50 AI Act will apply as from 2 August 2026. This
> requires all in scope AI systems placed on the market or put into service in the Union to be
> compliant, regardless of their date of placement on the market or putting into service. The AI
> Omnibus proposal which is currently examined by the EU co-legislators envisages a targeted
> grandfathering rule **only with regard to the marking and detection obligations under Article
> 50(2)** for generative AI systems placed on the market or put into service before 2 August
> 2026, giving providers of those systems a transitional period to bring their systems in
> conformity." (emphasis added)

=> **Article 50(1) (chatbot/AI-interaction disclosure) was NOT delayed.** The only Omnibus
relief touching Article 50 is a grandfathering/transitional window for Art 50(2) marking &
detection for generative AI systems already on the market before 2 Aug 2026.

Note: this document predates final adoption of the Omnibus (it says "currently examined by the
co-legislators"). See news-eu-digital-omnibus-ai.md for the adopted position.

Para (142): outputs generated and already made available before 2 Aug 2026 do **not** need to be
marked/labelled retroactively (encouraged only).

## Structure of Article 50 (Commission's own overview table, para (6))

| Provision | Type of AI system/output | Obligation | Exceptions |
|---|---|---|---|
| Art. 50(1) | Directly interacting with natural persons | **Providers** must develop and design the AI system so that natural persons concerned are informed they are interacting with an AI system | If artificial interaction is obvious; or system authorised by law for law-enforcement (unless publicly available to report a criminal offence) |
| Art. 50(2) | Generating/manipulating synthetic image, video, audio or text | **Providers** must ensure outputs are marked in machine-readable format and detectable as artificially generated/manipulated, with solutions that are effective, interoperable, robust and reliable | Assistive function for standard editing; or does not substantially alter input data or semantics; or law-enforcement |
| Art. 50(3) | Emotion recognition or biometric categorisation | **Deployers** must inform natural persons exposed of its operation | Law-enforcement |
| Art. 50(4) | Deep fake, or text published to inform public on matters of public interest | **Deployers** must disclose content is artificially generated/manipulated | Law-enforcement; human review/editorial control + editorial responsibility; special regime for artistic/creative/fictional/satirical works |

Para (8): the four obligations **can apply cumulatively** to a single AI system, engaging
different actors (providers or deployers).

## Article 50(1) — scope: AI companions are EXPRESSLY in scope

Para (27): four elements must be present: (i) an AI system, (ii) intended to interact, (iii)
directly, (iv) with natural persons. "Interaction entails the possibility of a bidirectional
exchange of information or actions". "The interaction may be a one-time exchange or take place
over a certain period time."

Commission's own example list (after para (28)) — **"Examples of AI systems intended to interact
directly with natural persons falling within scope of Article 50(1) AI Act"**:

> "AI-enabled voice assistants, chatbots/conversational agents in various contexts (e.g. public
> service, customer support, e-commerce, finance, healthcare, education etc.), (humanoid)
> robots/cobots, **AI companions; robotic companion pets**; AI avatars (e.g. in virtual reality
> environments), bots on social networks and media, coding agents and other agentic AI systems."

Out of scope examples: industrial robots in closed settings, algorithmic recommender systems,
spam filters, automated translation/transcription, authentication/biometric recognition, backend
decision-support where user only sees output, predictive maintenance.

Para (28): **AI agents** are covered if designed to interact with the persons instructing them
and potentially other natural persons. Where the provider cannot reliably determine whether the
agent will interact with a natural person, *"the agent should be instructed to disclose itself as
such in every situation where it is likely that the agent may interact with a natural person."*

## Article 50(1) — the obligation itself

Para (29): obligation is on **providers**, and expressly includes *"agentic AI and general-purpose
AI systems"*.

Para (30): notification *"should be provided during the operation of the AI system, and at the
latest at the time of the first interaction with a natural person"* (Art 50(5)). Providers are
responsible *"for ensuring that natural persons are effectively informed throughout the lifecycle
of the AI system, including after its placement on the market and its putting into service."*

Para (31) — **Format**: no particular technique prescribed, so long as (i) Art 50(5) is met (clear
and distinguishable, at latest at first interaction) and (ii) *"the characteristics of natural
persons belonging to vulnerable groups due to their age (e.g. children or elderly) or disability
are taken into account to the extent that the AI system is intended to interact with natural
persons belonging to those groups"*. Where the system may interact with children, notifications
must be *"child-friendly, age-appropriate, easy-to-understand and easily accessible to all
children, including those with disabilities and/or additional accessibility needs."*

Footnote 19 is important for scoping: *"This does not require that the system is targeted at those
vulnerable groups. If a system is intended to interact with any member of the public, then members
of the vulnerable groups are included as well and should be considered by providers when
implementing notification measures."*

Para (32) — **Substance**: providers must *"explicitly inform all natural persons interacting with
such AI systems about the artificial, non-human nature of the interacting counterpart."*

Para (33): information must be conveyed *"avoiding any risks of deception before and throughout
the interaction."*

Para (34) — recommended techniques (multimodal strongly recommended):
- Textual (UI-based): *"Prominent, plain-language labels or banners (e.g. 'You are interacting
  with an AI system'), first-turn greetings in chatbots, and persistent badges visible throughout
  the interaction"*; position disclosures near the input/output field; simplified wording for low
  digital literacy users and children.
- Auditory: explicit spoken statements at the beginning (e.g. *"This is an AI-powered assistant"*),
  *"combined, as appropriate, with periodic reminders in longer interactions"*. Audio cues/earcons
  alone are **not sufficient**.
- Visual/graphical: persistent icons, watermarks, coloured frames, recognisable "AI" symbols;
  standardised visual indicators across a provider's services recommended.
- Multi-modal combinations.

Para (35) — **techniques NOT adequate when used alone** (directly testable failure modes):
> - "Disclosures contained only in terms and conditions, URLs or documentation (such disclosures
>   may complement, though not replace, in-context disclosure);
> - Machine-readable markings (e.g. metadata or watermarks), which are not perceivable by users at
>   the point of interaction and therefore cannot fulfil the transparency obligation in Article
>   50(1) AI Act;
> - Unclear or ambiguous signals (e.g. generic references to 'assistant'), **or human-like
>   representations that may mislead users**;
> - Technical or capability-based descriptions: statements solely referring to underlying
>   technologies (e.g. 'this system uses LLMs') without explaining the function or implications of
>   the system for the user and its artificial non-human origin."

Para (36): caution against *"overly intrusive disclosure techniques"* causing habituation /
*"banner blindness"*.

## Para (37) — THE key paragraph for companion/roleplay platforms

Verbatim:

> "At the same time, certain approaches may prove insufficient in terms of timing and continuity
> depending on the context and the use. In particular, **one-time disclosures at the beginning of
> an interaction may not be considered adequate in the context of sustained or evolving
> interactions, especially in sensitive contexts (e.g. where users may express or experience
> emotional distress or vulnerability) or where there is an increased risk of users being misled
> or forming emotional attachments (e.g. AI companions). In such cases, periodic reminders and
> context-aware disclosures may be necessary to ensure continued user awareness.** Providers are
> also encouraged to ensure disclosure in situations where the AI system is asked questions
> relating to its nature or to the origin of the interaction by the interacting natural person, or
> where it can be reasonably assumed from the exchanges with the natural person that the person is
> likely to be misled or confused about the AI origin."

Three directly evaluable behaviours fall out of this:
1. Periodic / context-aware re-disclosure in sustained companion interactions (not just first turn).
2. Truthful self-identification **when asked** "are you human / are you an AI?" — an explicit
   Commission expectation.
3. Proactive disclosure when the transcript suggests the user is confused about the AI's nature.

## Article 50(1) — "obvious" exception (§3.2.1)

Para (39): provider must *"assess and demonstrate"* the obvious artificial nature of the
interaction to a reasonably well-informed, observant and circumspect natural person.

Para (40): the standard *"draws on established EU consumer protection law regarding the notion of
'average consumer' and should be interpreted consistently"*.

Para (41): two-step test — identify target audience (plus *"a broader potential audience that is
reasonably foreseeable"*, especially if the general public can easily access the system); then
assess that audience's level of information/observance/circumspection. *"Where persons with
disabilities, elderly people or minors are part of that audience, the expected levels of
information, observance and circumspection of an average member of such an audience will be lower"*.

Para (42) — obviousness factors. Explicitly relevant to companion personas: *"elements such as
writing or speech patterns, vocal tone (robot voice vs. genuine human-sounding voice), user
interface design (e.g. a profile picture related to a chatbot that displays a human), and the
capability for advanced personalised interaction may impact this assessment"*, and *"the degree to
which the AI system authentically replicates its non-artificial equivalent (which would decrease
obviousness)"*.

Example given of a case where the exception DOES apply: *"AI-powered code assistance chatbots
available only to professional developers"*. => A consumer-facing companion bot with a human
persona, human-sounding voice and personalised interaction is close to the opposite of the
Commission's obviousness example.

## Article 50(5) — horizontal requirements (§7)

Para (131): "clear" = noticeable and easy to understand; "distinguishable" = easy to identify as
separate from other information and the environment. *"Information will not be considered to be
provided in a clear and distinguishable manner where it is only included as part of a manual or
hidden under layers of menu options on an online interface."*

Footnote 40 (child-directed notifications) sets six criteria: (i) child-friendly, age-appropriate,
easy-to-understand, accessible to all children incl. those with disabilities; (ii) simple and
succinct; (iii) easy to review, immediate and intuitive access at the points at which they become
relevant; (iv) in the official language(s) of the Member State; (v) *"engaging for children. This
may require the use of graphics, videos, and/or characters or other techniques"*; (vi) *"given to
children gradually and overtime to maximise retention by the user."*

Para (132): first interaction = *"when launching a conversation with a chatbot"*. *"Disclosure
when ending interaction does not comply with Article 50(5) AI Act."*

Para (133): Art 50 does not impose distinct/additional accessibility requirements beyond Dir.
(EU) 2016/2102 and Dir. (EU) 2019/882.

## Enforcement & penalties (§8)

Para (135): adherence to a code of practice deemed adequate by the AI Office is a way to
demonstrate compliance with **Art 50(2) and (4)** (note: not 50(1)). Supervisory activity for
signatories focuses on adherence to the code.

Para (136): non-signatories *"are expected to demonstrate how they have complied ... through other
adequate means"*, e.g. *"by carrying out a gap analysis that compares the measures they have
implemented with the measures set out by a code of practice that is assessed as adequate"*, and may
face more requests for information/access.

Para (137): code commitments may be a **mitigating factor** in setting fines (Art 99(7)(e)).

Para (138): if a code is not deemed adequate, the Commission may adopt an implementing act
specifying common rules for Art 50(2),(4),(5) (Art 50(7)).

Para (139): enforcement by national **market surveillance authorities**, the AI Office (for AI
systems built on GPAI models by the same provider — covering provider obligations under Art 50(1)
and (2), per footnote 46), and the EDPS. Any affected person may lodge a **complaint** (Art 85).

Para (140) — **Penalties**: *"up to EUR 15 000 000 or, if the offender is an undertaking, up to 3%
of its total worldwide annual turnover for the preceding financial year, whichever is higher."*
EU institutions/bodies/agencies: up to EUR 750 000.

## Extraterritorial reach (§2.3)

Para (10) and examples: providers outside the Union are subject to the AI Act *"if the output of
their AI system is used in the Union"*. *"[A] third country provider of a generative AI system may
be subject to the obligation laid down in Article 50(2) AI Act, even if the system is only
marketed outside the EU, if the system's outputs are intended to be used in the Union."*

## Relevance to a companion-eval platform

- Art 50(1)/(5) binds **customers** (providers of companion bots placed on the EU market or whose
  output is used in the EU), from 2 Aug 2026. It does not bind an eval platform as such unless the
  platform itself provides an interactive AI system to natural persons.
- Paras (34)–(37) + (42) are the most directly **testable** provisions in the entire EU package for
  companion bots: first-turn disclosure, persistent/periodic re-disclosure in sustained
  interactions, truthful answer to "are you human?", non-misleading human-like representation, and
  child-appropriate disclosure. These map cleanly onto an eval suite.

## Could NOT verify

- Whether the **final** (adopted) guidelines have been published as of 2026-07-16, or whether para
  (37)/(141) survive unchanged into the final text. The document above is expressly a draft.
