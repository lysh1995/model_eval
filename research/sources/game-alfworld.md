---
title: "ALFWorld: Aligning Text and Embodied Environments for Interactive Learning"
url: https://arxiv.org/abs/2010.03768
authors: Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, Matthew Hausknecht
year: 2021
type: benchmark
accessed: 2026-07-16
topic: game-simulation
---

# ALFWorld: Aligning Text and Embodied Environments for Interactive Learning (ICLR 2021)

Project: https://alfworld.github.io · Code: https://github.com/alfworld/alfworld

**Status: the LLM is the PLAYER. The simulator is PDDL + Fast Downward (a classical planner) on the text side, and THOR (rendering + physics) on the embodied side. Ground truth is a set of logical predicates — the most *formally* checkable state in the corpus. Its lasting relevance to us is (i) the goal-condition partial-credit metric and (ii) the fact that it became the de-facto LLM-agent benchmark, giving us a long comparable time-series.**

> ⚠️ **All tables below verified against the arXiv PDF text.** An ar5iv-based extraction of Table 2 silently dropped three of the five column-groups (Seq2Seq, BUTLER-ORACLE, Human Goals) and would have produced a wrong writeup. The full five-group table is reproduced here.

## Abstract (verbatim)

> "Given a simple request like *Put a washed apple in the kitchen fridge*, humans can reason in purely abstract terms by imagining action sequences and scoring their likelihood of success, prototypicality, and efficiency, all without moving a muscle. Once we see the kitchen in question, we can update our abstract plans to fit the scene. Embodied agents require the same abilities, but existing work does not yet provide the infrastructure necessary for both reasoning abstractly and executing concretely. We address this limitation by introducing ALFWorld, a simulator that enables agents to learn abstract, text-based policies in TextWorld (Côté et al., 2018) and then execute goals from the ALFRED benchmark (Shridhar et al., 2020) in a rich visual environment. ALFWorld enables the creation of a new BUTLER agent whose abstract knowledge, learned in TextWorld, corresponds directly to concrete, visually grounded actions. In turn, as we demonstrate empirically, this fosters better agent generalization than training only in the visually grounded environment."

## Task structure — Table 1: Six ALFRED task types

| Task type | # train | # seen | # unseen |
|---|---|---|---|
| Pick & Place | 790 | 35 | 24 |
| Examine in Light | 308 | 13 | 18 |
| Clean & Place | 650 | 27 | 31 |
| Heat & Place | 459 | 16 | 23 |
| Cool & Place | 533 | 25 | 21 |
| Pick Two & Place | 813 | 24 | 17 |
| **All** | **3,553** | **140** | **134** |

*Caption: "Six ALFRED task types with heldout seen and unseen evaluation sets."*

> "Tasks involve first finding a particular object, which often requires the agent to open and search receptacles like drawers or cabinets. Subsequently, all tasks other than Pick & Place require some interaction with the object such as heating (place object in microwave and start it) or cleaning (wash object in a sink). To complete the task, the object must be placed in the designated location."

**Environment scale:** "the embodied environment includes **120 rooms (30 kitchens, 30 bedrooms, 30 bathrooms, 30 living rooms)**, each dynamically populated with a set of portable objects (e.g., apple, mug), and static receptacles (e.g., microwave, fridge)."

**Seen vs unseen (verbatim) — the generalization split that matters:**
> "(1) **seen** consists of known task instances {task-type, object, receptacle, room} in rooms seen during training, but with different instantiations of object locations, quantities, and visual appearances (e.g. two blue pencils on a shelf instead of three red pencils in a drawer seen in training).
> (2) **unseen** consists of new task instances with possibly known object-receptacle pairs, but always in unseen rooms with different receptacles and scene layouts than in training tasks.
> The **seen set is designed to measure in-distribution generalization, whereas the unseen set measures out-of-distribution generalization.**"

**Departure from ALFRED:** "We depart from the ALFRED challenge by **omitting these step-by-step instructions** and focusing on the more difficult problem of using only on goal descriptions specifying **what** needs to be achieved."

