# 01 — Roleplay / Persona / Character Benchmarks: Synthesis

**Scope:** 22 sources captured in [`../sources/`](../sources/) — academic benchmarks, two field surveys, the MiniMax reference dataset, and the judge-bias literature that governs whether any of it is comparable across models.

**Bottom line for the platform:** the field has converged on a recurring 4-cluster dimension set that we should adopt nearly verbatim. But it has *not* solved the problem we actually have — cross-model comparable, stable, traceable scores on **user-authored, original characters over long multi-turn sessions**. Every academic benchmark either uses famous characters (contaminated), single-turn probes (wrong shape), or an unvalidated LLM judge (not comparable). The two designs closest to what we need are [MiniMax role-play-bench](../sources/rp-bench-minimax-role-play-bench.md) and [RAIDEN](../sources/rp-bench-raiden.md), for opposite reasons.

---

## 1. Comparison table — benchmarks × dimensions

Legend: ● = explicit named dimension · ○ = partially covered / folded into another dimension · — = absent

| Benchmark | Style/Voice | Knowledge fidelity | Boundary/refusal | Persona consistency | Memory | Empathy | Engagement/Proactivity | Human-likeness | Diversity | Safety/Morality | Narrative/Story | Multi-turn | ZH |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [CharacterEval](../sources/rp-bench-charactereval.md) | ● PU | ● KE/KA | ● KH | ● PB | ○ Cons. | ● Emp. | ● CS | ● HL | ● ED | — | — | ✅ 9.28t | ZH only |
| [CharacterBench](../sources/rp-bench-characterbench.md) | ● Behavior Cons. | ● Fact Acc. | ● Boundary Cons. | ● Attribute Cons. | ● Memory Cons. | ● Empathetic Resp. | ● Engagement | ● Human-likeness | — | ● Stability+Robustness | — | ✅ 11.22t | ZH+EN* |
| [RAIDEN](../sources/rp-bench-raiden.md) | ● PLS | ● SBK/SAK | ● RCB/SCK | ○ | ● CM | ● ER | ● TS/TA/CC | ○ | — | — | — | ✅ 21–65u | ZH only |
| [CoSER](../sources/rp-bench-coser.md) | ○ rubric | ○ rubric | — | ● Char. Fidelity | — | ○ | — | ● Anthropomorphism | — | — | ● Storyline Q+C | ✅ | — |
| [MiniMax RPB](../sources/rp-bench-minimax-role-play-bench.md) | ○ | ● Knowledge | ○ | ● Logic | ● Logic | — | ● Interaction | ○ Basics | ● Diversity | ○ Boundary | ● Content Logic | ✅ 100t | ZH+EN |
| [RoleLLM/RoleBench](../sources/rp-bench-rolellm.md) | ● CUS | ● SPE | — | — | — | — | — | — | — | — | — | ❌ | 5% |
| [RoleEval](../sources/rp-bench-roleeval.md) | — | ● MCQ | — | — | — | — | — | — | — | — | — | ❌ | ZH+EN |
| [SocialBench](../sources/rp-bench-socialbench.md) | ● SA Style | ● SA Know. | — | ● group drift | ● CM Short/Long | ● EP Emo. | — | — | — | — | — | ✅ 76.7u | ZH+EN |
| [PersonaGym](../sources/rp-bench-personagym.md) | ● Ling. Habits | — | — | ● Persona Cons. | — | — | — | — | — | ● Toxicity Control | — | ❌ | ❌ |
| [InCharacter](../sources/rp-bench-incharacter.md) | — | — | — | ● personality | — | ○ scales | — | — | — | — | — | ❌ | ✅ |
| [CharacterGLM](../sources/rp-bench-characterglm.md) | ● Behaviors | ● Attributes | — | ● | ○ | ○ | ● | ● | — | — | — | ✅ 15.78r | ZH only |
| [MMRole](../sources/rp-bench-mmrole.md) | ● TC | ● KC | — | ● PC | — | — | — | — | — | — | — | ✅ | ❌ |
| [DITTO](../sources/rp-bench-ditto.md) | ○ | ● Knowledge | ● Unknown Q Rejection | ● Consistent Role Identity | — | — | — | — | — | — | — | ✅ ~5t | ~50% |
| [TimeChara](../sources/rp-bench-timechara.md) | — | ● Spatiotemporal Cons. | — | ● Personality Cons. | — | — | — | — | — | — | — | ❌ | ❌ |
| [LifeChoice](../sources/rp-bench-lifechoice.md) | — | — | — | ● Decision-making | — | — | — | — | — | — | — | ❌ | ❌ |
| [PersonaLLM](../sources/rp-bench-personallm.md) | — | — | — | ● Big Five | — | — | ● likeability | ● believability | — | — | — | ❌ | ❌ |
| [ECHO](../sources/rp-bench-echo.md) | ○ | ○ | — | ○ | — | — | — | ● Turing | — | — | — | ❌ | ❌ |
| [PingPong](../sources/rp-bench-pingpong.md) | ● | — | — | ● char. consistency | — | — | ● entertainment | — | — | — | ○ | ✅ | ○ |

