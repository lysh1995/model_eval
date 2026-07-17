---
title: "FIREBALL: A Dataset of Dungeons and Dragons Actual-Play with Structured Game State Information"
url: https://aclanthology.org/2023.acl-long.229/
authors: Andrew Zhu, Karmanya Aggarwal, Alexander Feng, Lara J. Martin, Chris Callison-Burch
year: 2023
type: dataset
accessed: 2026-07-16
topic: game-simulation
---

# FIREBALL (ACL 2023 Long)

**arXiv:** 2305.01528 | **Data:** https://huggingface.co/datasets/lara-martin/FIREBALL | **Code:** https://github.com/zhudotexe/FIREBALL

THE key paper for this platform: it pairs natural language with **ground-truth structured game state** captured from the Avrae Discord bot. Unlike prior work (Callison-Burch et al. 2022) whose game state was *heuristically* inferred, FIREBALL's state is a **true gold standard** — emitted by the actual game engine. This makes violations checkable against a machine-readable record.

## 1. Dataset statistics (verbatim)

- **25k unique combat scenarios**
- **8M utterances** from **3.6k unique authors**
- **1.3M unique combat states**
- **160K unique actors**
- Collected from Discord servers using the **Avrae** bot (official D&D Discord bot, owned by Wizards of the Coast)

### Command distribution (Table 1)

| Type | Count |
|---|---|
| Combat | 713,568 |
| Actions | 608,527 |
| Custom | 313,898 |
| Character | 97,033 |
| Checks | 95,413 |
| Dice Rolls | 76,990 |
| Other | 204,174 |
| **Total** | **2,109,603** |

The `command` event type (n = 2,109,603) fires when "An Avrae command has successfully executed. Includes information about the game [state]".

### Filtering / distillation pipeline

1. **Utterance–Action Alignment** — matched chronologically.
2. **Authorship Filtering** — removed non-player/DM utterances; discarded multi-actor triples.
3. **IC/OOC Classification** — **GPT-3 Ada classifier, 94% accuracy on a validation set of 125 utterances.**
4. Yields **120,000 aligned utterance–command pairs** (Utterance-to-Command task).
5. Yields **43,000 aligned state–utterance pairs** (State-to-Narration task).

## 2. Task definitions (verbatim intent)

**Utterance to Command.** Given a natural-language roleplay utterance plus game state (actor list with attributes), predict the Avrae command matching player intent and targeting the correct entities.

**State to Narration.** "we want to generate a narrative utterance describing the effects of a player's actions, given all of the state changes since the start of the player's turn in combat." Example: a party fights a Sea Hag; the cleric attacks with her mace and misses; she narrates the miss as the hag dodging.

## 3. Automatic metrics — DEFINITIONS AND NUMBERS

### 3a. Utterance to Command (Table 2) — **OBJECTIVE / EXECUTABLE**

| Model | Pass Rate | Unit Tests | SGleu | RougeL |
|---|---|---|---|---|
| FT+S | **0.726** | **0.65** | 0.355 | 0.75 |
| FT | 0.235 | 0.234 | 0.189 | 0.551 |
| FS+S | 0.432 | 0.429 | 0.325 | 0.771 |
| FS | 0.319 | 0.25 | 0.246 | 0.598 |

Metric definitions:
- **Pass Rate** — proportion of generated commands that are **actually executable by the Avrae system**. Fully objective: the interpreter either accepts the command or it does not.
- **Unit Tests** — **custom hand-written tests validating that the desired state updates occurred.** This is the single most transferable idea in the paper: a *semantic* correctness check that is still fully automatic, because ground-truth post-state is known.
- **SGleu** — average Sentence GLEU (Mutton et al., 2007).
- **RougeL** — longest-common-subsequence overlap.

Models: base **GPT-3 Davinci (as of Dec. 2022)**. FT/FT+S finetuned on 30K FIREBALL examples; FS/FS+S few-shot with 3 exemplars. `+S` = with state. Evaluated on **1,000 held-out test examples**.

Note the ordering flip: **FS+S beats FT+S on RougeL (0.771 vs 0.75) but loses badly on Pass Rate (0.432 vs 0.726)** — surface-overlap metrics disagree with executable correctness. Direct evidence that n-gram metrics mismeasure this task.

### 3b. State to Narration (Table 3) — **WEAK / UNINFORMATIVE**

| Model | Perplexity | BERTScore | ROUGE-1 |
|---|---|---|---|
| DIALOG | 208.97 | 0.8458 | 0.1077 |
| COMMAND | **156.98** | 0.8421 | 0.0919 |
| FIREBALL-SHORT | 202.39 | **0.8478** | 0.1087 |
| FIREBALL-FULL | 208.98 | 0.8476 | **0.1156** |
| Human | **452.653** | N/A | N/A |

