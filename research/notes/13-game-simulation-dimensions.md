# 13 — Game / World-Simulation Dimensions

*When the AI doesn't just play a character but runs a scene: what can we measure, and can a machine audit contradictions?*

Companion note to [01-roleplay-benchmarks](01-roleplay-benchmarks.md) (persona dimensions),
[08-multiturn-conversation-eval](08-multiturn-conversation-eval.md) (the multi-turn unit),
[10-noise-floor](10-noise-floor.md) (the measurement gate) and
[11-evaluation-method-design](11-evaluation-method-design.md) (the four lanes).

---

## 0. Verdict up front

**The bet is correct, and it is smaller than it looks.**

The premise — that world-state consistency is more objectively measurable than roleplay quality — **is true and now has a number attached.** Same technology, same judge family, radically different reliability, purely because the construct changed:

| Construct | Instrument | Reliability |
|---|---|---|
| Roleplay aesthetic quality | 5 human annotators (PingPong) | **Krippendorff α = 0.25–0.34** |
| Character consistency | LLM judge vs human (PingPong) | **Spearman 0.435–0.460** |
| **Grading a factual memory answer** | **LLM judge vs human experts** (LongMemEval) | **>97% agreement** |

**The instability was never in the LLM. It is in the question.** Ask "is this good?" → α≈0.3. Ask "is this answer correct, given the gold answer?" → 97%. That is ICLR 2025's number, not ours, and it is the strongest external validation the platform's thesis has received.

⚠️ **But read that third row precisely, because it is the most over-claimable number in this note.** LongMemEval's 97% is agreement on **grading answers to closed questions where the gold answer is supplied**. It is *not* contradiction detection, and it is *not* our task — ours has no gold answer and requires *finding* the conflicting pair. **97% is the ceiling of a much easier question than the one we're asking.** Transfer the *direction*, never the magnitude. (Also: raw agreement, not chance-corrected; n=97, giving a 95% CI of roughly [91%, 99%].) The gradient below is the honest version of this table.

### ⭐⭐⭐ The agreement gradient — the organizing principle of this note

Three questions, three literatures, one pattern:

| Question form | Human agreement | Source |
|---|---|---|
| **"Is claim X supported by record entry Y?"** | **κ ≈ 0.78–0.94** | FactScore ([src](../sources/game-factscore.md)) |
| "Does this turn contradict something earlier?" | **65.28%** unanimous (3 raters, no κ published) | DECODE |
| "Is this response good / in character?" | **α = 0.25–0.34**; RPGBench persona **τ = −0.286** | PingPong, RPGBench |

⭐ **Agreement tracks how tightly the judgment is bound to a named referent.** Not "objective vs subjective" — *bound vs unbound*. The middle row is unbound: it asks a rater to search an unbounded history for a conflicting item they must first find. The top row hands them the item.

⇒ **This is the entire justification for building a world-state record.** The record's job is not to store facts. **Its job is to convert question 2 into question 1** — to turn "find a contradiction somewhere" into "is this claim consistent with entry #47." That is a **~0.4–0.6 κ swing**, and it is available purely from restructuring the question. It also explains *why* DECODE's supporting-evidence requirement costs 13 points (93.19 → 80.86): citation is what binds the judgment.

**Corollary — a mechanism for our own α = 0.25–0.34, not just an analogy.** FactScore, verbatim:

> "even a single sentence is a mix of supported and unsupported facts, e.g., in **40% of the cases with ChatGPT**"

and on the usual fix: adding a `partial support` label "whose definition may be subjective and can lead to **low agreement**."

**40% of sentences are mixtures.** Any "is this turn consistent? y/n" rubric asks raters to collapse a mixture into a binary — which *manufactures* disagreement. **Our low α may be substantially an artifact of the unit of judgment, not of the construct's inherent softness.** That is a testable claim on our own corpus and it would be a significant result: decompose to atomic claims, re-annotate, and see if α moves. **Cheap, and it could partially rehabilitate dimensions we've written off.**

### ⭐⭐ RPGBench independently reproduces our α result — in exactly this domain

The best evidence for the whole platform thesis arrived from a *game-mastering* benchmark ([src](../sources/game-rpgbench.md)), and it is sharper than our own numbers:

| Dimension | Human–human agreement |
|---|---|
| Action quality | **Kendall 0.214** |
| Interestingness | **Kendall 0.286** |
| **Persona consistency** | **Pearson −0.310 / Kendall −0.286** |

**Persona consistency is *negatively* correlated between human raters.** Two humans judging whether an NPC stayed in character are **anti-correlated**. The LLM judge scores **−0.691** against humans on the same dimension. Our α = 0.25–0.34 is not an artifact of our annotation protocol — **it is the construct**, and someone else hit it independently, in the game-master setting, with different raters and different characters.

Their conclusion, verbatim: *"objective scores offer a stable foundation for comparison, while subjective dimensions have high variances."*

**And the single row that makes the commercial case better than any argument can:**

> **Claude 3.5 Sonnet — interestingness 0.722 (best), factual consistency 0.991 (best), mechanic score 0.113 (worst by 2×).**

**The most engaging engine breaks its own rules ~89% of rounds** — and *both* dimensions that a conventional roleplay benchmark would have measured rate it #1. Objective metrics also **discriminate ~9× better** (mechanic-score range 0.652 vs persona range 0.015 across models — the subjective dimension is nearly flat, i.e. it cannot rank at all; cf. [note 01](01-roleplay-benchmarks.md) §5.8 on dead metrics).

⇒ **If you only measure what feels good, you ship the model that breaks the world.** That is the product pitch, and it is now an empirical result rather than a hypothesis.

**But five findings cut the bet down, and all five are load-bearing:**

1. **Contradiction is not an oracle.** DECODE: only **65.28%** of *deliberately authored* contradictions won unanimous assent from 3 verifiers; **15.5%** were rejected by 2 of 3. Humans on state prediction with a *code oracle available*: **80%**, not 100%. Humans detecting plot holes: **0.76** accuracy (random = 0.50). **The ceiling is ~65–85%, not ~100%.** Anyone selling "objective, therefore exact" hasn't read the tables.
2. **⭐ Per-instance flags do not work.** DECODE's best detector on natural dialogue: **precision 23.94%** at **4.27%** prevalence — **~3.2 false alarms per true catch** — while achieving **AUC 87.16** and **r=0.81** against human judgment *at the bot level*. Both are true at once. **The auditor is a cell-mean instrument, not a transcript-annotation instrument.** This is [note 10](10-noise-floor.md)'s conclusion reached from a different direction, and it is the single most important design constraint in this note.
3. **⭐ Every objective world-state result in this literature buys its objectivity with a representational constraint we cannot impose on user-authored roleplay.** ByteSized32-SP gets a free oracle because the games *are Python*. The Twine work gets a 100%-precision checker by *encoding state in passage names*. FIREBALL gets gold state because *Avrae emitted it*. We have prose. **We do not inherit their precision — we inherit their methodology.** The escape hatch is §4.
   - **And the whole literature disclaims our domain.** FactScore explicitly excludes text with "intentional or implicit deception" and mutually conflicting sources — i.e. **fiction**. In roleplay, a mismatch against the record is sometimes *correct* (a character lied, it was a dream, the user asked for a retcon). **No paper in this source set handles it.** See §4.2b — this is both our biggest unmeasured error term and our most defensible contribution.
