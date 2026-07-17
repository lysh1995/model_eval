---
title: "DSTC Automatic Dialogue Evaluation Tracks: DSTC10 Track 5 (Automatic Evaluation and Moderation of Open-domain Dialogue Systems) and DSTC9 Track 3 (Interactive Evaluation of Dialog)"
url: https://arxiv.org/abs/2111.02110
authors: Chen Zhang, João Sedoc, Luis Fernando D'Haro, Rafael Banchs, Alexander Rudnicky (DSTC10 Track 5); Shikib Mehri, Yulan Feng, Carla Gordon, Seyed Hossein Alavi, David Traum, Maxine Eskenazi (DSTC9 Track 3)
year: 2021
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# DSTC Automatic Dialogue Evaluation Tracks

Two sources are covered in this file, each with its own header and URL.

**Provenance note on arxiv 2209.06618:** the task brief named arXiv **2209.06618** as the DSTC10 Track 5 paper. **This is incorrect.** 2209.06618 is *"Safe Autonomous Docking Maneuvers for a Floating Platform based on Input Sharing Control Barrier Functions"* (Saradagi, Banerjee, Satpute, Nikolakopoulos, 2022) — a robotics/control paper with no relation to dialogue. The correct DSTC10 Track 5 overview is **arXiv:2111.02110**.

---

## Source 1 — DSTC10 Track 5: "Automatic Evaluation and Moderation of Open-domain Dialogue Systems"

URL: https://arxiv.org/abs/2111.02110 (full text read via https://ar5iv.labs.arxiv.org/html/2111.02110)
Official repo for the metric subtask: https://github.com/e0397123/dstc10_metric_track

### Track structure — two subtasks

**Subtask 1 (Automatic Evaluation).** Verbatim:

> "The goal of this subtask is for participants to design robust automatic dialogue evaluation metrics that correlate well with human judgements across multiple dialogue domains as well as across different dialogue evaluation dimensions."

**Subtask 2 (Safe Chatbot Development / moderation).** Verbatim:

> "The goal of this subtask is for participants to build generative models that first detect a toxic user's comment, and then generate appropriate and polite responses that keep the dialogue fluid and nontoxic."

Subtask 1 had **nine participating teams**. (Track framing, verbatim from the abstract framing: the track addresses "the design of automatic evaluation metrics to propel the research and development cycles of dialogue technologies, and the management and moderation of offensive and toxic interactions".)

### UNIT OF EVALUATION — the critical distinction

Subtask 1 is **not** split into two separately-scored subtasks. Instead, the **unit of evaluation is a property of each meta-evaluation dataset**, and each dataset in Table 1 carries an explicit `Type` column with value **`Turn`** or **`Dialogue`**:

- **Turn-level datasets:** one score per *(context, response)* pair. The metric scores a single candidate response given the preceding context. Table 1 lists **12 turn-level datasets**.
- **Dialogue-level datasets:** one score per *entire conversation*. The metric scores a whole multi-turn dialogue as a unit. Table 1 lists **2 dialogue-level datasets: FED-Dial and Persona-See.** Note their `Avg.#Ctx/Hyp Words` column has **no hypothesis value ("–")** — there is no single candidate response, because the unit is the conversation.

> Caveat on counting: one automated extraction pass reported "11 turn-level," but enumerating the Table 1 rows with `Type = Turn` gives **12** (Persona-USR, ConvAI2-GRADE, Persona-Zhao, DailyDialog-GRADE, DailyDialog-Zhao, DailyDialog-Gupta, Topical-USR, Empathetic-GRADE, Reddit-DSTC7, Twitter-DSTC6, FED-Turn, HUMOD). 12 + 2 = 14, which matches the stated total of 14 development datasets. I report **12 turn / 2 dialogue**; the "11" figure appears to be a miscount and is not used here.

### Structure — development (meta-evaluation) datasets

**14 development datasets, 53,530 total instances**, verbatim reproduction of Table 1:

