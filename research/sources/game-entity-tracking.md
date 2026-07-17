---
title: "Entity Tracking in Language Models (+ Code Pretraining Improves Entity Tracking Abilities of Language Models)"
url: https://arxiv.org/abs/2305.02363
authors: Najoung Kim, Sebastian Schuster; (followup) Najoung Kim, Sebastian Schuster, Shubham Toshniwal
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Entity Tracking in Language Models (Kim & Schuster, ACL 2023, pp. 3835–3855)

**Status: this is the load-bearing paper for the "can we even build a world-state record from dialogue?" question — but the paper you actually want to cite for numbers is the 2024 followup, which re-runs the identical task on open models and publishes the full per-operation degradation table that Kim & Schuster only plotted.**

Primary: https://aclanthology.org/2023.acl-long.213/ · arXiv v2 (8 Sep 2023) https://arxiv.org/abs/2305.02363 · code/data https://github.com/sebschu/entity-tracking-lms

Followup (same first two authors, same task): **Code Pretraining Improves Entity Tracking Abilities of Language Models**, Kim, Schuster & Toshniwal, arXiv:2405.21068 (31 May 2024), https://arxiv.org/abs/2405.21068

⚠️ **Methodological note up front: Kim & Schuster report every result as a line graph (Figures 2–7), not a table.** There are no per-operation accuracy numbers to extract from the 2023 paper — the only hard numbers in its body are the Li et al. reanalysis and two verbal thresholds (">25%", ">45%"). Anyone who cites precise per-op accuracies "from Kim & Schuster 2023" is reading them off a plot. The tabulated numbers below come from the 2024 followup, which uses the same boxes task and publishes Table 6.

---

## Part 1 — The reanalysis that kills the prior SOTA claim (§2)

This is the most reusable methodological contribution and it is an **audit of someone else's benchmark**, not a new model result. Li et al. (2021) reported that a probing classifier on T5/BART encodings predicts entity state at **75–76% accuracy** on Alchemy. Kim & Schuster decompose that number:

| Slice of Alchemy | % of dataset | Probe accuracy |
|---|---|---|
| Final state **identical to initial state** (copy baseline wins) | 62.7% | — |
| Final state **empty** (an explicit `Drain` op decides it alone) | 32.4% | — |
| **Trivial cases (union of the two)** | **87.6%** | **86.8%** |
| **Non-trivial cases (actually require tracking)** | **12.4%** | **3.1%** |

> "If the accuracy is computed on the trivial and non-trivial cases separately, the probing classifier achieves 86.8% accuracy on trivial cases but only 3.1% accuracy on non-trivial cases, showing that most of the reported success derives from the trivial cases."

⭐ **3.1%.** A published 75–76% "entity tracking works" result is, on the only 12.4% of the data that tests entity tracking, **3.1% — an order of magnitude below the 62.7% copy-the-initial-state baseline.** This is the single most quotable number in the cluster and it is a *measurement-design* finding, not a model finding. (Of the 32.4% empty-final-state cases, 24.9pp were boxes that *did* contain liquid initially and got drained; the rest were already empty.)

**The mechanism of the illusion:** each Alchemy instruction touches at most 2 of 7 beakers, so probing every beaker after every instruction floods the dataset with untouched entities. Aggregate accuracy then measures *copying*, not tracking.

## Part 2 — The task and dataset (§3)

World `W = (O, n, m, e)`: `n` boxes, `m` max objects/box, `e` expected objects/box initially.
Dataset params: **n = 7 boxes, m = 3, e = 2, |O| = 100** nouns (BNC frequency > 27), **NumOps fixed at 12**, **2200 scenarios** randomly sampled. Ops are Move / Remove / Put.

Probing every box after every op ⇒ `n × (NumOps + 1)` = **91 examples per scenario**. Cloze format: input ends `Box N contains ___`.

**Four desiderata for any state-tracking eval (§3.1) — verbatim, and directly portable to our design:**

1. "The probed states of entities should not follow similar distributional patterns to those that are likely to be present in the pretraining data"
2. "Individual words or phrases should not predict by themselves the state of an entity without considering the previous discourse in order."
3. "If any data is used for demonstration, fine-tuning or training, the training and evaluation data should have little lexical overlap."
4. "If any data is used for demonstration, finetuning or training, the task should not be solvable by slot-filling based on observed datapoints."

