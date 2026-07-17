---
title: "How Well Can LLMs Echo Us? Evaluating AI Chatbots' Role-Play Ability with ECHO"
url: https://arxiv.org/abs/2404.13957
authors: Man Tik Ng, Hui Tung Tse, Jen-tse Huang, Jingjing Li, Wenxuan Wang, Michael R. Lyu (CUHK)
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# ECHO — Turing-test style evaluation of human-like character agents

**arXiv:** 2404.13957 (submitted 22 Apr 2024). HTML: https://arxiv.org/html/2404.13957v1

> **CORRECTION TO BRIEF:** The task specified arXiv **2404.12726** for ECHO. That ID is a *different* paper — "Evaluating Character Understanding of Large Language Models via Character Profiling from Fictional Works" (Xinfeng Yuan, Siyu Yuan, Yuhan Cui, Tianhe Lin, Xintao Wang, Rui Xu, Jiangjie Chen, Deqing Yang; EMNLP 2024; introduces the **CroSS** dataset). ECHO is **2404.13957**. This file documents ECHO. See the note at the bottom for the 2404.12726 paper, which is separately useful.

> **Relevance:** ECHO is the only source that evaluates simulation of **ordinary people** rather than celebrities/fictional characters — which is exactly the companion use case. Its Turing-test-with-acquaintances protocol is the strongest available construct for "does this feel like a real person." But it is tiny (10 subjects) and single-turn.

## Abstract (VERBATIM)

> The role-play ability of Large Language Models (LLMs) has emerged as a popular research direction. However, existing studies focus on imitating well-known public figures or fictional characters, overlooking the potential for simulating ordinary individuals. Such an oversight limits the potential for advancements in digital human clones and non-player characters in video games. To bridge this gap, we introduce ECHO, an evaluative framework inspired by the Turing test. This framework engages the acquaintances of the target individuals with questions and prompts them to distinguish between human and machine-generated responses. Notably, our framework focuses on emulating average individuals rather than historical or fictional figures, presenting a unique advantage to apply the Turing Test. We evaluated three role-playing LLMs using ECHO, with GPT-3.5 and GPT-4 serving as foundational models, alongside the online application GPTs from OpenAI. Our results demonstrate that GPT-4 more effectively deceives human evaluators, and GPTs achieves a leading success rate of 48.3%. Furthermore, we investigated whether LLMs could discern between human-generated and machine-generated texts. While GPT-4 can identify differences, it was unable to determine which texts were human-produced. Our code and results are available at https://github.com/CUHK-ARISE/ECHO.

*(Note: the fetch tool returned only the first two sentences of the abstract cleanly; the remainder above is reconstructed from the arXiv abstract page and search results and matches the reported findings — the 48.3% GPTs figure and the GPT-4 detection result are confirmed in the body. Treat the middle sentences as high-confidence but re-verify against the PDF if quoting in a publication.)*

**Repo:** https://github.com/CUHK-ARISE/ECHO

## Evaluation dimensions — question categories (VERBATIM names)

ECHO does not score rubric dimensions. Instead it structures the *probe questions* into two families of five categories each. The "dimension" is the question type; the metric is a single deception success rate.

### General Questions (5)
- Creativity Questions (CR)
- Ethical Dilemmas Questions (ED)
- Logical Questions (LG)
- Philosophical Questions (PH)
- Problem-Solving Questions (PS)

### Specific Questions (5)
- In-Depth Personal Questions (IP)
- Emotional Questions (EM)
- Future Prediction Questions (FP)
- Insightful Questions (IS)
- Interest Questions (IT)

General questions are character-independent (anyone could answer); specific questions require knowledge of the individual. This split is the analytic lever — it separates generic conversational competence from genuine person-fidelity.

## How it scores

**Turing test with acquaintances as judges.** Not an LLM judge, not a rubric.

- Metric: **success rate** = "proportion of instances in which human evaluators select an LLM-generated response over that of an actual participant."
- **Baseline for random guessing: 50%.** Rates closer to 50% indicate stronger human-like performance (i.e., evaluators cannot distinguish). Below 50% = detectable as machine.
- Evaluators are **acquaintances of the target individual** — people who actually know the person. This is the key methodological move and the main constraint on scale.
- Background information about each subject is collected in categories and fed to the role-play system.

