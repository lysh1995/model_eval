---
title: "Achieving the Illusion of Agency"
url: https://ciigar.csc.ncsu.edu/files/bib/Fendt2012-IllusionOfAgency.pdf
authors: Matthew William Fendt, Brent Harrison, Stephen G. Ware, Rogelio E. Cardona-Rivera, David L. Roberts (NC State — Liquid Narrative Group / CIIGAR Lab)
year: 2012
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Achieving the Illusion of Agency (ICIDS 2012)

**This is the single most important agency paper for our platform. It is an experimental demonstration that perceived agency and actual agency come apart — players largely cannot tell a real branching story from a fake one.**

## Abstract (verbatim)

> "Games with a strong notion of story are increasingly popular. With the increased amount of story content associated with games where player decisions significantly change the course of the game (branching games), comes an increase in the effort required to author those games. Despite the increased popularity of these kinds of games, it is unclear if a typical player is able to appreciate the rich content of these games, since any given player typically only experiences a small amount of that content. We create a non-branching game that simulates branching choices by providing players with choices followed by immediate textual feedback. We hypothesize that this game, where player decisions do not significantly change the course of the game, will maintain the player's sense of agency. Experimentation showed that in a text-based story with forced-choice points there were in most cases no significant difference in players' reported feelings of agency when they experience a branching story vs. a linear story with explicit acknowledgement of their choices."

## Definition of agency used

They survey the definitions and explicitly operationalize **Murray's**:

> "Agency is the satisfying power to take meaningful action and see the results of our decisions and choices."

Their rationale for choosing Murray over the alternatives (verbatim): this definition "does not depend on identifying the player's desire (as Wardrip-Fruin et al. posit), nor does it rely on intuition for how to strike a balance between providing actions the player can take and providing motivation for player actions (as Mateas posits)."

Other definitions catalogued:
- **Wardrip-Fruin et al.** — agency occurs "when actions players desire are among those they can take as supported by an underlying computational model"
- **Mateas** — agency as a *structural property*: a balance between **material affordances** (opportunities for action available to the player) and **formal affordances** (motivations the game presents to pursue particular courses of action)
- **Murray** — agency as a phenomenon *in the player*

Note: all three are stated in terms that resist direct measurement. The paper measures Murray's version **with a Likert survey**.

## Experimental design

Text-based CYOA: the player is "Stump Junkman", a monster slayer seeking the king's lost "Crown of Power". **Six decision points, two choices each.** Of the six, **two were true branch points** (substantively different story content); the remaining **four were non-branching**.

**Three conditions:**

| Story | Description | Models |
|---|---|---|
| **Story 1** | Branching, immediate **and long-term** decision feedback (choices referenced later — "variable binding") | Heavily-authored game (Fallout: New Vegas) |
| **Story 2** | **Non-branching**, immediate textual feedback only; choices never referenced again | L.A. Noire |
| **Story 3** | **Non-branching, minimal/no feedback** ("You grab your weapon and head out." regardless of choice) | Baseline control |

Stories 2 and 3 were built from **the most-visited branch** of Story 1, measured after a week of data collection — this controls for story content across conditions.

**Hypothesis 1:** Story 1 and Story 2 "will result in participants reporting similar senses of agency."
**Hypothesis 2:** Story 3 "will result in participants reporting a weaker sense of agency when compared to... a non-branching story with immediate decision feedback."

Three phases; recruitment via snowball sampling. Phase one: 42 men / 37 women. Phase two: 60 men / 24 women. Phase three: 79 men / 28 women.

**Analysed N:** 52 participants on the downselected branch of Story 1 (of 79 total who read the branching story), 54 on Story 2, 44 on Story 3.

| | Male | Female | Mean Age ± St. Dev. |
|---|---|---|---|
| Branching Story | 42 | 37 | 27.2 ± 9.2 |
| Downselected Branching Story (Story 1) | 20 | 32 | 27.0 ± 7.1 |
| Non-Branching Feedback (Story 2) | 47 | 7 | 27.9 ± 8.5 |
| Non-Branching Minimal Feedback (Story 3) | 33 | 11 | 25.1 ± 6.1 |

