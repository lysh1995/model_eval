---
title: "Agency Reconsidered"
url: https://eis.ucsc.edu/papers/nwf-C7-digra09-agency.pdf
authors: Noah Wardrip-Fruin, Michael Mateas, Steven Dow, Serdar Sali (UC Santa Cruz Expressive Intelligence Studio; Carnegie Mellon)
year: 2009
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Agency Reconsidered (DiGRA 2009) — the canonical agency definition paper

This is the paper the whole agency literature cites, and it is a **theory paper with no metric**. It is included precisely because it establishes that the field's foundational statement of agency is deliberately non-operational — which is itself the finding.

## Abstract (verbatim)

> "The concept of 'agency' in games and other playable media (also referred to as 'intention') has been discussed as a player experience and a structural property of works. We shift focus, considering agency, instead, as a phenomenon involving both player and game, one that occurs when the actions players desire are among those they can take (and vice versa) as supported by an underlying computational model. This shifts attention away from questions such as whether agency is 'free will' (it is not) and toward questions such as how works evoke the desires agency satisfies, employ computational models in the service of player action and ongoing dramatic probability, use interfaces and mediation to encourage appropriate audience expectation, shift from initial audience expectation to an understanding of the computational model, and can be shaped with recognition of the inherently improvisational nature of agency."

Author keywords: computer games, interactive drama, agency, intention, perceived consequence, affordances, Eliza effect, SimCity effect, augmented reality, human-computer interaction, improvisation.

## The three competing definitions (verbatim)

1. **Murray** — agency as audience experience: "the satisfying power to take meaningful action and see the results of our decisions and choices"
2. **Mateas** — agency as structural property: "Players will experience agency when there is a balance between the material and formal constraints. When the actions motivated by the formal constraints (affordances) via dramatic probability in the plot are commensurate with the material constraints (affordances) made available from the levels of spectacle, pattern, language and thought, then players will experience agency. An imbalance results in a decrease in agency."
   - **material affordances** = opportunities for action available to the player
   - **formal affordances** = motivations the game presents (via dramatic probability) to pursue particular actions
   - Diagnosis of adventure games: "there are typically many more material affordances than formal affordances — so there are many things to do, but no clear sense of why one action would be preferable to another."
3. **This paper** — agency as a phenomenon involving both, "when the actions players desire are among those they can take (and vice versa) as supported by an underlying computational model."

**Note that all three are unmeasurable as stated.** Murray requires knowing whether an action felt "meaningful". Mateas requires quantifying a "balance" between two kinds of affordance. Wardrip-Fruin et al. require knowing what the player *desired*. There is no metric in this paper, and none is proposed.

## The Eliza effect (verbatim, central to our problem)

The Eliza effect = "the not-uncommon illusion that a computer system is much more 'intelligent' (complex and capable) than it is in reality."

Wardrip-Fruin's position, from *Expressive Processing* (2009): leveraging the Eliza effect "is a deeply problematic direction for digital media."

On fragility — the paper's example of Eliza breaking down:

> Player: "Can I ask you for help" → Eliza/Doctor: "DO YOU WANT TO BE ABLE TO ASK I FOR HELP"

> "Such fragility causes two problems in relation to agency. First, breakdowns damage the sense of dramatic probability in the situation. Second, they make the audience member question whether the materials presented for action (the whole of the English language, as invited by the open text field) can actually be used intentionally."

> "the Eliza effect works, for however long it works, because of the power of the initial expectations of the player, which are eventually too greatly violated. The illusion of agency is short lived."

Crucially, players who push on Eliza discover it "is, at heart, a textual transformation device." That is "an experience of agency in relation to Eliza as a software toy, but not in relation to the fictional world of Eliza/Doctor. In other words, for the sorts of experiences that interest Murray, Church, and the authors of this paper, it is a dead end."

## The SimCity effect (verbatim) — the contrast case

Both Eliza and SimCity start from player expectation. The difference:

> "Playing with Eliza, the initial impression encouraged by the Doctor character is eventually revealed as utterly removed from the internal system model. As this happens, the system ceases to operate as a representation of a fictional world."

> "On the other hand, the underlying model in SimCity is designed as a representation of a dynamic city... While initial engagement with SimCity is based on player expectation, **the elements presented on the surface have analogues within the internal processes and data.** Successful play requires understanding how initial expectation differs from system operation, incrementally building a model of the system's internal processes based on experimentation. **This is how agency happens.**"

The requirement that follows (verbatim):

> "To create the phenomenon of player agency in relation to a fictional world it is necessary to suggest dramatically probable events, make material affordances available for taking those actions, and provide underlying system support for both the interpretation of those actions and the perceivable system response to those actions (which should preserve dramatic probabilities or suggest coherent new ones). In other words, **agency requires the construction of a playable software model of the domain of the fictional world.**"

