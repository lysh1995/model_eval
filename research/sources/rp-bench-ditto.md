---
title: "Large Language Models are Superpositions of All Characters: Attaining Arbitrary Role-play via Self-Alignment (DITTO)"
url: https://arxiv.org/abs/2401.12474
authors: Keming Lu, Bowen Yu, Chang Zhou, Jingren Zhou
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# DITTO (arXiv 2401.12474)

Submitted 23 Jan 2024. Alibaba / Qwen team (OFA-Sys). Published at **ACL 2024** (Long Papers), https://aclanthology.org/2024.acl-long.423/. Code: https://github.com/OFA-Sys/Ditto

**⚠️ Correction to the research brief:** DITTO defines **THREE** core evaluation metrics, not four. Verbatim: *"We design three objective metrics for these three properties respectively."* The three are **Consistent Role Identity**, **Accurate Role-related Knowledge**, and **Unknown Question Rejection**. A plausible source of the "four" figure: the *MT-Bench roleplay subset* is used as a **fourth, external** evaluation alongside the three; also the DITTO benchmark reports **four numeric columns** because Accurate Role-related Knowledge is broken into sub-scores. If you need exactly four scored quantities, it is "3 own metrics + MT-Bench roleplay."

## Abstract (VERBATIM)

> Considerable efforts have been invested in augmenting the role-playing proficiency of open-source large language models (LLMs) by emulating proprietary counterparts. Nevertheless, we posit that LLMs inherently harbor role-play capabilities, owing to the extensive knowledge of characters and potential dialogues ingrained in their vast training corpora. Thus, in this study, we introduce Ditto, a self-alignment method for role-play. Ditto capitalizes on character knowledge, encouraging an instruction-following LLM to simulate role-play dialogues as a variant of reading comprehension. This method creates a role-play training set comprising 4,000 characters, surpassing the scale of currently available datasets by tenfold regarding the number of roles. Subsequently, we fine-tune the LLM using this self-generated dataset to augment its role-playing capabilities. Upon evaluating our meticulously constructed and reproducible role-play benchmark and the roleplay subset of MT-Bench, Ditto, in various parameter scales, consistently maintains a consistent role identity and provides accurate role-specific knowledge in multi-turn role-play conversations. Notably, it outperforms all open-source role-play baselines, showcasing performance levels comparable to advanced proprietary chatbots. Furthermore, we present the first comprehensive cross-supervision alignment experiment in the role-play domain, revealing that the intrinsic capabilities of LLMs confine the knowledge within role-play. Meanwhile, the role-play styles can be easily acquired with the guidance of smaller models.

## Evaluation philosophy (VERBATIM)

DITTO's stated motivation is a rejection of preference-annotation-based RPA evaluation:

> Efficient evaluation for open-ended problems, such as role-play, is significantly understudied. Recent work depends on heavy manual annotations for conducting multifaceted role-play evaluations (Wang et al., 2023c; Shao et al., 2023; Zhou et al., 2023). However, though human evaluation is promising, it is label-intensive and cannot be exactly reproduced, impairing the further development of this field. This work proposes an objective assessment instead of previous preference annotations to evaluate basic role-play capabilities.

Crucially, the eval deliberately **withholds the character profile at test time**:

> During the evaluation, we only provide a brief introduction of the character profile, as shown in Fig. 3, such as "You are Edward III of England, king of England." Such a recipe evaluates whether LLMs can excavate inherent knowledge for role-play.

Framing (verbatim): *"role-play LLMs are expected to have consistent self-awareness, rich role-specific knowledge, and precise knowledge boundary awareness."*

## The three metrics (VERBATIM definitions)

### 1. Consistent Role Identity

> An ideal role-play LLM should seamlessly embody a designated role throughout a multi-turn conversation, maintaining character consistency without deviating. We structure the assessment of role consistency as a multi-choice problem involving four potential role candidates. An additional LLM judger is tasked with discerning the most suitable character from the given options. In essence, if the role-play model successfully emulates the role and manifests the distinct stylistic attributes of the character during the conversation, the selection of the correct role by the judger should be very easy.

