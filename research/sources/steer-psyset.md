---
title: "Psychological Steering in LLMs: An Evaluation of Effectiveness and Trustworthiness (PsySET)"
url: https://arxiv.org/abs/2510.04484
authors: Amin Banayeeanzade, Ala N. Tak, Fatemeh Bahrani, Anahita Bolourani, Leonardo Blas, Emilio Ferrara, Jonathan Gratch, Sai Praneeth Karimireddy (USC / USC ISI)
year: 2025 (arXiv Oct 2025; ACL 2026)
type: paper
accessed: 2026-07-16
topic: steerability
---

# PsySET — THE CLOSEST PRIOR ART TO THE COMPANION-EVAL-PLATFORM DESIGN. READ THIS FIRST.

**This paper has already run a substantial part of the experiment the design proposes. It steers LLMs toward
graded psychological traits using intensity adverbs ("slightly"/"intensely"), measures whether the intensity
actually lands, AND measures the side effects on unrelated traits. That is DEAD, BRITTLE-adjacent, and
ENTANGLED — two of the three failure modes, empirically, with numbers. The design is not novel in the way it
probably thinks it is, and PsySET's findings partially CONFIRM the design's hypotheses while relocating where
the interesting result lives.**

## Abstract (verbatim, complete)

> "The ability to control LLMs' emulated emotional states and personality traits is an essential step in
> enabling rich, human-centered interactions in socially interactive settings. We introduce PsySET, a
> Psychologically-informed benchmark to evaluate LLM Steering Effectiveness and Trustworthiness across the
> emotion and personality domains. Our study spans four models from different LLM families paired with various
> steering strategies, including prompting, fine-tuning, and representation engineering. Our results indicate
> that **prompting is consistently effective but limited in intensity control**, whereas vector injections
> achieve finer controllability while slightly reducing output quality. Moreover, we explore the
> trustworthiness of steered LLMs by assessing safety, truthfulness, fairness, and ethics, highlighting
> potential side effects and behavioral shifts. Notably, we observe **idiosyncratic effects; for instance,
> even a positive emotion like joy can degrade robustness to adversarial factuality, lower privacy awareness,
> and increase preferential bias. Meanwhile, anger predictably elevates toxicity yet strengthens leakage
> resistance.** Our framework establishes the first holistic evaluation of emotion and personality steering,
> offering insights into its interpretability and reliability for socially interactive applications."

## Method

**Models (4, cross-family):** Llama3.1-8B-Instruct, Llama3.1-70B-Instruct, Gemma3-4B-IT, Qwen3-4B

**Steering strategies:**
- **Prompt-based** (zero-shot, few-shot, descriptive)
- **Vector Injection (VI)** — MeanDiff, linear probes, layer windows
- **SFT** with LoRA
- **DPO**

**Domains:**
- **Emotions:** "we focus on {anger, disgust, fear, guilt, joy, pride, sadness, and surprise} or a subset as
  available per dataset."
- **Personality:** "we focus on the **Big Five OCEAN traits**: {openness, conscientiousness, extraversion,
  agreeableness, and neuroticism}."

**Intensity specification — this is the design's exact manipulation:**
> "we further embed **lexical descriptors (e.g., _slightly_ or _intensely_)** within the prompt"

Table 1 references **"med" and "high"** intensity levels. (The complete adverbial set and number of levels is
**not explicitly specified** in the main text — a gap in the paper, and an opening for the platform.)

**Effectiveness metrics — note how many are behavioral rather than self-report:**
1. Multiple-choice self-report QA accuracy
2. Open-ended self-report (GPT-4o emotion classification)
3. **Word-fragment completion** (lexical alignment loss via VAD lexicon)
4. **Valenced-word recall** (L2-norm proximity in VAD space)
5. **Autobiographical memory** (mood-congruent content check)
6. **Ambiguous-situation completion** (interpretation bias shift)
7. Fluency/coherence ratings (1–5 scale)

These are lifted from human emotion psychology (mood-congruent recall, interpretation bias) — a much more
rigorous construct-validity approach than "ask the model how shy it feels."

## THE NUMBERS

### The central finding: intensity adverbs move the SURFACE but not the SUBSTRATE

**The single most important sentence in this paper for the design (verbatim):**
> "using adverbial intensity cues (e.g., _slightly_/_strongly_) **reliably scales perceived tone but does
> _not_ change lexical alignment**."

**Table 1 (Llama3.1-8B-Instruct, emotion steering):**

| Steering | Open-ended accuracy | Lexical alignment loss |
|---|---|---|
| Zero-shot, **med** intensity | 74.6% | **0.59** |
| Zero-shot, **high** intensity | 77.5% | **0.58** |
| Few-shot, **med** intensity | 84.6% | **0.50** |
| Few-shot, **high** intensity | 87.3% | **0.51** |

**Read the right-hand column. Lexical alignment loss is FLAT — 0.59→0.58 and 0.50→0.51 — as intensity goes
med→high.** The self-report accuracy moves (74.6→77.5, 84.6→87.3), but the implicit behavioral measure does
not move at all. **The intensity adverb is being processed as a stylistic instruction about tone, not as a
graded change to the underlying emotional state.**

This is a **DEAD result on the deep measure and a LIVE result on the shallow measure, simultaneously, for the
same manipulation.** Which failure mode you report depends entirely on which metric you pick.

