# 03 — Measuring Creativity, Storytelling & Narrative Quality

Synthesis note. Sources in `../sources/creativity-*.md`. Accessed 2026-07-16.

---

## 0. The four findings that should drive the design

1. **Creativity is conjunctive, not additive.** 70 years of consensus (Stein 1953; Runco & Jaeger 2012): creativity = novelty **AND** appropriateness. Operationalized best by *Death of the Novel(ty)*: an expression is creative iff simultaneously **sensical ∧ pragmatic ∧ novel**. → Never average novelty with coherence. Use a **gate/min**, not a mean. An incoherent-but-weird reply and a boring-but-sound reply must both score ~0.

2. **Originality is population-relative *by definition*.** Guilford scored originality as *statistical infrequency within the sample*. TTCT is norm-referenced. This is not an implementation detail we can skip — **there is no such thing as a per-response originality score without a reference distribution.** It licenses the population tier (§3) on 1950s theory, not just recent LLM papers.

3. **LLM judges cannot do absolute creativity scoring, but can do pairwise.** r = 0.159 and 40% self-consistency for absolute rubric scoring; ~0 correlation with experts on TTCW. But **73–78% human agreement on pairwise comparison** (LitBench). Amabile's CAT independently confirms: even human experts are only reliable (α .80–.90) when rating *relatively within a set*, never absolutely. **The format is the variable, not the model.**

4. **Every per-response metric can improve while the product gets worse.** Writers using GPT-4 wrote *better* stories that were *more similar to each other*. Alignment cuts Creativity Index 30.1%. Homogenization is **invisible to any per-response metric, by construction**. This is the regression we most need to catch and the one a naive design will completely miss.

---

## 1. Scope the claim first (Boden)

We are measuring **exploratory + combinatorial P-creativity**: novel *relative to the distribution of plausible responses to this scenario*. Not transformational, not H-creativity. Write this into the spec. It's what makes the fixed-scenario / fixed-anchor design defensible rather than arbitrary — the reference class is declared, so the number means something specific.

---

## 2. The population vs per-response distinction — read this before designing schemas

| | Per-response | Population-level |
|---|---|---|
| Unit | one message | a **set** of k responses to the *same* scenario |
| Examples | slop density, intra-response repetition, constraint satisfaction, pairwise Elo | homogenization, self-BLEU, compression ratio, trope concentration, Guilford-originality |
| Can you show it in a UI next to a response? | yes | **no — it has no per-response value** |
| Cost driver | judge calls | **k× generation calls**, ~0 judge |

**Diversity/homogenization is a property of a distribution, not of a text.** Self-BLEU of one response is undefined. This must be a distinct entity in the data model with its own aggregation path — retrofitting it later is a schema migration.

To measure it: fix a scenario, sample **k ≥ 10** independent generations at production temperature, compute pairwise stats across the k. Multiplies generation cost by k, adds no judge cost. Generation is ~100× cheaper than judging — this is the cheapest high-value tier we have and the easiest to under-prioritize.

**Third axis often missed:** cross-*turn* repetition (looping within one long conversation). Needs 20+ turn conversations. Most benchmarks are single-shot and would never see our top user complaint.

---

## 3. Candidate operationalizations

### TIER A — no model call. Run on 100% of traffic.

Deterministic → perfect test-retest → these are the **regression detectors**. None of them measure creativity positively; they measure its *absence*. That's fine and it's the honest framing.

---
**A1. Slop / cliché density** *(highest value in this tier)*
- **Definition:** frequency of n-grams statistically over-represented in LLM output vs human writing.
- **Compute:** EQ-Bench formula — 60% slop words + 25% not-x-but-y patterns + 15% slop trigrams. Build list by comparing ~10 models' outputs against a human reference corpus. **Build our own from roleplay/companion text** — generic GPT-ism lists miss "a mischievous glint in her eye", "voice barely above a whisper", "little did they know".
- **Cost:** ~free, O(n).
- **Validation:** no published human correlation. Defensibility comes from construction, not correlation: it's a frequency ratio against a human reference distribution, so we claim only "matches known cliché inventory", not "is uncreative". Easy claim to defend.
- **Failure mode:** negative-only (low slop ≠ creative). Gameable once teams optimize against a public list. **Keep the list versioned and partly held out.**

