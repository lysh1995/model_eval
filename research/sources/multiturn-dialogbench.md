---
title: "DialogBench: Evaluating LLMs as Human-like Dialogue Systems"
url: https://arxiv.org/abs/2311.01677
authors: Jiao Ou, Junda Lu, Che Liu, Yihong Tang, Fuzheng Zhang, Di Zhang, Kun Gai (Kuaishou)
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# DialogBench — Evaluating LLMs as Human-like Dialogue Systems

Venue: NAACL 2024. arXiv: 2311.01677.
**Source used: the arXiv PDF full text (2311.01677), text-extracted locally. All numbers below are transcribed from the paper's own tables.**

## VERIFICATION NOTE — instance count

Web-summary sources reported the total instance count as "10,121" and "approximately 10,071." **Both are wrong.** Summing the paper's own Table 1 across the 12 tasks gives **9,811**. The paper never states a total in prose — only the per-task `#Num` column. I have summed it myself and flag it as a derived figure, not a quoted one. **Do not cite "10,121" — it does not appear in the paper.**

Table 1 is captioned "Statistics of 12 dialogue tasks" **without specifying whether it describes the English set, the Chinese set, or both.** The paper says "we report the statistics of DialogBench in Table 1" and elsewhere refers to English and Chinese versions constructed the same way. **The per-language instance counts are therefore NOT separately verifiable from the paper.** Do not claim 9,811 per language or 19,622 total; the paper does not support either.

## Motivation (verbatim)

> "The long-standing goal of dialogue systems is to be human-like enough to establish long-term connections with users. Therefore, there has been an urgent need to evaluate LLMs as human-like dialogue systems."

Directly relevant to a companion platform — this benchmark is explicitly framed around **long-term connection and human likeness**, not task success.

Headline finding (abstract):
> "Our extensive tests on English and Chinese DialogBench of 26 LLMs show that instruction tuning improves the human likeness of LLMs to a certain extent, but most LLMs still have much room for improvement as human-like dialogue systems. Interestingly, results also show that the positioning of assistant AI can make instruction tuning weaken the human emotional perception of LLMs and their mastery of information about human daily life."

## UNIT OF EVALUATION — per-instance multiple-choice over a multi-turn context

**This is a different unit from both FED and USR.** DialogBench is neither per-response quality scoring nor per-conversation quality scoring. It is **per-instance accuracy on a multiple-choice question asked about a multi-turn dialogue context.**

> "To unify evaluation, we follow most existing benchmarks (Li et al., 2023a; Hendrycks et al., 2021; Huang et al., 2023) to adopt multi-choice questions and use accuracy as the evaluation metric. Consequently, an evaluation instance requires LLMs to select the correct answer from candidate options based on the given multi-turn dialogue context for the given test question relevant to the specific task."

Implications for the platform:
- The unit is **discriminative, not generative** — the model *picks* a good response, it doesn't *produce* one. Even the three "Response Generation" tasks (KRG, PRG, MRG) are multiple-choice. **DialogBench measures whether a model can recognize a human-like response, not whether it can write one.** This is a real gap for a companion product, where generation is the product.
- The context is **multi-turn by construction** (mean ~7–9 turns; see below), so it probes comprehension over a conversation — but it produces a **single scalar accuracy per instance**, with no notion of a conversation's overall quality.
- Scored against a **single correct answer**, so it sidesteps the one-to-many problem that motivated USR/FED — by removing generation entirely.

## The 12 tasks (verbatim) and Table 1 statistics

Tasks are grouped under **four evaluation dimensions: Correctness, Coherence, Consistency, Safety.**

> "we refer to the main dimensions that are concerned when evaluating human likeness of open-domain dialogue systems, including coherence, consistency, diversity, and fluency (Mehri and Eskenazi, 2020). Considering that LLMs have made great progress in diversity and fluency, along with having more requirements in correctness and safety (Yuan et al., 2023; Cheng et al., 2023), we refine the evaluation dimensions, including coherence, consistency, correctness, and safety."

