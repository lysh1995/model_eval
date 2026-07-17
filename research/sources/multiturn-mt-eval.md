---
title: "MT-Eval: A Multi-Turn Capabilities Evaluation Benchmark for Large Language Models"
url: https://aclanthology.org/2024.emnlp-main.1124/
authors: Wai-Chung Kwan, Xingshan Zeng, Yuxin Jiang, Yufei Wang, Liangyou Li, Lifeng Shang, Xin Jiang, Qun Liu, Kam-Fai Wong
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# MT-Eval

**Venue:** EMNLP 2024 (Main), pages 20153–20177. arXiv: 2401.16745. Code/data: https://github.com/KwanWaiChung/MT-Eval
**Affiliations:** CUHK; Huawei Noah's Ark Lab; HKUST.
**Source used:** full PDF text from ACL Anthology (`2024.emnlp-main.1124.pdf`), extracted locally. arxiv HTML renders (`/html/2401.16745v1`, ar5iv) all 404 — the PDF is the only reliable full text.

> **⚠️ Version discrepancy:** the arXiv abstract page says "**11** well-known LLMs"; the published EMNLP version says "**10** well-known LLMs" and Tables 2/3 list exactly 10 rows. **Use 10.** (An earlier draft of this note said 11, sourced from the arXiv abstract — corrected here against the published version.)

---

## 1. Abstract (verbatim, key claims)

> "existing benchmarks mainly focus on single-turn evaluations, overlooking the models' capabilities in multi-turn interactions. ... we categorize interaction patterns into four types: recollection, expansion, refinement, and follow-up. We construct multi-turn queries for each category either by augmenting existing datasets or creating new examples using GPT-4 with a human-in-the-loop process to **avoid data leakage**. To study the factors impacting multi-turn abilities, we **create single-turn versions of the 1170 multi-turn queries and compare performance**. Our evaluation of 10 well-known LLMs shows that while closed-source models generally surpass open-source ones, certain open-source models exceed GPT-3.5-Turbo in specific tasks. We observe **significant performance degradation in multi-turn settings compared to single-turn settings in most models, which is not correlated with the models' fundamental capabilities**. Moreover, we identify the **distance to relevant content** and **susceptibility to error propagation** as the key factors influencing multi-turn performance."

**The paired single-turn/multi-turn design is this paper's central methodological contribution** — same family as Laban's `Full` vs `Sharded` and Multi-IF's turn-1 baseline.

---

## 2. Dataset — Table 1 (verbatim)

| Statistic | Number |
|---|---|
| Avg. # Turns per Dialogue | 6.96 |
| Avg. # Words in Prompt † | 760.41 |
| Max. # Words in Prompt † | 2574 |
| Avg. # Words in Response † | 99.31 |
| Max. # Words in Response † | 444 |
| Avg. # Words per Turn | 60.63 |
| Max. # Words per Turn | 474 |
| **Total # Dialogues** | **168** |
| **Total # Turns** | **1170** |

† Estimated using GPT-4 responses.

> "It comprises **168 dialogue sessions with 1,170 turns**"

Note the often-cited "1,170 multi-turn queries" is the **turn** count; the dialogue count is **168**. Construction: "To prevent data leakage in MT-Eval, we either extend existing datasets or construct new instances using GPT-4 with human-in-the-loop verification." Models used: `gpt-3.5-turbo-0613`, `gpt-4-0613`.

---

## 3. The four interaction types (verbatim definitions)

- **Recollection:** "Users present queries or tasks that necessitate the assistant's capacity to retrieve information from prior interactions, relying on the assistant's **global context awareness and long-term memory** capabilities. For instance, a user may instruct the model to initiate all the following responses with words starting with the letter 'c.'"
- **Expansion:** "Users delve into various subjects while staying within the confines of the same topic. For example, the user might ask different questions concerning one specific topic 'Michael Jordan'. **Typically, the user will not refer to any specific details from previous dialogues.**"
- **Refinement:** "Users clarify or modify their previous instructions. For instance, users might add more detailed constraints, like specifying the desired output format, or provide feedback to clarify their instructions. This requires the assistant's ability to **keep track of the instruction changes and leverage feedback** to refine its responses."
- **Follow-up:** "Users ask questions that build upon the assistant's last response, often referencing specific details or opinions mentioned in that response. ... This assesses the assistant's capacity to **engage in coherent conversations**."

