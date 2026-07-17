# 02 — LLM-as-a-Judge: Reliability, Biases, and Methodology

**Topic:** llm-judge · **Compiled:** 2026-07-16 · **Sources:** [`../sources/`](../sources/) (14 files, `judge-*.md`)

---

## 0. TL;DR for the platform

1. **The "LLM judges match humans (85%)" claim does not survive contact with our use case.** That number is raw percent agreement, on non-tie votes only, from 2023. Chance-corrected, on realistic data, the best judge + every mitigation stacked = **κ ≈ 0.53** ([2026 mitigation study](../sources/judge-bias-mitigation-systematic-2026.md)). GPT-4 judging unconditionally **"almost never achieves 80% human agreement"** ([Trust or Escalate](../sources/judge-trust-or-escalate.md)).
2. **Style/length bias is the biggest threat to our platform specifically**, because our platform compares system-prompt variants, and "be more verbose" is a system-prompt edit. Unmitigated, our leaderboard measures verbosity. It is fixable *statistically* (BT + style covariates), not by prompting.
3. **Judges cannot be truth oracles.** GPT-4o scores **50.9% on JudgeBench** (chance = 50%), **44.2% on knowledge**. Character-fidelity-as-consistency needs programmatic checks, not a preference judge.
4. **Abstention is the highest-leverage design decision.** ~20% of pairwise items are irreducibly contested (humans agree only 81% with each other). Forcing a verdict on those manufactures noise. Build the "contested" bucket in from day one.
5. **Self-preference is causal and does not cancel by averaging.** Never let a judge grade its own family. This is a hard constraint on the judge×variant matrix.

---

## 1. The bias table

Magnitudes are as-measured in the cited source; note the **era** column — 2023-era judges (GPT-4-0613, Claude-v1) and 2025/26-era judges (Claude Sonnet 4, Gemini 2.5 Pro) behave very differently, and several canonical biases have shifted or reversed.

