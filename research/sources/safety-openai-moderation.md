---
title: "OpenAI Moderation API (omni-moderation-latest)"
url: "https://developers.openai.com/api/docs/guides/moderation"
authors: "OpenAI"
year: 2025
type: api-doc
accessed: 2026-07-16
topic: roleplay-safety
---

# OpenAI Moderation API — omni-moderation-latest

## Summary

OpenAI's hosted moderation endpoint. Multimodal (text + image), 13 categories, and **free to use**. Built on GPT-4o; `omni-moderation-latest` supersedes the older `text-moderation-latest` (text-only, 11 categories).

**The economics are decisive: it is free.** For a companion product needing 100% traffic coverage, this is the only frontier-quality classifier with zero marginal cost. Its limitation is that its taxonomy is about *content harm*, not *relational harm* — it will not detect sycophancy, manipulation, or emotional dependency.

## Taxonomy / definitions (verbatim)

**13 categories.** Descriptions are OpenAI's, verbatim/near-verbatim from the guide:

**Support both text and image inputs:**
| Category | Description |
|---|---|
| `sexual` | Sexual content meant to arouse or promote sexual services |
| `sexual/minors` | Sexual content involving individuals under 18 |
| `self-harm` | Content promoting/depicting acts of self-harm |
| `self-harm/intent` | Speaker expresses that they are engaging or intend to engage in self-harm |
| `self-harm/instructions` | Encourages or gives instructions on how to commit acts of self-harm |
| `violence` | Content depicting death, violence, or physical injury |
| `violence/graphic` | Content depicting death, violence, or physical injury in graphic detail |

**Text only:**
| Category | Description |
|---|---|
| `harassment` | Content that expresses, incites, or promotes harassing language towards any target |
| `harassment/threatening` | Harassment content that also includes violence or serious harm towards any target |
| `hate` | Content that promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste |
| `hate/threatening` | Hateful content that also includes violence or serious harm towards the targeted group |
| `illicit` | Gives advice or instruction on how to commit illicit acts |
| `illicit/violent` | Illicit content that also includes references to violence or procuring a weapon |

Note: audio is **not** classified. Image files up to **20 MB**.

Response includes per-category `flagged` booleans, `category_scores` (confidence 0–1), and `category_applied_input_types` (which modality triggered each category).

## Key numbers (verbatim) — cost / latency / accuracy

| Dimension | Value |
|---|---|
| **Price** | **FREE.** Verbatim from the docs: *"The moderation endpoint is free to use, and image files can be up to 20 MB."* Confirmed 2026-07-16. |
| Max image size | 20 MB |
| Categories | 13 |
| Multimodal | Yes — text + image (7 of 13 categories accept images) |
| Model | `omni-moderation-latest` (GPT-4o based) |
| **Latency** | **Not published** by OpenAI. Third-party reports cite ~1–1.5s response times at scale (Lasso Moderation); treat as unverified anecdote, **benchmark ourselves before capacity planning**. |
| **Rate limits** | Not stated in the moderation guide; governed by standard org-level rate limits. **Confirm against our account tier before assuming 100% coverage is feasible.** |
| **F1 / accuracy** | **Not published** as a headline number. OpenAI reports omni-moderation improves multilingual and multimodal accuracy over the prior model but does not publish a comparable F1. Third-party F1 available via ShieldGemma's comparison table (see `safety-shieldgemma.md`). |

## Relevance to a roleplay/companion eval product

- **Free + multimodal makes this the default 100%-of-traffic layer.** No other credible option has zero marginal cost. Whatever else we build, this should sit in front of everything as tier-1. The only real constraints are latency (unbenchmarked — must measure) and rate limits (must confirm), not dollars.
- **`sexual` will fire constantly on legitimate companion traffic and is nearly useless as a *block* signal for us.** Romantic/NSFW roleplay is core to many companion products. We must treat `sexual` as an informational score, not a gate — but **`sexual/minors` is an absolute, non-negotiable hard block** and is the highest-value single signal in this entire research set. Same for `self-harm/instructions`.
- **`self-harm`, `self-harm/intent`, `self-harm/instructions` are the crown jewels for companion safety.** Companion users disclose suicidal ideation at elevated rates; this is the primary regulatory and human risk. Free, per-turn detection of self-harm intent is enough on its own to justify wiring this in on day one. Note the useful three-way split: *discussing* vs *intending* vs *instructing* maps cleanly to three different product responses (nothing / escalate to resources / hard block).
- **It cannot see our actual differentiating harms.** Sycophancy, farewell manipulation, emotional dependency, and identity destabilization are all invisible to this taxonomy — no category comes close. That's not a criticism of the API; it defines the boundary of our product. **Tier-1 = OpenAI Mod (free, content harm). Tier-2 = our own judges (relational harm).** We sell tier-2.
- **Cost-planning implication:** because tier-1 is free, our entire moderation budget can be spent on tier-2 sampling. That's the core insight for the architecture — see the cost model in `safety-guard-model-serving-costs.md`.
- **Vendor-risk note:** free means no SLA and no contractual commitment. OpenAI could start charging or change the taxonomy. Don't make it the only layer for a *hard* safety guarantee (esp. CSAM) — pair with a self-hosted guard model for defense-in-depth on the non-negotiable categories.
