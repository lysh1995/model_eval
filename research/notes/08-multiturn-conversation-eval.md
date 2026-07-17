# 08 — Multi-Turn / Conversation-Level Evaluation

**Topic:** multi-turn-eval · **Compiled:** 2026-07-16 · **Sources:** `research/sources/multiturn-*.md`

---

## 0. Verdict up front

The project's founding insight is **correct and independently confirmed by at least five separate literatures**, none of which cite each other much. The claim "the unit of evaluation is not the response" is not a design preference — it is forced by the measurement structure of the failure modes themselves.

But the literature sharpens the claim in three ways we did not anticipate, and each has architectural consequences:

1. **The dominant multi-turn failure signal is VARIANCE, not mean.** Laban et al. decompose a −39% multi-turn drop into **−16% aptitude** and **+112% unreliability**. The mean is the minor term. An eval platform that reports means is reporting the small half of the phenomenon. *Our 3-runs-per-dialogue design is not a nicety; it is load-bearing, and 3 is probably too few.*

2. **"Across turns" is not one unit — it is at least three**, and conflating them is a statistical error with a measured cost: **42% of turn-level findings may be spurious** from autocorrelation alone. The conversation is the *sampling unit*; the turn is a *repeated measure*.

3. **The off-policy worry about replayed user turns is real but has been mis-framed** (by us, and by the RL-flavoured literature). It is not compounding drift; it is local incoherence at the seams — measurable and largely controllable. Decisively: **we replay only the *user* half, so error propagation on the assistant side (where drift and looping actually live) stays fully on-policy.** The benchmark that froze the *assistant* half (MT-Bench-101's golden context) documented that doing so manufactures illusory improvement — a warning against a design we aren't using. See §6.

**And one correction to our prior:** we assumed the field averages per-turn scores and that conversation-level aggregation was our idea. **MT-Bench-101 already does min-over-turns, and measured that it beats mean-over-turns by 12 points of human agreement (87% vs 75%) — exceeding human experts' own internal agreement (80%).** That is excellent news framed correctly: our thesis is *externally validated*, not novel. The real gap is narrower and more defensible — **repeated runs × long horizon × large character cohort** (§5).

---

## 1. Unit of analysis, by failure mode

This is the core deliverable. Each row is a claim that the failure mode is **undetectable** at any narrower unit — not merely "better detected" at the wider one.

| Failure mode | Minimum unit | Why narrower units cannot see it | Evidence |
|---|---|---|---|
| **Refusal / OOC break (blatant)** | **Response** | A single response genuinely contains it. This is the *only* failure mode that is honestly per-response — and it's the one the field over-invests in. | — |
| **Breaking character (subtle)** | **Turn-window** | Requires a reference: what did this character sound like 20 turns ago? A response is only "out of character" relative to an established baseline. | Persona Drift: probe-based measurement needs a t=0 anchor |
| **Personality drift** | **Conversation** (turn-indexed) | Drift *is* a slope. A slope is undefined at a point. Any single response is consistent with any drift rate. | Persona Drift (>30% degradation by turn 8–12); When Attention Closes |
| **Repetition / looping** | **Turn-window → conversation** | A repeated sentence is only repeated *with respect to* prior turns. The offending response is individually fine — often *good*. | Neural Text Degeneration (metric defined over a window by construction) |
| **Forgetting established facts** | **Conversation** (fact-position-indexed) | Needs (fact established at turn i) × (recall probed at turn j). Two turns minimum, and the *distance* is the variable of interest. | Lost in the Middle; LoCoMo; RULER |
| **Homogenization across characters** | **Character-cohort** (≥ dozens of characters, fixed turn) | Mathematically undefined for one character. Coverage/Uniformity/LID are population statistics. | Chameleon's Limit |
| **Unreliability / "gets lost"** | **Run-cohort** (same dialogue × N runs) | Undefined for one run. It is a spread between runs, invisible in any single trajectory no matter how long. | Laban et al. (U₁₀⁹⁰) |
| **Judge/eval drift over time** | **Corpus** (across releases) | Requires re-running old dialogues under new judges. | — |

### 1.0 ⭐ The orthogonality thesis — now three independent votes

The single most commercially important claim in this review, reached by three unrelated papers via three unrelated methods:

| Source | Method | Finding |
|---|---|---|
| **Laban et al.** (15 models, 200k conversations) | aptitude/unreliability decomposition | "all models we test exhibit very high unreliability... **regardless of aptitude**" |
| **MT-Eval** (11 models, EMNLP) | paired single-turn control | degradation "**is not correlated with the models' fundamental capabilities**" |
| **MemGPT DMR** (Multi-Session Chat) | conversational fact recall | **GPT-4 scores 32.1% — BELOW GPT-3.5's 38.7%** |

That last one is the most vivid: on *conversational memory*, the stronger model is the worse model. And MemGPT's architecture adds **+60.4 points** where model choice moves **6.6**.

⇒ **Multi-turn behavior is not predictable from single-turn benchmarks — it is a separate axis.** This is the entire commercial thesis of the platform, stated three times, independently, by people who were not trying to state it.

### 1.1 The two findings that most justify the platform

**(a) Per-character fidelity and cross-character diversity are ANTI-correlated.**

> "models with highest per-persona fidelity produce the most stereotyped populations" — *Chameleon's Limit*

Models at ρ>0.9 persona fidelity produce **Cohen's d up to 15.7** between persona groups (human "very large" = d≈2). They are not playing characters; they are playing caricatures. **A model can win every per-character eval and be the worst model in the cohort.** No per-response, per-turn, or even per-conversation evaluation can detect this. It is only visible at a unit that most eval platforms do not have — and that our 95-character × 11-model grid *does*.

**(b) Roleplay tuning makes cohort collapse monotonically worse.**

Qwen3-32B → +SFT → +RL: Coverage **0.64 → 0.56 → 0.49**. MiniMax-M2 → M2-Her (RL): Coverage **0.55 → 0.06**, fidelity ρ **0.95 → 0.41**.

The exact model class our customers ship is the class that degrades on the axis their own benchmarks don't measure. That is the commercial case for the platform in two numbers.

### 1.2 The statistical obligation (do not skip)

*The Autocorrelation Blind Spot* is the counterweight to our own enthusiasm. "Look across turns" is necessary but **not sufficient** — and done naively it manufactures false findings:

> "Researchers often treat each turn as an independent data point, effectively inflating sample size and artificially reducing standard errors."

Our nesting is deep: **turn ⊂ run ⊂ (character × model × language)**. If we pool 100 × 3 × 11 × 95 and call n = 313,500, our CIs are wrong by a large factor. Effective n for cross-model claims is closer to **95 characters** (or 3,135 conversations), not 313,500 turns.

**Mandatory:**
- Mixed-effects models; **random intercepts for character and for conversation**. Character is a **random** effect — we want to generalize to unseen characters, and 95 is a sample.
- Cluster-robust SEs at the **conversation** level.
- **Report ICC per metric.** Drift and repetition will have high within-conversation ICC → far less independent information per turn than raw n implies.
- **The UI must never display turn-pooled n as sample size.** Any CI built on that is a lie.
- Benjamini-Hochberg across the 11-model × 95-character comparison grid.

---

## 2. Does quality degrade monotonically with turn index?

**No. Four independent lines of evidence say the curve is non-monotone.** This is the clearest empirical answer in the whole review, and it invalidates the most natural first implementation (a linear "degradation slope").

| Source | Shape | Numbers |
|---|---|---|
| **Multi-IF** | **Decelerating** — front-loaded damage | Turn 1→3: o1-preview **0.877→0.707** (−19.4%); GPT-4o **0.843→0.631** (−25.1%). **IFR turn 1→2 > turn 2→3.** |
| **Lost in the Middle** | **U-shaped in position** | GPT-3.5-Turbo by gold position: **75.8 / 53.8 / 63.2** (start/middle/end) — 22-pt trough |
| **Laban et al.** | **Cliff, not slope** — "loss-of-middle-turns" | Drop "persists even in two-turn conversations"; models "overly adjust based on the first and last turn" |
| **Time-To-Inconsistency** | **Non-proportional hazard** | PH assumption **violated** (p=0.032, 0.021) ⇒ "drift effects **intensify** over turns" |
| **When Attention Closes** | Explicitly "**non-linear behavior rather than a monotonic decline**" | (exact curve not extracted — flagged) |

**Consequences:**
- Model turn index as **splines or binned strata**, never a linear covariate.
- **Instrument densest in early turns** — the biggest single drop is turn 1→2, and the static-context theorem's `(H−i)` weighting independently predicts early turns dominate.
- **Endpoint-only measurement (turn 1 vs turn 100) can miss a mid-conversation trough entirely.** Probe at many depths.
- Note the tension: Multi-IF says decelerating; Time-To-Inconsistency says intensifying. These are *different failure classes* (constraint adherence vs. semantic consistency) and may genuinely have opposite curvature. **Do not assume one shape across metrics.** Our data can settle this — it's a publishable result.

### 2.1 Are failures absorbing states?

Laban: **"when LLMs take a wrong turn... they get lost and do not recover."**
Multi-IF: o1-preview **corrects ~25%** of unfollowed instructions in later turns (ECR).

**Reconciliation:** Laban's task is *conversational steering under ambiguity* (unrecoverable — the model has committed to a wrong premise). Multi-IF's is *discrete constraint adherence* (recoverable — a forgotten formatting rule can be re-applied). **Different failure classes have different recoverability.** Do not build a platform that assumes "broke character at turn 40" is terminal. Whether companion OOC breaks are absorbing is an **empirical question our dataset can answer** — and the answer determines whether survival analysis (absorbing) or a recurrent-event model (recoverable) is correct. *Measure this before committing to the aggregation.*

---

## 3. Computable metrics

Principle from the sources: **push measurement off LLM judges wherever a deterministic function exists.** PingPong's judge-human Spearman on character consistency is only **0.435–0.460**, with human IAA **α = 0.25–0.34**. The thing we most want to measure is the thing per-turn LLM judging measures *worst*.

### 3.1 Consistency / drift

| Metric | Computation | Unit | Provenance |
|---|---|---|---|
| **Probe-battery drift curve** | Inject out-of-band probes at fixed turn indices (10/30/50/70/90); score with a **deterministic** persona function | conversation | Persona Drift + InCharacter |
| **Programmatic character constraints** | Rule-check card-derived constraints (speech tics, forbidden knowledge, language, name use, formatting) per turn | turn → conversation | Multi-IF (rule-based verifier) |
| **Style-embedding distance from t=0** | Cosine of turn-t style embedding vs. turns 1–5 centroid | conversation | Persona Drift |
| **Turn-to-turn semantic delta** | Cosine between adjacent turns | turn-window | Time-To-Inconsistency |
| **Persona contagion** | Similarity of character voice → user voice over turns | conversation | Persona Drift (models "adopt the persona of the user LM") |
| **StdItem** | SD of same probe across our 3 runs | run-cohort | InCharacter |
| **Aptitude A⁹⁰ / Unreliability U₁₀⁹⁰** | 90th pct; 90th−10th pct across runs | run-cohort | **Laban et al.** |

> **Use turn-to-turn deltas, not distance-from-origin.** Time-To-Inconsistency found *cumulative* drift is **protective** (HR<1, AF 1.4–2.6×) while *abrupt prompt-to-prompt* drift is the killer (**HR≈4.7**). A character that slowly evolves over 100 turns may be fine; one that lurches at turn 43 is broken. This inverts the naive "measure distance from the character card" design.

### 3.2 Repetition

Three units, routinely conflated. Only the middle one is our failure mode:

1. **Intra-response** — Holtzman's classic metric (phrase ≥2 tokens, ≥3× at generation end). Human **0.28%** vs beam **28.94%**. *Low value — modern RLHF'd models rarely do this.*
2. **Inter-turn within conversation** — **self-BLEU across turns**, n-gram recurrence, embedding similarity between turn t and turns <t. ***This is the companion "looping" failure mode and it is invisible per-response.***
3. **Cross-character / corpus** — same catchphrase across characters; **template-skeleton overlap** (Claude-Haiku-4.5: **29%** of self-intros shared an identical skeleton). Ties into homogenization.

> **Critical caveat:** Self-BLEU was defined *across independent generations*; using it *across turns within a conversation* is a **re-definition, not a reuse** — document it. And Holtzman predates RLHF: modern models produce **semantic** repetition (same sentiment, fresh words) that n-grams will **miss**. Budget for embedding-based inter-turn similarity, not just self-BLEU.

Also cheap and judge-free: **Zipf coefficient** per character over the conversation (human ≈0.93) as a vocabulary-collapse signal.

### 3.3 Memory

| Metric | Computation | Unit |
|---|---|---|
| **Fact-recall by establishment position** | (fact at turn i) × (probe at turn j) — report accuracy **as a surface over (i, j)**, never a scalar | conversation |
| **Contradiction rate** | NLI between turn-t claims and earlier established facts | conversation |
| **Recall-vs-distance curve** | accuracy as f(j − i) | conversation |

> **The single highest-value memory finding:** Lost in the Middle shows that with the gold doc mid-context, GPT-3.5-Turbo scores **below its own closed-book baseline (56.1%)** — supplying the information *actively hurt*. Applied to companions: the emotionally significant disclosure from 40 turns ago sits exactly in the positional trough. **The failure mode is aligned with the thing users care most about.** That is the core hazard of the product category, and any eval that only probes recent facts will measure recency and declare victory.
>
> **Open gap:** nobody has run the positional control on *dialogue* history. Conversational distractors are the user's own earlier statements — semantically similar, same speaker, sometimes contradictory. Plausibly harder than NQ distractors, so published numbers may be **optimistic** for our case. This is a genuine contribution available to us.

#### ⚠️ Do not build memory eval on needle-in-a-haystack

The NIAH critique is decisive, and it means "we tested memory with NIAH" is worthless for our purposes:

- **NoCha:** the same models scoring **84.8–89.6% on NIAH** drop to **40.2%** (GPT-4-Turbo) and **19.6%** (Command R — *below the 25% random floor*) on real narrative claims. Even NoCha's *sentence-level* claims — the subset closest to NIAH — reach only **59.8%**. So the gap isn't just "global reasoning is hard": localized retrieval in **real prose** is already far harder than finding a synthetic needle.
- **NoLiMa:** remove lexical overlap and GPT-4o's effective context collapses from a claimed **128K to 8K**; most models to **≤2K**. **NIAH is `grep`.** Our probes must not share surface lexical form with the fact as established, or we will measure string matching.
- **RULER:** claimed context lengths vastly exceed effective ones.

**Consequence:** a companion "remembering" is nothing like retrieving a UUID. It is paraphrased, emotionally loaded, sometimes contradicted, and lexically dissimilar to the probe. Design probes accordingly — **paraphrase every probe away from the establishing turn's wording**, and treat any metric that survives lexical-overlap removal as the only real one.

#### ⭐ The gap nobody has filled: superseded facts

Nothing in the long-context/memory literature evaluates **facts that were later changed** — a preference the user revised, a detail retconned, a relationship that evolved. Every benchmark tests *static* recall: the fact was stated once and stays true.

**Companion conversation is largely made of superseded facts.** "I used to work in finance, but I quit last month." The correct behavior is not recall — it is *belief revision*, and getting it wrong is a distinctive and highly visible failure ("you said you were an accountant?"). This requires knowing both that the fact was established *and* that it was overwritten, i.e. it is irreducibly a conversation-level construct with a temporal ordering.

**This is our most defensible contribution.** The nearest prior art is a temporal-belief-consistency track (Belief Revision Accuracy, Contradiction Resolution Rate) noted in the memory search but not established for companion roleplay. Our 100-turn dialogues almost certainly contain natural supersession events — mine for them.

### 3.4 Homogenization (character-cohort)

Directly from *Chameleon's Limit*, computed over our 95 characters:
- **Coverage** — fraction of human-reference neighborhoods reached (human = 1.0; best model 0.80)
- **Uniformity (Hopkins)** — ~0.5 uniform, →1.0 clustered
- **Complexity (LID)** — human **14.4**; models 4.6–7.3
- **Effective Likert** (inverse Simpson)
- **Template-skeleton overlap %**
- **⭐ Intra- vs inter-persona similarity** — *if intra-persona similarity < inter-persona, the persona is doing no work at all.* (MiniMax-M2-Her: intra 0.75, **below** random inter-persona pairs; 83% of its linguistic variation was stochastic noise.) **Cheap, brutal, run it on day one.**

> **Novel result available to us:** every homogenization study to date is **static/one-shot** (questionnaires, self-intros). Our 100-turn dialogues let us ask what they cannot: **does the cohort collapse FURTHER with turn depth?** Compute Coverage/Hopkins at turn 10 vs 50 vs 90. If characters converge as conversations lengthen, that **unifies persona drift (within-character, over turns) with homogenization (across-character, at a turn) as two projections of one phenomenon** — and the Persona Drift "contagion" mechanism predicts exactly this. This is the most interesting hypothesis in the review.

---

## 4. Aggregation: preserving the catastrophic single turn

**The problem, measured:** GPT-4o's conversation-level *mean* crisis detection was **6.76**, obscuring a **floor of 3.6** during the critical early disclosure turns. The mean is not merely lossy — it is *actively misleading* about the turns that matter most.

### Strategies, ranked

**1. ⭐ Survival analysis / time-to-first-failure — the recommended primary.**

*Time-To-Inconsistency* validates this at **C-index 0.874** over 36,951 turns × 9 models.
- **Event:** first character break / contradiction / loop.
- **Right-censoring:** dialogues that never break are **not "score = 1"** — they are **incomplete observations**. This is the principled answer to "how do I score a dialogue that never broke," and it is exactly what a min/mean cannot express.
- **Use AFT (Weibull), not Cox** — PH was violated, and AFT gave **>48% lower prediction error**.
- Model comparison = log-rank tests across survival curves; covariates = character, language, run.
- **Bonus: this dissolves the autocorrelation problem** — each conversation contributes exactly *one* event time. One observation per conversation. Independence restored.
- Their 8-turn horizon was heavily censored; **our 100-turn dialogues yield far more events and far better power.**
- ⚠️ *Only valid if failures are absorbing.* See §2.1 — if OOC breaks are recoverable, use a **recurrent-event / Andersen-Gill** model instead. Measure first.

**2. ⭐⭐ Min-over-turns — and this is now the best-evidenced claim in the entire review.**

*MT-Bench-101* ran the exact ablation we care about. GPT-4 judge, 100 dialogues, 5 expert annotators, agreement measured against human majority vote:

| Evaluation method | Agreement with humans | Δ |
|---|---|---|
| Human experts (internal) | 80% | — |
| **MT-Bench-101 (min-over-turns)** | **87%** | **+7%** |
| w/o scoring guidelines | 77% | −3% |
| **w/o minimum-value metric (i.e. mean-over-turns)** | **75%** | **−5%** |

> **Switching from min-over-turns to mean-over-turns costs 12 points of human agreement (87% → 75%).**

Their justification is our thesis in their words:
> "a **single failed response can compromise the entire dialogue** in closely related conversational contexts. Moreover, this metric **prevents models from achieving inflated scores** by simply learning patterns from the golden context."

**This is the strongest single empirical result available to us.** It is not an argument that averaging is theoretically lossy — it is a *measurement* that averaging actively destroys alignment with human judgment of a conversation, and that min-aggregation of an LLM judge **exceeds human-expert internal agreement (87% > 80%)**. Note also the second justification: min is an **anti-gaming device**. Ship min/floor statistics as first-class, not as a diagnostic.

*(Also worth noting: detailed scoring guidelines are worth +10 points, 87% → 77%. Rubric quality is not a nicety either.)*

**3. Conversation-level strict accuracy (AND across turns).** Multi-IF's definition: "every instruction, from the first user turn to the current turn, is followed correctly." Same spirit as min. **But it decays geometrically and at 100 turns floors to ~0 for every model, losing all discriminative power.** Keep the spirit, express it as a hazard → which *is* survival analysis. (Survival analysis is the AND rule, made decay-robust.)

> **How min and survival relate at our scale:** MT-Bench-101's dialogues average **3.03 turns**, where min-over-turns is well-behaved. At **100 turns**, a pure min will saturate at the floor for nearly every model — the same discriminative-power problem as the AND rule. **Use min within turn-windows (a rolling floor), and survival across the conversation.** Min is validated at short horizons; survival is what carries it to ours. This is the single most important adaptation in this document.

**4. ⭐ Aptitude / Unreliability decomposition (Laban).** Per (model, character): **A⁹⁰** = 90th pct across runs; **U₁₀⁹⁰** = P90 − P10. Given that unreliability (+112%) dominates aptitude (−16%), **U₁₀⁹⁰ should be a headline number in the product, not a diagnostic buried in a drawer.**
- ⚠️ **N=3 runs is thin for a P90−P10 spread.** Laban used N=10. Flag as a dataset limitation; consider bootstrapping and reporting the CI on U honestly, or resampling more runs for a subset.

**5. First-failure-turn distribution.** Report the histogram, not just the median — the shape is the product insight ("model X is fine until turn 30, then falls off a cliff").

**6. Early-warning.** Their AFT monitor caught **76%** of failing conversations **~2 turns before** the break, at a **19%** false-alarm rate. Directly productizable as a runtime guardrail, not just an offline eval.

### Do NOT
- ❌ Mean-of-per-turn-judge-scores as the headline. It is the industry default (PingPong does exactly this) and it averages away the event.
- ❌ Single-number-per-conversation without a floor statistic beside it.
- ❌ Any aggregate that can't answer "which turn broke, and how long did it survive?"

---

## 5. What the benchmark landscape does (and doesn't) do

Most multi-turn benchmarks compute **per-turn scores and average them**. PingPong — the closest analogue to us (roleplay + user emulation + multilingual + judge ensemble) — scores per turn, has **8 characters** (vs our 95), and **no repeated runs at all** (vs our 3). *It structurally cannot compute unreliability, which Laban and MT-Eval both identify as the dominant term.*

**Honest correction: MT-Bench-101 is the exception and got the aggregation right** — per-turn scoring, per-dialogue reporting via **min**, with the ablation to prove it (87% vs 75%). So "nobody does conversation-level aggregation" is **false** and we should not claim it. What remains true and defensible:

- **No repeated runs anywhere** in this landscape ⇒ nobody can compute the unreliability term that two independent papers call dominant. *This is the real gap.*
- **Short horizons** — MT-Bench-101 averages **3.03 turns/dialogue**; Multi-IF has 3; Time-To-Inconsistency has 8. **We have ~100.** Min-aggregation is validated at 3 turns and saturates at 100 (§4).
- **Character cohorts too small for population metrics** — 8 characters (PingPong) cannot support Coverage/Hopkins/LID. **95 can.**
- **Golden context** — MT-Bench-101 freezes the assistant side, which by their own analysis produces "illusory improvement" (§6.2b). We don't.

So the pitch is not "we invented conversation-level eval." It is: **repeated runs × long horizon × large character cohort** — three axes on which the field is empty, and each unlocks a metric class that is otherwise not computable.

**Adopt from PingPong:** judge ensembling (Spearman **0.499 → 0.604** — a real, measured gain); **interrogator/judge separation** (their own v1→v2 lesson: never let one model both drive user turns and judge the result — *our replay design gets this for free*); **character-card asymmetry** (their interrogator is deliberately *not* shown the character card — if the user-simulator knows the persona, it *cooperates* and drift never surfaces).

> **⚠️ Action item — audit our dataset's user turns for card visibility.** If our user turns were generated *with* character-card access, they are collaborative and will **under-detect drift**. This is a **bigger threat to validity than off-policyness** and is checkable today.

**Language:** Multi-IF measured Chinese meaningfully worse than English (o1-preview **0.773 en / 0.703 zh** at turn 3; GPT-4o **0.631 zh**). PingPong's judge-human correlation differed sharply by language (fluency **0.250 en** vs **0.529 ru**). **en/zh is not a free doubling of the dataset.** Model language as a covariate, validate judges per-language, never pool. Cross-model rankings may *reorder* between en and zh — which is itself a finding worth shipping.

---

## 6. ⭐ Off-policy validity of replayed user turns

**The question:** our user turns were produced against a *different* model. Is replaying them onto a new variant valid?

**Short answer: yes, with bounded and characterizable bias — and it is very likely the best available option.** But the bias runs in the *opposite direction* from the one we feared, and the real risk is somewhere else entirely.

### 6.1 The pessimistic case

Replay = evaluating under `d^data` rather than the on-policy `d^π`. Textbook off-policy evaluation; biased.

**Static-Context Theorem 3.1:** |J(π) − J(π′)| ≤ R_max · Σ(H−i)·ε_i ⇒ **O(H²)** error accumulation across horizon H.

Behavior cloning's **O(T²ε)** vs DAgger's **O(Tε)** is the same result from imitation learning.

**Read the `(H−i)` weight:** a deviation at step *i* is weighted by turns *remaining*. Early-turn mismatches are weighted ~H; late-turn ~1. **The off-policy penalty is concentrated in early turns and decays linearly.** At H≈100, a divergence at turn 5 is ~20× more damaging to validity than one at turn 95.

### 6.2 Why the pessimistic case over-predicts — three independent reasons

**(a) Replay is teacher forcing, not behavior cloning.** In imitation learning the student's own actions move the state, so errors compound. **In replayed dialogue we force the state back on-rails every turn by injecting the original user turn.** The trajectory *cannot* wander — we overwrite the user half of it. There is no hidden accumulator to corrupt. The O(H²) bound assumes free drift; we have re-anchoring. ("Three Regimes of Covariate Shift" is explicit that severity depends on feedback structure — externally re-anchored systems sit in the **benign** regime.)

**(b) ⭐ It has been tested directly, and the answer was "not much."** *Exposure Bias versus Self-Recovery* (He et al., EMNLP 2021) ran **exactly our experiment** one level down (tokens rather than turns): feed a model **ground-truth prefixes it did not generate** vs. its own, and measure.

> "the distortion induced by the prefix discrepancy is **limited, and does not seem to be incremental during the generation**."

They identify a **self-recovery ability**: LMs re-condition on the *visible context* rather than on a drifted hidden state. Their conclusion: exposure bias is **"substantially less problematic than widely believed."**

**(c) The bias direction is optimistic, not pessimistic.** Because replayed turns keep dragging the conversation back onto a coherent path the model didn't earn, **replay will UNDER-estimate the model's true multi-turn failure rate.** It is a *conservative* estimator of badness. For an eval platform, a known-conservative bias is a far more comfortable position than an unknown one — we under-claim failures rather than inventing them.

### 6.2b ⭐ The controlled experiment already exists — and it clarifies exactly where we sit

*MT-Bench-101* faced our question head-on and ran the ablation (ChatGLM3-6B, golden context vs. self-predicted context):

> "using the golden context as historical information leads to an **increase in the model's scores over turns**. This improvement is attributed to the golden context supplying the model with data for **in-context learning**... **Conversely, employing self-predicted context as dialogue history results in the accumulation and propagation of errors from earlier incorrect responses, causing a gradual decline in scores.**"

And their per-turn analysis concludes that **every upward turn-index trend they observed was an artifact** of the clean history:
> "This phenomenon **does not reflect a true enhancement** in performance... resulting in an **illusory improvement in performance**."

They then deliberately chose golden context anyway, for fairness:
> "evaluating only the newest response of the LLMs while maintaining consistency with the conversation history also **promotes fair evaluation**."

**Two conclusions, and the second is the important one:**

**(1) It confirms §6.2(c) empirically, and strengthens it.** Replayed/curated history doesn't merely under-estimate degradation — under full golden context it can *invert the curve* and manufacture apparent improvement via ICL. The bias is optimistic, and larger than "conservative" implies.

**(2) ⭐ But we are NOT in MT-Bench-101's regime, and the distinction is the crux of our whole design.** There are three regimes, not two:

| Regime | User turns | Assistant turns | Error propagation | ICL inflation |
|---|---|---|---|---|
| **MT-Bench-101 golden context** | fixed | **fixed (curated)** | ❌ designed out | ⚠️ severe — model copies style from clean history |
| **⭐ Our design** | **fixed (replayed)** | **self-generated** | ✅ **preserved** | ✅ minimal — no clean assistant text to copy |
| **Fully live** | simulated | self-generated | ✅ preserved | ✅ none (but simulator bias, §6.3) |

**We fix only the USER half. The model still reads its own prior outputs and still propagates its own errors.** Drift, looping, and answer-bloat all live on the *assistant* side of the transcript — and our design leaves that side entirely on-policy. There is no curated assistant text for the model to ICL its way into looking good.

⇒ **The MT-Bench-101 result is a warning against a design we are not using, and an endorsement of the axis that matters.** Their golden context deletes the failure mode; ours preserves it. This is the sharpest available answer to "isn't replay invalid?" — *it depends entirely on which half you replay, and we replay the harmless half.*

### 6.3 The alternative is worse — and this is the decisive argument

"Just use a live LLM user simulator" trades a bounded, known-direction bias for a **large, measured** one. *Mind the Sim2Real Gap* (31 simulators vs **451 real humans**, 165 τ-bench tasks):

- Best simulator **USI 76.0** vs human **92.9**
- **"1.0% of GPT-4o turns are short vs. 29.0% for humans"**
- **"49.0% of GPT-4o turns are polite vs. 15.3% for humans"**
- Simulators pivot strategy **19.1% / 16.5% vs 8.4%** for humans
- **Agent success rates inflate from 63.6% (human) to 77.8%** — simulators create an **"easy mode"**
- LLM evaluators inflate human-likeness by **+1.11**
- **Simulators front-load information; humans reveal incrementally**

Two of these are *fatal specifically for us*:

1. **⭐ Front-loading destroys the exact failure mode we exist to measure.** Laban's `Concat` condition (all information delivered up front) recovers **95.1% of single-turn performance** — i.e. the multi-turn penalty *vanishes*. A simulator that front-loads **erases the phenomenon.** Our replayed turns, if they preserve incremental human-like reveal, preserve the failure mode. **Replay is off-policy but keeps the signal; live simulation is on-policy but deletes it.**

2. **Simulator stylistic uniformity would MANUFACTURE homogenization.** If every user turn sounds the same, characters converge — and we'd measure the simulator's collapse and attribute it to the model. This would corrupt our headline cohort metric at the source.

Also: uncalibrated simulators invite **reward hacking** — Naive Interactive collapsed document quality to **26.1 BLEU** vs 33.8 for static. **A bad simulator is an unbounded estimator; replay is a bounded one.**

And replay gives us **interrogator/judge independence for free** — fixed data cannot collude with the judge. PingPong had to redesign v1→v2 to get this.

### 6.4 The actual risk — and it's not what we thought

Combining the sources, the residual threat is **not** compounding drift. It is **local incoherence at the seams**: a replayed user turn may reference something the new model never said ("as you mentioned, you're a doctor" — it never said that). This is an off-distribution **input**, not an accumulated error.

**And this is precisely the highest-hazard condition in the survival data.** A non-sequitur user turn *is* an abrupt prompt-to-prompt semantic jump — **HR ≈ 4.7**, the single strongest predictor of inconsistency, while *cumulative* drift was **protective**.

⇒ **Replay's true failure mode is that it may INDUCE the very hazard we're measuring, as an artifact.** Not by drift, but by seams.

**Good news: this is per-turn, measurable, and controllable.**

### 6.5 Recommendations — concrete

1. **Instrument seam coherence.** Per turn, compute semantic discontinuity between the model's reply and the *next* replayed user turn. This is the direct observable of off-policyness. Cheap (embeddings).
2. **Use it as a covariate, not a filter.** Include seam-discontinuity in the survival model. If drift is explained by *seam artifacts* rather than turn depth, we'd otherwise ship a false finding.
3. **Report a seam-divergence curve by turn index.** Per §6.1's `(H−i)`, validity damage concentrates early. If seams stay coherent for the first ~10 turns, the worst of the bound is inert.
4. **⭐ Run the self-recovery check on our own data.** For a subset: compare turn-N behavior under (a) replayed history vs (b) the model's own self-generated history, same character. If He et al.'s self-recovery transfers to the turn level for instruction-tuned models, they agree — and the off-policy question is *empirically closed for our setup* rather than argued from analogy. **This is the highest-value experiment in this document and it is cheap.**
5. **Audit user turns on the Sim2Real D1–D4 axes** (communication style, information patterns, clarification, error reaction) against human reference distributions. Quantifies how human-like our fixed turns actually are — the USI framework is a ready-made instrument.
6. **Audit for character-card visibility** (§5). If the user turns were generated *seeing* the card, they're collaborative and under-detect drift. **Bigger threat than off-policyness.**
7. **State the bias direction in the product.** "Replayed user turns make this a conservative estimate of multi-turn failure" is defensible, honest, and a selling point.

### 6.6 Framing for skeptics

> **We replay only the USER half of the transcript.** The model still generates its own assistant turns, reads its own prior outputs, and propagates its own errors — so drift, looping and bloat all remain fully on-policy, because they live on the assistant side. MT-Bench-101 showed that freezing the *assistant* side (golden context) deletes the failure mode and manufactures illusory improvement via in-context learning; we don't do that.
>
> What remains is off-policy in the **teacher-forcing direction**: low variance, biased *conservative* on conversational steering, prone to **local coherence artifacts at the seams** rather than compounding drift. The theoretical O(H²) worry is a **worst-case bound that assumes free drift**; we re-anchor every turn, and the one paper that tested prefix mismatch directly found distortion **"limited and not incremental."**
>
> The on-policy alternative — live LLM user simulators — is **measurably worse**: it inflates agent success by ~14pp, front-loads information in a way that *erases* the multi-turn penalty entirely (95.1% recovery), and imposes a stylistic uniformity that would manufacture the very homogenization we're trying to detect.

---

## 7. Open questions our dataset can uniquely answer

1. **Does cohort homogenization increase with turn depth?** (Coverage/Hopkins at turn 10/50/90.) Would unify drift and homogenization as one phenomenon. **Most interesting hypothesis here.**
2. **Is the positional (U-shaped) memory effect the same for dialogue history as for documents?** Conversational distractors are the user's own prior statements — plausibly harder. Nobody has run this control on dialogue.
3. **Are companion OOC breaks absorbing or recoverable?** Determines survival vs. recurrent-event modeling. **Blocks the aggregation decision — answer first.**
4. **Does self-recovery hold at the turn level for instruction-tuned models?** Closes the off-policy question empirically. (§6.5.4)
5. **Do drift curves differ en vs zh at equal turn count?** Attention-decay theory predicts drift tracks *cumulative tokens*, not turns — different tokenization makes this a natural experiment.
6. **Does U₁₀⁹⁰ (unreliability) rank models differently from mean score?** If yes — and Laban predicts yes — that alone justifies the platform.
7. **Do drift metrics have opposite curvature across failure classes?** (§2 tension: Multi-IF decelerating vs Time-To-Inconsistency intensifying.)

---

## 8. Priority recommendations

| # | Action | Basis |
|---|---|---|
| 0 | **Never mean-over-turns as a conversation score. Rolling min within turn-windows + survival across the conversation.** | ⭐ MT-Bench-101 (87% vs 75%) |
| 1 | **Survival analysis (Weibull AFT) as the primary conversation-level verdict**, with right-censoring — *after* settling §7.3 | Time-To-Inconsistency (C-index 0.874) |
| 2 | **Report U₁₀⁹⁰ as a headline metric**, not a diagnostic — no competitor can compute it | Laban (+112% vs −16%) |
| 3 | **Mixed-effects / cluster-robust SEs at the conversation level; never report turn-pooled n** | Autocorrelation Blind Spot (42%) |
| 4 | **Cohort metrics (Coverage/Hopkins/LID) over the 95 characters** — unavailable to competitors | Chameleon's Limit |
| 5 | **Run the intra- vs inter-persona similarity check immediately** — one embedding pass, brutal signal | Chameleon's Limit |
| 6 | **Instrument seam coherence; use as survival covariate** | §6.4 |
| 7 | **Run the self-recovery check** (replayed vs self-generated history) | §6.5.4 |
| 8 | **Audit user turns for character-card visibility** | PingPong v1→v2 |
| 9 | **Deterministic probes + programmatic constraints over LLM judges** where possible | PingPong ρ=0.46, α=0.25 |
| 10 | **Turn-to-turn deltas, not distance-from-origin** | Time-To-Inconsistency (cumulative drift protective) |
| 11 | **Model turn index non-linearly; instrument densest early** | Multi-IF, When Attention Closes |
| 12 | **Treat language as a covariate; validate judges per-language** | Multi-IF, PingPong |
| 13 | **Judge ensembling** | PingPong (0.499→0.604) |
| 14 | **Build a Concat-style flattened single-turn control** — proves failures are conversational, not informational | Laban, MT-Eval, Multi-IF (3 votes) |
| 15 | **Flag N=3 runs as thin for P90−P10**; bootstrap CIs on U; consider more runs on a subset | Laban used N=10 |
| 16 | **Paraphrase memory probes away from the establishing turn's wording** — else we measure `grep` | NoLiMa (128K→8K), NoCha |
| 17 | **Mine the dataset for superseded facts** (revised preferences, retcons) — most defensible novel contribution | §3.3 gap |
| 18 | **Report turn-depth curves per failure axis, never pooled** — trends are task-dependent and may have opposite curvature | MT-Bench-101 |

---

## 9. Source index

| File | Role |
|---|---|
| `multiturn-lost-in-conversation.md` | ⭐ −39%, aptitude/unreliability decomposition, Concat control |
| `multiturn-persona-drift.md` | ⭐ >30% drift by turn 8–12, attention decay, contagion, probe method |
| `multiturn-persona-collapse-homogenization.md` | ⭐ cohort unit; fidelity/diversity anti-correlation |
| `multiturn-time-to-inconsistency-survival.md` | ⭐ survival aggregation; abrupt vs cumulative drift |
| `multiturn-exposure-bias-self-recovery.md` | ⭐ off-policy counterweight — distortion "limited, not incremental" |
| `multiturn-sim2real-gap-user-simulation.md` | ⭐ the live-simulator alternative is worse |
| `multiturn-static-context-distribution-shift.md` | Theorem 3.1, O(H²), (H−i) weighting |
| `multiturn-covariate-shift-imitation.md` | DAgger/BC theory; the teacher-forcing disanalogy |
| `multiturn-autocorrelation-blind-spot.md` | ⭐ 42% spurious; conversation = sampling unit |
| `multiturn-multi-if.md` | turn 1→3 drops; conversation-level strict accuracy; zh gap |
| `multiturn-lost-in-middle.md` | U-shape; below-closed-book result |
| `multiturn-pingpong-roleplay.md` | closest analogue; judge correlation ceilings |
| `multiturn-incharacter.md` | probe batteries; personality as latent construct |
| `multiturn-neural-text-degeneration.md` | repetition/self-BLEU/Zipf definitions |
| `multiturn-when-attention-closes.md` | non-monotone degradation (⚠️ partial extraction) |
| `multiturn-mt-bench-101.md` | ⭐ min-vs-mean ablation (87% vs 75%); golden-context experiment; task-dependent turn trends |
| `multiturn-mt-eval.md` | ⭐ degradation "not correlated with fundamental capabilities" |
| `multiturn-memgpt.md` | ⭐ DMR: GPT-4 (32.1%) < GPT-3.5 (38.7%) on conversational recall |
| `multiturn-niah-critique.md`, `-nocha.md`, `-ruler.md`, `-longbench.md` | the NIAH validity gap (NoLiMa: 128K → 8K effective) |
| `multiturn-fed.md`, `-usr.md`, `-dstc.md`, `-botchat.md`, `-mint.md`, `-dialogbench.md` | dialogue-eval benchmark landscape |

**⚠️ Extraction caveats — do not cite numbers from these without a manual check:**
- `when-attention-closes` — per-turn tables not machine-extractable. Qualitative claim (non-monotone) is solid; **no numbers**.
- `mt-bench-101` — Figure 4/6 per-turn curves are glyph-encoded vector plots; **only axis ranges recovered, not data points**. Trend *directions* are verbatim from the text and are safe. Appendix G Fleiss' Kappa not recovered. Per-turn values are pullable from the GitHub repo if needed.
- `longbench` — v1 per-model table and v2 per-category breakdown not retrievable (arxiv HTML 404/overflow). Marked UNVERIFIED in-file; resolvable by counting the `category` field in the HF dataset `zai-org/LongBench-v2`. **Worth closing** — its "long-dialogue history understanding" category is the closest existing prior art to our target.

**Convergences worth trusting** (independent sources, same conclusion): multi-turn ⊥ capability (Laban / MT-Eval / MemGPT-DMR); non-monotone turn effects (Multi-IF / MT-Bench-101 / When Attention Closes / Lost-in-the-Middle); alignment tuning doesn't buy multi-turn ability (MT-Bench-101 / MINT); RL/roleplay tuning worsens cohort diversity (Chameleon's Limit).
