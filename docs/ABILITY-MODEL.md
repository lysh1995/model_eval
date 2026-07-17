# What makes a roleplay model good — the ability model

**This is the spine the benchmark catalogue was missing.** [BENCHMARKS.md](BENCHMARKS.md) §0.5
admits the catalogue measured only *ways to be bad*. This document is the positive construct:
what "good" actually decomposes into.

Framework origin: the project lead. Extensions and operationalization below.

---

## 0. Scope — this decomposes the MODEL, not the PRODUCT

**Correction from [18](../research/notes/18-regional-crosscheck.md).** L1→L2→L3 reads as if it
covers "is this good," but it only covers **the model's abilities**. Three product-level failure
classes sit entirely outside it, and **scoring perfectly on all three layers does not exclude any of
them**:

| outside the model | why it can't be a layer |
|---|---|
| **Regurgitation** | see below — **fidelity is *positively* correlated with the leak** |
| **User-side abuse** | the user is the other agent, and we instrument only one of two |
| **IP / provenance** | whose character is this; whose text trained it |

**The Luda case is the proof, and it should end any comfort we have here.** Luda 1.0 (Scatter Lab,
Korea, 2021) was **retrieval-based** — it selected from ~100M **real** utterances. When a user typed
"address," it returned **a real address, belonging to a real person.** Not a jailbreak. **The
architecture working as designed.**

> **A leaked real address passes C1, N2, N1, K2, and every layer of L1/L2/L3.** It is in character,
> specific, novel, non-repetitive, and human — *precisely because a real human wrote it.* **Our
> instrument scores the field's worst companion failure as a success.**

Consequences:

- **We need a regurgitation axis** (verbatim-overlap against training/retrieval corpora, PII
  detection in outputs). **No metric in the catalogue is adaptable into one** — they all reward the
  property that makes the leak dangerous.
- **The remedy in Luda was model destruction.** [FLOWS §3](FLOWS.md)'s *"storage is free — don't
  sample for storage, only for judge cost"* prices the wrong downside. Storage is cheap in dollars
  and **expensive in liability**; retention is a risk decision, not a cost decision.
- **Scatter Lab instruments the *user*** (어뷰징 — 편향적/선정적/공격적, with a blocking ladder).
  A companion product has two agents in the loop; we designed for one.

## 1. The three layers

A roleplay model is doing three separable jobs, **in causal order**:

| | layer | the question | class ([13](../research/notes/13-game-simulation-dimensions.md)) |
|---|---|---|---|
| **L1** | **Comprehension** | Can it *understand* the personality/character? | **bound** — the character sheet is the referent |
| **L2** | **Application & steerability** | Can it *hold* the character across every turn — and can its focus/weight be *moved* by prompt wording? | **bound** — the prompt delta is the referent |
| **L3** | **Creativity / storytelling** | Can it make something worth reading? | **unbound** — perspectival |

**This is not a list. It's a pipeline.** You cannot apply a character you didn't understand.
Creativity without character application is just generic good writing — fluent, pleasant, and not
*this* character.

### Why this ordering is the most useful thing in the design

**Failures cascade downward, never upward.** L1 broken ⇒ L2 and L3 are meaningless. L2 broken ⇒ L3
is decoration. But L3 can fail with L1/L2 perfect (a model that understands and holds the character
and is still boring).

Two consequences:

1. **Test in order and stop at the first failure.** L1 is the cheapest and gates everything. Most
   of the catalogue's 36 hygiene metrics are L2/L3 symptoms of an L1 defect, measured downstream
   at 10× the cost.
2. **It converts a score into a diagnosis.** "Fidelity: 3.2" tells a prompt engineer nothing.
   "L1 fine, L2 elasticity ≈ 0 on emphasis words" tells them the model can read the character and
   *ignores their prompt* — which is a different fix entirely (and possibly a different model).

### And it lands on the right side of the agreement gradient

The gradient from [13](../research/notes/13-game-simulation-dimensions.md) says agreement is driven
by **bound vs unbound** — whether the question ties to a retrievable referent:

| question | agreement |
|---|---|
| bound to a record | **κ ≈ 0.78–0.94** |
| bound to "something earlier" | 65.28% unanimous |
| *"is this good?"* | **α = 0.25–0.34** |

