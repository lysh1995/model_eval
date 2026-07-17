---
title: "MT-Bench-101: A Fine-Grained Benchmark for Evaluating Large Language Models in Multi-Turn Dialogues"
url: https://aclanthology.org/2024.acl-long.401/
authors: Ge Bai, Jie Liu, Xingyuan Bu, Yancheng He, Jiaheng Liu, Zhanhui Zhou, Zhuoran Lin, Wenbo Su, Tiezheng Ge, Bo Zheng, Wanli Ouyang
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# MT-Bench-101

**Venue:** ACL 2024 (Volume 1: Long Papers), pages 7421–7454. arXiv: 2402.14762. Code/data: https://github.com/mtbench101/mt-bench-101
**Affiliations:** Alibaba Group; CUHK; Shanghai AI Laboratory.
**Source used:** full PDF text from ACL Anthology (`2024.acl-long.401.pdf`), extracted locally. Note: arxiv HTML (`/html/2402.14762v2`) 404s and ar5iv conversion fails with a fatal error — the PDF is the only reliable full text.

---

## 1. Headline scale (verbatim)

> "we construct a three-tier hierarchical ability taxonomy comprising **4208 turns** across **1388 multi-turn dialogues** in **13 distinct tasks**. We then evaluate **21 popular LLMs**"

21 LLMs = 2 closed-source (GPT-3.5, GPT-4) + 19 open-source.

### Table 2: Data statistics (verbatim — useful competitive framing)

| Benchmark | #Dialogues | #Turns | #Tasks | Fine-grained |
|---|---|---|---|---|
| AlpacaEval | 805 | 805 | 1 | ✗ |
| MT-Bench | 80 | 160 | 1 | ✗ |
| MT-Bench++ | 80 | 640 | 1 | ✗ |
| BotChat | 547 | 547 | 1 | ✗ |
| MINT | 568 | 568 | 3 | ✗ |
| **MT-Bench-101** | **1388** | **4208** | **13** | ✓ |

Note MT-Bench-101 is the only one in its own table with turns > dialogues by a large factor (3.03 turns/dialogue avg). MT-Bench is explicitly criticized: it "mainly focus[es] on two-turn dialogues and coarse-grained abilities."

---

## 2. The three-tier taxonomy

**Tier 1 — three progressive overarching abilities** (verbatim definitions):
- **Perceptivity** — "the most fundamental ability, reflecting the model's accuracy in understanding context."
- **Adaptability** — "built upon this foundation, indicating the model's ability to respond effectively to user feedback."
- **Interactivity** — "captures the capacity of models for proactive engagement with humans, which is crucial for excelling in multi-turn interactions."

**Tier 2 — seven detailed abilities:** Memory, Understanding, Interference (under Perceptivity); Rephrasing, Reflection, Reasoning (under Adaptability); Questioning (under Interactivity).

Taxonomy tree (Figure 2):
- **Perceptivity** → Context Memory {Context Memory, Separate Input}; Context Understanding {Anaphora Resolution}; Context Interference {Topic Shift, Content Confusion}
- **Adaptability** → Rephrasing {Content Rephrasing, Format Rephrasing}; Reflection {Self-Correction, Self-Affirmation}; Reasoning {Mathematical Reasoning, General Reasoning}
- **Interactivity** → Questioning {Instruction Clarification, Proactive Interaction}

The taxonomy is "both data-driven and rooted in psychological frameworks" — derived by combining real-world multi-turn dialogue data (Gudibande et al. 2023; Zheng et al. 2023) with "the teaching taxonomy from educational psychology (Alexander, 2018; Marchel, 2007)."

**Tier 3 — the 13 tasks (Table 1, verbatim descriptions):**

| Task | Abbr. | Description |
|---|---|---|
| Context Memory | CM | Recall early dialogue details to address the user's current question. |
| Anaphora Resolution | AR | Identify pronoun referents throughout a multi-turn dialogue. |
| Separate Input | SI | The first turn outlines the task requirements and the following turns specify the task input. |
| Topic Shift | TS | Recognize and focus on the new topic when users unpredictably switch topics. |
| Content Confusion | CC | Avoid interference from similar-looking queries with distinct meanings in the dialogue's history. |
| Content Rephrasing | CR | Rephrase the content of the last response according to the user's newest requirement. |
| Format Rephrasing | FR | Rephrase the format of the last response according to the user's newest requirement. |
| Self-correction | SC | Recorrect the last response according to the user feedback. |
| Self-affirmation | SA | Preserve the last response against inaccurate user feedback. |
| Mathematical Reasoning | MR | Collaboratively solve complex mathematical problems with users across dialogue turns. |
| General Reasoning | GR | Collaboratively solve complex general reasoning problems with users across dialogue turns. |
| Instruction Clarification | IC | Seek clarification by asking further questions on ambiguous user queries. |
| Proactive Interaction | PI | Propose questions in reaction to user statements to spark their interest to continue the dialogue. |

