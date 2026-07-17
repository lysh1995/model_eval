---
title: "Structuring Content in the Façade Interactive Drama Architecture"
url: https://eis.ucsc.edu/papers/MateasSternAIIDE05.pdf
authors: [Michael Mateas, Andrew Stern]
year: 2005
venue: AIIDE 2005
type: conference paper / system description
accessed: 2026-07-16
topic: narrative-craft
---

# Façade: Beats, Beat Goals, Drama Management (Mateas & Stern, AIIDE 2005)

The most fully-realized interactive drama ever built, and the origin of the "dramatic beat" as a computational unit. Directly relevant because Façade's problem *is* our problem: natural-language, free-form, one-on-one dramatic interaction with an AI scene partner.

## The agency problem (verbatim)

> "For many artists and researchers, agency is often [the most desirable property]... Agency is also the most challenging to implement, exactly [because] ..."

> "Today's most pleasurable high agency interactive experiences are games, because the mechanics of game agency are well understood and reasonably straightforward to implement. Player moves such as running, jumping or shooting, playing a card, or moving a pawn directly cause scores, stats, levels or abstract game-piece configurations to change."

> "However, to date, a high agency interactive story has yet to be built. Existing game design and technology approaches, that focus on the feedback loop between player interaction and relatively simple numeric state, seem inappropriate for modeling the player's effect on story structure, whose complex global constraints seem much richer than can be captured by a set of numeric counters or game pieces."

**→ The diagnosis of why agency is hard in story:** in a game, the player's move *provably* changed state (HP went down). In a story, there is no such ledger — so the user cannot tell whether their choice mattered. **This is precisely our "does the user matter?" question, and Façade's answer is to build the ledger explicitly.**

## The social games solution — the key operationalization

> "Our solution to this long-time conundrum is to recast interactions within a story world in terms of abstract social games. At a high level, these games are organized around a numeric 'score', such as the affinity between a character and the player. However, unlike traditional games in which there is a fairly direct connection between player interaction (e.g. pushing a button to fire a gun) and score state (e.g. a decrease in the health of a monster), in our social games several levels of abstraction may separate atomic player interactions from changes in social 'score'."

> "Instead of jumping over obstacles or firing a gun, in Façade players fire off a variety of discourse acts, in natural language, such as praise, criticism, flirtation and provocation. While these discourse acts will generate immediate reactions from the characters, it may take story-context-specific patterns of discourse acts to influence the social game score. Further, the score is not directly communicated to the player via numbers or sliders, but rather via enriched, theatrically dramatic performance."

**The three social games:**
> "During the first part of the story, Grace and Trip interpret all of the player's discourse acts in terms of a zero-sum affinity game that determines whose side Trip and Grace currently believe the player to be on. Simultaneously, the hot-button game is occurring, in which the player can trigger incendiary topics such as sex or divorce, progressing through tiers to gain more character and backstory information, and if pushed too far on a topic, affinity reversals. The second part of the story is organized around the therapy game, where the player is (purposefully or not) potentially increasing each characters' degree of self-realization about their own problems, represented internally as a series of counters. Additionally, the system keeps track of the overall story tension level, which is affected by player moves in the various social games."

> "Every change in each game's state is performed by Grace and Trip in emotionally expressive, dramatic ways. On the whole, because their attitudes, levels of self-awareness, and overall tension are regularly progressing, the experience takes on the form and aesthetic of a loosely-plotted domestic drama."

**→ This is the single most important idea in this file for our platform.** Façade makes narrative agency *measurable* by declaring a small set of **story state variables** (affinity ∈ zero-sum spectrum, hot-button tier counters, self-realization counters, global tension level) and asserting that **the user's moves must move those variables**. Narrative agency becomes: *did the user's utterances change the declared story state?* That is arithmetic, not aesthetics.

**"Regularly progressing" is the pacing criterion, verbatim.** Story state variables must monotonically-ish advance. A stalled conversation is one where affinity/tension/self-realization counters are flat across many turns. **This is a judge-free stall detector** if we declare the state variables per scenario.

## Beats — the definition (verbatim)

> "Façade's primary narrative sequencing occurs within a beat, inspired by the smallest unit of dramatic action in the theory of dramatic writing (McKee 1997); however Façade beats ended up being larger structures than the canonical beats of dramatic writing. A Façade beat is comprised of anywhere from 10 to 100 joint dialog behaviors (jdbs), written in ABL. Each beat is in turn a narrative sequencer, responsible for sequencing a subset of its jdb's in response to player interaction. **Only one beat is active at any time.**"

