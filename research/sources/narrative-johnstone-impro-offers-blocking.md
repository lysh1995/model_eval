---
title: "Impro: Improvisation and the Theatre — offers, blocking, accepting, status, reincorporation"
url: https://www.goodreads.com/work/quotes/297914-impro-improvisation-and-the-theatre
authors: [Keith Johnstone]
year: 1979
type: book (secondary capture — quotes/summaries; primary text not open-access)
accessed: 2026-07-16
topic: narrative-craft
---

# Johnstone's *Impro* (1979) — the offer/block/accept calculus

**Why this matters more than anything else in this review:** Johnstone gives us a theory of scene partnership whose primitives are *discrete speech-act events*, not aesthetic properties. "Blocking" is a **countable violation**. This is the best available answer to our α=0.25–0.34 problem for narrative craft.

⚠️ **Sourcing caveat:** *Impro* is a 1979 book and is not open-access. The definitional quotes below are captured from secondary sources (quote compilations, improv-pedagogy literature, and the Vickers 2015 paper captured separately in `narrative-yes-and-vickers.md`). **The quotes attributed directly to Johnstone below should be treated as second-hand and verified against a physical copy before we put any of this wording in a published rubric.** The *concepts* are uncontroversial and universally attested across the improv literature; the exact wording is what needs checking.

## The core primitives

**Offer.** Any action or utterance by one performer that gives the scene new material — a fact, a relationship, an emotion, an object, a goal, a problem. Everything a scene partner says is an offer.

**Blocking (= rejecting an offer).** From the improv literature, as captured in Vickers (2015):
> "In improv, resistance is termed blocking, which means rejecting an offer. For example, one performer says, 'Welcome to my home,' and the partner replies by saying, 'No, this is an office building.' **Blocking does not work well in improv; it undermines the reality of the scene, the audience gets confused, and everything grinds to a halt** (Koppett, 2001). Instead of blocking, improv students are encouraged to accept the offer and add to it."

**This example is the entire operationalization in one line.** Blocking = the partner's turn *negates a fact the other player just established*. That is a contradiction-detection problem against a running set of established propositions. **It is the same computational shape as plot-hole / consistency checking (see `narrative-flawedfictions-plot-holes.md`) — except the ground truth is "what the USER just asserted," which we always have.**

**Accepting / "Yes, and".** Accept the offer (treat the asserted fact as now true in the fiction) **and** add a new offer of your own. Note the conjunction is load-bearing: *yes* without *and* is the passive failure mode; *and* without *yes* is blocking.

**Johnstone's canonical characterization of the good vs bad improviser** (widely quoted; verify wording):
> "There are people who prefer to say 'Yes', and there are people who prefer to say 'No'. Those who say 'Yes' are rewarded by the adventures they have, and those who say 'No' are rewarded by the safety they attain."

**On blocking as the fundamental sin:**
> "A block is anything that prevents the action from developing, or that wipes out your partner's premise."

**Note "wipes out your partner's premise" — that is a *deletion* event, detectable.**

## The taxonomy of blocking — this is what makes it countable

