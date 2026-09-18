"""grounding_chain -- the wiring between the fleet's chained skills.

The fleet's systems are chained skills going through a series of events. What's
missing: the GROUNDING WIRE between links — a controller that reads the ledger
state, computes what fires next from evidence, fires it, and appends a grounding
row explaining why.

GROUNDING PRINCIPLE: the state of the system IS the evidence. The next action
is determined by what the evidence says, not by a clock or a hope.

All commands are STATIC lists (no computed values reach the shell). The drivers
themselves handle batching and lock checking.

RUN:  .venv\\Scripts\\python.exe scripts\\grounding_chain.py [--dry] [--once]
Schema: grounding_chain.v1
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BASE = ROOT / "watch" / "inbox" / "union_fullsend_20260917"
CHAIN_LOG = BASE / "grounding_chain.jsonl"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")

CMD_RESEARCH = [PY, str(ROOT / "scripts" / "union_fullsend_day.py"), "--batch", "16"]
CMD_BUILD = [PY, str(ROOT / "scripts" / "build_lane_game.py"), "--batch", "2"]


def read_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def queue_remaining() -> int:
    s = read_json(BASE / "state.json")
    if not s:
        return 0
    done = set(s.get("done", []))
    dead = set(s.get("dead", {}).keys())
    att = s.get("attempts", {})
    count = 0
    qf = BASE / "queue.jsonl"
    if qf.is_file():
        for ln in qf.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            rid = r.get("id")
            if rid and rid not in done and rid not in dead and att.get(rid, 0) < 2:
                count += 1
    return count


def build_remaining() -> int:
    b = read_json(BASE / "build_lane" / "state.json")
    if not b:
        return 0
    done = set(b.get("done", []))
    dead = set(b.get("dead", {}).keys())
    att = b.get("attempts", {})
    count = 0
    bf = BASE / "build_lane" / "briefs.json"
    if bf.is_file():
        try:
            briefs = json.loads(bf.read_text(encoding="utf-8"))
            for r in briefs:
                rid = r.get("id") if isinstance(r, dict) else None
                if rid and rid not in done and rid not in dead and att.get(rid, 0) < 2:
                    count += 1
        except Exception:
            pass
    return count


def lock_age(p: Path):
    if not p.is_file():
        return None
    return time.time() - p.stat().st_mtime


def evaluate() -> list[dict]:
    actions = []
    r_lock = lock_age(BASE / "run.lock")
    b_lock = lock_age(BASE / "build_lane" / "run.lock")
    r_rem = queue_remaining()
    b_rem = build_remaining()
    hour = datetime.now().hour

    if r_rem > 0:
        lock_ok = r_lock is None or r_lock > 900
        if lock_ok:
            actions.append({
                "action": "research",
                "cmd": CMD_RESEARCH,
                "why": f"research queue {r_rem}, lock clear/stale",
                "condition": "queue_nonempty + lock_clear",
            })

    if b_rem > 0:
        lock_ok = b_lock is None or b_lock > 900
        if lock_ok:
            actions.append({
                "action": "build",
                "cmd": CMD_BUILD,
                "why": f"build briefs {b_rem}, lock clear/stale",
                "condition": "briefs_nonempty + lock_clear",
            })

    if r_rem < 6:
        actions.append({
            "action": "tender_signal",
            "cmd": None,
            "why": f"research queue {r_rem} below tender threshold",
            "condition": "queue_low",
        })

    if hour >= 11:
        actions.append({
            "action": "schedule_note",
            "cmd": None,
            "why": "post-11:00 glm free window active on Lite",
            "condition": "schedule_window",
        })

    if not actions:
        actions.append({
            "action": "idle",
            "cmd": None,
            "why": "all clear, waiting for wants or next cycle",
            "condition": "all_clear",
        })
    return actions


def record(actions: list[dict]) -> None:
    row = {"schema": "grounding_chain.v1",
           "ts": datetime.now(timezone.utc).isoformat(),
           "actions": actions}
    with CHAIN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="grounding-chain")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval", type=int, default=60)
    a = ap.parse_args(argv)

    while True:
        actions = evaluate()
        record(actions)
        for act in actions:
            why = act.get("why", "")
            name = act.get("action", "?")
            if act.get("cmd") is None or a.dry:
                print(f"[grounding] {name}: {why}")
                continue
            print(f"[grounding] firing {name}: {why}")
            try:
                subprocess.run(act["cmd"], cwd=str(ROOT), timeout=900,
                               shell=False)
            except Exception as e:
                print(f"[grounding] fire failed: {e}")
        if a.once:
            break
        time.sleep(a.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
