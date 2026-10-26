#!/usr/bin/env python3
"""B2-359 probe 3: focused byte-sha confirmations on the seven suspect chains.

Each probe: snapshot target sha/count, run the single test file under the
repo venv, snapshot again, print BEFORE/AFTER deltas. No marker guessing:
the sha and the row count are the verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PY = ROOT / ".venv" / "Scripts" / "python.exe"


def sha(rel):
    p = ROOT / rel
    if not p.exists():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def run(file):
    r = subprocess.run([str(PY), "-m", "pytest", file, "-q", "--no-header",
                        "-p", "no:cacheprovider", "--rootdir", str(ROOT)],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    tail = (r.stdout or "").strip().splitlines()
    return r.returncode, tail[-1] if tail else ""


def before_after(label, file, snap_fn):
    b = snap_fn()
    code, summary = run(file)
    a = snap_fn()
    moved = b != a
    print(f"### {label}")
    print(f"    run: exit={code} {summary}")
    print(f"    before: {json.dumps(b, default=str)[:400]}")
    print(f"    after:  {json.dumps(a, default=str)[:400]}")
    print(f"    MOVED: {moved}")
    sys.stdout.flush()
    return {"label": label, "file": file, "before": b, "after": a,
            "moved": moved, "exit": code, "summary": summary}


def n_handoff():
    d = ROOT / "queue" / "handoff"
    f = sorted(d.glob("cloud-*.json"), key=lambda p: p.stat().st_mtime)
    pytest_src = [p.name for p in d.glob("*.json")
                  if "pytest" in p.read_text(encoding="utf-8", errors="replace")]
    return {"n_cloud": len(f), "newest": f[-1].name if f else None,
            "n_pytest_source": len(pytest_src)}


def trail_lines():
    p = ROOT / "memory" / "runs" / "seat_registry_trail.jsonl"
    return {"lines": sum(1 for _ in open(p, encoding="utf-8", errors="replace"))}


def state_flags():
    return {"mag_power_off_exists": (ROOT / "state" / "mag_power.off").exists()}


def inbox_state():
    dec = ROOT / "memory" / "decisions_log.jsonl"
    inb = ROOT / "memory" / "operator_inbox.json"
    pending = None
    try:
        data = json.loads(inb.read_text(encoding="utf-8"))
        pending = [i.get("id") for i in data.get("pending", []) if i.get("status") != "processed"]
    except Exception as e:
        pending = f"err:{e}"
    return {"decisions_lines": sum(1 for _ in open(dec, encoding="utf-8", errors="replace")),
            "operator_inbox_sha": sha("memory/operator_inbox.json"),
            "pending_ids": pending}


def desk():
    return {"agent_desk_sha": sha("memory/working/agent_desk.md")}


def queue_count():
    n = 0
    for dp, dn, fn in os.walk(ROOT / "queue"):
        n += len(fn)
    return {"queue_files": n}


def daily_md():
    return {"sha": sha("memory/improve/daily/2026-09-26-behavioral.md")}


def main():
    results = []
    results.append(before_after("improve_loop -> queue/handoff", "tests/test_improve_loop.py", n_handoff))
    results.append(before_after("seat_registry -> seat trail", "tests/test_seat_registry.py", trail_lines))
    results.append(before_after("lifecycle -> state latest", "tests/test_lifecycle.py",
                                lambda: {"lifecycle": sha("state/lifecycle_latest.json"),
                                         "stacks": sha("state/temperature_stacks_latest.json")}))
    results.append(before_after("t1_steering -> operator inbox drain", "tests/test_t1_steering.py", inbox_state))
    results.append(before_after("repack_integration -> operator inbox drain", "tests/test_repack_integration.py", inbox_state))
    results.append(before_after("power -> mag_power.off", "tests/test_power.py", state_flags))
    results.append(before_after("desk_baseline_probe -> live desk", "tests/test_desk_baseline_probe.py", desk))
    results.append(before_after("steward -> queue/", "tests/test_steward_queue_has_goal.py", queue_count))
    results.append(before_after("growth_cycle -> daily md (run 1)", "tests/test_growth_cycle.py", daily_md))
    results.append(before_after("growth_cycle -> daily md (run 2, back-to-back)", "tests/test_growth_cycle.py", daily_md))
    out = Path(__file__).with_name("B2_359_confirm_results.json")
    out.write_text(json.dumps(results, indent=1, default=str), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
