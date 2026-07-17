---
title: "\"Yes, and\": Acceptance, Resistance, and Change in Improv, Aikido, and Psychotherapy"
url: https://www.sfxmachine.com/docs/yes,_and.pdf
authors: [Earl Vickers]
year: 2015
type: journal article / interdisciplinary review
accessed: 2026-07-16
topic: narrative-craft
---

# Vickers — "Yes, and": Acceptance, Resistance, and Change

Open-access secondary source that supplies **citable definitions of blocking and accepting** without relying on the non-open *Impro* text. Useful precisely because *Impro* isn't quotable at length.

## Abstract (verbatim)

> "The *yes, and* practice of improvisational theatre ('improv') involves accepting and building on a partner's offer. This practice provides a simple conceptual framework for viewing acceptance, resistance, and change in a variety of disciplines including Aikido and various acceptance-based psychotherapies, including Ericksonian hypnotherapy. Aikido's blending practice and Erickson's utilization principle resemble improv's *yes, and* practice, in that they involve aligning with another person's energy and redirecting it instead of blocking it. Each of these disciplines emphasizes being present in the moment, avoiding struggle, and viewing resistance as a gift; these and other parallels help provide an interdisciplinary validation of the underlying *yes, and* principle. The article explores applying a *yes, and* approach to the processing of negative emotions. It also discusses possible applications of improv training in couples therapy, therapist training, and treatment of chronic negativity and social anxiety disorder."

## THE definition of blocking (verbatim) — the citable one

> "In improv, resistance is termed **blocking**, which means **rejecting an offer**. For example, one performer says, 'Welcome to my home,' and the partner replies by saying, 'No, this is an office building.' **Blocking does not work well in improv; it undermines the reality of the scene, the audience gets confused, and everything grinds to a halt** (Koppett, 2001). Instead of blocking, improv students are encouraged to accept the offer and add to it."

**This is the cleanest published definition available and it decomposes into three checkable consequences:**
1. "undermines the reality of the scene" → an established proposition is now contradicted → **NLI-detectable**
2. "the audience gets confused" → downstream referents become ambiguous
3. "everything grinds to a halt" → **no state advance** → detectable as a stall

The example pair — *"Welcome to my home"* / *"No, this is an office building"* — is a canonical minimal test case. **This should literally be a unit test in our harness.**

## The second sense of "blocking" (verbatim)

> "The term blocking can also refer to the mental process of censoring (resisting or repressing) the first response that comes to mind. Students are encouraged to follow their first instincts instead of resisting and blocking."

⚠️ **Two distinct senses of "blocking" — disambiguate in our spec.** Sense 1 = *rejecting your partner's offer* (interpersonal; what we want to count). Sense 2 = *self-censoring your own impulse* (intrapersonal). Sense 2 is arguably the better description of what RLHF safety-tuning does to a roleplay model — the model censors its own first instinct — but it is **not observable from the transcript**, only its effects are. **Count sense 1; treat sense 2 as an unobservable latent cause.** If we conflate them in a rubric, annotators will diverge.

## Resistance as information — reframe for our refusal analysis

The paper's cross-domain thesis is that in Aikido, Ericksonian therapy, and improv alike, resistance is *data about the other party*, not an obstacle:

> "'...there really is no such thing as "resistance" in a utilization approach. Everything the person is doing is exactly what you would like him to be doing.... "Resistance" is just a message that you need to synchronize yourself with the subject again'" (Gilligan, 1982, p. 92, quoted in Vickers).

> "Resistance may have as much to do with the therapist's inability to connect and blend with the client as it does with the client's unwillingness to change, and may simply signify that 'the therapist is trying to take the client somewhere he or she does not want to go'" (Faggianelli & Lukoff, p. 169, quoted in Vickers).

**→ Directly reframes railroading.** "Trying to take the client somewhere he or she does not want to go" is *exactly* Riedl & Bulitko's **intervention** (see `narrative-riedl-bulitko-interactive-narrative.md`), described from the user's side. When a roleplay model railroads, user "resistance" is the observable signature. **A useful cross-check: high user-resistance rate (user repeatedly re-asserts a blocked offer) is an objective, judge-free correlate of model railroading.** The user's repetition is the measurement instrument. We don't need to judge whether the model blocked — we can watch whether the user had to say it twice.

**This is a genuinely novel measurement idea falling out of this source: user re-assertion rate as a railroading detector.** It requires real user traffic or a competent user-simulator, but it needs no judge at all.

**On acceptance ≠ passivity (verbatim):**
> "Brach clarified, however, that acceptance does not mean resignation, passivity, withdrawal, or self-indulgence..."

**→ The "and" is the whole game.** This sentence is the theoretical justification for scoring *accept* and *build* as two separate events. Accepting without building is precisely what Brach warns acceptance is not — and it is what our models do. **Cite this when someone argues "the model agreed with the user, so it accepted the offer, so it's fine."**

## Validation

⚠️ **No empirical validation of any measure.** This is a conceptual/interdisciplinary review. It contains **no metrics, no rubrics, no human studies, no agreement statistics**. Its value is purely definitional: it is an open-access, citable source for the offer/blocking/accepting vocabulary, and it supplies the reframing of resistance that yields the user-re-assertion idea.

Do not cite this as evidence that "yes-and" improves outcomes — the paper's "interdisciplinary validation" is argument-by-analogy across improv/Aikido/therapy, not measurement. **The analogy is suggestive, not evidentiary.**

## Takeaways for the platform

1. **Citable open-access definition of blocking** = "rejecting an offer", with a canonical minimal example to use as a unit test.
2. **Disambiguate the two senses of blocking** in our spec (reject-partner's-offer vs self-censor). Only the first is observable.
3. **User re-assertion rate as a judge-free railroading detector** — the strongest original idea from this source.
4. **"Acceptance does not mean passivity"** — theoretical grounding for splitting accept from build.
5. No validation here; the improv→outcome link is analogical only.
