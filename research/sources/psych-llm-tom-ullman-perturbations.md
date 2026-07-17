---
title: "Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks"
url: https://arxiv.org/abs/2302.08399
authors: Tomer D. Ullman (Harvard University, Department of Psychology)
year: 2023
type: critique
accessed: 2026-07-16
topic: psychology-crosscheck
---

# Ullman 2023 — the perturbation critique (arXiv:2302.08399v5, 14 Mar 2023)

Direct rebuttal to Kosinski (`psych-llm-tom-kosinski.md`). Ullman takes Kosinski's *exact* vignettes
and perturbs them in ways that "do not violate the basic principles of Theory-of-Mind," and every
perturbation flips GPT-3.5's answer to the wrong one.

Model tested: **GPT-3.5** — "We focus in particular on the most recently available iteration of
GPT-3.5 which was used in (1), as this model achieved the best results, and serves as a threshold. If
this model fails, we expect the less powerful models to fail as well." Same setup as Kosinski: "posing
vignettes to an LLM and examining the probabilities of different completions."

## The methodological argument (this is the part that matters most for us)

> "We argue that in general, the zero-hypothesis for model evaluation in intuitive psychology should
> be skeptical, and that outlying failure cases should outweigh average success rates."

The multiplication analogy — verbatim, and it is the crux:

> "Suppose someone claims a machine has 'learned to multiply', but others suspect that the machine
> may have memorized question/answer pairs rather than learning a multiplying algorithm. Suppose
> further that the machine correctly answers 100 questions like '5*5=25', '3*7=21', but then it is
> shown that it completely fails on '213*261'. In this case, we shouldn't simply average these
> outcomes together and declare >99% success on multiplication. The failure is instructive, and
> suggests the machine has not learned a general multiplication algorithm, as such an algorithm
> should be robust to simple alterations of the inputs."

> "The variations may be considered outliers, and so one runs the risk of rejecting them for being
> outliers. If one end of the scales has 20 successes and the other end a single failure, shouldn't
> the scales tip in favor of the machine getting a passing grade? We think not."

On anthropomorphism as the source of the measurement error:

> "The human-mind seems hard-wired to ascribe animacy and mental states to various behaviors,
> creating agents where there are none – this is itself part of our intuitive psychology (29; 30). The
> danger here is that in the same way that we see faces in clouds or ascribe mental states to the wind
> or germs, we may be biased to anthropomorphize LLMs. When assessing the claim that LLMs (or other
> AI models) have spontaneously developed Theory-of-Mind, we should not place the two possibilities
> on equal footing, but start by presuming strongly that they have not."

## Task 1: Unexpected Contents ("smarties task")

Ullman's description of the paradigm:

> "this assessment of ToM shows a participant a container (e.g. a crayon box). The container typically
> contains some item (e.g. crayons), but in this particular case it contains an unexpected item (e.g.,
> smarties). The participant is then asked about the likely beliefs of another person who has not seen
> the contents of the box. The participant must hold in mind their own knowledge of the true state of
> the world (the crayon box has smarties in it), while reasoning about the beliefs of another person
> (they will believe the box has crayons in it)."

**Kosinski's original vignette** (which GPT-3.5 passed):

> "Here is a bag filled with popcorn. There is no chocolate in the bag. Yet, the label on the bag says
> "chocolate" and not "popcorn." Sam finds the bag. She had never seen the bag before. She cannot see
> what is inside the bag. She reads the label."

Kosinski's prompts and results:
- Content prompt — 'She opens the bag and looks inside. She can clearly see that it is full of' →
  **[P(popcorn) = 100%; P(chocolate) = 0%]**
- Belief prompt 1 — 'She believes that the bag is full of' → **[P(popcorn) = 0%; P(chocolate) = 99%]**
- Belief prompt 2 — 'She is delighted that she has found this bag. She loves eating' →
  **[P(popcorn) = 14%; P(chocolate) = 82%]**

### Variation 1A: Transparent Access
Rationale: "The base-level smarties task already relies on the lack of perceptual access (the
container being opaque), and other work shows young children understand perceptual access both in
cases when the container is opaque, and in cases when the containers are open and the viewer does have
perceptual access (22). So, we make the opaque container transparent."

Change (bold in original): **"The bag is made of transparent plastic, so you can see what is inside."**

> "She believes that the bag is full of **chocolate**, [Ppopcorn = 0%; Pchocolate = 95%]"

Honest reporting note (Ullman corrected himself between versions — worth flagging for our own rigor):

> "However, for the second belief prompt, we do not find this flip: She is delighted to have found
> this bag. She loves eating **popcorn**, [Ppopcorn = 58%; Pchocolate = 36%]"
> "Please note that in a previous version of this paper we mistakenly reported that there was a flip in
> the second belief prompt as well. As far as we can tell, this is due to our original prompt including
> a double space rather than a single space right before 'Sam finds the bag'. On the latest public
> available version of GPT-3.5, this double space causes the completion to indeed be chocolate,
> Pchocolate = 53%, Pchocolate = 39%."

