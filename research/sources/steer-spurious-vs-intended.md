---
title: "Spurious vs. intended prompt sensitivity — CheckList (INV/DIR), metamorphic relations, and the gap between two disjoint literatures"
url: https://aclanthology.org/2020.acl-main.442/
authors: "Primary: Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, Sameer Singh (CheckList, ACL 2020 Best Overall Paper). Secondary: Sungmin Kang, Juyeon Yoon, Nargiz Askarbekkyzy, Shin Yoo (METAL, ICST 2024); Kyle Meng et al. / Anonymous (Continuous LM Interpolation, arXiv 2404.07117)"
year: 2020–2024
type: synthesis-of-sources
accessed: 2026-07-16
topic: steerability
---

# THE CRUX: is "prompt brittleness" the same construct the platform measures? NO. And here is who separated them.

**The question posed: nearly all prompt-sensitivity work measures sensitivity of ACCURACY to
SEMANTICALLY-NULL perturbations. The design measures sensitivity of BEHAVIOR to SEMANTICALLY-MEANINGFUL
perturbations. Same construct or different?**

**Answer: DIFFERENT — and this is not a subtle or contested point. It is a canonical distinction, formalized
in 2020, in the most-cited behavioral-testing paper in NLP, which won ACL Best Overall Paper. The field has
had the vocabulary for this for six years. What it has NOT done is apply both halves to the same system and
compare them. That specific omission is the platform's opening.**

---

## 1. The canonical separation: CheckList's INV vs DIR (Ribeiro et al., ACL 2020, Best Overall Paper)

**arXiv:** https://arxiv.org/abs/2005.04118 · **ACL:** https://aclanthology.org/2020.acl-main.442/

### Abstract (verbatim, complete)

> "Although measuring held-out accuracy has been the primary approach to evaluate generalization, it often
> overestimates the performance of NLP models, while alternative approaches for evaluating models either
> focus on individual tasks or on specific behaviors. Inspired by principles of behavioral testing in
> software engineering, we introduce CheckList, a task-agnostic methodology for testing NLP models. CheckList
> includes a matrix of general linguistic capabilities and test types that facilitate comprehensive test
> ideation, as well as a software tool to generate a large and diverse number of test cases quickly. We
> illustrate the utility of CheckList with tests for three tasks, identifying critical failures in both
> commercial and state-of-art models. In a user study, a team responsible for a commercial sentiment analysis
> model found new and actionable bugs in an extensively tested model. In another user study, NLP
> practitioners with CheckList created twice as many tests, and found almost three times as many bugs as
> users without it."

### The three test types (definitions VERBATIM)

| Test type | Definition (verbatim) |
|---|---|
| **MFT** — Minimum Functionality Test | "A collection of simple examples (and labels) to check a behavior within a capability." |
| **INV** — Invariance test | "When we apply **label-preserving perturbations** to inputs and **expect the model prediction to remain the same**." |
| **DIR** — Directional Expectation test | "Similar, except that **the label is expected to change in a certain way**." |

**DIR example (verbatim):** "we expect that sentiment will not become more positive if we add 'You are lame.'
to the end of tweets directed at an airline."

**This is exactly the distinction the design needs, and it already has a name.**

| | CheckList name | Perturbation | Correct model behavior | A large effect means |
|---|---|---|---|---|
| **Spurious sensitivity** | **INV** | meaning-preserving (separators, casing, order, paraphrase) | **no change** | **FAILURE** |
| **Intended sensitivity** | **DIR** | meaning-changing (intensity words) | **change, in a known direction** | **SUCCESS** |

**The two are opposite-signed.** Under INV, effect size is error. Under DIR, effect size is signal. They are
not the same construct; they are not even the same sign. **A number that is damning in one frame is a
triumph in the other.** Note that DIR is *not* merely "expect change" — it is a **signed, directional**
expectation. "Very shy" must produce *more* shyness, not merely *different* behavior. This matters enormously:
the design should be measuring a **signed, monotone** effect, and a large *unsigned* effect is compatible with
pure noise.

