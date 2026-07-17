---
title: "Designing and Evaluating Dialogue LLMs for Co-Creative Improvised Theatre"
url: https://arxiv.org/pdf/2405.07111
authors: [Boyd Branch, Piotr Mirowski, Kory Mathewson, Sophia Ppali, Alexandra Covaci]
year: 2024
type: conference paper (arXiv)
accessed: 2026-07-16
topic: narrative-craft
---

# Co-Creative Improvised Theatre with LLMs (A.L.Ex / Improbotics, Edinburgh Fringe)

**The only source found where professional improvisers evaluate an LLM as a SCENE PARTNER**, in live performance, over a month-long run at the Edinburgh Festival Fringe. Unusually valuable: the failure vocabulary comes from practitioners who have precise technical language for exactly the constructs we're trying to measure.

Setup: an LLM ("A.L.Ex") either drives a **Robot** (AI controls a robot on stage) or feeds lines to a human actor (**Cyborg**). Human-in-the-loop curator selects from generated lines on a tablet.

## The practitioner failure vocabulary (verbatim, from performer free-text responses)

These are the money quotes. **Professional improvisers, unprompted, name our exact failure modes:**

> "**He makes it difficult to yes and**"

> "**Lack of complete collaboration and 'yes, and'**"

> "**Can be tough to move the scene on**"

> "It was a bit of a slog. A.L.Ex did produce some nice moments with the performers but felt **majority of the time was not giving performers much to work with in regards to funny lines or lines to progress the story**."

> "[The AI's responses] elevated the scene. **Less for when lines generated were fairly generic** or [when] the language model did not return a response"

> "**Too many lines generated, not allowing scene to build.** Careful selection needed by the person holding the tablet."

> "There was much more **justifying** of A.L.Ex's lines in this show due to the increased **non-sequiters or odd replies, statements**"

> "**Like doing long form with a 5 year old**"

**→ "not giving performers much to work with... lines to progress the story" is the *offer-generation deficit* stated by a professional.** The complaint is not that the AI is out of character or incoherent — it's that **it doesn't hand you anything to build on.** That is the wimping failure (accept-without-and), observed in the wild, by experts, and it is invisible to every dimension in note 01's table.

**→ "He makes it difficult to yes and" is the inverse framing and is even more useful:** the AI's turns are hard for a *human* to accept-and-build from. This suggests a measurable: **the offer-affordance of the AI's turn** — does it leave the partner something to work with? Not "is it good", but "is it *build-on-able*".

## Status — a live, observed instance

> "I had to adapt the character I was playing in the dating scene. **I came on as a high status character but then had my status lowered by a comment by A.L.ex. It reminded me in the importance to be able to adapt status as an improviser. Be aware of it.**"

**→ Direct empirical support for status transactions as a real, salient, in-the-moment dynamic** that practitioners actively track. A model *can* execute a status move (it lowered the human's status). The question our platform should ask is whether it does so *deliberately and appropriately* — status moves as a countable event class.

## The burden-shifting finding — the most important structural insight here

Multiple performers describe having to do the AI's narrative work for it:

> "I had to have more of a mind on **plot** and keeping the scenes grounded in the **reality we had created**."

> "I had to do more on **plot, relationship and justifying**."

> "I think sometimes people would have to **justify** what A.L.Ex had said in the scene depending on how the human delivered the lines. Which can sometimes create great moments or slight awkwardness"

> "The **justifying** of the lines meant as performers we had to be increasingly on the same page with each other to justify what A.L.Ex said in context of the scene / show."

**→ THIS IS THE KEY FINDING FOR OUR PLATFORM.** The AI's narrative deficit is **absorbed by the human partner**, who compensates by doing extra plot work and "justifying" (retroactively rationalizing the AI's non-sequiturs into the fiction). **The scene can look fine while the human is carrying it.**

**Implication: per-response quality metrics will systematically miss this.** If we score the AI's turns, a well-justified non-sequitur looks like a successful beat. The cost is paid on the *human's* side of the ledger. **The measurable is the user's compensatory labor, not the model's output quality** — which is a *user-side* metric, and we currently have none.

**Candidate objective correlates of burden-shifting:** rate at which the user re-establishes/repairs facts, user turn length growth over a session, rate of user turns that restate context, user-initiated topic repair. **All judge-free, all computable from a transcript, all invisible to model-side scoring.** This pairs directly with the user-re-assertion idea in `narrative-yes-and-vickers.md`.

## Audience survey results (quantitative)

Q12 (109 responses) — "As a performer, A.L.Ex (The robot/AI) appeared:" (0–100 scale)

| Attribute | Score |
|---|---|
| machine like | 65.69 |
| human like | 28.78 |
| artificial | 60.39 |
| lifelike | 29.76 |
| to communicate naturally | 34.23 |
| to communicate unnaturally | 56.35 |

Q10 — audience stance toward A.L.Ex (counts):
| Response | n |
|---|---|
| Rooting for A.L.Ex to succeed. | 32 |
| Neutral or indifferent to A.L.Ex. | 24 |
| Rooting for the humans to outperform A.L.Ex. | 16 |
| Rooting for A.L.Ex to outperform the humans. | 10 |
| Empathising and caring about A.L.Ex. | 7 |
| Something else. | 8 |
| Forgetting A.L.Ex was a robot. | 4 |
| Rooting for A.L.Ex to fail. | 2 |

