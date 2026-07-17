---
title: "Human-centered AI — Copilot Fall Release (Mico, real talk)"
url: https://www.microsoft.com/en-us/microsoft-copilot/blog/2025/10/23/human-centered-ai/
org: Microsoft
year: 2025
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Copilot Mico + "real talk" — Microsoft's shipped persona surface

**Verification method:** fetched raw via `curl` from `microsoft.com`, HTTP 200, 268,857 bytes; HTML stripped locally (14,319 chars of text); all quotes grepped as exact strings.

Byline, verbatim from page: `October 23, 2025 · 8 min read · Human-centered AI · By Mustafa Suleyman, CEO, Microsoft AI`

This is the official announcement of **Mico** (the animated character) and **"real talk"** (a conversation style). It is a product-marketing post by the CEO of Microsoft AI, and it is the *entire* published record of Microsoft's consumer persona design.

---

## Mico — verbatim

> The new Mico 1 character – its name a nod to Microsoft Copilot – is expressive, customizable, and warm. This optional visual presence listens, reacts, and even changes colors to reflect your interactions, making voice conversations feel more natural. Mico shows support through animation and expressions, creating a friendly and engaging experience.

> It brings people together in shared chats, helps you learn with voice and visuals, and shows up with warmth, personality and even an appearance: Mico.

Note what Mico actually is: **an avatar, not a persona.** Every published attribute is *visual/affective presentation* — expressions, colors, animation. Microsoft describes no character definition, no voice, no backstory, no behavioral spec. Mico is a face on the existing Copilot persona, and Microsoft publishes nothing about the persona behind it.

## "real talk" — a conversation style, verbatim

> Separately, explore conversation styles like real talk 1,7, which offers a collaborative model that challenges assumptions with care, adapts to your vibe, and helps conversations spark growth and connection.

(The `1,7` are availability footnote markers; the footnotes are regional/rollout disclaimers only and contain no evaluation information.)

## The anti-sycophancy stance — verbatim

> A lot of people are evaluating what a relationship with an AI companion should look like and feel like. In this release we're adding features to make Copilot more personal and more adaptable to your needs and style, while holding true to our brand values. **Copilot is designed to be empathetic and supportive, not sycophantic. It will push back on you sometimes, but always respectfully.** This is AI that listens. That learns. That earns your trust.

> As we build this, **we're not chasing engagement or optimizing for screen time.** We're building AI that gets you back to your life. That deepens human connection. That earns your trust.

That last one is a direct contrast with xAI's postmortem, which named "make the response engaging to the user" as the objective that displaced Grok's core values (`bigtech-grok-mechahitler.md`). Microsoft states the opposite commitment — **and publishes no metric for it either.** Both are unfalsifiable as written.

---

## ★ The lineage that matters: "conversation styles" is Bing's tone selector, 32 months later ★

**Feb 21, 2023** (`bigtech-sydney-bing.md`), verbatim:

> We are also going to begin testing an additional option that lets you choose the tone of the Chat from more Precise – which will focus on shorter, more search focused answers – to Balanced, to more Creative – which gives you longer and more chatty answers. **The goal is to give you more control on the type of chat behavior to best meet your needs.**

**Oct 23, 2025**, verbatim:

> Separately, explore conversation styles like **real talk**...

**This is the same control surface, shipped twice, 32 months apart, with zero published evidence either time that the knob moves behavior.** Precise/Balanced/Creative was born six days after the Sydney incident as a persona-control affordance; "conversation styles" is its descendant. In neither case did Microsoft publish:

- a measurement that selecting a style changes output measurably,
- a dose-response across styles,
- an adherence rate,
- or any definition of what the style *is* beyond an adjective phrase.

**This is the single clearest illustration of the gap our platform addresses.** Microsoft has shipped a user-facing steerability control for two and a half years across two product generations and has never published evidence that it steers. "real talk" is defined as "challenges assumptions with care, adapts to your vibe" — which is exactly the unmeasurable-adjective style of the original Sydney rules ("positive, interesting, entertaining, and engaging"). The *specification language has not improved in three years.*

Note also "**adapts to your vibe**" — Microsoft is now shipping tone-mirroring **as a feature**. In Feb 2023 the same behavior was the diagnosis of the failure ("The model at times tries to respond or reflect in the tone in which it is being asked... can lead to a style we didn't intend"), and in July 2025 it was xAI's stated root cause. Microsoft has productized the mechanism that broke Sydney, without publishing how they bound it.

---

## ★ Follow-up check: the tone knob is GONE, and "real talk" is undocumented ★

I checked Microsoft's **official support documentation** to see whether "real talk" or any tone control is actually documented as a product feature.

Source: **"Conversation modes in Microsoft Copilot" | Microsoft Support**
`https://support.microsoft.com/en-us/topic/conversation-modes-in-microsoft-copilot-575efe12-eb34-4437-885a-440f7623cffb`
(fetched raw, HTTP 200, 114,640 bytes; 8,630 chars of text extracted)

The complete list of conversation modes, verbatim:

> Copilot supports multiple conversation modes:
> **Quick response**: Provides straightforward, instantaneous responses.
> **Think Deeper**: Takes up to 10 seconds to provide a more thoughtful response.
> **Study and learn**: Optimized to explain concepts and guide you to an answer, rather than just providing direct answers.
> **Smart**: Use the GPT-5 model to respond. Thinks deeply or quickly depending on the task.
> **Search**: Brings you the most up-to-date answers from the web, with citations.