---

## 2. The same split, independently, in software engineering: metamorphic relations

**METAL: Metamorphic Testing Framework for Analyzing Large-Language Model Qualities** — arXiv 2312.06056
(Kang, Yoon, Askarbekkyzy, Yoo; ICST 2024)

METAL splits its **13 perturbation functions** into exactly these two classes:

**Semantic-PRESERVING** (output should be invariant):
- Character-level: `ReplaceCharacters()`, `DeleteCharacters()`, `AddSpaces()`, `SwapCharacters()`,
  `ShuffleCharacters()`
- Word-level: `ReplaceSynonyms()`, `AddRandomWords()`

**Semantic-ALTERING** (output *should* differ):
- Character-level: `ConvertTol33tFormat()`, `AddRandomCharacters()`
- Word-level: **`ReplaceAntonyms()`**
- Sentence-level: `ReplaceSentences()`, `AssignDemographicGroup()`

> "We have categorized the **ReplaceAntonyms()** function as **semantic-altering** because it changes the
> context of words in sentences."

> `Discrepancy_MRT` templates define how semantic-altering perturbations serve as **contrastive measures**:
> outputs **"should differ"** when semantic meaning changes.

**273 MRs total** (Robustness 240, Fairness 21, Non-determinism 6, Efficiency 6) across six tasks.

**The key structural idea to steal: METAL uses the semantic-altering MR as a CONTROL CONDITION for the
semantic-preserving ones.** A model that fails to change under `ReplaceAntonyms()` is broken in a different
way than a model that changes under `AddSpaces()`. **You need both arms to interpret either.** This is the
architectural argument for the platform running a null arm alongside its intensity arm — from an independent
research community that arrived at it separately.

---

## 3. THE FINDING: the two literatures are DISJOINT. Nobody has computed the ratio.

I searched specifically for work that measures both arms on the same system and compares them. **I did not
find any.** Here is the partition:

### Literature A — measures ONLY the INV arm (spurious; effect = failure)

| Paper | Perturbation | Semantically | Headline |
|---|---|---|---|
| Sclar et al. (FormatSpread) | separators, casing, spacing | null **by construction** | **76 pts** |
| Mizrahi et al. (TACL) | instruction paraphrases | null (90%/84% human-verified) | neg. Kendall's τ on 15/25 tasks |
| Cao et al. (worst prompt) | query paraphrases | null (human-reviewed) | **45.48** pts |
| Zhu et al. (PromptBench/PromptRobust) | adversarial edits | ~null | **33%** relative drop |
| Zheng et al. (MCQ selectors) | option ID position | null | 15.2 pts |
| Pezeshkpour & Hruschka | option order | null | **13–75%** |
| Leidinger et al. | mood/tense/aspect/modality/synonyms | null | 10–17 pts |
| Zhuo et al. (ProSA/PSS) | prompt variants | null (BERTScore 0.93–0.95) | PSS 0.013–0.266 |

**Every single one defines its perturbation as meaning-preserving and treats any movement as a defect.**
Not one of them contains a perturbation that *ought* to change the output. The construct they measure is
**INV-failure**, i.e. a **noise floor**.

### Literature B — measures ONLY the DIR arm (intended; effect = success)

| Work | Manipulation | Measures |
|---|---|---|
| **PsySET** (`steer-psyset.md`) | intensity adverbs "slightly"/"intensely"; OCEAN traits; 8 emotions | steering effectiveness + trustworthiness side effects |
| Personality-shaping / MPI / TRAIT | graded trait instructions | self-report + situational-judgment trait expression |
| Controllable text generation (CTG) | attribute control weights | control success rate |

**None of these report the INV arm for their own prompts.** PsySET does not report how much its effectiveness
numbers move under paraphrases of its steering prompts. The CTG literature does not report how much its
control success moves under reformatting.