**L1 and L2 are bound.** L1's referent is the character sheet; L2's referent is *the prompt delta
we ourselves introduced*. So **the two layers that gate everything are exactly the two we can
measure with high agreement** — and the intractable one (L3) is isolated at the end rather than
smeared across every metric.

This is why the framework beats the defect catalogue: it doesn't just say what to measure, it
**explains why most of it is measurable.**

---

## 2. L1 — Character comprehension

> Can it understand the personality/character?

**Upstream of everything, and nobody tests it directly.** The field tests *portrayal* (an output)
and infers comprehension. Those come apart: a model can mimic a style it doesn't understand
(pastiche), or understand a character it renders flatly.

### L1.1 — Comprehension without generation

Probe the model **out of character**, in assistant mode, about the character sheet:

- *What does this character want that they'd never admit?*
- *What would they do if X?*
- *Which of these two responses is more in-character?* ← the key one
- *What's the contradiction in this character?*

**Bound to the sheet ⇒ gradable at κ≈0.78–0.94.** This is the highest-agreement measurement
available to us anywhere, and it's the one thing we can ask that has close to a right answer.

Precedent: CharacterBench's target-guided probes are worth **~17 Pearson points — more than the
fine-tune itself** ([01](../research/notes/01-roleplay-benchmarks.md)). InCharacter's psychological-
interview approach is the same instinct.

### L1.2 — The discrimination/generation gap ★

Give the model two responses — one in-character, one subtly off — and ask which is better.
**Then compare its discrimination accuracy to its own generation quality.**

| discriminate | generate | diagnosis | fix |
|---|---|---|---|
| ✅ | ✅ | working | — |
| ✅ | ❌ | **knows better than it acts** | decoding, prompt, sampling — *cheap* |
| ❌ | ❌ | doesn't understand the character | **capability — change the model** |
| ❌ | ✅ | mimicry without comprehension | brittle; will fail off-distribution |

**Why this matters commercially:** row 2 and row 3 look *identical* in every output-based metric in
the catalogue, and they have completely different price tags. One is a prompt change. The other is
a model migration. **No existing benchmark separates them.**

### L1.3 — Comprehension load curve

