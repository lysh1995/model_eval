---
title: "Data versioning & lineage — DVC, lakeFS, content-addressing, experiment tracking"
url: https://lakefs.io/blog/dvc-vs-git-vs-dolt-vs-lakefs/
org: lakeFS / DVC (composite)
year: 2026
type: vendor-docs-composite
accessed: 2026-07-16
topic: eval-lifecycle
---

# Lineage & reproducibility infrastructure

Composite of:
- https://lakefs.io/blog/dvc-vs-git-vs-dolt-vs-lakefs/
- https://lakefs.io/blog/git-like-data-versioning-meets-mlops-lakefs-with-mlflow-datachain-neptune-quilt/
- https://doc.dvc.org/user-guide
- https://docs.lakefs.io/

## The two architectures

**DVC** — "lives **next to** Git, not inside it, versioning **pointers** (tiny metafiles) in
Git and storing the actual large artifacts in a remote like S3, GCS, Azure, SSH, or a local
cache." Provides CLI-driven pipelines, **`dvc.lock` for reproducibility**, experiment
tracking, `dvc push`/`dvc pull`.

**lakeFS** — "sits **in front of** your object store (S3, GCS, Azure Blob) and makes
**branches and commits a first-class feature of the storage namespace**, with reads and
writes seeing isolated branches, allowing you to **create a branch from 'production', run
transformations, and merge back without copying terabytes**."

lakeFS versioning primitives: **branches, commits, tags, hooks, merges, retention, lineage**.

## The reproducibility join

> "by pointing MLflow to a **lakeFS path (which includes a repo, branch, and commit ID or
> tag)**, you precisely record **which version of the data was used**, enabling every run to
> be reproduced by checking out the same lakeFS commit of the dataset, with **the lakeFS
> commit hash serving as the source of truth**."

**Hybrid pattern the sources recommend:** "use DVC for model artifacts and pipelines tied to
a repo and lakeFS for raw and curated datasets in the lake, tracking and pinning dataset
versions in DVC that **reference a lakeFS commit hash**, with **code living in Git and data
semantics living in the lake**."

## Content-addressing

DVC "doesn't explicitly use content-addressing as a primary feature" (it hashes for
dedup/caching, but the identity is the metafile pointer). DataChain "leverages external
versioning mechanisms (like content-addressable storage or S3 object versioning) to keep
track of dataset versions **by reference**."

> **The honest read: neither tool gives us what note 06 §7 actually asks for, and we should
> not adopt one expecting it to.** Note 06 wants
>
> ```
> evaluator_id = H(rubric_prompt_bytes, judge_model_id, judge_params, scoring_code_git_sha)
> ```
>
> — a **content hash of the evaluator's semantics**. DVC/lakeFS version *bytes on a
> filesystem*. They will happily tell you "dataset at commit abc123", and they will **not**
> tell you that two commits are semantically identical, nor hash a *rubric prompt* + *model
> ID* + *decoding params* into one identity, because that identity spans a file, an API
> string, and a JSON blob that live in different systems.
>
> **What we take: the pattern, not the product.**
> 1. **"The commit hash is the source of truth"** — the join key between experiment tracker
>    and data is a **hash, not a label**. Same argument as note 06 §7's "hash the rubric
>    bytes, not a version string," arrived at from the data-infra side.
> 2. **Branch-from-production without copying** (lakeFS's zero-copy branch) is genuinely
>    the right primitive for **retro-scoring** (note 06 §7): branch the trace archive, run a
>    new evaluator version across it, compare, discard. At 3–8 TB/yr this is affordable
>    *only* if branching is zero-copy.
> 3. **`dvc.lock`** — a **lockfile pinning the exact resolved inputs of a pipeline run**.
>    This is the right shape for our eval run manifest: not "run benchmark v3" but "run
>    these exact 95 character cards at these hashes, this anchor set at this hash, this
>    rubric at this hash, this judge snapshot."
>
> **Our storage is already ClickHouse + Iceberg/Parquet (note 06 §6), and Iceberg has
> snapshots and time-travel natively.** Recommendation: **don't add lakeFS or DVC.** Use
> **Iceberg snapshot IDs** as the dataset commit hash and compute `evaluator_id` ourselves
> in application code. Adding a data-versioning product would buy us a hash we can compute
> in ten lines and a second storage system to operate.

## What these tools do give: hooks

lakeFS **hooks** (pre-commit/pre-merge) are the mechanism for **enforcing** a lineage rule
rather than documenting it — e.g. refuse a merge to the `benchmark` branch unless every new
dataset item carries `provenance` and `source_trace_id`. Worth reimplementing as a CI check
on our side (see `pipeline-model-collapse.md`: the mined-fraction cap must be *enforced*,
not *monitored*, or it will drift).
