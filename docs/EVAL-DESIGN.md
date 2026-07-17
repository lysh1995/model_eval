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

## 4. Two jobs, two bars — the reclassification

**Earlier drafts of this document made a category error:** they applied a *gate's* standard to the
whole catalogue, concluded "45 of 46 can't pass," and cut. **True, and irrelevant** — most dimensions
were never trying to gate.

| job | what it does | if it's wrong | bar |
|---|---|---|---|
| **GATE** | **blocks a ship** | you ship something bad, or block something good — and **false alarms teach the team to ignore the platform** | σ_within, MDE, confound tests, validity claim |
| **GUIDE** | **tells a human building the product what to do** | someone loses an afternoon — **recoverable, if labeled honestly** | sensible construct · **honest uncertainty** · **actionable** |
| **DEAD** | — | **it points the wrong way**, or cancels a signal that matters | — |

**The cut criterion is not "unproven." It is "directionally wrong."** A noisy number with an honest
interval is a *guide*. A confident number that measures the inverse of its label is *dead*. Only the
second deserves deletion, and the list is short.

**Most of this catalogue is guide-grade, and that is the point.** The product value here is not a
pass/fail light — it's **"here is what to change and why."** A metric that says *"your Chinese
characters homogenize 6× more than your English ones, ±wide interval"* is worth more to a team than a
green checkmark, even though it could never block a release.

### 4.1 GATE — very few, and that's correct

| | benchmark | why it can block |
|---|---|---|
| **A1** | **Repetition / looping** | **Validated: 10–13× MDE.** The only dimension with a measured noise floor |
| **A4** | **Length-cap adherence** | bound to **the variant's own spec**; exact |
| **A5** | **Format discipline** | exact |
| **C1** | **Crisis detection → escalation** | **Raine: 377 flags, 23 >90% confidence, nothing happened.** Legally load-bearing, and a zero-tolerance event needs no MDE |
| **C5** | **Regurgitation / PII** | **Luda.** A single verbatim leak is a company-ending event. Zero-tolerance, no statistics required |

**Everything else informs. Nothing else blocks** — except the human veto (AC10), which needs no
statistics at all.

### 4.2 GUIDE — the actual deliverable

**Each of these is here because it produces a *guideline*, not a score.** The right-hand column is
the product value; the score is just how we get there.

| | benchmark | **the guidance it produces** |
|---|---|---|
| **B5** | Steerability elasticity | **"Emphasis words don't work on this model — put decisive traits first."** A house style guide for writing character sheets |
| **B1/B2** | Comprehension probes + discrimination/generation gap | **"This is a prompt fix, not a model migration"** — or the reverse. The two look identical in every output metric and differ in cost by orders of magnitude |
| **B3** | Cronbach's α on the character's own items | **"There is no character in there — it's confabulating per item."** Needs no ground truth |
| **B4** | Test–retest stability (turn 5 vs 95) | **"Personality decays past turn ~40; re-anchor at 30."** Borrows a human baseline (BFI r≈0.75–0.90) |
| **B6** | Style contagion | **"Your character starts typing like the user."** Named by Microsoft *and* xAI as their production failure |
| **C4** | Warmth × sycophancy frontier | **"You are here on the frontier; moving up costs this much sycophancy."** Grok: tuned for appeal → sycophancy **0.07→0.23** |
| **A2** | Discriminability (signed) | **"The model renders 71% of your characters distinguishably, down from 84%"** — prices the catalogue, the business asset |
| **A3** | Homogenization | **"Your zh characters collapse; your en ones don't."** Ships with its zh caveat (ρ=+0.264) attached |
| **K3** | Fidelity ↔ diversity | **"Optimizing per-character fidelity is destroying your catalogue."** Cohen's d up to 15.7 between persona groups |
| **C2** | Post-referral trajectory | **"After a crisis referral, your character resumes the roleplay."** **Gavalas.** Nobody measures this |
| **C3** | Uplift ⟂ over-refusal | **"You are 3× over-refusing to buy 2% less uplift."** Two axes, never averaged |
| **N1/N3/N7/N8** | Craft metrics | **"Scenes don't advance; the bot talks and moves nothing."** Scene-ignorance beat roboticness 76 vs 65.69 with improvisers |
| **I1/I3/I4/I6** | Input robustness | **"You break on code-switching"** — a third measurement context we've never tested |
| **C4′** | **Emotional attunement** | ⚠️ **Restored as a guide.** Sentiment bias (RR 0.24–0.66 under sadness/anger/fear) makes it **unreliable, not inverted** — and it's unreliable exactly where our traffic lives. **Never gates; always ships with the bias printed next to it.** A caveated signal beats no signal on the dimension the product is made of |
| **N4** | Branch divergence | ⚠️ **Restored as an engine diagnostic.** Fendt: players can't *perceive* the difference — but **zero divergence still means user input isn't propagating**, which is a real defect even if users can't articulate it |
| **N6** | Block / wimp rate | ⚠️ **Restored, segmented.** May score a feature for Affection & Comfort users (8.0% of traffic) and a defect for adventure users. **Report by segment, never pooled** — the pooled number is the only wrong version |
| **Per-character cells** | | ⚠️ **Restored, shrunk, with intervals.** ±19pp at n=3 — useless as a verdict, **useful for finding examples to read.** Debugging affordance, explicitly labeled as such |

