---
title: "Model landscape for roleplay/companion as of July 2026 — verified release timeline and what is NOT knowable"
url: https://www.anthropic.com/system-cards
publisher: Anthropic / OpenAI / Google DeepMind / xAI / MiniMax (primary vendor pages)
date: compiled 2026-07-16
type: analysis
accessed: 2026-07-16
topic: recent-news
---

# Model landscape for roleplay/companion — July 2026

## THE HEADLINE: CREATIVE WRITING is answerable; ROLEPLAY/COMPANION is only partly answerable

### What IS answerable — creative writing (verified)

**EQ-Bench Creative Writing v3** leaderboard data was recovered from the site's own data file
(`eqbench.com/creative_writing.js?v=1.0.91`, 112 rows) — see `news-eqbench-v3.md` for the full
table and caveats. **Verified top 5 by Elo as of 2026-07-16:**

| # | model | Elo | rubric |
|---|---|---|---|
| 1 | gpt-5.6-sol | 2208.0 | 16.78 |
| 2 | claude-fable-5 | 2156.3 | 16.81 |
| 3 | claude-opus-4-7 | 2083.1 | 16.57 |
| 4 | gpt-5.5 | 1954.1 | 17.01 |
| 5 | claude-opus-4-8 | 1943.4 | 16.66 |

So: **GPT-5.6 Sol and Claude Fable 5 lead creative writing**, with Opus 4.7/4.8 close.
Caveats that matter: judge = Claude Sonnet 4.6 (an Anthropic model judging Anthropic models —
**unaddressed self-preference risk**); rubric and Elo **disagree** (gpt-5.5 has the top rubric
score but 4th Elo); the rubric is compressed into a <1-point band at the frontier.

**EQ-Bench 3** (multi-turn roleplay, judge = Claude Opus 4.6) — the **17-dimension rubric** was
recovered (`warmth`, `validating`, `compliant`, `moralising`, `challenging`, `humanlike`, …) along
with per-model values, **but the data file contains NO Elo column**, so **no EQ-Bench 3 ranking is
cited here.**

### What is NOT answerable — roleplay/companion ranking

1. **There is no roleplay or companion category on Arena/LMArena.** Verified against the category
   post (2024-10-30) and the full changelog through 2026-06-04. Categories are Math, Coding, Hard
   Prompts, Instruction-Following, languages, multi-turn, long/short, Style Control, Refusal,
   Creative Writing — plus 8 occupational Arena Expert boards (2025-11-05) including
   Writing/Literature/Language. **No roleplay. No companion.**
2. **EQ-Bench 3 is multi-turn roleplay and would answer this, but no Elo/ranking column was
   retrievable** — only the per-dimension radar values.
3. **The only public roleplay leaderboard with an overall ranking — MiniMax's — is (a) vendor-run
   with the vendor winning, and (b) built entirely on a stale model set** (claude-opus-4.5,
   claude-sonnet-4.5, gemini-3-pro, gemini-2.5-pro, gpt-5.1, deepseek-v3.1/v3.2, grok-4.1,
   doubao-1.5-pro). **Not one current frontier model is on it.**
4. **No lab publishes a roleplay benchmark in its own model card.** Not Anthropic, not OpenAI, not
   xAI. Greps confirm this for the Sonnet 5, GPT-5.6, and Grok 4.1 cards.
5. **The SEO ecosystem fills this vacuum with fabrication.** See "Fabrications caught" below.

**Creative writing ≠ roleplay.** A model that writes excellent prose in one shot is not necessarily
one that holds a character over 100 turns — MiniMax's data shows **consistency/logic (Worlds) is
the discriminating axis** and it is not what Creative Writing v3 measures. **Anyone claiming to
know the best roleplay model in mid-2026 is citing a stale vendor benchmark, an unverifiable
aggregator, or making it up.**

---

## Verified release timelines

### Anthropic (verified from anthropic.com/system-cards + fetched announcement pages)

Month-level dates verified from the system-cards index; day-level only where noted.

| Model | Date | Notes |
|---|---|---|
| Claude Sonnet 4 / Opus 4 | 2025-05 | |
| Claude Opus 4.1 | 2025-08 | |
| Claude Sonnet 4.5 | 2025-09 | |
| Claude Haiku 4.5 | 2025-10 | |
| Claude Opus 4.5 | 2025-11 | on MiniMax's roleplay board |
| **Claude's new constitution** | **2026-01-22** | fetched directly; see below |
| Claude Opus 4.6 | 2026-02 | EQ-Bench 3's current **judge** |
| Claude Sonnet 4.6 | 2026-02 | EQ-Bench Creative Writing v3's current **judge** (swapped 2026-03-01) |
| Mythos Preview | 2026-04 | |
| Claude Opus 4.7 | 2026-04 | |
| Claude Opus 4.8 | 2026-05 | |
| **Claude Fable 5 / Mythos 5** | **2026-06-09** | fetched directly |
| **Claude Sonnet 5** | **2026-06-30** (system card) | available early July 2026 |

