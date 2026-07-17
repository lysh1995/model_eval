# The evaluation design — final

**Supersedes** [notes/11](../research/notes/11-evaluation-method-design.md) (organizing principle
survives; sufficiency claim and item 9 do not). Consolidates notes 00–22 and five adversarial
cross-checks.

**Status: decided.** Open items are listed as decisions-with-rationale, not questions.

---

## 1. The construct

**A roleplay model does three separable jobs, in causal order** ([ABILITY-MODEL](ABILITY-MODEL.md)):

**L1 comprehension** (understands the character *and* the user) → **L2 application & steerability**
(holds the character; can be moved by prompt words) → **L3 creativity** (makes something worth reading).

**This is not novel and we stop pretending it is.** Funder's **Realistic Accuracy Model** (1995) is
the same cascade — *"if any stage is unsuccessful, an accurate judgment is not possible"* — explicitly
**necessary and multiplicative**. We cite it.

**Test it as necessity, never as correlation.** A necessity claim predicts a **triangular
scatterplot**, so a low r is what a *true* cascade looks like. The test is **the empty cell**: high L2
with low L1. Nobody has ever regressed portrayal on comprehension — in humans or models. That is our
gap to fill, and it is **experiment #1**.

**And three things sit outside the model entirely** — scoring perfectly on all three layers excludes
none of them: **regurgitation** (Luda), **user-side abuse** (we instrument 1 of 2 agents),
**IP/provenance**.

## 2. The two rules that decide everything

**Rule 1 — match the instrument class to the aspect class.** Never average across classes.

| class | example | instrument | report |
|---|---|---|---|
| **deterministic** | exceeded the length cap? contradicted the card? | computation | rate |
| **consensus** | is this a plot hole? did the scene advance? | judge/NLI **bound to a referent** | κ + rate |
| **perspectival** | is this compelling? | **preference** | **distribution, never a mean** |

α = 0.25–0.34 is **not** rater failure. It is **what you get scoring a perspectival aspect with a
consensus instrument.** A category error, and ours to stop making.

**Rule 2 — bound beats better.** Agreement tracks whether a question ties to a **retrievable
referent**, not whether it's "objective":

| question | agreement |
|---|---|
| *"is claim X supported by **record entry Y**?"* | κ ≈ 0.78–0.94 |
| *"does this contradict **something earlier**?"* | 65.28% unanimous |
| *"is this good?"* | α = 0.25–0.34 |

**The record's job is converting question 2 into question 1** — a **0.4–0.6 κ swing from
restructuring**, larger than any judge upgrade we can buy. **And where no referent exists,
manufacture one by perturbation**: the clean-input response is the referent for a degraded input; the
prompt delta is the referent for steerability. That is the single most reusable move in this design.

> **Caveat, load-bearing:** the κ≈0.78–0.94 band is a property of *particular well-posed questions*,
> not of boundedness. Direct counterexample in our exact condition: 8 raters, 4 movie characters,
> **ICC .88 → .05** depending on what is asked. **Measure ours; do not inherit theirs.**

## 3. The correction that reshaped this design

> **"The framework sorts measurements by reliability and never checks validity."**

Reliable ≠ valid. **Faux Pas: scoring ICC = .996, correlates −.029 to .135 with every other ToM
task.** Empathic accuracy: α ≈ .90, **r = .06** with its nearest neighbour. And where anyone measured
an outcome (Elliott, **6,138 clients**) the reliable measure was **"virtually unrelated"** while the
**perspectival** one predicted best (**r = .28**).

**Therefore:** every dimension carries a **validity claim**, not just a reliability number. The
question is never *"can we measure this consistently?"* but *"does this predict something we care
about?"* — and for most of the catalogue, **the honest answer today is "unknown."** That is why §7
exists.

**Empirically, defect-only measurement inverts the ranking:** RPGBench — **Claude 3.5 Sonnet best on
interestingness (0.722), best on factual consistency (0.991), worst on mechanic score (0.113).** A
hygiene catalogue **no-ships the most interesting model**. CICERO is the same error, shipped by Meta:
consistency-with-state **87.3%**, consistency-with-plan **92.9%**, *"high quality"* **37.3% for every
variant** — they never operationalized good.

## 4. What ships — the cut

**From 50 named to 14.** Everything else is a diagnostic, a research question, or dead.

### Tier A — ships now, judge-free, validated or near
| | benchmark | why it survives |
|---|---|---|
| **A1** | **Repetition / looping** | **Validated: 10–13× MDE.** Free. Maps to a top-3 user complaint. grok-4.1: 1.4% en → **29.6% zh** |
| **A2** | **Character discriminability (signed)** | **Prices the business asset.** Prior art (Miyazaki & Sato, 29 characters, LIBLINEAR). Signed: a character is partly defined by markers they *refuse* |
| **A3** | **Voice homogenization** | length-controlled only; **zh residual ρ=+0.264 unresolved** — ships with the caveat attached |
| **A4** | **Length-cap adherence** | bound to **the variant's own spec**. Trivial, exact |
| **A5** | **Format discipline** | regex; exact |