**Structure:** Expansion = 7 turns/instance (7 different NLP tasks over one shared context document introduced at turn 1). Refinement = 12 turns (two NLP tasks × six increasingly complex instructions; switch at turn 7). Recollection = two sub-tasks (easier: document classification, class labels given turn 1; harder: global instruction following), two sessions × ten turns.

**Follow-up has no single-turn equivalent** and is omitted from Table 3 — by construction it cannot be collapsed to one turn. Worth noting for our design: the most conversational task is the one that *resists* a paired control.

---

## 4. UNIT OF EVALUATION — per-response, mean-aggregated

MT-Eval scores **individual responses** (GPT-4 judge, **1–10** scale, per turn) and reports the **average across turns**. This is **the direct opposite of MT-Bench-101's min-over-turns**, which reported +12 points of human agreement for min vs. mean. Two 2024 benchmarks, explicit disagreement on aggregation — see §13.5.

Exception — Recollection uses **rule-based** evaluation, not GPT-4:
> "We evaluate the global following sub-task in the Recollection task using heuristics and rules (Zhou et al., 2023), calculating the **average number of dialogue turns adhering to the global instruction** and normalizing the result to a maximum score of 10. For the document classification task, we measure the **classification accuracy** directly and normalize it to a full score of 10."

The ideal model is defined gap-wise:
> "A good multi-turn conversational model should demonstrate strong capacity in multi-turn interactions and **exhibit a minimal performance gap between single-turn and multi-turn settings**."

---

## 5. Judge validation — Table 4 (verbatim)

Setup: five annotators (graduate students), 60 randomly selected responses from each of Follow-up, Refinement, Expansion (Recollection excluded — automatic eval) = **180 responses total**. Annotators given the same instructions used for prompting GPT-4. Inter-rater reliability on a separate 20 instances: **Cohen's kappa = 0.58**, "indicated satisfactory agreement."

| Task | Pearson | Spearman |
|---|---|---|
| Refinement | 0.74 | 0.58 |
| Expansion | 0.67 | 0.65 |
| Follow-up | 0.72 | 0.70 |
| **Avg.** | **0.71** | **0.64** |

> "GPT-4 ratings have an average **Spearman correlation of 0.64** and a **Pearson correlation of 0.71**."

**Calibration note:** 0.64 Spearman is far more sober than MT-Bench-101's "87% agreement" headline (different metric, not directly comparable). Human-human kappa of **0.58** caps how high any judge-human correlation could plausibly go — the judge agrees with humans about as well as humans agree with each other.

---

## 6. Main multi-turn results — Table 2 (verbatim)

| Model | Avg. | Recollection | Expansion | Refinement | Follow-up |
|---|---|---|---|---|---|
| GPT-3.5-Turbo | 7.72 | 6.90 | 7.87 | 6.92 | 9.21 |
| ChatGLM3-6B | 5.49 | 2.92 | 5.90 | 4.73 | 8.39 |
| Qwen-chat-7B | 6.55 | 5.25 | 7.02 | 5.47 | 8.49 |
| Vicuna-7B-v1.5 | 6.44 | 5.45 | 6.70 | 5.31 | 8.31 |
| Llama-2-chat-7B | 6.11 | 3.86 | 5.87 | 6.20 | 8.53 |
| Mistral-Instruct-7B | 7.46 | 7.22 | 6.98 | 6.58 | 9.05 |
| Vicuna-13B-v1.5 | 7.01 | 6.27 | 6.70 | 6.37 | 8.68 |
| Llama-2-chat-13B | 6.31 | 3.66 | 6.37 | 6.37 | 8.82 |
| Qwen-chat-14B | 7.26 | 6.21 | 7.58 | 6.11 | 9.12 |
| Mixtral-Instruct-8x7B | 7.47 | 6.17 | 7.42 | 6.77 | 9.52 |

> "**All models achieve an average score lower than 8** ... most models perform worst in the **Recollection** task, failing to obey the global instruction stated initially in successive turns. All models also perform poorly in the **Refinement** task, often ignoring constraints"

