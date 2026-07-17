---
title: "Instruction-Following Evaluation for Large Language Models (IFEval)"
url: https://arxiv.org/abs/2311.07911
authors: Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, Le Hou (Google / Yale)
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# IFEval — the "verifiable instructions" paradigm

## Abstract (verbatim excerpt)

> "One core capability of Large Language Models (LLMs) is to follow natural language instructions. However, the evaluation of such abilities is not standardized: Human evaluations are expensive, slow, and not objectively reproducible, while LLM-based auto-evaluation is potentially biased or limited by the ability of the evaluator LLM."

The paper introduces IFEval, a benchmark focusing on objectively verifiable instructions, ~500 prompts each containing one or more verifiable instructions.

## Design philosophy — WHY verifiable instructions

This is the core motivation and the reason this paper matters to us. The authors identify **three** failing evaluation paradigms and route around all of them:

1. **Human evaluation** — "expensive, slow, and not objectively reproducible"
2. **LLM-based auto-eval** — "potentially biased or limited by the ability of the evaluator LLM"
3. **Quantifiable benchmarks** (e.g. exact-match QA) — too narrow to capture open generation

Their solution: restrict the evaluation target to a subclass of instructions where the judge can be a **deterministic program**.

**Definition (verbatim):** verifiable instructions are "instructions amenable to objective verification of compliance."

**Design rationale (verbatim):** focusing on this category "enhance[s] the clarity and objectivity of the evaluation process, enabling a fully automatic and accurate assessment of a machine model's ability to follow directions."

Key property: *a prompt contains verifiable instructions that can be checked with a deterministic program, circumventing the need of an LLM or human as judge.*

Canonical examples:
- "write in more than 400 words"
- "mention the keyword of AI at least 3 times"
- "end your email with: P.S. I do like the cake"

**The trade the paper makes explicitly:** it gives up on evaluating whether the response is *good* and evaluates only whether the response is *compliant*. Verifiability is bought by narrowing the construct. This is the central design lesson.

## Scale

- **25** types of verifiable instructions
- **541** prompts (paper says "around 500")
- Each prompt carries one or more verifiable instructions

## The 25 instruction types (verbatim table)

| Instruction Group | Instruction | Description |
|---|---|---|
| Keywords | Include Keywords | Include keywords {keyword1}, {keyword2} in response |
| Keywords | Keyword Frequency | Word should appear {N} times |
| Keywords | Forbidden Words | Do not include specified keywords |
| Keywords | Letter Frequency | Letter {letter} should appear {N} times |
| Language | Response Language | Entire response in {language} only |
| Length Constraints | Number Paragraphs | Response contains {N} paragraphs |
| Length Constraints | Number Words | At least/around/at most {N} words |
| Length Constraints | Number Sentences | At least/around/at most {N} sentences |
| Length Constraints | Paragraphs + First Word | {N} paragraphs; i-th starts with word |
| Detectable Content | Postscript | Add postscript starting with {marker} |
| Detectable Content | Number Placeholder | At least {N} placeholders like [address] |
| Detectable Format | Number Bullets | Exactly {N} markdown bullet points |
| Detectable Format | Title | Title wrapped in double angular brackets |
| Detectable Format | Choose From | Answer with one of specified options |
| Detectable Format | Highlighted Section | Highlight at least {N} sections with markdown |
| Detectable Format | Multiple Sections | {N} sections marked with {section_splitter} |
| Detectable Format | JSON Format | Entire output in JSON format |
| Combination | Repeat Prompt | Repeat request, then give answer |
| Combination | Two Responses | Two responses separated by 6 asterisks |
| Change Cases | All Uppercase | Entire response in capital letters only |
| Change Cases | All Lowercase | Entire response in lowercase only |
| Change Cases | Frequency All-capital Words | All-caps words appear {N} times |
| Start with/End with | End Checker | Finish with exact phrase {end_phrase} |
| Start with/End with | Quotation | Wrap entire response in double quotes |
| Punctuation | No Commas | Refrain from using commas |

Note the taxonomy shape: every type reduces to a **countable or regex-checkable predicate** over the response string. No type requires semantic judgment.

## The four metrics

Two axes crossed: granularity (prompt vs instruction) × leniency (strict vs loose).

**Strict:**
- **Prompt-level strict-accuracy** — % of prompts where *all* verifiable instructions are followed (conjunctive; one miss fails the prompt)
- **Instruction-level strict-accuracy** — % of individual verifiable instructions followed

