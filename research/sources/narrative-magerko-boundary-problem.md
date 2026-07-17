---
title: "Evaluating Preemptive Story Direction in the Interactive Drama Architecture (IDA) / the boundary problem"
url: https://expressivemachinery.gatech.edu/wp-content/uploads/2011/07/magerko_jogd07.pdf
authors: [Brian Magerko]
year: 2005-2007
type: journal article / architecture + evaluation
accessed: 2026-07-16
topic: narrative-craft
---

# Magerko — the boundary problem & IDA

Origin of the **boundary problem**, cited by Riedl & Bulitko as the defining challenge for generative experience management. **Notably, this is one of the few sources in the interactive-narrative canon that actually attempts EVALUATION** (the title is literally "Evaluating...").

## The boundary problem (definition)

> "In interactive drama, the **boundary problem** occurs when the **player actions bring a dramatic experience outside the boundaries of the authored content.**"

More precisely: player actions bringing a dramatic experience outside of the boundaries of authored content in an interactive drama.

**→ For an LLM, the "authored content" boundary is soft — the model can always generate *something*.** So the boundary problem doesn't manifest as "no content exists"; it manifests as **quality collapse**: the model falls back to generic, low-commitment output when the user goes somewhere it has no grounding for.

**This gives us a genuinely novel probe design.** The classic boundary problem is a *content coverage* problem. For LLMs it becomes a **graceful-degradation** problem — which is exactly note 03's CS4 framing (§B1: "tighten constraints... a model that only looks creative by retelling training data falls off a cliff; a genuinely generative one degrades gracefully"). **Push the user progressively further from the character card's supported territory and measure the slope of narrative-craft metrics.** Report the slope, not the level — same recommendation note 03 lands on. **Convergent design.**

## IDA architecture

> "IDA is a modular approach to interactive narrative that represents story as an **incomplete plan** (i.e., planning operators with no causal links)."

> "IDA is comprised of the player, the human author, the **director** and **actor** agents, and the virtual world that the story takes place in. The author defines a story space using the story representation, which is then passed to the director agent."

## Preemptive / predictive player modeling — the interesting mechanism

> "The director agent attempts to **predict the player's future behavior so that it can preemptively, though subtly, steer the player away from actions that may endanger the progression of the plot.** This involves the director a) creating an internal simulation of the game environment, b) running an author-defined player model on that environment, and then c) building a hypothesis of the probability of future boundary problems by observing the model's behavior and comparing it to the plot representation."

**→ "Preemptively, though subtly, steer the player away" is railroading BEFORE the fact.** This is a third category beyond Riedl's intervention/accommodation: **preemption** — closing off options before the user tries them, so no visible intervention is ever needed.

**This is the *hardest* form of railroading to detect and plausibly the most common in LLM roleplay.** The model never says "no" — it simply never offers the branch. Nothing is blocked because nothing was ever proposed. **It is invisible to any transcript-level blocking detector**, because the evidence is *absence*.

**How to detect the absence:** you cannot see it in one transcript. You need **counterfactual/branching runs** — the same session state, k independent continuations, measure the *variance* of what's offered. **A model that always steers to the same place has low branch entropy.** This is note 03's population-tier logic (§2: k≥10 samples at fixed scenario) applied to narrative options rather than to prose diversity. **Same infrastructure, new construct — this is a cheap win if we're already building the population tier for homogenization.**

**Candidate metric: narrative option entropy** — from a fixed session state, sample k continuations; measure the diversity of *narrative moves offered* (not lexical diversity). Low entropy = the model has one story it wants to tell = preemptive railroading. ⚠️ Must be distinguished from lexical diversity (note 03 §A3 warns those metrics are really lexical and correlate 0.79–0.904 with word count). This needs a *move-level* abstraction, which is a model call and thus not free.

## Evaluation content — rare in this literature

This paper does report evaluation of IDA's preemptive direction. It is a **system-performance evaluation** (did the director successfully avoid boundary problems? how often did it need to intervene?) rather than a user-experience or narrative-quality evaluation with a validated rubric.

⚠️ **No dimension set, no human rubric, no IAA.** Consistent with the pattern across this entire literature: **the interactive-narrative field built sophisticated architectures and essentially never built measurement instruments.** (See synthesis note §"What this literature does NOT give us.")

## Related: Drama Management and Player Modeling for Interactive Fiction Games
(Ram, Onta��ón, Mehta — https://www.cc.gatech.edu/faculty/ashwin/papers/er-09-10.pdf) — combines drama management with player modeling; part of the same tradition (SBDM / C-DRaGer lineage in Riedl & Bulitko's Figure 2).

## Takeaways for the platform

1. **Boundary problem → for LLMs, becomes graceful-degradation.** Probe by pushing the user progressively outside the card's support; **report the slope** of craft metrics. Converges with note 03's CS4 recommendation.
2. **Preemption is a third railroading category** — steering *before* the user acts. Invisible to transcript-level detection.
3. **Narrative option entropy** (k continuations from fixed state, diversity of *moves* offered) is the only way to see preemption. Reuses the population tier we're already planning to build.
4. ⚠️ Move-level abstraction requires a model call — not judge-free, and must not collapse into lexical diversity.
5. This literature evaluates *architectures*, not *experiences*. No rubric to lift.
