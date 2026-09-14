#!/usr/bin/env python3
"""Self-test for scripts/ack_reaper.py — fixture tree, subprocess runs, exit 0 always."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REAPER = os.path.join(os.path.dirname(HERE), "scripts", "ack_reaper.py")

NOW = "2026-09-12T01:00:00+00:00"
STALE_ACK = "2026-09-10T12:00:00+00:00"        # 37h before NOW -> due
FRESH_ACK = "2026-09-11T20:00:00+00:00"        # 5h before NOW  -> quiet


def build_fixture(root: str) -> dict[str, str]:
    os.makedirs(os.path.join(root, "logs"), exist_ok=True)
    os.makedirs(os.path.join(root, "state"), exist_ok=True)
    alert_lines = [
        {"ts": "2026-09-11T00:00:00+00:00", "type": "signature_pressure",
         "sig": "run_shell:stale1", "count": 500, "tool": "run_shell",
         "sample": "stale ack, must re-scream"},
        {"ts": "2026-09-11T18:00:00+00:00", "type": "signature_pressure",
         "sig": "run_shell:fresh1", "count": 10, "tool": "run_shell",
         "sample": "freshly acked, must stay quiet"},
        {"ts": "2026-09-11T23:30:00+00:00", "type": "threshold", "sig": "_:neverseen",
         "count": 100, "tool": None, "sample": "no marker at all"},
        "not json at all\n",
    ]
    with open(os.path.join(root, "logs", "failure_kb_alerts.jsonl"), "w",
              encoding="utf-8") as fh:
        for row in alert_lines:
            fh.write(row if isinstance(row, str) else json.dumps(row) + "\n")
    markers = {
        "2026-09-11T00:00:00+00:00|run_shell:stale1": STALE_ACK,
        "2026-09-11T18:00:00+00:00|run_shell:fresh1": FRESH_ACK,
    }
    with open(os.path.join(root, "state", "failure_kb_alerts_read.json"), "w",
              encoding="utf-8") as fh:
        json.dump(markers, fh)
    # hold placed 30h ago with 24h ttl -> due
    with open(os.path.join(root, "state", "f2p_hold.json"), "w", encoding="utf-8") as fh:
        json.dump({"created": "2026-09-10T19:00:00+00:00", "ttl_hours": 24,
                   "reason": "fixture"}, fh)
    # hold placed 2h ago with 24h ttl -> quiet
    with open(os.path.join(root, "state", "lane_hold.json"), "w", encoding="utf-8") as fh:
        json.dump({"created": "2026-09-11T23:00:00+00:00", "ttl_hours": 24}, fh)
    # unreadable hold -> due (safest)
    with open(os.path.join(root, "state", "broken_hold.json"), "w",
              encoding="utf-8") as fh:
        fh.write("{oops")
    return {"queue": os.path.join(root, "watch", "inbox", "ACK_REAPER_QUEUE.md"),
            "read": os.path.join(root, "state", "failure_kb_alerts_read.json"),
            "hold_ledger": os.path.join(root, "state", "ack_reaper_holds.json")}


def run(root: str, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, REAPER, "--root", root, "--now", NOW, *extra],
        capture_output=True, text=True, timeout=60)


def main() -> int:
    fails: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        print(("PASS " if cond else "FAIL ") + name + ((": " + detail) if detail and not cond else ""))
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory() as root:
        paths = build_fixture(root)
        r1 = run(root)
        out1 = r1.stdout + r1.stderr
        check("exit 0 on first run", r1.returncode == 0, out1)
        check("screams stale alert", "run_shell:stale1" in out1)
        check("screams never-acked alert", "_:neverseen" in out1)
        check("stays quiet on fresh alert", "run_shell:fresh1" not in out1)
        check("screams over-ttl hold", "f2p_hold.json" in out1)
        check("screams unparseable hold", "broken_hold.json" in out1)
        check("quiet on fresh hold", "lane_hold.json" not in out1)
        check("loud stdout says SCREAM", "SCREAM" in out1)
        check("queue file written", os.path.exists(paths["queue"]))
        q1 = open(paths["queue"], encoding="utf-8").read() if os.path.exists(paths["queue"]) else ""
        check("queue has 4 rows",
              sum(1 for ln in q1.splitlines() if ln.startswith("| 2026")) == 4, q1)
        read_now = json.load(open(paths["read"], encoding="utf-8"))
        check("stale marker advanced", read_now.get(
            "2026-09-11T00:00:00+00:00|run_shell:stale1", "").startswith("2026-09-12"))
        check("fresh marker untouched", read_now.get(
            "2026-09-11T18:00:00+00:00|run_shell:fresh1") == FRESH_ACK)
        ledger = json.load(open(paths["hold_ledger"], encoding="utf-8"))
        check("hold ledger advanced", set(ledger) == {"f2p_hold.json", "broken_hold.json"})

        # idempotency: second run 10 minutes later finds nothing new
        r2 = run(root, "--now", "2026-09-12T01:10:00+00:00")
        out2 = r2.stdout + r2.stderr
        q2 = open(paths["queue"], encoding="utf-8").read()
        check("exit 0 on second run", r2.returncode == 0, out2)
        check("second run quiet", "SCREAM" not in out2, out2)
        check("queue unchanged (idempotent)", q2 == q1)
        check("second-run quiet line", "quiet" in out2)

        # dry-run: screams but writes nothing
        with tempfile.TemporaryDirectory() as root2:
            build_fixture(root2)
            r3 = run(root2, "--dry-run")
            out3 = r3.stdout + r3.stderr
            check("dry-run exit 0 and screams",
                  r3.returncode == 0 and "SCREAM" in out3, out3)
            check("dry-run writes no queue",
                  not os.path.exists(os.path.join(root2, "watch")))

        # hostile inputs: missing files + garbage markers must still exit 0
        with tempfile.TemporaryDirectory() as root3:
            r4 = run(root3)
            check("exit 0 with empty tree", r4.returncode == 0, r4.stdout + r4.stderr)
            os.makedirs(os.path.join(root3, "state"), exist_ok=True)
            with open(os.path.join(root3, "state", "failure_kb_alerts_read.json"),
                      "w", encoding="utf-8") as fh:
                fh.write("]garbage[")
            r5 = run(root3)
            check("exit 0 with garbage marker file", r5.returncode == 0, r5.stdout)

    print("\n%s (%d checks)" % ("ALL PASS" if not fails else "FAILED: " + ", ".join(fails),
                                21))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
