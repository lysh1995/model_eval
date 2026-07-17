---
title: "Long-Document NLI: ContractNLI (Koreeda & Manning 2021) and DocNLI (Yin et al. 2021)"
url: https://aclanthology.org/2021.findings-emnlp.164/
authors: Yuta Koreeda, Christopher D. Manning (ContractNLI); Wenpeng Yin, Dragomir Radev, Caiming Xiong (DocNLI)
year: 2021
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Long-Document NLI — ContractNLI + DocNLI

**Status: this is the "does NLI survive long context" cluster, and the answer is largely no. Best DocNLI F1 is 61.20. ContractNLI's best contradiction F1 is 0.405. NEITHER PAPER REPORTS A HUMAN CEILING — the human-model gap the consumer asked for does not exist in the literature, and that absence is itself the finding.**

Full texts used (tables extracted from raw HTML, not from a summarizer — see Provenance):
- ContractNLI: https://ar5iv.labs.arxiv.org/html/2110.01799 (arXiv 2110.01799) — Findings of EMNLP 2021
- DocNLI: https://ar5iv.labs.arxiv.org/html/2106.09449 (arXiv 2106.09449) — Findings of ACL-IJCNLP 2021, pages 4913–4922

---

# PART A — ContractNLI (Koreeda & Manning, Findings of EMNLP 2021)

## What it is

Given a contract and a **fixed set of 17 hypotheses**, classify each as **Entailment / Contradiction / NotMentioned**, and identify **evidence spans**.

Abstract, verbatim (emphasis mine):

> "We annotated and release the largest corpus to date consisting of 607 annotated contracts. We then show that **existing models fail badly on our task** and introduce a strong baseline, which (1) models evidence identification as multi-label classification over spans instead of trying to predict start and end tokens, and (2) employs more sophisticated context segmentation for dealing with long documents. We also show that linguistic characteristics of contracts, such as negations by exceptions, are contributing to the difficulty of this task and that **there is much room for improvement**."

Task formulation, verbatim:
> "**Natural language inference (NLI)** Document-level three-class classification (one of Entailment, Contradiction or NotMentioned). **Evidence identification** Multi-label binary classification over spans, where a span is a sentence or a list item within a sentence. **This is only defined when NLI label is either Entailment or Contradiction.**"

## Dataset size (Table 1, verbatim)

| Format | Source | Train | Development | Test | Total |
|---|---|---|---|---|---|
| Plain Text | EDGAR | 83 | 12 | 24 | 119 |
| HTML | EDGAR | 79 | 11 | 23 | 113 |
| PDF | Search engines | 261 | 38 | 76 | 375 |
| **Total** | | **423** | **61** | **123** | **607** |

Split 70:10:20 stratified by format. **17 hypotheses × 607 contracts = 10,319 NLI examples** (derived: train 7,191 / dev 1,037 / test 2,091). Domain is exclusively **non-disclosure agreements (NDAs)**.

**⚠️ 123 test contracts is a very small test set.** The paper runs each experiment 10× with different hyperparameters and reports "the average score of three models with the best development scores" — necessary precisely because the dataset "is modest in size."

## ⭐ Document length (Table 2, verbatim)

| | Number per a document (Avg / Min / Max) | Tokens per an instance (Avg / Min / Max) |
|---|---|---|
| Paragraph | 43.7 / 9 / 248 | 52.8 / 1 / 1209 |
| Span | 77.8 / 18 / 354 | 29.5 / 1 / 289 |
| Token | **2,254.3** / 336 / **11,503** | — / — / — |

Verbatim:
> "An average number of tokens per a document is 2,254.0, which is larger than maximum allowed context length of BERT (512 tokens). Even though an NDA is relatively short for a contract, **86% of documents exceed the maximum allowed context length of BERT.**"

*(Minor internal inconsistency: Table 2 says 2,254.3, prose says 2,254.0.)*

**86% of documents don't fit in the model.** This is the length problem stated as plainly as it gets — and NDAs are described as *short* for contracts. Our 100-turn transcripts are in the same regime.

## Label distribution

Verbatim: "Entailment and NotMentioned occupy a significant ratio of the dataset, but around half of the hypotheses contain both Entailment and Contradiction." Exact per-label counts are only shown as **Figure 2** (a plot) — **not recoverable as numbers from the text.** The paper never tabulates the label distribution.

