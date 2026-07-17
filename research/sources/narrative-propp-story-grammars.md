---
title: "Propp's Morphology as a Grammar for Generation; story grammars; tagging Propp functions with LLMs"
url: https://drops.dagstuhl.de/storage/01oasics/oasics-vol032-cmn2013/OASIcs.CMN.2013.106/OASIcs.CMN.2013.106.pdf
authors: [Pablo Gervás; (Propp 1928); CEUR authors for LLM tagging]
year: 1928-2025
type: multi-paper capture (formalism + computational reuse + LLM tagging)
accessed: 2026-07-16
topic: narrative-craft
---

# Propp's Morphology & story grammars — structure as a countable checklist

The oldest formalism relevant to our brief, and the one that most directly turns "story structure" into **a finite vocabulary of discrete, taggable events**.

## Propp's formalism

> "Vladimir Propp developed a grammar covering Russian folktales, decomposing stories into an **initial state with characters and a set of narrative functions over states**. Propp showed that approximately **30 narrative functions plus constraints on function ordering** could generate the whole corpus of Russian folktales."

> "From a corpus of over 100 fairy tales, Propp formulated **character functions** (Hero, Villain, Helper, etc.) as well as **temporal functions** (a preparatory action, a complication, the defeat of the villain, etc.)."

**The essential property for us: ~31 functions, in a constrained order, drawn from a CLOSED vocabulary.** Propp's functions include (canonical list, abbreviated): absentation, interdiction, violation, reconnaissance, delivery, trickery, complicity, **villainy/lack**, mediation, counteraction, departure, first function of the donor, hero's reaction, receipt of a magical agent, guidance, **struggle**, branding, **victory**, liquidation of lack, return, pursuit, rescue, unrecognized arrival, unfounded claims, difficult task, solution, recognition, exposure, transfiguration, punishment, wedding.

**→ This is a TAGGING problem, not a rating problem.** "Which function is this beat performing?" is a classification with a closed label set. Classification agreement is typically far higher than Likert agreement. **This is the structural move our platform needs: replace "rate the story structure 1–5" with "tag the beats, then check the sequence."**

## Gervás's computational reuse

> "Propp's semi-formal analysis has often been used as theoretical background for **automated generation** of stories, with its rigorous description of Russian folk tale elements inspiring several story generation systems. Propp's formalism constitutes a **blueprint for a story generation system intended to reproduce a particular model of story while strongly adhering to specific genre and domain conventions.**"

**Modern extensions (Gervás, "Adapting Proppian Morphology for Generating Narrative Structures", ICCC 2025):**
> "Recent extensions to Propp's formalism include **grouping character functions into axes of interest** to cover **long-range dependencies between character functions** and explicitly **adding roles** to capture restrictions on character instantiation."

**→ "Long-range dependencies between character functions" is the structural analogue of our multi-turn problem.** Propp's ordering constraints are *precisely* long-range narrative dependencies — e.g. `villainy` must eventually be answered by `liquidation of lack`; an `interdiction` should be followed by a `violation`. **Unclosed function pairs are countable.**

## LLM tagging of Propp functions — the enabling result

**"Tagging Narrative with Propp's Character Functions Using Large Language Models"** (CEUR Vol-3671, paper 12 · https://ceur-ws.org/Vol-3671/paper12.pdf)

This is the practical unlock: **LLMs can be used to tag narrative text with Propp functions.** If that tagging is reliable, then story-structure analysis becomes a cheap, automated, classification-based pipeline rather than an expert-rubric exercise.

⚠️ **I did not extract this paper's accuracy/agreement numbers.** **Before we build on this, get the tagging reliability figures** — the entire value of the approach rests on whether the tagger agrees with human taggers. If Propp-tagging agreement is itself ~0.3, we've gained nothing and just moved the noise.

## The operationalization for our platform

**Do NOT adopt Propp's 31 folktale functions literally.** They are genre-specific (magical agents, villainy, weddings) and will not fit companion chat, where per note 01's traffic prior the modal session is Friendly Interactions / Casual Greetings / Affection & Comfort — not a quest.

**DO adopt the METHOD:**
1. Define a **small, closed vocabulary of dramatic moves** appropriate to companion/roleplay (e.g.: *offer, complication, revelation, escalation, reversal, callback, resolution, deflection, stall*).
2. **Tag each AI turn** with zero or more moves.
3. Derive metrics from the tag sequence:
   - **move density** (moves per turn) → pacing
   - **move diversity** (entropy over the vocabulary) → is it doing the same thing forever?
   - **unclosed dependencies** (complication introduced but never resolved) → countable
   - **escalation** (is there a monotone-ish rise in stake-bearing moves?) → curve fitting

**Every one of these is arithmetic over a tag sequence.** The only judgment is the tagging step — a closed-set classification, which is exactly the kind of task where agreement is high and where a small fine-tuned model beats a prompted frontier judge (note 01: CharacterRM 0.631 vs GPT-4 0.385; the gain is from *task shape*, not model).

**→ This is the single most important architectural recommendation from this file: MOVE THE JUDGMENT FROM RATING TO TAGGING.** Our α=0.25–0.34 problem is a *rating* problem. Tagging is a different task with a different (and empirically much better) agreement profile. Propp is 1928's proof that narrative admits a closed label vocabulary.

⚠️ **The honest caveat:** we have no evidence yet that *our* proposed move vocabulary would tag reliably. Propp's vocabulary was derived from and validated on a narrow, highly-conventional corpus (Russian folktales) — its tractability may not survive transfer to open-ended companion chat. **Deriving the vocabulary bottom-up from our own traffic (à la StoryER's LDA) is more likely to work than importing one.** The tagging-vs-rating argument is sound in principle; the specific vocabulary is an open research question and **the agreement of our tagger is the thing to measure first.**

## Related

- **Computational Drafting of Plot Structures for Russian Folk Tales** (PMC5005406)
- **Narrative Context Protocol: An Open-Source Storytelling Framework for Generative AI** (arXiv 2503.04844) — modern attempt at a structured storytelling interchange format.
- **Reviewing Propp's Story Generation Procedure in the Light of Computational Creativity** (Gervás, AISB50)

## Validation status

⚠️ **Propp himself: descriptive structuralism from 1928, no reliability statistics, and much criticized** (post-hoc fitting, genre-bound, functions elastic enough to fit anything). **Do not present Propp as validated science.** Its value is existence-proof-of-a-closed-vocabulary, not empirical authority.

⚠️ Gervás's work is generation-focused; **no human evaluation of a Propp-based *metric*.**

⚠️ The LLM-tagging paper is the only empirical link and **its numbers are not captured here.**

## Takeaways for the platform

1. **THE BIG ONE: move the judgment from RATING to TAGGING.** Closed-vocabulary classification has a fundamentally better agreement profile than Likert rating. This is the structural answer to α=0.25–0.34.
2. **Don't use Propp's 31 functions** — genre-mismatched with companion traffic. Use the *method*.
3. **Derive our move vocabulary bottom-up from our own traffic** (pair with StoryER's LDA method) rather than importing a literary one.
4. **Unclosed dependencies (complication → no resolution) are countable** and map to Dramatron's "the stories do not finish."
5. ⚠️ **Measure our tagger's agreement FIRST.** If tagging agreement is also ~0.3, the whole approach collapses and we've learned that cheaply.
6. Propp is an existence proof, not evidence.
