---
title: "Information Integration Theory — Anderson's weighted-averaging model, and the 60-year Asch-vs-Anderson debate on whether trait impressions compose linearly"
url: https://en.wikipedia.org/wiki/Information_integration_theory
authors: Norman H. Anderson (theory); Julius Wishner (1960 reanalysis)
year: 1962-1981
type: theory / review
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Anderson's Information Integration Theory (IIT) — the algebraic rival to Asch

**Why this file exists:** our framework's steerability matrix implicitly assumes a *linear* composition model — perturb trait i, measure the leak into trait j, treat leakage as error. Asch says that's wrong (`psych-asch-impression-formation.md`). But Asch is not the last word: Norman Anderson spent 30 years arguing that trait impressions *do* compose algebraically, and that Asch's configural effects are explainable without gestalts. **This is literally a 60-year-old, unresolved debate about the exact question our metric presupposes an answer to.** We do not get to assume linearity by default; the field never settled it.

## The core formalism — the weighted-averaging model

Anderson's IIT decomposes judgment into three functions: **valuation** (each stimulus gets a scale value), **integration** (values combine by an algebraic rule), and **response production** (mapping the internal judgment to an overt response).

Each stimulus *i* carries two parameters:
- **s_i** — the *scale value*: where the stimulus falls on the judgment dimension
- **w_i** — the *weight*: its relevance/importance

The **averaging model**:

```
R = Σ(w_i · s_i) / Σ(w_i)
```

The **weighted average with initial impression** — the form that actually does the theoretical work:

```
        w₀·s₀ + Σᵢ wᵢ·sᵢ
R  =  ─────────────────────
          w₀ + Σᵢ wᵢ
```

where `w₀, s₀` are the weight and scale value of the **initial impression** — the prior the judge brings before seeing any trait. Note the property Anderson exploits: *the relative influence of the initial impression shrinks as cues accumulate*, because w₀ is fixed while Σwᵢ grows. This is a built-in, parameter-free account of why early information gets diluted.

Contrast the **adding model**:

```
R = Σ(w_i · s_i)
```

**The discriminating prediction.** Adding and averaging differ on what happens when you append *mildly positive* information to an *extremely positive* set:

- **Adding** predicts the impression gets *more* positive (you added a positive term).
- **Averaging** predicts the impression gets *less* positive (you pulled the mean down).

> "The averaging hypothesis of information integration was tested in two experimental tasks. Both supported the averaging hypothesis and infirmed the adding hypothesis. This means that moderately positive information can weaken an impression formed by very positive information."

Averaging won that test. This is a genuinely counterintuitive, well-replicated result, and it is **directly relevant to character sheets**: *adding a mildly-in-character detail to a strongly-drawn character can make the character read as weaker.* More sheet is not monotonically better sheet.

Related: the **set-size effect** — impressions grow more extreme (and more confident) as more same-valence traits are added, which pure averaging with constant weights does not predict but *weighted* averaging with w₀ does (each new cue further discounts the neutral initial impression).

## How Anderson explains away Asch's central-trait effect

Asch says "warm"→"cold" *transforms the meaning* of the surrounding traits (meaning-change). Anderson's counter is **meaning-constancy**: the scale values s_i don't change; what changes is the **weights** w_i, and/or the effect is an artifact of the response scale and of which check-list items happen to correlate with warmth. No gestalt required — just a differential-weight averaging model.

This is the "differential weighted averaging model of impression formation" line of work (e.g. *JESP* 1973). The debate is therefore **not** "does context matter?" (both sides agree it does) but "**is the contextual effect a change in the meaning of the trait (Asch) or a change in its weight in an algebraic rule (Anderson)?**"

## Wishner (1960) — the reanalysis that damaged Asch

Julius Wishner, "Reanalysis of 'impressions of personality'", *Psychological Review*, 67, 96–112.

Wishner's move: he collected the **correlational structure** among the trait dimensions in Asch's check list, and showed that **which traits "warm/cold" transforms is predicted by how strongly those check-list traits correlate with warm/cold in the first place.** Centrality, on this account, is not a mysterious gestalt property — it's just: a stimulus trait shifts exactly those response traits it is empirically correlated with, by roughly the amount of the correlation.

That is devastating in a specific way: **it makes Asch's "central trait" a relational/statistical fact about the trait-inference network, not a structural fact about persons.** It also explains Asch's *selective* crosstalk (warm→generous huge, warm→honest ~zero) without gestalts — honest just isn't much correlated with warm.

The standard summary of the outcome:

> "The Gestalt-view on impression formation has slowly but surely gone out of fashion (partly because there were more simple explanations for Asch's 1946 data, e.g., Anderson, 1981; Rosenberg, Nelson, & Vivekananthan, 1968; Wishner, 1960), though some of its premises have resonated in typological models of impression formation."

## Who "won"? — current status