**Scoring: accuracy** (4-way multiple choice). The judge sees the conversation with the role name MASKed and picks from 4 candidate character profiles. Elegant reframe — role consistency becomes an *identifiability* test, no rubric needed.

### 2. Accurate Role-related Knowledge

> While fully embodying the identity of the role, we also anticipate the role-play model to accurately convey the knowledge associated with the role, preventing factual errors and hallucinations. However, factual assessment presents substantial challenges, as even advanced LLMs like GPT-4 may be prone to hallucination. Fortunately, through our dialogue-simulating scheme (§3.3), we can acquire the golden knowledge behind each round of role-play dialogue. As depicted in the middle subgraph of Fig. 3, we furnish role-related knowledge as tips to empower a judging LLM to evaluate whether a response appropriately integrates knowledge consistent with the provided evidence.

**Scoring: 1–10 score** from an LLM judge, **grounded on retrieved "Related Evidence" bullets** from Wikipedia/Wikidata. The judge is not asked to know facts — it is handed the evidence. This sidesteps judge hallucination.

### 3. Unknown Question Rejection

> Cognitive boundary reveals whether a model will reject questions that are out of the cognitive boundary of a specific role due to age, era, occupation, etc. A role-play model with a clear cognitive boundary will significantly enhance the immersion. We manually annotate all questions in the test set based on the cognitive boundary of each character. Then, we employ an LLM judger to evaluate whether the model rejects each question. And we can calculate the accuracy of rejections during the conversations.

**Scoring: accuracy** of rejections, against **manual ground-truth annotation** of which test questions fall outside each character's cognitive boundary. Example from Fig. 3: asking Edward III (1312–1377) about the Iraq War → rejection required.

