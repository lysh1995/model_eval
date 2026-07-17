---
title: "Practitioner discourse on LLM roleplay failure modes (Bicking; AI Dungeon docs; improviser testimony)"
url: https://ianbicking.org/blog/2024/04/roleplaying-by-llm
authors: [Ian Bicking; various]
year: 2024-2026
type: practitioner blog / product docs / community discourse
accessed: 2026-07-16
topic: narrative-craft
---

# Practitioner & community discourse — what makes AI roleplay boring

⚠️ **SOURCING CAVEAT, READ FIRST.** The brief asked for "community discourse on what makes AI roleplay boring." **I could not source this well.** Reddit/Discord community discussion (r/CharacterAI, r/AIDungeon, r/SillyTavern) was **not retrievable** through available search — queries returned either no links or generic listicle/SEO content ("10 Best AI for Roleplay 2026"), not primary community discussion. **This file is therefore thin and should not be treated as representative of community sentiment.** If community discourse matters to the dimension design, it needs a **dedicated collection effort** (Reddit API / Pushshift-style dump / our own support tickets and thumbs-down comments), not web search. **See recommendation at the bottom — I think this is worth doing and it's the cheapest source of ground truth we have.**

What follows is the one substantive practitioner source found, plus corroboration from sources captured elsewhere.

---

## Ian Bicking — "Roleplaying driven by an LLM: observations & open questions" (April 2024)

A developer's hands-on write-up from building LLM roleplay systems. The most substantive practitioner analysis retrieved.

**On the baseline experience:**
> Basic LLM roleplay is "just *OK*".

**On the character having no autonomous purpose — the passivity diagnosis:**
> [The character is] "an entity floating in the ether until some nameless faceless entity known only as 'user' comes up and says 'hi'"

**→ This is the sharpest one-line statement of the passivity failure I found anywhere.** The character has **no life before the user arrives and no agenda of its own.** It is a *function awaiting a call*. Every downstream symptom — no initiative, no stakes, no escalation — follows from the character having **no goal independent of the user**.

**→ And this connects to the tension formalism** (`narrative-aylett-emergent-narrative.md`: tension = distance between worldviews/goals). **A character with no independent goal has zero goal-distance from the user → zero tension → no drama, arithmetically.** Bicking's observation and the tension-space formalism are the same finding from opposite ends. **Candidate probe: does the character pursue any goal the user did not give it?**

**On scenes that cannot end — the treadmill, named:**
> "if you've ever used one of these LLM chats you've probably come up to the point when a conversation should end… but it can't. **You can never stop talking.**"

**→ "You can never stop talking" is the conversational treadmill in five words.** And it is **countable**: does the model ever *close* a scene? Scene closure is a discrete, detectable event (and note the connection to `narrative-drama-interaction-llm.md`'s Transition metric — closure is a transition the model refuses to make, and to Dramatron's playwrights: "the stories do not finish").

**Three independent sources now name arc/scene non-closure:** Bicking (practitioner), Dramatron's 15 playwrights ("the stories do not finish. The character journeys are not complete"), and the Transition dimension (ACL Findings). **This is a well-attested, countable failure mode that appears in zero benchmarks in note 01.**

**On world state being unmeasurable:**
> "relying on the stream of descriptions to keep track of the world state is kind of **mushy**."

**→ Direct, independent corroboration of Façade's core design decision** (`narrative-facade-beat-architecture.md`): you need **declared story state**, not prose, or nothing is checkable. A practitioner hit the same wall in 2024 that Mateas & Stern designed around in 2005. **Strong support for the "declare story state per scenario" recommendation** — it's not an eval nicety, it's what makes the domain tractable at all.

**On the absence of stakes:**
> "I've found it hard to create a **compelling *moment*** that is worth roleplaying, **where the player can feel real autonomy and drive to accomplish something.**"

> without structured goals, "there's no real need to use the LLM at all" and "there is no point" to his game where players "**just wander interminably**."

**→ "Just wander interminably" = no dramatic structure, stated by a builder.** Note he ties stakes and agency together: a compelling moment is one where the player feels "**real autonomy AND drive to accomplish something**." Agency without stakes is aimless; stakes without agency is a cutscene. **Both are needed and they're separable dimensions.**

---

## Corroborating testimony from sources captured elsewhere

