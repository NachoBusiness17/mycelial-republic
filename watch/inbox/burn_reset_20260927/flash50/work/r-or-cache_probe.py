"""r-or-cache live probe — OpenRouter prompt caching across stealth/ling/muse families.

Method (mirrors mag/_cache_ab_probe.py): SAME fixed prefix, back-to-back calls,
read usage.prompt_tokens_details.cached_tokens on every call. A real cache gives
2nd-call cached_tokens ~= prompt_tokens. Also records cache_write_tokens,
cache_discount, usage_details, and the native provider token that served each call.
$0 impact: muse-glimmer ~2.6k input tokens at $0.30/M ~= $0.0008; the other two are free.
"""
import json
import os
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
KEY = ""
for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
    if line.strip().startswith("OPENROUTER_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
        break
assert KEY, "no OPENROUTER_API_KEY in .env"

PREFIX = ("OpenRouter prompt-cache probe. This fixed context block is repeated verbatim "
          "across back-to-back calls so the provider can reuse its KV cache for it. " * 40)
PREFIX += ("Stable reference paragraph: the fleet routes stealth drops, ling MoE variants, "
           "and muse distills through one OpenRouter key chain. ") * 8
SESSION = "r-or-cache-probe-20260928"
MODELS = [
    "meta/muse-glimmer-30b",            # muse family, paid, Phala/DeepInfra/Together
    "inclusionai/ling-3.0-flash-fin:free",  # ling family, free lane
    "stealth/space-bunny-alpha",        # stealth family, $0/$0 anonymous drop
]
OUT = Path(__file__).with_name("r-or-cache_probe_results.jsonl")


def call(model: str, tail: str) -> dict:
    body = {
        "model": model,
        "session_id": SESSION,
        "max_tokens": 16,
        "temperature": 0,
        "usage": {"include": True},
        "messages": [
            {"role": "system", "content": PREFIX},
            {"role": "user", "content": "Reply with the single word: probe " + tail},
        ],
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + KEY,
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:8765",
            "X-Title": "Mag Resource Harness",
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            r = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"model": model, "ok": False, "error": repr(e)[:200], "latency_s": round(time.time() - t0, 1)}
    u = r.get("usage") or {}
    details = u.get("prompt_tokens_details") or {}
    return {
        "model": model,
        "ok": True,
        "provider": r.get("provider"),
        "latency_s": round(time.time() - t0, 1),
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "cached_tokens": details.get("cached_tokens"),
        "cache_write_tokens": details.get("cache_write_tokens"),
        "cache_discount": u.get("cache_discount"),
        "cost": u.get("cost"),
        "prompt_tokens_details_raw": details,
        "native_tokens": r.get("native_tokens") or (
            {k: u.get(k) for k in ("native_prompt_tokens", "native_completion_tokens",
                                   "native_tokens_cached", "native_tokens_reasoning")}),
    }


rows = []
for model in MODELS:
    for i in range(3):
        row = call(model, f"v{i}")
        rows.append(row)
        print(json.dumps({k: row.get(k) for k in ("model", "ok", "provider", "prompt_tokens",
                                                  "cached_tokens", "cache_write_tokens",
                                                  "cache_discount", "cost", "error")}, ensure_ascii=False))
        time.sleep(2)

with OUT.open("a", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("banked ->", OUT)
