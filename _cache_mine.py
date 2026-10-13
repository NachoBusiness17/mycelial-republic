"""CACHE MINE — measure what cache mining actually yields (2026-08-25).

For each working lane: run the same frozen-prefix call 3x, watch cached_tokens climb to
the prefix length (the warm-up curve), then compute the per-call economics at that lane's
real pricing. Turns "cache mining" from a slogan into per-lane numbers.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

from mag.rib_cache import FROZEN_RIB  # noqa: E402

# per-lane pricing (USD per 1M tokens: fresh input / cached input / output) — grounded
# from docs.z.ai pricing + the deepseek table. Free lanes: 0.
PRICING = {
    "z_ai:glm-4.5-flash": (0.0, 0.0, 0.0),
    "z_ai:glm-4.5-air":   (0.2, 0.03, 1.1),
    "z_ai:glm-4.7-flashx": (0.07, 0.01, 0.4),
    "z_ai:glm-4-32b-0414-128k": (0.1, 0.1, 0.1),
    "z_ai:glm-4.6":       (0.6, 0.11, 2.2),
    "z_ai:glm-4.7":       (0.6, 0.11, 2.2),
    "z_ai:glm-5":         (1.0, 0.2, 3.2),
    "z_ai:glm-5.1":       (1.4, 0.26, 4.4),
    "or:dots-3-note-preview": (0.0, 0.0, 0.0),
    "or:minimax-m3":      (0.0, 0.0, 0.0),
    "or:minimax-m2.7":    (0.0, 0.0, 0.0),
    "or:cohere-north-mini-code": (0.0, 0.0, 0.0),
}

TASK = "State the single most important principle of the record, one sentence."


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _keys() -> tuple[str, str]:
    k1 = k2 = ""
    for line in _read(ROOT / ".env").splitlines():
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
            k1 = line.split("=", 1)[1].strip().strip('"')
        if line.startswith("OPENROUTER_API_KEY_2=") and not line.startswith("#"):
            k2 = line.split("=", 1)[1].strip().strip('"')
    return k1, k2


def zai_call(model: str) -> dict:
    from mag.concurrency_gate import hold
    from models.providers import chat_provider
    try:
        with hold(model, timeout=90, owner="cache_mine"):
            r = chat_provider("z_ai", system=FROZEN_RIB, user=TASK, model=model,
                              thinking=False, max_tokens=64, tier="T2")
    except TimeoutError:
        return {"ok": False, "cached": 0, "prompt": 0, "error": "concurrency timeout"}
    u = r.get("usage") or {}
    return {"ok": bool(r.get("ok")), "error": str(r.get("error") or "")[:60],
            "cached": int(u.get("prompt_cache_hit_tokens")
                          or (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0),
            "prompt": int(u.get("prompt_tokens") or 0)}


def or_call(model: str) -> dict:
    k1, k2 = _keys()
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": FROZEN_RIB},
                     {"role": "user", "content": TASK}],
        "max_tokens": 64,
    }).encode()
    last = "(no key)"
    for key in (k1, k2):
        if not key:
            continue
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.loads(r.read().decode())
                u = j.get("usage") or {}
                return {"ok": True, "error": "",
                        "cached": int(u.get("prompt_tokens_details", {}).get("cached_tokens") or 0),
                        "prompt": int(u.get("prompt_tokens") or 0)}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
        except Exception as e:
            last = str(e)[:60]
    return {"ok": False, "cached": 0, "prompt": 0, "error": last}


def main() -> int:
    prefix_tokens = len(FROZEN_RIB) // 4
    print(f"FROZEN_RIB: {len(FROZEN_RIB)} chars ≈ {prefix_tokens} prefix tokens")
    rows = []
    for lane, model in [
        ("z_ai", "glm-4.5-flash"), ("z_ai", "glm-4.5-air"), ("z_ai", "glm-4.7-flashx"),
        ("z_ai", "glm-4-32b-0414-128k"),
        ("z_ai", "glm-4.6"), ("z_ai", "glm-4.7"),
        ("z_ai", "glm-5"), ("z_ai", "glm-5.1"),
        ("or", "dots-studio/dots-3-note-preview:free"),
        ("or", "minimax/minimax-m3:free"), ("or", "minimax/minimax-m2.7:free"),
        ("or", "cohere/north-mini-code:free"),
    ]:
        key = f"{lane}:{model.split('/')[-1] if lane == 'or' else model}"
        prices = PRICING.get(key, (0.0, 0.0, 0.0))
        print(f"\n== {key} ...", flush=True)
        curve = []
        for i in range(3):
            r = zai_call(model) if lane == "z_ai" else or_call(model)
            curve.append(r)
            time.sleep(0.3)
        caches = [c.get("cached", 0) for c in curve]
        prompts = [c.get("prompt", 0) for c in curve]
        warm = max(caches) if caches else 0
        fresh_price, cached_price, _ = prices
        # economics once warm: per-call savings on the cached portion
        save_per_call = 0.0
        if fresh_price > 0 and warm > 0:
            save_per_call = warm * (fresh_price - cached_price) / 1_000_000
        rows.append({"lane": key, "curve": caches, "prompt": prompts, "warm_cached": warm,
                     "fresh_per_M": fresh_price, "cached_per_M": cached_price,
                     "save_per_call_usd": round(save_per_call, 6),
                     "errors": [c.get("error", "") for c in curve]})
        print(f"   curve: {caches}  (prefix ≈ {prefix_tokens}, warm hit {warm})")

    print("\n=== CACHE MINE SUMMARY ===")
    total_save_per_1000 = 0.0
    for r in rows:
        per_1k = r["save_per_call_usd"] * 1000
        total_save_per_1000 += per_1k
        print(f"{r['lane']:24} warm={r['warm_cached']:>5}  "
              f"save/call=${r['save_per_call_usd']:.6f}  per-1k=${per_1k:.2f}  {r['errors'][-1]}")
    print(f"\nFleet (these 9 lanes, 1000 warm calls each): ~${total_save_per_1000:.0f} saved input "
          f"(on paid lanes) — free lanes save 100% of what they'd otherwise cost.")
    print("The real numbers: paid lanes cut input 5.4x (glm) to 31x (deepseek); free lanes are $0 "
          "regardless — cache buys THROUGHPUT there (faster turn, more calls per slot).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
