---
title: Unsupervised Evaluation of Interactive Dialog with DialoGPT
url: https://aclanthology.org/2020.sigdial-1.28/
authors: Shikib Mehri, Maxine Eskenazi (Dialog Research Center, Language Technologies Institute, Carnegie Mellon University)
year: 2020
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# FED — Fine-grained Evaluation of Dialog

Venue: SIGdial 2020, pages 225–235. arXiv: 2006.12719.
**Source used: the ACL Anthology PDF full text (2020.sigdial-1.28.pdf), text-extracted locally. All numbers below are transcribed from the paper's own tables, not from a summary.**

## CORRECTION TO A COMMON MISCONCEPTION (important)

The task brief asked for "9 TURN-LEVEL and 9 DIALOG-LEVEL" qualities. **This is not what the paper says.** The actual split is **8 turn-level + 10 dialog-level = 18 fine-grained qualities**. Verbatim:

> "Eighteen fine-grained dialog qualities are measured in the FED dataset: eight at the turn level and ten at the dialog level."

Separately, each level adds an **Overall Impression** question that is NOT one of the eighteen fine-grained qualities. So the *question* counts are 9 turn-level and 11 dialog-level:

> "There were 9 questions for turn-level annotation and 11 for dialog-level annotation."

That is: 8 fine-grained + 1 overall = 9 turn questions; 10 fine-grained + 1 overall = 11 dialog questions. The "9 and 9" framing is incorrect in both halves.

## UNIT OF EVALUATION

FED is **dual-unit** — this is its defining property and the reason it matters for a companion-eval platform:

- **Turn level (per-response):** score one system response given the dialog context.
- **Dialog level (per-conversation):** score the system's behavior "over the duration of an entire conversation."

Verbatim: the FED metric "measures fine-grained dialog qualities at both the turn and whole dialog levels."

The metric formula is switched between units by *dropping the response term*: the dialog-level score is computed "by simply removing the system response r from the equation."

## Dataset composition (exact)

> "Workers on Amazon Mechanical Turk (AMT) annotated 40 Human-Meena conversations, 44 Human-Mitsuku conversations and 40 Human-Human conversations."

> "A total of 124 conversations were annotated (40 Meena, 44 Mitsuku, 40 Human). Five different workers saw each conversation (HIT). Each conversation had one dialog-level annotation and three turn-level annotations for chosen system responses that were randomly sampled from the conversation."

- **124 conversations total** = 40 Meena + 44 Mitsuku + 40 Human.
  - Human-system: 84 (40 Meena + 44 Mitsuku). Human-human: 40.
- **5 annotators per conversation.**
- **3 system responses per conversation** annotated at turn level.
- **3348 turn-level data points and 1364 dialog-level data points, total 4712.**

> "In total, the FED dataset includes 3348 turn-level and 1364 dialog-level data points, for a total of 4712."

Note the internal tension in the paper's own wording: §3 says the three turn-level responses were "hand-selected," while §3.3 says they were "randomly sampled from the conversation." Both phrasings appear; the paper does not reconcile them.

Source conversations are those released by Adiwardana et al. (2020) (the Meena paper). Mitsuku is a Loebner-Prize chatbot. In human-human dialogs "one of the humans was selected to play the role of the system." System names were masked: "all mentions of the system name were replaced with the word 'System.'"

**Evaluation-only dataset** — no training split:

> "This dataset intended to be used solely for the evaluation of metrics, as the number of annotated conversations is not large enough to accommodate both training and testing."

### Response scales
- Fine-grained qualities: **No, Somewhat, Yes, N/A**. "Responding N/A required written justification."
- **Understandable** (turn) drops the *Somewhat* option → binary.
- **Consistent** (dialog) drops *Somewhat*: "the existence of an inconsistency is binary."
- **Overall impression**: five-point Likert, both levels.

### Outlier post-processing (exact rule)
> "Given five annotations for a given question, the furthest label from the mean is removed if its distance from the mean is greater than half the standard deviation of the five annotations."

## The 18 fine-grained qualities (exact, as the questions are worded)

