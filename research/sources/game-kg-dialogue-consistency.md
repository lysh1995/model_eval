---
title: "Neural Path Hunter: Reducing Hallucination in Dialogue Systems via Path Grounding"
url: https://aclanthology.org/2021.emnlp-main.168/
authors: Nouha Dziri, Andrea Madotto, Osmar Zaiane, Avishek Joey Bose
year: 2021
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Neural Path Hunter (Dziri et al., EMNLP 2021, pp. 2197–2214)

**Status: the closest published analogue to our "audit a turn against a structured record" design. It builds exactly the thing we want — a token-level critic that flags claims contradicting a knowledge graph — and the honest headline is that the critic's recall is 61.02% and the refined output still hallucinates 56.5% of the time by human judgement.**

Primary: https://aclanthology.org/2021.emnlp-main.168/ · arXiv https://arxiv.org/abs/2104.08455 · code https://github.com/nouhadziri/Neural-Path-Hunter

Architecture: **generate-then-refine**, applied post-hoc to *any* dialogue model "without retraining the model." Two modules: (1) a **token-level hallucination critic** that flags and masks suspect entity mentions; (2) an **entity mention retriever** that re-queries the k-hop subgraph for a replacement.

## Setup

**Dataset: OpenDialKG** (Moon et al., 2019) — "the only publicly available dataset that provides open-ended dialogue responses grounded on paths from a given KG." Freebase subgraph: **~1.2M triples, ~101k distinct entities, 1357 distinct relations.** Domains: movie, music, sport, book.

⚠️ **No official split.** The authors randomly split 80/10/10 → **61778 train / 7933 valid / 7719 test**; after filtering to only utterances annotated with a KG path, **23314 / 2954 / 2954**. So **~62% of the corpus is discarded as un-groundable chit-chat.** Hold onto that number — see relevance #5.

**Formalisation:** dialogue history `D = (x_1..x_n)`, triples `K_n = (t_1..t_j)`, each `t_i = ⟨[SBJ],[PRE],[OBJ]⟩`. Response `x̄_{n+1}` must be faithful to a non-empty subset `M_n ⊂ K_n`. Entity mentions are spans `m_i = (m_i, m_i^b, m_i^e)`.

**Two hallucination types — the taxonomy is the reusable part:**
- **Extrinsic** — mention is not a `[SBJ]`/`[OBJ]` in `M_n` at all (invented entity).
- **Intrinsic** — mentions are real but the *path between them* is unsupported; a `[PRE]` is misused. Example: "Crescendo was written by Becca Fitzpatrick" → "Becca Fitzpatrick was written by Crescendo."

**Critic training data is synthetic** (no labelled data exists). Corruptions: extrinsic = replace each `m_i` with a same-type entity *not* in `G_c^k` or `D`; intrinsic = swap `[SBJ]`/`[OBJ]` pairs. **60%/40% extrinsic/intrinsic split.** Critic = RoBERTa-large, sequence labelling, binary label per word position, lr 2e-5, 5 epochs.

## Result 1 — How much do KG-grounded dialogue models hallucinate at all? (§2.1)

**Table 2 / Table 7 — human assessment of 1500 GPT2-KG responses (300 × 5 decoding strategies), mean % ±90% CI. 3 annotators/example, majority vote, Krippendorff's α = 0.72.**

| Decoding | Hallucination (Ex) | (In) | (B) | Faithful | Generic | Coherence | Fluency |
|---|---|---|---|---|---|---|---|
| Greedy | 17.66 ± 2.6 | 2.00 ± 3.5 | 1.66 ± 0.5 | 69.00 ± 3.2 | 9.66 ± 2.7 | 81.66 ± 3.2 | 95.67 ± 1.6 |
| Beam Search | 18.33 ± 2.8 | 3.33 ± 3.8 | 4.00 ± 1.8 | 68.00 ± 3.9 | 6.33 ± 2.7 | 83.33 ± 1.6 | 97.00 ± 1.9 |
| Nucleus 0.9 | 25.33 ± 2.1 | 4.00 ± 3.6 | 2.33 ± 3.6 | 64.66 ± 2.3 | 3.66 ± 3.2 | 83.66 ± 2.4 | 99.10 ± 0.6 |
| Nucleus 0.5 | 23.33 ± 2.2 | 5.33 ± 3.1 | 4.33 ± 0.8 | 59.90 ± 2.5 | 7.00 ± 2.6 | 87.66 ± 2.1 | 98.34 ± 0.4 |
| Top20 | 28.33 ± 1.5 | 7.00 ± 2.6 | 5.00 ± 1.5 | 55.00 ± 0.6 | 4.66 ± 1.8 | 80.33 ± 1.6 | 97.34 ± 0.5 |

