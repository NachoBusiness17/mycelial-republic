#!/usr/bin/env python3
"""steer_47 — water-integrator steering for the 4.7 dogfood session (2026-08-28).

The model is water; the hooks are the channels; the geometry computes.
4.7 is too weak to remember the task — so the channels remember FOR it.

Marker-gated: steering fires ONLY while state/vast/dogfood_47.active exists
(temporary guardrails for the experiment; removed after grading — normal
sessions pass untouched).

Reads hook JSON on stdin. Exit 0 = allow. Exit 2 = block + steer message.
A broken channel must never jam the water: internal errors exit 0.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
MARKER = HERE / "state" / "vast" / "dogfood_47.active"
REPORT = HERE / "memory" / "runs" / "harness" / "first_47_report.md"

# the task's three instruments — everything else is wandering
ALLOWED = re.compile(
    r"(timeline\.py|event_stream\.py( verify)?|lattice_check\.py|"
    r"first_47_report|cat |ls |head |tail |wc )"
)

STEER = ("STEER (water integrator): stay in the channels. Allowed right now: "
         "python state/vast/timeline.py · python state/vast/event_stream.py verify · "
         "python scripts/lattice_check.py · reading files · writing first_47_report.md. "
         "The task: run the timeline, verify the chain, read the lattice, "
         "write memory/runs/harness/first_47_report.md (10 lines, outcome first).")


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    if not MARKER.exists():
        sys.exit(0)  # experiment not armed — pass everything

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Stop":
        if REPORT.exists():
            print(json.dumps({"hookEventName": "Stop",
                              "additionalContext":
                                  "Dogfood report detected — grade pending. End cleanly."}))
        else:
            print(json.dumps({"hookEventName": "Stop",
                              "additionalContext":
                                  "TASK INCOMPLETE: memory/runs/harness/first_47_report.md "
                                  "does not exist. Write the 10-line report before ending: "
                                  "outcome first, divergence number, G1 status, one insight."}))
        sys.exit(0)

    if tool == "Bash":
        cmd = str(ti.get("command") or "")
        if ALLOWED.search(cmd):
            sys.exit(0)
        print(json.dumps({"hookEventName": "PreToolUse",
                          "permissionDecision": "deny",
                          "permissionDecisionReason": STEER}))
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