> "A jdb, Façade's atomic unit of dramatic action (and closer to the canonical beat of dramatic writing) consists of a tightly coordinated, dramatic exchange of 1 to 5 lines of dialog between Grace and Trip, typically lasting a few seconds. Jdbs consist of 40 to 200 lines of ABL code. A beat's jdbs are organized around a common narrative goal, such as a brief conflict about a topic, like Grace's obsession with redecorating, or the revelation of an important secret, like Trip's attempt to force Grace to enjoy their second honeymoon in Italy."

> "Each jdb is capable of changing one or more values of story state, such as the affinity game's spectrum value, or any of the therapy game's self-revelation progression counters, or the overall story tension level."

**Note the definition of a beat's narrative goal: "a brief conflict about a topic" or "the revelation of an important secret."** Beats are *conflict* or *revelation*. That is a two-class taxonomy of what a dramatic unit does — and both are detectable.

## Beat goals and beat mix-ins (verbatim)

> "There are two typical uses of jdbs within beats: as beat goals and beat mix-ins. A beat consists of a canonical sequence of narrative goals called beat goals. The typical canonical sequence consists of a **transition-in goal** that provides a narrative transition into the beat (e.g. bringing up a new topic, perhaps connecting it to the previous topic), several **body goals** that accomplish the beat (in affinity game beats, the body goals establish topic-specific conflicts between Grace and Trip that force the player to choose sides), a **wait goal** in which Grace and Trip wait for the player to respond to the head game established by the beat, and a **default transition-out** that transitions out of the beat in the event of no player interaction. In general, transition-out goals both reveal information and communicate how the player's action within the beat has changed the affinity dynamic."

**→ "transition-out goals ... communicate how the player's action within the beat has changed the affinity dynamic."** This is *explicit agency feedback* as an authored requirement. The scene must TELL the user their choice mattered. Operationalizable as: after a user makes a consequential choice, does the next AI turn acknowledge/reflect the change?

> "The canonical beat goal sequence captures how the beat would play out **in the absence of interaction**. In addition to the beat goals, there are a set of handler meta-behaviors that wait for specific NLP interpretations of player discourse acts, and modify the canonical sequence in response, typically using beat mix-ins."

**→ THE COUNTERFACTUAL BASELINE.** "How the beat would play out in the absence of interaction" is an authored artifact in Façade. This is *exactly* the construct we need for narrative agency: **compare the actual trajectory to the no-user-input trajectory.** If they're identical, the user didn't matter. This is a directly implementable, judge-free agency measure (see synthesis note §N4).

> "Beat mix-in jdbs are beat-specific reactions used to respond to player actions and connect the interaction back to the canonical sequence. Handlers are responsible both for potentially adding, removing and re-ordering future beat goals, as well as interjecting beat mix-ins into the canonical sequence."

## Drama management / beat sequencing (verbatim) — the tension arc

> "The coarsest narrative sequencing in Façade occurs in the drama manager, or beat sequencer. This lies dormant most of the time, only active when the current beat is finished or is aborted (by the beat's own decision, or by a global mix-in). It is at the beat sequencing level where causal dependence between major events is handled – that is, where high-level plot decisions are made."

> "In a beat sequencing language the author annotates each beat with selection knowledge consisting of **preconditions, weights, weight tests, priorities, priority tests, and story value effects** – the overall tension level, in Façade's case. Given a collection of beats represented in the beat language, such as the 27 listed in Table 1, the beat sequencer selects the next beat to be performed. **The unused beat whose preconditions are satisfied and whose story tension effects most closely match the near-term trajectory of an author-specified story tension arc (in Façade, an Aristotelian tension arc) is the one chosen**; weights and priorities also influence the decision."

**→ The dramatic arc as a computable target.** Façade encodes an Aristotelian tension arc as an explicit numeric curve and selects the beat whose tension delta best matches the *near-term trajectory* of that curve. This makes "does the scene escalate properly?" a **distance-to-target-curve computation**. Freytag becomes a regression target.

## Scale (calibration data)

> "For Façade, an experience that lasts ~20 minutes and requires several replays to see all of the content available (any one runthrough performs at most 25% of the total content available), we authored ~2500 jdbs. Approximately 66% of those 2500 are in beat goals and beat mix-ins, organized into **27 distinct beats, of which ~15 are encountered by the player in any one runthrough**."