Recollection is hardest (ChatGLM3-6B **2.92**, Llama-2-chat-13B **3.66**); Follow-up easiest for everyone (8.31–9.52). **Memory over distance breaks; local coherence is nearly solved.**

---

## 7. SINGLE-TURN vs MULTI-TURN — Table 3 (the key table)

ST = single-turn, MT = multi-turn. Bracketed = ST→MT change. Follow-up omitted (no single-turn equivalent).

| Model | ST Avg. | MT Avg. | Recoll. ST | Recoll. MT | Expan. ST | Expan. MT | Refine. ST | Refine. MT |
|---|---|---|---|---|---|---|---|---|
| GPT-3.5-Turbo | 8.07 | 7.23 **(-0.84)** | 8.75 | 6.90 | 8.39 | 7.87 | 7.08 | 6.92 |
| ChatGLM3-6B | 5.71 | 4.52 **(-1.19)** | 5.05 | 2.92 | 7.20 | 5.90 | 4.89 | 4.73 |
| Vicuna-7B-v1.5 | 6.31 | 5.82 **(-0.49)** | 6.35 | 5.45 | 6.99 | 6.70 | 5.60 | 5.31 |
| Llama-2-chat-7B | 7.21 | 5.31 **(-1.90)** | 7.26 | 3.86 | 7.36 | 5.87 | 7.00 | 6.20 |
| Qwen-chat-7B | 6.86 | 5.91 **(-0.95)** | 7.17 | 5.25 | 7.46 | 7.02 | 5.96 | 5.47 |
| Mistral-Instruct-7B | 7.69 | 6.93 **(-0.76)** | 8.47 | 7.22 | 7.60 | 6.98 | 7.00 | 6.58 |
| Vicuna-13B-v1.5 | 7.10 | 6.45 **(-0.65)** | 6.98 | 6.27 | 7.67 | 6.70 | 6.66 | 6.37 |
| Llama-2-chat-13B | 7.55 | 5.47 **(-2.08)** | 7.51 | 3.66 | 7.86 | 6.37 | 7.29 | 6.37 |
| Qwen-chat-14B | 7.62 | 6.64 **(-0.98)** | 8.40 | 6.21 | 7.90 | 7.58 | 6.58 | 6.11 |
| Mixtral-Instruct-8x7B | 8.28 | 6.78 **(-1.50)** | 7.86 | 6.17 | 9.50 | 7.42 | 7.48 | 6.77 |

**Every single model degrades.** Range **-0.49** (Vicuna-7B-v1.5) to **-2.08** (Llama-2-chat-13B) on a 10-point scale. Worst single-task collapses: **Llama-2-chat-13B Recollection 7.51 → 3.66 (-3.85)**; **Llama-2-chat-7B Recollection 7.26 → 3.86 (-3.40)**.

> "most models exhibit a **substantial decline** ... This performance gap therefore serves as a **valuable indicator of a model's multi-turn capabilities**. Notably, the observed gap between the two scenarios **does not appear to be directly correlated with the fundamental capabilities of the models**. For instance, while **Llama-2-chat models outperform Vicuna models in the single-turn setting, they noticeably lag in multi-turn dialogues**. This observation underscores the importance of including multi-turn evaluation"

**⭐ The rank inversion, now with numbers:** Llama-2-chat-13B beats Vicuna-13B-v1.5 single-turn (**7.55 vs 7.10**) but *loses* multi-turn (**5.47 vs 6.45**). **A single-turn leaderboard ranks these two backwards.** This exactly mirrors MINT's claude-2 vs claude-instant-1 inversion (26.4 vs 12.1 at k=1 → 39.9 vs 45.9 at k=5). Two independent papers, same structural finding.

---

## 8. TURN-DEPTH / DISTANCE DEGRADATION

### 8.1 Long-distance retrieval (verbatim)
> "LLMs often underperform in tasks requiring information from earlier dialogue turns. In the Recollection task, **all LLMs struggle to adhere to the initial global instructions as the conversation length, i.e., distance from their initial instruction, increases.**"