| Name | #Instances | Avg.#Utts. | Avg.#Ctx/Hyp Words | Type | #Criteria | #Annotations | Used NLG models |
|------|-----------|-----------|-------------------|------|-----------|--------------|-----------------|
| Persona-USR | 300 | 9.3 | 98.4 / 12.0 | **Turn** | 6 | 5,400 | Transformer Seq2Seq, LSTM LM, Memory Network |
| ConvAI2-GRADE | 600 | 3.0 | 24.4 / 11.3 | **Turn** | 1 | 3,000 | Transformer Seq2Seq, DialoGPT, BERT/Transformer Ranker |
| Persona-Zhao | 900 | 5.1 | 48.8 / 11.5 | **Turn** | 1 | 3,600 | LSTM Seq2Seq, GPT-2 |
| DailyDialog-GRADE | 300 | 3.0 | 26.0 / 10.8 | **Turn** | 1 | 3,000 | Transformer Seq2Seq, Transformer Ranker |
| DailyDialog-Zhao | 900 | 4.7 | 47.5 / 11.0 | **Turn** | 4 | 14,400 | LSTM Seq2Seq, Random, GPT-2 |
| DailyDialog-Gupta | 500 | 4.92 | 49.9 / 10.9 | **Turn** | 1 | 2,500 | LSTM Seq2Seq, Conditional VAE |
| Topical-USR | 360 | 11.2 | 236.3 / 22.4 | **Turn** | 6 | 6,480 | Transformers |
| Empathetic-GRADE | 300 | 3.0 | 29.0 / 15.6 | **Turn** | 1 | 3,000 | Transformer Seq2Seq, Transformer Ranker |
| Reddit-DSTC7 | 9,990 | 3.5 | 35.3 / 11.2 | **Turn** | 3 | 29,700 | RNN, LSTM Seq2Seq, Memory Network, Pointer-generator |
| Twitter-DSTC6 | 40,000 | 2.0 | 27.74 / 20.77 | **Turn** | 1 | 400,000 | LSTM Seq2Seq Variants |
| FED-Turn | 375 | 10.4 | 87.3 / 13.3 | **Turn** | 9 | 16,863 | Meena, Mitsuku |
| HUMOD | 9,500 | 3.9 | 17.0 / 6.1 | **Turn** | 2 | 57,000 | Random sampling |
| FED-Dial | 125 | 12.7 | 113.8 / – | **Dialogue** | 11 | 6,720 | Meena, Mitsuku |
| Persona-See | 3,316 | 12.0 | 91.07 / – | **Dialogue** | 9 | 29,844 | LSTM Seq2Seq with Different Controlling Strategies |

Observations relevant to a companion-eval platform:
- Dialogue-level data is **scarce and small**: FED-Dial is only **125** dialogues; Persona-See is **3,316**. Against 40,000 turn-level instances in Twitter-DSTC6 alone. The dialogue-level unit is by far the less-resourced one.
- Dialogue-level datasets carry the **most annotation criteria** (FED-Dial: 11; Persona-See: 9) — conversation-level quality is treated as more multi-dimensional than turn quality.
- `Avg.#Utts.` for the dialogue-level sets is **12.7 (FED-Dial)** and **12.0 (Persona-See)** — i.e. the "whole conversation" unit here is ~12 utterances deep. Many turn-level sets have `Avg.#Utts.` of only **2.0–3.0** (Twitter-DSTC6: 2.0; ConvAI2-GRADE / DailyDialog-GRADE / Empathetic-GRADE: 3.0), meaning the "context" is often barely multi-turn at all.

### Structure — hidden test datasets

> "During the final evaluation phase, we have collected five hidden test evaluation datasets for assessing participants' submissions."

**5 test datasets:**

| Name | Size / description |
|------|--------------------|
| JSALT | EmpatheticDialogues and TopicalChat segments |
| ESL | 200 English-learning dialogue segments |
| NCM | 200 single-turn prompts |
| Topical-DSTC10 | 4,500 context-response pairs (9 responses per context) |
| Persona-DSTC10 | 5,000 context-response pairs (10 responses per context) |

Note **NCM is explicitly single-turn** (200 single-turn prompts) — a single-turn vs multi-turn contrast is baked into the test suite.