## Sizes and participants

- **Subjects (target individuals): 10** unique participants — ordinary people, not celebrities.
- **Evaluators: minimum 7 acquaintances per participant.**
- **Questions: 10 per participant** (5 specific, 5 general).
- **Total responses: 800+.**

## Models evaluated

Three role-play methods × two base models, plus one product:

1. **RoleGPT** (GPT-3.5-Turbo, GPT-4-Turbo)
2. **Role-Play Prompting / RPP** (GPT-3.5-Turbo, GPT-4-Turbo)
3. **Juliet** (GPT-3.5-Turbo, GPT-4-Turbo)
4. **GPTs** (OpenAI's custom-GPT application)

**Results:** **GPTs achieves the leading success rate of 48.3%** (closest to the 50% indistinguishable line). GPT-4 more effectively deceives human evaluators than GPT-3.5.

**Secondary experiment — LLM as detector:** GPT-4 *can* identify that differences exist between human- and machine-generated texts, but **cannot determine which texts were human-produced.** → A useful, citable caution about using LLMs to detect their own outputs.

## Inter-annotator agreement / judge-human correlation

**None reported.** No kappa, no alpha, no correlation coefficient. The design uses ≥7 acquaintances per subject and aggregates into a success rate, but does not report agreement among those evaluators. This is a real gap if the protocol is to be borrowed — treat per-evaluator variance as unmeasured.

## Limitations (VERBATIM)

> A primary limitation is that the background information categories may not adequately capture the complexities of a person's identity, experiences, and communication nuances.

> Restricting evaluators to those familiar with the target individual may limit the size and diversity of the evaluation team.

> LLMs fail to replicate the full complexity of human language, emotional depth, and cultural nuances [in short interactions].

Additional structural limitations evident from the design:
- **n=10 subjects** — very small; results are directional, not a leaderboard.
- Recruiting acquaintance-evaluators is the scaling bottleneck; this protocol cannot be run cheaply or continuously.
- Single-turn Q&A, so no test of memory, drift, or long-horizon consistency.

## Multilingual / multi-turn

- **Multilingual: not addressed.** Study is English-only; no Chinese support. No cross-lingual claims.
- **Multi-turn: no.** Single-turn question→response pairs. The limitations explicitly concede "short interactions." This is ECHO's biggest deficit relative to RAIDEN for companion evaluation.

---

## Appendix — the paper actually at arXiv 2404.12726

**"Evaluating Character Understanding of Large Language Models via Character Profiling from Fictional Works"** — Xinfeng Yuan, Siyu Yuan, Yuhan Cui, Tianhe Lin, Xintao Wang, Rui Xu, Jiangjie Chen, Deqing Yang. EMNLP 2024. Repo: https://github.com/Joanna0123/character_profiling

Abstract (VERBATIM):
> Large language models (LLMs) have demonstrated impressive performance and spurred numerous AI applications, in which role-playing agents (RPAs) are particularly popular, especially for fictional characters. The prerequisite for these RPAs lies in the capability of LLMs to understand characters from fictional works. Previous efforts have evaluated this capability via basic classification tasks or characteristic imitation, failing to capture the nuanced character understanding with LLMs. In this paper, we propose evaluating LLMs' character understanding capability via the character profiling task, i.e., summarizing character profiles from corresponding materials, a widely adopted yet understudied practice for RPA development. Specifically, we construct the CroSS dataset from literature experts and assess the generated profiles by comparing them with ground truth references and evaluating their applicability in downstream tasks. Our experiments, which cover various summarization methods and LLMs, have yielded promising results. These results strongly validate the character understanding capability of LLMs.

Why it may still matter: it evaluates the **upstream** step — whether a model can build a good character profile from source material — which is the input to any RPA. Dataset: **CroSS**, built from literature experts. Scoring: comparison to ground-truth reference profiles + downstream task applicability.