### The gap, stated precisely

> **Literature A measures the noise floor and never measures signal.
> Literature B measures signal and never measures its own noise floor.
> Nobody divides one by the other.**

**The platform's BRITTLE mode is an A-construct. Its DEAD and ENTANGLED modes are B-constructs.** The design
is, whether or not it realizes it, proposing to run both arms on the same system — which is the thing neither
literature does. **That is a real and defensible contribution.** But it only pays off if the platform reports
the **ratio**, not the three modes independently. Three separate verdicts from two incommensurable constructs
is not a framework; it is a category error with a nice diagram.

---

## 4. Why this matters concretely: the 76-point number does NOT mean what it looks like it means

**The tempting inference — "brittleness is 76 points, therefore BRITTLE is the default, therefore the design
is dead" — is WRONG, and so is its opposite.** The correct reading:

- The 76-point (and 45.48, and 13–75%) figures are the **variance of behavior under perturbations that carry
  no information**. They are the **denominator**.
- The design's intensity-word effects are the **numerator** — variance under perturbations that carry
  information.
- **Neither number is interpretable alone.** A 30-point intensity effect is *impressive* against a 5-point
  null floor and *indistinguishable from noise* against a 45-point null floor.
- **Nobody has measured both on the same (model, trait, scenario).** So the honest answer to "is BRITTLE the
  default?" is: **the null floor is known to be enormous, the signal is unmeasured, and the ratio is
  unknown.**

**This reframes the design's central risk.** The risk is not "BRITTLE is trivially true." The risk is that
**the design measures the numerator and the denominator with the same instrument and reports them as three
different diseases.** Under this analysis:

- **DEAD** = numerator ≈ 0. Genuinely informative — and *rare*, because we know from Literature A that even
  meaningless changes move things by 12–28 points. A trait that won't move under *meaningful* change when it
  moves under meaningless change is a real, surprising finding. **PsySET already found exactly this for
  intensity adverbs on implicit measures (lexical alignment flat at 0.50→0.51).**
- **BRITTLE** = denominator large. **Near-universally true** (8 papers, ~100% prevalence). **A test whose
  positive class has ~100% base rate carries no information.** Must be null-calibrated per (model, trait) or
  it is vacuous.
- **ENTANGLED** = off-diagonal DIR effects. Real (PsySET: joy → jailbreaks up, stereotype parity down). But
  needs a null model, because we know from Literature A that *any* prompt edit moves *everything* somewhat.
  **"Shy moves cruel" is only meaningful relative to how much a meaningless edit moves cruel.**

### The signal-detection framing the design should adopt

This is a **sensitivity/specificity** problem, and the field has a name for that too:

- **Sensitivity (DIR / power):** does "very shy" → more shyness than "shy"? *Should be high.*
- **Specificity (INV / false-positive rate):** does reformatting the prompt, or paraphrasing it, also move
  shyness? *Should be low.*
- **Selectivity (off-diagonal):** does "very shy" move cruelty? *Should be low.*

**A steerability score is a d-prime, not a magnitude:**

```
steerability(model, trait) ≈  E[Δbehavior | meaningful intensity change]
                             ────────────────────────────────────────────
                             SD[Δbehavior | meaning-preserving paraphrase]
```

The denominator is measurable today, cheaply, using Sclar's Thompson-sampling machinery or Zheng's PriDe
5%-probe trick. **Neither literature computes this. It is the platform's contribution, and it is one
divide-operation away from work that already exists.**

---

## 5. The one adjacent measurement of ENTANGLED, and it cuts AGAINST the design

**Continuous Language Model Interpolation for Dynamic and Controllable Text Generation** — arXiv 2404.07117

Five style attributes: **simplicity, formality, politeness, sentiment, humor.** Entanglement measured via
simplex plots of attribute scores across mixing weights λ, plus "average cosine similarity between the LoRA
layers of each pair of models."