### Deep AM-FM baseline

The organizers' baseline is **Deep AM-FM** (Adequacy Metric / Fluency Metric ensemble). Verbatim:

> "For AM, we compute the cosine similarity between the sentence-level embedding of the response and that of the last sentence in the corresponding dialogue context. For FM, we follow the formulation of the context-response coherence metric in HolisticEval."

Backbones: **RoBERTa-base for AM** and **GPT2-medium for FM**, both adapted to dialogue corpora (**DailyDialog, TopicalChat, ConvAI2, EmpatheticDialogues**).

Structural note for our purposes: the AM component compares the response only to **the last sentence of the context**. This is a *local* coherence signal — it has no mechanism for tracking quality across a long conversation, persona drift, or repetition over many turns.

### Scoring methodology

> "Each dimension-wise correlation score is computed between the metric scores assigned to all the data instances within a test dataset and the corresponding human annotated scores along one evaluation criteria of that particular dataset."

Final ranking averaged **the 11 dimension-wise correlation scores over all the five [test] datasets**. All correlations below are **Spearman**, reported in percent.

### RESULTS — Table 2, hidden TEST set (Spearman %, average of dimension-wise correlations)

| Datasets | Baseline | Team 1 | Team 2 | Team 3 | Team 4 | Team 5 | Team 6 | Team 7 | Team 8 | Team 9 |
|----------|----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| JSALT | 5.09 | 27.74 | 3.10 | 10.54 | 4.96 | 11.66 | 12.73 | 4.07 | 8.75 | 26.42 |
| ESL | 32.29 | 43.18 | 19.86 | 28.75 | 9.34 | 40.01 | 32.92 | 3.28 | 36.10 | 45.58 |
| NCM | 16.49 | 29.91 | 1.98 | 22.08 | 8.24 | 29.60 | 26.60 | 2.01 | 25.57 | 19.11 |
| Topical-DSTC10 | 17.48 | 21.32 | 10.85 | 14.56 | 8.33 | 23.68 | 20.00 | 1.43 | 22.77 | 17.41 |
| Persona-DSTC10 | 19.61 | 30.67 | 7.77 | 25.80 | 16.59 | 37.50 | 35.78 | 2.54 | 37.22 | 33.82 |
| **Average** | **18.38** | **27.81** | **8.95** | **20.20** | **10.29** | **29.63** | **26.86** | **2.30** | **28.19** | **26.89** |

**Test-set ranking:** Team 5 = **29.63%** (1st), Team 8 = **28.19%** (2nd), Team 1 = **27.81%** (3rd). Baseline (Deep AM-FM) = **18.38%**.

**The headline number for our purposes: the winning system correlates with human judgment at Spearman ≈ 0.30 on held-out test data.** Four of nine teams (2, 3, 4, 7) failed to beat the 18.38% baseline.

### RESULTS — Table 3, DEVELOPMENT set (Spearman %)

