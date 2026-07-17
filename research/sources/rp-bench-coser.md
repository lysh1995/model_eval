---
title: "CoSER: Coordinating LLM-Based Persona Simulation of Established Roles"
url: https://arxiv.org/abs/2502.09082
authors: Xintao Wang, Heng Wang, Yifei Zhang, Xinfeng Yuan, Rui Xu, Jen-tse Huang, Siyu Yuan, Haoran Guo, Jiangjie Chen, Shuchang Zhou, Wei Wang, Yanghua Xiao
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# CoSER (arXiv 2502.09082)

**Note on title:** The arXiv landing page title is *"CoSER: A Comprehensive Literary Dataset and Framework for Training and Evaluating LLM Role-Playing and Persona Simulation"* (the running header used throughout the PDF). The paper is also widely cited under the ICML-style title *"CoSER: Coordinating LLM-Based Persona Simulation of Established Roles"* — the GitHub repo README uses this second form. Both refer to the same work. Submitted 13 Feb 2025.

- Code: https://github.com/Neph0s/CoSER
- Models: `Neph0s/CoSER-Llama-3.1-70B`, `Neph0s/CoSER-Llama-3.1-8B` (HuggingFace)
- Data: `Neph0s/CoSER-Books-Gutenberg` (public-domain subset), full processed dataset on HF

## Abstract (VERBATIM)

> Role-playing language agents (RPLAs) have emerged as promising applications of large language models (LLMs). However, simulating established characters presents a challenging task for RPLAs, due to the lack of authentic character datasets and nuanced evaluation methods using such data. In this paper, we present CoSER, a collection of a high-quality dataset, open models, and an evaluation protocol towards effective RPLAs of established characters. The CoSER dataset covers 17,966 characters from 771 renowned books. It provides authentic dialogues with real-world intricacies, as well as diverse data types such as conversation setups, character experiences and internal thoughts. Drawing from acting methodology, we introduce given-circumstance acting for training and evaluating role-playing LLMs, where LLMs sequentially portray multiple characters in book scenes. Using our dataset, we develop CoSER 8B and CoSER 70B, i.e., advanced open role-playing LLMs built on LLaMA-3.1 models. Extensive experiments demonstrate the value of the CoSER dataset for RPLA training, evaluation and retrieval. Moreover, CoSER 70B exhibits state-of-the-art performance surpassing or matching GPT-4o on our evaluation and three existing benchmarks, i.e., achieving 75.80% and 93.47% accuracy on the InCharacter and LifeChoice benchmarks respectively.

## Evaluation dimensions (VERBATIM definitions)

The paper states dimensions were drawn from "conversations from real users and our multi-agent simulations, as well as dimensions from previous work (Shanahan et al., 2023; Shao et al., 2023; Chen et al., 2024a)." Critically: **"Each dimension is assessed in independent LLM requests."** LLM critics receive extra material beyond what actor LLMs see — "the original conversation M and plot summary."

1. **Anthropomorphism**: "Evaluates whether RPLAs behave in a human-like manner, with rubrics covering self-identity, emotional depth, persona coherence, and social interaction."
2. **Character Fidelity**: "Assesses whether RPLAs faithfully portray their characters, with rubrics examining language style, knowledge and background, personality and behavior, and social relationships."
3. **Storyline Quality**: "Evaluates whether the simulated conversation develops naturally, with rubrics focusing on narrative flow and logical consistency."
4. **Storyline Consistency**: "Measures alignment between the simulated conversation M̄ and original dialogue M, i.e., whether RPLAs' reactions (emotions, attitudes, behaviors) remain consistent with the original."

Each dimension is reported on a 0–100 scale.

## Given-Circumstance Acting (GCA)

Two stages:

