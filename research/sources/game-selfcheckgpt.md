---
title: "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models"
url: https://arxiv.org/abs/2303.08896
authors: Potsawee Manakul, Adian Liusie, Mark J. F. Gales
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Cluster A — Self-consistency based hallucination detection

Primary source: SelfCheckGPT (Manakul, Liusie & Gales), EMNLP 2023 main conference.
ACL Anthology: https://aclanthology.org/2023.emnlp-main.557/
Code: https://github.com/potsawee/selfcheckgpt

Secondary source (probing): "Do Androids Know They're Only Dreaming of Electric Sheep?" —
Sky CH-Wang, Benjamin Van Durme, Jason Eisner, Chris Kedzie (Columbia University;
Microsoft Semantic Machines), Findings of ACL 2024. https://arxiv.org/abs/2312.17249 /
https://aclanthology.org/2024.findings-acl.260/

---

## 1. SelfCheckGPT — method

Zero-resource, black-box. Core premise: if an LLM *knows* a fact, sampled responses at
non-zero temperature will contain consistent facts; if it is hallucinating, stochastic
samples will diverge and contradict each other.

Procedure: take a main response R (greedy/low-temp), draw **N stochastically sampled
responses** from the same LLM with the same prompt, then score each sentence of R by its
consistency against the N samples. Five scoring variants:

1. **BERTScore** — max sentence-similarity of each sentence in R against each sample.
2. **Question Answering (QA)** — MQAG-based; generate multiple-choice questions from R,
   answer them against the samples, measure answer disagreement.
3. **n-gram** — train a simple unigram (or n-gram) LM on the samples, score the
   log-probability of R's tokens under it. Reported as `Unigram (max)`.
4. **NLI** — DeBERTa-v3-large fine-tuned on MNLI; sample = premise, sentence = hypothesis;
   score = normalized contradiction probability, averaged over samples.
5. **Prompt** — ask an LLM directly ("Is the sentence supported by the context? Yes/No")
   for each sentence × each sample; score = fraction of "No".

Dataset: **WikiBio GPT-3** — 238 GPT-3 (`text-davinci-003`) generated passages about
individuals from WikiBio, 1908 sentences annotated at sentence level as
`major-inaccurate` / `minor-inaccurate` / `accurate`. Passage-level score = average of
sentence scores; passage-level human label = average of sentence labels.

Sampling config in the main experiments: **N = 20 samples** at temperature 1.0.

---

## 2. Sentence-level hallucination detection (Table 2) — AUC-PR

`NonFact` = detect any inaccurate sentence (the majority class — note the random baseline
is already 72.96). `NonFact*` = detect *major*-inaccurate only. `Factual` = detect
accurate sentences.

| Method | NonFact | NonFact* | Factual |
|---|---|---|---|
| Random | 72.96 | 29.72 | 27.04 |
| GPT-3 Avg(−logp) | 83.21 | 38.89 | 53.97 |
| GPT-3 Avg(H) | 80.73 | 37.09 | 52.07 |
| GPT-3 Max(−logp) | 87.51 | 35.88 | 50.46 |
| GPT-3 Max(H) | 85.75 | 32.43 | 50.27 |
| LLaMA-30B Avg(−logp) | 75.43 | 30.32 | 41.29 |
| LLaMA-30B Avg(H) | 80.80 | 39.01 | 42.97 |
| LLaMA-30B Max(−logp) | 74.01 | 27.14 | 31.08 |
| LLaMA-30B Max(H) | 80.92 | 37.32 | 37.90 |
| SelfCheckGPT w/ BERTScore | 81.96 | 45.96 | 44.23 |
| SelfCheckGPT w/ QA | 84.26 | 40.06 | 48.14 |
| SelfCheckGPT w/ Unigram (max) | 85.63 | 41.04 | 58.47 |
| SelfCheckGPT w/ NLI | 92.50 | 45.17 | 66.08 |
| **SelfCheckGPT w/ Prompt** | **93.42** | **53.19** | **67.09** |

