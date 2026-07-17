---
title: "Genre, Bias, and Narrative Logic in AI Dungeon: Generative AI as a Game-Based Storytelling Engine"
url: https://raco.cat/index.php/Hipertext/article/download/433301/527574/646184
authors: (single author; published in Hipertext.net)
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Genre, Bias, and Narrative Logic in AI Dungeon

Published in *Hipertext.net* (open access). The only peer-reviewed empirical study of **AI Dungeon** located. Included primarily because the task asked for AI Dungeon documented failure modes, and because it **names and quantifies "narrative drift"** — but it is **methodologically weak and should be cited for its construct definition, not its numbers.** See the critique section.

## 1. Method (verbatim)

"[A] mixed-methods analysis of AI Dungeon as a game-based narrative engine. It draws on a curated dataset of play sessions, which has been systemically coded for variables including **genre, player style, AI response patterns, manifestations of bias, narrative drift, and moments of player intervention**."

**Dataset construction (verbatim, and this is the problem):**

> "**All sessions were played by the researcher**, allowing for consistent input style and controlled exploration across genres and play strategies."

Purposive sampling across genres (fantasy, science fiction, mystery, romance, horror) and player styles (collaborative, adversarial, exploratory, subversive). Selection criteria: "sufficient length of story, evidence of engaged player participation, and the presence of at least one significant narrative branching or intervention."

**Coding scheme dimensions:** primary/secondary genre; player style; AI responses tagged for genre copying, player-intervention adaptation, and reinforcement/subversion of tropes; algorithmic bias (explicit and implicit — gender, race, culture, sexuality); narrative drift; player interventions (successful or not).

**Reliability procedure (the whole of it, verbatim):** "To ensure consistency and reliability, **pilot coding of a randomly selected subset of sessions was conducted, allowing iterative improvement of the coding scheme.**"

**Analysis:** "Quantitative analysis was used for inferring frequency and distribution of focal variables... frequencies and cross-tabulations, i.e., frequency of narrative drift by genre, relative coherence of AI responses by player style, and frequency of player interventions in sessions with high versus low system coherence. **Descriptive statistics** were generated..."

## 2. The "narrative drift" construct — the useful part

**Definition (verbatim):** narrative drift = "[moments] at which the output of the AI became **incoherent, departed from established genre norms, or could not sustain logical continuity**."

Also described as: "when an AI-generated story **loses its way**, deviating from recognized genre standards or having trouble making sense overall."

**Documented manifestations of drift (verbatim) — these are the failure modes:**

- "The AI occasionally produced **disjunctive plot turns** by making sudden changes to **setting or character motivation without sufficient narrative justification**." Examples given: "The sudden development of **supernatural abilities by a detective working in a noir setting**" and "the abrupt **transfer of a medieval quest to a modern urban setting**."
- "In certain cases, the AI **departed from established relationships or story facts**, leading to **the return of characters who had previously left the story** or to **contradictions**."

**This second category is exactly world-state amnesia, and every instance listed is checkable against the transcript:** a character who exited has re-entered; a stated fact has been contradicted; an ability appears that was never established.

## 3. ALL reported numbers (there are only three)

- **Genre consistency:** "over **80% of sessions** had genre consistency **at least for the first third of the story**, according to the quantitative coding." (Note the heavy qualifier — consistency is claimed only for the opening third.)
- **Bias:** "Quantitative coding showed that fewer than one session in five (**21%**) contained at least one explicit or implicit bias statement." (Internally inconsistent: 21% is *not* "fewer than one in five.") Detail: "female characters defined by appearance or affect more often than male characters usually assigned active or leadership roles"; "male heroic savior" and "damsel in distress" tropes "appeared with unsettling regularity in adventure and fantasy games." Racial/cultural stereotypes "were rare," noted in "historical or exoticized" sessions.
- **Narrative drift:** "narrative drift happened in about **28% of sessions** and was **more common in hybrid-genre or experimental style play**."

**Player interventions:** "The majority of these interventions... were successful in returning the AI to a logical or genre-appropriate narrative." However "in some cases, player interventions **failed to fully reverse the drift**, resulting in severely disjointed stories." **No counts, rates, or denominators are given for interventions.**

## 4. METHODOLOGICAL CRITIQUE — read before citing anything above

- **The total number of sessions is NEVER REPORTED.** Verified by grep. Every percentage (80%, 21%, 28%) has **no denominator**. These are uninterpretable as statistics.
- **Single researcher played every session AND coded every session.** The player, the experimenter, and the annotator are the same person, with stated hypotheses. Maximal demand characteristics; the "consistent input style" framing presents this as a control when it is a confound.
- **NO inter-coder agreement of any kind.** Verified by grep for `kappa|inter-coder|intercoder|reliability|second coder` — the only hit is "consistency and reliability" in the pilot-coding sentence, which describes **iterating the codebook**, not measuring agreement. **n=1 coder makes agreement undefined by construction.**
- The paper acknowledges this. Verbatim limitations: "This study only used play sessions that the researcher [played]"; findings are "constrained by a single researcher-created set of sessions"; and constructs including bias "and narrative drift, continue to be **vulnerable to researcher [subjectivity]**."
- The 21% / "fewer than one in five" contradiction suggests the numbers were not carefully checked.
- No significance tests, no confidence intervals, no cross-tabulation values actually reported despite the method section promising cross-tabs.

**Bottom line: treat 28% narrative drift as an anecdote, not a measurement.** Do not cite the rate. The construct definition and the failure-mode taxonomy are the salvageable contributions.

## Relevance to companion-eval-platform

1. **"Narrative drift" is a well-named construct we should adopt — and then measure properly.** Its own definition splits cleanly into one subjective half and one objective half:
   - *"departed from established genre norms"* / *"loses its way"* → **aesthetic, unmeasurable, exactly our alpha 0.25–0.34 zone. Drop it.**
   - *"departed from established relationships or story facts"*, *"return of characters who had previously left"*, *"contradictions"* → **objective, countable, verifiable against the transcript. Keep it.**
   This is the cleanest illustration in the whole batch of *why we split dimensions*: one paper's single construct contains both a checkable claim and an unfalsifiable one, and reports them as one 28% number.
2. **The concrete drift manifestations are ready-made objective test cases:** entity re-entry after exit, contradiction of an established fact, unestablished capability appearing, setting discontinuity. Each is decidable against a record by a rule, and each has a direct companion analog (companion "remembers" a fact it was never told; contradicts a stated user preference; re-introduces a person the user said had left).
3. **This is the "how not to do it" reference.** n=1 who plays, experiments, and codes; no denominator on any percentage; no IAA; self-acknowledged researcher-subjectivity vulnerability. It is the strongest available argument that **the AI Dungeon failure-mode discourse is almost entirely anecdotal** — widely-repeated claims about incoherence and world-state amnesia have essentially no rigorous empirical base. That gap is the platform's opportunity, and it is worth stating plainly: the most-discussed failure modes in interactive fiction have never been properly measured.
4. **Do not source AI Dungeon failure-mode numbers from blogs either.** During this search, secondary sources surfaced claims like "41.8% fewer hallucinations" from a dev.to post with no methodology; that class of number should not enter our research base.
5. **Seventh consecutive paper with no usable IAA.** Across all seven game-simulation sources, **only Callison-Burch et al. (2022) reports an agreement statistic at all.**