"Ex", "In", "B" = extrinsic, intrinsic, both.

**The paper's three observations, verbatim-adjacent:**
1. "Humans notice most hallucinations in KG-grounded dialogue systems are **extrinsic**." (In OpenDialKG, "54.80% of the responses contain extra entity mentions that are not supported by either D or G_c^1.")
2. Greedy hallucinates least; **top-k sampling highest at 40.33% total.**
3. ⭐ "Increased diversity in response generation —i.e. (less generic), is positively correlated with an increase in hallucination."

> ⭐ **The diversity/faithfulness tradeoff is measured here, not asserted.** Greedy: 21.32% total hallucination, 9.66% generic. Top20: 40.33% total hallucination, 4.66% generic. **Halving genericness roughly doubles hallucination.** Note the ±CIs on the intrinsic column (±3.5 on a 2.00 mean) — the intrinsic sub-numbers are noise; only the extrinsic column and the totals are load-bearing.

## Result 2 — ⭐ The critic's precision/recall/F1 (Table 5)

**Evaluated on 500 human-annotated GPT2-KG greedy responses (span-level hallucination annotation), Krippendorff's α = 0.73.**

| Model | Precision | Recall | F1 |
|---|---|---|---|
| RoBERTa-Intrin | 44.9 | 32.54 | 37.73 |
| RoBERTa-Extrin | 68.65 | 46.94 | 55.76 |
| **RoBERTa-Intrin-Extrin** | **83.05\*** | **61.02\*** | **70.35\*** |

(\* p-value < 0.001)

### The adversarial read on Table 5 — this is the number the consumer wants

1. ⭐ **Recall is 61.02%. The critic misses ~39% of hallucinations.** This is the best configuration, on in-domain data, with a closed 101k-entity Freebase KG and gold triples supplied. **A contradiction auditor that silently passes 2 in 5 contradictions is not a guardrail — it is a source of false confidence.** F1 = 70.35 is carried by precision.
2. ⭐ **Intrinsic hallucination detection is barely functional: F1 37.73, recall 32.54.** The intrinsic-only critic catches **under a third** of relation-level errors — the errors where all the entities are real and only the *relationship* is wrong. And this is the *easy* version: intrinsic negatives were generated by literally swapping `[SBJ]`/`[OBJ]`, a corruption so mechanical that it often produces ungrammatical or absurd text ("Becca Fitzpatrick was written by Crescendo"). **A detector that reaches 37.73 F1 on a synthetic corruption that obvious will do worse on real relational errors.**
3. ⭐ **The gain from combining is suspiciously large and deserves scrutiny.** Extrin-only → Intrin-Extrin jumps precision 68.65 → 83.05 and recall 46.94 → 61.02 on the *same* 500-example eval set. The combined critic saw *both* corruption types in training and so is calibrated to the mixed test distribution; the single-type critics are distribution-mismatched at test. **The 70.35 is partly a measure of train/test corruption-mix alignment, not purely of detection skill.** The paper does not report a critic trained on real (non-synthetic) hallucinations, because none exist — the synthetic-to-real gap is entirely unmeasured.
4. **The critic is the linchpin: without it everything collapses.** NPH-w/o-critic (mask *all* entity mentions rather than flagged ones) is "the worst in every metric compared to all baselines" — FeQA drops to 18.23 / 16.21 / 15.89, i.e. **below the unrefined baselines**, and BLEU roughly halves (11.79 → 6.49). Refinement without accurate flagging is actively harmful.