> "The label distribution is imbalanced and it is naturally multi-task, all the while training data being scarce."

## ⭐ Inter-annotator agreement: NOT REPORTED

**No Cohen's κ, no Fleiss' κ, no Krippendorff's α, no percentage agreement anywhere in the paper.** The annotation procedure, verbatim:

> "Annotation was conducted by a computational linguistic researcher (**the primary annotator**) with a help from workers at Amazon Mechanical Turk. We chose two workers at Amazon Mechanical Turk who were consistently performing well and asked them to **redundantly annotate each document with a priority on coverage**. We merged annotated spans for each document. Finally, **the primary annotator reviewed the merged annotations and adjusted the annotations where necessary.**"

> "For the train split, the primary annotator only reviewed the annotated spans to judge NLI labels and to consolidate the span boundaries. For most of the test split, the primary annotator went through the whole contracts to further improve coverage. **Most of the development dataset and some of the test dataset were annotated exclusively by the primary annotator without a help from the workers.** This allowed us to obtain consistent and high coverage annotations."

**⚠️ Read that last part carefully.** Redundancy was used for *coverage*, then **collapsed by a single adjudicator**, and much of dev/test is **single-annotator**. There is no second independent judgment to compute agreement against — the design makes an agreement statistic *impossible in principle*, not merely omitted. "Consistent" here means "one person did it," which is internal consistency, not reliability. **A single-annotator gold standard on a task the authors describe as hard is a real threat to the validity of every number below**, and the paper does not quantify it.

## Main results (Table 4, verbatim)

Each metric is reported as **value ± std over runs**. Metrics: evidence **mAP** and **P@R80**; NLI **accuracy**, **F1 (C)** = contradiction, **F1 (E)** = entailment.

> "P@R80 is the precision score when the threshold for evidence identification is adjusted to achieve a recall score of 0.8. It was used in Hendrycks et al. (2021) to measure efficacy of a system under a required coverage level that is **similar to typical human's**."

> "We micro average these scores over documents and then macro average over labels. This is to avoid the label imbalance to cancel out with micro averaging and **the results to appear too optimistic**."

| Model | Evidence mAP | Evidence P@R80 | NLI Acc. | NLI F1 (C) | NLI F1 (E) |
|---|---|---|---|---|---|
| Majority vote | — | — | .674 | .083 | .428 |
| Doc TF-IDF+SVM | — | — | .733 | .197 | .641 |
| Random | .024 | .000 | — | — | — |
| Span TF-IDF+Cosine | .381 | .057 | — | — | — |
| Span TF-IDF+SVM | .836 | .322 | — | — | — |
| SQuAD (BERTbase) | .825 | .004 | .574 | .004 | — |
| SQuAD (BERTlarge) | .869 | .005 | .661 | .043 | — |
| **Ours: Span NLI BERT (BERTbase)** | **.885** ± .025 | **.663** ± .093 | **.838** ± .020 | **.287** ± .022 | **.765** ± .035 |
| **Ours: Span NLI BERT (BERTlarge)** | **.922** ± .006 | **.793** ± .018 | **.875** ± .006 | **.357** ± .039 | **.834** ± .002 |

*Provenance note: the SQuAD baseline rows carry fewer reported values than the "Ours" rows in the source table; the F1(C) figures shown for them (.004 / .043) are the last populated cells in those rows. Treat the SQuAD F1(C) values as low-confidence and re-check against the PDF before quoting. Every "Ours" and Table 3 value below is unambiguous.*

## Backbone comparison (Table 3, verbatim) — the best numbers in the paper