1. **Multi-agent simulation.** Given a scenario, character profiles, and per-character motivations extracted from the book, LLMs *sequentially portray multiple characters* in the scene. A next-speaker-prediction (NSP) model routes turns (paper uses CoSER 70B for NSP); an environment model (GPT-4o) handles non-character output. The `continue-from` parameter *k* controls how many original turns seed the simulation (set to k=0 in main results).
2. **Penalty-based LLM judging.** Described verbatim:

> Different from previous LLM-as-a-judge methods for RPLA evaluation, our LLM critics: 1) apply penalty-based scoring by identifying role-playing flaws following detailed rubrics, and 2) leverage the original conversation M as reference.

> Specifically, we employ LLM critics to identify flaw instances ℱ in M̄ of specific rubrics, such as "deviate from the original conversation" or "lack initiative and goals", instead of directly outputting a score in previous work (Wang et al., 2024a; Tu et al., 2024). Each flaw f is assigned a severity v_f from 1 (minor) to 5 (severe). The initial score for each dimension is calculated as s = 100 − 5 * Σ_{f∈ℱ} v_f.

The key design move: the critic **enumerates discrete flaw instances with severities** rather than emitting a holistic score. Default critic LLM is **GPT-4o** (footnote: "This paper uses GPT-4o as the critic LLM by default."). The repo pins `gpt-4o-24-08-06` for reproduction.

### Length correction

Longer simulations accrue more flaws mechanically. Fitted bias:

> score = −1.5909 × rounds + 59.0617, which means that for each additional round in the simulation, the score decreases by approximately 1.6 points.

Corrected score (following Dubois et al. 2024 length-debiasing):

> s = 100 − 5 * Σ_{f∈ℱ} v_f + λ|M̄|, where λ is set to 1.5 based on statistical analysis

## Judge–human agreement

CoSER reports **"Alignment (%)"**, not Pearson/Spearman/Kendall. No inter-annotator agreement statistic (no kappa/alpha) is reported. Definition (verbatim):

> The alignment metrics are measured via the frequency of agreement between LLM and human judges when comparing model pairs, excluding cases where judges assign similar scores to both models (i.e., score differences ≤ 1 for human judges or ≤ 5% for automatic metrics).

Table 5 — Alignment (%), with ablations:

| Scoring method | Alignment (%) |
|---|---|
| GCA (GPT-4o) | 68.6 |
| — w/o reference | 64.3 |
| — w/o rubrics | 65.1 |
| — w/o length correction | 64.5 |
| — w/o dimension separation | 65.2 |
| GCA (DeepSeek-V3) | 65.1 |
| **GCA (DeepSeek-R1)** | **77.5** |
| BLEU | 75.3 |
| ROUGE-L | 72.0 |

**Caveat worth flagging:** plain **BLEU (75.3) out-aligns the GPT-4o GCA critic (68.6)**; only the reasoning model DeepSeek-R1 (77.5) beats BLEU. Each ablation costs only ~3–4 points, so no single component (reference, rubrics, length correction, dimension separation) is individually load-bearing. Human evaluation is noted as "highly challenging and time-consuming" at ~15 minutes per model per sample.

Table 11 — scores (%) under different judge LLMs (rank stability check):

| Model | GPT-4o | DeepSeek-R1 | DeepSeek-V3 |
|---|---|---|---|
| GPT-3.5 | 52.8 | 35.9 | 40.5 |
| LLaMA-3.1-8B | 51.8 | 37.2 | 36.8 |
| Abab7-preview | 53.7 | 41.5 | 40.4 |
| CoSER-8B | 56.1 | 44.5 | 45.9 |
| GPT-4o | 58.5 | 48.4 | 46.1 |
| Claude-3.5-Sonnet | 56.2 | 54.8 | 40.7 |
| CoSER-70B | 57.4 | 50.8 | 47.7 |

Absolute scores shift dramatically by judge (GPT-3.5 ranges 35.9–52.8) — only rankings are claimed stable.

## Dataset

