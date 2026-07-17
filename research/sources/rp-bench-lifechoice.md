---
title: "Character is Destiny: Can Role-Playing Language Agents Make Persona-Driven Decisions? (LIFECHOICE benchmark)"
url: https://arxiv.org/abs/2404.12138
authors: Rui Xu, Xintao Wang, Jiangjie Chen, Siyu Yuan, Xinfeng Yuan, Jiaqing Liang, Zulong Chen, Xiaoqing Dong, Yanghua Xiao (Fudan University, Alibaba)
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# LIFECHOICE — persona-driven decision benchmark

**arXiv:** 2404.12138. HTML: https://arxiv.org/html/2404.12138v2
Title evolved across versions: v1 "Character is Destiny: Can Large Language Models Simulate Persona-Driven Decisions in Role-Playing?" → v2 "Character is Destiny: Can Role-Playing Language Agents Make Persona-Driven Decisions?"

> **Relevance:** LIFECHOICE is the field's answer to "does the character actually *have* a personality, or just a voice?" It scores whether a model predicts the choice a character would make — behavior, not style. This is the hardest thing to fake and the most under-measured dimension in companion products.

## Abstract (VERBATIM, v2)

> Can Large Language Models (LLMs) simulate humans in making important decisions? Recent research has unveiled the potential of using LLMs to develop role-playing language agents (RPLAs), mimicking mainly the knowledge and tones of various characters. However, imitative decision-making necessitates a more nuanced understanding of personas. In this paper, we benchmark the ability of LLMs in persona-driven decision-making. Specifically, we investigate whether LLMs can predict characters' decisions provided by the preceding stories in high-quality novels. Leveraging character analyses written by literary experts, we construct a dataset LIFECHOICE comprising 1,462 characters' decision points from 388 books. Then, we conduct comprehensive experiments on LIFECHOICE, with various LLMs and RPLA methodologies. The results demonstrate that state-of-the-art LLMs exhibit promising capabilities in this task, yet substantial room for improvement remains. Hence, we further propose the CHARMAP method, which adopts persona-based memory retrieval and significantly advances RPLAs on this task, achieving 5.03% increase in accuracy.

⚠️ **Version discrepancy on dataset size — note when citing.**
- **v2 (current, authoritative): 1,462 decision points from 388 books.**
- v1: 1,401 decision points from 395 books.
Use the v2 numbers.

## What it measures — the dimension

A single construct, but a deep one: **persona-driven decision-making** — whether an RPLA, given the preceding story, predicts the decision the character actually made.

The paper's framing: prior RPLA work mimics "mainly the knowledge and tones of various characters," but "imitative decision-making necessitates a more nuanced understanding of personas." LIFECHOICE deliberately targets the layer *beneath* voice and trivia.

### Motivation taxonomy (the decision points are typed)

Decisions are categorized by what drives them:

- **Character-driven (67.77%)** — personality, emotions, relationships, values, desires.
- **Plot-driven (32.23%)** — external conflicts, tasks, secrets, pursuits, power struggles.

This split matters: character-driven decisions are the ones that actually test persona fidelity; plot-driven ones can be solved by narrative reasoning alone. A well-built eval should report these separately.

## How it scores

**Multiple-choice probes with accuracy — no LLM judge, no rubric, no human scoring at eval time.**

- **Task format:** multiple-choice questions (**4 options**) derived from real character decisions in high-quality novels.
- **Metric:** **accuracy** — proportion of correct option selections.
- **Context:** the preceding story is provided. **Context length ~150k tokens average** — this is a long-context benchmark as much as a persona benchmark.
- **Ground truth:** the decision the character actually made in the book. Objective, not judged.
- **Source of expert signal:** **character analyses written by literary experts**, sourced from **SuperSummary**.

**Construction pipeline (3 steps):**
1. Decision point detection
2. Distractor generation
3. Motivation extraction

The distractor-generation step is what makes accuracy meaningful — the wrong options must be plausible-but-out-of-character.

**Advantage of this design:** immune to judge bias and judge cost entirely. **Disadvantage:** multiple-choice is not how companions are actually used, and 150k-token contexts are not a realistic product setting.

## Models evaluated + exact accuracy

| Model | Accuracy (%) |
|---|---|
| **Human performance** | **92.01** |
| **CharMap (GPT-4)** — proposed method | **67.95** |
| GPT-4 | 62.92 |
| Claude-3.5 | 62.85 |
| Gemini-1.5-pro | 57.16 |
| LLaMA-3 | 57.02 |

**Headline gaps:**
- **Human 92.01 vs. best model 67.95 → ~24 point gap.** The largest human–model gap among the benchmarks surveyed here. Persona-driven decision-making is genuinely unsolved.
- CharMap adds **+5.03%** accuracy over GPT-4 (62.92 → 67.95), via **persona-based memory retrieval**.

## Proposed method — CHARMAP

"adopts persona-based memory retrieval and significantly advances RPLAs on this task, achieving 5.03% increase in accuracy." The lesson: *retrieval conditioned on persona* beats generic retrieval — relevant to any companion system with long-term memory.

## Limitations (VERBATIM)

> Although we have controlled the quality of the novels, there may still be issues with the plot and characters since the author designed the storyline, which can result in illogical choices within the book.

I.e., the ground truth is only as coherent as the novelist — authors sometimes write characters out of character, and LIFECHOICE inherits that noise as an accuracy ceiling below 100%. (Human performance at 92.01%, not ~100%, is consistent with this.)

Additional structural limitations:
- Multiple-choice format compresses open-ended behavior into 4 options.
- ~150k-token contexts conflate long-context retrieval ability with persona understanding — a model may fail for context-length reasons rather than persona reasons.

## Multilingual / multi-turn

- **Multilingual: no.** English novels exclusively. **No Chinese support mentioned.**
- **Multi-turn: no.** Single-turn decision prediction. No conversational or dialogue extension.

## Related — "character hallucination benchmark"

The brief paired LifeChoice with "CharacterHallucination." Searching that term surfaces **TimeChara** (arXiv 2405.18027) as the canonical character-hallucination benchmark — documented separately in `rp-bench-timechara.md`. There is no separate standalone benchmark named "CharacterHallucination"; the term is used descriptively in the literature, and TimeChara owns the point-in-time formulation. Related adjacent works found during search: **Guess What I am Thinking: A Benchmark for Inner Thought Reasoning of Role-Playing Language Agents** (arXiv 2503.08193) and **FURINA** (arXiv 2510.06800), both potentially worth a follow-up pass.

## Takeaways for a companion-eval platform

- **Behavior > voice.** Style consistency is easy to measure and easy to fake; decision consistency is neither. A companion eval that only scores tone is measuring the shallow layer.
- The **character-driven vs. plot-driven** split is a reusable filter for building decision probes.
- **Objective ground truth** (what the character actually did) sidesteps the entire judge-bias problem — worth replicating wherever a factual anchor exists.
- **Persona-conditioned memory retrieval (CharMap) is the one intervention shown to move the needle** — architecturally relevant, not just evaluative.