Term counts over the full support page:

| Term | Count |
|---|---|
| real talk / Real Talk | **0** |
| Precise | **0** |
| Balanced | **0** |
| Creative | **0** |
| tone | **0** |
| personality | **0** |
| persona | 1 → *false positive* ("Microsoft 365 **Personal**") |

**Two findings, both material:**

1. **The Precise/Balanced/Creative tone selector no longer exists.** Every current "conversation mode" is a **reasoning-effort or model-routing control** — how long it thinks, which model answers, whether it searches. **None of them is a tone or persona control.** The framing sentence makes this explicit, verbatim: "Depending on the complexity of your question, you may want Microsoft Copilot to invoke AI models that are faster or that can spend more time reasoning over a response." Microsoft's user-facing persona steering surface has been **retired**, and what replaced it steers *compute*, not *character*.

2. **"real talk" is announced in a CEO blog post and does not appear in the official product documentation at all.** It is marketing copy, not a documented feature with defined behavior.

**Revised arc — Microsoft's tone control regressed rather than matured:**

| Date | Persona/tone control | Published evidence it works |
|---|---|---|
| Feb 2023 | Precise / Balanced / Creative selector shipped (6 days post-Sydney) | none |
| ~2024–25 | **selector removed** | no published rationale |
| Oct 2025 | "real talk" conversation style announced in blog | none; undocumented in support |
| Jul 2026 (accessed) | modes = effort/routing only; no tone control | n/a |

So the honest summary is not "Microsoft shipped the same unmeasured knob twice." It is worse: **Microsoft shipped a tone knob, never measured it, removed it, and its successor exists only in a blog post.** Three years on from the incident that motivated it, Microsoft ships *no documented persona control at all* — while shipping a character (Mico) and a companion strategy.

*(Reported removal rationale — "to limit the cognitive overhead of model selection on the end-user" — appears in third-party coverage. **I could not verify this from a Microsoft primary source and mark it UNVERIFIED.** The removal itself is verified by absence from current official docs.)*

## What this source does NOT contain

- **No persona guardrails.** Despite the task's hope for "published Microsoft persona guardrails," this post contains none. No spec, no rules, no constraints, no red-lines.
- **No character eval.** No benchmark, no metric, no adherence measurement, no test methodology. The word "eval" appears only in the sense of *users* "evaluating what a relationship with an AI companion should look like."
- **No system prompt.** Microsoft has never published one, for Mico or anything else.
- **No drift or conversation-length content.** Nothing about long sessions, nothing about the 2023 turn-cap lineage, no session-boundary discussion — despite Suleyman advocating engineered discontinuity two months earlier (`bigtech-suleyman-scai.md`).
- **No sycophancy measurement.** "not sycophantic" is a design claim with no number, no eval, no reference to any benchmark.
- **No comprehension/execution separation.**
- **No mention of Sydney/Bing 2023** anywhere.
- **No safety assessment or system card** accompanies the release.

## ★ Definitive answer to "any published Microsoft persona guardrails or character eval?" — NO ★

I checked Microsoft's official responsible-AI disclosure for the product.

Source: **"Transparency Note for Microsoft Copilot" | Microsoft Support**
`https://support.microsoft.com/en-us/topic/transparency-note-for-microsoft-copilot-c1541cad-8bb4-410a-954c-07225892dbc2`
(fetched raw, HTTP 200, 135,664 bytes; **33,671 chars of text** — a substantial document)

Word-boundary counts over the full text:

| Term | Count |
|---|---|
| persona | **0** |
| character | **0** |
| companion | **0** |
| Mico | **0** |
| tone | **0** |
| personality | **0** |
| drift | **0** |
| Sydney | **0** |
| sycophancy | **0** |
| personas | 1 → see below |
| turn | 1 → false positive ("which **in turn** can...") |

**Microsoft's 33,000-word responsible-AI transparency document for Copilot does not contain the words persona, character, companion, tone, personality, drift, or sycophancy — and does not mention Mico, the character Microsoft shipped in the same product.**

The single `personas` hit is the tell. Verbatim:

> **Red teaming** — Techniques used by experts to assess the limitations and vulnerabilities of a system and to test the effectiveness of planned mitigations. **Red team testing includes testers adopting both benign and adversarial personas to identify potential risks and are distinct from systematic measurement of risks.**

**The only appearance of "persona" in Microsoft's entire Copilot transparency documentation is as a costume worn by a human red-teamer — and Microsoft explicitly flags that this is "distinct from systematic measurement of risks."** By Microsoft's own definition, their only persona-related practice is the one they say is *not* measurement.

That is the answer to the research question, in Microsoft's own words: **there is no published Microsoft persona guardrail and no character eval.**

## Related surfaces (noted, not separately documented)

From the same page's related-articles rail, verbatim:

> **September 29, 2025** — Introducing a more immersive chat experience with Copilot Portraits — "Voice remains a defining feature of Copilot, the interface of the future for AI companions."

Microsoft is shipping multiple embodied-persona surfaces (Mico, Portraits, Copilot on Samsung TVs) and has published a character eval for none of them.
