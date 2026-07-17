---
title: "Dialogue Natural Language Inference"
url: https://arxiv.org/abs/1811.00671
authors: Sean Welleck, Jason Weston, Arthur Szlam, Kyunghyun Cho
year: 2019
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Dialogue NLI (ACL 2019)

**Status: the founding paper for "consistency-as-NLI". It works — but the headline result is measured on a rigged candidate set, the method only checks the persona (never the dialogue history), and the paper reports NO inter-annotator agreement statistic at all. Read the caveats before citing.**

Full text used: https://ar5iv.labs.arxiv.org/html/1811.00671 (tables extracted from raw HTML, not from a summarizer)

## What it is

Frames dialogue consistency as NLI. Persona sentences and utterances from **Persona-Chat** are annotated with `(e1, relation, e2)` triples; sentence pairs are then labelled **entailment / neutral / contradiction** by *rule over the triples*, not by human judgment.

> "we reduce the problem of consistency in dialogue to natural language inference"

**⚠️ The generative process is the story.** Labels are derived from triple annotations. Contradictions are **manufactured by substitution**:
- **Relation Swap** — swap the relation in the triple
- **Entity Swap** — swap `e2` for a different entity
- **Numerics** — "replacing the sentence's numeric surface form with a different randomly sampled integer"

So the contradiction class is largely **string-substitution artifacts**, not naturally occurring self-contradiction. This matters enormously for us (see Relevance §1).

## Dataset size (Table 2, verbatim)

`(u,p)` = (utterance, persona sentence); `(p,p)` = (persona sentence, persona sentence).

| Data Type | Label | Train (u,p) | Train (p,p) | Valid (u,p) | Valid (p,p) | Test (u,p) | Test (p,p) | Test-Gold (u,p) | Test-Gold (p,p) |
|---|---|---|---|---|---|---|---|---|---|
| Matching Triple | E | 43,000 | 57,000 | 5,000 | 500 | 4,500 | 900 | 3,712 | 615 |
| Misc. Utterance | N | 50,000 | - | 3,350 | - | 3,000 | - | 2,282 | - |
| Persona Pairing | N | 20,000 | 10,000 | 2,000 | - | 2,000 | - | 1,466 | - |
| Relation Swap | N | 20,000 | - | 150 | - | 400 | - | 260 | - |
| Relation Swap | C | 19,116 | 2,600 | 85 | 14 | 422 | 50 | 279 | 44 |
| Entity Swap | C | 47,194 | 31,200 | 4,069 | 832 | 3,400 | 828 | 2,246 | 591 |
| Numerics | C | 10,000 | - | 500 | - | 1,000 | - | 881 | - |
| **Overall** | | **310,110** | | **16,500** | | **16,500** | | **12,376** | |

**Derived label totals** (my arithmetic over Table 2 — not stated in the paper):

| Split | E | N | C | Total |
|---|---|---|---|---|
| Train | 100,000 | 100,000 | 110,110 | 310,110 |
| Test | 5,400 | 5,400 | 5,700 | 16,500 |
| Test-Gold | 4,327 | 4,008 | 4,041 | 12,376 |

*Arithmetic check: C is the most common test class at 5,700/16,500 = **34.55%**, matching the paper's reported Most Common Class = 34.54. On Test-Gold, E is most common at 4,327/12,376 = **34.96%**, matching the paper's 34.96 exactly. The derivation is validated against the paper's own baseline.*

10,832 persona sentences were triple-annotated via Amazon Mechanical Turk.

## ⭐ Inter-annotator agreement: NOT REPORTED

**The paper reports no kappa, no percentage agreement, no alpha.** This is the single biggest gap for our purposes. The *only* agreement-adjacent statement in the entire paper:

> "We additionally create a gold-standard test set (Test Gold) by crowdsourcing three label annotations for each example in the test set. **We keep each test example for which two or more annotators agreed with its dataset label.**"

