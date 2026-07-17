# 04 — Psychometrics & Measurement Theory: Actionable Requirements

**Topic owner:** measurement validity
**Date:** 2026-07-16
**Sources:** `research/sources/psycho-*.md`

---

## 0. The framing that should drive the platform

The requirement — *"define proper ways to calculate the points (even for creativity or some hard
dimensions), so we can have a SAME BASELINE for each model"* — is, in psychometric terms:

> Build a measurement instrument that is **reliable** (low noise), **valid** (measures the construct
> we named), and **invariant** (means the same thing across models, languages, and characters).

Those three are separable, testable, and orderable. **Invariance is the one that "SAME BASELINE"
literally names, and it is the one nobody builds.** All three are cheap to test compared to the cost
of shipping on a broken score.

The governing insight from Jacobs & Wallach: "creativity" is an **unobservable theoretical
construct**. It cannot be measured directly, only inferred from observable properties. **Our rubric
IS a measurement model** — a set of assumptions linking observables to a latent variable. Most eval
platforms never write those assumptions down, which is why their numbers cannot be defended when
challenged.

**The order of operations is not negotiable:**

```
Construct definition → Rubric/anchors → Reliability → Validity → Invariance → Ranking → Slicing
```

Every step is gated on the one before. Fitting Bradley-Terry on unreliable judges produces precise
rankings of noise. Slicing by 190 cells before you have invariance produces 190 uninterpretable
numbers. **Do not skip forward.**

---

## 1. Before any code: fix the constructs (Week 0)

### 1.1 Contestedness audit
Jacobs & Wallach's **content validity** decomposes into contestedness, substantive validity, and
structural validity. Contestedness comes first: **does our team even agree what "creativity" means?**

Deliverable: one page per dimension stating (a) the definition, (b) what is explicitly **excluded**,
(c) the population of scenarios it generalizes to.

### 1.2 The retranslation test — run this first, it is the cheapest kill signal
From BARS (Smith & Kendall 1963). Procedure:
1. SMEs write 10-15 **critical incidents** per dimension — concrete observed behaviours from real
   transcripts.
2. Pool and shuffle all incidents across all dimensions.
3. A **second, independent** group blind-sorts them back into dimensions.
4. **Discard incidents that fail to sort back (<60-75% agreement).**

**If a dimension's incidents don't sort back above ~70%, that dimension is not a distinct construct.
Merge it or cut it. No downstream statistic can repair this.** Expect "creativity", "engagement", and
"personality" to substantially collapse into each other. Better to learn that in week 0 than after
building 95 characters of tooling around them.

This step is unglamorous and it is the highest-leverage item in this document.

### 1.3 Rubric spec (empirically grounded, not taste)
| Decision | Choice | Source |
|---|---|---|
| Scale | **0-5** | Li et al. 2026: "the grading scale of 0-5 yields the strongest human-LLM alignment" |
| Anchors | **Every level** gets a behavioural anchor from a real transcript | Unanchored Likert "collapses toward central scores" |
| Anchor content | Observable behaviour, never adjectives | BARS |
| Scoring | CoT → token-probability-weighted score | G-Eval (Liu et al. 2023) |
| Position | Counterbalanced / swapped | position bias |
| Length | Logged as covariate | verbosity bias |

"Introduces an unprompted plot complication referencing an earlier turn" is an anchor.
"Highly creative" is not.

**Do not use a 1-10 or 1-100 scale.** Wider scales make central-tendency bias worse and reduce human
alignment. This is settled empirically and is a free win.

---

## 2. Reliability: what we must compute and report

### 2.1 The mandatory per-dimension stat block

Every dimension ships with this or it does not ship:

```
dimension: creativity
  krippendorff_alpha_ordinal : 0.74    # inter-judge agreement
  icc_2_1_absolute           : 0.68    # judge-as-variance-facet, absolute agreement
  phi_dependability          : 0.81    # G-theory, absolute decisions  ← the headline number
  sem                        : 0.31    # standard error of measurement, in score units
  noise_floor_rerun          : 0.22    # same model, same items, different seed
  n_items / n_judges / n_runs: 40 / 3 / 3
```

### 2.2 Which coefficient, and why

- **Krippendorff's α (ordinal metric)** is the default: handles >2 judges, ordinal data, and missing
  ratings. Kappa cannot do all three.
