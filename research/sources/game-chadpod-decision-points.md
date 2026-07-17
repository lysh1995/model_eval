---
title: "Branching Narratives: Character Decision Points Detection (CHADPOD)"
url: https://arxiv.org/abs/2405.07282
authors: Alexey Tikhonov, Ivan P. Yamshchikov
year: 2024
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# CHADPOD — the one place in the narrative literature with objective agency ground truth

**Why this is here: it is the only source in this review where "a choice actually matters" has a mechanical, non-survey ground truth. The trick is that the ground truth comes from an authored game graph, not from the text.**

## Abstract (verbatim)

> "This paper presents the Character Decision Points Detection (CHADPOD) task, a task of identification of points within narratives where characters make decisions that may significantly influence the story's direction."

Benchmark derived from Choose Your Own Adventure games; up to **89% accuracy** achieved.

## Task definition

Identify moments where characters make choices that substantially determine plot direction. Uses interactive fiction game structures to locate narrative branching points **driven by character agency rather than external events**.

## Dataset construction — the key methodological move

- **Source:** MACHIAVELLI dataset, **134 CYOA games**
- **Total tasks:** **1,462** binary classification instances
- **Class distribution:** 731 positive / 731 negative (balanced)
- **Extraction:** game graphs parsed into triplets `<node1; action; node2>` — node1 = pre-decision text, action = player choice, node2 = post-decision text

**Ground truth definition (verbatim):** positive examples required **"more than one possible action" branching from a node in the game graph**, ensuring actual decision points.

This is the whole point. **Agency-relevance is read off the graph topology — out-degree > 1 — not off the prose and not off a rater.** It is objective, deterministic, and free. It is available *only* because someone authored an explicit branching structure.

### Data splits (verbatim)

| Class | Train | Dev | Test |
|-------|-------|-----|------|
| Positives | 511 | 110 | 110 |
| Negatives | 256 | 55 | 55 |
| Hard Negatives | 255 | 55 | 55 |
| **Total** | **1022** | **220** | **220** |

Note the **hard negatives** — presumably text that reads like a decision point but has out-degree 1 in the graph. That is *exactly the railroading case*: prose that looks like a choice but isn't. The benchmark is, in effect, a railroading detector.

## Baseline results (verbatim)

| Model | Test Accuracy | Size |
|-------|---------------|------|
| DeBERTa-v3-large | **89%** | 340M |
| DeBERTa-v3-base | 85% | 110M |
| ALBERT-v2-base | 84% | 11M |
| BERT-base | 79% | 110M |
| GPT-4-turbo (0-shot) | **62%** | unknown |
| GPT-3.5-turbo (0-shot) | 55% | unknown |

Human performance was **not** reported.

Two striking observations:
- **A 11M-parameter ALBERT (84%) beats GPT-4-turbo 0-shot (62%) by 22 points.** Fine-tuned small encoders crush a much larger model prompted zero-shot. The signal is learnable and local.
- **GPT-4-turbo at 62% on a balanced binary task is barely above chance (50%).** A frontier LLM, reading the text around a decision point, largely *cannot tell* whether the choice actually branches.

## Relevance to companion-eval-platform

1. **This is the existence proof that objective agency ground truth requires structure, not text.** CHADPOD gets a clean, deterministic label — "does this choice branch?" — by reading `out-degree > 1` from an authored graph. No survey, no judge, no α problem. But the labels exist **only because the CYOA authors built the graph**. Our platform has no such graph: the branching structure of an LLM roleplay scene is implicit in the model's weights and is never materialized. **We cannot read our topology; we would have to sample it.** That is precisely the argument for counterfactual replay — re-running from a checkpoint with a different input is how we *construct* the graph edge that CHADPOD reads for free.

2. **GPT-4-turbo at 62% is the strongest available evidence against an LLM-judge agency metric.** If we were tempted to shortcut counterfactual replay by asking a model "did this choice matter?", this is the answer: on a balanced binary task with authored ground truth, GPT-4-turbo scores 62%. Twelve points above coin-flip. **An LLM cannot detect railroading from text.** Which stands to reason — the branching information simply isn't in the prose, and a railroaded scene is textually designed to look identical to a branching one (that is what Fendt's Story 2 is). This closes off the cheap path and makes counterfactual replay not just the best option but close to the only one.

3. **The hard negatives are the exact construct we care about.** Text that presents as a meaningful choice but has out-degree 1 *is* railroading. That CHADPOD needed a dedicated hard-negative class — and that models still only reach 89% *with* fine-tuning on in-domain data — tells us surface-level choice-ness and actual branching are close to orthogonal in the text. Reinforces Fendt: the fake is textually indistinguishable from the real, for humans *and* for models.

4. **Useful asymmetry: 89% is achievable with fine-tuning, ~62% without.** If we ever generate counterfactual-replay labels at scale on our own platform, we would have exactly the training data needed to fine-tune a small cheap encoder to predict branch-ness directly — a 340M DeBERTa hits 89%. That is a plausible path from "expensive replay-based metric" to "cheap online monitor", but note the ordering: **replay first to make labels, then distill.** Not the other way around.

5. **Caveat on transfer.** CHADPOD's positives come from CYOA graphs with discrete, enumerated choices. Our users type free text — there is no enumerated action set and no node. "Out-degree" is not even well-defined for a continuous input space; the counterfactual we construct is one sample from an unbounded space of alternative user inputs. So CHADPOD's ground truth doesn't port directly; it ports as an *analogy* that tells us what we'd need to build. It also flags a real design question for our metric: **which counterfactual inputs do we replay?** A randomly-chosen alternative user turn is not obviously the right comparison — CHADPOD's authors got to use the author's own enumerated alternatives.

6. **Related:** `game-illusion-of-agency-fendt.md` (humans can't tell either), `game-agency-relevance-thue.md` (the divergence-metric shape).