## Result 3 — Does refinement actually fix it? (Table 3)

**Degree of hallucination pre/post-refinement on OpenDialKG test. Higher FeQA = more faithful. "Critic" = % of responses flagged hallucinated (lower better). (\* p < 0.001.) NPH uses GPT2 embeddings for KG-Entity Memory.**

| Model | FeQA | Critic | BLEU |
|---|---|---|---|
| GPT2-KG | 26.54 | 19.04 | 11.79\* |
| + NPH | 28.98\* | 11.72\* | 11.29 |
| + NPH w/o NCE | 26.02 | 17.91 | 10.98 |
| + NPH w. CompGCN | 26.89 | 15.41 | 11.10 |
| + NPH w/o MLM | 27.01 | 15.02 | 10.88 |
| + NPH w/o critic | 18.23 | 19.65 | 6.49 |
| AdapterBot | 23.11 | 26.68 | 10.56 |
| + NPH | 27.21\* | 18.51\* | 10.74\* |
| + NPH w/o NCE | 24.02 | 25.02 | 9.98 |
| + NPH w. CompGCN | 25.83 | 20.23 | 10.11 |
| + NPH w/o MLM | 26.02 | 21.04 | 10.06 |
| + NPH w/o critic | 16.21 | 27.22 | 5.64 |
| GPT2-KE | 19.54 | 28.87 | 6.24\* |
| + NPH | 26.21\* | 20.34\* | 6.06 |
| + NPH w/o NCE | 20.34 | 24.32 | 5.89 |
| + NPH w. CompGCN | 23.23 | 21.21 | 6.01 |
| + NPH w/o MLM | 24.01 | 22.40 | 5.99 |
| + NPH w/o critic | 15.89 | 30.71 | 3.49 |
| **Gold response** | **33.34** | **5.2** | **—** |

**Headline claim: "a relative improvement of faithfulness over dialogue responses by 20.35% based on FeQA"** (GPT2-KG 26.54 → 28.98 is the +9.2% relative; the 20.35% is the best-case across baselines — GPT2-KE 19.54 → 26.21 = +34%; AdapterBot 23.11 → 27.21 = +17.7%. **Check which pairing any citation of "20.35%" refers to.**)

⚠️ **The gold-response row is the one to read.** Gold responses score **FeQA 33.34** and **Critic 5.2** — i.e. **the critic flags 5.2% of human-written, KG-grounded gold responses as hallucinated (false positives), and FeQA scores ground truth at only 33.34/100.** So: (a) the *metric ceiling* is 33.34, and NPH's 28.98 is 87% of ceiling — a much less impressive framing than "+20.35%"; (b) **NPH-refined output sits at Critic 11.72 vs gold's 5.2 — still more than double the gold hallucination rate.** The gap to human is not closed, it is halved at best.

⚠️ **BLEU gets worse in 2 of 3 baselines** (11.79 → 11.29; 6.24 → 6.06) and the improvements are not starred. The authors' defence is that BLEU is "an imperfect measure," which is true and also convenient.

## Result 4 — Retrieval ablations (Table 4)

**On gold responses from OpenDialKG test.**

| Embedding | Model | Neg. candidates | PPL | Hits@1 | Hits@3 | Hits@10 | MR | MRR |
|---|---|---|---|---|---|---|---|---|
| GPT2-Emb | NPH | SANS | 8.56 | 0.73 | 0.92 | 0.99 | 1.76 | 0.83 |
| GPT2-Emb | NPH | In-Batch Negatives | 8.67 | 0.42 | 0.75 | 0.94 | 3.08 | 0.68 |
| GPT2-Emb | NPH w/o NCE | — | 9.64 | 0.02 | 0.05 | 0.1 | 35.49 | 0.07 |
| GPT2-Emb | NPH w/o MLM | SANS | 9.73 | 0.47 | 0.76 | 0.96 | 2.83 | 0.64 |
| GPT2-Emb | NPH w/o MLM | In-Batch Negatives | 9.70 | 0.20 | 0.43 | 0.75 | 9.22 | 0.36 |
| CompGCN-Emb | NPH | SANS | 8.99 | 0.13 | 0.26 | 0.52 | 14.27 | 0.25 |
| CompGCN-Emb | NPH | In-Batch Negatives | 10.04 | 0.08 | 0.17 | 0.43 | 15.75 | 0.16 |
| CompGCN-Emb | NPH w/o NCE | — | 10.61 | 0.04 | 0.12 | 0.27 | 26.50 | 0.12 |
| CompGCN-Emb | NPH w/o MLM | SANS | 9.63 | 0.08 | 0.21 | 0.47 | 15.52 | 0.20 |
| CompGCN-Emb | NPH w/o MLM | In-Batch Negatives | 9.64 | 0.02 | 0.05 | 0.16 | 80.52 | 0.07 |