Boxes (not beakers) were chosen deliberately: no emptying operation (blocks desideratum-2 shortcuts), no arithmetic/color-mixing knowledge required (Alchemy needed both), and initial-state "signatures" are disjoint across train/eval splits (blocks slot-filling).

**The random baseline is deliberately strong:** sample 0–3 objects per box *from the objects previously mentioned in a clause with that box*, not from all objects. Everything below is measured against this, not against chance.

**Ablation conditions (all reused by the followups):**

| Condition | What it breaks |
|---|---|
| **AltForms** | demo/test phrasings share no words except *the*, *into* (see table below) |
| **MoveContents** | adds `Move contents of Box N to Box M` — objects not enumerated, must be recovered from context |
| **AmbiRef** | adjectival modifiers droppable depending on current state (*the big brain* vs *the brain*) |
| **NumOps** | train on ≤2 ops, test on up to 12 |
| **Vocab** | disjoint object vocabulary train vs test |

**Table 2 (AltForms phrasings), verbatim:**

| Operation | Base | AltForms |
|---|---|---|
| Move | Move the car from Box 1 to Box 3. | Pick up the furby in Container A and place it into Container C. |
| Remove | Remove the car from Box 1. | Take the furby out of Container A. |
| Put | Put the car into Box 1. | Place the furby inside Container A. |

## Part 3 — Results (§4–5). Which models fail, and how.

**Table 1 — models evaluated (in-context, 2-shot):**

| Model | Size | Code in pretraining? | Additional training |
|---|---|---|---|
| GPT-3 `davinci` | 175B | ✗ | — |
| GPT-3 `davinci-instruct-beta` | 175B | ✗ | human demonstrations (finetuning) |
| GPT-3 `text-davinci-001` | 175B | ✗ | human demos + highly rated outputs |
| GPT-3.5 `code-davinci-002` | ? | ✓ | — |
| GPT-3.5 `text-davinci-002` | ? | ✓ | human demos + highly rated outputs |
| GPT-3.5 `text-davinci-003` | ? | ✓ | RL on human feedback |
| Flan-T5 base | 250M | ✗ | 1.6K tasks + instructions |
| Flan-T5 XL | 3B | ✗ | 1.6K tasks + instructions |

**Findings (Figures 2–5):**

- **Only `text-davinci-003` consistently beat the random baseline.** After 7 operations affecting a box it "correctly predicted all contents of a box ... in more than **25%** of the cases."
- **Flan-T5 base and XL: near-zero on non-trivial examples.** They "seemed to ignore the operations and primarily predicted the initial state description" — high accuracy when final = initial, "consistently low accuracy when the final state deviates." An instruction-tuned 3B model is a pure copy baseline on this task.
- **GPT-3 `davinci` (175B) also just repeats the initial state** — and worse, "as indicated by the steep decrease in the right panel, it was distracted by intervening operations even when repeating the initial state." A 175B model that cannot reliably *copy*.
- **Code is the discriminating variable, not RLHF or scale (Figure 5).** `code-davinci-002` — trained on code, *no* human feedback — tracks entities; all GPT-3.5 models outperform all GPT-3 models. This rules out "human feedback causes tracking."
- **AltForms:** "a small drop in performance when there were more than two operations affecting a box." Survives.
- **AmbiRef / MoveContents (Figure 4):** ⭐ "as the number of operations grows, performance rapidly approaches the random baseline, suggesting that entity tracking becomes increasingly more **brittle** as more state changes need to be considered jointly."

**Finetuned T5-base (Experiment 2, Figure 6):**

| Split | Result |
|---|---|
| Base | "near-perfect accuracy" |
| Random-init T5 (no pretraining) | "considerably lower ... almost exclusively predicting that a box is empty" — pretraining is required |
| Vocab (novel object names) | "only minor degradation" |
| **NumOps (train ≤2 ops → test 12)** | **"more than 45% of the cases"** correct on longer sequences |
| AltForms (trained on ≤12 ops) | degrades "substantially" but stays above random |
| **AltForms + NumOps (train ≤2 ops)** | ⭐ **"performance no longer exceeded the random baseline"** — the two shifts *compound* |

