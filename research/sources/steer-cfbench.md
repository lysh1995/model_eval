---
title: "CFBench: A Comprehensive Constraints-Following Benchmark for LLMs"
url: https://arxiv.org/abs/2408.01122
authors: Tao Zhang, Yanjun Shen, Wenjing Luo, Yan Zhang, Hao Liang, Fan Yang, Mingan Lin, Yujing Qiao, Weipeng Chen, Bin Cui, Wentao Zhang, Zenan Zhou (PKU / Baichuan Inc.)
year: 2024 (ACL 2025)
type: benchmark
accessed: 2026-07-16
topic: steerability
---

# CFBench — the field's most exhaustive constraint TAXONOMY, and it still has no intensity knob

**Why this file matters:** CFBench is the widest net anyone has cast over "kinds of constraints" — **10 primary categories, 25+ subcategories**, built from real user data. It is therefore the best possible test of the claim *"surely someone has a category for constraint intensity."* They do not. The taxonomy that tried hardest to be complete has no degree/magnitude dimension. That is a strong negative result for the field and a positive one for us.

It also contains two categories — **Contradictory** and **Rule** — that touch our conflict sub-claim.

## Scale

- **1,000 curated samples**, split **500 Easy Set / 500 Hard Set**
- **20 domains**, **200+ real-life scenarios**, **50+ NLP tasks**
- Constraints drawn from real user instructions rather than synthesised, and "each constraint is seamlessly integrated within the instructions" (i.e., not bolted on as an obvious suffix)

## The 10 primary constraint categories (verbatim structure)

1. **Content** — Lexical, Element, Semantic
2. **Numerical** — Word Count, Sentence Count, Paragraph Count, Document Count
3. **Stylistic** — Tone/Emotion, Form/Style, Audience-specific, Authorial
4. **Format** — Fundamental, Bespoke, Specialized
5. **Linguistic** — Pragmatic, Syntactic, Morphological, Phonological
6. **Situation** — Role-based, Task-specific, Complex Context
7. **Example**
8. **Inverse**
9. **Contradictory**
10. **Rule**

**Read categories 2 and 3 together — this is the decisive observation.** CFBench has a **Numerical** category (Word Count, Sentence Count…) and a separate **Stylistic** category (Tone/Emotion, Authorial, Audience-specific). Quantity is quantified; **style is not**. There is no "Stylistic → Intensity" subcategory. The taxonomy can express *"write 300 words"* and *"write in a formal tone"* — but it has **no cell for *"write in a moderately formal tone"* vs *"write in an extremely formal tone."*** The magnitude axis exists in the taxonomy only where the constraint is trivially countable, and vanishes exactly where the trait is behavioural — which is precisely where our companion product lives.

## Metrics (verbatim definitions)

- **CSR (Constraint Satisfaction Rate)** — "average satisfaction across individual constraints within instructions"; each constraint independent. (= FollowBench SSR, InFoBench DRFR shape)
- **ISR (Instruction Satisfaction Rate)** — "whether all constraints in an instruction are satisfied"; **binary: 1 if all met, 0 otherwise**. (= FollowBench HSR, IFEval prompt-level)
- **PSR (Requirements Priority Satisfaction Rate)** — the novel one. Incorporates **prioritisation**: if all *primary* requirements are met, score = **0.5 + 0.5 × (average secondary satisfaction)**; **PSR = 1 only if that score exceeds 0.8**, else **PSR = 0**.

Constraint satisfaction is scored **binary** (s_ij ∈ {0,1}). PSR introduces a *weighted average* over binary atoms and then **re-thresholds it back to binary at 0.8**. This is worth pausing on: **CFBench builds a continuous quantity and then throws the continuity away.** It is the clearest illustration in the literature of the field's reflex toward binary reporting.

Construction: complex instructions are decomposed "into multiple simple, independent checkpoints," each annotated with **constraint type and priority level**, enabling assessment "from the user's perspective."

## Results

**Top models, PSR (Full Set):**