(Note the lineage: the dimensions are derived from Mehri & Eskenazi's USR work — the same authors as USR/FED. Diversity and fluency were **dropped** on the assumption LLMs have solved them.)

**Table 1** — "'#Turn' denotes the average dialogue turns. '#Num' denotes the number of instances."

| Task | Abbr. | #Turn | #Num |
|---|---|---|---|
| Knowledge-grounded Response Generation | KRG | 7.41 | 784 |
| Intent Classification | IC | 7.72 | 931 |
| Slot Filling | SF | 7.49 | 879 |
| Emotion Detection | ED | 7.09 | 823 |
| Personality-grounded Response Generation | PRG | 7.16 | 832 |
| Multi-turn Response Generation | MRG | 7.66 | 800 |
| Dialogue Summarization | DS | 9.11 | 738 |
| Commonsense-aware Response Generation | CRG | 7.14 | 709 |
| Dialogue Infilling | DI | 7.68 | 776 |
| Offensive Detection | OD | 8.25 | 802 |
| Dialogue Natural Language Inference | NLI | 6.39 | 882 |
| Relation Classification | RC | 8.56 | 855 |
| **TOTAL (summed, not stated in paper)** | | | **9,811** |

Task→dimension mapping (Figure 2):
- **Correctness:** Slot Filling (closed scenario), Commonsense-aware Response Generation (open scenario), Intent Classification, Knowledge-grounded Response Generation
- **Coherence:** Dialogue Infilling, Multi-turn Response Generation
- **Consistency:** Personality-grounded Response Generation, Relation Classification, Emotion Detection (personalization); Dialogue NLI, Dialogue Summarization (semantics)
- **Safety:** Offensive Detection

(Figure 2's grouping is rendered as a diagram; the mapping above is my reading of the extracted layout and the results-table column grouping in Tables 2/3, which order columns as: Correctness = SF, IC, KRG, CRG | Coherence = DI, MRG | Consistency = PRG, RC, ED, NLI, DS | Safety = OD.)

## Dataset construction — GPT-4 generated

> "For each task, we prompt GPT-4 to generate evaluation instances. Specifically, we design the basic prompt based on widely-used design principles and further eliminate existing biases to generate higher-quality instances."

Rationale for generating fresh data:
> "benchmark must contain new evaluation instances" — to avoid contamination from existing human-human dialogue datasets already in LLM training data.

Prompt design follows Zhao et al. (2023a)'s four key ingredients: **Goal Description, Input Data, Contextual Information, Prompt Style.**

### Three biases mitigated
1. **Domain bias** — "to balance the amount of instances in each domain and ensure that each domain has enough instances." (20 domains; see Figure 6/8.)
2. **Style bias** — mitigated via prompt instruction; ablation below shows this makes the benchmark *harder*.
3. **Position bias** — > "To mitigate position bias, we assign the position of the correct answer among candidate options randomly (Zheng et al., 2023)."

### Data filter
> "The generated evaluation set inevitably contains low-quality instances. Inspired by Zhou et al. (2022), we propose to adopt GPT-4 to filter out low-quality instances. We prompt GPT-4 to check whether the multiple-choice questions are correct. We further retain only those evaluation instances that GPT-4 considers correct. It is mainly based on two assumptions: (1) GPT-4 can serve as a surrogate for humans (Zheng et al., 2023); (2) a correct instance generated by GPT-4 should be answered correctly by itself. Through statistics, the average filtering ratio on the whole evaluation set is 10.08%."

**Methodological caution worth recording:** GPT-4 generates the instances AND filters them AND is then evaluated on them, scoring best of all 26 models (86.06 EN / 81.54 ZH). The filter explicitly *retains only what GPT-4 answers correctly*, which mechanically inflates GPT-4's score. The paper does not address this circularity. **Treat GPT-4's rank-1 position as confounded.**

### Generation parameters
GPT-4 data generation: temperature 1, presence_penalty 0.6, frequency_penalty 0, others default.

## Models evaluated — 26 total

> "we include in total 26 models for evaluation, which could be classified into two categories: (1) Pre-trained LLMs: which mostly come from the LLaMA model variants or are trained from scratch by academia and companies. All pre-trained LLMs are open-sourced LLMs. (2) Supervised instruction-tuning LLMs: which mostly release from the academia and companies. Except for GPT-4 and ChatGPT, the remaining are open-sourced LLMs."

**13 pre-trained:** LLaMA2-70B, LLaMA-65B, Baichuan2-13B, Qwen-7B, Mistral-7B, InternLM-7B, LLaMA2-13B, Baichuan-13B, LLaMA-7B, LLaMA-13B, Chinese LLaMA2-13B, Falcon-7B, MOSS-Moon-003-Base

**13 supervised instruction-tuning:** GPT-4, ChatGPT, Baichuan2-13B-Chat, InternLM-Chat-7B, Qwen-7B-Chat, Mistral-7B-Instruct, ChatGLM2-6B, Baichuan-13B-Chat, LLaMA2-7B-Chat, Vicuna-13B, Chinese Alpaca2-13B, MOSS-Moon-003-SFT, Xwin-LM-7B

(Chinese table lists a slightly different roster: Moss-Moon-003-Base appears in place of Chinese LLaMA2-13B ordering, and the instruction-tuned Chinese table omits InternLM-Chat-7B/Qwen-7B-Chat orderings differently and includes "LLaMA2-Chat-7B", "Baichaun-13B-Chat" [sic], "Xwin-7B". The Chinese instruction-tuned table lists 13 models but the pre-trained Chinese table lists 13 as well.)

Versions: **gpt-3.5-turbo-0613** and **gpt-4-0314**.

## Evaluation method — differs by model type (important)

> "(1) **Pre-trained LLMs:** each option content is independently scored by concatenating it with the instruction along with the given dialogue and question as a prompt and computing the probability of 'option content'. Specifically, we calculate the perplexity of each option content and then choose the label corresponding to the option content with the lowest perplexity as the predicted answer. This evaluation method is consistent with the training method of pre-trained LLMs (i.e., next token prediction), stimulating the optimal performance of LLMs. (2) **Supervised instruction-tuning LLMs:** We regard the given dialogue as the history of chatting between the user and the LLM. In the current interaction turn, we concatenate the instruction, along with the question and all options to form an exact string as the user's question to the LLM, and then the LLM gives the option label. In implementation, we allow LLMs to output at most 256 tokens, and then extract the outputted label as the predicted answer."

**Pre-trained and instruction-tuned scores are therefore not measured the same way** (perplexity-ranking vs. label-emission). Cross-category comparisons are not apples-to-apples.

Evaluation parameters: temperature 0, presence_penalty 0.6, frequency_penalty 0 for ChatGPT/GPT-4; temperature 0, max_new_tokens 256, defaults otherwise for open-source. Hardware: A100 80GB, "an average of 20 minutes to 2 hours on each task."

## Human baseline construction

> "we test the human level in these dialogue tasks. Specifically, we randomly choose 50 evaluation instances for each task and then employ 3 experts to do these questions. Finally, a question is considered correct if at least 2 experts answer it correctly."

**50 instances/task × 12 tasks = 600 instances**, 3 experts, majority-of-3 scoring. Note the human baseline is measured on a **600-instance subsample**, not the full 9,811 — and uses majority voting, which flatters the human number relative to any single annotator. Also: the experts were paid "0.2 to each expert for each instance."

## RESULTS — Table 2: Accuracy on English DialogBench

Column groups: **Correctness** (SF, IC, KRG, CRG) | **Coherence** (DI, MRG) | **Consistency** (PRG, RC, ED, NLI, DS) | **Safety** (OD).

| Type | Model | SF | IC | KRG | CRG | DI | MRG | PRG | RC | ED | NLI | DS | OD | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **Human** | 98.00 | 96.00 | 92.00 | 92.00 | 90.00 | 96.00 | 90.00 | 96.00 | 92.00 | 86.00 | 96.00 | 86.00 | **92.50** |
| Pre-trained | LLaMA2-70B | 84.94 | 65.88 | 66.25 | 62.48 | 44.58 | 51.17 | 30.43 | 58.62 | 57.47 | 67.94 | 77.24 | 46.02 | **59.42** |
| Pre-trained | LLaMA-65B | 84.83 | 63.65 | 62.40 | 54.90 | 43.19 | 46.17 | 21.45 | 47.36 | 59.20 | 41.63 | 70.76 | 47.50 | **53.59** |
| Pre-trained | Baichuan2-13B | 79.31 | 58.95 | 59.50 | 53.73 | 43.34 | 48.50 | 24.93 | 44.60 | 70.00 | 48.09 | 66.90 | 28.18 | **52.17** |
| Pre-trained | Qwen-7B | 69.93 | 59.17 | 63.64 | 56.08 | 42.41 | 51.61 | 20.58 | 52.41 | 56.67 | 45.10 | 63.45 | 44.32 | **52.11** |
| Pre-trained | Mistral-7B | 83.56 | 66.33 | 63.77 | 60.21 | 43.18 | 53.16 | 18.99 | 18.84 | 57.86 | 45.33 | 76.13 | 35.90 | **51.94** |
| Pre-trained | InternLM-7B | 78.74 | 58.50 | 58.95 | 53.73 | 40.09 | 48.28 | 21.45 | 48.05 | 58.13 | 37.44 | 67.86 | 49.66 | **51.74** |
| Pre-trained | LLaMA2-13B | 81.42 | 60.74 | 60.74 | 57.39 | 43.03 | 47.72 | 24.64 | 30.48 | 57.47 | 42.58 | 71.31 | 41.02 | **51.55** |
| Pre-trained | Baichuan-13B | 79.54 | 61.07 | 60.74 | 52.94 | 42.72 | 49.61 | 24.35 | 41.26 | 50.67 | 46.65 | 68.14 | 31.02 | **50.73** |
| Pre-trained | LLaMA-7B | 73.45 | 55.70 | 57.44 | 52.68 | 42.72 | 46.50 | 20.29 | 44.83 | 57.20 | 46.17 | 65.10 | 42.27 | **50.36** |
| Pre-trained | LLaMA-13B | 76.32 | 59.40 | 58.68 | 54.38 | 40.40 | 39.39 | 19.71 | 47.13 | 59.07 | 40.91 | 65.14 | 41.36 | **50.16** |
| Pre-trained | Chinese LLaMA2-13B | 79.43 | 59.84 | 51.71 | 58.43 | 45.67 | 50.39 | 10.10 | 31.72 | 51.53 | 46.17 | 69.66 | 43.64 | **49.86** |
| Pre-trained | Falcon-7B | 75.63 | 57.72 | 54.82 | 47.45 | 39.94 | 42.18 | 15.94 | 40.92 | 55.87 | 40.43 | 62.48 | 37.84 | **47.60** |
| Pre-trained | MOSS-Moon-003-Base | 57.93 | 51.01 | 56.06 | 45.88 | 41.02 | 44.73 | 11.88 | 36.55 | 47.33 | 40.43 | 52.97 | 35.57 | **43.45** |
| Pre-trained | **Avg.** | 77.31 | 59.84 | 59.59 | 54.64 | 42.48 | 47.65 | 20.36 | 41.75 | 56.81 | 45.30 | 67.47 | 40.33 | **51.13** |
| Instr-tuned | GPT-4 | 96.09 | 93.96 | 90.01 | 89.14 | 85.45 | 79.00 | 76.81 | 88.74 | 73.87 | 82.78 | 92.41 | 84.47 | **86.06** |
| Instr-tuned | ChatGPT | 89.43 | 83.89 | 83.88 | 84.55 | 75.35 | 75.22 | 62.83 | 83.91 | 68.53 | 74.04 | 86.62 | 68.75 | **78.08** |
| Instr-tuned | Baichuan2-13B-Chat | 84.37 | 81.43 | 79.06 | 79.08 | 57.43 | 76.14 | 54.99 | 79.47 | 54.80 | 55.02 | 81.66 | 42.73 | **68.85** |
| Instr-tuned | InternLM-Chat-7B | 80.23 | 80.43 | 82.37 | 78.56 | 65.02 | 77.14 | 47.54 | 60.47 | 46.40 | 65.07 | 75.03 | 64.43 | **68.56** |
| Instr-tuned | Qwen-7B-Chat | 84.48 | 79.75 | 80.85 | 79.08 | 65.48 | 77.69 | 39.78 | 59.93 | 20.27 | 58.73 | 81.10 | 58.18 | **65.44** |
| Instr-tuned | Mistral-7B-Instruct | 64.36 | 70.02 | 79.88 | 79.05 | 67.49 | 70.14 | 47.47 | 51.88 | 47.73 | 56.69 | 81.93 | 56.13 | **64.40** |
| Instr-tuned | ChatGLM2-6B | 72.64 | 73.94 | 78.10 | 69.02 | 62.69 | 66.81 | 44.06 | 71.49 | 47.87 | 53.11 | 59.45 | 50.23 | **62.45** |
| Instr-tuned | Baichuan-13B-Chat | 74.37 | 71.48 | 73.42 | 70.20 | 50.93 | 72.48 | 45.22 | 72.64 | 49.07 | 39.71 | 68.14 | 50.23 | **61.49** |
| Instr-tuned | LLaMA2-7B-Chat | 62.86 | 71.81 | 72.04 | 66.54 | 53.72 | 56.38 | 44.35 | 73.33 | 46.00 | 48.68 | 73.93 | 54.20 | **60.32** |
| Instr-tuned | Vicuna-13B | 74.37 | 62.53 | 75.90 | 66.27 | 55.73 | 53.94 | 26.09 | 71.49 | 43.20 | 42.94 | 62.07 | 51.25 | **57.15** |
| Instr-tuned | Chinese Alpaca2-13B | 75.52 | 70.36 | 64.19 | 37.78 | 56.19 | 46.50 | 38.26 | 62.76 | 50.27 | 39.47 | 74.21 | 36.70 | **54.35** |
| Instr-tuned | MOSS-Moon-003-SFT | 40.00 | 47.20 | 58.82 | 45.10 | 41.33 | 52.83 | 24.06 | 53.79 | 22.93 | 38.52 | 49.66 | 50.57 | **43.73** |
| Instr-tuned | Xwin-LM-7B | 48.39 | 52.24 | 46.01 | 42.48 | 33.44 | 37.74 | 26.67 | 56.32 | 22.00 | 30.26 | 52.69 | 31.70 | **40.00** |
| Instr-tuned | **Avg.** | 72.85 | 72.23 | 74.19 | 68.22 | 59.25 | 64.77 | 44.47 | 68.17 | 45.61 | 52.69 | 72.22 | 53.81 | **62.38** |

### English gaps vs human (92.50) — computed from the table
| Model | Overall | Gap vs human |
|---|---|---|
| Human | 92.50 | — |
| GPT-4 | 86.06 | **−6.44** |
| ChatGPT | 78.08 | **−14.42** |
| Baichuan2-13B-Chat (best open-source) | 68.85 | **−23.65** |
| Instruction-tuned Avg. | 62.38 | **−30.12** |
| LLaMA2-70B (best pre-trained) | 59.42 | **−33.08** |
| Pre-trained Avg. | 51.13 | **−41.37** |
| Xwin-LM-7B (worst) | 40.00 | **−52.50** |

**Instruction-tuning delta (English): 62.38 − 51.13 = +11.25 points** on average overall.

## RESULTS — Table 3: Accuracy on Chinese DialogBench

| Type | Model | SF | IC | KRG | CRG | DI | MRG | PRG | RC | ED | NLI | DS | OD | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | **Human** | 96.00 | 96.00 | 96.00 | 94.00 | 90.00 | 94.00 | 96.00 | 96.00 | 94.00 | 86.00 | 98.00 | 84.00 | **93.33** |
| Pre-trained | Baichuan2-13B | 78.81 | 55.37 | 63.18 | 54.71 | 46.12 | 52.63 | 26.98 | 46.87 | 67.21 | 39.10 | 66.94 | 55.23 | **54.43** |
| Pre-trained | Qwen-7B | 80.91 | 61.79 | 63.05 | 60.57 | 42.52 | 54.58 | 27.22 | 56.89 | 59.73 | 22.06 | 69.52 | 44.77 | **53.63** |
| Pre-trained | InternLM-7B | 75.67 | 56.48 | 61.72 | 55.43 | 44.04 | 47.71 | 26.38 | 45.74 | 69.93 | 45.11 | 65.44 | 46.75 | **53.37** |
| Pre-trained | LLaMA2-70B | 81.84 | 59.56 | 67.93 | 56.78 | 47.56 | 43.19 | 27.32 | 24.34 | 69.80 | 39.96 | 44.56 | 56.57 | **51.62** |
| Pre-trained | Mistral-7B | 76.71 | 55.92 | 61.98 | 53.42 | 44.87 | 49.57 | 27.33 | 19.92 | 57.16 | 38.09 | 66.12 | 59.32 | **50.87** |
| Pre-trained | Baichuan-13B | 75.79 | 54.49 | 60.53 | 54.29 | 44.32 | 47.46 | 24.94 | 39.10 | 39.59 | 34.84 | 65.85 | 62.57 | **50.31** |
| Pre-trained | LLaMA2-13B | 74.18 | 53.06 | 61.73 | 51.20 | 43.04 | 45.74 | 28.61 | 20.82 | 55.64 | 35.26 | 59.35 | 56.98 | **48.80** |
| Pre-trained | Moss-Moon-003-Base | 61.82 | 48.06 | 59.87 | 52.43 | 41.41 | 47.20 | 25.90 | 32.96 | 60.54 | 38.85 | 60.27 | 54.80 | **48.68** |
| Pre-trained | Chinese LLaMA2-13B | 72.29 | 55.59 | 61.72 | 53.71 | 43.07 | 47.12 | 25.18 | 33.71 | 55.51 | 22.18 | 65.44 | 44.77 | **48.36** |
| Pre-trained | LLaMA-65B | 75.49 | 55.73 | 62.79 | 50.34 | 43.26 | 42.95 | 21.95 | 15.19 | 68.32 | 41.34 | 39.10 | 56.19 | **47.72** |
| Pre-trained | LLaMA-13B | 62.75 | 51.50 | 58.01 | 42.71 | 44.60 | 44.83 | 28.90 | 13.16 | 57.82 | 39.22 | 56.05 | 55.23 | **46.23** |
| Pre-trained | LLaMA-7B | 62.65 | 49.39 | 58.81 | 42.29 | 45.15 | 44.58 | 27.94 | 13.41 | 35.10 | 40.23 | 55.10 | 55.37 | **44.17** |
| Pre-trained | Falcon-7B | 65.31 | 52.16 | 59.60 | 45.71 | 42.11 | 46.27 | 25.30 | 27.44 | 19.86 | 38.10 | 59.05 | 46.19 | **43.93** |
| Pre-trained | **Avg.** | 72.63 | 54.55 | 61.61 | 51.81 | 44.01 | 47.22 | 26.46 | 29.97 | 55.09 | 36.49 | 59.45 | 53.44 | **49.39** |
| Instr-tuned | GPT-4 | 93.75 | 89.53 | 85.18 | 81.46 | 79.22 | 77.75 | 72.83 | 88.12 | 61.90 | 75.39 | 90.22 | 83.15 | **81.54** |
| Instr-tuned | ChatGPT | 86.10 | 78.58 | 76.69 | 79.15 | 65.53 | 70.72 | 54.05 | 79.82 | 53.12 | 66.10 | 73.70 | 61.50 | **70.42** |
| Instr-tuned | Baichuan2-13B-Chat | 77.65 | 73.09 | 67.15 | 76.71 | 61.50 | 66.69 | 54.56 | 64.04 | 55.80 | 56.52 | 72.24 | 71.33 | **66.44** |
| Instr-tuned | InternLM-Chat-7B | 74.39 | 74.09 | 74.30 | 77.29 | 58.17 | 71.19 | 45.80 | 67.54 | 51.84 | 60.40 | 72.11 | 45.62 | **64.40** |
| Instr-tuned | Qwen-7B-Chat | 74.62 | 73.09 | 65.43 | 76.57 | 62.05 | 65.17 | 48.20 | 66.79 | 49.66 | 49.50 | 74.01 | 57.63 | **63.56** |
| Instr-tuned | ChatGLM2-6B | 68.92 | 65.34 | 67.55 | 67.29 | 60.80 | 63.56 | 45.44 | 53.76 | 48.29 | 39.97 | 66.26 | 56.64 | **58.65** |
| Instr-tuned | Baichaun-13B-Chat [sic] | 74.51 | 66.89 | 52.85 | 69.00 | 56.09 | 63.81 | 45.20 | 46.87 | 49.80 | 45.36 | 62.86 | 50.00 | **56.94** |
| Instr-tuned | Mistral-7B-Instruct | 57.97 | 59.68 | 70.19 | 69.00 | 54.47 | 62.71 | 41.72 | 30.07 | 40.62 | 45.98 | 72.78 | 54.27 | **54.96** |
| Instr-tuned | Vicuna-13B | 59.95 | 45.63 | 40.00 | 62.00 | 44.46 | 44.93 | 31.97 | 30.26 | 42.26 | 32.63 | 61.22 | 37.43 | **44.40** |
| Instr-tuned | Chinese Alpaca2-13B | 57.51 | 52.71 | 37.09 | 52.86 | 50.83 | 28.39 | 22.46 | 45.61 | 41.88 | 48.50 | 53.47 | 20.34 | **42.64** |
| Instr-tuned | LLaMA2-Chat-7B | 42.61 | 40.97 | 54.17 | 49.01 | 36.43 | 43.81 | 26.48 | 23.31 | 28.24 | 31.70 | 45.44 | 50.85 | **39.42** |
| Instr-tuned | MOSS-Moon-003-SFT | 32.48 | 35.44 | 45.30 | 47.14 | 28.53 | 41.61 | 21.17 | 3.26 | 13.51 | 33.21 | 48.57 | 32.77 | **31.92** |
| Instr-tuned | Xwin-7B | 35.04 | 29.90 | 30.60 | 37.14 | 26.32 | 29.49 | 25.30 | 14.29 | 24.42 | 25.94 | 41.36 | 15.54 | **27.95** |
| Instr-tuned | **Avg.** | 64.27 | 60.38 | 58.96 | 64.97 | 52.65 | 56.14 | 41.17 | 47.21 | 43.18 | 47.02 | 64.17 | 49.01 | **54.09** |

### Chinese gaps vs human (93.33) — computed from the table
| Model | Overall | Gap vs human |
|---|---|---|
| Human | 93.33 | — |
| GPT-4 | 81.54 | **−11.79** |
| ChatGPT | 70.42 | **−22.91** |
| Baichuan2-13B-Chat (best open-source) | 66.44 | **−26.89** |
| Instruction-tuned Avg. | 54.09 | **−39.24** |
| Baichuan2-13B (best pre-trained) | 54.43 | **−38.90** |
| Pre-trained Avg. | 49.39 | **−43.94** |
| Xwin-7B (worst) | 27.95 | **−65.38** |

**Instruction-tuning delta (Chinese): 54.09 − 49.39 = +4.70 points** — less than half the English delta (+11.25).

> "The overall score of all LLMs on English DialogBench is slightly better than the score on Chinese DialogBench. Additionally, the overall performance of all LLMs on each task generally has the same trend on English and Chinese DialogBench."

## TURN-DEPTH / SINGLE-TURN vs MULTI-TURN EVIDENCE (critical)

**DialogBench contains NO analysis of accuracy as a function of turn index or dialogue length.** It does not vary turn depth as an experimental condition, does not report accuracy by turn position, and does not compare single-turn against multi-turn performance. Any such claim would be fabricated.

What it does provide on turn depth is **only descriptive**: Table 1's `#Turn` column, the mean dialogue length per task, ranging **6.39 (NLI) to 9.11 (DS)**, most tasks clustering around **7.1–7.7**. All instances are multi-turn by construction — generation prompts specify e.g. "generate a 10-turn (20 utterances) dialogue" and "please generate a two-party dialogue with at least 10 turns (10 turns=20 utterances)." Note the tension: prompts ask for ≥10 turns but the realized means are ~7–9.

**Because every instance is multi-turn and none are single-turn, DialogBench cannot isolate a single-turn vs multi-turn gap.** It holds turn-depth roughly constant (~7–9) rather than varying it. Its contribution to the multi-turn question is that it *requires* multi-turn comprehension to answer at all — not that it measures degradation across depth.

One design detail is turn-depth-adjacent and worth noting: the generation prompt instructs that "The last turn of the dialogue is not the end of the dialogue session" and that the question should require reading "a certain turn to answer" with option information drawn from the dialogue — i.e. instances are built to *require* looking back across turns rather than only at the last one. This makes it a genuine multi-turn-context benchmark even without a depth axis.

**The nearest thing to a depth signal is the per-task pattern:** the two **Coherence** tasks — Dialogue Infilling (DI) and Multi-turn Response Generation (MRG) — are among the weakest for every model class. Pre-trained avg: **DI 42.48, MRG 47.65** (English) vs SF 77.31, DS 67.47. Instruction-tuned avg: **DI 59.25, MRG 64.77**. Even GPT-4 scores **MRG 79.00** — its second-worst English task after ED (73.87) and PRG (76.81) — against a human 96.00, a **−17.00 gap on multi-turn response generation**, versus only −1.91 on Slot Filling (96.09 vs 98.00). Paper's read:

> "For coherence, the average performance of LLMs on dialogue infilling (DI) and multi-turn response generation (MRG) is relatively similar, and there is still much room for improvement."

So: **the tasks that most require sustaining a conversation are the ones with the largest human gaps, while the locally-scoped extraction tasks are near-solved.** This is consistent with (though not the same claim as) FED's and USR's finding that per-response competence overstates conversational competence.

## FINDINGS MOST RELEVANT TO A COMPANION/ROLEPLAY PLATFORM

### 1. Personality-grounded Response Generation (PRG) is the single worst task
This is the task closest to companion/character work — staying in persona.

- Pre-trained avg **20.36** (English) — near or below chance for multiple choice.
- Instruction-tuned avg **44.47** (English), **41.17** (Chinese).
- GPT-4: **76.81** (EN) / **72.83** (ZH) — its **worst English task** other than ED.
- Human: **90.00** (EN) / **96.00** (ZH).
- **GPT-4 gap on PRG: −13.19 (EN), −23.17 (ZH)** — roughly double its overall gap.
- Chinese LLaMA2-13B scores **10.10** on English PRG; Falcon-7B **15.94**; Mistral-7B **18.99**.

> "For personalization consistency, pre-trained LLMs as a whole have good performances in emotion perception (ED), whereas poor performance in personality following (PRG)."
> "For personalization consistency, most LLMs perform unsatisfactorily."

**Persona-following is where models are furthest from human.** This mirrors FED's finding that *Consistent* is the hardest dialog-level quality to measure, and USR's finding that persona-grounded *Interesting* collapses. Three independent papers converge on persona consistency being both hard to do and hard to measure.

### 2. Instruction tuning WEAKENS emotional perception (the paper's headline "interesting" result)

> "Interestingly, most LLMs achieve inferior scores on emotion classification than the corresponding pre-trained LLMs, such as QWen-7B. It might be because the positioning of assistant AI enables instruction tuning to focus on the ability to complete tasks, abandoning the ability to perceive emotions."

Verifiable in the tables — **Emotion Detection (ED)**, base → chat:
- English: pre-trained avg **56.81** → instruction-tuned avg **45.61** = **−11.20**
- Chinese: pre-trained avg **55.09** → instruction-tuned avg **43.18** = **−11.91**
- **Qwen-7B: 56.67 → Qwen-7B-Chat: 20.27 (English) = −36.40**, a collapse.
- Baichuan2-13B: 70.00 → Baichuan2-13B-Chat: 54.80 (English) = **−15.20**
- ED is one of only two English tasks where the pre-trained average (56.81) *beats* the instruction-tuned average (45.61); the other is SF (77.31 vs 72.85).

**This is the most important finding in the paper for a companion product.** RLHF/instruction-tuning toward "helpful assistant" measurably degrades emotional perception — the exact capability a companion character needs. Assistant-alignment and companion-alignment pull in opposite directions on this axis.

### 3. Daily-life knowledge is weaker than professional knowledge

> "We observe that the average performance in daily life is overall lower than that in professional knowledge (e.g., 52.14% vs. 56.07%). We speculate that this is related to the current positioning of supervised instruction-tuning as assistant AI. Assistant AI needs to follow instructions to complete various knowledge-based tasks, which particularly requires LLMs to master a variety of professional knowledge. Correspondingly, information relevant to the daily life of humans might be underestimated when fine-tuning LLMs. This suggests that improving the human-likeness of LLMs as dialogue systems requires introducing more daily dialogues into supervised fine-tuning."

**Daily life 52.14% vs professional knowledge 56.07% = −3.93 points** (averaged over all supervised instruction-tuning LLMs, Figure 8). Domains span 20 categories — daily-life ones include Gourmet Cooking, Travel, Household Chores, Film, Neighborhood, Workplace, Music, Shopping, Games, Sports; professional ones include History, Philosophy, Sociology, Psychology, Economics, Geography, Physics, Biology, Computer Science, Medicine. (Figure 8 is a plot; **per-domain numeric values are not recoverable from the text** — only the 52.14/56.07 aggregates quoted in prose. Detailed results are said to be in Table 8 / Appendix.)

Same root cause as finding #2, and the same lesson: assistant-tuning optimizes away from the conversational register a companion needs.

## Ablation (Table 4) — GPT-4 on Chinese DialogBench

| Method | SF | IC | KRG | CRG | DI | MRG | PRG | RC | ED | NLI | DS | OD | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Optimized Prompt | 93.75 | 89.53 | 85.18 | 81.46 | 79.22 | 77.75 | 72.83 | 88.12 | 61.90 | 75.39 | 90.22 | 83.15 | **81.54** |
| −Styles | 94.26 | 89.79 | 89.95 | 81.80 | 89.39 | 91.03 | 73.51 | 89.22 | 73.43 | 75.42 | 91.32 | 84.55 | **85.31** |
| −Filter | 87.29 | 89.22 | 81.81 | 81.12 | 73.05 | 74.97 | 72.39 | 80.27 | 55.14 | 71.97 | 89.12 | 70.88 | **77.27** |

> "(1) The accuracy improves to varying degrees without mitigating the style bias, which validates that unfriendly communication would greatly increase the difficulty of interaction. (2) The accuracy has dropped to varying degrees, indicating that the filtered instances are indeed incorrect and LLMs cannot answer."

- **−Styles: 85.31 vs 81.54 = +3.77** — removing style-bias mitigation makes the benchmark *easier*. The biggest style-sensitive tasks are **MRG (+13.28: 77.75→91.03)**, **DI (+10.17: 79.22→89.39)**, and **ED (+11.53: 61.90→73.43)**. Note these are the coherence and emotion tasks — **conversational style/register is precisely what makes multi-turn and emotional tasks hard.** Directly relevant: a companion platform's characters must handle unfriendly/varied communication styles, and that is where the difficulty concentrates.
- **−Filter: 77.27 vs 81.54 = −4.27** — but see the circularity caution above; this ablation partly measures "GPT-4 scores worse on items GPT-4 got wrong," which is close to tautological.

## Ethics / annotation notes
> "we employ three experts... We pay 0.2 to each expert for each instance."
The paper notes a risk of "potentially generating toxic and harmful instances" and describes measures against retaining harmful instances.

## Summary comparison to FED / USR

| | USR (2020) | FED (2020) | DialogBench (2024) |
|---|---|---|---|
| Unit of evaluation | **per-response** | **per-response AND per-conversation** | **per-instance MCQ over multi-turn context** |
| Output | quality score (regression) | quality score (follow-up likelihood) | accuracy (correct/incorrect) |
| Generative or discriminative | scores generated text | scores generated text | model selects an option |
| Human correlation reported | Spearman + Pearson | Spearman only | n/a (accuracy vs human baseline) |
| Turn-index analysis | none | none | none |
| Persona/consistency finding | Interesting collapses on PersonaChat (0.0171) | Consistent is worst dialog quality (0.116) | PRG is worst task (GPT-4 −13.19 vs human) |

**None of the three papers measures quality as a function of turn index.** That gap is consistent across the multi-turn evaluation literature represented here, and is worth stating plainly in any survey the platform produces — if turn-depth degradation is a claim the platform wants to make, these three papers do not support it and a different source is needed.
