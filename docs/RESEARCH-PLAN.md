# Research plan — status, gaps, and what still needs investigation

Last updated 2026-07-18.

**Research is complete, and the platform it informed is built and running as a local end-to-end
service.** This ledger now records a finished body of work and the gaps that remain open for a
human or the product team, not an in-flight effort.

**Method:** 16 parallel research streams (11 primary + 5 adversarial cross-checks), each instructed
to save raw sources verbatim (not thin summaries) so we never need to refetch, and to report
numbers with their provenance. Output: **475 raw sources**, 26 synthesis notes. Streams were told
to flag fabricated or unverifiable numbers rather than pass them through — two streams caught
invented figures from web summarizers and corrected three citation errors against source PDFs.
Given the design rests on numbers like κ≈0.53 and ρ=−0.082, that discipline is the point.

## Stream status — all 16 complete

Research is done. All 16 streams are closed, and the design they informed is built and running.
26 synthesis notes (00–25) back the 475 raw sources.

### Primary research streams (11)

| # | Stream | Sources | Note | Status |
|---|---|---|---|---|
| 1 | Roleplay / persona benchmarks | 22 | [01](../research/notes/01-roleplay-benchmarks.md) | ✅ |
| 2 | LLM-judge reliability & bias | 19 | [02](../research/notes/02-llm-judge-reliability.md) | ✅ |
| 3 | Creativity & storytelling measurement | 15 | [03](../research/notes/03-creativity-measurement.md) | ✅ |
| 4 | Psychometrics & measurement theory | 13 | [04](../research/notes/04-psychometrics-measurement.md) | ✅ |
| 5 | Companion products in practice | 10 | [05](../research/notes/05-companion-products-practice.md) | ✅ |
| 6 | Production scale & monitoring | 35 | [06](../research/notes/06-production-scale-monitoring.md) | ✅ |
| 7 | Roleplay safety | 54 | [07](../research/notes/07-roleplay-safety.md) | ✅ |
| 8 | Multi-turn / long-horizon eval | 28 | [08](../research/notes/08-multiturn-conversation-eval.md) | ✅ |
| 9 | Narrative craft dimensions | 18 | [12](../research/notes/12-narrative-craft-dimensions.md) | ✅ |
| 10 | Game / world simulation dimensions | 42 | [13](../research/notes/13-game-simulation-dimensions.md) | ✅ |
| 11 | Eval lifecycle & collection schema | 15 | [14](../research/notes/14-eval-lifecycle-system.md) | ✅ |

### Adversarial cross-checks (5)

Commissioned to *attack* the design, and they landed: one **retracted our headline claim**
(steerability is already measured — four times over), one showed **our own metrics score the
field's worst failure as a success** (Luda — a leaked real address passes every metric we have),
and one found the framework **sorts by reliability and never checks validity** (Funder's RAM,
published 1995, is our cascade).

| # | Stream | Sources | Note | Status |
|---|---|---|---|---|
| 12 | Psychology cross-check | 41 | [16](../research/notes/16-psychology-crosscheck.md) | ✅ — sorts by reliability, never checks validity |
| 13 | Big-tech lab practice | 40 | [17](../research/notes/17-bigtech-practice-crosscheck.md) | ✅ — retracts the headline; IFEval defines persona out of existence |
| 14 | Non-Anglophone / regional | 30 | [18](../research/notes/18-regional-crosscheck.md) | ✅ — Luda: field's worst failure scores as success |
| 15 | Steerability prior art | 35 | [19](../research/notes/19-steerability-crosscheck.md) | ✅ — L2.2 "unmeasured" refuted; measured four times |
| 16 | Recent developments | 58 | [20](../research/notes/20-recent-developments.md) | ✅ — mid-2025→2026, primary-source-verified |

### First-party measurements (measured by us, reproducible — not literature)

