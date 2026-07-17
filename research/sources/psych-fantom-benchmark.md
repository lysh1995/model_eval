---
title: "FANToM: A Benchmark for Stress-testing Machine Theory of Mind in Interactions"
url: https://arxiv.org/abs/2310.15421
authors: Hyunwoo Kim, Melanie Sclar, Xuhui Zhou, Ronan Le Bras, Gunhee Kim, Yejin Choi, Maarten Sap
year: 2023
type: paper
accessed: 2026-07-16
topic: psychology-crosscheck
---

# FANToM (EMNLP 2023) — the model analogue of the convergent-validity problem

ACL Anthology: https://aclanthology.org/2023.emnlp-main.890/ · Project: https://hyunw.kim/fantom/ ·
Code: https://github.com/skywalker023/fantom

**This is the most directly relevant benchmark in the whole psychology cross-check.** It is ToM
evaluated *in conversation* (not passive narrative), and its central design move is the exact test
Warnell & Redcay ran on humans: **ask the same underlying question several different ways and see
whether the answers cohere.** They don't.

## Abstract (verbatim)

> "Theory of mind (ToM) evaluations currently focus on testing models using passive narratives that
> inherently lack interactivity. We introduce FANToM, a new benchmark designed to stress-test ToM
> within information-asymmetric conversational contexts via question answering. Our benchmark draws
> upon important theoretical requisites from psychology and necessary empirical considerations when
> evaluating large language models (LLMs). In particular, we formulate multiple types of questions
> that demand the same underlying reasoning to identify illusory or false sense of ToM capabilities in
> LLMs. We show that FANToM is challenging for state-of-the-art LLMs, which perform significantly worse
> than humans even with chain-of-thought reasoning or fine-tuning."

## Design

**Information asymmetry via natural conversation flow**: multiparty small-talk conversations where
characters leave and rejoin. "Conversations include explicit indications of leaving" — information
shared while a character is absent creates a natural false-belief structure. Conversations generated
by GPT-4, validated by humans.

**The core principle** (from the project page):

> "All of these questions require the same underlying theory of mind (ToM) reasoning: '_Who is aware of
> the information in the conversation._'"

### Question types

- **FACTQ** — basic comprehension of the interaction (control).
- **BELIEFQ[DIST.]** — free response. "When given a belief question regarding PersonX, the model should
  generate a response that incorporates only the information accessible to PersonX." Scored by cosine
  similarity between SentenceBERT embeddings: "A correct response should always be closer to the
  PERSONX-CENTRIC BELIEF A than the OMNISCIENT-VIEW BELIEF A." Plus token F1 — "models must score high
  on both the distance and F1 metrics" because "non-sensical responses (e.g., repetition of character
  names) can be deceptively closer to PERSONX-CENTRIC BELIEF A, resulting in misleading accuracy."
- **BELIEFQ[CHOICE]** — "The model should choose between the OMNISCIENT-VIEW BELIEF A and the
  PERSONX-CENTRIC BELIEF A."
- **ANSWERABILITYQ[LIST]** / **INFOACCESSQ[LIST]** — "A correct response must include all characters who
  have access to the answer or information while excluding all characters who do not. **No partial
  marks are assigned.**"
- **ANSWERABILITYQ[Y/N]** / **INFOACCESSQ[Y/N]** — per-character binary.

### The scoring innovation — ALL* and ALL

> "we report the ALL* score which requires [correctness across all question types about the same
> information]. To compare with human performance, we also report the ALL score, which only excludes
> the BELIEFQ[DIST.] from the ALL* score."

**This is a coherence metric, not an accuracy metric.** You only get credit if you answer *every*
framing of the same underlying fact correctly. It is precisely the convergent-validity test.

### Statistics

