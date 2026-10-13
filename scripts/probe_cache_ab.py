"""A/B cache-mining probe — settle "is the provider caching?" with data, not vibes.

Provenance (2026-08-25): the fleet spent a morning disputing whether glm-4.7-flash
actually prefix-caches (ledger said 0.3%, A/B said 99%+). Root cause of the dispute:
the ledger's low ratio was PREFIX VARIATION in other callers, not provider behavior.
This probe isolates the variable: two byte-identical calls through mag.glm_flash's
frozen self. Call 2's cached_tokens is the truth.

Verdict rules (honest, not hopeful):
  call2 cached/prompt >= 0.90  -> mining: OK   (provider caches; look elsewhere for waste)
  call2 cached/prompt >= 0.50  -> mining: WEAK (partial hits; suspect prefix drift)
  call2 cached/prompt <  0.50  -> mining: BROKEN (no auto-cache on this lane today)

Usage:
  .venv/Scripts/python.exe scripts/probe_cache_ab.py            # default probe on glm-4.7-flash
  .venv/Scripts/python.exe scripts/probe_cache_ab.py --json     # machine-readable, exit 0/1/2

Exit codes: 0 mining OK · 1 weak/broken · 2 probe error (API/lane down).
Run it any day the ledger's hit ratio looks wrong; trust it over the ledger,
because it controls the prefix.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run_probe() -> dict:
    from mag.glm_flash import cached_chat

    task = "Reply with exactly: CACHE-PROBE-ACK"
    r1 = cached_chat(task)
    r2 = cached_chat(task)
    ratio1 = r1["cached_tokens"] / r1["prompt_tokens"] if r1["prompt_tokens"] else 0.0
    ratio2 = r2["cached_tokens"] / r2["prompt_tokens"] if r2["prompt_tokens"] else 0.0

    if not (r1.get("ok") and r2.get("ok")):
        verdict = "error"
        err = r2.get("error") or r1.get("error") or "unknown"
    elif ratio2 >= 0.90:
        verdict = "ok"
        err = ""
    elif ratio2 >= 0.50:
        verdict = "weak"
        err = ""
    else:
        verdict = "broken"
        err = ""

    return {
        "schema": "probe_cache_ab.v1",
        "model": r2.get("model") or "glm-4.7-flash",
        "call1": {k: r1[k] for k in ("ok", "cached_tokens", "prompt_tokens", "completion_tokens")},
        "call2": {k: r2[k] for k in ("ok", "cached_tokens", "prompt_tokens", "completion_tokens")},
        "cache_ratio_call1": round(ratio1, 4),
        "cache_ratio_call2": round(ratio2, 4),
        "verdict": verdict,
        "error": err,
        "note": "byte-identical calls through the frozen self; call2's ratio is the mining truth",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="A/B cache-mining probe (glm-4.7-flash)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    out = run_probe()
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        c1, c2 = out["call1"], out["call2"]
        print(f"call1: {c1['cached_tokens']}/{c1['prompt_tokens']} cached ({out['cache_ratio_call1']*100:.1f}%) — the write")
        print(f"call2: {c2['cached_tokens']}/{c2['prompt_tokens']} cached ({out['cache_ratio_call2']*100:.1f}%) — the mine")
        print(f"verdict: {out['verdict'].upper()}" + (f" ({out['error']})" if out["error"] else ""))

    if out["verdict"] == "error":
        return 2
    return 0 if out["verdict"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
