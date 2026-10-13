"""Janitor: provider liveness probe for the 12 free-tier remote providers.

One 1-token call per provider through the canonical models.providers.chat_provider
path (env loading, multi-key failover, browser UA, quota ledger). Writes results
to memory/runs/janitor/provider_liveness.json. Never prints or stores key values.

The 12 = the free-tier remote lanes of providers.yaml routing (public_summarize
free block): openrouter, nvidia, groq, z_ai, github_models, mistral, moonshot,
fireworks, cerebras, cohere, hf_router, dashscope. Local ollama and paid
providers (deepseek*, openai, anthropic, gemini, xai, vast) are out of scope.

Run: .venv\\Scripts\\python.exe scripts\\provider_liveness.py [--dry]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from models.providers import chat_provider, get_provider, provider_keys  # noqa: E402

FREE_PROVIDERS = [
    "openrouter",
    "nvidia",
    "groq",
    "z_ai",
    "github_models",
    "mistral",
    "moonshot",
    "fireworks",
    "cerebras",
    "cohere",
    "hf_router",
    "dashscope",
]

PROBE_SYSTEM = "You are a liveness probe."
PROBE_USER = "Reply with exactly one word: pong"
MAX_TOKENS = 1
OUT_PATH = REPO / "memory" / "runs" / "janitor" / "provider_liveness.json"


def classify(res: dict) -> tuple[bool | None, str]:
    """alive: True=endpoint+auth+quota OK, False=dead/error, None=could not test."""
    if res.get("ok"):
        return True, "alive"
    if res.get("empty_reasoning"):
        # HTTP 200, auth + quota fine; the 1-token budget was consumed by a
        # reasoning model before emitting content. Lane is alive; probe budget
        # too small for THIS model, not a provider failure.
        return True, "alive_probe_budget_consumed_by_reasoning"
    err = str(res.get("error") or "")
    if err.startswith("missing API key"):
        return None, "no_key"
    if err.startswith("quota exhausted"):
        return None, "mag_quota_gate_refused"
    if err.startswith("refused") or err.startswith("deferred_peak"):
        return None, "gate_refused"
    return False, "error"


def probe(pid: str) -> dict:
    t0 = time.perf_counter()
    res = chat_provider(
        pid,
        PROBE_SYSTEM,
        PROBE_USER,
        max_tokens=MAX_TOKENS,
        tier="T2",
    )
    wall_ms = int((time.perf_counter() - t0) * 1000)
    alive, status = classify(res)
    usage = res.get("usage") or {}
    row = {
        "provider": pid,
        "alive": alive,
        "status": status,
        "ok": bool(res.get("ok")),
        "model": res.get("model"),
        "wall_ms": wall_ms,
        "completion_tokens": usage.get("completion_tokens"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "key_idx": res.get("key_idx"),
    }
    if not res.get("ok"):
        row["error"] = str(res.get("error"))[:300]
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="show plan, make no calls")
    args = ap.parse_args()

    if args.dry:
        for pid in FREE_PROVIDERS:
            p = get_provider(pid) or {}
            print(f"would probe {pid:14} model={p.get('default_model')}")
        print(f"would write {OUT_PATH}")
        return 0

    rows = []
    for pid in FREE_PROVIDERS:
        p = get_provider(pid) or {}
        row = probe(pid)
        row["key_present"] = bool(provider_keys(p))
        rows.append(row)
        mark = {True: "ALIVE", False: "DEAD", None: "UNTESTED"}[row["alive"]]
        print(f"{mark:8} {pid:14} {row['status']:44} {row['wall_ms']:6}ms {row.get('error', '')[:80]}")

    summary = {
        "n_probed": len(rows),
        "n_alive": sum(1 for r in rows if r["alive"] is True),
        "n_dead": sum(1 for r in rows if r["alive"] is False),
        "n_untested": sum(1 for r in rows if r["alive"] is None),
        "no_key": [r["provider"] for r in rows if r["status"] == "no_key"],
        "dead": [r["provider"] for r in rows if r["alive"] is False],
    }
    out = {
        "schema": "provider_liveness.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "probe": {
            "system": PROBE_SYSTEM,
            "user": PROBE_USER,
            "max_tokens": MAX_TOKENS,
            "tier": "T2",
            "path": "models.providers.chat_provider",
            "providers_tested": FREE_PROVIDERS,
            "selection": "free-tier remote lanes from configs/providers.yaml routing "
                         "(public_summarize free block); local ollama + paid providers excluded",
        },
        "results": rows,
        "summary": summary,
        "cost": "$0 (1-token probes on free-tier lanes only)",
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nalive={summary['n_alive']}/{summary['n_probed']} "
          f"dead={summary['n_dead']} untested={summary['n_untested']} -> {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