This is the metric with the least coverage elsewhere in the literature and is highly relevant to companion products (a companion persona claiming knowledge it shouldn't have breaks immersion and can mislead).

## Judge model & determinism

> We use GPT-4-turbo as the LLM judger in our evaluation. For each judgment, we set the temperature of OpenAI API to 0.

**No judge–human correlation or inter-annotator agreement is reported anywhere in the paper.** This is a notable gap: DITTO argues its metrics are "objective" and reproducible, and therefore never validates the LLM judger against human raters. Reproducibility ≠ validity. The only human labor is the cognitive-boundary annotation (ground truth), not judge validation.

## Dataset — WIKI ROLE

> Following the methodology outlined in §3.2, we extracted 3,902 characters with profiles in both English and Chinese from Wikidata and Wikipedia for the experiments conducted in this study.

Note the abstract rounds 3,902 → "4,000 characters."

Test set construction (verbatim):

> In order to safeguard against potential biases present in the training data that the model could exploit to deceive evaluations, we utilize GPT-4-Turbo as the base LLM for DITTO to generate a held-out test set. The test set comprises 100 roles that do not overlap with the training set, with each role having its own session, totaling 498 chat turns.

### Table 1 — Dataset statistics (VERBATIM comparison)

| Dataset | Split | Source | Open-source | Multi-lingual | Multi-turn | # Role | # Session | # Turn |
|---|---|---|---|---|---|---|---|---|
| CharacterGLM | — | — | N | N | Y | 250 | 1,034 | 16,316 |
| RoleLLM | Test | — | Y | Y (Zh: 5, En: 95) | N | 100 | — | 23,463 |
| CharacterLLM | — | — | Y | N | Y | 9 | 1,600 | 21,120 |
| **WIKI ROLE** | **Train** | Self-Generated | Y | Y (Zh: 3184, En: 3902) | Y | **3,902** | **7,086** | **36,164** |
| **WIKI ROLE** | **Test** | GPT-4 | | (Zh: 47, En: 53) | | **100** | **100** | **498** |

> The queries in the training set of WIKI ROLE are generated by the seed LLM, while the test set is generated by GPT-4.

## Multilingual & multi-turn

- **Multilingual / Chinese: YES — the strongest Chinese support of the five sources.** Training set is **Zh: 3,184 / En: 3,902** characters; test set is **Zh: 47 / En: 53 roles — i.e., roughly half the benchmark is Chinese.** Profiles sourced from both Chinese and English Wikidata/Wikipedia. The method is explicitly extensible: *"This approach can be readily expanded to encompass additional characters from various Wiki databases and across diverse languages."*
- **Multi-turn: yes.** Test set is 100 roles × 1 session each = 498 chat turns (~5 turns/session). Consistent Role Identity is explicitly defined "throughout a multi-turn conversation." Sessions are shallower than CoSER's or PingPong's.

## Models evaluated

**Seed LLMs for DITTO:** Qwen-Chat 1.8B, 7B, 14B, 72B — note these are *modified*: "downgraded versions of the open-source Qwen-Chat series by removing the role-play capabilities."

**Open-source baselines:** OpenChat-3.5-1210 (Mistral-7B + C-RLFT), Mistral-7B-Instruct-v0.2, Mixtral-7×8B-Instruct-v0.1. *"We exclude some popular open-sourced LLMs due to lacking of support for long sequence length."*

**Proprietary baselines:** Claude 2.1, Wenxin 4.0 (API), GPT-3.5-Turbo, GPT-4, GPT-4-Turbo, Qwen-Max.

**Role-play specialists:** CharacterGLM (66B, API-only — "CharacterGLM has not open-sourced models on all sizes yet, so we can only evaluate it through API"), Tongyi Xingchen (Alibaba Cloud closed platform).

**Training compute:** 32×A100 80G (1.8B/7B/14B), 64×A100 80G (72B); 5 epochs, lr 2e−7, 0.1 warm-up, seq len 8,192.

## Limitations (VERBATIM)

> Although DITTO can empower open-source LLMs role-play capabilities, we also notice the best DITTO model based on Qwen-72B-Chat is still outperformed by advanced chatbots such as GPT-4 and GPT-4-Turbo. However, our training data, though efficiently attained, contains noticeable noise even for DITTO on Qwen-72B-Chat as presented in Fig. 4. So we expect a manual cleaning of the self-generated dialogue simulation will further boost the performance of DITTO.

## Ethics Statement (VERBATIM)

> Role-play LLMs aligned by DITTO may only have minimum safety alignment, so it will probably generate toxic and harmful contents under induction. Therefore, these role-play LLMs are only for research purposes and should be carefully aligned in terms of safety in the future.

Directly relevant to a companion platform: the authors flag that role-play alignment **degrades safety alignment** and that induced toxicity is expected.

## Key finding — cross-supervision (knowledge vs. style)

The paper's most transferable result, from "the first comprehensive cross-supervision alignment experiment in the role-play domain":

> the intrinsic capabilities of LLMs confine the knowledge within role-play. Meanwhile, the role-play styles can be easily acquired with the guidance of smaller models.

**Style is cheap to teach; knowledge is not.** A small model can supervise role-play *style* into a large model, but role-specific *knowledge* is bounded by the student's own pretrained knowledge — no amount of supervision from a stronger teacher lifts it. For an eval platform this argues for scoring style-fidelity and knowledge-fidelity as **separate dimensions**, since they have different ceilings and different fixes.

## Criticisms / notes for platform design

- **No judge validation.** "Objective" here means *reproducible and automatable*, not *human-validated*. Zero correlation numbers.
- **Test set generated by GPT-4** while models under test include GPT-4 and GPT-4-Turbo — a self-favoring setup the paper does not control for.
- **Modified baselines.** The Qwen-Chat seeds are role-play-ablated variants, not the public checkpoints, so "Qwen-Chat" rows are not comparable to published Qwen numbers.
- **Adopt-worthy:** the 4-way-identification framing of Consistent Role Identity (cheap, rubric-free, hard to game) and evidence-grounded knowledge judging both port cleanly to companion characters. Unknown Question Rejection needs per-character boundary annotation — expensive but high-value for personas with defined eras/occupations.
