# Quickstart

Zero dependencies. Pure stdlib Python 3.9+. No API key needed for anything below. One entrance:
`python3 -m ceval`.

## Track A — run the platform (the service)

DB-backed, end to end. Ships with a committed demo (`demo/`), so this runs on a clean clone with
no dataset download and no key.

```bash
python3 -m ceval init                 # create the SQLite DB — 9 content-addressed tables
python3 -m ceval seed                 # load the bundled demo variants + dialogues (demo/) → DB
python3 -m ceval eval run --sim       # score offline + online, persist grades + evidence
python3 -m ceval dashboard            # write out/platform_dashboard.html (static) + _interactive
python3 -m ceval serve                # OR serve it live → http://127.0.0.1:8787 (renders per request)
```

`eval run --sim` uses the **labelled simulated** judge (token-thrifty, deterministic, marked as
such in the dashboard). Drop `--sim` to use the **recorded real-Claude** judge scores in
`demo/judge/` where they exist. Compute and online grades are real measurements either way.

### Inject your own model, prompt, and variant

Everything gets a content-addressed id and persists. Re-run `eval` and `dashboard` to see it.

```bash
M=$(python3 -m ceval model  add --name gpt-5.1 --provider openrouter)     # → m_...
P=$(python3 -m ceval prompt add --name Playful --prompt "Tease, riff, never break character." \
                                --intent "playful, high-agency")           # → p_...
python3 -m ceval variant add --model-id $M --prompt-id $P --id v_playful --label Playful

# add offline data points (a dialogue = a variant playing a character), accumulate over time
python3 -m ceval data add --variant v_playful --character en_dialogue_011 --turns-file conv.json
# or generate them (needs a provider key, or a subagent to fulfil the written request file)
python3 -m ceval data gen --variant v_playful

python3 -m ceval eval run --sim
python3 -m ceval dashboard
python3 -m ceval model list          # also: prompt list · variant list
```

### Storage backend

```bash
python3 -m ceval schema --mysql       # print the MySQL DDL (the designed production database)
python3 -m ceval --db mysql://user:pass@host/db  init   # activates the pymysql driver if installed
```

`--db` defaults to `sqlite:///out/ceval.db`. Same table definitions emit driver-appropriate DDL,
so nothing diverges between the runnable SQLite backend and the designed MySQL one.

## Track B — reproduce the measurement science

The findings that justify the design — judge-free, on the raw MiniMax corpus. First fetch the data
(171 MB, gitignored, redownloadable):

```bash
mkdir -p data/{en,zh} data/_quarantine
B=https://huggingface.co/datasets/MiniMaxAI/role-play-bench/resolve/main/data
for L in en zh; do
  curl -sL "$B/$L/seeds.jsonl"       -o data/$L/seeds.jsonl
  curl -sL "$B/$L/dialogues.jsonl"   -o data/$L/dialogues.jsonl
  curl -sL "$B/$L/evaluations.jsonl" -o data/_quarantine/evaluations.$L.jsonl  # QUARANTINED
done
```

```bash
python3 -m ceval probe status                                   # config + what's live vs mocked
python3 -m ceval probe run     --lang en                        # score every model, judge-free
python3 -m ceval probe run     --lang zh                        # a different world — ρ(en,zh) = −0.082
python3 -m ceval probe compare deepseek-v3.2 deepseek-v3.1 --lang en   # ship report: Δ, CI, MDE
python3 -m ceval probe drill   deepseek-v3.2 --lang en          # per-character, SHRUNK, with intervals
python3 -m ceval probe pool                                     # the platform refuses to pool languages
```

And the first-party statistical findings, straight from `scripts/`:

```bash
python3 scripts/noise_floor.py            # σ_within > σ_between: a conversation isn't evaluable
python3 scripts/srm_variance.py           # the chemistry term: 6.7% (en) / 14.6% (zh)
python3 scripts/l1_convergent_reading.py  # characters vary 4–5× in readability
python3 scripts/card_awareness_audit2.py  # did the user simulator see the character card?
PYTHONPATH=. python3 scripts/e2e.py       # R1/R2/R3/R7/R11 in one run: create → dry-run → gate → ship → collect → loop
```

## Enabling the judge lane

Lanes 0–2 need no model calls and run today. Lane 3 (pairwise judging) needs a key:

```bash
cp config.example.json config.json
export ANTHROPIC_API_KEY=sk-ant-...      # then set judges[].kind = "anthropic"
export OPENROUTER_API_KEY=sk-or-...      # then set judges[].kind = "openrouter"
python3 -m ceval probe status            # confirms LIVE vs mock
```

**Keys are never stored in config.json** — it names the env var to read.

**The judge panel must be family-disjoint.** Self-preference is causal and does not cancel by
averaging: Claude-3.5 judging its own pairs went 64.3% → **44.8%, below chance**. Three
same-family judges are one judge with extra steps.

## Verifying the rules bite

The framework refuses, at import time, to load a metric with no confound test, no validity claim,
or `role=GATE` without a measured noise floor. It refuses to compare across evaluator versions, to
pool across languages, and to construct a card-aware user simulator. Try it:

```bash
python3 -c "
from ceval.metrics.base import Metric, Role
class Bad(Metric):
    name='bad'; validity='x'
    def compute(self, items): return {}
"   # -> TypeError: no registered confound tests
```
