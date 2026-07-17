---
title: "Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset (CRD3)"
url: https://aclanthology.org/2020.acl-main.459/
authors: Revanth Rameshkumar, Peter Bailey (Microsoft)
year: 2020
type: dataset
accessed: 2026-07-16
topic: game-simulation
---

# CRD3 — Critical Role D&D Dataset (ACL 2020, pp. 5121–5134)

**Code/data:** https://github.com/RevanthRameshkumar/CRD3 | **HF:** https://huggingface.co/datasets/microsoft/crd3

Transcripts of the *Critical Role* live-streamed D&D show, paired with fan-wiki abstractive summaries. Numbers below extracted directly from the ACL PDF text.

## 1. Dataset statistics (Table 1, verbatim)

| Metric | CRD3 | MELD | M. WOZ | AMI | CNN | DailyMail |
|---|---|---|---|---|---|---|
| Dialogue Count | **159** | 190 | 10438 | 142 | 92465 | 219506 |
| Turn Count | **398,682** | 13708 | 143048 | 79672 | 3074340 | 6189038 |
| Total token count in dialogues | **5,056,647** | 120913 | 1886018 | 706803 | 60476397 | 154282948 |
| Unique token count in dialogues | **42,509** | 6251 | 20197 | 9958 | 341451 | 596032 |
| Avg. turns per dialogue | **2507.4** | 72.2 | 13.7 | 561.1 | 33.4 | 28.2 |
| Avg. tokens per turn | 12.7 | 8.82 | 13.2 | 8.9 | 19.7 | 24.9 |
| Total token count in summaries | 327,899 | - | - | 22965 | 3897045 | 11308821 |
| Avg. tokens per summary | 2062.3 | - | - | 161.7 | 42.1 | 51.5 |
| Avg. summary:dialogue token ratio | 0.065 | - | - | 0.038 | 0.085 | 0.087 |

**Composition:** 159 episodes from two campaigns — **Campaign 1 = 113 episodes, Campaign 2 = 46 episodes.** Episodes are unscripted, live-streamed, several hours long.

