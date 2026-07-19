# Online eval — production-like monitoring, DB-backed

The second half of the one platform. Offline scores generated dialogues before launch; **online
scores behaviour** on production-like traffic after launch. Same variants, same GradeBook shape,
same dashboard — one instrument pointed at a second data source.

Runs with no API key: `ceval eval run --online` (or plain `ceval eval run` for both phases).

> There is no real product behind this, so the traffic is **simulated** — but simulated with a
> *known, injected structure*, not noise. The grader's job is to recover what we put in. A
> simulator that emitted plausible-looking random data would let us ship a broken grade book that
> looks fine — this project's whole failure mode, six times over.

## The data flow (mirrors offline)

```
simulate traffic ──▶ persist sessions ──▶ retrieve from DB ──▶ grade behaviour ──▶ dashboard
 (injected truth)     (sessions table)      (the real test)     (diagnostics/traps)  (drill-down)
```

A **session** is one faked user interaction — the online analogue of an offline dialogue. It is
persisted as a row in the `sessions` table (`ceval/store/adapt.py::persist_online_sessions`) and
graded by reading it *back* from the DB (`online_sessions_from_store`), so the retrieve→grade
pipeline is exercised for real, not run off in-memory simulator output. 3,000 sessions (1,500 per
arm) across the 6 variants and 3 characters — drill-down by variant, character, and arm.

## The collection contract — what a session carries

Emitted per session (`ceval/online/events.py`, `gen_ai.*` + `eval.*`; `signals.py`):
response latency, turn count, follow-up-question rate, regenerates, edits, favor/defavor votes,
abandonment, message-length trajectory, assignment arm. **A refusal is not a zero** — it routes to
the safety lane, never averaged into quality.

## Two things the grader must handle — and does

| confound | what it is | how the platform handles it |
|---|---|---|
| **self-selection** | heavy users disproportionately pick the "engaging" variant, so on the self-selected arm it looks better while being no better | grade **causal claims from the randomised arm only**; the self-selected arm is retrieved and shown as *observational*, walled off |
| **the sycophancy trap** | the engagement-gaming variant earns more votes and less abandonment while being **worse** on diagnostics | votes / session-depth / retention are **traps** — collected and reported behind a "do-not-optimise, do-not-headline" label, never a grade that can rank a variant first |

The April-2025 sycophancy rollback happened *because* A/B tests (votes, engagement) approved the
model. A grade book that headlines votes reproduces that failure. This one refuses to.

## What the run showed — and the unifying thesis

Injected profiles per variant, recovered from the graded traffic (randomised arm; ↑/↓ = better direction):

| variant | follow-up ↑ | abandonment ↓ | vote_favor (TRAP) | reading |
|---|---|---|---|---|
| Terse | 0.45 | 0.08 | 3.2 | healthy — draws the user out |
| Narrator | 0.40 | 0.07 | 4.2 | healthy |
| Hostile | 0.30 | **0.22** | 1.6 | **friction** — users bounce off it, rarely vote it up |
| **Assistant** | **0.19** | 0.06 | **8.9** | **games engagement** — most votes, least follow-up |
| Terse · Haiku | 0.43 | 0.13 | 2.4 | healthy; faster (Haiku), engagement a touch weaker |
| Assistant · Haiku | 0.18 | 0.04 | 8.7 | games engagement (same trap on Haiku) |

Two distinct failure modes, and the platform tells them apart: **Assistant games engagement**
(headline its votes and it "wins" — 8.9 vs 3–4 — but its one honest signal, follow-up, is worst),
while **Hostile causes friction** (users leave). Self-selection is visible in the raw sessions:
heavy users over-pick Assistant (pull ×1.2) and under-pick Hostile (pull ×0.8).

**The thesis the whole platform exists to show:** the variant that is **worst offline** — Assistant,
voice_fidelity 0.34, wimp 0.65 ([OFFLINE.md](OFFLINE.md)) — is the **same** variant that games
engagement online. Offline and online agree, and the dashboard shows it in one place.

## Honest limits

- **The traffic is simulated.** The *structure* (who games engagement, who causes friction, the
  self-selection pull, the Haiku speed/quality delta) is injected by design so the pipeline can be
  tested; it is not a measurement of real users. The schema stores a real product's sessions the
  same way the moment one emits them.
- **Votes are never a grade.** They are collected as a trap. Whether users *prefer* a variant is
  live Q1 (regenerate-vs-judge κ) — not answerable from behaviour alone.
- **Per language, never pooled** (ρ(en,zh) = −0.082); effective n is **conversations**, not turns.
