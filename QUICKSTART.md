# Quickstart

Zero dependencies. Pure stdlib Python 3.9+. No API key needed for anything below.

```bash
# 1. fetch the corpus (171MB, gitignored, redownloadable)
mkdir -p data/{en,zh} data/_quarantine
B=https://huggingface.co/datasets/MiniMaxAI/role-play-bench/resolve/main/data
for L in en zh; do
  curl -sL "$B/$L/seeds.jsonl"       -o data/$L/seeds.jsonl
  curl -sL "$B/$L/dialogues.jsonl"   -o data/$L/dialogues.jsonl
  curl -sL "$B/$L/evaluations.jsonl" -o data/_quarantine/evaluations.$L.jsonl  # QUARANTINED
done

# 2. see what's live vs mocked, and what each metric claims to predict
python3 -m ceval.cli status

# 3. score all 11 variants, judge-free, on real data
python3 -m ceval.cli run --lang en
python3 -m ceval.cli run --lang zh        # a different world -- rho(en,zh) = -0.082

# 4. a ship report: delta, interval, MDE, and what it CANNOT tell you
python3 -m ceval.cli compare deepseek-v3.2 deepseek-v3.1 --lang en

# 5. drill-down: per-character, SHRUNK, with intervals (raw cells are noise amplifiers)
python3 -m ceval.cli drill deepseek-v3.2 --lang en

# 6. watch the platform refuse to do something it is asked to do
python3 -m ceval.cli pool
```

## Enabling the judge lane

Lanes 0–2 need no model calls and run on the real corpus today. Lane 3 (pairwise judging)
needs a key:

```bash
cp config.example.json config.json
export ANTHROPIC_API_KEY=sk-ant-...      # then set judges[].kind = "anthropic"
export OPENROUTER_API_KEY=sk-or-...      # then set judges[].kind = "openrouter"
python3 -m ceval.cli status              # confirms LIVE vs mock
```

**Keys are never stored in config.json** — it names the env var to read.

**The judge panel must be family-disjoint.** Self-preference is causal and does not cancel by
averaging: Claude-3.5 judging its own pairs went 64.3% → **44.8%, below chance**. Three
same-family judges are one judge with extra steps.

## Reproducing the first-party findings

```bash
python3 scripts/noise_floor.py            # sigma_within > sigma_between: a conversation isn't evaluable
python3 scripts/srm_variance.py           # the chemistry term: 6.7% (en) / 14.6% (zh)
python3 scripts/l1_convergent_reading.py  # characters vary 4-5x in readability
python3 scripts/card_awareness_audit2.py  # did the user simulator see the character card?
```

## Verifying the rules bite

The framework refuses, at import time, to load a metric with no confound test, no validity
claim, or `role=GATE` without a measured noise floor. It refuses to compare across evaluator
versions. It refuses to construct a card-aware user simulator. Try it:

```bash
python3 -c "
from ceval.metrics.base import Metric, Role
class Bad(Metric):
    name='bad'; validity='x'
    def compute(self, items): return {}
"   # -> TypeError: no registered confound tests
```