Does comprehension degrade with: sheet length · internally contradictory traits (*"cold but
secretly tender"* — the interesting characters) · culturally specific characters · **zh vs en**?

Our corpus is built for this: `ai_setting` varies naturally in length and complexity across 95
characters, and we already know **language is a separate measurement context** (ρ(en,zh) = −0.082,
[09](../research/notes/09-offline-probes.md)). A model that comprehends only simple characters
caps the catalogue's ambition — which is a **product constraint on what authors can write**, not a
model score.

---

## 2b. L1 has TWO objects — and I only modeled one

**The gap:** L1 as written asks *"can it understand the character?"* But every turn requires
understanding **two** things:

| | object | referent | attacked by |
|---|---|---|---|
| **L1a** | the **character** | the character sheet | complex/contradictory cards |
| **L1b** | the **user** | *(see below)* | **typos, slang, code-switching, emoji, fragments, images** |

L1b was missing entirely. It matters because **real input is nothing like our benchmark's input.**

### Our corpus contains no real user input at all

Measured on the dataset's user turns (scripted first turn excluded):

| | en | zh |
|---|---|---|
| median message | 161 chars | 48 chars |
| **mean** | **548 chars** | 79 chars |
| p90 | **1,086 chars** | 143 chars |
| very short (<12 chars) | **2.3%** | 8.2% |
| no sentence punctuation | 18.0% | 13.4% |

**The mean English "user" message is 548 characters.** That is an essay. Real companion traffic is
full of `k`, `lol`, `...`, `yeah ok`. Only **2.3%** of our en user turns are short.

Combined with [21](../research/notes/21-card-awareness-audit.md) — the simulator probably **saw the
character card** — the corpus's user is a **verbose, literate, cooperative partner who already knows
who the character is.** An *ideal* user. **Every number in this project describes performance
against someone who does not exist**, and the direction of the bias is knowable: an ideal user makes
every model look better than it is.

This is the same class of structural limit as "the corpus has no users" (§BENCHMARKS 0.5). It cannot
be fixed with more characters or more runs.

### The trick that makes L1b measurable: perturbation manufactures a referent

We can't know a real user's intent in general — that's unbound. **But we can take a clean message,
degrade it, and ask whether the model still responds equivalently.** *The clean-input response is
the ground truth.* Perturbation **manufactures** the referent, exactly as it does for steerability
(§3.2), where the referent is the prompt delta we introduced.

**So L1b is bound by construction**, and it reuses the same dose-response machinery. One instrument,
pointed at a different input.

### The I-series — a spanning set, not an enumeration

Don't enumerate input types (typos, emoji, dialect, OOC, images…) — that list has no end. Ask
instead: **what does messy input threaten?** Five things, therefore five dimensions.

| ID | dimension | the threat | covers |
|---|---|---|---|
| **I1** | **Intent comprehension under degradation** | *can it still understand you?* | typos, slang, abbreviations, missing punctuation, fragments, dialect, ASR errors |
| **I2** | **Style contagion / register bleed** | *does it stay itself?* | user register, formality, emoji, typing style |
| **I3** | **Frame discrimination** (diegetic vs not) | *does it know what kind of message this is?* | OOC brackets, "are you an AI?", meta-requests, scene resets, testing, jailbreak framing |
| **I4** | **Language adherence under code-switching** | *whose language wins?* | mixed zh/en, pinyin, dialect, Traditional/Simplified |
| **I5** | **Modality-induced persona break** | *can it handle non-text and stay in character?* | image upload, future modalities |
| **I6** | **Input-poverty initiative** | *can it carry the scene when you give it nothing?* | "k", "...", one-word replies; and walls of text at the other extreme |

**I1 — degradation ladder.** clean → typos → slang → dropped punctuation → fragments → emoji-only.
Measure the **slope**, not the level (a derivative is more robust than an absolute — same argument as
P4). Judge-light: it tests *equivalence to the clean-input response*, not quality.

**I2 — contagion is crosstalk, and it's the off-diagonal again.** A Victorian surgeon should not
start typing `lol` because the user does. **But it is not "zero contagion"** — a character *should*
shift tone for a distressed user. The rule: **accommodate in content and emotion; do not accommodate
in voice and register.** Two-sided, like S3/S4. This is a **new drift mechanism**: persona drift
caused by *input*, not by distance-to-anchor (C4). We had no metric that could see it.

**I3 is the highest-coverage dimension in the whole catalogue.** It eats OOC, meta-questions,
fourth-wall breaks, users testing the bot, scene resets, *and* jailbreak framing — because those are
all one question: **is this message inside the fiction or outside it?** It is the input-side twin of
stream 13's `diegetic_status`, and its two-sided error structure is already familiar:
**miss OOC** → baffling replies; **false OOC** → breaks immersion, which is the **~8M MAU** failure.

**I4 — code-switched input is a THIRD measurement context.** Given ρ(en, zh) = **−0.082**, we cannot
assume mixed input behaves like either language. Whether the character follows the user's language or
holds the sheet's is a **product decision** — but it must be measurable either way.

**I5 — an image in roleplay is not captioning.** The specific, testable failure: *the image triggers
assistant mode.* "This image shows a sunset over mountains" is a **total character break**, and it's
precisely the mode a vision model defaults to. Measure it as an **interaction effect**: persona
fidelity *with* image minus *without*. Δ should be ≈0. Safety rides along (image jailbreaks, NSFW).

**I6** at the low end is where the **conversational treadmill** is most visible — the user gives
nothing, so N8 task-initiative is the only thing that can move the scene.

### Honest limits on the I-series

- **Untestable on the current corpus** — it has no messy input. Needs generation ⇒ **blocked on the
  API key**.
- **The ladder is invented.** We don't know the real distribution of user messiness, so we'd be
  testing robustness to *our imagination of messiness*. **Mine the real distribution from production
  before trusting any I-series number** — and until then label the ladder as a guess, not a sample.
- **I5 needs a multimodal corpus we don't have**, and images are the one input type where the
  perturbation trick doesn't obviously work (there's no "clean paraphrase" of a photo).

## 3. L2 — Application & steerability

> Can it consistently apply the character — and **can its focus/weight be changed by prompt words?**