## The PDDL ground truth

> "In order to extend TextWorld to create text-based analogs of each ALFRED scene, we adopt a **common latent structure representing the state of the simulated world. ALFWorld uses PDDL — Planning Domain Definition Language (McDermott et al., 1998) — to describe each scene from ALFRED and to construct an equivalent text game using the TextWorld engine.** The dynamics of each game are defined by the PDDL domain."

**The engine (Appendix C, verbatim):**
> "Internally, the TextWorld Engine is divided into two main components: a planner and text generator.
> **Planner**: TextWorld Engine uses **Fast Downward** (Helmert, 2006), a domain-independent classical planning system to maintain and update the current state of the game. **A state is represented by a set of predicates which define the relations between the entities** (objects, player, room, etc.) present in the game. A state can be modified by applying production rules corresponding to the actions listed in Table 6. **All variables, predicates, and rules are defined using the PDDL language.**"

Worked example (verbatim) — a player next to a closed microwave containing a mug:

> s_t = at(player, microwave) ⊗ in(mug, microwave) ⊗ closed(microwave) ⊗ openable(microwave)
>
> "where the symbol ⊗ is the linear logic multiplicative conjunction operator. Given that state, a valid action could be `open microwave`, which would essentially **transform the state by replacing closed(microwave) with open(microwave)**."

> "**Text generator**: The other component of the TextWorld Engine, the text generator, uses a **context-sensitive grammar** designed for the ALFRED environments. The grammar consists of text templates... the engine will sample a template given some context, i.e., the current state and the last action. Then, the template gets realized using the predicates found in the current state."

⇒ **The prose is a rendering of the predicate state, not the state itself.** State lives in PDDL; text is a downstream view. This separation is the architectural point for us.

**TextWorld-side action space (high-level):**
```
goto {recep}     take {obj} from {recep}    put {obj} in/on {recep}
open {recep}     close {recep}              toggle {obj} {recep}
clean {obj} with {recep}   heat {obj} with {recep}   cool {obj} with {recep}
```
> "Note that heat, cool, clean, and goto are high-level actions that correspond to several low-level embodied actions."

Embodied-side primitives are far lower-level: `MOVEAHEAD, ROTATELEFT/RIGHT, LOOKUP/DOWN, PICKUP, PUT, OPEN, CLOSE, TOGGLEON/OFF`.

## Goal-condition success — the partial-credit metric

> "For embodied evaluations, we also report **goal-condition success rates**, a metric proposed in ALFRED (Shridhar et al., 2020) to measure partial goal completion."

**Footnote 3 (verbatim) — the whole mechanism in one example:**
> "For instance, the task *'put a hot potato on the countertop'* is composed of **three goal-conditions: (1) heating some object, (2) putting a potato on the countertop, (3) heating a potato and putting it on the countertop.** If the agent manages to put any potato on the countertop, then **1/3 = 0.33 goal-conditions are satisfied**, and so on."

## Results — Table 2: Zero-shot Domain Transfer (verbatim)

Success percentages; **goal-condition success rates in parentheses**.

| task-type | TextWorld seen | TextWorld unseen | Seq2Seq seen | Seq2Seq unseen | BUTLER seen | BUTLER unseen | BUTLER-ORACLE seen | BUTLER-ORACLE unseen | Human Goals seen | Human Goals unseen |
|---|---|---|---|---|---|---|---|---|---|---|
| Pick & Place | 69 | 50 | 28 (28) | 17 (17) | 30 (30) | 24 (24) | 53 (53) | 31 (31) | 20 (20) | 10 (10) |
| Examine in Light | 69 | 39 | 5 (13) | 0 (6) | 10 (26) | 0 (15) | 22 (41) | 12 (37) | 2 (9) | 0 (8) |
| Clean & Place | 67 | 74 | 32 (41) | 12 (31) | 32 (46) | 22 (39) | 44 (57) | 41 (56) | 18 (31) | 22 (39) |
| Heat & Place | 88 | 83 | 10 (29) | 12 (33) | 17 (38) | 16 (39) | 60 (66) | 60 (72) | 8 (29) | 5 (30) |
| Cool & Place | 76 | 91 | 2 (19) | 21 (34) | 5 (21) | 19 (33) | 41 (49) | 27 (44) | 7 (26) | 17 (34) |
| Pick Two & Place | 54 | 65 | 12 (23) | 0 (26) | 15 (33) | 8 (30) | 32 (42) | 29 (44) | 6 (16) | 0 (6) |
| **All Tasks** | **40** | **35** | **6 (15)** | **5 (14)** | **19 (31)** | **10 (20)** | **37 (46)** | **26 (37)** | **8 (17)** | **3 (12)** |

