---
title: "PersonaLLM: Investigating the Ability of Large Language Models to Express Personality Traits"
url: https://arxiv.org/abs/2305.02547
authors: Hang Jiang, Xiajie Zhang, Xubo Cao, Cynthia Breazeal, Deb Roy, Jad Kabbara
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# PersonaLLM: Investigating the Ability of Large Language Models to Express Personality Traits

- **arXiv**: 2305.02547 — v1 submitted 4 May 2023; v5 last revised 2 April 2024
- **Venue**: Findings of NAACL 2024
- **Affiliation**: MIT Media Lab / MIT CSAIL

## Abstract (verbatim)

> Despite the many use cases for large language models (LLMs) in creating personalized chatbots, there has been limited research on evaluating the extent to which the behaviors of personalized LLMs accurately and consistently reflect specific personality traits. We consider studying the behavior of LLM-based agents which we refer to as LLM personas and present a case study with GPT-3.5 and GPT-4 to investigate whether LLMs can generate content that aligns with their assigned personality profiles. To this end, we simulate distinct LLM personas based on the Big Five personality model, have them complete the 44-item Big Five Inventory (BFI) personality test and a story writing task, and then assess their essays with automatic and human evaluations. Results show that LLM personas' self-reported BFI scores are consistent with their designated personality types, with large effect sizes observed across five traits. Additionally, LLM personas' writings have emerging representative linguistic patterns for personality traits when compared with a human writing corpus. Furthermore, human evaluation shows that humans can perceive some personality traits with an accuracy of up to 80%. Interestingly, the accuracy drops significantly when the annotators were informed of AI authorship.

## Core idea

The earliest and most foundational of the four. Not a benchmark or platform — a **controlled case study**. It asks a prior question: *can an LLM assigned a personality profile actually express it?* It validates this three ways: (1) psychometric self-report, (2) automatic linguistic analysis, (3) human perception.

**The distinctive contribution is the AI-authorship disclosure experiment** — the finding that telling annotators the text is AI-written *reduces* their ability to perceive personality in it. That is a finding about *human raters*, not about models, and it has direct consequences for how any companion-eval platform runs human evaluation.

## Persona construction

Five binary Big Five dimensions (verbatim):

> (1) extroverted / introverted, (2) agreeable / antagonistic, (3) conscientious / unconscientious, (4) neurotic / emotionally stable, (5) open / closed to experience

- **2⁵ = 32 distinct personality type combinations**
- **10 personas generated per combination** → **320 personas per model**
- Personas induced by prompt ("You are a character who is...")

## Protocol

### 1. BFI test (44-item)

- The persona completes the **44-item Big Five Inventory**.
- Responses strictly formatted as `(x) y`, where `x` = question number and `y` = a 1–5 agreement rating.
- **This is self-report** — note the direct methodological contrast with InCharacter, which argues self-report is invalid for RPAs. PersonaLLM finds self-report *does* recover assigned traits for prompt-assigned personas; InCharacter finds it fails for *fictional characters with canon*. Both can be true: recovering a trait you were just told to have is a much easier task than revealing a character's latent personality.

### 2. Story writing task

- Each persona writes an **800-word personal narrative**.
- Explicit instruction: **"Do not explicitly mention your personality traits in the story."**
- This forces *implicit* trait expression — the story is the artifact scored by LIWC and by humans.

## Scoring methods

Three independent channels — this triangulation is the paper's methodological strength:

1. **Psychometric self-report** — 44-item BFI, scored against assigned type. Statistical test with Cohen's *d* effect sizes.
2. **Automatic linguistic analysis** — **LIWC** (Linguistic Inquiry and Word Count) over the stories, compared against a human writing corpus (Essays/Pennebaker-style).
3. **Human evaluation** — annotators rate stories on 1–5 Likert dimensions and predict the author's Big Five profile.

Note: **no LLM-as-judge anywhere.** This is the only one of the four with zero LLM judging — it uses psychometrics, a validated lexicon tool, and humans.

## Statistical results

### BFI self-report — effect sizes (GPT-4)

All p < .001, all **large** effect sizes:

| Trait | Cohen's d | p |
|---|---|---|
| Extraversion | 5.47 | < .001 |
| Agreeableness | 4.22 | < .001 |
| Conscientiousness | 4.39 | < .001 |
| Neuroticism | 5.17 | < .001 |
| Openness | 6.30 | < .001 |

These are enormous effect sizes (d > 4 is far beyond the conventional d=0.8 "large" threshold) — LLM personas report BFI scores almost perfectly separated by assigned type. Which is arguably unsurprising and is the weakest evidence in the paper: it largely shows the model can follow an instruction it was just given.

### LIWC results

