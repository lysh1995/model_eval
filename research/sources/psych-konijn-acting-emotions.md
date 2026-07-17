---
title: "Konijn, *Acting Emotions: Shaping Emotions on Stage* — task-emotion theory and the field study of professional actors"
url: https://library.oapen.org/handle/20.500.12657/35086
authors: Elly A. Konijn (Vrije Universiteit Amsterdam)
year: 2000
type: paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Konijn — the one large empirical test of what actors actually feel, and it contradicts the acting theories

**Sourcing note:** ⚠️ **Secondary capture. The full text is nominally open-access via OAPEN (Amsterdam University Press, 2000, 209pp, ISBN 9789053564448) but the OAPEN bitstream, DOAB, JSTOR and Project MUSE all returned HTTP 403 to automated retrieval on 2026-07-16.** Everything below is assembled from the publisher's description, the verified table of contents, and secondary summaries of the findings. **The paradigm is well-attested; specific numbers below are NOT verified against the primary and MUST be checked before publication.** This is the highest-value unverified source in the batch — someone should retrieve the PDF manually. Treat the sample sizes and percentages as *unknown*, not as reported here.

## Publication and structure

Publisher's framing:

> "Actors and actresses play characters such as the embittered Medea, or the lovelorn Romeo, or the grieving and tearful Hecabe. The theatre audience holds its breath, and then sparks begin to fly. **But what about the actor? Has he been affected by the emotions of the character he is playing? What's going on inside his mind?**"

> The work "bridges theory and practice through empirical research with professional actors from the Netherlands, Flanders, and America, addressing **'the age-old issue of double consciousness, the paradox of the actor who must nightly express emotions while creating the illusion of spontaneity.'**"

**Table of contents (verified):**
> "Acting Emotions: An American Context · The Paradox Considered · Acting Styles · Emotions and Acting · Imagination and Impersonation · Actors in Practice · Professional Actors Emotions and Performing Styles · Notes, References, Appendix"

Chapter 7 ("Professional Actors Emotions and Performing Styles") carries the field study:
> "Chapter 7 presents results of a survey of professional actors."

## Task-emotion theory — the paradigm

The core move is a **three-way partition of what is going on emotionally in an actor at the moment of performance**:

- **Character-emotions** — the emotions of the role: Medea's rage, Romeo's love. What the audience is meant to perceive.
- **Task-emotions** — the actor's *own*, real, felt emotions arising from **the task of performing**: nerves, concentration, tension, excitement, the thrill of executing well in front of people.
- **Private emotions** — the actor's offstage personal emotional life (the raw material Strasberg's affective memory draws on).

Definitions as captured from secondary sources:

> "Task emotions are emotions such as **nervousness, concentration and excitement** that actors experience during performance, as distinguished from character-emotions—the emotions of the characters they portray."

> "Task emotions… allow an actor to **perform, not just feel**."

Konijn's central theoretical claim:

> "Konijn suggested that **task-emotions can play a central part in portraying character-emotions on stage, and would seem to be useful for acting with conviction, but are not discussed in any of the accepted acting theories.**"

**Read that carefully. The claim is that the emotion that actually powers a convincing performance is the actor's real, felt emotion about *doing the job well* — and that none of the acting theories (Stanislavski, Strasberg, Meisner, Brecht, Diderot) even have a category for it.** The whole 250-year debate about whether the actor feels the character's emotions is, on Konijn's account, asking about the wrong emotion.

## The empirical findings

> "Konijn's study examined the experience of actors in the United States and the Netherlands before, during, and after playing an emotional scene onstage, with the goal of testing her 'task-emotion theory' of acting."

> "Only recently have the emotions of the actor on stage portraying character-emotions been looked at scientifically from a psychological perspective, and Konijn presented empirical results of a questionnaire drawing on answers from a wide sample of professional actors."

> "The research involved a large-scale field study of the emotions of professional actors, with the responses of Dutch and Flemish actors supplemented by responses from American actors."

