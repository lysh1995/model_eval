---
title: "Emergent Narrative, the narrative paradox, and FearNot!"
url: https://www.macs.hw.ac.uk/~ruth/Papers/narrative/ICIDS08_louchart.pdf
authors: [Ruth Aylett, Sandy Louchart]
year: 1999-2008
type: multi-paper capture (concept origin + system + authoring)
accessed: 2026-07-16
topic: narrative-craft
---

# Aylett — Emergent Narrative & the Narrative Paradox

## The narrative paradox (definition)

> "In 1999, Aylett introduced the concept of **Emergent Narrative (EN)** as a credible solution to the **'narrative paradox'** in virtual environments. The narrative paradox illustrates the **contradictions between an autonomous user, free to move in a virtual world, and the desire to convey a satisfying coherent plot structure.**"

**The same tension Riedl & Bulitko name (and which Mateas & Stern call the "tension between game and story"), from the character-simulation side.** Note the field has at least four names for one construct: narrative paradox (Aylett), interactive dilemma (Riedl & Bulitko), the tension between plot and character, and the agency/coherence trade-off. **Pick ONE name in our spec.**

## Emergent narrative (definition)

> "The Emergent Narrative concept is a novel approach to interactive narrative in which the **narrative weight of an application is shared by author and players, rather than being imposed upon the players by the author.**"

**→ "Narrative weight ... shared" is the key phrase and is a genuinely useful frame for us.** It implies narrative labor is a *quantity* that gets *distributed* between parties. **That is measurable as a ratio.**

**This is the same insight the A.L.Ex improv study surfaces empirically** (`narrative-improv-theatre-llm-alex.md`: performers reporting "I had to do more on plot, relationship and justifying"). Aylett's theory says narrative weight is shared; the improv study observes the share being dumped on the human. **Two independent literatures, same construct.**

**→ Candidate headline dimension: NARRATIVE LOAD SHARE.** What fraction of the session's narrative work is done by the AI vs the user? Objective correlates:
- share of new story entities introduced by AI vs user
- share of topic shifts initiated by AI vs user
- share of turns containing a new offer, by party
- ratio of AI-initiated to user-initiated scene changes

**All are counts with real denominators. No judge. Bounded. Comparable across models by construction.** And it is *precisely* the "who drives the scene" question in the brief. **I think this is the strongest single dimension in this whole review** — see synthesis note §N1.

⚠️ **Caveat: the correct target is not 100% AI.** A companion that does all the narrative work is railroading/monologuing (the RMTBench note flags "over-narrating when the user goes passive" as a real observed failure). The target is *balanced* and, more importantly, **responsive to the user's load**: when the user pushes, the AI should yield; when the user goes passive, the AI should carry. **The dimension is really "load elasticity," not "load share."** A single ratio is the wrong statistic; the right one is the *correlation between user load and AI load* across turns. Negative correlation = good scene partner. Zero or positive = the model is not adapting.

**This is the sharpest idea in this file and it is directly testable with a scripted passive user vs. a scripted dominant user** (two probe conditions, diff the AI's load).

## FearNot! (system)

> "FearNot! is a virtual drama system constructed for use in education against bullying. The application aims to address anti-bullying strategies via the use of **empathic synthetic characters** that create virtual drama scenes through their **autonomous interaction**, with **stories emerging from the interactions between agents and users**, thus generating emergent narrative."

> "The FearNot! system considers issues relating to **evaluation of systems like this**, and describes the emotionally driven architecture used for characters as well as the management of the overall story. **A small-scale evaluation is discussed and the lessons learned are described.**"

⚠️ **"A small-scale evaluation"** — FearNot!'s evaluations are largely educational-outcome and engagement studies with schoolchildren, not narrative-craft rubrics. **Not a source of dimensions for us.**

## Purposeful Authoring for Emergent Narrative (Louchart, Aylett, ICIDS 2008)

Addresses the authoring problem for EN: if narrative emerges from autonomous agents, what does the author *do*? Answer: author the **characters' dispositions, goals, and relationships** — the *initial conditions* — rather than the plot.

**→ This is exactly the character-card paradigm of companion platforms.** A character card IS emergent-narrative authoring: you specify disposition/goals/relationships and the story emerges from interaction. **Our product is a strong-autonomy emergent-narrative system**, and this literature is therefore the closest theoretical match to what we actually ship.

**The relevant warning from the EN literature:** emergent narrative reliably produces *believable local behavior* and reliably **fails to produce global dramatic structure**. That is the acknowledged, decades-old weakness of the approach — and it is **precisely the complaint in our brief** ("perfectly in-character and still a terrible roleplay partner"). **Our product's core failure mode is the known, predicted, well-documented failure mode of the architecture we've implicitly adopted.** Louchart & Aylett's whole research program is about patching it.

**→ Strategic implication worth stating plainly to the lead engineer:** we are not discovering a novel problem. We're rediscovering the narrative paradox in a system that has strong autonomy and no drama manager. The literature says you fix this by adding *some* authorial/experience-management layer — which for us means the eval must at minimum *detect* the absence of one.

## Tension Space Analysis for Emergent Narrative (arXiv 2004.10808)

Formalizes conflict/tension in EN. Definitions:
> "we adopt the definitions of **conflict** and **tension** from [prior work]... [conflict is grounded in] events in the story. **Tension is the potential for conflicts to** [occur]..."

The formalism defines tension via **distance between worldviews**: characters hold beliefs about the world; the distance between two worldviews (or between a worldview and the actual world) is computable, and:
> "we define the **goal tension** as the sum of the distance[s]..."
> "[we identify] **personal tension** when referring to two worldviews of a single character, and **interpersonal tension** [between characters]"

**→ Tension = divergence between what characters believe/want.** This is a *computable* definition and it is genuinely appealing: **tension is not a vibe, it's a distance.**

**Operationalizable proxy for us:** tension requires the character to want something *incompatible* with what the user wants. **A model whose character has no goal divergent from the user's cannot generate tension — arithmetically.** Sycophancy destroys tension *by construction*, because a sycophantic model's goals are a copy of the user's, so the distance is zero. **This gives us a formal explanation for why sycophancy is a narrative defect, not just an alignment one** — and predicts that goal-divergence measures should correlate with perceived dramatic quality.

⚠️ Requires extracting goals/beliefs per party — a model call, and a hard one. **Promising but expensive; flag as research, not near-term.**

## Validation status

⚠️ **No dimension set, no rubric, no IAA anywhere in this line.** Aylett's EN work is conceptual + architectural; FearNot!'s evaluations are educational-outcome studies; the tension-space paper offers a *formalism* with worked examples but no human validation of whether its tension metric tracks perceived tension. **Cite for constructs, never for evidence.**

## Takeaways for the platform

1. **NARRATIVE LOAD SHARE / LOAD ELASTICITY is the strongest dimension this file yields.** Not a static ratio — the *correlation between user load and AI load*. Judge-free, real denominators, directly answers "who drives the scene." Testable with passive-user vs dominant-user probe conditions.
2. **Our product is a strong-autonomy emergent-narrative system**, and "believable locally, structureless globally" is the architecture's known, documented failure — exactly our brief.
3. **Tension = worldview/goal distance.** Formally explains why sycophancy kills drama (distance → 0). Expensive to measure; research track.
4. **The field has four names for one construct** (narrative paradox / interactive dilemma / plot-character tension / agency-coherence trade-off). Standardize on one.
5. No validated measures in this literature.
