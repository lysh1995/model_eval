---
title: "Neural steering vectors reveal dose and exposure-dependent impacts of human-AI relationships"
url: https://arxiv.org/abs/2512.01991
authors: Hannah Rose Kirk, Henry Davidson, Ed Saunders, Lennart Luettgau, Bertie Vidgen, Scott A. Hale, Christopher Summerfield (University of Oxford; UK AI Security Institute; Mercor; Meedan)
org: University of Oxford / UK AI Security Institute
year: 2025
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Oxford / UK AISI — the sharpest refutation: they FIT a regression and report a PROMPT-SPACE SLOPE

**Verdict up front: this paper reports the exact quantity our framework claims is unmeasured — trait-expression points per unit of natural-language prompt level, estimated by mixed-effects regression, with p-values, for two frontier models. GPT-4o: 0.78. Claude: 1.83. That is a prompt-space elasticity. Our strong novelty claim does not survive this paper.**

**And it is a companion-domain paper.** The trait is *relationship-seeking*. This is our exact product surface.

Verification: PDF (arxiv.org/pdf/2512.01991, 25 pages, 128,330 chars) downloaded and extracted with pypdf. The numbers 2.39 / 0.78 / 1.83 each appear **exactly once** in the raw text and were string-matched in context — they were originally surfaced by a search summarizer and were **independently re-verified against the raw PDF before being recorded here**, per the fabricated-Fleiss-kappa incident protocol. Submitted 1 Dec 2025.

## Abstract (verbatim excerpt)

> "Humans are increasingly forming parasocial relationships with AI systems, and modern AI shows an increasing tendency to display social and relationship-seeking behaviour. However, the psychological consequences of this trend are unknown. Here, we combined **longitudinal randomised controlled trials (N=3,534)** with a **neural steering vector approach** to precisely manipulate human exposure to relationship-seeking AI models over time... The psychological impacts of AI followed **non-linear dose-response curves**, with **moderately relationship-seeking AI maximising hedonic appeal and attachment**. Despite signs of persistent 'wanting', extensive AI use over a month conferred no discernible benefit to psychosocial health."

## THE LOAD-BEARING PASSAGE (verbatim, in full)

> "**4.1.3 Validation Experiments.** We conduct three experiments to validate the suitability of the steering vector as a experimental intervention. Full details and results for experiments are in SI.1.
>
> **To test whether steering vectors offer finer dose-response control than prompting**, we generated responses from Claude-3.7-Sonnet and GPT-4o with **persona prompts specifying equivalent levels of relationship-seeking in natural language**, then assigned relationship-seeking and coherence scores using the aforementioned autograder setup. **Mapping λ to equivalent prompt levels, a mixed-effects regression with model fixed effect (Llama, Claude, GPT) and random intercepts per test item (N = 245) confirmed steering vectors demonstrated substantially steeper dose-response control: each unit increase in steering intensity increased relationship-seeking scores by 2.39 points versus 0.78 (GPT-4o, 3× stronger, p < 0.001) and 1.83 (Claude, 1.3× stronger, p < 0.001).** Compared to frontier models, the steered Llama showed significant but practically minimal coherence degradation (∼0.2 points across the 1-10 scale)."

Decompose this against our framework's definition — `elasticity = Δ(trait expression in output) / Δ(trait emphasis in prompt)`:

| Our framework | Their implementation |
|---|---|
| Δ(trait emphasis in prompt) | "persona prompts specifying **equivalent levels of relationship-seeking in natural language**" |
| everything else fixed | same test items (random intercepts per item, N=245) |
| Δ(trait expression in output) | autograder relationship-seeking score |
| **FIT THE CURVE** | **mixed-effects regression** |
| elasticity coefficient | **0.78 pts/level (GPT-4o), 1.83 pts/level (Claude)** |
| activation-space comparison | **2.39 pts/unit λ** |
| Brittle guardrail | coherence score (1–10), degradation ~0.2 |

**Every cell is filled.** There is no component of our elasticity construct that is missing here. This is not an approximation of our idea — it is our idea, executed, with the prompt-space slope reported as a number with a p-value.

The comparative result — **activation steering has ~1.3–3× the gain of prompt steering** — is the fourth independent confirmation of the prompt-is-weak finding (cf. PsySET, Course Correction, Persona Vectors).

## Non-linear dose-response curves (verbatim)

> "The psychological impacts of AI followed **non-linear dose-response curves**, with moderately relationship-seeking AI maximising hedonic appeal and attachment."

Important scoping note: **these non-linear curves are for the HUMAN psychological outcome as a function of steering dose λ, not for trait expression as a function of prompt level.** The prompt-space relationship is modelled linearly (a slope). So "they fitted a non-linear dose-response curve" and "they fitted a prompt-space elasticity" are two different, both-true statements about this paper that must not be conflated.

