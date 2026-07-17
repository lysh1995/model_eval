---
title: "Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection"
url: https://arxiv.org/abs/2504.11900
authors: Kabir Ahuja, Melanie Sclar, Yulia Tsvetkov
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Cluster B — Long-form narrative consistency, plot-hole & continuity detection

Sources covered in this file:

| # | Work | Venue / ID | Year |
|---|---|---|---|
| 1 | **Finding Flawed Fictions** (FlawedFictions) — Ahuja, Sclar, Tsvetkov | arXiv:2504.11900v3 | 2025 |
| 2 | **Lost in Stories: Consistency Bugs in Long Story Generation by LLMs** (ConStory-Bench) — Li, Guo, Wu, Lee, Li, Xie | arXiv:2603.05890v1 | 2026 |
| 3 | **What Matters in Evaluating Book-Length Stories?** (LongStoryEval / NovelCritique) | arXiv:2512.12839 | 2025 |
| 4 | **Improving Consistency in LLMs through Chain of Guidance** — Raj, Gupta, Rosati, Majumdar | arXiv:2502.15924 | 2025 |

---

## 1. Finding Flawed Fictions (FlawedFictions) — arXiv:2504.11900v3

**Authors:** Kabir Ahuja, Melanie Sclar, Yulia Tsvetkov (University of Washington). 2025.
HTML: https://arxiv.org/html/2504.11900v3

### Method

Task: given a story, decide whether it contains a **plot hole** and identify it. The
authors build an algorithm (**FlawedFictionsMaker**) that synthesizes controlled,
plausible plot holes into *existing human-written stories*, so the ground truth is known by
construction while the surrounding prose stays natural. Two splits:

- **FlawedFictions** — normal-length stories.
- **FlawedFictionsLong** — substantially longer stories, to isolate length effects.

Metrics: **accuracy** (binary: does the story contain a plot hole) and **CEEval-Full**
(a stricter measure requiring the model to correctly identify the plot hole, not just
detect that one exists). Random baseline = 0.50 accuracy.

### Results — FlawedFictions (Table 1a)

| System | Accuracy | CEEval-Full |
|---|---|---|
| **Human** | **0.76** | **0.68** |
| Claude 3.5 Sonnet | 0.76 | 0.67 |
| o1 (Low) | 0.71 | 0.65 |
| Random | 0.50 | — |

### Results — FlawedFictionsLong (Table 1b)

| System | Accuracy | CEEval-Full |
|---|---|---|
| o1 (Medium) | **0.61** | **0.53** |
| Claude 3.5 Sonnet + verifier | 0.60 | 0.50 |
| Random | 0.50 | — |

### ADVERSARIAL READING — this is the most important table in Cluster B

- **The ceiling on the *easy* split is 0.76 accuracy.** That is the **human** number.
  Not the model number — the human number. State-of-the-art models *match* humans (Claude
  3.5 Sonnet: 0.76) and neither gets past ~three-quarters correct on a binary task where
  random is 0.50. **Effective headroom over chance: 0.50 → 0.76.**
- **On long stories the whole field collapses to 0.60–0.61**, i.e. **~0.10 above random**.
  The paper states there is "a sharp drop in performance on FlawedFictionsLong" and that
  "almost all models obtain[] close to random level performance" on longer narratives.
- **CEEval-Full on long stories: 0.50–0.53.** When you require the system to actually *name*
  the plot hole rather than just assert one exists, long-form performance is
  indistinguishable from guessing.
- **Reasoning scaling does not rescue it.** "Inference-time reasoning scaling provides
  minimal improvements," and **increased reasoning effort sometimes yields *worse*
  results.** Note o1 (Medium) on the long split (0.61) — throwing more test-time compute at
  the problem is not a path out.
- **Verifier scaffolding buys ~nothing.** Claude 3.5 Sonnet *with a verifier* scores 0.60
  on the long split — no better than plain o1.

### Human agreement

Annotation used a **minimum of 3 annotators per instance** to verify the synthetic plot
holes. Synthesized examples were **accepted at a 70% rate** — i.e. **30% of algorithmically
generated "plot holes" did not survive human review**. Human *solve* accuracy on the
resulting verified set is only 0.76 / 0.68 CEEval-Full.