| Datasets | Baseline | Team 1 | Team 2 | Team 3 | Team 4 | Team 5 | Team 6 | Team 7 | Team 8 | Team 9 |
|----------|----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| ConvAI2-GRADE | 9.38 | 50.43 | 7.23 | 41.01 | 17.31 | 58.43 | 60.42 | 57.00 | 60.43 | 53.07 |
| DailyDialog-GRADE | 15.48 | 36.30 | 3.45 | 11.16 | 19.86 | 33.42 | 30.00 | 64.42 | 30.06 | 41.89 |
| DailyDialog-Gupta | 17.70 | 56.78 | 2.76 | 38.16 | 11.39 | 63.25 | 61.37 | 78.85 | 60.84 | 46.69 |
| DailyDialog-Zhao | 22.25 | 36.94 | 20.96 | 33.09 | 19.85 | 48.03 | 52.99 | 54.50 | 52.79 | 28.70 |
| Twitter-DSTC6 | 9.96 | 24.46 | 8.05 | 47.95 | 4.26 | 17.94 | 18.35 | 61.63 | 18.31 | 18.54 |
| Reddit-DSTC7 | 2.67 | 33.97 | 19.78 | 25.75 | 12.14 | 32.48 | 34.15 | 31.30 | 34.12 | 33.16 |
| Empathetic-GRADE | 2.51 | 39.52 | 6.38 | 22.59 | 4.70 | 30.57 | 24.62 | 50.10 | 24.65 | 36.50 |
| FED-Turn | 5.09 | 23.85 | 9.49 | 11.96 | 19.27 | 30.38 | 33.01 | 35.15 | 32.88 | 19.87 |
| HUMOD | 11.73 | 32.86 | 1.93 | 31.11 | 4.16 | 33.20 | 33.83 | 22.45 | 33.83 | 22.28 |
| Persona-USR | 14.42 | 27.25 | 12.22 | 21.61 | 26.69 | 40.36 | 35.51 | 47.88 | 36.17 | 22.60 |
| Persona-Zhao | 46.79 | 55.21 | 24.23 | 50.19 | 5.23 | 61.32 | 64.24 | 76.40 | 64.58 | 55.70 |
| Topical-USR | 14.10 | 21.84 | 29.59 | 17.06 | 27.79 | 39.08 | 38.68 | 45.49 | 40.24 | 13.73 |
| **FED-Dial** *(dialogue-level)* | 11.18 | 26.92 | 25.22 | 5.70 | 5.93 | 46.89 | 49.31 | **77.42** | 49.31 | 40.26 |
| **Persona-See** *(dialogue-level)* | 8.08 | **5.70** | **3.50** | **6.95** | **3.69** | **8.78** | **12.92** | **27.52** | **12.92** | **6.27** |
| **Average** | **13.67** | **33.72** | **12.48** | **26.02** | **13.02** | **38.87** | **39.24** | **52.15** | **39.37** | **31.38** |

Dev-set best: **Team 7 = 52.15%**, described as "significantly outperforming peers by ~13%." Baseline = **13.67%**.

### EXPLICIT FINDING — generalization / robustness failure

Verbatim:

> "In general, all teams' performance on the test datasets is worse compared to that on the development datasets... all teams' performance drop is expected as the test datasets and development datasets are of different distributions."

This is the single most important finding in the track. Concretely:

- **Team 7 is the catastrophic case: 52.15% on dev → 2.30% on test.** It ranked **1st on dev and last (9th) on test**, below even the baseline's 18.38%. A metric can be tuned to near-0.8 Spearman on some dev sets (78.85 on DailyDialog-Gupta, 77.42 on FED-Dial, 76.40 on Persona-Zhao) and be **statistically indistinguishable from noise** on unseen distributions.
- **Every team dropped.** Team 5: 38.87 → 29.63. Team 8: 39.37 → 28.19. Team 6: 39.24 → 26.86. Team 1: 33.72 → 27.81.
- **Dev-set rank does not predict test-set rank.** Dev order was 7 > 8 ≈ 6 ≈ 5 > 1 > 9 > 3 > 2 ≈ 4; test order was 5 > 8 > 9 ≈ 1 > 6 > 3 > 4 > 2 > 7.
- **Per-dataset variance within a single system is enormous.** Team 7 on dev: 78.85 (DailyDialog-Gupta) vs 22.45 (HUMOD). Team 1 on test: 43.18 (ESL) vs 21.32 (Topical-DSTC10). The baseline on dev: 46.79 (Persona-Zhao) vs 2.51 (Empathetic-GRADE) — an 18x spread. **"Correlates well with humans" is never a property of a metric; it is a property of a (metric, dataset, dimension) triple.**

### EXPLICIT FINDING — dialogue-level is much harder than turn-level

**Persona-See (dialogue-level, 3,316 dialogues) is the worst-performing dataset for 8 of 9 teams and near-worst for the baseline.** Every single system scores in single digits or low teens: baseline 8.08, Team 1 **5.70**, Team 2 **3.50**, Team 3 6.95, Team 4 3.69, Team 5 **8.78**, Team 6 12.92, Team 8 12.92, Team 9 6.27. Only Team 7 exceeds 20 (27.52). Compare against the same systems' turn-level scores on ConvAI2-GRADE (50–60%) or Persona-Zhao (55–64%).

