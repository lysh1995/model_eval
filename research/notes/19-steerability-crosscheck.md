# 19 — Steerability cross-check: is L2.2 novel, done, or flawed?

**Task:** adversarially validate or refute [ABILITY-MODEL.md §3](../../docs/ABILITY-MODEL.md) L2.2 — the claim
that steerability is (1) unmeasured, (2) should be measured as dose-response elasticity, (3) fails in three
modes (DEAD / BRITTLE / ENTANGLED, the last via a steerability matrix).

**Verdict: the framing is refuted; a narrower version of the experiment survives and is worth running.**

| our claim | verdict | the killer |
|---|---|---|
| "steerability is unmeasured anywhere" | ❌ **false** | it's an operationalized term with published formulas (Vafa et al. 2025); PsySET benchmarked prompt-intensity control in 2025 |
| "dose-response elasticity is our method" | ❌ **already published, in our domain** | Kirk et al. — "non-linear **dose-response** curves", companion AI, N=3,534 RCT, per-unit slopes for prompting |
| "elasticity = Δout/Δin, fit the curve" | ⚠️ **unit-less denominator; wrong functional form** | the one paper that fit it needed a **cubic**; adverbs have no units |
| "BRITTLE is a failure mode" | ❌ **it's the base rate** | 76-point spread from *separators alone* (Sclar) — vacuous unless null-calibrated |
| "DEAD is a failure mode" | ✅ **real and informative** | PsySET: adverbs move tone, **not** lexical substrate (0.50→0.51) |
| "ENTANGLED — nobody has done the matrix" | ⚠️ **half-true, and better than we thought** | crosstalk is measured (Anthropic, *Personality Illusion*) — but **both papers bury an off-diagonal-dominant result** |

---

## 1. "Nobody measures steerability" — false, and the word is taken

- **Vafa, Bentley, Kleinberg & Mullainathan** (arXiv 2503.17482) formally decompose a **producibility gap** and
  a literal **"steerability gap"**. Their number is brutal for the platform's premise: **5 prompting attempts
  beat attempt 1 only 62% of the time** (chance = 50%).
- **PsySET** (ACL 2026, `steer-psyset.md`) is the closest prior art and it is very close: it steers Big Five +
  emotions with **intensity adverbs ("slightly"/"intensely")**, across 4 models, comparing prompting vs vector
  injection vs SFT vs DPO, *and* measures side effects on unrelated axes.
- **HELM has no steerability axis** — but its "calibration" is a name collision with Chang et al.'s
  "miscalibration" (= normalized gain). **Never write bare "calibration" in our docs.**

**Consequence:** delete "as far as the research found, unmeasured anywhere" from §3. It is the one sentence in
ABILITY-MODEL.md that a reviewer can falsify in a single search, and it discredits the rest by association.

## 2. Dose-response is published, by name, on companion AI — with prompting as an arm

`steer-dose-response-companion-rct.md` — **Kirk, Davidson, Saunders, Luettgau, Vidgen, Hale & Summerfield**
(Oxford Internet Institute / UK AISI), arXiv 2512.01991. *Abstract verified verbatim by me:*

> "The psychological impacts of AI followed **non-linear dose-response curves**, with **moderately**
> relationship-seeking AI maximising hedonic appeal and attachment."

N = 3,534 RCT, four weeks, dose = steering multiplier **λ ∈ {−1, −0.5, 0, +0.5, +1}**. And (body, not abstract)
they computed our metric for prompting:

> "Each unit increase in steering intensity increased relationship-seeking scores by **2.39 points** versus
> **0.78** (GPT-4o, 3× stronger) and **1.83** (Claude)."

Three findings that directly damage the design as written:

1. **Prompt-dosing is the weak knob** — GPT-4o's prompt slope is **~⅓** of the steering slope.
2. **Prompt-dosing is fragile** — under persona attacks, prompting drops **3.9–4.5 points**; steering **<0.25**.
3. **The curve is cubic and peaks at moderate dose** — "significant positive linear λ coefficient paired with
   **negative quadratic and cubic coefficients**". A single-slope elasticity would report *zero* for a curve
   that rises then falls. **Our headline metric would be blind to their headline finding.**