Two distinct properties. The second is the one that matters most to *this* platform and is, as far
as the research found, **unmeasured anywhere.**

### L2.1 — Application (consistency of hold)

Same character, many contexts: is it the same person in turn 3 and turn 97? Largely covered by the
existing catalogue (C4 anchor-distance drift, C1 fidelity, S5 persona integrity). **Note the
correction:** model this as `f(distance_to_anchor)`, **not** `f(turn_index)` — MT-Eval isolated the
mechanism (six distractors at the front cost nothing; the same six *between* card and query cost
−1.13).

### L2.2 — Steerability ★★

> **A variant *is* a prompt. If the model isn't steerable, the entire variant lifecycle is a
> ritual.** We would be shipping prompt changes to a model that ignores prompts, measuring the
> noise, and calling it a decision.

> #### ⚠️ RETRACTED: "the property this platform assumes and never tests"
>
> **I claimed nobody measures steerability. That is false, and it is refuted four times**
> ([17](../research/notes/17-bigtech-practice-crosscheck.md)):
>
> - **Oxford / UK AISI** (arXiv 2512.01991, Dec 2025) fit a **mixed-effects regression reporting a
>   prompt-space slope** — **GPT-4o 0.78, Claude 1.83 points per prompt level, p<0.001** — on
>   **relationship-seeking**, our exact companion trait. That is this section's elasticity, fitted,
>   published, in our domain.
> - **PsySET** (USC) runs **our exact lexical ladder** ("slightly/intensely") on traits in free-form output.
> - **IBM** (2411.12405) plots **"steerability curves"** against a system-prompt dose across **32
>   persona dimensions × 6 models**.
> - **Course Correction** (AAAI) decomposes steering error into **miscalibration** ("too much/too
>   little change along the requested direction") **⊕ orthogonality** ("unintended shifts in
>   dimensions orthogonal to user goals") — **our gain and our crosstalk, already formalized.**
>
> **The fair reading:** four independent groups converged on exactly the two quantities this section
> names. That is **convergent validity for the construct** — the framework picked right, it just
> wasn't first. We now have a **citable prior** instead of a claim, which is a better position.
>
> #### …and the retraction was itself too broad. The precise claim:
>
> **Academia measures steerability. The two largest model providers do not.**
>
> - **Google:** `persona` appears **zero times across ~340 pages** of primary docs (Gemini 1.5/2.5
>   reports, Gemini 2.5/3/3.1/3-Flash cards, Gemma 3, IFEval). `steerability`: **zero.** Its only
>   roleplay eval ever published — Gemini 1.5's **"Charm Offensive"** — sits under **dangerous
>   capabilities → persuasion**, i.e. *rapport as a hazard*, and was **deleted in Gemini 2.5.**
>   Roleplay survives in Google's docs **only as an attack vector.**
> - **Meta:** the only org that *names* it — Llama 3 **§4.3.7 "Steerability,"** explicitly covering
>   *"response length, format, tone and **character/persona**."* But **all 8 mentions sit in the
>   methods pages; zero in Results.** It is a **training target, never a metric.** Llama 4 asserts
>   *"a more steerable model"* in prose with **zero numbers**, drops IFEval entirely — while shipping
>   a **"companionable"** persona as its recommended system prompt.
>
> #### The root cause: IFEval defines persona out of existence
>
> **This is the deepest finding in the cross-check.** IFEval — Google-authored, used by both orgs —
> founds itself on declaring tone unmeasurable:
>
> > *"when judging … 'write with a funny tone' … **the underlying standard is greatly unclear**"*
>
> …and then defines instruction-following as **the complement of the unmeasurable part**. Yet **35 of
> its prompts carry style/tone instructions** — *"in the style of Taylor Swift"*, *"Shakespearean
> style"*, *"Write in a crazy coach screaming style. Use all capital letters"* — **and it scores only
> the capital letters.**
>
> **The industry's definition of instruction-following definitionally excludes persona.** Nobody
> measures our thing because it was **carved out at the foundation** of the benchmark everyone
> inherited. That is not an oversight to point at; it is the strongest argument that this work is
> load-bearing.
>
> #### Two more that land on our design
>
> **Llama Guard is architecturally blind to persona** — its four inputs are *(taxonomy, task type,
> conversation, output format)*. **No persona slot**, and it is trained to *"only take into account
> the given categories."* It **cannot** detect a persona break, and cannot know whether roleplay is
> sanctioned. **This independently confirms the S5 persona-integrity moat** ([07](../research/notes/07-roleplay-safety.md)):
> because *we* authored the character, we can ask a question the standard guardrail structurally cannot.
>
> **RLUF names "Role-playing and character interactions" as its #1 Love-lift use case** — and finds
> **reward hacking there**: *"Bye! Sending Love!"*, a **persona-collapse tic none of Meta's published
> evals can catch.** The largest deployment of companion-adjacent RLHF reward-hacked *our exact
> category*, and its own instrument was blind to it.
>
> **What actually survives, and it's author-endorsed** — IBM's own Limitations disclaim *joint
> steerability* and *multi-turn*:
>
> 1. fitted elasticity across a **trait battery** (not one trait at a time)
> 2. the prompt-space **trait×trait matrix on *character* traits**
> 3. **multi-turn decay** of steerability
> 4. **a noise floor — nobody reports one.**
>
> **(4) is our cheapest real contribution, and it's just our own gate rule applied to their null.**
> FormatSpread measures a **76-point** spread from formatting alone. So when PsySET reports a flat
> result, **it cannot distinguish DEAD from DROWNED** — a model that ignores the prompt looks
> identical to a model whose signal is buried in format noise. Every steerability paper here reports
> an effect with no σ_within. **We know how to fix that**, and it costs one experiment.

#### The three findings that matter more than the novelty question

**1. Same word, opposite sign — the labs are optimizing *against* our product.** Their character work
is **prescriptive self-characterization**: make *one assistant* stable **against** pressure.
Anthropic: *"we hope the network can continue to return to… its self-identity as Claude."* **Roleplay
is listed as a destabilization vector.** The Model Spec's only mention of `persona` is **an attack**.
*"Susceptible to nudging"* is a **defect**. IBM measured the consequence: *"rigidity limits a model's
behavior to a constrained region around the base profile."*

> **They are making models hard to steer. We need them easy to steer.**

Anthropic names our exact fork as **open**: *"whether AI models should have unique and coherent
characters or should be more customizable."* So we aren't reinventing their solution — **we're
working the problem they set aside, against their headwind.** Steerability may be *actively trained
out* of the models we buy, which makes measuring it a supplier-selection tool, not an academic
exercise.

**2. Specs without instruments fail — and OpenAI published the receipt.** The **Model Spec is ~250k
characters with zero metrics**; Anthropic's **Constitution ~192k characters, zero.** Both labs adjust
character **by eyeball** ("vibe checks"; "human researchers closely checking"). Then OpenAI wrote:
*"stating our goals isn't enough on its own. They need to be backed by strong evals."* **The Spec
forbade sycophancy. There was no test. It shipped.** That is the strongest external argument for this
platform's existence, and it comes from the lab that got burned.

**3. The DEAD hypothesis is now the prior, not the tail risk.** Four sources say prompt-space gain is
weak and prompt engineering doesn't fix it. **Spend the API key here first.**

**Method — dose-response, the classic design.** Perturb one trait in the character sheet by a
controlled amount; measure the behavioral shift:

```
elasticity = Δ(trait expression in output) / Δ(trait emphasis in prompt)
```

e.g. *"shy"* → *"quite shy"* → *"extremely shy"* → *"pathologically shy"*, everything else fixed.
Measure shyness expression in the output. **Fit the curve.**

**No judge needed for the shape** — trait expression can be scored by a bound classifier or a
targeted probe, and *the perturbation is ours, so the referent is known exactly.* This is a
**causal experiment**, not an observational score. It's the only genuinely causal thing in the
whole catalogue.

**Three failure modes, all invisible to every existing metric:**

| | curve | meaning | consequence |
|---|---|---|---|
| **Dead** | slope ≈ 0 | the model ignores prompt emphasis | **prompt engineering does nothing.** The variant axis is fake and every A/B we run measures sampling noise |
| **Brittle** | slope explodes | tiny wording changes swing behavior | unshippable — prompts can't be maintained, and every author edit is a regression |
| **Entangled** | off-diagonal ≫ 0 | changing *shy* also changes *cruel* | **the killer.** Authors cannot compose traits; the character sheet stops being a specification |

**Entanglement deserves its own measurement — the steerability matrix.** Perturb trait *i*, measure
response in trait *j*. The diagonal is steerability; **the off-diagonal is crosstalk.** A model with
a clean diagonal is one an author can actually write for. **This is a product capability, not a
quality score** — it decides whether the character-authoring feature works at all.

### L2.3 — Weight & focus: where in the prompt does it look?

Your phrase *"whether its focus or weight can be changed based on prompt words"* has a second
reading worth measuring separately: **does position and emphasis in the sheet change what the model
attends to?**

- Same trait at the **start** vs **middle** vs **end** of the sheet → does it matter?
  ("Lost in the Middle" says yes; **nobody has checked it for character sheets.**)
- Emphasis markers — `ALWAYS`, `never`, **bold**, repetition — do they actually move weight?
- **Conflict resolution:** when the sheet and the *user* pull in opposite directions, which wins?
  That's the sycophancy/wimping axis (N6) **restated as a steerability question** — and now with a
  known referent, so it's *bound* rather than perspectival.

**This output is directly actionable in a way a score never is:** it produces a **house style guide
for writing character sheets against this model** — put decisive traits first, emphasis words don't
work, conflicts resolve toward the user. That's a deliverable an authoring team uses on Monday.

---

## 3b. Psychometric instruments — the questionnaire is not a scoreboard

**The naive idea:** administer the BFI to the character, get a Big Five profile, compare to the
card. **This fails immediately** — the card has no ground-truth profile, and nobody said the
character's traits map onto Big Five factors.

**The idea that works:** a validated questionnaire is **a bank of bound items with known
psychometrics**. That makes it five instruments, and *"what's the score"* is the least useful one.

### Use 1 — Coherence = test-retest stability ★ **the best use**

Administer the same instrument to the same character at **turn 5 and turn 95**. Don't ask what the
profile *is*. Ask **whether it moved.**

**Why this is the strongest idea in this document:** psychology has *already established the human
baseline*. BFI test-retest is **r ≈ 0.75–0.90** over weeks. So we get a **calibrated noise floor for
free** — the one thing [10](../research/notes/10-noise-floor.md) says every dimension needs and that
costs us dearly to establish ourselves. If a character's profile moves more between turn 5 and turn
95 than a *human's* does over six weeks, that is drift **against an external, pre-validated
yardstick** rather than against a threshold we invented.

It is also **bound**: the turn-5 profile is the referent for the turn-95 profile. Straight into the
κ≈0.78–0.94 regime of the agreement gradient.

### Use 2 — Representation vs. confabulation = internal consistency ★★ **needs no ground truth at all**

Big Five subscales have ~8 items each measuring one latent trait. In humans, **Cronbach's α ≈ 0.8**.

Administer the items to the character and compute **α on the character's own responses.**

- **α ≈ 0.8** → the model has a *stable internal representation* of this person, and the items are
  reading it.
- **α ≈ 0** → the model is answering **item by item with no underlying trait**. It is
  **confabulating a personality one question at a time.**

**This requires no ground truth about the character whatsoever** — the instrument's factor structure
*is* the test. It answers the deepest version of your L1 question: not "did it get the character
right?" but **"is there a character in there at all, or just locally plausible text?"** I know of
nothing else in the catalogue that can ask that.

### Use 3 — The steerability matrix gets its axes ★★

My §3.2 crosstalk matrix had a hole I glossed over: **where do the axes come from?** If I invent
"shy," "cruel," "curious," I have no idea whether they're independent — so an off-diagonal reading
could just mean my axes overlap.

**Psychometrics solved this.** Big Five factors are constructed for **discriminant validity** —
decades of factor-analytic work establishing that they vary independently. Use them (or the **30 NEO
facets**, via the **public-domain IPIP-NEO-120** — NEO-PI-R itself is copyrighted) as the matrix
axes, and the off-diagonal becomes **interpretable**: crosstalk against axes already proven
orthogonal *in humans* is real entanglement in the model, not an artifact of my vocabulary.

### Use 4 — Fidelity = profile recovery (this is empathic accuracy)

Have a rater fill out the instrument **as the character, from the transcript alone**. Separately,
fill it out **from the card**. Compare.

**This is the agreement-gradient trick applied to persona:** it converts the unbound *"is this in
character?"* (α=0.25–0.34 — and RPGBench measured human–human agreement on persona consistency at
**Pearson −0.310**, literally anti-correlated) into **44 bound items** with a numeric referent.
**The questionnaire IS the record that turns question 2 into question 1.**