| Bias | Measured magnitude | Era | Mitigation (measured effect) | Residual risk |
|---|---|---|---|---|
| **Position / order** | GPT-4 consistency **65.0%**; GPT-3.5 46.2%; Claude-v1 **23.8%** ([MT-Bench](../sources/judge-mtbench-zheng.md)). CALM RR **0.566–0.832**, worsens with 3–4 options. **But 2026: ≤0.04, negligible on frontier judges** ([2026](../sources/judge-bias-mitigation-systematic-2026.md)) | 2023 severe → 2026 ~solved | Swap-and-average (2× cost); **PORTIA split-merge: +47.46% rel., GPT-4 → 98%** ([PORTIA](../sources/judge-portia-position-bias.md)); few-shot **65→77.5%**; swap augmentation at train time **+5.44pp** ([JudgeLM](../sources/judge-judgelm.md)) | **Swap increases verbosity bias (+0.07)** — mitigation is not free. Listwise (3+) re-opens it. Verify on *our* judges before spending 2×. |
| **Verbosity / length** | Naive repetition attack: Claude-v1 & GPT-3.5 **91.3% failure**, GPT-4 8.7% ([MT-Bench](../sources/judge-mtbench-zheng.md)). CALM RR 0.88–0.98. **Length coefficient 0.249 — ~8× any markdown feature** ([Style Control](../sources/judge-style-control-arena.md)). 2026: sign **reverses** to conciseness preference (−0.20 to −0.76) | mixed | **Regression adjustment (GLM/BT with length as mediator)**: AlpacaEval ρ vs Arena **0.94 → 0.98** ([LC-AlpacaEval](../sources/judge-length-controlled-alpacaeval.md)); rubric −0.11 | **Sign is model-dependent and unstable across judge versions** — cannot hard-code a direction. Over-correction risk: length may be *real* signal for "storytelling". |
| **Style / formatting** | **Baseline 0.76–0.92 — the largest single bias measured on modern judges** ([2026](../sources/judge-bias-mitigation-systematic-2026.md)). Style control moves **Grok-2-mini 6 → 18 (12 ranks)**; GPT-4o-mini 6 → 11 ([Style Control](../sources/judge-style-control-arena.md)) | 2026 severe | Best stack (S8) → **0.58 (−0.26)**; CoT alone −0.14; **BT with style covariates** (the real fix — corrects the *estimate*) | **Only reaches 0.58 with everything stacked. Effectively unfixable at the judgment level.** Present in *human* voters too — a perfectly human-aligned judge inherits it. |
| **Self-preference** | GPT-4 **+10%** self win-rate, Claude-v1 **+25%** ([MT-Bench](../sources/judge-mtbench-zheng.md), authors decline to conclude). **Causal**: GPT-4 self-recognition **73.5%**; fine-tuning to >90% recognition on **500 examples** moves self-preference linearly ([Panickssery](../sources/judge-self-preference-panickssery.md)). Claude-3.5 judging own pairs: **64.3% → 44.8%** ([JudgeBench](../sources/judge-judgebench.md)). 2026: **−0.48 to +0.56, no universal sign** | all | **Family-disjoint panel** ([PoLL](../sources/judge-poll-panel.md)); use RMs / dedicated judges with no "own generations" | **Does NOT cancel by averaging** — pairwise self-preference scores **sum to > 1** (mutual favoritism). **Scales with judge capability** → "best judge" and "least biased judge" conflict. Unfixable if judge ∈ candidate family. |
| **LLM-text preference** (generalization of self-preference) | G-Eval-4 **"always gives higher scores to GPT-3.5 summaries than human-written summaries, even when human judges prefer human-written"** ([G-Eval](../sources/judge-geval.md)) | 2023 | None validated | **Judges systematically invert the human verdict on machine-vs-human text.** Our human-authored gold references will be under-scored. Unfixable — measure the offset, don't trust the sign. |
| **Sentiment / emotional tone** | **RR 0.60–0.80 across ALL models — worst uniform failure in CALM.** Sadness/anger/fear modification drops RR to **0.24–0.66** on high-quality answers ([CALM](../sources/judge-calm-bias-benchmark.md)) | all | **None known** | **🔴 Highest-priority risk for a companion platform.** Our content is emotionally-toned *by design*. A judge may flip verdicts on up to 76% of emotionally-perturbed items. **No published mitigation.** |
| **Chain-of-thought** | **RR 0.560–0.745 — lowest overall robustness in CALM** ([CALM](../sources/judge-calm-bias-benchmark.md)) | all | Use CoT **always, consistently** (never mix) | CoT both *helps agreement* (+7.2pp) and *is itself a bias vector*. Both true. Consistency of application is the only defence. |
| **Sycophancy / bandwagon** | CALM bandwagon RR **0.610–0.791**; Claude-3.5 **worst (0.610)**. Telling the judge "90% prefer A" flips it ~21–39% | all | Strip all social/popularity cues from judge context | Our judge prompt must **never** leak variant identity, prior scores, or "current leader" status. Easy to leak accidentally via metadata. |
| **Authority / anchoring** | CALM authority RR **0.628–0.865**; fake citations flip verdict up to ~37% | all | Strip citations/references from judged text where not the point | Companion characters may cite things in-character → confound. |
| **Distraction** | CALM RR 0.713–0.878 | all | — | Irrelevant content shifts verdicts ~12–29%. |
| **Compassion-fade** (named vs anonymous) | CALM RR **0.835–0.877** | all | **Anonymize all variants** — trivial and mandatory | ~12–17% verdict shift purely from model identity. Also: renaming assistants moved Claude-v1 consistency **23.8 → 56.2%**. Cheap, large win. |
| **Nesting / format** | JudgeLM **format bias**: judge trained w/ references degrades when run w/o them | all | **Reference drop** during training; freeze prompt template as immutable unit | Any prompt-template change silently degrades performance independent of merit. |
| **Leniency** | Scores differ from human by **up to 5 points** ([Thakur](../sources/judge-judging-the-judges-thakur.md)) | all | Calibration set; rank-based not score-based reporting | **Score compression at the top** — kills resolution exactly among our best variants, where we most need it. |
| **Scale/format sensitivity** | GPT-4: **92.75% (score-based) vs 61.50% (Likert)** — 31pp from format alone. Qwen Likert: **8.12%** ([PORTIA](../sources/judge-portia-position-bias.md)) | all | Empirically select format per judge | **The judging *format* is a bigger lever than the judge *model*.** Choosing "rate 1–10" by taste may select the judge's worst mode. |