| | | |
|---|---|---|
| Dataset ground truth | [00](../research/notes/00-dataset-ground-truth.md) | ✅ measured |
| Judge-free probes | [09](../research/notes/09-offline-probes.md) | ✅ measured |
| Noise floor / variance decomposition | [10](../research/notes/10-noise-floor.md) | ✅ measured |
| L1 convergent reading | [15](../research/notes/15-l1-convergent-reading.md) | ✅ measured — **suggestive, not established** |
| Card-awareness audit | [21](../research/notes/21-card-awareness-audit.md) | ✅ measured — treat this corpus's drift numbers as a lower bound |
| SRM chemistry (model×character) | [22](../research/notes/22-srm-chemistry.md) | ✅ measured — 6.7% (en) / 14.6% (zh) where it should be ~0 |
| Homogenization vs discriminability | [23](../research/notes/23-homogenization-vs-discriminability.md) | ✅ measured — produced by the platform itself |
| Safety-lane build | [24](../research/notes/24-safety-lane-build.md) | ✅ built — 3 of 4 detectors broken on first contact |
| Scale, measured (50M/day) | [25](../research/notes/25-scale-measured.md) | ✅ measured — from measured units, not borrowed |

### Design (built)

| | | |
|---|---|---|
| Evaluation method design | [11](../research/notes/11-evaluation-method-design.md) | ✅ superseded by [EVAL-DESIGN.md](EVAL-DESIGN.md); the design is built |
| **Ability model** (L1→L2→L3) | [ABILITY-MODEL.md](ABILITY-MODEL.md) | ✅ built — feeds [EVAL-DESIGN.md](EVAL-DESIGN.md) |

## Why streams 9–11 were added mid-flight

The original eight produced a taxonomy heavy on **persona fidelity** ("does it stay in
character") and thin on **narrative craft** ("is it a good scene partner"). Those are different
skills: a model can be perfectly in-character and still be a terrible partner — passive,
railroading, no stakes, no escalation. A *game* simulation adds a third axis again: world state,
consequence persistence, player agency. R10 asks for this explicitly and the first eight streams
don't answer it.

---

## Gaps — what we do NOT know

### Blocked on the API key (highest priority — nothing in Lane 3 is validated)

Every judge-lane number in the design is **borrowed from the literature, not measured on our
data**. Until these run, Lane 3 is a plan, not a result:

1. **Our judge's κ** against a human calibration set, on *our* rubric, *our* characters.
   Literature ceiling is κ≈0.53 — we don't know ours.
2. **Our position-bias exposure.** Literature says it's ~solved on frontier judges (≤0.04 in 2026
   vs 35% in 2023) and that swap-and-average *worsens* verbosity bias. If true we save 2× on
   every judgment. **Cheap experiment, large payoff — do it first.**
3. **Our sentiment-bias exposure.** RR 0.60–0.80 generally, 0.24–0.66 under sadness/anger/fear,
   **no published mitigation**. Companion traffic is *made of* this. Biggest unquantified risk in
   the design.
4. **Our abstention rate.** Literature: ~19–20%. Drives both cost and the human-queue staffing.
5. **σ_within for judge dimensions.** Will be *worse* than the 0.0847 we measured for repetition —
   judge stochasticity stacks on generation stochasticity. Every dimension needs its own before
   it can gate.

### Not blocked — should be run now

6. ~~**User-turn card-awareness audit.**~~ **RUN** — [21](../research/notes/21-card-awareness-audit.md).
   Verdict: **suggestive of card access, not conclusive.** Own-card term leak beats a
   topic-matched control by **1.59× (en) / 1.48× (zh), p<0.0001**, surviving a precedence test and
   exclusion of the scripted first turn — but the topic control is weak (Jaccard 0.058), so topic
   cannot be ruled out. **Decisive follow-up not yet run: restrict to proper nouns** — topic cannot
   explain the user knowing the character's sister's name before the AI says it. Until then, treat
   this corpus's drift numbers as a **lower bound**, and make our own simulator **card-blind by
   construction**.