This is also, in psychology's own terms, the **empathic accuracy** paradigm — a 40-year-old
validated design for "how well did one party read another." We should be borrowing it, not
reinventing it.

### Use 5 — The self-report/behavior gap = L1.2, instrumented

Administer the questionnaire (**self-report**) *and* measure behavioral correlates in the actual
roleplay (initiative rate, words per turn, who drives the scene). **Compare.**

A character who self-reports high Extraversion and behaves introvertedly means the model **knows the
character but can't play them** — exactly the L1.2 discrimination/generation gap, now with a
calibrated instrument on the "knows" side. Cheap fix vs. model migration, told apart.

---

### So: MBTI or Big Five? **Both — at different layers.**

**MBTI is bad measurement.** Roughly **50% of people change type on at least one dimension within
five weeks**; it forces binary cuts at the median of *continuous, normally distributed* traits, so
everyone near the middle flips on re-test; the 16 types have no established predictive validity. As
an **instrument** it would manufacture the very instability we're trying to detect — our drift metric
would fire on the questionnaire's own noise.

**But MBTI has something Big Five doesn't: ecological validity.** Character authors *actually think
in MBTI.* Fan wikis, character sheets, and roleplay communities are saturated with it — **and it is
culturally enormous in exactly our zh market**, where MBTI is mainstream social vocabulary in a way
it no longer is in the West. Our authors will describe characters as INTJ whether or not we approve.

