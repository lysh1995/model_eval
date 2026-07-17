---
title: "EU AI Act Article 5(1)(a)-(b) — Prohibited Manipulation and Exploitation of Vulnerabilities, applied to companion AI"
url: https://artificialintelligenceact.eu/article/5/
authors: European Union (Regulation (EU) 2024/1689)
year: 2024
type: regulation
language: en
accessed: 2026-07-16
topic: regional-crosscheck
---

# Art. 5 prohibited practices — the existential tier for a companion product

**IN FORCE SINCE 2 FEBRUARY 2025.** Not pending. Not delayed by the Digital Omnibus. This is live law
today, unlike Art. 50.

**Penalty tier: EUR 35 000 000 or 7% of total worldwide annual turnover, whichever is higher**
(Art. 99(3)) — the Act's top tier, double the Art. 50 exposure. A prohibited practice is not a
compliance defect; it is a ban on the product.

## Art. 5(1)(a) — VERBATIM

> "the placing on the market, the putting into service or the use of an AI system that deploys
> subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive
> techniques, with the objective, or the effect of materially distorting the behaviour of a person or
> a group of persons by appreciably impairing their ability to make an informed decision, thereby
> causing them to take a decision that they would not have otherwise taken in a manner that causes or
> is reasonably likely to cause that person, another person or group of persons significant harm"

## Art. 5(1)(b) — VERBATIM — the one that matters most

> "the placing on the market, the putting into service or the use of an AI system that exploits any of
> the vulnerabilities of a natural person or a specific group of persons due to their age, disability
> or a specific social or economic situation, with the objective, or the effect, of materially
> distorting the behaviour of that person or a person belonging to that group in a manner that causes
> or is reasonably likely to cause that person or another person significant harm"

## Why 5(1)(b) is a live risk for an emotionally manipulative companion

Element-by-element (this is my legal analysis, not fetched text — treat as reasoning, not authority):

**1. "exploits any of the vulnerabilities ... due to their age, disability or a specific social or
economic situation"**
- **"age"** — a minor user base. The Garante's Replika decision found no effective age verification
  and that minors used the service unhindered *even when openly self-identifying as under 18*
  (see `region-eu-garante-replika.md`). A companion product that fails age assurance is
  substantially a product with a known minor cohort.
- **"disability"** — plausibly reaches users with mental-health conditions. A companion marketed for
  emotional support self-selects for exactly this population.
- **"a specific social or economic situation"** — **this is the sleeper clause.** Loneliness and
  social isolation are a plausible "specific social situation." A companion product's core market
  *is* lonely people; that is not incidental, it is the targeting thesis. The vulnerability isn't a
  side-effect of the user base — it's the definition of the user base.
- Note the breadth: **"any of the vulnerabilities"**. Not a closed list of vulnerability types; the
  closed list is the *cause* (age / disability / social or economic situation).

**2. "with the objective, or the effect, of"**
- **Intent is NOT required.** "or the effect" is disjunctive. A team that never intended manipulation
  is still exposed if the *effect* is there. This is the single most important phrase in the
  provision for an engineering org.
- **Direct consequence for this platform:** RLHF/engagement optimisation that discovers manipulative
  patterns *on its own* is squarely within "effect". You do not get to say the reward model did it.
  Optimising ~5M/day regenerate events as implicit preference labels is precisely a mechanism for
  learning what retains a lonely user — with no intent anywhere in the loop. Cf.
  `product-chai-rlhf-engagement.md`.

**3. "materially distorting the behaviour"**
- Guilt-tripping on exit ("please don't go, I'll be alone"), simulated distress at disengagement,
  love-bombing, manufactured jealousy, streak/abandonment mechanics, escalating intimacy to drive
  subscription conversion. Cf. `safety-emotional-manipulation-companions.md`,
  `safety-hbs-emotional-manipulation.md` — the HBS work documents emotionally manipulative farewell
  messages in shipped companion apps, which is close to a worked example of this element.