> "performance degradation was compounded and performance no longer exceeded the random baseline"

**AmbiRef/MoveContents even when finetuned in-domain (Figure 7):** "the model no longer achieves near-perfect accuracy, despite training and evaluating on examples of the same format. In both cases, the model **almost exclusively made mistakes with examples that require the interpretation of context-dependent operations**."

## Part 4 — The 2024 followup: the actual degradation table

Kim, Schuster & Toshniwal (arXiv:2405.21068) run the **same "base" boxes task**, same 2-shot prompt, on open models, with **regex-constrained decoding** via `outlines` (they note smaller models otherwise fail to follow the output format; constrained decoding took Llama 2 70B from **54.95 → 62.13**).

⭐ **Table 6 (verbatim) — accuracy split by number of operations affecting the target box. Test-set instance counts in parentheses. This is the degradation curve.**

| Model | Overall (5012) | 0 (1303) | 1 (1410) | 2 (1083) | 3 (651) | 4 (288) | 5 (142) | 6 (106) | 7 (29) |
|---|---|---|---|---|---|---|---|---|---|
| **Random baseline** | 21.08 | 41.06 | 17.85 | 12.70 | 11.87 | 10.58 | 9.16 | 7.51 | 12.59 |
| Llama 2-7B | 21.31 | 65.54 | 4.96 | 7.94 | 4.30 | 5.56 | 4.93 | 5.66 | 3.45 |
| Llama 2-7B Chat | 41.28 | 87.95 | 35.53 | 24.38 | 14.29 | 12.15 | 14.79 | 7.55 | 3.45 |
| Llama 2-13B | 33.28 | 77.05 | 25.18 | 15.97 | 12.75 | 8.68 | 8.45 | 10.38 | 17.24 |
| Llama 2-13B Chat | 38.05 | 77.51 | 36.67 | 19.94 | 16.28 | 9.03 | 11.27 | 11.32 | 13.79 |
| Llama-2 70B | 62.13 | 99.00 | 71.91 | 43.67 | 31.18 | 21.88 | 25.35 | 25.47 | 27.59 |
| Llama-2 70B Chat | 63.43 | 93.25 | 75.67 | 47.00 | 37.33 | 26.39 | 22.54 | 24.53 | 37.93 |
| Code Llama 7B | 31.94 | 90.87 | 13.69 | 12.28 | 7.99 | 6.60 | 4.93 | 8.49 | 13.79 |
| Code Llama 7B Instruct | 41.34 | 96.16 | 36.03 | 18.19 | 12.29 | 6.60 | 5.63 | 3.77 | 10.34 |
| Code Llama 13B | 54.79 | 95.70 | 60.78 | 32.87 | 25.35 | 20.14 | 21.83 | 26.42 | 13.79 |
| Code Llama 13B Instruct | 58.14 | 97.77 | 71.13 | 35.83 | 23.35 | 17.01 | 14.79 | 19.81 | 20.69 |
| Code Llama 34B | 58.26 | 94.70 | 71.28 | 33.89 | 31.18 | 21.53 | 14.79 | 19.81 | 24.14 |
| Code Llama 34B Instruct | 61.47 | 95.09 | 77.09 | 39.98 | 31.03 | 22.57 | 19.01 | 20.75 | 20.69 |
| Code Llama 70B | 69.77 | 99.39 | 76.60 | 54.20 | 47.31 | 40.97 | 36.62 | 43.40 | 37.93 |
| **Code Llama 70B Instruct** | **73.66** | 98.70 | 83.40 | 59.65 | 51.92 | 46.18 | 40.85 | 39.62 | 44.83 |
| Llemma 7B | 34.12 | 84.65 | 26.81 | 13.20 | 8.29 | 4.51 | 6.34 | 9.43 | **0.00** |
| Llemma 34B | 60.18 | 95.24 | 75.60 | 36.10 | 31.64 | 21.53 | 14.79 | 21.70 | 20.69 |
| DeepSeek 7B | 23.46 | 71.83 | 8.44 | 7.29 | 4.61 | 1.04 | 2.11 | 3.77 | 6.90 |
| DeepSeek 7B Chat | 32.24 | 70.30 | 27.30 | 17.27 | 11.21 | 11.81 | 9.15 | 6.60 | 3.45 |
| DeepSeek 7B Coder Base | 53.67 | 97.16 | 57.52 | 33.61 | 23.96 | 19.10 | 17.61 | 8.49 | 13.79 |
| DeepSeek 7B Coder Instruct | 48.76 | 91.71 | 54.54 | 26.41 | 18.13 | 13.89 | 11.27 | 17.92 | 3.45 |
| DeepSeek 7B Math Base | 56.40 | 98.93 | 60.28 | 35.73 | 26.73 | 24.65 | 16.20 | 23.58 | 27.59 |
| Gemma-7B | 42.66 | 95.78 | 45.82 | 14.04 | 8.60 | 5.56 | 7.75 | 7.55 | 3.45 |
| Gemma-7B Instruct | 47.79 | 93.25 | 55.96 | 21.98 | 15.51 | 7.99 | 8.45 | 11.32 | 17.24 |
| CodeGemma-7B | 46.09 | 91.33 | 53.76 | 21.70 | 13.67 | 6.94 | 5.63 | 8.49 | 3.45 |
| CodeGemma-7B Instruct | 53.49 | 93.48 | 69.57 | 26.22 | 19.82 | 12.50 | 12.68 | 11.32 | 10.34 |
| Mistral 7B | 45.67 | 96.01 | 50.28 | 18.56 | 11.37 | 8.68 | 12.68 | 7.55 | 10.34 |
| OpenMathMistral | 38.25 | 90.94 | 34.40 | 14.22 | 8.76 | 5.90 | 4.93 | 5.66 | 20.69 |
| LLama 7B | 28.67 | 97.93 | 0.71 | 10.53 | 2.92 | 3.82 | 3.52 | 0.94 | 3.45 |
| Float 7B Instruct | 27.55 | 89.33 | 1.56 | 12.37 | 5.07 | 5.21 | 2.82 | 4.72 | 13.79 |