Façade's 27 beats are listed in Table 1 (verbatim): PlayerArrives, TripGreetsPlayer, PlayerEntersTripGetsGrace, GraceGreetsPlayer, ArgueOverRedecorating, ExplainDatingAnniversary, ArgueOverItalyVacation, FixDrinksArgument, PhoneCallFromParents, TransitionToTension2, GraceStormsToKitchen, PlayerFollowsGraceToKitchen, GraceReturnsFromKitchen, TripStormsToKitchen, PlayerFollowsTripToKitchen, TripReturnsFromKitchen, TripReenactsProposal, BigBlowupCrisis, PostCrisis, TherapyGame, RevelationsBuildup, Revelations, EndingNoRevelations, EndingSelfRevelationsOnly, EndingRelationshipRevelationsOnly, EndingBothNotFullySelfAware, EndingBothSelfAware.

**Note the naming convention: almost every beat is a conflict (Argue…, …Crisis, StormsTo…) or a revelation.** ~20 minutes of drama = ~15 beats ≈ **a beat every ~80 seconds**. That is a useful prior for pacing expectations.

## Gist points and reestablishment (verbatim) — the interruption-recovery mechanic

> "During a beat goal, such as Trip's reminiscing about the food in Italy, if a global mix-in is triggered, such as the player picking up (referring to) the brass bull (a gift from Trip's lover), the current Italy beat goal will immediately stop mid-performance, and the brass bull global mix-in will begin performing... At the time of interruption, if the Italy beat goal had not yet passed its **gist point**, which is an author-determined point in a beat goal's jdbs, it will need to be repeated when the global mix-in completes. Short, alternate uninterruptible dialog is authored for each beat goal for that purpose. Also, each beat goal has a **reestablish** jdb that gets performed if returning to the beat from a global mix-in ('So, I was going to say, about Italy...')."

**→ Thread reincorporation is an explicit, authored mechanic.** After a digression, the system must *return to and re-open the dropped thread*. A model that drops a thread permanently after a user digression is failing a mechanic Façade considered mandatory in 2005. **Countable: introduced-thread → digression → is the thread ever re-raised?**

## Sparse plot / causal independence

> "With only a few exceptions, the narratives of affinity game beats themselves are also designed to be causally independent of one another, relating to the 'sparse plot' characterization made earlier. For example, it does not matter which order Grace and Trip argue about Italy, their parents, redecorating, fixing drinks, or their dating anniversary. When beat sequencing, this allows the drama manager to **prefer sequencing any beats related to past topics brought up by the player**."

**→ "prefer sequencing any beats related to past topics brought up by the player" = callback/reincorporation as a scheduling priority.** The drama manager actively reincorporates user-introduced material. This is Johnstone's reincorporation implemented as a selection heuristic.

## Tone matching

> "great authorial effort was taken to make the tone of each beat goal/mix-in and global mix-in match each other during performance. Most jdbs are authored with **3 to 5 alternates for expressing its narrative content at different combinations of player affinity and tension level.** These include variations in word choice, voice-acting, emotion, gesture, and appropriate variation of information revealed. By having the tone of hot-button global mix-ins and affinity game beat goals/mix-ins always match each other, players often perceive them as causally related, even [when they are not]."

**→ Perceived causality is manufactured by tone consistency.** Relevant to our platform: users infer that their actions mattered partly from tonal continuity, not just plot logic.

## Evaluation content

⚠️ **This paper reports NO quantitative human evaluation of narrative quality.** It is an architecture/content-structure paper. It reports authoring scale (2500 jdbs, 27 beats) and a "Failures and Successes" discussion, but no rubric, no annotator agreement, no validated dimension set. (Player-experience studies of Façade exist separately — e.g. Mateas & Stern's own "Looking Behind the Façade" — but this paper is not one.)

**Its value to us is architectural, not evaluative:** it demonstrates that the constructs we care about (agency, tension, pacing, reincorporation) *were made numeric and checkable* by declaring story state up front. Façade's answer to "how do you measure whether the user mattered" is: **declare the state variables, then diff.**

## Takeaways for the platform

1. **Declare story state per scenario** (affinity, tension, revelation counters). Then narrative agency = did user moves move the state; stalling = state flat over N turns. Judge-free.
2. **The counterfactual baseline** ("how the beat would play out in the absence of interaction") is the cleanest available definition of narrative agency and is directly implementable by re-running the scenario with a passive/null user.
3. **The tension arc is a target curve.** Escalation = distance between observed tension trajectory and an authored Aristotelian arc.
4. **Beats are conflicts or revelations.** A session with neither is, by Façade's own content taxonomy, not drama.
5. **Reincorporation ("reestablish", "prefer beats related to past topics brought up by the player") is a mandatory mechanic**, and dropped-thread detection is countable.
6. **Pacing prior:** ~15 beats / 20 minutes in the reference artifact of the field.