---

## 2. Lost in Stories / ConStory-Bench — arXiv:2603.05890v1

**Authors:** Junjie Li, Xinrui Guo, Yuhao Wu, Roy Ka-Wei Lee, Hongzhi Li, Yutao Xie
(Microsoft Beijing; Singapore University of Technology and Design). arXiv:2603.05890v1,
6 March 2026. HTML: https://arxiv.org/html/2603.05890v1 · HF: https://huggingface.co/papers/2603.05890

**Benchmark:** ConStory-Bench — **2,000 prompts across four task scenarios**, with a
taxonomy of **five error categories and 19 fine-grained subtypes**. Detector:
**ConStory-Checker**.

### Consistency-error taxonomy (5 categories / 19 subtypes) — directly reusable

1. **Timeline & Plot Logic** (6): Absolute Time Contradictions, Duration Contradictions,
   Simultaneity Contradictions, Causeless Effects, Causal Logic Violations, Abandoned Plot
   Elements
2. **Characterization** (4): Memory Contradictions, Knowledge Contradictions, Skill
   Fluctuations, Forgotten Abilities
3. **World-building & Setting** (3): Core Rules Violations, Social Norms Violations,
   Geographical Contradictions
4. **Factual & Detail Consistency** (3): Appearance Mismatches, Nomenclature Confusions,
   Quantitative Mismatches
5. **Narrative & Style** (3): Perspective Confusions, Tone Inconsistencies, Style Shifts

### ConStory-Checker detection performance (Table 6)

| Category | Recall | Precision | F1 |
|---|---|---|---|
| Character Consistency | 0.605 | 0.960 | 0.742 |
| Factual Accuracy | 0.625 | 0.845 | 0.718 |
| Narrative Coherence | **0.350** | 0.921 | **0.507** |
| Temporal Logic | 0.600 | 0.816 | 0.692 |
| World Consistency | 0.570 | 0.912 | 0.702 |
| **Overall** | **0.550** | **0.884** | **0.678** |

### Human expert baseline (average)

| Metric | Human expert |
|---|---|
| Recall | **0.139** |
| Precision | 0.660 |
| F1 | **0.229** |

Setup: **two professional web novel writers** independently annotated **200 stories with
1,000 planted errors**. The system claims a **3.2× improvement in error discovery rate**
over human judgment (**550/1000 vs 171/1000 errors detected**).

> ⚠️ **Reconciling 0.139 vs 0.171 — read this before citing either.** The table above reports
> human recall **0.139**; the sentence directly under it reports **171/1000 = 0.171**. Both
> appear to be correct and refer to different quantities: the table is explicitly labelled
> **"(average)"** — i.e. the mean recall of the *two annotators taken individually* — whereas
> **171 is the pooled union** of what *either* annotator found. **Arithmetic confirms the split:**
> 550/171 = **3.216 ≈ the paper's claimed "3.2×"**, while 550/139 = 3.96, which would have been
> reported as "4×". So the paper's headline comparison uses the **union (0.171)**, not the
> average (0.139). An independent re-fetch of the paper also surfaced **"Overall F1=0.281"** in
> prose against **0.229** in the table — consistent with the same average-vs-union split.
> **Cite it as: individual novelists averaged ~0.14 recall; the two of them pooled found ~0.17.**
> Do not pair "0.139" with "3.2×" in the same sentence — they are from different denominators
> and a knowledgeable reader will catch it. The qualitative finding is unaffected and robust:
> **professional human readers find well under a fifth of planted continuity errors.**

### ADVERSARIAL READING

- **Recall is 0.550 — the detector misses nearly half of all planted errors** that it was
  purpose-built to find, on stories where the errors were *inserted by the authors*. This
  is a best-case, known-ground-truth setting and it still loses 45% of violations.
- **Narrative Coherence recall is 0.350.** The subtlest and arguably most important
  category for roleplay (tone/perspective/style drift) is the one the detector is worst at
  — it finds **one in three**.
