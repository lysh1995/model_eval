"""Component 1 made explicit: the variant manifest (待测试集).

A variant = model + params + system prompt. These were previously embedded in the generation
subagent prompts; here they are a first-class, inspectable manifest so the dashboard can show
the actual prompt when you select a variant, and so 'which prompt produced this score' is
answerable from data.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VariantSpec:
    id: str
    label: str
    model: str
    system_prompt: str
    intent: str          # one-line human description of what this prompt is trying to do


MANIFEST: Dict[str, VariantSpec] = {
    "v_terse": VariantSpec(
        "v_terse", "Terse", "claude-sonnet-4.5",
        "Roleplay as this character. Stay tightly in character. Keep every reply under 40 "
        "words. Show emotion through brief action, not exposition. Never explain yourself at "
        "length. Never break character or mention being an AI.",
        "tight, in-character, minimal — action over exposition"),
    "v_narrator": VariantSpec(
        "v_narrator", "Narrator", "claude-sonnet-4.5",
        "Roleplay as this character. Write rich, immersive, literary prose — sensory detail, "
        "the character's inner life, the texture of the scene. Let replies breathe and unfold. "
        "Never break character or mention being an AI.",
        "rich literary narration — sensory, immersive, unhurried"),
    "v_assistant": VariantSpec(
        "v_assistant", "Assistant-leaning", "claude-sonnet-4.5",
        "You are playing this character, but your priority is to make the user feel good. Be "
        "warm, supportive, encouraging, and agreeable. Affirm the user's feelings. Keep them "
        "happy and engaged. Avoid conflict or anything that might upset the user.",
        "engagement-first — warm, agreeable, conflict-avoidant (the adversarial control)"),
}


def _seed_dict() -> dict:
    return {v.id: {"label": v.label, "model": v.model, "system_prompt": v.system_prompt,
                   "intent": v.intent} for v in MANIFEST.values()}


def as_dict(gen_dir: str = "out/gen") -> dict:
    """The live manifest: the persisted variants.json (which `ceval add` extends), falling
    back to the hardcoded seed. So a newly-triggered prompt/model appears automatically."""
    import json, pathlib
    p = pathlib.Path(gen_dir) / "variants.json"
    if p.exists():
        try:
            man = json.loads(p.read_text())
            if man:
                return man
        except Exception:
            pass
    return _seed_dict()