- **ICC(2,1) absolute agreement** alongside — specify all three facets (two-way random, single
  rater, absolute agreement) or the number is uninterpretable. **Absolute agreement, not
  consistency**: "SAME BASELINE" means judges must give the *same number*, not merely rank the same.
- **Gwet's AC1** for skewed dimensions (safety violations, ~98% one category). See §2.4.

### 2.3 Thresholds — what "trustworthy" means

| Statistic | Ship | Tentative | Broken |
|---|---|---|---|
| Krippendorff's α | **≥ 0.80** | 0.67–0.79 | < 0.67 |
| ICC(2,1) | ≥ 0.75 | 0.50–0.75 | < 0.50 |
| **Φ (dependability)** | **≥ 0.80** | 0.70–0.80 | < 0.70 |
| Cronbach's α (across items) | ≥ 0.70 (0.90 high-stakes) | — | < 0.70 |

Krippendorff's own words for the middle band: **"the lower bound for tentative conclusions ...
outcomes should be interpreted with concern."** Our platform should render that literally — a
dimension at α=0.72 displays with a warning badge and is **excluded from ship gates** while still
being reported.

**Proposed policy:** a dimension below α=0.67 is **not published at all**. Publishing a number the
instrument cannot support is worse than publishing nothing, because it gets optimized against.

### 2.4 Two traps that will bite us

**The kappa paradox.** Kappa corrects for chance using marginal distributions. When one category
dominates, expected agreement → observed agreement and **kappa collapses to ~0 even at 95%+ raw
agreement**. Kappa is therefore **not comparable across dimensions with different base rates**. Use
Gwet's AC1 on skewed dimensions.

**Reliability is population-dependent — this one is subtle and important.** `ρ = σ²_T/(σ²_T+σ²_E)`.
If we compare 5 near-identical checkpoints, `σ²_T` is tiny, so **reliability looks terrible even with
a perfect rubric.** This *will* happen to us and it *will* be misdiagnosed as a broken rubric.

**Therefore: report SEM as the primary quality number.** `SEM = SD·√(1−ρ)`. It is in score units, it
is population-independent, and it directly answers the only question an engineer asks: *is this
0.2-point gap real?* (95% CI on a true score: `X ± 1.96·SEM`.)

### 2.5 The validity ceiling — post this on the wall
Observed correlation between two measures cannot exceed `√(ρ_xx' · ρ_yy')`.

**If our judge's reliability is 0.6, correlation with human preference can never exceed 0.77 — no
matter how good the model is.** Every complaint that "the eval doesn't match human intuition" should
first check whether it is mathematically *permitted* to. Fix reliability before hunting validity.

---

## 3. Variance decomposition: where is our noise? (G-theory)

**This is the highest-value single experiment in this document.** One crossed G-study tells us where
every future dollar should go.

### 3.1 The study
Fully crossed design: **models × scenarios × judges × runs**. Pilot at ~5 models × 40 scenarios ×
3 judges × 3 runs = 1,800 cells. Fit by REML (`lme4` in R, or `statsmodels` mixed LM in Python).

Decompose:
```
σ²_total = σ²_m + σ²_i + σ²_j + σ²_mi + σ²_mj + σ²_ij + σ²_mij,e
```

### 3.2 How to read the output — this is the decision table

| Component | Meaning | If it's large, do this |
|---|---|---|
| `σ²_m` | **Signal.** Real model differences | good — this is what we want |
| `σ²_i` | Scenario difficulty | harmless for ranking |
| `σ²_j` | Judge severity | fatal for absolute scores → fix anchors |
| `σ²_mi` | **model × scenario** | **the benchmark lottery, quantified** → add scenarios |
| `σ²_mj` | **model × judge** | **judge favours a model family** → diversify judges. Most dangerous component |
| `σ²_mij,e` | residual + seed noise | add runs / lower temperature |

**`σ²_mj` is the one to watch.** A judge from the same family as a candidate model is a
self-enhancement bias vector, and it shows up here and nowhere else. If `σ²_mj` is material, we
cannot use a single judge, full stop.

### 3.3 Report Φ, not Eρ²
```
Eρ² = σ²_m / (σ²_m + σ²_rel)                    # relative decisions (ranking)
Φ   = σ²_m / (σ²_m + σ²_abs),  σ²_abs ≥ σ²_rel  # absolute decisions
```
`Φ ≤ Eρ²` always. **Our requirement is a same-baseline absolute score, so Φ is our headline
reliability number.** Reporting Eρ² would flatter us and answer the wrong question.