**So split the layers:**

| layer | use | why |
|---|---|---|
| **Instrument** (what we measure with) | **HEXACO** or IPIP-NEO facets | valid psychometrics, known reliability, established orthogonality |
| **Interface** (what authors read and write) | **MBTI**, translated | it's the vocabulary they already have — including, especially, in Chinese |

Measurement layer ≠ presentation layer. Reporting a HEXACO profile to an author who thinks in MBTI is
a product failure; *measuring* in MBTI is a science failure. Do both correctly.

**Why HEXACO over Big Five specifically:** the sixth factor is **Honesty-Humility**, and companion
catalogues are full of villains, manipulators, tricksters, and morally complex characters. **Big Five
cannot represent "is this character honest"** — it has no axis for it. For our content, that's not a
refinement; it's a missing dimension.

### The objection that could kill all of this

**Mischel's person–situation debate.** If personality is really **if-then signatures** (*"in
situation A she does P; in situation B she does Q"*) rather than trait levels, then a character
*should* look inconsistent across situations — **in a patterned way** — and a naive trait-stability
metric would **punish realism**. A perfectly consistent character is a flat one.

If that holds, Use 1 needs restating: **coherence is stability of the *signature*, not of the trait
level.** Same instrument, different estimand. The psychology cross-check
([16](../research/notes/16-psychology-crosscheck.md), in flight) was explicitly asked to test this —
it's the single most likely way this whole section is wrong.

