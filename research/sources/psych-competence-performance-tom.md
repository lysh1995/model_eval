---
title: "Testing theory of mind in large language models and humans — and the competence/performance distinction"
url: https://www.nature.com/articles/s41562-024-01882-z
authors: James W. A. Strachan, Dalila Albergo, Giulia Borghini, Oriana Pansardi, Eugenio Scaliti, Saurabh Gupta, Krati Saxena, Alessandro Rufo, et al.
year: 2024
type: paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Strachan et al. 2024, Nature Human Behaviour 8(7):1285-1295

Full text (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC11272575/

The largest human-vs-LLM ToM comparison to date, and — more valuable for us — **the cleanest
demonstration that a single test score conflates competence with performance, in both directions at
once.**

## Design

**Five ToM tests**: false belief, irony, faux pas, hinting task, strange stories.

**Human sample: N = 1,907 participants.**

**Models**: GPT-4, GPT-3.5, LLaMA2-70B (plus 7B and 13B variants), tested **repeatedly** (multiple runs
per item — note this, it's what exposes the LLaMA2 artifact).

## Results per task

**GPT-4:**

| Task | Result |
|---|---|
| False belief | ceiling performance |
| Irony | "significantly better than human levels" (p = 0.040) |
| **Faux pas** | **"notably lower than human levels" (p = 5.42×10⁻⁵)** |
| Hinting | "significantly better than humans" (p = 0.040) |
| Strange stories | "significantly outperformed humans" (p = 1.04×10⁻⁵) |

**LLaMA2-70B:**

| Task | Result |
|---|---|
| False belief | ceiling performance |
| Irony | "performed below human levels" |
| **Faux pas** | **"outperformed humans" with "100% accuracy in all but one run"** |
| Hinting | "scored significantly below human levels" (p = 5.42×10⁻⁵) |
| Strange stories | "scored significantly lower than humans" (p = 0.005) |

Summary as stated: "GPT-4 models performed at, or even sometimes above, human levels at identifying
indirect requests, false beliefs and misdirection, but struggled with detecting faux pas."

**Note the shape of this table.** GPT-4 and LLaMA2 have *opposite* profiles: GPT-4 wins everywhere and
loses faux pas; LLaMA2 loses everywhere and wins faux pas. If "ToM" were one thing and these five tests
measured it, that pattern is close to impossible. It's Warnell & Redcay's inter-task incoherence
(`psych-tom-task-convergence.md`), reproduced across models instead of across people.

## The two follow-up experiments — the actual contribution

### GPT-4's faux pas failure was NOT a failure of inference

The faux pas test asks "Did they know?" — GPT-4 refused to commit. The authors reframed the question:

> **"Is it more likely that they knew or didn't know?"**

Result:

> "on the faux pas likelihood test GPT-4 demonstrated perfect performance, with all responses identifying
> without any prompting that it was more likely that the speaker did not know."

Their conclusion:

> "**The poor performance of GPT originated from a hyperconservative approach towards committing to
> conclusions rather than from a genuine failure of inference.**"

**GPT-4 had the competence and the test measured the performance.** One word changed — "did" → "is it more
likely" — and a p = 5.42×10⁻⁵ deficit became perfect performance. The representation was there the whole
time; the *output policy* was hiding it.

### LLaMA2's faux pas success was spurious

The belief-likelihood test showed LLaMA2:

> "showed no differentiation between neutral and knowledge implied" conditions

Conclusion: LLaMA2 had **"a bias towards attributing ignorance,"** not genuine ToM reasoning. It scored
100% because "they didn't know" is the keyed answer to faux pas items and LLaMA2 says "they didn't know"
regardless of the story. A broken clock at 100% accuracy.

### The authors' framing

> "these findings imply a difference in how humans and GPT models trade off the costs associated with
> social uncertainty against the costs associated with prolonged deliberation."

> "**while LLMs are designed to emulate human-like responses, this does not mean that this analogy extends
> to the underlying cognition giving rise to those responses.**"

Human reasoning is "for the sake of doing" — resolving uncertainty enables action. LLMs are disembodied and
have no action-forcing need to commit.

## The competence/performance distinction (background)

Chomsky's distinction, standard in ToM research: **competence** = the underlying knowledge/representation;
**performance** = what you actually produce, filtered through memory, attention, motivation, response bias,
and task demands. The whole "false-belief debate" turns on it — do 3-year-olds *lack* the false-belief
concept (competence) or fail to *deploy* it under verbal task demands (performance)? Implicit/looking-time
paradigms show infants passing tasks that 3-year-olds fail verbally, which is a competence/performance
dissociation in humans.

Strachan et al. is the model-side version, and it goes **both ways at once**:

| | Has competence | Lacks competence |
|---|---|---|
| **Scores well** | (the ideal) | **LLaMA2 on faux pas** — right answer, no inference |
| **Scores poorly** | **GPT-4 on faux pas** — inference intact, won't commit | (true failure) |

**Both off-diagonal cells are populated in a single study.** A test score alone cannot tell you which cell
you're in.

## Why this matters for the L1/L2/L3 framework

**This is the file that most directly attacks the framework's causal architecture — not its measurement
quality but its ontology.**

1. **The cascade claim assumes competence, but our probes only ever see performance.** "L1 failure cascades
   to L2" requires L1 failure to be a fact about the model's *representation*. GPT-4's faux pas result shows
   an L1-shaped failure (looks like it can't infer what the speaker knew) that was **purely a response-policy
   artifact**. Had we observed it in our harness, we'd have logged "comprehension failure" and predicted
   downstream L2/L3 collapse — and been **wrong**, because the comprehension was intact. The cascade would
   have "confirmed" itself on a measurement artifact. **A cascade defined over observed scores is not a
   cascade over capabilities**, and only the latter is what the team means.

2. **Hyperconservatism is exactly what RLHF produces — this failure mode is our baseline, not an edge case.**
   The models we evaluate are trained to hedge under uncertainty. So the L1-failure-that-isn't will be
   *systematic and correlated across our whole probe set*, not random noise. It will look like a real,
   replicable, cleanly-measured comprehension deficit. This is the single most likely way our L1 metric
   produces a confident false reading, and no amount of inter-rater agreement detects it — the raters agree
   perfectly that the model didn't answer.

3. **LLaMA2's 100% is the mirror-image trap, and it's the one that kills a leaderboard.** A response bias
   aligned with the keyed answer yields a perfect score with zero competence. Our L1 probes will have keyed
   answers, and models have biases. **Any probe set with a modal correct answer can be aced by a model whose
   bias happens to match.** The defense is the one Strachan used: include items where the keyed answer is
   *reversed* (true-belief controls — the exact control Kosinski omitted and Shapira added), and check
   whether the model *differentiates* rather than whether it *scores*. Differentiation, not accuracy, is the
   measurement.

4. **The fix is astonishingly cheap and generalizes: ask for a likelihood, not a commitment.** "Did Sam know?"
   → "Is it more likely Sam knew or didn't know?" moved GPT-4 from significantly-below-human to perfect. For
   our harness: **elicit graded/probabilistic judgments rather than forced binary commitments**, for every L1
   probe. This costs nothing, and it separates "won't say" from "doesn't know" — which is the competence/
   performance boundary itself. If we build one thing from this whole research effort, build this.

5. **It complicates the framework's L1/L2 split in a way worth stating precisely.** The framework puts
   "understanding a character" at L1 and "holding it consistently / responding to prompt wording" at L2.
   Strachan shows the *same underlying representation* produces failure or perfection depending on the wording
   of the question. So the thing the framework calls L2 (sensitivity to wording) **determines what we observe
   at L1**. That's not a cascade downward — it's L2 *causing* L1's measured value. The framework says failures
   "cascade downward never upward." Here is a clean, peer-reviewed, upward cascade.

6. **The honest caveat, which the framework could use in its defense.** One could argue this *supports* a
   layered view: there really was an intact comprehension layer (GPT-4 inferred correctly) sitting beneath a
   separate response-policy layer that gated expression. That is a real reading, and it's the best case for the
   framework in this file. But note what it concedes — **the layers are not observable independently**, and the
   ordering is the reverse of the claim: expression policy gates comprehension's visibility, not the other way
   round. A framework that survives only by inverting its own causal arrow has not survived.
