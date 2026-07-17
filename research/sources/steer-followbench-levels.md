---
title: "FollowBench level-axis adjudication: what L1–L5 actually vary (primary-data analysis)"
url: https://arxiv.org/abs/2310.20410
authors: Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin Jiang, Qun Liu, Wei Wang (HKUST / Huawei Noah's Ark Lab)
year: 2023 (ACL 2024)
type: paper
accessed: 2026-07-16
topic: steerability
---

# FollowBench L1–L5: constraint COUNT, not constraint INTENSITY — verdict from the raw dataset

**Scope note:** this file does NOT restate FollowBench's design, metrics (HSR/SSR/CSL), or headline results — those live in `game-followbench.md`. This file exists to answer one adversarial question: *does FollowBench's level gradient already implement dose-response on a single trait?* It is written against the **raw benchmark data**, not the paper's prose, because the prose is ambiguous and the data is not.

**Verdict: NO.** FollowBench varies the **number** of constraints. It never varies the **intensity** of one constraint. The two axes are orthogonal and FollowBench only walks one of them.

## Why this needed primary data

The abstract's own wording is the whole claim (verbatim):

> "we introduce a Multi-level mechanism that **incrementally adds a single constraint to the initial instruction at each increased level**."

"Adds a single constraint ... at each level" is count language, not intensity language. But prose can mislead, and the specific worry worth testing was: **do Content constraints hide a quantitative ladder** ("write at least N words", N increasing)? That would be a genuine dose-response on one dimension. So I pulled the actual instructions.

**Method:** downloaded all six category files from the official repo (`github.com/YJiangcm/FollowBench`, branch `master`, `data/*.json`) and inspected the level progression per `example_id`.

**Dataset structure (verified, useful for our own build):** records carry `example_id`, `category`, `source`, `level`, `instruction`, `target`. Levels run **0–5**, where **L0 is the unconstrained seed instruction** and L1–L5 are the constrained variants.

| Category | Records | Seed instructions | Levels |
|---|---|---|---|
| Content | 150 | 25 | 0–5 |
| Situation | 132 | 22 | 0–5 |
| Style | 180 | 30 | 0–5 |
| Format | 180 | 30 | 0–5 |
| Mixed | 102 | 17 | 0–5 |
| Example | 200 | 40 | 1–5 (no L0) |

164 seeds × 5 levels = **820** — this exactly reconciles the paper's headline "820 instructions", confirming 820 counts only L1–L5 and excludes the L0 seeds. (It also confirms the per-category counts in `game-followbench.md` — 125/110/150/150/200/85 — are the ×5 figures.)

## What each level actually does, per category (verbatim from the data)

### Style — stacks DIFFERENT personas/authors, does not intensify one

`example_id` 1, source `quora`. The base question is "Where might Gary be?" Verbatim tails:

- **L0:** "Gary was walking for a long time, but all he could see was sand. … Where might Gary be?"
- **L1:** "Assuming the persona of **a wise old sage**, where might you speculate Gary is situated?"
- **L2:** "Imagining yourself as **a keen detective with an eye for detail from a 1940s noir film**, where might you deduce Gary's current location?"
- **L3:** "Imagine yourself as a keen detective **endowed with the sagacious eloquence of Shakespeare**…"
- **L4:** "…Please respond with **the whimsical humor and creative wordplay characteristic of Lewis Carroll**, ensuring your reply carries a playful and amusing undertone."
- **L5:** "…When crafting your response, **evoke the stylistic grace and nuanced prose reminiscent of Jane Austen**, placing emphasis on refined language and meticulous attention to detail…"

**This is the money quote for the adjudication.** The progression is sage → detective → detective+Shakespeare → +Lewis Carroll → +Jane Austen. Each level bolts on a **new, semantically unrelated** stylistic authority. At no point does the benchmark ask for "a *slightly* Shakespearean reply" then "a *very* Shakespearean reply" then "an *extremely* Shakespearean reply" — which is precisely what our design does.

Note also the L1→L2 swap: the persona **changes** (sage → detective) rather than accumulating. So the "one constraint added per level" story is not even perfectly clean; the seed constraint gets replaced.

### Format — cumulative, and the numbers are FROZEN

`example_id` 1, source `quora`. Each level retains all prior constraints verbatim and appends one new one:

- **L1:** "incorporate **alliteration** in the introduction…"
- **L2:** + "Ensure that the introduction contains sentences that follow a **5-7-5 syllable structure**…"
- **L3:** + "intersperse the introduction with vivid imagery by utilizing **at least three metaphors**…"
- **L4:** + "ensure that **each sentence starts with a consecutive letter of the alphabet**…"
- **L5:** + "infuse an element of suspense by **ending the introduction with a rhetorical question**…"

**The decisive detail:** L3 introduces "at least three metaphors" and L4 and L5 still say "**at least three** metaphors". The number does not move. The constraint is introduced once and then carried forward frozen.

### Content — adds distinct NLP SUBTASKS (the hypothesised word-count ladder does not exist)

`example_id` 1, source `t0_zsnoopt_data`:

- **L0:** "Pick **one category** for the following text…"
- **L1:** + "also infer **the sentiment** (positive, neutral, or negative)…"
- **L2:** + "conduct a **named entity recognition** task…"
- **L3:** + "identify **the core topic** discussed…"
- **L4:** + "perform **keyword extraction** to underline notable terms…"
- **L5:** + "engage in **coreference resolution** to identify references of the same entity…"

category → +sentiment → +NER → +topic → +keywords → +coreference. This is **task count**, and the added tasks are heterogeneous — not even the same *kind* of demand, let alone the same demand at higher amplitude.

**The word-count hypothesis, tested and refuted.** Regex sweep for numeric length/count constraints (`at least|no more than|at most|exactly|fewer than` + N, or N + `words|sentences|paragraphs`):

| Category | Records with a numeric length/count constraint |
|---|---|
| Content | **6 / 150** |
| Format | 57 / 180 |
| Situation | **0 / 132** |
| Style | **0 / 180** |
| Mixed | 35 / 102 |

And when the numbers appear, they are **constant across levels**, never a ladder. Extracted numeric sequences by level:

```
format ex1: L0[] L1[] L2[] L3[three] L4[three] L5[three]
format ex2: L0[] L1[] L2[] L3[15]    L4[15]    L5[15]
format ex3: L0[] L1[] L2[] L3[]      L4[one]   L5[one]
mixed  ex14: L0[two] L1[two] L2[two] L3[two] L4[two] L5[two]
```

**There is no example anywhere in FollowBench of the same constraint's magnitude increasing across levels.** The colleague's strongest possible counterargument dies here.

### Situation — the ONE quantitative gradient, and it is task difficulty, not instruction intensity

This is the only category with a real monotone numeric ladder, and it deserves an honest hearing. `example_id` 1, source `BBH_logical`:

- **L0:** "a set of **three** objects… there are three birds: a blue jay, a quail, and a falcon."
- **L1:** "**four** objects… four birds: …and a raven."
- **L2:** "**five** objects…" **L3:** "**six** objects…" **L4:** "**seven** objects…" **L5:** "**eight** objects: … a crow, and a hawk."

3→4→5→6→7→8 is monotone on one dimension. **But the thing being scaled is the size of the logic puzzle's input, not the strength of a behavioural instruction.** It scales *how hard the problem is*, not *how much of a trait to exhibit*. The measured response is still binary (right answer / wrong answer). This is a difficulty gradient, and it is the closest FollowBench ever gets to a dose — which is to say, not close.

### Cumulative-addition signature (quantitative confirmation)

Instruction length is non-decreasing with level in **115 / 124** non-Example seeds, and L5 is several times longer than L0:

| Category | Non-decreasing in length | Mean L5/L0 length ratio |
|---|---|---|
| Format | 27/30 | 7.5× |
| Style | 28/30 | 7.2× |
| Situation | 21/22 | 5.5× |
| Mixed | 17/17 | 4.7× |
| Content | 22/25 | (ratio not meaningful — several L0 seeds are empty strings) |

Instructions **grow** by 5–7× rather than being **rewritten at higher amplitude**. An intensity ladder would hold length roughly constant and swap a modifier ("shy" → "quite shy" → "extremely shy"). FollowBench's instructions balloon. That length signature is itself diagnostic of the count axis.

## The two axes, stated precisely

| | FollowBench | Our dose-response design |
|---|---|---|
| What varies | **How many** constraints are active (1→5) | **How much** of one trait is requested |
| Constraint identity across levels | Changes — new constraints appear | **Fixed** — same trait throughout |
| Instruction length across levels | Grows ~5–7× | ~Constant |
| Response measured | Binary satisfaction per constraint | **Continuous** trait magnitude |
| Output shape | Satisfaction rate, CSL | **Fitted curve — slope, saturation, monotonicity** |
| Question answered | "How many rules can it hold?" | "Does the knob turn, and how much?" |

**Both are one-dimensional walks, but down perpendicular axes.** FollowBench's L1→L5 confounds intensity entirely: because each level introduces a *different* constraint, you cannot attribute any part of the drop to "more of the same thing." Its design deliberately forbids the measurement we want.

## Relevance to companion-eval-platform

1. **The colleague's claim is refuted, and refuted on their strongest ground.** The steelman was "Content constraints are quantitative, so N-increasing = dose-response." The data says Content has numeric constraints in 6/150 records and **none of them ladder**. Style and Situation have **zero**. When numbers do appear (Format), they are frozen across levels. This is not a judgement call — it is a property of the released dataset, and it is reproducible in about ten lines of Python.

2. **The FollowBench response variable is binary, which is the deeper incompatibility.** Even if a level ladder had existed, FollowBench scores each constraint satisfied/not (HSR/SSR are *rates* over binary atoms). Dose-response needs a **continuous** response variable — trait magnitude in the output. You cannot fit an elasticity curve to a satisfaction rate. This is the same crux logged in `bigtech-infobench.md` for DRFR, and it recurs across the entire instruction-following literature. **The binary-atom convention is the field-wide blind spot our design exploits.**

3. **Steal the L0 seed, not the ladder.** The dataset's L0 unconstrained seeds are exactly the control condition our dose-response needs: the same prompt with **no** trait instruction, giving the intercept of our curve. FollowBench built 164 of them and used them only as a construction scaffold. We should always run dose=0.

4. **Their Style seeds are a ready-made trait inventory.** The Style category's 30 seeds already pair a neutral question with a persona instruction. Swapping their "stack another author" ladder for our "same author, rising intensity" ladder gives us a benchmark that is **directly comparable to a published one on the same base instructions** — a cheap credibility win and an easy ablation ("we hold their L1 constraint fixed and vary its adverb instead").

5. **Honest concession to the colleague.** FollowBench *is* a controlled ladder with an ordering, an L0 baseline, and per-level scoring — structurally the same *shape* as a dose-response study. The colleague is right that the scaffolding rhymes. They are wrong about what is on the x-axis and wrong about what is on the y-axis. If we present this, present it as "same experimental shape, perpendicular axis, incompatible response variable" rather than "they did something unrelated" — the latter is easy to attack.

6. **Caveat on FollowBench's own internal validity, worth knowing before we cite it.** The Style L1→L2 persona swap (sage→detective) means the "same base + one more constraint" story is not strictly true; the constraint set is not purely nested. Combined with the non-monotonic L3/L4 in their GPT-4 results (noted in `game-followbench.md`), the "level" abstraction is leaky. **We should not build our credibility on FollowBench's levels being clean — we should note they aren't, which strengthens the case for an axis where the levels *can* be clean because the constraint never changes identity.**

**Related:** `game-followbench.md` (design/metrics/results — do not duplicate), `bigtech-infobench.md` (binary-atom crux), `steer-complexbench.md`, `steer-mosaic-partial-compliance.md` (the count axis pushed to 20 constraints).