### 3.4 The D-study answers the budget question
`n_i` and `n_j` sit in the denominators of `σ²_rel` and `σ²_abs`. So the D-study literally computes
"20 more scenarios vs 1 more judge — which buys more Φ per dollar?" **Stop arguing about this in
meetings; it is a formula.**

### 3.5 The noise floor is non-negotiable
Madaan et al. found IRT and item analysis **"struggle to meaningfully reduce variance."** IRT buys
*efficiency*, not *stability*. These are orthogonal budget lines and conflating them is a real risk
given how attractive tinyBenchmarks looks.

**Before any leaderboard ships:** re-run the same model on the same scenarios with different seeds.
That spread is the **noise floor**. No difference below it is reportable, ever, regardless of N.
Render it as a shaded band on every chart so it is impossible to ignore.

---

## 4. Validity: is it measuring the thing we named?

| Type | Test for us | Pass condition |
|---|---|---|
| **Face** | Do scores look plausible? | sniff test |
| **Content** | Retranslation (§1.2) | >70% blind sort-back |
| **Convergent** | Correlate with human preference on a gold set | r ≥ 0.7 (disattenuate! §2.5) |
| **Discriminant** | Correlate dimensions with **each other** | **inter-dimension r < 0.7** |
| **Criterion** | Predict a held-out outcome (retention, thumbs-up, session length) | significant |
| **Consequential** | What does optimizing this cause? | see below |

### 4.1 Discriminant validity is where we will fail
If "creativity" and "engagement" correlate at r=0.9, **we have one dimension with two names** and a
dashboard that triple-counts it. Ship a **dimension × dimension correlation matrix** as a
first-class platform artifact, not a one-off analysis. Corrected for attenuation:
`r_true = r_obs / √(ρ_xx'·ρ_yy')`.

Expected finding: our 6-8 dimensions are really 2-3 factors. Run an EFA/factor analysis to find out.
That is a good outcome — fewer, real dimensions beat more, fake ones.

### 4.2 Consequential validity — the one engineers skip
"What world do the measurements bring into being?" For a **companion product** this is not
philosophy, it is product risk: **a rubric that rewards "engagement" will select for models that
maximize session length**, which for a companion app means selecting for **emotional dependency**. We
would be building a sycophancy optimizer and calling it a quality metric.

**Concretely: for every dimension, write down the model that would win by gaming it.** If that model
is one we would be ashamed to ship, the dimension needs a counter-weighted dimension (e.g. pair
engagement with a healthy-boundaries / user-wellbeing measure) or it should not be a ship gate. This
deserves a named owner, not a footnote.

### 4.3 Cheap criterion check: known-ordering
Score a deliberately-degraded model, base, and known-better model. **If a dimension doesn't order
those correctly, it's broken.** Add to CI. This is the fastest validity test available and catches
regressions in the *instrument itself*.

---

## 5. Cross-language and cross-character comparability (measurement invariance)

**This is the direct answer to "SAME BASELINE" and it is the section most likely to be skipped.**

The claim "model A beats model B in both en and zh" is a **latent mean comparison across groups**. It
is **only valid under scalar invariance**. Without it, a mean difference is uninterpretable: we
cannot distinguish "A is better in zh" from "the instrument behaves differently in zh."

### 5.1 The ladder (multi-group CFA, groups = language)

| Level | Constrains | Licenses |
|---|---|---|
| Configural | same structure | nothing |
| Metric | + loadings | comparing correlations |
| **Scalar** | + **intercepts** | **comparing means ← we need this** |
| Strict | + residuals | comparing raw sums |