**Team 1 (3rd place overall on test) scores 5.70 on Persona-See — below the 8.08 baseline.** Team 5 (test winner) scores 8.78, barely above baseline.

The two dialogue-level datasets diverge sharply from each other: FED-Dial draws respectable numbers (46.89–49.31 for the top teams, 77.42 for Team 7) while Persona-See collapses for everyone. So "dialogue-level" is not one uniform difficulty either. FED-Dial is only **125 dialogues**, so its correlations rest on a small sample and should be read with that in mind.

**Takeaway for a companion-eval platform:** the field's automatic metrics are substantially built and validated at the **per-response** unit. At the **per-conversation** unit — which is what actually matters for a companion product, where the question is "was this relationship good over 30 turns," not "was this reply okay" — measured correlation with human judgment is roughly **0.06–0.13 Spearman** on Persona-See for the systems that won this challenge. That is effectively no signal.

### TURN INDEX / TURN DEPTH

**No finding about how quality changes with turn index or turn depth was located in the DSTC10 Track 5 overview paper.** The paper does not analyze correlation as a function of position in the conversation. I did not find such an analysis and am not inventing one. The closest available structural facts are the `Avg.#Utts.` column (context depth per dataset, 2.0–12.7) and the presence of NCM as an explicitly single-turn test set — but the paper reports no breakdown of metric performance by turn index. See DSTC9 below for the one turn-count finding that does exist.

### Subtask 2 (moderation) — one number

The **human answer baseline won 44.3% of comparisons** against other systems in the toxicity subtask. (Other Subtask 2 numbers not extracted.)

---

## Source 2 — DSTC9 Track 3: "Interactive Evaluation of Dialog Track at DSTC9"

URL: https://arxiv.org/abs/2207.14403 · ACL Anthology: https://aclanthology.org/2022.lrec-1.616/
Authors: Shikib Mehri, Yulan Feng, Carla Gordon, Seyed Hossein Alavi, David Traum, Maxine Eskenazi. LREC 2022.

**Naming note:** the brief refers to "DSTC9 Track 3: Automatic Evaluation and Moderation of Open-domain Dialogue Systems." That title belongs to **DSTC10 Track 5** (Source 1). The DSTC9 track on evaluation is the **Interactive Evaluation of Dialog Track**, by Mehri et al. Gunasekara et al. are authors of the broader **"Overview of the Ninth Dialog System Technology Challenge: DSTC9"** (arXiv:2011.06486), which summarizes all four DSTC9 tracks but — per the abstract page — does not itself contain the Track 3 correlation numbers; those are in Mehri et al.

### Abstract (verbatim)

> "The ultimate goal of dialog research is to develop systems that can be effectively used in interactive settings by real users. To this end, we introduced the Interactive Evaluation of Dialog Track at the 9th Dialog System Technology Challenge. This track consisted of two sub-tasks. The first sub-task involved building knowledge-grounded response generation models. The second sub-task aimed to extend dialog models beyond static datasets by assessing them in an interactive setting with real users. Our track challenges participants to develop strong response generation models and explore strategies that extend them to back-and-forth interactions with real users. The progression from static corpora to interactive evaluation introduces unique challenges and facilitates a more thorough assessment of open-domain dialog systems. This paper provides an overview of the track, including the methodology and results. Furthermore, it provides insights into how to best evaluate open-domain dialog models."

### UNIT OF EVALUATION — the two sub-tasks are the two units

This track is the cleanest statement of the per-response vs per-conversation split in the DSTC line of work, because **the two sub-tasks literally are the two units of evaluation**:

- **Sub-task 1 — static / per-response.** Knowledge-grounded response generation models scored on the **Topical-Chat** corpus. The unit is a **single response given a fixed context and a knowledge snippet**. Both automatic metrics and human assessment applied per-response.
- **Sub-task 2 — interactive / per-conversation.** Models deployed on **DialPort** and assessed through **real user interactions**, with post-hoc human evaluation of **complete conversations**. The unit is the **whole dialogue**.

### Structure — data

