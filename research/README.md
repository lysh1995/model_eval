# Research knowledge base

271 raw sources + 15 synthesis notes, built by 11 parallel research streams (2026-07-16). **All streams complete.**

**Structure:**
- `sources/` — raw captures. Each has YAML frontmatter (title, url, authors, year, type,
  accessed, topic) and substantive content: abstracts verbatim, dimension definitions verbatim,
  methodology, tables. Deliberately not thin summaries — the goal is never needing to refetch.
- `notes/` — per-stream synthesis, plus our own first-party measurements.

**Source prefixes:** `rp-bench-` roleplay benchmarks · `judge-` LLM-judge reliability ·
`creativity-` creativity measurement · `psycho-` psychometrics · `product-` companion products ·
`scale-` production monitoring · `safety-` roleplay safety & law · `multiturn-` long-horizon eval ·
`narrative-` narrative craft · `game-` world simulation · `pipeline-` eval lifecycle

## Notes index

### First-party — measured by us, reproducible
| | |
|---|---|
| [00 — Dataset ground truth](notes/00-dataset-ground-truth.md) | What the corpus actually contains. **The brief's replay premise was wrong** and is corrected here |
| [09 — Judge-free probes](notes/09-offline-probes.md) | Which failure modes are present and separable. **Includes the metric we broke, twice** |
| [10 — Noise floor](notes/10-noise-floor.md) | Variance decomposition from the 3 runs/cell. **What the platform can and cannot detect** |
| [15 — L1 convergent reading](notes/15-l1-convergent-reading.md) | Do models agree on how to read a character? Characters vary 4–5x in readability |
| [21 — Card-awareness audit](notes/21-card-awareness-audit.md) | **Did the user simulator see the character card?** Suggestive yes — which would mean our drift numbers are a lower bound |

### Design
| | |
|---|---|
| [11 — Evaluation method design](notes/11-evaluation-method-design.md) | **The core design.** Which fields, how to grade, how to normalize |

### Literature streams
| | |
|---|---|
| [01 — Roleplay benchmarks](notes/01-roleplay-benchmarks.md) | The recurring dimension set; why famous-character benchmarks don't transfer |
| [02 — LLM-judge reliability](notes/02-llm-judge-reliability.md) | Biases, magnitudes, mitigations; the κ≈0.53 ceiling |
| [03 — Creativity measurement](notes/03-creativity-measurement.md) | Why absolute creativity scoring is dead; pairwise + anchors |
| [04 — Psychometrics](notes/04-psychometrics-measurement.md) | Construct validity, G-theory, measurement invariance, slicing |
| [05 — Companion products](notes/05-companion-products-practice.md) | Real failure modes; behavioral signals and which are traps |
| [06 — Production scale](notes/06-production-scale-monitoring.md) | Tiering, sampling, drift, the cost model at 50M/day |
| [07 — Roleplay safety](notes/07-roleplay-safety.md) | Two-axis safety; the fiction-strip test; the legal floor |
| [08 — Multi-turn eval](notes/08-multiturn-conversation-eval.md) | Unit of analysis; min-over-turns; off-policy replay validity |
| [12 — Narrative craft](notes/12-narrative-craft-dimensions.md) | Scene-ignorance beats roboticness as the perceived failure; the narrative paradox |
| [13 — Game simulation](notes/13-game-simulation-dimensions.md) | **The agreement gradient (bound vs unbound); RPGBench; CICERO** |
| [14 — Eval lifecycle](notes/14-eval-lifecycle-system.md) | Shadow is not a quality gate; no standard carries evaluator identity |

## A note on rigor

Streams were instructed to flag fabricated or unverifiable numbers rather than pass them through.
Unrecoverable figures are marked as such rather than estimated. The design rests on numbers like
κ≈0.53 and ρ=−0.082 — agents that check beat agents that agree.

**This was not paranoia. It caught three real things:**

1. **A research tool fabricated an entire results section** — WebFetch invented a table including a
   plausible Fleiss' κ=0.73. Caught by cross-checking; stream 13 then re-extracted every
   load-bearing number from primary PDFs via `pypdf`.
2. **Arithmetic checking then found two genuine errors in DECODE's *published* table.**
3. Two other streams independently caught invented figures from web summarizers and corrected three
   citation errors against source PDFs.

**Assume any number not traced to a PDF is unverified — including in our own documents.** During
this session an inflated source count (312 vs the actual 271) was written into *this file*, in the
section about rigor, and caught on review. The failure mode is not exotic; it is the default.

### The tools themselves return wrong answers silently

Two independent instances, both caught, both of a kind that produces **confident false findings** rather
than errors:

- **`grep` silently returned 0 on files containing NUL bytes.** macOS grep treats such files as binary
  and **exits 0 with no output and no error**. `grep -oi "intent" cicero.norm` → **0**; Python → **197**.
  This published two **false zeros** before being caught — *"IFEval contains no tone/style"* (true:
  tone=11, style=28), **an absence that inverted the real finding**, and *"RLUF role-play = 0"* (true: 2),
  which had **buried RLUF's most important result**. All counts were re-run in Python.
- **A naive `grep -i persona` returned 13 hits in Gemini 1.5 — all 13 were "personal data."** Word-boundary
  regex gives the true answer: **zero**. The inflated figure was nearly reported.

**A tool that returns a plausible wrong number is more dangerous than one that crashes.** Neither of these
looked like a failure.

### A fabrication guard worth keeping

`kappa` / `Fleiss` / `Krippendorff` / `inter-rater` / `Cohen's` appear **0 times across all 14 Google and
Meta primary documents.** Neither org reports **any** inter-rater reliability statistic anywhere.
**Therefore: any κ attributed to those papers is fabricated.** This is a checkable invariant, and it exists
because a research tool in this project *did* invent a Fleiss' κ=0.73 earlier the same day.

Confidence tiers are recorded in [../docs/RESEARCH-PLAN.md](../docs/RESEARCH-PLAN.md#confidence-assessment).
Notably **low-confidence**: bias magnitudes on *our* judge (unmeasured — blocked on API key), the
sampling floor's dependence on a guessed traffic shape, and the MIT dependency finding
(correlational, general assistant not a companion, 61% attrition).
