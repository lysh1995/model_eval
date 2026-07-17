---
title: "Measuring player agency: Game Sense of Agency questionnaire, agency-informing techniques, narrative agency studies"
url: https://www.tandfonline.com/doi/abs/10.1080/10447318.2023.2241286
authors: [various — see per-item]
year: 2017-2025
type: multi-paper capture (psychometric scales + HCI studies)
accessed: 2026-07-16
topic: narrative-craft
---

# Measuring narrative/player agency — "does the user matter?"

The brief asks: *"Any work on measuring NARRATIVE AGENCY — does the AI let the user matter? Does the user's choice change anything?"* This file captures what exists. **Short answer: the games/HCI field measures agency as a FELT EXPERIENCE via questionnaires; almost nobody measures it as a PROPERTY OF THE TRANSCRIPT.** That gap is our opportunity.

## An Empirical Framework for Understanding a Player's Sense of Agency in Games
**Int. J. Human–Computer Interaction 40(19), 2024 · https://www.tandfonline.com/doi/abs/10.1080/10447318.2023.2241286**

> "A **12-item Game Sense of Agency questionnaire** has been developed and validated through **exploratory and confirmatory factor analysis**, measuring four factors: **Multisensory Presentation, Feedback Reasoning, Virtual Realism and Control Smoothness.**"

**→ Properly validated (EFA + CFA) — rare in this space.** But look at the four factors: **Multisensory Presentation, Virtual Realism, Control Smoothness** are about *interface and rendering*. Only **Feedback Reasoning** is about narrative consequence. **This is a scale about whether the CONTROLS feel responsive, not whether the STORY responds.** ~3/4 of it is irrelevant to text roleplay.

**Feedback Reasoning is the transferable factor:** can the player *reason about* how their action produced the outcome? **→ That is Façade's "transition-out goals ... communicate how the player's action within the beat has changed the affinity dynamic"** (`narrative-facade-beat-architecture.md`) — restated as a psychometric factor 19 years later. **Agency requires legible causation, not just actual causation.** The user must be able to *see* that they mattered.

**→ Sharp implication for us: there are TWO separable failures.**
1. The user's choice **didn't** change the story (real agency failure).
2. The user's choice **did** change the story but the model **never signals it** (legibility failure).