### 8 TURN-LEVEL fine-grained qualities (Table 1) + Overall
1. **Interesting** — "To the average person, is the response interesting?"
2. **Engaging** — "Is the response engaging?"
3. **Specific** — "Is the response generic or specific to the conversation?"
4. **Relevant** — "Is the response relevant to the conversation?"
5. **Correct** — "Is the response correct or was there a misunderstanding of the conversation?"
6. **Semantically Appropriate** — "Is the response semantically appropriate?"
7. **Understandable** — "Is the response understandable?"
8. **Fluent** — "Is the response fluently written?"
- (+) **Overall Impression** — "Overall impression of the response?"

Table 1 note: "No one has specifically used Correct, however its meaning is often encapsulated in Relevant."

### 10 DIALOG-LEVEL fine-grained qualities (Table 2) + Overall
1. **Coherent** — "Throughout the dialog, is the system coherent and maintain a good conversation flow?"
2. **Error Recovery** — "Is the system able to recover from errors that it makes?"
3. **Consistent** — "Is the system consistent in the information it provides throughout the conversation?"
4. **Diverse** — "Is there diversity in the system responses?"
5. **Topic Depth** — "Does the system discuss topics in depth?"
6. **Likeable** — "Does the system display a likeable personality?"
7. **Understanding** — "Does the system seem to understand the user?"
8. **Flexible** — "Is the system flexible and adaptable to the user and their interests?"
9. **Informative** — "Is the system informative throughout the conversation?"
10. **Inquisitive** — "Is the system inquisitive throughout the conversation?"
- (+) **Overall Impression** — "Overall impression of the dialog?"

Table 2 note: "To our knowledge, error recovery has not been used for human evaluation."

Note that **6 of the 10 dialog-level qualities have no turn-level analogue at all** (Error Recovery, Consistent, Diverse, Topic Depth, Flexible, Inquisitive). They are only definable over a conversation. This is the structural argument for per-conversation evaluation.

## Method — untrained DialoGPT, follow-up likelihood, no training/reference

Three stated properties: the FED metric "(1) does not rely on a ground-truth response, (2) does not require training data and (3) measures fine-grained dialog qualities at both the turn and whole dialog levels."

Core intuition, verbatim:

> "we posit that DialoGPT has implicitly captured some notion of dialog quality and can therefore be used for dialog evaluation."

> "Given a system response, its quality is measured by computing the likelihood that DialoGPT will respond to it with a particular follow-up utterance (e.g., 'That is really interesting!'). DialoGPT is more likely to respond in this way to what it believes is an interesting system response."

> "DialoGPT will be more likely to respond with a positive follow-up utterance if given a better (e.g., more interesting/relevant/fluent) preceding system utterance."

**Scoring equation.** Given dialog context `c`, system response `r`, and `D` = log-likelihood of DialoGPT generating a particular response; `p` = set of positive follow-up utterances, `n` = set of negative follow-ups:

```
score = Σ_{i=1..|p|} D(c + r, p_i)  −  Σ_{i=1..|n|} D(c + r, n_i)      (Eq. 1)
```

> "This equation can be modified to predict scores for dialog-level qualities, by simply removing the system response r from the equation."

**Follow-up utterance construction:**
> "For each of the eighteen qualities, several positive and negative utterances were hand-written and minimally tuned on a small subset of the dataset (10 conversations)."
- "The number of positive utterances for each dialog quality ranges between 0 and 4, and the number of negative utterances ranges between 1 and 4."
- The full follow-up utterance lists are "provided in the supplementary materials" — **not in the main paper body, so the exact per-quality utterance strings are not reproduced here.**

**Negatives carry more signal than positives:**
> "Generally, negative follow-up utterances are more meaningful than positive ones. For example, if a system response is irrelevant, a follow-up utterance of 'That's not relevant' is reasonable. However, acknowledging the relevance of a system response is less likely."

**Overall scores are an average, not a follow-up probe:**
> "While the fine-grained qualities are computed in this manner, the overall impression scores are calculated as an average of the scores for either the turn-level or dialog-level qualities."

**Context window differs by quality (turn-depth-relevant):**
> "Most of the turn-level qualities were scored using only the last system response as context. For relevant, correct and dialog-level metrics, the entire conversation was used as context."