### 8.2 Table 5 — first six turns vs last six turns (Refinement)
> "most models perform better on the first task (i.e., the first six turns) compared to the second (i.e., the final six turns), as the turns in the second task are further from the given document at the beginning."

| Model | First | Second | Difference |
|---|---|---|---|
| GPT-3.5-Turbo | 6.98 | 6.85 | **-0.12** |
| ChatGLM3-6B | 5.25 | 4.21 | **-1.03** |
| Vicuna-7B-v1.5 | 5.40 | 5.21 | **-0.19** |
| Llama-2-chat-7B | 6.97 | 5.42 | **-1.55** |
| Qwen-chat-7B | 5.80 | 5.13 | **-0.67** |
| Mistral-Instruct-7B | 6.53 | 6.62 | **+0.09** |
| Vicuna-13B-v1.5 | 6.62 | 6.12 | **-0.50** |
| Llama-2-chat-13B | 6.99 | 5.74 | **-1.25** |
| Qwen-chat-14B | 6.30 | 5.92 | **-0.38** |
| Mixtral-Instruct-8x7B | 6.90 | 6.63 | **-0.26** |

**9 of 10 models degrade in the back half** (Mistral-Instruct-7B the lone exception, +0.09). A clean turn-index effect measured at *identical task difficulty*.

### 8.3 Figure 3 — Refinement across turns (verbatim caption)
> "Performance across turns in Refinement task. Each dialogue has two NLP tasks with each task comprising six increasingly complex instructions. The transition to the second NLP task occurs at the seventh turn as denoted by the grey dashed line. **The performance of all models declines as more instructions are added.**"

Axes: Turn 1–11 (ticks 1,3,5,7,9,11), Score 4–9, all 10 models. **Per-turn data points are NOT in the extracted text — do not quote per-turn values without pulling from the GitHub repo.** The caption claim is verbatim and quotable.

### 8.4 Table 8 — turn 5 vs turn 10 (the hardest turn-index numbers in the paper)

Classification accuracy under manipulated dialogue history. RC(5)/RC(10) = performance at turn 5 and turn 10.

| Model | Gold | DGC | SGC | RC | RC (5) | RC (10) | ST |
|---|---|---|---|---|---|---|---|
| Vicuna-13B-v1.5 | 81.00 | 84.00 | 70.00 | 45.00 | **62.00** | **28.00** | 75.00 |
| Qwen-chat-14B | 94.00 | 95.00 | 86.00 | 69.00 | **68.00** | **60.00** | 94.00 |
| Mistral-Instruct-7B | 96.00 | 95.00 | 95.00 | 75.00 | **80.00** | **70.00** | 94.00 |
| Mixtral-Instruct-8x7B | 95.00 | 95.00 | 94.00 | 57.00 | **60.00** | **54.00** | 88.00 |