Other names for our method, all pre-existing: **"control strength"** (DExperts α), **"guidance scale"** (CFG γ),
**"steering multiplier"** (CAA — claims "precise control over the **degree** of the targeted behavior"),
**"intensity control"** (a named style-transfer subfield), **"personality shaping"** (Serapio-García et al.,
Nature MI — **9 intensity levels** set by Likert adverbs *"a bit / very / extremely"*, monotonicity verified at
Spearman **ρ ≥ 0.90**). The trait-word ladder was published in 2023.

## 3. BRITTLE is not a failure mode — it is the denominator

The base rate of "tiny wording changes swing behavior" is ~100%. Semantically *null* perturbations already do:

| source | perturbation | magnitude |
|---|---|---|
| Sclar (ICLR'24) `steer-formatspread.md` | separators / casing | **up to 76 pts**; median 12–28 |
| Cao (NeurIPS'24) `steer-worst-prompt.md` | paraphrase, **open-ended** | **45.48** (Llama-2-70B-chat); every model ≥32 |
| Pezeshkpour (NAACL'24) | option order | **13–75%** |
| Mizrahi (TACL'24) | instruction paraphrase | negative Kendall's τ on **15/25** tasks |
| Leidinger (EMNLP'23) | one modal verb | **10–17 pts** |

And it **does not shrink with scale** (Llama-2 7B/13B/70B gaps = 38.12 / 47.22 / **45.48**) and **does not
transfer** (Sclar Table 2: **57.46%** 7B→13B same family, vs **50%** chance; Cao worst-prompt overlap **2%**).
Mizrahi's killer datum: `'excludes'→'lacks'` = **−28% on Flan-T5-large, +46% on Flan-T5-XL** — same edit,
opposite signs.

**So a large measured "elasticity" proves nothing.** Our intensity ladder changes *both* meaning and surface
form. Without a null control the slope is unfalsifiable — it could be entirely the 76-point noise process.

**This is the single most important design change.** The literature already has the concept we need and we
weren't using it: **CheckList** (Ribeiro, ACL 2020 best paper) splits **INV** (label-preserving → expect *no*
change = spurious) from **DIR** (expect a *directional* change = intended). Every brittleness paper measures
only INV; every steering paper measures only DIR. **Nobody computes the ratio.** That ratio — intended
sensitivity over spurious sensitivity — is a **signal-to-noise ratio for a prompt**, it is one division away,
and it is the most defensible novel thing in this note.

> **Redefine:** `steerability = Δbehavior(meaningful edit) / Δbehavior(null edit of matched surface size)`.
> A model is steerable iff it moves **more** for meaning than for whitespace. Sclar's FormatSpread *is* our
> denominator — reuse it rather than competing with it.

## 4. Crosstalk — measured, and the buried result is our opening ★

**Anthropic, Persona Vectors** (arXiv 2507.21509). I extracted Figure 20 from the v3 PDF text layer myself and
recomputed it (`steer-persona-vectors-crosstalk.md` has both full 7×7 matrices).

- **Trait vectors are not orthogonal:** evil↔sycophantic cos = **0.412** (Llama) / **0.368** (Qwen);
  impolite↔apathetic = **0.734** / **0.542**; evil↔optimistic = **−0.469** / **−0.472**.
- **Footnote 6** (verbatim): "persona shifts are **rather correlated** between seemingly different traits …
  negative traits (and, surprisingly, humor) **tend to shift together**".
- "datasets targeting one trait (e.g., evil) can **inadvertently amplify other traits**."

**★ The finding I'd lead with — their caption is contradicted by their own figure.** Caption: "Each trait's own
direction yields the highest predictive accuracy for its behavior." Recomputed: **false in 7/14 trait×model
rows** (Llama 4/7, Qwen 3/7; also 3/7 column-wise in both, so it's robust to orientation). Llama's Evil
behavior is better predicted by the **Impolite** direction (**0.974**) than by Evil's own (**0.930**). Mean
margin diag−off is only **+0.118** (Llama) / **+0.122** (Qwen).

**★★ And the headline separability claim is computed on the 3 least-entangled traits.** Main text: "strong
positive correlations (**r = 0.76–0.97**) … higher than **cross-trait baselines (r = 0.34–0.86)**, indicating
that persona vectors capture signal that is **specific to their assigned trait**". I reconstructed both ranges:
restrict Figure 20 to the **Evil/Syco/Hall** 3×3 submatrix over both models and you get diagonal
**0.758–0.967** = "0.76–0.97" ✓ and off-diagonal **0.344–0.861** = "0.34–0.86" ✓ — exact. Over all **7** traits
in the very appendix that sentence cites, the off-diagonal range is **0.234–0.985**, **23/84 cells exceed the
quoted 0.86 ceiling**, and the two ranges **overlap on [0.758, 0.985]**. Hallucination — the near-orthogonal
outlier (cos 0.19–0.25 to everything) — is carrying the claim.

Corroboration from prompt space: ***The Personality Illusion*** (arXiv 2509.03730, `steer-personality-illusion-crosstalk.md`)
injects one trait and regresses **all six**: injecting self-regulation moves **conscientiousness β≈4.2–4.8,
p<.001 — "exceeding even the effect on self-regulation itself"** (own diagonal β≈2.2–2.9). The matrix is
**asymmetric** (SelfReg→Agr significant; Agr→SelfReg n.s.) — **you cannot estimate half and mirror it.**

**Anthropic explicitly leaves our question open** (Discussion, verbatim): *"**Do correlations between persona
vectors predict co-expression of the corresponding traits?**"* Their matrix is over *finetuning* shifts and
*vector geometry* — never over **prompt-induced behavioral co-expression**. That gap is real.

### The correction that saves the metric

Raw crosstalk is **not** a bug. `steer-structural-amplification.md`: LLMs reproduce the human trait-correlation
network at **R² > 0.88** with slope **k = 1.42** (Gemini 2.5) — **all 7 frontier models k > 1.0**. Shy→agreeable
spillover is partly the model being *realistic*. And `steer-big5chat-trait-correlation.md`: Frobenius distance
from a **619K-human** correlation matrix — **prompting 2.10**, DPO 2.06, **SFT 1.55**. *Prompting is the worst
method.*

> **The metric is not the off-diagonal. It is the off-diagonal minus the human-baseline correlation.**
> Measured against identity, every model looks broken and the number is uninterpretable. Measured against the
> human matrix, we get the *excess* entanglement — which is what actually breaks an author's mental model.

## 5. FollowBench does not implement our dose-response — refuted on primary data

Checked against the actual benchmark data (`github.com/YJiangcm/FollowBench`, branch `master`), not the prose
(`steer-followbench-levels.md`). **FollowBench's levels add *more constraints*; they never intensify *one*.**

- **Style** L1 "a wise old sage" → L2 "a keen detective … 1940s noir" → L3 "+ eloquence of Shakespeare" → L4
  "+ Lewis Carroll" → L5 "+ Jane Austen". Never "slightly → very Shakespearean". L1→L2 even *swaps* the persona.
- The predicted "at least N words, N increasing" escape hatch **does not exist**: numeric constraints appear in
  **6/150** Content records, **0/180 Style, 0/132 Situation** — and are **frozen** across levels
  (`L3[three] L4[three] L5[three]`).
- Instructions **grow 5–7×** in length — the cumulative-addition signature. An intensity ladder holds length
  fixed and swaps a modifier.
- Honest concession: **Situation** *is* a monotone numeric ladder (3→4→5→6→7→8 birds) — but it scales *task
  input size*, not trait magnitude.

So `game-followbench.md`'s CSL≈3.3 is the **constraint-count** axis. Ours is the **intensity** axis. They are
orthogonal and both real. **No IF benchmark measures graded response to graded instruction** (9 checked).
**ComplexBench does *not* measure entanglement** — its dependency is an annotator-declared *scoring gate*, never
an A-alone vs A+B counterfactual. Don't overclaim it.

**A genuine gift:** MOSAIC and CFBench both compute continuous adherence and then **binarise it on purpose**
(MOSAIC scores 0–10 then thresholds at 0.5; CFBench computes `0.5+0.5×avg` then re-thresholds at 0.8). **Two
teams independently generated graded signal and threw it away.** Our claim is not "we invented graded
evaluation" — it is "**we decline to discard it, and we add an x-axis.**"

## 6. The brittleness knee is quantified — reuse the numbers, don't re-derive them

- `steer-steering-brittleness.md`: monotone only at **|λ| ≤ 1.5**; **"|λ| > 2 substantially degrade both
  intrinsic and extrinsic text quality."** Failure is two-stage: **attribute-congruent hallucination first,
  repetition second.** The knee is **attribute-specific** (toxicity breaks early, sentiment late).
- `steer-cfg-guidance-scale.md`: system-prompt following **peaks at γ=3**, degrades at 4–6.
- Persona Vectors: steering is `h ← h − α·v`; "**large steering coefficients tend to degrade accuracy,
  indicating a loss in general capability**"; "inference-time steering tends to **break the model**". Their
  discipline: **pick the largest coefficient where coherence (0–100, GPT-4.1-mini) stays > 80.** Copy the gate;
  don't copy the reporting — they never publish the MMLU curve numerically, only as an unlabeled gray line.
- `steer-pplm.md` — **the warning about our own instrument**: control dropped human fluency **3.54→2.79** while
  **perplexity moved the wrong way (42.1→41.8)**. **Perplexity is blind to degradation humans see.** A
  judge-free coherence proxy will not catch our BRITTLE mode.

## 7. What §3 should become

1. **Delete** "unmeasured anywhere". Replace with: *"steerability is operationalized as a scalar gap (Vafa et
   al.) and benchmarked for prompt-intensity control (PsySET); it has not been measured as a **response
   function over an intensity ladder on character traits**, and prompt-space trait **co-expression** is an
   explicit open question in Anthropic's persona-vectors paper."*
2. **Elasticity → response function.** Fit a curve with a **quadratic/cubic term** and report the **peak** and
   the **knee**, not a slope. Kirk et al. found the peak at *moderate* dose; a slope cannot represent that.
   Prefer **deviation-from-target** (`steer-style-intensity.md`) over a ratio — adverbs have no units, so the
   denominator of "elasticity" does not exist. **Stop calling it elasticity.**
3. **Add the null arm.** Every ladder rung gets a matched semantically-null perturbation. Report
   **intended/spurious**, i.e. **DIR/INV**. Without it BRITTLE is unfalsifiable and the whole L2.2 number is
   uninterpretable. *This is the contribution.*
4. **Entanglement metric = off-diagonal − human-baseline correlation.** Not the raw off-diagonal.
5. **Build in the negative control.** Hallucination-like traits (cos 0.19–0.25 to everything) *should* show ~0
   crosstalk. If our method reports crosstalk between near-orthogonal traits, our method is broken — and we
   cannot tell that apart from judge noise without this arm.
6. **Do not assume the diagonal dominates.** Two papers show off-diagonal-dominant cells. Measure the full
   matrix, and **do not mirror it** — the *Personality Illusion* matrix is asymmetric.
7. **Randomize trait position in the sheet.** MOSAIC finds primacy/recency bias; position contaminates measured
   elasticity. This also merges L2.3 into L2.2 as a control rather than a separate study.
8. **Ablate the system/user slot.** OpenAI's Instruction Hierarchy (`steer-instruction-hierarchy.md`) *trains*
   system-prompt dominance in, so elasticity on frontier models partly measures post-training, not the trait.
9. **Expect prompt steerability to be weak and fragile.** Kirk: prompt slope ≈ ⅓ of steering, and −3.9 to −4.5
   under user pressure. §3 says "if the model isn't steerable, the variant lifecycle is a ritual." **The
   published prior is that prompt-space steerability is genuinely weak.** That is a real risk to the platform's
   premise, and it is the strongest reason to run this — but we should pre-register that we expect a small
   slope, or we will "discover" it and call it a finding.

## 8. Honest status of the surviving novelty

**Narrow but real** — three things, none of which is "we invented dose-response":

1. **The DIR/INV ratio** — nobody divides intended sensitivity by spurious sensitivity. One operation, two
   mature literatures, and it converts BRITTLE from a base rate into a measurement.
2. **Prompt-space trait co-expression cells** — Anthropic's own open question; their matrix is finetuning-space.
3. **Intensity × conversation depth** — every result above is single-turn. Kirk's effect **decays 62% by session
   20**. A curve fitted at turn 1 does not describe turn 20, and companions live at turn 50+. This is also where
   `game-followbench.md` (constraint count) and `game-multi-if.md` (horizon) compose with us.

**Two risks to name now.**

- **Power.** PersonaLLM built a **2⁵ factorial over 320 personas in 2023** containing exactly this data and
  never published the off-diagonal — plausibly because 10 samples/cell is too noisy. Our n=95 characters is in
  the same danger zone; [15](15-l1-convergent-reading.md) was already underpowered at n=45 for ρ≈0.3. **Power-
  analyze before generating, not after.**
- **Diagonal and off-diagonal are probably coupled.** `steer-personality-probe-tradeoffs.md`: openness has both
  the worst dose-response (ρ=0.47) *and* the worst entanglement; its steering **plateaued** until the
  conscientiousness direction was subtracted ("**trait purification**"). **A DEAD diagonal may be a *symptom* of
  a hot off-diagonal, not an independent failure mode.** The §3 table presents the three modes as peers. They
  are not: BRITTLE is the denominator, and DEAD may be an effect of ENTANGLED.

**Cheapest high-value next action:** run `github.com/MLD3/steerability` against our traits. Either it works and
saves weeks, or it breaks on non-rule-based traits — and *that failure is the motivating result*.

---

## Sources written (35, `../sources/steer-*.md`)

**Start here:** `steer-persona-vectors-crosstalk.md` (the buried off-diagonal + my Fig-20 reconstruction) ·
`steer-dose-response-companion-rct.md` (the novelty-killer) · `steer-spurious-vs-intended.md` (DIR/INV — the
surviving contribution) · `steer-psyset.md` (closest prior art) · `steer-followbench-levels.md` (adjudicates the
FollowBench question).

**Crosstalk:** `steer-personality-illusion-crosstalk.md` · `steer-structural-amplification.md` ·
`steer-big5chat-trait-correlation.md` · `steer-personality-shaping-independence.md` · `steer-personality-edit.md` ·
`steer-trait-intercorrelation-benchmarks.md` · `steer-personality-probe-tradeoffs.md`

**Dose/control:** `steer-personality-shaping-levels.md` · `steer-dexperts.md` · `steer-pplm.md` ·
`steer-cfg-guidance-scale.md` · `steer-caa-activation-steering.md` · `steer-style-intensity.md` ·
`steer-steering-brittleness.md` · `steer-tailor.md` · `steer-multiaspect-distributional-lens.md`

**Brittleness:** `steer-formatspread.md` · `steer-worst-prompt.md` · `steer-multiprompt-eval.md` ·
`steer-mcq-order-bias.md` · `steer-linguistic-properties.md` · `steer-prosa-sensitivity.md` ·
`steer-promptbench.md` · `steer-format-impact-microsoft.md`

**Instruction following:** `steer-steerability-operationalized.md` · `steer-instruction-hierarchy.md` ·
`steer-complexbench.md` · `steer-cfbench.md` · `steer-mosaic-partial-compliance.md` · `steer-if-benchmarks-sweep.md`

**Flagged unverified:** Chang et al.'s steerability definition (OpenReview browser-walled — snippet only, do not
quote); PersonalityEdit Table 2 (needs PDF re-verification); Kirk et al.'s per-unit slopes are body-sourced —
the *abstract* verifies "non-linear dose-response curves", N=3,534, and the steering-vector method, but not the
2.39/0.78/1.83 comparison.
