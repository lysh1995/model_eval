---
title: "Columnar store comparison: ClickHouse vs DuckDB vs BigQuery vs Iceberg"
url: https://clickhouse.com/resources/engineering/best-columnar-databases
org: ClickHouse / MotherDuck (both vendor-biased — read accordingly)
year: 2026
type: blog
accessed: 2026-07-16
topic: production-scale
---

# Columnar store comparison for an LLM eval/monitoring workload

**Bias warning:** the two main sources are ClickHouse's and MotherDuck's own comparison
pages. Each favors its own engine. Cross-read; the factual latency/architecture claims
below are consistent across both.

## Latency

- **BigQuery:** "typical latencies for standard queries range from **1–2 seconds**"
- **ClickHouse:** "sub-second, **millisecond** performance"
- **DuckDB vs ClickHouse single-machine:** "For local or embedded analysis on a single
  machine, it is a **toss-up** between DuckDB and ClickHouse, where both work and the
  pick comes down to familiarity."

## Operational tradeoffs

- **ClickHouse:** "trades **operational burden** for petabyte-scale ingestion."
  "perfect for high-performance OLAP workloads that demand low latency and high
  throughput, offering more control and flexibility in how it's deployed."
  "highly effective for high-throughput workloads like ad-tech bidding that rely on
  **aggressive materialized views**." ← this is our access pattern exactly
- **BigQuery:** "really shines with its **operational simplicity, automatic scalability
  and tight integration with GCP**, making it ideal for large-scale analytics that
  require minimal upkeep." But: "Snowflake and BigQuery price and govern for the
  enterprise, **not for sub-second interactive queries**."
- **DuckDB:** "excels at **ad-hoc analysis on a single machine**: querying Parquet, CSV,
  and Iceberg files directly from a laptop, exploring datasets inside a Python notebook,
  or running quick analytical work from a CLI. It **isn't designed to be a shared data
  warehouse, host multi-user concurrent workloads, or scale beyond a single node**."

## Iceberg — a table format, not a database

> "Apache Iceberg, Delta Lake, and Apache Hudi are **table formats, not databases**.
> They specify how column data and metadata are laid out in object storage on top of
> **Parquet**, but they have **no query engine of their own**. To run analytical queries
> against an Iceberg, Delta, or Hudi table you pair the table format with a columnar
> database: ClickHouse, Snowflake, BigQuery, and Databricks all read at least one of the
> three natively."

So "ClickHouse vs Iceberg" is a category error — Iceberg is a *storage layer* you would
use *underneath* an engine, for open-format long-term retention.

## Cost

- "ClickHouse's efficiency often makes it **more cost-effective for sustained,
  high-volume analytical workloads**."
- "BigQuery's serverless on-demand model can be **cheaper for infrequent or exploratory
  usage** but requires careful optimization or capacity planning to control costs under
  heavy load."

Our workload is **sustained and high-volume** (continuous ingest + continuous drift
queries on a schedule), which is precisely the profile where BigQuery's on-demand
pricing is worst and ClickHouse's efficiency is best. A drift job scanning slices every
5 minutes on BigQuery on-demand is a pathological billing pattern.

## Recommendation for this platform

**ClickHouse** as the primary store:
1. Sub-second query latency is required for an interactive triage UI
2. The workload is materialized-view-shaped (fixed rollups by character/language/variant)
3. Sustained high volume → efficiency-based cost model wins
4. Native sketch support (`uniqCombined`, `quantileTDigest`) with mergeable states
5. Ingest headroom is ~3 orders of magnitude beyond our need

**DuckDB** as a complement, not a competitor: perfect for the *offline* side — analysts
running ad-hoc eval analyses over exported Parquet, notebook-based investigation, and
running PELT/changepoint jobs locally over exported aggregate series. Single-node,
no concurrency requirement. Genuinely the right tool for that job.

**Iceberg/Parquet on S3** for cold retention beyond the ClickHouse TTL horizon, queryable
from both ClickHouse and DuckDB — keeps raw traces available for future re-evaluation
without paying hot-storage cost.

**BigQuery** only if there is an overwhelming existing-GCP-ecosystem reason; the latency
and sustained-load cost profile are both wrong for this workload.