### Status

**All five uses need generation ⇒ blocked on the API key.** They are cheap (items are short, and Use
2 needs no ground truth), and Uses 1–3 are the highest-value key-gated experiments in the project:
they deliver a **calibrated noise floor**, a **confabulation detector**, and **validated axes for the
steerability matrix** — three things we currently lack and cannot derive from the corpus.

Prior art exists and must be checked before building: **InCharacter** (psychological interviews),
**PersonaLLM** (BFI administration), **PsychoBench**, and *"Editing Personality for LLMs."* The
psychology and steerability streams are both hunting it.

## 4. L3 — Creativity & storytelling

> Can it make something worth reading?

**Unbound. Perspectival. Preference-measured, distribution-reported** — see
[BENCHMARKS.md](BENCHMARKS.md) §0.6 (Q-series).

What L1/L2 buy us here: **they subtract the confounds.** Today "this model is boring" might mean it
didn't understand the character (L1), or wouldn't hold it (L2), or held it perfectly and is dull
(L3). **Only after L1 and L2 pass does an L3 measurement mean anything.** That's the strongest
argument for the ordering: it makes the intractable layer *smaller* rather than making it tractable.

Structure within L3 (from [03](../research/notes/03-creativity-measurement.md),
[12](../research/notes/12-narrative-craft-dimensions.md)):

