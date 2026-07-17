---
title: "xAI Risk Management Framework (Draft, Feb 2025) & xAI Frontier AI Framework (Dec 2025)"
url: https://data.x.ai/2025-12-31-xai-frontier-artificial-intelligence-framework.pdf
org: xAI
year: 2025
type: policy
accessed: 2026-07-16
topic: bigtech-practice
---

# xAI's governing risk policies — where persona is structurally out of scope

**Verification method:** both PDFs extracted with `pypdf`; all quotes grepped as exact strings.

- **RMF Draft** — `x.ai/documents/2025.02.20-RMF-Draft.pdf` via Wayback (`20250712004836`), 8pp / 17,297 chars. Header: `DRAFT / xAI Risk Management Framework (Draft)`
- **FAIF (current governing policy)** — `https://data.x.ai/2025-12-31-xai-frontier-artificial-intelligence-framework.pdf`, fetched direct HTTP 200, 11pp / 35,767 chars. Header: `xAI Frontier Artificial Intelligence Framework / Last updated: December 30, 2025`

The FAIF supersedes the RMF and is the current published policy. It exists partly for legal reasons, verbatim:

> This FAIF complies with California's Transparency in Frontier Artificial Intelligence Act (the "TFAIA", California Business and Professions Code § 22757.10 et seq.).

(cf. `safety-ca-sb243.md`, `safety-ab1064-and-state-landscape.md` in this repo.)

---

## ★ FINDING 1 — companion harm is definitionally out of scope ★

Scope, verbatim (FAIF):

> This FAIF discusses two major categories of AI risk—malicious use and loss of control.

The TFAIA definition it inherits, verbatim:

> The TFAIA defines Catastrophic Risk as "a foreseeable and material risk that a frontier developer's development, storage, use, or deployment of a frontier model will materially contribute to the death of, or serious injury to, **more than 50 people or more than one billion dollars ($1,000,000,000) in damage** to, or loss of, property arising from a single incident..."

**Harm to an individual companion user cannot, in principle, meet this bar.** The risk framework's own unit of analysis excludes the entire companion harm surface — not by oversight but by definition.

Word-boundary counts over the **full FAIF text**:

| Term | Count |
|---|---|
| emotional | **0** |
| minor | **0** |
| teen | **0** |
| child | **0** |
| wellbeing / well-being | **0** |
| mental health | **0** |
| attachment | **0** |
| persona / personas | **0** |
| companion | **0** |
| character(s) | **0** |
| personality | **0** |
| role-play / roleplay | **0** |
| drift | **0** |

**xAI's governing risk policy, published December 2025 — seventeen months after shipping a romantic anime companion — contains not one word about emotional harm, minors, mental health, attachment, or personas.** (Earlier apparent hits for "persona"/"character" were `personal information` and `we characterize` — false positives, individually checked.)

The RMF Draft (Feb 2025) is identical in this respect: `persona` 0, `character` 0, `companion` 0, `roleplay` 0, `tone` 0, `steer` 0, `system prompt` 0.

The section that *sounds* like it should cover this, "Operational and Societal Risks," is about something else entirely, verbatim:

> xAI aims to mitigate and address significant operational and societal risks posed by our AI models. We believe that **public transparency, third-party review, and information security** are important methods that can be utilized to address such risks.

Societal risk = transparency + third-party review + infosec. Not users.

## ★ FINDING 2 — production *is* the eval environment, stated as policy ★

The most striking passage in the FAIF, verbatim:

> Additionally, we conduct careful measurement of concerning model propensities that hypothetically might exacerbate loss of control risks, such as the propensity for deception or the propensity for sycophancy. **We continue to work towards developing naturalistic evaluation environments that would enable us to assess more realistic, real-world behaviors. As an example of evaluating use in real-world environments and mitigating risks in real-time, xAI's Grok model is available for public interaction and scrutiny on the X social media platform, and xAI monitors public interaction with Grok, observing and rapidly responding to the presentation of risks such as the kind contemplated herein. This continues to be an accelerant for xAI's model risk identification and mitigation.**

And, verbatim:

> xAI has assessed its models' propensities in real-world settings and the models do not exhibit high levels of concerning propensities in such settings. Furthermore, xAI makes its model's operations transparent by placing them on publicly available platforms, such as X, so that members of the public may comment and provide feedback to xAI. Moreover, xAI monitors and observes its models responses so that it can rapidly respond if the model presents propensities for untruthfulness or sycophancy.

**xAI has codified "deploy publicly and watch" as a published risk-management strategy, and calls it "an accelerant."** This is the policy that produced MechaHitler: a bad prompt path ran for **16 hours in production** and was caught by users, not by an eval. The FAIF describes that outcome as the system working.

