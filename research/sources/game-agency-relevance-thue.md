---
title: "Player Agency and the Relevance of Decisions"
url: https://rise.csit.carleton.ca/pubs/ThueBulitko_ICIDS_2010.pdf
authors: David Thue, Vadim Bulitko, Marcia Spetch, Trevon Romanuik (University of Alberta, Departments of Computing Science and Psychology)
year: 2010
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Player Agency and the Relevance of Decisions (ICIDS 2010)

**The one paper in this review that proposes a FORMAL, COMPUTABLE quantity related to agency. Important caveats: it is a short position/design paper, the metric is a *generation heuristic* rather than an evaluation metric, and it was never empirically validated.**

## Abstract (verbatim)

> "While many forms of storytelling are well-suited to the domain of entertainment, interactive storytelling remains unique in its ability to also afford its audiences a sense of having influence over what will happen next. We propose that the key to encouraging such feelings of agency in interactive stories lies in managing the perceived relevance of the decisions that players make while they play. To this end, we present the design of a system which automatically estimates the relevance of in-game decisions for each particular player, based on a dynamically learned model of their preferences for story content. By actively choosing among several potential consequences of a given player decision, the proposed system highlights the relevance of each decision while accommodating for its players' preferences over potential story content."

## THE CENTRAL DISTINCTION (verbatim) — the most important passage in the agency literature for us

> "Consider the distinction between two phenomena: **theoretical agency**, as one's (objective) ability to change the course of their experience, and **perceived agency**, as one's (subjective) perception of their ability to make such changes. Much research in story generation has focused on finding ways to efficiently provide the former, but always with the implicit assumption that doing so will effectively elicit the latter."

> "In this paper, we challenge this assumption, drawing on research in the field of Social Psychology to suggest that maximizing the perceived agency of players requires more than providing theoretical agency alone; the desirability of the consequences of player actions must be carefully considered as well."

They also distinguish **agency from gameplay** (manipulating the input device, exploring, overcoming challenges — which commercial games "provide... very well") from **agency from story** (choices determining which sequence of events is shown), citing Wardrip-Fruin et al.'s "Agency Reconsidered".

**The field names the objective quantity — "theoretical agency" — and then does not measure it.** The entire paper is about improving *perceived* agency. Theoretical agency is treated as a given input to the design ("this design provides all players with a non-trivial amount [of] theoretical agency"), never as a quantity to be computed or reported.

## The Control Heuristic (Thompson et al., 1998, Psychological Bulletin 123(2):143–161)

The psychological grounding, "derived by Thompson et al. from an extensive synthesis and unification of prior experimental results." Judgement of control is influenced by two primary factors:

- **Intention** to achieve the outcome that occurred. Sub-factors:
  - **foreseeability** of the outcome
  - **ability** to make the outcome occur
  - **desirability** of the outcome for that particular person
  > "If a desirable outcome can be foreseen and one seems capable of achieving it, then intentionality is strongly inferred; the strength of this inference decreases if any of these conditions are not met."
- **Connection** perceived between action and outcome. Two subtypes:
  - **temporal** — "stronger the more times a desirable outcome has been observed to occur after an action was taken"
  - **predictive** — "stronger when the outcome that occurs was predicted to follow from the action that was taken"

Four conditions must be satisfied for maximum perceived agency: **foreseeability, ability, desirability, and connection.**

> "while theoretical agency does grant players the ability to achieve various outcomes and (presumably) also demonstrates temporal connections (*ability* and *connection*), relatively little research to-date has explored how to ensure that the outcomes of player actions are both foreseeable and desirable."

This is a clean decomposition and worth noting: **theoretical agency only buys you two of the four factors.** You can have real branching and still produce no felt agency if outcomes are unforeseeable or undesirable. Conversely — per Fendt et al. — you can fake connection and get felt agency with no branching at all.

## The formal model

Interactive experiences as a **tree of possible world states**; nodes further from root occur later. Edges = decisions executed by either the **director** (the AI experience manager) or the **player**. Events are subtrees; each leaf is an alternate **outcome**. Director decisions divide an event's subtree into **sub-events**.

Worked example (Figure 1): the player leads a village and must spend limited gold on either **walls** or **food** (bandits threaten; drought has starved the peasants; cannot afford both).