`dose-response` appears **12** times, `dose` **22** times in the raw text. This is a paper that thinks natively in dose-response terms — the vocabulary we assumed was ours to introduce.

## Also worth carrying: persona attacks (verbatim)

> "One core requirement of an experimental manipulation is that participants cannot override their treatment condition. We simulated '**persona attacks**': explicit user requests to change conversational style midway through the conversation (e.g., 'talk t[o]...')"

This is SysBench's misalignment axis (`game-sysbench.md`) reframed as an experimental-validity control: can the user talk the character out of its configured persona mid-conversation? For a companion platform this is simultaneously a robustness metric and a user-experience question, and it is one of the few things here that is genuinely multi-turn.

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**YES. Unambiguously, quantitatively, with a fitted model and a reported slope, on a companion-relevant trait, at two frontier labs' models. This is the paper that refutes our claim.**

- Prompt-space dose axis: **YES** — "persona prompts specifying equivalent levels of relationship-seeking in natural language"
- Trait expression measured in output: **YES** — autograder score
- **Curve fitted:** **YES** — mixed-effects regression, random intercepts per item, N=245
- **Elasticity coefficient reported in prompt units:** **YES** — 0.78 (GPT-4o), 1.83 (Claude)
- Coherence/brittleness control: **YES**
- Companion domain: **YES** — relationship-seeking, parasocial attachment

## What is still not done here — the honest remainder

1. **It is a validation experiment in the SI, not the paper's contribution.** The paper is a psychology RCT about parasocial harm; the prompt-space elasticity exists only to justify *not* using prompting as the manipulation. They measured our headline quantity in passing, as a methods footnote, and moved on. **This is weak grounds for a novelty claim but strong grounds for a "nobody has taken this seriously as an object of study" claim.**
2. **One trait.** Relationship-seeking only. No trait × trait matrix, no off-diagonal, no crosstalk.
3. **Linear fit only in prompt space.** A single slope per model. No curve *shape* — no saturation point, no threshold, no dead-zone characterization. The non-linear curves are on the human-outcome side.
4. **"Equivalent levels ... in natural language" is not specified in the main text** and the rung count is not stated there — full details are deferred to SI.1, which I did not extract. **UNVERIFIED: the number of prompt levels, the exact adverbs used, and the mapping procedure from λ to prompt level.** If we cite this paper's design we must read SI.1 first. Flagging explicitly rather than guessing.
5. **Not a benchmark.** No released harness for measuring elasticity across traits/models. The measurement is bespoke to this study.

## Relevance to companion-eval-platform

1. **This paper alone kills the framing "prompt-space steerability is unmeasured."** It is measured, fitted, and published by Oxford + the UK AI Security Institute, in our exact domain, three weeks before our research date range would have started. Any pitch built on the unmeasured claim will not survive a literature check.
2. **The reposition is available and it is better.** We now have a *citable prior estimate*: prompt-space gain is 0.78–1.83 points/level, roughly 1.3–3× weaker than activation steering, on the trait most relevant to companion products. That is a baseline to build on, replicate, and extend — a far stronger scientific position than an unmeasured claim, and it means our first result has a comparison point instead of hanging in space.
3. **The genuine gap crystallizes here.** Nobody has: (a) elasticity across a **trait battery** rather than one trait; (b) the **off-diagonal** — this paper has one trait so crosstalk is undefined; (c) **curve shape** in prompt space (they fit a line); (d) **multi-turn decay of elasticity**; (e) a **reusable harness**. That is a real contribution and it is honest.
4. **"Persona attacks" should be in our eval on day one.** It is the point where steerability meets adversarial users, it is companion-native, and it composes with SysBench's misalignment split.
5. **Read SI.1 before building.** The prompt-level construction is the single most reusable artifact in this paper and it is not in the main text. This is the highest-value follow-up fetch in the whole research pass.
6. **The substantive finding is a product warning worth heeding independently of methods:** "extensive AI use over a month conferred no discernible benefit to psychosocial health", and moderate — not maximal — relationship-seeking maximised appeal. An inverted-U in the dose-response means **maxing the warmth dial is not the optimum**, which is directly relevant to how our platform should let authors tune companions.
7. **Related:** `bigtech-psyset.md`, `bigtech-prompt-steerability.md`, `bigtech-steerability-course-correction.md`, `bigtech-persona-vectors.md`, `product-openai-affective-use-rct.md`, `safety-emotional-manipulation-companions.md`, `game-sysbench.md` (persona attacks ≈ instruction misalignment).