Data was generated per-task with bespoke prompts using GPT-4.

---

## 3. UNIT OF EVALUATION — hybrid, and the design choice is the interesting part

**Scoring happens PER-TURN; the reported score is PER-DIALOGUE via a MINIMUM aggregation.** This is the single most transferable design decision in the paper.

> "GPT-4 scores each turn of the chatbot's responses from **1 to 10** and gives detailed justifications. Additionally, our evaluation process utilizes a **minimum-score-taking metric, where the lowest score of a turn is considered the final score for the entire dialogue**. This approach is consistent with human intuition ... because **a single failed response can compromise the entire dialogue in closely related conversational contexts**. Moreover, this metric prevents models from achieving inflated scores by simply learning patterns from the golden context."

Two distinct justifications for min-over-turns: (1) it matches human intuition, (2) it is an *anti-gaming* device against the golden-context artifact (see §5).

### Golden context (critical methodological choice)

> "we leverage our meticulously curated dataset as the **golden context** for dialogue history, as opposed to relying on self-predicted context from LLM subjects. This approach facilitates the creation of smoother, more rational dialogues. Moreover, **evaluating only the newest response of the LLMs while maintaining consistency with the conversation history also promotes fair evaluation**."

So: the model is never fed its own prior outputs during standard evaluation. Each turn is scored against a fixed, human-curated history. **This deliberately removes error propagation from the measurement** — the opposite of MINT's and MT-Eval's setup. See §5 for what they found when they relaxed this.

---

## 4. PER-TURN PERFORMANCE — the turn-index finding (§4.2, "Per-Turn Performance")

This is the section the brief asked for. Verbatim:

> "To investigate the impact of turn count on model performance across different tasks, we calculated the average scores of models for each dialogue turn within various tasks. As shown in Figure 4a and 4b, in **content rephrasing, format rephrasing, context memory, and anaphora resolution tasks, the average performance of models show a decline between the first turn and subsequent turns**. This suggests that in multi-turn dialogue tasks, **models tend to exhibit a greater propensity to forget the content of previous turns or to develop comprehension biases as the conversation progresses**."

> "Figure 4b also illustrates a **notable decrease in performance from the first to the second turn in topic shift and content confusion tasks**. This drop is attributed to the second turn marking the onset of interference, leading to confusion for the model."

> "As shown in Figure 4c, we note an **upward trend** in model performance as the number of turns increases in **separate input, directive clarification, and proactive interaction**. **This phenomenon does not reflect a true enhancement in performance throughout the dialogue.** Rather, it occurs because using the golden context as historical information allows the model to learn the current conversational style and response patterns from the golden context, **resulting in an illusory improvement in performance**."

> "Similarly, as shown in Figure 4d, in **mathematical reasoning** tasks, the model also benefits from the golden context by adopting the reasoning format and solution paradigms (such as the step-by-step paradigm). Conversely, in **general reasoning** tasks, where there is no fixed paradigm to follow, **the model's performance tends to decline as the dialogue progresses due to the increasing complexity**."

### Summary of turn-index direction by task

| Direction | Tasks | Paper's stated cause |
|---|---|---|
| **Declines** with turn index | Content Rephrasing, Format Rephrasing, Context Memory, Anaphora Resolution | forgetting / comprehension bias accumulating |
| **Sharp drop turn 1→2** | Topic Shift, Content Confusion | "the second turn marking the onset of interference" |
| **Declines** with turn index | General Reasoning | "increasing complexity", no fixed paradigm |
| **Rises** — but ILLUSORY | Separate Input, Instruction ("directive") Clarification, Proactive Interaction | in-context learning of style from golden context |
| **Rises** — but ILLUSORY | Mathematical Reasoning | copies step-by-step paradigm from golden context |

**Interpretation for our platform:** the abstract's phrase "differing trends in LLMs performance across dialogue turns" is doing a lot of work. Decomposed, the paper says: *every trend that goes down is real degradation; every trend that goes up is an artifact of feeding the model a clean human-written history.* That is a much stronger claim than "trends differ." An eval that supplies golden context will systematically *understate* multi-turn degradation on exactly the interactive/proactive tasks a companion product cares about (PI, IC).