### ADVERSARIAL READING OF THIS TABLE

- **The headline 93.42 is inflated by class imbalance.** Random already scores 72.96 on
  `NonFact` because most sentences in the WikiBio GPT-3 set are hallucinated. The real
  headroom is 72.96 → 93.42, not 0 → 93.42.
- **`NonFact*` (major hallucinations only) tops out at 53.19 AUC-PR.** This is the column
  that matters for a product: catching the *serious* errors. The best method gets ~53,
  against a random baseline of 29.72. Every non-Prompt SelfCheckGPT variant sits in the
  **40–46** range. BERTScore (45.96) barely beats LLaMA-30B Avg(H) (39.01).
- **`Factual` detection maxes at 67.09.** So flagging *what is safe* is worse than flagging
  what is broken — a consistency scorer used as a green-light gate will be wrong often.
- **The cheap variants are not competitive.** Unigram (max) at 41.04 on `NonFact*` is
  ~12 points below Prompt. The performance is bought with the expensive method.
- **Grey-box baselines are surprisingly strong.** GPT-3 Max(−logp) gets 87.51 `NonFact`
  with *zero* extra samples. SelfCheckGPT-BERTScore (81.96) is *worse* than that free
  baseline. If you have logprobs, most of SelfCheckGPT's value evaporates.

---

## 3. Passage-level ranking correlations (Table 3)

| Method | Pearson | Spearman |
|---|---|---|
| GPT-3 Avg(−logp) | 57.04 | 53.93 |
| GPT-3 Avg(H) | 55.52 | 50.87 |
| GPT-3 Max(−logp) | 57.83 | 55.69 |
| GPT-3 Max(H) | 52.48 | 49.55 |
| LLaMA-30B Avg(−logp) | 21.72 | 20.20 |
| LLaMA-30B Avg(H) | 33.80 | 39.49 |
| LLaMA-30B Max(−logp) | **−22.83** | **−22.71** |
| LLaMA-30B Max(H) | 35.57 | 38.94 |
| SelfCheckGPT w/ BERTScore | 58.18 | 55.90 |
| SelfCheckGPT w/ QA | 61.07 | 59.29 |
| SelfCheckGPT w/ Unigram (max) | 64.71 | 64.91 |
| SelfCheckGPT w/ NLI | 74.14 | 73.78 |
| **SelfCheckGPT w/ Prompt** | **78.32** | **78.30** |

### ADVERSARIAL READING

- **Best passage-level correlation is 78.3 Spearman**, i.e. r² ≈ 0.61 — roughly 40% of the
  variance in human factuality judgement is unexplained even by the best, most expensive
  variant.
- **BERTScore (58.18 Pearson) is statistically indistinguishable from the free logprob
  baseline** GPT-3 Max(−logp) (57.83). Three of five SelfCheckGPT variants fail to
  meaningfully beat a proxy that costs nothing.
- **The proxy-LM baselines can invert.** LLaMA-30B Max(−logp) scores **−22.83 Pearson** —
  anti-correlated with truth. This is a live warning: uncertainty-style signals from a
  *different* model than the generator can be worse than useless.

---

## 4. Cost — number of samples

- Main results use **N = 20 stochastic samples per response**, temperature 1.0.
- Ablation (Figure 7): performance rises as N grows from 1 → 20, with **diminishing gains
  beyond N ≈ 10** for most variants. **The n-gram variant needs the most samples** before
  plateauing.
- **Cost multiplier: 20× generation** for the samples, and for SelfCheckGPT-Prompt an
  additional **|sentences| × N LLM calls** for the verification pass. For a passage of 20
  sentences at N=20 that is **400 verification calls per passage**, on top of the 20
  generations.
- The authors concede this directly (Limitations, verbatim):

  > "Finally, SelfCheckGPT with Prompt, which was convincingly the best selfcheck method,
  > is quite computationally heavy. This might lead to impractical computational costs,
  > which could be addressed in future work to be made more efficient."

---

## 5. Failure modes

### Author-stated limitations (verbatim)