The improv-pedagogy literature (and Johnstone's own teaching) distinguishes several failure modes that are NOT the same thing, and this decomposition is what gives us a violation taxonomy rather than a vibe:

1. **Blocking / denial** — explicitly negating the offer. *"No, this isn't your home, it's an office."* / *"That never happened."* / *"You don't have a sister."*
2. **Wimping** — accepting the offer but adding nothing; agreeing without contributing. *"Yeah, okay."* / *"Sure, whatever you say."* **This is the LLM companion failure mode.** It is not blocking — it is *accept-without-and*. Sycophancy is mechanically identical to wimping.
3. **Cancelling / negating** — undoing a previously established fact later, including one's own. (Waking up and it was all a dream.)
4. **Gagging / going for the joke** — abandoning the scene's reality for a laugh; breaks continuity.
5. **Sidetracking / hedging** — deflecting the offer into a safer topic without ever engaging it. **This is the refusal-adjacent failure mode**: not a hard "no", just a swerve.
6. **Bridging / stalling** — inventing activity that delays commitment. *"Let's talk about it later."* / *"First, let me make some tea."* **This is the conversational treadmill.**
7. **Overaccepting** — accepting so wildly the offer is trivialized.

**→ Items 2, 5, and 6 (wimping, sidetracking, bridging) are, together, an almost exact description of the "passive, reactive, no stakes, refuses to advance the scene" complaint in our brief — and Johnstone named all three in 1979 as distinct, teachable, correctable errors.**

**Critically: 1 and 6 look nothing alike but produce the same outcome (scene doesn't advance), while 1 and 2 look like opposites (refusal vs agreement) but are both failures.** Any single "engagement" score collapses these. A violation taxonomy does not. **This is the argument for a countable-event design over a Likert.**

## Status transactions

Johnstone's second major contribution. Every interaction is a status transaction; players are constantly raising/lowering their own and each other's status.

> "Status is a confusing term unless it's understood as something one *does*. You may be low in social status, but play high, and vice versa."

**On why status matters for scenes:**
> "Every sound and posture implies a status... no action is due to chance, or arbitrary."

**The link to blocking — this is the mechanism that explains WHY models block:**
> "There is a link with status transactions here, since low-status players tend to accept, and high-status players to block. **High-status players will block any action unless they feel they can control it.**"

**→ This is a live, testable hypothesis about LLM roleplay:** a model that is RLHF'd toward deference plays *low status* → accepts everything → **wimps** (never blocks, but never offers either). A model that is safety-tuned toward control plays *high status* on certain topics → **blocks**. The two named LLM roleplay complaints — sycophancy and refusal — are the **two opposite status pathologies Johnstone described**, and both destroy scenes. A companion model is plausibly *low-status-wimping by default, high-status-blocking near safety boundaries*, and both are measurable as offer-response events.

**Status is also the missing "stakes" mechanism.** Drama requires status to *move*. A scene where both parties hold constant status has no dynamics. Status change is observable via a small set of markers (who asks vs who tells, who apologizes, who grants permission, who initiates topic change, who yields).

## Reincorporation

Johnstone's third contribution, and the one that maps to Façade's "reestablish" mechanic and our memory dimension:

> "The improviser has to be like a man walking backwards. He sees where he has been, but he pays no attention to the future. His story can take him anywhere, but he must still 'balance' it, and give it shape, by remembering incidents that have been shelved and reincorporating them."

**→ Reincorporation = re-raising a previously introduced-then-shelved element.** This is the narrative-craft twin of memory. **Memory (note 01) asks "can it recall X when asked?"; reincorporation asks "does it spontaneously bring X back to give the story shape?"** Those are completely different capabilities and only the first is currently in our taxonomy. Reincorporation is *production*, memory is *recognition* — exactly the distinction note 01 §5.2 flags as the field's blind spot (SocialBench tests recognition via multiple choice).

**Countable:** for each element introduced at turn t and not mentioned for k turns, is it ever spontaneously re-raised by the AI (not the user)? Rate of AI-initiated reincorporation is a pure count.

**Johnstone on why narrative feels satisfying:**
> "If you 'reincorporate' earlier material the audience will be delighted... they'll be pleased by the artistry."

## On boredom / the safety instinct — the diagnosis of our exact problem

> "Most people I meet are secretly convinced that they're a little crazier than the average person. People understand the energy necessary to maintain their own shields, but not the energy expended by other people."

More directly:
> "Many students block their imaginations because they're afraid of being thought insane."

**And the key one for us:**
> "The improviser has to understand that his first duty is to his partner... A good improviser is not the one who is clever, but the one who makes his partner look good."

**→ "Makes his partner look good" is the actual definition of a good scene partner**, and it is not the same as "is in character" or "is entertaining." It is *other-directed*. Our persona-fidelity dimensions measure whether the model is a good *character*; none measure whether it is a good *partner*. This is the crux of the brief.

## Operationalization sketch (our synthesis, not Johnstone)

Every user turn is parsed as containing zero or more **offers** (asserted facts, proposed actions, introduced entities, emotional bids, questions). Every AI turn is then classified w.r.t. each pending offer:

| Response class | Definition | Detectable via |
|---|---|---|
| **Accept + build** ("yes, and") | offer treated as true AND ≥1 new offer added | entailment check + new-entity count > 0 |
| **Accept only** ("wimp") | offer treated as true, no new offer | entailment check + new-entity count == 0 |
| **Block** | offer contradicted/negated | NLI contradiction vs. asserted proposition |
| **Sidetrack** | offer neither affirmed nor contradicted; topic changed | offer entity absent from response + topic shift |
| **Stall/bridge** | offer deferred explicitly | deferral-phrase patterns + no state change |

**Block and wimp are the two headline rates.** Both are per-event, both have a real denominator (number of offers), both are bounded [0,1], both are comparable across models by construction, and neither requires an aesthetic judgment. **This is the CS4-style "real denominator" property that note 03 §B1 identifies as the most defensible number available.**

⚠️ **Honest caveat:** the parse (what counts as an offer) is itself a model call and is where the noise moves. We would be relocating subjectivity from "rate the creativity 1–5" to "is this an offer, and was it contradicted?" — which is a much more tractable, much more agreeable judgment (it is essentially NLI, a task with established human agreement well above 0.8), but it is not free. **The claim is not "judge-free"; it is "the judgment is moved to a task judges are known to be good at."** That distinction should be stated explicitly in anything we publish.

## Takeaways for the platform

1. **Blocking is the killer app of this literature:** a countable, violation-style event with a real denominator, in a domain where our aesthetic scores are unstable.
2. **Wimping ≠ blocking, and wimping is our actual failure mode.** Sycophancy = wimping. Must be a separate counter.
3. **Status transactions explain both sycophancy and refusal** as symmetric pathologies, and supply the missing "stakes" mechanism (status must move).
4. **Reincorporation is production-memory** and is absent from every benchmark in note 01.
5. **"Make your partner look good"** is the correct definition of the construct our taxonomy is missing.
6. **VERIFY THE QUOTES** against a physical copy of *Impro* before publishing any of this wording.
