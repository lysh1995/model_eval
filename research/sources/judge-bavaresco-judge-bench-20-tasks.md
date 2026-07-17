---
title: "LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks (JUDGE-BENCH)"
url: https://arxiv.org/abs/2406.18403
authors:
  - Anna Bavaresco
  - Raffaella Bernardi
  - Leonardo Bertolazzi
  - Desmond Elliott
  - Raquel Fernández
  - Albert Gatt
  - Esam Ghaleb
  - Mario Giulianelli
  - Michael Hanna
  - Alexander Koller
  - André F. T. Martins
  - Philipp Mondorf
  - Vera Neplenbroek
  - Sandro Pezzelle
  - Barbara Plank
  - David Schlangen
  - Alessandro Suglia
  - Aditya K. Surikuchi
  - Ece Takmaz
  - Alberto Testoni
year: 2024
venue: ACL 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# LLMs instead of Human Judges? (JUDGE-BENCH)

> Not to be confused with **JudgeBench** (Tan et al., 2410.12784). Different paper, confusingly similar name. This one (Bavaresco et al.) is about **replicating human annotations across 20 NLP tasks**; the other is about **hard factual/reasoning pairs**.

## Abstract (verbatim)

> There is an increasing trend towards evaluating NLP models with LLMs instead of human judgments, raising questions about the validity of these evaluations, as well as their reproducibility in the case of proprietary models. We provide JUDGE-BENCH, an extensible collection of 20 NLP datasets with human annotations covering a broad range of evaluated properties and types of data, and comprehensively evaluate 11 current LLMs, covering both open-weight and proprietary models, for their ability to replicate the annotations. Our evaluations show substantial variance across models and datasets. Models are reliable evaluators on some tasks, but overall display substantial variability depending on the property being evaluated, the expertise level of the human judges, and whether the language is human or model-generated. We conclude that LLMs should be carefully validated against human judgments before being used as evaluators.

## Methodology

- **20 NLP datasets** with existing human annotations
- **11 LLMs** — both open-weight and proprietary
- Task: replicate the human annotations. Correlation measured against the human labels.

The design is the right one for our question: rather than asking "does the judge agree with humans on average," it asks **"on which properties, on whose annotations, and on what kind of text does the judge agree?"**

## Key findings

**"Substantial variance across models and datasets."** There is no single "judge reliability" number. The paper's central result is a *negative* one about generalization.

Reliability depends on **three identified moderators** — each of which is adverse for us:

1. **The property being evaluated.** Judges are reliable on some properties and not others. Our properties (character fidelity, creativity, storytelling) are subjective and abstract — the hard end. Reliability on "fluency" tells us nothing about reliability on "character fidelity."
2. **The expertise level of the human judges.** Agreement is different against expert vs crowdworker annotations. **This means our human ground truth is itself a design decision that changes the answer.** If we validate against crowdworkers and ship against expert intent, we have validated the wrong target. For companion characters, the "expert" is arguably the character designer — a bespoke and expensive annotator pool.
3. **Whether the language is human- or model-generated.** Judges behave differently on model text vs human text. Converges with G-Eval's finding that judges over-score machine text vs human text. Our eval data will be nearly all model-generated, with human-authored gold references — a mixed regime where this moderator bites.

## The conclusion, verbatim

> "We conclude that LLMs should be carefully validated against human judgments before being used as evaluators."

## Implications for our platform

- **This is the strongest citation for "you must build your own validation set."** Published judge-agreement numbers do not transfer to our task. Not approximately, not directionally — the paper's finding is that variance across tasks is *substantial*, so a borrowed number carries close to zero information about our setting.
- **Judge selection must be empirical and per-dimension.** The best judge for "character fidelity" may not be the best for "storytelling." We should be prepared to run different judges/rubrics per dimension and to justify each with our own agreement data.
- **Our human annotation protocol is a first-class design artifact.** Who annotates (expert character designers vs crowdworkers) changes what we are measuring. This must be decided deliberately and documented as part of the evaluator version.
- **Reproducibility of proprietary judges is called out in the abstract itself** — converges with the drift literature.