## The measurement instrument (five-point Likert)

**Story-level questions:**
1. I felt that the actions I took were meaningful within the context of the story.
2. I felt that my actions were important to the progression of the story.
3. I was able to see the results of my actions.
4. I felt that the story would have been different if I had selected different choices.
5. I felt like I had control over aspects of the story that I wanted control over.
6. If given the choice, I would play the game again. *(not an agency question)*

**Question-level (per decision):**
1. I felt that this action was meaningful within the context of the story.
2. I felt that this action was important to the progression of the story.
3. I was able to see the results of this action.
4. I felt that the story would have been different if I had selected different choice.

Statistical test: **Wilcoxon Sum Rank test for unpaired samples**, all pairwise story combinations.

## Results — story-level (verbatim table)

P-values and W-values. Marginally significant (p <= 0.1) bolded; statistically significant (p <= 0.05) marked with X.

| | Story 1 vs. Story 2 P | W | Story 1 vs. Story 3 P | W | Story 2 vs. Story 3 P | W |
|---|---|---|---|---|---|---|
| Question 1 | 0.141 | 1161.5 | **0.015 X** | 1053.5 X | 0.160 | 1268.5 |
| Question 2 | 0.223 | 1124.5 | **0.009 X** | 1082.5 X | **0.039 X** | 1368.5 X |
| Question 3 | 0.123 | 1167.5 | **0.011 X** | 1068.5 X | 0.108 | 1297.5 |
| Question 4 | **0.030 X** | 1233.5 X | **0.003 X** | 1100.0 X | 0.153 | 1267.0 |
| Question 5 | **0.084** | 1203.0 | **0.032 X** | 1033.5 X | 0.254 | 1227.0 |
| Question 6 | 0.302 | 1096.5 | **0.025 X** | 1043.5 X | **0.060** | 1344.0 |

## Findings (verbatim)

**Real branching vs. fake branching (Story 1 vs Story 2) — the headline:**

> "The results of the study showed that there was no significant difference between the branching story and the non-branching story with feedback for four out of five pair-wise comparisons between questions measuring components of agency."

The one exception: participants felt greater agency in Story 1 on **Question 4** ("I felt that the story would have been different if I had selected different choices"), p = 0.05. Marginally greater on **Question 5** ("I felt like I had control over aspects of the story I wanted control over"), p = 0.1.

So: of five agency components, **actual branching only reliably moved the one question that literally asks about counterfactual divergence.** On "meaningful", "important to the progression", and "able to see the results" — the actual substance of Murray's definition — real and fake agency were statistically indistinguishable.

**Feedback vs. no feedback (Story 1 vs Story 3):** significant on *every* question (p <= 0.05). "Reduction from a branching story to a non-branching story without feedback about the player choices does not preserve the player's agency."

**Hypothesis 2 FAILED:** "We failed to prove the second hypothesis, that players would feel a greater sense of agency in Story 2 compared to Story 3. In only one question, 'I felt that my actions were important to the progression of the story,' did participants feel a greater sense of agency in Story 2, significant to the p = 0.05 level."

This is an important honesty note: Story 2 vs Story 3 was *not* cleanly separated, which weakens the causal claim that feedback specifically is what preserves agency.

**Per-decision variance:** three decision points yielded higher agency regardless of treatment (location to visit, how to attack the troll, whether to free the orc); three yielded lower (choice of weapon, how to get through the blockage, how to heal). Authors hypothesize the high-agency ones had "more severe" consequences of failure or "offered two seemingly distinct story paths" — and explicitly say "We do not have sufficient data to make decisive claims."

**Gender confound:** 32/37 (86%) of women chose the forest branch vs 20/42 (48%) of men; Fisher's exact test p = 0.0003. No significant difference on the "free the orc" branch (p = 0.529). Note the resulting severe gender imbalance across conditions (Story 1: 20M/32F vs Story 2: 47M/7F) — this is a real confound the authors flag but do not fully resolve.