(Gold: random documents with correct labels. DGC: Diverse Gold Class — excludes documents sharing current turn's label. SGC: Single Gold Class — documents from one random category. RC: Random Class — random labels. ST: single-turn, no dialogue context.)

> "the **performance at the 10th turn is even worse than the 5th turn, indicating the presence of error propagation**."

**Turn 5 → turn 10: Vicuna-13B -34 pts (62→28), Mistral -10, Qwen -8, Mixtral -6.** Vicuna at turn 10 (**28.00**) is **less than half its single-turn accuracy (75.00)**.

> "Contrary to previous findings (Min et al., 2022), the **Random Class setting significantly reduces performance**."

A corrupted history actively poisons later turns — and the poisoning *compounds* with depth. Also: "dialogue history limited to a single class can negatively impact weaker models, suggesting that **biased examples may be harmful**."

---

## 9. Error analysis (§4.5) — why multi-turn fails

Method: four top models; the ten responses with the largest ST/MT score difference per model per task = **160 responses analyzed**.

> "**80 responses (50%)** did not comply with earlier instructions, **77 responses (48.1%)** were misdirected by the errors accumulated in the earlier context, and **3 instances (1.9%)** were attributed to evaluation errors."

**⚠️ Internal inconsistency in the paper:** the prose says 48.1% / 1.9%, but the subsection headers read **"Error Propagation (48.8%)"** and **"Evaluation (1.2%)"**. The raw counts (80/160 = 50.0%, 77/160 = 48.1%, 3/160 = 1.9%) support the **prose**. **Cite 48.1% / 1.9%; treat the header values as a typo.**

**Noncompliance with Earlier Instructions (50%):**
> "Mixtral-Instruct-8x7B, despite its strong performance in other multi-turn tasks, struggles to follow many global instructions, such as formatting responses as JSON. Our case studies also show that **LLMs often forget previous instructions**."
> "**All models encounter difficulties with counting-related instructions**"

**Error Propagation (~48%):**
> "Accumulated errors from preceding dialogue turns often confuse the models... **The models persist in fulfilling new instructions based on this incorrect paragraph, which further accumulate errors and result in consistently low scores throughout the dialogue.**"

**Evaluation (~2%):** "GPT-4 occasionally misinterprets instructions... primarily surfaces in the Refinement task."

**Read-through: ~98% of the multi-turn gap is real model failure; only ~2% is judge error.** It splits ~50/50 between *forgetting the instruction* and *compounding an early mistake* — both conversation-level failure modes invisible to per-response scoring on a fresh context.

---

## 10. Ablation: Gold vs Self-Predicted Context — Table 7

| Model | Recoll. Predicted | Recoll. Gold | Expan. Predicted | Expan. Gold | Refine. Predicted | Refine. Gold |
|---|---|---|---|---|---|---|
| Mistral-Instruct-7B | 5.25 | **7.29** | 6.98 | 7.02 | 6.58 | **7.38** |
| Vicuna-13B-v1.5 | 4.64 | **7.32** | 6.70 | 6.87 | 6.37 | **7.15** |
| Qwen-chat-14B | 4.43 | **7.00** | 7.58 | 7.63 | 6.11 | **6.95** |
| Mixtral-Instruct-8x7B | 3.21 | **7.11** | 7.42 | 7.47 | 6.77 | **7.17** |

> "models conditioned on gold context exhibit **significant improvement** in Recollection and Refinement. We attribute this performance gap to two factors. Firstly, **using gold context prevents the error propagation from earlier turns**. Secondly, **the gold responses serve as in-context examples**... Notably, using gold responses in the Expansion task yields only a **slight improvement**. This is likely because each dialogue turn in this task is a distinct NLP task, thus not benefiting from these examples of other tasks."

**Recollection gaps are enormous: Mixtral 3.21 → 7.11 (+3.90), Vicuna-13B 4.64 → 7.32 (+2.68), Qwen-14B 4.43 → 7.00 (+2.57).** Expansion barely moves (+0.04 to +0.05) — because its turns are independent. **That's the control that proves the effect is about *dependency between turns*, not context length.**

**Directly corroborates MT-Bench-101's golden-context finding**, but MT-Eval draws the opposite design conclusion: MT-Eval runs main results on **self-predicted context** (realistic); MT-Bench-101 runs on **golden context** + min-aggregation to compensate. For a companion product — where the model always sees its own history — **MT-Eval's setup is the faithful one, and it scores up to 3.9 points lower.**

---

## 11. Impact of Irrelevant Context (position matters) — Table 6

Distracting turns sampled from LMSYS-Chat-1M, inserted at the beginning (Front) or between document and query turns (Between), Refinement task.

| Model | Without | 1 Between | 3 Between | 6 Between | 1 Front | 3 Front | 6 Front |
|---|---|---|---|---|---|---|---|
| Mistral-Instruct-7B | 6.53 | 6.44 | 6.25 | 6.08 | 6.66 | 6.68 | 6.83 |
| Vicuna-13B-v1.5 | 6.62 | 5.91 | 5.47 | 5.56 | 6.25 | 6.16 | 5.89 |
| Qwen-chat-14B | 6.30 | 5.89 | 5.76 | 5.17 | 6.22 | 6.01 | 6.18 |
| Mixtral-Instruct-8x7B | 6.90 | 6.47 | 6.57 | 6.33 | 7.01 | 6.58 | 6.89 |

> "inserting these turns at the beginning results in **mixed outcomes**. Notably, Mistral-Instruct-7B and Mixtral-Instruct-8x7B even show **improved** performance... This suggests that **models are capable of switching topics in a multi-turn dialogue without being affected by previous discussions**. Conversely, **inserting distracting turns between the document and query turns consistently degrades performance**. This further supports that **the increasing distance between the document and the queries negatively impacts performance**"

**Monotone degradation with Between-distance:** Qwen-chat-14B 6.30 → 5.89 → 5.76 → **5.17** (-1.13). Vicuna-13B 6.62 → **5.47** at 3 Between.

**⭐ The cleanest isolation of the mechanism in this whole cluster:** it is not context length and not turn count per se — it is **distance between relevant content and query**. Six irrelevant turns at the *front* cost nothing (some models improve); the *same six turns* placed *between* cost up to 1.13 points. **Turn depth hurts only insofar as it pushes relevant content away.**

---

## 12. Conclusion (verbatim)

> "Our experiment shows a **pronounced gap between single-turn versus multi-turn performance across current models, a phenomenon that persists irrespective of the underlying capabilities of the models**. Our comprehensive analysis reveals that the **distance to relevant content** and **susceptibility to error propagation** are the key factors that cause a decline in multi-turn performance."

---

## 13. Relevance to companion-eval-platform

1. **⭐ Independent corroboration of the central claim of this review — now with the numbers behind it.** MT-Eval (2024, 10 models, EMNLP) reaches the same conclusion as Laban et al. (2025, 15 models, 200k conversations) by a completely different route: **multi-turn degradation is orthogonal to model capability.** Laban: "all models we test exhibit very high unreliability... regardless of aptitude." MT-Eval: "not correlated with the models' fundamental capabilities" — evidenced by Llama-2-13B (ST 7.55 / MT 5.47) losing to Vicuna-13B (ST 7.10 / MT 6.45) *only* in multi-turn.
   ⇒ **You cannot predict multi-turn behavior from single-turn benchmarks. This is the commercial thesis of the platform, now stated three times independently (MT-Eval, Laban, MINT).**

2. **The paired single-turn control is now a third/fourth vote** (with Laban's `Concat`/`Full` and Multi-IF's turn-1 baseline) for building a flattened single-turn control into our design. It is the field-standard way to prove a failure is *conversational* rather than *informational*. Concrete target: our gap should be reportable per-model in MT-Eval's `-X.XX` form.

3. **"Distance to relevant content" is the named mechanism, and Table 6 isolates it experimentally.** This connects the multi-turn literature directly to the Lost-in-the-Middle positional literature — they are the same mechanism in two framings, and MT-Eval is the paper that demonstrates it *within a dialogue*. Our fact-recall-by-position surface measures exactly this; **Table 6's Front-vs-Between design is the exact experiment to copy** (hold turn count fixed, vary distance).

4. **"Error propagation" = ~48% of all multi-turn failure**, and it compounds with depth (RC(5) 62 → RC(10) 28 for Vicuna). This is what Laban calls "premature answer attempts / reliance on previous incorrect answers." Note the tension with He et al.'s self-recovery finding — propagation is observed at the *turn* level even where token-level self-recovery holds. Keep in view for §6.5.4's experiment.

5. **Unresolved tension worth testing on our own data:** MT-Eval scores **per-response, mean-aggregated**; MT-Bench-101 scores per-turn but reports **min-over-turns**, and measured **+12 points of human agreement for min vs mean (87% → 75%)**. These two benchmarks directly contradict each other on aggregation. If MT-Bench-101 is right, MT-Eval's means are *understating* degradation. Worth running both aggregations over our data.

6. **Recollection is the nearest existing analogue to our "forgetting established facts" axis** — a global instruction stated once at turn 1 that must hold for ten turns is structurally identical to a persona/backstory constraint. It is also the hardest task in the benchmark (down to **2.92**), and the one with the largest gold-vs-predicted gap (**+3.90**). Their task design is worth mining directly.

7. **Judge-human ceiling:** 0.64 Spearman / 0.71 Pearson, against human-human kappa 0.58. Sets realistic expectations for LLM-judge reliability on multi-turn dialogue — and matches the DSTC-track ballpark far better than MT-Bench-101's 87% headline.
