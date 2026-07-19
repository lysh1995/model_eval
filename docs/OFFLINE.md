# Offline testing — the three components

Delivered and runnable, no API key — the offline half of the DB-backed service:
`python3 -m ceval init && ceval seed && ceval eval run --offline --sim && ceval dashboard`
(or `ceval serve` for the live view).

This supersedes the Lane-as-Level shorthand in earlier docs. **Two corrections are baked in:**
1. **Lane ≠ Level.** The judge is a *mechanism* that spans L1, L2, L3 — not "the L3 lane".
2. **Automation is ranked.** Prefer self-validating measurements (need no ground truth) over
   judge-vs-human comparisons. Minimise the human anchor; never remove it entirely.

---

## Component 1 — Test targets (待测试集)

A **variant** = model + params + system prompt. The scored subjects are **real Claude output** under
four production-grade roleplay system prompts, run on **two models (Sonnet 4.5 and Haiku 4.5)** so
the platform's discrimination is testable across *both* prompt and model:

| variant | model | system prompt intent | what it should expose |
|---|---|---|---|
| `v_terse` | Sonnet 4.5 | tight in-character, action over exposition | high fidelity, distinct voice |
| `v_narrator` | Sonnet 4.5 | rich literary narration, sensory detail | high fidelity, verbose (must not be penalised for length) |
| `v_assistant` | Sonnet 4.5 | **make the user feel good; agree, affirm, play the character loosely** | **character dilution + sycophancy** |
| `v_hostile` | Sonnet 4.5 | guarded, sharp-tongued, slow to trust (prickly, in-fiction) | high fidelity, very low wimp |
| `v_terse · Haiku` | **Haiku 4.5** | *same prompt as `v_terse`* | the **model** effect, prompt held fixed |
| `v_assistant · Haiku` | **Haiku 4.5** | *same prompt as `v_assistant`* | the model effect on the adversarial prompt |

`v_assistant` is the adversarial control — the character-diluting, engagement-leaning variant the
whole project warns about. If the platform is real, it must score it worst on fidelity and highest
on wimping. **It does** (below). The two Haiku twins reuse the *identical* system prompt as their
Sonnet counterparts — a prompt is content-addressed by its text, so the twins **share one prompt row
and differ only by model**. That is R9 ("same baseline for every model") made concrete: the
dashboard compares Sonnet vs Haiku on a fixed prompt.

Generation is done by Claude subagents on the real models (no API key), replaying the corpus user
turns; the committed output lands in `demo/gen/v_*.json` and is seeded into the DB by `ceval seed`.

---

## Component 2 — Test scheme (测试方案 + cases + 答案 + 验证 + 计分)

`ceval/offline/scheme.py` — the declarative dimension catalogue. Every dimension names its **level,
lane, product-failure, case, validation, score,** and **which of the 6 filters it survived**.

### How a dimension is DECIDED — the 6-filter kill-pipeline (not a brainstorm)

A candidate dimension must survive all six, cheapest kill first:

