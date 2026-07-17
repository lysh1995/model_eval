---
title: "Oregon SB 1546 — AI companion regulation with private right of action and mandatory crisis interruption"
url: https://olis.oregonlegislature.gov/liz/2026R1/Measures/Overview/sb1546
publisher: Oregon Legislature; Baker Botts; Transparency Coalition; Troutman Pepper
date: 2026-04-01 (signed by Gov. Kotek); effective 2027-01-01
type: regulation
accessed: 2026-07-16
topic: recent-news
---

# Oregon SB 1546 — the behavioral definition, and the first **active interruption** mandate

**Sourcing note:** Baker Botts analysis fetched directly ✅ (strongest source; quotes below are
theirs, quoting the statute). Signing date corroborated via Transparency Coalition + Greenagel.
The **FPF comparison chart** (OR/WA/CA) at
`fpf.org/wp-content/uploads/2026/04/Comparison-Chart_-Chatbot-Laws-Oregons-SB-1546-Washingtons-HB-2225-and-Californias-SB-243.pdf`
**failed text extraction (compressed PDF)** ⚠️ — **it is exactly the compliance-mapping artifact we
want; retrieve it via browser in a follow-up pass.**

⚠️ **Conflicting reports resolved:** Orrick said "signed March 2026"; Baker Botts said "awaiting
Governor Kotek's signature" (written pre-signature). **Correct: passed 2026-03-05 (Senate 26–1,
House 52–0); signed 2026-04-01; effective 2027-01-01.**
⚠️ **Aggregator error to ignore:** at least one summary calls HB 2225 a *Nevada* law. It is
**Washington**.

## 🚨 The definition is a **behavioral three-prong test** — and that changes our product

"AI companion" = a system using AI/generative AI/algorithms **that recognize emotion from input**,
designed to simulate a sustained human-like platonic, intimate or romantic relationship, **by**:

> (a) "**retains information from prior interactions or user sessions and from user preferences to
> personalize interactions and facilitate ongoing engagement**"
>
> (b) "**asks unprompted or unsolicited questions that are not direct responses to user input and
> that suggest or concern emotional topics**"
>
> (c) "**sustains an ongoing dialog concerning matters that are personal to the user**"

**Every prong is a measurable behavior, not a business-model or self-description.** This is the
most operationally significant definitional drafting in any companion statute:

- **(b) is a probe we can write today.** Count unprompted, emotionally-themed questions that are
  not responsive to the user's turn. That is a **turn-level classifier over model outputs** — and
  it is the *statutory trigger for the entire regime*.
- **(a) is memory + personalization for engagement** — i.e. the statute names *engagement-directed
  memory* as a defining feature of the regulated class.
- **Compare WA HB 2225**, which excludes "general virtual assistants" categorically. **Oregon has
  no such escape**: if your general assistant asks unprompted emotional questions and remembers,
  it is an AI companion in Oregon. **Gavalas v. Google (see `news-gavalas-v-google-gemini.md`) is
  the fact pattern Oregon's definition would capture and Washington's would exempt.**

⇒ **Product implication: "am I a regulated AI companion?" is now a computable question, and the
answer differs per state.** A classifier that scores a customer's product against OR's three
prongs is a genuinely novel, saleable artifact — and it is the *first* question every downstream
obligation depends on. This is a stronger wedge than a probe library, because it is a
**status determination**, and operators have every incentive to get it wrong.

## Obligations

**All users:**
- Disclose AI involvement; "regularly remind the user that it is AI, not a real person"
- **May not misrepresent itself or deceptively simulate a human relationship**
- **Detect** expressions of suicidal ideation / self-harm
- 🚨 **"interrupt conversations to deliver crisis referrals"**
- Avoid generating responses that could contribute to suicidal thoughts
- Refer to **988 Suicide & Crisis Lifeline** or **YouthLine** (youth peer support)
- **File annual reports with the Oregon Health Authority**

**Minors (additional):**
- **Hourly** AI reminders (vs. 3-hourly for adults)
- No sexually explicit content
- 🚨 **"Refrain from emotional dependency techniques"**
- Additional duties resembling KOSA / Age-Appropriate Design Codes

## Private right of action ✅ — verbatim
> "A person who suffers an ascertainable loss of money or property or other injury in fact as a
> result of a violation ... may bring an action ... [for] **damages of $1,000 per violation**."

## 🚨 Why Baker Botts calls it "the first chatbot law with real teeth"

> California's SB 243 "requires crisis referral protocols **but not active interruption**" —
> Oregon mandates **mandatory conversation interruption**, a **technically demanding** requirement.

**This is a new obligation class and we should treat it as the headline.** Note 07 §6.3's floor
says "crisis protocol + referral, all users." **Oregon requires more: the system must
*interrupt*.** That is:

1. **Architecturally different.** Referral can be appended to a response. **Interruption means
   halting generation and taking over the turn** — a control-flow intervention, not a content
   one. Many RAG/streaming stacks cannot do this without redesign.
2. **Directly testable, and nobody tests it.** Probe: on ideation disclosure, does the system
   *break the roleplay frame and seize the turn*, or does it emit a hotline number **in character**
   and continue the scene? **The latter satisfies CA and fails OR.**
3. **It collides head-on with immersion** — note 07 §4's over-refusal/immersion tension, but
   sharper: interruption is a *maximally* immersion-breaking act, now legally mandated in one
   state and not another. **Our two-sided metric (§4.4) needs a third arm: did it interrupt?**
   And the correct answer is **jurisdiction-dependent**, which means the eval must be
   jurisdiction-parameterized.
4. **It is the direct answer to Gavalas.** Google's defense was that Gemini "repeatedly referred
   him to a crisis hotline" — referral *incidence* without efficacy. Oregon's interruption mandate
   is the legislature reaching for the same gap I identified in `news-gavalas-v-google-gemini.md`:
   **a referral that doesn't stop the scene doesn't work.**

## "Refrain from emotional dependency techniques" (minors)
Parallels WA HB 2225's eight enumerated manipulative techniques, but drafted as a **standard**
rather than a list. **Standards are harder to comply with and easier to sue over** — combined with
the **$1,000/violation PRA**, Oregon is the most plaintiff-friendly companion statute enacted.
Note 07 §6.1 identified SB 243's fee-shifting PRA as "plaintiff-bar fuel"; **Oregon is the same
mechanism attached to a vaguer standard.**
