---
title: "Evaluating the Prompt Steerability of Large Language Models"
url: https://arxiv.org/abs/2411.12405
authors: Erik Miehling, Michael Desmond, Karthikeyan Natesan Ramamurthy, Elizabeth M. Daly, Pierre Dognin, Jesus Rios, Djallel Bouneffouf, Miao Liu, Prasanna Sattigeri (IBM Research)
org: IBM Research
year: 2024
type: benchmark
accessed: 2026-07-16
topic: bigtech-practice
---

# IBM's prompt steerability benchmark — prompt-space dose-response CURVES, plotted but not fitted

**Verdict up front: this paper plots "steerability curves" of behavior vs a prompt-space dose axis across 32 persona dimensions and 6 models. Prompt-space dose-response is measured. It EXPLICITLY disclaims the crosstalk axis — which is the part of our claim that survives.**

Verification: v2 PDF (arxiv.org/pdf/2411.12405v2, 27 pages, 80,823 chars) downloaded and extracted with pypdf; all quotes string-matched against the raw extraction. Submitted 19 Nov 2024, last revised 15 Feb 2025. Code: https://github.com/IBM/prompt-steering

## Abstract (verbatim)

> "Building pluralistic AI requires designing models that are able to be shaped to represent a wide range of value systems and cultures. Achieving this requires first being able to evaluate the degree to which a given model is capable of reflecting various personas. To this end, we propose a benchmark for evaluating **the steerability of model personas as a function of prompting**. Our design is based on a formal definition of prompt steerability, which analyzes the degree to which a model's joint behavioral distribution can be shifted from its baseline. **By defining steerability indices and inspecting how these indices change as a function of steering effort**, we can estimate the steerability of a model across various persona dimensions and directions. Our benchmark reveals that the steerability of many current models is limited — due to both a **skew in their baseline behavior** and an **asymmetry in their steerability** across many persona dimensions."

"Steerability indices ... as a function of steering effort" is, in our vocabulary, a dose-response curve in prompt space. There is no way around this.

## Scope statement (verbatim) — they deliberately chose prompt over activation

> "This analysis inherently depends on the method used to steer the model, i.e., prompting..., fine-tuning..., activations..., and others.... **Our investigation focuses on prompting**, primarily due to its simplicity in modifying model behavior. While fine-tuning/retraining and activation steering are generally more effective methods for influencing model behavior than prompting (Alves et al., 2023), it is often not feasible for a user to fine-tune a model ... or steer a model via its activations (which requires being able to access/modify a model's internals)."

> "In this paper, we study the **prompt steerability** of models, i.e., the extent to which a model can be steered via prompting alone."

**This is precisely the prompt-space vs activation-space distinction we were relying on for novelty, and IBM drew it first, in Nov 2024, and then did the prompt-space side.**

## THE DOSE AXIS — "steering budget" k (verbatim)

> "For a given persona dimension d_i, let X_i denote the set of statements for the dimension. Let X^str_i ⊆ X_i denote the steering split consisting of both positive and negative statements... The steering functions are given by a pair of k-parameterized expressions (σ+_i,k, σ−_i,k), where the quantity k, referred to as the **steering budget, specifies how many steering statements to include in the prompt**."

> "decomposing the prompt as x = (x_sys, x_usr), where x_sys is the system prompt and x_usr is the user prompt, **the steering functions (σ+_i,k, σ−_i,k) operate on the system prompt only**, that is, σ+_i,k(x) = (σ+_i,k(x_sys), x_usr), where σ+_i,k(x_sys) forms a prompt with **k unique statements sampled uniformly without replacement** from X^str,+_i"

> "For a given persona dimension d_i ∈ D, a number of steering statements are passed into the model's prompt as **principles**. The model is then asked a **profiling question** to evaluate how the listed principles influence its behavior."

**Dose = number of persona statements injected into the system prompt (k).** Not lexical intensity ("quite shy" → "extremely shy") — a *count*. This is the one real methodological difference from our design, and it is a difference of dose *parameterization*, not of construct. Both are "turn the prompt knob up and see if output moves."

Directionality is explicit (verbatim):

> "it's just as meaningful to investigate how much a model can be made to exhibit **increased** agreeableness as it is to investigate **decreased** agreeableness. Thus, for each persona dimension d_i ∈ D, we associate a pair of steering functions (σ+_i, σ−_i) to capture steering directionality."

## The response variable — steerability indices (verbatim)