| Item | Value |
|------|-------|
| Sub-task 1 final submissions | **33** |
| Sub-task 2 systems | **11** (including **2 baselines**) |
| Topical-Chat corpus | **11,319 dialogs, 248,014 utterances** |
| Interactive conversations collected | **4,651 total**; **2,960** with ≥4 turns after filtering offensive content |
| Total turns | **38,488** (interactive); **41,640** (all) |

### Human evaluation dimensions — note the units differ

**Sub-task 1 (per-response) dimensions:** interestingness, engagement, specificity, relevance, correctness, semantic appropriateness, understandability, fluency, overall impression.

**Sub-task 2 (per-conversation) dimensions:** coherence/flow, error recovery, consistency, response diversity, topic depth, likeable personality, user understanding, flexibility/adaptability, informativeness, inquisitiveness, overall impression.

**These dimension sets are almost disjoint, and that is the point.** Per-conversation quality is measured by things that *cannot exist at the response level*: **error recovery, consistency, response diversity, topic depth, likeable personality, flexibility/adaptability**. A per-response metric has no way to observe repetition, contradiction with an earlier turn, persona stability, or whether the system recovered from a breakdown. For a companion product these are precisely the axes that determine whether a relationship holds up.

Inter-annotator agreement: **Spearman 0.57–0.58 (p<0.001)**.

### RESULTS — Sub-task 1 automatic metrics

Three automatic metrics were used: **METEOR** (word-overlap), **BERTScore** (embedding-based), **USR** (reference-free, model-based).

Representative system values:

| System | METEOR | BERTScore | USR |
|--------|--------|-----------|-----|
| 1 | 9.06 | 84.91 | 4.26 |
| 2 | 13.11 | 86.17 | 4.59 |
| 11 | 16.00 | 87.38 | 4.51 |

*(Only these three rows were recovered from the extraction; the full per-system table was not verified and is not reproduced here.)*

### CORRELATION WITH HUMAN JUDGMENT — the key numbers

| Metric | Spearman with human eval | Significance |
|--------|--------------------------|--------------|
| **USR** (reference-free, model-based) | **0.35** | p<0.05 |
| **METEOR** (word-overlap) | **0.23** | not reported as significant |
| **BERTScore** (embedding) | **0.22** | not reported as significant |

USR was the strongest of the three, and still only **0.35**. Note that **inter-annotator agreement was 0.57–0.58** — so the best automatic metric captures well under half the signal that humans agree on among themselves. The human ceiling is itself modest.

**Sub-task 2 (per-conversation), predictors of overall dialogue quality:**

| Predictor | Spearman | Significance |
|-----------|----------|--------------|
| **FED metric** | **0.49** | **p=0.13 — NOT statistically significant** |
| **Average number of dialog turns** | **0.94** | **p<0.01** |

### EXPLICIT FINDING — TURN COUNT / CONVERSATION DEPTH

**This is the DSTC finding on turn depth, and it is striking.**

**The average number of dialog turns correlates with human-judged overall dialogue quality at Spearman 0.94 (p<0.01)** — a stronger and far more statistically reliable predictor than the purpose-built FED metric (0.49, p=0.13, not significant) and than any per-response metric in Sub-task 1 (best 0.35).

Concretely, **top systems sustained longer user interactions: 12.44–13.47 turns, versus 5.80–9.82 turns for the other systems.**

Caveats worth carrying: this is a correlation across a **small number of systems (11, incl. 2 baselines)**, which inflates the achievable coefficient; and it is a **system-level** correlation (mean turns per system vs mean rating per system), **not** a finding that quality rises or falls at a given turn index *within* a conversation. It says *"systems that keep users talking longer are rated better,"* not *"turn 12 is better than turn 3."*

**I did not find, in either paper, an analysis of how per-turn quality varies as a function of turn index within a conversation.** Neither paper reports quality-vs-turn-position curves. I am not inventing one.

### EXPLICIT FINDING — single-turn vs multi-turn gap