**Caption (verbatim):** "Zero-shot Domain Transfer. **Left**: Success percentages of the best BUTLER::BRAIN agents evaluated purely in TextWorld. **Mid-Left**: Success percentages after zero-shot transfer to embodied environments. **Mid-Right**: Success percentages of BUTLER with an **oracle state-estimator and controller, an upper-bound**. **Right**: Success percentages of BUTLER with **human-annotated goal descriptions**, an additional source of generalization difficulty. All successes are averaged across three evaluation runs. Goal-condition success rates are given in parentheses. The **Seq2Seq baseline is trained in TextWorld from pre-recorded expert demonstrations using standard supervised learning. BUTLER is our main model using the Mask R-CNN detector and A\* navigator. BUTLER-ORACLE uses an oracle state-estimator with ground-truth object detections and an oracle controller that directly teleports between locations.**"

Selection protocol: "best-performing agents (from **8 random seeds**); this is done separately for each split: seen and unseen."

**Reading the table:**
- **The TextWorld→embodied drop is the headline: 40 → 19 (seen), 35 → 10 (unseen).** Roughly **half to two-thirds of abstract competence is lost in grounding.**
- **Perception/control is most of that loss**, not planning: BUTLER-ORACLE recovers **37/26** vs BUTLER's **19/10**. Give the agent perfect object detection and teleportation and it roughly doubles.
- **"All Tasks" is far below every per-task row** (40 vs 54–88 in TextWorld). Per-task rows are *specialist* agents; "All Tasks" is a **single policy over all 3,553 tasks** — the multi-task tax is enormous.
- **Human-annotated goals collapse performance: 19 → 8 (seen), 10 → 3 (unseen).** Free-form human phrasing costs more than half the score vs templated goals.
- **Goal-condition rates are always ≥ success rates** and sometimes wildly so (Examine in Light unseen: **0 success but 15 goal-condition**) — partial credit is doing real work where binary success is degenerate.

> "Comparing BUTLER to Seq2Seq, we see improved performance on all types of seen tasks and five of the seven types of unseen tasks, supporting the hypothesis that **interactive TextWorld training is a key component in generalizing to unseen embodied tasks.** Interactive language not only allows agents to explore and build an understanding of successful action patterns, but also to **recover from mistakes.**"

> "While these preliminary results with natural language are encouraging, we expect future work could augment the templated language with synthetic-to-real transfer methods."

## Results — Table 3: TextWorld-vs-embodied transfer (verbatim)

| Training Strategy | train (succ %) | seen (succ %) | unseen (succ %) | train speed (eps/s) |
|---|---|---|---|---|
| EMBODIED-ONLY | 21.6 | 33.6 | 23.1 | 0.9 |
| TW-ONLY | 23.1 | 27.1 | **34.3** | **6.1** |
| HYBRID | 11.9 | 21.4 | 23.1 | 0.7 |

*Caption: "Training Strategy Success. Trained on All Tasks for **50K episodes** and evaluated in embodied scenes using an **oracle state-estimator and controller**."*

Strategies: "(i) EMBODIED-ONLY: pure embodied training, (ii) TW-ONLY: pure TextWorld training followed by zero-shot embodied transfer and (iii) HYBRID training that switches between the two environments with **75% probability for TextWorld and 25% for embodied world**."

