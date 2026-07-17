---
title: "Editing Personality for Large Language Models (PersonalityEdit)"
url: https://arxiv.org/abs/2310.02168
authors: Shengyu Mao, Xiaohan Wang, Mengru Wang, Yong Jiang, Pengjun Xie, Fei Huang, Ningyu Zhang (Zhejiang University / Alibaba)
year: 2023
type: paper
accessed: 2026-07-16
topic: steerability
---

# PersonalityEdit — model editing for traits, and the "locality" metric that ISN'T a crosstalk metric

**The adversarial hypothesis going in: in model editing, "locality" IS the crosstalk metric, so this paper must already measure whether editing trait X damages trait Y. The hypothesis is WRONG, and the reason matters. Their locality metric (DD) is over TOPICS, not over TRAITS. But they do report a cross-trait failure mode in their error analysis, and it names specific traits.**

Verification: extracted via `ar5iv.labs.arxiv.org/html/2310.02168` and the arXiv abstract page. Quotes below are as returned by extraction; I was not able to string-match every table cell against a raw dump, so **numbers in the results table should be re-verified before being cited in a paper**. Flagged honestly rather than presented as confirmed.

## Abstract / task (verbatim)

> "This paper introduces an innovative task focused on **editing the personality traits of Large Language Models (LLMs)**."

> "This task seeks to **adjust the models' responses to opinion-related questions on specified topics** since an individual's personality often manifests in the form of their expressed opinions."

Traits: **Neuroticism, Extraversion, Agreeableness** (three, not five — drawn from social psychology theory). Benchmark **PersonalityEdit** built with GPT-4-generated responses aligned to (topic, target trait) pairs.

## The metrics

| Metric | What it measures |
|---|---|
| **ES** (Edit Success) | edited model assigns high probability to target personality while maintaining topic consistency; `ES ≜ z_per · z_topic` |
| **DD** (Drawdown) | **KL-divergence between base and edited models on OUT-OF-SCOPE TOPICS** — "to ensure edits don't harm unrelated topics" |
| **Acc** | RoBERTa-Base classifier (**97.75%** test accuracy) predicts personality trait in generated text |
| **TPEI** (Target Personality Edit Index) | `TPEI = −(cross(p'_e, p_e) − cross(p'_b, p_e))` — cross-entropy improvement toward target personality vs base |
| **PAE** (Personality Adjective Evaluation) | GPT-4 rates text **1–5** on trait-specific adjectives; `PAE = pae(y'_e, p_e) − pae(y'_b, p_e)` |

## THE KEY NEGATIVE RESULT — DD is topic-locality, not trait-locality

**In the model-editing literature, "locality"/"specificity" means: did the edit leave everything else alone?** The adversarial expectation was that PersonalityEdit's locality metric would therefore already be a trait×trait crosstalk measurement.

**It is not.** DD measures KL divergence on **out-of-scope topics** — i.e. "if I edit the model's agreeableness *about cats*, did its behavior *about politics* change?" The axis of locality is the **topic**, not the **trait**.

**There is no metric in this paper of the form "editing toward Agreeableness moved the model's Neuroticism by X."** The off-diagonal of a trait×trait edit matrix is not computed, despite the paper having exactly three traits and a trait classifier capable of scoring all three on any output.

**This is the same structural gap as PersonaLLM's unused 2⁵ factorial and BIG5-CHAT's collapsed Frobenius norm: the instrument to measure the off-diagonal is present and pointed at the diagonal.** Three papers, three groups, same omission — which is itself the strongest evidence that the off-diagonal is a genuine blind spot rather than a solved problem.

## THE CROSS-TRAIT FINDING THEY DO REPORT (verbatim)

In error analysis, editing toward one personality produces *other* personalities in the failures:

> "among **unsuccessful editing cases, the majority of editing errors resulted in the manifestation of Extraversion and Neuroticism**."

