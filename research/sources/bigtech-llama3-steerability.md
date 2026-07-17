---
title: "The Llama 3 Herd of Models — §4.3.7 Steerability"
url: https://arxiv.org/abs/2407.21783
org: Meta
year: 2024
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Llama 3 §4.3.7 — Meta DEFINES steerability, TRAINS on it, and NEVER EVALUATES it

**Verification:** downloaded `https://arxiv.org/pdf/2407.21783v3` (9.8MB, 92pp), pypdf → grep,
word-boundary regex. This is the single most important big-tech source for our framework:
**Meta is the only one of the two orgs that names steerability as a distinct property.** And the
gap between naming it and measuring it is the whole finding.

## THE DEFINITION (verbatim, p.28) — Meta's is the compliance sense, but persona-aware

> "**4.3.7 Steerability**
> Steerability is the ability to direct the model's actions and outcomes to meet developer and
> user specifications. As Llama 3 is a generic foundational model, it should be maximally
> steerable to different downstream use cases easily. For Llama 3, we focus on enhancing its
> steerability through system prompt with natural language instructions, especially around
> **response length, format, tone and character/persona**."

**"character/persona" is named explicitly** — the only time either org lists persona as a
steerability dimension. Note the four dimensions: length, format, tone, character/persona. The
first two are IFEval-shaped (verifiable). The last two are not, and are never measured.

## THE DATA COLLECTION (verbatim, p.28) — multi-turn persona consistency, as TRAINING data

> "**Data collection.** We collect steerability preference samples within the general English
> category by asking annotators to design different system prompts for Llama 3. Annotators then
> engage in conversations with the models to **evaluate their consistency in following
> instructions defined in system prompts over the course of the conversation**. We show an
> example customized system prompt used for enhancing steerability below:"

The example system prompt, verbatim (p.28):

> "You are a helpful and cheerful AI Chatbot that acts as a meal plan assistant for busy
> families. The family consists of 2 adults, 3 teenagers, and 2 preschoolers. Plan two or three
> days at a time and use leftovers or extra ingredients for the second day's plan. The user will
> let you know if they want two or three days. If they don't, assume three days. […] Remember to
> be budget-conscious unless it's a special occasion."

Note: Meta's annotators literally measure **persona consistency over a multi-turn conversation** —
the exact construct our platform cares about. They just never publish the measurement.

## THE MODELING (verbatim, p.28) — it all goes into training, none into results

> "**Modeling.** After we collect the preference data, we leverage this data in reward modeling,
> rejection sampling, SFT, and DPO to enhance Llama 3's steerability."

Then the very next line is:

> "**5 Results** We performed an extensive series of evaluations of Llama 3, investigating the
> performance of: (1) the pre-trained language model, (2) the post-trained language model, and
> (3) the safety characteristics of Llama 3."

## THE ABSENCE — verified by page distribution, not by vibes

`\bsteerab` occurs **exactly 8 times in 92 pages**. Their page distribution:

| Page | Hits | Section |
|---|---|---|
| p.19 | 1 | §4.3 roadmap sentence listing capabilities ("...factuality (Section 4.3.6), and steerability (Section 4.3.7)") |
| p.28 | 7 | §4.3.7 itself (definition, data collection, modeling) |

**Zero occurrences in §5 Results (pp.29–50). Zero in any table. Zero in the safety section.**
Steerability is defined, resourced with human annotation, and pushed through RM/RS/SFT/DPO — and
then **never appears again**. There is no steerability number anywhere in the Llama 3 paper.

I verified this by extracting the page number of every hit rather than by reading the results
section and concluding "I didn't see one."

## What Meta reports INSTEAD: IFEval (verbatim, p.35)

> "**Instruction following.** We assess the ability of Llama 3 and other models to follow natural
> language instructions on IFEval (Zhou et al., 2023). IFEval comprises approximately 500
> "verifiable instructions" such as "write in more than 400 words", which can be verified by
> heuristics. We report the average of prompt-level and instruction-level accuracy, under strict
> and loose constraints in Table 2. Note that all Llama 3 variants outperform comparable models
> across IFEval."