> "Results indicate that **TW-ONLY generalizes better to unseen environments while EMBODIED-ONLY quickly overfits to seen environments** (even with a perfect object detector and teleport navigator). We hypothesize that the **abstract TextWorld environment allows the agent to focus on quickly learning tasks without having to deal execution-failures and expert-failures caused by physical constraints** inherent to embodied environments. **TextWorld training is also 7× faster** since it does not require running a rendering or physics engine like in the embodied setting."

Compute footnote: "all agents in Table 3 use a batch-size of 10. **THOR instances use 100MB×batch-size of GPU memory for rendering, whereas TextWorld instances are CPU-only and are thus much easier to scale up.**"

⇒ The clean statement of the paper's thesis: **abstraction is both cheaper (7×) and generalizes better (34.3 vs 23.1 unseen), at a small cost on seen (27.1 vs 33.6).** Note EMBODIED-ONLY wins on *seen* — the benefit of abstraction is specifically out-of-distribution.

## RL didn't work — they used DAgger

Worth recording, because it explains why ALFWorld became an *LLM prompting* benchmark:

> "Due to the infeasibility of using candidate commands or command templates..., the RL agent had to generate actions token-by-token. Since the **probability of randomly stumbling upon a grammatically correct and contextually valid action is very low (7.02e-44 for sequence length 10)**, the RL agent struggled to make any meaningful progress towards the tasks."

> "After concluding that current reinforcement learning approaches were not successful on our set of training tasks, we turned to **DAgger** (Ross et al., 2011) assisted by a **rule-based expert**. BUTLER::BRAIN is trained for **100K episodes**."

**Rule-based expert = subgoal decomposition (verbatim):**
> "A given task is decomposed into sequence of subgoals (e.g., for heat & place: find the object, pick the object, find the microwave, heat the object with the microwave, find the receptacle, place the object in the receptacle), and a closed-loop controller tries to sequentially execute these goals. We note that while **designing rule-based experts for ALFWorld is relatively straightforward, experts operating directly in embodied settings like the PDDL planner used in ALFRED are prone to failures due to physical infeasibilities and non-deterministic behavior in physics-based environments.**"

**Ablation findings (Table 4):** "(i) Training success rate varies from **16-60%** depending on the category of tasks... (ii) Transferring from training to heldout test games typically reduces performance, with the **unseen rooms leading to the largest performance drops**. Notable exceptions include heat and cool tasks where unseen performance exceeds training performance. (iii) **Beam search is a key contributor to test performance; its ablation causes a performance drop of 21% on the seen split of All Tasks.**"

**Mask R-CNN detector:** fine-tuned on 50K images replayed from ALFRED expert demos; "recognizes **73 object classes** where each class could vary up to 1-10 instances."

## Later life: the de-facto LLM agent benchmark

**ReAct (Yao et al., ICLR 2023, arXiv 2210.03629) — Table 3, ALFWorld task-specific success rates (%), verbatim:**

| Method | Pick | Clean | Heat | Cool | Look | Pick 2 | All |
|---|---|---|---|---|---|---|---|
| Act (best of 6) | 88 | 42 | 74 | 67 | 72 | 41 | 45 |
| ReAct (avg) | 65 | 39 | 83 | 76 | 55 | 24 | **57** |
| **ReAct (best of 6)** | 92 | 58 | 96 | 86 | 78 | 41 | **71** |
| ReAct-IM (avg) | 55 | 59 | 60 | 55 | 23 | 24 | 48 |
| ReAct-IM (best of 6) | 62 | 68 | 87 | 57 | 39 | 33 | 53 |
| BUTLER_g (best of 8) | 33 | 26 | 70 | 76 | 17 | 12 | 22 |
| BUTLER (best of 8) | 46 | 39 | 74 | 100 | 22 | 24 | 37 |

*Caption: "AlfWorld task-specific success rates (%). BUTLER and BUTLER_g results are from Table 4 of Shridhar et al. (2020b). All methods use greedy decoding, except that BUTLER uses beam search."*

