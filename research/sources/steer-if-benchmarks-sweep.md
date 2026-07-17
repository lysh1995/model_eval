---
title: "Instruction-following benchmark sweep: CELLO, FoFo, LIFBench, RuleBench — four negative results on the intensity axis"
url: https://arxiv.org/abs/2309.09150
authors: CELLO — Qianyu He et al. (Fudan); FoFo — Congying Xia et al. (Salesforce AI Research); LIFBench — Xiaodong Wu et al.; RuleBench — Wangtao Sun et al. (CAS)
year: 2023-2024
type: benchmark
accessed: 2026-07-16
topic: steerability
---

# Four more instruction-following benchmarks — all count/complexity axes, none with an intensity knob

This file closes out the instruction-following sweep with **four negative results**, recorded together because each individually warrants a paragraph, not a page. Recording them matters: the novelty claim is only as strong as the search behind it, and "we checked these four and they don't do it" is a claim we must be able to defend by name.

**Summary verdict: none of the four vary the intensity of a single constraint. None has a continuous trait-magnitude response variable. Each walks a *different* non-intensity axis — which is itself the useful finding.**

| Benchmark | Axis it walks | Dose? | Continuous response? |
|---|---|---|---|
| CELLO | task/input complexity (8 features) | NO | NO |
| FoFo | format difficulty across domains | NO | NO |
| LIFBench | context length, phrasing, variables | NO | NO (rubric) |
| RuleBench | inferential rule complexity | NO | NO |

---

## 1. CELLO — "Can Large Language Models Understand Real-World Complex Instructions?" (AAAI 2024)

**URL:** https://arxiv.org/abs/2309.09150 · code: `github.com/Abbey4799/CELLO`

Abstract (verbatim excerpt):

> "However, they still struggle with **complex instructions**, which can be either **complex task descriptions that require multiple tasks and constraints**, or **complex input that contains long context, noise, heterogeneous information and multi-turn format**. Due to these features, LLMs often **ignore semantic constraints from task descriptions, generate incorrect formats, violate length or sample count constraints, and be unfaithful to the input text**. Existing benchmarks are insufficient to assess LLMs' ability to understand complex instructions, as they are **close-ended and simple**. To bridge this gap, we propose CELLO... We design **eight features** for complex instructions and construct a comprehensive evaluation dataset from real-world scenarios. We also establish **four criteria** and develop corresponding metrics, as current ones are **inadequate, biased or too strict and coarse-grained**."

**Verdict: NO dose.** "Complexity" here decomposes into *multiple tasks*, *multiple constraints*, *long context*, *noise*, *heterogeneous information*, *multi-turn* — every one a **count or difficulty** dimension. The failure list is telling: models "ignore semantic constraints" (binary), "violate length or sample count constraints" (count). No degree anywhere.

**The one line worth stealing:** CELLO criticises existing metrics as **"too strict and coarse-grained."** That is the field, in its own words, complaining about binary satisfaction — and then CELLO's answer was better criteria, still not a continuous trait scale. **Useful as evidence that the binary-atom convention is a known irritant the field has repeatedly failed to escape.**

---

## 2. FoFo — "A Benchmark to Evaluate LLMs' Format-Following Capability" (ACL 2024, Salesforce)

**URL:** https://arxiv.org/abs/2402.18667 · code: `github.com/SalesforceAIResearch/FoFo`

Abstract (verbatim excerpt):

> "This paper presents FoFo, a pioneering benchmark for evaluating large language models' (LLMs) ability to follow **complex, domain-specific formats**, a crucial yet underexamined capability for their application as AI agents."

Built via an **AI-Human collaborative method** across real-world formats; evaluated on Llama 2, WizardLM, GPT-4, PALM2, Gemini.

**Verdict: NO dose.** A format is matched or not; there is no "moderately JSON."

**But one finding here is genuinely important to us — arguably the most useful thing in this file:**

> **"LLMs' format-following performance is independent of their content generation quality"**

— strong overall performance does **not** predict format adherence, and "format proficiency **varies across different domains**."

**Why this matters: it is an independence/orthogonality result between two capability dimensions, established empirically.** It supports the premise underneath our entanglement work — that adherence dimensions are *separable* and can move independently of each other and of general capability. It also warns that **a model good at being a companion may be bad at holding a format constraint, and vice versa**; we must not collapse them into one adherence number. And it means **we cannot use general model quality as a proxy for steerability** — the ranking may not transfer at all. That has direct consequences for how we present per-model results.

---

## 3. LIFBench — "Instruction Following Performance and Stability in Long-Context Scenarios" (ACL 2025)

**URL:** https://arxiv.org/abs/2411.07037

Abstract (verbatim excerpt):