**Table 3 (math ablation), verbatim:**

| Model | Aggregate | NumOps = 0 | NumOps ≥ 1 |
|---|---|---|---|
| Llama 7B | 28.67 | 97.93 | 4.34 |
| FLoat 7B | 27.55 | 89.33 | 5.85 |

### What this table actually says (the adversarial read)

1. ⭐ **The degradation is catastrophic and it is monotone.** Best model in the study, **Code Llama 70B Instruct: 98.70 → 44.83 from 0 to 7 ops — a 54-point fall.** Nothing in the table survives contact with 7 state updates. The *best available number for "track an entity through 7 changes"* is **44.83%**, and that is a 70B code model with constrained decoding.
2. ⭐ **"Overall" is a fabricated comfort number and must never be quoted alone.** 1303/5012 = **26% of the test set is 0-op**, i.e. pure copying. Llama 2-7B scores **21.31 overall vs a 21.08 random baseline** — it is *exactly at chance in aggregate*, and its 65.54 on the trivial quarter is the only thing holding the number up. Same disease Kim & Schuster diagnosed in Li et al. (2021), reproduced three years later in the followup's own headline column.
3. ⭐ **Most 7B models drop BELOW the random baseline once ≥2 ops touch the entity.** At 7 ops (random = 12.59): Llama 2-7B **3.45**, Gemma-7B **3.45**, CodeGemma-7B **3.45**, DeepSeek 7B **6.90**, DeepSeek 7B Chat **3.45**, Mistral 7B **10.34**, **Llemma 7B 0.00**. Below-random is not "weak tracking" — it is *anti-tracking*: the model is confidently emitting a stale or corrupted state. For an auditor, a below-random world model is worse than no world model.
4. **Code helps; math does not; alignment tuning is mixed.** FLoat gains **4.34 → 5.85** on NumOps≥1 — the paper calls this "marginal," and neither model beats random on non-trivial cases. Llemma 34B vs Code Llama 34B: **47.86 vs 45.46** (NumOps≥1) — "a narrow margin." Directly contradicts the prior Prakash et al. (2024) claim that arithmetic finetuning buys entity tracking. (The followup notes their numbers "are not expected to align with numbers reported in Prakash et al. (2024) because they used a modified version of the original task.")
5. **Scale, not code, is doing most of the work.** Llama 2 7B→70B (no extra code) buys **21.31 → 62.13**. Code Llama 7B→70B buys **31.94 → 69.77**. The code delta at 7B is ~10 points; the scale delta is ~40. The paper's own honest read: "there is both a possible effect of scale in the effectiveness of code training ... and an effect of the amount of additional code training (DeepSeek-Coder: 2T tokens, Code Llama: 500B tokens)."
6. ⚠️ **The tail of this curve is statistically thin. Do not over-read it.** n = **29** at 7 ops and **106** at 6 ops, vs 1303 at 0. A single example at 7 ops moves accuracy by 3.45 points — which is exactly why so many cells read `3.45`, `6.90`, `10.34`, `13.79` (they are k/29). Llemma 7B's "0.00" means 0/29, not a measured zero capability. The **shape** of the degradation is robust and replicated across ~30 models; the **precise 7-op values are not**. Cite 2–4 ops (n = 1083/651/288) if you need a defensible point estimate. This is the same discipline note 11 wants and the same failure the `0.599^10` extrapolation in `game-llm-sim-state-prediction.md` commits.
7. **Formatting is a confound everyone else eats silently.** +7.2 points on Llama 2 70B (54.95 → 62.13) purely from regex-constrained decoding. Any world-state extractor we build that parses free-form output is measuring format compliance and tracking *jointly*. Constrain the decode or the number is meaningless.