- **17,966 characters** from **771 renowned books** (sourced from "Best Books on Goodreads")
- **29,798 authentic conversations**
- **392,298 utterances**
- Hierarchical data model: **plots** (raw text, summary, conversations, character states/experiences) → **conversations** (dialogue transcripts + scenario descriptions + character motivations) → **characters** (profiles, expressions in plots, conversations)
- Rich types: conversation setups, character experiences, **internal thoughts**, thought & action annotations inline in dialogue
- **CoSER Test**: 200 conversations held out from the final 10% of each book — 100 from books used in CoSER training, 100 from unseen books

## Models evaluated

Closed: GPT-3.5, GPT-4o, Claude-3.5-Sonnet, Gemini-1.5-Pro, Abab7-preview, Doubao-pro. Open: LLaMA-3.1-8B/70B, Qwen-2, DeepSeek-V3, Mistral, plus **CoSER 8B / CoSER 70B** (LLaMA-3.1 fine-tunes). External benchmarks used: InCharacter (75.80% acc), LifeChoice (93.47% acc), CharacterEval.

## Multilingual & multi-turn

- **Multi-turn: yes, natively** — this is CoSER's core strength. GCA simulates full multi-turn scenes with multiple RPLAs and an NSP router, not single-turn Q&A.
- **Multilingual: weak / effectively English-only.** The corpus is 771 English-language renowned books. No Chinese split is reported. Chinese-relevant only indirectly (Chinese-developed models like DeepSeek/Qwen/Abab are *evaluated*, and CoSER Test compares against Chinese benchmark CharacterEval). **For a Chinese-language companion platform, CoSER supplies methodology, not data.**

## Limitations (VERBATIM)

> There are several limitations to this study:
>
> First, evaluation via given-circumstance acting still faces challenges related to LLM judges. While the simulation stage effectively elicits RPLA performance, the judging stage still relies on LLM judges. Despite our penalty-based scoring mechanism and detailed rubrics, problems such as length bias persist. Moreover, LLM Judges may lack the necessary knowledge to accurately evaluate character fidelity.
>
> Second, while the dialogues extracted from novels are authentic, their corresponding thoughts remain to be optimized by future work. Character thoughts are often sparse in the original content, and are inferred by LLMs based on limited context. The generated thoughts hardly capture characters' sophisticated thinking processes.
>
> Third, although we've developed comprehensive data representations and curation pipeline to obtain high-quality data, we have not yet addressed the issue of recall in data extraction. Our current dataset may not cover all plots, conversations and characters from the source material. Improving recall is hence an important area for future research.
>
> Fourth, due to copyright concerns, we release only the processed data, not the raw content from the novels. This may hinder future studies aimed to explore the use of raw text for RPLA developments. Our dataset is intended for research purposes only, and we hope our research findings will benefit RPLA developers who respect copyright policies and develop applications with proper licensing.
>
> Finally, our evaluation may be influenced by the varying levels of familiarity that different actor LLMs have with the selected books. While we use renowned novels, we cannot confirm whether a specific LLM has thoroughly learned about a particular book. Therefore, comparing different pre-trained models may not be entirely fair. However, comparing models within the same series would be appropriate.

## Additional criticisms / notes for platform design

- **Contamination is structural.** The last limitation concedes cross-model comparison "may not be entirely fair" because renowned books sit in pretraining data unevenly. CoSER Test's 100-seen/100-unseen split partially probes this.
- **Impact statement:** dataset "intended for research purposes only"; authors do not distribute raw novel content due to copyright; users must "adhere to copyright policies and obtain proper permissions"; applications involving real individuals "must strictly respect personal data privacy."
- **Transferability to companion use:** GCA presupposes a *ground-truth reference dialogue* from a book. Open-ended companion chat has no such reference — the Storyline Consistency dimension and the "leverage the original conversation as reference" critic design do not port directly. Anthropomorphism and Character Fidelity rubrics do port; both are reference-optional.