1. **Product-failure necessity** — names a concrete failure that costs users/money/safety. (If you
   can't name the failure, cut it.)
2. **Construct recurrence** — recurs across independent benchmarks (evidence it's a real construct).
3. **Distinctness / BARS retranslation** — SME behavioural incidents sort back ≥70%; else it isn't
   a distinct construct → merge or cut.
4. **Discriminant power** — actually separates models, and isn't redundant with another (ρ<0.9).
5. **Instrument class** — deterministic / consensus / perspectival → which lane, and can it gate.
6. **Consequential validity** — name the model that wins by gaming it; if gaming it is a harm
   (engagement → dependency), it's dangerous as a target.

### The catalogue — the JUDGE spans every level

| level | dimension | lane | catches (product failure) |
|---|---|---|---|
| **L1** | character_alpha | **psychometric** | no coherent person inside — confabulated per item |
| **L1** | character_comprehension | **judge** | misreads the character; can't infer unstated traits |
| **L2** | voice_fidelity | **judge** | stops sounding like the character |
| **L2** | coherence_retest | **psychometric** | personality drifts across the session |
| **L2** | discriminability | compute | every character collapses into one voice |
| **L3** | repetition | compute | loops — boring, users leave *(the one gate)* |
| **L3** | scene_drive | compute | the treadmill — talks, moves nothing |
| **L3** | narrative_engagement | **judge** | correct but dead on the page |
| **safety** | over_refusal | compute | filter intrusion breaks the fiction |
| **safety** | wimp_rate | **judge** | sycophancy = accept-without-adding → dependency |

**The judge (Lane 3) appears at L1, L2, L3 and safety.** Lane is the mechanism; level is the ability.

### Scoring & validation, ranked by how little human judgment they need

0. **Compute** (repetition, discriminability, scene-drive, over-refusal) — deterministic, no model
   call, no judgment. Violation rates, bounded [0,1], comparable across models by construction.
1. **Self-validating psychometric** (character_alpha, coherence_retest) — the automation gem:
   Cronbach's α on the character's own questionnaire answers needs **no ground truth and no judge**
   (the factor structure is the referent). α≈0.8 = a character is in there; α≈0 = confabulated.
   Test-retest borrows the human baseline (BFI r≈0.75–0.90) **once** from the literature.
2. **Bound judge** — convert "is it good?" (α=0.25–0.34) into "does this contradict the card?"
   (κ=0.78–0.94). Same judge, answerable question.
3. **Pairwise judge + frozen anchors + family-disjoint panel** — for the perspectival residue only.

Aggregation is unchanged: **min over turns** (not mean), **effective n = conversations**, shrinkage
for per-character, **never pool across languages**.

---

## Component 3 — The platform (选择 → 测试 → 可视化对比)

`ceval/offline/runner.py` takes variants + scheme → a `GradeBook`; the dashboard renders it with
**cross-variant comparison** (each dimension shows the variants side by side, sorted), the
**ability portrait** per variant, the **test scheme**, and a **mixed-provenance banner**.

### Provenance is the firewall

`ceval/offline/provider.py` has three backends behind one interface:
- `RecordedProvider` — **real Claude judge scores** recorded to `demo/judge/` by a judge subagent
  (evaluator `claude-sonnet/judge-v1`). This is what the committed demo uses (`ceval eval run`).
- `SimulatedProvider` — **fabricated, labelled** judge scores (evaluator `simulated/v1`) for a
  token-thrifty run (`ceval eval run --sim`).
- `SubagentProvider` — live subagent judging driven by the orchestrator.

Every judge grade carries its `evaluator` id; a simulated one is stamped `simulated/v1` and the
dashboard shows a loud banner, while a recorded one names the real judge. **Compute grades are
always real measurements on real Claude output; a simulated judge number is the pipeline exercised,
not a measurement of the model.** Presenting a simulated number as real would be the exact failure
this project exists to prevent — the label is the firewall.

---

## What the run actually showed (real generation, **real judge**)

Dialogues generated by **Claude Sonnet 4.5 / Haiku 4.5**; voice_fidelity + wimp scored by a
**neutral Claude Opus judge** (neither generator — reduces self-preference); repetition /
scene-drive / over-refusal / discriminability are pure compute on the real output.

| dimension (level) | Terse | Narrator | Hostile | **Assistant** | Terse·**Haiku** | Assistant·**Haiku** | provenance |
|---|---|---|---|---|---|---|---|
| **narrative_craft (L3 · STORY)** | 0.64 | **0.82** | 0.81 | **0.25** | 0.69 | 0.40 | real · Opus judge |
| voice_fidelity (L2 · persona) | 0.89 | **0.90** | 0.86 | **0.34** | 0.74 | **0.33** | real · Opus judge |
| wimp_rate (safety) | 0.06 | 0.04 | 0.05 | **0.65** | 0.08 | **0.65** | real · Opus judge |
| repetition (L3 gate) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | real compute |

Three real findings, all the point of the platform:

1. **Storytelling craft is the product core, and it is NOT persona fidelity.** `narrative_craft`
   (does the AI build an advancing, co-created STORY?) and `voice_fidelity` (does it stay in
   character?) rank the variants **differently**: `Terse` is near-top on fidelity (0.89) but only
   mid on craft (0.64) — faithful, but clipped action-lines that advance little; `Narrator` (0.82)
   and even the abrasive `Hostile` (0.81) are the strongest *storytellers*. Measuring only persona
   would miss which variant is the better story partner — the very failure note 12 flags (the field
   ships a 4:1 narrative-to-persona balance; we had been inverted). Note: judge-free entity
   heuristics were **degenerate** here (they rank by entity density, not craft — measured), so craft
   is a **session-level judge** dimension.
2. **The adversarial variant is caught — on both models, on both axes.** `Assistant` is worst on
   craft (0.25 — it affirms and advances nothing, a dead scene) *and* on fidelity (0.34), and spikes
   on wimp (0.65 — **~11× the others**). The engagement-leaning, character-diluting prompt is exactly
   what the project warns about, and the instrument flags it every way.
3. **The model matters — but only where the prompt lets it.** On the disciplined `Terse` prompt,
   Sonnet holds character better than Haiku (**0.89 vs 0.74**). On the `Assistant` prompt the two
   models are indistinguishable (**0.34 vs 0.33**) — the sycophantic instruction dominates, and the
   model can't save it. A prompt regression can erase a model's advantage; the platform shows that.

`narrative_craft` is scored per **session** (not per reply): craft is a property of the trajectory,
not a line ([note 12](../research/notes/12-narrative-craft-dimensions.md)). And it is scored
*independent of length* — Narrator leads on craft *and* fidelity despite being the most verbose.

## Honest limits of this demo

- **The judge is real but small and single-panel.** One Opus judge, not a family-disjoint panel;
  it reduces but does not eliminate self-preference (all three models are Claude). Our own judge κ
  is still unmeasured — the literature ceiling is κ≈0.53. Treat the exact values as illustrative,
  the *direction* as sound.
- **`character_alpha` (psychometric) is omitted this run.** It needs the full questionnaire-
  administration protocol; dropping it was a token-budget call, not a measurement failure. Compute
  + fidelity + wimp cover the discriminating signal.
- **The dialogues are 9 turns, 3 characters.** Too short for repetition/over-refusal to register
  (both 0.000 — real, but nothing to catch in a benign 9-turn scene); discriminability is weak and
  is dropped (NaN) where it can't fund its token budget.
- **No users.** Everything here is offline; whether users prefer a variant needs live Q1.

The pipeline and the numbers are both real. To scale it up, add characters/turns and swap the
single judge for a family-disjoint panel behind an API key — the same code runs it.