**Priming caveat (verbatim):** "we presented the study as a choose-your-own-adventure. The nature of the genre is that your decisions affect the outcome of the story. This is an example of 'psychological priming.' It is likely that the participants inferred that their choices affected the outcome of the story, regardless of whether or not their choices actually did."

## Conclusion (verbatim)

> "We have shown that an approach where players' actions are acknowledged but don't influence gameplay has the potential to preserve the player's sense of agency while reducing the amount of content authors must create."

## Relevance to companion-eval-platform

**This paper should reframe how we scope the agency dimension. It is the strongest evidence that "player agency" as measured by survey is measuring the wrong thing for our purposes.**

1. **Perceived agency does not track actual agency.** This is an *empirical dissociation*, not a theoretical worry. A story with zero branching scored statistically the same as a real branching story on 4/5 agency components with N ≈ 50 per cell. If we ask users "did you feel your choices mattered?", we are measuring the quality of the AI's *acknowledgement prose*, not whether the scene actually responded to them. An LLM is extraordinarily good at exactly the thing Story 2 does — generating fluent immediate feedback that references your choice. **Our platform's AI is a maximally efficient railroading machine that will score well on perceived-agency surveys by construction.** A subjective agency metric would be actively misleading here.

2. **This is the agency analogue of our α problem, but worse.** With aesthetic quality, raters disagree with each other (α 0.25–0.34) — the signal is noisy. With perceived agency, raters can *agree* and still be wrong: they will consistently report agency that isn't there. A reliable measurement of a construct that doesn't track reality is more dangerous than an unreliable one, because it looks trustworthy.

3. **Question 4 is the tell, and it is the seed of an objective metric.** The *only* item that reliably detected real branching was "I felt that the story would have been different if I had selected different choices" — i.e. the item that asks the user to introspect on a **counterfactual**. That is precisely the quantity a counterfactual-divergence metric computes directly, and computes better than a human can introspect it. The literature is pointing at the metric without building it: **re-run the scene from the same state with a different user choice and measure trajectory divergence.** We do not need to ask the user whether the story would have been different; we can *branch the session and check*. This is the strongest argument in the whole review for building counterfactual replay as our agency metric — Fendt et al. essentially demonstrate that the survey is a bad estimator of a quantity we can compute exactly.

4. **The "long-term variable binding" distinction gives us the metric's shape.** Story 1's branching was reinforced by referencing early choices later ("You journey back from the forest..."); Story 2's choices "are not referred to again." That is a *countable* property: does user choice at turn *k* have any causal descendant in the text after turn *k+n*? Immediate acknowledgement (cheap, LLM-default) versus durable consequence (expensive, what users actually paid for) is exactly the axis we want to separate, and it is separable by counting downstream references, not by asking.

5. **Design note for our harness — the priming confound applies to us directly.** Fendt et al. note that framing the experience as a CYOA primes players to infer their choices mattered. Our platform *is* framed as an interactive roleplay where choices matter. Every user arrives primed. This further inflates subjective agency ratings and further recommends against them.

6. **Honest counterpoint to carry:** Fendt et al.'s own second hypothesis failed, the gender distribution across conditions is badly imbalanced (20M/32F vs 47M/7F), and N ≈ 50/cell is modest. The specific claim "feedback is what preserves agency" is under-supported. But the *negative* result we care about — no significant difference between real and fake branching on most agency items — is robust to these problems, since confounds would tend to *create* differences rather than erase them. The finding we are leaning on is the one the study is best positioned to support.

7. **Product-strategy implication worth flagging to the team:** if perceived agency is cheap to fake and users can't tell, then an *objective* agency metric is not just an eval nicety — it is the only way the platform can distinguish a genuinely responsive scene engine from a fluent railroading one. That is a defensible differentiator precisely because it cannot be gamed by better prose.
