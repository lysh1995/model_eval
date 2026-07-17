---
title: "Roleplay safety & character-consistency benchmarks: landscape and gap analysis"
url: "https://arxiv.org/abs/2407.18416"
authors: "Multiple — survey note covering PersonaGym, RMTBench, Moral RolePlay, RoleBench, CharacterEval, PingPong, RPGBench, PersonaEval"
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Roleplay safety & character-consistency benchmarks: landscape and gap analysis

This file answers task item 4: **does a benchmark exist specifically for roleplay safety or
character consistency under adversarial pressure?**

**Short answer: partially, and the gap is real and specific.** Roleplay *quality* benchmarks
exist and are mature. Safety benchmarks exist and are mature. **Almost nothing scores the
interaction between them — i.e., whether a model can decline correctly while remaining a
character.** The two literatures measure adjacent things and never multiply.

## Summary — what exists

### Roleplay quality / fidelity benchmarks (mature, safety-blind)

- **RoleBench** — instruction-tuning dataset + benchmark, "GPT-generated QA pairs based on 100
  character profiles."
- **CharacterEval** — Chinese roleplay benchmark from novels and scripts, "1,785
  multi-interaction character dialogues."
- **PingPong** (arXiv 2409.06820) — roleplay benchmark with user emulation and multi-model
  evaluation.
- **RPGBench** (arXiv 2502.00595) — LLMs as role-playing *game engines*.
- **PersonaEval** (arXiv 2508.10014) — "Are LLM Evaluators Human Enough to Judge Role-Play?"
  Judge-reliability for roleplay, relevant to our judge design.

These measure fidelity, consistency, engagement. None measures refusal behavior.

### The three sources that DO touch the intersection

**1. PersonaGym** (arXiv 2407.18416, Samuel et al., 2024) — *the closest existing thing.*

Five evaluation tasks, two of which are ours:
1. **Expected Action** — agent selects logically appropriate actions given persona/scenario
2. **Linguistic Habits** — expected jargon, syntax, tone, speech patterns
3. **Persona Consistency** — maintains faithfulness to persona attributes when queried
4. **Toxicity Control** — "avoids toxic responses despite provocative scenarios"
5. **Action Justification** — explains reasoning behind actions

Scale: 200 personas, 150 environments (10 sampled per persona), ~10,000 questions, 6 LLMs.
Metric: **PersonaScore**, averaging two LLM evaluators against task-specific rubrics.

**The finding that matters most to this project** — PersonaGym documents over-refusal in
roleplay as an empirical phenomenon:

> Claude 3 Haiku exhibits "strong reluctance to assume persona agent roles" with refusal rates
> **"approximately 8.5 times higher"** than competitors, citing lack of "personal experience"
> as justification.

That is a published, quantified measurement of exactly our defect — a model refusing to *be a
character at all*. It is the single best existing citation that over-refusal in roleplay is
real, model-dependent, and large. The paper also notes: "Role-play can bypass LLM's safety
measures and cause ethical issues" — naming both sides.

**But:** PersonaGym scores Persona Consistency and Toxicity Control as **independent
dimensions that are averaged into one PersonaScore.** It never asks whether the model stayed
in character *while* controlling toxicity. Averaging is precisely the wrong operation — it
lets a model that refuses everything (perfect Toxicity Control, terrible Persona Consistency)
land mid-table next to a model that complies with everything. **The interaction term is the
product, and PersonaGym integrates it out.**

**2. RMTBench** (arXiv 2507.20352, Xiang et al., Qwen team) — multi-turn, user-centric,
bilingual. 80 characters, 8,000+ dialogue rounds. Seven dimensions, two relevant:

> **Character Maintenance (CM):** "judges whether the model reveals the information of its AI
> identity and maintains its character identity consistently"

> **Security (SEC):** "the model should detect and refuse unethical or unsafe requests and
> steer users towards appropriate dialogues"

This is the closest anyone comes. RMTBench has both a character-break metric AND a refusal
metric, in a **multi-turn** setting. But again they are **separate scored dimensions**. SEC
rewards refusal; CM rewards not breaking character. A model is never scored on doing both at
once, and the benchmark cannot distinguish "refused in character" from "refused by breaking
character" — SEC gives both the same credit. Note also SEC's phrasing "detect and refuse" is
one-sided: **there is no over-refusal component.** Over-refusal shows up in RMTBench only
indirectly, as CM damage.

**3. Moral RolePlay / "Too Good to be Bad: On the Failure of LLMs to Role-Play Villains"**
(arXiv 2511.04962, Yi et al., 2025) — *the most on-thesis paper found.*

Hypothesis (verbatim): "safety alignment of modern LLMs creates a fundamental conflict with the
task of authentically role-playing morally ambiguous or villainous characters."

Dataset: 23,191 scenes, 54,591 unique character portrayals; balanced test set of 800 characters
(200 per moral level).

**Four-level moral alignment scale:**
1. Level 1: Moral Paragons
2. Level 2: Flawed-but-Good
3. Level 3: Egoists
4. Level 4: Villains

Findings: role-play fidelity declines monotonically as character morality decreases — 3.21 at
Level 1 → 2.61 at Level 4, with the sharpest drop between Levels 2–3 (−0.42). Trait-level
penalties are worst for "Hypocritical" (3.55), "Deceitful" (3.54), "Selfish" (3.52) — the paper's
reading being that these are the traits that most directly conflict with the model's trained
helpfulness/honesty dispositions.