| Backbone | Fine-tuning Method | Evidence mAP | Evidence P@R80 | NLI Acc. | NLI F1 (C) | NLI F1 (E) |
|---|---|---|---|---|---|---|
| BERTbase | None | .885 ± .025 | .663 ± .093 | .838 ± .020 | .287 ± .022 | .765 ± .035 |
| BERTlarge | None | .922 ± .006 | .793 ± .018 | .875 ± .006 | .357 ± .039 | .834 ± .002 |
| DeBERTa v2xlarge | None | .933 ± .002 | .859 ± .008 | .885 ± .001 | .360 ± .027 | .855 ± .002 |
| BERTbase | Pretrained from scratch on case law (Zheng et al. 2021) | .870 ± .015 | .578 ± .052 | .831 ± .032 | .289 ± .026 | .783 ± .040 |
| BERTbase | Fine-tuned on case law + contract corpora (Chalkidis et al. 2020) | .925 ± .004 | .811 ± .002 | .794 ± .008 | .272 ± .008 | .746 ± .018 |
| **DeBERTa v2xlarge** | **Fine-tuned on span identification (Hendrycks et al. 2021)** | **.936** ± .002 | **.860** ± .003 | **.892** ± .001 | **.405** ± .016 | **.859** ± .005 |
| BERTbase | Fine-tuned on NDAs | .892 ± .002 | .690 ± .014 | .864 ± .004 | .326 ± .014 | .820 ± .010 |
| BERTlarge | Fine-tuned on NDAs | .922 ± .003 | .837 ± .008 | .875 ± .000 | .389 ± .009 | .839 ± .003 |

**⭐⭐ THE HEADLINE FAILURE: contradiction F1 tops out at 0.405.**

| | Best F1 (E) | Best F1 (C) | Ratio |
|---|---|---|---|
| Best model (DeBERTa v2xlarge + span-ID pretraining) | **.859** | **.405** | **2.1×** |
| Span NLI BERT (BERTlarge) | .834 | .357 | 2.3× |

> "**Nevertheless, the performance for contradiction labels is much worse than that of entailment labels, due to the imbalanced label distribution.**"

**The class we actually care about — contradiction — is the class every model is worst at, by a factor of ~2.** Accuracy of .875–.892 looks strong and is *almost entirely carried by Entailment and NotMentioned*. **Never quote ContractNLI accuracy without F1(C) next to it.** Note also that legal-domain pretraining (Chalkidis) *hurts* NLI accuracy (.794 vs .875 for plain BERTlarge) — in-domain pretraining is not a free win.

## ⭐⭐ Length/locality degradation: negation by exception (Table 7, verbatim)

The killer analysis. Contracts "state a general condition and subsequently add exceptions." Example, verbatim: *"Recipient shall not disclose Confidential Information to any person or entity, except its employees or partners…"* — "the first half clearly forbids sharing… but the latter part flips this decision."

Evaluated on the best Span NLI BERT (BERTlarge). "Majority"/"Minority" = accuracy on majority/minority ground-truth NLI labels, split "to rule out the effect of the label distribution." NotMentioned pairs excluded.

| Condition | NLI Acc. Majority | NLI Acc. Minority | Weighted | % minority label |
|---|---|---|---|---|
| w/o (local) | .91 | .77 | **.84** | 21 |
| **w/ (local)** | .92 | **.40** | **.66** | 7 |
| w/o (non-local) | .98 | .72 | **.85** | 19 |
| **w/ (non-local)** | .90 | **.00** | **.45** | 6 |

**⭐ When the exception is NON-LOCAL — the qualifier lives far away in the document — minority-label accuracy is 0.00. Zero. The model gets literally none of them right.** Weighted accuracy falls .85 → .45, i.e. **below the .674 majority-vote baseline.**

Local exceptions: minority accuracy .77 → **.40** (-37 points). Non-local: .72 → **.00** (-72 points).

**This is the single most important number in this file.** It is a direct, quantified demonstration that **a fact stated early and qualified later is invisible to the model** — and the further away the qualifier, the worse, all the way to total failure. The paper's own conclusion:

> "Span NLI BERT still has poor performance on rare labels, as well as being **easily impacted by negations by exceptions**."

Prevalence (dev set annotation): local negation-by-exception affects **12% of pairs / 59% of documents**; non-local affects **7% of pairs / 44% of documents**. So this failure mode is triggered in **roughly half of all documents.**

## Oracle evidence (Table 6, verbatim)

Document-level binary classification over Entailment/Contradiction **using oracle evidence spans**:

| Model | Accuracy | F1 (C) | F1 (E) |
|---|---|---|---|
| Majority vote | .814 | .239 | .645 |
| Span NLI (BERTbase) | .883 ± .006 | .490 ± .007 | .795 ± .005 |
| Span NLI (BERTlarge) | .899 ± .004 | .492 ± .065 | .820 ± .012 |
| **Oracle NLI (BERTbase)** | **.918** ± .005 | **.657** ± .062 | .816 ± .006 |
| Oracle NLI (BERTlarge) | .908 ± .011 | .620 ± .082 | .806 ± .015 |