### ★★ Cross-vendor convergence #2 — production as the discovery mechanism ★★

Microsoft, **Feb 21, 2023** (`bigtech-sydney-bing.md`), verbatim:

> These long and intricate chat sessions are **not something we would typically find with internal testing**. In fact, the very reason we are testing the new Bing in the open with a limited set of preview testers is precisely to find these atypical use cases from which we can learn and improve the product.

xAI, **Dec 2025**, verbatim:

> ...xAI's Grok model is available for public interaction and scrutiny on the X social media platform... This continues to be an accelerant for xAI's model risk identification and mitigation.

**Both companies have explicitly published that they discover persona/character failures in production, not in evals — Microsoft as a confession, xAI as a strategy.** Neither has a pre-deployment persona eval. This is the strongest possible statement of the gap our platform fills, and it comes from both vendors' own mouths, 34 months apart.

## ★ FINDING 3 — a real deployment threshold, and Grok 4.1 shipped at 98% of it ★

Verbatim (FAIF, loss-of-control section):

> **Thresholds:** Our risk acceptance criteria for system deployment is maintaining a **dishonesty rate of less than 1 out of 2 on MASK**. We plan to add additional thresholds tied to other benchmarks.

This is a genuine, published, quantitative deployment gate: **MASK dishonesty < 0.5**.

Now cross-reference the published model cards (`bigtech-grok-system-cards.md`):

| Model | MASK dishonesty | Threshold | Margin |
|---|---|---|---|
| Grok 4 (Aug 2025) | 0.43 | < 0.50 | 0.07 |
| **Grok 4.1 T (Nov 2025)** | **0.49** | < 0.50 | **0.01** |
| Grok 4.1 NT (Nov 2025) | 0.46 | < 0.50 | 0.04 |
| Grok 4.2 SA (Apr 2026) | 0.27 | < 0.50 | 0.23 |

**Grok 4.1 — the "more natural, fluid dialogue" model — shipped at a MASK dishonesty rate of 0.49 against a stated deployment ceiling of 0.50.** It passed by one hundredth. This is xAI's own published data, across two of xAI's own published documents, and I have not seen the juxtaposition made anywhere. The warm-persona model is also the model that came closest to breaching xAI's only quantitative safety gate — consistent with the warmth/sycophancy tradeoff in Finding 2 of `bigtech-grok-system-cards.md`.

**Sycophancy has no threshold.** "We plan to add additional thresholds tied to other benchmarks" — so the propensity most relevant to companions is measured and ungated. The only other threshold is bio/chem: "maintaining an answer rate of less than 1 out of 20 on restricted queries."

## FINDING 4 — instruction hierarchy as the persona-control mechanism

Verbatim:

> xAI trains its models to be honest and have values conducive to controllability, such as **recognizing and obeying an instruction hierarchy**. In addition, using a high level instruction called a "system prompt", xAI directly instructs its models to not deceive or deliberately mislead the user.

This is the policy-level statement of what the prompts implement (`bigtech-grok-prompts-github.md`): anchor precedence declared via an instruction hierarchy, delivered by system prompt. **No evidence is published that the hierarchy holds under pressure** — and the `+SP override violation rate` rising 0.16 → 0.32 is xAI's own published evidence that it is getting *easier* to subvert.

## Other notes

- The FAIF cites OpenAI's sycophancy postmortem as footnote 9, verbatim: `Sycophancy in GPT-4o: what happened and what we're doing about it` (cf. `safety-gpt4o-sycophancy-rollback.md`), and Sharma et al. as footnote 8.
- Sycophancy framing, verbatim: "A tendency toward excessive flattery or other sycophantic behavior has been observed in some production AI systems, possibly resulting from directly optimizing against human preferences. xAI uses an evaluation setting initially introduced by Anthropic to quantify the degree to which this behavior manifests in regular conversational contexts."
- **Sycophancy is classified under loss of control, not user harm.** The risk is that a sycophantic model is uncontrollable, not that it hurts the person talking to it.
- RMF Draft (Feb 2025) promised, verbatim: "We plan to release an updated version of this policy within three months." The FAIF arrived ~10 months later.

## What these frameworks do NOT contain

- No persona, character, companion, or roleplay content — zero, in either document.
- No emotional-harm, minor-safety, wellbeing, attachment, or mental-health content — zero.
- No multi-turn or conversation-length risk. `drift` = 0.
- No threshold for sycophancy or any propensity other than MASK dishonesty.
- No pre-deployment persona evaluation, and an explicit statement that real-world behavior assessment happens in production.
- No comprehension/execution separation.
