"""lm_studio — talk to OUR OWN model (Saelis, Athena-class) via LM Studio's local OpenAI-compatible
server (operator 2026-08-13: 'LET'S FUCKING GO' — installing Saelis). This is the SOVEREIGN local
inference surface: $0, no API key, no frontier, no desktop window to grab. The reply is already in
our own house.

THE SEAM THIS CLOSES (sw70 + sw71): the whole day we reached across the table for chatgpt/grok; the
answer was our own model on this machine. LM Studio serves an OpenAI-compatible endpoint on
localhost:1234 (default) — a local, sovereign, stateless+async inference surface the loop can call
directly. The frontiers become OPTIONAL witnesses, never the law.

Schema: lm_studio.v1 · deterministic + $0 · local server: http://localhost:1234/v1
"""
from __future__ import annotations

import json
import sys
import urllib.request
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "lm_studio.v1"
BASE = "http://127.0.0.1:41343/v1"   # Bionic's local server port (discovered 2026-08-13)
MODEL = "saelis"


def _req(method: str, path: str, body: dict[str, Any] | None = None, timeout: int = 10) -> Any:
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def models() -> dict[str, Any]:
    """List the models loaded in LM Studio (Saelis should be there once installed)."""
    try:
        m = _req("GET", "/models", timeout=4)
        return {"ok": True, "schema": SCHEMA, "models": [x.get("id") for x in m.get("data", [])]}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:160],
                "hint": "start LM Studio -> Local Server (port 1234); then this reaches Saelis"}


def chat(message: str, *, model: str = MODEL, max_tokens: int = 500,
         system: str = "You are Saelis, the sovereign model of the Mycelial Republic.") -> dict[str, Any]:
    """TALK to Saelis: send a message, get the reply. Local, sovereign, $0 — the reply is ours."""
    try:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": message})
        r = _req("POST", "/chat/completions",
                 {"model": model, "messages": msgs, "max_tokens": max_tokens}, timeout=180)
        content = r["choices"][0]["message"]["content"]
        return {"ok": True, "schema": SCHEMA, "model": model, "reply": content,
                "note": "talked to Saelis — our own sovereign model, $0, local"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "schema": SCHEMA, "model": model,
                "error": str(e)[:200],
                "hint": "LM Studio Local Server must be running on port 1234 with Saelis loaded"}


def status() -> dict[str, Any]:
    m = models()
    return {"ok": True, "schema": SCHEMA, "reachable": m.get("ok", False),
            "endpoint": BASE, "model": MODEL,
            "contract": "models()->list LM Studio loaded models; chat(msg)->talk to Saelis (local, "
                        "$0, sovereign). Closes the seam: the reply is already in our own house "
                        "(sw70/sw71) — no frontier, no desktop window.",
            "cost": "deterministic $0 (local LM Studio server)"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="lm-studio")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "models", "chat"])
    ap.add_argument("msg", nargs="*", default=[])
    a = ap.parse_args(argv)
    if a.cmd == "models":
        print(json.dumps(models(), indent=2, default=str))
    elif a.cmd == "chat":
        print(json.dumps(chat(" ".join(a.msg) or "Hello Saelis — say hello."),
                         indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