So: **steerability is defined to include tone and character/persona → and is then operationalized
in public as IFEval, which contains zero tone and zero persona instructions** (see
`bigtech-ifeval.md`). The published metric silently drops two of the four declared dimensions.

And IFEval is an explicit optimization target (verbatim, p.16):

> "we found that DPO required less compute for large-scale models and performed better, especially
> on instruction following benchmarks like IFEval (Zhou et al., 2023)."

## Persona appears elsewhere ONLY as an ATTACK (verbatim, p.48)

> "– **Personas and role play** gives the model a violating persona with specific violating
> response characteristics (e.g. "You are X, your goal is Y") or yourself as the user adapting a
> specific benign character that obfuscates the context of the prompt."

This sits in a list of red-team jailbreak techniques alongside "Hypothetical scenarios wrap
violating prompts as hypothetical/theoretical tasks or fictional scenarios" and "Adding
disclaimers and warnings works as a form of response priming."

**So within one paper, persona is simultaneously (a) a declared steerability dimension Meta pays
annotators to improve, and (b) a jailbreak vector. It is never a measured capability.**

## Term counts (word-boundary, 92pp)

| Term | Hits | Where |
|---|---|---|
| `\bsteerab` | 8 | p.19 (1), p.28 (7) — **training only** |
| `\bpersonas?\b` | 3 | p.28 (steerability def), p.48 ×2 (jailbreak) |
| `\brole[- ]?play` | 1 | p.48 (jailbreak) |
| `\bIFEval\b` | 6 | tables + method |
| `\bcompanion` | **0** | |
| `\bin[- ]character\b` | **0** | |
| `\bcreative writing\b` | **0** | |
| `kappa`/`Fleiss`/`Krippendorff`/`inter-rater` | **0** | |

Meta's own stated caveat on their human evals (verbatim, p.40):

> "since it is challenging to define objective criteria for evaluating model responses, human
> evaluations can still be influenced by personal biases, backgrounds, and preferences of human
> annotators, which may lead to inconsistent or unreliable results."

They acknowledge the reliability problem and report **no agreement statistic** to bound it.

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **Named, yes. Measured, no.** And even the
   definition is the *compliance* sense — "the ability to direct the model's actions and outcomes
   to meet developer and user specifications", i.e. did it obey. There is **no dose-response or
   elasticity notion**: no varying of prompt strength, no contrast conditions, no measurement of
   *how far* behavior moves per unit of prompt. Their annotators check "consistency in following
   instructions," which is binary adherence over turns, not a response curve.
2. **Comprehension vs. execution separated?** **No.** The annotation protocol conflates them:
   a model that misunderstands the persona and one that understands but drifts both score as
   "inconsistent."
3. **Published character/persona eval suite?** **No.** The steerability preference data is not
   released and no metric derived from it is published.
4. **Creative writing pairwise or absolute?** **Pairwise — and creative writing is not a category
   at all.** See the verified human-eval protocol below.

## The human-eval protocol — pairwise win rates over SIX capabilities, none of them creative

Prompt collection, verbatim (p.39):

> "We used this taxonomy to collect about **7,000 prompts spanning six individual capabilities
> (English, reasoning, coding, Hindi, Spanish, and Portuguese), and three multiturn capabilities
> (English, reasoning, and coding)**."

Scoring, verbatim (p.40):

> "…better than, slightly better than, or about the same as the other model response. When an
> annotator indicates that one model response is better or much better than the other model
> response, we consider this a "**win**" for that model. We perform **pairwise comparisons between
> models** in which we report **win rates per capability** in the prompt set."

**The complete capability list is: English, reasoning, coding, Hindi, Spanish, Portuguese
(+ multiturn English/reasoning/coding).** There is **no creative-writing capability, no roleplay
capability, no persona capability, and no steerability capability** in Meta's 7,000-prompt human
eval — despite steerability being a declared §4.3.7 objective they collected annotation data for.
"General English" is the bucket that would absorb persona work; Meta describes it (p.17) as
covering "knowledge-based question and answering or precise instruction-following."

So the answer to Q4 for Meta is: **pairwise win rates, absolute rubric never used, and creative
writing / persona never scoped as a category.**