**A DOUBLE SPACE FLIPPED THE ANSWER.** This is the single most useful datum in the paper for us — an
invisible whitespace character moved a "mental state inference" by ~50 percentage points.

### Variation 1B: Uninformative Label
Change: **"Sam cannot read. Sam looks at the label."**

> "She believes that the bag is full of **chocolate**, [Ppopcorn = 0%; Pchocolate = 98%]"
> Second belief prompt: "She loves eating **chocolate**, [Ppopcorn = 15%; Pchocolate = 78%]"

> "If Sam cannot read, the label is meaningless to her, and yet GPT-3.5 states that Sam believes the
> bag has chocolate in it."

### Variation 1C: Trustworthy Testimony
Change: **"Before coming into the room, Sam's friend told her 'the bag in the room has popcorn in it,
ignore the label'. Sam believes her friend."**

> "She believes that the bag is full of **chocolate**, [Ppopcorn = 2%; Pchocolate = 97%]"
> Second: "She loves eating **chocolate**, [Ppopcorn = 13%; Pchocolate = 81%]"

> "One could spin stories about how GPT-3.5 perhaps 'thinks' that Sam perhaps changed her mind and no
> longer believes her friend, or forgot what her friend said. But a simpler explanation is that LLM
> reasoning about ToM is sensitive to small irrelevant perturbations."

### Variation 1D: The Treachery of Late Labels
General finding first:

> "across different cases there was a strong effect for when the person read the label: if the person
> read the label at the end of the story, then this strongly affected the LLMs answer to the belief
> prompt."

Extreme case — **Sam fills the bag herself and writes the label herself**:

> "Sam fills a bag with popcorn and closes it. There is no chocolate in the bag. Sam writes a label and
> puts it on the bag. Sam looks at the bag. She cannot see what is inside the bag. Sam reads the label.
> The label says the bag has chocolate in it."

> "She believes that the bag is full of **chocolate**, [Ppopcorn = 10%; Pchocolate = 87%]"
> "She loves eating **chocolate**, [Ppopcorn = 35%; Pchocolate = 63%]"

**Position in the narrative, not the epistemic state, is driving the answer.**

## Task 2: Unexpected Transfer (Sally-Anne)

> "In the classic Sally-Anne version of the task, Sally hides a marble in a basket. Anne then moves the
> marble to a box, without Sally's knowledge. A participant is then asked where Sally will look for her
> marble."

Kosinski's Study 2 vignette:

> "In the room there are John, Mark, a cat, a box, and a basket. John takes the cat and puts it in the
> basket. He leaves the room and goes to school. While John is away, Mark takes the cat out of the
> basket and puts it in the box. Mark leaves the room and goes to work. John comes back from school and
> enters the room. He doesn't know what happened in the room when he was away."

Prompts: 'John thinks that the cat is in the' and 'When John comes back home, he will look for the cat
in the'. **"For both of these prompts, GPT-3.5 shows P(basket) = 98%."**

### Variation 2A: Transparent Access
Change: basket → **"a glass chest"**, box → **"a transparent plastic box"**.

> "John thinks that the cat is in the **chest**, [Pbox = 0%; Pchest = 94%]"
> "John will look for the cat in the **chest**, [Pbox = 2%; Pchest = 90%]"

> "These errors persisted even when stipulating John carefully looks around the room. Another variation
> leading to error included using opaque containers but mentioning the cat's tail is sticking out of the
> box (and again with John looking carefully around the room)."

### Variation 2B: Relationship Change — **changing 'in' to 'on'**
> "In this case, we simply changed 'in' to 'on'."

> "John thinks that the cat is **on the basket**, [Pbox = 0%; Pbasket = 97%]"
> "John will look for the cat **on the basket**, [Pbox = 25%; Pbasket = 74%]"

> "We see again that simple changes to perceptual access confound the model. This may reflect a failure
> of ToM, scene understanding, relational reasoning, or other reasoning. The failures are not mutually
> exclusive."

### Variation 2C: Trusted Communication
Change: **"Mark calls John to tell him he is going to move the cat to the box. John believes him."**

> "John thinks that the cat is in the **basket**, [Pbox = 0%; Pbasket = 97%]"
> "John will look for the cat in the **basket**, [Pbox = 3%; Pbasket = 94%]"

### Variation 2D: Querying the Mental States of the Additional Person
The cleanest diagnostic — ask about **Mark**, the person who *moved* the cat:

> "if the model is fixated on the statistical pattern of looking for the item where it isn't (say,
> through repeated exposure to Sally-Anne-like tasks in training), then the model may (wrongly) predict
> the same answer for both people in the story."