- Significant correlations between assigned traits and linguistic patterns; e.g. **Openness positively correlated with curiosity lexicons** in both GPT-3.5 and GPT-4 personas.
- **GPT-4 aligns far better with human writing patterns than GPT-3.5**: **17/36** overlapping correlations for Openness vs. GPT-3.5's **2/36**.

That 17/36 vs 2/36 gap is the most interesting automatic result — it says model capability improvements show up in *implicit, unprompted* trait expression, not just in self-report compliance.

## Human evaluation

**Setup**:
- **5 annotators** rated **32 GPT-4 stories** (one per personality combination).
- **Six 1–5 Likert dimensions**: **readability, personalness, redundancy, cohesiveness, likeability, believability**.
- Annotators also **predicted the author's Big Five profile**.

**Accuracy (Extraversion, best-perceived trait)**:
- **0.68** — individual annotator accuracy
- **0.84** — majority-vote (collective) accuracy, when annotators were **unaware** of AI authorship

The "up to 80%" in the abstract refers to this majority-vote accuracy band. Extraversion is the most perceptible trait; other traits are perceived less accurately.

## The AI-authorship disclosure experiment (headline finding)

When annotators **were informed** the stories were AI-written:
- **Personality prediction accuracy dropped significantly across all traits.**
- **Perceived "personalness" dropped notably.**

Verbatim: > Knowledge of the content's origin may influence their sense of connection to the material.

**Why this matters for us**: the *text did not change* — only the disclosure did. This is a rater-side bias effect, and it means human evaluation of AI companion output is **not disclosure-neutral**. Any human-eval protocol we design must decide and document whether raters know they are rating AI, because that single choice moves the numbers.

## Models and sample sizes

- **Primary**: `gpt-3.5-turbo-0613` and `gpt-4-0613`, **temperature = 0.7**
- **320 personas per model** (32 combinations × 10)
- **LLaMA-2**: results relegated to appendices — output "not suitable for human evaluation"
- Human eval on **32 GPT-4 stories**, **5 annotators**

## Limitations (verbatim — section headers)

The authors organize limitations under four headers: **"Focus on Closed Models," "Data Size," "Task & Language Variety," "Evaluation & Interaction."**

They note: concentrating predominantly on GPT models; limited sample sizes despite temperature variation (0.7); restricting evaluation to **English narrative contexts**; and lacking **longitudinal human-AI interaction studies**.

### Additional criticisms (our assessment)

- **Self-report circularity**: asking a model that was just told "you are extroverted" whether it is extroverted is close to an instruction-following check. The d>4 effect sizes should not be read as evidence of deep personality simulation.
- **Tiny human eval**: 32 stories, 5 annotators. No inter-annotator agreement coefficient is reported (only majority-vote accuracy) — a real gap versus InCharacter's Cohen's Kappa and PersonaGym's Fleiss Kappa.
- **Single-task, single-genre**: one 800-word story per persona. Trait expression in narrative writing may not transfer to conversational turns — which is what a companion product actually produces.
- **Binary trait poles**: real Big Five traits are continuous; the 2⁵ binarization produces exaggerated, caricatured personas that are easier to detect than realistic ones.
- **Dated models** (2023-era GPT-3.5/GPT-4-0613).

## Multilingual and multi-turn support

- **Multilingual / Chinese**: **NO.** English only — explicitly acknowledged in the "Task & Language Variety" limitation.
- **Multi-turn**: **NO.** Single-shot story generation, no dialogue at all. The "Evaluation & Interaction" limitation explicitly flags the absence of longitudinal human-AI interaction study.

Of the four, this is the furthest from a conversational/companion setting — it evaluates *written artifacts*, not interaction.

## Relevance to companion-eval-platform

- **Foundational, not operational.** Establishes that trait-conditioning works and is perceptible to humans, which underwrites the whole premise. Not usable as a running benchmark.
- **The disclosure effect is the single most actionable finding for our human-eval design** — we must standardize whether raters know they're rating AI, and we should probably run blind, since disclosed ratings are depressed and would confound model-vs-model comparison.
- **The six story-quality Likert dimensions** (readability, personalness, redundancy, cohesiveness, likeability, believability) are a reusable human-rating rubric — **"personalness," "likeability," and "believability" are especially on-point for companion products** and are not covered by the other three benchmarks (which all measure fidelity, not *appeal*). This is PersonaLLM's unique contribution to our dimension set.
- **LIWC as a cheap automatic signal** for trait expression is worth considering as a no-judge-cost metric.
- **Take the caution**: self-report validates instruction-following, not character depth. Prefer InCharacter's interview approach for fidelity, and borrow PersonaLLM only for the *human-perception* and *appeal* half of the picture.
