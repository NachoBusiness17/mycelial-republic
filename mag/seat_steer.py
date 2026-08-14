"""seat_steer — the ARCHITECTURE PATH for live seat actions (send a message into ChatGPT/grok/etc)
so the agent NEVER reaches for a shell. Mirrors mag/extension_deploy.py + mag/embassy_deliver.py
(the established "op with no queue/REST path gets one built" precedent — stolen from them).

OPERATOR (2026-08-12): "why do you reach for tools like powershell?" -> "build the path".
The reason I reached for the shell: it was the only generic executor I had for a live action. The
FIX is to give every live seat action an architecture-native path:
  1. send(surface, message)  — the actual steer: reuse chatgpt_bot / grok_bot / browser_driver for
                               the surface, fold the answer + spend to memory/runs/seat_steer/. The
                               agent calls THIS, never a shell.
  2. enqueue(surface, message) — write a QUEUE TASK FILE so the DRAINER executes send() headless.
                               I drop a file; the drainer runs it; no shell, no hand-run.
  3. spawn_task handler       — a `[seat-steer]` prefix in orchestrator.spawn_task runs send()
                               inline (mirroring the [steward]/[token-chain]/[frontier-advice]).
  4. REST route               — POST /api/v1/seat/steer  ->  send() (like /api/v1/extension/deploy).

Honest: send() reports if the seat/browser is down — never fabricates an answer.

Schema: seat_steer.v1 · deterministic $0 (routing) · reuse: chatgpt_bot, grok_bot, browser_driver,
frontier_council, extension_deploy (the path precedent).
"""
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "seat_steer.v1"
REPORT_DIR = ROOT / "memory" / "runs" / "seat_steer"
PREFIX = "[seat-steer]"

# Which surfaces this path can steer -> which seat module drives them.
SURFACE_DRIVERS = {
    "chatgpt": ("chatgpt_bot", "chatgpt"),
    "grok": ("grok_bot", "grok"),
    "grok_x": ("grok_bot", "x"),
    "deepseek": ("browser_driver", "deepseek"),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def send(surface: str, message: str, *, max_wait_s: int = 120) -> dict[str, Any]:
    """The ACTUAL live steer for a surface. Reuses the seat module (chatgpt_bot/grok_bot/
    browser_driver). Honest: if the seat/browser is down, reports it — never fabricates an answer.
    Folds the answer + spend to memory/runs/seat_steer/."""
    surface = (surface or "").strip().lower()
    message = (message or "").strip()
    if not message:
        return {"ok": False, "schema": SCHEMA, "error": "empty message"}
    driver = SURFACE_DRIVERS.get(surface)
    if not driver:
        return {"ok": False, "schema": SCHEMA, "surface": surface,
                "error": f"unknown surface {surface!r}; known: {sorted(SURFACE_DRIVERS)}"}
    mod_name, seat_surface = driver
    # STEER via the seat module (best-effort; honest if the seat is down)
    try:
        if mod_name == "browser_driver":
            from mag import browser_driver as bd
            r = bd.ask(message, surface=seat_surface, max_wait_s=max_wait_s)
            result = {"ok": r.get("ok", False), "answer": r.get("answer", ""),
                      "error": r.get("error")}
        else:
            seat = __import__(f"mag.{mod_name}", fromlist=[mod_name])
            r = seat.steer(message, surface=seat_surface, max_wait_s=max_wait_s)
            result = {"ok": r.get("ok", False), "answer": r.get("answer", ""),
                      "error": r.get("error")}
    except Exception as e:
        result = {"ok": False, "error": f"steer failed: {str(e)[:160]}"}
    # fold the answer + a frontier spend (routing guard inside frontier_council.spend)
    spend = {}
    try:
        from mag import frontier_council as fc
        spend = fc.spend(message, "chatgpt" if surface == "chatgpt" else
                         ("grok_web" if surface == "grok" else
                          ("grok_x" if surface == "grok_x" else "deepseek")))
    except Exception as e:
        spend = {"error": str(e)[:120]}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = _now()
    row = {"schema": SCHEMA, "ts": ts, "surface": surface, "message": message[:400],
           "answer": result.get("answer", ""), "ok": bool(result.get("ok")), "spend": spend}
    report = REPORT_DIR / f"steer_{ts[:19].replace(':','').replace('-','').replace('T','_')}_{surface}.json"
    report.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": bool(result.get("ok")), "schema": SCHEMA, "surface": surface,
            "message": message[:160], "answer": (result.get("answer") or "")[:2000],
            "spend": spend, "report": str(report.relative_to(ROOT)),
            "honest": "if the seat was down this reports it — the answer is never fabricated"}


def enqueue(surface: str, message: str, *, priority: int = 10) -> dict[str, Any]:
    """THE PATH: write a QUEUE TASK FILE so the DRAINER executes send() headless. I drop a file; the
    drainer runs it. NO shell, NO hand-run. The task goal is `[seat-steer] surface | message`, which
    spawn_task routes to send() (the handler below)."""
    surface = (surface or "").strip().lower()
    message = (message or "").strip()
    if surface not in SURFACE_DRIVERS:
        return {"ok": False, "schema": SCHEMA, "error": f"unknown surface {surface!r}"}
    if not message:
        return {"ok": False, "schema": SCHEMA, "error": "empty message"}
    try:
        from mag import orchestrator as o
        return o.enqueue(f"{PREFIX} {surface} | {message}", provider="deepseek",
                         tag="seat-steer", priority=priority, tier="mission")
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": f"enqueue failed: {str(e)[:120]}"}


def execute_goal(goal: str) -> dict[str, Any]:
    """Drainable handler body: parse `[seat-steer] surface | message` and run send() headless.
    Called by the orchestrator.spawn_task `[seat-steer]` prefix handler."""
    body = (goal or "").strip()
    if body.lower().startswith(PREFIX.lower()):
        body = body[len(PREFIX):].strip()
    if "|" in body:
        surface, message = body.split("|", 1)
        surface, message = surface.strip(), message.strip()
    else:
        surface, message = "chatgpt", body
    return send(surface, message)


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "send(surface,message)->the live steer (reuse the seat, fold answer+spend); "
                        "enqueue(surface,message)->write a queue task file so the DRAINER runs it "
                        "headless; execute_goal()->the drainable handler body; REST POST "
                        "/api/v1/seat/steer",
            "reuse": "chatgpt_bot + grok_bot + browser_driver + frontier_council + extension_deploy "
                     "(the path precedent)",
            "doctrine": "the agent never reaches for a shell — it enqueues a task file and the "
                        "drainer runs the live action headless"}


if __name__ == "__main__":
    import argparse, json
    ap = argparse.ArgumentParser(prog="seat-steer")
    ap.add_argument("cmd", nargs="?", default="status", choices=["send", "enqueue", "status"])
    ap.add_argument("--surface", default="chatgpt")
    ap.add_argument("--message", default="")
    ap.add_argument("--enqueue", action="store_true")
    a = ap.parse_args()
    if a.cmd == "enqueue" or a.enqueue:
        print(json.dumps(enqueue(a.surface, a.message or "say hi"), indent=2, default=str))
    elif a.cmd == "send":
        print(json.dumps(send(a.surface, a.message or "say hi"), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
