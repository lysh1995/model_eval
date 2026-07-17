# C2: 50M/day from measured units (2026-07-17)

Reproduce: `PYTHONPATH=. python3 scripts/scale_report.py`

The brief: *"Assume 50M generations/day in production. Demonstrate your design holds at that
volume with real numbers."* Until now every scale figure in this project was **borrowed** —
a vendor price, a ClickHouse benchmark, someone else's cost calc. Those are citations. The
brief asked for a demonstration.

Every number below carries provenance: **MEASURED** (timed here, real corpus) / **BORROWED**
(published) / **ASSUMED** (a guess about production we cannot check).

## The load-bearing claim, tested

The whole tiering argument rests on *"Lanes 0–2 are free enough to run on 100% of traffic."*
If false, the cost model is fiction.

| | |
|---|---|
| Lane 1 throughput | **386 dialogues/sec/core** — MEASURED (best of 3, single core, pure stdlib, 495 real dialogues / 50,490 turns) |
| 50M/day requires | **1.5 cores** |
| cost | **$1.44/day** |

**VERDICT: HOLDS.** 100% coverage of Lane 1 at 50M/day is a rounding error. Not asserted —
measured, on this machine, reproducible.

## Cost at 50M/day

| lane | coverage | items/day | $/day | provenance |
|---|---|---|---|---|
| 1 (computation) | 100% | 50,000,000 | **1.44** | measured |
| 3 (haiku-4.5) | 1% | 500,000 | 150.25 | our token count (measured) × published price (borrowed) |
| 3-gold (opus-4.8) | 0.01% | 5,000 | 45.08 | same |
| **TOTAL** | | | **196.76** | **= $71,819/yr** |

**Counterfactual — no tiering:** 100% haiku = **$5.48M/yr (76×)**. 100% opus live =
**$164.5M/yr (2,291×)**.

Note this is *lower* than the $283k/yr the research stream cited — because our rubric is
smaller than whatever they assumed. **Their number was never ours.**

## The finding: prompt caching does not engage, and the fix is to make the rubric BIGGER

Our rubric prefix is **527 tokens**. Caching needs **≥4,096 to engage at all, silently**.
So the widely-cited *"prompt caching saves $370k/yr"* is, for us, **$0/yr**.

Then the arithmetic gets strange. Cached tokens cost **10× less**:

| rubric tokens | cache? | $/yr @ 500k judgments/day |
|---|---|---|
| **527 (ours)** | no | **$80,939** |
| 4,000 | no | $397,850 |
| **4,096** | **yes** | **$70,226** ← optimum |
| 6,000 | yes | $87,600 |
| 10,000 | yes | $124,100 |

**Two things fall out:**

1. **A 4,096-token rubric is 13% CHEAPER than our 527-token one**, despite being 8× larger.
   Break-even: `4096 × $0.10 = 410` price-units vs `527 × $1.00 = 527`. **Caching wins at 8×
   the size.**
2. **4,000 → 4,096 tokens — a 96-token difference — changes cost by 5.7×** ($397,850 →
   $70,226). This is a **cliff, not a slope**, and nothing warns you which side you are on.

**Recommendation: deliberately author the rubric to ≥4,096 tokens.** It sounds absurd and the
arithmetic is unambiguous. It also uses the space well — a longer rubric can carry the
behavioural anchors, the abstention rules, and the reference exemplars we want anyway.

**This is what "real numbers" buys.** Citing the $370k saving would have let us believe we
already had it. Measuring our own token footprint shows we have **$0** — and that the fix is
the opposite of what an engineer's instinct (*"trim the prompt"*) would suggest. Trimming our
rubric makes it **more** expensive.

## Storage & sampling

| | |
|---|---|
| event size | **476 bytes** — MEASURED on 200 real turns, uncompressed |
| storage | **8.7 TB/yr** uncompressed (a columnar store typically gets 5–10×) |
| ingest | 579 rows/sec sustained |

**Sampling — 950 cells (95 chars × 2 langs × 5 variants):** uniform 1% on a *flat*
distribution gives 526 judged/cell/day; a 500/cell/day floor costs 475k/day = **0.95% of
traffic** — the same budget.

⚠️ **ASSUMED, and it matters:** real traffic is **not** flat. The floor exists precisely
*because* a head/tail distribution starves the tail — but the actual shape is unknown to us.
This is a design under an assumption, and it is the **first thing to measure in production**.

## Provenance ledger

**MEASURED** — Lane 1 throughput (386/sec/core) · event size (476 B) · our rubric prefix (527 tok)
**BORROWED** — model prices · $0.04/core-hour · the ~4 chars/token heuristic (±15%)
**ASSUMED** — flat traffic (**it is not**) · 1% judge coverage (a policy choice) · 95×5 scoping
