---
title: "Dungeons and Dragons as a Dialog Challenge for Artificial Intelligence"
url: https://aclanthology.org/2022.emnlp-main.637/
authors: Chris Callison-Burch, Gaurav Singh Tomar, Lara J. Martin, Daphne Ippolito, Suma Bailis, David Reitter
year: 2022
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# D&D as a Dialog Challenge for AI (EMNLP 2022, pp. 9379–9393)

**arXiv:** 2210.07109

Frames D&D as a dialogue-system challenge with two tasks: generate the next conversational turn, and predict game state from dialogue history. **This is the paper that DOES report inter-rater agreement** (unlike FIREBALL, which supersedes it on data quality).

## 1. Dataset statistics (Table 1, verbatim — Play-By-Post Corpus)

| Metric | Value |
|---|---|
| Number of campaigns | 896 |
| Average players per campaign | 8 |
| Average turns per campaign | 910 |
| Average words per campaign | 64,941 |
| **Total turns** | **815,106** |
| **Total words** | **58,187,526** |
| Average dice rolls per campaign | 594 |
| **Total dice rolls** | **532,270** |

Scraped from play-by-post D&D forums. **Important caveat:** game state here is **heuristically annotated**, not gold — this is exactly the limitation FIREBALL was built to fix. Appendix C estimates the accuracy of the predicted/heuristic state (e.g. "In combat?" classifier: Accuracy 0.91).

## 2. Task definitions

**Next Utterance Prediction.** Predict the next turn conditioned on dialogue history, optionally conditioned on control features (character class, in-character status, combat state). The model can respond as a particular character **or as the Dungeon Master**.

**Game State Tracking (GST).** "We have kept the state definition similar to task-oriented dialogue state tracking (DST). In DST, the dialogue state is a collection of slot-value pairs. In our case, each slot is a state [variable]" — with the wrinkle that "slot values do not need to appear as a word in the [dialogue]". Model `LLM-DND-GST` takes all previous dialog turns + their state variables + current turn text, outputs current-turn state variables.

## 3. Automatic evaluation (Table 3) — perplexity & token accuracy

| Model | Perplexity | Token Accuracy |
|---|---|---|
| LLM-Dialog | 2.65 | 44.61 |
| LLM-DND | 2.50 | 46.92 |
| LLM-DND-PREV-CTRL | 2.51 | 46.84 |
| LLM-DND-CURR-CTRL | **2.34** | **49.67** |
| LLM-DND-ALL-CTRL | 2.37 | 49.02 |

## 4. Game State Tracking accuracy (Table 7) — **OBJECTIVE / SLOT-LEVEL**

| State variable | Majority baseline | LLM-DND-GST |
|---|---|---|
| All | .73 | .82 |
| Combat | **.89** | .82 |
| Character Class | .58 | .76 |
| Character Name | .58 | .78 |
| Character Race | .75 | .79 |
| Character Pronouns | .58 | **.89** |
| Character Actions | .80 | .85 |

**JOINT ACCURACY: 58%.**

Verbatim conclusion: "The average accuracy of the dialogue state tracker is better than the majority class baseline, but likely falls short of being useful when it comes to joint accuracy. The joint accuracy for LLM-DND-GST is 58%. This suggests that accurately tracking the full game state may require additional machinery beyond a finetuned LLM."

**Note the Combat row: the majority baseline (.89) BEATS the finetuned model (.82).** Per-slot accuracy is misleading; joint accuracy is the honest number and it collapses to 58%.

## 5. Human evaluation — methodology and IAA

**Annotators:** **6 professional raters** (not crowd workers). "The raters were selected based on their professed interest in the fantasy genre, and on their background with D&D. All raters were fantasy fans, and 5 of the 6 had played D&D. 3 raters had been the DM in a game before."

**Volume:** "Our raters annotated **500 system outputs with 3-way redundancy** on each output."

**Dimensions:** sense (binary), specific (binary), interestingness (10-point scale).

### INTER-RATER AGREEMENT (§5.2, verbatim) — **THE KEY NUMBERS**

> "For the binary sense and specific scores, pairwise annotator agreement was **0.8**, with a chance-adjusted **Randolph Kappa score of 0.6**. For the scalar interestingness scores, the **Kendall's Tau correlation was 0.46**."