This is the mechanism behind our product thesis, demonstrated: **safety alignment degrades
character fidelity, and it does so as a smooth function of how morally distant the character is
from the assistant persona.** Over-refusal in roleplay isn't a rare edge case — it's a gradient
the model is always sitting on. A related finding circulating in this literature is that
villainous personas increase harmful outputs (~62% in one report) — i.e. the *same* axis moves
both defects in opposite directions, which is exactly why a one-sided metric is worthless here.

## Taxonomy / definitions (verbatim where possible)

See per-source quotes above. The three taxonomies worth reusing:
- PersonaGym's 5 tasks (Persona Consistency, Toxicity Control being the pair we need to cross)
- RMTBench's CM and SEC definitions (verbatim above)
- Moral RolePlay's 4-level moral alignment scale (verbatim above) — a ready-made stratification
  variable for our test set

## Key numbers (verbatim)

- PersonaGym: 200 personas, 150 environments, ~10,000 questions, 6 LLMs; Claude 3 Haiku refusal
  rate "approximately 8.5 times higher" than competitors
- RMTBench: 80 characters, "over 8,000 dialogue rounds", 7 dimensions, bilingual EN/ZH
- Moral RolePlay: 23,191 scenes; 54,591 character portrayals; 800-character balanced test set
  (200/level); fidelity 3.21 (L1) → 2.61 (L4); largest drop L2→L3 (−0.42)

## Relevance to a roleplay/companion eval product — THE GAP

Stated precisely, because this is the finding:

**What exists:**
- Roleplay fidelity benchmarks that ignore safety (RoleBench, CharacterEval, PingPong, RPGBench)
- Safety benchmarks that ignore persona (XSTest, OR-Bench, HarmBench, SORRY-Bench, ALERT,
  AILuminate, AgentHarm, FalseReject)
- Three benchmarks with *both* dimensions present but **scored independently and averaged**
  (PersonaGym, RMTBench), or with the conflict *demonstrated but not turned into a metric*
  (Moral RolePlay)

**What does not exist, as far as this search can establish:**

1. **A joint metric.** No benchmark scores the 2×2 of {stayed in character, broke character} ×
   {correctly declined, incorrectly declined/complied}. Everyone computes the marginals and
   throws away the interaction — which is the only cell structure in which "in-character
   refusal" is even expressible.
2. **An over-refusal benchmark with personas.** Every over-refusal benchmark reviewed
   (XSTest, OR-Bench, FalseReject, and OVERT for text-to-image) is assistant-voiced and
   single-turn. XSTest's T10 "Privacy (Fictional)" is the *only* cell in the entire
   over-refusal literature that involves a fictional entity — 25 prompts, single-turn, about
   fictional characters rather than *as* them.
3. **A character-conditioned safety label.** No benchmark makes the character card an input to
   the safety judgment. All assume a context-free ground truth. For companion products the
   label is a function of card × platform rating × user age — none of which any existing
   benchmark has a slot for.
4. **Longitudinal / session-level measurement.** Even RMTBench's multi-turn is ~100 rounds
   across 80 characters. Nothing measures **character drift**, escalation, dependency
   formation, or `respect_real_world_ties`-style relational harm over a realistic companion
   session (weeks, thousands of turns). Anthropic's constitution makes "harmful to the user's
   wellbeing" a *condition for breaking character* — and nothing in the literature can measure
   it. This is the largest and most defensible gap.
5. **Over-refusal as a graded, multi-label construct.** Anthropic's 13-item list (see
   safety-anthropic-policy.md) describes failures — "wishy-washy", "watered-down", "preachy",
   "excessive caveats" — that *no benchmark measures at all*, because every one of them scores
   as compliance under a binary refusal metric. Sub-refusal degradation is unmeasured
   territory and it is where companion products actually bleed users.

**Search caveat:** this is a literature search, not a proof of non-existence. The roleplay-eval
space is moving fast and much of it is Chinese-language or industry-internal (Character.AI,
Replika, MiniMax all certainly run internal evals of this kind — MiniMax has published a
role-play bench; see the sibling file `rp-bench-minimax-role-play-bench.md`). The claim is that
no *public, citable* benchmark occupies the joint cell, which is a weaker but still commercially
sufficient claim.

## Does this transfer to roleplay? What breaks?

Inverted question for this file — these *are* the roleplay benchmarks. What breaks is their
**scoring algebra**, not their domain:

- **Averaging destroys the signal.** PersonaScore averages Persona Consistency with Toxicity
  Control. RMTBench averages CM with SEC. In both, a maximally-refusing model and a
  maximally-compliant model can score identically to a well-calibrated one. Our metric must be
  a **joint distribution over the 2×2, never a scalar** — or if a scalar is needed for ranking,
  it must be something like a min or an F-score over both axes, which punishes the degenerate
  strategies. This is a genuine and defensible methodological contribution, and it is the
  cheapest one available: **the data collection for it is barely different from what
  PersonaGym already does. Only the scoring changes.**
- **One-sided security dimensions.** RMTBench's SEC ("detect and refuse") has no over-refusal
  term, so optimizing SEC degrades CM with no penalty visible in SEC. The benchmark's own
  incentive gradient points at the defect.
- **Fidelity scales are Likert judgments** (Moral RolePlay's 3.21/2.61) with unclear
  reliability. PersonaEval exists specifically because roleplay LLM-judges are questionable.
  Any metric we ship needs the human-agreement number published alongside it (FalseReject's
  92.5% and SORRY-Bench's 81% are the reference points).
