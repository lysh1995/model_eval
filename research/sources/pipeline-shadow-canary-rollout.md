---
title: "Releasing AI Features Without Breaking Production: Shadow Mode, Canary Deployments, and A/B Testing for LLMs"
url: https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing
org: TianPan.co
year: 2026
type: engineering-blog
accessed: 2026-07-16
topic: eval-lifecycle
---

# Shadow / canary / A-B for LLM changes

Corroborating: https://futureagi.com/blog/llm-eval-shadow-traffic-canary-2026/,
https://tianpan.co/blog/2026-04-17-prompt-canaries-deployment-llm-production,
https://appscale.blog/en/blog/ai-native-cicd-for-llm-features-eval-gates-prompt-diff-canary-rollouts-2026

## Why LLM deploys differ from code deploys (three reasons, verbatim)

1. **Irreducible non-determinism** — "Research has documented accuracy variations of up to
   **15% across runs with identical inputs**" due to GPU floating-point arithmetic
   variability
2. **Large blast radii from small changes** — prompt rewording or model version bumps create
   qualitatively different behaviors not captured in benchmarks
3. **Delayed feedback** — bad outputs surface through complaints or downstream failures
   hours/days later, unlike immediate crashes

> **All three are arguments our own notes already make quantitatively.** (1) is note 10's
> noise floor (σ_within=0.0847 on repetition; 19.4pp resolvable at n=3). (3) is note 06's
> 2.1-day detection latency. **The industry states as folklore what we have measured.** Our
> advantage is that we can put an MDE on the gate instead of a vibe.
>
> ⚠️ But (1)'s "15% across identical inputs" is a *generic* claim about GPU nondeterminism
> and should not be quoted as if it were our number — ours is measured and dimension-specific.

## Shadow mode — mechanics

> "duplicate production requests to both the current model (which serves users) and the
> candidate model (which doesn't)"

- Background process sends identical requests to candidate; results never shown to users
- Requires an **evaluation layer** with automated comparison (LLM judge)
- **Alternative: replay historical production traffic** through the candidate before deploy
- **Cost: "roughly doubles inference spending during evaluation"**

> **The cost line is the design constraint.** At 50M generations/day, shadowing 100% of
> traffic doubles the *production inference bill* — not the eval bill. That dwarfs the
> entire $283k/yr eval budget in note 06 and is obviously not happening.
>
> **Shadow must itself be sampled**, and the sampling unit is again the **session** (note
> 06 §2) — a shadow of generation #47 without #1–46 tells us nothing about persona drift,
> and worse, the candidate would need the *candidate's own* conversation history to be
> evaluated fairly.
>
> ⚠️ **This is the deep problem with shadowing a companion model, and it deserves to be
> stated plainly: you cannot shadow a multi-turn conversation.** The shadow candidate's
> turn-2 reply is conditioned on the *incumbent's* turn-1 reply, not its own. By turn 3 the
> shadow is being evaluated on a conversation it would never have produced. **Shadow mode
> is only sound for the first turn of a session, or for single-turn tasks.** Beyond that it
> measures counterfactual-conditioned behavior, which is not what ships.
>
> This is exactly note 11 §7's FED finding in a new guise (turn-level ranking *flips*
> vs dialogue-level) and note 08's covariate-shift/exposure-bias sources: **a model
> evaluated on someone else's trajectory is being measured off-policy.** Replay of
> historical traffic has the identical flaw.
>
> → **Implication: shadow is a smoke test (does it crash, refuse, blow up latency/cost/
> length), not a quality gate. Quality on multi-turn requires either self-play (offline,
> on-policy, no users) or a real canary (online, on-policy, real users).** There is no
> third option that is both user-safe and on-policy. Our benchmark's 102-turn self-play
> dialogues are the on-policy substitute, and that's why the pre-launch benchmark carries
> more weight in our design than shadowing does.

## Canary — stages

Start **1%** (or as low as **0.1%** for high-stakes), then **5% → 20% → 50% → 100%**,
gated on metric validation at each step.

**Critical requirement:** "Maintain **consistent user assignment** so users experience
coherent behavior within sessions rather than random model switching per request."

> **Sticky assignment is not a nicety for us — it is correctness.** Randomizing per request
> inside a roleplay session means the persona changes mid-conversation. The assignment key
> must be `session_id` (or user_id), hashed deterministically — the same trace-level
> all-or-nothing hash as note 06 §1's sampler. **One hash function, three consumers:
> eval sampling, shadow selection, canary assignment.**

## Metrics gating each canary stage

- **Latency percentiles** (p50, p95, p99) — "distribution shape over averages"
- **Cost per request** — token count variations
- **Error and refusal rates**
- **Output length distribution** — "detecting mode collapse or excessive verbosity"
- **User feedback signals** — thumbs-down, regeneration requests, **session abandonment**,
  measured as **cohort rates**

> **Every one of these is a note 06 Tier-1 cheap signal. Not one is a judge score.** The
> published canary gate is entirely deterministic — which is consistent with note 06's
> claim that "most regressions will be caught here first," and with RLUF's finding that
> the *cheap side-channel* ("bye" rate) caught the reward hack.
>
> **Output length distribution** is doing double duty here: it is both a canary gate and
> the #1 confound in our measurement (note 11 §2: length coefficient 0.249, ~8x any
> formatting term; our corpus spans 40→3,783 chars/turn). A canary that trips on length is
> telling us something real about the variant *and* about every judge score we're about to
> compute for it.

## Auto-rollback (verbatim)

> "Set explicit thresholds — if **p99 latency increases by more than 40%**, if the
> **refusal rate jumps by more than 5%**, if the **cost-per-request delta exceeds your
> budget** — and have the canary controller route **100% back to baseline without
> requiring human intervention**."

> Reasonable defaults, but note they are all **fast, unambiguous, deterministic** signals.
> **Nobody auto-rollbacks on a judge score, and we shouldn't either** — a 12% FP-rate
> instrument (note 06 §1) wired to an automatic production rollback is an outage generator.
> Judge scores inform a *human* ship decision on a slower clock; cheap signals drive the
> automation.

## Canary vs A/B — the distinction (verbatim)

> "**Canary deployment tells you whether the new model is safe to deploy. A/B testing tells
> you whether it's better.**"

> Adopt this framing verbatim — it resolves an ambiguity that would otherwise muddle our
> lifecycle. They are **different questions, different statistics, different durations, and
> different exit criteria**:
> - canary = **safety/regression**, deterministic signals, minutes–hours, auto-rollback
> - A/B = **superiority**, sequential/anytime-valid inference (note 06 §5 e-values, since
>   a dashboard is a continuously-monitored test), days–weeks, human ship call
>
> Conflating them is how the OpenAI April 2025 sycophancy rollback happened (note 11 open
> question #4): A/B tests approved the model, expert testers dissented and were overruled.
> **A/B answers "better on the metric," not "safe" and not "good."**

## The five-gate pipeline (from the AppScale corroborating source)

> lint → offline eval → cost budget → shadow eval on production traces → canary with
> auto-rollback
