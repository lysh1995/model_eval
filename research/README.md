# Research knowledge base

210 raw sources + synthesis notes, built by 11 parallel research streams (2026-07-16).

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
| [12 — Narrative craft](notes/12-narrative-craft-dimensions.md) | 🔄 storytelling dimensions with objective correlates |
| [13 — Game simulation](notes/13-game-simulation-dimensions.md) | 🔄 world state, consequence, agency |
| [14 — Eval lifecycle](notes/14-eval-lifecycle-system.md) | 🔄 collection schema, dry-run → online → loop |

## A note on rigor

Streams were instructed to flag fabricated or unverifiable numbers rather than pass them through.
Two independently caught invented figures from web summarizers and corrected three citation errors
against source PDFs; unrecoverable figures are marked as such rather than estimated. The design
rests on numbers like κ≈0.53 and ρ=−0.082 — eight agents that check beat eight that agree.

Confidence tiers are recorded in [../docs/RESEARCH-PLAN.md](../docs/RESEARCH-PLAN.md#confidence-assessment).
Notably **low-confidence**: bias magnitudes on *our* judge (unmeasured — blocked on API key), the
sampling floor's dependence on a guessed traffic shape, and the MIT dependency finding
(correlational, general assistant not a companion, 61% attrition).