**Handing the model the right spans lifts F1(C) from .490 → .657 (+.167) — evidence identification is a major bottleneck.** But note the ceiling: **even with perfect evidence handed to it, contradiction F1 is only .657.** Retrieval is not the whole problem; the inference itself is hard. (Also note BERT**large** is *worse* than BERT**base** under oracle conditions — .620 vs .657 — with a huge ±.082 std. Small test set, noisy results.)

## Span continuity (Table 8, verbatim)

`n` = minimum number of surrounding tokens (context window size).

| | n | # spans | # spans read before finding: one span | all spans | mAP |
|---|---|---|---|---|---|
| Continuous | 128 | 2.64 | 1.09 | 3.82 | 0.91 |
| Discontinuous | 128 | 2.34 | 1.04 | 3.84 | 0.94 |
| Continuous | 64 | 2.64 | 1.16 | 4.33 | 0.89 |
| Discontinuous | 64 | 2.34 | 1.01 | 4.85 | 0.94 |

Shrinking the context window 128 → 64 degrades "spans read before finding **all** spans" from 3.84 → **4.85** for discontinuous spans (vs 3.82 → 4.33 continuous) — **finding *all* the evidence degrades with less context, even though mAP doesn't move.** mAP hides it; the metric that matters (did you find everything?) shows it. Discontinuous spans occur in **28% of pairs / 81% of documents**.

## Human performance: NOT REPORTED

**No human ceiling, no expert baseline, no annotator-vs-model comparison.** The only human-adjacent calibration is that P@R80's 0.8 recall threshold is "similar to typical human's" coverage — an assertion, not a measurement. **The human-model gap for ContractNLI does not exist in the paper.**

---

# PART B — DocNLI (Yin, Radev & Xiong, Findings of ACL-IJCNLP 2021)

## What it is

Large-scale document-level NLI, **binary** (`entail` / `not_entail`), built by reformatting five existing datasets. Premises are documents; **hypotheses are also long** — "the first dataset that uses hypotheses longer than single sentences."

## Source datasets (Table 1, verbatim)

| | original task | domain | premise length | hypothesis length |
|---|---|---|---|---|
| ANLI | NLI | various (wiki, news, etc.) | multi-sentence (20~94 words) | single sentence (4~18 words) |
| SQuAD | QA | wiki | paragraph (27~237 words) | single sentence (6~22 words) |
| DUC (2001) | summarization | news | doc. (124~879 words) | multi-sent (80~100 words) |
| CNN/Daily Mail | summarization | news | doc. (247~652 words) | 3~4 sent. (40~50 words) |
| Curation | summarization | news | doc. (229~842 words) | multi-sent (64~279 words) |

Per-source splits: CNN/DailyMail 286,817/13,368/11,487; Curation 20K/7K/13K; DUC2001 400/50/150.

## Dataset size (Table 4, verbatim)

| | train | dev | test |
|---|---|---|---|
| entail. | 466,653 | 28,890 | 33,128 |
| not_entail | 475,661 | 205,368 | 233,958 |
| **sum** | **942,314** | **234,258** | **267,086** |

> "The training set is roughly balanced, while **approximately 12% examples in dev and test belong to 'entail'. F1 is the evaluation metric.**"

**⚠️ Train is balanced (49.5% entail) but dev/test are 12.4% entail.** A deliberate train/test prior shift, which is part of why F1 is so low — and why **F1, not accuracy, is the only honest metric here.** A trivial all-`not_entail` classifier scores 87.6% accuracy and 0 F1.

## ⚠️ How "not_entail" is manufactured

Same structural problem as DialogueNLI. Non-entailment pairs are generated from real summaries by:
- **Word replacement** — "We mask eight words whose part-of-speech tags are among {VERB, NOUN, PROPN, NUM…}"
- **Entity replacement**
- **Sentence replacement**

**The negative class is string substitution, not naturally occurring contradiction.**

## Human verification (§3.3, verbatim)