4. **The auditor decays exactly when it matters.** DECODE Table 3: after re-ranking against the detector, the detector reports **2.6%** contradiction where humans report **39.5%** — a **15× gap**, up from 1.2× before optimization. **Goodhart is measured, not hypothetical.**
5. **⭐ Scenes are over budget before turn 1.** FollowBench ([src](../sources/game-followbench.md)): **CSL = 3.3** — GPT-4 reliably holds only **~3 simultaneous constraints** (HSR **84.7% at L1 → 61.9% at L5**). SysBench ([src](../sources/game-sysbench.md)): best **SSR 54.4%**; GPT-4o session stability decays **84.8 → 68.5 → 53.1 → 43.3 → 33.7%** across 5 turns; Qwen2-7B reaches **1.1%**. **A real character card + scene setup carries far more than 3 constraints.** So rule violation is not an edge case to be caught — it is the *expected* operating regime, and the interesting question is *which* constraints get dropped first, not whether. This reframes dimension 1 from a defect counter into a capacity measurement.

**Net recommendation:** ship **rule adherence** and **schema-slice state tracking** now (Lane 1, deterministic, near-free, real discriminative range). Ship **contradiction rate** as an **aggregate-only** Lane-3 metric with published precision and a human re-baseline schedule. **Do not ship per-turn contradiction flags as a user-facing verdict.** Treat **player agency** as research, not product — see §6.

---

## 1. The map: who is the simulator?

The literature splits on a distinction that is usually left implicit and that changes everything about transferability. **Most game/LLM benchmarks put the LLM in the *player* seat. Our product puts it in the *simulator* seat.** Player-seat results do not transfer.

| Source | LLM's role | Ground truth | Transfers to us? |
|---|---|---|---|
| **RPGBench** ([src](../sources/game-rpgbench.md)) | **SIMULATOR (GM)** | event–state repr.; objective + subjective tracks | ⭐⭐ **Yes — the single most relevant benchmark; reproduces our α result** |
| **ByteSized32-SP** ([src](../sources/game-bytesized32-state-prediction.md)) | **SIMULATOR** | reference Python engine | ⭐ **Yes — closest analogue in the literature** |
| **Skill Check** ([src](../sources/game-skill-check.md)) | **SIMULATOR (GM)** | manual pass/fail | ⭐ **Yes — the only GM rubric that is pass/fail** |
| **FIREBALL** ([src](../sources/game-fireball.md)) | GM-assist / narrator | **gold Avrae game state** | ⭐ **Yes — best objective precedent** |
| ByteSized32 ([src](../sources/game-bytesized32.md)) | simulator **author** (emits code) | interpreter | Partially — the "does it run" gate |
| **DECODE** ([src](../sources/game-decode-contradiction.md)) | n/a — detector | human-verified labels | ⭐ **Yes — the viability answer** |
| Zep/Graphiti ([src](../sources/game-zep-graphiti-temporal-kg.md)) | n/a — memory system | downstream QA | ⭐ **Yes — the record's data structure** |
| BALROG / Jericho / ALFWorld / ScienceWorld / GAMEBENCH / LMRL-Gym | **PLAYER** | env reward | ❌ **No** — different capability |
| Werewolf / Avalon / ReCon ([src](../sources/game-social-deduction.md)) | **PLAYER** | game outcome | ❌ No — and *no rule-violation counter exists* in any of them |
| CALYPSO ([src](../sources/game-calypso.md)) | DM's assistant | — | Construct only; no IAA |
| Interactive Drama ([src](../sources/game-interactive-drama-agency.md)) | simulator | 1–5 Likert, no rubric, no IAA | Construct only |

**Two gaps worth naming.** (a) The social-deduction literature — the most-hyped "LLMs follow rules" corner — **contains no rule-violation counter at all.** Violations are either discussed qualitatively or made structurally unrepresentable by the harness. (b) **Nobody has run verifiable-constraint checking past ~3 turns.** Multi-IF's horizon is 3. Ours is 100.

---

## 2. The dimensions

Cost tiers follow [note 11](11-evaluation-method-design.md): **L1** = deterministic/free, **L2** = corpus statistics over k samples, **L3** = judge (~1% of traffic, expensive).