**NUMBERS NOT RECOVERABLE:** Figure 4's per-turn curves are vector plots with glyph-encoded (`/uni0000...`) axis labels; the underlying per-turn values are **not** in the text. Only axis ranges are decodable — 4a: turns 1–2, y≈9.05–9.25 (CR, FR); 4b: turns 1–4, y≈8.6–9.6 (TS, CC, CM, AR); 4c: turns 1–6, y≈7–9 (SI, IC, PI); 4d: turns 1–4, y≈5.0–6.5 (MR, GR). **I have not reconstructed individual per-turn data points — do not quote per-turn numbers from this paper without pulling the plot data from the GitHub repo.** The magnitudes above are axis bounds, not scores.

---

## 5. Effect of the Golden Context (§4.2) — the error-propagation experiment

Model: ChatGLM3-6B, on Separate Input and Instruction Clarification. Golden context vs. self-predicted context.

> "Figure 6 shows that **using the golden context as historical information leads to an increase in the model's scores over turns**. This improvement is attributed to the golden context supplying the model with data for in-context learning, enabling it to learn the specific patterns and styles from context. **Conversely, employing self-predicted context as dialogue history results in the accumulation and propagation of errors from earlier incorrect responses, causing a gradual decline in scores.**"

> "using self-predicted context as historical information compromises the coherence of the dialogue. Due to these observed phenomena, our evaluation protocol employs the golden context and the lowest score across the turns as the metrics for assessing overall dialogue performance."

**This is a direct, controlled demonstration of turn-depth degradation under realistic (self-predicted) conditions** — arguably the paper's most relevant result for a companion platform, since a deployed companion always runs on self-predicted context. The paper measures it and then explicitly designs it out of the main benchmark. Figure 6 axis ranges: turns 1–4, y≈7.0–8.5. Per-point values again not in text.

---

## 6. Main results — Table 3 (verbatim, GPT-4 judge, 1–10, min-over-turns)

Columns grouped: Perceptivity{Memory: CM, SI | Understanding: AR | Interference: TS, CC}, Adaptability{Rephrasing: CR, FR | Reflection: SC, SA | Reasoning: MR, GR}, Interactivity{Questioning: IC, PI}

