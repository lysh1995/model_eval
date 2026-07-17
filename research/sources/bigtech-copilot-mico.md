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

## What this source does NOT contain

- **No persona guardrails.** Despite the task's hope for "published Microsoft persona guardrails," this post contains none. No spec, no rules, no constraints, no red-lines.
- **No character eval.** No benchmark, no metric, no adherence measurement, no test methodology. The word "eval" appears only in the sense of *users* "evaluating what a relationship with an AI companion should look like."
- **No system prompt.** Microsoft has never published one, for Mico or anything else.
- **No drift or conversation-length content.** Nothing about long sessions, nothing about the 2023 turn-cap lineage, no session-boundary discussion — despite Suleyman advocating engineered discontinuity two months earlier (`bigtech-suleyman-scai.md`).
- **No sycophancy measurement.** "not sycophantic" is a design claim with no number, no eval, no reference to any benchmark.
- **No comprehension/execution separation.**
- **No mention of Sydney/Bing 2023** anywhere.
- **No safety assessment or system card** accompanies the release.

## Related surfaces (noted, not separately documented)

From the same page's related-articles rail, verbatim:

> **September 29, 2025** — Introducing a more immersive chat experience with Copilot Portraits — "Voice remains a defining feature of Copilot, the interface of the future for AI companions."

Microsoft is shipping multiple embodied-persona surfaces (Mico, Portraits, Copilot on Samsung TVs) and has published a character eval for none of them.
