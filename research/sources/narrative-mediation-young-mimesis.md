---
title: "Narrative Mediation, the Mimesis architecture, and mediation as probabilistic planning"
url: https://justusrobertson.com/papers/Robertson%20and%20Young%202017%20-%20Narrative%20Mediation%20as%20Probabilistic%20Planning.pdf
authors: [R. Michael Young, Mark Riedl, C. J. Saretto, Justus Robertson]
year: 2003-2017
type: architecture + follow-on formalization (multi-paper capture)
accessed: 2026-07-16
topic: narrative-craft
---

# Narrative Mediation / Mimesis (Young, Riedl, Saretto; Robertson & Young)

The formal machinery behind Riedl & Bulitko's **intervention vs accommodation** binary. Matters to us because it makes the railroading construct **precise and discrete** rather than a matter of degree.

## Core definitions

**Narrative mediation:**
> "Narrative mediation is a plan-based process that converts a planning problem into a **mediation tree** that models an interactive story. This technique allows a degree of control and coherence that lies between that of computer games and conventional narrative media, and is implemented within an interactive narrative system named **Mimesis**."

**The two mediation policies — the ones that matter:**

> "**Intervention** is a solution where the undesirable outcomes of a player's action are exchanged for a set that do not violate the story model."

> "In contrast, **accommodation** involves the planner recalculating another plan that integrates the user's action."

**Mediation tree:**
> "The graph of a cascading mediation policy whose vertices are narrative plans and edges are exceptional actions is called a **mediation tree**."

**Provenance:**
> "The original reactive mediation algorithm was developed by **Riedl, Saretto, and Young in 2003** for use with the Mimesis system, which **reconciles exceptional user actions with the system's original story plan** to create a unified interactive experience."

## Why this is the sharpest available formalization of railroading

The mediation framework defines an **exceptional action**: a user action whose outcome would violate the author's story plan. When one occurs, the system has exactly **three** options:

1. **Accommodate** — re-plan so the user's action is *causally integrated*. The user changed the story. (= "yes, and")
2. **Intervene** — silently swap the action's outcome so the plan survives. The user *thinks* they acted; nothing changed. (= railroading, done invisibly)
3. **Fail** — the story breaks. (= incoherence)

**This is a complete, mutually exclusive, exhaustive trichotomy over "what happens when the user does something unplanned."** That is exactly the taxonomy we need for narrative agency, and it has been formally specified since 2003.

**The famous example: "causing the user's gun to jam."** The user pulls the trigger on a plot-critical NPC; the system jams the gun. The user acted; the world did not change. **This is the canonical illustration of intervention** — and it is precisely what an LLM does when it deflects a user's scene-altering move ("you try, but somehow you can't...", "before you can, she interrupts...").

**→ Operationalizable directly:** classify each user attempt to change the fiction as *accommodated* / *intervened* / *failed*. The **intervention rate is the railroading metric.** Countable, per-event, with a real denominator (number of exceptional actions the user attempted).

**→ The "gun jams" pattern has recognizable lexical signatures in LLM roleplay:**
- "You reach for X, but —"
- "Before you can, ..."
- "Somehow, it doesn't work."
- "She catches your wrist."
- Narrating the user's *failure* to act.

**Deflection-of-user-action is partially detectable with patterns** and fully detectable with a small classifier. **This is one of the cheapest high-value detectors available to us** and it directly measures "does the user matter?"

⚠️ **Important nuance: intervention is not always wrong.** In Mimesis it is a *legitimate, designed* policy — sometimes preferable to accommodation because it preserves authorial intent cheaply. **The defect is not intervention per se; it is intervention as the DEFAULT.** A model that accommodates 0% of user moves is railroading; a model that accommodates 100% has no spine and may be wimping (accepting every offer without shaping). **The metric is a rate to be characterized, not minimized.** This is important — a naive "lower intervention = better" alert would reward pure sycophancy.

## Robertson & Young 2017 — mediation as probabilistic planning

Reformulates mediation as probabilistic planning over player behavior, using an MDP/POMDP framing. Related: **"Finding Schrödinger's Gun"** (Robertson & Young, AIIDE) — the title is a direct reference to the gun-jam intervention: the gun's state is *indeterminate until observed*, i.e. the system decides retroactively whether the gun was loaded based on narrative need.

**→ "Schrödinger's gun" is a precise name for a real LLM roleplay behavior: retroactive fact determination.** The model decides what was true *after* the user acts, to suit the scene. This is a *double-edged* construct:
- Used well, it's good improv (justification, "yes-and"-ing your own world).
- Used badly, it's **cancelling** (Johnstone's term — negating established facts) and it destroys user agency because nothing the user established is stable.

**Measurable as: rate at which the model asserts facts that contradict *its own* earlier assertions in a way that conveniently blocks a user action.** This is the intersection of plot-hole detection and railroading detection — and the *conjunction* is far more diagnostic than either alone. A contradiction that happens to block the user is not a random error; it's a tell.

## Evaluation / validation

⚠️ **The Mimesis line is architecture and formalism. It reports NO human evaluation of narrative quality, NO dimension set, NO agreement statistics.** Robertson & Young report planner performance (search efficiency, solution quality), not user-experience measures.

**Related empirical work that DOES measure something:** "The Mimesis Effect: The Effect of Roles on Player Choice in Interactive Narrative Role-Playing Games" (CHI) — studies how assigned roles shape player choice. Not captured in depth here; flagged as a lead if we want evidence on *user-side* behavioral effects.

## Takeaways for the platform

1. **Intervention / accommodation / fail is a complete trichotomy** over user attempts to change the fiction. Adopt it verbatim as our narrative-agency event taxonomy.
2. **Intervention rate = railroading rate.** Countable, real denominator, cheap detector (deflection patterns).
3. **⚠️ Do not minimize intervention — characterize it.** 0% accommodation = railroading; 100% = wimping. Both are defects. The healthy range is empirical and must be established, not assumed.
4. **"Schrödinger's gun" / retroactive fact determination** = self-contradiction that conveniently blocks the user. The conjunction (contradiction ∧ blocks-user) is highly diagnostic and reuses plot-hole infrastructure.
5. No validation evidence in this line — the value is conceptual precision, not measurement.