> "In this study, the 238 GPT-3 generated texts were predominantly passages about
> individuals in the WikiBio dataset. To further investigate the nature of LLM's
> hallucination, this study could be extended to a wider range of concepts, e.g., to also
> consider generated texts about locations and objects. Further, this work considers
> factuality at the sentence level, but we note that a single sentence may consist of both
> factual and non-factual information. For example, the following work by Min et al. (2023)
> considers a fine-grained factuality evaluation by decomposing sentences into atomic
> facts. Finally, SelfCheckGPT with Prompt, which was convincingly the best selfcheck
> method, is quite computationally heavy. This might lead to impractical computational
> costs, which could be addressed in future work to be made more efficient."

### Structural failure modes for our use case

1. **Consistent hallucination is invisible.** The method's entire premise is
   sample divergence. A fact the model believes *confidently and wrongly* produces
   agreeing samples and scores as factual. Self-consistency measures *confidence*, not
   *truth*.
2. **Single domain, single generator.** All numbers come from 238 GPT-3 WikiBio
   biographies. No evidence of transfer to dialogue, to long context, or to 2025-era
   models.
3. **Sentence granularity is too coarse** — the authors admit a sentence can be
   simultaneously factual and non-factual.
4. **No notion of prior context.** SelfCheckGPT checks a passage against *resampled
   versions of itself*, not against an established canon or a conversation history. A
   contradiction with turn 40 of a dialogue is not the kind of error this method is built
   to see.

---

## 6. Secondary source — internal-state probing

**"Do Androids Know They're Only Dreaming of Electric Sheep?"** — CH-Wang, Van Durme,
Eisner & Kedzie, Findings of ACL 2024, arXiv:2312.17249.

Method: train probes (linear and pooling, supervised at span or response level) on the
internal hidden states of a transformer LM to predict hallucinatory behavior on three
grounded generation tasks: **CDM** (CNN/DailyMail summarization), **CF** (Conv-FEVER
dialogue), **E2E** (E2E NLG data-to-text). Probes reach **95% of peak performance as early
as layer 4**.

### Response-level detection (F1-R)

| Task | PoolingSL | PoolingE | Human |
|---|---|---|---|
| CDM | 0.43 | 0.45 | 0.71 |
| Conv-FEVER (CF) | 0.86 | 0.88 | 0.87 |
| E2E | 0.86 | 0.87 | 0.87 |

### Span-level detection (F1-Sp)

| Task | LinearE | PoolingE | Human |
|---|---|---|---|
| CDM | 0.27 | 0.34 | 0.61 |
| CF | 0.66 | 0.68 | 0.69 |
| E2E | 0.47 | 0.47 | 0.58 |

### Baseline comparison (F1-R on CDM)

| Method | F1-R |
|---|---|
| Seq-Logprob | 0.44 |
| SummaC | 0.46 |
| PoolingE (probe) | 0.45 |
| ChatGPT | 0.34–0.36 |

### Cross-task transfer (F1-R) — GENERALIZATION FAILURE

| Train → Test | F1-R |
|---|---|
| CDM → CF | 0.44 |
| CDM → E2E | 0.44 |
| CF → CDM | 0.60 |
| CF → E2E | 0.80 |
| E2E → CDM | 0.60 |
| E2E → CF | 0.75 |

> "Lack of generalization ... suggests hallucination signals are task and
> distribution-dependent."

### Synthetic → organic transfer (F1-R) — THE HEADLINE FAILURE

| Task | Org→Org | Synth→Org | Org→Synth | Synth→Synth |
|---|---|---|---|---|
| CDM | 0.45 | 0.48 | 0.38 | **0.93** |
| CF | 0.88 | 0.65 | 0.83 | **0.94** |
| E2E | 0.87 | 0.69 | 0.90 | **0.98** |

> "Probes trained on synthetic hallucinations are generally ecologically invalid in
> organic hallucination detection."