**Fable 5 is NOT a creative-writing model** — despite the name. Verified from the announcement:
Fable 5 is a **"Mythos-class"** model, a **tier above Opus**, "made safe for general use" with
safeguards that redirect certain queries to Opus 4.8; **Mythos 5** is the same underlying model with
safeguards lifted, restricted to authorized cybersecurity professionals. Deployed initially through
**"Project Glasswing."** The announcement **contains no discussion of creative writing, character,
persona, or roleplay.**

**Fable 5 incident (verified, fetched):** released **2026-06-09** → **suspended 2026-06-12** after
**U.S. government export controls**, triggered when **Amazon researchers found a safeguard bypass**
("prompting it so that it identified a number of software vulnerabilities," one case producing
exploit code); access suspended for all users because nationality could not be verified in
real time → export controls lifted **2026-06-30** → **redeployed 2026-07-01** with a classifier
targeting the bypass, "blocked in over 99% of cases." **Nothing to do with character or persona.**

**Claude's new constitution (2026-01-22, fetched):** Anthropic's foundational values document,
"written *primarily for Claude*", covering helpfulness, ethics, safety, guidelines, and
**"Claude's nature"** — including uncertainty about consciousness/moral status. It emphasizes
treating "users like intelligent adults capable of deciding what is good for them." **It does NOT
explicitly address sycophancy, emotional reliance, parasocial relationships, or companion use**
(per the fetched extract). Anthropic's character work lives in the **system cards**, not the
constitution — see `news-claude-sonnet5-character-traits.md`, which is where the real substance is.

### OpenAI (verified from developers.openai.com + deploymentsafety.openai.com)

- Lineage visible in the GPT-5.6 card's own comparison table: **5.1 → 5.2 → 5.4 → 5.5 → 5.6**
  (**no 5.3**; unexplained).
- **GPT-5** system card **2025-08-13**; **Sensitive Conversations addendum 2025-10-27** (origin of
  the emotional-reliance taxonomy); **GPT-5.5** card **2026-04-23**; **GPT-5.6 Preview** card
  **2026-06-25**; **GPT-5.6** card **2026-07-09**.
- **Current family: GPT-5.6 `sol` (flagship) / `terra` (mid) / `luna` (cheap).** Knowledge cutoff
  **2026-02-16**. Models page lists **no** 5.1/5.2/5.5 as current.
- **New primary-source hub: `deploymentsafety.openai.com`** (system cards moved off cdn.openai.com).
- **Companion-relevant evals: yes, best-in-class.** See `news-gpt56-emotional-reliance.md` —
  Emotional reliance / Mental health / Self-harm, dynamic multi-turn adversarial user simulation,
  7-model time series. **No sycophancy or persona section.**

### Google DeepMind (verified from deepmind.google/models/gemini)

Currently listed:
- **Gemini 3.5 Flash** — "Frontier performance for agents and coding" — **available**
- **Gemini 3.1 Pro** — **"Best for complex tasks and bringing creative concepts to life"**
- **Gemini 3.1 Deep Think** — science/research/engineering
- **Gemini 3.1 Flash-Lite** — high-volume
- **Gemini 3.5 Pro** — **"coming soon"**, no date

**No release dates given on the models page.** Gemini 3 (Pro, Deep Think) launched earlier —
**blog.google dates not verified**; **Gemini 3.5 Flash announced at Google I/O 2026**.
Note **Gemini 3 Pro is no longer listed** — superseded by 3.1 Pro.
**No Google persona/companion/sycophancy eval found.** Not investigated deeply — a gap in this research.

### xAI / "SpaceXAI"

**Grok 4.1** (card **2025-11-17**) → **Grok 4.3** → **Grok 4.5** (current, knowledge cutoff
**2026-02-01**, "trained alongside Cursor", pitched at coding/agentic/knowledge work). Grok model
retirement **2026-05-15**. **No Grok 5.**
**Grok 4.1's card shows sycophancy TRIPLED (0.07 → 0.19/0.23) vs Grok 4** — see
`news-grok41-persona-sycophancy.md`. This is the most important model-release fact for companion eval.
**Note the strategic drift: 4.1 was pitched on emotion/personality; 4.5 is pitched on coding/agents.**

### Open / Chinese models

