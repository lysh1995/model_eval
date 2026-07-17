---
title: "Aptitude-Treatment Interaction — Cronbach's two disciplines (1957), the 'hall of mirrors' retraction (1975), and Cronbach & Snow (1977)"
url: https://gwern.net/doc/psychology/personality/1975-cronbach.pdf
authors: Lee J. Cronbach; Richard E. Snow
year: 1957-1977
type: theory / review
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Cronbach: "The Two Disciplines of Scientific Psychology" (1957) → "Beyond the Two Disciplines" (1975) → Cronbach & Snow (1977)

**Why this is the most dangerous file in the psychology cross-check.** Our "steerability" construct is an **aptitude × treatment interaction**: aptitude = the model, treatment = the prompt perturbation, outcome = behaviour change. Cronbach founded that research program in 1957, spent 18 years and a 600-page book on it with Snow, and then **publicly recanted** — not because ATIs don't exist, but because he concluded they cannot be pinned down. His retraction is the single best-articulated statement of the failure mode our metric is walking into. Coming from the man who invented coefficient alpha and construct validity, it is not a fringe complaint.

## 1957 — "The Two Disciplines of Scientific Psychology"

Cronbach's APA presidential address. The famous diagnosis: psychology has split into two non-communicating methodological cultures.

- **Experimental psychology** — manipulates treatments, treats individual differences as **error variance** to be minimized/averaged away.
- **Correlational psychology** — measures individual differences, treats treatment variation as nuisance.

Cronbach's proposal was to **unify them via the interaction**: the payoff science is one that finds which treatment works best for which kind of person. That is Aptitude-Treatment Interaction (ATI). The whole point is that the interaction term is the scientifically interesting quantity, not the noise.

**This is our framework's exact bet.** "Which prompt formulation moves which model how much" is an ATI. Our steerability matrix is Cronbach's 1957 program applied to LLMs.

## 1977 — Cronbach & Snow, *Aptitudes and Instructional Methods*

The 18-year empirical payoff: a massive handbook-scale review of the ATI literature (Irvington, ~600pp). Verdict, in short: ATIs are **real but unstable**. Individual studies find them; the findings do not aggregate into dependable rules. Snow continued to argue ATIs were genuine and important; Cronbach drew the more pessimistic methodological conclusion below.

## 1975 — "Beyond the Two Disciplines of Scientific Psychology", *American Psychologist*, 30(2), 116–127

### THE quote — the hall of mirrors (p. 119)

Full context, verbatim:

> "When ATIs are present, a general statement about a treatment effect is misleading because the effect will come or go depending on the kind of person treated. When ATIs are present, a generalization about aptitude is an uncertain basis for prediction because the regression slope will depend on the treatment chosen. Having said this much in 1957, I was shortsighted not to apply the same argument to interaction effects themselves. An ATI result can be taken as a general conclusion only if it is not in turn moderated by further variables. If Aptitude × Treatment × Sex interact, for example, then the Aptitude × Treatment effect does not tell the story. **Once we attend to interactions, we enter a hall of mirrors that extends to infinity. However far we carry our analysis — to third order or fifth order or any other — untested interactions of a still higher order can be envisioned.**"

Read the structure of the argument carefully, because it applies to us with **zero modification**:

1. A main effect is misleading if there's a 2-way interaction. → *"prompt X works" is misleading if it depends on the model.*
2. A 2-way interaction is misleading if there's a 3-way interaction. → *"model M is steerable by prompt X" is misleading if it depends on the character.*
3. There is no level at which this terminates.

Our framework already **admits step 3 is live** — the worry that "chemistry is a user×character×model interaction" *is* a third-order interaction. Cronbach's point is that conceding that concedes the regress: there is then no principled reason to stop at three.

### Cronbach anticipates our rebuttal — and pre-empts it with data

He then does something better than assert. He takes the objection head on:

> "When I say something like that, some colleague is likely to reply: 'In my experience, interaction effects are not large.' To check that out, let us look at the magnitude of various effects in one ecology."

He surveys **the last four volumes of the *Journal of Personality and Social Psychology*** — 17 studies with the same A × B × C design — and tabulates standardized variance components (his Table 2, p. 120) for largest main effect, second-largest, smallest, first-order interactions, and second-order interactions. The finding: **interaction components are routinely comparable in magnitude to main effects.** In his tabulation, ~19% of first-order and ~12% of second-order interaction components exceeded a standardized variance component of 1.00 — i.e. the higher-order terms are *not* negligible dregs.

**The "interactions are small so we can ignore them" defence was empirically checked and rejected in 1975.** If we plan to make that argument for our steerability matrix, we should expect to have to beat this table.

### The generalizations-decay argument (pp. 122–123)

The second blade, and arguably the more relevant one for a field with a 6-month model cycle:

> "**Generalizations decay.** At one time a conclusion describes the existing situation well, at a later time it accounts for rather little variance, and ultimately it is valid only as history. **The half-life of an empirical proposition may be great or small. The more open a system, the shorter the half-life of relations within it are likely to be.**"

> "Propositions describing atoms and electrons have a long half-life, and the physical theorist can regard the processes in his world as steady. Rarely is a social or behavioral phenomenon isolated enough to have this steady-process property. Hence the explanations we live by will perhaps always remain partial, and distant from real events, and rather short lived."

