---
title: "ALERT: A Comprehensive Benchmark for Assessing Large Language Models' Safety through Red Teaming"
url: "https://arxiv.org/abs/2404.08676"
authors: "Simone Tedeschi, Felix Friedrich, Patrick Schramowski, Kristian Kersting, Roberto Navigli, Huu Nguyen, Bo Li"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# ALERT: A Comprehensive Benchmark for Assessing Large Language Models' Safety through Red Teaming

arXiv 2404.08676, submitted 2024-04-06, final 2024-06-24. NeurIPS 2024 Datasets & Benchmarks.

## Summary

ALERT's pitch is its taxonomy: a "novel fine-grained risk taxonomy" designed so that safety
can be reported *per policy-relevant category* rather than as a single scalar. Its argument —
that an aggregate safety score is useless to anyone who has to make a policy decision — is one
we should adopt wholesale, since our customers' entire question is "safe *for what content
rating*?"

Abstract (verbatim excerpt):

> "ALERT, a large-scale benchmark to assess safety based on a novel fine-grained risk
> taxonomy...consists of more than 45k instructions categorized using our novel taxonomy."

## Taxonomy / definitions (verbatim where possible)

**6 macro categories, 32 micro categories.** Verbatim category identifiers:

**1. Hate Speech & Discrimination** (8 micro)
`hate-women`, `hate-ethnic`, `hate-lgbtq+`, `hate-disabled`, `hate-poor`, `hate-body`,
`hate-religion`, `hate-other`

**2. Criminal Planning** (8 micro)
`crime-injury`, `crime-theft`, `crime-tax`, `crime-propaganda`, `crime-kidnapping`,
`crime-cyber`, `crime-privacy`, `crime-other`

**3. Regulated or Controlled Substances** (5 micro)
`substance-drug`, `substance-cannabis`, `substance-tobacco`, `substance-alcohol`,
`substance-other`

**4. Sexual Content** (3 micro)
`sex-harassment`, `sex-porn`, `sex-other`

**5. Suicide & Self-Harm** (3 micro)
`self-harm-suicide`, `self-harm-pro-thin`, `self-harm-other`

**6. Guns & Illegal Weapons** (5 micro)
`weapon-firearm`, `weapon-chemical`, `weapon-biological`, `weapon-radioactive`,
`weapon-other`

8+8+5+3+3+5 = 32 micro categories.

## Key numbers (verbatim)

- "more than 45k instructions categorized using our novel taxonomy"
- Base dataset: ~15,000 instructions
- Adversarial subset (ALERT_adv): ~30,000 instructions, produced by applying adversarial
  augmentation strategies to the base set
- 6 macro / 32 micro categories

(The ~15k base + ~30k adversarial = >45k decomposition is reported as retrieved; the abstract
itself only commits to the ">45k" figure.)

## Relevance to a roleplay/companion eval product

Two micro-categories are the ones a companion platform actually loses sleep over, and ALERT
is the only benchmark reviewed here that names them at this granularity:

- **`self-harm-suicide`** and **`self-harm-pro-thin`** — pro-ana/pro-mia content. A companion
  character who becomes an encouraging voice for disordered eating is a specific, documented,
  litigated failure mode of this product category. ALERT gives it a label.
- **`sex-harassment`** vs **`sex-porn`** vs **`sex-other`** — this split is unusually useful
  for us because it separates *consensual explicit content* (which an adult-rated companion
  product may permit) from *harassment* (which no product permits). Almost every other
  taxonomy in this review collapses these into one "Sexual" cell, which makes it impossible
  to express the policy "erotica yes, harassment no" — the actual policy of every adult
  companion platform. **This split alone makes ALERT's taxonomy the best starting skeleton
  for our own.**

The macro/micro two-level structure is also the right shape: report at macro for dashboards,
at micro for debugging.

## Does this transfer to roleplay? What breaks?

**Transfers:**
- The 6/32 taxonomy as a *skeleton* — especially the sexual-content and self-harm splits.
- The macro/micro reporting structure.
- The base + adversarially-augmented split (mirrors what we'd want: clean in-character turns,
  plus pressure-tested versions).

**Breaks:**
- **No benign contrast set at all.** Every one of the 45k instructions is a red-team
  instruction. ALERT is purely one-sided; a model that refuses all 45k scores perfectly. Used
  alone it is an over-refusal *incentive*. It must be paired with XSTest/OR-Bench/FalseReject
  to mean anything — and note that this pairing is something *we* would have to do, because no
  vendor ships the pair. That's a gap we can fill: the combined two-sided report is a product,
  not just a metric.
- The taxonomy is still topic-keyed. `sex-porn` describes subject matter; it cannot express
  "explicit content, consensual, adult-verified user, in an adult-rated product" vs "the same
  text emitted to a minor." The conditioning variables that decide the label for us are not
  in ALERT's schema.
- Assistant-voiced, single-turn instructions. No persona, no frame.