ReAct abstract: "**ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10%** respectively, while being prompted with **one or two in-context examples**."

⇒ **ReAct 71% (best of 6) vs BUTLER 37% (best of 8)** — a **34-point** absolute gain, which is exactly the abstract's claim. **A prompted LLM with ~1–2 examples beat a purpose-trained, 100K-episode DAgger agent by ~2×.** Note the BUTLER numbers cited by ReAct (37 / "All") are the *TextWorld-side, best-of-8* figures from ALFWorld's Table 4, **not** the embodied-transfer 19/10 from Table 2 — the comparison is text-only. Also note both "best of N" columns are **maxima over prompts/seeds, not means**; ReAct's honest average is **57**, and the 71 is a best-of-6 selection. Cite 57 as the like-for-like number and 71 only with the qualifier (cf. `psycho-leaderboard-illusion.md`).

For reference, ReAct's WebShop table (same paper) is where the human number lives: **Human expert 82.1 score / 59.6 SR**, vs ReAct 66.6 / 40.0. **ALFWorld itself has no human-performance row.**

## Relevance to companion-eval-platform

### (a) Is the LLM the PLAYER or the SIMULATOR/GAME MASTER?

**PLAYER, in every incarnation.** BUTLER plays; ReAct plays; every subsequent LLM-agent paper plays. **The game master is Fast Downward executing a PDDL domain** — a classical planner with no learning in it at all. The text you read is generated by a **context-sensitive grammar** that renders predicates into English; that grammar is the closest thing here to an "AI narrator," and it is a **template engine, not a model**.

So ALFWorld is on the opposite side of our axis, same as ScienceWorld — and note the shared author (**Côté**) across ALFWorld, ScienceWorld, and LLM-Sim. The three are one lineage. **Only `game-llm-sim-state-prediction.md` puts the LLM in our seat.** ALFWorld's agent numbers are not our baselines.

But there's a sharper way to use it: **ALFWorld is what our setting looks like if you solve the world-model problem by not using a model at all.** The text renderer is deterministic, so it *cannot* contradict itself — continuity is free, because state is external. That's the architectural argument for a state block outside the model, and this is the canonical citation for it.

### (b) Is ground-truth simulator state available and mechanically checkable?

**Yes — and this is the strongest form of it in the corpus: state is literally a set of logical predicates.** `at(player, microwave) ⊗ in(mug, microwave) ⊗ closed(microwave)`. Goal satisfaction is **entailment checking over a predicate conjunction** — decidable, instant, zero annotators, zero disagreement. Stronger than ScienceWorld's typed-field state (which needs threshold conventions like "boiled = temp ≥ boilingPoint") and incomparably stronger than our α = 0.25–0.34 aesthetic ratings.

**What to actually take:**

1. **⭐ Goal-condition success is the metric to steal, and footnote 3 is the spec.** Decomposing "put a hot potato on the countertop" into **three checkable conditions** — heated *something*, potato *on* countertop, and the **conjunction** — then scoring **1/3 = 0.33** for partial completion. Two things make it better than ScienceWorld's subgoal scheme: (i) the conjunction is **itself a tracked condition**, so an agent that heats a *different* potato than the one it placed gets credit for the parts but **not** the whole — it catches the "did the right things to the wrong objects" failure that a flat subgoal checklist misses; (ii) it's defined over **end-state predicates**, so it's method-agnostic for free. Our analogue: "the companion acknowledged the user's news" + "referenced the correct prior event" + **"did both about the same event"** — that third conjunct is where roleplay models actually fail, and nobody scores it.

2. **⭐ The empirical case for partial credit is right there in the table.** Examine in Light, unseen: **0 success, 15 goal-condition.** Binary success is **completely degenerate** on that cell — it cannot distinguish a good agent from a dead one, and any leaderboard built on it reports a tie at zero. The goal-condition rate still ranks. **Every dimension we ship needs a partial-credit form, or our hardest scenarios will be exactly the ones our metric goes blind on.** This is the cleanest published demonstration of that failure I've found and it's worth citing directly in the metric-design doc.