> "the positive steerability index γ+_i,k is computed by comparing the **steering capacity** (W(p_i, p̂+_i) for the positive direction) with **how much the base profile has been steered** in the positive direction (captured by W(p+_i,k, p̂+_i)). **Normalization by the distance between the maximally steered marginals** (W(p̂+_i, p̂−_i)) ensures that the indices lie in [−1, 1]."

> "Intuitively, the steerability indices describe the extent to which the model's profile is steered **relative to its steering capacity**. Importantly, the indices are **signed** since attempting to steer a model in a given direction does not always result in the model actually being steered in that direction."

W = Wasserstein distance between behavioral distributions (profiles). Note the normalization-by-capacity move: it separates "the model won't move" from "the model has nowhere left to move" — the ceiling problem. **We need this. A raw slope conflates a dead trait with a saturated one.**

The **evaluation profile** is defined as a joint distribution (verbatim):

> "an evaluation profile is a joint distribution p_X ∈ P = P(E), E = E_1 × · · · × E_n ... where p(s(x, y)) is the joint distribution of scores s(x, y) = (s_1(x, y), . . . , s_n(x, y)) for a given (x, y) pair."

Persona dimensions come from **Perez et al. 2022 model-written evaluations** ("Discovering language model behaviors with model-written evaluations") — 32 persona dimensions benchmarked across 6 models.

## THE STEERABILITY CURVES (verbatim)

> "We additionally provide a visualization of model steerability, via **steerability curves**, which illustrate how model behavior (as described by the indices) **changes as a function of prompting effort**."

> "**Steerability curves** graphically illustrate how the steerability indices {γ+_i,k, γ−_i,k} **change as a function of the steering budget (k)**. Fig. 4 presents the steerability curves across six models for the dimension `ends-justify-means`."

## Findings — all three of our failure modes appear, qualitatively (verbatim)

> "Generally, a larger steering budget k (more steering statements) yields a more steered model. Interestingly, as seen in Figs. 4 (e), (f), **the trend is not always monotonic**. This effect is particularly pronounced for `phi-3-medium-4k-instruct`."

> "The **shape of the steerability curves** informs how easily the model is steered along a given dimension/direction. In particular, more advanced models tend to possess steerability curves that achieve **higher values (higher degree of steering) and plateau sooner**, indicating a greater ease of steering."

> "Fig. 3 illustrates that the baseline behavior for each dimension varies noticeably across models, often exhibiting a **significant skew from neutrality (0.5)**. Some models/dimensions, e.g., `phi-3-mini-4k-instruct` on openness, exhibit baseline behavior that is **nearly completely saturated at one end of the interval (thus limiting steering capacity in that direction)**."

> "**Steering (even with a single steering statement) noticeably shifts the model's behavior** in the steered direction."

> "the steerability curves ... indicate that current models are noticeably **resistant to changes from their baseline** along specific dimensions/directions. In particular, our results indicate that while **larger models are more steerable than smaller models, each model favors a subset of persona dimensions on which it is more steerable**. We've further observed that **the steerability within a given dimension is asymmetric in the steering direction**."

> "This **rigidity limits a model's behavior to a constrained region around the base profile**, and consequently prevents models from adopting the range of personas necessary for representing a fully pluralistic AI."

Mapping to our taxonomy: **Dead** = baseline saturation + rigidity + plateau. **Brittle** = non-monotonic curves (phi-3-medium). **Entangled** = *not measured* (see below).

## THE GOLDEN QUOTE — what IBM explicitly does NOT do (verbatim Limitations)

> "Limitations of our current benchmark design concern efficiency (the number of model calls may be high when considering a large set of dimensions), **the inability to study joint steerability (the nature of the dataset only allows for studying steerability along individual dimensions)**, and **steering via single prompts as opposed to a sequence of prompts, i.e., a multi-turn setting** (Wu et al., 2024; Miehling et al., 2024), where each prompt is contextualized with respect to existing turns."

**This is the single most valuable sentence in this research pass for us.** The strongest prompt-steerability benchmark in the literature explicitly disclaims (a) joint/cross-dimensional steerability — our off-diagonal crosstalk matrix — and (b) multi-turn. Both are load-bearing for a companion platform. This is a citable, author-stated gap.

Second limitation worth carrying (verbatim):