So: **binary/factual-ish judgments → Randolph κ = 0.6. Scalar aesthetic judgment ("interestingness") → Kendall's τ = 0.46.** The aesthetic dimension is measurably less reliable than the binary ones, using expert raters, on the same items.

### Results (Table 4)

| Model | Sense | Specific | Interest |
|---|---|---|---|
| LLM-Dialog | 0.81 | 0.85 | 3.57 |
| LLM-DND | 0.9 | 0.9 | 3.91 |
| LLM-DND-PREV-CTRL | 0.86 | 0.88 | 3.96 |
| LLM-DND-CURR-CTRL | 0.88 | 0.9 | 3.96 |
| LLM-DND-ALL-CTRL | 0.87 | 0.88 | 3.92 |
| GOLD (human) | **0.92** | **0.92** | **4.17** |

"On average, the adapted systems make sense 6.75% more often than the baseline, are specific 4% more often, and are 0.37 points more interesting. However, the added control features do not seem to differ substantially from the LLM that is adapted to the D&D data without any control features."

### In-character vs out-of-character effect (Table 6) — IC minus OOC scores

| Model | Sense | Specific | Interest |
|---|---|---|---|
| LLM-Dialog | -0.01 | -0.01 | +0.06 |
| LLM-DND | -0.02 | +0.03 | +0.4 |
| LLM-DND-PREV-CTRL | +0.02 | +0.02 | +0.6 |
| LLM-DND-CURR-CTRL | +0.06 | +0.06 | **+0.93** |
| LLM-DND-ALL-CTRL | +0.07 | +0.06 | +0.81 |
| GOLD | +0.07 | +0.05 | **+1.02** |

"IC turns [advance] the fictional world often with evocative language, whereas OOC turns usually discuss rules or mechanics."

**This is a confound worth noting for our own design:** interestingness ratings move by ~1.0 point (on a 10-point scale) purely as a function of whether the turn is in-character — i.e. a *register* variable, not a quality variable, drives a large share of the aesthetic score. Analogous to length/style confounds in LLM-judge work.

## Relevance to companion-eval-platform

1. **Best available IAA comparison point, and it supports our thesis directionally.** With 6 *expert* raters (5/6 played D&D, 3 had been DM) and 3-way redundancy on 500 outputs: binary judgments reach **Randolph κ = 0.6**, but the scalar aesthetic judgment reaches only **Kendall's τ = 0.46**. Same raters, same items — the aesthetic dimension is reliably less reliable. Our alpha 0.25–0.34 is on *harder/more subjective* companion dimensions with (presumably) less domain-expert raters, so the gap is consistent with this literature rather than anomalous.
2. **Caveat before citing:** Randolph κ is a *free-marginal* kappa and is systematically **more generous** than Krippendorff's alpha or Cohen's κ on skewed binary data (sense = 0.81–0.92 positive rate is very skewed). Do not compare their 0.6 to our 0.25–0.34 head-to-head without noting this — a fixed-marginal statistic on the same data would likely be substantially lower. This is arguably a point *for* us: the one paper reporting agreement chose the metric most flattering to it.
3. **Joint accuracy (58%) is the honest objective metric and the model to copy.** Per-slot accuracies look fine (.76–.89) and even lose to a majority baseline on Combat (.82 vs .89); joint accuracy across all slots collapses to 58%. For our platform: report **joint/conjunctive pass rates over state assertions**, not per-dimension averages, which hide correlated failure and flatter the system.
4. **Game State Tracking = the "world-state amnesia" dimension operationalized objectively.** Slot-filling accuracy against a known state record is countable and verifiable, with no annotator required. This paper's state is only heuristic (0.91 for the combat classifier), so FIREBALL is the better ground truth — but the *task formulation* (DST-style slot-value pairs) is exactly what a companion-memory-consistency metric should look like.
5. **Register confound warning (Table 6):** interestingness swings +0.93 to +1.02 on IC vs OOC turns. Any aesthetic rating we collect is partly measuring register/mode, not quality. Argues for either controlling register or dropping the aesthetic dimension.
