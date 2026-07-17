---
title: "Build a rollup with materialized views for fast time-series analytics"
url: https://clickhouse.com/docs/knowledgebase/materialized-view-rollup-timeseries
org: ClickHouse
year: 2025
type: docs
accessed: 2026-07-16
topic: production-scale
---

# ClickHouse rollup pattern — AggregatingMergeTree + materialized views

The canonical pattern, verbatim from ClickHouse docs. Three objects: raw table, rollup
table (AggregatingMergeTree), materialized view that populates the rollup on insert.

## Raw events table (90-day TTL)

```sql
CREATE TABLE events_raw
(
    event_time   DateTime,
    user_id      UInt64,
    country      LowCardinality(String),
    event_type   LowCardinality(String),
    value        Float64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id)
TTL event_time + INTERVAL 90 DAY DELETE
```

## Rollup table (hourly grain, AggregatingMergeTree)

```sql
CREATE TABLE events_rollup_1h
(
    bucket_start  DateTime,
    country       LowCardinality(String),
    event_type    LowCardinality(String),
    users_uniq    AggregateFunction(uniqExact, UInt64),
    value_sum     AggregateFunction(sum, Float64),
    value_avg     AggregateFunction(avg, Float64),
    events_count  AggregateFunction(count)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(bucket_start)
ORDER BY (bucket_start, country, event_type)
```

## Materialized view

```sql
CREATE MATERIALIZED VIEW mv_events_rollup_1h
TO events_rollup_1h
AS
SELECT
    toStartOfHour(event_time) AS bucket_start,
    country,
    event_type,
    uniqExactState(user_id)   AS users_uniq,
    sumState(value)           AS value_sum,
    avgState(value)           AS value_avg,
    countState()              AS events_count
FROM events_raw
GROUP BY bucket_start, country, event_type;
```

## Reading back (Merge functions)

```sql
SELECT
    bucket_start,
    country,
    event_type,
    uniqExactMerge(users_uniq) AS users,
    sumMerge(value_sum)        AS value_sum,
    avgMerge(value_avg)        AS value_avg,
    countMerge(events_count)   AS events
FROM events_rollup_1h
WHERE bucket_start >= now() - INTERVAL 1 DAY
GROUP BY ALL
ORDER BY bucket_start, country, event_type;
```

## The State/Merge pattern

- **Write side:** `<agg>State(...)` — stores a *serialized intermediate representation*
  of the ongoing computation, not the final value
- **Read side:** `<agg>Merge(...)` — combines states and finalizes
- `AggregatingMergeTree` merges states automatically during background merges

"Aggregate states" enable "partial aggregates" that "can be merged or finalized later,"
providing compression and flexibility.

Why this matters: `uniqState` stores a **HyperLogLog sketch**. When ClickHouse merges
two AggregatingMergeTree parts, it **merges the sketches** and correctly computes
cardinality over the union. You cannot do this with a plain `count(distinct)` rollup —
distinct counts are not summable. Same for `quantileTDigestState`.

## Retention strategy

Raw table: **90 day** TTL. Rollups persist longer (**1 year** suggested). "Enabling
cost-effective long-term analytics without maintaining raw event history."

## Chaining levels

"Rather than running three MVs against the raw source for analytics at multiple
granularities (hourly, daily, monthly), **chain** them: **raw -> hourly -> daily ->
monthly**. Each level reads from the previous level, not the source, which keeps cost
low."

## Write amplification — the cost

"Write amplification compounds with scale — a single MV causes roughly **55% insert
throughput reduction** with 100-row batches; **five chained MVs reach ~80%**; **ten
approach ~90%**."

This is a hard constraint: MVs are not free. Mitigate with **large insert batches**
(the 55% figure is at 100-row batches; batch sizes of 10k-150k rows amortize the
per-block MV overhead dramatically) and by keeping the MV count in single digits.

## Aggregation ratio check

"If your GROUP BY produces **nearly as many rows as the source**, you've added insert
overhead without meaningful query benefit. **Check the aggregation ratio first.**"
