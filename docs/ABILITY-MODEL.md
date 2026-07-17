# What makes a roleplay model good — the ability model

**This is the spine the benchmark catalogue was missing.** [BENCHMARKS.md](BENCHMARKS.md) §0.5
admits the catalogue measured only *ways to be bad*. This document is the positive construct:
what "good" actually decomposes into.

Framework origin: the project lead. Extensions and operationalization below.

---

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

### L2.2 — Steerability ★★ **the property this platform assumes and never tests**

> **A variant *is* a prompt. If the model isn't steerable, the entire variant lifecycle is a
> ritual.** We would be shipping prompt changes to a model that ignores prompts, measuring the
> noise, and calling it a decision.

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
