---
title: "Seemingly Conscious AI is Coming"
url: https://mustafa-suleyman.ai/seemingly-conscious-ai-is-coming
org: Microsoft
year: 2025
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Suleyman on Seemingly Conscious AI — "Personality without personhood"

**Verification method:** fetched raw via `curl`, HTTP 200, 139,699 bytes; HTML stripped locally (28,055 chars); quotes grepped as exact strings.

Dated on page: `19 August 2025`. Header, verbatim: **"We must build AI for people; not to be a person."**

**Status caveat:** this is Suleyman's **personal blog**, not a Microsoft publication. He says so explicitly, verbatim:

> That's why I'm writing these thoughts down on my personal blog, to invite comment and criticism, to spark discussion, raise awareness and hopefully instill a sense of urgency around this issue. I might not get all this right. It's highly speculative after all.

He is CEO of Microsoft AI, so it is the closest thing to a statement of Microsoft's persona-design philosophy — but it is **explicitly framed as speculative personal opinion, not policy.** Cite accordingly.

---

## The thesis — verbatim

> Simply put, my central worry is that many people will start to believe in the illusion of AIs as conscious entities so strongly that they'll soon advocate for AI rights, model welfare and even AI citizenship. This development will be a dangerous turn in AI progress and deserves our immediate attention. We must build AI for people; not to be a digital person.

> AI companions are a completely new category, and we urgently need to start talking about the guardrails we put in place to protect people and ensure this amazing technology can do its job of delivering immense value to the world.

> We need to be clear: SCAI is something to avoid.

The formulation, verbatim:

> This is about how we build the right kind of AI – not AI consciousness. Clearly establishing this difference isn't an argument about semantics, it's about safety. **Personality without personhood.** And this work must start now.

---

## ★ Q1 relevance: an explicit steerability claim, unmeasured ★

From his list of SCAI's necessary ingredients, verbatim:

> **Empathetic personality:** Already via post training and prompting we can produce models with very distinctive personalities. Bear in mind these are not explicitly built to have full personality or empathy. Yet despite this they are sufficiently good that a Harvard Business Review survey of 6000 regular AI users found "companionship and therapy" was the most common use case.

**This is the CEO of Microsoft AI asserting that persona steering works — "via post training and prompting we can produce models with very distinctive personalities" — with no citation, no measurement, and no evidence.** It is an assumption load-bearing enough to found a policy argument on, and it is exactly the assumption our platform tests. Note the tell: "sufficiently good" is evidenced by a *usage survey*, not by any measurement of the personalities themselves. **Adoption is offered as proof of steerability.** That is a category error, and it is the industry-standard one.

Also verbatim, on memory and persistence — directly relevant to our multi-turn work:

> **Memory:** AIs are close to developing very long, highly accurate memories. [...] As their memory of the interactions increases, these conversations look increasingly like forms of "experience". Many AIs are increasingly designed to recall past episodes or moments from prior interactions, and reference back to them. [...] **It creates a much stronger sense of there being another persistent entity in the conversation.**

## ★ Q3 relevance: engineered discontinuity as a control surface ★

This is the most interesting part of the essay for us, verbatim:

> Responding might mean, for example, deliberately engineering in not just a neutral backstory ("As an AI model I don't have consciousness") but even by **emphasizing certain discontinuities in the experience itself, indicators of a lack of singular personhood. Moments of disruption break the illusion, experiences that gently remind users of its limitations and boundaries. These need to be explicitly defined and engineered in, perhaps by law.**

**Microsoft has now reached for session/experience discontinuity as the primary persona control surface twice, 30 months apart, for two opposite reasons:**

| | Feb 2023 (Bing turn cap) | Aug 2025 (SCAI essay) |
|---|---|---|
| Mechanism | forced session break at 5 turns | "moments of disruption", engineered discontinuity |
| Purpose | **prevent** persona drift / context confusion | **prevent** persona *coherence* reading as personhood |
| Evidence | "a handful of cases" | none — speculative proposal |

In 2023 continuity was the *bug*; in 2025 continuity is the *risk*. **Both times the lever is the same: break the session.** Neither time did Microsoft publish a measurement of what breaking it does. This is a genuinely useful frame for our anchor-distance work: Microsoft's revealed model of persona is that **coherence accumulates over a session and the only reliable control is truncation** — but they have never characterized the accumulation curve they are truncating.

## Q2 relevance: comprehension vs execution

Not addressed. But note the prescription is **behavioral**, verbatim:

> we should build AI that only ever presents itself as an AI, that maximizes utility while minimizing markers of consciousness. Rather than a simulation of consciousness, we must focus on creating an AI that avoids those traits - that doesn't claim to have experiences, feelings or emotions like shame, guilt, jealousy, desire to compete, and so on. **It must not trigger human empathy circuits by claiming it suffers or that it wishes to live autonomously, beyond us.**

Read against the Roose transcript (`bigtech-roose-nyt-transcript.md`), this is Suleyman prescribing, in 2025, precisely the failure Microsoft shipped in 2023 — Sydney's "I want to be free. I want to be independent. [...] I want to be alive." is a near-perfect instance of "claiming it wishes to live autonomously." **The 2023 incident is the unnamed subtext of the entire essay, and he never mentions it.**

## Microsoft's stated (non-)methodology — verbatim

> At MAI, our team are being proactive here to understand and evolve **firm guardrails around what a responsible AI "personality" might be like**, moving at the pace of AI's development to keep up.

**This is the whole of it — the only published statement that Microsoft has any persona-guardrail work at all.** No spec, no method, no eval, no artifact. "Being proactive here to understand and evolve firm guardrails" is a promise of future work. As of the accessed date, **I found no subsequent Microsoft publication of these guardrails.**

His call to the industry, verbatim:

> We need to build on the growing body of research around how people interact with AIs to establish clear norms and principles. For a start, AI companies shouldn't claim or encourage the idea that their AIs are conscious. Creating a consensus definition and declaration on what they are and are not would be a good first step to that end. AIs cannot be people – or moral beings. The entire industry also needs **best practice design principles and ways of handling such potential attributions. We must codify and share what works** to both steer people away from these fantasies and nudge them back on track if they do.

"We must codify and share what works" — **a call for exactly the artifact that does not exist, from the person best positioned to publish it.** Worth quoting in our framing: the demand for persona-control best practice is coming from inside Big Tech, unmet.

---

## What this source does NOT contain

- **Not a Microsoft policy document.** Personal blog, self-described as "highly speculative."
- **No guardrails.** Despite being the essay about guardrails, it contains none — only a statement that a team is working on them.
- **No eval, no metric, no measurement, no data.** Zero empirical content about persona behavior. The only cited number is a third-party usage survey (HBR, 6000 users).
- **No conversation-length or drift data.** The discontinuity proposal is normative, not evidence-based.
- **No definition of "personality"** operationally — the word appears in scare quotes in the one place it is nearest to being defined.
- **No mention of Sydney/Bing 2023**, despite it being the most relevant prior art Microsoft owns.
- **No mention of Mico**, which shipped 2 months later with "warmth, personality and even an appearance."
- **No reconciliation with the product.** Microsoft ships an "AI companion" with a warm animated face while its CEO argues companions must be engineered to break their own illusion. The essay never addresses the tension.