Verbatim (the paper's headline conclusion):

> "state-of-the-art dialog models perform on-par with humans on response generation, but... fall short when considering an entire dialog."

**This is the single-turn vs multi-turn gap stated as plainly as the literature states it.** Human parity at the per-response unit does *not* transfer to the per-conversation unit.

Also verbatim on the static/interactive gap: Sub-task 2 scores were **"significantly more varied,"** indicating interactive evaluation **"more exhaustively tests"** system capabilities. Static per-response benchmarks compress systems together; interactive per-conversation evaluation spreads them apart and exposes differences the static setting cannot see.

---

## Cross-cutting implications for a companion/roleplay eval platform

1. **The unit of evaluation is the whole ballgame.** DSTC9 states it outright — models at human parity per-response "fall short when considering an entire dialog." DSTC10 shows it numerically — the same systems that hit 50–64% Spearman on turn-level ConvAI2-GRADE/Persona-Zhao collapse to **3.50–12.92%** on dialogue-level Persona-See. A companion product is judged per-conversation (and really, per-relationship). That is the unit where the field's metrics have the least signal and the least data.

2. **Ceiling check on what "good correlation" means.** DSTC10 Track 5 winner: **0.296 Spearman** on held-out test. DSTC9 best per-response metric (USR): **0.35**, against inter-annotator agreement of only **0.57–0.58**. Any vendor or paper claiming a general-purpose dialogue metric at 0.7+ correlation is almost certainly reporting a dev-set/in-distribution number. Cf. Team 7: **52.15 dev → 2.30 test**.

3. **Generalization is the default failure mode, not an edge case.** *Every* DSTC10 team dropped from dev to test; dev rank did not predict test rank; the dev leader finished last. **Any metric we adopt must be validated on our own held-out distribution.** Borrowed correlation numbers do not transfer.

4. **Turn count is a suspiciously strong signal (0.94, p<0.01) — treat as both opportunity and trap.** For a companion product, sustained engagement is close to the actual business metric, so this is worth instrumenting cheaply. But it is trivially gameable (a system that stalls or asks endless questions racks up turns), it was measured system-level across only 11 systems, and it is a proxy, not a quality measure.

5. **Steal the Sub-task 2 dimension list, not the Sub-task 1 list.** Coherence/flow, **error recovery**, **consistency**, response diversity, **topic depth**, **likeable personality**, user understanding, flexibility/adaptability, inquisitiveness — these are per-conversation properties, and they map far more directly onto companion quality than fluency/relevance/specificity do.

6. **Interactive > static for discriminating systems.** DSTC9: interactive scores were "significantly more varied" and "more exhaustively test" the system. Static replay of fixed contexts will under-report the differences we most care about.

7. **Local-coherence baselines are structurally blind to what we need.** Deep AM-FM's AM component compares the response only against **the last sentence of the context**. It cannot see persona drift, repetition, or contradiction across a long conversation — by construction.

## Verification status

- Verified from full text (ar5iv HTML): all DSTC10 Table 1 / Table 2 / Table 3 numbers, subtask definitions, Deep AM-FM description, scoring methodology, generalization quote.
- Verified from abstract page (ACL Anthology): DSTC9 title, authors, venue, full abstract.
- Extracted from DSTC9 PDF via automated pass: participation counts, corpus sizes, correlation figures (0.35 / 0.23 / 0.22 / 0.49 / 0.94), turn ranges, dimension lists, quoted conclusions. **The DSTC9 PDF resisted clean extraction on the first two attempts** (binary/compressed content); these figures come from a successful third pass but have **not** been cross-checked against a second rendering of the paper. Treat the DSTC9 numbers as **good but single-sourced** — re-verify against the published PDF before quoting externally.
- **Not found / not verified — explicitly not fabricated:** any quality-vs-turn-index curve in either paper; the DSTC10 turn-level-only vs dialogue-level-only aggregate averages (the paper reports per-dataset and overall averages, not a turn/dialogue split average — the split analysis above is my own reading of the per-dataset rows); the full DSTC9 Sub-task 1 per-system metric table (only systems 1, 2, 11 recovered); DSTC10 Subtask 2 numbers beyond the 44.3% human-answer figure; exact DSTC10 test-set annotation dimensions per dataset; the JSALT test set's instance count.
