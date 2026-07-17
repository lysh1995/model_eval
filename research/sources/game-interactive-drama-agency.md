---
title: "Towards Enhanced Immersion and Agency for LLM-based Interactive Drama"
url: https://arxiv.org/abs/2502.17878
authors: Hongqiu Wu, Weiqi Wu, Tianyang Xu, Jiameng Zhang, Hai Zhao (Shanghai Jiao Tong University)
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Towards Enhanced Immersion and Agency for LLM-based Interactive Drama

Code: https://github.com/gingasan/interactive-drama

**Status: the only paper in this review that names *player agency* as an evaluation dimension for LLM drama. Its measurement of agency is a 1–5 Likert with no rubric, no IAA, and n=10 players. Include it because it defines the construct and because its weakness is itself the finding.**

## What it is

LLM-based interactive drama where a player converses freely with role agents inside an authored plot. Architecture contributions: **Playwriting-guided generation**, **Plot-based Reflection**, and a **Director-Actor / Hybrid** agent split.

## The evaluation framework

**Immersion — four dimensions:**
1. **Character Consistency** — behavioral coherence
2. **Character Attractiveness** — appeal/engagement
3. **Narrative Completeness** — story sufficiency
4. **Narrative Progression** — plot advancement

**⭐ Agency — two dimensions:**
1. **Player Influence** — the degree to which player behaviour influences the story
2. **Intention Following** — how far characters' reactions fulfil player intentions

**This two-way split is conceptually right and worth keeping.** They are genuinely different failures:
- **Low Player Influence** = *railroading*. The plot happens at you. Your choices don't propagate.
- **Low Intention Following** = *ignoring*. The character doesn't even register what you tried to do.

Note the second is nearly identical to MiniMax's "AI Ignores User" (note 01 §4), reached from the games side rather than the product side. **Independent convergence — that raises my confidence that Intention Following is a real dimension.**

## ⚠️ How it is actually measured

> "we ask the annotators to rate each dimension using an integer score from **1 to 5** where 5 represents the best and 1 represents the worst."

- **Human-scored**, not LLM-scored, not automatic.
- **No rubric is given** — not in the main text, not in an appendix. Six annotators, "native speakers with a background in humanities," were handed six dimension *names* and a 1–5 scale.
- **10 volunteers** experienced the drama; 10 GPT-4o agent players constructed alongside; ~60 play sessions total.
- **No inter-annotator agreement is reported. No correlation with any external judgment. No validation of any kind.**

## Results

**Table 4 (Role agents):**

| Variant | Consist. | Attract. | Complete. | Progress. | **Influence** | **Intention** |
|---|---|---|---|---|---|---|
| Director-Actor | 3.9 | 4.2 | 3.8 | 3.6 | **4.2** | **3.9** |
| Hybrid | 4.1 | 3.9 | 4.3 | 4.3 | **4.0** | **4.0** |
| w/o Plot-based Reflection | 4.0 | 3.5 | 4.2 | 3.9 | **3.5** | **3.3** |

Also: Table 3 = story-generation win-rates over 50 topics (Conflict, Suspense, Emotion, Character); Table 5 = human vs aggressive agent players.

**Read the range: every number lives in 3.3–4.3.** A 1–5 scale compressed into one point of range, from 6 unvalidated annotators over ~60 sessions, with no IAA. Given note 01's finding that humans reach only α=0.25–0.34 on roleplay aesthetics with a *rubric*, **these differences are almost certainly not resolvable.** The ablation claims Plot-based Reflection buys +0.7 on Influence (3.5→4.2) — plausible, and completely unsupported by any uncertainty estimate.

**This is precisely the instrument our platform exists to replace.** Do not port these numbers. Port the construct definitions.

## Agency vs narrative coherence

The paper gestures at the tension but does not engage it:

> "Not every scene in a drama encourages heavy player agency... expository scenes... emphasize narrative"

— which motivates their Hybrid architecture. **No explicit theoretical or empirical treatment of the trade-off, and no citation to Wardrip-Fruin or to Yu & Riedl's agency-coherence dilemma** in the text we could retrieve. The interactive-narrative field has had this literature for 15+ years; this paper does not connect to it. Symptomatic of the LLM-roleplay literature generally (cf. note 01's finding that this field re-derives rather than reads).

**Their observation is still operationally useful to us:** agency is *scene-conditional*. Measuring "player influence" uniformly across a dialogue is a category error — an expository opening *should* score low. Any agency metric we build must condition on scene type or it will punish correct behaviour. This is the sparse/dense distinction from CharacterBench (note 01 §4) applied to agency.

## Relevance to companion-eval-platform

1. **⭐ Take the Influence / Intention-Following split; discard the instrument.** Two distinct, product-shaped failure modes (railroading vs ignoring). Intention Following independently corroborates MiniMax's "AI Ignores User."
2. **⭐ The state of the art on player agency is an unvalidated 6-annotator Likert with no rubric.** If we ship *any* objective agency metric with a measured noise floor, we are ahead of the published frontier. That is a low bar and a real opportunity — but see note 13 for why it's still the hardest of our proposed dimensions.
3. **Agency is scene-conditional.** Do not compute it uniformly over turns. Condition on scene type, or restrict to turns where the user actually attempted to exert influence (a sparse dimension, per CharacterBench).
4. **Intention Following is cheap and near-objective; Player Influence is expensive and counterfactual.** Following = "did the reply engage the user's stated intent" — single-turn, local, judgeable. Influence = "would the story have gone differently otherwise" — irreducibly requires a *branch*, i.e. re-rolling from turn t with a different user action. Only the second needs counterfactual rollouts. **Split them in cost tiering.**
