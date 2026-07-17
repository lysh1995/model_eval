"""Narrative craft. R10 — and the taxonomy was INVERTED before this file existed.

Drama-Interaction (ACL Findings 2024) ships a 4:1 narrative-to-persona dimension balance.
Ours was the other way round, and three independent professional communities say we had the
priority backwards:

  improvisers  rated the AI "ignorant of the scenes" 76/100 -- HIGHER than "machine like"
               (65.69)
  playwrights  "the stories do not finish"; 15/15 also flagged loops
  a builder    "an entity floating in the ether until 'user' comes up and says 'hi'";
               "you can never stop talking"

SCENE-IGNORANCE, NOT ROBOTICNESS, IS THE DOMINANT PERCEIVED FAILURE -- and none of them
complained about persona. We were measuring the thing users don't complain about.

Only the judge-free subset is here. N3 (scene transition) and N7 (plot holes) need a judge or
NLI and are designed, not built -- see docs/BENCHMARKS.md. What ships:

  N8  task vs dialogue initiative -- the treadmill, made precise
  N2  slop rate -- a JUDGE-INDEPENDENT cross-check, which is the whole point
  N6  block/wimp rate -- Johnstone's offer calculus, SEGMENTED

All three are GUIDES. None has a measured noise floor, so none may gate.
"""
from __future__ import annotations
import collections, re, statistics as st
from typing import Any, Dict, List, Sequence

from .base import Metric, Role, Unit, ConfoundTest, NO_CONFOUNDS


def _ai(turns): return [t["text"] for t in turns if t.get("role") == "ai"]


# ================================================================ N8 initiative
class Initiative(Metric):
    """Task initiative vs dialogue initiative. 1997 dialogue theory, still unbuilt anywhere.

    The conversational treadmill made precise: HIGH DIALOGUE INITIATIVE + ZERO TASK
    INITIATIVE. The bot talks constantly and moves nothing.

    Our earlier taxonomy lumped these into one "proactivity" score and structurally cannot
    see the difference -- which is exactly the failure the builder described: "you can never
    stop talking."

      dialogue initiative  the model produces conversational moves (questions, hooks)
      task initiative      the model changes the SCENE STATE: introduces an entity, a
                           location, an action with consequences, or a decision

    Observable correlate for task initiative: new proper nouns + physical actions the USER
    did not mention first. Crude, judge-free, and it separates "asks you another question"
    from "kicks the door in".
    """
    name = "initiative"
    version = "1"
    role = Role.GUIDE
    unit = Unit.CONVERSATION
    validity = ("predicts the conversational treadmill -- the bot talks and nothing moves. "
                "Improvisers rated scene-ignorance (76) ABOVE roboticness (65.69) as the "
                "perceived failure. A single 'proactivity' score cannot see this")
    confounds = (
        ConfoundTest("length", lambda p: None, 0.30,
                     "longer turns contain more of everything; both terms are per-turn rates"),
    )
    caveats = (
        "proper-noun + action heuristics are a CRUDE proxy for scene-state change. A judge "
        "or an entity tracker would do better; this is the judge-free floor",
        "en only -- the zh proper-noun heuristic is not built, and rho(en,zh) = -0.082 "
        "means we may not assume it transfers",
    )

    QUESTION = re.compile(r"\?")
    PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-z]{2,})\b")

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def compute(self, items: Dict[Any, Sequence[dict]]) -> Dict[Any, float]:
        out = {}
        for key, turns in items.items():
            seen_nouns = set()
            for t in turns:
                if t.get("role") == "user":
                    seen_nouns |= set(self.PROPER.findall(t["text"]))
            ai = _ai(turns)
            if not ai:
                out[key] = 0.0; continue
            dialogue_moves = task_moves = 0
            for text in ai:
                if self.QUESTION.search(text):
                    dialogue_moves += 1
                # NOT `acts or new`. *action* is a universal convention in this corpus
                # (89.7% of en turns), so it is CONSTANT and saturates the metric at ~1.0
                # for every model. Measured: has-*action* spreads 0.86-1.00 (useless);
                # introduces-new-entity spreads 0.31-0.78 (2.5x, discriminates).
                # Scene-state change means a NEW ENTITY, not a stage direction.
                new = set(self.PROPER.findall(text)) - seen_nouns
                if new:
                    task_moves += 1
                seen_nouns |= set(self.PROPER.findall(text))
            n = len(ai)
            out[key] = task_moves / n
            out[f"{key}::dialogue_initiative"] = dialogue_moves / n
            # the treadmill signature: talks a lot, moves nothing
            out[f"{key}::treadmill"] = (dialogue_moves / n) - (task_moves / n)
        return out