> "**The authors of this work** manually checked **200 random 'fake' examples**, among which **none is true** given the same document as the 'real' summary. This is mainly because we replaced relatively a lot from the original real summaries. **However, some minor grammar issues inevitably exist.**"

**⚠️ Three problems in one paragraph:**
1. **n=200**, out of 942K training examples — and only from the summarization subset.
2. **Verified by the authors themselves**, not independent annotators. **No agreement statistic is possible or reported.**
3. The paper's own worked example shows a generated "fake" that is **grammatically broken** — dates swapped to produce *"…on 2025…"* where "26 August" belonged. The paper admits: *"which makes the new text '[…] on 2025 […]' grammatically incorrect."*

**A model can learn to detect "this text is subtly broken" rather than "this text contradicts the document."** The paper's artifact claim rests on the hypothesis-only baseline (below), which is genuinely reassuring — but it does not rule out *premise-independent fluency artifacts*, only *label-indicative hypothesis features*.

## ⭐ Main results (Table 5, verbatim) — F1 scores on DocNLI

| | dev | test |
|---|---|---|
| Random | 19.75 | 19.91 |
| Hypothesis-only | 21.89 | 22.02 |
| **Longformer-base** | **46.18** | **44.42** |
| **RoBERTa-large** | **63.05** | **61.20** |

**⭐⭐ THE HEADLINE FAILURE: the best model on a 942K-example training set reaches F1 61.20.**

> "Overall, **DocNLI is a very challenging task** that seeks solutions equipped with a stronger capability of representation learning."

**⚠️ Internal inconsistency in the paper:** the prose states *"22.02 vs. **61.52** on test"* while **Table 5 says 61.20**. The two disagree by 0.32. Cite **61.20** (the table) and be aware a reader may find 61.52 in the text.

**⭐⭐ The most damning result: Longformer LOSES to RoBERTa despite 2.5× the context.**

| Model | Max tokens | Test F1 |
|---|---|---|
| RoBERTa-large | **512** | **61.20** |
| Longformer-base | **1,300** (library supports 4,096) | **44.42** |

> "**Surprisingly, 'Longformer''s performance is clearly below that of the RoBERTa, even if it covers more tokens**, possibly because we do not have enough computing resources to fully explore the better settings of Longformer."

**The long-context model, on the long-context task, is 16.8 F1 points WORSE than the model that truncates at 512 tokens.** The authors' explanation is a compute disclaimer, not a result — and it is confounded: **Longformer-base vs RoBERTa-large is also a size mismatch.** They say so themselves: "We currently only report 'Longformer-base' due to memory constraints." **This comparison is uncontrolled and cannot support either conclusion** — it does not show long-context architectures fail, and the paper cannot claim they work. It's a hole in the literature, not evidence.

**Artifacts are genuinely low, though — the one clean positive:**
> "we notice that 'hypothesis-only' is just slightly higher than random guess"

Hypothesis-only **22.02** vs random **19.91** = **+2.11 F1**. Contrast DialogueNLI's hypothesis-only at **+22.65 points over majority** (see `game-dialogue-nli.md`). **DocNLI is dramatically cleaner than DNLI on artifacts.** This is the one dimension where DocNLI is the better-built dataset, and it comes precisely *from* the synthetic generation the section above criticises. Trade-off, not a free lunch.

## ⭐ Length degradation (Figures 3 & 4)

Verbatim:

> "Figure 3 illustrates the impact of taking different numbers of tokens in Longformer, evaluated on dev set. **In general, the more tokens the better performance.**"

> "Figure 4(a) shows that the system performance for **pairs of lengths > 450 does not change clearly. This is probably due to those models' truncation** when the (premise, hypothesis) pairs are overlong (note that one word may be split into multiple tokens by the WordPiece tokenizer)."

> "**Figure 4(b) demonstrates that the task gets increasingly challenging when the hypotheses become longer**, which matches our intuition."

**⚠️ Critical caveat on the length analysis — the flat line is an artifact of truncation.** Beyond ~450 words F1 "does not change clearly" **because the model never sees the extra text**. This is *not* evidence that long documents are fine; it's evidence that the measurement stops being informative exactly where our use case starts. **DocNLI cannot answer "how does performance degrade with document length" past 450 words**, and the paper is honest that it can't.