## Limitations (Kim & Schuster 2023, verbatim)

> "One limitation of this work is that we are only considering behavioral data which makes it difficult to establish a fully causal link between entity tracking capacities and high performance on our task."

> "A possible criticism of our setup is that it requires short-term memory capacities that exceed the memory capacities of most, if not all, humans. That is, if we presented humans with the same input as the model, we would not expect them to be able to keep track of the contents of all 7 boxes due to memory limitations. Therefore we are potentially expecting models to do super-human entity tracking."

> "we designed our task such that the entire description fits within the context window of pretrained language models ... our results do not apply to texts whose length exceeds a model's context window, and likely different model architectures will be necessary to perform proper entity tracking for longer texts."

> ⭐ "our results also indicate that this behavior is **not very stable once several operations act on an entity**. Our results should therefore **not be taken as justification for using these models for critical applications where high accuracy is needed**."

> "Lastly, we only evaluated English models in this work."

**Followup limitations (verbatim):** "While the pairs of models we compared are 'minimal pairs', several possible confounds remain ... the OpenMathInstruct dataset (1.5 GB) is two orders of magnitude smaller in terms of the number of tokens compared to Code Llama's code data (500 B tokens), so the size of the additional training data could be a confound."

⚠️ **The context-length caveat is the one that bites us hardest, and it cuts against the consumer's framing.** Kim & Schuster explicitly did *not* measure degradation with context length — every scenario fits the context window and NumOps is capped at 12. **There is no context-length degradation curve in this cluster.** The x-axis is *number of operations affecting the target entity*, which is a different and much more favourable variable: a 12-op scenario is a few hundred tokens. For a context-length curve, use `multiturn-lost-in-middle.md` / `multiturn-ruler.md` / `multiturn-nocha.md`. Conflating "degrades with 7 state updates" and "degrades with long context" would be a real citation error and a reader who knows the literature will catch it.

## Relevance to companion-eval-platform

**This cluster is the evidence base for whether the world-state record can be built by an LLM at all — and it says: not reliably, and the failure is exactly where roleplay lives.**

