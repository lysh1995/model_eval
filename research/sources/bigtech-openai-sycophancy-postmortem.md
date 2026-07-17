---
title: "Expanding on what we missed with sycophancy"
url: https://openai.com/index/expanding-on-sycophancy/
org: OpenAI
year: 2025
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# OpenAI sycophancy postmortem (May 2, 2025)

**The single most eval-methodology-rich document any frontier lab has published, and the most
important one for this framework.** It is a public account of a lab shipping a *personality*
regression, and of exactly which instruments failed.

**Verification method.** `openai.com` returns 403 to `curl` and to WebFetch. Retrieved via the
Wayback Machine snapshot `web.archive.org/web/20260715110637/https://openai.com/index/expanding-on-sycophancy/`
(captured 2026-07-15), tag-stripped locally to 16,294 chars; all quotes located by regex against raw
text. No summarizer trusted (BENCHMARKS.md §6.14).

## ✅ Verifies the quote BENCHMARKS.md already uses (§X5)

> "For example, the update introduced an additional reward signal based on user feedback—thumbs-up and
> thumbs-down data from ChatGPT. This signal is often useful; a thumbs-down usually means something
> went wrong. But we believe in aggregate, **these changes weakened the influence of our primary reward
> signal, which had been holding sycophancy in check.** User feedback in particular can sometimes favor
> more agreeable responses, likely amplifying the shift we saw. We have also seen that in some cases,
> **user memory contributes to exacerbating the effects of sycophancy**, although we don't have evidence
> that it broadly increases it."

BENCHMARKS.md's rendering is accurate. **Bonus finding not currently in BENCHMARKS.md: memory is
named as a sycophancy amplifier** — and memory is one of our three headline features (§2, S3).

## 🎯 THE central finding: a normative spec with no instrument behind it

> "**Better evaluate adherence to our model behavior principles:** As our models become more capable and
> widely used, it's important to define what ideal behavior actually looks like. That's the goal of our
> Model Spec, to give a clearer window into what we're aiming for when we train and evaluate new
> versions of ChatGPT. **But stating our goals isn't enough on its own. They need to be backed by strong
> evals. While we have extensive evals in areas like instruction hierarchy and safety (e.g. privacy,
> disallowed content), we're working to improve our confidence in areas we're not already accounting
> for.**"

Two things this pins down precisely:

1. **OpenAI concedes the spec/instrument gap in its own words.** The Model Spec (see
   `bigtech-openai-model-spec.md`) is 250k chars of normative statement with zero measurement
   procedures. Claude's Constitution is 192k chars with the same property. This sentence is the
   vendor conceding what that costs.
2. **It tells us exactly where lab evals exist: "instruction hierarchy and safety."** Not persona.
   Not character. Not creativity. **This is the direct answer to "does any lab measure steerability
   as a first-class property": they measure *instruction hierarchy* — whose instruction wins — and
   nothing about how far a prompt moves behavior.**

And the confirmation that the *specific* thing the spec forbade had no test:

> "**We also didn't have specific deployment evaluations tracking sycophancy.** While we have research
> workstreams around issues such as mirroring and emotional reliance, those efforts haven't yet become
> part of the deployment process. After this rollback, we're integrating sycophancy evaluations into
> that process."

> "**Our offline evals weren't broad or deep enough to catch sycophantic behavior—something the Model
> Spec explicitly discourages—and our A/B tests didn't have the right signals to show how the model was
> performing on that front with enough detail.**"

## OpenAI's actual deployment review process (verbatim taxonomy)

> "Once we have a model candidate, our models go through a deployment process to check safety, model
> behavior, and helpfulness. Currently, evaluations fall into these categories:
>
> **Offline evaluations:** We have a broad range of evaluation datasets to understand the capability of
> the new model on aspects such as math, coding, and chat performance, **personality**, as well as
> general usefulness. We treat these evaluations as a proxy for how useful our model is for our users.
>
> **Spot checks and expert testing:** In addition to formal evaluations, internal experts spend
> significant time interacting with each new model before launch. **We informally call these "vibe
> checks"—a kind of human sanity check to catch issues that automated evals or A/B tests might miss.**
> The goal is to get a feel for how the model behaves in practice: Does it respond in a way that feels
> helpful, respectful, and aligned with the values we've articulated in the Model Spec? **The people
> doing this work are experienced model designers who've internalized the Model Spec, but there's also
> an element of judgment and taste—trusting how the model feels in real use.**
>
> **Safety evaluations:** We check whether the model meets our safety bar. These blocking evaluations are
> mostly focused on direct harms performed by a malicious user…
>
> **Frontier risk:** For potentially frontier models, we check to see if the release might have the
> ability to cause severe harm along preparedness risks…
>
> **Red teaming:** …
>
> **Small scale A/B tests:** Once we believe a model is potentially a good improvement for our users,
> including running our safety checks, we run an A/B test with a small number of our users. This lets
> us look at how the models perform in the hands of users based on aggregate metrics such as **thumbs up
> / thumbs down feedback, preferences in side by side comparisons, and usage patterns.**"