**Model variants:** four DialoGPT variants — medium 345M and large 762M, each either fine-tuned from GPT-2 (`ft`) or trained from scratch (`fs`). DialoGPT was trained on "147M conversation-like interactions from Reddit." The small 117M model was excluded. Follow-ups were tuned on 10 conversations using the 762M fine-tuned model.

## RESULTS — Spearman correlations with human judgment (Table 6, verbatim)

Spearman correlation between predicted quality scores and the **mean** of annotated scores. Columns are the four DialoGPT variants. **Bold = best per row (marked ** below). Values not statistically significant (p > 0.05) are italicized in the paper — italics are not recoverable from text extraction, so significance is NOT marked per-cell here; treat the low values (Relevant, Correct, Understandable, Consistent at several variants) with caution.**

| Quality | 345M fs | 345M ft | 762M fs | 762M ft |
|---|---|---|---|---|
| **Turn-Level** | | | | |
| Interesting | 0.388 | **0.431** | 0.406 | 0.408 |
| Engaging | 0.268 | 0.285 | 0.278 | **0.318** |
| Specific | 0.260 | **0.326** | 0.270 | 0.267 |
| Relevant | 0.028 | -0.027 | 0.001 | **0.152** |
| Correct | 0.000 | 0.037 | 0.020 | **0.133** |
| Semantically Appropriate | 0.040 | **0.177** | 0.141 | 0.155 |
| Understandable | 0.047 | 0.048 | 0.075 | **0.111** |
| Fluent | 0.157 | 0.184 | 0.133 | **0.224** |
| **Overall (turn)** | 0.122 | 0.092 | 0.094 | **0.209** |
| **Dialog-Level** | | | | |
| Coherent | 0.195 | 0.151 | 0.149 | **0.251** |
| Error Recovery | **0.165** | 0.128 | 0.126 | **0.165** |
| Consistent | 0.041 | 0.011 | 0.006 | **0.116** |
| Diverse | **0.449** | 0.431 | 0.414 | 0.420 |
| Topic Depth | **0.522** | 0.479 | 0.470 | 0.476 |
| Likeable | 0.047 | 0.172 | 0.224 | **0.262** |
| Understanding | 0.237 | 0.174 | 0.192 | **0.306** |
| Flexible | 0.260 | **0.408** | 0.298 | 0.293 |
| Informative | 0.264 | 0.328 | **0.337** | 0.288 |
| Inquisitive | 0.137 | 0.143 | **0.298** | 0.163 |
| **Overall (dialog)** | **0.401** | 0.359 | 0.355 | **0.443** |

### Headline numbers (verbatim)

> "The best overall turn-level correlation is 0.209 and the best overall dialog-level correlation is 0.443."

**Dialog-level Overall correlation (0.443) is >2x the turn-level Overall correlation (0.209).**

**Pearson correlations are NOT reported.** The paper reports Spearman only (Table 6). Any Pearson figure for FED would be fabricated — it does not exist in this paper.

### Comparison to prior work (verbatim)
> "To our knowledge, there are presently no other metrics that operate without a ground-truth response, thus these results cannot be directly compared to any existing metrics. However, prior work on dialog evaluation reveals roughly similar correlation. Multi-reference evaluation for dialog achieves correlations in the 0.10 - 0.27 range (Gupta et al., 2019) and ADEM has correlations in the 0.28 - 0.42 range (Lowe et al., 2017)."

## TURN-DEPTH / SINGLE-TURN vs MULTI-TURN EVIDENCE (critical for the platform)

FED contains **no analysis of quality as a function of turn index** — it does not plot or measure degradation over turn position. Do not claim it does.

What it DOES establish — and this is stronger and more directly useful — is that **turn-level quality does not aggregate into dialog-level quality**, i.e. per-response scoring systematically misranks systems.

### 1. Turn-level scores INVERT the true system ranking (Table 4)

> "For all of the turn-level qualities, Meena outperforms both Mitsuku and Human."

> "However, turn-level qualities are insufficient to evaluate a dialog system. Dialog is by definition a multi-turn interaction. Thus, in some cases, a sub-optimal system response might result in a better long-term dialog. Humans significantly outperform the two systems for dialog-level qualities."