Metrics: **Perplexity** (scored by a GPT-2 baseline LM), **BERTScore** (contextual-embedding similarity to reference), **ROUGE-1** (unigram overlap).

**CRITICAL FINDING: human-written narration has the WORST perplexity (452.653) by nearly 3x**, and COMMAND has the best perplexity (156.98) while being the second-worst model on human judgment. BERTScore spans only **0.8421–0.8478 (range 0.0057)** across all four models — essentially no discrimination. The paper states these metrics are "an imperfect fit for our task where two narrations can differ substantially yet both be of high quality," and explicitly notes "the disparity in results between automated and human evaluation... is expected given previous work that reached similar conclusions (Sagarkar et al., 2018; DeLucia et al., 2021)."

Models (State-to-Narration): four GPT-3 **Davinci (Dec. 2022)** finetunes, each on **20,000 state-utterance pairs**. DIALOG = last 5 messages only; COMMAND = command only; FIREBALL-SHORT = mechanical results; FIREBALL-FULL = comprehensive state.

## 4. Human evaluation — methodology and numbers

**Annotators:** **45 evaluators recruited from the Avrae user base.** 37 had used Avrae for over a year; 37 had been the Dungeon Master of a game using Avrae.

**Protocol:** Each evaluator rated **3 to 7 scenarios randomly drawn from a set of 75**, with **at least 3-way redundancy** per scenario. Compensation: digital goods on D&D Beyond with a market value of **$36**.

**Questions asked (verbatim):**
- "Does the response make sense?" (yes/no)
- "Is the response specific?" (yes/no)
- "How interesting is the response?" (10-point scale)

**Results (Table 4):**

| Model | Sense | Specific | Interest |
|---|---|---|---|
| DIALOG | 0.36 | 0.27 | 4.27 |
| COMMAND | 0.41 | 0.37 | 4.72 |
| FIREBALL-SHORT | 0.52 | 0.48 | **4.98** |
| FIREBALL-FULL | **0.55** | 0.47 | 4.6 |
| Human | 0.54 | 0.48 | 4.91 |

**Both FIREBALL variants match or exceed human-written narration on Sense and Specific.** FIREBALL-SHORT (4.98) also out-scores Human (4.91) on Interest. Read with caution — see IAA below.

**Statistical significance (Appendix H):** Student's t-tests between model pairs at p<0.001 / p<0.01 / p<0.05 thresholds; FIREBALL-FULL vs. DIALOG reported p=0.0000 for Sense and Specific.

**INTER-ANNOTATOR AGREEMENT: NOT REPORTED.** Verified by grepping the full paper text for `krippendorff|kappa|inter-annotat|inter-rater|agreement|kendall` — **zero matches.** Despite 3-way redundancy (which makes agreement computable), no Krippendorff's alpha, Cohen's/Fleiss' kappa, or correlation figure is given. This is a finding: the paper's headline "matches human quality" claim rests on 3-way-redundant subjective ratings of **unknown reliability**, and t-tests were run treating those ratings as if independent and reliable.

## Relevance to companion-eval-platform

**This is the strongest objective-metric precedent we have found.** Concretely transferable:

1. **"Unit Tests" metric is the template for our objective dimensions.** Hand-written assertions checked against ground-truth post-state give a *semantic* correctness score with **zero annotator variance** — no alpha to worry about, because there is no human in the loop. A violation is checkable against a record. This directly answers our alpha 0.25–0.34 problem: don't stabilize the judge, replace the judgment.
2. **Pass Rate is the cheapest possible objective metric** — did the emitted action parse/execute against the engine? Any companion with structured tool/state surfaces (memory writes, profile fields, scheduled events) admits an identical metric.
3. **Explicit evidence that aesthetic metrics fail here, matching our finding.** Human text scores *worst* perplexity (452 vs 157–209); BERTScore range across all models is 0.0057. Cite this as external corroboration that fluency/similarity proxies are inverted or flat on creative-generation tasks.
4. **Pass Rate vs. RougeL ordering flip (FS+S wins RougeL, loses Pass Rate by 0.29)** is a citable, quantified demonstration that surface metrics rank systems wrongly when an executable ground truth exists.
5. **Cautionary precedent on IAA:** FIREBALL is a top-tier ACL long paper with 45 domain-expert annotators, 3-way redundancy, and t-tests to p=0.0000 — and still reports **no agreement statistic at all**. Useful for positioning: reporting alpha (even a bad 0.25–0.34) is *more* rigorous than the ACL-published norm in this subfield. Our low alpha is not a defect unique to us; it is the thing everyone else declined to measure.
6. **Structured-state pairing is the architectural lesson.** Grounding generation in machine-readable state improved *human* Sense from 0.36 (DIALOG) to 0.55 (FIREBALL-FULL), a +0.19 absolute gain — state access improves subjective quality AND enables objective checking. Both arguments point the same way.