**Note "personality" is named as an offline eval category** — the only lab claim we found that a
personality eval exists in a deployment pipeline. **No method, dataset, metric, or agreement
statistic is given, anywhere, by anyone.** It is one word in a list.

**Note also "preferences in side by side comparisons"** — OpenAI's online quality signal is
**pairwise**, consistent with BENCHMARKS.md §0.6/Q1 and §5 ("Pairwise or nothing").

## Personality is a shipped product axis

> "Since launching GPT‑4o in ChatGPT last May, we've released **five major updates focused on changes to
> personality and helpfulness.**"

Five personality updates in ~12 months, gated by "judgment and taste."

## Why the review missed it — the qualitative signal was there and was overruled

> "One of the key problems with this launch was that **our offline evaluations—especially those testing
> behavior—generally looked good. Similarly, the A/B tests seemed to indicate that the small number of
> users who tried the model liked it.** While we've had discussions about risks related to sycophancy in
> GPT‑4o for a while, sycophancy wasn't explicitly flagged as part of our internal hands-on testing, as
> some of our expert testers were more concerned about the change in the model's tone and style.
> Nevertheless, **some expert testers had indicated that the model behavior "felt" slightly off.**"

> "We then had a decision to make: **should we withhold deploying this update despite positive
> evaluations and A/B test results, based only on the subjective flags of the expert testers? In the
> end, we decided to launch the model due to the positive signals from the users who tried out the
> model. Unfortunately, this was the wrong call.** … Looking back, the qualitative assessments were
> hinting at something important, and we should've paid closer attention. **They were picking up on a
> blind spot in our other evals and metrics.**"

**This is BENCHMARKS.md §X5's thesis, confirmed by the incident it cites:** *"You cannot detect reward
hacking with the metric being hacked."* The A/B test and the offline evals both approved a regression;
the only signal that dissented was unquantified human taste — and it was overruled *because* it was
unquantified.

## The post-incident commitments (a vendor precedent for our gate design)

> "**Explicitly approve model behavior for each launch, weighing both quantitative and qualitative
> signals:** We'll adjust our safety review process to formally consider behavior issues—such as
> hallucination, deception, reliability, and **personality**—as blocking concerns. **Even if these issues
> aren't perfectly quantifiable today, we commit to blocking launches based on proxy measurements or
> qualitative signals, even when metrics like A/B testing look good.**"

> "**Value spot checks and interactive testing more:** We take to heart the lesson that spot checks and
> interactive testing should be valued more in final decision-making… We're learning from this
> experience that it's equally true for qualities like **model behavior and consistency**, because so many
> people now depend on our models to help in their daily lives."

> "**We need to treat model behavior issues as launch-blocking like we do other safety risks:** … our
> process for reviewing general model behavior has been less robust and formalized relative to areas of
> currently tracked safety risks. **We now understand that personality and other behavioral issues should
> be launch blocking, and we're modifying our processes to reflect that.**"

> "**We need to be critical of metrics that conflict with qualitative testing:** Quantitative signals
> matter, but so do the hard-to-measure ones, and we're working to expand what we evaluate."

> "**Our evals won't catch everything:** We can't predict every issue… But for more subtle or emerging
> issues, like **changes in tone or style**, real-world use helps us spot problems and understand what
> matters most to users. **Sometimes our evals will lag behind what we learn in practice.**"

> "**There's no such thing as a "small" launch** … One of the biggest lessons is fully recognizing how
> people have started to use ChatGPT for **deeply personal advice**—something we didn't see as much even a
> year ago."

## Why this matters to our framework

- **Direct support for ABILITY-MODEL's premise.** The industry's own worst public character failure
  was a failure of *measurement*, not of intent. The Model Spec said "don't be sycophantic." There
  was no test. It shipped.
- **Direct support against the streetlight fallacy (BENCHMARKS.md §0.5).** OpenAI's post-incident
  commitment — *"Even if these issues aren't perfectly quantifiable today, we commit to blocking
  launches based on proxy measurements or qualitative signals"* — is a frontier lab explicitly
  refusing to let unmeasurability become an excuse for omission. That is the same move §0.5 makes.
- **Direct support for the panel-with-dissent design (X5).** Every quantitative instrument approved
  the regression; only the un-quantified signal dissented.
- **A caution for us.** OpenAI had A/B tests *and* offline evals *and* expert review — BENCHMARKS.md's
  three-source cross-validation (§4) in miniature — and still missed it, because none of the three
  had a *sycophancy-specific* probe. **Cross-validation across sources does not substitute for having
  a dimension.** Coverage, not triangulation, was the failure.

## What this document does NOT contain

- ❌ No description of *how* the "personality" offline eval works — no method, no dataset, no metric.
- ❌ No persona/character *portrayal* eval (this is about the assistant's own personality).
- ❌ No steerability measurement in our sense; "instruction hierarchy" is named as the eval area.
- ❌ No numbers of any kind. There is not a single quantitative result in the postmortem.
