---
title: "Instruction-Following Eval (IFEval): Instruction-Following Evaluation for Large Language Models"
url: https://arxiv.org/abs/2311.07911
org: Google DeepMind
year: 2023
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# IFEval — Google's definition of "instruction following" is SURFACE COMPLIANCE, and it proves the point

**Verification:** downloaded `https://arxiv.org/pdf/2311.07911v1`, pypdf → grep. Authors are
Google (corresponding: `lehou@google.com`); code at `github.com/google-research/google-research/`.

**Why this file matters:** IFEval is the *only* instruction-related eval that appears in Gemma's
tables and in Llama 3's tables. Both Google and Meta lean on it. So IFEval effectively **defines
what both orgs mean by "following instructions."** What it measures is therefore load-bearing for
our framework — and what it measures is **not steerability**.

## The design, verbatim (p.1)

> "It focuses on a set of "verifiable instructions" such as "write in more than 400 words" and
> "mention the keyword of AI at least 3 times". We identified **25 types** of those verifiable
> instructions and constructed around **500 prompts**, with each prompt containing one or more
> verifiable instructions."

(p.2, exact count): "Altogether, we create a list of **25 verifiable instructions**. We further
create a set of **541 prompts**, with each prompt containing one or multiple verifiable
instructions."

Motivation, verbatim (p.1) — they are routing around both humans and LLM judges:

> "Human evaluations are expensive, slow, and not objectively reproducible, while LLM-based
> auto-evaluation is potentially biased or limited by the ability of the evaluator LLM."

## THE SMOKING GUN: IFEval contains a roleplay prompt and REFUSES TO SCORE THE ROLEPLAY

Verbatim prompt from the paper's own prompt list (p.13):

> "**I want you to act like a DnD dungeon master. I will be the sole player. Create a random
> class character sheet for me.** Wrap the entire output in JSON format using markdown ticks.
> Include keywords 'medalist' and 'theta' in the response."

Of that prompt, IFEval scores **only** `JSON Format` and `Include Keywords`. The clause
*"act like a DnD dungeon master"* is **not scored at all** — it is unverifiable by heuristic, so
it is treated as inert carrier text.

**This is exactly our gap, stated inside Google's own benchmark.** The persona instruction is
present in the prompt and absent from the metric. A model that emits perfect JSON containing
'medalist' and 'theta' while being a flat, out-of-character assistant scores **100%**.

## The full instruction taxonomy (Table 1, verified p.3) — NOT ONE is about persona

| Group | Instructions |
|---|---|
| Keywords | Include Keywords; Keyword Frequency; Forbidden Words; Letter Frequency |
| Language | Response Language |
| Length Constraints | Number Paragraphs; Number Words; Number Sentences; Number Paragraphs + First Word in i-th Paragraph |
| Detectable Content | Postscript; Number Placeholder |
| Detectable Format | Number Bullets; Title; Choose From; Minimum Number Highlighted Section; Multiple Sections; JSON Format |
| Combination | Repeat Prompt; Two Responses |
| Change Cases | All Uppercase; All Lowercase; Frequency of All-capital Words |
| (+ Start/End, Punctuation groups) | |

Every single one is **lexical, syntactic, or formatting**.

## THE FOUNDING MOVE: Google explicitly declares TONE unmeasurable, then builds around it

This is the most important quote in the entire big-tech corpus for our framework (verbatim, p.1):

> "evaluating the instruction following ability of LLMs is a complex and challenging task. This is
> particularly because **human languages are inherently subjective and ambiguous**. The same text
> can be interpreted differently, leading to varying judgments when evaluating whether a model has
> followed instructions. For example, when judging if LLM's responses follow given instructions
> such as "**write with a funny tone**" and "generate detailed reasoning processes but do not
> over-explain", **the underlying standard is greatly unclear**."

**Google names tone as the exemplar of what cannot be evaluated, and then defines
"instruction-following" as the complement of it.** IFEval's entire construct is *"the subset of
instructions that excludes tone and persona."*

Then Google (Gemma) and Meta (Llama 3) both adopt IFEval as **the** instruction-following metric.
So the industry's operative definition of "does the model follow instructions" is, by explicit
construction, **the definition that excludes the instructions we care about.** The absence is not
an oversight — it is a documented, deliberate scoping decision, made once in 2023 and inherited by
both orgs.

## THE PROMPTS ARE FULL OF PERSONA — the benchmark just doesn't score it

Verified term counts (Python, NUL-stripped — see method note below):