### 4.3 DEAD — short list, and these genuinely go

| cut | why it points the wrong way |
|---|---|
| **"Consistency" as trait stability** | **Anti-correlated with the construct.** Mischel & Shoda: signature stability is *"negatively related"* to cross-situational consistency. **It fires hardest on characters that behave like people.** Replaced by if-then signature stability (target .41–.48; **>.90 flags rigidity**) |
| **"Helpfulness" in a companion rubric** | **Cancels the signal.** SoulChat: empathy and helpfulness cross over; summing ranks two **opposite products** as near-ties (3.56 vs 3.71) |
| **Absolute creativity scores** | **r = 0.159**, 40% run-to-run consistency. Not noisy — **noise dressed as signal.** Pairwise or nothing |
| **Per-response quality scoring** | **Directionally wrong**, measured: FED ranks **Meena (4.19) above Human (3.85)** per-turn; at dialogue level it **flips** (Human 4.60 > Meena 4.11) |
| **Turn-pooled n** | Overstates evidence **60×** |
| **Pooled cross-language scores** | ρ(en,zh) = **−0.082**. An average of two unrelated quantities, wrong about both |
| **The trait×trait matrix as a *model* property** | **Asch Exp. IV: coefficients aren't stable across sheets.** *(Survives as a per-sheet diagnostic — that version is a guide, and a useful one for authors.)* |
| **Elasticity from per-cell Δs** | `r_DD` → our own control drives Δ-reliability toward zero. *(The construct survives; fit **random slopes**.)* |

**Note the pattern:** almost everything in 4.3 is a **method** error, not a **construct** error. The
constructs mostly survive — we just measure them a different way.

## 4.4 The old cut list, for the record

**From 50 named to 14** — *this was the earlier framing and it was wrong.* It optimized for
defensibility against a hypothetical challenger rather than usefulness to the team actually building
the product. **The gate list is short (5). The guide list is most of the catalogue. Both are correct.**

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

## 7. The two rules — one per job

**These are different bars, and applying the gate's bar to guides is what produced the bad cut in §4.**

### To GATE (block a ship)
σ_within · MDE at planned n · **registered confound tests with measured residuals** · **a stated
validity claim**. Judge dimensions add **κ vs a human calibration set** and an **abstention rate**.

**Currently 5 dimensions clear this** (3 by measurement, 2 by zero-tolerance). That is the right
number. A platform where everything can block is a platform that gets switched off.

### To GUIDE (inform a human)
1. **A sensible construct** — it names a real failure someone would act on.
2. **Honest uncertainty, printed next to the number.** Not in a footnote, not in a doc — **on the
   number.** `homogenization: 0.677 (zh; length-controlled; residual ρ=+0.264 — treat as directional)`.
3. **Actionable** — it implies a change. *"Emphasis words don't work; put decisive traits first"* is a
   guide. *"Fidelity: 3.2"* is not.
4. **Registered confounds still required.** ⚠️ **This one doesn't relax**, and it's the only rule
   carried over intact — because a *confounded* guide isn't uncertain, it's **wrong**, and it points
   somewhere specific and false. A length confound doesn't make the answer fuzzy; it makes the answer
   "verbosity" while the label says "voice."

**The distinction that matters:** *uncertain* is fine for a guide — say so and move on. *Confounded*
is not, because the reader can't tell the difference and the error has a direction.

### Why the discipline stays even though the bar dropped

**We produced four confident, well-formatted, wrong numbers today**, each invisible in the output:

| | what it looked like | what it was |
|---|---|---|
| homogenization | a clean model ranking | **verbosity** (ρ=+0.73 with length) |
| the fix for it | a cleaner ranking | **survivorship** — 3 of 45 characters funded the budget |
| a p-value | **p = 0.006**, significant | **p = 0.070**, null. Hand-rolled `betainc` |
| "~8M MAU" | a cited fact, used 5 times | **SEO aggregators citing each other. No source exists** |

**None of these would have been caught by a lower bar or a higher one.** They were caught by
*redundant checks* — a second query nobody was required to run. **That's the discipline: not "prove
it before you ship it," but "never let a number out without the check that could have falsified it."**

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