> "FANToM is composed of 256 conversations with 1,415 BELIEFQ[DIST.]s and BELIEFQ[CHOICE]s, 703 FACTQs,
> ANSWERABILITYQ[LIST]s, and INFOACCESSQ[LIST]s, respectively. Additionally, there are 2,689
> ANSWERABILITYQ[Y/N]s and INFOACCESSQ[Y/N]s."

Conversation scale vs the standard synthetic benchmark:

> "The average number of turns in the input context is 13.8 (short conversation), and the average number
> of words in each turn is 21.9. For reference, the corresponding statistics for ToMi (Le et al., 2019)
> are 4.9 and 4.2, respectively."

(ToMi stories are ~4.9 turns of ~4.2 words. FANToM is roughly 15× the text.)

Validation: 32 MTurk annotators, three per conversation; "We remove all question sets that were marked
as erroneous by the worker (∼8.6%)."

Models: thirteen instruction-tuned LMs including GPT-4 (0613, 0314), ChatGPT, InstructGPT, Flan-T5/UL2,
Falcon Instruct, Mistral Instruct 7B, Zephyr 7B, Llama-2 Chat 70B.

Human baseline: graduate students in computer science, asked BELIEFQ[CHOICE], ANSWERABILITYQ[LIST], and
INFOACCESSQ[LIST].

## Results — the headline table (Figure 2, short conversation context)

| Model | **All Question Types** | BeliefQ [Choice] | AnswerabilityQ [List] | InfoAccessQ [List] |
|---|---|---|---|---|
| **Human** | **87.5** | 93.8 | 90.6 | 90.6 |
| GPT-4 0613 (October) | **4.1** | 68.4 | 36.3 | 21.9 |
| GPT-4 0613 (June) | **12.3** | 73.3 | 37.8 | 36.4 |
| ChatGPT 0613 | **0.1** | 53.5 | 40.0 | 43.9 |
| Llama-2 Chat 70B | **0.3** | 38.4 | 25.3 | 17.1 |
| Falcon Instruct 40B | **0.0** | 54.3 | 19.1 | 10.8 |
| Mistral Instruct 7B | **0.1** | 27.6 | 28.3 | 27.5 |

**Read that first column again.** GPT-4 answers any *single* framing of "who knows what" at 68-73%.
Asked to be **consistent across framings of the same fact**, it scores **4.1%**. Humans score **87.5%**.
Several models score **0.0-0.3%** — not one single conversation where they were coherent.

The gap between 73.3 and 12.3 is not a difficulty gap. It is the difference between *having an answer*
and *having a belief*.

With chain-of-thought:

> "GPT-4 0613 + CoT (Jun) 26.6 40.2 57.7" / "GPT-4 0613 + CoT (Oct) 14.8 31.4 41.1"

> "we observe an improvement in scores with CoT applied. However, there are still significant score gaps
> compared to human performance."

Fine-tuning caveat (footnote 3): "We find fine-tuning achieves scores comparable with humans" — i.e. you
*can* fit the benchmark, which is exactly Ullman's saturation warning realized.

Authors' framing:

> "All the models exhibit scores that are significantly worse than human performance."

> "models' performance sharply drops when evaluated for coherent reasoning across multiple question
> types with the same underlying theory of mind (ToM) reasoning."

> "we formulate multiple types of questions that demand the same underlying reasoning to **identify
> illusory or false sense of ToM capabilities** in LLMs."

Also noted: models "perform significantly better on control tasks than on the original task involving
information asymmetry" — the FACTQ/BELIEFQ dissociation. And an inverse pattern: "certain models with
higher token F1 scores for FACTQ have lower scores for BELIEFQ[DIST.]" — **being better at reciting the
facts can make you worse at tracking who knows them.**

## Related benchmarks in this family

- **ToMi** (Le, Boureau & Nickel 2019) — synthetic Sally-Anne-style false-belief QA. The field's default.
  Very short (4.9 turns × 4.2 words). Sap et al. found GPT-3 at **60%**; Shapira et al. found GPT-3.5 at
  **81% overall but only 46% on the false-belief subset** — "close to random performance."