**The two findings that matter most — both unverified, both devastating to identification theories if they hold:**

> "**The more negative the emotion of the character, the less likely the actor would report feeling that emotion onstage**, and **it did not matter whether the actors claimed they were trained to feel the emotions of their characters or trained to detach themselves from the emotions.**"

> "Konijn's evidence shows that theater spectators experienced **empathy and task emotions equally, but identificatory emotions hardly played a role.**"

The first is the killer. Two sub-claims:
1. **A negative relationship between character-emotion valence and actor felt-emotion.** The more anguished the role, the *less* the actor reports feeling it. Portrayal quality is not carried by felt congruence.
2. **Training paradigm did not moderate it.** Actors trained to *feel* (Method) and actors trained to *detach* (Brecht/technique) reported the same thing. **The thing that all the schools argue about made no measurable difference to what actors actually experience.** If true, the entire Adler/Strasberg/Meisner controversy is a dispute about vocabulary layered over an invariant underlying process.

Konijn's verdict on the inherited theory, per the publisher:

> The book "surveys various dominant acting styles and analyzes the current state of affairs regarding the psychology of emotions, uniting psychology of emotions with contemporary acting theories to conclude that **traditional acting theories are no longer valid for today's actor.**"

On where the historical positions sit:

> "Diderot in his 'Paradoxe sur le comedien' insisted that brilliant actors do not feel anything onstage, which resembles Bertolt Brecht's detached acting style, standing in opposition to method acting's empathy-oriented 'emotional reality.'"

## Implications for the L1→L2→L3 cascade

**Verdict: Konijn REFRAMES the question in a way that is bad for the cascade — she argues the layer we think is doing the work isn't the layer doing the work.**

1. **Task-emotion theory says performance is powered by a factor that is orthogonal to character comprehension entirely.** What makes a portrayal convincing is not the actor's grasp of Medea, nor the actor's feeling of Medea's rage, but the actor's *live, real, task-directed engagement* with executing the scene. **There is no L1 in this account at all.** The engine is at L2, and it runs on the performer's relationship to the task, not to the character.
2. **"It did not matter whether the actors claimed they were trained to feel… or trained to detach"** is a null result across the *exact* independent variable our framework cares about. The schools that order comprehension-first and the schools that order reactivity-first produce actors who report the same phenomenology. **If the ordering doesn't change the outcome for humans, our confidence that it's a real causal structure for models should drop.**
3. **The negative valence relationship inverts a naive cascade prediction.** A cascade would predict: understand the character deeply → feel/represent their state → portray it. Konijn finds the *hardest* character states (most negative) are the ones actors feel *least*, and those are typically the most acclaimed performances. Portrayal quality and internal-state congruence appear **anti**-correlated at the extremes.
4. **This gives us a hypothesis for LLM roleplay worth naming:** the model analogue of a task-emotion is whatever the model is actually optimising during generation — fluency, coherence, user-approval, instruction-adherence. Konijn's structure predicts **the quality of roleplay output is driven by the "task" pressure, not by any character representation**, and that character representation is a *product* the performance emits rather than a resource it consumes. That is directly at odds with L1 being causally upstream. It also predicts sycophancy-shaped failures (task pressure = please the user) should look like *character* failures — which is exactly what `safety-elephant-social-sycophancy.md` and `safety-syceval.md` describe.
5. **Konijn is the strongest single empirical challenge in this batch, and she is the source we could not verify.** Do not cite the numbers until someone retrieves the PDF. But the *structure* of the argument (three-way emotion partition, task-emotion as the engine) is well-attested across the secondary literature and is safe to reason with.
6. **Retrieval note for whoever picks this up:** OAPEN handle 20.500.12657/35086, file 340262.pdf; JSTOR stable j.ctt46n1zd (listed as an OA monograph); Project MUSE review at article/37556. All 403 to scripted retrieval; a human browser session should work.