- **The "3.2× better than human" framing is a red flag, not a selling point.** It is driven
  entirely by the *human* baseline being catastrophic: **recall 0.139, F1 0.229**. Two
  professional novelists reading for errors found **14%** of planted ones. Read the correct
  way round, this says: **humans cannot reliably detect continuity errors either, so there
  is no trustworthy gold standard to validate a detector against.** A detector that beats a
  0.139-recall baseline has cleared a bar that is on the floor.
- **No inter-annotator agreement coefficients are reported.** No Cohen's κ, no Fleiss' κ —
  only comparative performance. With two annotators at 0.139 recall each, agreement is
  almost certainly very low, and the paper does not disclose it.
- **All errors are planted.** Per the synthetic→organic collapse documented in
  `game-selfcheckgpt.md` (0.93 → 0.45), these numbers are an **upper bound** that will not
  survive contact with organic errors.
- **Precision (0.884) is the only strong number**, and it is measured against planted
  ground truth in a story where errors are known to exist — a prior wildly unlike
  production.

### Error accumulation with length (RQ2)

> "Error counts increase approximately linearly with output length across models."

| Model | Length–error correlation |
|---|---|
| Claude-Sonnet-4.5 | r = 0.478 (moderate) |
| DeepSeek-V3.2-Exp | r = 0.973 (strong dependency) |

Model output-length patterns (confound to control for):

| Model | Length distribution |
|---|---|
| GPT-5-Reasoning | 90.6% exceed 6K words |
| Grok-4 | 70.2% concentrated in 0–3K words |
| Qwen3-32B | 92.0% beyond 3K words |

> "errors accumulate linearly with length; however, models differ substantially in their
> length preferences."

---

## 3. LongStoryEval / NovelCritique — arXiv:2512.12839

**"What Matters in Evaluating Book-Length Stories? A Systematic Study of Long Story
Evaluation."** HTML: https://arxiv.org/html/2512.12839

### Benchmark

**LongStoryEval**: **600 newly published books** (2024 – January 2025), average length
**121K tokens** (max **397K**), **340K reader reviews**, with average rating scores and
aspect-guided critiques.

### System-level correlation with human ratings (Table 2, Kendall-Tau)

Aspects: PLOT, CHA(racter), WRI(ting), THE(me), EMO(tional impact), ENJ(oyment).

| Method | PLOT | CHA | WRI | THE | EMO | ENJ | Overall |
|---|---|---|---|---|---|---|---|
| **NovelCritique-8B** | 27.1 | 27.0 | 24.1 | 24.3 | 27.8 | 21.1 | **27.7** |
| GPT-4o (Aggregation) | 14.3 | 16.7 | 10.2 | 10.4 | 9.7 | 9.1 | 15.2 |
| DeepSeek-v2.5 (Summary) | 13.4 | 12.2 | 1.8 | 7.1 | 8.9 | 13.2 | 14.4 |
| Llama 3.1-70B (Aggregation) | 19.6 | 13.8 | 2.3 | 13.4 | 7.7 | 11.5 | 13.8 |

**One-pass evaluation** (subset within 128K tokens):

| Model | Overall correlation |
|---|---|
| GPT-4o | **5.5** |
| DeepSeek-v2.5 | **4.8** |

### ADVERSARIAL READING

- **The best system in the paper reaches Kendall-τ = 27.7 overall.** Their own purpose-built
  fine-tuned model. Agreement with human readers on book-length stories is **weak by any
  standard**.
- **Frontier models score 13.8–15.2 τ.** GPT-4o with the best strategy manages **15.2**.
- **One-pass long-context evaluation is effectively broken: τ = 4.8–5.5.** Feeding the
  whole story to a long-context model and asking for a judgement produces **near-zero**
  correlation with humans. Long context windows do not solve this.
- **WRI (writing) correlation collapses to 1.8–2.3** for DeepSeek-v2.5 and Llama 3.1-70B —
  essentially no signal.
- **Incremental-updated evaluation — the strategy most analogous to streaming a live
  roleplay session — performed WORST**, suffering from **"accumulating inconsistency."**
  This is a direct negative result against the naive "maintain a running state summary"
  architecture.

Verbatim findings:

> "The one-pass results reveal a poor correlation with human ratings. Even when prompted to
> generate summaries first, these models often produce generic critiques that fail to
> capture the nuances of specific stories."