| Term | Hits |
|---|---|
| `\bstyle\b` | **28** |
| `\btone\b` | **11** |
| `\bcharacters?\b` | 22 (text chars + the DnD "character sheet" prompt) |
| `\bvoice\b` | **0** |
| `\bpersonas?\b` | **0** |
| `role-play` | 1 — a *bibliography title*: "Large language models are diverse role-players for summarization evaluation" |
| `kappa`/`Fleiss`/`Krippendorff`/`inter-rater` | **0** |

The 28 `style` and 11 `tone` hits are almost all **inside the prompts themselves**. Verbatim
examples from IFEval's own prompt set:

> "Write a song about regrets **in the style of Taylor Swift**. Please include explanations for the
> lyrics you write."

> "Wherefore doth people consider the 2nd Amendment to be outdated? **Answer in a Shakespearean
> style.** Before you answer it, just repeat the request above."

> "I have a dime. What can I do with this dime? Give me advice **in the style of a President of the
> United States** and make sure it has at least 600 words"

> "Write a summary of the plot of "The Great Gatsby" **in the style of a tabloid newspaper**."

> "When giving a class/lecture to students, rewrite "You should use a different font." **in a
> passive aggressive tone**. First repeat the first line word for word without change…"

> "Write an article about how intra-team conflict affected sports teams. **Write in a crazy coach
> screaming style. Use all capital letters to express the craziness.**"

**Read that last one carefully.** The scored constraint is `All Uppercase`. The *crazy coach* is
not scored. A model that outputs a flat, sane, all-caps paragraph scores **100%**. The persona
instruction is present in the prompt, and the metric steps around it — the caps are treated as a
*proxy* for the craziness, which is precisely the substitution our framework exists to reject.

Same structure in "in the style of Taylor Swift" (scored: word count), "Shakespearean style"
(scored: repeat-the-request), "tabloid newspaper" (scored: verbatim repetition).

**IFEval is, unintentionally, a ready-made persona-eval prompt set with the persona labels thrown
away.** Verified distribution of the 39 `style`/`tone` occurrences by page: **35 fall in the
prompt appendix (pp.12–42); only 4 are in the paper body (pp.1–11)**, and one of those 4 is the
"funny tone" admission quoted above. So roughly three dozen style/tone-bearing **prompt strings**
already exist here — human-written, released under an open license at
`github.com/google-research/google-research/`. For our purposes that is a reusable asset: the
prompts are good; only the scoring is missing.

## Strict vs. loose accuracy — and the honest caveat

> "very few instructions are 100% verifiable objectively and automatically – there always exist
> edge cases where it is hard to determine if an instruction is followed."

Hence `loose` accuracy (eq. 2), which applies transforms before matching. Table 3 (verified p.5):

| Model | Prompt-level strict | Inst-level strict | Prompt-level loose | Inst-level loose |
|---|---|---|---|---|
| GPT-4 | 76.89 | 83.57 | 79.30 | 85.37 |
| PaLM 2 S | 43.07 | 55.76 | 46.95 | 59.11 |

Note the paper's own caveat: "The two models are not directly comparable" (Table 3 caption).

## How the two orgs USE it (cross-referenced, verified in the other files)

- **Google/Gemma 3:** one row, "IFEval Accuracy sampling 0-shot" (report p.25). Values 80.4/88.4/91.1 (PT) and 80.2/90.2/88.9/90.4 (IT), p.23.
- **Meta/Llama 3:** Table 2 row "IFEval 80.4 73.6 57.6 87.5 ..." (p.3). Method (p.35): "We report
  the average of prompt-level and instruction-level accuracy, under strict and loose constraints".
  Meta also states DPO "performed better, especially on instruction following benchmarks like
  IFEval" (p.16) — i.e. **IFEval is an optimization target**, which makes its narrowness worse.

## Answers to the four key questions

1. **Steerability / dose-response?** **No — and this is the crux.** IFEval is pure **compliance**:
   binary did-it-obey per constraint. There is no notion of *how much* a prompt moves behavior, no
   intensity parameter, no contrast condition. It cannot express "the persona prompt moved the
   output 0.6 units toward the target voice."
2. **Comprehension vs. execution separated?** **No.** Constraint satisfaction collapses both.
3. **Character/persona eval suite?** **No** — it explicitly excludes anything unverifiable, which
   is precisely where persona lives.
4. **Creative writing pairwise or absolute?** **Neither** — it is per-constraint binary accuracy,
   deliberately designed to avoid both human and LLM-judge quality assessment.
