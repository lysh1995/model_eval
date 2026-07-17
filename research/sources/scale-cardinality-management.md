---
title: "High-cardinality data handling in ClickHouse; cardinality explosion in rollups"
url: https://oneuptime.com/blog/post/2026-01-21-clickhouse-high-cardinality-data/view
org: OneUptime / ChistaData / BigDataBoutique / ClickHouse
year: 2026
type: blog
accessed: 2026-07-16
topic: production-scale
---

# Cardinality explosion management

## The problem statement

"When dealing with high-cardinality dimensions or complex aggregations, standard
materialized views become unwieldy — **each new combination generates a new row**,
leading to data explosion and bloated storage. Grouping by columns with very high unique
values can cause the target table to become **enormous, negating performance benefits**."

## Our specific cardinality math

Slicing dimensions for this platform:
- **~95 characters**
- **2 languages**
- **N variants** (say ~5 prompt/model variants)
- x time bucket

Cross product per hour: `95 x 2 x 5 = 950` rows/hour = **22,800 rows/day** =
**~8.3M rows/year** at hourly grain. This is *completely trivial* for ClickHouse — a
rollup table of 8M rows is a rounding error. The cardinality is bounded and small.

**The key insight: the character/language/variant cross-product is NOT a cardinality
problem.** It is ~1,000 combinations. The danger only appears if you add unbounded
dimensions — `user_id`, `session_id`, `request_id`, raw prompt text — to the GROUP BY.
Those are the explosive ones (millions of users), and they must stay in the raw table
and never enter a rollup key.

Rule: **rollup keys must be drawn only from bounded, enumerable dimensions.** Unbounded
identifiers live in raw storage and are reached via point lookups, or are counted via
sketches (`uniqState`) rather than grouped by.

## LowCardinality

"**LowCardinality is great for columns with under 10,000 unique values**."

- `character_id` (~95), `language` (2), `variant` (~5), `model` (~10),
  `finish_reason` (~5) → all comfortably `LowCardinality(String)`
- Gives dictionary encoding → the **30x+** compression tier from the compression doc
- `user_id` (millions) → NOT LowCardinality; use `UInt64`

"Create tables with LowCardinality types for low-cardinality dimensions like country and
event_type, paired with AggregateFunction columns for metrics."

## Aggregation states solve the explosion

"Aggregation states solve cardinality explosion by storing **serialized intermediate
representations** of ongoing computations — instead of storing the final count,
ClickHouse stores the state of functions like **`uniqCombined`** or
**`quantileTDigest`**, which can later be merged with other states or finalized."

"The fix is to **always use AggregatingMergeTree with the State/Merge pattern** for
anything beyond simple sums and counts."

"Aggregation states are particularly effective for high-cardinality unique counting:
**tracking distinct users without exploding group-by combinations**." — i.e. you get
"unique users per character per hour" without ever putting user_id in the key.

## Performance guardrail

"If your GROUP BY produces nearly as many rows as the source, you've added insert
overhead without meaningful query benefit. **Check the aggregation ratio first.**"

For us: 50M raw generations/day → 22,800 rollup rows/day = an aggregation ratio of
**~2,200:1**. Excellent — this is exactly the regime where rollups pay off enormously.