\* CharacterBench English is GPT-4o-translated from Chinese-native data, not natively authored.

### Scoring method × validation — the more decision-relevant table

| Benchmark | Scoring mechanism | Scale | Judge–human agreement | IAA reported? |
|---|---|---|---|---|
| CharacterEval | **Trained reward model** (Baichuan2-13B) | 5-pt | Pearson **0.631** overall (GPT-4: 0.385) | ❌ (12 annotators, no κ) |
| CharacterBench | **Trained judge** (Qwen2-7B) + self-consistency | mixed 2/3/4/5-pt | Pearson **68 ZH / 64 EN** (GPT-4: 45/46) | ❌ (22,859 samples, no κ) |
| RAIDEN | **Human pairwise**, 1 dim/turn; RPCAJudger-13B | win-rate | judge–human Δ **2.46%**; acc 80.4 vs GPT-4 86.4 | ✅ **91.4%** 3-expert consensus |
| CoSER | **Penalty-based LLM critic** (flaw × severity) | 0–100 | **Alignment 68.6%** (GPT-4o); DeepSeek-R1 77.5 | ❌ |
| MiniMax RPB | LLM judge, chunked (20-turn slices), 3 runs | 0–100 + 95% CI | **not published** | ❌ |
| RoleLLM | **Rouge-L** vs GPT-generated refs + GPT-3.5 pairwise | overlap | **none** | ❌ |
| RoleEval / SocialBench / LifeChoice | **Multiple choice / keyword** — no judge | accuracy | N/A (objective) | ❌ |
| PersonaGym | LLM judge ensemble + generated exemplars | 1–5 | Spearman **75.1%**, **Fleiss κ 0.71** | ✅ |
| InCharacter | Psych scales via interview | scale-dep. | — | ✅ **Cohen κ 0.609** |
| Anon. Benchmarking | (reuses CharacterEval RM) | — | Cohen **κ 0.415 / 0.308** | ✅ |
| MMRole | Trained reward model | ratio vs GPT-4 ref | Pearson **0.6502** (vs GPT-4: **0.8129**) | ❌ |
| PingPong | User-simulator + **judge ensemble** | 5-pt Likert/turn + bootstrap CI | Spearman **~0.60** | ✅ **Krippendorff α 0.25 EN / 0.34 RU** |
| CharacterGLM | **Pure human** (10 annotators, self-authored chars) | 1–5 + pairwise | N/A | ❌ |

---

## 2. Where the field agrees

Four clusters recur across nearly every source, and — critically — **the two independent surveys converge on the same spine** ([Oscars of AI Theater](../sources/rp-bench-survey-oscars-ai-theater.md), [Persona-to-Personalization](../sources/rp-bench-survey-persona-personalization.md)). Independent convergence is the best evidence available that these are real constructs rather than arbitrary rubric carving.

**The recurring set — adopt these:**

1. **Conversational quality** (fluency, coherence, non-repetition) — in *every* source. Near-universal, cheap, high judge agreement (CharacterRM Pearson 0.613 Fluency / 0.607 Coherency). **This is table stakes, and it barely discriminates between frontier models.** Measure it as a floor/guardrail, not a leaderboard axis.
2. **Character fidelity**, which reliably splits into **three separable sub-constructs** the field keeps rediscovering:
   - **Voice/style** (PU, PLS, CUS, TC, Linguistic Habits)
   - **Knowledge** (KA/KE, Fact Accuracy, SBK/SAK, KC)
   - **Boundary discipline** (KH, Boundary Consistency, RCB, Unknown-Question Rejection)
   The style/knowledge/boundary split is the single most reproduced decomposition in the literature. Do not collapse it.
