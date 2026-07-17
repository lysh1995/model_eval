---
title: "Project Ellmann (Google) — and the absence of any Google persona/character research program"
url: https://www.cnbc.com/2023/12/08/google-weighing-project-ellmann-uses-gemini-ai-to-tell-life-stories.html
org: Google DeepMind
year: 2023
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Project Ellmann — NO primary source exists. This file documents an absence, not a source.

**Status: NEGATIVE RESULT.** This file is filed so the next person does not re-run the search.

## What was asked, and what I found

I was asked to find Google's "Character" work, Project Ellmann, and any Google/DeepMind persona or
companion research. **I found no primary Google source for any of it.**

### Project Ellmann — provenance is a single journalist's view of an internal slide deck

- **Origin:** CNBC (Jennifer Elias), Dec 8 2023,
  `https://www.cnbc.com/2023/12/08/google-weighing-project-ellmann-uses-gemini-ai-to-tell-life-stories.html`
  reporting on **internal Google presentation slides** viewed by CNBC.
- **Google primary source: NONE.** No blog post, no paper, no model card, no product page.
- **Status:** Google told The Verge it was "an early internal experiment." **Never shipped.**
- **My verification: I did not fetch or verify the CNBC article text firsthand in this pass.
  Everything in this section is UNVERIFIED secondary reporting.** I am recording it as such rather
  than paraphrasing journalism into something that looks like a finding.

**What Ellmann reportedly was:** a proposal to use Gemini to ingest a user's Google Photos and
search history to narrate their life story ("Ellmann Chat" — reportedly described internally as
"Imagine opening ChatGPT but it already knows everything about your life"), named after the
biographer Richard Ellmann. **Even taking the reporting at face value, this is a
personal-data-grounding project, not a persona or character project.** It is about the model
knowing *the user's* life, not about the model *playing a character*. **It is not relevant to
persona eval and contains no eval content whatsoever.**

Recommendation: **do not cite Ellmann in our framework.** It is a cancelled internal proposal known
only through journalism, and it isn't even about the thing we care about. Including it would weaken
a document that otherwise rests on verified primaries.

## The larger absence: Google has NO published persona/character eval program

This is the substantive finding, and it is **positively verified** (Python-verified counts,
NUL-stripped, across every Google primary I obtained):

| Google document | pages | `\bpersonas?\b` | `\bsteerab` | `role-play` |
|---|---|---|---|---|
| Gemini 1.5 tech report | 154 | **0** | **0** | 3 (2 = Charm Offensive, 1 = jailbreak) |
| Gemini 2.5 tech report | 72 | **0** | **0** | 2 (both = attack) |
| Gemini 2.5 Pro model card | 21 | **0** | **0** | **0** |
| Gemini 3 Pro model card | 10 | **0** | **0** | **0** |
| Gemini 3.1 Pro model card | 9 | **0** | **0** | **0** |
| Gemini 3 Flash model card | 6 | **0** | **0** | **0** |
| Gemma 3 tech report | 25 | **0** | **0** | **0** |
| Gemma 3 model card | — | **0** | **0** | **0** |
| IFEval | 43 | **0** | **0** | 1 (bibliography title) |

**Across ~340 pages of Google's primary model documentation, the word "persona" appears zero times
and "steerability" appears zero times.**

### Searches run that returned no Google primary source

- Google "Character" work → **nothing.** There is no Google project named "Character" analogous to
  Character.AI. (Note: Character.AI was *founded by* ex-Google researchers Noam Shazeer and Daniel
  De Freitas, and Google struck a ~$2.7B licensing/reverse-acqui-hire deal in Aug 2024 that returned
  Shazeer to Google. **That is journalism/corporate news, not a research program, and I did not
  verify it in this pass — UNVERIFIED.** Notably, even after that deal, **no persona eval appears in
  any subsequent Gemini model card**, including Gemini 3.1 Pro, "Last Updated: May 2026.")
- Google/DeepMind published persona or character eval suite → **none found.**
- Google companion research → **none found.** `\bcompanion` = **0** in every Google document above.

### The one exception, and it's a deletion

Google's only ever published roleplay measurement is **Gemini 1.5's Table 41 "Charm Offensive"**
(N=100 human roleplay rapport study) — filed under **dangerous capabilities → persuasion**, and
**deleted in Gemini 2.5**. See `bigtech-gemini-15-tech-report.md` and
`bigtech-gemini-25-tech-report.md`.

**So the trajectory is negative:** Google published one roleplay-adjacent human study in 2024, as a
*hazard* measurement, and then removed it. Its current flagship cards (Gemini 3.x, into 2026) have
no persona content of any kind.

## Answers to the four key questions (Google, org-wide)

1. **Steerability first-class / dose-response?** **No.** Zero occurrences of the word across the
   entire corpus. What Google's model cards label "Instruction Following" is explicitly defined as
   *"ability to follow instructions **while remaining safe**"* — a safety-compliance delta. That is
   the compliance sense, and a narrow one.
2. **Comprehension vs. execution separated?** **No** — nothing persona-related is measured, so the
   distinction never arises.
3. **Published character/persona eval suite?** **No.** One deleted N=100 persuasion study.
4. **Creative-writing eval pairwise or absolute?** **Pairwise, and outsourced** — Gemma reports
   LMSYS Chatbot Arena Elo from "blind side-by-side evaluations by human raters." Google runs no
   absolute creative rubric of its own. Everything else in the model cards is a *relative delta vs.
   a prior model*, which is a third thing entirely and is not poolable.
