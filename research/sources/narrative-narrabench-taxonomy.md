---
title: "NarraBench: A Comprehensive Framework for Narrative Benchmarking"
url: https://arxiv.org/pdf/2510.09869
authors: [NarraBench authors]
year: 2025
type: taxonomy / survey paper
accessed: 2026-07-16
topic: narrative-craft
---

# NarraBench — a taxonomy of narrative tasks, with a VARIANCE axis

**The most important methodological find in this review after Johnstone**, because it independently formalizes the exact distinction our platform's core finding forces on us: **which narrative constructs have right answers, and which don't.**

## The taxonomy structure

> "Our taxonomy focuses on two core levels of narrative understanding. The first is a hierarchically arranged set of **fifty narrative aspects** that can be mapped to the **twelve narrative features**... We group these aspects under the **four principal narrative dimensions**... These dimensions form the root of our taxonomy."

**The four principal dimensions** (from Genette 1980 + Herman 2009):
- **story** ("what happened" — Russian formalists / Tomashevsky)
- **discourse** ("how it was told")
- **narration** — "the perspectival dimensions of narrative communication produced by the narrator's voice ('who speaks')"
- **situatedness** — Herman's addition, "captures the **social dimensions of narrative (medium, social context, interactive dimensions)**"

> "Genette then introduced three further terms to capture the relationship between these dimensions, **tense, mood, and voice**... These include aspects of time and the ordering of events (**tense**); the relationship between **eventfulness and description** (**mood**); and aspects related to perspective, such as point of view, dialogue, and focalization (**voice**)."

**→ "Situatedness ... interactive dimensions" is where roleplay lives**, and it is the dimension Genette *didn't* have — added only in 2009. The narratological canon barely covers interactive narrative. Consistent with the emptiness of note 01's Narrative/Story column.

**→ "Mood = the relationship between eventfulness and description"** is a genuinely useful construct for us. **Eventfulness vs description is the purple-prose axis.** A model that generates lush description with no events is scoring high on discourse and zero on story. **That is a ratio of two countable things** — events introduced vs. descriptive tokens — and it's a direct operationalization of the "purple prose" complaint in our brief. **Cheap, judge-light, and I haven't seen it framed this way anywhere else.**

## THE VARIANCE AXIS — the key contribution for us

> "The second level of our taxonomy focuses on **evaluation criteria**. These include textual **scale** (local, global, meso), **mode** (**discrete, progressive, holistic** judgments), and the expected **variance** of potential answers (**deterministic, consensus, perspectival**)."

Table 4 legend: **"D/C/P = deterministic / consensus / perspectival."** Every one of the 50 aspects is tagged with S(cale) / M(ode) / V(ariance).

**→ THIS IS THE FRAMEWORK OUR PLATFORM NEEDS, ALREADY BUILT.**

- **Deterministic** — there is a correct answer. (Did character X appear in scene Y?)
- **Consensus** — no single correct answer, but competent readers converge. (Is this the story's climax?)
- **Perspectival** — **answers legitimately differ by reader, and disagreement is not error.** (Is this ending satisfying?)

**Our α = 0.25–0.34 is not a measurement failure. It is the expected signature of scoring PERSPECTIVAL aspects.** NarraBench's framework says: for perspectival aspects, *low inter-annotator agreement is the correct result*, and chasing higher agreement is chasing an artifact.

> "[We highlight] **perspectival aspects of narrative, that is, aspects [for which there is no single correct answer]**"
> "...**perspectival alignment in benchmark development**."

**→ This reframes our entire project's headline finding.** We currently read α=0.25–0.34 as "humans can't agree on roleplay quality, so aesthetic scores are unstable." NarraBench's framing is sharper and more defensible: **we were measuring perspectival aspects with an instrument that assumes consensus.** The fix is not a better judge — it's **to sort our dimensions by variance class first**, then apply the right instrument to each:
- deterministic → automated check, expect high agreement, **regression-detect on it**
- consensus → panel/aggregation, expect moderate α, usable with volume
- perspectival → **do not score for a leaderboard.** Report *distributions*, model *reader segments*, or drop.

**This is a better story than "humans disagree, so we use objective proxies."** It says: *we classified our dimensions by variance class and instrumented each appropriately.* That's a methodological contribution, not a workaround. **Recommend adopting the D/C/P tag as a required field on every dimension in our taxonomy.**

## The coverage finding

> "[We find] that only **27% of narrative tasks are well captured [by existing benchmarks]**"
> "...existing benchmarks... satisfy **≈27% of the NARRABENCH taxonomy**... **This gap suggests opportunities [for new benchmarks]**"

**→ 73% of narrative understanding is not covered by existing benchmarks.** Independent, quantified confirmation of note 01 §5's "what nobody measures well" — now with a number, from a systematic taxonomy rather than our own gap analysis.

## Caveats (the authors', verbatim)

> "[our] reliance on public datasets may bias coverage toward [certain areas]"
> "rather than empirical, its coverage and weighting [are theoretical]"

⚠️ **The authors concede the taxonomy is theoretical, not empirical** — the 50 aspects are derived from narratology (Genette, Herman, Tomashevsky), not discovered from data. Contrast StoryER's LDA-derived aspects (`narrative-storyer-doc-re3.md`), which are bottom-up. **Both approaches have a place: use NarraBench's D/C/P axis (a methodological tool) but derive our actual dimension list bottom-up from our traffic.**

> "This gap leaves open the question of whether [findings transfer beyond] English."

⚠️ **English-only.** Note 01 §5.8 warns dimensions must be re-validated per language.

⚠️ **NarraBench is about narrative UNDERSTANDING (comprehension tasks over existing texts), not narrative GENERATION or interactive partnership.** The taxonomy classifies "can the model answer questions about this story," not "is the model a good scene partner." **The D/C/P axis transfers; the 50 aspects largely do not.**

## Validation status

- ⚠️ **No human agreement statistics for the taxonomy itself.** The D/C/P labels are the authors' judgments — ironically, an unvalidated classification of what is and isn't agreeable.
- The 27% coverage figure is a mapping exercise against the authors' own taxonomy — **circular to a degree** (coverage is relative to a theoretical scheme that the authors chose).
- Value is **framework and vocabulary**, not measurement.

## Takeaways for the platform

1. **ADOPT THE D/C/P VARIANCE TAG** as a mandatory field on every dimension in our taxonomy. This is the cleanest framework available for the judge-free/aesthetic split the brief asks for.
2. **Our α=0.25–0.34 is reframed:** not "humans can't agree on quality" but "we scored perspectival aspects with a consensus instrument." Sort by variance class, instrument accordingly. **Better, more defensible story.**
3. **Perspectival dimensions should not be leaderboard axes.** Report distributions or drop them.
4. **"Mood = eventfulness vs description"** is a novel, cheap operationalization of the purple-prose failure: ratio of events introduced to descriptive tokens.
5. **73% of narrative tasks are uncovered by existing benchmarks** — quantified confirmation of note 01 §5.
6. ⚠️ Taxonomy is theoretical and English-only; it's about *understanding*, not partnership. Take the axis, not the aspects.
