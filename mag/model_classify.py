"""model_classify — classify the kind of content by the model that produced it.

Operator (2026-08-12): "go classify the kind of content via its model eg deepseek v4 flash low or
sol 5.6 grok 4.5 deepseek pro etc."

The pipeline already records content WITH its producing model (refine role_outputs.model, grok
ledger.model, agent_corpus version). This classifies a model -> a capability tier (low/med/high) +
a content kind, so downstream knows the quality/cost class of every piece of content WITHOUT
re-reading it. Deterministic + pure stdlib (bare-metal rule — survives losing all remote compute).
Idempotent + content-addressed where it touches the corpus.

Tier legend (operator examples):
  low   — deepseek-v4-flash, deepseek-chat, small local (gemma/llama-3/phi/qwen-small): bulk/code-exec
  med   — deepseek-pro/reasoner, deepseek-v4, kimi, gpt-4o, claude-sonnet: reasoning
  high  — sol 5.6, grok-4.5, gpt-5, gpt-4.1, claude-opus/o3: frontier

Schema: model_classify.v1 · deterministic + $0 · pure stdlib
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "model_classify.v1"

# tier -> (regex list, content kind). First matching tier wins (high > med > low).
MODEL_TIERS: list[tuple[str, str, list[str]]] = [
    ("high", "frontier", [
        r"sol[-\s]?5", r"grok[-\s]?4", r"grok[-\s]?4\.5", r"gpt-5", r"gpt-4\.1",
        r"claude[-\s]?opus", r"claude[-\s]?4", r"\bo[34]", r"grok-(big-brain|reasoning)",
    ]),
    ("med", "reasoning", [
        r"deepseek[-\s]?pro", r"deepseek[-\s]?reasoner", r"deepseek[-\s]?r1", r"deepseek-v4\b",
        r"deepseek-v4-pro", r"kimi", r"gpt-4o", r"claude[-\s]?sonnet", r"gemini[-\s]?2",
        r"qwen[-\s]?(?:72|110|32)", r"deepseek-v3",
    ]),
    ("low", "bulk", [
        r"deepseek[-\s]?v4-flash", r"deepseek[-\s]?chat", r"flash", r"gemma", r"llama[-\s]?3",
        r"mistral[-\s]?7b", r"phi[-\s]?\d", r"qwen[-\s]?(?:0\.5|1\.5|2\.5b|small)", r"flex",
    ]),
]

_DEFAULT = ("med", "reasoning")


def tier_of(model: str) -> tuple[str, str]:
    """Return (tier, kind) for a model id. Deterministic, first-match-wins, high > med > low."""
    m = (model or "").strip().lower()
    if not m:
        return _DEFAULT
    for tier, kind, pats in MODEL_TIERS:
        for pat in pats:
            if re.search(pat, m):
                return tier, kind
    return _DEFAULT


def classify(text: str = "", model: str = "") -> dict[str, Any]:
    """Classify content by its producing model. Returns {model, tier, kind, chars}."""
    tier, kind = tier_of(model)
    return {
        "schema": SCHEMA,
        "model": (model or "").strip(),
        "tier": tier,
        "kind": kind,
        "chars": len(text or ""),
    }


def classify_corpus() -> dict[str, Any]:
    """Classify the durable agent_corpus ledgers by each agent's producing model/version."""
    try:
        from mag.agent_corpus import corpus, AGENTS
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:120]}
    out: dict[str, Any] = {}
    by_tier = {"high": 0, "med": 0, "low": 0}
    for a in AGENTS:
        agent = a["id"]
        c = corpus(agent)
        versions = a.get("versions") or []
        if not versions:
            out[agent] = {"tier": "med", "kind": "reasoning", "n_chats": c.get("n_chats", 0)}
            continue
        # classify by the agent's newest known version (provenance of record)
        v = versions[-1]
        tier, kind = tier_of(v)
        n = c.get("n_chats", 0)
        by_tier[tier] = by_tier.get(tier, 0) + n
        out[agent] = {"model": v, "tier": tier, "kind": kind, "n_chats": n}
    return {"ok": True, "schema": SCHEMA, "agents": out, "by_tier": by_tier,
            "total_chats": sum(by_tier.values())}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "classify(text, model) -> {model, tier: low|med|high, kind: bulk|reasoning|"
                        "frontier}; classify_corpus() -> per-agent tier from agent_corpus; "
                        "deterministic, pure stdlib.",
            "tiers": [t for t, _, _ in MODEL_TIERS]}


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="model_classify")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("classify", help="classify(text, model)")
    c.add_argument("--model", default="")
    c.add_argument("--text", default="")
    sub.add_parser("corpus", help="classify the agent_corpus ledgers by model")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "corpus":
        print(json.dumps(classify_corpus(), indent=2, ensure_ascii=False, default=str))
        return 0
    if a.cmd == "status":
        print(json.dumps(status(), indent=2, default=str))
        return 0
    print(json.dumps(classify(a.text, a.model), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
