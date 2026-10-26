#!/usr/bin/env python3
"""compute_finder -- where the free compute is, and the shortest path to it.

Operator, 2026-10-24: "find new compute, make getting the other compute easy for
me. if it's not easy it's not water. people are giving away compute every day."

So this tool answers exactly two questions:
  1. what can I use RIGHT NOW (key present, endpoint answers)?
  2. what can I claim in two minutes (signup URL + the exact env line)?

It does not invent providers. Everything here was probed on 2026-10-24 or is a
named free tier with a public signup. A provider is only "easy" if it is
OpenAI-compatible: one base URL, one bearer token, no SDK.

    python tools/compute_finder.py map            # READY / CLAIM / DEAD
    python tools/compute_finder.py claim          # only the two-minute ones
    python tools/compute_finder.py check <id>     # probe one provider
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "configs" / "compute_catalog.json"
ENV_FILES = [ROOT / ".env", Path(os.path.expanduser("~")) / "AppData" / "Local" / "hermes" / ".env"]
UA = "sovereign-mag-compute-finder/1.0"


def load_env() -> dict[str, str]:
    env = {}
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def probe(provider: dict, env: dict) -> dict:
    key = env.get(provider["key_env"]) or os.environ.get(provider["key_env"], "")
    if not key:
        return {"id": provider["id"], "state": "CLAIM", "detail": provider.get("status_hint", ""),
                "signup": provider.get("signup"), "key_env": provider["key_env"]}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": UA}
    headers.update(provider.get("extra_headers") or {})
    body = {"model": provider["model"],
            "messages": [{"role": "user", "content": "Reply exactly: ALIVE"}],
            "max_tokens": 1200}
    url = provider["base"].rstrip("/") + "/chat/completions"
    started = datetime.now(timezone.utc)
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
            msg = (payload.get("choices") or [{}])[0].get("message", {}) or {}
            text = msg.get("content") or msg.get("reasoning_content") or ""
        except json.JSONDecodeError:
            text = raw[:40]
        ok = bool(str(text).strip())
        ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
        return {"id": provider["id"], "state": "READY" if ok else "EMPTY",
                "detail": f"{provider['model']} · {ms} ms · {str(text).strip()[:12]!r}", "ms": ms}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:140].replace("\n", " ")
        return {"id": provider["id"], "state": "DEAD", "detail": f"HTTP {exc.code} {detail}"}
    except Exception as exc:  # noqa: BLE001
        return {"id": provider["id"], "state": "DEAD", "detail": f"{type(exc).__name__}: {str(exc)[:90]}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Free/cheap compute map")
    ap.add_argument("cmd", choices=["map", "claim", "check", "add"])
    ap.add_argument("provider", nargs="?")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    env = load_env()
    providers = catalog["providers"]

    if args.cmd == "add":
        match = [p for p in providers if p["id"] == args.provider]
        if not match:
            print(f"unknown provider {args.provider!r}")
            return 2
        prov = match[0]
        try:
            value = input(f"paste {prov['key_env']} (not echoed to shell history): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\naborted")
            return 2
        if not value:
            print("empty key, nothing written")
            return 2
        trial = dict(env); trial[prov["key_env"]] = value
        res = probe(prov, trial)
        if res["state"] != "READY":
            print(f"REFUSED - key did not answer: {res['state']} {res['detail']}")
            print("nothing written to .env")
            return 1
        with (ROOT / ".env").open("a", encoding="utf-8") as fh:
            fh.write(f"\n{prov['key_env']}={value}\n")
        print(f"WROTE {prov['key_env']} to .env and it answers: {res['detail']}")
        return 0
    if args.cmd == "check":
        match = [p for p in providers if p["id"] == args.provider]
        if not match:
            print(f"unknown provider {args.provider!r}; ids: {[p['id'] for p in providers]}")
            return 2
        res = probe(match[0], env)
        print(json.dumps(res, indent=2) if args.json else f"{res['state']:6s} {res['id']:18s} {res['detail']}")
        return 0 if res["state"] == "READY" else 1

    results = [probe(p, env) for p in providers]
    if args.cmd == "claim":
        results = [r for r in results if r["state"] == "CLAIM"]
    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    icon = {"READY": "READY ", "CLAIM": "CLAIM ", "EMPTY": "EMPTY ", "DEAD": "DEAD  "}
    for r in sorted(results, key=lambda x: {"READY": 0, "EMPTY": 1, "CLAIM": 2, "DEAD": 3}[x["state"]]):
        line = f"{icon[r['state']]} {r['id']:18s} {str(r.get('detail'))[:64]}"
        print(line)
        if r["state"] == "CLAIM":
            print(f"        {r['signup']}")
            print(f"        echo '{r['key_env']}=<paste>' >> .env   then: python tools/compute_finder.py check {r['id']}")
    ready = sum(1 for r in results if r["state"] == "READY")
    claim = sum(1 for r in results if r["state"] == "CLAIM")
    print(f"\n{ready} ready · {claim} claimable in ~2 min · {len(results) - ready - claim} dead")
    return 0


if __name__ == "__main__":
    sys.exit(main())