**Speakers:** "We extract **72 total speakers** from the entire CRD3 dataset; **9 of which are the main cast** (players and DM) and make up **99.48% of the total turns**; the **DM alone makes up 111,994 turns**." (compare: MELD's 6 main cast = 83.27% of turns.)

**DM turns = 111,994 / 398,682 = 28.1% of all turns.** This is the single largest available corpus of *human DM behavior* specifically, which is why it matters for GM modeling.

Summaries are structured with **different levels of summarization**: (1) wiki opening blurb (briefest), (2) pre-show and announcements, (3) recap, (4) episode plot (largest, narrative developments, sub-divided by narrative topic). Break/post-episode sections also included.

## 2. Alignment / data augmentation method — WITH THRESHOLDS

Goal: break summaries into chunks and align each chunk to a contiguous segment of turns. Dialogue D of T turns; summary S split into n contiguous chunks; a_i is a contiguous set of turns (a_i = t_j:k).

**Match score (verbatim):** a scaled version of ROUGE-F1:

> β(s, a) = |τ(s) ∩ τ(a)| * ROUGE_F1

The authors evaluated "variations of ROUGE (Lin, 2004), variations of TF-IDF" before selecting this.

**Alignment algorithm:** **Needleman-Wunsch** over the match-score matrix (chosen to allow multiple turns assigned to one summary chunk, and one turn to overlap several summary chunks; strong order constraints).

**Augmentation:** run the algorithm for chunk sizes **C = 2, 3, and 4 sentences**, with C shifted starting windows → increases s,a pairs by a factor of C.

**Filtering thresholds (verbatim):**
- Remove dialogues with **|S| ≤ 10 chunks** (incomplete wikis) → **55,385 s,a pairs**
- Impose **2 < |t_j:k| ≤ 100**
- Strip pairs where s_i contains "Q: " (differently-formatted Q&A segment)
- → **34,243 pairs final**

**Table 3 — number of s_i,a_i pairs generated per chunk size:**

| Chunk Size | w/o Filtering | w/ Filtering |
|---|---|---|
| 2 | 18569 | 11124 |
| 3 | 18438 | 11635 |
| 4 | 18378 | 11484 |

**Splits:** 26,232 training / 3,470 validation / 4,541 test s,a pairs.

## 3. Alignment quality — OBJECTIVE VALIDATION

"We calculate precision and recall with respect to the turns on a random sample of **100 pairs** from the training split... and obtain a **precision of 0.8692 and recall of 0.9042.**"

Error analysis: "precision errors are mostly from extraneous trailing or leading turns attached to the properly aligned set of turns, and **almost never from complete misalignment**. We find recall errors are from turn sequences that start too late or end too early, and also almost never from complete misalignment."

## 4. Q&A evaluation of summary quality — a CLEVER OBJECTIVE PROXY

Method: on a random sample of **50 s_i,a_i pairs**, "the questioner records **two questions and answers per pair**, with the questions and answers coming **only from the summaries s_i**" — one **factoid** question (open-ended: yes/no, entity names, or short text) and one **multiple choice** question (4 options, at most one correct). "The questions are then answered by **another person, using only the aligned turns a_i** from the pair."

**Table 4 — Q&A evaluation results:**

| Question Type | Correct | Incorrect | Precision |
|---|---|---|---|
| Free Form | 39 | 11 | **78%** |
| Multiple Choice | 42 | 8 | **84%** |
| **Total** | **81** | **19** | **81%** |

"Out of the **19 incorrect answers**, we found that **17 of them were due to summary alignment errors**... The other **2 were due to misinterpretation of the question**. This indicates, with perfect alignment, all questions could have been answered correctly; meaning what is in the summaries is an accurate reflection of what is in the transcript." Also: "**12 incorrect answers were due to no answer**", i.e. the answerer felt they lacked information to attempt an answer.

**Authors' own caveat (verbatim):** "Unlike ROUGE precision, which relies on word overlap, this evaluation can incorporate latent semantic and contextual information. It is important to note that **latent information used when answering varies greatly between people, making this method subjective with respect to the answerer.** In future work, it would be interesting to **measure variance of accuracy and information in the answers using a large number of people.**"

→ i.e. the authors **explicitly flag that they did not measure inter-annotator variance and that they should have.**

## 5. Summarization benchmark (Table 5)

Baseline architecture: **Chen and Bansal (2018)** `fast_abs_rl` (rnn-ext + abs + RL + rerank), used **semi-supervised** because "the generated data has noise due to imperfections in the alignment method and due to potentially broken coreference." Extractor trained on a **sequence of turns rather than individual sentences** (due to non-narrative chit-chat between salient turns).

| | R1 | R2 | RL | METEOR |
|---|---|---|---|---|
| **Extractive (rnn-ext + RL)** | | | | |
| P | 20.83 ±.34 | 7.34 ±0.28 | 18.38 ±.32 | |
| R | 44.59 ±.66 | 17.42 ±.62 | 39.22 ±.61 | 16.58 |
| F1 | 25.20 ±.34 | 9.23 ±.32 | 22.20 ±.32 | |
| *Reported on CNN/DM (same model)* | *41.47* | *18.72* | *37.76* | *22.35* |
| **Abstractive (rnn-ext + abs + RL + rerank)** | | | | |
| P | 27.38 ±.34 | 5.91 ±.20 | 25.18 ±.32 | |
| R | 22.65 ±.27 | 4.75 ±.16 | 20.74 ±.26 | 8.33 |
| F1 | 23.35 ±.23 | 4.91 ±.16 | 21.41 ±.23 | |
| *Reported on CNN/DM (same model)* | *40.88* | *17.80* | *38.54* | *20.38* |

(± = 0.95 confidence interval.)

**CRD3 F1 is roughly half of the same model's CNN/DM F1** (25.20 vs 41.47 R1 extractive; 23.35 vs 40.88 abstractive) — collaborative-narrative dialogue is far harder than news.

"The purely extractive model significantly outperforms the combined model in recall and in F-1, due to the much higher recall."

**n-gram overlap analysis (validation set):** "the mean ratio of unique overlapping summary n-grams to total unique summary n-grams are: **1-gram = 0.679, 2-gram = 0.336, and 3-gram = 0.205.**"

## 6. IAA status

**NO inter-annotator agreement is reported. NO conventional human evaluation of generated summaries is reported.** Verified by grepping the full paper text for `krippendorff|kappa|inter-annotat|inter-rater|agreement` — **zero matches.** The only human-in-the-loop measurement is the Q&A precision study (§4), which uses **one questioner and one answerer** and whose authors explicitly acknowledge it is "subjective with respect to the answerer" with unmeasured between-person variance.

Stated dataset limitation (verbatim): "The dataset has relatively few episodes (159)".

## Relevance to companion-eval-platform

1. **The Q&A-precision method (§4) is the most directly stealable idea here, and it converts a subjective judgment into a countable one.** Instead of asking a rater "is this summary faithful?" (aesthetic, low alpha), they ask: *generate questions from the summary, have a different person answer them from the source alone, count correct answers.* Result: 81% overall (78% free-form / 84% MC), with **17 of 19 failures attributable to a specific, locatable alignment error**. Failures are diagnosable, not just scored. This is a template for a **companion memory-faithfulness metric**: generate factoid questions from the companion's claimed memory, answer them from the conversation record, count.
2. **But note the honest caveat — and that they never fixed it.** The authors themselves say the Q&A method is "subjective with respect to the answerer" and that measuring "variance of accuracy... using a large number of people" is future work. **They used n=1 answerer and reported no variance.** If we adopt this method we must do the thing they deferred: multiple answerers, report alpha. A Q&A-based metric is *more* objective than a Likert rating but is **not** annotator-free — the answerer still decides what counts as answerable (12 of 19 failures were "no answer", a judgment call about sufficiency).
3. **Third consecutive D&D paper with zero IAA** (CRD3 2020, Callison-Burch 2022 is the sole exception, FIREBALL 2023 none, Skill Check 2023 none). The non-reporting of agreement is the field norm, not our failure.
4. **CRD3 is the best corpus of *human DM* behavior: 111,994 DM turns (28.1% of 398,682).** If we ever need a human-GM reference distribution or few-shot exemplars, this is the source. Caveat: it is *performed* D&D for an audience (Critical Role are professional voice actors), so it is a ceiling/atypical sample, not representative play.
5. **Useful difficulty calibration:** the identical model scores ~2x lower F1 on CRD3 than CNN/DM (25.20 vs 41.47 R1). Collaborative multi-party narrative is measurably harder than the tasks these metrics were designed for — supports our skepticism that off-the-shelf overlap metrics transfer to companion/roleplay content.
6. **3-gram overlap of 0.205** between summaries and source is a concrete quantification of how much genuine abstraction occurs — useful if we need a threshold for "is this a summary or a copy?"
