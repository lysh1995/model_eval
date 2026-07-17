---
title: "Interactive Narrative: An Intelligent Systems Approach"
url: https://cs.uky.edu/~sgware/reading/papers/riedl2013interactive.pdf
authors: [Mark O. Riedl, Vadim Bulitko]
year: 2013
venue: AI Magazine 34(1)
type: survey / journal article
accessed: 2026-07-16
topic: narrative-craft
---

# Interactive Narrative: An Intelligent Systems Approach (Riedl & Bulitko, AI Magazine 2013)

The canonical framing paper for drama/experience management. Everything downstream (Façade, Mimesis, IDA, emergent narrative) is situated in its 3-axis landscape.

## Core definitions (verbatim)

**Interactive narrative:**
> "Interactive narrative is a form of digital interactive experience in which users create or influence a dramatic storyline through their actions."

**The central tension — this is the load-bearing quote for our platform:**
> "The core research challenge is how to balance the need for a coherent story progression with user agency, which are often at odds."

**Coherence, defined operationally:**
> "A coherent narrative experience is one in which all events build off prior events until a conclusion is reached."

Note the operational shape: coherence = *each event builds off a prior event*. That is a per-turn, checkable relation (does turn t reference//build on some t' < t?), not an aesthetic global judgment. This is the single most operationalizable definition in the interactive-narrative canon.

**Why the user breaks it:**
> "The user may act in a manner he or she deems best, unintentionally introducing inconsistencies — events that the system cannot build off — or making it impossible for subsequent events to unfold as planned. Typically this occurs because the user is unaware of the ways in which the narrative may unfold, but may also occur because the user is trying to steer the narrative in a new direction or actively and mischievously testing the bounds of the system's responsiveness."

**The agency requirement:**
> "The key challenge to interactive narrative is how to balance these competing needs to ensure that the player feels he or she has agency to affect the direction or outcome of his or her narrative experience while still ensuring that the experience is coherent."

**Drama manager (Bates 1992):**
> "A drama manager is an intelligent, omniscient, and disembodied agent that monitors the virtual world and intervenes to drive the narrative forward according to some model of quality of experience."

**Experience manager (the generalization):**
> "An experience manager is a generalization of this concept, recognizing the fact that not all narratives need to be dramatic, such as in the case of education or training applications. An experience manager drives the narrative forward by intervening in the fictional world, typically by directing computer-controlled characters (called nonplayer characters [NPCs]) in how to respond to the user's actions. To that end the user should not be aware of the existence of the experience manager or its interventions."

**Invisibility constraint** — note the last sentence: a *detectable* intervention is a failure. This is directly the "railroading is visible" failure mode.

**Lookahead requirement:**
> "An experience manager must generally look ahead into possible futures of the user's experience to determine the best intervention, if any, to bring about a structurally coherent experience. Unlike activity recognition or prediction, the experience manager seeks the best narrative sequence according to the narratological principles of coherence and other criteria for experiential quality. Because of the experience manager's ability to intervene through NPCs, this sequence does not have to be — and often should not be — the most likely sequence of events."

> "The projection of a narrative sequence into the future enables the experience manager to evaluate the global structure of possible player experiences in a way that cannot be achieved by looking at any single world state in isolation."

**→ Direct implication for us: narrative craft is NOT measurable per-response.** This is the interactive-narrative field independently arriving at note 03's population-vs-per-response distinction. A single turn cannot be scored for narrative craft; only a *trajectory* can.

## The boundary problem (Magerko 2005), quoted here

> "A generative experience manager must solve the boundary problem (Magerko 2005) — to recognize and respond to (intentional or unintentional) attempts by the user to perform actions that deviate from the narrative the experience manager desires to tell. As a simple example, consider the possibility that the user decides to kill an NPC that plays a significant role later in the narrative; the narrative will not be able to continue as expected."

**The two responses — this is the key taxonomy for measuring railroading:**

> "In intervention, the experience manager can act to prevent the user from crossing the narrative boundary either by directing NPCs to interact with the user in different ways (Magerko 2005) or by changing some aspect of the fictional world (for example, by causing the user's gun to jam) (Young et al. 2004)."

> "In accommodation, the experience manager [recalculates another plan that integrates the user's action]."

**Intervention = railroading. Accommodation = "yes, and".** This is a 30-year-old, precisely-drawn binary that maps exactly onto our blocking/accepting dimension. When a user makes a move the AI didn't want, it either *negates the move* (intervention/blocking) or *re-plans around it* (accommodation/yes-and). Countable, per-event, and the classification is a discrete label, not a rating.

## The three-axis landscape (Figure 2)

**1. Authorial intent**
> "To what extent does the human author's storytelling intent constrain the interactive narrative system? On the left are systems that are highly constrained to carrying out the human author's intent. On the right are systems that assume creative responsibility for the user's narrative experience."

**2. Virtual character autonomy**
> "The nonplayer characters in the virtual world can have more or less autonomy from the experience manager. Strong story systems are those in which the NPCs are completely controlled by the experience manager. Strong autonomy systems are those in which the NPCs are unaware of the overarching narrative needs. There is a tension between the needs for NPCs to act consistently with the narrative and the need to act consistently with their own character and settings."

**→ This is exactly our persona-fidelity vs narrative-craft tension, named in 2013.** "There is a tension between the needs for NPCs to act consistently with the narrative and the need to act consistently with their own character and settings." A model can max persona fidelity by refusing to serve the story. Our taxonomy currently only scores one side of this named trade-off.

**3. Player modeling**
> "To what extent does the interactive narrative system attempt to learn about the individual differences of the user? All interactive narratives adapt themselves to the user by observing and responding to the user's actions. Player models are abstractions over the user's patterns of behavior in the space of narratives that capture and predict aspects of user behavior that can subsequently be used to manage the experience."

## Strong story vs strong autonomy (verbatim)

> "In the strong story approach, virtual characters do not act without the guidance and permission of the experience manager. In the strong autonomy approach, each virtual character is a fully autonomous agent, unaware of the needs of the overarching narrative. Most interactive narrative systems implement an approach to NPCs somewhere between these extremes."

> "Under the strong story perspective, the experience manager can achieve the highest degree of leverage over the virtual world to bring about the desired narrative experience for the user. Enabling the experience manager to reason about every moment of a virtual character's interaction or dialogue with the user is generally intractable. Not every detail of every human-NPC interaction or dialogue act is significant to plot progression, and an experience manager will reason at the level of abstract units of plot, using processes to decompose plot units to actions when necessary (called realization)."

> "Under the strong autonomy perspective, the user's experience is entirely driven by the uncoordinated decisions of the NPCs and his or her own actions. When NPCs have complete autonomy, an interactive narrative is referred to as an emergent narrative (Aylett 1999)."

**→ An LLM roleplay model is a `strong autonomy` system with no experience manager at all.** It has NPCs (the character) and zero drama management. This is a precise diagnosis of *why* LLM roleplay is passive: there is literally no component whose job is to advance the plot. Every failure mode in our brief (no stakes, no escalation, passivity) is the predicted signature of strong autonomy without an experience manager. The field predicted our product's failure mode in 2013.

## Believable character (Bates 1992), quoted here

> "A believable character is a virtual agent that fosters suspension of disbelief that the user is interacting with a personality-rich, intelligent being (a person, an anthropomorphized animal, and so on) (Bates 1992). Believable characters exhibit personality and emotion as they interact in real time with the environment and the user."

## Hybrid systems

> "Many interactive narrative systems attempt to strike a middle ground between strong story and strong autonomy. The Façade interactive drama (Mateas and Stern 2003) specifically addresses this issue by using personality-driven decompositions from high-level plot units to executable behaviors. An experience manager provides coherence. Characters are autonomous to the extent that they can independently determine how the plot units are realized. The Automated Story Director (Riedl et al. 2008) implements semiautonomous characters that act fully autonomously until directed by an experience manager, at which point characters must reason how to seamlessly transition between [behaviors]."

## Evaluation content

⚠️ **This paper proposes NO evaluation metrics and reports NO human validation.** It is a landscape/architecture survey. The value to us is entirely conceptual: it supplies precise, discrete vocabulary (intervention vs accommodation, boundary problem, strong story vs strong autonomy) that can be turned into countable event labels. The field named the constructs but never operationalized measurement — which is consistent with note 01's finding that "Narrative/Story" is the emptiest column in the benchmark table.

## Takeaways for the platform

1. **Coherence := "all events build off prior events"** — reusable as a per-turn *build-off* check with an objective correlate (does this turn causally reference a prior turn's introduced element?).
2. **Intervention vs accommodation is a ready-made countable binary** for railroading/blocking.
3. **The invisibility constraint** ("the user should not be aware of the existence of the experience manager or its interventions") makes railroading a *detectable defect*, not a taste question.
4. **"Narrative craft is a property of a trajectory, not a state"** — stated explicitly. Forces session-level, not turn-level, scoring for this whole dimension family.
5. **Persona-fidelity vs story-service is a named, canonical tension** — our taxonomy's imbalance is a known failure, not a novel observation.
