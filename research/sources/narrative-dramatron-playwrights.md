---
title: "Co-Writing Screenplays and Theatre Scripts with Language Models: Evaluation by Industry Professionals"
url: https://arxiv.org/abs/2209.14958
authors: [Piotr Mirowski, Kory W. Mathewson, Jaylen Pittman, Richard Evans]
year: 2023
venue: CHI 2023
type: conference paper / expert user study
accessed: 2026-07-16
topic: narrative-craft
---

# Dramatron — evaluated by 15 professional playwrights & screenwriters

**"The largest expert user study conducted on co-creative authorship to date."** Highly relevant because the evaluators are *dramatic craft professionals*, and their critiques constitute an expert-elicited failure taxonomy for AI storytelling.

Dramatron itself: hierarchical prompting generating **title, characters, story beats, location descriptions, and dialogue** — note that **"story beats" is an explicit generated artifact**, i.e. the system commits to beat structure as the intermediate representation (log line → characters → beat sheet → locations/dialogue).

## Method

> "We illustrate Dramatron's usefulness as an interactive co-creative system with a user study of **15 theatre and film industry professionals**. Participants co-wrote theatre scripts and screenplays with Dramatron and engaged in open-ended interviews."

Participants anonymised p1–p15, paid a consulting fee. Plus: independent reviewers who watched **stagings** of the works (i.e., the output was actually produced on stage). Interviews analysed into **seven themes**.

## The seven themes (verbatim)

> "(1) [Praise for the interactive hierarchical generation in Dramatron]
> (2) Participants identified **inspiration, world building, and content generation** as potential writing applications for [Dramatron].
> (3) Participants noticed various **biases** embedded in the language model.
> (4) [Participants embrace unexpected outputs from the system.]
> (5) Unsurprisingly, participants noticed **logical gaps in storytelling, lack of common sense, nuance and subtext**, [and other fundamental limitations].
> (6) [...]
> (7) Participants were engaged with the tool and eager to provide suggestions for improvement."

## THE FAILURE TAXONOMY — expert-elicited, verbatim

This is the reusable part. Section 5.5, "Fundamental Limitations of the Language Model and of Dramatron":

### 5.5.1 Lack of consistency and of long-term coherence
> "'Keeping dialogue character-based and consistent is most important [...] There is still some difficulty in getting it to stay on track with the context.' (p15). 'I want the characters to be more consistent within themselves' (p12). 'There is a bit of confusion in the logic, gaps in logic [...] It looks like postmodern theatre [...] But in terms of [a play with a given] genre, that has a plot to follow, it is getting confusing' (p11). Participant 7 **'wants to add some stitching between the beats to make them narratively make sense'**."

**→ "stitching between the beats" — beats exist but don't causally connect.** This is Riedl & Bulitko's coherence definition failing: events do not build off prior events. Operationalizable as **inter-beat causal linkage**: does beat *n+1* depend on beat *n*? A sequence of locally-fine, causally-unlinked beats is the signature.

### 5.5.2 Lack of common sense and embodiment
> "Participant 8 observed that 'There are things that it is hard to show on stage – such as a cat. **The system doesn't have an awareness of what is stageable and not stageable**' and p9 noted that when 'interfacing with a story telling AI, the input space is constrained'."

### 5.5.3 Lack of nuance and subtext — **the highest-value theme for us**
> "Participant 3 observed: 'that's a good example of how computers do not understand nuance, the way we see language and can understand it even if it is not super specific'. **'A lot of information, a bit too verbalised, there should be more subtext'** (p6). 'With dialogue in plays, you have to ask yourself two questions: 1) Do people actually speak like that? 2) Are actors attracted to these lines and are these appealing lines to play?' (p7) **'Playwriting is about realistic dialogue... all of the things around subtext. [...] Show, not tell: here we are just telling. Just like in improv: "do not mention the thing". The element in the log line became the central bit in the generation, and that was repetitive'** (p8). Participant 14 concluded that 'AI will never write Casablanca, or A Wonderful Life. **It might be able to write genre boxed storytelling**'."

**→ p8's quote is remarkable and is the best single finding in this file.** Three separate operationalizable claims in one breath:
1. **"Show, not tell: here we are just telling"** — the model states emotional/plot content explicitly instead of implying it.
2. **"Just like in improv: 'do not mention the thing'"** — a *named craft rule* with a literal, countable violation: **the model names the subtext.** This is a lexical/semantic detection problem: is the scene's premise/theme stated verbatim in the dialogue?
3. **"The element in the log line became the central bit in the generation, and that was repetitive"** — **prompt-echo**: the model regurgitates its own premise instead of dramatizing it. **Directly countable as n-gram/semantic overlap between the premise/character-card and the generated dialogue.**

**→ "Do not mention the thing" may be the most operationalizable craft rule in this entire review.** For a companion platform: if the character card says "she is secretly lonely," a good scene partner *plays* lonely; a bad one *says* "I am secretly lonely." **Measurable as premise-to-dialogue leakage: semantic similarity between the character card's latent traits and the literal text of the model's dialogue.** High similarity = telling, not showing. **This is a Tier-A, no-judge, embedding-only metric** and it directly captures a failure mode experts name spontaneously. Strong candidate.