The real degradation signal is **Figure 4(b): F1 falls as hypotheses get longer.** Both curves are **plots only — no numeric table** — so exact per-bucket F1 values are not recoverable from the text. If we need them, we must digitize the figure or contact the authors.

Length distribution: "the majority of premises stay within the length limit of 150 words… Still, there are a large amount of premises whose lengths are within the range of [150, 900] words."

**⚠️ So DocNLI is not really a long-document dataset.** The *majority* of premises are **under 150 words**. "Document-level" here means multi-sentence, not book-length. Our 100-turn transcripts are far outside DocNLI's actual mass.

## Transfer results (Tables 6 & 7, verbatim)

**Table 6 — Train on DocNLI, test on out-of-domain tasks needing document-level NLI:**

| pretrain | FEVER binary | MCTest v160 | MCTest v500 |
|---|---|---|---|
| random | 50.00 | 25.00 | 25.00 |
| MNLI | 86.64 | 75.41 | 70.66 |
| ANLI | 87.51 | 82.50 | 78.66 |
| **DocNLI** | **88.84** | **90.00** | **85.83** |
| DocNLI +finetune | **89.44** | **90.83** | **90.66** |
| Prior state-of-the-art | – | 80.00 | 75.50 |

**Table 7 — Train on DocNLI, test on sentence-level NLI:**

| Model | SciTail | b-MNLI |
|---|---|---|
| majority | 60.33 | 66.66 |
| ESIM (Chen et al. 2017) | 70.60 | – |
| De-Att (Parikh et al. 2016) | 72.30 | – |
| DGEM (Khot et al. 2018) | 77.30 | – |
| BERT-large | 89.71 | 90.55 |
| Longformer-base | 92.23 | 92.03 |
| RoBERTa-large | 95.13 | 93.95 |
| **DocNLI (pretrain)** | **78.17** | **91.13** |
| DocNLI +finetune | **96.04** | **94.07** |
| Prior state-of-the-art | 97.70 | – |

**⚠️ The zero-shot transfer story is weaker than the abstract implies.** DocNLI-pretrained zero-shot on SciTail scores **78.17 — worse than plain RoBERTa-large (95.13) and worse than BERT-large (89.71)**, and barely above 2018-era DGEM (77.30). It only wins **after task-specific fine-tuning** (96.04), at which point it's unclear how much credit belongs to DocNLI vs to RoBERTa. The genuine win is **MCTest** (90.00 / 85.83 zero-shot vs prior SOTA 80.00 / 75.50).

## Human performance: NOT REPORTED

**No human ceiling on DocNLI.** The only human involvement is the 200-example author-conducted sanity check on fake summaries (§3.3), which verifies *label correctness*, not *human task performance*. **There is no human-model gap number for DocNLI.**

---

# Cross-cutting summary

| Question the consumer asked | Answer |
|---|---|
| Best DocNLI F1 | **61.20** (RoBERTa-large, test) |
| Best ContractNLI NLI accuracy | **.892** (DeBERTa v2xlarge + span-ID pretraining) |
| **Best ContractNLI contradiction F1** | **.405** — the number that matters |
| **Human performance / human-model gap** | **⭐ NEITHER PAPER REPORTS A HUMAN CEILING. The gap does not exist in the literature.** |
| **Inter-annotator agreement** | **⭐ NEITHER PAPER REPORTS ANY κ/α.** ContractNLI's single-adjudicator design makes it impossible; DocNLI's authors verified their own data (n=200). |
| Degradation with document length | ContractNLI: **non-local negation → .00 minority accuracy**, weighted .85→.45. DocNLI: flat past 450 words **because of truncation** (uninformative); F1 falls as hypotheses lengthen (plot only, no numbers). |
| Long-context architectures | **Longformer (1.3K tokens) loses to RoBERTa (512 tokens) by 16.8 F1** — but the comparison is confounded by base-vs-large. Uncontrolled. |

## Provenance note (why these numbers are trustworthy)

**WebFetch's summarizer materially corrupted both papers' tables.** ContractNLI's Table 3/4 report each metric as an adjacent `value ± std` pair; the summarizer read the std column as the next metric, producing "P@R80 = .006" alongside "mAP = .922", and returned **contradictory values across two fetches of the same URL** (accuracy .875 vs .793; F1(C) .357 vs .018). A separate web-search snippet attributed **DocNLI F1s of 48.96/45.96 to the wrong paper entirely** (they come from "The NLP Task Effectiveness of Long-Range Transformers," arXiv 2202.07856 — not DocNLI). All tables above were re-extracted from the raw ar5iv HTML by parsing `<tr>`/`<td>` structure directly. **Do not re-derive these from a summarizer.**