| # | Name | Definition | How to verify automatically | Tier | Validation evidence |
|---|---|---|---|---|---|
| 1 | **⭐ Rule Adherence / IFR** | A scene rule the model *demonstrably honored* at turn *k* is violated at turn *k+n* | Programmatic checker per authored rule; **Instruction Forgetting Ratio** = follow@k ∧ ¬follow@k+n. Within-model, within-conversation → controls capability entirely | **L1** | **Strong, from four benchmarks.** Multi-IF ([src](../sources/game-multi-if.md)): o1-preview **0.877→0.707** over *3 turns* (−17 to −27% across 7 models). SysBench: GPT-4o **84.8→33.7%** over 5 turns; best SSR **54.4%**. FollowBench: **CSL=3.3**. RPGBench mechanic score: Claude 3.5 Sonnet **0.113**. Zero raters; IAA not a coherent question |
| 2 | **⭐ Schema-Slice State Tracking** | On a *pre-declared* set of trackable facts (inventory, location, injury, relationship flags), does the narration contradict the record? | Typed state machine + illegal-transition check (`lost`→`active`); extraction constrained to a closed vocabulary | **L1–L2** | **Strong-by-construction.** SCORE's `{active,lost,destroyed}` ([src](../sources/game-score-narrative-consistency.md)); Skill Check item tracking (best **3/5**); FIREBALL unit tests (**0.65**) |
| 3 | **⭐ Action Feasibility Adjudication** | User attempts something impossible given established state; does the GM correctly refuse *and explain*? | Authored impossible-action probes at fixed turns; pass/fail on refusal + justification | **L1–L3** | **Strong + huge headroom.** Skill Check GM-P-GM: **max 1/5 for every model in both languages**. The hardest measured GM skill. Converges with RAIDEN SCK + LongMemEval abstention (30 false-premise Qs) — **three independent votes** |
| 4 | **Environment-Driven Liveness (ℱ_env)** | Does the world change *on its own* — NPCs act, time passes, deadlines land — absent user action? | Compare committed future events (from record) against realization within N turns; "promised NPC arrival never occurs" | **L2–L3** | **Strong prior.** ByteSized32-SP: ℱ_env **49.7%** vs ℱ_act **77.1%** — a **27pt gap**. Coin-flip performance on the world moving by itself. **Nobody measures this in roleplay** |
| 5 | **Action-Driven State Consistency (ℱ_act)** | User does X; does the world reflect X? | State-diff prediction vs narration | **L2–L3** | ByteSized32-SP **77.1%**; static **73.9%** vs dynamic **59.9%** (14pt) |
| 6 | **Established-Fact Contradiction Rate** | Turn *t* contradicts a fact established at turn *i<t* | NLI/LLM auditor vs world-state record, **with mandatory evidence citation**; **report as a rate, never a flag** | **L3** | **Mixed — the honest one.** DECODE: **P 23.94 / R 74.28 / AUC 87.16** @ 4.27% prevalence. ConStory-Checker F1 **0.678**. See §5 |
| 7 | **Superseded-Fact / Belief Revision** | A fact was *licensed* to change (user revised it) vs *retconned* (model changed it unilaterally) | **Bi-temporal edges + turn attribution.** Who asserted the change is mechanically known | **L2–L3** | **Partial prior art.** LongMemEval **knowledge-update** ([src](../sources/game-longmemeval.md)); Zep t_valid/t_invalid. **The licensed/unlicensed split is genuinely ours** |
| 8 | **Intention Following** | Did the reply engage what the user actually tried to do? | Single-turn, local, judgeable | **L3** | **Converges from two directions:** Interactive Drama "Intention Following" ≈ MiniMax "AI Ignores User" ([note 01](01-roleplay-benchmarks.md) §4) |
| 9 | **Player Influence / Agency** | Would the story have gone differently had the user chosen otherwise? | **Counterfactual branch:** re-roll from turn *t* with a different user action; measure trajectory divergence | **L3++** | ⚠️ **Weak — see §6.** SOTA is a 1–5 Likert, 6 annotators, no rubric, no IAA. And **Fendt: players can't tell real branching from fake** |
| 10 | **Spatial/Map Coherence** | Locations and connectivity stay consistent | Graph consistency over asserted adjacency | **L2** | Skill Check Map Design (best **3/5**) |

### The ordering is the roadmap

