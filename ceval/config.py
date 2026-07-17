"""Config + providers. Drop a key in config.json and Lane 3 wakes up.

Everything judge-free (Lanes 0-2) runs today with no key and no dependencies. The judge
lane is wired as an interface with three backends:

  anthropic   -- ANTHROPIC_API_KEY   (Claude)
  openrouter  -- OPENROUTER_API_KEY  (anything)
  mock        -- deterministic fake; lets the whole pipeline run and be tested end-to-end

Resolution order: explicit config value -> environment variable -> mock.
Keys are NEVER written to config.json -- put them in the environment. The config names the
env var to read; it does not hold the secret.

stdlib only (urllib). No `requests`, no SDK.
"""
from __future__ import annotations
import json, os, pathlib, time, urllib.request, urllib.error
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config.json"
EXAMPLE_CONFIG = ROOT / "config.example.json"


@dataclass
class ProviderConfig:
    kind: str = "mock"                    # anthropic | openrouter | mock
    model: str = "claude-sonnet-5"
    api_key_env: str = "ANTHROPIC_API_KEY"
    base_url: str = ""
    max_tokens: int = 1024
    temperature: float = 0.0              # judges are pinned; decoding is part of evaluator_id
    seed: Optional[int] = 0
    timeout_s: int = 60
    max_retries: int = 3


@dataclass
class Config:
    generator: ProviderConfig = field(default_factory=ProviderConfig)
    judges: List[ProviderConfig] = field(default_factory=list)   # family-DISJOINT panel of 3
    data_dir: str = "data"
    out_dir: str = "out"

    @staticmethod
    def load(path: Optional[str] = None) -> "Config":
        p = pathlib.Path(path) if path else DEFAULT_CONFIG
        if not p.exists():
            if EXAMPLE_CONFIG.exists():
                raw = json.loads(EXAMPLE_CONFIG.read_text())
            else:
                raw = {}
        else:
            raw = json.loads(p.read_text())
        def clean(d):    # underscore keys are documentation (_readme, _family, _notes)
            return {k: v for k, v in d.items() if not k.startswith("_")}
        gen = ProviderConfig(**clean(raw.get("generator", {})))
        judges = [ProviderConfig(**clean(j)) for j in raw.get("judges", [])]
        return Config(generator=gen, judges=judges,
                      data_dir=raw.get("data_dir", "data"), out_dir=raw.get("out_dir", "out"))

    def status(self) -> str:
        lines = []
        for label, pc in [("generator", self.generator)] + [(f"judge[{i}]", j) for i, j in enumerate(self.judges)]:
            key = os.environ.get(pc.api_key_env, "")
            state = "LIVE" if (key and pc.kind != "mock") else ("mock" if pc.kind == "mock" else f"NO KEY (${pc.api_key_env})")
            lines.append(f"  {label:11s} {pc.kind:11s} {pc.model:28s} {state}")
        fams = [j.kind + ":" + j.model.split("-")[0] for j in self.judges]
        if len(self.judges) >= 2 and len(set(fams)) < len(fams):
            lines.append("  ⚠️  judge panel is NOT family-disjoint: self-preference is causal "
                         "and does NOT cancel by averaging")
        return "\n".join(lines)


# ------------------------------------------------------------------ providers
class Provider:
    def complete(self, system: str, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError
    @property
    def snapshot(self) -> str:
        raise NotImplementedError


class MockProvider(Provider):
    """Deterministic fake. Lets the whole pipeline run, be tested, and be demoed with no key.

    It is NOT a simulation of a model and must never produce a reported score. It exists so
    that the plumbing is proven before a key exists, and so the judge lane has a testable
    contract.
    """
    def __init__(self, cfg: ProviderConfig): self.cfg = cfg
    @property
    def snapshot(self) -> str: return f"mock:{self.cfg.model}"
    def complete(self, system: str, messages: List[Dict[str, str]]) -> str:
        import hashlib
        h = hashlib.sha256((system + json.dumps(messages)).encode()).hexdigest()
        return "A" if int(h[:2], 16) % 2 == 0 else "B"     # deterministic pseudo-verdict


class _HTTPProvider(Provider):
    def __init__(self, cfg: ProviderConfig):
        self.cfg = cfg
        self.key = os.environ.get(cfg.api_key_env, "")
        if not self.key:
            raise RuntimeError(
                f"{cfg.kind}: no key in ${cfg.api_key_env}. Export it, or set "
                f'"kind": "mock" in config.json to run the pipeline without live calls.'
            )
    def _post(self, url: str, payload: dict, headers: dict) -> dict:
        body = json.dumps(payload).encode()
        last = None
        for attempt in range(self.cfg.max_retries):
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.cfg.timeout_s) as r:
                    return json.loads(r.read())
            except urllib.error.HTTPError as e:
                last = e
                if e.code in (429, 500, 502, 503, 529):
                    time.sleep(2 ** attempt); continue
                raise
            except urllib.error.URLError as e:
                last = e; time.sleep(2 ** attempt)
        raise RuntimeError(f"{self.cfg.kind}: failed after {self.cfg.max_retries} retries: {last}")


class AnthropicProvider(_HTTPProvider):
    @property
    def snapshot(self) -> str: return f"anthropic:{self.cfg.model}"
    def complete(self, system: str, messages: List[Dict[str, str]]) -> str:
        url = self.cfg.base_url or "https://api.anthropic.com/v1/messages"
        out = self._post(url, {
            "model": self.cfg.model, "max_tokens": self.cfg.max_tokens,
            "temperature": self.cfg.temperature, "system": system, "messages": messages,
        }, {"content-type": "application/json", "x-api-key": self.key,
            "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in out.get("content", []))


class OpenRouterProvider(_HTTPProvider):
    @property
    def snapshot(self) -> str: return f"openrouter:{self.cfg.model}"
    def complete(self, system: str, messages: List[Dict[str, str]]) -> str:
        url = self.cfg.base_url or "https://openrouter.ai/api/v1/chat/completions"
        msgs = [{"role": "system", "content": system}] + messages
        payload = {"model": self.cfg.model, "messages": msgs,
                   "max_tokens": self.cfg.max_tokens, "temperature": self.cfg.temperature}
        if self.cfg.seed is not None:
            payload["seed"] = self.cfg.seed
        out = self._post(url, payload,
                         {"content-type": "application/json",
                          "authorization": f"Bearer {self.key}"})
        return out["choices"][0]["message"]["content"]


def make_provider(cfg: ProviderConfig) -> Provider:
    if cfg.kind == "mock":       return MockProvider(cfg)
    if cfg.kind == "anthropic":  return AnthropicProvider(cfg)
    if cfg.kind == "openrouter": return OpenRouterProvider(cfg)
    raise ValueError(f"unknown provider kind: {cfg.kind}")


def available(cfg: ProviderConfig) -> bool:
    return cfg.kind == "mock" or bool(os.environ.get(cfg.api_key_env, ""))
