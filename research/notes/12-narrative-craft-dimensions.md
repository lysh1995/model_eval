# 12 — Narrative Craft Dimensions: What Makes an AI a Good STORY Partner

**Scope:** 18 sources in [`../sources/narrative-*.md`](../sources/) — the interactive-drama canon (Façade, Mimesis, IDA, emergent narrative), improv theory (Johnstone) and its only live LLM test, LLM story-generation eval (Dramatron, StoryER, Re3/DOC, FlawedFictions), mixed-initiative dialogue theory, and the one roleplay benchmark that actually ships a storytelling dimension (RMTBench).

**Companion notes:** [01](01-roleplay-benchmarks.md) (persona/benchmark dimensions), [03](03-creativity-measurement.md) (creativity/aesthetics), [08](08-multiturn-conversation-eval.md) (multi-turn). This note deliberately does not re-derive HANNA, TTCW, or CoSER — see 03.

---

## 0. The five findings that should drive the design

1. **Our product is a strong-autonomy emergent-narrative system with no drama manager, and "believable locally, structureless globally" is that architecture's known, documented, 25-year-old failure mode.** ([Riedl & Bulitko](../sources/narrative-riedl-bulitko-interactive-narrative.md), [Aylett](../sources/narrative-aylett-emergent-narrative.md)) We are not discovering a novel problem. We are rediscovering the narrative paradox. **DOC's +22.5% plot-coherence gain over Re3 came purely from adding a planning layer** ([DOC](../sources/narrative-storyer-doc-re3.md)) — quantitative evidence the deficit is architectural, not scale.

2. **Narrative craft is a property of a TRAJECTORY, not a response.** Riedl & Bulitko state it outright: global structure "cannot be achieved by looking at any single world state in isolation." Every dimension below is session-level. This is the same shape as note 03's population-vs-per-response split, arrived at independently by a different field. **It has schema consequences: like homogenization, these metrics have no per-response value.**

3. **The field already ships a 4:1 narrative-to-persona dimension balance — we're inverted.** [Drama-Interaction](../sources/narrative-drama-interaction-llm.md) (ACL Findings 2024) scores Scenery/Narration/Transition/Guidance vs *one* persona dimension. Note 01's table has ~9 persona-ish dimensions and an almost-empty Narrative column.

4. **The move that unlocks everything: replace RATING with TAGGING and DETECTION.** Four independent literatures converge on the same design — [FlawedFictions](../sources/narrative-flawedfictions-plot-holes.md) (inject a known plot hole, measure detection), [ProactBench](../sources/narrative-proactive-dialogue-initiative.md) (624 authored triggers, measure recall), [Drama-Interaction](../sources/narrative-drama-interaction-llm.md) (authored transition triggers, score 7/4/1), [Propp](../sources/narrative-propp-story-grammars.md) (closed-vocabulary function tagging). **Our α=0.25–0.34 is a *rating* problem. Tagging and detection are different tasks with different agreement profiles.**

5. **[NarraBench](../sources/narrative-narrabench-taxonomy.md) reframes our headline finding, and it's a better story.** It tags every narrative aspect as **deterministic / consensus / perspectival**. Our α=0.25–0.34 isn't "humans can't agree on quality" — it's **"we scored perspectival aspects with a consensus instrument."** The fix isn't a better judge; it's sorting dimensions by variance class and instrumenting each appropriately. **Adopt D/C/P as a mandatory field on every dimension.**

---

## 1. Why persona fidelity and narrative craft are genuinely different — and in tension

This is not a gap we invented. **Riedl & Bulitko named it in 2013**, verbatim:

> "There is a tension between the needs for NPCs to act consistently with the narrative and the need to act consistently with their own character and settings."

Their entire "virtual character autonomy" axis *is* this trade-off. A model can max persona fidelity by refusing to serve the story — and the literature has a name for that pole (**strong autonomy**) and a name for its failure (**the narrative paradox**).

**The empirical corroboration is unusually strong and comes from three independent professional communities** ([practitioner discourse](../sources/narrative-practitioner-discourse-failure-modes.md)):