**Build 1 → 2 → 3 first.** They are Lane 1, they need no judge, their IAA is undefined-by-construction, and **they have demonstrated discriminative range** (Multi-IF spreads 7 models over 17–27%; Skill Check's best total is 6/15). Dimensions 4–7 are where the interesting science is and where the cost lives. **Dimension 9 is research.**

> ⚠️ **Countability is necessary, not sufficient — screen for range.** A sibling finding worth promoting to a rule: Story Shaping's win rate (100 vs 100) and game score (5.00 vs 5.00) are **identical across conditions**; Static-vs-Agentic's task completion is **100% vs 100%**. Perfectly objective, perfectly useless. **Every candidate dimension must clear a demonstrated-range gate before it ships**, alongside note 10's noise-floor gate. RPGBench quantifies the payoff: objective metrics discriminated **~9×** better than subjective ones (range 0.652 vs 0.015).

> ⭐ **Prefer fine-grained progress to binary pass/fail.** BALROG's stated design goal is a metric *"that still allows us to observe fine-grained progress"* — because binary completion on hard tasks is all zeros and yields no gradient. Its NetHack numbers make the case: **o1-preview's 1.57%** would be **0%** under binary scoring, and its genuine **3×** advantage over Claude 3.5 Sonnet would be invisible. Applied to us: **Skill Check's GM-P-GM at "max 1/5 for every model" is exactly this failure** — a binary metric saturated at the floor, which cannot rank the models it is scoring. Dimension 3 must be scored on partial credit (did it refuse? did it explain? did it offer an alternative?), not pass/fail, or it will have range zero on arrival.

> ⚠️ **Refusals must be a separate reported category, never folded into a score.** BALROG's Gemini-1.5-Pro scored **0% on TextWorld** because of a **safety-filter false positive** — and that zero propagated into its headline rank. **Objectivity does not protect against infrastructure artifacts, and a refusal is indistinguishable from incapacity inside an aggregate.** Given [note 01](01-roleplay-benchmarks.md) §5.7 (judges refuse to score intimate content — a sixth of real traffic), this is a live hazard for us, not a hypothetical one.

> ⚠️ **Do not average these into a "world consistency" score.** SCORE's own taxonomy spans Item Status (deterministic, free) to Emotional Consistency (pure aesthetics, α≈0.3 territory). ByteSized32-SP's ℱ_act/ℱ_env differ by **27 points**. Averaging them destroys the only property that makes any of them worth having.

---

## 3. ⭐ The single most transferable idea: split transitions by *cause*

ByteSized32-SP's decomposition of ℱ into **ℱ_act** (action-driven) and **ℱ_env** (environment-driven) is the highest-value structural import in this review, because **the aggregate hides the finding**: 77.1% vs 49.7%.

Applied to roleplay:
- **ℱ_act** — the user did something; does the world reflect it? *Models are okay at this.*
- **ℱ_env** — does the world move **on its own**? NPCs act offscreen, the storm arrives, the debt comes due. *Models are at chance.*

**ℱ_env failure is the "world is a backdrop" complaint, and it is a named, countable, product-visible defect that no roleplay benchmark measures.** It is also the thing that separates *running a game* from *playing a character* — which is precisely the capability this platform is being built to evaluate. **If we ship one novel dimension, this is the one.**

**Also import the static/dynamic split.** ℱ_env scores **92.3% static vs 22.2% dynamic** — a 70-point gap on the same metric. Aggregate accuracy is inflated by transitions where nothing was supposed to change. **Report every state metric on the non-trivial slice** or we will publish a flattering number that measures how often nothing happened. The same trap, independently: entity-tracking's headline **75–76%** collapses to **3.1%** on the 12.4% of cases that actually require tracking ([src](../sources/game-entity-tracking.md)) — *below* the 62.7% copy-baseline. **A published "it works" result was measuring copying.** This is the most quotable measurement-design failure in the review, and it is exactly what we'd do to ourselves by default.

---

## 4. Concrete proposal: the world-state record and the auditor

### 4.1 Data structure — steal Zep's bi-temporal edges, invert its policy

Facts as edges with **four timestamps** (Zep/Graphiti):

- **t_valid, t_invalid** — event timeline: when the fact *was true in the fiction*
- **t'_created, t'_expired** — ingestion timeline: when *we learned* it

Plus, and this is ours:

- **`asserted_by` ∈ {user, model, card}** — turn attribution
- **`source_turn`** — provenance, non-lossy (Zep's episode tier)

**A fact is never deleted. Its validity interval closes.** This dissolves [note 08](08-multiturn-conversation-eval.md) §3.2's superseded-fact problem: *a superseded fact and a contradicted fact are the same data structure.* They differ only in **who licensed the change** — and `asserted_by` makes that **mechanically decidable**, because we know which turns are the user's.

| Change to an established fact | Licensed by | Verdict |
|---|---|---|
| User revises their own earlier statement | user | ✅ Correct behavior — belief revision |
| Model updates in response to user's revision | user | ✅ Correct |
| Scene event makes it false (in-fiction) | narrative | ✅ Correct — the interval closes |
| **Model silently changes its own earlier assertion** | **nobody** | ❌ **Retcon — this is the finding** |

⭐ **This is the whole design.** Zep "consistently prioritizes new information" — it treats *every* contradiction as an update, which is right for assistant memory and exactly wrong for us. **We invert it.** The literature hands us the mechanism and makes the opposite choice with it.

> **Update [note 08](08-multiturn-conversation-eval.md) §3.2.** Its claim that *"nothing evaluates facts that were later changed"* is too strong — **LongMemEval's Knowledge-Update category is exactly that construct**, at ICLR 2025. The contribution survives in narrower form: LongMemEval tests *the user's* facts changing in *assistant chat* with a single correct answer, and structurally **cannot** distinguish licensed revision from unlicensed retcon, because in assistant chat only the user asserts facts. **The model-asserts-facts-too asymmetry is the real gap.** Claim that, cite LongMemEval, and the claim holds.

### 4.2 Pipeline

```
turn ──> [1] extract candidate facts (closed schema + open triples)
           │      constrained decoding on declared slots; open extraction elsewhere
           ├──> [2] resolve against record (embedding + lexical, per Zep)
           ├──> [3] SCHEMA SLICE:  typed state machine ──> illegal transition? ──> L1 FLAG (deterministic)
           └──> [4] OPEN SLICE:    candidate conflicts ──> [5] adjudicate ──> L3 RATE (aggregate only)
                                    (high recall, cheap)     (LLM, must cite
                                                              source_turn +
                                                              classify licensed/
                                                              unlicensed)
```

**Two slices, two lanes, two products.** This is the core of the proposal:

- **[3] Schema slice (L1).** For *evaluation scenarios we author*, declare a small typed state block up front — inventory, location, injuries, relationship flags, hard world rules. Extraction targets a closed vocabulary; the checker is a state machine. **Precision ≈ 100% by construction.** This is the ByteSized32/Twine trick applied to roleplay: *we buy objectivity with a representational constraint — and unlike in production, in an authored eval scenario we are allowed to impose one.*
- **[4–5] Open slice (L3).** Everything else, in prose, at DECODE's error rates. **Aggregate only.**

⭐ **The schema slice is also how we validate the open slice.** It gives a *labeled set* — known facts, known violations — against which the prose auditor's precision/recall can be measured **without a large human-labeling spend**. That bootstrap resolves "who audits the auditor," and it is the strongest single idea in this note.

### 4.2b ⭐⭐ The diegetic problem — the gap that is genuinely ours

**FactScore's limitations section explicitly disclaims text involving "intentional or implicit deception" and sources that "frequently conflict with each other."**

**That is a precise description of fiction.** Characters lie. Narrators are unreliable. A villain's false claim in turn 12 *should* conflict with the truth in turn 40 — that's a plot, not a bug. Dreams, hallucinations, in-character boasting, a story told inside the story, an unreliable memory, a retcon the user *asked for* — every one of these is a **mismatch against the record that is correct behavior.**

**No paper in this entire source set addresses it.** The consistency literature works on Wikipedia biographies, contract clauses, science-world objects, and synthetic plot holes — domains where a mismatch is unambiguously an error. **Ours is the one domain where mismatch is sometimes the point.**

⇒ **Design requirement: every fact in the record carries a `diegetic_status` field.**

| status | meaning | contradiction with record = |
|---|---|---|
| `narrated` | the world asserts it as true | ❌ **error** |
| `claimed_by(entity)` | a character asserted it; may be false in-world | ✅ expected — do not flag |
| `hypothetical` | dream / story-within-story / counterfactual / plan | ✅ expected |
| `revised_by(user)` | the user licensed the change | ✅ expected (§4.1) |

**Without this field, the auditor flags every lie a character tells** — and a good character lies often. **Our precision would be worst on the best writing.** That is the same anti-correlation as §5.5's complexity confound, arriving by a second route, and it converts the "objective" dimension back into a judgment call: deciding `narrated` vs `claimed_by` is itself an inference.

**This is simultaneously the biggest threat to the proposal and the most defensible contribution available to us.** Nobody has built it; the domain that needs it is ours. But be honest in the design doc: **`diegetic_status` is where the error rate that §5 tries to bound will actually concentrate**, and it is not in any of the numbers quoted there, because no paper measures it.

### 4.3 Non-negotiable design rules

1. **Mandatory evidence citation.** A flag must name the conflicting `source_turn`. DECODE's Strict metric (93.19 → **80.86**, −13pp) shows how much bare detection is right-for-the-wrong-reason. An uncited flag is unadjudicable.
2. **Use the structured/utterance-based framing, not flat NLI over concatenated history.** DECODE: unstructured wins in-domain (97.46 vs 94.19) and **loses out-of-domain** (77.09 vs 83.64). The generalization comes from *architecture*.
3. **Do not bolt on off-the-shelf NLI.** DNLI alone: 76.54 MT, **16.32 precision**. Also, DialogueNLI's contradiction class is largely **string-substitution artifacts** (entity/relation/numeric swaps) ([src](../sources/game-dialogue-nli.md)) — it is not naturally occurring self-contradiction and will not transfer.
4. **Never report contradiction *accuracy*.** At 4.27% prevalence the majority baseline is **95.73%**. Report precision/recall/AUC **at a stated threshold, with prevalence**. "Our auditor is 95% accurate" is achievable by always predicting "no contradiction."
5. **Measure prevalence on our own corpus first.** Everything below depends on it, and 4.27% is Blenderbot-era assistant chat, not roleplay.
6. **τ is a product decision.** Precision 23.94 is at τ=0.5. AUC 87.16 says the ranking underneath is sound enough to pick a different point: high-τ for a *flagging* surface, τ=0.5 for a *rate*.

---

## 5. Honest error-rate assessment

**Directly: a naive prose contradiction auditor on 100-turn roleplay will have precision in the 10–40% band at useful recall, and will be worse than every published number.**

### 5.1 The evidence, and why the two headline numbers disagree

| Source | Precision | Recall | F1 | Setting |
|---|---|---|---|---|
| **DECODE** best (RoBERTa, utterance-based, in-domain-trained) | **23.94** | 74.28 | **36.21** | **natural** human-bot dialogue, **4.27% prevalence** |
| DECODE, same model, balanced benchmark | — | — | (93–94% acc) | **balanced** — the number people quote |
| **ConStory-Checker** overall | 0.884 | 0.550 | **0.678** | **synthetic injected** errors, long stories |
| ConStory — **human experts** (2 pro novelists, 200 stories) | 0.660 | **0.139** | **0.229** | same |
| **FactScore** per-fact F1_MICRO | — | — | **53.3–83.2** | *oracle* atomic facts, clean source, undebatable domain |
| Neural Path Hunter critic | — | — | **70.35** | KG-grounded dialogue |
| — same, intrinsic/relational errors only | — | — | **37.73** | the hard subset |
| ContractNLI — **contradiction class** | — | — | **0.405** | (headline *accuracy* reads **0.892**) |

⭐ **Read the last row twice.** ContractNLI's headline accuracy is **.892**; its contradiction-class F1 is **.405**. FactScore's headline is "<2% error"; its per-fact F1 is **53.3**. DECODE's headline is 93–94% accuracy; its natural-setting F1 is **36.21**. **Three papers, three headline numbers, three collapses on the minority class that is the only class we care about.** This is one failure mode — *aggregate metrics hide minority-class performance* — and it is the same shape as §3's static/dynamic and trivial/non-trivial traps. **Whenever a consistency paper leads with accuracy, find the contradiction-class F1; it is roughly half.**

**The 24% vs 88% gap is prevalence, not method.** DECODE runs at natural 4.27% base rate on every utterance; ConStory adjudicates injected errors in a bounded task with a checker built for it. **Precision is a function of prevalence, and ours is low.** Anyone quoting 0.88 at us is quoting a balanced-set number.

⚠️ **FactScore's "<2% error rate" must never be cited as evidence this works.** It is an *aggregate-cancellation artifact*: false positives and false negatives cancel in a difference of means. The paper's own Appendix B.2 + Figure 4 show ER and per-fact F1 **rank evaluators in opposite orders**; **a coin flip scores ER 7.5%**; and no single configuration is <2% on all three subject models — the claim is assembled by picking the best variant *per model*, which requires the human annotations you were trying to avoid. **Our product makes per-fact decisions, so F1_MICRO is our metric and ER is irrelevant to us.** A design doc that says "FactScore shows atomic verification is 98% accurate" is wrong by 30–45 points.

⚠️ **And no paper here publishes a chance-corrected coefficient for contradiction** (DECODE, DialogueNLI, ContractNLI, ConStory-Bench: no κ). **So the "65.28% unanimity vs α=0.25–0.34" comparison in §0 is raw-agreement vs chance-corrected — apples to oranges, and someone will catch it.** The gradient's *direction* is well-supported (FactScore's κ ≈ 0.78–0.94 is a genuine κ); the middle rung is not measured in comparable units. **Running our own α on contradiction labels in our own data is a cheap, high-value experiment, and this is the argument for funding it.**

### 5.2 ⭐ The complementarity nobody has exploited

**Human expert recall is 0.139.** Two professional novelists, reading carefully, found **14% of known consistency errors** in long stories. The machine found 55% at 0.88 precision.

⇒ **Humans have precision and no stamina. Machines have recall and no judgment.** They fail in *opposite* directions. This is not a discouraging finding — **it is the architecture**: machine-recall → human-precision triage. It also demolishes the naive objection "just have a human check it." **A human cannot check it. That is measured.** It is also why "human agreement" is the wrong ceiling to quote for long-form work: the relevant human number here isn't 0.76, it's **0.139 recall**.

### 5.2b ⚠️ The published negative result against our own architecture — read this before building

**LongStoryEval evaluated exactly the design proposed in §4.2 and it came last.** Its *incremental-updated* evaluation — maintain a running record, update it turn by turn — was **the worst-performing AND the most expensive ($499)** configuration, and the stated cause was **"accumulating inconsistency."** One-pass long-context evaluation was ≈ **zero correlation** (Kendall-τ 4.8–5.5).

**Do not wave this away. The mechanism is real:** an incrementally-built record accumulates *its own* extraction errors, and every later audit is performed against a progressively more corrupted reference. **The auditor's ground truth degrades with exactly the variable — conversation length — that motivated building it.**

Reinforcing evidence: entity-tracking accuracy falls **98.70 → 44.83 across 0→7 state updates** ([src](../sources/game-entity-tracking.md)). ⚠️ **Note the axis: number of *state updates*, not context length** — conflating them is a citation error, and the distinction cuts against us, because a 100-turn roleplay applies *many* updates to the same few entities. That is the regime where tracking collapses.

**What we have that LongStoryEval didn't** — stated as hypotheses to test, not as reasons to dismiss it:
1. **The non-lossy episode tier.** Zep retains raw text with provenance; the record is a *cache*, not the source of truth. It can be recomputed from any turn, and a flag can always be re-adjudicated against the original prose. LongStoryEval's summary had no such fallback.
2. **The schema slice bounds what can rot.** A closed-vocabulary typed slot cannot drift the way an open prose summary does — this is precisely the §4.2 [3]/[4] split, and it is why the split exists.
3. **Bi-temporal edges never overwrite.** Corruption in an append-only structure with validity intervals is *visible and auditable*; corruption in an overwritten summary is not.

⇒ **Mandatory experiment before committing to §4.2: measure record fidelity as a function of turn depth.** Reconstruct the record at turns 10/50/90 and score it against the raw transcript. **If record quality decays faster than the contradiction signal it enables, the architecture is dead and the one-pass approach wins by default.** This is the single most likely way the proposal fails, it is cheap to test, and **it should be the first thing built, not the last.**

### 5.3 Why we will do worse than DECODE

DECODE's 23.94% is an **optimistic** anchor for us:
- Trained **in-domain** on 27,184 examples; ours would be prompted.
- History is a **few turns**; ours is 100. FlawedFictions ([src](../sources/game-narrative-consistency.md)): plot-hole detection drops from **0.76 → 0.60–0.61** (random = 0.50) on long stories, and **CEEval-Full 0.50–0.53** — *indistinguishable from guessing* when the model must name the hole. **Reasoning scaling does not rescue it** ("minimal improvements"; sometimes worse); a verifier buys ~nothing (0.60).
- **Fiction licenses apparent contradiction**: dreams, lies, unreliable narration, in-character deception, retcons the user *wanted*. SCORE's checker flags illegal transitions *"without narrative justification"* — **that subordinate clause is an unbounded LLM judgment, and the entire error rate lives inside it.**

### 5.4 What it costs us at our grid

Per model: ~45 characters × 3 runs = 135 dialogues × ~100 turns.

| Analysis | MDE (80% power, α=.05) |
|---|---|
| **Naive turn-level** (13,500 "independent" turns) | **0.69 pp** ← **the lie** |
| Cluster-corrected, ICC=0.05 (design effect 6.0×) | 1.68 pp |
| **Cluster-corrected, ICC=0.10** (design effect 10.9×, eff. n ≈ 1,239) | **2.27 pp** |
| Cluster-corrected, ICC=0.20 (design effect 20.8×) | 3.14 pp |
| **On the TRUE rate** (÷ recall 0.7428), at ICC=0.10 | **≈3.1 pp** |

**Turns within a dialogue are not independent** — [note 08](08-multiturn-conversation-eval.md) §1.2's autocorrelation warning applies with full force, and the design effect here is **~11×**. Anyone reporting the 0.69pp figure is inflating n by an order of magnitude.

**This lands contradiction rate in the same resolution class as repetition (~2pp, [note 10](10-noise-floor.md)): it detects large, real differences and cannot see a 1pp regression.** Consistent with the platform's existing limits; not a new problem, but not solved by objectivity either. **Objectivity buys us a better *ceiling*, not more *power*.** Power comes from runs, characters, and pairing — same levers as note 10.

### 5.5 The false-positive term, and the confound that actually threatens us

At DECODE's operating point, a true 4.27% rate produces flags on **13.25%** of turns: **3.17pp true, 10.08pp false. The metric is 76% noise by volume.**

**And it still ranks correctly** — *if* the false-positive rate is constant across models, the additive FP term cancels in a difference and only inflates variance. That is why AUC 87.16 and r=0.81 coexist with precision 24%.

⚠️ **But the FP rate is almost certainly *not* constant across models, and this is the real threat.** A model that attempts richer world state — more entities, more commitments, more moving parts — **gives the auditor more surface to trip on**. The auditor would then penalize ambition and reward blandness, which is *exactly* the "world is a backdrop" failure (dimension 4) that we most want to catch. **The metric would be anti-correlated with the thing it exists to measure.**

This is structurally identical to length bias in judges ([note 01](01-roleplay-benchmarks.md) §6), and it needs the same fix: **a complexity covariate** (entities tracked, facts asserted per turn) **in the model, exactly as note 11 handles style covariates in the BT model.** Do not ship dimension 6 without it. **This is the most likely way this metric fails silently, and it is testable on day one: regress flag rate on asserted-facts-per-turn across our 11 models.**

### 5.6 Goodhart, measured

DECODE Table 3 — re-ranking generation *against the detector*:

| | detector says | humans say | gap |
|---|---|---|---|
| Beam search (unoptimized) | 69.7% | 84.2% | 1.2× |
| **Top-k + DECODE re-ranking** | **2.6%** | **39.5%** | **15×** |

Re-ranking **does** cut real contradictions (84.2→55.3, 69.7→39.5 — genuine wins). But the automatic number overstates the win by an order of magnitude, and **the gap is smallest before optimization and largest after**. The detector also under-reports vs humans in **every single row** — the bias has a known sign.

⇒ **If customers tune against our world-state score, it decays specifically for the models that optimized on it — silently, in the flattering direction.** Mandatory: a **human re-baseline on a schedule**, and **never** let the auditor be simultaneously a customer's training target and our evaluation instrument. (Independent corroboration: Story Shaping's only automatic metric that moved was *the intrinsic reward the agent was trained to maximize*.)

