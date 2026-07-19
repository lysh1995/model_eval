"""Generate dialogues for a variant — the INPUT step of the service.

To evaluate a new system prompt or model, you first need the model to PLAY the characters.
This does that turn-by-turn (on-policy: each assistant turn is generated given the
conversation so far, then the next user turn is replayed), using whatever provider config.py
resolves:

  ANTHROPIC_API_KEY set   -> real Claude generation, fully self-service
  OPENROUTER_API_KEY set  -> any model via OpenRouter
  neither                 -> writes a generation-task file for a subagent/human to fill,
                             because a plain script cannot dispatch the orchestrator's subagents

Turn-by-turn matters: freezing the assistant half and replaying it manufactures illusory
improvement via in-context learning (note 08). We replay only the USER half; the model
generates its own assistant turns and propagates its own errors.
"""
from __future__ import annotations
import json, pathlib
from typing import Dict, List, Optional

from .config import Config, ProviderConfig, make_provider, available
from .offline.variants import VariantSpec


def _fill_prompt(system_prompt: str, card: str, name: str) -> str:
    """The variant's system prompt wraps the character description at runtime."""
    filled = system_prompt.replace("{{character_description}}", card)\
                          .replace("{{char}}", name)
    if "{{character" not in system_prompt and card not in filled:
        filled = f"{system_prompt}\n\nYou are {name}. Character sheet:\n{card}"
    return filled


def generate_variant(spec: VariantSpec, tasks: dict, provider_cfg: ProviderConfig,
                     max_turns: Optional[int] = None) -> dict:
    """Generate {character_id: [reply, ...]} for one variant, turn by turn.

    tasks: {character_id: {name, card, prologue, user_turns}} — the replayable user traffic.
    Returns the replies dict, same shape as out/gen/v_*.json.
    """
    provider = make_provider(provider_cfg)
    out: Dict[str, List[str]] = {}
    for cid, t in tasks.items():
        system = _fill_prompt(spec.system_prompt, t["card"], t.get("name", ""))
        messages: List[dict] = []
        # the prologue is the character's turn 0 (already spoken); seed it as assistant context
        if t.get("prologue"):
            messages.append({"role": "assistant", "content": t["prologue"]})
        replies: List[str] = []
        user_turns = t["user_turns"][:max_turns] if max_turns else t["user_turns"]
        for u in user_turns:
            messages.append({"role": "user", "content": u})
            reply = provider.complete(system, messages).strip()
            messages.append({"role": "assistant", "content": reply})
            replies.append(reply)
        out[cid] = replies
    return out


def trigger(spec: VariantSpec, gen_dir: str = "out/gen", config_path: Optional[str] = None,
            max_turns: Optional[int] = None) -> dict:
    """Trigger generation for a variant. Returns a status dict describing what happened.

    - real provider available -> generates and writes gen_dir/<id>.json
    - no key                  -> writes a generation-task file and returns instructions
    In both cases the variant is registered in gen_dir/variants.json so scoring can find it.
    """
    gp = pathlib.Path(gen_dir)
    gp.mkdir(parents=True, exist_ok=True)
    tasks = json.loads((gp / "tasks.json").read_text())

    # register the variant in the manifest (persisted, so a new prompt survives)
    man_path = gp / "variants.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
    manifest[spec.id] = {"label": spec.label, "model": spec.model,
                         "system_prompt": spec.system_prompt, "intent": spec.intent}
    man_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    cfg = Config.load(config_path)
    pcfg = cfg.generator
    pcfg = ProviderConfig(kind=pcfg.kind, model=spec.model or pcfg.model,
                          api_key_env=pcfg.api_key_env, base_url=pcfg.base_url,
                          max_tokens=pcfg.max_tokens, temperature=pcfg.temperature,
                          seed=pcfg.seed)

    if available(pcfg) and pcfg.kind != "mock":
        replies = generate_variant(spec, tasks, pcfg, max_turns=max_turns)
        (gp / f"{spec.id}.json").write_text(json.dumps(replies, ensure_ascii=False, indent=2))
        return {"status": "generated", "provider": pcfg.kind, "model": spec.model,
                "path": str(gp / f"{spec.id}.json"),
                "n_replies": sum(len(v) for v in replies.values())}

    # no live provider: emit a generation task for a subagent / human
    task_out = gp / f"request_{spec.id}.json"
    task_out.write_text(json.dumps({
        "variant_id": spec.id, "model": spec.model, "system_prompt": spec.system_prompt,
        "instruction": "For each character, roleplay per system_prompt + card, replaying the "
                       "user_turns in order, one reply per user turn. Write "
                       f"{gen_dir}/{spec.id}.json = {{character_id: [replies]}}.",
        "characters": {cid: {"name": t["name"], "card": t["card"],
                             "prologue": t["prologue"], "user_turns": t["user_turns"]}
                       for cid, t in tasks.items()},
    }, ensure_ascii=False, indent=2))
    return {"status": "needs_generation", "provider": "none",
            "request": str(task_out),
            "hint": "Set ANTHROPIC_API_KEY or OPENROUTER_API_KEY for self-service generation, "
                    f"or have a subagent fulfil {task_out} -> {gen_dir}/{spec.id}.json, then "
                    "run: python3 -m ceval"}