**Brittleness exposed by the ablations:**
- ⭐ **Remove the NCE contrastive loss and Hits@1 goes 0.73 → 0.02** ("↓ 70 Hits@1"). MRR 0.83 → 0.07. **The entire retrieval capability lives in the contrastive objective**, not in the LM or the graph.
- ⭐ **CompGCN (global graph structure) is a disaster: Hits@1 0.73 → 0.13.** Learning entity embeddings from the *whole* KG is **5.6× worse** than just using pre-trained GPT2 embeddings of the local subgraph. The authors' explanation: "local information ... is significantly more important to generate a faithful response" as "conversation topics may drift."
- **Negative sampling strategy alone swings Hits@1 0.73 → 0.42** (SANS vs in-batch). **These are not robust numbers; they are the product of a well-tuned stack where every component is load-bearing.**
- ⚠️ **Table 4 is measured on *gold* responses**, not generated ones. Retrieval quality on clean human text is an upper bound on retrieval quality inside the actual refinement loop, where the input is a flawed generated response and the critic's 61% recall has already decided what to mask.

## Result 5 — Human evaluation (Table 6)

**1200 responses (200 × 6). Annotators shown D, K_n, and the retrieved path. The 200 per baseline are responses *already flagged as hallucinated by the critic*.**

| Model | Hallucination | Fluency |
|---|---|---|
| GPT2-KG | 97.5 ± 0.6 | 92.5 ± 1.6 |
| GPT2-KG (+ NPH) | **56.5 ± 1.2** | 88.5 ± 0.7 |
| AdapterBot | 95.5 ± 0.8 | 90.5 ± 0.4 |
| AdapterBot (+ NPH) | **59.0 ± 0.5** | 87.5 ± 1.2 |
| GPT2+KE | 97.0 ± 0.2 | 91.5 ± 0.7 |
| GPT2+KE (+ NPH) | **58.5 ± 0.6** | 86.0 ± 0.9 |

⭐ **This is the most important table in the paper and the paper does not frame it this way.** The authors read the pre-refinement column as critic precision ("the hallucination critic achieves a precision of 97.5% for GPT2-KB responses") and the delta as success ("reduce hallucinations by a large margin 42.05% ... with a marginal drop in fluency (4.32%)").

**The other reading: after the full NPH pipeline runs — critic flags it, MLM masks it, retriever queries the KG, response is refined — 56.5% of those responses are STILL hallucinated by human judgement.** The system fixes slightly under half of what it correctly detects. Combine with the critic's 61.02% recall and the end-to-end picture is:

> **≈ 0.61 (detected) × ≈ 0.44 (successfully repaired) ≈ 27% of hallucinations are actually eliminated end-to-end.**

⚠️ **That 27% is my composition, not the paper's, and it assumes detection and repair success are independent — they are probably positively correlated (a clear-cut extrinsic error is both easier to flag *and* easier to fix), so the true figure is likely somewhat higher.** But the direction is right and the paper never reports an end-to-end rate. **Nothing in this paper supports "KG grounding solves hallucination."**

**Fluency degrades in all three** (92.5 → 88.5; 90.5 → 87.5; 91.5 → 86.0). Refinement is not free.

## Failure modes and limitations

**The paper has no Limitations section** (pre-dates the ACL requirement). Failure modes must be reverse-engineered from the ablations. Named or implied:

1. **Extrinsic ≫ intrinsic**, and intrinsic detection is where the method is weakest (F1 37.73). Relational/temporal errors are the blind spot.
2. **Global graph structure hurts** (CompGCN Hits@1 0.13 vs 0.73) — the method only works on a *local, dialogue-aligned* k-hop subgraph.
3. **Requires a paired KG.** Stated as the paper's own closing caveat: "we considered a paired KG aligned with dialogue but in many other applications, such dialogue to KG alignment may be difficult to easily obtain necessitating the usage of the full graph which is interesting direction for future work."
4. **Entity-mention-shaped errors only.** The critic is a span labeller over entity mentions, seeded by a SpaCy NER tagger. Hallucinations that are not entity mentions — false attitudes, invented events, wrong causality, wrong time — are **out of scope by construction**.
5. **Synthetic training corruptions.** The critic never sees a real hallucination during training. The synthetic→real gap is unmeasured.
6. **Single dataset, single language, one KG.** No external validity evidence.
7. **Metric ceiling problems.** FeQA on gold = 33.34; critic false-positive rate on gold = 5.2%.

## Secondary: Think Before You Speak (Zhou et al., ACL 2022)

**Think-Before-Speaking (TBS)** — https://aclanthology.org/2022.acl-long.88/, arXiv:2110.08501. Zhou, Gopalakrishnan, Hedayatnia, Kim, Pujara, Ren, Liu, Hakkani-Tur. Generate implicit commonsense knowledge (ConceptNet triples) *first*, then condition the response on it.

Relevant numbers: generated knowledge "makes sense" **86.3%** (non-novel) / **85.9%** (novel); "is relevant to the dialogue" **85.7%** / **86.5%**. Human agreement κ = 0.73–0.80. **~77% of generated knowledge is actually used in the response.**

⚠️ **These are from a WebFetch summary of the ar5iv HTML, not verified against the PDF like the NPH numbers above — treat as approximate and re-verify before citing.** The stated failure modes: no multi-hop triple matching; "ConceptNet mostly contains taxonomic and lexical knowledge ... limiting the diversity of generated knowledge"; and the model always generates knowledge whether or not it is needed.

**The useful adversarial framing:** ~85% sensible knowledge sounds strong until you compound it — **~15% of turns are conditioned on knowledge that doesn't make sense**, and ~23% of generated knowledge is ignored by the response anyway. **Externalising structure does not make it correct.** Directly relevant to us: writing a world-state record does not make the record true, and a downstream auditor inherits the extractor's error rate.

## Relevance to companion-eval-platform

**This is the closest thing to a prior implementation of our exact feature — extract structure from dialogue, audit later turns against it, flag contradictions — and it is a cautionary tale, not a blueprint.**

