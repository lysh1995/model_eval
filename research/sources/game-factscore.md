---
title: "FACTSCORE: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation"
url: https://aclanthology.org/2023.emnlp-main.741/
authors: Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# FactScore — atomic fact decomposition + verification (EMNLP 2023, pp. 12076–12100)

**Status: the source for "decompose generated text into atomic facts and verify each against a record." That is precisely the world-state-auditor architecture. The headline "<2% error rate" is real but is an AGGREGATE-LEVEL number that does not mean what an architect skimming the abstract will think it means. The per-fact number — the one our design actually depends on — is F1 53.3–83.2 and is buried in Appendix B.2.**

arXiv: https://arxiv.org/abs/2305.14251

> **Verification note.** Every number below extracted from the **primary PDF via pypdf**, not from a summarizer. This mattered: a WebFetch pass over the arXiv HTML returned the abstract's "<2% error" framing plus a fabricated "Figure 3" model ranking with invented per-model FActScores (GPT-4 "~67%", Alpaca 7B "~22%", "Human baseline ~89%", "r=0.99") — those specific values were not verifiable in the PDF and are **not** reproduced here. Sibling agents in this batch independently caught WebFetch fabricating tables for three other papers in this source set (an invented `NumOps≥1` column for entity-tracking; an invented Fleiss' κ=0.73 for Skill Check; mutually contradictory ContractNLI values across two fetches of one URL). **Treat any number in this corpus not marked as PDF-verified as unverified.**

## Method

Three-stage pipeline:
1. **Decompose** each generation into *atomic facts* — short statements each carrying one piece of information. Sentences are split automatically, then fed to InstructGPT to break into atomic facts.
2. **Verify** each atomic fact against a knowledge source (Wikipedia) as `Supported` / `Not-supported` / `Irrelevant`.
3. **Aggregate**: FActScore = % of atomic facts that are Supported.

Task domain: **people biographies only**, knowledge source Wikipedia.

Estimator variants: `No-context LM`, `Self-check LM` (SelfCheckGPT-style, no retrieval), `Retrieve→LM`, `NP` (nonparametric probability), `Retrieve→LM + NP` (ensemble). LM_EVAL ∈ {LLAMA 65B, Inst-LLAMA 7B, ChatGPT}. Retriever: GTR.

**Why atomic decomposition at all** — the paper's own motivation, verbatim, and it is a direct argument for our design:

> "using a sentence as a unit; however, **even a single sentence is a mix of supported and unsupported facts, e.g., in 40% of the cases with ChatGPT.** Previous and concurrent work either (1) defines an additional label of `partial support` **whose definition may be subjective and can lead to low agreement**, or (2) takes the strictest definition of `support` that requires every piece of information to be supported, which ignores the partial support cases…"

⭐ **Sentence-level or turn-level consistency judgments are ill-posed** — 40% of ChatGPT sentences mix true and false content. Any "is this turn consistent? y/n" rubric is asking raters to collapse a mixture into a binary, which *manufactures* the low agreement. **This is a mechanism for our α = 0.25–0.34 problem, not just an analogy.**

## Table 1 — data statistics and human FActScore (verbatim)

| | InstGPT | ChatGPT | PPLAI |
|---|---|---|---|
| Use search | ✗ | ✗ | ✓ |
| % responding | 99.5 | 85.8 | 90.7 |
| # tokens / response | 110.6 | 154.5 | 151.0 |
| # sentences / response | 6.2 | 7.9 | 9.8 |
| **# facts / response** | **26.3** | **34.7** | **40.8** |
| *Statistics of the labels* | | | |
| Supported | 42.3 | 50.0 | 64.9 |
| Not-supported | 43.2 | 27.5 | 11.1 |
| Irrelevant | 14.0 | 8.3 | 14.8 |
| Abstains from answering | 0.5 | 14.2 | 9.3 |
| **FACTSCORE** | **42.5** | **58.3** | **71.5** |

InstGPT = InstructGPT, PPLAI = PerplexityAI.

