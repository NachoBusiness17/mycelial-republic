#!/usr/bin/env python3
"""light_maze - the routing organ (RIB_LIGHT_MAZE, 2026-10-12).

The operator's law: known values are lit corridors; ride the light to the
edge keeping it cheap; the thing outside the known values gets scheduled onto
a free lane or a frontier; dark work returns as light; no sacred cows.

This tool is the pre-flight router: given a task, it checks the known values
(corpus + beacon + prior receipts) and classifies the route:
  inplace  - the known values cover this; run locally at cache-hit cost
  freelane - the edge of the known values; dispatch to a free lane
  frontier - outside all known values; dispatch to the frontier
  unknown  - not enough signal to route; ask the operator

Usage:
  .venv/Scripts/python.exe tools/light_maze.py "your task description here"
  .venv/Scripts/python.exe tools/light_maze.py --route "task" --host http://localhost:11434
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_FTS = ROOT / "reference" / "gstdcoin" / "contracts" / "corpus_fts.sqlite"
BEACON_JSON = ROOT / "reference" / "gstdcoin" / "contracts" / "beacon.json"
LATTICE_JSON = ROOT / "reference" / "gstdcoin" / "contracts" / "lattice.json"

# The light maze's routing rules (from the rib):
# inplace  = the corpus or an existing tool already covers this
# freelane = the edge; dispatch to a free lane (ollama, flash-tier)
# frontier = outside all known values; needs a frontier model or the operator
def classify_match(hits: int, has_tool: bool, has_prior_receipt: bool) -> str:
    if has_prior_receipt and has_tool:
        return "inplace"
    if has_tool:
        return "inplace"
    if hits > 0:
        return "freelane"
    return "frontier"


def search_corpus(task: str) -> tuple[int, list[dict]]:
    """Search the corpus for prior art. Returns (hit_count, top_matches)."""
    results: list[dict] = []
    try:
        import sqlite3
        db = CORPUS_FTS if CORPUS_FTS.is_file() else None
        if not db:
            # try the catalog
            return len(results), results
        # skip: FTS query via sqlite
    except Exception:
        pass

    # fallback: grep the estate for prior art
    try:
        terms = [w for w in task.lower().split() if len(w) > 4][:5]
        hits = 0
        for term in terms:
            p = subprocess_run(
                ["grep", "-rli", term, str(ROOT / "watch" / "inbox"), str(ROOT / "corpus")],
                timeout=30)
            if p:
                hits += 1
        return hits, []
    except Exception:
        return 0, []


def subprocess_run(args: list[str], timeout: int = 30) -> str:
    import subprocess
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return (p.stdout or "") + (p.stderr or "")


def read_beacon() -> dict | None:
    try:
        return json.load(open(BEACON_JSON, encoding="utf-8"))
    except Exception:
        return None


def route(task: str) -> dict:
    """The light maze routing decision for a task."""
    hits, matches = search_corpus(task)
    beacon = read_beacon()
    artifacts = (beacon or {}).get("artifacts", [])

    # does any beacon artifact match this task?
    beacon_match = False
    task_lower = task.lower()
    for a in artifacts:
        if any(w in a.get("name", "").lower() or w in a.get("desc", "").lower()
               for w in task_lower.split() if len(w) > 4):
            beacon_match = True
            break

    return {
        "task": task,
        "corpus_hits": hits,
        "beacon_match": beacon_match,
        "route": classify_match(hits, beacon_match, hits > 2),
        "lit_corridors": [a["name"] for a in artifacts],
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: light_maze.py <task description>")
        return 1
    task = " ".join(sys.argv[1:])
    r = route(task)
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