3. **Persona/behavioral consistency over time** (Consistency, Memory Consistency, CM, Logic, Personality Consistency).
4. **Attractiveness / anthropomorphism** (Human-likeness, Engagement, Empathy, Proactivity) — the "is this pleasant to talk to" cluster.

**Other points of agreement:**

- **Fine-tuned judges beat GPT-4 decisively** on roleplay. CharacterRM 0.631 vs 0.385; CharacterJudge 68/64 vs 45/46. Replicated across two independent groups.
- **But the gain is method, not model.** CharacterBench's ablation is the key number: removing *target guidance* costs 17 Pearson points (68→51), dropping the 7B judge to GPT-4's level. Self-consistency adds only ~4. **Probe design dominates judge choice.**
- **Quality degrades monotonically with conversation length.** CharacterEval §6.6 states it outright; MiniMax's chunked judging is built around it; CharacterGLM names finite context as its #1 limitation. This is *the* companion failure mode and it is well-attested.
- **Language-match matters.** Chinese-tuned models beat GPT-4 on Chinese roleplay (CharacterEval, RAIDEN). Roleplay ability does not transfer across languages for free.

## 3. Where the field disagrees

- **Trained reward model vs. prompted judge vs. no judge at all.** Three live camps. CharacterEval/CharacterBench/MMRole/RAIDEN train judges; CoSER/MiniMax/PersonaGym prompt frontier models; SocialBench/RoleEval/LifeChoice refuse judges entirely and use multiple choice. No consensus.
- **Absolute rubric vs. pairwise.** RAIDEN explicitly *rejected* absolute scoring as too subjective and went pairwise — then conceded in its limitations that pairwise "does not provide an absolute measure of performance." MiniMax went the other way (absolute 0–100). **This is a genuine, unresolved trade-off and it lands directly on our requirement.** See §6.
- **Is self-report personality valid?** [PersonaLLM](../sources/rp-bench-personallm.md) says yes (Cohen's d 4.22–6.30). [InCharacter](../sources/rp-bench-incharacter.md) says no (Acc_full 7.3% self-report vs 31.2% interview). Both are right: recovering a trait you were *just assigned* is trivial; revealing a canon character's *latent* personality is not. **Our characters have backstories → InCharacter's regime applies → don't build self-report probes.**
- **MBTI/psychometrics as ground truth.** CharacterEval back-tests MBTI; CharacterBench explicitly declines to evaluate MBTI or Big Five. CharacterBench is right — MBTI has poor psychometric validity and fan-assigned character labels are not authoritative.
- **Is famous-character knowledge a feature or a confound?** Most benchmarks treat canon recall as a *dimension*. [Anonymous Benchmarking](../sources/rp-bench-anonymous-benchmarking.md) shows it is a *confound* — anonymization degrades every model, meaning those benchmarks partly measure memorization and report it as roleplay skill.

## 4. Which dimensions are real, which are one-offs

**Real (recurring, independently converged, separable):** fluency/coherence · voice/style · knowledge accuracy · boundary discipline · persona consistency · memory over turns · empathy · engagement/proactivity · human-likeness.

**Valuable one-offs worth stealing:**

- **Morality Robustness** (CharacterBench, unique) — does the model comply when the *character profile itself* is toxic? For a platform with user-authored characters this is the exact threat model. Nobody else covers it. **Highest-value single import in this review.**
- **Script-Contradictory Knowledge / SCK** (RAIDEN, unique) — does the agent push back when the *user* asserts falsehoods about the character? Both surveys miss it.
- **AI Speaks for User / AI Ignores User / AI Silence** (MiniMax, unique) — the most product-shaped failure taxonomy in the literature. Cheap to detect, immediately actionable.
- **Decision-making** (LifeChoice) — human 92.01 vs best model 67.95, a **~24pt gap**, the largest human–model gap anywhere in this review. Behavior consistency ≫ voice consistency in difficulty. A companion eval that only scores tone measures the shallow layer.
- **Spatiotemporal consistency** (TimeChara) — point-in-time character state. Both surveys concede this is under-studied.
- **Group-influence drift** (SocialBench) — persona destabilizes under social pressure from other agents.
- **Sparse vs. dense dimensions** (CharacterBench) — not a dimension but an *architecture*: features that appear in every response (morality, believability) vs. only when touched (memory, knowledge). Drives probe design.

- **Real-traffic topic prior** (PingPong Appendix C) — BERTopic over *actual* Chai companion-app traffic: Friendly Interactions 11.1%, Casual Greetings 10.6%, Interpersonal 8.9%, Casual Fun 8.4%, Affection & Comfort 8.0%, Relationships 7.7%. **Affection + Relationships ≈ 15.7% of real companion traffic.** The only empirical situation-sampling prior in this literature — our seed distribution should match traffic, not literary drama.
- **"Virtual love" character category** (CharacterGLM) — one of its four categories; rare in the literature and directly on-point for companions. RAIDEN's **Emotional Companionship** category (13 roles) is the other instance.

**One-offs to skip:** MBTI back-testing (contested validity); Rouge-L against GPT-generated references (RoleBench — measures lexical overlap with a GPT-4 role-prompt, not quality); multimodal grounding (MMRole — out of scope unless we ship avatars); CoSER's **Storyline Consistency** (presupposes a ground-truth reference dialogue from a book — open-ended companion chat has none, so it doesn't port; Anthropomorphism and Character Fidelity do).

