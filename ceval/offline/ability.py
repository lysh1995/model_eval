"""Model ability portrait: turn judge-free signals into a CHARACTERISATION.

A grade book of defect rates does not answer the question a PM actually asks -- "is this an
intriguing storyteller? a good roleplay partner?" This module composes the judge-free signals
into a per-model portrait, organised by the ability spine (ABILITY-MODEL.md):

  L1 comprehension  -- understand the character.        Mostly NEEDS A JUDGE. Marked honestly.
  L2 application    -- hold and DISTINGUISH characters. Measured (discriminability, collapse).
  L3 craft          -- tell an engaging story.          The CRAFT is measured (scene-driving,
                       looping, richness, hooks); the AESTHETIC verdict ("intriguing") is
                       perspectival and NEEDS a judge + real users. Marked.

The output is not a ranking -- there is no single "best" storyteller, which is the whole
point. It is a portrait: where each model sits on each axis, and a one-line characterisation
derived from its most distinctive traits.

The honest boundary, stated in the data: L1 and the L3 aesthetic verdict are NOT judge-free.
This module measures the observable CORRELATES of storytelling ability, not the ability
itself -- and says so.
"""
from __future__ import annotations
import re, statistics as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional


def measure_field(corpus, language: str, budget: int = 900) -> Dict[str, Dict[str, float]]:
    """Compute the judge-free ability signals for every model in a corpus.

    Modular on purpose: the portrait is derived from these, and both the dashboard and any
    script can call this without duplicating the measurement. All signals are length-aware
    where it matters (lexical diversity and discriminability at a fixed token budget), per
    the length-confound lesson (note 09: the naive versions measured verbosity).
    """
    from ..metrics.builtin import Repetition, Discriminability, Homogenization
    from ..metrics.craft import Initiative

    ACTION = re.compile(r"\*[^*]{3,}\*")
    Q = re.compile(r"\?")

    def distinct2(toks):
        if len(toks) < 2:
            return 0.0
        g = [tuple(toks[i:i+2]) for i in range(len(toks) - 1)]
        return len(set(g)) / len(g)

    rep = Repetition(language)
    ini = Initiative(language)
    out: Dict[str, Dict[str, float]] = {}
    for m in corpus.models():
        dlgs = [d for d in corpus.dialogues if d.model_name == m]
        lens, act, q, lex, reps, tread, drive = [], [], [], [], [], [], []
        for d in dlgs:
            ai = d.ai_texts()
            if not ai:
                continue
            lens.append(st.mean(len(t) for t in ai))
            act.append(sum(1 for t in ai if ACTION.search(t)) / len(ai))
            q.append(sum(1 for t in ai if Q.search(t)) / len(ai))
            toks = " ".join(ai).lower().split()[:budget] if language == "en" \
                else list("".join(ai))[:budget]
            lex.append(distinct2(toks))
            reps.append(rep.compute({d.seed_id: d.turns})[d.seed_id])
            comp = ini.compute({d.seed_id: d.turns})
            tread.append(comp[f"{d.seed_id}::treadmill"])
            drive.append(comp[d.seed_id])
        texts = corpus.character_texts(m)
        out[m] = {
            "length": st.mean(lens) if lens else float("nan"),
            "action": st.mean(act) if act else float("nan"),
            "question": st.mean(q) if q else float("nan"),
            "lexical": st.mean(lex) if lex else float("nan"),
            "repetition": st.mean(reps) if reps else float("nan"),
            "discrim": Discriminability(language, budget).run(texts).values.get("accuracy", float("nan")),
            "homo": Homogenization(language, budget).run(texts).values.get("similarity", float("nan")),
            "treadmill": st.mean(tread) if tread else float("nan"),
            "scene_drive": st.mean(drive) if drive else float("nan"),
        }
    return out


@dataclass
class Axis:
    key: str
    layer: str              # L1 / L2 / L3
    label: str
    pole_low: str
    pole_high: str
    higher_is_richer: bool  # for the bar direction; NOT a value judgement
    measured: bool = True
    unit: str = ""


# The spine. Order = reading order in the portrait.
AXES: List[Axis] = [
    Axis("comprehension", "L1", "Character comprehension",
         "unmeasured", "unmeasured", True, measured=False,
         unit="needs out-of-character probes → judge"),
    Axis("discrim", "L2", "Distinct voices",
         "blurs characters into one voice", "each character a distinct voice", True),
    Axis("homo", "L2", "Voice separation",
         "voices collapse together", "voices stay separate", False),
    Axis("scene_drive", "L3", "Scene-driving",
         "reactive — waits to be led", "propulsive — moves the story", True),
    Axis("repetition", "L3", "Freshness",
         "loops and repeats", "stays fresh", False),
    Axis("lexical", "L3", "Vocabulary",
         "plain, repetitive words", "rich, varied words", True),
    Axis("question", "L3", "Draws the user in",
         "declarative — talks at you", "inquisitive — draws you out", True),
    Axis("length", "L3", "Pacing",
         "terse", "essayistic, writes at length", True),
]

AESTHETIC_VERDICT_NOTE = (
    "Whether the writing is actually INTRIGUING is perspectival (human agreement α=0.25–0.34) "
    "and cannot be settled judge-free. These are the observable CORRELATES of craft, not the "
    "aesthetic verdict. That needs a pairwise judge and, ultimately, real users.")


@dataclass
class AbilitySignal:
    axis: Axis
    value: float
    position: float          # 0..1 across the field; NaN if unmeasured
    measured: bool