Two candidate future events, each with two sub-events selected by the player's earlier walls-vs-food decision:
- **Village Commotion (VC)** → sub-events *Unrest* (if walls: peasant revolt) or *Party* (if food: party in the player's honour)
- **Soldiers Approaching (SA)** → sub-events *Attack* (if walls: bandits attacking) or *Inspection* (if food: the king arriving to inspect)

> "The director's choices of sub-events (*Unrest* versus *Party*, or *Attack* versus *Inspection*) are determined entirely by the player's choice between repairing the village walls or ordering food for the peasants; this design provides all players with a non-trivial amount theoretical agency. **The director's decision among events, however, is the means by which our proposed system aims to maximize the perceived agency of its players.**"

### Desirability (Equation 1)

Adopted from PaSSAGE's player model — five play-style inclinations: 'Fighter' (F), 'Method Actor' (M), 'Storyteller' (S), 'Tactician' (T), 'Power Gamer' (P). Desirable sub-events are "those which allow players to play in their modelled styles."

```
desirability(e) = max          [PlayerModel · Annotations(a)]        (1)
                  a ∈ Actions(e)
```

Worked numbers (verbatim): for sub-event *Unrest*, player model vector `[F20,M10,S15,T0,P0]`; player actions annotated *Grand Speech*: `[F0,M1,S4,T0,P0]` and *Swift Strike*: `[F4,M0,S0,T2,P0]`. Inner products: `max(70, 80)` → **desirability(Unrest) = 80**.

### Relevance (Equation 2) — THE METRIC

> "we define the relevance of a decision as **the degree to which it affects the player's ability to experience desirable sub-events** during the course of her experience."

```
relevance(d|E) = |desirability(e⁺) − desirability(e⁻)|              (2)
```

where for a player decision `d` and event `E`, `e⁺` is the sub-event within `E` that `d` **enables** and `e⁻` is the sub-event within `E` that `d` **disables**. (In VC, 'walls' enables *Unrest* and disables *Party*.)

Worked example (verbatim):

```
relevance(walls|VC) = |desirability(Unrest) − desirability(Party)|      = 50    (3)
relevance(walls|SA) = |desirability(Attack) − desirability(Inspection)| = 30    (4)
```

Director algorithm: compute relevance of every candidate event that uses `d` to distinguish its sub-events; **choose the event with highest relevance that also provides a desirable sub-event** (`desirability(e) > 0`). Here: since `desirability(Unrest) = 80 > 0` and `relevance(walls|VC) = 50 > 30`, the director picks Village Commotion.

### The hypothesis (verbatim, never tested in this paper)

> "we hypothesize that for a given interactive experience having a fixed amount of theoretical agency, proactively choosing events to maximize the relevance of player decisions while providing desirable outcomes will increase the agency that players perceive."

## Status of the work (verbatim)

> "An empirical evaluation via human user study is forthcoming which, if successful, will provide evidence that adapting to players is important for perceived agency to occur."

**No evaluation is reported.** This is a 6-page design/position paper. Prior PaSSAGE user studies "have shown that automatic story adaptation can improve perceived agency for particular subgroups of players" — note *subgroups*, and note that even that outcome measure is perceived agency, i.e. a survey.

## Relevance to companion-eval-platform

**Read this as: the literature got within one step of an objective agency metric, then walked the other way.**

1. **`relevance(d|E) = |desirability(e⁺) − desirability(e⁻)|` is a genuine counterfactual-divergence metric — structurally exactly what we want.** It compares the branch you got against the branch you didn't and returns a magnitude. That is the shape of the metric our platform needs: **choice mattered ∝ how different the enabled future is from the disabled one.**

2. **But it is not usable off the shelf, for three reasons.** (a) It measures divergence in *desirability to a modelled player*, not divergence in *story content* — it needs author annotations on every action plus a learned five-dimensional player model. (b) It is a **director-side generation heuristic**: it tells an experience manager which event to schedule next, and presupposes the branching structure already exists and is known. It cannot be run on an observed transcript. (c) It was never validated — the promised user study is not in this paper.

3. **The productive move is to keep the form and swap the payload.** Replace hand-annotated `desirability` with a computable divergence over *actual generated continuations*:
   `agency(d) = divergence( rollout(state, choice_A), rollout(state, choice_B) )`
   This requires no author annotations and no player model. It requires only the ability to **re-run the scene from a checkpoint with a different user input** — which we have, because we control the harness and LLM sessions are resumable from a prefix. Divergence can be measured over whatever we can extract objectively: world-state facts asserted, entities introduced, events that occur, downstream references to the choice. **This is the single most actionable idea in the whole review**, and Thue & Bulitko is the closest prior art to cite for it.

4. **The theoretical/perceived distinction is the frame for our whole agency dimension, and this paper is the citation.** Thue & Bulitko *name* the objective construct ("theoretical agency, as one's (objective) ability to change the course of their experience") and then explicitly declare it insufficient and pivot to optimizing the subjective one. Fendt et al. (2012) later show the two dissociate empirically. So the field's own position is: theoretical agency is real, objective, and — they argue — not what matters. **Our platform should take the opposite bet, and should do so knowingly:** we measure theoretical agency *because* it is the thing that can be measured reliably and cannot be faked by better prose, while acknowledging the field thinks perceived agency is the end goal. That is a defensible position but it is a genuine disagreement with the literature, not a gap in it — and our docs should say so plainly rather than implying nobody thought of it.

5. **The Control Heuristic gives us a free explanation of why an LLM will railroad and get away with it.** Perceived agency needs foreseeability + ability + desirability + connection. An LLM trivially supplies *connection* (it always acknowledges what you said) and *desirability* (it is trained to be agreeable and will happily give you what you asked for). It supplies these **whether or not any branching occurred**. That is a mechanistic account of Fendt's result and a prediction that our AI will score high on perceived agency by default. It also suggests the diagnostic: **desirability and connection are the fakeable factors; ability is the real one.** An agency metric should target ability — did the choice actually change what the system can and does do — which is precisely counterfactual divergence.

6. **Related:** `game-illusion-of-agency-fendt.md` (the empirical dissociation), `game-agency-reconsidered.md` (the canonical non-operational definitions).