**The critical number (verbatim):**
> "Q14 (100 responses) asked if the AI's responses appeared to be 'similar to a human' (avg: 53) and 'motivated toward mutual benefit with other actors' (avg: 64). Of note is that despite the appearance of some originality, positive intent, and degree of human-like response, in the context of performance, **the AI generally still presented machine-like responses perceived as 'ignorant of the scenes' (avg: 76)**."

**→ "ignorant of the scenes" scores 76 — the HIGHEST of any negative attribute, and higher than "machine like" (65.69).** The dominant audience-perceived failure is **not** that it sounds robotic — it's that **it doesn't know what scene it's in**. Scene-awareness, not voice, is the bottleneck. This is a strong external validation that our taxonomy is measuring the wrong thing: we score voice/persona (which audiences rate ~53–65) while the actual failure is situational/narrative (76).

> "more than half reported that the AI appeared **'responsive to what was happening on stage'**, with nearly half reporting responses appeared 'unique' and to have their own 'style'."

⚠️ **Note the tension:** >50% said "responsive to what was happening on stage" while 76 avg said "ignorant of the scenes". **Local responsiveness ≠ scene comprehension.** The model tracks the last utterance but not the scene. This is precisely the "mirroring" complaint — reactive coupling to turn *t−1* without a model of the *scene*. **Measurable: does the response condition on the scene state, or only on the previous turn?** (An ablation: truncate context to only the last turn — if output barely changes, the model was only mirroring. **This is a clean, judge-free probe and it's cheap.**)

## The authors' own framing (verbatim)

> "By its nature, improvised theatre presents a difficult problem for conversational AI (Martin and others, 2016): **the roles for characters are emergent and based on shared mutual understanding of complex social structures and norms. Theatre scenes have both tacit and explicit rules of engagement.** Subsequently, attempting to build a system that can shift between any given emergent situation is still beyond the capacity of publicly available text-only chatbots."

On the "Speed Dating" game:
> "A human improviser in the same situation is capable of quickly adapting their behavior to the offers made by the various dates, in turn revealing various aspects of their own character over time, which eventually broadcast the unique likes and dislikes that one of the ensemble of dating characters will match with... **We observed that the AI could not convincingly provide consistent dating criteria.** Instead, the success of the game for the audience simply depended on how the Robot responded to the outlandish offers being made by the human improvisers."

On the "Wedding Speech" game:
> "[The game] tested **how well the AI would be able to take disparate threads of a potential story and weave them together into a coherent as well as entertaining speech**."

**→ "take disparate threads and weave them together" = reincorporation as a designed test.** This is a directly stealable probe design: seed k independent elements across a session, then create a moment that demands synthesis, and count how many of the k are reincorporated. **Bounded [0,k], real denominator, no judge.**

## Positive findings (what the AI was good at)

> "The surprises!" / "The word play and puns. The fact it could out rap me. Plus even the unrelated, most out of context lines, could be used in a humorous way" / "The change in energy in the scene" / "It helped shape the story or take it into directions I wasn't expecting! **But that is also due to the human selecting the lines**" / "Pushed me to take more risks"

⚠️ **Note the confound flagged by the performer themselves:** "that is also due to the human selecting the lines." **The human-in-the-loop curator is a selection filter that inflates apparent AI quality.** Any eval with a human picking from k candidates measures `max over k`, not the model's expected output. Relevant to our design: **best-of-k is not the production distribution.**

> "Turn-taking remains a difficult challenge for performing with AI."

## Validation status

- **Real deployment**, month-long, Edinburgh Fringe. Ecological validity is high.
- Audience surveys: n≈100–109 per question, 0–100 attribute ratings.
- Performer feedback: **free-text, qualitative, small n (cast-sized), no coding scheme, no agreement statistics.**
- ⚠️ **No dimension set, no rubric, no IAA, no per-turn annotation.** The performer quotes are *unstructured testimony*, not measurements. Their value is **hypothesis-generating vocabulary**, not evidence of effect sizes.
- ⚠️ Confounds: speech recognition errors, human curator selection, delay/latency. The authors are explicit that ASR errors contaminated the AI's inputs. **Do not read the negative results as a clean measurement of LLM improv ability.**

## Takeaways for the platform

1. **"Ignorant of the scenes" (76) beats "machine like" (65.69) as the dominant perceived failure.** External evidence that scene/narrative comprehension — not voice — is the bottleneck. Our taxonomy is weighted backwards.
2. **Burden-shifting is the central mechanism to measure:** the human silently absorbs the AI's narrative deficit. Measure the *user's* compensatory labor (re-assertion, repair, restating context), not just model output.
3. **"Not giving performers much to work with"** = offer-affordance deficit. Candidate dimension: is the AI's turn *build-on-able*?
4. **Local responsiveness ≠ scene awareness.** Cheap probe: truncate context to last turn; if output is unchanged, the model was mirroring.
5. **The Wedding Speech design is a stealable reincorporation probe** (seed k threads, force synthesis, count recalls).
6. **Best-of-k with a human curator inflates quality** — beware in our own harness design.
7. Practitioner vocabulary (yes-and, justifying, status, offers) is precise and consistent with Johnstone — the constructs transfer to LLM evaluation intact.
