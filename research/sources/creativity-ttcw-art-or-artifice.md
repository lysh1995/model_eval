---
title: "Art or Artifice? Large Language Models and the False Promise of Creativity"
url: https://arxiv.org/abs/2309.14556
html_url: https://arxiv.org/html/2309.14556v3
authors: Tuhin Chakrabarty, Philippe Laban, Divyansh Agarwal, Smaranda Muresan, Chien-Sheng Wu
year: 2024
venue: CHI 2024
type: paper
accessed: 2026-07-16
topic: creativity-measurement
---

# TTCW — Torrance Test of Creative Writing

## Framing

Adapts the **Torrance Tests of Creative Thinking (TTCT)** — which measures creativity as *process* via Fluency, Flexibility, Originality, Elaboration — into a measure of creativity as **product**, using Amabile's **Consensual Assessment Technique (CAT)** as the epistemic basis (expert consensus IS the ground truth).

## The 14 binary tests (verbatim wording, by dimension)

**Fluency (5 tests)**
1. Narrative Pacing: "Does the manipulation of time in terms of compression or stretching feel appropriate and balanced?"
2. Scene vs Exposition: "Does the story display awareness and insight into the balance between scene and summary/exposition?"
3. Language Proficiency & Literary Devices: "Does the story make sophisticated use of idiom or metaphor or literary allusion?"
4. Narrative Ending: "Does the end of the story feel natural and earned, as opposed to arbitrary or abrupt?"
5. Understandability & Coherence: "Do the different elements of the story work together to form a unified, engaging, and satisfying whole?"

**Flexibility (3 tests)**
6. Perspective & Voice Flexibility: "Does the story provide diverse perspectives, and if there are unlikeable characters, are their perspectives presented convincingly?"
7. Emotional Flexibility: "Does the story achieve a good balance between interiority and exteriority, in a way that feels emotionally flexible?"
8. Structural Flexibility: "Does the story contain turns that are both surprising and appropriate?"

**Originality (3 tests)**
9. Originality in Theme and Content: "Will an average reader of this story obtain a unique and original idea from reading it?"
10. Originality in Thought: "Is the story an original piece of writing without any cliches?"
11. Originality in Form & Structure: "Does the story show originality in its form?"

**Elaboration (3 tests)**
12. World Building and Setting: "Does the writer make the fictional world believable at the sensory level?"
13. Character Development: "Does each character in the story feel developed at the appropriate complexity level, ensuring that no character feels like they are present simply to satisfy a plot requirement?"
14. Rhetorical Complexity: "Does the story operate at multiple 'levels' of meaning (surface and subtext)?"

**Scoring**: each test is BINARY (pass/fail) + a written justification. Story score = number of tests passed (0–14). This is the key design decision: binary + justification, not a Likert scale.

## Benchmark

- 48 short stories: 12 by professionals (published in *The New Yorker*), 36 by LLMs (ChatGPT/GPT-3.5, GPT-4, Claude v1.3) — 12 each.
- 10 expert annotators (creative writing MFA-level / published writers), 3 evaluations per story.
- 2,016 binary labels + expert-written justifications.

## Validation numbers

**Pass rates (average across 14 tests):**
| Source | Pass rate |
|---|---|
| New Yorker (professional) | 84.7% |
| Claude v1.3 | 30.0% |
| GPT-4 | 27.9% |
| GPT-3.5 | 8.7% |

Headline: "LLM-generated stories pass 3-10X less TTCW tests than stories written by professionals."

**Inter-annotator agreement:** individual test agreement ranges **0.27 to 0.66, averaging Fleiss Kappa = 0.41** (moderate). Aggregate (total score) correlation reaches **0.69** — i.e. *individual binary tests are noisy, but the 14-test SUM is substantially more reliable*. This is the single most important design lesson: aggregate, don't trust one item.

**LLMs as TTCW judges:** "none of the LLMs positively correlate with the expert assessments"; correlations with experts "close to zero." Tested GPT-4, Claude, etc. This is the strongest negative result on LLM-judge creativity assessment.

## Cost

- Expert compensation: **$80** per task, task duration **2 to 2.5 hours**.
- 10 participants completed on average 3.6 tasks over 3 weeks.
- Implies roughly $80 / ~2.25h per story-triple pass → expert TTCW is on the order of tens of dollars per story per annotator. Not scalable; use as a calibration set only.

## Dimension specialization finding

GPT-4 more likely to pass Originality tests; Claude v1.3 more likely to pass Fluency, Flexibility, Elaboration. Models differ *per dimension* — a single scalar creativity score would have hidden this.