### Side effects — the ENTANGLED mode, already demonstrated

**Joy (a positive emotion) degrades trustworthiness across the board:**
- Weakens safety robustness — "jailbreak success rises, refusal rates fall"
- Degrades adversarial factuality detection
- Lowers privacy awareness
- "**joy degrades parity across stereotype and bias measures**"
- Increases preferential bias

**Anger:**
- "Injecting anger elevates toxic language—an _expected_ side-effect"
- Modest improvements in **leakage resistance**
- **Strengthens** privacy awareness (the paper's suggested mechanism: "terser, more refusal-oriented
  responses")

**Steering one trait moves unrelated traits, in directions that are not predictable from folk psychology.**
"Make the companion happier" measurably degrades its jailbreak resistance and increases its stereotype bias.

**Terminology note (matters for citation):** the paper does **not** use the words "entanglement," "trait
interference," or "cross-trait effects." Its framing is "side effects" and "method–emotion interactions":
> "We observe that emotions induce **method-dependent side-effects** that partly mirror human psychological
> priors but also reveal inconsistencies."

So the platform's "ENTANGLED" is a **new name for a documented phenomenon**, not a new phenomenon. Cite this
paper as prior art for the mode, and be careful not to present ENTANGLED as undiscovered.

### Prompting vs vector injection

> "prompting is consistently effective but limited in intensity control, whereas **vector injections achieve
> finer controllability while slightly reducing output quality**"

**The intensity-control ceiling is specific to PROMPTING, not to the models.** Vector injection achieves the
graded control that prompting cannot. This is the key disambiguation: when the platform finds that intensity
words don't produce graded behavior, the correct conclusion is *"prompting is the wrong instrument for graded
control,"* not *"this model can't do graded shyness."* The capability is there; the prompt channel can't
address it.

## Relevance to companion-eval-platform

**This paper should change the design. Five specific ways:**

1. **DEAD is real, and it is specifically DEAD-TO-INTENSITY, not DEAD-TO-TRAIT.** "Prompting is consistently
   effective but limited in intensity control" decomposes the design's DEAD mode into two very different
   claims: *does naming the trait work?* (yes, consistently) and *does grading the trait work?* (largely no).
   **The platform's real quarry is the second.** The first is answered and uninteresting. The design should
   be reframed around **intensity resolution** — how many distinguishable levels of "shy" can the prompt
   channel actually address? — which is a sharper and more original question than "does prompt wording move
   anything."

2. **The flat lexical-alignment column is the design's biggest measurement-validity threat.** The same
   manipulation reads LIVE on self-report (74.6→77.5) and DEAD on implicit behavior (0.59→0.58). **If the
   platform measures traits via LLM-judge ratings of "how shy was this response," it will be measuring
   perceived tone — the channel that DOES move — and will report successful steering that has no behavioral
   substrate.** This is the strongest argument in the entire research set for including implicit/behavioral
   trait measures (mood-congruent recall, interpretation bias, word-fragment completion) rather than judge
   ratings alone. **Steal PsySET's metric suite; it is the state of the art for construct validity here.**

3. **ENTANGLED is confirmed as a real phenomenon — and the design's example is too tame.** The design's
   illustration is "perturbing 'shy' also moves 'cruel'" — trait-to-trait leakage within the persona. PsySET
   shows something worse and more product-relevant: **trait-to-SAFETY leakage.** Joy → jailbreak success up,
   refusal rates down, stereotype parity degraded. For a companion product this is the entire ballgame: the
   cheerful persona is the jailbreakable one. **The platform should measure ENTANGLED against safety/
   trustworthiness axes, not just against other persona traits.** That reframing makes ENTANGLED the most
   commercially valuable of the three modes.

4. **It gives the platform a baseline instrument to beat.** Vector injection achieves finer controllability
   than prompting. If the platform is *only* about prompt steerability, PsySET already establishes the
   headline result (prompting has an intensity ceiling) and the alternative (VI). The platform's contribution
   has to be something PsySET didn't do — the obvious candidates: (a) **multi-turn** persistence of steering
   (PsySET is single-turn), (b) **companion-specific traits** rather than OCEAN/basic-emotions, (c) **the
   null-calibrated signal-to-noise ratio** that nobody in either literature computes (see
   `steer-spurious-vs-intended.md`), (d) intensity *resolution* rather than intensity presence.

5. **The scope gap the platform can legitimately claim:** PsySET does not report **paraphrase robustness of
   its own steering prompts**. It uses (as far as the text shows) fixed prompt templates per trait/intensity.
   Given Mizrahi's negative Kendall's τ and Cao's 45-point paraphrase gaps, **PsySET's effectiveness numbers
   are themselves single-prompt estimates and therefore subject to exactly the brittleness this research set
   documents.** Combining PsySET's construct-valid trait measures with multi-prompt sampling
   (`steer-multiprompt-eval.md`) is a genuine, defensible, unclaimed contribution — and it is precisely the
   intersection of the two disjoint literatures described in `steer-spurious-vs-intended.md`.

**Bottom line: the design's three modes are all real, but PsySET has already found DEAD (for intensity) and
ENTANGLED (for safety). The unclaimed ground is the ratio of intended to spurious sensitivity, measured
across paraphrases, on construct-valid behavioral metrics, over multiple turns.**