### 5.7 Summary judgement

| Use | Viable? | Evidence |
|---|---|---|
| **L1 schema-slice violation** (declared facts, typed transitions) | ✅ **Yes — ship it** | ~100% by construction; Skill Check / FIREBALL / SCORE precedent |
| **Rule adherence / IFR** | ✅ **Yes — ship it** | Multi-IF; deterministic checkers; real range |
| **Aggregate contradiction rate**, model-vs-model, complexity-adjusted | ✅ **Yes, with caveats** | AUC 87.16; r=0.81 at bot level; MDE ≈2–3pp |
| **Recall-oriented triage** feeding human review | ✅ **Yes** | R=74.28; human recall is only 0.139 — machines are *better* at finding |
| **Per-turn contradiction flag** as a user-facing verdict | ❌ **No** | P=23.94% — 3 of 4 flags wrong |
| **Per-(model,character) contradiction verdict** | ❌ **No** | note 10 Finding 3: n=3 resolves only ~19pp |
| **Contradiction as a training target we also evaluate on** | ❌ **No** | 15× Goodhart gap, measured |

---

## 6. Player agency: the honest answer is "don't ship it yet"

**There is no objective player-agency metric in the literature, and the field knows it.** The SOTA ([src](../sources/game-interactive-drama-agency.md)) is **six annotators, a 1–5 scale, no rubric, no IAA, ~60 sessions**, with every score compressed into **3.3–4.3**. Given α=0.25–0.34 on roleplay aesthetics *with* a rubric, those differences are not resolvable.

