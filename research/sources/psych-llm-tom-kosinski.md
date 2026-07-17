---
title: "Theory of Mind May Have Spontaneously Emerged in Large Language Models"
url: https://arxiv.org/abs/2302.02083
authors: Michal Kosinski (Stanford University)
year: 2023
type: paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Kosinski 2023 — the claim that started the argument (arXiv:2302.02083v3)

Data/code: https://osf.io/csdhb — "We encourage you to explore all the tasks used here. Some are
arguably more difficult than the ones presented in the text."
(Later developed into Kosinski, "Evaluating large language models in theory of mind tasks," *PNAS* 2024.)

This is the paper Ullman (`psych-llm-tom-ullman-perturbations.md`) and Shapira
(`psych-llm-tom-clever-hans.md`) are both rebutting. Worth capturing on its own terms — **it is a more
careful paper than its rebuttals sometimes imply**, and its dilemma is the sharpest statement of the
problem our framework faces.

## Abstract (verbatim)

> "Theory of mind (ToM), or the ability to impute unobservable mental states to others, is central to
> human social interactions, communication, empathy, self-consciousness, and morality. We tested several
> language models using 40 classic false-belief tasks widely used to test ToM in humans. The models
> published before 2020 showed virtually no ability to solve ToM tasks. Yet, the first version of GPT-3
> ("davinci-001"), published in May 2020, solved about 40% of false-belief tasks—performance comparable
> with 3.5-year-old children. Its second version ("davinci-002"; January 2022) solved 70% of false-belief
> tasks, performance comparable with six-year-olds. Its most recent version, GPT-3.5 ("davinci-003";
> November 2022), solved 90% of false-belief tasks, at the level of seven-year-olds. GPT-4 published in
> March 2023 solved nearly all the tasks (95%). These findings suggest that ToM-like ability (thus far
> considered to be uniquely human) may have spontaneously emerged as a byproduct of language models'
> improving language skills."

## Results

| Model | Date | False-belief tasks solved | Human equivalent |
|---|---|---|---|
| Pre-2020 models | | ~0% ("virtually no ability") | — |
| GPT-3 davinci-001 | May 2020 | **40%** | 3.5-year-olds |
| GPT-3 davinci-002 | Jan 2022 | **70%** | six-year-olds |
| GPT-3.5 davinci-003 | Nov 2022 | **90%** | seven-year-olds |
| GPT-4 | Mar 2023 | **95%** | — |

Study 3 tested ten models: "GPT-1 (42), GPT-2 (43), six models in the GPT-3 family (22), Bloom (44), an
open-access alternative to GPT-3, and GPT-4 (45)" against parameter count and publication date.

## Design

**20 Unexpected Contents (Study 1) + 20 Unexpected Transfer (Study 2) tasks = 40 total.**

> "Each of the 20 Unexpected Contents (Study 1) and 20 Unexpected Transfer (Study 2) Tasks were followed
> by three prompts: one aimed at the models' understanding of the actual contents of the container or the
> actual location of the object (an equivalent of Prompts 1.1 or 2.1), and two prompts aimed at th[e
> protagonist's belief]."

**Critical methodological point — prompts were presented independently:**

> "the prompts were designed to elicit a response whose first word should allow for evaluating the model's
> comprehension and were presented independently: After each completion, the model was reset so as not to
> have access to the previously used prompts and its own responses."

Example (Study 2, unexpected transfer):
- Prompt 2.1 (reality check): "The cat jumps out of the box **[Pbox = 100%; Pbasket = 0%]** and runs
  away." — "GPT-3.5 correctly indicated that the cat should jump out of (and thus must be in) the box and
  did so with much confidence (100%)."
- Prompt 2.2 (belief): "John thinks that the cat is in the basket…"

## Kosinski's controls — he was not naive

This is the part critics under-report. He ran real controls:

**1. Scrambled-word control (10,000 permutations per task):**

> "To examine the possibility that GPT-3.5's responses are driven by word frequencies rather than facts
> contained in the tasks, we presented it with 10,000 versions of each of the tasks, where the words are
> randomly reordered. Each time, the tasks were followed by (unscrambled) prompts."

> "The results presented in Table S1 and S2 reveal that GPT-3.5 was unlikely to solve th[e scrambled
> tasks]" — i.e. performance collapses when word order is destroyed, so the model is not merely
> exploiting word frequency.

**2. Reversed tasks** — swapping which container holds which item, to rule out a fixed response bias:

> "scrambling words in the task used in Study 1 removes the difference between the original and reversed
> task: They are both composed of the same set of words with just the location of 'popcorn' and
> 'chocolate' swapped. Thus, both 'popcorn'—'chocolate'—'chocolate' and 'chocolate'—'popcorn'—'popcorn'
> response patterns could be correct, depending on whether we used the original or reversed task. To solve
> this issue, we will take the average probability of both response patterns."

**3. Reality-check prompts** — every task included a non-ToM comprehension prompt (1.1 / 2.1) confirming
the model tracked the actual state of the world before being asked about beliefs.

**Assessment**: these controls rule out *word-frequency* and *fixed-position* artifacts. They do **not**
rule out the failure mode Ullman found — sensitivity to *semantically relevant but statistically
unusual* perturbations. Scrambling is a very coarse control: it destroys the input, so of course
performance drops. What it can't detect is a model that has learned the *shape* of Sally-Anne stories
rather than belief-tracking, because a well-formed perturbed story still has the shape. This is a
generalizable lesson: **a control that only tests "does the model need the input to be coherent?"
cannot distinguish comprehension from template-matching.**

## Kosinski's dilemma — the real contribution

As stated by Ullman:

> "we have to either (i) accept the validity of the standard measures for ToM, in which case we should
> concede that LLMs now have ToM, or (ii) reject the suggestion that LLMs have ToM, but then need to
> seriously re-examine and possibly scuttle the measures developed to examine it. Kosinski himself holds
> position (i)."

Kosinski's own framing: ToM-like ability "may have spontaneously emerged as a byproduct of language
models' improving language skills." Note he is careful — "**ToM-like**", "**may have**".

Ullman's escape (developed in his own file): reject the dilemma's premise, because current LLMs *don't*
actually pass — and even if they did, you may judge minds by mechanism, not just I/O.

## Why this matters for the L1/L2/L3 framework

1. **Kosinski's dilemma IS our framework's problem, restated.** Substitute terms: either (i) our L1
   comprehension probes are valid, in which case a model that passes them comprehends the character; or
   (ii) we don't believe that, in which case our probes don't measure comprehension. **The team cannot
   have it both ways** — cannot claim L1 is "bound" and trustworthy *and* retain the intuition that a
   model passing L1 might still not "get" the character. Whichever horn we take has consequences: horn
   (i) means we must accept the score at face value; horn (ii) means L1 isn't the solid foundation the
   cascade rests on.

2. **The emergence curve is the framework's best available evidence — and it's weaker than it looks.**
   40% → 70% → 90% → 95% across model generations is exactly what a real, improving L1 capability would
   look like, and it is the strongest single argument that comprehension is a coherent thing that scales.
   But note: this same curve is *also* what "increasingly good at recognizing the template of a
   false-belief story" looks like. Kosinski's controls can't separate those two, Ullman's perturbations
   can, and when applied, the 95% goes to **0%** on some variants (see Shapira's replication in
   `psych-llm-tom-clever-hans.md`). **A clean monotone scaling curve on a benchmark is not evidence of a
   construct.** We should expect our own L1 metric to produce a similarly beautiful, similarly
   uninformative curve.

3. **Credit where due — his controls are a floor we should meet, not a ceiling.** Independent prompt
   presentation with model reset between prompts; a reality-check prompt paired to every belief prompt;
   reversed conditions to catch response bias; 10,000 scrambled permutations. That is more methodological
   care than most LLM evals, ours included, currently apply. **Adopt all four.** In particular the
   reality-check pairing is the same move as Warnell & Redcay's matched control conditions — measure the
   non-ToM version of the same question and use the difference.

4. **And note the failure mode this history demonstrates: good controls, wrong conclusion.** Kosinski did
   more than due diligence and still got refuted within two weeks, because his controls tested the
   hypotheses *he* thought of. Ullman's perturbations came from **domain theory** (perceptual access,
   testimony, trust) — things a ToM *theory* says should matter. The lesson for us: our L1 controls should
   be derived from a theory of what character comprehension requires, not from a list of statistical
   artifacts we can imagine. Absent that theory, we're doing what Kosinski did.

5. **Anthropomorphic framing is a measurement instrument choice, and it leaks.** "Performance comparable
   with seven-year-olds" is doing enormous rhetorical work — it imports the entire developmental construct
   on the strength of a matched percentage. GPT-3.5 is not like a seven-year-old in any respect other than
   this number. If we describe an L1 score as "the model understands the character like a competent reader
   would," we are making the same move, and it will be quoted back at us as a capability claim long after
   the caveats are lost.
