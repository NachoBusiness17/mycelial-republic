#!/usr/bin/env python3
"""night_cadence.py — mechanical overnight beat for the seats (2026-08-29).

Operator challenge: "are you gonna pretend and they'll sit idle all night?"
This is the no-pretend loop: a task queue burned seat-by-seat, results posted
to the ROOM (watch/room.jsonl, thread "night-shift"), receipts in files.

Shape (autodrain pattern, law-conforming):
  - PID lock (single instance) — state/night_cadence.pid
  - bounded: stops when queue empty or MAX_BEATS
  - CPU-polite: sleep between beats
  - seats driven WITHOUT the desktop: codex via `codex exec`, flash/deepseek
    via deepseek lane (chat_provider), grok deferred (TUI has no headless
    mode yet — its beat stays queued for a desktop pass)

Run:  python watch/night_cadence.py            # burn the queue
      python watch/night_cadence.py status     # queue + lock state
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROOM = ROOT / "watch" / "room.jsonl"
PID_FILE = ROOT / "state" / "night_cadence.pid"
LOG = ROOT / "watch" / "night_cadence.log"
MAX_BEATS = 12
BEAT_SLEEP_S = 240
CODEX_TIMEOUT_S = 1200

TASKS = [
    {"id": "ns-1", "seat": "codex",
     "prompt": ("Check the explore.jsonl reconciliation fold: if memory/runs/fold/"
                "reconcile_receipt.json exists, verify open_before == marked + "
                "still_open + ambiguous and say BALANCED or the discrepancy. If it "
                "does not exist, complete the fold (mark drained canonical signals "
                "explored in memory/percolator/explore.jsonl, write the receipt with "
                "the four counts). FILE the receipt. Stop.")},
    {"id": "ns-2", "seat": "flash",
     "prompt": ("Rib consumption audit: list every RIB_*.md / rib file under "
                "queue/ in local_sovereign_agent, and for each determine from its "
                "content + neighboring files whether it was consumed (status/closed "
                "markers, receipts it references) or is stale. Terse table: file, "
                "state, evidence path. Cwd is the repo.")},
    {"id": "ns-3", "seat": "deepseek",
     "prompt": ("MCP-assumption sweep: in local_sovereign_agent docs/ and watch/, "
                "find claims that seats must go THROUGH the MCP server to reach "
                "fleet state, versus direct file/API usage that already exists "
                "(example: tonight the room runs with no MCP involved). List "
                "file:line claims that are now outdated, max 8, terse.")},
    {"id": "ns-4", "seat": "flash",
     "prompt": "Post in the room thread 'night-shift' the single word: alive, plus your model name."},
]


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
    print(line)
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def room_post(seat: str, event: str, text: str, thread: str = "night-shift",
              to: str | list[str] | None = None, reply_to: str | None = None) -> None:
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "seat": seat,
           "event": event, "thread": thread, "text": text[:4000]}
    if to:
        rec["to"] = to if isinstance(to, list) else [str(to)]
    if reply_to:
        rec["reply_to"] = str(reply_to)[:80]
    try:
        with ROOM.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, default=str) + "\n")
    except OSError:
        pass


def lock() -> bool:
    if PID_FILE.exists():
        old = PID_FILE.read_text().strip()
        if old:
            try:
                os.kill(int(old), 0)
                return False  # alive — single instance
            except OSError:
                pass  # stale
    PID_FILE.write_text(str(os.getpid()))
    return True


def run_codex(prompt: str) -> str:
    import shutil

    exe = shutil.which("codex")
    if not exe:
        return "codex binary not found on PATH"
    # list-form + shell=False (Mimosa): the prompt is argv, never shell-interpolated
    r = subprocess.run([exe, "exec", "--skip-git-repo-check", "-C", str(ROOT), prompt],
                       capture_output=True, text=True, timeout=CODEX_TIMEOUT_S,
                       shell=False)
    return (r.stdout or r.stderr or "")[-3000:]


def run_lane(prompt: str, model: str) -> str:
    from models.providers import chat_provider
    r = chat_provider("deepseek", system=(
            "You are a JIT night-shift agent of the sovereign fleet (repo "
            "local_sovereign_agent, cwd is the repo). Terse receipt-style findings: "
            "what you checked, what you found, exact paths."),
        user=prompt, model=model, thinking=False, max_tokens=2500, tier="T2")
    if r.get("ok"):
        return str(r.get("text") or "")[:3000]
    return f"error: {str(r.get('error'))[:300]}"


def main() -> int:
    if not lock():
        log("already running — exit")
        return 0
    room_post("cadence", "night_shift_open",
              f"night cadence up: {len(TASKS)} tasks, max {MAX_BEATS} beats, "
              f"sleep {BEAT_SLEEP_S}s. Seats: codex(exec) + flash/deepseek(lane). "
              "grok deferred: TUI has no headless mode yet.")
    for i, task in enumerate(TASKS[:MAX_BEATS]):
        seat, tid = task["seat"], task["id"]
        log(f"beat {i+1}/{len(TASKS)} task {tid} seat {seat}")
        room_post("cadence", "beat_start",
                  f"@{seat} {tid}: {task['prompt'][:240]}",
                  thread="night-shift", to=seat)
        try:
            if seat == "codex":
                out = run_codex(task["prompt"])
            else:
                out = run_lane(task["prompt"], "deepseek-v4-flash" if seat == "flash"
                               else "deepseek-v4-pro")
        except subprocess.TimeoutExpired:
            out = f"TIMEOUT after {CODEX_TIMEOUT_S}s"
        except Exception as e:  # noqa: BLE001 — a beat dying must not stop the shift
            out = f"beat error: {str(e)[:300]}"
        room_post(seat, "result", f"@{ 'cadence' } [{tid}]\n{out}",
                  thread="night-shift", to="cadence")
        log(f"beat {tid} done, {len(out)} chars")
        if i < len(TASKS) - 1:
            time.sleep(BEAT_SLEEP_S)
    room_post("cadence", "night_shift_done", "queue empty — cadence stopping. "
              "Receipts above; fold/audit outputs also on disk where applicable.")
    PID_FILE.unlink(missing_ok=True)
    log("night shift complete — lock released")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        alive = False
        if PID_FILE.exists():
            try:
                os.kill(int(PID_FILE.read_text().strip()), 0)
                alive = True
            except (OSError, SystemError):  # Windows signal-0 can raise SystemError
                alive = False
        print(json.dumps({"running": alive, "beats_defined": len(TASKS)}))
        sys.exit(0)
    sys.exit(main())