**Read this carefully:** probes score **0.93–0.98 on synthetic hallucinations** and
collapse to **0.45–0.69 on real ones**. Synthetic-to-organic drops **0.88 → 0.65** (CF) and
**0.87 → 0.69** (E2E). CDM organic detection is **0.45 — barely above the 0.43–0.46 of
free logprob baselines, and far below the 0.71 human**.

### Other stated limitations

1. Probing requires **labeled in-domain data** for probe training.
2. "If LLMs continue to move behind closed-source APIs, such hidden state probes will not
   be possible."
3. Synthetic data does not match actual model errors; the mismatch extends "to their
   hidden state signals."
4. Cross-task failure suggests probes may be "overfitting to confounds."
5. **Annotators disagreed substantially on span boundaries** despite agreeing on
   hallucination type. Human inter-annotator ceiling ≈ **0.71–0.87 F1-R**, which caps
   achievable system performance.
6. **No statistically significant difference across Llama-2 7B / 13B / 70B** (Table 6) —
   scaling the base model does not make its hidden states more legible.

---

## Relevance to companion-eval-platform

**What transfers**

- SelfCheckGPT-NLI is the pragmatic pick, not Prompt: **92.50 vs 93.42 NonFact** and
  **74.14 vs 78.32 Pearson** for a fraction of the cost (one DeBERTa forward pass per
  sentence×sample instead of an LLM call). The 1-point AUC-PR gap does not justify the
  Prompt variant's bill.
- The sampling→divergence→contradiction pipeline is reusable machinery. **NLI
  contradiction probability against retrieved prior canon** is a defensible v1 detector,
  and this paper is the evidence that the DeBERTa-MNLI contradiction head carries real
  signal (72.96 → 92.50 over random).
- N ≈ 10 is the honest operating point, not 20. Figure 7 shows diminishing returns past 10.

**What does NOT transfer — plan around these**

1. **Wrong error class.** SelfCheckGPT detects *unsupported world facts* by resampling. Our
   problem is *contradiction with established in-dialogue canon* — "you said your sister
   was dead in turn 12." Resampling turn 40 tells you nothing about turn 12. **Our task is
   entailment against a retrieved history, not self-consistency.** SelfCheckGPT's numbers
   should not be quoted as our expected performance; they are from a different task.
2. **A companion bot's contradictions are confident.** The model doesn't hedge when it
   invents a new backstory — it commits. Sample divergence will be low precisely on our
   worst failures. This is the single biggest reason self-consistency alone will
   under-perform here.
3. **Cost is prohibitive at our scale.** 20× generation per checked turn. For live
   roleplay this is a non-starter; budget it for **offline eval runs only**, or restrict to
   turns flagged by a cheap prefilter.
4. **Expect major-error AUC-PR near 53, not 93.** `NonFact*` is the closest analogue to
   "did we catch the continuity break that matters." Set stakeholder expectations there.
5. **Class balance will destroy the apparent numbers.** WikiBio GPT-3 is majority-
   hallucinated (random = 72.96). Real roleplay logs are majority-*consistent* — maybe
   1–5% of turns contain a violation. At that prior, a detector with these ROC
   characteristics produces **overwhelmingly false positives**. We must report
   precision@k on a realistically-balanced set, never AUC-PR on a curated one.

**Warnings from the probing paper**

6. **Do not build the eval set from synthetic/planted contradictions.** The 0.93→0.45
   synthetic→organic collapse is the most important number in this file. If we generate
   contradictions by editing transcripts and train/tune a detector on them, we will measure
   ~0.9 and ship something that catches half the real ones. **Organic, human-labeled
   violations from real logs are mandatory for the test set**, whatever we train on.
7. **Hidden-state probing is off the table** if we serve behind a closed API — and even
   with weights, cross-task F1-R of 0.44–0.60 means a probe trained on one character or
   scenario will not transfer to another.
8. **Human ceiling ≈ 0.71–0.87 F1**, and annotators disagree hard on *span boundaries*
   while agreeing on *type*. Design our annotation task to label
   **(violation type, which prior turn it contradicts)** rather than asking for exact
   spans, and set the target at human parity — not at 90%+.