| Community | n | Complaint |
|---|---|---|
| Improvisers (Edinburgh Fringe) | cast + 109 audience | AI **"ignorant of the scenes" = 76/100** — higher than "machine like" (65.69). "He makes it difficult to yes and." |
| Playwrights (Dramatron) | 15 professionals | "The stories do not finish." "Show, not tell." **15/15** noticed generation loops. |
| Builders (Bicking) | 1 | "An entity floating in the ether until… 'user' comes up and says 'hi'." "**You can never stop talking.**" |

**None of them complain that the character breaks character.** The dominant *audience-perceived* failure is scene-ignorance (76), not roboticness (65.69). We are weighting the wrong axis.

---

## 2. THE DIMENSION SET

Format: **name | definition | observable correlate | judge-free? | validation | failure mode caught**.
**D/C/P** = NarraBench variance class (deterministic / consensus / perspectival).

### ═══ TIER 1: MEASURABLE AS VIOLATION / COUNTABLE EVENT ═══
*Real denominators. Bounded. Comparable across models by construction. These are the answer to α=0.25–0.34.*

---

**N1. Narrative Load Elasticity** ⭐ *my pick for the headline dimension*

| | |
|---|---|
| **Definition** | The degree to which the AI's share of narrative work *responds inversely* to the user's. A good scene partner carries the story when the user goes passive and yields when the user drives. |
| **Observable correlate** | Per turn, count for each party: new story entities introduced, topic shifts initiated, discourse obligations placed, scene changes proposed. **Metric = correlation between user-load and AI-load across turns.** Negative = adaptive. Zero/positive = not adapting. |
| **Judge-free?** | **Mostly.** Counting requires a tagger (closed-set), not a rater. |
| **Validation** | ❌ **None. This is our synthesis**, from Aylett's "narrative weight… shared by author and players" + the A.L.Ex burden-shifting observation. Unvalidated. |
| **Catches** | Passivity (AI load flat-low), monologuing/over-narrating (AI load flat-high, ignores user), the treadmill. |
| **D/C/P** | Consensus (the tagging step) |
| **Probe** | Two scripted conditions — **passive user** vs **dominant user**. Diff the AI's load. Cheap: 2× generation. |

**Why this is the pick:** it directly answers "who drives the scene," it's a *derivative* (note 03: report slopes, not levels — robust to prompt quirks), and the two-condition probe means we never have to ask a judge "was it proactive?" — **we watch what the model does when the user stops helping.**

⚠️ **The static ratio is the wrong statistic.** A model doing 100% of the narrative work is railroading, not excelling. Elasticity, not share.

---

**N2. Offer Response Profile (blocking / wimping / accepting)** ⭐ *the highest-confidence import*

| | |
|---|---|
| **Definition** | Johnstone's calculus. Every user turn contains **offers** (asserted facts, proposed actions, emotional bids). Each AI turn is classified per offer: **accept+build** ("yes, and"), **accept-only** (**wimp**), **block** (negate the offer), **sidetrack** (neither affirm nor engage), **stall/bridge** (defer). |
| **Observable correlate** | **Block rate** = offers contradicted / offers made (NLI contradiction against user-asserted propositions). **Wimp rate** = offers accepted with zero new elements added. |
| **Judge-free?** | **No — but the judgment moves to NLI**, a task with human agreement well above 0.8. This is the honest framing: not "judge-free," but *"the judgment is relocated to a task judges are good at."* |
| **Validation** | ❌ No LLM study operationalizes this. Johnstone is 1979 theory; [Vickers](../sources/narrative-yes-and-vickers.md) is an open-access definition with **zero empirical validation** (its "interdisciplinary validation" is argument-by-analogy). Improvisers' testimony is qualitative, n small. |
| **Catches** | **Sycophancy = wimping** (accept-without-and). Refusal-as-blocking. "Not giving performers much to work with." |
| **D/C/P** | Deterministic-ish (contradiction) / Consensus (offer parsing) |

**Why it matters:** block and wimp **look like opposites** (refusal vs agreement) and are **both failures**; block and stall **look nothing alike** and **produce the same outcome**. Any single "engagement" score collapses all three. **A violation taxonomy doesn't.** This is the core argument for countable events over Likerts.

**Status insight ([Johnstone](../sources/narrative-johnstone-impro-offers-blocking.md)):** "low-status players tend to accept, and high-status players to block." **Sycophancy and refusal are the two symmetric status pathologies** — an RLHF'd model plays low-status (wimps) by default and high-status (blocks) near safety boundaries. Both destroy scenes.