---
**A2. Repetition — intra-response / cross-turn / cross-conversation** *(best product-aligned metric we have)*
- **Definition:** three separate scores. `rep_intra` = frac. of 5-grams recurring within a message. `rep_cross` = frac. of 5-grams in turn t_i already seen in t_j, j<i. `rep_conv` = 4-gram self-repetition across different conversations.
- **Compute:** n-gram counting; convention is 5- and 10-grams, flag when an n-gram appears ≥3×. O(n).
- **Cost:** free. Requires long multi-turn conversations in the harness (real cost is generation, not scoring).
- **Validation:** face validity + the loudest complaint in the roleplay practitioner community. Unambiguously bad — no construct debate to lose.
- **Failure mode:** verbatim-only; misses semantic looping (same beat, new words). Add an embedding-similarity variant for that.
- **Recommended headline number:** **slope of `rep_cross` vs turn index** — "narrative staleness". Cheap, defensible, and a derivative, so robust to prompt idiosyncrasy.

---
**A3. Distributional diversity across k samples** *(the anti-homogenization tier)*
- **Definition:** how different are k responses to the same scenario.
- **Compute — use the standardization paper's recommended four:**
  - `CR(D)` = uncompressed size / compressed size — **strongly correlated with most n-gram measures, costs seconds.** Primary.
  - `CR:POS` — compression of POS sequences; **specifically distinguishes human from machine text.** Primary.
  - `SRS(d) = log(Σ N_i + 1)`, N_i = # docs containing 4-gram i. Moderate correlation w/ others → independent signal.
  - `Self-BLEU` — weakly correlated w/ others → independent perspective, but O(n²) and **"prohibitively slow"** (48–800h for 50k samples). Sample only.
  - **Explicitly reject BERTScore homogenization**: "There is no good justification to report it."
- **Cost:** k× generation; scoring is seconds (except self-BLEU).
- **Validation:** distinct-n and self-BLEU **correlate poorly with human diversity judgment** — humans judge *semantic* diversity, these measure lexical. Treat as change-detectors, not ground truth.
- **⚠️ FAILURE MODE — THE BIGGEST TRAP IN THIS DOC:** *all* these scores correlate **0.79–0.904 with word count**; "scores are not meaningfully comparable" across differing lengths. If model A is chattier than model B, our creativity leaderboard is a **verbosity leaderboard**. **Mandatory: truncate to a fixed token budget before scoring, and report length alongside every diversity number.**
- Second failure mode: gameable by incoherent output. Must be **gated on a coherence check** (see §0.1).

---
**A4. n-gram novelty / Creativity Index — ⚠️ RECOMMEND AGAINST as a score**
- `uniq(x,L) = ∑_k 𝟙{f(x[i:i+n],C)=0 ∀i∈(k-n,k], n≥L} / ||x||`; CI = ∑_{n≥L} uniq(x,n). DJ Search makes it linear-time.
- **Validation is fatal:** yes, novelty is positively associated with creativity (OR≈1.96/SD, p<0.001) — but **~91% of top-quartile n-gram-novel expressions are NOT judged creative** (CI [0.90,0.92]); ~79% not creative to *any* annotator. Precision ≈9%. Also ~25% of creative expressions fall *below* mean perplexity.
- Also: "reflects primarily lexical diversity"; **highly sensitive to L** (5–7 vs 5–11 changes scores substantially); depends on reference corpus choice.
- Worst: for weaker models, **higher n-gram novelty actively *hurts* pragmaticality** (OLMo-2 β=−0.48, p<0.001) — humans show no such effect. **Optimizing this metric makes weak models incoherent.**
- **Verdict:** do not ship per-response. The *tractable* reuse is to swap the web corpus for **our own prior-response corpus** — which converts it into A3 homogenization, which is what we actually want. Keep CI only as a population-level human-vs-model sanity check (humans score 66.2% higher; alignment costs 30.1%).

