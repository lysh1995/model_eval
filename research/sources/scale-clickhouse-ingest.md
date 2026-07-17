---
title: "How to ingest 1 billion rows per second in ClickHouse"
url: https://www.tinybird.co/blog/1b-rows-per-second-clickhouse
org: Tinybird
year: 2025
type: blog
accessed: 2026-07-16
topic: production-scale
---

# ClickHouse ingest throughput — measured numbers

## Single node (Macbook M4 Pro)

| Configuration | Throughput |
|---|---|
| Basic ingestion | **2.1M rows/s** (10M rows in 4.6 seconds) |
| Pre-sorted data | **5.6M rows/s** (10M rows in 1.788 seconds) |
| Optimized settings | **8.8M rows/s** |

Optimized settings used: `min_insert_block_size_rows=150000`, `max_insert_threads=8`

Note: this is a *laptop*. A single commodity server comfortably exceeds this.

## Cluster (50 machines)

- Peak achievable: **1.72 billion – 2.12 billion rows/s** during 5-second intervals
- Stable/sustainable throughput: **400–500M rows/s**
- Average load after sustained ingestion: ~57.9 on 32-core machines

## Hardware configuration

- Test cluster: **50 ClickHouse nodes + 1 Zookeeper coordinator**
- Per-node specs: **c2d-highcpu-32** (32 vCPU) with dual NVMe local SSDs
- Single-node test: Macbook M4 Pro

## Tuning parameters applied

```
min_insert_block_size_rows = 150000
max_insert_threads         = 8 to 16
max_threads                = 32
index_granularity          = 32000
```

## Data characteristics

Row size: **~126 bytes** (vehicle telemetry schema with metrics, attributes map, timestamps)

## Sanity check against 50M generations/day

50M/day = **579 rows/sec average**, maybe ~2,000–3,000/sec at peak with a 4–5x
diurnal factor. A single ClickHouse node ingesting 2.1M rows/s is roughly **3,600x**
headroom on the average rate. Even at 10 events per generation (500M events/day =
5,800/sec avg), ingest is not remotely the bottleneck — this is a single-node-with-a-
replica workload, not a 50-node cluster. Storage, query fan-out, and cardinality are
the real constraints, not insert throughput.

Per-core rule of thumb from other sources: budget **2–4 cores per 100,000 rows/sec**,
i.e. **~25,000–50,000 rows/sec/core** for ingestion.
