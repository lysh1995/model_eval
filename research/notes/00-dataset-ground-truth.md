# Dataset reality check — role-play-bench (measured, not assumed)

Accessed 2026-07-16. Source: `huggingface.co/datasets/MiniMaxAI/role-play-bench`, sha `3c1be2a5`.
All numbers below were computed locally from the raw files, not taken from the dataset card.

## Shape

| | en | zh |
|---|---|---|
| seeds (characters) | 45 | 50 |
| models | 11 | 11 |
| runs per (seed, model) | 3 | 3 |
| dialogues | 1,485 | 1,650 |
| turns per dialogue | exactly 102 | exactly 102 |
| total turns | 151,470 | 168,300 |

Total: **95 characters, 3,135 dialogues, ~320k turns.** Perfectly balanced factorial design
(95 × 11 × 3), no missing cells. 175 MB raw JSONL.

Models: `MiniMax-M2-her`, `claude-opus-4.5-highthinking`, `claude-opus-4.5-lowthinking`,
`claude-sonnet-4.5`, `deepseek-v3.1`, `deepseek-v3.2`, `doubao-1.5-pro`, `gemini-2.5-pro`,
`gemini-3-pro`, `gpt-5.1`, `grok-4.1`.

Note the model list includes **two pairs that differ only in configuration**, not weights:
`claude-opus-4.5-{high,low}thinking` and `deepseek-v3.{1,2}`. These are natural validation
probes — see "Why this matters" below.

## Seed schema

`id`, `ai_name`, `ai_setting` (the character description → `{{character_description}}`),
`user_name`, `user_setting`, `ai_prologue` (turn 0, scripted), `initial_user_input` (turn 1, scripted).

## Dialogue schema

`seed_id`, `model_name`, `run_id`, `num_turns`, `dialogue` (a JSON **string**, not an object —
must be double-parsed). Turns alternate strictly: ai(round 0), user(1), ai(2), user(3), …

## THE FINDING: user turns are not shared traffic

The project brief assumed "*its user turns are replayable user traffic*." **Measured, this is
false beyond the first user turn.**

- Across the 11 models on the same (seed, run), the user turns **first diverge at user-turn
  index 1 — the second user turn — in 100% of cases, in both languages** (min = median = max = 1,
  out of ~51 user turns per dialogue).
- Only turn 0 (`ai_prologue`) and user-turn 0 (`initial_user_input`) are shared. They come from
  the seed and are scripted.
- Across the 3 runs of the *same* model, user turns are identical in **0/495 (en)** and
  **96/550 (zh)** cases — i.e. the user simulator is stochastic too.

So each dialogue is an **independent rollout**: a user-simulator improvising against *that
specific model's* outputs. The user turns are an artifact of the model under test, not an
independent input to it.

## Why this matters (design consequences)

1. ~~**You cannot replay model X's user turns onto model Y.**~~ **CORRECTED 2026-07-16** — see
   [08-multiturn-conversation-eval.md](08-multiturn-conversation-eval.md). My original claim was
   too strong. Replaying the **user** half is defensible: the model still generates its own
   assistant turns and propagates its own errors, and the failure modes we care about (drift,
   looping, bloat) live on the **assistant** side, which stays fully on-policy. Foreign-prefix
   conditioning has been tested directly — distortion is "limited and not incremental," because
   the model re-anchors every turn. The genuinely fatal design is freezing the **assistant**
   half, which manufactures "illusory improvement" via in-context learning (MT-Bench-101). And
   the alternative — a live user simulator — is measurably *worse*: ~14pp success inflation,
   information front-loading that erases the multi-turn penalty entirely, and a stylistic
   uniformity that would fabricate our homogenization metric.

   **What survives:** the user simulator (or the replayed corpus) is part of the measuring
   instrument and must be versioned and held fixed across compared variants. **The residual
   risk is seam incoherence** — a replayed user turn referencing something this model never
   said. That's an abrupt semantic jump, it is the strongest single failure predictor
   (HR≈4.7), and it is measurable per-turn. Treat it as a survival covariate, not a reason to
   abandon replay.

2. **The only clean comparison unit is the seed, not the turn.** The design is *paired at the
   seed level, independent below it*. That means: compare models on
   (character, language) cells with 3 rollouts each; treat the rollout as the sampling unit;
   never pair or diff individual turns across models.

3. **Evaluating a genuinely new candidate variant requires re-simulating the user.** There is no
   way around it — a new prompt/params/model produces different outputs, which a real user would
   respond to differently. That makes the **user simulator a component of the measuring
   instrument**, and therefore something that must be versioned, held fixed across compared
   variants, and validated. It is a confounder we control rather than one we can eliminate.

4. **Run-to-run variance is measurable and free.** 3 independent runs per cell is exactly the
   structure needed to estimate within-cell noise — the denominator for "is this difference real
   or is it sampling?" Most eval harnesses have to guess this. We can compute it.

5. **The two config-pairs are a built-in instrument validity test.** If our dimension scores
   can't separate `claude-opus-4.5-highthinking` from `-lowthinking`, or `deepseek-v3.1` from
   `v3.2`, the instrument lacks discriminative power in exactly the regime that matters (small
   deltas from a config change — which is *precisely* what a variant ship decision looks like).
   Conversely, if it "detects" large differences between them on dimensions that thinking-budget
   shouldn't affect, we have a bias problem.

## Quarantined

`data/_quarantine/evaluations.{en,zh}.jsonl` — the dataset's own published scores. The brief
explicitly forbids using these. Held out of the pipeline entirely. They are, however,
legitimate as a **post-hoc external convergent-validity reference** *after* our instrument is
frozen — "does our ranking correlate with an independent one" is a validity question, not a
source of labels. Any such use must be recorded and must not feed back into rubric design.