---
**A5. Perplexity — ⚠️ REJECT.** Distributions for creative and uncreative text "overlap substantially across all domains"; reflects "fluency rather than novelty." No.

---

### TIER B — objective checks, cheap or tiny-model. High confidence.

**B1. Constraint satisfaction + the CS4 degradation curve** *(my pick for the most defensible number in the whole doc)*
- **Definition:** roleplay is *natively* constrained generation — stay in character, honor the persona card, respect world facts, maintain continuity, hit the tone. CS4's insight: **tighten constraints to block regurgitation of memorized narrative.** A model that only looks creative by retelling training data falls off a cliff; a genuinely generative one degrades gracefully.
- **Compute:** per-scenario constraint sets at 3 tiers (loose/medium/tight, cf. CS4's 9/23/39). Score = satisfied/total. Mostly programmatic or tiny-model checks.
- **Cost:** near-free per check; 3× generation for the curve.
- **Validation:** CS4 validated it "without human annotations"; constraint satisfaction is objectively checkable, so validation is definitional not correlational.
- **Why it's the best number:** bounded [0,1], **real denominator**, comparable across models **by construction**, no judge. This is the closest thing to what the user asked for.
- **Report the slope, not the level.** The degradation curve is the creativity signal, and a derivative is far more robust to judge noise and prompt quirks than a level.
- **Failure mode:** measures *headroom*, not charm. A model can satisfy everything and be dull. Necessary, not sufficient.

**B2. Coherence / plot-hole gating via perturbation tests (from OpenMEVA)**
- OpenMEVA's test suite (d) = **robustness to perturbations**. Steal this: shuffle events, inject a contradiction, swap a character name, violate an established fact — **verify our metric's score DROPS.**
- **This is a meta-test of our metrics, and it should gate the whole platform.** A coherence metric that doesn't move under a deliberately injected plot hole is not measuring coherence. Run it in CI.
- Context: existing metrics "fail to recognize discourse-level incoherence, and lack inferential knowledge (e.g., causal order between events)" — so assume ours is broken until this test passes.

---

### TIER C — judge required. Expensive. Sample, don't saturate.

**C1. Pairwise vs fixed anchors → Bradley-Terry / Elo** *(the primary creativity number)*
- **Definition:** for each scenario, a **frozen anchor set** of reference responses spanning the quality range. Score every model's response against the same anchors. Convert wins → BT/Elo scalar.
- **Why this and not rubric scoring:** LitBench — **73% agreement** (Claude-3.7-Sonnet off-the-shelf), **78%** (trained BT/generative reward models) vs **r=0.159** for absolute rubric scoring. Amabile's CAT reaches α .80–.90 *only* because it's relative-within-set. EQ-Bench v3 uses rubric+Elo hybrid for exactly this reason.
- **Fixed anchors are what give us the user's "same baseline for each model"** — comparability by construction, no absolute calibration of a judge that provably can't calibrate absolutely.
- **Cost:** anchors × models × scenarios judge calls. Anchors are the cost lever; a fixed anchor set amortizes across every model we ever test.
- **Ceiling:** ~73–78% means **~1 in 4 pairwise calls disagrees with a human.** Need volume to average down. Debias for **length, temporal, popularity** — LitBench had to.
- **Failure mode:** judge slop-bias (below).

**C2. TTCW-style rubric — diagnostics only, NOT the score**
- 14 binary tests + written justification across Fluency (5) / Flexibility (3) / Originality (3) / Elaboration (3). Full wording in `creativity-ttcw-art-or-artifice.md`.
- **Validation, expert-administered:** professionals 84.7% pass vs Claude v1.3 30.0%, GPT-4 27.9%, GPT-3.5 8.7% — 3–10× gap. Expert per-item **Fleiss κ = 0.41** (range 0.27–0.66) but **aggregate correlation 0.69**. → **Binary + justification + SUM. Aggregation rescues noisy items.** Steal this pattern for our judge.
- **Validation, LLM-administered:** **"none of the LLMs positively correlate with the expert assessments."** → **We cannot use TTCW as an automated score.**
- **Cost, expert:** $80/task, 2–2.5h. Tens of dollars per story per annotator. → **calibration set only**, never the pipeline.
- **Use:** (a) rubric skeleton for per-dimension diagnostics attached to C1's verdict; (b) the gold protocol for our human calibration set; (c) its dimension-specialization finding (GPT-4 → Originality; Claude → Fluency/Flexibility/Elaboration) proves **a single scalar hides real model differences → always report per-dimension.**

**C3. Narrative rubric — HANNA's 6 criteria**
- **Relevance, Coherence, Empathy, Surprise, Engagement, Complexity** — 5-point Likert, "6 orthogonal and comprehensive human criteria." 1,056 stories, 3 raters, 19,008 annotations, 72 metrics benchmarked.
- Directly reusable rubric skeleton for roleplay. Note **Surprise and Engagement are separated from Coherence** — hard evidence that creativity must not be one number. **Empathy** is first-class and is arguably our *highest-weight* dimension for companion characters.
- Crowd workers (not MFA experts) gave usable signal → cheaper protocol than TTCW, coarser construct. Good middle tier for our human calibration set.
- **Failure mode:** Likert absolute scoring is exactly the format judges fail at. Use these as *dimensions for pairwise* ("which is more engaging?"), not as absolute 1–5 scales.

---

## 4. The judge failure mode we must design around

**Judges favor fluent-but-generic text.** Evidence: r=0.159 vs humans; **40% consistency across 3 runs**; **~20% contradictory judgments** under minor prompt variation; label bias; prefers own generations; "defaults to assessing whether the response sounds plausible"; "confident, fluent hallucinations often receive high scores." **EQ-Bench's authors admit uncontrolled "slop bias (favoring overused tropes)"** — and built a mechanical slop metric because they didn't trust their own judge to catch it.

**Why this is not a normal noise problem:** this bias is **correlated with the construct**, not random. It systematically **overrates** the mode-collapsed, trope-heavy output we're hunting and **underrates** genuine creative risk. Random noise averages out with more samples; **this does not — more samples buy a more precise wrong answer.**

Mitigations must be **structural**:
1. Mechanical, **judge-independent** slop metric as a permanent cross-check (A1). If judge score ↑ while slop ↑, **trust the slop metric** and treat the run as suspect.
2. **Pairwise vs fixed anchors** (C1) — absolute fluency preference partially cancels.
3. **Human calibration set**, refreshed; **publish the agreement number as a first-class output alongside every score.** The agreement rate *is* the honest confidence interval.
4. **Pin judge model + version + prompt as part of the benchmark definition** (EQ-Bench: "for leaderboard parity"). Changing the judge invalidates cross-run comparison. **Judge version bumps must be treated as breaking changes with a re-baseline.**
5. N≥3 repeats, **median** aggregation, fixed seeds. Establish a **noise floor** from repeat runs; any delta below it is **not a regression.** Given 40% self-consistency, this floor is large — measure it before shipping any alerting.
6. **Report judge reliability (α/ICC/Krippendorff) every run.** CAT's discipline: reliability is an empirical result, not a property of the instrument. **If judge α collapses, that run's scores are void.**

---

## 5. Realistic expectations — the ceiling

- **DAT**, the gold-standard automated divergent-thinking measure, correlates with other creativity measures at only **r ≈ 0.32–0.51**. That is the realistic ceiling for *any* cheap automatic creativity proxy. **Do not promise r > 0.6.**
- **DAT test-retest r = 0.73 > all its validity correlations.** The crucial lesson: **a metric can be highly stable (great for regression detection) while only moderately valid (bad for absolute claims).** These are *separate properties*, and our platform needs the first far more than the second. **This is the key to the whole project:** we do not need to solve "what is creativity" to ship a defensible regression detector. We need stability + a declared reference class. Sell stability; caveat validity.
- **CAT expert α = .80–.90** is the ceiling for *any* creativity measurement, human included.
- **Metrics do not agree with each other.** "Different metrics often disagree on the same data points"; CI says one dataset is more creative, perplexity says the opposite; "metrics that distinguish creativity in one domain fail in others." **No convergent validity.** → Never average heterogeneous metrics into one "creativity score" and claim it means something. Pick metrics per *declared sub-construct*.

---

## 6. Recommended scoring architecture

```
Creativity Score (per model, per scenario-suite) — a VECTOR, never a scalar
│
├─ GATE (conjunctive — creativity requires appropriateness)
│   └─ coherence + constraint satisfaction (B1, B2)
│      if the response is incoherent or breaks character → creativity := 0
│      Do NOT average novelty with coherence. min/gate, not mean.
│
├─ TIER A  no model call · 100% of traffic · deterministic · REGRESSION DETECTORS
│   ├─ slop density            (A1)  ← cross-check on the judge
│   ├─ repetition: intra / cross-turn / cross-conv  (A2)  ← headline: rep_cross slope
│   └─ [population, k≥10 per scenario] CR, CR:POS, SRS, self-BLEU(sampled)  (A3)
│      ⚠ length-normalize or this is a verbosity leaderboard
│
├─ TIER B  objective · cheap · HIGH CONFIDENCE
│   └─ constraint satisfaction ratio across 3 tightness tiers → report the SLOPE  (B1)
│
└─ TIER C  judge · sampled · THE PRIMARY NUMBER
    ├─ pairwise vs FIXED ANCHORS → Bradley-Terry / Elo   (C1)
    └─ per-dimension diagnostics, binary+justification, SUMMED  (C2/C3)
       dims: Originality · Surprise · Engagement · Empathy · Complexity · Coherence
       ⚠ always per-dimension — a scalar hides real model differences (TTCW)
       ⚠ ship with the human-agreement number attached, always
```

**Cost shape:** Tier A ≈ free, 100%. Tier B ≈ free per check, 3× generation. Tier C ≈ dominant cost, sample. Population tier costs k× *generation* (~100× cheaper than judging) — **cheapest high-value tier, easiest to under-prioritize, and the only one that can see homogenization.**

**Non-negotiables:**
1. Length-normalize before any diversity/slop metric. (0.79–0.904 length correlation.)
2. Fixed anchor set + pinned judge version, or nothing is comparable.
3. Multi-turn conversations (20+), or we never observe looping — our top user-visible failure.
4. Gate, don't average — creativity is conjunctive.
5. Report per-dimension and report judge agreement. No naked scalar.
6. Establish the noise floor from repeat runs *before* wiring up regression alerts.

---

## 7. Open questions

- Build our own companion-domain slop list — what's the human reference corpus? (Published fiction? Human RP logs? Licensing?)
- Anchor set construction: who writes the anchors, and how do we refresh them without breaking the baseline?
- Semantic (not lexical) looping detection — embedding-based `rep_cross` variant; needs its own validation.
- Human calibration set: TTCW protocol ($80/2.5h/expert) vs HANNA protocol (crowd, 5-pt Likert)? Probably HANNA-style for volume + a small TTCW-style expert set for the ceiling.
- NSFW aversion in judges (EQ-Bench flags it) is a live risk for companion content — a judge that flinches will systematically misscore a big slice of our traffic.