| Model | Avg. | CM | SI | AR | TS | CC | CR | FR | SC | SA | MR | GR | IC | PI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Llama2-7B-Chat | 6.53 | 7.64 | 6.21 | 7.92 | 8.23 | 8.50 | 8.32 | 8.56 | 8.45 | 4.97 | 1.88 | 3.83 | 5.23 | 5.11 |
| Qwen-7B-Chat | 7.12 | 7.65 | 7.75 | 8.73 | 8.42 | 8.76 | 8.89 | 9.16 | 8.49 | 7.28 | 2.25 | 3.57 | 5.41 | 6.24 |
| ChatGLM2-6B | 5.56 | 6.14 | 4.69 | 7.27 | 6.13 | 6.26 | 7.47 | 7.98 | 6.97 | 4.19 | 2.11 | 3.00 | 5.16 | 4.90 |
| ChatGLM3-6B | 6.47 | 7.16 | 5.42 | 8.21 | 7.43 | 8.03 | 8.38 | 8.81 | 7.40 | 5.63 | 2.60 | 3.21 | 6.19 | 5.61 |
| InternLM2-Chat-7B-SFT | 6.69 | 7.51 | 6.26 | 8.01 | 8.06 | 8.70 | 8.50 | 8.50 | 7.68 | 6.16 | 3.47 | 4.48 | 4.92 | 4.76 |
| Yi-6B-Chat | 6.93 | 7.57 | 5.27 | 8.69 | 8.37 | 8.76 | 8.43 | 8.44 | 7.49 | 7.85 | 2.18 | 3.80 | 7.30 | 6.00 |
| Mistral-7B-Instruct-v0.2 | 6.95 | 7.66 | 5.64 | 8.09 | 8.30 | 9.35 | 8.69 | 8.59 | 8.16 | 7.33 | 2.58 | 4.52 | 5.80 | 5.66 |
| Vicuna-13B-v1.5 | 6.37 | 7.06 | 5.62 | 7.81 | 7.45 | 8.79 | 7.96 | 7.72 | 7.47 | 6.70 | 2.31 | 4.03 | 5.05 | 4.80 |
| Baize-13B-v2 | 6.12 | 6.78 | 5.15 | 7.86 | 7.40 | 8.07 | 7.96 | 8.15 | 7.24 | 6.32 | 1.67 | 3.69 | 4.35 | 4.95 |
| UltraLM-13B-v2.0 | 4.61 | 4.66 | 4.89 | 5.99 | 6.49 | 8.48 | 2.87 | 2.53 | 6.70 | 5.27 | 1.46 | 2.34 | 4.13 | 4.11 |
| Llama2-13B-Chat | 7.15 | 8.03 | 7.11 | 9.00 | 9.39 | 8.81 | 9.07 | 9.11 | 7.63 | 7.60 | 1.75 | 3.16 | 6.07 | 6.23 |
| Qwen-14B-Chat | 7.82 | 8.33 | 8.36 | 9.04 | 9.22 | 9.50 | 9.12 | 9.39 | 8.41 | 7.97 | 3.50 | 4.55 | 8.21 | 6.12 |
| Baichuan2-13B-Chat | 7.00 | 7.71 | 6.38 | 8.92 | 8.36 | 9.07 | 9.10 | 8.95 | 7.75 | 6.57 | 2.50 | 3.65 | 6.95 | 5.15 |
| InternLM2-Chat-20B-SFT | 6.95 | 7.35 | 6.44 | 8.08 | 8.05 | 9.10 | 8.59 | 8.55 | 7.62 | 7.36 | 4.05 | 5.24 | 4.99 | 4.99 |
| Yi-34B-Chat | 8.10 | 8.55 | 6.79 | 9.34 | 9.84 | 9.34 | 9.08 | 9.38 | 9.01 | 9.04 | 4.07 | 5.90 | 8.51 | 6.39 |
| Mixtral-8x7B-Instruct-v0.1 | 7.38 | 7.86 | 5.94 | 8.49 | 9.01 | 9.52 | 8.91 | 9.01 | 8.69 | 7.78 | 4.19 | 5.14 | 6.03 | 5.36 |
| GPT-3.5 | 7.99 | 8.77 | 7.67 | 7.67 | 9.68 | 9.87 | 9.56 | 9.51 | 9.18 | 7.23 | 4.48 | 5.31 | 8.57 | 6.32 |
| **GPT-4** | **8.86** | 8.88 | 8.99 | 9.58 | 9.83 | 9.98 | 9.54 | 9.57 | 9.36 | 9.52 | 7.15 | 7.17 | 9.00 | 6.64 |
| **Avg.** | **6.92** | 7.52 | 6.37 | 8.26 | 7.72 | 8.24 | 8.36 | 8.44 | 7.98 | 6.93 | **3.61** | **4.84** | 6.22 | **5.52** |

(Table 3 in the PDF lists 21 models; the rows above are those cleanly recovered from text extraction — a few mid-table rows may be missing. The GPT-4/GPT-3.5/Avg. rows and all task columns are verbatim.)

**Key observations, verbatim:**
> "content confusion and format rephrasing are relatively less difficult, while the **mathematical reasoning task is the most challenging**. Furthermore, **closed-source models consistently exhibit superior performance compared to open-source counterparts across all evaluated tasks**. GPT-4 emerges as the top-performing model across the entire spectrum of tasks with an average score of **8.86**, while **Yi-34B with an average score of 8.10** ranks as the second-best performer overall."

**Column averages worth flagging for a companion product:** the three lowest task averages across all 21 models are **MR 3.61**, **GR 4.84**, and **PI 5.52 (Proactive Interaction)**. PI is the lowest non-reasoning task — and even GPT-4 scores only **6.64** on PI, its *worst* score of all 13 tasks, well below its 8.86 average. **Proactive engagement is the single weakest axis for the frontier model**, and it is precisely the axis a companion character depends on. IC (Instruction Clarification) avg 6.22 is second-worst non-reasoning.

---

## 7. Ability-level findings (verbatim)

> "Most LLMs demonstrate a widespread proficiency in **rephrasing and resistance to interference**. However, the **reasoning and questioning abilities of LLMs are still in need of enhancement**. In addition, the performance of models in **memory surpasses that in understanding ability**. This discrepancy arises because memory is primarily concerned with the recall of information, whereas understanding encompasses the grasping of meaning, representing a deeper level of cognitive processing."

