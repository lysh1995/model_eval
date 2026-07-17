---
title: "CS4: Measuring the Creativity of Large Language Models Automatically by Controlling the Number of Story-Writing Constraints"
url: https://arxiv.org/abs/2410.04197
html_url: https://arxiv.org/html/2410.04197
year: 2024
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# CS4 — creativity as constraint satisfaction under increasing specificity

## Core idea

The problem being solved: "LLM-generated stories could seemingly look creative but be very similar to existing stories in their training corpus."

The trick: **by increasing the number of requirements/constraints in the prompt, you increase prompt specificity and hinder LLMs from retelling high-quality narratives in their training data.**

This converts creativity into something measurable *without human annotation*: if a model can only produce good output when it's allowed to regurgitate a memorized narrative, its quality will collapse as constraints tighten. A genuinely generative model degrades gracefully.

## Method

- Constraint levels: **9, 23, and 39 constraints**.
- Each model generates **150 stories** total.
- For each user instruction, the tested LLM revises a base story to satisfy constraints.
- Revised stories evaluated on: **constraint satisfaction ratio, quality, and diversity**.
- "empowers measurement of LLMs' creativity without human annotations."

## The metric that matters

Not the absolute score at any one constraint level — it's the **slope**: quality (and constraint-satisfaction) as a function of constraint count. The *degradation curve* is the creativity signal.

## Why this is powerful for roleplay/companion eval

This is the most directly transferable design in the whole literature, because:

1. **Constraint satisfaction is objectively checkable** — mostly no judge needed. "Did the response mention X / avoid Y / stay in first person / keep the character's established fear of water?" These are cheap programmatic or tiny-model checks.
2. It gives a **defensible number that is comparable across models by construction** — same constraint set, same base scenario, count satisfied. It's a ratio, bounded [0,1], with a real denominator. This is the most "defensible number" property in the entire topic.
3. **It maps perfectly onto roleplay**, which is *natively* a constrained generation task: stay in character, honor the persona card, respect established world facts, maintain continuity with prior turns, hit the requested tone. We do not need to invent artificial constraints the way CS4 did — our product already has them.
4. The degradation curve turns creativity into a **derivative**, which is far more robust to judge noise and prompt idiosyncrasy than a level.

## Design sketch for us

Define per-scenario constraint sets at 3 tiers (loose / medium / tight). Score = constraint-satisfaction ratio × quality, plotted across tiers. A model that memorized tropes shows a steep cliff; a creative one shows a gentle slope. Report the slope as "generative headroom."
