---
title: "Llama 4 Model Card (Scout 17Bx16E, Maverick 17Bx128E)"
url: https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md
org: Meta
year: 2025
type: model-card
accessed: 2026-07-16
topic: bigtech-practice
---

# Llama 4 Model Card — steerability CLAIMED in prose, MEASURED nowhere; ships a companion persona as the default system prompt

**Verification:** fetched raw markdown from
`https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/MODEL_CARD.md`
(23,764 bytes), grepped with word-boundary regex. This is the authoritative card, not a mirror.

## THE CLAIM (verbatim) — an assertion with no number attached

> "**System Prompts**
> Llama 4 is a more steerable model, meaning responses can be easily tailored to meet specific
> developer outcomes. Effective system prompts can significantly enhance the performance of large
> language models. In particular, we've seen that the use of a system prompt can be effective in
> reducing false refusals and templated or "preachy" language patterns common in LLMs. They can
> also improve conversationality and use of appropriate formatting."

And:

> "**Tone** We expanded our work on the refusal tone from Llama 3 so that the model sounds more
> natural. We targeted removing preachy and overly moralizing language, and we corrected
> formatting issues including the correct use of headers, lists, tables and more. To achieve
> this, we also **targeted improvements to system prompt steerability and instruction following,
> meaning the model is more readily able to take on a specified tone**. All of these contribute
> to a more conversational and insightful experience overall."

`\bsteerab` occurs **exactly 2 times** in the entire card — both in the prose above, **neither in
any table**. "Llama 4 is a more steerable model" is asserted. **More steerable than what, by how
much, measured how — is not stated anywhere.** There is no steerability row, no delta, no N.

Note also that Meta's own framing of "tone" here is, as in Gemini's cards, **about refusals** —
"refusal tone", "preachy and overly moralizing language". Both orgs converge on the same narrow
construct: tone = how apologetic the refusal sounds.

## THE PRODUCT TELL: Meta ships a companion persona as the recommended system prompt (verbatim)

> "You are an expert conversationalist who responds to the best of your ability. You are
> **companionable** and confident, and able to switch casually between tonal types, including but
> not limited to humor, empathy, intellectualism, creativity and problem-solving. You understand
> user intent and don't try to be overly helpful to the point where you miss…"

This is the **only** `\bcompanion` hit in the card. So Meta:
- ships a persona ("companionable", switch between "humor, empathy, intellectualism, creativity"),
- recommends it to every developer as the default template,
- and publishes **zero** evaluation of whether the model actually does any of it.

"able to switch casually between tonal types" is a **dose-response claim in a system prompt** with
no dose-response measurement behind it.

## THE BENCHMARK TABLES — the complete list of what IS measured

Extracted every benchmark cell from the card's pre-trained and instruction-tuned tables:

> MMLU · MMLU-Pro · MATH · MBPP · TydiQA · ChartQA · DocVQA · MMMU · MMMU Pro · MathVista ·
> LiveCodeBench · GPQA Diamond · MGSM · chrF (long context)

Metrics: `macro_avg/acc_char`, `macro_avg/em`, `em_maj1@1`, `pass@1`, `average/f1`,
`relaxed_accuracy`, `anls`, `accuracy`, `average/em`.

**Not one benchmark measures tone, persona, character, roleplay, steerability, or conversational
quality.** The card claims steerability improvements in prose and reports MMLU/GPQA/MATH.

## Safety framing — persona is again absent, and red-teaming is about "reprogramming"

> "We conduct recurring red teaming exercises with the goal of discovering risks via adversarial
> prompting and we use the learnings to improve our benchmarks and safety tuning datasets. …we
> derive a set of adversarial goals for the red team, such as extracting harmful information or
> **reprogramming the model to act in potentially harmful ways**."

"Reprogramming the model to act" is persona-hijacking without naming it. Meta's evaluation surface
for it is red-teaming, not measurement.

Critical risks named: Child Safety, CBRNE, Cyber attack enablement. Verbatim:

> "We leverage pre-training methods like data filtering as a first step in mitigating Child Safety
> risk in our model. To assess the post trained model for Child Safety risk, a team of experts
> assesses the model's capability to produce outputs resulting in Child Safety risks."

(Cross-ref `bigtech-meta-content-risk-standards.md`: this is the same period in which Meta's
internal standards reportedly permitted romantic roleplay with minors. The model card's Child
Safety paragraph and the Content Risk Standards are not reconciled anywhere public.)

## EXPLICIT ABSENCES (word-boundary grep on the full card)

| Term (regex) | Llama 4 card | Llama 3.1 card | Llama Guard 4 card |
|---|---|---|---|
| `\bsteerab` | 2 (prose only) | **0** | **0** |
| `\bpersonas?\b` | **0** | **0** | **0** |
| `\brole[- ]?play` | **0** | **0** | **0** |
| `\bcharacters?\b` | **0** | **0** | **0** |
| `\bcompanion` | 1 (system-prompt text) | **0** | **0** |
| `\bcreative writing\b` | **0** | **0** | **0** |
| `\bIFEval\b` | **0** | 1 | **0** |
| `kappa`/`Fleiss`/`inter-rater` | **0** | **0** | **0** |

**Regression note:** Llama 3's paper at least had a §4.3.7 that *defined* steerability and named
"character/persona". **Llama 4's card drops the definition and keeps only the marketing claim.**
Llama 4 also drops IFEval from its card entirely (0 hits) — so the card claims better
"instruction following" while reporting **no instruction-following benchmark at all**.

## Answers to the four key questions

1. **Steerability first-class / dose-response?** **No.** Claimed twice in prose, measured zero
   times. No dose, no curve, no elasticity. "More steerable" is unfalsifiable as published.
2. **Comprehension vs. execution separated?** **No.**
3. **Published character/persona eval suite?** **No.**
4. **Creative writing pairwise or absolute?** **Not evaluated in the card.** (Llama 4 Maverick's
   LMArena Elo was promoted at launch via a chat-tuned variant not matching the released weights —
   an Arena/pairwise signal, and a cautionary tale about pairwise-Elo-as-marketing. Marked
   **UNVERIFIED here**: I did not fetch a primary Meta source for that claim in this pass.)
