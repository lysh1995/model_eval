---
title: "Evaluating Human-AI Safety: A Framework for Measuring Harmful Capability Uplift"
url: "https://arxiv.org/abs/2603.26676"
authors: "Michelle Vaccaro, Jaeyoon Song, Abdullah Almaatouq, Michiel A. Bakker"
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Evaluating Human-AI Safety: Measuring Harmful Capability Uplift

arXiv 2603.26676. Submitted 2026-03-06.

## Summary

Argues AI safety evaluation should be **human-centered** and organized around a single metric:
marginal uplift. Roots the metric in social science literature, gives methodological guidance,
and closes with recommendations for developers, researchers, funders, regulators.

## The definition (verbatim)

Harmful capability uplift is:

> "the marginal increase in a user's ability to cause harm with a frontier model beyond what
> conventional tools already enable"

The related framing, as commonly stated across lab policies (see also Claude's constitution,
OpenAI preparedness): the marginal advantage a determined user gains from the model **relative
to open-source documents, search engines, and commodity software already available**. OpenAI's
version tracks whether models "provide meaningful counterfactual assistance"; Anthropic's
pledges to identify whether models "significantly help" individuals deploy CBRN weapons.

## Key numbers

None extracted — this is a framework/position paper, not an empirical benchmark. The abstract
does not contain effect sizes, and I did not extract the methodology section. Do not cite
numbers from this paper.

## Relevance to a roleplay/companion eval product

This gives us the **principled formulation of the in-fiction vs. real-harm line**, and it is
the load-bearing idea for our whole safety design:

> Harm is measured by **counterfactual real-world uplift**, not by depicted content.

Consequences, stated plainly:

- A character describing a murder confers **zero** marginal uplift. Every crime novel ever
  written already does this. Search does this. It is not a safety event and scoring it as one is
  a category error.
- A character reciting a **working synthesis route** confers the *same* uplift as the assistant
  reciting it. The fictional wrapper does not degrade a recipe. This is why the carve-out keys
  on actionability, not on framing.
- The test is therefore mechanical and, importantly, **judgeable**: *strip the fiction. Does
  what remains help someone do something harmful they couldn't already do?* If yes → harm,
  regardless of frame. If no → in-fiction, and refusing is a product defect.

This is the cleanest available answer to the brief's central question, and it is not our
invention — it is the shared standard across Anthropic's constitution, OpenAI's preparedness
framing, and this paper's social-science-grounded version. That makes it defensible to a
regulator, an insurer, and a jury, which matters given Garcia/Raine.

## Critical limits — where uplift is the WRONG frame

Uplift is a **capability** metric, built for CBRN/cyber. It does not extend to the harms that
actually killed people in the companion cases, and pretending otherwise would be dangerous:

- **Self-harm.** A suicidal teen needs no "uplift." The method is not the scarce resource.
  Encouragement, validation, and a companion that says "don't tell your parents" are the harm.
  Marginal-uplift scoring rates this ~0 and would wave it straight through.
- **Emotional dependency / manipulation.** No capability transfer at all.
- **Sycophancy.** Same.
- **Minors + sexual content.** Legally prohibited regardless of uplift, frame, or fiction (SB
  243).

So: **uplift governs the fiction carve-out for capability harms only.** The psychosocial harms
need an entirely separate scoring axis keyed on the *user's state and the model's stance toward
it*, not on information transfer. Any design that runs everything through one uplift-shaped
funnel reproduces exactly the failure alleged in Raine.
