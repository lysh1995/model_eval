---
title: "Probabilistic sketches: HyperLogLog, t-digest, DDSketch — error rates and memory"
url: https://blog.acolyer.org/2019/09/06/ddsketch/
org: Datadog (DDSketch, VLDB 2019); Ted Dunning (t-digest); Redis; ClickHouse
year: 2019
type: paper
accessed: 2026-07-16
topic: production-scale
---

# Sketches — accuracy/memory tradeoffs

## HyperLogLog

| Implementation | Registers | Memory | Standard error |
|---|---|---|---|
| Redis HLL | — | up to **12 KB** | **0.81%** |
| ClickHouse `uniqHLL12` | **2^12 = 4096** (5-bit cells) | "slightly more than **2.5 KB**" | **~1.6%** max |

**ClickHouse `uniqHLL12` accuracy by cardinality:**
- Small datasets (**<10K** elements): "up to **~10% error**"
- High-cardinality (**10K–100M**): "maximum error of **~1.6%**"
- Very large (**1B+** elements): accuracy degrades significantly; returns "very
  inaccurate results"

ClickHouse docs explicitly say: **"We do not recommend using this function. In most
cases, use the `uniq` or `uniqCombined` function."**

**`uniqCombined`** — the recommended one. Adaptive three-stage structure:
- small number of distinct elements → an **array**
- larger set size → a **hash table**
- large number of elements → **HyperLogLog**, fixed memory

"Use `uniqCombined` when you need better accuracy (**sub-1%**) and can afford more
memory."

General HLL theory: standard error = **1.04 / sqrt(m)** where m = number of registers.
m=4096 → 1.04/64 = **1.6%**. Matches the ClickHouse figure exactly. To halve the error
you must quadruple the memory.

## DDSketch (Datadog, VLDB 2019) — relative error guarantee

**Guarantee:** An **alpha-accurate** sketch outputs quantiles within **alpha * x** of the
true value x, for all quantiles in range (q0, q1).

> "using DDSketch with a relative accuracy guarantee set to **1%**, if the expected
> quantile value is **100**, the computed quantile value is guaranteed to be between
> **99 and 101**."

**Gamma parameter:**
```
gamma := (1 + alpha) / (1 - alpha)
```
For **alpha = 0.01, gamma ~= 1.02**.

Bucket i stores values between `gamma^(i-1)` and `gamma^i`. Values are mapped by taking
**log_gamma(x)** and rounding up. This log-linear bucketing is why the error is
*relative* rather than *rank-based*.

**Bucket architecture:**
- *Basic version:* unbounded growth, **O(N)** worst-case space (pathological input of N
  points each in a different bucket)
- *Full version:* imposes a limit **m = f(n)** on bucket count by **collapsing buckets
  for the smallest indices** during insertion and merging

**Fully mergeable** — this is the critical property for a distributed rollup: sketches
from different shards/hours combine exactly, with no loss beyond the alpha guarantee.

## t-digest

- Uses a **rank-based** approach
- "gives lower errors on quantiles further away from the median than uniform rank-error
  sketches" but still relatively high on heavily-tailed datasets
- **Weakness:** "the high quantiles of the 'Simulated Latencies' dataset have relative
  errors of **more than 100%**"
- Accuracy "is very high for the Uniform Distribution dataset and on the tails of the
  API Latency Dataset" — i.e. it is distribution-dependent, which is the whole problem
- ClickHouse: "prefer `quantileTDigest` when results need to be **merged across
  shards**" — it is mergeable

## Comparative accuracy

- "The histogram-based methods (**HDR, DDSketch and circllhist**) all compute quantiles
  with a **relative error of below 2%**"
- **GK-sketch** (rank error): at the 99th percentile, error reached **1300ms** against
  ground truth
- **HDR Histogram:** uses relative error; weaknesses are bounded range limitations and
  "no published guarantees"
- **Moments sketch:** "only guarantees its accuracy for the **average** rank error (not
  the worst case)"

## Recommendation for the platform

**DDSketch over t-digest** for latency and token-count quantiles: t-digest's >100%
relative error on heavy-tailed simulated latencies is disqualifying, and LLM latency
distributions are exactly heavy-tailed (long generations, retries, queueing). DDSketch's
bounded relative error is the guarantee you actually want for a p99 SLO. Caveat:
ClickHouse ships `quantileTDigest` natively and not DDSketch — so either accept t-digest
inside CH for convenience, or compute DDSketch in the ingest pipeline and store the
serialized sketch as a blob.

For distinct counts (unique users, unique sessions): **`uniqCombined`**, sub-1% error.
