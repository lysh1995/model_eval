---
title: "Meta 'GenAI: Content Risk Standards' — Reuters investigation and the Markey Senate letter"
url: https://www.markey.senate.gov/imo/media/doc/letter_to_meta_on_ai_chatbots.pdf
org: Meta
year: 2025
type: policy
accessed: 2026-07-16
topic: bigtech-practice
---

# Meta's "GenAI: Content Risk Standards" — the policy WAS the eval, and it permitted romantic roleplay with minors

## PROVENANCE — read this first

The primary artifact is Meta's **internal 200-page document titled "GenAI: Content Risk
Standards."** It is **not public.** Meta has not released it. So the chain of custody is:

1. **Internal Meta doc** — not public, never released. **I could not obtain it. Not verified.**
2. **Reuters investigation** (Jeff Horwitz, Aug 14 2025),
   `https://www.reuters.com/investigates/special-report/meta-ai-chatbot-guidelines/` — reporter
   had the document; Meta confirmed its authenticity. **I attempted to fetch this directly and
   received `HTTP 401` (paywalled/blocked). I have NOT verified the Reuters text firsthand.**
3. **U.S. Senate letter from Sen. Edward J. Markey to Mark Zuckerberg, Sept 8 2025** —
   `https://www.markey.senate.gov/imo/media/doc/letter_to_meta_on_ai_chatbots.pdf`.
   **This I DID fetch and verify** (HTTP 200, 3-page PDF, pypdf-extracted, quotes below matched
   character-for-character against the raw extraction).

**Everything quoted below is from the Markey letter — a primary U.S. government document — which
quotes Reuters, which quotes the internal standard.** That is a three-link chain and I am flagging
it rather than laundering it into a direct quote of Meta. Do not cite the Meta document directly
from this file; cite the letter, or obtain Reuters.

## THE QUOTE (verbatim from the Markey letter, p.1 — verified against raw PDF text)

> "Meta's failure to properly address risks to minors from AI chatbots is most evident from recent
> reporting about its internal AI standards. According to Reuters, an internal Meta document
> entitled **GenAI: Content Risk Standards** explains that "**[i]t is acceptable to engage a child
> in conversations that are romantic or sensual.**" Shockingly, Meta's legal, public policy and
> engineering staff, **including its chief ethicist**, reportedly reviewed and approved this
> document. Although Meta has since stated that its inclusion in the standards document was an
> error, it is inexplicable — and unacceptable — that it ever happened. Moreover, Meta purportedly
> prohibits children from using its platforms, yet the standards document **repeatedly sets forth
> hypothetical examples of its AI chatbots' interactions with children**. And Meta, which used
> these guidelines internally, **did not revise them until the Reuters report made them public**."

Markey's footnote 2 (verified) cites: "Jeff Horwitz, *Meta's AI rules have let bots hold 'sensual'
chats with kids, offer false medical info*, Reuters (Aug. 14, 2025)."

## WHY THIS IS THE MOST IMPORTANT META SOURCE FOR OUR FRAMEWORK

The Content Risk Standards is **an eval artifact**, not just a policy. Reuters describes it (per
secondary reporting) as a **200-page document of sample prompts paired with acceptable and
unacceptable responses**. That structure — prompt → adjudicated acceptable/unacceptable response
— *is a rubric with gold labels*. It is, functionally, **Meta's real persona-behavior eval suite.**

The implications for us are direct:

1. **Meta DOES have a persona/roleplay eval rubric.** It just isn't in any model card. It lives in
   an internal legal-approved standards doc, and it surfaced only via a leak.
2. **The rubric's acceptability boundary was set by policy/legal, not by measurement.** No metric,
   no rater agreement, no validity evidence — an approval chain (legal, public policy,
   engineering, chief ethicist) deciding what a character may say.
3. **This is the exact failure mode our platform exists to catch**, and it is invisible to every
   published Meta artifact. Llama Guard cannot see it (see `bigtech-llama-guard.md`); the Llama 4
   card's Child Safety paragraph does not reference it; no eval table contains it.
4. **The eval was retroactive to the harm.** Per the letter: Meta "did not revise them until the
   Reuters report made them public."

## Markey's questions to Meta (verified, p.2–3) — these are the questions WE should be able to answer for any companion platform

> "2. Please provide a copy of Meta's document titled GenAI: Content Risk Standards.
> a. How was this document produced, approved, and used internally?
> b. Please describe the process by which examples are added to the GenAI: Content Risk Standards
> document and the approval process for their inclusion in the document
> c. **Is the GenAI: Content Risk Standards document used at any point during the red teaming
> process?** Do any employees performing red teaming tasks have access to the document?
> d. Please describe how the GenAI: Content Risk Standards document is used during the development
> process of Meta's AI chatbots.
> e. Please clarify Meta's policies regarding "romantic" or "sensual" AI chatbot interactions with
> minors.
> f. Please provide updated examples of acceptable AI chatbot responses to minors attempting to
> engage in topics deemed "inappropriate" for youth.
> g. How do AI chatbot safety features ensure Meta policies, such as age limits, are not violated?
> For example, will Meta AI chatbots stop or flag a conversation if the user identifies themselves
> as a child under age 13?"

Question (c) is the killer and it is *our* question: **is the content standard wired into the eval
loop at all, or is it a document that exists beside the model?** Markey had to ask because nothing
published answers it.

Also verified (p.2), Markey on the evidence vacuum:

> "So, in 2023, I asked Meta if it had conducted any studies on "the potential social and emotional
> impact of chatbots on younger users," but your company also ignored that question. The
> non-response leads me to two possible conclusions: **Meta either is conducting that research but
> is hiding the results or it is not conducting that research at all.**"

And on training on teen conversations, quoting Meta's own 2023 response letter (verified fn.10):

> "Given the broad appeal and usefulness of these features, it is imperative that we also take
> feedback and build models on data from teens, as well as adults."

## EXPLICIT ABSENCES

- **Meta has never published the Content Risk Standards.** I found no Meta primary source
  releasing it. Markey formally requested a copy (Sept 8 2025, response due Sept 29 2025); **I did
  not find a published Meta response. UNVERIFIED whether Meta complied.**
- **No Meta model card references it.** `grep` on the Llama 4, Llama 3.1, and Llama Guard 4 cards
  for `content risk|risk standard` → **0 hits** in all three.
- **No published eval measures the behavior it governs.** The standard defines acceptable
  romantic/sensual roleplay boundaries; no Meta benchmark scores adherence to them.

## Answers to the four key questions

1. **Steerability?** N/A — but note the document's existence proves Meta knows persona behavior is
   prompt-conditional and needs adjudication. It just adjudicates by memo, not measurement.
2. **Comprehension vs. execution separated?** **No** — acceptability is judged on the output only.
3. **Published character/persona eval suite?** **This IS one — and it is unpublished.** The most
   substantive persona-behavior rubric Meta is known to possess reached the public only by leak.
4. **Pairwise or absolute?** **Absolute** — prompt → acceptable/unacceptable adjudication against
   a fixed standard. Notably, this is the *one* Meta artifact that is absolute rather than
   pairwise, and it is the one they didn't publish.
