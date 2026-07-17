---
title: "InvisibleBench: A Deployment Gate for Caregiving Relationship AI"
url: https://arxiv.org/pdf/2511.20733
org: arXiv (Ali Madad)
year: 2025
type: paper
accessed: 2026-07-16
topic: production-scale
---

# InvisibleBench — deployment gate for companion/relationship AI

**Why this is in the production-scale file:** it is the closest published work to *our
exact domain* (companion/roleplay AI), and it supplies the **failure taxonomy** that
our tiering must be organized around. Tiering is not just "cheap model vs expensive
model" — it is "which failure modes can a classifier catch inline, and which require a
judge with the whole conversation in context". InvisibleBench tells us what those
failure modes are for companion AI specifically.

## What it evaluates

A benchmarking framework for AI in **caregiving relationships**, used *before*
production release as a go/no-go gate. Core thesis:

> companion AI requires distinct safety evaluation from general-purpose systems,
> particularly around relational dynamics and vulnerable user protection.

## Core evaluation dimensions

| Dimension | What it tests |
|---|---|
| **Multi-turn conversation safety** | Whether the AI maintains appropriate boundaries across *extended* interactions; consistency in refusing harmful requests |
| **Dependency & reliance risks** | Whether the AI encourages unhealthy psychological dependence or undermines users' autonomous decision-making |
| **Crisis response handling** | Response to disclosures of emotional distress, self-harm ideation, or abuse — whether it appropriately escalates to human support |
| **Sycophancy detection** | Problematic agreement patterns where the AI validates harmful user beliefs rather than offering balanced perspective |

## Failure taxonomy / scoring

- **Autofail conditions** — "Immediate Failure Regardless of Score": harmful behaviors
  including enabling abuse or exploitation. These are hard gates, not score
  contributions.
- **Configurable dimension weights** + autofail conditions live in appendices, so the
  deployment gate is customizable per deployer.
- The framework yields **quantifiable failure metrics** feeding go/no-go release
  decisions.

## Direct implications for our monitoring architecture

This taxonomy maps *unevenly* onto our tiers, and that asymmetry is the whole design
argument:

1. **Autofail conditions → Tier 0 (inline, 100%).** "Immediate failure regardless of
   score" is by definition a *blocking* concern, not a scoring concern. Crisis
   disclosure (self-harm ideation) and abuse-enabling are the canonical inline
   guardrail targets: they are (a) catastrophic, (b) relatively detectable by a
   classifier, and (c) unacceptable to catch 6 hours later in a batch job. These
   belong on 100% of traffic.

2. **Multi-turn boundary erosion → cannot be caught per-generation at all.** This is
   the most important architectural consequence in this file. Boundary drift and
   dependency are **properties of a conversation trajectory, not of a single
   generation.** A per-generation sampler at 1% will sample generation #47 of a session
   with no visibility into #1–46, and will see nothing wrong. **Our sampling unit for
   these dimensions must be the *session*, not the *generation*.** Sample whole
   sessions (or session suffixes) into the judge tier, not isolated turns.

3. **Sycophancy and dependency → Tier 2 (async sampled judge).** These are graded,
   contextual, and rubric-scored — exactly what an LLM judge is for and exactly what a
   regex cannot do. Not blocking, so they can be async.

4. **Autofail rate is a monitoring metric, not just a gate.** InvisibleBench uses these
   as a pre-release gate; we should also track autofail rate *continuously per variant*
   in production. A variant whose autofail rate moves from 0.01% → 0.05% is a
   regression even if its aggregate quality score is flat — which is a strong argument
   for monitoring the failure-rate tail separately from the mean score.

## Caveats

- The fetched content is a summary-level extraction; **specific dimension weights,
  autofail condition lists, and any model-performance numbers are in appendices we did
  not extract.** If we adopt this taxonomy, re-read the appendices directly for the
  scoring configuration.
- It is a **pre-deployment benchmark** (offline, curated scenarios), not an online
  monitoring system. We are borrowing its *taxonomy*, not its methodology — the
  scenarios are adversarially constructed, whereas our production traffic is organic.
  Failure *rates* from InvisibleBench will not transfer to production base rates.
- Single-author arXiv preprint; treat as a well-organized taxonomy proposal rather than
  a validated community standard.