7. **Self-recovery check.** Same character, replayed history vs self-generated history. Closes
   the off-policy question empirically rather than by citation. Needs generation, not judging.
8. **Classifier latency benchmark.** Cost is a non-issue (OpenAI Moderation free; Llama Guard 4
   ≈ $10k/100M turns) but **latency is the binding constraint and nobody publishes it.** Budget a
   week. Note Perspective API is **dead (ends 2026-12-31)** — off the table.
9. **Length-controlled homogenization, zh residual.** After length control the en confound is
   gone (ρ=−0.018) but **zh retains ρ=+0.264** — real effect or residual artifact? Not separable
   at n=11 models. Needs either more models or a within-model design.
10. **Repetition metric cross-language comparability.** We use word-5-grams (en) and char-8-grams
    (zh). Rankings are valid within a language; the two are **not the same instrument**. Either
    justify the mapping or stop comparing the numbers.

### Unknowable from here — needs product input

11. **Character traffic distribution in production.** The 500/cell/day sampling floor assumes a
    head/tail shape we're guessing at. Real distribution changes the sampling math.
12. **Our real abstention/escalation volume** → human queue staffing and cost.
13. **Does the product randomize the default model?** Determines whether online comparisons can
    support causal claims at all. Log `assignment_arm` regardless — it costs nothing and is
    **unrecoverable after the fact**.
14. **Session length distribution.** The multi-turn safety danger zone is ~5–10 turns; whether
    that's our median or our tail changes the risk profile entirely.

### Needs a human, not a subagent

15. **Legal review** of CA SB 243 / NY GBL Art. 47 / EU AI Act Art. 50 (**in force 2026-08-02**).
    Our findings are desk research against primary sources, not advice. This is the only
    workstream with an external calendar.
16. **BARS retranslation** for the rubric: SMEs write concrete behavioral incidents per dimension;
    a second blind group re-sorts them; incidents failing to sort back (<70%) are discarded. **If
    a dimension's incidents don't sort back, it isn't a distinct construct** — merge or cut.
    Expect "creativity"/"engagement"/"personality" to substantially collapse. Cheapest kill signal
    available, and **no downstream statistic repairs a failure here.**
17. **Consequential validity owner per dimension** — name the model that wins by gaming it.
    For a companion product, **"engagement" gamed = emotional dependency.**

---

## Deliberate non-investigations

- **The dataset's published scores** (`evaluations.jsonl`) — quarantined per the brief. Legitimate
  later as an *external convergent-validity reference* once our instrument is frozen; never as a
  label source or an input to rubric design.
- **Famous-character benchmarks as a model-selection source.** Anonymizing character names degrades
  every model, so those leaderboards partly measure canon memorization. **Our characters are
  user-authored — the anonymized setting *is* our production setting.**
- **Training/RLHF.** Out of scope (PROJECT.md §2). Findings feed humans, not a reward model.

---

## Confidence assessment

**High** (measured by us, reproducible): the noise floor, the language non-invariance, the length
confound, repetition as a working metric, the dataset's structure.

**Medium** (literature, multi-source convergent): judge κ ceiling, pairwise > absolute, min > mean
aggregation, PoLL dominance, the tiering cost model, human agreement ceilings.

**Low** (single-source, or measured in a configuration unlike ours): specific bias magnitudes on
*our* judge; the 500/cell/day floor's dependence on a guessed traffic shape; behavioral-proxy
validity generally. The MIT dependency finding is **correlational**, ran on a general assistant
rather than a companion, with 61% attrition; top-decile "2x/3x" figures are press-sourced and
unverified — do not put these in a deck without re-checking.

**The standing risk this whole plan exists to manage:** we demonstrated locally, twice in one
afternoon, that a literature-recommended metric implemented the obvious way produces a confident,
plausible, *wrong* ranking — first via a length confound (ρ=+0.73), then via a survivorship
confound introduced by the fix. Neither was visible in the output. **Plausibility is not
validation.**