## The thought experiment that names our exact problem (verbatim)

The paper's objection to defining agency as an audience experience:

> "Imagine you are watching a video of a pre-recorded gameplay session, but you have a controller in your hand, you believe you are playing, and the pre-recorded player is doing everything you wish to do at exactly the moment you believe you are taking the action through the controller. Isn't that agency?"

Their answer is no:

> "our concern is with creation and understanding of playable media. We believe this sort of argument, which rests the weight of the experience on limited, hard-coded options and/or the shallow and fragile Eliza effect, points toward the wrong directions in the design space. It also elides the actual workings of the computational system."

This is a **normative** rejection, not an empirical one. They concede that the experience is subjectively identical and reject it on design-philosophy grounds. Fendt et al. (2012) later ran essentially this experiment and found players indeed could not tell (`game-illusion-of-agency-fendt.md`).

## Findings on Façade (Dow's empirical study)

Three versions: original desktop, voice-controlled desktop, and full augmented-reality ("Holodeck") version with a physical set and head-mounted display.

> "Despite widespread belief that more immersive and realistic games are desirable, players having a greater sense that they are present in a real situation **can be detrimental to agency**. Player expectations of computational models are incorrectly signaled, creating a gulf compared with the actions and responses that are possible."

On Façade's therapy game, where player actions largely do *not* affect the underlying model:

> "Many continued to console, provoke, and otherwise engage Façade's characters during the therapy game, even when their actions were not having an impact on the underlying model and not resulting in a meaningful response from the game. One could say this confirms the power of the Eliza effect as a primary design approach. We disagree. Rather, it shows that audience expectation is still active even after system understanding begins to develop. **Agency becomes part of the expectation, so that even when agency is not occurring, the audience seeks it.**"

Player quote: *"I felt that I could do a lot. I just didn't know what..."*

## Summary claims (verbatim)

> "Agency waxes and wanes during play, but players respond differently if the possibility of agency has already been established earlier in the experience."

> "designers may wish to craft play toward certain types of plan failure and consequences that do not terminate play but allow for the expression of ongoing intention in a continuing fictional world."

## Relevance to companion-eval-platform

1. **The field's canonical definition is explicitly non-operational, and this is the honest headline for the agency dimension.** After surveying every definition, the most-cited paper in the area lands on "when the actions players desire are among those they can take." Measuring that requires knowing what the player *desired* — accessible only by asking them. **The foundational agency literature is subjective by construction.** If we want an objective agency metric we are not adopting one from this field; we are inventing one.

2. **Our platform is an Eliza-effect machine, and this paper explains why that is dangerous rather than free.** An LLM roleplay engine is precisely a "textual transformation device" that suggests dramatic probability and accepts open-ended text — Eliza with a vastly better transformation function. The Eliza effect's failure mode is *fragility*: it holds until expectations are "too greatly violated", then collapses. This predicts our real user-facing failure is not gradual quality decline but **sudden collapse of the fiction** when the model contradicts established world state. That is a rule-adherence violation. **The agency problem and the rule-adherence problem are the same problem viewed from two sides**, which is a strong argument for prioritizing the verifiable-constraint work: it is the tractable face of the same phenomenon.

3. **The SimCity criterion is the closest thing here to an objective agency test, and it is suggestive for us.** "The elements presented on the surface have analogues within the internal processes and data." That is a *checkable structural property*: does the fiction's surface correspond to a persistent underlying state? A system with no world model can only fake it. This points at the same place Fendt's Question 4 does — an agency metric grounded in whether the system *has* and *respects* state, not in whether the user feels it does. Cf. `game-llm-sim-state-prediction.md`: if the model can't track world state, there is no model for the surface to have analogues within, and per this paper agency is impossible in principle rather than merely absent.

4. **"Immersion can be detrimental to agency" is a counterintuitive product warning.** The AR Façade increased presence and *hurt* agency, because it signaled affordances the model couldn't support. Our analogue: the more fluent and human the AI sounds, the wider the player's assumed action space, and the harder the eventual breakdown. **Fluency writes cheques the world model can't cash.** Improving prose quality may actively worsen the agency experience — which, if true, is a genuinely important finding for a platform whose instinct is to optimize prose.

5. **"Agency becomes part of the expectation" cuts against naive engagement metrics.** Façade players kept trying to influence a system that was ignoring them. So *engagement is not evidence of agency* — a user energetically trying to steer a railroaded scene looks identical in telemetry to a user successfully steering a responsive one. Any behavioral proxy for agency must distinguish attempts from effects, which again means measuring the system side (did the state change?), not the user side.

6. **Use this file as the citation for the "no objective agency metric exists" claim.** It is the field's own summary of every definition on offer, and none of them is measurable without asking the player.