**~26–41 atomic facts per short (110–155 token) response.** A roleplay turn is comparable in length. Scale that to a 100-turn session: **~3,000 atomic facts per conversation** to extract, store, and cross-check pairwise-ish against a growing record. This is the cost driver nobody budgets for.

## Human annotation cost and agreement

> "15–25 USD per hour. Annotation requires extensive effort and time, leading to the **cost of $4 per generation**. We assign two freelancers for the 10% of the data and calculate the agreement rate: **96%, 90% and 88%** for InstructGPT, ChatGPT and PerplexityAI, respectively."

**Caveats on the agreement number — important, and it cuts *both* ways:**
- It is **raw percent agreement, not chance-corrected.** No κ is reported anywhere in the paper.
- It is measured on **only 10% of the data, with 2 annotators.**
- **Derived κ (MY calculation, not the paper's — treat as indicative only):** using Table 1's label marginals to compute chance agreement p_e, then κ = (p_o − p_e)/(1 − p_e):
  - InstructGPT: p_e ≈ 0.385 → **κ ≈ 0.94**
  - ChatGPT: p_e ≈ 0.452 → **κ ≈ 0.82**
  - PerplexityAI: p_e ≈ 0.455 → **κ ≈ 0.78**
  These assume independent annotators drawing from the observed marginals; the paper gives no confusion matrix, so they are estimates.

⭐⭐ **This is the most encouraging finding in the entire source set, and it is the one that justifies the world-state-record programme.** Atomic-fact-vs-explicit-source verification gets **κ ≈ 0.78–0.94** from humans. Compare: roleplay aesthetics **α = 0.25–0.34**; DECODE contradiction unanimity **65.28%** with no κ published at all (`game-decode-contradiction.md`). **The agreement gradient tracks how tightly the judgment is bound to a named referent** — "is claim X supported by record entry Y" ≫ "does this turn contradict something" ≫ "is this good." *That gradient is the argument for the record.* Grounding the question in an explicit, citable entry is what buys the agreement — which converges exactly on DECODE's supporting-evidence design and its −13pp Strict metric.

**But the caveat that guts the transfer** (Limitations, verbatim):

> "All of our experiments focus on people biographies and Wikipedia, because many LMs can generate biographies with **objective and specific facts (rather than subjective and vague ones)** and Wikipedia has a high coverage for them."

> "FACTSCORE is **not applicable when the facts are more nuanced, open-ended, and debatable** … or with a knowledge source whose text **frequently conflicts with each other**. Moreover, **FACTSCORE may not be suitable for the human-written text that is nuanced and includes intentional or implicit deception.**"

⭐⭐⭐ **Read that last sentence against our product. Fiction *is* intentional deception.** Characters lie. Narrators are unreliable. Dreams, hypotheticals, in-character bluffing, planned retcons, and secrets-the-character-doesn't-know-yet are *features* of good roleplay, not defects. And a roleplay canon is exactly "a knowledge source whose text frequently conflicts with itself" as the story revises itself. **The authors explicitly disclaim our use case.** The κ ≈ 0.78–0.94 was purchased by choosing a domain engineered to be undebatable; we do not get to inherit it for free.

## ⭐ Table 3 — Error Rate (ER), the headline metric (verbatim)

ER = "the difference between the ground truth and the estimated FACTSCORE". `retrv` = retrieval used. `+`/`−` = over/under-estimation by more than 5% absolute. `ranking` ✓ = preserves the ground-truth ranking of the three subject LMs.

| Evaluator | retrv | InstGPT ER | InstGPT FS | ChatGPT ER | ChatGPT FS | PPLAI ER | PPLAI FS | ranking |
|---|---|---|---|---|---|---|---|---|
| **Human (ground truth)** | | | 42.5 | | 58.3 | | 71.5 | |
| *Trivial* | | | | | | | | |
| Always `Supported` | | 57.5 | 100.0 + | 41.7 | 100.0 + | 28.5 | 100.0 + | ✗ |
| Always `Not-supported` | | 42.5 | 0.0 − | 58.3 | 0.0 − | 71.5 | 0.0 − | ✗ |
| **Always Random** | | **7.5** | 50.0 + | **8.3** | 50.0 − | **21.5** | 50.0 − | ✗ |
| *I-LLAMA* | | | | | | | | |
| No-context LM | ✗ | 7.1 | 49.6 + | 7.8 | 50.5 − | 34.7 | 36.8 − | ✗ |
| NP | ✓ | 14.8 | 57.3 + | 13.7 | 72.0 + | **1.4** | 72.9 | ✓ |
| Retrieve→LM | ✓ | 14.1 | 56.6 + | 17.1 | 75.4 + | **0.1** | 71.6 | ✗ |
| **Retrieve→LM + NP** | ✓ | **1.4** | 41.1 | **0.4** | 58.7 | **9.9** | 61.6 − | ✓ |
| *ChatGPT* | | | | | | | | |
| No-context LM | ✗ | 39.6 | 82.1 + | 31.7 | 90.1 + | 3.3 | 74.8 | ✗ |
| Retrieve→LM | ✓ | 5.1 | 47.6 + | 6.8 | 65.1 + | 0.8 | 72.3 | ✓ |
| Retrieve→LM + NP | ✓ | 5.2 | 37.3 − | 4.7 | 53.6 | 8.7 | 62.8 − | ✓ |

### Three things this table says that the abstract does not

1. **"Always Random" — a coin flip — achieves ER 7.5 / 8.3 / 21.5.** A trivial baseline that reads nothing beats most real estimators on two of three subjects. **ER is a very forgiving metric** because it is a difference of aggregates: a coin flip lands near 50%, and the ground truth happens to be near 50%. Any metric where random scores 7.5% "error" is not measuring understanding.

2. **The "<2% error rate" is a per-subject cherry-pick.** `Retrieve→LM + NP` gets 1.4 / 0.4 but **9.9 on PerplexityAI**. `Retrieve→LM` alone gets **0.1 on PerplexityAI** but **14.1 on InstructGPT**. **No single configuration is under 2% on all three.** The abstract's claim is assembled by selecting the best variant *per subject model* — which you can only do **after** you have the human annotations you were trying to avoid collecting. The paper concedes the mechanism: "When a LM_SUBJ is PerplexityAI, single methods … give a low ER, and **ensemble methods have a higher ER due to an underestimation**." For a **new, unannotated** model — our actual situation — you do not know which variant to use, and the honest expected error is **the average or worst case (~2–10%), not 0.4%.**

3. **The FS columns show the errors are large and merely cancel.** Best-ER estimator on InstructGPT reports FS 41.1 vs human 42.5 — but that near-match is not the sum of near-matches; see F1_MICRO below.

## ⭐⭐ Appendix B.2 — ER vs F1_MICRO. The paper explicitly warns the headline is an aggregate.

The paper's own framing, verbatim:

> "**F1_MICRO cares about the individual decision, while ER cares about the aggregated estimation.** An evaluator that has a high (better) F1_MICRO but always overestimates or underestimates factual precision may have a higher (worse) ER … Conversely, **an evaluator that has a lower (worse) F1_MICRO but is not biased toward overestimation nor underestimation may have a lower (better) ER**."

Figure 4 is the authors *demonstrating the metric inverts the ranking*: Evaluator A has AccuracyMICRO 67% / ER 10%; Evaluator B has AccuracyMICRO 57% / **ER 5%**. "Evaluator A is better in F1_MICRO, and Evaluator B is better in ER." **The worse per-fact evaluator wins on the headline metric.**

F1_MICRO definition: over atomic facts, with G = ground-truth `Not-supported` set and P = predicted `Not-supported` set — i.e. **it measures how well the estimator identifies the facts that are NOT supported.** That is exactly our task (find the contradiction), and it assumes **oracle atomic facts (decomposed by human experts) are given** — so it *excludes* decomposition error entirely.

**Table 9: Results in F1_MICRO using Inst-LLAMA 7B as LM_EVAL** (verbatim)

| Evaluator | retrv | InstGPT | ChatGPT | PPLAI |
|---|---|---|---|---|
| Always `Supported` | - | 0.0 | 0.0 | 0.0 |
| Always `Not-supported` | - | **71.4** | **58.3** | 30.9 |
| Random | - | 52.2 | 45.0 | 25.7 |
| No-context LM | ✗ | 61.2 | 52.2 | 31.4 |
| Self-check LM | ✗ | 66.0 | 48.4 | - |
| Retrieve→LM | ✓ | 78.7 | 61.9 | 51.1 |
| NP | ✓ | 70.0 | 56.6 | 51.4 |
| **Retrieve→LM + NP** | ✓ | **83.2** | **70.5** | **53.3** |

### ★★★ THE NUMBER. The same estimator, same rows, same paper:
- **Aggregate: ER 1.4 / 0.4 / 9.9 → "less than 2% error."**
- **Per fact: F1_MICRO 83.2 / 70.5 / 53.3.**

**"<2% error" and "F1 53.3" are the same system.** The aggregate is accurate because false-positives and false-negatives cancel, not because the individual judgments are right. On PerplexityAI the per-fact F1 is **53.3** — and the **trivial "Always Not-supported" baseline scores 30.9** while **Random scores 25.7**. The sophisticated retrieval+NP ensemble beats a constant baseline by ~22 points.

**Worse, on InstructGPT the constant baseline "Always Not-supported" scores F1 71.4** — the full pipeline (83.2) beats *"assume everything is a hallucination"* **by 11.8 points.** (This is inflated by InstructGPT's 43.2% Not-supported base rate, which is what makes a constant guess look strong — the same base-rate effect that collapses DECODE's precision to 23.94 in the opposite direction.)

**Table 10: Ablation in F1_MICRO on choice of LM_EVAL** (verbatim) — the cost/quality curve

| Evaluator | retrv | InstGPT | ChatGPT | PPLAI |
|---|---|---|---|---|
| *LLAMA 65B* | | | | |
| No-context LM | ✗ | 22.2 | 20.0 | 18.6 |
| Retrieve→LM | ✓ | 54.6 | 42.1 | 36.1 |
| Retrieve→LM + NP | ✓ | 80.1 | 67.1 | 55.1 |
| *Inst-LLAMA 7B* | | | | |
| No-context LM | ✗ | 61.2 | 52.2 | 31.4 |
| Retrieve→LM | ✓ | 78.7 | 61.9 | 51.1 |
| Retrieve→LM + NP | ✓ | 83.2 | 70.5 | 53.3 |
| *ChatGPT* | | | | |
| No-context LM | ✗ | 40.0 | 25.4 | 25.4 |
| **Retrieve→LM** | ✓ | **87.5** | **80.2** | **65.8** |
| Retrieve→LM + NP | ✓ | 86.6 | 77.8 | 60.8 |

**Best per-fact F1 anywhere in the paper: 87.5 / 80.2 / 65.8** (ChatGPT + retrieval). **Even with a frontier LM_EVAL, oracle human-decomposed atomic facts, and a clean Wikipedia knowledge source, per-fact verification F1 on the hardest subject is 65.8.** Note Inst-LLAMA **7B beats LLAMA 65B** — scale is not the lever; **retrieval is** (No-context 22.2 → Retrieve 54.6 with LLAMA 65B, a +32 point jump).

**Table 11: QA vs TF Prompting (F1_MICRO, Inst-LLAMA 7B)** (verbatim)

| Evaluator | InstGPT | ChatGPT | PPLAI |
|---|---|---|---|
| Always `Supported` | 30.8 | 37.1 | 45.0 |
| Always `Not-supported` | 35.7 | 29.1 | 15.5 |
| Random | 50.5 | 50.2 | 43.2 |
| *QA Prompting* | | | |
| No-context LM | 56.5 | 48.8 | 32.5 |
| Self-check LM | 65.3 | 63.2 | - |
| Retrieve→LM | 65.3 | 58.2 | 47.3 |
| *TF Prompting* | | | |
| No-context LM | 57.3 | 55.3 | 41.7 |
| Self-check LM | 68.0 | 61.9 | - |
| **Retrieve→LM** | **78.9** | **71.4** | **69.2** |

**Prompt format is worth up to 22 F1 points** (QA 47.3 → TF 69.2 on PPLAI). Failure mode named: "generated questions often being **overly vague or ambiguous**" — e.g. for the fact `Samuel Oboh is an architect`, the model asks "What is Samuel Oboh's job?", expects "Architect", gets "Vice President", and scores it wrong. **A verification harness's phrasing is a bigger lever than its model size** — and this is a silent, uninstrumented failure.

**Table 12: Retrieval system ablation (F1_MICRO)** (verbatim)

| Retrieval | InstGPT | ChatGPT | PPLAI |
|---|---|---|---|
| BM25 | 78.5 | 70.8 | 69.1 |
| GTR Large | 78.9 | 71.4 | 69.2 |
| GTR xLarge | 79.2 | 71.3 | 69.0 |

**BM25 ≈ GTR xLarge (78.5 vs 79.2).** Dense retrieval buys ~0.7 points over keyword search. **Do not spend money on a fancy retriever for the record lookup** — spend it on the verification prompt (+22) and the LM_EVAL (+9).

## Self-check without retrieval underperforms — bears directly on SelfCheckGPT

> "Self-check LM outperforms no-context LM by 4–11%, which confirms findings from Manakul et al. (2023). **However, both significantly underperform methods that use retrieval.** This is in contrast to Manakul et al. (2023) that reports that Self-check without retrieval achieves performance that is close to that with retrieval, **likely because the data in Manakul et al. (2023) contains more frequent entities.**"

⭐ **A direct, named contradiction of SelfCheckGPT's central claim**, with a diagnosis: SelfCheckGPT looks good on *popular* entities the model already knows. Self-check 66.0 vs Retrieve→LM+NP 83.2 on InstructGPT. **Roleplay canon is the least frequent "entity" imaginable — it was invented five minutes ago and appears in exactly one document.** Cross-reference `game-selfcheckgpt.md`. Sampling-based self-consistency is the *worst-positioned* method for our problem, and this paper says so with numbers.

## Relevance to companion-eval-platform

1. **⭐⭐⭐ Never cite "<2% error" as evidence the auditor will work. It is an aggregate-cancellation artifact.** Same system, same table: **ER 0.4–9.9% but per-fact F1 53.3–83.2.** The paper *itself* devotes Appendix B.2 + Figure 4 to demonstrating that ER and F1_MICRO **rank evaluators in opposite orders**. Our product makes **per-fact** decisions ("turn 47 contradicts record entry 12"), so **F1_MICRO is our metric and ER is irrelevant to us.** If a design doc says "FactScore shows atomic verification is 98% accurate," it is wrong by ~30–45 points. Budget **F1 ≈ 0.65–0.85 in the best case**, and that is *with* oracle decomposition, a clean knowledge source, and an undebatable domain — none of which we have.

2. **⭐⭐ The agreement gradient is the real deliverable, and it validates the record — with a bounded promise.** Human κ ≈ 0.78–0.94 (my derivation) on atomic-fact-vs-source, vs DECODE's 65.28% unanimity on contradiction, vs α = 0.25–0.34 on aesthetics. **Binding the judgment to a specific citable record entry is what buys agreement.** This is the strongest available evidence for building the world-state record *at all*, and it converges with DECODE's supporting-evidence design from a different direction. **But the honest version of the claim is:** the record raises the ceiling on *human* agreement, which is a precondition for a good metric — it does **not** make the *automated* detector accurate (F1 still 53–87). Two different problems; the record only solves the first. Do not let the κ number be quoted as if it were the detector's number.

3. **⭐⭐ The authors explicitly disclaim fiction.** "not suitable for … text that is nuanced and includes **intentional or implicit deception**"; "not applicable when the facts are more nuanced, open-ended, and debatable"; not for "a knowledge source whose text frequently conflicts with each other." **Roleplay is all three at once.** A character who lies is not a contradiction; a dream sequence is not a contradiction; a deliberate retcon is a *feature*. **Our auditor's hardest problem is not detecting mismatches — it is distinguishing an in-fiction mismatch (good) from an out-of-fiction one (bad), and FactScore offers zero traction on that.** This distinction does not exist in any paper in this source set. It is the actual research gap and it is ours to own. Concretely: the record needs a *diegetic status* field (asserted-by-narrator / claimed-by-character / dreamed / retconned), or the auditor will flag every lie a character tells.

4. **⭐ Atomic decomposition is the right primitive, and it explains our α problem mechanistically.** "even a single sentence is a mix of supported and unsupported facts, **e.g., in 40% of the cases**." Our raters were asked to score whole turns/sessions on mixed content — that *manufactures* disagreement independent of rater skill. The paper also names the trap in the obvious fix: a `partial support` label "**may be subjective and can lead to low agreement**." So the fix is **not** a 3-point scale; it is **finer units with a cited referent**. This is a concrete, testable redesign of our rubric.

5. **⭐ Cost is the sleeper risk, and it scales super-linearly.** ~26–41 atomic facts per 110–155-token response ⇒ **~3,000 facts per 100-turn session**. Human annotation ran **$4 per single generation** at $15–25/hr — a 100-turn session is ~$400 to annotate by hand, which caps our gold-set size hard and should be planned now, not discovered later. And unlike biographies (one static Wikipedia page), our record **grows during the conversation**, so late turns check against a larger record. Combined with the LongStoryEval finding that incremental-update evaluation was **both worst and most expensive** due to "accumulating inconsistency" (`game-narrative-consistency.md`), the naive rolling-canon design is the one architecture with published evidence against it.

6. **Where to spend, from the ablations — a ranked, evidence-backed list.** Verification prompt format **+22 F1** (QA 47.3 → TF 69.2); LM_EVAL quality **+9** (Inst-LLAMA 83.2 → ChatGPT 87.5 on InstGPT; +32 for retrieval on LLAMA 65B); retriever sophistication **+0.7** (BM25 78.5 → GTR xLarge 79.2). **Retrieval-vs-none is the single biggest lever (+32); retriever *quality* is nearly free.** Use BM25 over the record and spend the budget on prompt engineering and eval-model quality. Also note **Inst-LLAMA 7B > LLAMA 65B** — instruction tuning beats 9× scale for this task, so a small tuned verifier is viable at production cost.

7. **Beware trivial baselines — report them or be embarrassed by them.** "Always Random" gets **ER 7.5**; "Always Not-supported" gets **F1_MICRO 71.4** on InstructGPT. Both are meaningless systems. **Every number we publish must be accompanied by a constant-prediction and a random baseline at the true base rate**, or it is uninterpretable. This is the same lesson DECODE teaches from the other side (95.73% accuracy by always predicting "no contradiction" at 4.27% prevalence). **Across both papers the pattern is identical: the headline metric is chosen where the base rate flatters it.**

8. **Kills self-consistency for our use case, with a named mechanism.** FactScore reproduces SelfCheckGPT's gain over no-context (+4–11%) but shows both "significantly underperform methods that use retrieval," diagnosing SelfCheckGPT's favorable results as an artifact of **frequent entities**. Roleplay canon is maximally infrequent — invented in-session, present in one document, zero pretraining support. **Retrieval against an explicit record is not merely better than sampling-based self-consistency for us; self-consistency's published advantage is an artifact that specifically will not transfer.** See `game-selfcheckgpt.md` (0.93→0.45 F1 synthetic→organic collapse).