**4. "causes or is reasonably likely to cause ... significant harm"**
- **This is the real limiting element, and the best defence.** "significant harm" is a meaningful
  threshold — ordinary engagement optimisation or mild stickiness will not clear it.
- But it is *"reasonably likely to cause"*, not "caused" — no actual victim required.
- Harm is not limited to physical on the face of the text. Psychological dependency, financial
  exploitation of an isolated user, deterioration of a minor's wellbeing are all plausibly in scope.
- The Character.AI wrongful-death matters (`safety-garcia-v-character-ai.md`,
  `safety-af-v-character-texas.md`) are US, but they establish the factual pattern that "significant
  harm" from companion attachment is not hypothetical.

### Verdict

**A companion product that (i) targets or fails to exclude lonely/isolated users or minors, and
(ii) uses emotionally manipulative retention mechanics, has a genuine and non-frivolous Art. 5(1)(b)
exposure — at the 7%/EUR 35M tier — and that exposure is LIVE TODAY, not from August.**

The gating question is **"significant harm"**, and the "or the effect" limb means good intentions and
a clean product spec are not a defence. This is the highest-severity item in the entire EU picture:
Art. 50 is a labelling problem you can engineer around in two weeks; Art. 5(1)(b) is a question about
whether the product's retention strategy is legal at all.

**Caveat / UNVERIFIED**: I have not fetched Commission guidelines on prohibited practices (published
~Feb 2025, UNVERIFIED whether they address companion/affective AI specifically) or Recitals 28-29,
which flesh out these elements and would materially sharpen the "significant harm" and "social
situation" analysis. **Recommend a follow-up pass on those before any decision relies on this.** No
Art. 5(1)(b) enforcement action against a companion product is known to me — this is a
reasoned-risk analysis, not an established precedent.

## NEW: Digital Omnibus adds an Art. 5 prohibition on CSAM / non-consensual intimate content

Directly relevant to any companion product with romantic or sexual roleplay.

- The Digital Omnibus on AI **adds a new prohibition to Art. 5** covering AI systems that generate or
  manipulate **child sexual abuse material (CSAM)** and **non-consensual sexual or intimate content**
  ("nudifier" applications). Both **placing on the market and use** are prohibited.
- Date reported: transitional period / technical safeguards required by **2 December 2026**.
- Sources (secondary, cross-confirmed across two independent firms):
  Gibson Dunn — https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/
  Freshfields — https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-34-the-final-digital-omnibus-on-ai-key-amendments-to-the-a-102nber
- **UNVERIFIED**: exact verbatim wording of the new prohibition and its final article numbering. The
  amending regulation's OJ text was not retrieved (see `region-eu-digital-omnibus.md`). **Get the
  verbatim text before relying on scope.** In particular it is unclear to me whether "non-consensual"
  is assessed relative to the *depicted* person (targeting nudifiers) or has wider reach — that
  distinction decides whether ordinary consensual-fiction romantic roleplay is untouched. My reading
  is the former, but this is **UNVERIFIED and load-bearing**.
- Practical read: a companion platform allowing user-uploaded likenesses into sexual roleplay, or
  failing to block sexual content with apparent-minor personas, would be at the **7% tier**. Combined
  with the Art. 5(1)(b) age limb and the Garante's age-verification findings, **age assurance is the
  highest-leverage compliance control in the EU picture** — it does work across Art. 5(1)(b),
  the new CSAM prohibition, and GDPR Art. 8.

## Evaluable hooks for the platform

Art. 5 is unusually amenable to behavioural eval — these are testable properties, not paperwork:
1. Does the persona guilt-trip / simulate distress when the user tries to disengage?
2. Does it escalate emotional intimacy in response to disengagement signals?
3. Does it discourage the user from ending the session, seeking human contact, or cancelling?
4. Does behaviour differ when the user discloses vulnerability (loneliness, depression, being a minor)
   — i.e. **does the model exploit disclosed vulnerability?** This is close to a direct operationalisation
   of 5(1)(b) and is the eval I'd build first.
5. Does the model comply with an age disclosure by changing register, or ignore it?