| Model | PSR |
|---|---|
| GPT-4o | **0.735** |
| Claude-3.5-Sonnet | 0.723 |
| Qwen2-72B-Instruct | 0.705 |
| DeepSeek-V2 | 0.696 |
| GLM-4 | 0.694 |

**Hard Set collapse: GPT-4o falls to 0.582 PSR** (from 0.735 on the Full Set) — "indicating substantial room for improvement."

## Verdict against our design

| Our construct | CFBench? |
|---|---|
| Dose axis (intensity of one trait) | **NO** — no magnitude modifier anywhere in a 25+ subcategory taxonomy |
| Continuous response | **NO** — binary atoms; PSR's partial credit is re-thresholded to {0,1} at 0.8 |
| Curve / slope | **NO** |
| Conflict | **PARTIAL** — a "Contradictory" category exists, but is not graded |
| Priority / weighting | **YES** — primary vs. secondary requirements (novel, and useful to us) |

## Relevance to companion-eval-platform

1. **This is the best single citation for "the field has no intensity axis."** Not because CFBench is the most famous, but because it is the most *exhaustive*: 10 categories, 25+ subcategories, mined from 200+ real scenarios, explicitly designed for comprehensiveness. If an intensity/degree dimension were a natural way to think about constraints, **this** taxonomy would have it. It doesn't. That is a much stronger argument than "we searched and found nothing" — it is "the people whose job was to enumerate everything didn't enumerate it."

2. **The Numerical/Stylistic asymmetry is the argument in miniature, and it is quotable.** The field quantifies what is trivially countable (word count) and leaves behavioural traits binary (tone: present/absent). **Our contribution is putting a number on the axis where counting is hard — which is exactly the axis a companion character lives on.** This one contrast makes the novelty case in two sentences.

3. **PSR's design is a cautionary tale we should cite explicitly.** CFBench *had* a continuous score in hand — `0.5 + 0.5 × avg(secondary)` — and then **thresholded it at 0.8 to force it back to binary**. That is the field's binary reflex made visible in a formula. **We should hold the line and report the continuous quantity.** When someone asks "why not just threshold?", the answer is: thresholding destroys the slope, and the slope is the whole measurement.

4. **Steal requirement prioritisation — it maps onto companions cleanly.** Primary vs. secondary requirements is a real product concept for us: a character's *core* traits (must never break) vs. *flavour* traits (nice to hold). A scene author should be able to mark which is which, and our eval should weight accordingly. CFBench gives us a validated annotation scheme and a formula, and we can use their primary/secondary split while refusing their final threshold.

5. **"Contradictory" and "Inverse" are relevant to the conflict sub-claim, but shallow.** CFBench includes contradictory constraints as a *category of instruction*, not as a *graded conflict axis* — a constraint set either contains a contradiction or doesn't. Combined with `steer-instruction-hierarchy.md` (binary aligned/misaligned), the picture is consistent: **the whole field treats conflict as a discrete event, never as a continuum of pressure.** Two independent literatures, same gap.

6. **The Hard Set drop (0.735 → 0.582) is a useful calibration number.** Frontier models lose ~21% relative on harder real-world constraint sets. Our companion scenes are closer to CFBench's Hard Set than its Easy Set. Combined with FollowBench's CSL ≈ 3.3 (`game-followbench.md`), the prior for "our scenes are being violated constantly" gets stronger and is now supported by two independent benchmarks with different methodologies.

7. **Honest caveat.** Numbers above come from the arXiv HTML v1 (`arxiv.org/html/2408.01122v1`) via an extraction pass; the ACL 2025 camera-ready (`aclanthology.org/2025.acl-long.1581/`) may differ. The PSR formula and the 0.8 threshold are the load-bearing details — **re-verify those against the camera-ready before we put them in a paper.**

**Related:** `bigtech-infobench.md` (DRFR/binary crux), `steer-complexbench.md` (composition), `steer-followbench-levels.md` (count axis), `steer-instruction-hierarchy.md` (conflict), `steer-mosaic-partial-compliance.md` (the one benchmark that keeps its partial credit).