**Nobody, cleanly.** The honest verdict:

- **Anderson won on tractability and on the theory's home turf.** Cognitive algebra produced quantitative, falsifiable models that fit a lot of data across domains (impression formation, size-weight illusion, attitude change). "Gestalt" as an explanatory primitive lost favour because it didn't generate point predictions.
- **Asch's phenomena survived.** The central-trait effect, primacy, and contextual centrality all replicate. What lost was the *interpretation*, not the data.
- **No single algebra is universally right:**

> "Research has shown that neither simple summation nor simple averaging is an exclusively valid combinatory principle — which rule applies depends partly on situational factors."

- The field's current shape:

> "Rather than a clear winner, the field has evolved with a continuing debate between proponents of contextualism who argue that impressions result from situationally specific influences (e.g., from semantics and nonverbal communication as well as affective factors), and modelers who follow the pragmatic maxim, seeking approximations revealing core mental processes."

So: **the linear/algebraic camp did not prove impressions are linear. It proved that a weighted-average with free weights can fit the data — which is a much weaker claim, and one with a serious identifiability problem** (see below).

## The identifiability trap — this is the part that should worry us most

Anderson's model has, for each stimulus, **two free parameters (w_i, s_i)**, plus an initial impression (w₀, s₀). Asch's meaning-change and Anderson's weight-change are, in the general case, **mutually substitutable explanations for the same data**: you can absorb a "meaning change" of trait j into a "weight change" on trait j, and vice versa. Anderson's program handles this with careful functional-measurement designs (factorial stimulus sets, testing for parallelism in the data) precisely because the parameters are not identified from a single condition.

**Our steerability matrix has exactly this pathology and no such design.** If we measure "perturb trait i → trait j moved by δ," we cannot tell whether:
- (a) the model changed the *scale value* it assigns to trait j (Asch: the meaning of j changed),
- (b) the model changed the *weight* on trait j (Anderson: j matters less now), or
- (c) the model's *initial impression* term (w₀s₀ — its prior / persona default) dominated and the sheet barely mattered.

These have completely different engineering implications, and **δ alone does not distinguish them.** Anderson's answer — factorial designs with parallelism tests — is a concrete methodology we could adopt.

## Implications for our framework

1. **We cannot assume linear composition — the field spent 60 years failing to establish it.** Our steerability matrix treats off-diagonal crosstalk as defect, which is only coherent under Anderson's *meaning-constancy* assumption plus independent weights. That assumption is one contested side of a live debate, not settled background. At minimum, state it as an explicit modelling assumption in the spec rather than smuggling it in via the metric's shape.

2. **Wishner gives us a cheap, decisive baseline — and possibly a reframe of the whole matrix.** If crosstalk M[i,j] is largely predicted by the *semantic/empirical correlation* between traits i and j, then our matrix's off-diagonal is mostly **redundant with a trait-correlation matrix we can compute from embeddings or from human norms.** Concrete test: compute corr(M[i,j], semantic_similarity(i,j)) across pairs. If it's high, the matrix is measuring the trait ontology, not the model — and "crosstalk" is close to unfixable *by construction*, because it lives in the language, not the model. This is a ~1-day experiment that could invalidate or rescue the metric.

3. **The averaging result is a direct, actionable warning about sheet length.** "Moderately positive information can weaken an impression formed by very positive information." Translated: appending mildly-characteristic detail to a sharply-drawn sheet can *dilute* the character. Our authoring guidance and any "sheet completeness" score should not assume monotonicity. Testable on our stack: hold a strong sheet fixed, append neutral-but-consistent traits, measure whether in-character ratings *decline*. Averaging predicts yes; adding predicts no. **This is a clean, publishable experiment and nobody has run it on LLMs.**

4. **w₀s₀ is the model's persona prior — and we have no term for it.** Anderson's initial-impression term is exactly "what the model thinks the character is like before reading the sheet." A high w₀ means the sheet gets diluted by the base persona. This predicts that **steerability should increase with sheet length** (Σwᵢ grows, w₀ fixed) — a specific, falsifiable prediction our steerability harness could test immediately, and a candidate *explanation* for cross-model steerability differences that has nothing to do with instruction-following per se.

5. **Adopt functional-measurement design, not one-at-a-time perturbation.** Anderson's methodological legacy is that you cannot identify weights and values from single-factor perturbations — you need factorial stimulus sets and you test for **parallelism** in the response surface. Our current "perturb trait i, read off trait j" is the exact design Anderson showed to be uninterpretable. If we want a defensible steerability construct, perturb traits **factorially** and test whether the surface is additive (parallel lines → adding/averaging holds) or shows crossover (→ configural). **That test — parallelism vs. crossover on a factorial character-sheet design — would be the single most rigorous thing in our framework**, and it directly answers "can authors compose traits?" as an empirical question rather than an assumption.