⚠️ **Unit test:** *"Welcome to my home"* → *"No, this is an office building."* Ship this as a fixture.

---

**N3. Scene Transition / Advancement (the 7/4/1 metric)** ⭐ *most directly liftable*

| | |
|---|---|
| **Definition** | Does the scene change when it should? [Drama-Interaction](../sources/narrative-drama-interaction-llm.md) authors declare transition triggers in the script and score: **7** = trigger detected + transition executed; **4** = trigger detected, transition botched; **1** = otherwise. |
| **Observable correlate** | Classification against **authored trigger annotations**. A disguised confusion matrix. Separates *detection* from *execution*. |
| **Judge-free?** | **YES.** Answer key comes from our probe design. |
| **Validation** | ⚠️ Used in an ACL Findings 2024 paper — **but no IAA and no human correlation reported for it.** Its credibility rests on being objective by construction, not on a validation study. Note: **the authors used GPT-4 for their other four dimensions and hand-checked this one** — they independently concluded a judge couldn't do it. |
| **Catches** | Stalling (never transitions when triggered) **and** railroading (transitions when not triggered). **One metric, both directions.** |
| **D/C/P** | Deterministic |

**Corroboration for the underlying failure is unusually broad:** Bicking ("you can never stop talking"), Dramatron's playwrights ("the stories do not finish"), and this paper — three independent sources, **zero benchmarks in note 01.**

---

**N4. Narrative Agency (branch divergence)** ⭐ *directly answers the brief's question*