> "their ability to **stably** follow instructions in long-context inputs has become critical... existing benchmarks seldom focus on instruction-following in long-context scenarios or **stability on different inputs**... LIFBench comprises **three long-context scenarios and eleven diverse tasks**, featuring **2,766 instructions** generated through an automated expansion method across three dimensions: **length, expression, and variables**."

**LIFEval:** "a **rubric-based** assessment method that enables precise, automated scoring of complex LLM responses **without reliance on LLM-assisted assessments or human judgment**."

**Verdict: NO dose — but note the near-miss on the wrong axis.** LIFBench's three expansion dimensions are:
- **length** → context size (a real numeric ladder, but on *input length*, not instruction strength — same category error as FollowBench's Situation birds-3-to-8)
- **expression** → **paraphrase variation** — this is *prompt sensitivity*, our platform's noise floor, not our signal (see `steer-prosa-sensitivity.md`, `steer-multiprompt-eval.md`, `steer-worst-prompt.md`)
- **variables** → task parameter substitution

**Two things to take:** (a) **"Stability on different inputs" as a first-class metric is the right instinct and we need it** — an elasticity slope measured on one phrasing is worthless if a paraphrase moves it more than a dose step does. **LIFBench's expression dimension is the template for our noise-floor control: dose effect must exceed paraphrase variance, or we are reporting nothing.** That is a mandatory validity check on our headline claim, not an optional extra. (b) **LIFEval avoids LLM judges entirely via rubrics** — an existence proof that judge-free scoring is possible, though only for rule-checkable tasks. Our semantic traits will not get this luxury, and we should say so honestly rather than pretend our judge is as clean.

---

## 4. RuleBench — "Beyond Instruction Following: Evaluating Inferential Rule Following of LLMs"

**URL:** https://arxiv.org/abs/2407.08440

Abstract (verbatim excerpt):

> "Although Large Language Models (LLMs) have demonstrated strong ability, they are further supposed to be **controlled and guided** by [rules] in real-world scenarios to be safe, accurate, and intelligent... **no prior work has made a clear evaluation of the inferential rule-following capability of LLMs.** Previous studies... **fail to distinguish the inferential rule-following scenarios from the instruction-following scenarios.** Therefore, this paper first clarifies the concept of inferential rule-following and proposes a comprehensive benchmark, RuleBench... Our experimental results on a variety of LLMs show that they are **still limited in following rules**. We further propose **Inferential Rule-Following Tuning (IRFT)**. The experimental results show that through IRFT, LLMs can learn abstract rule-following abilities **from purely synthetic data** and then generalize to RuleBench."

Scenarios span **relation extraction, content moderation, commonsense QA, science QA, judgment prediction**.

**Verdict: NO dose.** A rule is applied correctly or it isn't — this is *logical inference over rules*, closer to reasoning than to behavioural steering. Rules do not have intensity; a syllogism is not "quite valid."

**Relevance is mostly by contrast, and it is a distinction we should adopt.** RuleBench's own framing move is to **separate rule-following from instruction-following** as distinct constructs. That is a precedent for our move: **separate trait-intensity-following from constraint-satisfaction-following.** Their argument shape — "prior work conflates two things that are actually different, so we name and benchmark the neglected one" — is exactly our argument shape, and it was publishable. Worth mirroring rhetorically.

Also: **IRFT shows abstract following behaviour can be trained from purely synthetic data and generalise.** If our platform finds companion models have poor elasticity, this is precedent that synthetic dose-response training data could fix it — a plausible downstream product story ("we don't just measure the curve, we can straighten it").

---

## Net effect on the novelty claim

**Nine instruction-following benchmarks now checked** — IFEval, InFoBench, FollowBench, SysBench, ComplexBench, CFBench, MOSAIC, plus these four (CELLO, FoFo, LIFBench, RuleBench). Every one of them varies **count, complexity, length, phrasing, format, or logical structure**. **Not one varies the intensity of a single constraint. Not one has a continuous trait-magnitude response variable.** The axes the field has thoroughly mined:

- **count** (FollowBench 1–5, MOSAIC 1–20, ComplexBench composition, CFBench)
- **turns** (SysBench, Multi-IF)
- **context length** (LIFBench)
- **phrasing** (LIFBench expression; and the whole prompt-sensitivity literature)
- **structure/dependency** (ComplexBench Chain/Selection)
- **priority/conflict** (Instruction Hierarchy, CFBench Contradictory)

**The intensity axis is empty. That is the finding, and it is now defensible by enumeration rather than by assertion.**

**Related:** `steer-followbench-levels.md`, `steer-complexbench.md`, `steer-cfbench.md`, `steer-mosaic-partial-compliance.md`, `steer-instruction-hierarchy.md`, `bigtech-infobench.md`, `bigtech-ifeval.md`, `game-sysbench.md`.