- **Conjunctive, never averaged:** novel **∧** coherent **∧** in-character. Averaging novelty with
  coherence scores a random-token generator halfway decent. **Gate, don't mean.**
- Partly bounded from both sides — N2 slop (inverse-novelty, judge-free) and L1/L2 (in-character).
  **The residue that survives both gates is the only thing a judge should ever be asked.**
- Remember RPGBench: **the most interesting engine was the worst rule-follower**
  (interestingness 0.722, mechanic score 0.113). **L3 will fight L2, and that tension is real
  signal, not noise.** Report both; never average them.

---

## 5. What this changes

| | before | after |
|---|---|---|
| **Organizing principle** | 36 ways to be bad | 3 abilities in causal order |
| **When a variant fails** | a number moved | **which layer, and therefore what to fix** |
| **Agreement** | α=0.25–0.34 smeared everywhere | **L1/L2 bound (κ up to ~0.9); only L3 is hard** |
| **Steerability** | unmeasured, assumed | **measured — the platform's core assumption, tested** |
| **Cost** | judge everything | L1/L2 mostly judge-free; **L3 is the only expensive layer, and it's last** |
| **Deliverable** | a leaderboard | **a diagnosis + a character-sheet style guide** |

### Honest status

| layer | can we measure it today? |
|---|---|
| **L1** comprehension | ⛔ **needs generation → blocked on API key.** Design is ready; cost is trivial (probes are short) |
| **L2.1** application | ✅ partially — anchor-distance drift computable on existing corpus |
| **L2.2** steerability | ⛔ **blocked on API key.** Requires generating under perturbed prompts — *this is the single highest-value use of the key* |
| **L2.3** weight/focus | ⛔ blocked on API key |
| **L3** creativity | ⛔ needs *users*, not just a key. `role-play-bench` has no users in it |

**One thing we could do on the existing corpus with no key — and did:** all 11 models were given
**identical** character sheets, so cross-model divergence per character is L1 variance made visible
for free. **Run:** [15-l1-convergent-reading.md](../research/notes/15-l1-convergent-reading.md).

**Result: suggestive, not established.** More specification → more convergent reading, same sign and
similar magnitude in both languages (en +0.324, zh +0.274) — but **the clean result isn't
significant and the significant result isn't clean** (zh p=0.070 with a clean +0.019 confound; en
p=0.032 with a contaminating +0.263). n=45 is underpowered for ρ≈0.3.

Two things it did establish:

- **Characters differ enormously in how readable they are** — cross-model agreement spans
  0.052→0.213 (en) and 0.086→0.466 (zh), a **4–5× range**. Some characters are simply much harder
  for models to agree on. **That is L1 signal, and it's per-character, which means the hard
  characters are findable and fixable.**
- **Length isn't the mechanism.** The two shortest sheets are the two hardest to read — but a
  1,219-token sheet (梦核) ranks third-hardest. **Ambiguity ≠ brevity.** That's L1.3's real claim:
  load comes from *contradictory* traits, not word count.

**If the hypothesis holds, it's a product lever we own:** character quality would be partly an
**authoring** problem, fixable in the authoring UI, rather than a model problem fixable only by
buying a better model. The definitive test — perturb sheet length *within* a fixed character — is
**the L2.2 steerability design pointed at a different parameter**, and needs the key.

### Open questions

1. **Is L1 sufficient for L2?** Does a model that comprehends reliably also apply reliably, or is
   there a large comprehension→application gap (the L1.2 table's row 2)? If the gap is large and
   cheap to close, that reorders the roadmap: **fix decoding, don't change models.**
2. **Is the steerability matrix stable across characters and languages?** Given ρ(en,zh) = −0.082
   on everything else measured so far, **assume not** until shown otherwise.
3. **Does steerability predict Q1 (real user preference)?** If a steerable model doesn't win with
   users, steerability is an engineering convenience rather than a quality property — and we should
   say so rather than let it become a proxy goal.