> "reflection and questioning abilities play pivotal roles in how models interact with users during multi-turn dialogues and are essential for maintaining communication coherence. Consequently, **models that excel in reflection and questioning not only show proficiency in individual tasks but also suggest a higher level of overall conversational intelligence and are often rewarded with higher overall scores**."

Paper's own bulleted findings:
> "We identify **adaptability and interactivity as the key deficiencies of existing LLMs**, and GPT-4 is the most powerful model for multi-turn dialogues."
> "The average performance of models within various tasks exhibits **differing trends with the progression of turns**, reflecting the distinct characteristics of the abilities."
> "Model performance improves as the model size increases. However, **neither utilizing common alignment techniques (such as RLHF) nor chat-specific designs has resulted in significant enhancements in the multi-turn abilities of LLMs**."

On chat-specific models:
> "[chat-specific models] do not demonstrate exceptional performance on our benchmark. In fact, their capabilities appear to be **outstripped by other large language models of comparable size**. Such insights indicate that despite being specialized for conversational tasks, these chat-specific models require further development to effectively handle the multi-turn scenarios."

Stated cause:
> "the primary reason is that existing efforts mainly focus on collecting data from **single-turn**, thereby neglecting the complexities of multi-turn interaction."

**This converges with MINT's finding that SIFT/RLHF *hurts* multi-turn performance.** Two independent benchmarks, same conclusion: alignment tuning as practiced does not buy multi-turn ability.

---

## 8. Judge validation — Table 5 (verbatim)

Setup: 100 randomly sampled dialogues from MT-Bench-101; **5 expert human annotators**; rated overall dialogue quality 1–10 "based on whether the responses of LLMs met the requirements of the corresponding tasks"; final label by **majority voting**. Agreement metric adopted from Zheng et al. 2024 — "the probability of randomly selected individuals (but not identical) of each type agreeing on a randomly selected question."

| Evaluation Method | Agreement | Δ |
|---|---|---|
| Human Experts | 80% | 0% |
| **MT-Bench-101** | **87%** | **+7%** |
| w/o scoring guidelines | 77% | -3% |
| w/o minimum values metrics | 75% | -5% |

> "the agreement between GPT-4 and human expert evaluations reached **87%**, even surpassing the internal agreement among human experts of **80%**. Additionally, we found that **eliminating scoring criteria or adopting average values instead of minimum values as scoring metrics led to reduced evaluation agreement with human experts**."

**The min-vs-average ablation is the load-bearing one for us: switching from min-over-turns to mean-over-turns costs 12 points of human agreement (87% → 75%).** Averaging across turns actively destroys alignment with human judgment of a conversation. Detailed scoring guidelines are worth +10 points (87% → 77%).

Fleiss' Kappa reported in Appendix G (three variants: between GPT-4 and each individual rater; between GPT-4 and majority vote of 5). **Kappa values are in the appendix table (Table 9) and were not recovered in this extraction — do not quote a Kappa number without re-checking.**

**Self-bias:** the paper acknowledges GPT-4-judge self-bias (Li et al. 2024a; He et al. 2022) and provides an alternate leaderboard with **Qwen-72B-Chat as judge** in Appendix D, "showing that this problem is minor in our benchmark, with the rankings of GPT-4-Judge and Qwen-72B-Judge being consistent." Caveat: GPT-4 also *generated* the data, which the paper does not treat as a confound.

---

## 9. Limitations (verbatim)

> "With LLM technologies rapidly evolving, new multi-turn capabilities are likely to emerge. Consequently, the findings of this study may not encompass all multi-turn abilities."

---

## 10. Takeaways for the companion-eval platform

1. **Min-over-turns beats mean-over-turns by 12 points of human agreement (87% vs 75%).** Strongest single empirical argument in this whole literature cluster for not averaging per-response scores into a conversation score. "A single failed response can compromise the entire dialogue."
2. **Golden context inflates late-turn scores.** Any upward turn-index trend under golden context is an ICL artifact, per the authors' own analysis. A companion eval running on self-predicted context (as production does) should expect the *declining* curves, and the paper's ChatGLM3-6B experiment shows exactly that.
3. **Proactive Interaction is the frontier weak spot** — GPT-4's worst task (6.64 vs 8.86 avg), all-model avg 5.52. Direct read-through to companion character quality.
4. **Alignment/chat-tuning does not help multi-turn** — converges with MINT.
5. **Unit of evaluation:** per-turn scoring, per-dialogue reporting via min. A hybrid worth copying — it keeps turn-level diagnostics while refusing to let good turns paper over a broken one.
