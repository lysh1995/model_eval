---
title: "Database compression: encodings, codecs and ratios"
url: https://clickhouse.com/resources/engineering/database-compression
org: ClickHouse
year: 2025
type: docs
accessed: 2026-07-16
topic: production-scale
---

# ClickHouse compression — ratios and codecs

## Compression ratios achieved

| Context | Ratio |
|---|---|
| Column-based, typical analytical data | **5–10x** |
| Low-cardinality columns | **30x+** |
| Row-based (PostgreSQL), analytical data | **1.5–3x** |
| Character.AI production (across columns) | **15–20x** |
| Seemplicity vs Postgres | **5–6x** smaller |

**ClickBench 100M-row benchmark:** ClickHouse stores the dataset in **9.26 GiB** vs
PostgreSQL's **~100 GiB** — a **10x** advantage driven by storage layout.

Note the Character.AI data point is directly relevant: that is an LLM chat product,
and they report **15–20x** average compression. LLM trace data (highly repetitive
model names, prompt templates, enum-ish fields) compresses better than generic
analytics data.

## Codec comparison

| Codec | Compression Ratio | Decompression Speed |
|---|---|---|
| LZ4 (ClickHouse default) | ~2x | **3–5 GB/s** |
| Snappy | ~2x | 2–4 GB/s |
| ZSTD (levels 1–3) | ~2.5x | 1–2 GB/s |
| ZSTD (levels 9–19) | ~3x | 0.3–1 GB/s |
| Zlib | ~3x | 0.2–0.4 GB/s |

"ZSTD compresses about **30% smaller than LZ4** at default levels but decompresses
**2–3x slower**."

These are the *general-purpose codec* ratios applied on top of encodings — the 5–10x
end-to-end number comes from stacking column-aware encoding under the codec.

## Encoding techniques (applied before the codec)

- Dictionary encoding
- Run-length encoding (RLE)
- Delta encoding
- **DoubleDelta** (delta-of-delta) — for monotonic sequences like timestamps
- **Gorilla** — floating-point compression
- Frame-of-reference (FOR) with bit-packing
- **T64**

**Gorilla on Facebook's production time-series database: 12x reduction.**

## Practical schema guidance implied

- Timestamps: `CODEC(DoubleDelta, LZ4)` — near-free at high ingest rates
- Float metrics (judge scores, latencies): `CODEC(Gorilla, LZ4)`
- Enum-like strings (model name, language, character_id, variant): `LowCardinality(String)`
  → the 30x+ tier
- Large text blobs (prompt/completion): `CODEC(ZSTD(1))` — accept the 2–3x slower
  decompression for the 30% storage win, since these are rarely scanned in aggregate queries
