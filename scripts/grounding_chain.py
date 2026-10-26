"""grounding_chain -- the wiring between the fleet's chained skills.

The fleet's systems are chained skills going through a series of events. What's
missing: the GROUNDING WIRE between links, a controller that reads the ledger
state, computes what fires next from evidence, fires it, and appends a grounding
row explaining why.

GROUNDING PRINCIPLE: the state of the system IS the evidence. The next action
is determined by what the evidence says, not by a clock or a hope.

All commands are STATIC lists (no computed values reach the shell). The drivers
themselves handle batching and lock checking.

Rows are appended AFTER the cycle's fires settle: every fired action carries
exit_code (int; None on timeout or launch failure, with fire_error naming it)
plus state_before/state_after (lane remaining + lock age read around the child).
A hard kill of the chain itself mid-fire leaves no row for that cycle; the
drivers' own state and locks stay ground truth.

RUN:  .venv\\Scripts\\python.exe scripts\\grounding_chain.py [--dry] [--once]
Schema: grounding_chain.v1 (additive outcome fields, B2-56 2026-09-26)
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


def lane_state(name: str) -> dict:
    """Truth for one fired lane: remaining work + lock age, read from bytes."""
    if name == "research":
        return {"remaining": queue_remaining(),
                "lock_age_s": lock_age(BASE / "run.lock")}
    if name == "build":
        return {"remaining": build_remaining(),
                "lock_age_s": lock_age(BASE / "build_lane" / "run.lock")}
    return {}


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
    # FIX 2026-09-26 (B2-290). CAUSE: BASE/CHAIN_LOG were import-time constants
    # only, so the B2-56 returncode fire path had no end-to-end proof against a
    # real child and scratch state -- the existing tests monkeypatched the
    # module, which cannot catch a production write to the real log.
    # EVIDENCE: tests/test_grounding_chain.py held only fake-child tests; the
    # live-dead-child proof below is the first run that executes a real
    # subprocess against an injected scratch base and asserts the production
    # grounding_chain.jsonl is byte-untouched.
    # FIX: --base/--log args plus GROUNDING_CHAIN_BASE/GROUNDING_CHAIN_LOG env
    # rebind the module globals before the loop, so the whole chain (evaluate,
    # lane_state, record) runs on injected state.
    ap.add_argument("--base", default=None,
                    help="inject the lane base dir (scratch state for tests)")
    ap.add_argument("--log", default=None,
                    help="inject the chain log file (scratch log for tests)")
    a = ap.parse_args(argv)

    global BASE, CHAIN_LOG
    import os
    if a.base or os.environ.get("GROUNDING_CHAIN_BASE"):
        BASE = Path(a.base or os.environ["GROUNDING_CHAIN_BASE"])
    if a.log or os.environ.get("GROUNDING_CHAIN_LOG"):
        CHAIN_LOG = Path(a.log or os.environ["GROUNDING_CHAIN_LOG"])

    while True:
        actions = evaluate()
        for act in actions:
            why = act.get("why", "")
            name = act.get("action", "?")
            if act.get("cmd") is None or a.dry:
                print(f"[grounding] {name}: {why}")
                continue
            print(f"[grounding] firing {name}: {why}")
            # FIX 2026-09-26 (B2-56). CAUSE: the child returncode was discarded
            # here and the WHY row was appended before any fire, so a driver
            # that died mid-fire still left a "firing" row over stranded state.
            # EVIDENCE: the 2026-09-26 KeyError fire (union_fullsend_day.py
            # SYSTEMS missing attacker/builder styles) crashed the child,
            # stranded run.lock + state.json, while the 11:28:14Z
            # grounding_chain.jsonl row claimed the fire;
            # watch/inbox/burn_wave_20260926/B2_07_grounding_20260926.md.
            # FIX: the row is appended after the fires and each fired action
            # records the child exit code (or fire_error) plus the lane state
            # read before and after the child exited.
            act["state_before"] = lane_state(name)
            try:
                proc = subprocess.run(act["cmd"], cwd=str(ROOT), timeout=900,
                                      shell=False)
                act["exit_code"] = proc.returncode
                if proc.returncode != 0:
                    print(f"[grounding] fire failed: {name} exit "
                          f"{proc.returncode}")
            except subprocess.TimeoutExpired:
                act["exit_code"] = None
                act["fire_error"] = "timeout after 900s"
                print(f"[grounding] fire failed: {name} timeout after 900s")
            except Exception as e:
                act["exit_code"] = None
                act["fire_error"] = repr(e)
                print(f"[grounding] fire failed: {e}")
            act["state_after"] = lane_state(name)
        record(actions)
        if a.once:
            break
        time.sleep(a.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