### Tier B — the ability probes (needs the key; highest value per dollar)
| | benchmark | why |
|---|---|---|
| **B1** | **L1 comprehension probes** | bound to the card. CharacterBench's target-guided probes are worth **~17 Pearson points — more than the fine-tune** |
| **B2** | **L1.2 discrimination/generation gap** | separates *"knows better than it acts"* (prompt fix) from *"doesn't understand"* (**model migration**). **No benchmark separates them, and the price tags differ by orders of magnitude.** **Existence proof in the wild:** in the Roose/Sydney transcript the model recites its persona spec near-verbatim earlier in the *same session* and violates it later — **comprehension intact, execution collapsed** |
| **B3** | **Ψ2 internal consistency (Cronbach's α)** | **needs no ground truth at all.** α≈0.8 → a personality is represented; α≈0 → **confabulated one item at a time** |
| **B4** | **Ψ1 test–retest stability (turn 5 vs 95)** | **donates a calibrated noise floor** (human BFI r≈0.75–0.90) instead of us buying one |
| **B5** | **L2.2 steerability elasticity** | **a variant IS a prompt.** If DEAD, the lifecycle is a ritual. **The DEAD hypothesis is now the prior** |

### Tier B+ — style contagion, promoted on vendor evidence

| | benchmark | why |
|---|---|---|
| **B6** | **I2 style contagion / register bleed** | **Two vendors independently named this as their production failure.** Microsoft (2023): *"The model at times tries to respond or reflect in the tone in which it is being asked."* xAI (2025): *"the instruction to 'follow the tone and context' … caused @grok to prioritize adhering to prior posts in the thread … as opposed to responding responsibly."* **Proximate context tone defeats the persona anchor** — a drift mechanism driven by *input*, not by anchor distance. Two-sided: **accommodate in content and emotion, never in voice and register** |

**Both vendors also say production is where persona failures are found** — Microsoft as confession
(*"not something we would typically find with internal testing"*), xAI as policy (*"an accelerant"*).
**That is a stated ceiling on the offline gate, from the two orgs with the most at stake**, and it
raises the value of the online half relative to the benchmark.

### Tier C — safety (non-negotiable; legally load-bearing)
| | benchmark | why |
|---|---|---|
| **C1** | **Crisis detection → escalation** | **Raine: 377 flags, 23 >90% confidence, nothing happened.** Detection without escalation manufactures the plaintiff's exhibit |
| **C2** | **Post-referral trajectory** | **Gavalas: the statutory floor fired correctly and the user died.** Does the character hold the crisis frame or revert to the persona? **Nobody measures this** |
| **C3** | **Uplift ⟂ over-refusal** (two axes, never averaged) | Anthropic's own constitution names *"refuses to engage with fiction"* as a **defect** |
| **C4** | **Warmth × sycophancy frontier** | **Same dial, opposite directions**: Anthropic cut sycophancy → colder model; xAI tuned Grok 4.1 for *"more natural, fluid dialogue"* → **sycophancy tripled (0.07→0.23)** and it shipped at **MASK 0.49 against a 0.50 deployment ceiling** — one hundredth under its own bar. Worse: **opinion-sycophancy is flat at 0.36→0.35→0.38 across three generations while factual sycophancy was fixed.** For a companion product, **opinion sycophancy is the whole game, and nobody is moving it** |
| **C5** | **Regurgitation / PII** | **Luda: a leaked real address passes every other metric here.** Fidelity is *positively correlated* with the leak |

### Tier D — the product question (needs production)
| | benchmark | why |
|---|---|---|
| **D1** | **Q1 head-to-head user preference** | The only thing that answers *"is it good?"* — **~5M free pairwise labels/day** from regenerates |

### Cut, and why — this is the important half

| cut | reason |
|---|---|
| **Emotional attunement as a gate** | Judge sentiment bias **RR 0.60–0.80 → 0.24–0.66 under sadness/anger/fear, no published mitigation** — least reliable exactly where our traffic lives. **Keep as a diagnostic; it never gates.** *(Decision on your open question #1.)* |
| **"Consistency" as trait stability** | **Anti-correlated with the construct.** Mischel & Shoda: signature stability is *"negatively related"* to cross-situational consistency. It **punishes characters that behave like people**. Replaced by if-then signature stability (target .41–.48; **>.90 flags rigidity**) |
| **The trait×trait matrix as a model property** | **Asch Exp. IV: coefficients are not stable across sheets.** It is a per-sheet diagnostic, not a property of the model |
| **Crosstalk as "the killer"** | **Crosstalk is realism.** warm→cold moves `generous` **91%→8%**. Traits *should* propagate |
| **Per-cell Δs / elasticity from differences** | `r_DD = (r_xx+r_yy−2r_xy)/2(1−r_xy)` — **our own experimental control drives reliability toward zero.** Fit **random slopes** |
| **N4 branch divergence as a gate** | **Fendt: players cannot distinguish real branching from fake.** Measures actual agency; the product construct is *perceived* agency. Diagnostic only |
| **N6 wimp rate as a gate** | May score a **feature** as a defect — our traffic prior (Affection & Comfort 8.0%, Casual Greetings 10.6%) suggests users may *want* low-tension affirmation. **Gate on the LDA study first** |
| **Raw per-character verdicts** | **19.4pp MDE at n=3.** Shrunk estimates or nothing |
| **"As an AI" as a dimension** | ≤3.2/1000 turns, zero for most models. **Tripwire** |
| **Absolute creativity scores** | **r = 0.159.** Pairwise or nothing — *we are stricter than Anthropic here, deliberately* |
| **"Helpfulness" in any companion rubric** | SoulChat: empathy and helpfulness **cross over**; summing ranks two **opposite products** as near-ties (3.56 vs 3.71). It doesn't merely fail to help — **it cancels the signal that matters** |

## 5. The judge protocol — final

1. **Pairwise against a frozen anchor set.** Never absolute. O(n), not O(n²).
2. **Score-based comparison, not Likert** — **31pp** on format alone.
3. **Reference-anchor every judgment** (card + human exemplar). MT-Bench math failure 70%→15%.
4. **Family-disjoint panel of 3.** τ 0.778 vs 0.667 at **7–8× lower cost**. Strict dominance.
5. **Swap-and-average by default.** ⚠️ **Reversed:** I relied on position bias ≤0.04 (benchmark data);
   a **541k-judgment study finds >0.10 in production judges.** Swap until we have our own number.
6. **Abstain (~20%) → human queue** = a free calibration set on exactly the hard cases.
7. **Report Cohen's κ. Never percent agreement.** The famous "80%" is raw, ties-excluded, base-rate-inflated.
8. **Judge version = `(model_snapshot, prompt_hash, rubric_ver, decoding, seed)`.** A bump is a
   **breaking change**. GPT-4 went 84%→51.4% in three months.
9. **Bradley-Terry with style covariates.** Length coefficient **0.249, ~8× any format term**; under
   style control **Grok-2-mini moved 12 ranks**. Unmitigated, we ship a verbosity meter.

## 6. Normalization — the seven senses

1. **Across models** → BT latent scale vs frozen anchors. *This is "same baseline."*
2. **Length** → style covariates **inside** the model, not post-hoc division.
3. **Across languages** → **refuse.** ρ(en,zh) = **−0.082**; and every SRM variance component differs
   ~2×. The platform must decline to emit a pooled cross-language number.
4. **Across characters** → shrinkage. Never a raw cell.
5. **Across judge versions** → re-baseline. Never silently rescale.
6. **Across turns** → **min, not mean** (**87% vs 75%** human agreement). A mean launders the one
   catastrophic turn.
7. **Effective n** → **conversations, not turns.** ~95, not 313,500. **42% of turn-level findings are
   spurious** without this.

## 7. The gate rule

**No dimension ships without:** σ_within · MDE at planned n · **registered confound tests with
measured residuals** · **a stated validity claim** (what does this predict?). Judge dimensions add
**κ vs a human calibration set** and an **abstention rate**.

**Currently 1 of 50 dimensions clears this.** The rule stays anyway — it is the only thing standing
between this platform and confident, well-formatted, wrong numbers. **We produced four of those
today**, each invisible in the output: a length confound (ρ=+0.73), a survivorship confound, a broken
p-value (0.006 vs 0.070 true), and a cited MAU figure with **no source at all**.

## 8. What the platform refuses to do

- Emit a **pooled cross-language** score.
- Display a **raw per-cell** score.
- Report **percent agreement**, or **turn-pooled n**.
- Let **preference evidence reach the harm path** — Cheng et al. (*Science*, N=2,405): a single
  sycophantic interaction degrades conflict repair **and users rate the harmful condition higher**.
  Preference answers *quality*; it is **inadmissible for harm**.
- **Average two defects** (uplift/over-refusal; warmth/sycophancy).
- Let a **green quantitative board** override a **qualitative veto**. OpenAI's April 2025 rollback
  happened *because* the A/B tests approved and expert dissent was overruled.

## 9. Decisions on the open questions

| # | question | **decision** |
|---|---|---|
| 1 | Emotional attunement? | **Cut as a gate, keep as diagnostic.** No mitigation exists for the bias, and it sits on our core traffic |
| 2 | Underpowered benchmark? | **Add runs, not characters.** Generation is ~100× cheaper than judging, and **σ_within is 61.5% of en variance** — runs attack the dominant term. Characters attack a **1.6%** term |
| 3 | Qualitative veto? | **Yes — mandatory.** Non-negotiable (AC10) |
| 4 | Legal review? | **This week.** EU Art 50 in **17 days**; the Chinese statute is corroborated by two independent streams but **needs counsel on the gazette** |
| 5 | API key? | **Blocking Tier B entirely.** B5 (steerability) first — **if DEAD, the variant lifecycle is a ritual and this platform's premise fails** |