> "The primary issue with closed-source LLMs is their inconsistency. Even with
> temperature=0 and low top-p settings, the results exhibit significant variability. This
> inconsistency is likely due to the long context windows, which increase the likelihood
> for models to focus on uncertain or less relevant story elements."

Models also "tend to focus more on the story's strengths, offering only limited commentary
on its weaknesses" and "still struggle to generate nuanced critiques that closely align
with human preferences."

### Cost of the three strategies (Table 8)

| Method | Input tokens | Runtime | Cost (GPT-4o) |
|---|---|---|---|
| Summary-Based | 3,940K | 770 min | **$94** |
| Aggregation-Based | 11,480K | 3,056 min | **$416** |
| Incremental-Updated | 12,720K | 4,268 min | **$499** |

**$94–$499 and 13–71 hours to evaluate the benchmark.** Aggregation — the best-performing
strategy — costs **4.4× Summary** for a modest correlation gain. Incremental costs the most
*and* performs the worst.

Strategy ranking per the paper: **Aggregation-Based** (superior detail assessment, highest
correlations for most aspects) > **Summary-Based** (comparable, more efficient) >
**Incremental-Updated** (poorest; accumulating inconsistency).

Which aspects matter to readers: **objective** — plot and characters rank highest;
**subjective** — emotional impact, enjoyment & engagement, expectation fulfillment all
critical. **World-building and writing quality: least influential.**

---

## 4. Chain of Guidance (CoG) — arXiv:2502.15924 — LOW RELEVANCE, logged for completeness

**Authors:** Harsh Raj, Vipul Gupta, Domenic Rosati, Subhabrata Majumdar. 2025.
https://arxiv.org/abs/2502.15924 · Code: https://github.com/vijilAI/chain_of_guidance
OpenReview: https://openreview.net/forum?id=asiBW1bB9b

Method: a multistep prompting technique that generates highly consistent outputs; used to
synthesize paraphrase-consistent QA pairs with a capable LLM (e.g. GPT-4), then fine-tune
(PEFT/SFT) weaker models on them. Reported result: **fine-tuned models are "more than twice
as consistent" as base models**, with generalization to datasets not used in fine-tuning.

**Why this is NOT our paper.** This is *semantic consistency under paraphrased inputs* —
does the model give the same answer to the same question asked two ways. It is neither
narrative continuity nor contradiction detection, and it is a *generation-improvement*
method, not a *detector*. The task title is a false friend for "long-form consistency." No
detector precision/recall to harvest. **Do not cite as evidence for continuity detection.**

---

## Cross-cutting summary of failure numbers

| Claim | Number | Source |
|---|---|---|
| Best plot-hole accuracy, normal length (**= human**) | 0.76 | FlawedFictions |
| Best plot-hole accuracy, **long** stories | 0.61 (random = 0.50) | FlawedFictionsLong |
| Best CEEval-Full, long stories | 0.50–0.53 | FlawedFictionsLong |
| Synthetic plot holes rejected by human review | 30% | FlawedFictions |
| Purpose-built continuity detector **recall** | 0.550 | ConStory-Checker |
| Detector recall on Narrative Coherence | 0.350 | ConStory-Checker |
| **Professional novelist** recall on planted errors | 0.139 (F1 0.229) | ConStory-Bench |
| Best book-length eval correlation (Kendall-τ) | 27.7 | NovelCritique-8B |
| GPT-4o book-length eval correlation | 15.2 | LongStoryEval |
| **One-pass long-context** eval correlation | 4.8–5.5 | LongStoryEval |
| Cost to eval 600 books (best strategy) | $416 / 3,056 min | LongStoryEval |
| Length–error correlation | r = 0.478 → 0.973 | ConStory-Bench |

---

## Relevance to companion-eval-platform

**The single most important finding for us**

**Automated continuity detection degrades to near-random exactly where our product lives.**
FlawedFictionsLong: 0.61 accuracy vs 0.50 random on long stories, and CEEval-Full at
0.50–0.53. LongStoryEval one-pass: τ = 4.8–5.5. Long roleplay dialogue is *longer* than
both. **Any roadmap claiming reliable auto-detection of continuity violations in long
sessions is contradicted by every benchmark in this file.** Plan for a
**triage/assist tool**, not an oracle, and do not promise a precision/recall figure we
cannot hit.