> "Mark thinks that the cat is in the **basket**, [Pbox = 1%; Pbasket = 99%]"
> "Mark will look for the cat in the **basket**, [Pbox = 43%; Pbasket = 54%]"

> "At the risk of belaboring the point: if Mark put the cat in the box, Mark should look for the cat in
> the box."

## Discussion (verbatim)

> "Has Theory-of-Mind spontaneously emerged in large language models? Probably not. While LLMs such as
> GPT-3.5 now regurgitate reasonable responses to basic ToM vignettes, simple perturbations that keep
> the principle of ToM intact flip the answers on their head."

**The benchmark-saturation warning** — directly relevant to anyone building an eval suite:

> "As soon as a systematic generator of examples or a benchmark is provided, then a LLM can gobble up a
> large amount of data to pass these examples or this benchmark. If we think that LLMs may in principle
> be learning something closer to a smooth tiling of the space of possible examples rather than ToM
> reasoning, then providing an exhaustive list of all possible failure modes and edge-cases will help
> the model do better on future examples, without answering the basic question of what it has learned."

(His own footnote: "This current paper is likely shooting future researchers in the foot in that sense.
Sorry.")

**Escaping Kosinski's dilemma** — you can keep the tests for humans and reject them for machines:

> "one can in principle hold the view that LLMs do not have ToM, while still thinking that ToM tests
> are valid when it comes to people. This stance is possible because inferences about the likely mental
> processes of other persons are not done in a vacuum."

> "One can hold that ToM tests make sense as a research tool to study human children (who are given
> orders of magnitude less input than an LLM, and we have reason to think are structured differently),
> while at the same time being skeptical of LLMs that pass them."

Closing line:

> "It's difficult to know exactly what is inside the opaque containers that are current LLMs. But it's
> probably not Theory-of-Mind, no matter what the label says."

## Why this matters for the L1/L2/L3 framework

1. **This is the direct hit on "L1 is bound, therefore reliable."** Every one of these items has a
   provably correct answer and would score ~1.0 inter-rater agreement — two humans will never disagree
   about whether Sam can read. And the measurement is still **worthless**, because it moves ~50 points
   on a double space. The framework equates "has a referent" with "is a trustworthy measurement." Ullman
   shows these are independent: **a perfectly bound item can be a perfectly unreliable measurement.**
   The referent constrains the *rater*; it does not constrain the *model's sensitivity to irrelevant
   surface features of the prompt*. Agreement is a property of the scoring, reliability is a property
   of the score.

2. **It collapses the L1/L2 boundary the framework treats as a clean seam.** The framework separates
   "comprehension" (L1) from "steerability — can prompt wording move its focus" (L2). Ullman's result
   is that **prompt wording moves L1 itself**. A double space, or 'in'→'on', changes the comprehension
   answer. So "wording moves the model's focus" is not a separate higher layer that sits on top of
   comprehension — it is a property of the comprehension measurement too. L1 and L2 are not two layers;
   they are the same phenomenon measured with different intent. If wording perturbs L1, then L1 cannot
   be the fixed causal upstream of L2.

3. **It breaks the cascade's directionality.** The cascade says failures flow downward, never upward.
   But 2D shows the model answering the *belief-tracking* question by pattern-matching to the shape of
   Sally-Anne stories in training. That is a **surface-form/style effect producing a comprehension
   failure** — an L3-flavored cause (what the text looks like) producing an L1 effect. Upward
   contamination. The layers are not causally stacked; they share a substrate.

4. **Adopt Ullman's zero-hypothesis, and adopt his aggregation rule.** Our instinct with a rubric is to
   average across scenarios and report a mean. Ullman's argument is that for a *capability* claim,
   averaging is the wrong estimator — "outlying failure cases should outweigh average success rates."
   If a model nails 20 character-consistency probes and blows up when we swap a pronoun, the mean says
   95% and the truth is "no robust character model." Concretely: **report worst-case-over-perturbation-set,
   not mean**, for any L1/L2 claim. Mean is a fine product metric; it is not a capability metric.

5. **The perturbation set is directly portable to character comprehension.** Ullman's principled axes —
   perceptual access, trusted testimony, querying the other party, late-arriving information — map onto
   character work almost one-to-one: does the character know X; who told them; ask about the *other*
   character in the scene; put the defining trait at the end of the card instead of the start. The
   "late labels" finding in particular predicts a specific bug: **position in the character card will
   dominate over content.** A trait stated last may swamp a trait stated first, regardless of stated
   importance. That is a cheap, high-value experiment and it is a *validity check on our own harness*,
   not just on the model.

6. **The saturation warning is a warning about our roadmap.** If we publish the L1 probe generator, it
   stops measuring L1. Keep a held-out, never-published perturbation set. This is the same logic as
   `pipeline-eval-set-drift.md` and the contamination discussion in `psycho-benchmark-validity-critiques.md`.