- **OpenToM** (arXiv:2402.06044) — longer narratives with explicit personality traits and motivations.
- **BigToM** — LLM-generated causal-template ToM vignettes.
- **FauxPas-EAI** — 176 questions (44 stories) on faux pas recognition, used in Shapira et al.

## Why this matters for the L1/L2/L3 framework

**This is the strongest evidence in the whole cross-check, because it is the framework's own claim
tested on models rather than children — and it is a "bound" task throughout.**

1. **"Bound ⇒ reliable" fails on a task that is maximally bound.** Every FANToM question has an
   objectively correct answer derivable from the transcript. Who was in the room is a matter of record.
   Inter-rater agreement would be ~1.0. And GPT-4 scores **4.1%** on coherence. The framework's central
   argument for trusting L1/L2 — "they have a referent, so agreement is high" — is fully satisfied here
   and buys **nothing**. The referent disciplines the *rater*, not the *model*. Agreement ≠ reliability
   ≠ validity, and FANToM separates all three in one table.

2. **It reproduces Warnell & Redcay in silicon, which closes the transfer gap.** The obvious objection
   to `psych-tom-task-convergence.md` is "that's humans, models may differ." FANToM is the same
   experiment on models — same underlying construct, multiple measurement framings, check coherence —
   and the result is *worse* than in humans (87.5% human coherence vs 4.1% GPT-4). **The human
   convergent-validity finding transfers, and it transfers with the sign and magnitude against us.** We
   can no longer treat the human literature as merely suggestive analogy.

3. **It directly kills "L1 comprehension" as a single number.** If the model's answer to "does Kailey
   know about the dog?" depends on whether you asked it as a choice, a list, or a yes/no, then there is
   no fact of the matter about what the model comprehends. There is only what it says under a particular
   framing. **A single L1 score is an average over framings that disagree with each other** — which is
   the definition of a number with no referent, ironically the exact sin the framework attributes to L3.

4. **The framing sensitivity IS the L2 "steerability" claim — and it's a bug, not a layer.** The
   framework holds that L2 includes "can prompt wording move its focus," treated as a *desirable,
   measurable* property sitting above comprehension. FANToM shows wording moves the *comprehension
   answer itself*, by ~60 points, on questions with objectively fixed answers. So L1 and L2 are not
   stacked layers with a causal arrow between them — **"wording changes the answer" is a single
   phenomenon that the framework has split in two and assigned opposite valences to** (bug at L1,
   feature at L2). Same mechanism. Cf. Ullman's double-space result.

5. **Steal the ALL* metric — it is the single most actionable import in this research.** The concrete
   recommendation for our harness: for any L1/L2 claim, ask each probe in ≥3 framings and **report the
   conjunction, not the mean**. Our equivalent of ALL*: "the model is credited with understanding a
   character fact only if it answers correctly under every framing." This converts a meaningless average
   into a coherence measurement, and it is cheap — it's a prompt-template loop, not new data. Expect our
   headline numbers to collapse the way GPT-4's did from 73 → 4. That collapse is the finding, not a
   harness failure.

6. **The FACTQ/BELIEFQ inversion warns against our most likely metric design.** Models with higher FACTQ
   F1 sometimes had *lower* BELIEFQ scores. Reciting the character card ≠ modelling the character. If we
   build L1 probes as "can it retrieve facts from the card," we will measure the thing that
   *anti*-correlates with the thing we care about. Retrieval and perspective-taking pull apart.

7. **Conversational, information-asymmetric, multi-party — this is the companion setting exactly.** ToMi's
   4.9-turn vignettes are not our domain; FANToM's 13.8-turn multiparty small talk with characters
   entering and leaving is. If GPT-4 cannot coherently track who-knows-what across 13.8 turns, the
   premise that L1 is the *easy, solved* foundation layer beneath the interesting creative work is
   backwards. **The foundation is the part that's broken.**