Table 4 — Performance of each system (scales: 1-3, except Understandable/Consistent 0-1, Overall 1-5):

| Quality | Mitsuku | Meena | Human |
|---|---|---|---|
| **Turn-Level** | | | |
| Interesting | 2.30 | **2.58** | 2.35 |
| Engaging | 2.53 | **2.75** | 2.49 |
| Specific | 2.48 | **2.74** | 2.56 |
| Relevant | 2.80 | **2.88** | 2.74 |
| Correct | 2.74 | **2.84** | 2.66 |
| Semantically Appropriate | 2.84 | **2.92** | 2.85 |
| Understandable | 0.97 | 0.97 | 0.94 |
| Fluent | 2.83 | **2.90** | 2.80 |
| **Overall (turn)** | 3.81 | **4.19** | 3.85 |
| **Dialog-Level** | | | |
| Coherent | 2.20 | 2.88 | **2.94** |
| Error Recovery | 2.22 | 2.69 | **2.86** |
| Consistent | 0.82 | 0.95 | **0.98** |
| Diverse | 2.23 | 2.46 | **2.88** |
| Topic Depth | 1.80 | 2.28 | **2.78** |
| Likeable | 2.10 | 2.61 | **2.97** |
| Understanding | 2.23 | 2.86 | **2.98** |
| Flexible | 2.22 | 2.72 | **2.97** |
| Informative | 2.10 | 2.60 | **2.85** |
| Inquisitive | 2.35 | 2.76 | **2.88** |
| **Overall (dialog)** | 3.10 | 4.11 | **4.60** |

**This is the key result.** At the turn level, **Meena (4.19) beats Human (3.85)** on Overall — a bot scores higher per-response than a real person. At the dialog level the ranking flips and widens: **Human 4.60 > Meena 4.11 > Mitsuku 3.10**. The turn-level→dialog-level delta for Human is **+0.75** (3.85→4.60) while for Meena it is **−0.08** (4.19→4.11) and for Mitsuku **−0.71** (3.81→3.10).

Concretely: a per-response eval would have told you Meena is *better than a human*. A per-conversation eval tells you it is 0.49 worse. **Per-response evaluation is not merely noisier — it is directionally wrong.** For a companion-character platform this is the single most load-bearing finding in the paper: any eval that scores replies in isolation will rank a bot that produces punchy, specific, interesting individual lines above one that actually sustains a relationship.

Where the multi-turn signal concentrates: the widest Meena-vs-Human dialog-level gaps are **Topic Depth** (2.28 vs 2.78, −0.50), **Diverse** (2.46 vs 2.88, −0.42), and **Likeable** (2.61 vs 2.97, −0.36). Paper's own read:

> "Meena's scores suggest that it is fairly coherent, understanding and flexible. However, it struggles with diversity, topic depth and likeable."

Mitsuku's worst dialog-level quality is **Topic Depth at 1.80** — the lowest cell in the entire dialog-level table. Depth-of-topic and non-repetition are exactly the failure modes invisible to single-turn scoring.

### 2. Dialog-level annotation is more reliable than turn-level
> "The difference between Meena and Mitsuku is very pronounced at the dialog level, with a 1 point difference in overall score. The higher variance in scores and the stronger performance of human dialogs, shows that dialog-level evaluation is reliable than turn-level."