@dataclass
class AbilityProfile:
    model: str
    language: str
    signals: List[AbilitySignal]
    characterization: str
    traits: List[str]

    def to_row(self) -> dict:
        return {
            "model": self.model, "language": self.language,
            "characterization": self.characterization, "traits": self.traits,
            "signals": [{
                "key": s.axis.key, "layer": s.axis.layer, "label": s.axis.label,
                "value": s.value, "position": s.position, "measured": s.measured,
                "pole_low": s.axis.pole_low, "pole_high": s.axis.pole_high,
                "higher_is_richer": s.axis.higher_is_richer, "unit": s.axis.unit,
            } for s in self.signals],
        }


def _positions(field: Dict[str, Dict[str, float]], key: str) -> Dict[str, float]:
    """PERCENTILE-RANK position of each model on one axis, across the field. NaN-safe.

    NOT min-max: min-max lets one outlier (deepseek-v3.2 writes 3,229 chars/turn vs a field
    median of ~460) compress every other model to the bottom, so 8 of 11 falsely read
    'terse' and a mid-field model reads 'extreme'. That is the relative-position-as-absolute-
    trait trap this project has hit repeatedly. Rank is robust to skew: it answers 'where in
    the field does this model sit', which is exactly what a portrait claims.
    """
    ok = {m: r.get(key) for m, r in field.items() if r.get(key) is not None and r.get(key) == r.get(key)}
    if len(ok) < 3:
        return {m: float("nan") for m in field}
    order = sorted(ok, key=lambda m: ok[m])
    n = len(order)
    rank = {m: i / (n - 1) for i, m in enumerate(order)}   # 0..1 ordinal
    return {m: rank.get(m, float("nan")) for m in field}


def _characterise(model: str, pos: Dict[str, float]) -> tuple:
    """Derive a one-line portrait from the model's most distinctive positions.

    Picks standout traits (top/bottom third of the field) and composes them. This is a
    description of WHERE the model sits, not a verdict on whether that is good -- a terse
    reactive model is right for some products and wrong for others.
    """
    def p(k):
        return pos.get(k, float("nan"))

    # Only genuine tails (top/bottom ~quintile by RANK) count as distinctive. With 11 models
    # that flags roughly the 2 highest and 2 lowest per axis -- so each model earns 0-3
    # traits and mid-field models stay quiet, which is what makes it read as a portrait.
    HI, LO = .80, .20
    traits = []
    # pacing
    if p("length") >= HI: traits.append(("pacing", "an essayist — writes at length"))
    elif p("length") <= LO: traits.append(("pacing", "terse"))
    # scene-driving (L3 core)
    if p("scene_drive") >= HI: traits.append(("drive", "propulsive — drives the scene"))
    elif p("scene_drive") <= LO: traits.append(("drive", "reactive — waits to be led"))
    # distinctiveness (L2 core)
    if p("discrim") == p("discrim"):
        if p("discrim") >= HI: traits.append(("voice", "gives each character a distinct voice"))
        elif p("discrim") <= LO: traits.append(("voice", "blurs characters toward one voice"))
    # freshness
    if p("repetition") >= HI: traits.append(("loop", "but loops and repeats itself"))
    # hooks
    if p("question") >= HI: traits.append(("hook", "inquisitive — draws the user out"))
    # richness
    if p("lexical") <= LO: traits.append(("lex", "plain vocabulary"))
    elif p("lexical") >= HI: traits.append(("lex", "rich, varied vocabulary"))

    # compose: lead with pacing+drive, then voice, then the caveats
    order = ["pacing", "drive", "voice", "hook", "lex", "loop"]
    picked = sorted(traits, key=lambda t: order.index(t[0]) if t[0] in order else 99)[:4]
    phrases = [t[1] for t in picked]
    if not phrases:
        sentence = "a middle-of-the-field profile — no strongly distinctive trait judge-free."
    else:
        sentence = phrases[0][0].upper() + phrases[0][1:]
        if len(phrases) > 1:
            sentence += ", " + ", ".join(phrases[1:-1] + [phrases[-1]]) if len(phrases) > 2 \
                else ", " + phrases[1]
        sentence += "."
    return sentence, [t[1] for t in picked]


def build_profiles(field: Dict[str, Dict[str, float]], language: str) -> List[AbilityProfile]:
    """field: model -> {axis_key: value}. Returns one portrait per model."""
    pos_by_axis = {ax.key: _positions(field, ax.key) for ax in AXES if ax.measured}
    profiles = []
    for model, row in field.items():
        pos = {k: pos_by_axis[k].get(model, float("nan")) for k in pos_by_axis}
        signals = []
        for ax in AXES:
            if not ax.measured:
                signals.append(AbilitySignal(ax, float("nan"), float("nan"), False))
                continue
            v = row.get(ax.key, float("nan"))
            p = pos_by_axis[ax.key].get(model, float("nan"))
            # bars read as "richer/more" -> flip position for axes where low is richer
            display_p = p if ax.higher_is_richer else (1 - p if p == p else p)
            signals.append(AbilitySignal(ax, v, display_p, v == v))
        sentence, traits = _characterise(model, pos)
        profiles.append(AbilityProfile(model, language, signals, sentence, traits))
    # portrait order: by scene-driving (the L3 core), but this is NOT a ranking
    profiles.sort(key=lambda pr: -(field[pr.model].get("scene_drive") or 0))
    return profiles