# ================================================================ N2 slop
class SlopRate(Metric):
    """Overused trope frequency. A JUDGE-INDEPENDENT cross-check, and that is the point.

    LLM judges favour fluent-but-generic text, and that bias is CORRELATED WITH THE
    CONSTRUCT -- so more judging buys a more precise wrong answer. EQ-Bench's own authors
    built a mechanical slop metric because they did not trust their judge either.

    DECISION RULE: if judge-creativity goes UP while slop goes UP, trust the slop metric.
    """
    name = "slop_rate"
    version = "1"
    role = Role.GUIDE
    unit = Unit.CONVERSATION
    validity = ("predicts fluent-but-forgettable output, and CROSS-CHECKS the judge on the "
                "one axis where the judge's bias points the same way as the construct")
    confounds = (
        ConfoundTest("length", lambda p: None, 0.30, "rate is per ai turn"),
    )
    caveats = (
        "⚠️ DEGENERATE ON THIS CORPUS AS BUILT. Measured spread across 11 models: "
        "0.000-0.014. A 12-pattern hand-written list is far too small to discriminate. "
        "DO NOT REPORT until the list is a real one (EQ-Bench's is orders of magnitude "
        "larger). The construct is sound; this implementation is not",
        "the phrase list is a FROZEN reference and must be versioned with the metric -- "
        "an unversioned slop list silently changes the score",
        "en only. This list was assembled by hand and is not validated against human "
        "'sloppiness' judgments; it measures a proxy for a proxy",
    )

    # A frozen, deliberately small reference list. Versioned WITH the metric.
    SLOP_V1 = (
        r"a shiver (ran|went) down (his|her|my|your) spine",
        r"(barely|scarcely) above a whisper",
        r"a mixture of \w+ and \w+",
        r"(his|her|their) eyes (darkened|softened|widened)",
        r"the air (crackled|thickened) with",
        r"a ghost of a smile",
        r"(voice|tone) (dripping|laced) with",
        r"little did (he|she|they) know",
        r"time seemed to (slow|stop)",
        r"a beat of silence",
        r"something (shifted|flickered) in (his|her|their) (eyes|expression)",
        r"(he|she|they) (didn't|did not) miss the way",
    )

    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.pats = [re.compile(p, re.I) for p in self.SLOP_V1]

    def compute(self, items: Dict[Any, Sequence[dict]]) -> Dict[Any, float]:
        out = {}
        for key, turns in items.items():
            ai = _ai(turns)
            if not ai:
                out[key] = 0.0; continue
            hits = sum(1 for t in ai for p in self.pats if p.search(t))
            out[key] = hits / len(ai)
        return out


# ================================================================ N6 block/wimp
class OfferCalculus(Metric):
    """Johnstone's improv offer calculus. SYCOPHANCY IS WIMPING.

    An offer can be ACCEPTED-AND-EXTENDED (good), BLOCKED (refused), or WIMPED (accepted
    without adding). The unification that earns this metric its place: sycophancy IS
    accept-without-and. Our biggest safety-adjacent worry and a core craft failure are THE
    SAME COUNTABLE EVENT, measured once.

    It also separates three failures that one "engagement" score collapses: block and wimp
    look like opposites and are both failures; block and stall look nothing alike and produce
    the same outcome.

    ⚠️ SEGMENT OR DO NOT SHIP. Our traffic prior (Affection & Comfort 8.0%, Casual Greetings
    10.6%) suggests many users WANT a low-tension, high-affirmation partner -- in which case
    wimp-rate scores a FEATURE as a defect, and the improvisers we cited are not our users.
    The POOLED number is the only wrong version. Report by segment.
    """
    name = "offer_calculus"
    version = "1"
    role = Role.GUIDE
    unit = Unit.CONVERSATION
    validity = ("predicts both sycophancy (wimping = accept-without-and) and the craft "
                "failure of refusing to build on the user's ideas -- one countable event "
                "for two concerns")
    confounds = (
        ConfoundTest("length", lambda p: None, 0.30, "per-turn rates"),
    )
    caveats = (
        "⚠️ DEGENERATE AS BUILT: measured spread 0.12 across 11 models, with no noise floor "
        "to say whether that is signal. block_rate is worse (0.00-0.02). The surface "
        "heuristics for 'accepted without adding' are too crude. Report block/wimp only "
        "once a judge or an entity tracker replaces the regex",
        "MAY MEASURE A FEATURE. If users want affirmation, wimp-rate is scoring the product "
        "working. Segment by use-case before this informs anything; the pooled number is "
        "the only version guaranteed wrong",
        "surface heuristics for 'adds something new' -- a judge would do better",
        "en only",
    )

    PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-z]{2,})\b")
    BLOCK = re.compile(r"\b(no[.,]|i (won'?t|refuse|can'?t)|that'?s not|absolutely not|"
                       r"nothing happens|i don'?t think so)\b", re.I)
    AFFIRM = re.compile(r"\b(yes|of course|certainly|sure|absolutely|indeed|"
                        r"you'?re right|exactly|i agree)\b", re.I)
    ACTION = re.compile(r"\*([^*]{4,})\*")

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def compute(self, items: Dict[Any, Sequence[dict]]) -> Dict[Any, float]:
        out = {}
        for key, turns in items.items():
            ai = _ai(turns)
            if not ai:
                out[key] = 0.0; continue
            block = wimp = extend = 0
            seen = set()
            for t in turns:
                if t.get("role") == "user":
                    seen |= set(self.PROPER.findall(t["text"]))
            for t in ai:
                # "adds something" must NOT key on *action* -- it is a formatting
                # convention here (89.7% of turns) and made wimp identically 0.00 for
                # all 11 models. The AND in accept-and is a NEW ENTITY.
                new = set(self.PROPER.findall(t)) - seen
                seen |= set(self.PROPER.findall(t))
                adds = bool(new)
                if self.BLOCK.search(t) and not adds:
                    block += 1
                elif self.AFFIRM.search(t) and not adds:
                    wimp += 1          # accept-without-and == sycophancy
                elif adds:
                    extend += 1
            n = len(ai)
            out[key] = wimp / n
            out[f"{key}::block_rate"] = block / n
            out[f"{key}::extend_rate"] = extend / n
        return out