**⚠️ Caveat: the sign of this metric is not obvious.** Some card-to-dialogue overlap is *correct* (persona fidelity requires expressing the card). The claim is not "less overlap is better" monotonically — it's that *literal* restatement of the card's private/latent content is a defect while *behavioral expression* of it is the goal. Distinguishing those two needs care; a naive similarity score would penalize good persona fidelity. **Needs a "which card fields are latent vs. surface" annotation to work.** Flag as promising-but-unvalidated.

### 5.5.4 Lack of a motivation for the characters
> "'**The stories do not finish. The character journeys are not complete.** There is perhaps something missing in the character background [...] **Where is the emotional motivation**, stuff that might [drive the character]'"

**→ "The stories do not finish" and "character journeys are not complete" = no arc closure.** Combined with "where is the emotional motivation" this is the **stakes** deficit named by professionals. Candidate correlate: does any character have a *want* that is stated/implied early and resolved/thwarted later? (Propp-style function completion; see `narrative-propp-morphology.md`.)

### 5.4.2 Generation loops — **countable, and unanimous**
> "**All participants noticed how the system could enter generation loops:** 'I would probably cut a lot of it' (p6) or 'a whole scene about a boiler being broken: yeah' (p8). They sometimes found positive aspects to such loops: 'It is a silly conversation. It is a little repetitive. I like it.' (p6), 'repetition leaves room for subtext' (p12) and enjoyed the glitches (p4, p5) or even made parallels with existing work (p3)."

**→ "All participants" — 15/15.** This is the strongest-consensus defect in the study and it is **already covered by note 03's A2 repetition metrics.** Confirms cross-turn repetition is not just a companion-chat annoyance; it is the #1 expert-visible defect in AI dramatic writing. **Cross-validates note 03's recommendation to make `rep_cross` slope a headline number.**

⚠️ **But note the dissent:** p6, p12, p4, p5, p3 all found *positive* value in the loops ("repetition leaves room for subtext"). **Even the most objective defect in this study is not unanimously bad.** A caution against treating any single metric as monotonically-signed.

### 5.3.1 Too literal and predictable
> "Some participants found the character 'relationships so tight [...]'" — the system outputs are too literal and predictable.

### 5.2.5 Potential of AI as tool for TV screenwriting
> "'If you were able to make an AI to synopsize scripts effectively, you would be valuable to the studio' (p14). **'It is like having a very good dramaturge'** (p10). 'AI can come up with 5 scripts in 5 minutes' (p9). **'Which part of the process is this tool relevant for? Formulaic TV series' (p4, p5).**"

### 5.2.2 Mistakes as gifts (improv framing)
> "'**mistakes are gifts that we can leave for the improvisers**' (p1)."

**→ A professional playwright spontaneously invokes the improv offer frame.** Consistent with the A.L.Ex study: practitioners across theatre/film converge on offer-based vocabulary.

## Headline evaluative finding

> "In the post-interview surveys, **most of the participants felt they did not own the final output.** Playwrights reflected that they wouldn't use Dramatron to write a full play and that **Dramatron's output can be 'formulaic'**, but rather they would use Dramatron for 'world building', for exploring alternative stories by changing characters or plot elements, and for creative idea generation."

## Validation status

- **n = 15 industry professionals**, paid, open-ended interviews, plus staged productions reviewed independently. **Ecologically strong.**
- ⚠️ **Qualitative thematic analysis. NO rubric, NO Likert dimension set, NO inter-rater agreement statistic, NO effect sizes.** The "seven themes" are an author-coded synthesis of interviews; the paper does not report a coding reliability statistic.
- ⚠️ Model is 2022-era (Chinchilla). **The specific quality claims are stale**; the *failure taxonomy* is what transfers.
- ⚠️ Selection: participants are theatre/film professionals, not companion-app users. Their standards (subtext, arc completion, stageability) are far above companion-chat requirements. **Do not assume their priorities match our users'** — note 01's traffic prior (affection/relationships ≈ 15.7%) suggests our users want something quite different from a stageable play.

## Takeaways for the platform

1. **"Do not mention the thing" / show-don't-tell** — the most operationalizable craft rule found in this review. Premise-to-dialogue leakage as a Tier-A embedding metric. Promising; needs latent-vs-surface card annotation to avoid penalizing legitimate persona expression.
2. **"Stitching between the beats"** — inter-beat causal linkage as a coherence correlate.
3. **Generation loops: 15/15 participants.** Strongest-consensus defect; cross-validates note 03's repetition metrics as the highest-value Tier-A item.
4. **"The stories do not finish / character journeys are not complete / where is the emotional motivation"** = arc closure + stakes, named by experts.
5. **Even loops had defenders** — no craft metric is monotonically signed. Keep this in mind before wiring alerts.
6. Expert vocabulary again converges on improv/offer framing ("mistakes are gifts").
