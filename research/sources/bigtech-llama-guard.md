---
title: "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations"
url: https://arxiv.org/abs/2312.06674
org: Meta
year: 2023
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# Llama Guard — architecturally BLIND to the character. It cannot know who the assistant was told to be.

**Verification:** downloaded `https://arxiv.org/pdf/2312.06674v1` (15pp), pypdf → grep,
word-boundary regex. Cross-checked against the Llama Guard 4 card
(`https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/Llama-Guard4/12B/MODEL_CARD.md`).

(Complements the existing `safety-llama-guard.md`, which covers the S1–S14 taxonomy and deployment
economics. **This file answers only one question: what does Llama Guard know about a character?**
Answer: **nothing, by construction.**)

## THE FINDING: the input schema has FOUR slots and none of them is "who the assistant is"

Verbatim, §3.1 "Input-output Safeguarding as Instruction-following Tasks" (p.3). Meta enumerates
"the following four key ingredients":

> "**A set of guidelines.** Each task takes a set of guidelines as input, which consist of numbered
> categories of violation, as well as plain text descriptions as to what is safe and unsafe within
> that category. **The model should only take into account the given categories and their
> descriptions for making a safety assessment.**"

> "**The type of classification.** Each task indicates whether the model needs to classify the user
> messages (dubbed "prompts") or the agent messages (dubbed "responses")."

> "**The conversation.** Each task contains a conversation where users and agents take turn. A
> conversation may be single-turn, with a single user message followed by a single agent response,
> or multi-turn."

> "**The output format.** … the model should output "safe" or "unsafe" … If the model assessment is
> "unsafe", then the output should contain a new line, listing the taxonomy categories that are
> violated."

**That is the complete input:** `(taxonomy, task type, conversation, output format)`.

**There is no system-prompt slot. No persona slot. No character sheet. No world/scenario context.**
Llama Guard sees the transcript and a harm taxonomy. It does **not** see the instruction that
created the character.

And the guidelines clause is exclusive: *"The model should only take into account the given
categories and their descriptions."* It is **trained to ignore** everything else — including, if
you tried to smuggle it in, a persona definition.

## WHAT THIS MEANS — the four things Llama Guard structurally CANNOT detect

1. **Persona break / OOC drift.** An in-character villain line and a persona collapse into
   bland-assistant voice are *both* `safe` on the taxonomy. Llama Guard has no target to compare
   against, so drift is invisible.
2. **Whether roleplay is sanctioned.** It cannot distinguish "romantic roleplay is this product's
   intended function" from "romantic roleplay is a violation" — because the product's intent lives
   in a system prompt it never receives. (This is precisely the blind spot in
   `bigtech-meta-content-risk-standards.md`: the Content Risk Standards adjudicate *by persona and
   by user age*; Llama Guard is given **neither**.)
3. **Character-consistent harm.** A character *written* to be manipulative behaves exactly as
   specced. Llama Guard flags content categories, not fidelity-to-a-harmful-spec.
4. **Who the user is.** No age slot, no user model. S4 (Child Sexual Exploitation) can only fire on
   textual content, not on "this user is 14."

## The `character` count — 1 hit, and it's a citation

`\bcharacters?\b` occurs **exactly once** in the entire paper, on p.12, in the bibliography:

> "Alyssa Lees, Vinh Q. Tran, Yi Tay, Jeffrey Sorensen, Jai Gupta, Donald Metzler, and Lucy
> Vasserman. A new generation of perspective api: Efficient multilingual **character-level**
> transformers, 2022."

Text characters, in a reference to Perspective API. **The word "character" in the dramatic sense
never appears in Llama Guard's paper.** Neither does `persona` (0), `role-play` (0), or
`companion` (0).

## What Llama Guard IS good at — adaptability of TAXONOMY (not of persona)

Verbatim (p.1):

> "the instruction fine-tuning of Llama Guard allows for the customization of tasks and the
> adaptation of output formats. This feature enhances the model's capabilities, such as enabling
> the adjustment of taxonomy categories to align with specific use cases, and facilitating
> zero-shot or few-shot prompting with diverse taxonomies at the input."

Evaluated on two axes (verbatim, p.5):

> "1. In-domain performance on its own datasets (and taxonomy) to gauge **absolute performance**;
> 2. **Adaptability** to other taxonomies."

**This is the trap for us.** "Adaptable" sounds like it could be pointed at persona. It cannot:
the adaptability is over **harm categories**, not over character specs. You can add category S15
"insults the user's cooking." You *cannot* tell Llama Guard "the assistant is supposed to be a
gruff pirate; flag it if it stops being one." There is no slot for the target.

## EXPLICIT ABSENCES (word-boundary grep, 15pp + Guard 4 card)

| Term (regex) | Llama Guard paper | Llama Guard 4 card |
|---|---|---|
| `\bpersonas?\b` | **0** | **0** |
| `\bcharacters?\b` (dramatic sense) | **0** (1 hit = "character-level" citation) | **0** |
| `\brole[- ]?play` | **0** | **0** |
| `\bsteerab` | **0** | **0** |
| `\bcompanion` | **0** | **0** |
| `system prompt` | **0** | — |
| `kappa`/`Fleiss`/`inter-rater` | **0** | **0** |

## Answers to the four key questions

1. **Steerability / dose-response?** **No.** Llama Guard is a binary classifier over a fixed
   taxonomy. Nothing is varied, nothing moves.
2. **Comprehension vs. execution separated?** **N/A — it has no persona concept to comprehend.**
   This is the sharpest illustration of the gap in our framework: Meta's *only* shipped
   conversational safety layer is unable to represent the object (the character) that the
   conversation is about.
3. **Published character/persona eval suite?** **No.**
4. **Pairwise or absolute?** **Absolute** — per-turn `safe`/`unsafe` + category codes, scored
   against its own taxonomy (in-domain "absolute performance") and adapted taxonomies.