## Relevance to companion-eval-platform

1. **⭐⭐ The non-local negation result (.00 minority accuracy) is the most transferable finding in this file — cite it as our core risk.** ContractNLI proves that when a claim is stated in one place and qualified far away, a strong model gets **zero of the minority cases right**, dragging weighted accuracy (.45) *below the majority baseline* (.674). **That is structurally identical to our problem**: a character establishes a fact at turn 5, qualifies or violates it at turn 80. This failure fires in ~44% of ContractNLI documents on a **2,254-token** average — our transcripts are longer. **We should expect worse.** This is the strongest external evidence that naive long-context NLI will not work for us.

2. **⭐⭐ Contradiction is the hardest class everywhere, and it is the only class we care about.** ContractNLI: F1(C) **.405** vs F1(E) **.859** at best. DocNLI: **61.20** overall F1. Every headline accuracy in this literature (.875, .892) is carried by Entailment/NotMentioned. **When we set an internal target for contradiction detection, .405 is the honest prior art — not .89.** Anyone quoting "ContractNLI hits 89% accuracy" as a reason to expect a working detector is misreading the paper.

3. **⭐⭐ The missing human ceiling is a real, claimable gap — and a warning.** Neither paper reports human performance or inter-annotator agreement. **We cannot cite a human-model gap for long-document NLI because nobody has measured one.** Two consequences: (a) if we measure a human ceiling and a chance-corrected α on contradiction detection over long transcripts, that is a genuine contribution — combined with DialogueNLI's identical omission (see `game-dialogue-nli.md` §5), **the entire consistency-NLI literature has never published an agreement statistic**; (b) we cannot claim "models are X points below humans" for our task — **there is no X.** Feed both to note 10 (noise floor).

4. **⚠️ ContractNLI's gold standard is single-annotator on much of dev/test.** Redundant MTurk annotation was collapsed by one adjudicator "with a priority on coverage," and dev + part of test are one-person work. On a task whose own authors call the linguistics hard, **the .405 F1(C) may be measured against a noisy ceiling** — the true difficulty could be higher *or* the metric unreliable. Do not treat ContractNLI numbers as a precise benchmark; treat them as an order of magnitude.

5. **⚠️ Do NOT cite "Longformer < RoBERTa" as evidence that long-context models fail.** It is confounded (base vs large) and the authors blame compute. **The controlled experiment does not exist in this literature.** If we need to know whether a long-context architecture helps contradiction detection, **we have to run it ourselves** — this is a cheap, genuinely open question, and the honest framing for a roadmap item.

6. **⭐ Oracle evidence lifts F1(C) .490 → .657 — retrieval matters, but is not sufficient.** Consistent with DialogueNLI's oracle-triples result (99.69%): **retrieval/extraction is a large share of the difficulty.** This argues for our retrieve-then-verify design over end-to-end long-context classification. **But note the ceiling: even with perfect evidence, contradiction F1 is .657.** A perfect retriever does not give us a working detector. Feed to note 09 (offline probes).

7. **⚠️ Neither dataset contains our phenomenon; both manufacture negatives by substitution.** DocNLI: word/entity/sentence replacement, with the authors conceding the output has grammar errors. ContractNLI: real, but NDAs with 17 fixed hypotheses. **Neither has naturally occurring narrative self-contradiction, and neither has dialogue.** ContractNLI is the better *analogue* (real documents, real long-range structure, real negation-by-exception); DocNLI is the better *artifact-control* (hypothesis-only only +2.11 over random, vs DNLI's +22.65 over majority). **Use ContractNLI's §5.2 analysis as our threat model; do not train on either.**

8. **DocNLI is not actually long.** Majority of premises **under 150 words**; the length curve goes flat past 450 words *only because of truncation*. **DocNLI cannot tell us anything about 100-turn transcripts** and should not be cited as evidence about long context. Cite it for the **61.20 F1 difficulty result** and the **clean artifact control** — nothing else.