1. ⭐ **61.02% recall is the number to anchor our expectations to, and our setting is much harder.** NPH's critic operates with every advantage we will not have: a closed 101k-entity Freebase KG, **gold triples handed to it at inference**, a single domain, entity-shaped errors only, and a fixed 3-utterance history window. **Our world-state record is self-constructed from dialogue (so it carries its own extraction errors), open-vocabulary, and spans hundreds of turns.** If a specialised RoBERTa-large critic gets 61% recall on the easy version, an LLM auditor over a self-built roleplay record will do worse. **Budget for a contradiction auditor that misses ≥40% of contradictions and say so up front** — the same discipline note 00 applies to ground truth and note 10 applies to noise floors.
2. ⭐ **The extrinsic/intrinsic split is the import, and it maps cleanly onto roleplay — with a warning.** Extrinsic = the companion invents a fact absent from the record (a sister who was never mentioned). Intrinsic = every entity is real but the *relation* is wrong (your sister becomes your ex; the breakup happened *before* the move). **Intrinsic is the failure users actually report in companion products, and intrinsic detection is exactly where NPH is worst: F1 37.73, recall 32.54.** Do not average these into one "consistency" score — the 70.35 combined F1 hides a 37.73 on the half that matters to us. Same dimension-separation argument as the ℱ_act/ℱ_env split in `game-llm-sim-state-prediction.md`.
3. ⭐ **The 5.2% critic score on gold responses is our false-positive floor, and it is a product-killer at scale.** A critic that flags **5.2% of perfectly good human-written responses** as hallucinated, deployed as a live guardrail on a companion product, generates a flood of false alarms — see `scale-multiple-testing-bh-alert-fatigue.md`. **Any contradiction auditor we ship must be evaluated on known-consistent transcripts to measure its false-positive rate, not only on known-contradictory ones.** NPH reports this almost by accident, in one cell. We should report it deliberately, as a headline.
4. ⭐ **Human eval says the pipeline leaves 56.5% of detected hallucinations unfixed. Detection ≠ repair.** If our roadmap has an "auto-correct the contradiction" phase after the audit phase, this is the prior: **repair succeeds slightly under half the time even when detection is correct, and fluency drops ~4–6 points.** Scope the product to *flagging* (surface to the user / to a human reviewer), not silent auto-repair, until we have evidence we beat 44%.
5. ⭐ **The 62% chit-chat discard is the deepest problem for us and it is buried in Appendix A.** OpenDialKG goes 61778 → 23314 training examples because "not all utterances within the same dialogue are grounded on facts from the KG" and un-annotated chit-chat turns get dropped. **NPH only works on the subset of dialogue that is already KG-groundable.** Roleplay is the inverse ratio: the overwhelming majority of turns are affect, banter, subtext, and description — not extractable triples. **The world-state record will cover a small minority of what happens in a scene, and the contradiction auditor will be blind to everything else.** This bounds the *coverage* of the feature independently of its accuracy, and it is the argument a skeptical reviewer will reach for first. We should reach for it first ourselves.
6. **The diversity/faithfulness tradeoff is measured, and it is a direct product tension for us.** Greedy: 21.32% hallucination / 9.66% generic. Top20: 40.33% hallucination / 4.66% generic. **Companion products sample at high temperature precisely to avoid genericness — i.e. they sit at the top-right of this curve by design.** Anything we learn about hallucination at greedy decoding understates production reality by roughly 2×. Worth crossing with `creativity-repetition-dialogue.md` and `multiturn-neural-text-degeneration.md`: the same knob that fixes repetition breaks consistency.
7. **Local-over-global (CompGCN 0.13 vs GPT2 0.73) is a design directive.** Grounding against the *entire* accumulated world-state record is likely to be *worse* than grounding against a locally-relevant slice. "Conversation topics may drift" is exactly our setting. **Retrieve a local subgraph per turn; don't stuff the whole record in context.** Cross-check against `game-zep-graphiti-temporal-kg.md`, which takes the opposite (global temporal graph) bet — this table is evidence against it.
8. **Every component is load-bearing (NCE ablation: Hits@1 0.73 → 0.02).** This is not a robust recipe; it is a tuned stack. **Any "we'll just use an LLM instead of the retriever" simplification should be assumed to land near the ablated numbers until measured.**
9. **The synthetic-corruption trick is worth stealing for test-set construction, with eyes open.** Generating contradictions by perturbing a consistent transcript (swap relations, substitute entities) gives us cheap labelled data with a mechanical ground truth — genuinely attractive per note 00. **But NPH's own results warn us:** the intrinsic corruption (swap SBJ/OBJ) is so crude it yields near-nonsense, and the critic still only reaches 37.73 F1 on it. **Synthetic contradictions are an easier distribution than real ones, so a number measured on them is an upper bound — and the gap between them is unmeasured here and would be a genuine contribution for us to measure.**
10. **"Think Before You Speak" makes the extraction-error point.** ~85% sensible knowledge, ~77% of it used. **Externalising a structured record does not make the record correct**, and a contradiction auditor built on a self-extracted record compounds extractor error with auditor error. If extraction is ~85% and detection recall is ~61%, the composed system is well under half. **Measure the record's own accuracy separately from the auditor's — otherwise a wrong record generates confident false contradictions against perfectly consistent dialogue,** which is failure mode #3 with worse optics.