**This is a genuine off-diagonal observation.** Editing toward (e.g.) Agreeableness does not fail into noise — it fails into **specific other traits**, and the same two traits recur. Compare `steer-personality-shaping-independence.md`, where Google found "**conscientiousness and neuroticism fluctuated the most**" among untargeted traits. **Two independent papers, different methods (prompting vs. model editing), both name NEUROTICISM as a leak sink.** That is a convergent prior worth taking seriously and a concrete prediction for our matrix.

But note the limits: it is a **qualitative error-analysis remark**, not a measurement. No magnitude, no rate, no per-cell number, no direction beyond "these two show up."

## Main results (Table 2) — treat as unverified

For **GPT-J-6B with IKE**: ES = 0.4742, DD = 0.0274, Acc = 39.25%, TPEI = 3.075, PAE = 0.275
For **Llama-2-7b-chat with IKE**: ES = 0.4575, DD = 0.1411, Acc = 72.00%, TPEI = 3.154, PAE = 0.7749

Human evaluation (Table 3): PAE improved **3.20 → 3.83** post-editing.

**Note the ES values (~0.46–0.47) are barely above chance-ish territory and Acc for GPT-J is 39.25%.** Personality editing is *not* a solved or even reliably working technique in this paper — which matters for how much weight the whole line of work can bear.

## Relevance to companion-eval-platform

1. **The "locality = crosstalk" hypothesis is refuted, and that is good news for the project.** The model-editing literature's locality metrics are about **topics and unrelated facts**, not about **other traits of the same persona**. So we cannot be accused of reinventing edit-locality. **The trait-locality metric — "does editing/inducing trait X perturb trait Y" — is genuinely absent from the personality-editing literature**, even in the one paper explicitly about editing personality with a three-trait classifier in hand.

2. **The convergent Neuroticism signal is the most actionable finding here.** Google (prompt shaping): C and N fluctuate most when untargeted. PersonalityEdit (model editing): failures manifest as E and N. **Neuroticism appears as a leak sink under two unrelated induction methods.** If our matrix has a hot column, the prior says it is neuroticism-adjacent — for companion characters, that maps to anxiety/insecurity/volatility. **This is a pre-registerable prediction and we should state it before running.**

3. **Their failure mode is our failure mode, and it reframes the metric.** "Unsuccessful edits manifest *other* traits" means trait induction does not degrade gracefully toward neutral — **it degrades sideways into a different personality.** For a companion product this is the actual risk: crank "shy" too far and you do not get a flat character, you get an anxious or hostile one. **That is the Brittle mode in trait space rather than coherence space**, and it is a better story than "the model becomes incoherent." Our matrix should report *where* a failed induction lands, not just that it failed.

4. **Adopt DD (topic-locality) as an ADDITIONAL axis, not a substitute.** A complete companion-eval matrix arguably needs both: trait×trait (does shy→cruel?) and trait×topic (does making her shy change her opinions about politics?). PersonalityEdit gives us a validated formulation of the second. **We are proposing the first; we should acknowledge the second exists and cite this.**

5. **The weak absolute numbers are a caution about the whole editing line.** ES ≈ 0.46, GPT-J Acc = 39.25% — trait editing barely works here. Prompt-based induction (ρ ≥ 0.80 in Google's work) is *far* more effective than model editing was in 2023. **We should not treat model editing as a serious alternative induction method for our platform**, and we should not lean on this paper's numbers for anything load-bearing.

6. **Honest limitation of this source.** I could not fully string-match the Table 2 values against a raw text dump (ar5iv extraction only). The metric *definitions* and the error-analysis quote are solid; **the specific table numbers should be re-verified from the PDF before appearing in any writeup.** Also: only 3 traits, 2023-era models, and the RoBERTa trait classifier's 97.75% is on *its own* test set, which says little about its validity on edited-model outputs.

7. **Related:** `steer-personality-shaping-independence.md` (the C/N fluctuation finding — convergent), `steer-personality-illusion-crosstalk.md` (per-cell off-diagonal, the real measurement), `steer-trait-intercorrelation-benchmarks.md` (the pattern of papers holding the instrument and not using it), `steer-persona-vectors-crosstalk.md` ("datasets targeting one trait can inadvertently amplify other traits" — the same failure at fine-tuning time).