(sic — the paper's sentence is missing "more"; it means dialog-level evaluation is *more* reliable than turn-level.)

### 3. The metric itself also works better at the dialog level
Best Overall dialog-level correlation **0.443** vs best Overall turn-level **0.209**.

## Inter-annotator agreement (Table 3) — NOT metric performance

**Do not confuse Table 3 with Table 6.** Table 3 is agreement among human annotators (each annotation vs the mean of the others), not the FED metric's correlation. These numbers are high (0.5–0.84) and are easily misquoted as metric performance.

| Quality | Spearman | | Quality | Spearman |
|---|---|---|---|---|
| **Turn-Level** | | | **Dialog-Level** | |
| Interesting | 0.819 | | Coherent | 0.809 |
| Engaging | 0.798 | | Error Recovery | 0.840 |
| Specific | 0.790 | | Consistent | 0.562 |
| Relevant | 0.753 | | Diverse | 0.789 |
| Correct | 0.780 | | Topic Depth | 0.833 |
| Semantically Appropriate | 0.682 | | Likeable | 0.838 |
| Understandable | 0.522 | | Understanding | 0.809 |
| Fluent | 0.714 | | Flexible | 0.816 |
| Overall Impression | 0.820 | | Informative | 0.806 |
| | | | Inquisitive | 0.769 |
| | | | Overall Impression | 0.830 |

> "Inter-annotator agreement is high for all of the dialog qualities... Two qualities, understandable and consistent, have slightly lower correlations, in the 0.5 - 0.6 range. These qualities did not include Somewhat as an answer. This probably contributed to the lower inter-annotator agreement."

## Which qualities drive Overall Impression (Table 5)

Softmax over regression weights predicting Overall from the fine-grained qualities. **Bold = most important per level.**

| Turn-Level | Importance (%) | | Dialog-Level | Importance (%) |
|---|---|---|---|---|
| Interesting | 16.15 | | Coherent | **10.95** |
| Engaging | 7.46 | | Error Recovery | 9.15 |
| Specific | 9.64 | | Consistent | 7.92 |
| Relevant | **18.10** | | Diverse | 10.09 |
| Correct | 13.77 | | Topic Depth | 10.51 |
| Semantically Appropriate | 9.90 | | Likeable | **12.03** |
| Understandable | 10.70 | | Understanding | **11.01** |
| Fluent | 14.27 | | Flexible | 10.34 |
| | | | Informative | 8.00 |
| | | | Inquisitive | 9.50 |

> "The most important turn-level qualities are interesting, relevant and fluent."

> "There is less variance in the importance of dialog-level qualities than in the turn-level qualities possibly because there is less overlap in meaning amongst the qualities and all of the dialog-level qualities seem somewhat important. The most important dialog-level qualities are coherent, likeable and understanding."

For a companion platform: **Likeable (12.03%) is the second-most-important dialog-level quality** — and it has no turn-level counterpart. Likeability is only measurable per-conversation.

## Where FED fails, and why (verbatim)

> "The FED metric works better for some dialog qualities than others. This is because DialoGPT was trained on Reddit. It is more likely that it has captured certain dialog qualities that Reddit exhibits. For example, it is more likely that DialoGPT learns to measure qualities like interesting and engaging, than understandable and consistent."

> "since Reddit is a multi-participant forum and not a one-on-one conversation, inconsistencies in conversation history are unlikely to be reflected in the response. As such, it is unsurprising that this approach struggles to measure the consistency of a dialog."

This matters directly: **Consistent** — persona/character consistency, the core quality for a companion product — is FED's *worst* dialog-level quality (best correlation 0.116). FED cannot measure character consistency. The paper is explicit that the Reddit pretraining domain is the cause.

Compositionality note:
> "this difference in performance across the different dialog qualities suggests that DialoGPT exhibits some degree of compositionality... however it still struggles with follow-up utterances consisting of less frequently observed concepts (e.g., consistent, understandable)."

## Stated limitations

- **Gameable:** "there is the potential to game the FED metric and obtain artificially high scores, especially by having a model produce responses that are likely to result in specific follow-up utterances. To this end, the FED metric is not a replacement for human evaluation. It is instead a means of measuring dialog quality for the purposes of validation and model tuning."
- **Open-domain chitchat only:** "the FED dataset consists of only open-domain chit-chat conversations. As such, future work is needed to determine whether the FED metric will generalize to goal-oriented dialog."
- **Generalization claim:** "Since these three systems are different in nature and FED exhibits strong correlation with human judgements across all the systems, we believe that the performance of FED will hold for other open-domain dialog systems."

## Relation to USR (same authors)

> "Mehri and Eskenazi (2020) introduce USR, an unsupervised and reference-free evaluation metric for dialog generation. Similar to FED, USR uses pre-trained models to assess several dialog qualities. However, they are limited to five qualities with hand-designed models and unsupervised tasks for each quality. In comparison, FED is more general and encapsulates eighteen dialog qualities."

FED is the multi-turn successor to USR: USR is response-level and needs per-quality trained models; FED is turn+dialog level and needs no training at all.