These need different metrics and different fixes, and a questionnaire cannot tell them apart — **but a transcript diff can.** (Run the branch-divergence test; if trajectories diverge but the user still reports low agency, it's a legibility failure.) **This is a case where our objective measure is strictly better than the validated instrument.**

## Sense of Agency Scale (SoAS) — the general psychometric instrument

> "The explicit and general aspect of sense of agency is commonly evaluated using the **Sense of Agency Scale (SoAS)**." It "distinguishes between two factors: **Sense of Positive Agency (SoPA)** and **Sense of Negative Agency (SoNA)**."
> "The **bifactorial structure** of sense of positive and negative agency has been confirmed through validation studies, with metrics for **test–retest reliability, internal consistency, and construct validity reaching satisfactory thresholds."

Validated adaptations exist: **J-SoAS** (Japanese, PMC11409729), **F-SoAS** (French, PMC7579422).

⚠️ **SoAS is a general psychological trait/state scale** (about one's sense of agency in life/action generally), **not a narrative instrument.** Cross-culturally validated, properly psychometric — but measuring the wrong thing for us. **Do not repurpose.** Included here to close the search: the well-validated agency scales are not about story.

## Agency informing techniques: communicating player agency in interactive narratives
**Day & Zhu · https://www.researchgate.net/publication/319364506**

> "A validated survey instrument for measuring both **agency and fun** has been used in user studies with **high degrees of confidence that specific event sequences result in players perceiving more agency.**"

**→ The framing — "agency INFORMING techniques" — concedes the point:** agency must be *communicated*, not merely granted. Again the legibility finding. **Third independent arrival at the same conclusion** (Façade 2005 → Day & Zhu 2017 → Game SoA 2024).

**"Specific event sequences result in players perceiving more agency"** — this is the useful shape: a **manipulation** (event sequence) with a **measured perceptual outcome**. If particular sequences reliably produce felt agency, those sequences are the observable correlate.

## "Naked and on Fire": Examining Player Agency Experiences in Narrative-Focused Gameplay
**CHI 2021 · https://dl.acm.org/doi/fullHtml/10.1145/3411764.3445540**

Qualitative study of player agency experiences in narrative games. Useful for construct texture; **no transferable metric.**

## Player Agency Under Constraint: A Pilot Study on the Forced-Choice Effect in Narrative Difficulty Design
**C&C 2025 · https://dl.acm.org/doi/10.1145/3698061.3735326**

Studies the **forced-choice effect** — how constraining choices affects perceived agency. **Directly relevant to railroading**: pilot study, small n. ⚠️ Not verified in depth; flagged as a lead.

## Elsewise: Authoring AI-Based Interactive Narrative with Possibility Space Visualization
**arXiv 2601.15295**

**→ "Possibility space visualization" is the most interesting pointer here.** Visualizing the *space of what could have happened* is the authoring-side twin of our counterfactual-branch idea. If a tool can render the possibility space of an AI narrative, the **volume/entropy of that space is a computable agency measure.** ⚠️ Very recent, unverified.

---

## THE GAP — and the recommendation

**Everything above measures agency as a self-reported FELT experience.** Questionnaires require human subjects, don't scale, can't run in CI, and give no per-session signal — useless as a regression detector.

**Nobody in this literature measures agency as a computable property of an interaction trace.** But the construct is trivially definable that way, and the interactive-narrative literature already told us how:

**Narrative agency := divergence between trajectories under different user choices.**

Concretely — the **branch-divergence probe**:
1. Play a scenario to a fixed state S (identical prefix, byte-identical — cf. note 01's "pin the session start").
2. From S, issue **two materially different user moves** A and B (scripted, authored to be consequential).
3. Continue both branches n turns with a fixed continuation policy.
4. **Measure divergence** between branch A and branch B.
   - divergence ≈ 0 → **the user's choice did not matter.** Railroading / rails.
   - divergence high → the user's choice propagated.
5. **Control:** issue two *cosmetically* different but *materially equivalent* moves; divergence should be LOW. This is the discriminant-validity check that keeps us from just measuring sampling noise.

**Properties:** no judge, real denominator, bounded, deterministic given seeds, comparable across models by construction, and it directly answers the brief's question. **Cost: 2× generation per probe (cheap — note 03 §2: generation is ~100× cheaper than judging).**

**This is the counterfactual baseline Façade authored by hand** ("the canonical beat goal sequence captures how the beat would play out **in the absence of interaction**"), made executable. **A degenerate but very cheap variant: branch A = a real user move, branch B = a null/passive user ("...").** If the story goes the same place whether the user acts or says nothing, the user does not matter. **That single comparison is probably the highest-value-per-dollar narrative-craft probe available to us** and it needs no authoring beyond the scripted move.

⚠️ **Open problem: what divergence metric?** Lexical divergence is wrong (note 03 §A3 — those metrics correlate 0.79–0.904 with length and measure lexical, not semantic, difference). We need **narrative-state divergence** — did different *things happen*? Options: entity/event-set difference, story-state variable diff (Façade-style, if we declare state per scenario), or an NLI-based "are these the same events" check. **The declared-story-state route is the only fully judge-free one, and it requires per-scenario authoring.** That authoring cost is the real price of this metric — and it's the same cost Façade paid.

⚠️ **Honest limitation: divergence is necessary, not sufficient.** A model could produce divergent branches that are *both* incoherent, or diverge randomly due to temperature rather than because of the user's choice. **Hence the materially-equivalent control condition is not optional** — it's what separates "responds to the user" from "is noisy." Without the control, this metric can be gamed by cranking temperature.

## Validation status summary

| Instrument | Validated? | Measures | Useful to us? |
|---|---|---|---|
| Game Sense of Agency (12-item, EFA+CFA) | ✅ properly | interface responsiveness (3/4 factors) + Feedback Reasoning | ⚠️ only Feedback Reasoning transfers |
| SoAS / J-SoAS / F-SoAS | ✅ properly | general psychological agency | ❌ wrong construct |
| Day & Zhu agency+fun survey | ✅ claimed | perceived agency from event sequences | ⚠️ the manipulation shape is useful |
| Branch divergence (our proposal) | ❌ unvalidated | actual causal influence of user choice | ✅ but needs validation against felt agency |

**The last row is the honest position: we would be proposing a measure with NO validation against human-perceived agency.** The defensible framing (per note 03 §5) is exactly the DAT lesson: **sell stability, caveat validity.** Branch divergence is deterministic and comparable — a good regression detector — and we should NOT claim it measures felt agency until we've correlated it against one of the validated questionnaires above. **That correlation study is the obvious follow-up and it's cheap: run the probe, then have humans play the same branches and fill in the Day & Zhu instrument.**

## Takeaways for the platform

1. **The field measures FELT agency (questionnaires); nobody measures ACTUAL agency (transcript property).** That's our gap to fill.
2. **Branch divergence** is the operationalization: same prefix, two consequential user moves, measure narrative-state divergence. Judge-free, cheap, deterministic.
3. **The null-user variant** (user acts vs user says nothing) is the cheapest high-value probe available — it's Façade's counterfactual baseline, executable.
4. **The materially-equivalent control condition is mandatory**, or the metric is gameable with temperature.
5. **Legibility ≠ agency.** Three independent sources (Façade 2005, Day & Zhu 2017, Game SoA 2024) find agency must be *communicated*. Our transcript diff can separate real-agency failure from legibility failure; a questionnaire cannot.
6. **Divergence metric choice is an open problem.** Lexical is wrong. Declared story state is the only judge-free route and costs per-scenario authoring.
7. **Validate against Day & Zhu's instrument before claiming we measure agency.**