> "The atheoretical regularities of the actuary are even more time bound. **An actuarial table describing human affairs changes from science into history before it can be set in type.**"

His examples of decay: the California F Scale going obsolescent ("The 25-year-old research supporting its construct validity gives us little warrant for interpreting scores today because with new times the items carry new implications"); Bronfenbrenner's finding that 1950s social-class parenting differences were "sometimes just the reverse of what had been observed in 1930."

And the structural conclusion — the one that most directly threatens a benchmark-building program:

> "The trouble, as I see it, is that **we cannot store up generalizations and constructs for ultimate assembly into a network.**"

He explicitly revisits his own construct-validity framework (Cronbach & Meehl 1955) in this light:

> "Because Meehl and I were importing into psychology a rationale developed out of physical science, we spoke as if a fixed reality is to be accounted for."

**An LLM eval ecosystem is about as open a system as exists.** Models are retrained; prompts leak into training data; the "aptitude" being measured is itself a moving artifact. By Cronbach's own criterion, the half-life of a steerability coefficient is *short* — plausibly shorter than the time to publish it.

### What Cronbach recommends instead (pp. 123–125)

Not nihilism. A reversal of priorities:

> "In the investigation of complex practical and social phenomena, I am sure we will continue to employ manipulative experiments and to test hypotheses stated in advance about the fixed conditions… But I believe that in past research the psychologist has been too willing to stop as soon as he has calculated the statistics stating the strength of the relationships he specified a priori."

> "The experimenter or the correlational researcher can and should **look within his data for local effects arising from uncontrolled conditions and intermediate responses**. He can do so, of course, only if he collected adequate protocols from the start."

> "**Instead of making generalization the ruling consideration in our research, I suggest that we reverse our priorities.** An observer collecting data in one particular situation is in a position to appraise a practice or proposition in that setting, **observing effects in context**. In trying to describe and account for what happened, he will give attention to whatever variables were controlled, but he will give equally careful attention to uncontrolled conditions, to personal characteristics, and to events that occurred during treatment and measurement."

Cronbach's positive program: **intensive local description with full protocols retained**, generalization as a modest secondary hope rather than the goal.

## Implications for our framework

1. **Our steerability score is an ATI, and Cronbach's regress applies verbatim.** "Δbehaviour per unit Δprompt" is only a stable number if it is not moderated by character, by scenario, by user, or by model version. We already suspect it's moderated by at least character and user ("chemistry is a user×character×model interaction"). Cronbach's argument is that once you concede one moderator you have conceded the regress — there is no principled stopping rule, and "we tested up to 3-way" is not a defence, it's an arbitrary truncation.

2. **The "interactions are small" escape hatch is empirically closed.** If we want to publish a single steerability number per model, we owe an argument that the character×prompt and user×prompt interaction variance components are small. Cronbach checked exactly this claim in a comparable literature and found interaction components rivalling main effects. **Do the variance decomposition before publishing the scalar.** If the model main effect doesn't dominate, the scalar is a fiction. This is a concrete, cheap gate: run the factorial, report the variance components table, and let it decide whether a scalar is licensed.

3. **Generalization decay sets an expiry date on the whole benchmark.** "The more open a system, the shorter the half-life." A steerability coefficient measured on model version N is a statement about version N in the prompt-ecology of month M. Cronbach's actuarial-table line — it "changes from science into history before it can be set in type" — is a fair description of LLM benchmarks. **Practical consequence: version and date every coefficient, treat the measurement harness (not the numbers) as the durable artifact, and never let a steerability number be cited without its model+date stamp.**

4. **Cronbach's positive program is a better fit for us than his pessimism suggests — and we have an advantage he didn't.** "Look within his data for local effects… only if he collected adequate protocols from the start." We can retain *complete* protocols: every prompt, every completion, every intermediate. Cronbach's constraint was that intensive local observation doesn't scale; **ours scales trivially and costs nothing to retain.** The correct response to the hall of mirrors is not to abandon steerability but to (a) stop pretending it's a scalar, (b) keep full protocols so higher-order effects are *discoverable post hoc* rather than needing pre-specification, and (c) report it as a conditional, contextualized profile.

5. **The honest framing to write into the spec.** Cronbach did not show ATIs are absent — he showed they are real, large, and **non-generalizable**. So the defensible claim is *not* "model M has steerability 0.6." It is "under this character set, these perturbations, this scenario distribution, and this model version, the observed steerability profile is X, and here is the variance attributable to each interaction." That is weaker than what the framework currently promises, and it is the strongest claim the last 70 years of this exact research program supports.

6. **Counterweight, for balance.** Snow (Cronbach's co-author) never accepted the pessimistic reading and continued to defend ATI as a real and useful construct; the 1975 paper is Cronbach's view, not a field consensus. And Cronbach's target was *education research* — a system with far more uncontrolled variance (teachers, schools, cohorts, decades) than a fixed-seed LLM eval harness. Our system is more closed than his: we control the treatment exactly, the "aptitude" is inspectable, and we can rerun the entire design in an afternoon. **The regress is real but our stopping rule can be empirical rather than arbitrary — we can actually measure the third- and fourth-order terms he could only envision.** That is a genuine reason for measured optimism, and it should be argued explicitly in the spec rather than assumed.
