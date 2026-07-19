# The evaluation service — end-to-end local design

A DB-backed CLI service. Inject models, prompts, and data (each with an id); trigger offline +
online eval; render the dashboard. Everything persists.

```
INPUT                     DOMAIN (stored)              OUTPUT
models, prompts,   ──▶   dimensions + scoring   ──▶   dashboard
dialogues, sessions       grades + evidence            (static + interactive)
     (CLI)                     (DB)                       (original design)
```

## Storage — one schema, two drivers

The DB is the service's backbone. **MySQL is the designed production database; SQLite is the
zero-dependency runnable backend.** Same table definitions emit driver-appropriate DDL
(`ceval/store/db.py::ddl`), so nothing diverges.

| | |
|---|---|
| **MySQL** | the design. Full DDL in [`ceval/store/schema.sql`](../ceval/store/schema.sql). Driver activates when `pymysql` is installed. `--db mysql://user:pass@host/db` |
| **SQLite** | the default runnable backend — stdlib, no dependencies. `--db sqlite:///out/ceval.db` |

### Tables (each row has an id)

| table | what it holds |
|---|---|
| `models` | a model + provider + params → `m_<hash>` |
| `prompts` | a system prompt + intent → `p_<hash>` |
| `variants` | model_id × prompt_id (+ anchoring) → `v_<...>` — the unit under test |
| `characters` | the test characters (card, prologue, initial input) |
| `dialogues` | **offline data points** — a variant playing a character (turns). Keep adding. |
| `sessions` | **online data points** — user-behaviour signals per session |
| `evaluators` | judge versions (model_snapshot, prompt_hash, rubric_version) |
| `grades` | one score: variant × dimension × phase, with role/interval/evaluator/caveats |
| `evidence` | good/bad example replies per dimension — the "why this grade" |

Models, prompts, and variants are **content-addressed** (id = hash of content), so re-adding the
same prompt is idempotent and "which prompt produced this score" is answerable from the row.

## CLI — the service surface

```bash
ceval init                                            # create the schema
ceval seed                                            # load the bundled demo (demo/) -> DB
ceval schema --mysql                                  # print the MySQL DDL

# inject — each returns an id
ceval model  add --name gpt-5.1 --provider openrouter          # -> m_...
ceval prompt add --name Playful --prompt "..." --intent "..."  # -> p_...
ceval variant add --model-id m_... --prompt-id p_... --id v_playful --label Playful

# data — offline dialogues, accumulate over time
ceval data add --variant v_playful --character en_dialogue_011 --turns-file conv.json
ceval data gen --variant v_playful                    # generate (needs a key / subagent)

# evaluate + visualise
ceval eval run [--offline] [--online] [--sim]         # score from DB, persist grades + evidence
ceval dashboard [--serve]                              # render from DB (static + interactive)
ceval serve [--port 8787]                              # serve the dashboard live (renders per request)

ceval model list / prompt list / variant list
ceval probe run|compare|drill|pool                     # measurement-science reproductions (raw corpus)
```

`--db` selects the backend (default `sqlite:///out/ceval.db`). The committed demo seed data lives
in `demo/gen` + `demo/judge`; override with `--gen-dir` / `--judge-dir`.

## How eval flows through the DB

1. `data add` / `data gen` write **dialogues** (offline data points); `eval run --online`
   simulates production-like traffic and **persists it as `sessions` rows** (online data points),
   then grades from the DB — the user keeps adding data points for a variant.
2. `eval run` reads the DB, runs the scoring lanes (compute · psychometric · judge for offline;
   behavioural for online — diagnostics graded, traps walled off), and writes **grades** +
   **evidence** back to the DB, tagged with the evaluator version. See [ONLINE.md](ONLINE.md).
3. `dashboard` reads grades + evidence + variants from the DB and renders (overview matrix,
   per-variant detail with prompt + rank, good/bad examples). `serve` does the same but live —
   `ceval/serve.py` re-renders from the DB on **every request**, so the loop is: edit data / eval
   run → refresh the browser → new data. No cached file, no rebuild step.

The scoring pipeline itself is unchanged; only its input/output moved from files to the DB
(`ceval/store/adapt.py`) and the render moved behind a shared builder (`ceval/report.py`).

## Verified end to end (SQLite, from a fresh DB)

```
init               -> 9 tables
seed  (reads demo/)-> 2 models, 4 prompts, 6 variants, 18 dialogues, 3 characters
eval run           -> 33 offline grades (real Opus judge) + 3,000 online sessions persisted
                      -> 78 online grades (graded from the DB) + 36 evidence rows
dashboard          -> static + interactive HTML; Sonnet-vs-Haiku matrix + per-variant drill-down
serve              -> http://127.0.0.1:8787 renders the same, live from the DB; inject a variant
                      while it runs and it appears on the next request with no restart
```

A clean clone reproduces this with **zero dependencies and no API key** — the demo seed data is
committed in `demo/`.

## Honest limits

- **MySQL is designed, not exercised here** — no MySQL server or `pymysql` in this environment,
  so the runnable backend is SQLite. The MySQL DDL is delivered and the driver is written; it has
  not been run against a live MySQL instance.
- **Judge & psychometric grades** for a newly-injected variant appear only once its judge
  recordings exist (real-Claude judging via subagent, or `--sim`). Compute + online grades are
  automatic. A variant with only a couple of short dialogues gets near-zero/NaN on some metrics,
  honestly dropped rather than faked.
- **Online sessions are now persisted** as `sessions` rows and graded from the DB (drill-down by
  variant / character / arm). The **traffic is still simulated** — with a *known injected
  structure* so the grader can be tested, not real users; the schema stores a real product's
  sessions the same way when one emits them. See [ONLINE.md](ONLINE.md).
