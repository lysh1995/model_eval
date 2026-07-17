---
title: "I like fish, especially dolphins: Addressing Contradictions in Dialogue Modeling (DECODE)"
url: https://aclanthology.org/2021.acl-long.134/
authors: Yixin Nie, Mary Williamson, Mohit Bansal, Douwe Kiela, Jason Weston
year: 2021
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# DECODE — DialoguE COntradiction DEtection (ACL 2021, pp. 1699–1713)

**Status: THE decisive source for "is automated contradiction auditing viable?" The answer is a hard, quantified *yes and no*, and the split is exactly along the line our platform already draws between per-instance verdicts and cell-level aggregates.**

arXiv: https://arxiv.org/abs/2012.13391 · Project: https://parl.ai/projects/contradiction/

> **Verification note.** Every number below was extracted from the **primary PDF via pypdf** and cross-checked by arithmetic (see the two corrections). An earlier WebFetch summarizer paraphrased this paper with plausible-but-wrong framing ("unanimous agreement from three verifiers", "Table 4" for the main results, "6,314 verified contradictions"). **A sibling agent in this same batch caught WebFetch fabricating an entire results section for another paper (Skill Check: invented Fleiss' κ=0.73, invented baselines, invented 1–5 rubrics — none exist).** Treat any PDF-derived number in this source set as unverified unless it says otherwise.

## Task

> determine "whether the last utterance contradicts any previously conversed information"

and identify the **supporting evidence** utterances from the dialogue history. Two-way classification (contradiction / non-contradiction) **plus** evidence retrieval — the "Strict" metric requires both to be right.

⭐ **The supporting-evidence requirement is the design we should copy.** A flag that cites the specific earlier utterance it conflicts with is adjudicable; a bare "contradiction: yes" is not. It also makes the strict metric ~13 points harder (93.19 → 80.86), which tells you how much of naive contradiction "detection" is right-for-the-wrong-reason.

## Dataset (Table 1, verbatim)

| Split | Count | Label |
|---|---|---|
| Main (Train) | 27,184 | balanced |
| Main (Dev) | 4,026 | balanced |
| Main (Test) | 4,216 | balanced |
| Human-Bot (Test) | 764 | balanced |
| A2T (Test) | 2,079 | contradiction |
| RCT (Test) | 2,011 | non-contradiction |

Contradictions are **human-written on purpose**: annotators write one or two utterances such that the last contradicts something earlier. Train split holds unverified examples; **dev/test only contain verified examples**. A2T and RCT are auxiliary "checklist" transformations of test contradictions with known flipped/preserved labels.

## ⭐ Human agreement on contradiction labels (Table 4)

Each written contradiction went to **3 verifiers**:

| # of Verifiers Agreed | Count | Ratio |
|---|---|---|
| 0 | 484 | 7.67% |
| 1 | 497 | 7.87% |
| 2 | 1,211 | 19.18% |
| 3 | **4,122** (see correction) | 65.28% |
| **Total** | **6,314** | 100.00% |

> ⚠️ **Correction — apparent typo in the published paper.** The PDF's count column prints **6,214** for the "3 verifiers" row. That is arithmetically impossible: 6,214/6,314 = 98.4%, not 65.28%. The four ratios sum to exactly 100.00%, and 484/6,314 = 7.67%, 497/6,314 = 7.87%, 1,211/6,314 = 19.18% all match at N=6,314 — which forces the "3" row to be **4,122** (4,122/6,314 = 65.28% ✓). **The ratio column is self-consistent; the count column has a typo.** Use 4,122.

**What this number means, and it is the one to quote:**

- Only **65.28%** of *deliberately authored* contradictions were confirmed by all 3 verifiers.
- **15.54%** (0 or 1 verifier) were essentially rejected — a human wrote a contradiction on purpose and two-thirds of verifiers couldn't see it.
- **~35% of intentional contradictions do not command unanimous human assent.**

⇒ **Contradiction is more objective than aesthetics, but it is NOT a hard oracle.** This is the single most important calibration for note 13. The construct is real and far more stable than "quality" (α=0.25–0.34), yet it still has a ~65–85% human ceiling depending on how you count. Anyone promising a contradiction auditor that is "objective, therefore ~100%" has not read this table.

*(Note: this is agreement on curated, deliberate contradictions. Naturally occurring, subtle, in-fiction contradictions will be worse, not better.)*

## Main results (Table 2) — the balanced-set view

| Approach / Training Data | MT | MT (Strict) | HB | SE F1 |
|---|---|---|---|---|
| **Unstructured** — All | **97.46** | – | 77.09 | – |
| Unstructured — All − DNLI | 97.44 | – | 73.17 | – |
| Unstructured — All − ANLI-R3 | 98.04 | – | 73.56 | – |
| Unstructured — All − DECODE | 84.42 | – | 61.91 | – |
| Unstructured — DNLI | 57.19 | – | 60.34 | – |
| Unstructured — ANLI-R3 | 82.21 | – | 59.69 | – |
| Unstructured — DECODE | 96.85 | – | 70.03 | – |
| **Utterance-based** — SNLI+MNLI | 77.40 | 47.70 | 73.17 | 72.4 |
| Utterance-based — All | 94.19 | 80.08 | **83.64** | 88.5 |
| Utterance-based — All − DECODE | 86.67 | 66.95 | 77.36 | 80.6 |
| Utterance-based — DNLI | 76.54 | 63.09 | 75.26 | 71.2 |
| Utterance-based — ANLI-R3 | 81.59 | 69.11 | 70.52 | 74.3 |
| **Utterance-based — DECODE (best)** | **93.19** | **80.86** | **84.69** | **87.5** |
| BERT — DECODE | 88.88 | 74.14 | 75.52 | 84.3 |
| Electra — DECODE | 93.17 | 81.19 | 80.76 | 87.5 |
| BART — DECODE | 94.47 | 80.10 | 79.19 | 88.2 |
| **Majority** | 50.00 | 50.00 | 50.00 | 48.7 |

MT = Main Human-Human Test; HB = Human-Bot; SE F1 = supporting-evidence F1.

**The structure lesson:** unstructured wins in-domain (97.46 vs 94.19) and **loses badly out-of-domain** (77.09 vs 83.64). The utterance-based (structured) model generalizes better to bot dialogue *because of the architecture*, not the data — the authors ablate this explicitly. **Generalization to the distribution you actually care about is anti-correlated with in-domain score.** Note 08's covariate-shift theme, again.

**Transfer from generic NLI is poor:** DNLI alone → 76.54 MT; SNLI+MNLI → 77.40. Off-the-shelf NLI is not a contradiction detector for dialogue. **Do not expect to bolt an NLI model on and be done.**

## ⭐⭐ The result that decides our design (Table 7) — natural, unbalanced setting

The balanced sets above are an NLU convenience. The authors then run the detector on **raw interactive human-bot dialogue**: **764 dialogues, 8,933 utterances.**

**Prevalence: only 381 contradicting utterances = 4.27%.** Majority baseline accuracy = **95.73%** (the paper's footnote 7).

> ⚠️ **Extraction artifact corrected:** the PDF text reads "only 3817" — this is **"381" followed by footnote marker "7"**. Confirmed by arithmetic: 381/8,933 = 4.27% → majority baseline 95.73%, matching footnote 7 exactly. (3,817/8,933 = 42.7% would imply a 57.27% baseline, contradicting the paper.) **The real prevalence is 4.27%.**

**Table 7 — RoBERTa on all bot-generated utterances, threshold τ = 0.5:**

| Approach / Training Data | Precision | Recall | F1 | AUC |
|---|---|---|---|---|
| Unstructured — All | 15.89 | 60.11 | 25.14 | 80.47 |
| Unstructured — All − DECODE | 15.63 | 57.74 | 24.60 | 71.82 |
| Unstructured — DECODE | 17.05 | 50.13 | 25.45 | 73.40 |
| Utterance-based — All | 23.35 | 71.65 | 35.23 | 84.96 |
| Utterance-based — All − DECODE | 17.17 | 68.50 | 27.46 | 80.09 |
| Utterance-based — DNLI | 16.32 | 65.09 | 26.09 | 79.29 |
| Utterance-based — ANLI-R3 | 22.52 | 41.73 | 29.26 | 76.36 |
| **Utterance-based — DECODE (best)** | **23.94** | **74.28** | **36.21** | **87.16** |

The authors' own verdict, verbatim:

> "model precision on the task is **not satisfactory (23.94 at best)**. However, the best model achieves acceptable scores on both Recall and AUC. This indicates its potential usage for **strict blocking of inconsistent utterances**"

**Unpack 23.94% precision at 4.27% prevalence: 76.06% of flags are false. ~3.2 false alarms per true catch.** Recall is decent (74.28) and ranking is good (AUC 87.16), but the per-instance verdict is mostly wrong.

**This is the entire viability answer, and it splits cleanly:**

| Use | Verdict | Evidence |
|---|---|---|
| **Per-instance flag** shown to a user/engineer ("turn 43 contradicts turn 12") | ❌ **No** | 24% precision — 3 of 4 flags wrong |
| **Aggregate rate** compared across models/cells | ✅ **Yes** | AUC 87.16; r=0.81 vs human rate (but see below) |
| **Recall-oriented triage** — a filter feeding human review | ✅ **Yes** | 74.28% recall; that's what "strict blocking" means |

⇒ **Exactly the shape of note 10's conclusion, reached from a different direction: the unit of evaluation is never the single instance.** A contradiction auditor is a *cell-mean instrument*, not a *transcript-annotation instrument*. If the UI shows a flag on a turn, it is showing a coin flip weighted 3:1 *against* it.

## Correlation with human judgment (Figure 4)

> "the scores are positively correlated with human judgments, with a **Pearson correlation coefficient of 0.81**"

⚠️ **This r=0.81 is an ECOLOGICAL correlation and must not be read as per-utterance accuracy.** From the caption: the comparison is "averaged **by type of bot**," and "Each point in the plot is **a bot** which has conversed with humans and produced at least **180 utterances**." So r=0.81 is computed over a handful of *bot-level aggregate points*, not over utterances. Aggregation to bot level averages away exactly the per-instance noise that makes precision 24%.

**Both facts are true at once and they are not in tension:** per-utterance precision 23.94%, bot-level correlation with humans 0.81. **That is the strongest available evidence for the "aggregate, don't annotate" design** — and it is a textbook instance of note 08 §1.2's warning about treating aggregated points as if they licensed per-turn claims. *Cite r=0.81 for model ranking; never for a flag.*

## ⭐ Table 3 — Goodhart's law, demonstrated

Re-ranking generation with the DECODE detector, on Blenderbot BST 2.7B logs:

| Decoding Strategy | DECODE Contradict% (automatic) | Human Contradict% |
|---|---|---|
| **Standard generation** | | |
| Beam Search | 69.7% | 84.2% |
| Top-k (k=40) | 42.1% | 69.7% |
| Sample-and-Rank | 39.5% | 55.3% |
| **DECODE Re-ranking** | | |
| Beam Search | 46.1% | 55.3% |
| Top-k (k=40) | **2.6%** | **39.5%** |

**Read the last row.** After re-ranking against the detector, the *detector* says 2.6% contradiction; *humans* say 39.5%. **A 15× discrepancy — and it is smallest before optimization (69.7 vs 84.2, a 1.2× gap) and largest after (2.6 vs 39.5).**

⇒ **The moment you optimize against the contradiction metric, it stops measuring contradiction.** Re-ranking does reduce real contradictions (84.2% → 55.3% on beam; 69.7% → 39.5% on top-k — genuine wins), but the automatic number overstates the win by an order of magnitude.

**Direct consequence for the platform:** if we ship a world-state consistency score and customers tune against it, our metric decays *specifically for the models that optimized on it* — i.e. it breaks exactly when it matters, and it breaks silently, in the flattering direction. **Any contradiction metric we ship needs a periodic human-calibration re-baseline, and we must never let it become a training target we also evaluate on.** Note the detector also *systematically under-reports* vs humans in every single row — the bias has a known sign.

## Relevance to companion-eval-platform

1. **⭐ Human ceiling ≈ 65% unanimous / ~85% majority on deliberate contradictions.** Far above α=0.25–0.34, far below an oracle. **This is the honest error budget for note 13** and the number that should govern our claims.
2. **⭐ 23.94% precision at 4.27% prevalence is the headline risk.** Our world-state auditor's precision will be *worse* than DECODE's: roleplay contradictions are subtler, the history is longer (100 turns vs a few), fiction licenses apparent contradictions (dreams, lies, unreliable narration, retcons the user *wanted*), and DECODE's detector was trained in-domain on 27k examples while ours would be prompted. **Assume ~10–25% precision for a naive auditor and design so that precision doesn't have to be high.**
3. **⭐ Rare events break intuitions.** 4.27% prevalence means a 95.73% majority baseline. **Never report contradiction *accuracy*** — report precision/recall/AUC at a stated threshold, and report prevalence. An "our auditor is 95% accurate" claim is achievable by predicting "no contradiction" always. This is note 10's noise-floor gate applied to a rare-event metric.
4. **⭐ Copy the supporting-evidence requirement.** Force the auditor to cite the turn it conflicts with. Adjudicable, and the Strict metric (−13pp) shows how much it tightens the screw.
5. **Use the structured/utterance-based framing**, not a flat NLI over concatenated history — it's the architecture, not the data, that generalizes out-of-domain (77.09 → 83.64).
6. **Don't expect off-the-shelf NLI to work** (DNLI alone: 76.54 MT, 16.32 precision).
7. **Goodhart is measured, not hypothetical** (Table 3). Re-baseline against humans on a schedule; never let the auditor become a customer's optimization target and our evaluation instrument simultaneously.
8. **The tuning knob is τ.** Precision 23.94 is at τ=0.5. Raising τ trades recall for precision — for a *flagging* product we'd run high-τ (few, high-confidence flags); for a *rate* product we'd keep τ=0.5 and report the aggregate. **The threshold is a product decision, and the paper hands us the AUC (87.16) that says the ranking underneath is sound enough to pick a point on.**