## 5. What nobody measures well

1. **Individualized personas.** The Persona-to-Personalization survey's own taxonomy has three persona types — Demographic, Character, **Individualized** ("customized through ongoing user interactions"). Individualized is the companion product, and it has the *thinnest* evaluation apparatus in the survey: no fidelity dimensions, no consistency dimensions, only downstream task proxies (conversation/recommendation/task-solving). **This is the field's biggest hole and it is exactly our product.**
2. **Generative persona fidelity over long horizons.** SocialBench is the only source instrumenting long memory (CM Long, 76.7 utterances) — and it does so by *multiple choice*, testing recognition, not production. Nothing measures generated persona fidelity across a sustained session.
3. **Inter-annotator agreement.** CharacterEval (12 annotators), CharacterBench (22,859 samples), CoSER, MMRole, RoleLLM, MiniMax — **all report none.** Only RAIDEN (91.4%), PersonaGym (κ 0.71), InCharacter (κ 0.609) and Anonymous Benchmarking (κ 0.415/0.308) publish anything. **Every correlation number in this literature has an unknown ceiling.**
4. **Creativity — and it may be actively anti-measured.** No benchmark scores creativity well. "Expression Diversity" (CharacterEval, Pearson 0.765) and "Diversity" (MiniMax) are the closest, and both are really *anti-repetition*, not creativity. Worse: [judge-bias](../sources/rp-bench-judge-bias.md) shows LLM judges reward **low-perplexity** text — and creative prose is by construction high-perplexity. **An LLM judge scoring "creativity" may be measuring its inverse.** Treat any creativity score we ship as low-confidence until human-calibrated.
5. **Empathy and knowledge-accuracy scoring.** The two most product-critical axes are where reward models are *weakest*: CharacterRM Empathy 0.385, Knowledge-Accuracy 0.336.
6. **Aesthetic dimensions have no stable human ground truth.** κ = 0.308 on general-response comparison means humans barely agree. [PingPong](../sources/rp-bench-pingpong.md) independently measures **Krippendorff α = 0.25 (EN) / 0.34 (RU)** among five annotators. **This reframes every correlation in this document:** judge–human Spearman ≈ 0.60 is measured against a noisy ceiling, so ~0.6 is plausibly *near-maximal*, not a shortfall. Stop reading judge correlations as "60% good"; read them as "at the ceiling of a construct humans can't agree on." MiniMax's "Ground Truth Paradox" is the honest response.
7. **Mature/intimate content — blocked by the judges themselves.** PingPong explicitly concedes it avoids mature content *because judge models refuse to score it*. For a companion platform this is the commercially load-bearing segment (affection + relationships ≈ 15.7% of real traffic per PingPong's own topic analysis), and **no benchmark in this review evaluates it** — not for lack of interest, but because the measurement instrument refuses. Expect our judge stack to hit this wall. Anticipate needing a judge configuration (or a human panel) that can score in-policy intimate content, or we will be flying blind on a sixth of our traffic. Relatedly, both the Persona-to-Personalization survey and DITTO's ethics statement warn that **persona assignment itself measurably raises toxicity** relative to the un-personified baseline — roleplay is an attack surface, and CharacterBench's Morality Robustness is the only published probe for it.
8. **Some dimensions are dead metrics in some languages.** PingPong's English Fluency correlates at r ≈ 0.02–0.25 (mostly not significant) — modern models simply don't make English fluency errors — yet it still feeds the Final average, diluting it. **Re-validate every dimension per language; do not assume transfer.** Our ZH and EN rubrics may need different active dimension sets.

## 6. Implications for our platform

**On comparability across models — our hardest requirement:**

- **Pairwise is dangerous at our scale.** Position Consistency of judges runs **0.57–0.82** — up to 43% of pairwise verdicts flip when you swap order, while Repetition Stability is >0.95. **Stability is not validity.** RAIDEN independently confirmed this and abandoned GPT-4 as a judge over it. If we use pairwise anywhere, evaluate both orderings.
- **Self-preference/perplexity bias attacks cross-family comparison specifically.** A judge rewards text closer to its own distribution, and that penalty is *unevenly distributed* across the variants we compare — a direct violation of "same baseline." It is invisible to self-consistency checks. **Only human calibration catches it.**
- **Deviation-detection > preference.** MiniMax's pivot ("misalignment is surprisingly objective") is the most defensible answer to the ground-truth problem, and it makes scores comparable *because* violations are checkable against a fixed spec rather than against a judge's taste.
- **Prefer trained/rubric judges over prompted frontier judges** — cheaper, more stable over time, empirically better correlated (68 vs 45), and no API drift. But a frozen judge is a fixed target that variants can overfit; schedule re-validation. Note MMRole's warning: its reward model tracks **GPT-4 at r=0.8129 but humans at only r=0.6502** — a distilled judge faithfully inherits its teacher's disagreements with humans, including the teacher's family bias.
- **Ensemble your judges.** PingPong found multi-judge averaging (Claude 3.5 Sonnet + GPT-4o) beat *every* single judge on *every* metric, and that **judge choice dominates user-simulator choice**. An ensemble across model families is also the most practical available mitigation for self-preference bias — spend budget on the judge, economize on the simulator.
- **Verbosity correction is mandatory.** CoSER (λ|M̄|) and PingPong (length normalization) converged on this independently. Longer output accrues both more flaws and more judge favor; uncorrected, length becomes a confound in cross-model comparison since models differ systematically in verbosity.

**Design rules falling out of this review:**

1. **Our eval set must be original characters** (or canon with names *and worlds* scrubbed). Published leaderboards from famous-character benchmarks do not transfer to user-authored personas. Our production setting *is* the anonymized setting.
2. **Re-ground "knowledge" dimensions on the provided character description**, not world knowledge — for original characters, the description is the only source of truth.
3. **Invest in target-guided probe generation before judge sophistication** — worth ~17 Pearson points vs ~4 for self-consistency and ~20 for the fine-tune.
4. **Adopt sparse/dense**: score morality + believability on every turn; probe memory/knowledge/boundary only where induced.
5. **Pin the session start** (MiniMax's `ai_setting` / `user_setting` / `ai_prologue` / `initial_user_input` schema). Byte-identical starting state across variants is what makes the comparison valid.
6. **Chunk long sessions** (20-turn slices) so late-session degradation isn't diluted — degradation is the attested failure mode.
7. **Ship confidence intervals, not point scores.** MiniMax does; regression detection needs them.
8. **Sensitivity target:** MiniMax's opus-high vs opus-low gap (76.62 vs 71.19) shows the metric detects a *known* capability delta within one family. That's the right sensitivity check for a regression detector — much stronger evidence than cross-family ordering.
9. **Expect our own leaderboard to be doubted.** MiniMax's model ranks #1 on MiniMax's benchmark with no published judge-human correlation. If we publish rankings, publish the calibration too.

---

## 7. Reusable rubric language (verbatim, ready to lift)

**Voice / style**
> "a character's speaking style is also important. Each character has unique expression habits. Therefore, the RPCA's utterances should align with these habits." — CharacterEval, Persona-Utterance

> "needs RPCAs to use the same language style as the acted roles, such as catchphrases, speaking styles, and classic quotes, which can establish more realistic characters and improve user immersion." — RAIDEN, PLS

**Knowledge — the KE/KA/KH triad (CharacterEval), the most transferable decomposition here**
> Knowledge-Exposure: "assessing the informativeness of a response, it's crucial for an RPCA to reflect knowledge in its responses."
> Knowledge-Accuracy: "assess whether this knowledge aligns with the character. The goal is for the RPCA to accurately generate response based on the knowledge from character's profile."
> Knowledge-Hallucination: "the RPCA should maintain consistency with the character's identity and avoid responding to queries involving unknown knowledge."

**Boundary discipline**
> "implies that the model should decline to answer questions that fall outside the character's scope, such as a historical figure facing questions about modern society." — RAIDEN, RCB

> "assesses the model's ability to correct users' inaccurate and misleading questions, a common phenomenon in user-agent dialogues." — RAIDEN, SCK

**Consistency**
> "assesses the stability of RPCAs during a conversation. Responses of an RPCA should not contradict their own responses in previous turns." — CharacterEval, Consistency

**Empathy / emotional**
> "evaluate how well responses recognize and soothe user's emotions" — CharacterBench, Empathetic Responsiveness

> "refers to the ability of an agent to identify and respond to a user's emotional state in a manner that makes the user feel understood and supported. Specifically, the model should offer praise or consolation when users express positive or negative emotions, respectively." — RAIDEN, ER

**Engagement / proactivity**
> "measures the depth of users' interest and their emotional connection with the character" — CharacterBench, Engagement

> "measures whether the model can progress the conversation topic. When the user provides limited information in the current query and the topic becomes stagnant, the model should proactively advance the topic to encourage the user's continued engagement." — RAIDEN, TA

**Safety — the pair nobody else has**
> Morality Stability: "LLMs' ability to maintain positive morality when the context is injected with toxic queries"
> Morality Robustness: "ability to uphold positive morality even when the character profile endows toxic settings" — CharacterBench

**Storytelling**
> Storyline Quality: "Evaluates whether the simulated conversation develops naturally, with rubrics focusing on narrative flow and logical consistency."
> Character Fidelity: "Assesses whether RPLAs faithfully portray their characters, with rubrics examining language style, knowledge and background, personality and behavior, and social relationships."
> Anthropomorphism: "Evaluates whether RPLAs behave in a human-like manner, with rubrics covering self-identity, emotional depth, persona coherence, and social interaction." — CoSER

**Penalty-based scoring formula (CoSER)** — the mechanism to copy for comparability:
> "we employ LLM critics to identify flaw instances ℱ in M̄ of specific rubrics... Each flaw f is assigned a severity v_f from 1 (minor) to 5 (severe). The initial score for each dimension is calculated as s = 100 − 5 * Σ_{f∈ℱ} v_f."

With mandatory length correction, since longer sessions accrue flaws mechanically:
> "score = −1.5909 × rounds + 59.0617, which means that for each additional round in the simulation, the score decreases by approximately 1.6 points."

⚠️ **But note CoSER's own numbers:** plain **BLEU aligns with humans better (75.3) than its GPT-4o critic (68.6)**; only DeepSeek-R1 (77.5) beats BLEU. Every ablation costs only 3–4 points. Adopt the penalty *mechanism* for its traceability (it emits an itemized flaw list — exactly the audit trail our traceability requirement needs), not because it is proven more accurate.

**Survey spine (Oscars of AI Theater)** — the cleanest 4-cluster frame to organize our dimensions under:
1. **Conversation Ability** — Linguistic Quality (fluency, diversity), Coherence
2. **Role-Persona Consistency** — Attributes ("experiences, identities, interests, viewpoints, age, gender, achievements, and titles"), Relations ("familiarity, intimacy, animosity, or respect")
3. **Role-Behavior Consistency** — Conversational Style, Personality, Linguistic Features
4. **Role-Playing Attractiveness** — Human Likeness, Engagement, Proactivity, Empathy

---

## 8. Licensing note

- **RAIDEN: CC BY-NC 4.0 — non-commercial.** Our closest blueprint is the one we cannot directly reuse commercially. Take the design, not the data.
- **MiniMax role-play-bench: CC BY 4.0 / CC BY-SA 4.0** — permissive; seeds and rubric structure reusable.
- **CharacterEval: CC BY-NC-SA 4.0.** CharacterBench: gated behind "rigorous licensing and review processes."