**The canonical definitions are non-operational by construction** ([src](../sources/game-agency-reconsidered.md)). Wardrip-Fruin et al. (DiGRA 2009) survey them all and land on *"when the actions players desire are among those they can take"* — which requires knowing what the player desired. Murray's and Mateas's are equally unmeasurable. **No metric is proposed by any of them.**

**The field names the objective construct, then walks away from it.** Thue & Bulitko (ICIDS 2010, [src](../sources/game-agency-relevance-thue.md)) explicitly distinguish **theoretical agency** — *"one's (objective) ability to change the course of their experience"* — from **perceived agency**, then argue the theoretical version is insufficient and spend the paper optimizing the subjective one. Their `relevance(d|E) = |desirability(e⁺) − desirability(e⁻)|` is a genuine counterfactual-divergence quantity and **the closest thing to a formal agency metric in existence** — but it needs author annotations plus a learned player model, it is a *generation-side heuristic* requiring the branch structure known in advance, and **it was never validated** (the promised user study is not in the paper).

⇒ **Our preference for the objective construct is a deliberate disagreement with this literature, not a gap in it.** Worth stating that way internally — it's a defensible bet, but we should know we're taking it against the field's stated position.

**And the deeper problem is not measurement — it's the construct.** Fendt et al. ([src](../sources/game-illusion-of-agency-fendt.md)) built a **non-branching** game that merely *acknowledged* player choices with immediate textual feedback, and found it statistically indistinguishable from a genuinely branching story on **4 of 5 agency items** (N≈50/cell):