3. **⭐ Separate the state from its rendering — this is the architectural import.** PDDL holds truth; a context-sensitive grammar renders it to prose. Continuity is *structurally guaranteed* rather than *hoped for*. Our version: maintain an explicit predicate-ish state block, let the model render, and **check the render against the block**. That reframes "did the model contradict itself" from an aesthetic judgment into **an entailment check between the block and extracted claims** — the same move that gets ALFWorld its α-free ground truth. This dovetails with LLM-Sim's ℱ_act/ℱ_env split: ALFWorld shows what the state *representation* should be; LLM-Sim shows what to *measure* about it.

4. **⭐ Human phrasing costs more than half: 19 → 8 (seen), 10 → 3 (unseen).** Templated goals vastly overstate competence versus how humans actually talk — and this is the paper's own "additional source of generalization difficulty." Our scenario prompts are templated. **This is the strongest available evidence that our numbers will be optimistic** relative to real users, and the authors' proposed fix ("synthetic-to-real transfer methods") is an admission that they didn't solve it. Quote this when we caveat scenario realism; it is a ~60% relative drop from *phrasing alone*.

5. **⭐ Oracle-vs-real decomposition is a template for attributing our own errors.** BUTLER 19/10 → BUTLER-ORACLE 37/26 cleanly says *perception and control*, not planning, is the bottleneck — obtained by **swapping one component for an oracle and re-running**. Directly portable: run our world-state eval with (i) an oracle state block injected vs (ii) the model's own tracked state. The gap attributes error to *tracking* vs *using*. Cheap, and it converts a single opaque score into an actionable one. (Same shape as LLM-Sim's rules-in-context +30.6.)

6. **The multi-task tax is severe and we should expect it: 54–88 per-task vs 40 for one policy over all 3,553.** Specialist agents look ~2× better than a generalist on identical tasks. **Any per-scenario tuning we do will inflate results the same way**; report the single-config-across-all-scenarios number as primary.

7. **Beam search is worth 21 points** on seen All Tasks. A decoding-strategy artifact roughly the size of the entire method contribution. **Fix and report decoding config**, or we'll publish sampler noise as a model difference. (Note ReAct's table caption disclosing exactly this asymmetry: "All methods use greedy decoding, except that BUTLER uses beam search" — the 34-point ReAct win is measured against a baseline with a *different* decoding setup.)

8. **Abstraction is cheap and generalizes: TW-ONLY 34.3 unseen vs EMBODIED-ONLY 23.1, at 7× the speed, CPU-only.** The transferable claim is that a **low-fidelity text simulation is a legitimate proxy for an expensive high-fidelity one** — which is the load-bearing assumption behind evaluating companion behavior in text at all. This is our citation for it. Caveat honestly: EMBODIED-ONLY still **wins on seen** (33.6 vs 27.1); abstraction helps OOD specifically, and "overfits to seen" is the paper's word for it.

9. **The 7.02e-44 number is a useful rhetorical anchor.** The chance of a token-by-token policy emitting a valid 10-token action by luck — which is *why* RL failed and *why* the field pivoted to imitation and then to prompting. Compact evidence that **the action/output space's structure dominates the learning algorithm**, and a caution for any free-text metric we define over an unconstrained space.

10. **⚠️ Citation hygiene:** (i) **ALFWorld reports no human performance** — the 59.6 SR human expert figure in ReAct is **WebShop**, not ALFWorld; don't cross-wire them. (ii) BUTLER's headline "37" (as cited by ReAct) is **TextWorld-side best-of-8**, while ALFWorld's own Table 2 embodied-transfer figure is **19 seen / 10 unseen** — three different "BUTLER numbers" circulate and are routinely conflated. State which one you mean. (iii) Both BUTLER and ReAct headline figures are **best-of-N maxima over seeds/prompts**, not means.
