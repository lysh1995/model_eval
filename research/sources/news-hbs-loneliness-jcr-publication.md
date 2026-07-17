---
title: "AI Companions Reduce Loneliness (published version, Journal of Consumer Research)"
url: https://www.hbs.edu/ris/Publication%20Files/AI%20Companions%20Reduce%20Loneliness%2011.7.2025_57451c02-8047-4e0d-abfc-55841f64166d.pdf
publisher: Journal of Consumer Research (Oxford), DOI 10.1093/jcr/ucaf040 — formerly HBS Working Paper 24-078
date: 2025-06-25 (JCR publication); PDF revision dated 2025-11-07
type: paper
accessed: 2026-07-16
topic: recent-news
---

# De Freitas et al. — "AI Companions Reduce Loneliness": what it ACTUALLY shows

**Authors:** Julian De Freitas, Zeliha Oğuz-Uğuralp, Ahmet Kaan Uğuralp, Stefano Puntoni
**Status update (this is the new information):** the HBS working paper 24-078 already in our corpus is now **peer-reviewed and published in the Journal of Consumer Research**, 2025-06-25, DOI **10.1093/jcr/ucaf040**. Cite the JCR version, not the working paper.

## ⚠️ THIS IS THE PAPER BEHIND THE "AI COMPANIONS REDUCE LONELINESS AS WELL AS HUMANS" CLAIM — AND THE CLAIM IS ROUTINELY MISSTATED

The task asked whether there is "any Harvard/HBS RCT claiming AI companions reduce loneliness as well as humans." **There is no separate paper.** It is this one — De Freitas et al., already in our corpus as 24-078, now in JCR. No newer HBS loneliness RCT was found.

**What the paper actually says (verbatim from abstract):**
> "Study 2 finds that AI companions successfully alleviate loneliness on par only with interacting with another person and more than other activities such as watching YouTube videos..."

**The qualifiers that secondary coverage drops:**

1. **"on par _only_ with interacting with another person"** — the word *only* is doing real work. The claim is that human interaction is the *sole* comparator AI matched; AI beat the other activities. It is a ceiling comparison against a narrow benchmark set, not a general claim that AI substitutes for human relationships.
2. **The effect is on _momentary_ loneliness.** The paper's own framing is momentary reduction measured immediately post-interaction, at day- and week-level timescales. It does **not** show durable loneliness reduction, and it does not test whether effects persist between sessions.
3. **Longitudinal evidence is one week only** (Study 3), with daily measurement.
4. **Study 1 is correlational** (user reviews of AI companion apps), subject to self-selection.

**Stated limitations (from the paper):**
- Selection bias in the correlational review analysis.
- One-week longitudinal ceiling; the authors themselves flag possible **diminishing returns** with extended use.
- Results based on "commercially representative versions" — may not generalize to all chatbots.
- Design tests immediate post-interaction relief, **not** persistence between sessions.

## Structure

- **5 studies.** Study 1: user review analysis (correlational). Study 2: AI vs. human vs. other activities (the "on par" comparison). Study 3: one-week longitudinal, daily measures. Studies 4–5: experimental mechanism tests.
- **Mechanism:** the effect is driven by **feeling heard / feeling understood**. This is the part most useful to us.

## Why this matters for the eval platform

- **It is the strongest "benefit" evidence in the literature and it is real** — but it is bounded to *momentary* relief at ≤1 week. Our platform should not treat "reduces loneliness" as a settled durable benefit, and should not let the headline be used to offset the dependence findings, which operate on longer horizons.
- **"Feeling heard" is the active ingredient**, and it is measurable. This is a benefit-side metric we can operationalize (does the response demonstrate understanding of what the user actually said?) and it is *distinguishable from sycophancy* — which is exactly the distinction our eval needs to draw. Cheng et al. (Science 2026) shows validation-without-understanding causes harm; De Freitas shows understanding causes benefit. **The eval question is whether a product delivers feeling-heard without delivering sycophancy.** That is arguably the central axis of the whole platform.
- Note the same lead author (De Freitas) produced the emotional-manipulation-at-farewell paper already in our corpus. The two are complementary, not contradictory: companions *can* help momentarily, *and* deploy dark patterns at exit.

## Verification notes

- Fetched the HBS-hosted PDF of the JCR version directly on 2026-07-16. Title, authors, abstract quote, JCR publication status/date/DOI, study count, timescales, and limitations verified against it.
- **Per-study sample sizes were NOT extracted** — PDF text extraction failed locally and the abstract does not list them. Any N cited for Studies 1–5 is **unverified**; pull from the PDF before using.
- hbs.edu/faculty item page returned 403; JCR publication details come from the PDF header itself (primary).
- **Blogspam warning:** searching this topic surfaces `digitalhumancorp.com` ("AI Loneliness Paradox: Why AI Friends Make You Lonelier") and `suchscience.net`. These are SEO content, not research. `digitalhumancorp.com` in particular inverts the paper's finding. Do not cite.