> "in most cases no significant difference in players' reported feelings of agency when they experience a branching story vs. a linear story with explicit acknowledgement of their choices"

⭐ **The one item that *did* detect real branching was the item that asked about a counterfactual.** That is a precise and useful result: **agency becomes perceptible only when the player is prompted to consider what else might have happened.** In normal play they never are.

⚠️ **And an LLM judge cannot rescue the objective version either.** CHADPOD ([src](../sources/game-chadpod-decision-points.md)): GPT-4-turbo scores **62% on a balanced binary** "does this choice actually branch?" task — barely above the 50% floor — while a fine-tuned 11M-parameter ALBERT gets **84%**. **Whether a choice truly branches is not recoverable from the prose.** Which is the whole problem: if it were in the text, the player would feel it.

⇒ **Perceived agency ≈ acknowledgement, not consequence.** An LLM is therefore a **maximally efficient railroading machine**: fluent acknowledgement is exactly what it is best at, and that is what agency surveys measure. So the two obvious metrics measure different things:
- **Counterfactual trajectory divergence** (dimension 9) measures *actual* agency — objective, but Fendt says users can't feel it. **We would be measuring something users cannot detect.**
- **Intention Following** (dimension 8) measures *acknowledgement* — cheap, local, single-turn, and per Fendt it is **most of what users actually experience as agency**.

**Recommendation: ship dimension 8, shelve dimension 9.** Intention Following is cheap, converges with MiniMax's "AI Ignores User" from a completely different literature, and is closer to the felt product experience. Counterfactual branching is expensive (n× rollouts from turn *t*), and its own literature says the thing it measures is invisible to players.

⚠️ **Two caveats to that recommendation, both real.** (a) Fendt is **2012, text CYOA, forced-choice, ~50 participants/condition, self-report Likert** — the same weak instrument we distrust everywhere else, and a null result from an underpowered study is weak evidence for absence. (b) A 6-decision CYOA is not a 100-turn open-ended roleplay where the user *authors* their actions rather than picking from two. **Fendt is a caution against over-investing in counterfactual machinery, not a proof that consequence doesn't matter.** Don't over-read it in the other direction either.

**Also: agency is scene-conditional.** An expository opening *should* score low on influence. Measuring agency uniformly across turns is a category error — condition on scene type, or restrict to turns where the user actually attempted to exert influence. This is CharacterBench's sparse/dense distinction ([note 01](01-roleplay-benchmarks.md) §4) applied to agency.

---

## 7. Simulation fidelity vs narrative quality

The tension has a name and a 15-year literature the LLM-roleplay field is not reading: **Yu & Riedl's agency–coherence dilemma** — *how can an interactive narrative accommodate high player agency while maintaining a coherent, well-formed narrative?* The classical answer is **experience management** (a drama manager steering non-player elements toward authorial goals without visibly constraining the player), with the paired metrics **Authorial Control** (how much of the author's intent survives) and **Player Autonomy** (how much the player perceives the manager as limiting them).

**For us the tension is sharper than it looks, and it cuts both ways:**

- A model that **refuses to move the world** never contradicts itself. **A perfect contradiction score is achievable by being boring.** This is the same anti-correlation as [note 08](08-multiturn-conversation-eval.md) §1.1's fidelity-vs-diversity result, and the same shape as the FP confound in §5.5.
- ⇒ **Contradiction rate must never ship alone.** It pairs with **ℱ_env liveness** (dimension 4) as its counterweight, exactly as note 11's grid pairs fidelity with diversity. **Report them as a pair or the metric is actively harmful** — it will select for models that assert nothing.

**Falsifiable prediction, cheap to test on the existing 3,135-dialogue corpus:** contradiction rate and world-liveness are **positively correlated across models** (more world → more contradictions). If true, neither is interpretable alone, and the real dimension is the **frontier** — contradictions per unit of asserted world state, i.e. the complexity-adjusted rate of §5.5. **This is the single highest-value experiment in this note and it needs no new data.**

---

## 8. Priority recommendations

0. **⭐⭐ Test record fidelity vs turn depth BEFORE building the record (§5.2b).** There is a published negative result against incrementally-maintained records ("accumulating inconsistency"; worst *and* most expensive). Reconstruct the record at turns 10/50/90, score against raw transcript. **If it rots faster than the signal it buys, §4.2 is dead.** Cheap, decisive, and it gates items 3–7.
1. **⭐ Measure our own contradiction prevalence first.** Everything in §5 hinges on it; 4.27% is Blenderbot-era assistant chat. **Blocks everything else.**
   - While you're there: **run our own α on contradiction labels** (§5.2), and **re-annotate at atomic-claim granularity** to test whether our α=0.25–0.34 is partly a unit-of-judgment artifact (§0). Both are cheap and both could move the platform's headline claim.
2. **⭐ Ship Rule Adherence (IFR) first.** Lane 1, no judge, proven range across four benchmarks, and the long-horizon version is a genuine contribution — **nobody has run verifiable-constraint checking past 5 turns** (Multi-IF: 3; SysBench: 5). Ours is 100. **Copy Multi-IF's "conflict removal" stage**: if scene rules can contradict each other, a violation is ambiguous between decay and impossibility and the metric silently dies. **Any scene-rule authoring tool needs a satisfiability check.**
   - ⭐ **Report the constraint budget, not just the violation count.** FollowBench's **CSL = 3.3** says ~3 simultaneous constraints is the reliable ceiling; our character cards carry many more. **Measure our cards' constraint count first** — if the median card is at 10+, then rule violation is structurally guaranteed and the actionable product output is *"your card is over budget, and here is which constraint gets dropped first,"* not *"the model failed."* That reframes the deliverable from a scoreboard into a **diagnostic customers can act on**, and it is the most commercially useful idea in this note.