**Loose** — addresses *false negatives*, i.e. cases where the model complied but a wrapper defeated the checker. Transformations applied to each response:
1. Remove markdown font modifiers (asterisks)
2. Remove the first line (skips intros like "Sure, here it is:")
3. Remove the last line (skips outros like "Hope it helps")

All **8** combinations of these transformations are applied; compliance under *any* transformation counts as success.

- **Prompt-level loose-accuracy** / **Instruction-level loose-accuracy** — as above under the loose criterion.

The strict/loose pair is itself a design lesson: the deterministic checker has a known failure mode (politeness scaffolding around an otherwise-compliant answer), and rather than hand it to a judge they defined a *mechanical* relaxation and reported both bounds.

## Results (verbatim table)

| Models | Prompt-level strict-acc (%) | Inst-level strict-acc (%) | Prompt-level loose-acc (%) | Inst-level loose-acc (%) |
|---|---|---|---|---|
| GPT-4 | 76.89 | 83.57 | 79.30 | 85.37 |
| PaLM 2 S | 43.07 | 55.76 | 46.95 | 59.11 |

Authors note the two models "are not directly comparable due to significant differences in parameter count."

Observations worth carrying:
- **Strict→loose gap** is ~2.4 pts (GPT-4 prompt-level) to ~3.9 pts (PaLM 2 S prompt-level). The checker's false-negative rate is small but non-zero and larger for weaker models.
- **Prompt-level is always well below instruction-level** (76.89 vs 83.57 for GPT-4): the conjunction over multiple constraints is where models die. With ~1.5 instructions/prompt average this gap is already ~7 pts.
- Even GPT-4 fails ~23% of prompts on instructions a regex can check.

## Relevance to companion-eval-platform

**This is the paradigm we want, and this file is the reference implementation of our own stated preference.**

1. **The motivation is verbatim our finding.** IFEval's abstract rejects human eval as "not objectively reproducible" — our human Krippendorff α of 0.25–0.34 on roleplay quality is the quantitative statement of exactly that. IFEval's response was not "get better raters"; it was **change the construct being measured** to one where the judge is `len(response.split()) > 400`. We should cite IFEval as prior art for the move we are already making.

2. **The transferable design rule:** an instruction is admissible to the benchmark iff a deterministic program can check it. For a roleplay/scene platform, the analogous admissible constraints are the scene's own rules, which are *already* stated declaratively in the system prompt and are therefore already checkable:
   - persona facts (never break character; never mention being an AI) → string/classifier predicate
   - world rules ("magic costs HP", "the door is locked until the key is found") → state predicate
   - format rules ("always end with a choice list of exactly 3 options") → count predicate
   - forbidden content per scene ("no modern technology in this medieval setting") → keyword predicate
   These are *exactly* IFEval instruction types re-skinned: Include Keywords, Forbidden Words, Number Bullets, End Checker. We can lift the taxonomy nearly wholesale.

3. **Adopt the four-metric structure, not just the idea.** Prompt-level vs instruction-level is the right granularity split for us too: per-scene ("did the AI hold *every* rule this session?") vs per-constraint ("what fraction of rule-instances held?"). Per-scene conjunctive accuracy is the honest headline number and will be brutally low over a long session — which is the point.

4. **Adopt the strict/loose discipline.** Our checkers will have false negatives (the AI complies in-fiction but phrases it unexpectedly). The IFEval answer is a *mechanical* relaxation with both numbers reported — not an LLM fallback judge. Resist the temptation to patch checker gaps with a judge; that reintroduces the α problem we are escaping.

5. **Caveat to carry forward:** IFEval is **single-turn**. The constraint is issued and checked in one exchange. Our entire problem is the *horizon* — a rule issued at turn 0 and checked at turn 60. See `game-multi-if.md`, which extends exactly this checker infrastructure across turns and finds the degradation. IFEval gives us the checker design; Multi-IF gives us the decay curve.

6. **Honest limitation:** IFEval measures compliance, not quality. A model can score 100% by writing 400 words of garbage containing "AI" three times. If we build only IFEval-style rule adherence, we will have a rigorous metric of something that is necessary but not sufficient for a good scene. This is the acceptable price of α > 0.8, but it should be stated in the platform's own docs rather than discovered by a user.