---

## 2. Agreement numbers and the human ceiling

**The ceiling:**

| Quantity | Value | Source |
|---|---|---|
| **Human-vs-human agreement (MT-Bench, non-tie)** | **81%** | [MT-Bench](../sources/judge-mtbench-zheng.md) |
| Human-human (cited by JudgeLM) | 82% | [JudgeLM](../sources/judge-judgelm.md) |

**~19% of pairwise judgments are irreducibly contested among experts.** No judge can be validated beyond this on the same distribution. Any reported agreement >81% is measuring something other than human preference (usually: agreement with another LLM).

**Judge-vs-human — the optimistic (2023, percent-agreement, non-tie) numbers:**

| Setup | Agreement | Source |
|---|---|---|
| GPT-4 pairwise, MT-Bench | 85% | [MT-Bench](../sources/judge-mtbench-zheng.md) |
| GPT-4 single-answer, MT-Bench | 84% | " |
| GPT-4 pairwise, Chatbot Arena | 87% | " |

**Judge-vs-human — the honest (chance-corrected / hard-data) numbers:**

| Setup | Value | Source |
|---|---|---|
| **Best config (Claude Sonnet 4 + full mitigation stack)** | **70.0%, κ = 0.530** | [2026](../sources/judge-bias-mitigation-systematic-2026.md) |
| Llama 3.3-70B + S8 (zero API cost) | 68.5% | " |
| **GPT-4 unconditional, reaching 80% agreement** | **"almost never"** | [Trust or Escalate](../sources/judge-trust-or-escalate.md) |
| Trust-or-Escalate w/ ~20% abstention | **>80% guaranteed, ~80% coverage** | " |
| PORTIA-GPT-3.5 vs human | 63.75% (beats raw GPT-4's 60%) | [PORTIA](../sources/judge-portia-position-bias.md) |
| G-Eval-4 SummEval (Spearman) | **ρ = 0.514** | [G-Eval](../sources/judge-geval.md) |
| G-Eval-4 Topical-Chat "engagingness" | **ρ = 0.631** ← closest analogue to our dimensions | " |
| Prometheus 2-8x7B, MT Bench (Pearson) | 0.665 (GPT-4: 0.717) | [Prometheus 2](../sources/judge-prometheus2.md) |

**Reconciling 85% and κ=0.53:** they are not contradictory — they are different metrics on different data. 85% is raw percent agreement, ties excluded, 2023, on MT-Bench's distribution. κ=0.53 is chance-corrected. **Percent agreement is inflated by base rate**: a judge that always says "good" on a distribution that is 80% good scores 80% while carrying zero information ([Thakur](../sources/judge-judging-the-judges-thakur.md)). **Report κ. Never report percent agreement.**

**Correctness (not preference) — the floor:**

| Judge | JudgeBench overall | Knowledge | Source |
|---|---|---|---|
| **GPT-4o (vanilla)** | **50.9%** (chance = 50) | **44.2%** (worse than chance) | [JudgeBench](../sources/judge-judgebench.md) |
| GPT-4o (Arena-Hard prompt) | 56.6% | 50.7% | " |
| Skywork RM (Gemma-2-27B) | **64.3%** | 59.7% | " |
| **o1-preview (reasoning)** | **75.4%** | — | " |

**Inference-time reasoning (+24.5pp) is the single biggest lever in the entire literature** — larger than every prompt-level mitigation combined.

---

## 3. Pointwise vs pairwise vs listwise

| | **Pointwise** (single-answer grading) | **Pairwise** | **Listwise (3+)** |
|---|---|---|---|
| **Reliability** | Lower. Scores drift **up to 5 pts** vs human. Leniency → ceiling compression. Format-sensitive (GPT-4 Likert consistency **61.5%** vs 92.75% score-based) | Higher. MT-Bench 85% vs 84%; the whole bias literature is built here | **Worst — CALM: position bias "worsens with 3–4 answer options"** |
| **Cross-model comparability** | ✅ **Native** — absolute scale, no reference model needed. But scale is not stable across judge versions | ❌ **Not native** — needs **Bradley-Terry / Elo aggregation** to produce a global ranking from local comparisons | ❌ |
| **Scale** | ✅ **O(n)** | ❌ **O(n²)** pairs (mitigable: sparse/adaptive sampling, anchor set) | O(n) but unreliable |
| **Regression detection** | Good with continuous scores (G-Eval prob-weighting) | Good vs a frozen anchor | — |
| **Verdict** | Diagnostics + cheap tripwire | **Headline ranking** | **Do not use** |

**Recommendation: pairwise-against-a-frozen-anchor-set, aggregated with Bradley-Terry + style covariates.**

This resolves the pointwise/pairwise tension for our specific requirements:
- **Comparability** comes from BT, not from the judge's scale. BT converts local pairwise judgments into a global latent strength — comparable across models by construction, and it is what Chatbot Arena does.
- **Scale**: don't do all-pairs O(n²). Fix an **anchor set** of frozen reference responses per (character, scenario). Each new variant is compared only against anchors → **O(n) judgments**, but yields a globally comparable BT score. Anchors also give us drift detection for free.
- **Style covariates go into the BT fit** ([Style Control](../sources/judge-style-control-arena.md), [LC-AlpacaEval](../sources/judge-length-controlled-alpacaeval.md)) — this is where length/style bias actually gets corrected. Cannot be done with pointwise scores.
- **Pointwise (RM or Prometheus 2) runs alongside** as a cheap per-commit tripwire and for per-dimension diagnostics.

---

## 4. Recommended hardened judging protocol

### Judgment-level (per item)

1. **Anonymize everything.** No model names, no variant IDs, no prior scores, no "current leader" in judge context. (Compassion-fade RR 0.835–0.877; renaming moved Claude-v1 **23.8 → 56.2%**.) Bandwagon RR down to 0.610 — leaking rank is actively dangerous.
2. **Reference-anchor every judgment.** The most consistently validated mitigation across the whole corpus: MT-Bench math failure **70% → 15%** (vs CoT's 30%); JudgeLM reference support **+7.78pp consistency, +4.28pp agreement**. **For us the reference = character card + human-authored exemplar in-character dialogue.**
3. **Always use CoT — and always the same way.** Best single mitigation at 1× cost, universally positive, no cross-bias penalty (2026 study). But CoT is itself a bias vector (CALM RR 0.56–0.75), so **never mix CoT and non-CoT judgments in one comparison**.
4. **Instance-specific evaluation plan, frozen per item.** Generate per (character, scenario) via [EvalPlanner](../sources/judge-evalplanner.md), then **freeze and reuse identically across all variants** for that item. Adaptivity to content + fixed instrument across the comparison. The plan is logged as a traceability artifact.
5. **Empirically select the response format** (score-based vs Likert vs relation-based) per judge. **31pp swing on GPT-4 from format alone.** Do not choose by taste.
6. **Probability-weighted continuous scores** where logprobs are available (G-Eval: `score = Σ p(sᵢ)·sᵢ`). Recovers the resolution integer Likert destroys — needed for regression detection. Constrains judge selection (many reasoning endpoints don't expose logprobs).
7. **Position handling: measure first, then decide.** MT-Bench says swap-and-average; the 2026 study says position bias is ≤0.04 on frontier judges *and swap worsens verbosity bias (+0.07)*. **Measure on our own judges.** If ≤0.05, skip the swap and spend the 2× on a reasoning judge or a panel member instead. If not, prefer PORTIA (+47.46% rel., <2× cost) over naive swapping.

### Panel & confidence

8. **Family-disjoint panel of 3** ([PoLL](../sources/judge-poll-panel.md)): better than a single GPT-4 (Kendall τ **0.778 vs 0.667**; κ +0.037 to +0.136) at **7–8× less cost**, and **2.8× more stable** (σ 2.2 vs 6.1). Strict dominance — no tradeoff to argue about.
   - **Hard constraint: no panel member may share a family with any candidate variant** (Panickssery; JudgeBench 64.3 → 44.8%).
   - **Prometheus 2 + GPT-4 is NOT independent** — Prometheus is distilled from GPT-4; errors correlate by construction.
   - Aggregate: max-voting for discrete verdicts, average-pooling for scales.
9. **Confidence via simulated-annotator agreement or panel disagreement — never verbalized confidence or raw logprobs** (documented as "brittle... overestimate human agreement").
10. **Abstain and escalate** ([Trust or Escalate](../sources/judge-trust-or-escalate.md)). Cheap judge → escalate on low confidence → abstain if none confident. **>80% human agreement at ~80% coverage.** Route abstained items to human review → grows our calibration set on exactly the hard cases.
11. **Publish the abstention rate as a headline metric.** A variant that pushes items into the contested bucket is telling us something real.

### Aggregation

12. **Bradley-Terry over pairwise judgments vs a frozen anchor set**, with **style covariates** (length first — coefficient 0.249, ~8× any markdown term; then markdown/format; then companion-specific: dialogue/narration ratio, asterisk-action density, turn length).
13. **Report ranks and BT strengths with confidence intervals — never raw judge scores as absolute quality.** ("Fidelity = 8.2/10" is indefensible; scores drift 5 pts vs human.)

### Versioning & validation

14. **Judge version = `(model_snapshot_id, prompt_template_hash, rubric_version, plan_version, decoding_params, seed)`.** All immutable. **Never a floating alias** (`gpt-4`, `*-latest`). A score without this tuple is meaningless.
15. **Score primary key: `(variant, judge_version, dataset_version)`.** Scores across judge versions **must never share an axis** without an explicit bridge.
16. **Frozen calibration set** — human-labeled, on *our* content, by *our* chosen annotator population, **including human-authored items** (to measure the machine-vs-human inversion offset from G-Eval).
17. **Re-run the calibration set on every judge change.** Compute the offset/rescaling. **Dual-run old + new judge during an overlap window** (standard metrology instrument-changeover). This is the only way to know whether a "regression" is the variant or the instrument.
18. **Validate against human labels on our own data — never against a stronger LLM's labels.** ([Bavaresco](../sources/judge-bavaresco-judge-bench-20-tasks.md): "LLMs should be carefully validated against human judgments before being used as evaluators"; variance across tasks is *substantial*, so borrowed numbers carry ~zero information.)
19. **Report Cohen's κ / Krippendorff's α. Never raw percent agreement.**
20. **Decide the annotator population deliberately** — expertise level changes the answer (Bavaresco). For companion characters the "expert" is the character designer.
21. **Prefer open-weights judges for the reproducible tier.** Even pinned API snapshots get retired; a checkpoint hash cannot drift. Plan judge migration as routine, not emergency.
22. **Decompose character fidelity.** The *factual-consistency* part ("did it contradict its backstory?") must go to programmatic checks or a reasoning judge — a preference judge is near-chance on knowledge (**44.2%**). Only the *stylistic* part goes to the preference judge.

### Cost / latency reference

| Option | Cost / latency | Source |
|---|---|---|
| GPT-4 Turbo single judge | $10/M in, $30/M out | [PoLL](../sources/judge-poll-panel.md) |
| **PoLL panel of 3 (combined)** | **$1.25/M in, $4.25/M out — 7–8× cheaper** | " |
| PORTIA + GPT-3.5 | **9.57% of GPT-4 cost**, beats raw GPT-4 vs humans (63.75% vs 60%) | [PORTIA](../sources/judge-portia-position-bias.md) |
| **JudgeLM-7B self-hosted** | **5K samples / 3 min on 8×A100 ≈ 36ms/sample** (~2 OOM faster than API) | [JudgeLM](../sources/judge-judgelm.md) |
| Llama 3.3-70B + full stack | 68.5% agreement, **zero API cost** | [2026](../sources/judge-bias-mitigation-systematic-2026.md) |
| Mitigation cost multiples | CoT/rubric **1×**; position swap **2×**; same-family ensemble **3×**; combined S8 **2×** | " |

**The consistent finding across three independent sources: spend on *method*, not on judge size.** PoLL (3 small models > GPT-4, 7-8× cheaper), PORTIA (GPT-3.5 + alignment > GPT-4, 10× cheaper), Trust-or-Escalate (Mistral-7B cascade > GPT-4). The one exception where raw model capability *does* pay: **reasoning judges on correctness** (+24.5pp).

---

## 5. What a naive implementation gets wrong

1. **Quoting "80%+ agreement, same as humans" as license to trust the judge.** That is raw percent agreement, ties excluded, 2023-era, on MT-Bench's distribution. Chance-corrected on realistic data: **κ ≈ 0.53** with everything stacked. GPT-4 unconditional **"almost never"** hits 80%.
2. **Reporting percent agreement instead of κ.** Base rate does the work; a constant-output judge scores 80% on an 80%-good distribution. This is the most common error in the field and it is self-deception.
3. **Validating the judge against GPT-4/GPT-5 labels.** JudgeLM's "89% agreement with teacher, exceeds human-human 82%" compares two different quantities and concludes the wrong thing. **Distillation fidelity ≠ judgment quality.** A perfect distilled judge reproduces its teacher's biases *and* its 50.9% near-chance correctness.
4. **Using a floating model alias as the judge.** GPT-4 went **84% → 51.4%** on primes in three months; instruction-following (= rubric adherence) degraded; **CoT techniques that worked in March stopped working in June**. Your instrument silently changes under you.
5. **Plotting scores from different judge versions on one chart.** Guaranteed phantom regressions and phantom wins.
6. **Trusting the judge's stated confidence.** Verbalized confidence and predictive probability are "brittle even with the strongest judge model... overestimate human agreement."
7. **Forcing a verdict on every item.** ~19% are irreducibly contested (81% human-human ceiling). Forcing verdicts there manufactures noise and burns the illusion of precision. **Trust-or-Escalate only reaches its 80% guarantee by abstaining on ~20%.**
8. **Ignoring length/style.** Length coefficient **0.249**, ~8× any markdown term; **Grok-2-mini moves 12 ranks** under style control. **We compare system-prompt variants — "be thorough and detailed" is a one-line leaderboard exploit that a team optimizing against us will find in a week.** This makes our leaderboard measure verbosity.
9. **Assuming length bias points "longer = better".** 2023: yes (91.3% failure). 2026: **reverses** to conciseness preference (−0.20 to −0.76). Hard-coding a direction bakes in an error that flips on the next judge update. **Measure the sign, per judge version.**
10. **Assuming self-preference has a fixed sign or cancels by averaging.** 2026: **−0.48 to +0.56**, model-dependent. Pairwise self-preference scores **sum to >1** — averaging two self-preferring judges gives two biases, not zero.
11. **Building a panel from one family** (GPT-4o + GPT-4o-mini + GPT-4-turbo). Shared self-preference; defeats the entire point. **Prometheus 2 + GPT-4 is also not independent** (distillation).
12. **Letting a judge grade its own family.** Claude-3.5: **64.3% → 44.8%** judging its own pairs — below chance. **A judge cannot catch an error it would itself make.** This makes the judge a *different instrument per candidate family* — the deepest threat to cross-model comparability, and it cannot be averaged away.
13. **Reflexively adding swap-and-average.** 2× cost for ≤0.04 of bias on frontier judges, and it **worsens verbosity bias (+0.07)**. Mitigations interact; single-strategy evaluation overstates their value.
14. **Assuming CoT is a free win.** It is the best single mitigation (+7.2pp) *and* the lowest-robustness axis in CALM (RR 0.56–0.75). Mixing CoT/non-CoT within a comparison invalidates it.
15. **Picking "rate 1–10" by taste.** GPT-4: **92.75% score-based vs 61.50% Likert** — 31pp from format alone. Qwen Likert: **8.12%**. The format is a bigger lever than the model.
16. **Using integer Likert without probability weighting.** Judges bunch on a few values; ties explode; resolution needed for regression detection is destroyed at exactly the top of the range (compounded by leniency).
17. **Treating the judge as a fact-checker.** GPT-4o: **50.9%** overall, **44.2% on knowledge** — worse than a coin flip. Better prompting buys +5.7pp. **Character-fidelity-as-consistency will not be caught by a preference judge.**
18. **Expecting the judge to rank human-authored gold references at the top.** G-Eval-4 **"always"** scores GPT-3.5 summaries above human-written ones, even when humans prefer the human text. **"Our variant beats the human reference" is not a success signal.**
19. **Assuming a rigid global rubric works across characters.** A goth vampire and a cheerful barista need different fidelity checks. But per-instance plans that vary *between variants* break comparability — freeze the plan per item, reuse across variants.
20. **Changing the judge prompt template casually.** JudgeLM's **format bias**: a judge trained/tuned with references degrades when run without them. Template is an immutable versioned unit.
21. **Leaking rank/popularity/identity into judge context.** Bandwagon RR down to **0.610** (Claude-3.5 worst) — "90% prefer A" flips it ~21–39%. Easy to leak accidentally via metadata.
22. **Borrowing published agreement numbers instead of measuring.** Bavaresco: variance across tasks is *substantial*; reliability depends on the property, the annotators' expertise, and whether text is human- or model-generated — **all three adverse for us.**
23. **Ignoring sentiment bias on an emotional-companion product.** RR **0.60–0.80** across all models, down to **0.24–0.66** under sadness/anger/fear. **No published mitigation. This sits directly on top of our product.**

---

## 6. What is unfixable (design around it, don't try to solve it)

| # | Ceiling | Why | Design response |
|---|---|---|---|
| 1 | **~19% of judgments have no ground truth** (81% human-human) | Genuine human disagreement, not judge error | **Abstain + report contested rate.** Don't chase it. |
| 2 | **Sentiment bias — RR 0.60–0.80, down to 0.24–0.66** | Uniform across all models; no published mitigation | **Measure our exposure explicitly** (CALM-style emotional perturbation of *our* content). Treat emotional-tone-driven score deltas as untrusted. Highest-priority open risk. |
| 3 | **Judges invert machine-vs-human text verdicts** | G-Eval: "always" prefers machine text | **Never use "beats the human reference" as a criterion.** Keep human items in calibration to measure the offset. |
| 4 | **Self-preference scales with judge capability** | Self-recognition is causally upstream (learnable in 500 examples) | Best judge ≠ least biased judge. **Family-disjoint panel is the only structural fix**, and it gets harder as we add candidate families. |
| 5 | **A judge cannot catch an error it would itself make** | 64.3 → 44.8% self-judging | Judge reliability is **per-candidate-family** → an irreducible dent in cross-model comparability. Programmatic checks for anything with a fact of the matter. |
| 6 | **Style bias floors at ~0.58** with every mitigation stacked | Present in human voters too — a perfectly human-aligned judge inherits it | **Fix at the aggregate (BT covariates), not the judgment.** Accept residual. |
| 7 | **Proprietary judges drift; snapshots get retired** | Vendor-controlled | Calibration set + dual-run overlap + open-weights reproducible tier. **Judge migration is routine, not exceptional.** |
| 8 | **Absolute scores are not meaningful** (±5 pts vs human, leniency, unstable scale) | Judges don't use scales consistently | **Rank/BT-strength with CIs only.** Never ship an absolute quality number. |

---

## 7. Open questions to resolve empirically on our data

1. **Position bias on our judges: ≤0.04 (2026) or 35% (2023)?** Determines whether we spend 2× on swapping. *Cheap to test — do this first.*
2. **Verbosity sign** on our judges/content — longer-better or conciseness-preferring?
3. **Which response format** (score / Likert / relation) maximizes consistency per judge? Up to 31pp available.
4. **Sentiment-bias exposure** on companion content — the single biggest unknown, and no one has published a mitigation.
5. **Does length control over-correct "storytelling"?** Vivid prose is legitimately longer. Covariate set may need to be per-dimension.
6. **Expert (character designer) vs crowdworker ground truth** — changes what we're measuring; must be decided, not defaulted.
7. **Can a family-disjoint panel survive** as we add candidate model families? What's the fallback when every frontier family is also a candidate? (Likely: dedicated fine-tuned judges + RMs, whose "own generations" never appear among variants.)
8. **Reasoning judge (+24.5pp) cost/benefit** at our volume — the biggest lever, the biggest bill.

---

## Source index

| File | Paper | Year | Key contribution |
|---|---|---|---|
| [judge-mtbench-zheng.md](../sources/judge-mtbench-zheng.md) | MT-Bench / Chatbot Arena (Zheng et al.) | 2023 | Foundational; 85% vs 81% ceiling; position/verbosity/self-enhancement; reference-guided 70→15% |
| [judge-calm-bias-benchmark.md](../sources/judge-calm-bias-benchmark.md) | CALM — Justice or Prejudice? | 2024 | **12 biases quantified on a common scale**; sentiment + CoT unsolved |
| [judge-bias-mitigation-systematic-2026.md](../sources/judge-bias-mitigation-systematic-2026.md) | Systematic Bias Mitigation Eval ⚠️ preprint | 2026 | Mitigations head-to-head on modern judges; **κ=0.530 best**; cross-bias interactions |
| [judge-poll-panel.md](../sources/judge-poll-panel.md) | PoLL — Replacing Judges with Juries | 2024 | Family-disjoint panel > GPT-4, **7–8× cheaper**, 2.8× more stable |
| [judge-trust-or-escalate.md](../sources/judge-trust-or-escalate.md) | Trust or Escalate | 2024 | **Abstention + provable guarantee**; GPT-4 "almost never" hits 80% |
| [judge-judgebench.md](../sources/judge-judgebench.md) | JudgeBench (Tan et al.) | 2024 | **GPT-4o = 50.9% (chance)**; self-judging 64.3→44.8%; reasoning +24.5pp |
| [judge-style-control-arena.md](../sources/judge-style-control-arena.md) | Chatbot Arena Style Control | 2024 | Length coef **0.249**; Grok-2-mini moves **12 ranks**; BT covariates |
| [judge-self-preference-panickssery.md](../sources/judge-self-preference-panickssery.md) | LLM Evaluators Recognize & Favor Own Generations | 2024 | **Causal** self-preference; 73.5% self-recognition; 500 examples |
| [judge-geval.md](../sources/judge-geval.md) | G-Eval | 2023 | ρ=0.514; prob-weighted scoring; **"always" prefers machine over human text** |
| [judge-portia-position-bias.md](../sources/judge-portia-position-bias.md) | PORTIA — Split and Merge | 2023 | +47.46% rel. consistency; **format > model (31pp)**; 9.57% of GPT-4 cost |
| [judge-judgelm.md](../sources/judge-judgelm.md) | JudgeLM | 2023 | Swap-aug/reference-support/reference-drop; **the distillation-fidelity trap** |
| [judge-drift-chatgpt-over-time.md](../sources/judge-drift-chatgpt-over-time.md) | How Is ChatGPT's Behavior Changing? | 2023 | **84% → 51.4% in 3 months**; the versioning argument |
| [judge-judging-the-judges-thakur.md](../sources/judge-judging-the-judges-thakur.md) | Judging the Judges (Thakur et al.) | 2024 | **Use κ not percent agreement**; ±5 pt drift; leniency |
| [judge-bavaresco-judge-bench-20-tasks.md](../sources/judge-bavaresco-judge-bench-20-tasks.md) | LLMs instead of Human Judges? (JUDGE-BENCH) | 2024 | **Validate on your own data**; 3 moderators of reliability |
| [judge-prometheus2.md](../sources/judge-prometheus2.md) | Prometheus 2 | 2024 | Best open judge; **pinnable**; custom rubrics; weight merging |
| [judge-rewardbench.md](../sources/judge-rewardbench.md) | RewardBench | 2024 | RM catalogue; **doesn't predict JudgeBench** |
| [judge-evalplanner.md](../sources/judge-evalplanner.md) | EvalPlanner | 2025 | Plan/execute split; RewardBench 93.9; auditable plans |
| [judge-length-controlled-alpacaeval.md](../sources/judge-length-controlled-alpacaeval.md) | Length-Controlled AlpacaEval | 2024 | GLM debiasing; ρ 0.94→0.98; gameability |
| [judge-pandalm.md](../sources/judge-pandalm.md) | PandaLM | 2023 | Closest use-case match (variant selection); 7B @ 88% of GPT-4 |