**Criterion: ΔCFI > 0.01 ⇒ non-invariance.** (Not the χ² difference test — it "flags trivial
differences in large samples," and our samples are large.) Complementary: ΔRMSEA > 0.015,
ΔSRMR > 0.030 (metric) / > 0.010 (scalar).

### 5.2 When it fails (it will)
**Partial scalar invariance** is a legitimate, publishable outcome: free the intercepts of offending
items, keep the rest. Defensible if a majority of items remain invariant (≥2 per factor minimum).
Practically: find the DIF items, fix or drop them.

### 5.3 RC-DIF — the specific en/zh trap
**Response-category DIF**: judges in different languages interpret the *response categories*
differently — **a Chinese "4" is not an English "4"** — even when they understand the item
identically. Note this is a property of the *scale*, not the *content*, so translating the rubric
better does not fix it.

**Remedy: anchoring vignettes.** Have every judge (en and zh) rate the **same fixed set of anchor
transcripts** with known reference scores. Use their anchor ratings to **rescale each group's
response categories** onto a common metric. This is the single concrete mechanism that makes
"SAME BASELINE" true across languages rather than aspirational.

**Platform requirement:** a permanent, versioned **anchor set** rated by every judge in every
language on every run. Budget ~10-15 anchor transcripts per dimension. Treat it as calibration
infrastructure — like a scale's tare weight — not as eval content.

### 5.4 Characters
95 characters is too many for multi-group CFA per character (each group needs adequate N).
Recommended: **group characters into 4-6 archetypes** (e.g. warm/nurturing, aloof/tsundere,
playful/chaotic, mentor/authority) and test invariance across archetypes. Then model character as a
**random effect**, not 95 fixed groups. This is both statistically sounder and 20× cheaper.

---

## 6. Ranking and aggregation

### 6.1 Use Bradley-Terry, not Elo
```
P(i beats j) = σ(β_i − β_j)
```
**Elo is order-dependent** — shuffle the match history, get different ratings. It is an *online*
approximation to BT, designed for chess where players genuinely change. Our comparisons are **batch
and all available at once**, so fit BT by MLE directly. Using Elo here imports a drawback for no
benefit.

### 6.2 Mandatory: bootstrap CIs
"Bootstrap resampling gives a more reliable variance estimate, especially when the Bradley-Terry
assumptions are violated." **Never render a bare rank.** Ranks without CIs are the single biggest
source of false confidence in a leaderboard. If CIs overlap, the UI must say **"tied."**

Scale check: **"rating differences smaller than 30 Elo points typically require hundreds of
comparisons to validate."**

### 6.3 Monitor intransitivity
Preference cycles (A>B>C>A) genuinely occur because quality is **multi-dimensional**. Under
intransitivity, "estimated ratings are dependent on **who plays who**" — i.e. **the schedule, not
just quality, determines the rating.**

**Count 3-cycles in the empirical preference graph and ship it as a metric.** A high cycle rate means
the scalar leaderboard is **hiding a real trade-off** and that dimension should be reported
per-dimension rather than aggregated. Cycles are not a bug to suppress; they are "indicators of
diverse model specializations."

### 6.4 Do not reproduce the Leaderboard Illusion
We control our sampler, so we have no excuse for any of these:
1. **Pre-register the candidate variant** before seeing arena results. Best-of-N selection
   "systematically inflates the ratings" of whoever submits most variants — Meta tested **27 private
   variants** before Llama-4. Our teams will do exactly this by default.
2. **Equal sampling across variants**, enforced in code.
3. **Never silently deprecate** — removing a model changes the comparison graph and shifts *all*
   ratings.

### 6.5 BT is a cross-check, not the headline
Pairwise BT gives **relative ranking only**. It cannot answer "did we regress vs last release"
against a changing model pool — there is no fixed origin. **"SAME BASELINE" requires
anchored absolute rubric scores as the primary metric**, with BT as a secondary validation that the
absolute scores order models the same way. If BT and rubric disagree, that is a finding worth
investigating, not a bug to paper over.

---

## 7. Sample sizing: detecting a real regression

### 7.1 Declare the MDE first
**Nothing here is answerable without it.** "How many scenarios do we need?" is undefined until
someone states the **smallest regression we care about catching**. Get this decision from the
product owner in writing.

Practitioner calibration: **"If you only care about catching regressions of 10 points or more, 250
examples is sufficient. If you want to catch a 2-point lift, you need thousands of examples per
arm."**

### 7.2 Formulas
Independent arms:
```
n_per_arm = 16 · σ² / MDE²          # α=0.05, 80% power  (constant ≈ 21 for 90% power)
```

**Paired (use this):**
```
n_pairs = (z_{1-α/2} + z_{1-β})² · σ²_d / Δ²
σ²_d = σ²_A + σ²_B − 2ρ·σ_A·σ_B
```

### 7.3 Pairing is the free win — take it
Scenario difficulty (`σ²_i`) dominates our variance. **Run every variant on the identical scenario
set with identical seeds and pair the analysis.** Then `ρ` between arms is high, `σ²_d` collapses,
and required N drops by "an order of magnitude of compute."

**This costs nothing but discipline and is the cheapest power win available.** Make it a platform
invariant: the harness should make it *impossible* to run two variants on different scenario sets.

### 7.4 We have far less data than we think
Observations are **nested**: turns in conversations, conversations in characters, characters in
languages. Treating 190 slices × k scenarios as independent **overstates N**.

```
DEFF = 1 + (m − 1)·ICC        n_effective = n_raw / DEFF
```
With `m=10` scenarios/character and `ICC=0.2`: **DEFF = 2.8 → we have ~1/3 the sample we think.**

Better than correcting: **fit a mixed-effects model** with random intercepts for character and
scenario. Handles nesting natively, and it is the same model family as the G-study (§3), so it is
one piece of infrastructure serving both.

---

## 8. Slicing 95 characters × 2 languages without lying to ourselves

### 8.1 The arithmetic of false alarms
**190 slices × α=0.05 ⇒ ~9.5 false "regressions" per dimension per release, from pure noise.** With
8 dimensions that's ~76 spurious alerts every release. **A team chasing those loses trust in the
platform within two releases** — and the failure mode is not that people are misled, it is that they
correctly learn to ignore us.

### 8.2 Two-tier policy — the core recommendation

**Tier 1 — GATE (blocks release):**
One **pre-registered pooled test per dimension**. One test ⇒ **no correction needed**. This is the
ship/no-ship decision. Pre-registration is what makes it one test rather than a search.

**Tier 2 — SCREEN (never blocks):**
Per-slice tests, **BH-corrected at q=0.10**, surfaced as *"investigate"*. Explicitly labelled in the
UI as exploratory.

**Do not let Tier 2 block releases. Do not let Tier 1 be chosen after seeing the data.** Nearly every
eval platform gets this backwards and drowns in slice noise.

### 8.3 BH procedure
1. Sort p-values ascending `p_(1) ≤ … ≤ p_(m)`.
2. Find the **largest** `k` with `p_(k) ≤ (k/m)·q`.
3. **Reject all `H_(1)…H_(k)`** — including ones with p above their own threshold. *This step-up
   behaviour is what implementations get wrong.*

Adjusted p-values: `p_adj(k) = min_{j≥k}(m/j · p_(j))`, capped at 1.

**Use BH, not Bonferroni.** With m=190, Bonferroni gives α=0.00026 and we detect nothing. BH controls
`E(V/R)` and is "less stringent and increases the method's power."

**Dependence:** our slices are positively correlated (same model, judge, overlapping scenarios), so
**BH under PRDS is defensible**. Fall back to **Benjamini-Yekutieli** (divide q by `H_m ≈ 5.9`) only
if we ever need airtight guarantees — it costs ~6× power.

### 8.4 Shrinkage beats testing
Better than 190 hypothesis tests: a **hierarchical/partial-pooling model**. Character effects are
drawn from a shared prior, so noisy small-N characters shrink toward the global mean automatically.
**Extreme slices stop being extreme unless the data really supports it** — the multiple-comparisons
problem is largely dissolved rather than corrected. Gelman's argument ("we have no multiple
comparisons problems") applies cleanly here.

**Recommendation: skip the 190-test design entirely and go straight to hierarchical.** It is the same
mixed-effects infrastructure as §3 and §7.4 — three sections, one model.

### 8.5 Rank stability = the benchmark-lottery test
Dehghani et al.: **"if tasks were truly independent, the aggregate ranking should remain stable
regardless of the specific subset examined."** That is a **testable diagnostic** and it reuses
existing runs at zero marginal inference cost:

- **Bootstrap-resample the scenario set, refit, re-rank.** Report rank-stability. If our ranking
  flips under resampling, **our scenario set is deciding, not the models.**
- **Perturb prompt format** (reorder rubric dimensions in the judge prompt). If the ranking moves,
  **we are measuring the judge harness.** Rankings "often revers[e] leadership based on minor
  perturbations."

Both belong in CI as release gates on the *instrument*.

---

## 9. IRT: what it buys and what it doesn't

**Buys — efficiency.** Two-parameter model: `p_il = 1/(1+exp(−α_i^⊤θ_l + β_i))` where `θ_l` = model
ability, `α_i` = discrimination, `β_i` = difficulty. tinyBenchmarks: **100 items ⇒ ~2% estimation
error; MMLU 14,000→100 (140×).**

**Doesn't buy — stability.** Madaan et al.: IRT and item analysis **"struggle to meaningfully reduce
variance."**

**The one diagnostic to steal today:** **item discrimination `α_i`**. It directly answers *"is this
scenario earning its place?"* A scenario with `α_i ≈ 0` costs money and tells us nothing — every
model scores the same on it. **Expect a large fraction of our scenario bank to be dead weight**, and
`α_i` finds it cheaply from data we already have.

**Sequencing:** IRT is a phase-2 optimization. Get reliability, anchors, and invariance right first —
IRT on an invalid rubric just makes a broken measurement cheaper to compute.

---

## 10. Recommended build order

| Phase | Work | Gate |
|---|---|---|
| **0** | Construct definitions; **BARS retranslation**; 0-5 anchored rubric | >70% sort-back |
| **1** | 3 judges, pilot **G-study** (5 models × 40 scenarios × 3 judges × 3 runs) | Φ ≥ 0.80/dim |
| **1** | **Noise floor** (seed re-runs) | measured & rendered |
| **2** | Discriminant matrix + factor analysis | inter-dim r < 0.7 |
| **2** | **Anchor vignette set**, rated every run, every language | built & versioned |
| **2** | **Scalar invariance** en/zh | ΔCFI < 0.01 |
| **3** | Hierarchical model; paired designs; declared MDE | powered for MDE |
| **3** | BT + bootstrap CIs; cycle monitoring | CIs shipped |
| **4** | Rank-stability + prompt-perturbation CI gates | stable |
| **4** | IRT for scenario pruning (`α_i`) | — |

---

## 11. The ten things that make this measurement rather than vibes

1. **Retranslation before code.** <70% sort-back ⇒ the dimension isn't real. Cheapest kill signal.
2. **0-5 scale, behaviourally anchored at every level.** Empirical, not taste.
3. **Φ (dependability) ≥ 0.80 per dimension** — absolute, not relative. Below 0.67: don't publish.
4. **SEM as the headline number**, because reliability is population-dependent and will look fake-bad
   on similar checkpoints.
5. **Noise floor from seed re-runs**, rendered on every chart. Nothing below it is reportable.
6. **Anchoring vignettes + scalar invariance (ΔCFI<0.01)** — this *is* "SAME BASELINE" across en/zh.
   A Chinese 4 ≠ an English 4 until proven otherwise.
7. **Pair everything.** Identical scenarios, identical seeds, paired analysis. Order-of-magnitude
   compute win for free.
8. **Two-tier testing**: pre-registered pooled gate; BH q=0.10 slices that never block. Better:
   hierarchical shrinkage instead.
9. **BT + bootstrap CIs, never bare ranks; monitor cycles.** Pre-register candidates or we rebuild
   the Leaderboard Illusion in-house.
10. **Consequential validity has an owner.** For every dimension, name the model that would win by
    gaming it. For a companion product, "engagement" gamed = **emotional dependency**. That is a
    product risk, not an academic footnote.

---

## 12. Honest limitations of this note

- **Sources 2-8 are compilations** of reference/tutorial material and practitioner blogs, not single
  primary papers. The CTT, IRR, invariance, G-theory, FDR, and power files consolidate standard
  textbook results with the canonical citations named inline. The formulas are standard and
  verifiable; the *thresholds* are conventions, not laws.
- **Threshold numbers are conventions.** α≥0.80, ΔCFI>0.01, ICC bands, Landis-Koch labels are all
  community rules of thumb with real dissent behind them (Schmitt: "no sacred level" of alpha). They
  are defensible defaults and negotiating positions, not physics. **Declaring ours in advance is what
  matters more than which number we pick.**
- **The multi-group CFA prescription (§5) assumes a factor structure** across items within a
  dimension. If each dimension is a single judge score with no multi-item structure, classical MG-CFA
  doesn't directly apply and we'd need multi-group IRT / DIF testing on the item bank instead. **This
  is a real open design question** and depends on whether our rubric produces per-item sub-scores or
  one holistic score per dimension. If holistic, §5 needs rework — flagging explicitly rather than
  hiding it.
- **Li et al. 2026 (0-5 scale) is a single recent paper**, verified as real but not yet
  independently replicated as far as this research found. The direction (narrower scales, anchored)
  is corroborated by the broader central-tendency-bias literature; the specific "0-5 is optimal"
  claim rests on one study.
- **Not covered:** conformal prediction for calibrated judge uncertainty; Nash-averaging as an
  intransitivity-robust alternative to BT (Balduzzi et al. "Re-evaluating Evaluation"); judge
  fine-tuning/distillation; cost modelling. Nash-averaging in particular deserves follow-up if §6.3
  cycle counts come back high.
