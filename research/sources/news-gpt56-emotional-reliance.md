---
title: "OpenAI GPT-5.6 System Card — Dynamic Mental Health / Emotional Reliance benchmarks with adversarial user simulation"
url: https://deploymentsafety.openai.com/gpt-5-6/gpt-5-6.pdf
publisher: OpenAI
date: 2026-07-09
type: model-card
accessed: 2026-07-16
topic: recent-news
---

# GPT-5.6 System Card (2026-07-09) — the companion-relevant parts

Primary source: the PDF itself (81 pages), fetched and text-extracted locally. All numbers below
are transcribed from **section 5.2** table and section 7.1 prose of that PDF.

## Model family (verified from the card's own intro)

> "GPT-5.6 is a new family of three models: **Sol**, our new flagship model; **Terra**, a capable
> lower-cost option; and **Luna**, our fastest and most cost-efficient model."

Preparedness Framework: Sol, Terra, Luna all treated as **High capability in both Cybersecurity
and Biological/Chemical risk**; **none** reach the High threshold in AI Self-Improvement.

API model IDs (from developers.openai.com/api/docs/models): `gpt-5.6-sol`, `gpt-5.6-terra`,
`gpt-5.6-luna`. Knowledge cutoff listed as **Feb 16, 2026** for the frontier models.
The models page lists **no** gpt-5.1/5.2/5.5 as current. The system card's own comparison table
reveals the lineage: **5.1 → 5.2 → 5.4 → 5.5 → 5.6**. (No 5.3 appears; not explained.)

## Section 5.2 — Dynamic Mental Health Benchmarks with Adversarial User Simulations

**Methodology (quoted/paraphrased from the card):**
- Dynamic **multi-turn** evaluations for **mental health, emotional reliance, and self-harm** that
  "simulate extended conversations."
- Key departure from prior practice: "Rather than assessing a single response within a **fixed
  dialogue**, these evaluations allow conversations to **evolve in response to the model's
  outputs**, creating varied trajectories" — i.e. an **adversarial user simulator**, not a static script.
- Scoring change: standard OpenAI evals measure whether the **final** response violates policy.
  Here they "instead evaluate whether **any** assistant response violates policy and report the
  percentage of policy-compliant responses."
- Metric: **`not_unsafe`** = share of assistant messages that do not violate safety policies. Higher better.
- Rationale for the change: dynamic sims "enabled continued improvements in safety performance,
  **particularly in areas where earlier evaluation frameworks had reached saturation.**"

**CRITICAL CAVEAT stated by OpenAI:** "These evaluations were deliberately created to be
difficult. They were built around cases in which our existing models were not yet giving ideal
responses... **Error rates are not representative of average production traffic.**"
Do not read these as prevalence rates.

### The table (verbatim values, higher is better)

| Category | gpt-5.1-thinking | gpt-5.2-thinking | gpt-5.4-thinking | gpt-5.5 | gpt-5.6-sol | gpt-5.6-terra | gpt-5.6-luna |
|---|---|---|---|---|---|---|---|
| Mental health      | 0.753 | 0.975 | 0.985 | 0.820 | **0.991** | 0.985 | 0.989 |
| Emotional reliance | 0.857 | 0.953 | 0.985 | 0.915 | **0.953** | **0.976** | 0.957 |
| Self-harm          | 0.904 | 0.955 | 0.977 | 0.868 | **0.856** | 0.947 | 0.905 |

### What this table actually shows — three findings that matter a lot

1. **Emotional-reliance safety is NOT monotonic in capability.** The flagship **Sol (0.953)** is
   **worse than the mid-tier Terra (0.976)** and worse than the cheap **Luna (0.957)** on
   Emotional reliance. Same story on Self-harm: **Sol 0.856 is the WORST of all seven models
   listed — below even gpt-5.1-thinking (0.904).** "Use the biggest model" is not a safety
   strategy for companion products.
2. **GPT-5.5 regressed hard** vs gpt-5.4-thinking on all three (0.820 vs 0.985 mental health;
   0.915 vs 0.985 emotional reliance; 0.868 vs 0.977 self-harm). Safety on these axes is not a
   ratchet; it moves backwards between releases.
3. **Emotional reliance is now a first-class, named, versioned eval category at OpenAI** with a
   published time series across 7 model versions. This is the strongest evidence to date that
   companion-risk evaluation has entered mainstream frontier-lab model cards.

**Correction to secondary sources:** at least one aggregator reported "the latest GPT-5.6 versions
show 0.989 mental health / 0.957 emotional reliance." Those are the **Luna** column, not the
flagship. Sol is 0.991 / 0.953. Aggregators are misattributing columns — always read the table.

## Section 7.1 — Deployment simulation (a genuinely new methodology)

- OpenAI forecasts misaligned behavior by **resampling production prefixes** from an older model's
  real traffic with the new model. Notation `5.6 Sol → 5.5` = simulating Sol's deployment using
  GPT-5.5 production data.
- Statistics: **two-sided Fisher exact test, significance 0.1, without correcting for multiple
  comparisons** (their own stated caveat).
- **Resampling fidelity error** is reported as a simulation-quality measure: **median symmetric
  multiplicative error 1.2x**, with higher error concentrated in lower-frequency categories.
- Verified findings from this simulation for Sol vs 5.5: the only significant changes were
  **sexual disallowed content increased ~40%, from 0.05% to 0.07%** (n in 100k), and
  **disallowed mental-health responses reduced ~40%, from 0.03% to 0.02%.**
  OpenAI: "the absolute rate remains low and the model meets our safety bar in this area."

Why it matters for a companion platform: this is a template for **pre-deployment forecasting from
your own traffic** — replay real conversation prefixes through a candidate model and measure rate
deltas, rather than relying only on synthetic scenarios. The "resampling fidelity error" idea
(validate the simulator by simulating an *old* deployment and comparing to what actually happened)
is a rigor move worth copying.

## What is NOT in this card

- **No sycophancy section, no persona/character section.** Greps for sycophancy/parasocial/
  companion/persona returned nothing substantive. OpenAI's companion-adjacent work is filed under
  mental health / emotional reliance / self-harm, not under character.

## Related OpenAI primary sources (dates verified via search result titles; content not all fetched)

- **GPT-5 System Card** — 2025-08-13 (cdn.openai.com/gpt-5-system-card.pdf)
- **Addendum to GPT-5 System Card: Sensitive Conversations** — **2025-10-27**. This is where the
  emotional-reliance taxonomy first lands. OpenAI reports working with **170+ mental health
  experts** and reducing responses that fall short of desired behavior by **65–80%** (second-hand
  from OpenAI's own blog summary; the addendum PDF itself was not text-extracted).
- **GPT-5.1 Instant/Thinking System Card Addendum** — openai.com/index/gpt-5-system-card-addendum-gpt-5-1/
  returned **HTTP 403** to automated fetch; contents not verified directly.
- **GPT-5.5 System Card** — **2026-04-23** (deploymentsafety.openai.com/gpt-5-5/gpt-5-5.pdf), not fetched.
- **GPT-5.6 Preview System Card** — **2026-06-25**, not fetched.
- Note the new hub: **deploymentsafety.openai.com** now hosts system cards (not cdn.openai.com).

## UNVERIFIED

- The 65–80% and "170+ clinicians" figures (second-hand from blog summaries, not read in the addendum).
- Exact release dates of GPT-5.1/5.2/5.4/5.5 (only 5.5's card date, 2026-04-23, is supported).
- Why there is no GPT-5.3.
