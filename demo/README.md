# demo/ — committed evaluation fixtures

The bundled test data that makes the platform reproducible with zero dependencies and no API key.
`ceval seed` loads it into the local DB.

- `gen/` — offline **dialogue transcripts**: real Claude output (Sonnet 4.5 / Haiku 4.5) playing
  the demo characters turn by turn, plus `tasks.json` (characters + replayed user turns) and
  `variants.json` (the variant manifest).
- `judge/` — recorded **judge scores** for those transcripts: `fidelity_*` (voice fidelity + wimp),
  `craft_*` (session-level narrative craft), `input_*` (sampled replies for evidence).

Online session data is **simulated at run time** (`ceval eval run --online`), not stored here.