**Derived from that (my arithmetic, not the paper's):**

| Quantity | Value |
|---|---|
| Test examples | 16,500 |
| Survived (≥2 of 3 annotators agreed with the dataset label) | 12,376 |
| **Survival rate** | **75.01%** |
| **Discarded — fewer than 2/3 humans agreed with the automatic label** | **4,124 (24.99%)** |

**One in four automatically-generated labels could not get 2 out of 3 humans to agree with it.** That is the closest thing to an agreement number this paper contains, and it is not flattering. Note this is *agreement-with-the-dataset-label*, a weaker and more generous measure than inter-annotator agreement among the three annotators — the true pairwise α would be lower still, and is unrecoverable from the paper.

**⭐ Derived per-row survival rate — where the labels are weakest:**

| Data Type | Label | Test (u,p) | Test-Gold (u,p) | Survival |
|---|---|---|---|---|
| Numerics | C | 1,000 | 881 | **88.1%** |
| Matching Triple | E | 4,500 | 3,712 | 82.5% |
| Misc. Utterance | N | 3,000 | 2,282 | 76.1% |
| Persona Pairing | N | 2,000 | 1,466 | 73.3% |
| **Entity Swap** | **C** | 3,400 | 2,246 | **66.1%** |
| **Relation Swap** | **C** | 422 | 279 | **66.1%** |
| **Relation Swap** | **N** | 400 | 260 | **65.0%** |

**The synthetic contradiction classes are exactly the ones humans reject most — a third of Relation-Swap and Entity-Swap contradictions failed verification.** The mechanism that produces the "contradiction" label is the mechanism humans trust least. If you are building a contradiction detector, this is the number to worry about.

## Model accuracy (Table 3, verbatim)

| Model | Valid | Test | Test Gold |
|---|---|---|---|
| ESIM | 86.31 | **88.20** | **92.45** |
| InferSent | 85.82 | 85.68 | 89.96 |
| InferSent SNLI | 47.86 | **46.36** | 47.03 |
| InferSent Hyp. Only | 55.98 | **57.19** | 51.52 |
| Most Common Class | 33.33 | 34.54 | 34.96 |
| ESIM Gold Triples (oracle) | 99.52 | 99.46 | **99.69** |

**⚠️ Three adversarial readings the paper does not foreground:**

1. **Cross-domain transfer collapses.** InferSent trained on SNLI scores **46.36%** on Dialogue NLI test vs **85.68%** trained in-domain — a **39-point** collapse, barely above the 34.54% majority baseline. The paper attributes this to "mismatch in sentence distributions." **You cannot take an off-the-shelf NLI model into dialogue.** Any plan that assumes a pretrained NLI checkpoint will work on our transcripts is refuted by this row.

2. **There ARE hypothesis-only artifacts, despite the spin.** Hyp-only gets **57.19%** on test vs a 34.54% majority baseline — **+22.65 points obtainable without reading the premise at all.** The paper frames this positively:
   > "The hypothesis-only performance (51.52%) is lower than the hypothesis-only baseline for SNLI (69.00%)"
   
   Lower than SNLI's artifacts is not the same as no artifacts. Roughly a fifth of the achievable signal is premise-independent. (Note the paper quotes the Test-Gold figure 51.52 here, the more flattering of the two.)

3. **The oracle gap.** ESIM Gold Triples hits **99.69%** vs ESIM's **92.45%** — the triple contains "sufficient information to achieve near-perfect accuracy." The paper concedes "there is also room for improvement." Read adversarially: the task is nearly solved *when you already have the structured facts*, meaning the residual difficulty is **extraction**, not inference. Our problem is entirely extraction.

## The re-ranking method

Candidates are re-ranked by penalising predicted contradiction with the persona:

s_i^contradict = 0 if the candidate contradicts no persona sentence; otherwise max_j c_i,j (the highest contradiction-class softmax confidence over contradicting (u_i, p_j) pairs).

New score: **s_i^re-rank = s_i − λ(s_1 − s_k) · s_i^contradict**

> "λ and k control the NLI model's influence in re-ranking. For example, if the top candidate has a contradiction score of 1.0, then with λ=1, it will be moved to the k'th position in the ranking. λ=0 corresponds to no re-ranking."

Dialogue model = **key-value memory network** on Persona-Chat. NLI model = **ESIM** trained on Dialogue NLI.

### ⭐⭐ The method never checks the dialogue history

Footnote 6, verbatim:

> "**Future work could consider filtering previous-utterance contradictions (u_i, u_j) as well.**"

**The method only compares each candidate against the static persona list P. It never compares an utterance against what the model said earlier.** Self-contradiction across turns — the thing our platform exists to detect — is explicitly out of scope and deferred to future work. This is the most important sentence in the paper for us, and it is a footnote.

## ⭐ Persona consistency re-ranking results (Table 4, verbatim)

> "The reported metrics are percentages computed over each validation set."

| Metric | Haves Orig. | Haves Rerank | Likes Orig. | Likes Rerank | Attributes Orig. | Attributes Rerank |
|---|---|---|---|---|---|---|
| Hits@1 ↑ | 30.2 | **37.3** | 16.9 | **18.7** | 35.2 | **36.4** |
| Contradict@1 ↓ | 32.5 | **8.96** | 17.6 | **4.1** | 8.0 | **5.7** |
| Entail@1 ↑ | 55.2 | **74.6** | 77.9 | **90.6** | 87.5 | **88.6** |

**Note for the requester:** these three columns are **Haves / Likes / Attributes evaluation sets**, each with an `Orig.` (no re-ranking) vs `Rerank` column — they are **not** the "original vs revised persona" split from Persona-Chat. That orig/revised distinction belongs to a different paper's setup and does not appear in DNLI Table 4.

**⚠️ The candidate set is constructed to make this look good.** Verbatim setup:

> "Each example is associated with candidates U, consisting of the ground-truth utterance u_{t+1}, **10 entailment candidates** with the same triple as u_{t+1}, **10 contradicting candidates** with a different triple than that of u_{t+1}, and **10 random candidates**."

**31 candidates, of which 10 (32%) are deliberately planted contradictions**, and the eval sets are themselves selected as "next-utterances which are likely to yield persona contradiction or entailment." The Contradict@1 drop of 32.5 → 8.96 is measured in an environment engineered to contain contradictions at a rate no real dialogue exhibits, against a fixed candidate pool. **This is a probe of the NLI model's discrimination, not an estimate of real-world contradiction reduction.** Do not quote "contradictions cut by 3.6×" as a deployable expectation.

**⚠️ Hits@1 — the actual quality metric — barely moves.** +7.1 on Haves, **+1.8 on Likes**, **+1.2 on Attributes**. And the absolute values are dismal: **18.7% Hits@1 on Likes after re-ranking.** The model picks the right response under 1 time in 5 even on a 31-candidate set where it should score ~3% by chance. Re-ranking makes the model *less contradictory*, not *more correct*.

## Human evaluation (Table 5, verbatim)

100 conversations per model, ParlAI + MTurk, 1,155 persona sets, ≥5-6 turns, Bayesian calibration for annotator bias.

| Model | Overall Score ↑ Raw | Overall Score ↑ Calibrated | % Consistent ↑ Raw | % Consistent ↑ Calibrated | % Contradiction ↓ Raw | % Contradiction ↓ Calibrated |
|---|---|---|---|---|---|---|
| KV-Mem | 2.11 ± 1.12 | 2.21 ± 0.26 | 0.24 | 0.27 ± 0.07 | 0.23 | 0.25 ± 0.08 |
| KV-Mem + NLI | 2.34 ± 1.21 | **2.38 ± 0.26** | 0.28 | **0.35 ± 0.08** | 0.19 | **0.16 ± 0.06** |

> "The natural language inference re-ranking improves all the metrics, notably the fine-grained consistency score (0.27 vs. 0.35) and contradiction score (0.25 vs. 0.16)."

**⚠️⚠️ The error bars overlap on every single metric. No significance test is reported.**

| Metric | Delta | Std | Overlap? |
|---|---|---|---|
| Overall (calibrated) | 2.21 → 2.38 = **+0.17** | **±0.26** each | **Yes — the effect is smaller than one std** |
| % Consistent | 0.27 → 0.35 = +0.08 | ±0.07 / ±0.08 | Yes (0.27+0.07=0.34 vs 0.35−0.08=0.27) |
| % Contradiction | 0.25 → 0.16 = −0.09 | ±0.08 / ±0.06 | Yes (0.25−0.08=0.17 vs 0.16+0.06=0.22) |

**The headline human-eval claim — that NLI re-ranking improves dialogue consistency — is not statistically established by this table.** The overall-score gain (+0.17) is **two-thirds of a single standard deviation (±0.26)**. n=100 conversations/model. The paper asserts improvement on all three metrics without a test statistic or CI. This is the weakest link in the entire "NLI improves consistency" chain, and it is the load-bearing one — Table 4's big Contradict@1 drop is on the rigged candidate set; Table 5 is the only real-dialogue evidence, and it doesn't separate.

**⚠️ Even where it "works," the absolute numbers are bad:**
- **Overall score 2.38 out of 5** after re-ranking.
- **% Consistent = 0.35** — **65% of utterances are still not consistent with the persona.**
- **% Contradiction = 0.16** — still contradicting on roughly 1 utterance in 6.

The method takes a bad model and makes it a slightly-less-contradictory bad model.

## Stated scope limits

> "We do not consider relationships which require more than two sentences to express"

Combined with footnote 6 (no history checking), the method's reach is: **pairwise, persona-only, ≤2 sentences.**

## Relevance to companion-eval-platform

1. **⭐ The contradiction class is synthetic, and humans reject a third of it.** Relation-Swap and Entity-Swap contradictions survive human verification at only **66.1%** (derived above). A detector trained on DNLI learns "this entity got substituted," not "this character contradicted herself." Our contradictions are *narrative* — a character who claimed to fear water goes swimming — and no entity was swapped. **DNLI's training signal does not contain our phenomenon.** Do not fine-tune on DNLI and expect transfer.

2. **⭐⭐ The method never checks dialogue history (footnote 6).** Candidate-vs-persona only. Our entire construct is utterance-vs-*earlier utterance* over 100 turns. **The founding paper of consistency-as-NLI explicitly does not do the thing we need**, and labels it future work. This is a genuine gap we can claim — but claim it precisely: DNLI *chose* not to; it isn't that they tried and failed.

3. **⭐ Cite the 39-point cross-domain collapse (85.68 → 46.36) as the reason we cannot use an off-the-shelf NLI model.** SNLI→dialogue transfer lands at 46.36% against a 34.54% majority baseline. Any roadmap item reading "use a pretrained NLI checkpoint as the consistency probe" is refuted by this single row. If it doesn't survive SNLI→Persona-Chat, it will not survive Persona-Chat→our roleplay transcripts. Budget for in-domain data.

4. **⚠️ Do NOT cite "re-ranking cuts contradictions 32.5% → 8.96%" as a deployable number.** It is measured on a hand-built 31-candidate set that is **32% planted contradictions**, on eval sets pre-selected for contradiction-proneness. The honest real-dialogue number is Table 5: **0.25 → 0.16 with overlapping error bars and no significance test.** If we put the 3.6× figure in a deck, a reviewer who reads §5.2 will find the candidate construction in a minute.

5. **⭐ The agreement gap is our opening.** This paper reports **no kappa at all** — the field's founding consistency dataset has never published an inter-annotator agreement statistic for its NLI labels. The best available proxy is the **75.01% survival rate** I derived (25% of automatic labels couldn't get 2/3 humans to agree). Put next to note 10's noise-floor work: **if we report a real chance-corrected α for contradiction detection on roleplay, we will be reporting something DNLI never did.** That's a contribution, cheaply.

6. **The oracle result (99.69% from gold triples) says the hard part is extraction.** ESIM with ground-truth triples is essentially perfect; ESIM with sentences is 92.45. Inference over structured facts is solved. **Getting the structured facts out of free-form roleplay prose is the whole problem** — which is an argument for a state-tracking representation over an end-to-end NLI classifier. Feed to note 09 (offline probes).

7. **Hits@1 of 18.7% after re-ranking is a useful humility number.** Consistency filtering does not make a dialogue model good; it makes it less bad on one axis while response quality stays roughly flat (+1.2 to +7.1 Hits@1). If we ship a contradiction filter, we should expect the same decoupling — and we should measure quality separately, or we will claim credit for an improvement we didn't make.