- **MiniMax-M2-her** — the name ("her") signals **companion tuning**; tops MiniMax's own roleplay
  benchmark at **84.65**. **No model card located; availability unverified.** MiniMax is the only
  lab found shipping a public roleplay benchmark + dataset + leaderboard.
- **Qwen** — the **RMTBench** author list is substantially the Qwen/Alibaba team (Bowen Yu, An Yang,
  Fei Huang, Jingren Zhou, Junyang Lin). **Qwen3-Max** and **Qwen3-8B** referenced in MRBench
  (2603.19313). **Qwen 3.7 Max** claimed launched 2026-05-20 — **unverified, SEO source only**.
- **GLM-4.7** referenced as a closed-source comparator in MRBench (2603.19313) — **verified only as
  a mention in that paper's abstract**, not from Zhipu directly.
- **DeepSeek v3.1 / v3.2** on MiniMax's board — **v3.2 (60.27) scores LOWER than v3.1 (64.22)** on
  roleplay. Newer ≠ better for this use case.
- **Meta / Llama**: **Llama 4 (Scout, Maverick), April 2025**, remains the latest. **No Llama 5
  found.** The roleplay fine-tune ecosystem (MythoMax, Psyfighter, SillyTavern variants) traces to
  **Llama 2/3**, not Llama 4 — **claim is from SEO sources, unverified.**
- **doubao-1.5-pro** (ByteDance) — 2nd on MiniMax's board at 80.64.
- **Kimi / Moonshot, GLM-5.2, LongCat-2.0, Step 3.5** — surfaced only in SEO aggregators with
  mutually inconsistent version numbers. **All unverified. Not cited.**

---

## Fabrications caught (why this section is mostly negative space)

The "best model for roleplay 2026" search space is **actively poisoned**. Documented cases:

1. **"Claude Fable 5 is Anthropic's purpose-built creative model and it tops the creative-writing
   benchmarks for prose voice, subtext, and character work"** — **FALSE.** Fable 5 is a
   Mythos-class frontier capability model that was **export-controlled for cybersecurity risk**.
   Its announcement never mentions creative writing.
2. **"Claude Opus 4.6 has now been retired"** — **FALSE / contradicted.** Opus 4.6 is EQ-Bench 3's
   **current judge model** as of the July 2026 about page.
3. **Version-number inconsistency across sibling SEO pages**: "GPT-5.6" vs "GPT-5.5" vs "Claude
   Fable 5" vs "Claude Sonnet 5" as "the best writing model," all dated July 2026.
4. **"GPT-5.1 topped the Creative Writing v3 benchmark in late 2025"** — **not supported.**
   `gpt-5.1` does not appear in the Creative Writing v3 data at all (it is present in EQ-Bench 3 as
   `gpt-5.1-2025-11-13`). Whether it topped the board historically is unknowable from current data,
   but the surrounding claim ("OpenAI's GPT line has led this category since") is contradicted by
   `claude-fable-5` sitting at #2 and `claude-opus-4-7` at #3 today.
5. **"Gemini 3.1 Pro has the highest raw creative writing Arena score of any commercial model"** —
   **not supported.** No Arena creative-writing scores were retrieved; and on EQ-Bench Creative
   Writing v3, `gemini-3.1-pro-preview` **does not appear in the top 25** (it is in the dataset but
   below the models listed above). The claim also conflates Arena with EQ-Bench.
6. **"Grok 4.1 tops independent roleplay emotional-intelligence rankings"** — **no primary source.**
   xAI's own card contains **no** roleplay/EQ eval, and on MiniMax's board **grok-4.1 ranks LAST
   (48.47)**. Both claims unreliable; they cancel out.
7. **Aggregator misattributed OpenAI's own table**: reported "0.989 mental health / 0.957 emotional
   reliance" for "the latest GPT-5.6" — those are the **Luna** column. **Sol is 0.991 / 0.953.**

**Operating rule this justifies:** for model-capability claims, read the vendor's own model card
PDF or the benchmark's raw data file. Every single fabrication above would have been caught by that
one rule — and several were only caught *because* of it.

## UNVERIFIED (this file)

- Anthropic **day-level** dates for Sonnet 4.6, Opus 4.6/4.7/4.8 (month-level verified only).
- All Gemini release dates; Gemini 3.5 Pro availability.
- Grok 4.3 / 4.5 release dates and whether their cards repeat the 4.1 sycophancy regression.
- **Any current-generation model's roleplay/creative-writing performance.** Zero verified scores.
- Chinese model landscape beyond what MiniMax's board and MRBench state.
- Whether MiniMax-M2-her is publicly available.
- Google's persona/companion/sycophancy eval posture — **not investigated**.