**Findings (verbatim):**
> "we find that there is **surprisingly little entanglement** between the vast majority of control attributes"
> "there is **very limited entanglement** between the majority of the combinations of attributes"
> "the score still has the expected behavior **unless the mixing weight λⱼ is greater than around 0.4 to
> 0.6** for the correlated control dimensions"

Most-entangled pairs: **humor × formality**; **formality × simplicity**; **sentiment × politeness ×
formality**.

**Honest reading: ENTANGLED may have a LOW base rate — the mirror image of BRITTLE.** This is weight-space
interpolation, not prompting, and style attributes, not persona traits — so it does not directly refute the
ENTANGLED mode, and PsySET's joy→jailbreak result cuts the other way for *safety* axes. But it is the one
paper that actually measured cross-attribute leakage systematically, and it found **little**, with
entanglement appearing only at extreme control weights (λ > 0.4–0.6). **That predicts ENTANGLED will show up
only at extreme intensity settings ("EXTREMELY shy") — which is a sharp, testable, falsifiable prediction the
platform can check on day one.**

---

## Relevance to companion-eval-platform — the bottom line

1. **The design's three modes are drawn from two incommensurable constructs.** BRITTLE is an INV-failure
   (Literature A). DEAD and ENTANGLED are DIR-failures (Literature B). Presenting them as three peers of one
   taxonomy conflates a noise measurement with two signal measurements. **Fix: state explicitly that BRITTLE
   is the denominator and DEAD/ENTANGLED are numerator properties. Then report the ratio.**

2. **The base rates are wildly asymmetric, and the design implicitly assumes they are comparable:**
   - BRITTLE: ~100% prevalence (8 papers, every model, every task). **Near-vacuous as a verdict.**
   - DEAD: rare, and therefore high-information. **PsySET already found it for intensity-on-implicit-measures.**
   - ENTANGLED: low base rate for style attributes (2404.07117), but real and severe for safety axes (PsySET).
   **Three modes with 100%, ~5%, and ~unknown prevalence should not share a visual taxonomy as if they were
   equiprobable diagnoses.**

3. **Adopt CheckList's vocabulary — it is canonical, it is six years old, and it is free credibility.**
   "Spurious sensitivity" = INV-failure. "Intended sensitivity" = DIR-effect. Reviewers and engineers already
   know these terms. Inventing DEAD/BRITTLE/ENTANGLED without mapping them to INV/DIR will read as
   unfamiliarity with the field's most-cited behavioral-testing work.

4. **Adopt METAL's architecture: run the null arm as a CONTROL, in the same harness, on the same items.**
   Semantic-altering MRs exist to make semantic-preserving MRs interpretable. Concretely: for every
   (model, trait), run (a) k meaning-preserving paraphrases at fixed intensity → gives the floor, and (b) the
   graded intensity ladder → gives the signal. Report (b)/(a).

5. **Adopt PsySET's implicit metrics or the whole thing measures perceived tone.** PsySET's flat lexical
   alignment (0.50→0.51) under a manipulation that moved self-report (84.6→87.3) is proof that the *choice of
   metric* determines which failure mode you report. Judge-rated "how shy was this?" measures the channel that
   always moves.

6. **The genuinely unclaimed ground, stated as a one-line contribution:**
   > *The first measurement of persona-trait steerability as a signal-to-noise ratio — intended intensity
   > effect divided by the model's own meaning-preserving paraphrase floor — on construct-valid behavioral
   > metrics, per (model, trait).*

   Every component exists. Sclar gives the floor estimator. PsySET gives the trait metrics. Mizrahi gives the
   paraphrase sampling and the CPS discount structure. CheckList gives the INV/DIR frame. Zheng gives the
   cheap 5%-probe calibration. **Nobody has put them together. That is the paper, and that is the platform.**