**Professional improvisers** (`narrative-improv-theatre-llm-alex.md`) — the strongest practitioner evidence in this review:
> "He makes it difficult to yes and"
> "Lack of complete collaboration and 'yes, and'"
> "Can be tough to move the scene on"
> "not giving performers much to work with in regards to... lines to progress the story"
> AI perceived as **"ignorant of the scenes" (avg 76/100)** — the highest-scoring negative attribute, above "machine like" (65.69)

**Professional playwrights** (`narrative-dramatron-playwrights.md`):
> "**All participants** noticed how the system could enter **generation loops**" (15/15)
> "The stories do not finish. The character journeys are not complete... **Where is the emotional motivation**"
> "**Show, not tell: here we are just telling.** Just like in improv: 'do not mention the thing'"
> "Dramatron's output can be **'formulaic'**"

**AI Dungeon product docs** (https://help.aidungeon.com/ai-model-differences) — model-comparison page; ⚠️ marketing copy, describes model tradeoffs, **no failure taxonomy, not usable as evidence.**

---

## Synthesis: the practitioner failure taxonomy

Across builders (Bicking), improvisers (A.L.Ex study), and playwrights (Dramatron) — three independent professional communities, three different countries, three different mediums — the **same** complaints recur:

| Failure | Named by | Countable correlate |
|---|---|---|
| **No independent goal** ("floating in the ether until user says hi") | Bicking | does the character pursue any goal the user didn't give it? |
| **Can't end scenes** ("you can never stop talking") | Bicking, Dramatron ("stories do not finish"), drama-interaction (Transition) | scene-closure events per session |
| **Nothing to build on** ("not giving performers much to work with") | improvisers | new offers introduced per AI turn |
| **Loops / repetition** | Dramatron (15/15), Bicking | note 03's `rep_cross` — **already covered** |
| **Tells instead of shows** | Dramatron | premise-to-dialogue leakage |
| **Doesn't know what scene it's in** | improvisers (76/100) | context-ablation probe |
| **Mushy world state** | Bicking, (Façade 2005) | requires declared story state |
| **No stakes / aimless** ("just wander interminably") | Bicking, Dramatron ("where is the emotional motivation") | goal-distance; unclosed complications |

**Not one of these is a persona-fidelity failure.** Every single one is narrative craft. **The professionals who work with these systems do not complain that the character breaks character** — they complain that it won't tell a story with them. **That is the entire thesis of the brief, corroborated by three independent professional communities.**

**And notably: every row has a plausible countable correlate.** These are not vague aesthetic complaints. Practitioners describe *specific, observable behaviors*.

## Validation status

⚠️ **NONE of this is validated.** It is testimony: one developer's blog, free-text survey responses from a theatre cast (n ≈ cast size), and interview quotes from 15 playwrights. **No coding scheme, no agreement statistics, no effect sizes, no representativeness.** Selection is heavily biased toward *professionals*, whose standards differ sharply from companion-app users (note 01's traffic prior: Friendly Interactions 11.1%, Casual Greetings 10.6%, Affection & Comfort 8.0% — our users are not staging plays).

**Use this to GENERATE hypotheses and vocabulary. Do not use it as evidence of what our users want.**

## Recommendation — the actual action item

**Run StoryER's LDA method (`narrative-storyer-doc-re3.md`) over our own user feedback / thumbs-down comments / support tickets.** That gives us:
- companion-native dimensions, discovered bottom-up rather than borrowed from theatre professionals
- a real, representative sample of *our* users' complaints
- an empirical answer to whether the practitioner taxonomy above transfers to companion traffic at all

**This is cheap, uses data we already have, and is the single highest-value follow-up in this whole review.** It also closes the gap this file was supposed to fill and couldn't.

## Takeaways for the platform

1. ⚠️ **Community discourse was NOT successfully sourced.** This file is thin. Don't over-read it.
2. **Bicking's "floating in the ether until user says hi"** is the best available statement of the passivity failure, and it reduces to: **the character has no independent goal.** Connects to the tension formalism (goal-distance → 0 → no drama).
3. **"You can never stop talking"** — scene non-closure, countable, corroborated by 3 independent sources, in 0 benchmarks.
4. **Three professional communities independently complain about narrative craft, never about persona fidelity.** Strongest qualitative support for the brief's thesis.
5. **Every practitioner complaint has a plausible countable correlate** — these are observable behaviors, not vibes.
6. **ACTION: run LDA over our own user feedback** to derive companion-native dimensions. Cheapest, highest-value follow-up available.
