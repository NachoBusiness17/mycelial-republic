"""Provider config, the in-process test double, and real endpoint calls.

One config file (JSON or YAML) declares every endpoint: local clones,
the mid tier, and the frontier. A provider entry looks like:

    {
      "model_id": "flash-mid-1",
      "base_url": "http://localhost:4000/v1",
      "model": "vendor/flash",
      "tier": "mid",
      "cost_usd_per_call": 0.004,
      "latency_ms": 800,
      "test_double": true,
      "confidence_default": 0.9,
      "confidence_by_task_shape": {"design_judgment": 0.55}
    }

Top-level keys: tier_order (cheapest to most expensive, e.g.
["local", "mid", "frontier"]), exploration_model (the designated mid-tier
model for unknown task shapes), providers (list as above).

TEST-DOUBLE MODE: when "test_double" is true the provider is answered by
an in-process fake, indistinguishable from a real one at the router call
boundary. Answers are deterministic: derived from sha256 of the payload,
never RNG. Confidence is configurable per model and per task_shape.
Latency is DECLARED, not slept: the constraint filter uses the declared
estimate and the response reports it; tests stay fast and deterministic.

REAL MODE: OpenAI-compatible POST {base_url}/chat/completions via
stdlib urllib. Confidence convention: when the endpoint provides a
calibrated probability (our clones do), it is read from the response
field "confidence" at the top level or inside choices[0]; otherwise
confidence is null and rule (d) of the router does not apply.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


class ConfigError(Exception):
    pass


@dataclass
class ProviderConfig:
    model_id: str
    base_url: str
    model: str
    tier: str
    cost_usd_per_call: float
    latency_ms: int = 0
    test_double: bool = False
    confidence_default: float = 0.9
    confidence_by_task_shape: dict[str, float] = field(default_factory=dict)
    api_key_env: str = ""

    def confidence_for(self, task_shape: str) -> float:
        return float(self.confidence_by_task_shape.get(task_shape, self.confidence_default))


@dataclass
class ProviderResponse:
    provider: str
    answer: str
    confidence: Optional[float]
    cost_usd: float
    latency_ms: int
    task_shape: str
    prior_context: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "answer": self.answer,
            "confidence": self.confidence,
            "cost_usd": self.cost_usd,
            "latency_ms": self.latency_ms,
            "task_shape": self.task_shape,
            "prior_context": self.prior_context,
        }


class ProviderRegistry:
    def __init__(self, providers: list[ProviderConfig], tier_order: list[str],
                 exploration_model: str):
        self.providers = {p.model_id: p for p in providers}
        self.tier_order = list(tier_order)
        self.exploration_model = exploration_model
        for p in providers:
            if p.tier not in self.tier_order:
                raise ConfigError(
                    f"provider {p.model_id} has tier {p.tier!r} not in tier_order"
                    f" {self.tier_order}"
                )
        if exploration_model not in self.providers:
            raise ConfigError(
                f"exploration_model {exploration_model!r} is not a configured provider"
            )

    def tier_rank(self, tier: str) -> int:
        return self.tier_order.index(tier)

    def get(self, model_id: str) -> ProviderConfig:
        return self.providers[model_id]

    def all(self) -> list[ProviderConfig]:
        return sorted(
            self.providers.values(),
            key=lambda p: (self.tier_rank(p.tier), p.cost_usd_per_call, p.model_id),
        )


# -- config loading ---------------------------------------------------------


def load_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # optional dependency, only for YAML configs
        except ImportError as exc:
            raise ConfigError(
                f"{path} is YAML but PyYAML is not installed; use a .json config"
                f" or pip install pyyaml"
            ) from exc
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ConfigError(f"config root must be a mapping, got {type(data).__name__}")
    return data


def build_registry(config: dict[str, Any]) -> ProviderRegistry:
    tier_order = config.get("tier_order")
    if not tier_order or not isinstance(tier_order, list):
        raise ConfigError("config needs a non-empty tier_order list (cheapest first)")
    raw_providers = config.get("providers")
    if not raw_providers:
        raise ConfigError("config needs a non-empty providers list")
    providers: list[ProviderConfig] = []
    for entry in raw_providers:
        for key in ("model_id", "base_url", "model", "tier"):
            if not entry.get(key):
                raise ConfigError(f"provider entry missing {key}: {entry}")
        if "cost_usd_per_call" not in entry:
            raise ConfigError(f"provider {entry.get('model_id')} missing cost_usd_per_call")
        providers.append(
            ProviderConfig(
                model_id=str(entry["model_id"]),
                base_url=str(entry["base_url"]),
                model=str(entry["model"]),
                tier=str(entry["tier"]),
                cost_usd_per_call=float(entry["cost_usd_per_call"]),
                latency_ms=int(entry.get("latency_ms", 0)),
                test_double=bool(entry.get("test_double", False)),
                confidence_default=float(entry.get("confidence_default", 0.9)),
                confidence_by_task_shape={
                    str(k): float(v)
                    for k, v in entry.get("confidence_by_task_shape", {}).items()
                },
                api_key_env=str(entry.get("api_key_env", "")),
            )
        )
    exploration = config.get("exploration_model") or _default_exploration(providers, tier_order)
    return ProviderRegistry(providers, tier_order, exploration)


def _default_exploration(providers: list[ProviderConfig], tier_order: list[str]) -> str:
    """No explicit exploration_model: cheapest provider of the middle tier."""
    if not tier_order:
        raise ConfigError("empty tier_order")
    mid_tier = tier_order[len(tier_order) // 2]
    tier_members = sorted(
        (p for p in providers if p.tier == mid_tier),
        key=lambda p: (p.cost_usd_per_call, p.model_id),
    )
    if not tier_members:
        raise ConfigError(
            f"cannot pick a default exploration model: no providers in middle tier"
            f" {mid_tier!r}; set exploration_model explicitly"
        )
    return tier_members[0].model_id


# -- calling ----------------------------------------------------------------


def normalize_payload(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def payload_digest(payload: Any) -> str:
    return hashlib.sha256(normalize_payload(payload).encode("utf-8")).hexdigest()[:12]


def call_provider(
    config: ProviderConfig,
    task_shape: str,
    payload: Any,
    prior_answers: Optional[list[str]] = None,
) -> ProviderResponse:
    """Dispatch to the test double or the real endpoint.

    The router only ever talks through this boundary, so a test double is
    indistinguishable from a live provider to every caller above it.
    """
    prior = list(prior_answers or [])
    if config.test_double:
        return _call_test_double(config, task_shape, payload, prior)
    return _call_real(config, task_shape, payload, prior)


def _call_test_double(
    config: ProviderConfig,
    task_shape: str,
    payload: Any,
    prior_answers: list[str],
) -> ProviderResponse:
    digest = payload_digest(payload)
    answer = f"canned:{config.model_id}:{task_shape}:{digest}"
    if prior_answers:
        # Escalation context marker: proves the prior answer was attached.
        answer = f"{answer}|ctx:{len(prior_answers)}:{prior_answers[-1][:32]}"
    return ProviderResponse(
        provider=config.model_id,
        answer=answer,
        confidence=config.confidence_for(task_shape),
        cost_usd=config.cost_usd_per_call,
        latency_ms=config.latency_ms,
        task_shape=task_shape,
        prior_context=len(prior_answers),
    )


def _call_real(
    config: ProviderConfig,
    task_shape: str,
    payload: Any,
    prior_answers: list[str],
    timeout_s: float = 30.0,
) -> ProviderResponse:
    """OpenAI-compatible chat completion over stdlib urllib.

    v0 honesty: this path is written but NOT exercised against a live
    endpoint (tests run $0 offline through the test double). Confidence
    is read from the documented "confidence" response field our clones
    emit; plain OpenAI endpoints leave it null.
    """
    import os
    import time

    messages: list[dict[str, str]] = []
    for prev in prior_answers:
        messages.append({"role": "assistant", "content": prev})
        messages.append(
            {"role": "user", "content": "Your prior answer lacked confidence."}
        )
    messages.append({"role": "user", "content": normalize_payload(payload)})
    body = json.dumps(
        {"model": config.model, "messages": messages, "task_shape": task_shape}
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if config.api_key_env:
        key = os.environ.get(config.api_key_env, "")
        if key:
            headers["Authorization"] = f"Bearer {key}"
    url = config.base_url.rstrip("/") + "/chat/completions"
    start = time.monotonic()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    latency_ms = int((time.monotonic() - start) * 1000)
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    confidence = data.get("confidence", choice.get("confidence"))
    return ProviderResponse(
        provider=config.model_id,
        answer=str(message.get("content", "")),
        confidence=None if confidence is None else float(confidence),
        cost_usd=config.cost_usd_per_call,
        latency_ms=latency_ms,
        task_shape=task_shape,
        prior_context=len(prior_answers),
    )
