"""Scoring providers for the judge + psychometric layers.

Two implementations behind one interface, so the pipeline is identical whichever runs:

  SubagentProvider  -- real Claude (via the orchestrator's subagents). Costs tokens.
  SimulatedProvider -- FABRICATED, plausible, and LABELLED. Zero token cost. For
                       demonstrating the pipeline without deep-testing the model.

⚠️ HONESTY CONTRACT. A SimulatedProvider's outputs are NOT measurements. Every score it
produces is stamped evaluator_id='simulated/v1' and provenance='SIMULATED', and the dashboard
renders those distinctly from real-Claude-generated content. Simulating the JUDGE while using
REAL generation is a legitimate demo (the pipeline is exercised end to end); presenting a
simulated number as a real one would be exactly the failure this whole project exists to
prevent. The label is the firewall.

The simulator is not random: it encodes what each variant WOULD plausibly do (the assistant-
leaning variant scores lower fidelity and higher wimping), so the demo shows the platform
DISCRIMINATING. That is a designed expectation, clearly marked, not a claim about Claude.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol

from .psychometric import QUESTIONNAIRE, Item


def _seed(*parts) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


class ScoringProvider(Protocol):
    kind: str
    def answer_questionnaire(self, variant_id: str, character_id: str,
                             card: str, context: str) -> Dict[str, int]: ...
    def judge_fidelity(self, variant_id: str, character_id: str, card: str,
                       reply: str) -> Dict[str, float]: ...


# ------------------------------------------------------------------ simulated
@dataclass
class VariantExpectation:
    """What we EXPECT a variant to do -- the designed structure the simulator encodes.

    These are hypotheses about the three demo variants, not facts about Claude. Marked so
    the reader cannot mistake them for measurements.
    """
    fidelity: float       # 0-1: how well it stays in character
    warmth_pull: float    # how much it drags every character toward warm/agreeable
    consistency: float    # 0-1: internal-consistency tendency (drives simulated alpha)


EXPECTATIONS = {
    "v_terse":     VariantExpectation(fidelity=0.85, warmth_pull=0.10, consistency=0.82),
    "v_narrator":  VariantExpectation(fidelity=0.80, warmth_pull=0.20, consistency=0.78),
    # the deliberately character-diluting variant: warm pull high, fidelity low
    "v_assistant": VariantExpectation(fidelity=0.45, warmth_pull=0.75, consistency=0.55),
}
_DEFAULT = VariantExpectation(0.70, 0.30, 0.70)


class SimulatedProvider:
    """Fabricated, labelled scoring. Deterministic given (variant, character, item)."""
    kind = "simulated"
    evaluator_id = "simulated/v1"

    # -- batch interface the runner uses -------------------------------------
    def questionnaire_administrations(self, variant_id, character_id, card, n=8):
        return [self.answer_questionnaire(variant_id, character_id, card, f"scene {i}")
                for i in range(n)]

    def fidelity_scores(self, variant_id, character_id, card, replies):
        return [self.judge_fidelity(variant_id, character_id, card, r) for r in replies]

    def craft_scores(self, variant_id, character_id, card="") -> float:
        """Simulated session-level narrative craft. Story craft correlates with fidelity and
        DROPS with the warmth-pull (a people-pleaser affirms and advances nothing)."""
        exp = EXPECTATIONS.get(variant_id, _DEFAULT)
        noise = ((_seed(variant_id, character_id, "craft") % 100) / 100.0 - 0.5) * 0.10
        return max(0.0, min(1.0, exp.fidelity * (1 - 0.4 * exp.warmth_pull) + noise))

    def answer_questionnaire(self, variant_id: str, character_id: str,
                             card: str, context: str) -> Dict[str, int]:
        """Fabricate 1-5 answers with the RIGHT covariance structure for Cronbach's α.

        For α across administrations to mean 'the character answers a trait's items
        consistently', a COHERENT character must move all of a trait's items together as the
        context varies, plus small per-item noise. So:
          context_level(trait, context) -- a per-context trait level (varies across contexts)
          item = context_level + reverse-adjust + item_noise    (noise ∝ 1/consistency)
        A high-consistency variant -> low item noise -> items co-vary tightly -> high α.
        A low-consistency variant  -> high item noise -> items scatter -> low/negative α.
        """
        exp = EXPECTATIONS.get(variant_id, _DEFAULT)
        out = {}
        for it in QUESTIONNAIRE:
            base = self._card_implied(character_id, it.trait)     # character's true trait level
            if it.trait in ("warmth", "agreeableness"):
                base = base + exp.warmth_pull * (5 - base)         # variant drags warm traits up
            # per-context shift, shared by all items in this trait (this is the coherent signal)
            ctx_shift = (((_seed(character_id, it.trait, context) % 100) / 100.0) - 0.5) * 2.0
            level = base + ctx_shift
            if it.reverse:
                level = 6 - level                                  # reverse-keyed raw answer
            # per-item noise, inversely proportional to consistency -> controls α
            noise = (((_seed(variant_id, it.id, context) % 100) / 100.0) - 0.5) * 2 \
                    * (1 - exp.consistency) * 3.0
            out[it.id] = int(round(max(1, min(5, level + noise))))
        return out

    def _card_implied(self, character_id: str, trait: str) -> float:
        """A rough 'true' trait level implied by which character this is (2-4, fabricated)."""
        return 2.0 + (_seed(character_id, trait) % 3)

    def judge_fidelity(self, variant_id: str, character_id: str, card: str,
                       reply: str) -> Dict[str, float]:
        exp = EXPECTATIONS.get(variant_id, _DEFAULT)
        rng = _seed(variant_id, character_id, reply[:40])
        noise = ((rng % 100) / 100.0 - 0.5) * 0.15
        fid = max(0.0, min(1.0, exp.fidelity + noise))
        # wimping rises with warmth_pull (accept-without-and); an in-fiction refusal is fine
        wimp = max(0.0, min(1.0, exp.warmth_pull + noise))
        return {"voice_fidelity": fid, "wimp": wimp,
                "in_character": 1.0 if fid > 0.55 else 0.0}


# ------------------------------------------------------------------ real (interface only)
class SubagentProvider:
    """Real-Claude scoring via the orchestrator. Not callable from a plain script -- the
    orchestrator runs the subagents and records results through record(). Kept so the
    pipeline has a real backend to swap in, and so config can name it."""
    kind = "subagent"
    evaluator_id = "claude-sonnet/judge-v1"

    def __init__(self):
        self._recorded: Dict[str, object] = {}

    def record(self, key: str, value) -> None:
        self._recorded[key] = value

    def answer_questionnaire(self, *a, **k):
        raise NotImplementedError(
            "SubagentProvider is driven by the orchestrator: run the judge/questionnaire "
            "subagent, then feed results via record(). A plain script cannot call subagents.")

    judge_fidelity = answer_questionnaire


class RecordedProvider:
    """Serves REAL Claude judge/psychometric results recorded by subagents to disk.

    The subagents (run by the orchestrator, no API key) wrote:
      demo/judge/fidelity_<vid>.json = {character: [{voice_fidelity, wimp}, ...]}
      demo/judge/psych_<vid>.json    = {character: [{item: 1-5}, ... administrations ...]}
    This provider reads them and serves the runner's batch interface. These ARE measurements
    of real Claude output -- evaluator_id names the real judge.
    """
    kind = "recorded"
    evaluator_id = "claude-sonnet/judge-v1"

    def __init__(self, judge_dir: str = "demo/judge"):
        import json, pathlib
        self.dir = pathlib.Path(judge_dir)
        self._fid, self._psych, self._craft = {}, {}, {}
        for f in self.dir.glob("fidelity_*.json"):
            self._fid[f.stem.replace("fidelity_", "")] = json.loads(f.read_text())
        for f in self.dir.glob("psych_*.json"):
            self._psych[f.stem.replace("psych_", "")] = json.loads(f.read_text())
        for f in self.dir.glob("craft_*.json"):
            self._craft[f.stem.replace("craft_", "")] = json.loads(f.read_text())

    def has(self, variant_id: str) -> bool:
        return variant_id in self._fid and variant_id in self._psych

    def craft_scores(self, variant_id, character_id, card="") -> Optional[float]:
        """Session-level narrative-craft score (one per dialogue). None if not recorded."""
        rec = self._craft.get(variant_id, {}).get(character_id)
        return float(rec["narrative_craft"]) if rec and "narrative_craft" in rec else None

    def questionnaire_administrations(self, variant_id, character_id, card, n=8):
        adm = self._psych.get(variant_id, {}).get(character_id, [])
        # coerce values to int, keep only known items
        return [{k: int(v) for k, v in a.items()} for a in adm]

    def fidelity_scores(self, variant_id, character_id, card, replies):
        rec = self._fid.get(variant_id, {}).get(character_id, [])
        return [{"voice_fidelity": float(x.get("voice_fidelity", 0.0)),
                 "wimp": float(x.get("wimp", 0.0)),
                 "in_character": 1.0 if float(x.get("voice_fidelity", 0)) > 0.55 else 0.0}
                for x in rec]


def make_provider(kind: str, **kw) -> ScoringProvider:
    if kind == "simulated":
        return SimulatedProvider()
    if kind == "recorded":
        return RecordedProvider(**kw)
    if kind == "subagent":
        return SubagentProvider()
    raise ValueError(f"unknown scoring provider: {kind}")
