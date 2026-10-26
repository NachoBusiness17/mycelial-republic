"""V9 price probe - Nous inference API, one tiny call per model (2026-09-30).

Mission (operator): the Nous portal is discounted; the estate needs the real
price table. Prior session probed 6 models; this probes 26 more key models
(1 call each, max_tokens 50) and derives: model | blended $/M | input rate |
output rate. Rates derive from usage.cost_details.rate_source
(openrouter_list => OpenRouter catalog per-token rates, fetched live) and are
VALIDATED per model by comparing catalog-predicted cost against the actual
usage.cost the API metered. The actual/predicted ratio is the Nous-side
discount multiplier (1.0 = list rates).

Budget: $0.50 total cap (tiny probes only). Hard guard: stop at $0.40 spent
or when next-model worst-case projection would exceed $0.50. The diagnostic
ember-1 probe earlier this session cost $0.001005 and is counted in the cap.

Laws honored: budget guard before every fire; no em-dashes in anything this
file writes; results land as JSON next to the V9 receipt.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/v9_probe_prices.py [--dry]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERMES_DIR = Path(r"C:\Users\foste\AppData\Local\hermes")
BASE = "https://inference-api.nousresearch.com/v1/chat/completions"
KEY_ENVS = ("NOUS_SDD_API_KEY", "HERMES_API_KEY_1", "HERMES_API_KEY_2")
OR_MODELS = "https://openrouter.ai/api/v1/models"

BUDGET_CAP = 0.50        # mission cap, total
STOP_AT = 0.40           # hard stop for accumulated actual spend
PRIOR_SPENT = 0.001005   # ember-1 diagnostic probe already burned this session
MAX_TOKENS = 50
PROMPT = "Reply with the single word: ok"

# 26 targets: cheap tier, mid tier, all opuses, gpt-6 family, grok family, fable
MODELS = [
    # cheap
    "openai/gpt-oss-120b",
    "mistralai/ministral-3b-2512",
    "google/gemma-4-31b-it",
    # mid
    "mistralai/mistral-medium-3.1",
    "qwen/qwen3.7-plus",
    "aion-labs/aion-3.5",
    # opuses (all non-batch)
    "anthropic/claude-opus-4.1",
    "anthropic/claude-opus-4.5",
    "anthropic/claude-opus-4.6",
    "anthropic/claude-opus-4.7",
    "anthropic/claude-opus-4.8",
    "anthropic/claude-opus-5",
    "anthropic/claude-opus-5.5",
    # gpt-6 family (non-batch)
    "openai/gpt-6-astra",
    "openai/gpt-6-astra-pro",
    "openai/gpt-6-luna",
    "openai/gpt-6-sol",
    "openai/gpt-6-sol-pro",
    "openai/gpt-6.1-sol-pro",
    # grok family
    "x-ai/grok-4.20",
    "x-ai/grok-4.3",
    "x-ai/grok-4.5",
    "x-ai/grok-4.6",
    "x-ai/grok-4.7",
    # fable
    "anthropic/claude-fable-5",
    "anthropic/claude-fable-5.1",
]

# known from prior probing / duel metering (NOT re-probed here; listed in the
# receipt as prior rows): z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime,
# fireworks/ember-1 (+ the other 3 of the prior 6 not re-probed).


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            import os
            os.environ.setdefault(k.strip(), v.strip())


def load_keys() -> list[str]:
    load_dotenv(HERMES_DIR / ".env")
    load_dotenv(ROOT / ".env")
    keys = [k for k in (__import__("os").environ.get(e) for e in KEY_ENVS) if k]
    return keys


def fetch_catalog(want: set[str]) -> dict[str, tuple[float, float]]:
    """OpenRouter public catalog: per-token rates -> $/M pair."""
    req = urllib.request.Request(OR_MODELS, headers={"User-Agent": "mag-v9-probe"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    out: dict[str, tuple[float, float]] = {}
    for m in data.get("data", []):
        if m.get("id") in want:
            p = m.get("pricing", {})
            out[m["id"]] = (float(p["prompt"]) * 1e6, float(p["completion"]) * 1e6)
    return out


def call(model: str, key: str) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r) | {"_secs": round(time.time() - t0, 1)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)

    keys = load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    catalog = fetch_catalog(set(MODELS))
    missing = [m for m in MODELS if m not in catalog]
    print(f"catalog matched {len(catalog)}/{len(MODELS)}; missing: {missing}")
    if args.dry:
        print(json.dumps({"models": MODELS, "cap": BUDGET_CAP}, indent=1))
        return 0

    spent = PRIOR_SPENT
    rows: list[dict] = []
    out_path = Path(__file__).with_name("v9_probe_prices.json")

    for i, model in enumerate(MODELS):
        pin, pout = catalog.get(model, (None, None))
        # worst-case projection: 200 prompt + 60 completion tokens at catalog rates
        worst = 0.0
        if pin is not None:
            worst = (200 * pin + 60 * pout) / 1e6
        if spent + worst > BUDGET_CAP or spent > STOP_AT:
            print(f"BUDGET HOLD at ${spent:.4f}; stopping before {model}")
            break
        err = None
        try:
            resp = call(model, keys[i % len(keys)])
            u = resp.get("usage", {})
            usage = {
                "prompt_tokens": u.get("prompt_tokens"),
                "completion_tokens": u.get("completion_tokens"),
                "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                "cost": u.get("cost"),
                "cost_details": u.get("cost_details"),
            }
            msg = (resp.get("choices") or [{}])[0].get("message", {})
            row = {
                "model": model, "usage": usage,
                "finish": (resp.get("choices") or [{}])[0].get("finish_reason"),
                "content_head": (msg.get("content") or "")[:40],
                "secs": resp.get("_secs"),
            }
            if usage["cost"] is not None:
                spent += float(usage["cost"])
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read()[:200]!r}"
            row = {"model": model, "error": err}
        except Exception as e:  # noqa: BLE001 - record and continue to next model
            err = f"{type(e).__name__}: {e}"
            row = {"model": model, "error": err}
        rows.append(row)
        u = row.get("usage") or {}
        pred = None
        ratio = None
        if pin is not None and u.get("cost") is not None:
            pred = (u["prompt_tokens"] * pin + u["completion_tokens"] * pout) / 1e6
            ratio = u["cost"] / pred if pred > 0 else None
        print(f"[{i+1}/{len(MODELS)}] {model} cost={u.get('cost')} "
              f"pred={pred and round(pred, 6)} ratio={ratio and round(ratio, 4)} "
              f"in={u.get('prompt_tokens')} out={u.get('completion_tokens')} "
              f"err={err} spent=${spent:.4f}")

    payload = {
        "ran_at": "2026-09-30",
        "budget_cap": BUDGET_CAP,
        "prior_spent_counted": PRIOR_SPENT,
        "total_spent": round(spent, 6),
        "catalog_rates_per_M": catalog,
        "rows": rows,
    }
    out_path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"WROTE {out_path} ; total spent ${spent:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