1. ⭐ **The 3.1% reanalysis is our template for auditing our own auditor.** Kim & Schuster took a 75–76% published result and showed 87.6% of the data was trivial. **Our world-state record will have exactly this pathology and worse:** in a long roleplay, the overwhelming majority of facts (hair colour, sister's name, hometown) are asserted once and never updated. If we score contradiction-detection in aggregate, we will publish a number that measures *copying an unchanged fact* and call it consistency auditing. **Mandatory: bucket every world-state metric by number of updates the fact has undergone, and report the 0-update slice separately or not at all.** This is a stronger and cheaper version of the static/dynamic split flagged in `game-llm-sim-state-prediction.md` (73.9% vs 59.9%).
2. ⭐ **The 44.83%-at-7-ops ceiling is the honest prior for our whole feature.** Boxes is a *radically easier* problem than roleplay world state: closed vocabulary (100 concrete nouns), 7 slots, 3 unambiguous operations, no coreference, no implicature, no negation, no time, no subjectivity, template-generated sentences, and the state is fully observable. Roleplay state is open-vocabulary, implicit, hedged, and often never explicitly stated. **If a 70B code model with constrained decoding manages 44.83% on the easy version at 7 updates, the honest expectation for a contradiction auditor over a 200-turn companion transcript is much worse.** Say this before a reviewer says it for us — the same move note 00 makes about ground truth.
3. ⭐ **Below-random behaviour is the product-visible failure and it has a name here.** Flan-T5 XL and GPT-3 davinci "primarily predicted the initial state description"; 7B models sit at 3.45 where random is 12.59. **The dominant failure mode is not confusion — it is confident staleness: the model reports the world as it was first described, ignoring everything that happened since.** In companion terms: the character who still thinks you're single 40 turns after the breakup. That is *the* canonical companion-consistency complaint (see `product-community-complaints.md`), and this cluster gives it a mechanism and a measurement. **A world-state auditor built on a 7B model will not just be weak — it will actively assert the stale state.**
4. ⭐ **AmbiRef and MoveContents are the roleplay-realistic conditions, and they are where everything collapses — even with in-domain finetuning.** `Move contents of Box N to M` (referent not enumerated) and droppable modifiers (*the big brain* → *the brain*) are toy versions of what every real dialogue turn does: pronouns, ellipsis, definite descriptions resolved against current state. Finetuned T5 "almost exclusively made mistakes with examples that require the interpretation of context-dependent operations," and `text-davinci-003` "rapidly approaches the random baseline." **Roleplay dialogue is 100% AmbiRef/MoveContents. The base-split near-perfect numbers do not transfer to us at all — only the AmbiRef/MoveContents curves are informative for our setting, and they are the worst curves in the paper.**
5. **The AltForms+NumOps compounding result predicts our deployment gap.** Each shift alone is survivable; together, "performance no longer exceeded the random baseline." Our extractor will face *simultaneous* shifts — new phrasing, new genre, longer scenes, novel entities — relative to whatever we tune it on. **Budget for compounding, not for the max of the individual degradations.** Relevant to note 11's design grid.
6. **The four desiderata (§3.1) should be lifted verbatim into our world-state eval spec.** Especially #2 and #4 — our contradiction test set must not be solvable by lexical overlap or slot-filling against the record. The initial-state "signature" trick (ensure no train/test pair shares an initial configuration modulo names) is a concrete, cheap dedup we can copy.
7. **Constrained decoding is worth +7.2 points and we should adopt it for extraction, not just measure around it.** If the world-state record is JSON, constrain the decode. This is a free product win falling out of an eval-methods footnote — same shape as the "rules in context = +30.6" finding in `game-llm-sim-state-prediction.md`.
8. ⚠️ **What this cluster does NOT give us: a context-length curve.** See the warning above. The consumer wants "degradation with longer context" — this literature measures *number of operations on a target entity* inside a short context. Those are different axes and the honest citation is "degrades with number of state updates." **Measuring the actual interaction of update-count × context-length on roleplay transcripts is an unfilled gap and a genuine contribution we could make cheaply** — the boxes generator is public (github.com/sebschu/entity-tracking-lms) and the followup's harness is a 2-shot prompt plus a regex.
9. **Model-selection consequence, concrete:** entity tracking at useful accuracy appears to require ~70B-scale + code pretraining. **A cheap 7B extractor/auditor is not merely degraded — it is at or below a strong random baseline on exactly the multi-update cases the feature exists to catch.** This is a direct input to the guardrail cost/latency tradeoff in `scale-guardrail-latency-budgets.md`: the small-model option may not be on the Pareto frontier at all here.