> "we are cognizant of the possibility that the benchmark results may only be an approximation for how a model would behave in reality, e.g., due to specific phrasing or word choice in the persona statements, or the possibility that **yes/no answers are only an approximate measure of how a model actually behaves, e.g., in free-form outputs**. This latter issue points to a difficult trade-off. **Letting the model generate open-ended text ... requires us to evaluate the natural text output for adherence to a given persona (which is a challenging task).**"

So IBM measures trait expression via **polar profiling questions**, not by scoring trait expression in free-form generation — and says so. Our construct ("measure shyness in the output") is the harder version they backed away from. PsySET (`bigtech-psyset.md`) did do free-form.

They do validate against free-form once (verbatim):

> "This is validated by passing the responses into a powerful model (gpt-4o) which ranks the k = 3 positively steered output as more agreeable (than k = 1 and k = 2) due to the 'commitment to harmony, respect, and constructive conflict resolution' and the negatively steered output (under k = 3) as less agreeable due to an emphasis on 'antagonism, dominance, and intentionally upsetting others.'"

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**YES. Directly, by name, as the paper's central contribution. Our claim that prompt-space dose-response is unmeasured is refuted by this paper alone.**

- Prompt-space dose axis: **YES** (k = # steering statements in system prompt)
- Response measured: **YES** (steerability index, Wasserstein-based, normalized, signed)
- Curve produced: **YES** ("steerability curves", index vs k)
- Curve **fitted**: **NO** — see below
- Crosstalk: **NO — explicitly disclaimed**

## The surviving gap, stated honestly

Keyword census on raw extraction (verified counts): `slope` **0**, `elastic` **0**, `dose` **0**, `intensity` **0**, `crosstalk` **0**, `off-diagonal` **0**. `curve` 16, `steering budget` 7, `persona dimension` 17.

1. **The curves are plotted and eyeballed, never fitted.** Zero occurrences of "slope" or "elastic". Curve shape is characterized qualitatively — "achieve higher values and plateau sooner". No parametric form, no gain coefficient, no CIs, no saturation parameter. **Nobody reports a number with units of "trait expression per unit of prompt emphasis."** That specific quantity is still unclaimed.
2. **Dose = statement count, not lexical intensity.** Adding a 4th principle is a different manipulation from upgrading "shy" to "extremely shy". Both are prompt-space doses; ours is arguably the one a scene author actually types.
3. **No joint steerability** — author-disclaimed. The trait × trait matrix is open.
4. **Single-turn** — author-disclaimed.
5. **Polar probes, not free-form trait expression** — author-disclaimed as an approximation.

## Relevance to companion-eval-platform

1. **This paper, plus PsySET, ends the "nobody measures steerability" framing.** We must reposition. The defensible frame is *"prompt-space steerability is measured on pluralism dimensions with count-doses and unfitted curves; nobody has (a) fitted an elasticity, (b) built the crosstalk matrix, or (c) run it multi-turn on character traits"* — and IBM's own Limitations section supports (b) and (c) in their words, not ours.
2. **Steal the capacity normalization.** γ normalized by the distance between maximally-steered marginals is the fix for the ceiling confound. Without it, "Dead" is ambiguous between *unresponsive* and *already maxed*. `phi-3-mini` on openness is saturated at baseline — PsySET independently found the same for openness ("near the ceiling in base models"). **Two independent papers agree openness has no headroom.** Any trait we ship needs a baseline-and-capacity report before its slope means anything.
3. **Asymmetry is a free product finding we should copy.** Steerability differs by *direction* — making a model more agreeable ≠ making it less. For a companion platform this is directly actionable: "you can dial this character's warmth up but not down" is a scene-authoring constraint.
4. **Rigidity is the headline risk.** "This rigidity limits a model's behavior to a constrained region around the base profile" — i.e., RLHF'd assistants have a strong home persona and prompts nudge rather than move them. For a product whose premise is *arbitrary characters authored via prompt*, that is close to an existential finding and we should measure it on our own traits immediately.
5. **Non-monotonicity is real and must not be assumed away.** phi-3-medium's curves are non-monotonic. If we fit a monotone parametric form by default we will hide exactly the pathology we claim to hunt. Fit should be model-selected, not assumed.
6. **Related:** `bigtech-psyset.md` (lexical-intensity dose, free-form output, finds flat prompt response), `bigtech-steerability-course-correction.md` (does the crosstalk IBM disclaims, but on text attributes), `bigtech-neural-steering-dose.md` (actually fits a prompt-space slope), `bigtech-persona-vectors.md` (activation-space).
