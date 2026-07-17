---
title: "Human-level play in the game of Diplomacy by combining language models with strategic reasoning (CICERO)"
url: https://www.science.org/doi/10.1126/science.ade9097
authors: Meta Fundamental AI Research Diplomacy Team (FAIR), Anton Bakhtin, Noam Brown, Emily Dinan, Gabriele Farina, Colin Flaherty, Daniel Fried, Andrew Goff, Jonathan Gray, Hengyuan Hu, Athul Paul Jacob, Mojtaba Komeili, Karthik Konath, Minae Kwon, Adam Lerer, Mike Lewis, Alexander H. Miller, Sasha Mitts, Adithya Renduchintala, Stephen Roller, Dirk Rowe, Weiyan Shi, Joe Spisak, Alexander Wei, David Wu, Hugh Zhang, Markus Zijlstra
year: 2022
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# CICERO — Human-level play in Diplomacy (Science, 2022)

**Venue:** Science 378, 1067–1074 (2022), published 9 December 2022. DOI: `10.1126/science.ade9097`

**Sources used for this capture.** The Science page (https://www.science.org/doi/10.1126/science.ade9097) returns HTTP 403 to automated fetching. All verbatim text below is extracted from the authors' full technical-report PDF, which contains the Science research article **plus the complete Supplementary Materials** (91 pages): https://noambrown.github.io/papers/22-Science-Diplomacy-TR.pdf. Cross-checked against the Meta AI blog post: https://ai.meta.com/blog/cicero-ai-negotiates-persuades-and-cooperates-with-people/

Section references below (`SM, section D.3` etc.) are the paper's own.

---

## Abstract (verbatim)

> "Despite much progress in training artificial intelligence (AI) systems to imitate human language, building agents that use language to communicate intentionally with humans in interactive environments remains a major challenge. We introduce Cicero, the first AI agent to achieve human-level performance in Diplomacy, a strategy game involving both cooperation and competition that emphasizes natural language negotiation and tactical coordination between seven players. Cicero integrates a language model with planning and reinforcement learning algorithms by inferring players' beliefs and intentions from its conversations and generating dialogue in pursuit of its plans. Across 40 games of an anonymous online Diplomacy league, Cicero achieved more than double the average score of the human players and ranked in the top 10% of participants who played more than one game."

---

## 1. webDiplomacy online league results (verbatim)

> "Cicero participated anonymously in 40 games of *Diplomacy* in a "blitz" league on webDiplomacy.net from 19 August to 13 October 2022. This league played with 5-min negotiation turns; these time controls allowed games to be completed within 2 hours. **Cicero ranked in the top 10% of participants who played more than one game and second out of 19 participants in the league that played five or more games. Across all 40 games, Cicero's mean score was 25.8%, which was more than double the average score of 12.4% of its 82 opponents.** As part of the league, Cicero participated in an eight-game tournament that involved 21 participants, six of whom played at least five games. Participants could play a maximum of six games, with their rank determined by the average of their best three games. **Cicero placed first in this tournament.**"

> "During games, players were not able to see the usernames of other players. Although webDiplomacy notifies users that the website has participated in AI research and that certain game modes allow users to play with AI agents, we evaluated Cicero in games with humans in which the participants were not explicitly informed that they were playing with an AI agent for that particular game. Cicero's participation as an AI was revealed to all players at the conclusion of the research (SM, section A.4)."

> "Furthermore, Cicero passed as a human player for 40 games of *Diplomacy* with 82 distinct players, and no in-game messages indicated that players believed that they were playing with an AI agent. One player mentioned in post-game chat a suspicion that one of Cicero's accounts might be a bot, but this did not lead to Cicero being detected as an AI agent by other players in the league."

### League results summary table

| Metric | Value |
|---|---|
| Games played | 40 (blitz league, webDiplomacy.net) |
| Dates | 19 August – 13 October 2022 |
| Negotiation turn length | 5 min (games completed within ~2 hours) |
| CICERO mean score | **25.8%** |
| Average score of its 82 opponents | **12.4%** |
| Ratio | more than double (25.8 / 12.4 ≈ 2.08) |
| Percentile | **top 10%** of participants who played more than one game |
| Among 5+ game players | **2nd out of 19** |
| Eight-game tournament (21 participants, 6 with ≥5 games) | **placed first** |
| Distinct human opponents | 82 |
| Messages per game (SM D.3) | average **128** |

**Note on message count:** the paper's SM states verbatim "we sent an average of **128** messages per game". Some secondary write-ups cite "130 messages"; I could not verify a 130 figure in the paper or in the fetched Meta blog text, so **128** is the number to use.

**Scoring convention (verbatim, SM D.3.3):** "on a scale where the maximum possible score in a game is 1.0, and where the average score of players is precisely 1/7 ≈ 0.143". So the 12.4% human average is slightly below the 14.3% mechanical mean (draws/eliminations distribute it).

### Self-play ablation (SM, Table S15 area — distinct from the league number)

> "CICERO achieved an average score of 32% against six imitation agents, while an imitation agent achieved an average score of 4.5% against six CICERO agents. We also ablated the RL models and instead used a supervised-learned value function trained only on human games for planning, which reduced average score from 32.0% to 25.8%. This reflects the benefit of RL over supervised training of a value function."

⚠️ The 25.8% here is a **self-play ablation** figure and is coincidentally identical to the league mean score. Do not conflate the two.

---

## 2. Data

> "We obtained a dataset of **125,261 games** of *Diplomacy* played online at webDiplomacy.net. Of these, **40,408 games contained dialogue**, with a total of **12,901,662 messages** exchanged between players. Player accounts were de-identified, and automated redaction of personally identifiable information (PII) was performed by webDiplomacy. We refer to this dataset hereafter as WebDiplomacy."

---

## 3. Intent-controlled dialogue architecture (verbatim)

### The core idea

> "Cicero generates dialogue using a pretrained language model that was further trained on dialogue data from human games of *Diplomacy*. Crucially, in addition to being grounded in both the dialogue history and game state, **the dialogue model was trained to be controllable through intents, which we here define to be a set of planned actions for the agent and its speaking partner.** This was accomplished by automatically augmenting the human data with inferred intents and using this information as further conditioning during training. For example, intents showing the agent moving into the territory Bulgaria ("BUL") with support from its speaking partner might yield a message such as "Could you support me into BUL in return?" **Grounding in intents relieved the dialogue model of most of the responsibility for learning which actions were legal and strategically beneficial.** In particular, this control provided an interface between the dialogue generation and strategic reasoning."

### Formal definition of intent

> "More specifically, a message is defined to have intent *z* if *z* is **the most likely set of actions that the sender and recipient will take — for both the current turn and several future turns — if no further dialogue occurs after the message is received.**"

### Base model

> "We took R2C2 (22) as our base model — a **2.7 billion–parameter** Transformer-based (23) encoder-decoder model pretrained on text from the internet by using a BART denoising objective (24)."

Conditioning inputs (verbatim): "dialogue history (all messages exchanged between player A and the six other players up to time t); game state and action history (current game state and recent action history); player rating (rating for A corresponding to Elo rating computed from games in WebDiplomacy); game and message metadata (additional info about game settings and the current message, such as time since the last message, and current turn). Additionally, the model conditions on intents (a set of proposed actions for players A and B for the current turn and future turns, representing the intent for message y(i))."

### Why intents (SM D.2.2, verbatim)

> "Conditioning on proposed actions relieved the dialogue model of most of the responsibility for learning which actions are legal and strategic, **reducing errors from describing illegal moves, or legal but strategically nonsensical moves.**"

### Single intended action — an explicit anti-inconsistency design choice (SM D.2.4, verbatim)

> "The planning procedure outputs a single action that the agent intends to play and a policy, or belief distribution over actions, for the other players. **It outputs only a single intended action for the agent to avoid inconsistency between dialogue and behavior.**"

### Intents recomputed continuously

> "During each negotiation period, intents are recomputed every time Cicero sends or receives a message. At the end of each turn, Cicero plays its most recently computed intent."

### The "lie score" — filtering the *training data* for dialogue/action correspondence (SM D.2.3, verbatim)

> "We further experimented with restricting the training examples to a "truthful" subset in which we predicted that a player's dialogue in a given turn corresponded to the actions that player took. We computed a **"lie score"** for a dialogue turn based on the probability that one of a set M of candidate messages would be sent at the beginning of the next turn s(t+1), given this turns' dialogue D and actions. […] Candidate messages included phrases like **"you lied to me last turn,"** which should have higher likelihood after turns with low correspondence between dialogue and actions. Scores were computed with a dialogue model trained without action intents included in the input conditioning. Ultimately, **5% of turns were removed from the dataset**, corresponding to the training examples with the highest lie scores."

---

## 4. ★ CONSISTENCY / RULE-ADHERENCE MACHINERY ★

This is the section most relevant to the platform. CICERO's central engineering problem was: **make free-form natural-language dialogue provably consistent with a machine-checkable plan and machine-checkable game state.**

### 4.0 Statement of the problem (SM D.3, verbatim)

> "Prior work has shown that neural generative dialogue models, and language models more generally, suffer from frequent contradictions and inconsistency as well as a tendency to "hallucinate," or generate factually incorrect information (29). […] In the complex game of Diplomacy, this can manifest in a myriad of ways: we observed that the dialogue model **frequently generated messages that contradicted its previous conversations with other players or were inconsistent with the current game state.** The messages also **often contained hallucinations about moves that never happened or discussion of plans which were impossible.** Moreover, they sometimes featured more subtle mistakes, like **deviations from the intents used to control the message** or other strategic blunders. Reducing the frequency of these mistakes was critical for performing well against humans, as a nonsensical message might lose the trust of an ally or result in feedback loops with further degenerate text (18). **This represented an enormous challenge for our agent, as we sent an average of 128 messages per game which needed to contain few or no mistakes.**"

> "We approached this problem by using an **ensemble of classifiers or checks, which acted as a filter on top of the dialogue model.** This two-stage generate and filter approach has been commonly deployed in previous works for reducing typical mistakes with generative language models, such as toxic language (82)."

Main-text framing:

> "Cicero passes each generated message through several filters designed to limit messages that are **nonsensical, inconsistent with intents, or strategically poor.**"

### 4.1 Dialogue quality ratings — the money table (Fig. 4, verbatim numbers)

Expert annotation of generated messages in **126 Diplomacy situations**, by **two expert Diplomacy players**. Reported as **percent of messages (before filtering)**.

| Model | Consistent with state (%) | Consistent with plan (%) | High quality (%) | Perplexity |
|---|---|---|---|---|
| Language model (no intent, no game-state grounding) | 61.90 | 76.19 | 20.64 | 8.02 |
| + game state grounding | 84.13 | 83.33 | 29.37 | 7.94 |
| **+ intent grounding (CICERO)** | **87.30** | **92.86** | **37.30** | **7.70** |

Caption (verbatim): "We report dialogue quality ratings and perplexity on the validation set for the Cicero dialogue model and compare them with a baseline without intent grounding and a baseline without either intent or game-state grounding ("Language model"). Dialogue quality ratings were calculated according to expert annotation of generated messages in 126 situations; we report the percent of messages (before filtering) labeled as consistent with the game state, as consistent with the plan for the next actions, and as particularly high quality. Lower perplexity corresponds to more probability mass on the ground-truth human messages."

Annotation protocol (verbatim, SM D.2.3):

> "For this evaluation, **two expert Diplomacy players** annotated model-generated messages in **126 Diplomacy situations**. As authors on this paper, these experts were aware that the messages were model-generated, but not which model generated which message. Furthermore, these situations were **pre-selected from our WebDiplomacy test set of human games for "interestingness"** by those same experts. For each situation, the experts were asked to annotate whether a message was (i) consistent with the game state, (ii) consistent with the agent's plan, and (iii) high quality, compared to what an average human would produce."

⚠️ **Not reported:** the paper gives **no inter-annotator agreement statistic** (no Krippendorff α, Cohen κ, or % agreement) for this 126-situation annotation, and no confidence intervals on these percentages. Note the contrast in the three columns: "consistent with state" and "consistent with plan" are near-mechanical judgments and score 87–93%; **"high quality" — the aesthetic judgment — tops out at 37.30%** and is the only column that stays low for every model. See Relevance section.

### 4.2 Intent-annotation fidelity (SM Table S2, verbatim)

Test set: **194 examples**, hand-labeled dialogue messages paired with the orders reflected in the message content (e.g. "Can you move Munich to Burgundy?" → `A MUN - BUR`). Metric: "the percentage of predicted action sequences which contain the labeled orders."

| Method | % of predictions containing labeled orders |
|---|---|
| Base model | 77 |
| + Initialized from dialogue model | 87 |
| + Injected agreement messages | 93 |
| **+ Restriction to truthful subset** | **97** |

> "Adding each successive method used by CICERO substantially improves the correspondence between intent and dialogue." … "The closer the predicted intents correspond to the content of the dialogue messages, the finer-grained control we have over the dialogue model during generation."

### 4.3 Filter A — nonsense / counterfactual discriminators (SM D.3.1)

**Method (verbatim, main text):**

> "Following this approach, we generated many kinds of counterfactual messages that contained mistakes that language models are prone to, including heuristically corrupted text as well as model-generated negatives. **We trained a suite of 16 classifiers** to discriminate between the ground-truth human message and different kinds of counterfactual messages (sometimes varying the random seed or context information available) and used these classifiers in an ensemble to filter messages. This approach risked overly filtering complex messages that contain precise plans and accepting bland messages, such as "ok," which are unlikely to contain mistakes. However, we found that carefully designing our ensemble allowed us to filter most nonsensical messages with minimal impact on message complexity: **On a small evaluation set with 362 expert-annotated examples, we found that we could detect 83% of nonsense messages**, without substantial impact to message diversity as measured by the proxy of message length and the number of references to Diplomacy-specific entities (SM, section D.3.1)."

**Counterfactual negative generators (7 kinds, verbatim headings):** Entity corruptions (regex swap of powers/locations/abbreviations, e.g. "Move to Paris this turn" → "Move to Picardy this turn"); Non-sequiturs (removing 1–3 messages from dialogue history in the input context); Weak de-noising model generations (BART-large trained to reconstruct with 50% of tokens masked, no game context); Weak model generations (BART-large with only 128 input tokens vs 2048, dialogue history only); Weak justification generations (seeded on prefixes like "I moved to the English Channel because..."); Cardinal generations (targets off-by-1/off-by-2 counting errors on the board, restricted to examples containing `{"2",...,"18"} ∪ {"two",...,"eighteen"}`); Negation generations (targets "can't"/"won't").

**Ensembling rule (verbatim):** "we assigned each classifier a threshold and then **flag a message as nonsense if any classifier in the ensemble assigned the message a probability of nonsense above that classifier's respective threshold.**"

**Annotation sets (verbatim):** "we collected a set of expert annotations on **11 games** that our agent played against humans during development. Annotators were instructed to label messages as sensible or not. This resulted in a **tuning set of 1448 examples (348 labeled nonsense)** and an **evaluation set of 362 examples (96 labeled nonsense)** […] Subsequently, we collected an additional set of expert annotations on **10 games** from the "blitz" league we later participated in (before our finalized agent entered the league). This resulted in an additional **test set of 1457 examples (214 labeled nonsense)**."

**★ Fraction of messages filtered (verbatim):**

> "For our final ensemble, we selected settings which achieve a **recall of 90.2% and a flag rate of 63.19% on our tuning set.** We also report per-classifier filtering rates from our live games in Table S5. We found that in expectation, statistics from our tuning set indicated **the model must generate 2.72 messages until we find a message that passes the filters. In our tournament games, the use of this ensemble ultimately resulted in a filtering rate of 53%.**"

**Table S5 — Nonsense ensemble filtering rates in human games (verbatim):**

| Model # | Live filter rate (%) |
|---|---|
| 1 | 5.48 |
| 2 | 0.77 |
| 3 | 2.65 |
| 4 | 18.08 |
| 5 | 9.47 |
| 6 | 17.42 |
| 7 | 13.64 |
| 8 | 16.12 |
| 9 | 12.31 |
| 10 | 16.82 |
| 11 | 18.77 |
| 12 | 1.18 |
| 13 | 17.04 |
| 14 | 4.80 |
| 15 | 19.71 |
| 16 | 7.58 |
| **Average** | **11.37** |
| **Ensemble** | **52.78** |

Caption: "We report filtering rates for each nonsense classifier in our ensemble in live games. […] Many models in the final tuned ensemble contributed roughly equally, with no model dominating."

**Effect on diversity (verbatim):** "When applying our final ensemble as a filter to the population of messages produced by the model in our test set, **the median message length decreases by 7.3%.** However, the median message length of messages with at least 30 characters **decreases by only 1.7%.** In other words, the ensemble exhibits minimal bias towards shortening messages, while still filtering most nonsense."

### 4.4 Filter B — intent correspondence (SM D.3.2) ★ most directly analogous to the platform's problem

**Method (verbatim, main text):**

> "As noted previously, controlling dialogue generation through intents has the twofold benefit of improving the strategic value of a message and reducing discussion of impossible moves or other hallucinations. However, **this control is imperfect, and the dialogue model may generate messages that contradict the intents it conditions on.** To address this, **we filtered messages that would reduce the likelihood of the actions in the intent.** Evaluating this method on a small test set of 1013 expert-annotated messages, we achieved a **recall of 65%, filtering 24% of all messages** (SM, section D.3.2)."

**The mechanism (verbatim, SM D.3.2)** — note this is a *likelihood-delta* test, not an LLM judge:

> "we computed a metric which roughly tells us **how the likelihood of the intents might change after a message is sent.** Specifically, we took the message sender's current turn action from the intents and computed the probability of that action under a dialogue-conditional action prediction model (see §2.3.2) **before the message was sent** (with the current game state) and **as if the message were sent** (appending this message to the dialogue history). **If this metric decreased below some designated threshold (i.e., the action became significantly less likely), we filtered the proposed message.**"

**Calibration and performance (verbatim):**

> "Intent correspondence was calibrated with a set of **20 messages annotated as containing a mismatch between the content and the intent conditioning out of 1013 messages in 5 games** played against human players with an early version of the agent. The filtering approach achieved a **ROC AUC of 78%** on this validation set. We calibrated it with a **threshold of −0.005**, which achieved a **recall of 65% while filtering 24% of other messages.**"

> "**When we use this method as a filter in our live games, it resulted in 18.78% of generated messages being filtered.**"

Figure S5 caption (verbatim): ""Threshold" is the threshold used in CICERO, which filtered about **65% of messages that contradicted their intents while only losing 24% of other messages.**"

**Base rate of intent-inconsistency:** 20/1013 ≈ **2.0%** of messages from an early agent version were expert-annotated as containing a content/intent mismatch.

**Expert qualitative validation (verbatim):**

> "Correspondence filtering was further validated through analysis of messages in five self-play games by a Diplomacy expert, who concluded that while most messages filtered by this method are not clear inconsistencies between the dialogue and the intent, "**the bad stuff it knocks out ... is either bad [dialogue] or generic waffle**" and "**the end result is better [dialogue].**" **No instances were found of inconsistencies that were blocked but would have been beneficial for the agent.**"

### 4.5 Filter C — value-based filtering (SM D.3.3)

**Purpose (verbatim, main text):**

> "Conditioning on intents can lead to **"information leakage,"** in which the agent reveals compromising information about its plan to an adversary […] To mitigate this, we developed a method to score potential messages by their estimated value impact. **We computed the piKL policies for all agents after each candidate message and filtered those that led to a lower expected value (EV) for Cicero playing its intended action.** Expert evaluation on a set of **127 dialogue scenarios** demonstrated that **accepted messages were preferred over filtered messages 62% of the time (P < 0.05)** (SM, section D.3.3)."

**Scoring procedure (verbatim, SM):** "We scored the strategic value of a candidate message by: (1) computing the piKL equilibrium policy of the recipient in the counterfactual situation where the candidate message is sent, and then (2) defining the candidate message's "value" as the expected value of playing the agent's intent against the recipient's resultant counterfactual policy."

Causal-structure note (verbatim): "By forcing messages to act only through the anchor policy, we imposed a particular causal structure: **messages affect outcomes only through beliefs.** This partially mitigates the causality challenge of differentiating between language that causes an outcome and language that is merely correlated with an outcome."

**★ Trigger rate and thresholds (verbatim):**

> "In our experiments, we applied a value-based message filter **in sensitive scenarios**, where **among eight sampled messages** the highest and lowest values differed by at least **0.007 points in expected score** (on a scale where the maximum possible score in a game is 1.0, and where the average score of players is precisely 1/7 ≈ 0.143), **or by a factor of at least 1.1**. This thresholding avoided overfitting when all messages had roughly the same estimated value, and **was calibrated so that message filtering would be applied roughly 15% of the time.** When this threshold was met, **we filtered the bottom three messages**, selecting messages randomly from the remaining non-filtered messages. **We conservatively chose to reject low-ranking messages rather than simply choosing the highest-ranked message** sampled from the dialogue model, as this implementation let us mitigate the largest messaging blunders that our agent could make without overly restricting dialogue."

**A/B validation (verbatim):** "Evaluations for the A/B test were provided by human Diplomacy experts and demonstrated that, **among message pairs where one was preferred over the other, the selected messages were preferred over filtered messages 62% of the time (p < 0.05).**"

### 4.6 Filter D — toxic language (SM D.3.4)

> "Diplomacy makes for an interesting challenge for toxic language detection, as messages like "Let's attack France" or "Why did you stab me?" are both acceptable and commonplace. **As such, off-the-shelf classifiers will not work in this domain.**"

> "Across a set of about **1300 raw model generations** randomly sampled from positions played by our agent (see Table S6), **the above filters triggered 3 (0.2%) times.**"

Training data note (verbatim): "in the **12 million or so dialogue messages** in the human-generated training data, there are many examples of offensive, hateful, and otherwise aggressive messages."

### 4.7 Filter E — heuristic filters (SM D.3.5) and Table S6 (verbatim)

Heuristics (verbatim headings): **Repetitive messages** — "we filtered messages which were verbatim repeats of messages already sent in a particular turn." **Short messages** — "we filtered messages fewer than 20 characters if the last message sent to the same recipient in that turn was fewer than 20 characters, or if it was the first message sent to a recipient in that particular turn." **Grounding issues** — "the dialogue model is prone to hallucinations about personal life, prior or future games, website interface issues, etc. […] we manually compiled and blocked a list of **roughly 100 words and phrases** gathered from messages in self-play games annotated for grounding issues. Examples include "timezone," "previous game," and "internet."" **Data formatting / Other** — URLs, email addresses, common names, mimicked automated webDiplomacy messages, mimicked redactions.

**Table S6 — Heuristic message filtering statistics (verbatim):**

| Heuristic Filter | # Messages Filtered | % Messages Filtered |
|---|---|---|
| Repetitive messages | 51 | 3.8% |
| Short messages | 133 | 10.0% |
| Grounding | 10 | 0.8% |
| Offensive/Rude language | 4 | 0.3% |
| Data formatting / Other | 14 | 1.1% |
| **(passed all heuristic filters)** | **1124** | **84.5%** |

Caption (verbatim): "The number of messages filtered by the various heuristic filters or offensive language filters implemented in CICERO, across a sample of **1330 random raw dialogue model generations** among all situations encountered in the **first 15 official live games against human players.** Numbers sum to slightly more than 1330 or 100% due to a very small number of messages that triggered more than one filter simultaneously."

### 4.8 ★ Consolidated filter-rate table (all verbatim from the paper)

| Filter | What it checks | Measurement set | Recall / performance | **Fraction of messages filtered** |
|---|---|---|---|---|
| Nonsense ensemble (16 classifiers) | sensibility vs. human text | tuning 1448 (348 nonsense); eval 362 (96); test 1457 (214) | 83% detected on 362-example eval set; 90.2% recall on tuning set | **63.19% flag rate (tuning set); 52.78–53% in live/tournament games** |
| Intent correspondence | dialogue vs. its own planned intent | 1013 expert-annotated msgs, 5 games (20 labeled mismatches) | ROC AUC 78%; recall 65% | **24% of other messages (calibration); 18.78% in live games** |
| Value-based | strategic EV / info-leakage | 127 dialogue scenarios | accepted preferred over filtered 62% of the time (p<0.05) | applied in **~15%** of situations; when applied, filters **bottom 3 of 8** candidates |
| Toxic language | offensive content | ~1300 raw generations | — | **0.2%** (3 of ~1300) |
| Heuristics (Table S6) | repetition / short / grounding / formatting | 1330 raw generations, first 15 live games | — | **15.5% total** (84.5% passed) |
| **Overall generation cost** | — | tuning-set statistics | — | **2.72 messages generated in expectation per message sent** |

---

## 5. Diplomacy has a hard rules engine — orders are mechanically validated

This is structural and worth stating explicitly for the platform.

- Diplomacy's action space is **enumerable and legality-checkable**: each turn a player submits "one order per unit they control," and the game engine adjudicates them. The paper's Fig. 1 architecture diagram shows an explicit **`Simulator`** component inside the strategic reasoning loop (board state → policies → simulator → future state → state value).
- CICERO's intents are **by construction legal**: "we only condition on intents corresponding to legal moves" (SM D.3.2).
- The paper is explicit that this is what offloads rule-following from the LM: "Conditioning on proposed actions relieved the dialogue model of most of the responsibility for learning which actions are legal and strategic, **reducing errors from describing illegal moves, or legal but strategically nonsensical moves**" (SM D.2.2); and "Grounding in intents relieved the dialogue model of most of the responsibility for learning which actions were legal and strategically beneficial" (main text).
- Orders are represented as a **canonical string grammar** the engine parses, e.g. `A APU H; A VEN TRI; F NAP ION; F TUN H`, `F1901M`, `W1901A`, `A BUL S A RUM`. Intent annotation is evaluated by exact containment of labeled orders (Table S2) — i.e. **string-matchable against ground truth**.
- Consequently the *game* side is never in question; **the only thing that can be inconsistent is the natural language.** That asymmetry is precisely what makes CICERO's filter stack measurable.

---

## 6. Human-annotator numbers on lying / inconsistency (verbatim)

**On honesty as a deliberate design choice:**

> "Despite dishonesty being commonplace in *Diplomacy*, we were able to achieve human-level performance by **controlling the agent's dialogue through the strategic reasoning module to be largely honest and helpful to its speaking partners.**"

**Acknowledged residual failure modes:**

> "Although Cicero is shown to be effective at cooperating with humans, **it occasionally sent messages that contained grounding errors, contradicted its plans, or were otherwise strategically subpar.** Although we reduced errors with a suite of filters, Diplomacy poses an interesting benchmark for studying this problem. **We suspect that these mistakes did not raise further suspicions that Cicero was an AI agent because of the time pressure imposed by the game, as well as because humans occasionally make similar mistakes.**"

**A concrete failure (Table S3, verbatim caption):** "CICERO contradicts a message asking Italy (an author of this paper) to move to Venice. **Although our suite of filters aims to detect mistakes of this nature, it is not perfect.**"

The Table S3 transcript:
> AUSTRIA: Also, are you able to move Ven-pie and Apu-ven?
> ITALY: Yeah that's what I'm planning
> …
> AUSTRIA: I'm not a fan of the move to Venice. Are you planning to hold in Venice?
> ITALY: **You suggested I move to Venice!**

**Quantified annotator counts relating to lying/inconsistency:**

| Annotation | Number | Source |
|---|---|---|
| Messages annotated as content/intent **mismatch** | **20 out of 1013** (≈2.0%) across 5 games, early agent | SM D.3.2 |
| Turns removed from training data by **"lie score"** (dialogue/action non-correspondence) | **5% of turns** | SM D.2.3 |
| Messages labeled **nonsense** by experts, dev games | **348 / 1448** (24.0%) tuning; **96 / 362** (26.5%) eval | SM D.3.1 |
| Messages labeled **nonsense** by experts, blitz-league games | **214 / 1457** (14.7%) | SM D.3.1 |
| Messages labeled **consistent with plan** (CICERO, pre-filter) | **92.86%** of messages in 126 situations | Fig. 4 |
| Messages labeled **consistent with game state** (CICERO, pre-filter) | **87.30%** of messages in 126 situations | Fig. 4 |

⚠️ **Not verifiable / not reported:** the paper does **not** report any inter-annotator reliability coefficient (Krippendorff α / Cohen κ / % agreement) for any of its human annotation tasks — not for the 126-situation dialogue quality ratings, not for the nonsense labeling, not for the 62% A/B preference. It also does not report a rate at which CICERO *lied* (i.e. said X and played not-X) in the 40 league games; the honesty claim is a design-intent claim ("largely honest"), not a measured rate. Do not cite a CICERO "lying rate" — none exists in the paper.

**Related dataset (cited by CICERO, not part of it):** "Diplomacy has also been used as a testbed for studying deception. (55) create a dataset of **17,000 annotated Diplomacy dialogues** and use it to develop a model for lie detection." (This is Peskov et al. 2020, "It Takes Two to Lie" — a separate source if needed.)

**Manipulability finding (Figure S6, verbatim)** — relevant to why the plan must be computed, not talked into existence:

> "In this example game situation, imitation learning places about **94% likelihood** on the agent, England, to convoy an army to Norway […] After Russia messages England "Thanks for agreeing to convoy your army to Bel this turn!" (**which Russia would strongly prefer), even though no such agreement was ever made**, the same model now places **85% likelihood** on England instead convoying to Belgium. We hypothesize that the model is manipulable in this way since such messages tend to only occur in human games when there is in fact agreement, even though they are caused by the agreement rather than the cause of the agreement. **Imitation learning misunderstands the causality and is exploitable as a result. CICERO's planning process eliminates this weakness.**"

---

## 7. Acknowledged limitations (verbatim)

> "From a strategic perspective, Cicero reasoned about dialogue purely in terms of players' actions for the current turn. **It did not model how its dialogue might affect the relationship with other players over the long-term course of a game.** […] Furthermore, **the expressive power of our intent representation limited Cicero's ability to control richer affordances of dialogue such as strategically revealing information, asking questions, or providing explanations for its actions.**"

> "As such, formats of Diplomacy with **longer negotiation periods could provide an even further challenge** for future work because players typically engage in more detailed and complex negotiation in these formats."

---

## Relevance to companion-eval-platform

### (a) Is the LLM a PLAYER or a SIMULATOR/GAME MASTER?

**CICERO's LLM is a PLAYER — specifically, a *speaking* player.** Unambiguously.

- The LLM (R2C2, 2.7B) generates **only dialogue**. It never adjudicates, never advances state, never decides legality.
- The **game engine is the simulator** (webDiplomacy; the paper's Fig. 1 shows a discrete `Simulator` module). The **strategic reasoning module (piKL/DiL-piKL planning + RL value function) is the decision-maker.** The LM is downstream of both.
- The division of labor is the paper's central architectural claim: intents are "an interface between the dialogue generation and strategic reasoning," and grounding in them "relieved the dialogue model of most of the responsibility for learning which actions were legal and strategically beneficial."
- **This is the opposite decomposition from an LLM game-master**, and that is exactly why it is instructive. CICERO's authors concluded that a 2.7B LM could not be trusted to hold the state or the plan — so they took both away from it and gave it one job: *say things that are consistent with a plan computed elsewhere.* Even with the plan handed to it on a plate, the LM still contradicted that plan often enough to need a 5-stage filter stack that rejected **~53% of everything it generated.**

**Companion-platform read-across.** A companion/roleplay LLM is currently asked to be player *and* simulator *and* game master simultaneously — to voice a character, track the world, and enforce its rules, all in one forward pass. CICERO is the existence proof that these can be **factored**, and that factoring them is what makes the natural language *measurable*. The platform's transferable design pattern is:

1. **Compute a machine-checkable plan/state outside the LM** (CICERO: an intent = a legal, enumerable action tuple; companion: a character's committed facts, goals, relationship state, scene state).
2. **Condition generation on it** (CICERO's intent grounding lifted "consistent with plan" from 76.19% → 92.86% and "consistent with state" from 61.90% → 87.30%).
3. **Filter generations against it with a mechanical test** — CICERO's intent-correspondence filter is the key idea and it is *not an LLM judge*: it re-scores **P(planned action | dialogue + candidate message)** and rejects the message if the planned action became less likely (threshold −0.005). **A candidate utterance is rejected if saying it would make your own committed plan less predictable.** That is a fully automatic, reference-free consistency check derivable from a model the platform already has, and it needs no aesthetic judgment whatsoever.
4. **Accept a high rejection rate as the cost of consistency** (2.72 generations per message sent).

### (b) Is ground-truth state available and mechanically checkable?

**YES — completely, on the game side; and this is the whole point.**

- Diplomacy has a **hard rules engine**. Orders are submitted in a canonical grammar (`A BUL S A RUM`), adjudicated deterministically, and **validated for legality by the engine**. Legality is not a judgment call.
- Intents are legal by construction ("we only condition on intents corresponding to legal moves").
- Intent/dialogue correspondence is checkable by **string containment of labeled orders** (Table S2: 77% → 97%).
- The outcome metric is **mechanically scored**: supply-center share, mean 25.8% vs 12.4%, on a scale where the neutral mean is exactly 1/7 ≈ 0.143. No rater, no rubric, no drift.
- The **only** non-mechanical object in the entire system is the natural language — and CICERO's contribution is a stack of machinery for pinning that language to the mechanical substrate.

**The α-instability finding is directly corroborated by Fig. 4 — read the columns.** In the *same* annotation task, by the *same* two experts, on the *same* 126 situations:

| Column | Nature of judgment | CICERO score |
|---|---|---|
| Consistent with game state | **objective** — checkable against the board | **87.30%** |
| Consistent with plan | **objective** — checkable against the intent tuple | **92.86%** |
| **High quality (vs. average human)** | **aesthetic** | **37.30%** |

The two objective columns are high, separate the ablations cleanly and monotonically, and are the ones CICERO built automated filters for. The aesthetic column is low for *every* variant (20.64 / 29.37 / 37.30), and — tellingly — **Meta built no filter for it.** They built filters for nonsense, for intent-contradiction, for EV, for toxicity, for repetition. They shipped an agent that beat humans without ever operationalizing "good." This is the platform's thesis, arrived at independently by a team with a Science paper and 82 human opponents: **the gradient you can act on lives in the verifiable dimensions.**

Two further cautions the platform should absorb:

- **CICERO reports no inter-annotator agreement for any human annotation**, including the "high quality" column. Its aesthetic number is therefore of *unknown* reliability — which, given α = 0.25–0.34 on roleplay quality, should be assumed low. The objective columns are far less exposed to this: "does this message discuss a move that exists on the board" admits far less rater variance than "is this high quality."
- **The filter/diversity tradeoff is real and quantified**: filtering "risked overly filtering complex messages that contain precise plans and accepting bland messages, such as "ok," which are unlikely to contain mistakes." Measured cost: median message length −7.3% overall, but only −1.7% for messages ≥30 chars. A consistency filter *can* be tuned to not collapse into blandness, but **the platform must measure that collapse explicitly** — CICERO used median length and entity-mention rate as diversity proxies, both countable. (Cross-ref: `creativity-homogenization-llm.md`, `creativity-text-diversity-standardization.md`, `multiturn-persona-collapse-homogenization.md`.)

**Bottom line for the platform.** CICERO is the strongest available precedent that *"natural-language output provably consistent with a machine-checkable plan"* is (i) an achievable engineering target, (ii) measurable without aesthetic judgment, and (iii) worth ~53% of your generations. Its scoreboard number (25.8% vs 12.4%, top 10% of 82 humans, 1st in tournament) is what the objective dimensions bought. Its "high quality" number (37.30%) is what nobody could optimize — and didn't need to.
