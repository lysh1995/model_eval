---
title: "LMArena → Arena.ai: leaderboard changelog, methodology changes 2025-2026"
url: https://arena.ai/blog/leaderboard-changelog/
publisher: Arena (formerly LMArena / Chatbot Arena / LMSYS)
date: continuously updated; entries cited below span 2025-07-14 → 2026-06-04. Accessed 2026-07-16
type: blog
accessed: 2026-07-16
topic: recent-news
---

# Arena (formerly LMArena) — methodology changes 2025-2026

**Structural fact: the domain has moved.** `news.lmarena.ai/*` now **301-redirects to
`arena.ai/blog/*`**. The org has rebranded from LMArena to **Arena**. Any code, citation, or doc
pointing at `news.lmarena.ai` or `lmsys.org` should be updated.

## Verified changelog entries (from the primary changelog page)

### Statistics / ranking methodology
- **2025-07-23** — Confidence intervals moved **from bootstrapping to "CLT for M-estimators"**
  for computational efficiency. Also a **reweighting scheme** to balance models with very
  different vote counts.
- **2026-05-12** — **"Battles in Direct"**: direct-chat sessions are now converted into model
  battles. Critically, they **correct for position bias favoring Model A** and for
  **same-organization bias**, by adding features to the Bradley-Terry model:
  **`is_direct_battle`** and **`same_org_indicator`**.

  This is the single most important methodological change for anyone citing Arena scores:
  **position bias and same-org bias are now explicitly modeled as BT covariates**, not assumed away.

### Data quality
- **2025-07-14** — Enhanced **deduplication (filters ~10% of votes)** and **identity-leak
  detection (removes <4% of votes)**. Dedup targets high-frequency prompts in the **top 0.5%**
  percentile.
- **2025-09-02** — Filtering to remove mistaken image-gen/edit requests from text-arena vision data.
- **2025-09-17** — Filtering for statistically anomalous voting patterns; removes "votes from users
  whose votes are arbitrary."
- **2026-01-13** — Consistent vote filtering (identity-leak detection, quality filtering) and vote
  de-duplication extended to text-to-image and video arenas.

### Policy — direct response to Leaderboard Illusion critique
- **2025-09-18** — Introduced a **"preliminary" tag** for models that were **tested anonymously and
  then released publicly**, signalling that scores are pending stabilization post-launch.
  This is the concrete, shipped policy change that addresses the *private-variant testing* /
  *selective disclosure* complaint in arXiv 2504.20879. It does **not** address the
  sampling-rate disparity or the deprecation-rate disparity complaints.

### New categories / arenas
- **2025-11-05** — **Arena Expert**: framework identifying the "toughest, most expert-level
  prompts" — **5.5% of all prompts**, vs. the older "Hard" tier's **~33%**. Ships **eight new
  occupational leaderboards**: Software & IT Services; **Writing / Literature / Language**;
  Life/Physical/Social Science; Entertainment/Sports/Media; Business/Management/Financial Ops;
  Mathematical; Legal & Government; Medicine & Healthcare.
- **2026-02-09** — Text-to-Image Arena redesigned with prompt categories + quality filtering;
  deprecated the user-generated vs pre-generated distinction.
- **2026-02-25** — Code Arena WebDev segmented into **HTML** (standalone) and **React** (multi-file).
- **2026-03-10** — Video Arena consolidated voting categories after migration to the arena.ai
  platform; voting restricted to **prompt authors only**, discontinuing the separate "Author Vote"
  category.
- **2026-04-15** — Image-to-WebDev leaderboard.
- **2026-06-04** — **Agent Arena**, measuring **"behavioral signals like file downloads,
  disapproval events, retries, and steerability."**

## Is there a roleplay / companion category?

**No.** Verified against the category post (https://arena.ai/blog/arena-category/, **published
2024-10-30**): categories are Math, Coding, Hard Prompts, Instruction-Following, languages,
multi-turn, long/short query, Style Control, Refusal, and **Creative Writing**.

**Important correction to a common claim:** secondary sources describe Creative Writing as a
"new category." It is **not new — it dates to the 2024-10-30 post.** The closest thing to a *new*
writing-adjacent category is the **Writing/Literature/Language occupational leaderboard
(2025-11-05)** under Arena Expert.

**There is no roleplay arena and no companion arena as of 2026-07-16.** This is a genuine gap in
the public eval ecosystem and a reason a companion-eval platform has room to exist.

## How categories are computed (from the 2024-10-30 post)

- Categories start as **checklists of defining criteria**.
- Classification at scale via **"Label Bench"**: design system prompts from the category
  definition → generate ground-truth labels with strong LLMs on **2,000–5,000 sample battles** →
  optimize smaller classifiers and verify accuracy → deploy across all **~2 million battles**.
- Creative Writing classifier reported at **96.1% accuracy** using **Llama-3.1-70B**.

## UNVERIFIED

- Funding numbers. Secondary sources claim a May 2025 round of $100M at $600M valuation and a
  Jan 2026 Series A of $150M at $1.7B valuation (a16z), and separately "~$250M total at $1.7B."
  **These conflict with each other and none were confirmed against a primary Arena announcement
  or SEC filing. Do not cite.**
- Whether Arena has publicly responded in prose to the Leaderboard Illusion paper (the
  "preliminary" tag is inferred-by-timing as a response; the changelog does not cite the paper).