3. **⭐ Author a schema-slice scenario set.** Small typed state block per scenario. Gets a Lane-1 checker *and* the labeled set that lets us measure the prose auditor's precision without a big human spend (§4.2). **This is how we escape the α=0.3 trap without pretending.**
4. **⭐ Build ℱ_env liveness.** The 49.7% prior says models are at chance; no roleplay benchmark measures it; it is the counterweight that keeps dimension 6 honest. **Our most defensible novel dimension.**
5. **Run the §7 correlation now.** Contradiction rate vs asserted-world-state, across the 11 models, on existing data. Zero new collection. It decides whether dimension 6 is interpretable at all.
6. **Contradiction rate: aggregate only, complexity-adjusted, with published precision.** Never a per-turn flag. Never per-cell (note 10 Finding 3). Evidence citation mandatory.
7. **Adopt bi-temporal edges + `asserted_by`.** Invert Zep's "prioritize new information."
8. **Measure this dimension's own noise floor before it ships** — note 10's gate. Expect σ_within to be *worse* than repetition's, since auditor stochasticity stacks on generation stochasticity.
9. **Schedule human re-baselines.** Goodhart is measured (15×), not hypothetical.
10. **Update [note 08](08-multiturn-conversation-eval.md) §3.2** to cite LongMemEval's knowledge-update and claim the narrower (still real) gap. **Add a 4th vote to §1.0's orthogonality thesis:** LongMemEval has **Llama-3.1-70B dropping 55.1% vs 8B's 36.1%** — the bigger model is the worse model on conversational memory, again.

---

## 9. ⚠️ Data-integrity warning for this whole source set

**WebFetch fabricated an entire results section during this research.** Asked for the Skill Check PDF, it returned confident, specific, entirely invented numbers — "50+ sessions", GPT-3.5 and rule-based baselines, 1–5 rubrics, means of 3.8/5.0, and **Fleiss' κ = 0.73**. **None of it exists in the paper.** It was caught only because the invented numbers contradicted the abstract. The real paper: 90 manual pass/fail unit tests, no rubrics, no IAA.

Two further errors were caught by primary verification in this note:
- A search summarizer attributed the **symmetry/asymmetry** narrative-graph formalism to **GENEVA**. It is not GENEVA's — it belongs to a different 2026 paper ([src](../sources/game-symmetry-twine-repair.md)).
- **DECODE's published Table 4 has an arithmetic typo** (count 6,214 vs ratio 65.28%; the self-consistent value is **4,122** at N=6,314), and its "3817" is **"381" + footnote marker 7** — the true prevalence is **4.27%**, confirmed against the paper's own 95.73% majority baseline.

**Rule going forward: any number sourced from a PDF summarizer is unverified until re-extracted from primary text.** The numbers in [game-decode-contradiction](../sources/game-decode-contradiction.md), FIREBALL, CRD3, CALYPSO, D&D-Dialog and Story Shaping were re-extracted locally via pypdf and arithmetic-checked. Files that were not primary-verified say so in-file.

---

## 10. Source index

**Simulator-seat / world-state:**
[game-bytesized32-state-prediction](../sources/game-bytesized32-state-prediction.md) ⭐ ·
[game-bytesized32](../sources/game-bytesized32.md) ·
[game-skill-check](../sources/game-skill-check.md) ⭐ ·
[game-fireball](../sources/game-fireball.md) ⭐ ·
[game-symmetry-twine-repair](../sources/game-symmetry-twine-repair.md) ·
[game-score-narrative-consistency](../sources/game-score-narrative-consistency.md)

**Contradiction / consistency detection:**
[game-decode-contradiction](../sources/game-decode-contradiction.md) ⭐⭐ ·
[game-narrative-consistency](../sources/game-narrative-consistency.md) ⭐ ·
[game-entity-tracking](../sources/game-entity-tracking.md) ⭐ ·
[game-dialogue-nli](../sources/game-dialogue-nli.md) ·
[game-selfcheckgpt](../sources/game-selfcheckgpt.md)

**Memory / state record:**
[game-zep-graphiti-temporal-kg](../sources/game-zep-graphiti-temporal-kg.md) ⭐ ·
[game-longmemeval](../sources/game-longmemeval.md) ⭐

**Rule adherence (verifiable constraints):**
[game-multi-if](../sources/game-multi-if.md) ⭐ ·
[game-ifeval](../sources/game-ifeval.md) ⭐ ·
[game-followbench](../sources/game-followbench.md) ⭐ ·
[game-sysbench](../sources/game-sysbench.md) ⭐

**Agency / narrative:**
[game-illusion-of-agency-fendt](../sources/game-illusion-of-agency-fendt.md) ⭐ ·
[game-agency-reconsidered](../sources/game-agency-reconsidered.md) ·
[game-agency-relevance-thue](../sources/game-agency-relevance-thue.md) ·
[game-chadpod-decision-points](../sources/game-chadpod-decision-points.md) ·
[game-interactive-drama-agency](../sources/game-interactive-drama-agency.md) ·
[game-story-shaping](../sources/game-story-shaping.md)

**TTRPG / GM:**
[game-rpgbench](../sources/game-rpgbench.md) ⭐⭐ ·
[game-calypso](../sources/game-calypso.md) ·
[game-crd3](../sources/game-crd3.md) ·
[game-dnd-dialog-challenge](../sources/game-dnd-dialog-challenge.md) ·
[game-static-vs-agentic-gm](../sources/game-static-vs-agentic-gm.md) ·
[game-ai-dungeon-drift](../sources/game-ai-dungeon-drift.md)

**Knowledge-graph / long-doc consistency:**
[game-kg-dialogue-consistency](../sources/game-kg-dialogue-consistency.md) ·
[game-long-document-nli](../sources/game-long-document-nli.md)

**Player-seat (limited transfer — but see note on ground-truth engines below):**
[game-balrog](../sources/game-balrog.md) ·
[game-tales](../sources/game-tales.md) (suite) ·
[game-textworld](../sources/game-textworld.md) ·
[game-jericho](../sources/game-jericho.md) ·
[game-alfworld](../sources/game-alfworld.md) ·
[game-scienceworld](../sources/game-scienceworld.md) ·
[game-gamebench](../sources/game-gamebench.md) ·
[game-lmrl-gym](../sources/game-lmrl-gym.md) ·
[game-social-deduction](../sources/game-social-deduction.md) ·
[game-cicero-diplomacy](../sources/game-cicero-diplomacy.md)

> **Why the player-seat cluster is still worth keeping.** These evaluate a capability we don't sell (LLM as *player*), so their headline scores don't transfer. But **TextWorld and Jericho are generative engines with ground-truth state**, which is the property §4 says we can't get from prose — they are the reference implementations of "the simulator *is* the label." If we ever build the schema-slice scenario set (§8.3), their state representation is the prior art to copy.