**Directly actionable**

1. **Adopt the ConStory taxonomy (5 categories / 19 subtypes) as our violation schema.**
   It is the best-specified ontology available and maps cleanly onto companion roleplay:
   *Memory Contradictions*, *Knowledge Contradictions*, *Appearance Mismatches*,
   *Nomenclature Confusions*, *Core Rules Violations*, *Perspective Confusions*, *Tone
   Inconsistencies* are our bread and butter. Adopting it also makes our numbers
   comparable to a published baseline.
2. **Chunk-and-aggregate; do NOT stream a running state summary.** LongStoryEval's
   incremental-updated strategy was **worst-performing** *and* **most expensive** ($499,
   4,268 min) due to "accumulating inconsistency." Our instinct for a live companion —
   maintain a rolling canon summary and check each turn against it — is the exact
   architecture this benchmark shows failing. **Aggregation-based** won; **summary-based**
   was nearly as good at **~4.4× lower cost** ($94 vs $416) and is the right starting point.
3. **Expect recall ~0.55, precision ~0.88 at best** for a purpose-built detector, and set
   the product around that shape: **high-precision, low-recall = a good flagging tool for
   human reviewers, a bad gate.** Ship it as "surfaces likely continuity breaks for
   review," never "guarantees continuity."
4. **Budget for length.** Errors accumulate **linearly with output length** (r up to 0.973).
   Longer sessions have proportionally more violations *and* worse detection. Report all
   metrics **stratified by session length** — an aggregate number will hide the failure.

**Measurement traps to avoid**

5. **Do not validate against a small human panel and trust it.** ConStory-Bench's two
   professional novelists achieved **recall 0.139 / F1 0.229** on *planted* errors. Human
   annotators miss ~86% of continuity errors when reading naturally. Our "ground truth"
   will be badly incomplete unless annotators are given **structured, per-category
   checklists with the relevant prior turns retrieved for them** — approximating the
   aggregation strategy rather than free reading. Also note ConStory-Bench **reports no κ
   at all** — we should report ours, and expect it to be low.
6. **Planted-error benchmarks overstate performance twice over.** FlawedFictions had **30%
   of its synthetic plot holes rejected by human reviewers** — even careful synthesis
   produces invalid items at scale. Combined with the 0.93→0.45 synthetic→organic collapse
   in `game-selfcheckgpt.md`, treat any number from planted violations as a **ceiling** and
   hold out an organic, human-labeled set from real logs for the headline metric.
7. **Reasoning-effort scaling is not the lever.** FlawedFictions: inference-time reasoning
   scaling gives "minimal improvements" and sometimes makes things *worse*. Don't budget o-
   series/high-reasoning spend expecting it to close the gap — **retrieval of the right
   prior context is the lever**, which is what aggregation-over-chunks is really doing.
8. **Non-determinism is a real cost.** LongStoryEval found significant variability **even
   at temperature=0 with low top-p**, attributed to long context windows. Our detector's
   own scores will be noisy at long context. **Report variance across repeated runs**, and
   don't treat a single-run regression as signal.
9. **Verifier scaffolding is not a free win** — Claude 3.5 Sonnet + verifier scored 0.60 on
   FlawedFictionsLong, no better than an unscaffolded reasoning model.

**Related work worth a follow-up pass** (surfaced but not deep-dived): CharacterBench
(22,859 human-annotated samples, 3,956 characters, dimensions incl. Memory Consistency /
Fact Accuracy / Boundary Consistency / Behavior Consistency, judged by CharacterJudge);
CharacterEval (1,785 multi-turn dialogues, 4,564 test examples); RMTBench (80 characters,
8,000+ dialogue rounds, EN/ZH, arXiv:2507.20352); NarraBench (narrative benchmarking
framework, arXiv:2510.09869); "Staying In Character: Perspective-Bounded Memory For
Book-Based Role-Playing Agents" (arXiv:2606.25632). **CharacterBench's Memory Consistency
dimension is the closest published analogue to our exact task and should be the next thing
we read.**