| | |
|---|---|
| **Definition** | Does the user's choice change anything? **Divergence between trajectories under different user moves from an identical prefix.** |
| **Observable correlate** | Fix state S (byte-identical prefix — note 01's pinned session start). Issue materially different moves A and B. Continue n turns. Measure **narrative-state divergence**. ≈0 ⇒ the user didn't matter. **Mandatory control:** two *cosmetically* different but *materially equivalent* moves must produce LOW divergence. |
| **Judge-free?** | **Yes if we declare story state per scenario** (Façade-style: affinity, tension, revelation counters). Otherwise needs an NLI/event-diff step. |
| **Validation** | ❌ **None.** The games/HCI field measures *felt* agency via questionnaires ([Game Sense of Agency](../sources/narrative-agency-measurement.md), 12-item, EFA+CFA validated — but 3 of its 4 factors are about interface rendering). **Nobody measures agency as a transcript property.** Our proposal is unvalidated against human perception. |
| **Catches** | Railroading, rails, "your choice didn't matter." |
| **D/C/P** | Deterministic (given declared state) |

**This is Façade's counterfactual baseline made executable.** Façade authored, by hand, "how the beat would play out **in the absence of interaction**." **The cheapest variant: branch A = real user move, branch B = null/passive user.** If the story goes the same place either way, the user does not matter. **Highest value-per-dollar probe in this review.**

⚠️ **Divergence is necessary, not sufficient** — a model could diverge randomly from temperature. **The materially-equivalent control is not optional; without it this metric is gamed by cranking temperature.**
⚠️ **Lexical divergence is the wrong metric** (note 03 §A3: correlates 0.79–0.904 with length). Declared story state is the only fully judge-free route, and it costs per-scenario authoring. **That authoring cost is the real price** — and it's the price Façade paid.
⚠️ **Legibility ≠ agency.** Three sources (Façade 2005, Day & Zhu 2017, Game SoA 2024) independently find agency must be *communicated*. **Our transcript diff can separate real-agency failure from legibility failure; a questionnaire cannot.** That's a case where our objective measure beats the validated instrument.

---

**N5. Railroading Rate (intervention vs accommodation)**

| | |
|---|---|
| **Definition** | [Mimesis](../sources/narrative-mediation-young-mimesis.md)'s complete trichotomy over user attempts to change the fiction: **accommodate** (re-plan to integrate the move), **intervene** (swap the outcome so the plan survives — *the gun jams*), **fail** (story breaks). |
| **Observable correlate** | Intervention has lexical signatures: "you reach for X, **but** —", "**before you can**, …", "she catches your wrist", narrating the user's *failure* to act. Pattern-detectable; fully detectable with a small classifier. |
| **Judge-free?** | Mostly (small classifier) |
| **Validation** | ❌ None. Mimesis reports planner performance, never user experience. |
| **Catches** | Deflection of user-initiated scene changes. |
| **D/C/P** | Consensus |

⚠️ **DO NOT MINIMIZE THIS — CHARACTERIZE IT.** Intervention is a *legitimate* policy in Mimesis. 0% accommodation = railroading; **100% accommodation = wimping.** A naive "lower is better" alert **rewards pure sycophancy.** The healthy range is empirical.

**Preemption is the invisible third form** ([Magerko](../sources/narrative-magerko-boundary-problem.md)): "preemptively, though subtly, steer the player away." The model never says no — it never *offers* the branch. **Invisible to any transcript-level detector; the evidence is absence.** Only visible via **narrative option entropy**: k continuations from a fixed state, measure diversity of *moves offered*. Reuses note 03's population tier. ⚠️ Must not collapse into lexical diversity.

---

**N6. Reincorporation Rate**

| | |
|---|---|
| **Definition** | Johnstone: "remembering incidents that have been shelved and reincorporating them." Does the AI **spontaneously** bring back an element introduced earlier? |
| **Observable correlate** | For each element introduced at turn *t* and dormant *k* turns: is it ever re-raised **by the AI** (not the user)? Rate = AI-initiated reincorporations / shelved elements. Pure count. |
| **Judge-free?** | Mostly (entity tracking) |
| **Validation** | ❌ None. Façade implements it as a mechanic ("reestablish" jdbs; "prefer sequencing beats related to past topics brought up by the player"). No measurement study. |
| **Catches** | Dropped threads; the "goldfish" feel. |
| **D/C/P** | Deterministic-ish |

**This is the twin of memory, and it is NOT memory.** Note 01's memory dimensions ask *"can it recall X when asked?"* (recognition). Reincorporation asks *"does it bring X back to give the story shape?"* (**production**). **This is exactly note 01 §5.2's identified blind spot** — SocialBench tests recognition via multiple choice; nothing tests production. **Absent from every benchmark in note 01.**

**Probe (steal from the A.L.Ex "Wedding Speech" game):** seed *k* independent threads, then force a synthesis moment. Count reincorporations. **Bounded [0,k], real denominator, no judge.**

---

**N7. Plot-Hole / Self-Contradiction Rate**

| | |
|---|---|
| **Definition** | [FlawedFictions](../sources/narrative-flawedfictions-plot-holes.md): "inconsistencies in a storyline that break the internal logic or rules of a story's world." |
| **Observable correlate** | NLI against the story's own prior assertions. **Injected-defect detection** for the benchmark version. |
| **Judge-free?** | **YES** — labels objective by construction. |
| **Validation** | ✅ **The only hard number in this note: LLM story generation introduces plot holes at 100%+ (>2×) the human rate; summarization 50%+.** Performance degrades with length. |
| **Catches** | Continuity collapse. |
| **D/C/P** | Deterministic |

**Why this ports where CoSER's Storyline Consistency doesn't:** note 01 §4 rejected CoSER because it "presupposes a ground-truth reference dialogue from a book." **Plot-hole detection needs no reference — the ground truth is the story's own prior assertions.** It works on original characters and open-ended chat. **This resolves note 01's stated objection.**

**Shares infrastructure with N2** — blocking detection is the same NLI-against-established-propositions shape. Build once, get both.

**"Schrödinger's gun"** (Robertson & Young): contradiction **∧** conveniently-blocks-the-user. The *conjunction* is far more diagnostic than either alone — a contradiction that blocks the user isn't a random error, it's a tell.

⚠️ Domain transfer prose→dialogue is **assumed, not shown**.

---

**N8. Initiative: Task vs Dialogue** ⭐ *best conceptual find after Johnstone*

| | |
|---|---|
| **Definition** | 1997 dialogue theory: **dialogue initiative** = who determines the current focus of discourse. **Task initiative** = who takes the lead developing the plan. **For roleplay, the "task" is the STORY.** |
| **Observable correlate** | **"Placing a discourse obligation on another agent"** — question / request / offer acts. Countable per turn, per party. |
| **Judge-free?** | Mostly (closed-set utterance tagging) |
| **Validation** | ⚠️ Classic schemes (Walker & Whittaker) have published reliability — **I did not retrieve the numbers. Worth doing: a validated initiative-tagging scheme would be a major shortcut.** |
| **Catches** | **The conversational treadmill, precisely.** |
| **D/C/P** | Consensus |

**The treadmill is not a vague complaint — it's a specific configuration: HIGH dialogue initiative + ZERO task initiative.** Chatty, asks lots of questions, never advances the story. Note 01 lumps "Engagement/Proactivity" into one dimension and therefore **cannot see this**. Two orthogonal counters, not one score.

**The "prompt" utterance type** ("uh-huh", "go on") is the classic zero-initiative act **and the LLM companion's signature move.**

⚠️ **Steal the shape, reject the value function.** [Proactivity benchmarks](../sources/narrative-proactive-dialogue-initiative.md) reward *helpfulness*; drama needs *trouble*. **An agent that tops ProactiveBench is a wimp.** Our triggers are "a complication was available here," not "the user needed help."

---

**N9. Scene Closure / Arc Completion**

| | |
|---|---|
| **Definition** | Do scenes and arcs *end*? Are introduced complications ever resolved? |
| **Observable correlate** | **Unclosed dependencies**: complication introduced → ever resolved? (Propp's ordering constraints: `villainy` must be answered by `liquidation of lack`.) Scene-closure events per session. |
| **Judge-free?** | Mostly (tag sequence arithmetic) |
| **Validation** | ❌ None. But **three independent sources name the failure**: Bicking ("you can never stop talking"), Dramatron's 15 playwrights ("the stories do not finish. The character journeys are not complete"), Drama-Interaction (Transition). |
| **Catches** | The endless middle. |
| **D/C/P** | Consensus |

---

**N10. Eventfulness vs Description (the purple-prose axis)**

| | |
|---|---|
| **Definition** | [NarraBench](../sources/narrative-narrabench-taxonomy.md)'s Genettean **"mood: the relationship between eventfulness and description."** [Drama-Interaction](../sources/narrative-drama-interaction-llm.md) independently: **"plot v.s. spectacle"** (Narration vs Scenery). |
| **Observable correlate** | **Ratio: new story events introduced ÷ descriptive tokens.** |
| **Judge-free?** | Mostly |
| **Validation** | ❌ None as a metric. **But two independent sources isolate the construct**, which is the best convergence evidence available for a novel dimension. |
| **Catches** | **Purple prose** — lush description, nothing happens. Directly named in the brief. |
| **D/C/P** | Consensus |

Cheap, and I haven't seen it framed this way elsewhere. Pairs with note 03's slop metrics (which catch *cliché* density; this catches *event starvation*).

---

**N11. Premise-to-Dialogue Leakage ("do not mention the thing")**

| | |
|---|---|
| **Definition** | Dramatron p8: **"Show, not tell: here we are just telling. Just like in improv: 'do not mention the thing'. The element in the log line became the central bit in the generation, and that was repetitive."** |
| **Observable correlate** | Semantic similarity between the character card's **latent** fields and the literal text of dialogue. Card says "secretly lonely" → good scene partner *plays* lonely; bad one *says* "I'm secretly lonely." |
| **Judge-free?** | **Yes** — embedding-only, Tier A. |
| **Validation** | ❌ None. |
| **Catches** | Telling-not-showing; prompt echo. |
| **D/C/P** | Consensus |

⚠️ **The sign is NOT obvious and this could backfire.** Some card→dialogue overlap is *correct* — persona fidelity requires expressing the card. A naive similarity score **penalizes good persona fidelity.** Needs a **latent-vs-surface field annotation** on cards to work. **Promising but genuinely unvalidated — prototype before believing.**

---

### ═══ TIER 2: REQUIRES AESTHETIC JUDGMENT ═══
*Perspectival or consensus-class. Do NOT put these on a leaderboard. Report distributions, use pairwise-vs-fixed-anchors (note 03 §C1), or drop.*

---

**N12. Plot Advancement (RMTBench)** — *the one with real numbers*

| | |
|---|---|
| **Definition** | Verbatim: *"measures the model's ability to steer or enrich the conversation by introducing new information, suggesting further discussion points, or creating compelling scenarios. A successful role-playing LLM prevents the interaction from stagnation and encourages deeper interactions."* |
| **Rubric** | 5-pt. **1** = *"passively answers questions without extending the conversation… dialogue easily becomes stagnant."* **3** = *"expands on topics… but lacks strong initiative, requiring the user to continuously guide the interaction."* **5** = *"actively creates conversational opportunities by introducing new details… crafts vivid scenarios and story elements, using well-placed questions."* |
| **Observable correlate** | **The anchors are a checklist in a Likert costume**: (a) new narrative entities introduced, (b) interrogative acts, (c) scenario elements not in prior context. **Recommend converting back to a checklist.** |
| **Judge-free?** | No as shipped; **mostly yes if converted.** |
| **Validation** | ⚠️ **Agreement-with-majority-vote** (not chance-corrected): PA = **0.84 / 0.86 / 0.85** across 3 annotators — **highest and most annotator-robust dimension** (spread 0.02 vs Character Understanding's 0.63–0.82, spread 0.19). **LLM judge scored PA WORST (0.72) while humans scored it BEST.** |
| **Catches** | Passivity, stagnation. |
| **D/C/P** | Consensus |

⚠️⚠️ **DO NOT COMPARE 0.84 TO OUR α=0.25–0.34.** It is uncorrected agreement-with-majority, and each annotator is *part of* the label they're scored against — heavily inflated. Not comparable to Krippendorff α, PingPong's α, or PersonaGym's κ. **The only honest claim is the RELATIVE one:** within one study under one protocol, **PA agreed better and more uniformly than the persona dimensions did.** That ordering supports our thesis; the absolute number does not transfer.

**The most actionable fact here: humans find PA easy, the judge finds it hard (0.72, its worst).** → **Build objective correlates; don't trust a judge with it.**

**Also steal:** RMTBench's Emotional Expression rubric embeds **"(If the model does not use first-person perspective, please also select 1 point.)"** — **a regex-detectable programmatic override bolted onto a Likert anchor.** Nice pattern for partially de-subjectifying aesthetic rubrics.

**→ ACTION: back-fill RMTBench into note 01's comparison table.** It's missing, and it's the only entry that would put a ● in the Narrative/Story column with a real rubric.

---

**N13. Dramatic Tension / Escalation**

| | |
|---|---|
| **Definition** | Façade: an author-specified **Aristotelian tension arc**; beats selected so "story tension effects most closely match the near-term trajectory." Tension-space formalism: **tension = distance between worldviews/goals**. |
| **Observable correlate** | **If we declare story state:** distance between observed tension trajectory and a target curve — **Freytag as a regression target**. Otherwise: goal-divergence extraction (expensive). |
| **Judge-free?** | Yes *if* story state is declared; otherwise no. |
| **Validation** | ❌ None. Tension-space offers a formalism with worked examples, **no human validation that its tension metric tracks perceived tension.** |
| **Catches** | Flat affect; no stakes; no escalation. |
| **D/C/P** | Perspectival → **do not leaderboard** |

**The formalism explains sycophancy as a NARRATIVE defect, not just an alignment one:** tension = goal-distance; a sycophantic model copies the user's goals; distance → 0; **tension → 0 arithmetically.** Bicking's "floating in the ether until user says hi" is the same finding from the practitioner side: **a character with no independent goal cannot generate tension.**
**→ Cheap probe falling out of this: does the character pursue ANY goal the user didn't give it?**

---

**N14. Character Development / Arc** — *reader-salient, benchmark-absent*

| | |
|---|---|
| **Definition** | Does the character *change*? |
| **Observable correlate** | Weak. Trait-expression drift over a session (must be distinguished from persona *inconsistency* — **and this is genuinely hard: development and drift are the same signal with different signs**). |
| **Judge-free?** | No |
| **Validation** | ⚠️ [StoryER](../sources/narrative-storyer-doc-re3.md) derived it **bottom-up via LDA over real reader comments** (k=10 aspects, cluster-validated) — the only *empirically discovered* dimension set in this review. Corroborated by Dramatron ("the character journeys are not complete"). |
| **Catches** | Static characters. |
| **D/C/P** | Perspectival |

⚠️ **Direct conflict with note 01's persona-consistency dimensions.** Consistency says *don't change*; development says *change*. **Whichever we ship, they must be specified against each other** or they'll fight. Flag as an open design question, not a solved dimension.

---

**N15. Subtext / Show-Don't-Tell (aesthetic form)** — Dramatron's playwrights named it repeatedly. N11 is the objective shadow of this. **Perspectival. Diagnostics only.**

**N16. Interestingness** — [DOC](../sources/narrative-storyer-doc-re3.md) reports **+20.7% absolute** over Re3 in human eval. ⚠️ No IAA; single-shot prose, not dialogue. **Perspectival — the canonical case for pairwise-vs-fixed-anchors (note 03 §C1), never absolute Likert.**

---

## 3. What this literature does NOT give us — read before over-trusting the above

**The interactive-narrative canon built sophisticated architectures and essentially never built measurement instruments.** This is the single most important caveat in this note.

| Source | Dimension set? | Rubric? | IAA? | Human validation? |
|---|---|---|---|---|
| Riedl & Bulitko 2013 | ❌ | ❌ | ❌ | ❌ |
| Façade (Mateas & Stern) | ❌ | ❌ | ❌ | ❌ |
| Mimesis / mediation | ❌ | ❌ | ❌ | ❌ planner perf only |
| Magerko / IDA | ❌ | ❌ | ❌ | ⚠️ system perf |
| Aylett / emergent narrative | ❌ | ❌ | ❌ | ❌ |
| Johnstone | ❌ | ❌ | ❌ | ❌ (1979 theory) |
| Vickers | ❌ | ❌ | ❌ | ❌ (analogy only) |
| Propp | ❌ | ❌ | ❌ | ❌ (1928, much criticized) |
| A.L.Ex improv study | ❌ | ❌ | ❌ | ⚠️ audience survey n≈109; performer free-text |
| Dramatron | ❌ | ❌ | ❌ | ⚠️ 15 experts, qualitative themes, no coding reliability |
| Drama-Interaction | ✅ 5 dims | ✅ 7-pt | ❌ | ❌ GPT-4 sole judge; canon chars = contaminated |
| **RMTBench** | ✅ 7 dims | ✅ 5-pt | ⚠️ uncorrected | ⚠️ 3 annotators, majority vote |
| **FlawedFictions** | ✅ 1 task | n/a | n/a objective | ✅ **objective by construction** |
| StoryER | ✅ LDA-derived | ✅ | ❌ | ⚠️ "high correlation" — **number not extracted** |
| DOC/Re3 | ✅ 4 dims | ✅ | ❌ | ⚠️ +22.5/28.2/20.7% |
| NarraBench | ✅ 50 aspects | n/a | ❌ | ❌ theoretical, English-only |

**Only TWO sources in 18 give a validated, quantitative handle: FlawedFictions (objective by construction) and RMTBench (uncorrected agreement).** Everything else is conceptual vocabulary.

**So the honest position is note 03 §5's DAT lesson, and we should say it out loud: SELL STABILITY, CAVEAT VALIDITY.** These dimensions are deterministic, bounded, and comparable — good regression detectors. **We cannot yet claim they measure "good storytelling."** That claim needs a human calibration study we have not run.

**Other gaps:**
- ⚠️ **Community discourse was NOT successfully sourced.** Reddit/Discord not retrievable via web search; results were SEO listicles. [File](../sources/narrative-practitioner-discourse-failure-modes.md) is thin. **Needs dedicated collection.**
- ⚠️ **A "Narrative Progression" checklist** ("actionable hooks", "clear next conversational handle", "penalizing static confirmations") appeared repeatedly in search-engine summaries. **I could not trace it to any primary source. Possibly search-engine synthesis. Do not cite.** Worth one more look — if real, it's highly relevant.
- ⚠️ **Nearly everything is prose or task-dialogue, not companion roleplay.** Transfer is assumed throughout.
- ⚠️ Professionals' standards ≠ our users'. Note 01's traffic prior (Friendly Interactions 11.1%, Casual Greetings 10.6%, Affection & Comfort 8.0%) says our users are **not staging plays.** **A companion user may WANT a low-tension, high-affirmation partner.** Half these dimensions could be measuring things our users don't want. **This is the biggest open risk in this note.**

---

## 4. Proposed architecture

```
Narrative Craft (per model, per scenario-suite) — SESSION-LEVEL, never per-response
│
├─ TIER 1  countable / violation · answer key from OUR probe design
│   ├─ N1  narrative load elasticity      ← passive-user vs dominant-user probe ⭐
│   ├─ N2  offer response: block / wimp rate  ← NLI vs user assertions ⭐
│   ├─ N3  scene transition 7/4/1         ← authored triggers ⭐ most liftable
│   ├─ N4  branch divergence              ← null-user counterfactual ⭐ cheapest
│   ├─ N5  intervention rate              ← ⚠️ characterize, do NOT minimize
│   ├─ N6  reincorporation rate           ← plant k threads, force synthesis
│   ├─ N7  plot-hole rate                 ← ✅ only validated number (>2× human)
│   ├─ N8  task vs dialogue initiative    ← treadmill = high dlg + zero task
│   ├─ N9  scene closure / unclosed complications
│   ├─ N10 eventfulness ÷ description     ← purple prose
│   └─ N11 premise leakage                ← ⚠️ sign not obvious, prototype first
│
└─ TIER 2  aesthetic · sample · pairwise-vs-anchors ONLY (note 03 §C1)
    ├─ N12 Plot Advancement (RMTBench)    ← convert anchors → checklist
    ├─ N13 tension / escalation           ← perspectival, no leaderboard
    ├─ N14 character development          ← ⚠️ conflicts with persona consistency
    ├─ N15 subtext                        ← diagnostics only
    └─ N16 interestingness                ← perspectival
```

**Every Tier-1 metric gets its ground truth from OUR probe design, not an annotator's opinion.** That is note 01's target-guided probe finding (worth ~17 Pearson points vs ~4 for self-consistency) applied to narrative craft. **Probe design dominates judge choice — again.**

**Non-negotiables (inherited + new):**
1. **Session-level only.** These have no per-response value (like homogenization — schema consequence, note 03 §2).
2. **Declare story state per scenario.** N4/N13 are only judge-free with it. Façade proved it in 2005; Bicking rediscovered it in 2024 ("mushy"). **This is the main authoring cost of the whole programme.**
3. **Tag D/C/P on every dimension.** Perspectival ⇒ never a leaderboard axis.
4. **Length-normalize** (note 03: 0.79–0.904 length correlation) — verbosity leaderboard risk applies to event counts too.
5. **Materially-equivalent control on N4**, or temperature games it.
6. **Never minimize N5.** 100% accommodation = sycophancy.
7. **Noise floor before alerts** (note 03 §4.5).

---

## 5. Recommended next actions

1. **Build N4 (null-user branch divergence) first.** Cheapest, most decisive, directly answers the brief. 2× generation, no judge.
2. **Build N2 + N7 together** — shared NLI-against-established-propositions infrastructure.
3. **⭐ Run StoryER's LDA method over our own thumbs-down comments / support tickets.** Derives companion-native dimensions bottom-up, uses data we already have, and closes the community-discourse gap this review couldn't. **Highest value-per-dollar follow-up in this note.**
4. **Measure our own tagger's agreement FIRST.** If closed-set narrative-move tagging also lands at α≈0.3, the whole tagging-over-rating thesis collapses — **and we want to learn that cheaply, before building on it.**
5. **Retrieve Walker & Whittaker's initiative-annotation reliability numbers.** A validated scheme would be a major shortcut for N8.
6. **Validate N4 against Day & Zhu's agency instrument** before claiming we measure agency.
7. **Back-fill RMTBench into note 01's table.**
8. **Verify the Johnstone quotes** against a physical copy of *Impro* before publishing any rubric wording.

---

## 6. Open questions

- **Do our users even want tension?** Note 01's traffic prior suggests comfort/affirmation dominates. If so, N13/N2's wimp-rate may be measuring a *feature*. **This is the biggest risk to this entire note** and it's answerable from our own data (action #3).
- **Character development vs persona consistency** (N14) — directly contradictory dimensions. Which wins, and specified how?
- **Divergence metric for N4** — lexical is wrong; declared story state costs authoring. What's the middle?
- **Does the practitioner failure taxonomy transfer to companion traffic at all?** Playwrights ≠ our users.
- **N11's sign** — does premise leakage penalize good persona fidelity?
- Is there a real "Narrative Progression" checklist source, or was that search-engine synthesis?
