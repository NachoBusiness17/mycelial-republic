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
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# R1 repair (G2 lane g2-i10-light-maze, 2026-10-18): the old constant pointed at
# reference/gstdcoin/contracts/corpus_fts.sqlite, which does not exist on disk,
# and the FTS branch below it was a literal "# skip" stub, so the strongest
# known-values probe never fired. The real index is catalog/catalog_fts.sqlite
# (454 MB, verified 2026-10-18), written only by tools/corpus_fts_rebuild.py
# per the B2-465 corpus-FTS law in AGENTS.md. Evidence: memory/runs/genetic_burn/
# 20261018/G0/lanes/g24-open-flanks.md (R1) and the 2026-10-18 on-disk probe.
CORPUS_FTS = ROOT / "catalog" / "catalog_fts.sqlite"
BEACON_JSON = ROOT / "reference" / "gstdcoin" / "contracts" / "beacon.json"
LATTICE_JSON = ROOT / "reference" / "gstdcoin" / "contracts" / "lattice.json"

# R5 (G0 lane g24 spec): every decision appends here so the rib falsifier
# (lit-area growth per token vs blind premium routing) becomes meterable.
# MAG_LIGHT_MAZE_LEDGER overrides the path (tests and sandboxes use this);
# a failed write never blocks the route - the router advises, never blocks.
DEFAULT_LEDGER = ROOT / "memory" / "runs" / "light_maze" / "decisions.jsonl"

# Corpus signal below this many hits is too thin to route on: the caller gets
# "unknown" (ask the operator) instead of a confident free-lane dispatch.
THIN_SIGNAL_HITS = 3


def ledger_path() -> Path:
    """Resolved decision-ledger path (env override honored at call time)."""
    return Path(os.environ.get("MAG_LIGHT_MAZE_LEDGER") or DEFAULT_LEDGER)


# The light maze's routing rules (from the rib):
# inplace  = the corpus or an existing tool already covers this
# freelane = the edge; dispatch to a free lane (ollama, flash-tier)
# frontier = outside all known values; needs a frontier model or the operator
# unknown  = signal too thin to route; ask the operator
def classify_match(hits: int, has_tool: bool, has_prior_receipt: bool) -> str:
    """Pure route ladder over the probes (testable truth table).

    inplace  - a known organ/tool/beacon artifact covers the task
    freelane - corpus-lit (or prior-receipted) but uncovered: free lane
    frontier - zero signal in all probes
    unknown  - thin corpus signal, no coverage: ask the operator
    """
    if hits < 0:
        hits = 0
    if has_tool:
        return "inplace"
    if has_prior_receipt:
        # PROXY (kept per G2 lane order, 2026-10-18): the caller passes
        # hits > 2 as has_prior_receipt, a corpus-density proxy, not a real
        # receipt probe. Upgrade path (G0 lane g24 spec R2): probe the
        # watch/inbox/ receipt filenames/stems for the task terms and pass
        # that boolean instead; the classify signature already accepts it.
        # Neither the rib nor this file's probes name a concrete receipt
        # check today, so the proxy rides marked, not silent.
        return "freelane"
    if hits == 0:
        return "frontier"
    if hits < THIN_SIGNAL_HITS:
        return "unknown"
    return "freelane"


def _task_terms(task: str) -> list[str]:
    return [w for w in task.lower().split() if len(w) > 4][:5]


def search_corpus(task: str) -> tuple[int, list[dict]]:
    """Search the corpus for prior art. Returns (hit_count, top_matches)."""
    # R1: real FTS5 MATCH against catalog/catalog_fts.sqlite, opened
    # read-only so this tool can never race the sanctioned rebuild writer.
    try:
        if CORPUS_FTS.is_file():
            terms = _task_terms(task)
            if terms:
                match_q = " OR ".join('"%s"' % t.replace('"', '""') for t in terms)
                con = sqlite3.connect("file:%s?mode=ro" % CORPUS_FTS.as_posix(),
                                      uri=True)
                try:
                    total = con.execute(
                        "SELECT count(*) FROM corpus WHERE corpus MATCH ?",
                        (match_q,)).fetchone()[0]
                    rows = con.execute(
                        "SELECT path, title FROM corpus WHERE corpus MATCH ?"
                        " LIMIT 20", (match_q,)).fetchall()
                finally:
                    con.close()
                return int(total), [{"path": p, "title": t} for p, t in rows]
    except Exception:
        pass

    # fallback: grep the estate for prior art (missing/stale index days)
    try:
        terms = _task_terms(task)
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
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return (p.stdout or "") + (p.stderr or "")


def read_beacon() -> dict | None:
    try:
        return json.load(open(BEACON_JSON, encoding="utf-8"))
    except Exception:
        return None


def read_lit_map() -> list[str]:
    """R4: optional lit-map read (hot weights, cached envs).

    The rib cites scripts/hot-lattice.ts as the VRAM lit map; that file does
    not exist anywhere in the repo, so the lit map rides an env-pointed JSON
    file: MAG_LIT_MAP=/path/to/lit.json holding a list of lit names (or an
    object with a "lit" list). Absent or unreadable file = no lit map; the
    router then runs on corpus + beacon + receipts only. Never raises.
    """
    env = os.environ.get("MAG_LIT_MAP")
    if not env:
        return []
    try:
        data = json.load(open(env, encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, list):
        return [str(x) for x in data]
    if isinstance(data, dict):
        return [str(x) for x in data.get("lit", [])]
    return []


def append_ledger(record: dict) -> Path | None:
    """R5: append one decision row to the JSONL ledger. Never raises."""
    try:
        path = ledger_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
        return path
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

    # R4: a lit-map name hit is coverage by a known value (hot weights,
    # cached envs) - it counts like an organ/tool hit for the route ladder.
    lit_names = read_lit_map()
    lit_match = any(w in name.lower()
                    for name in lit_names
                    for w in task_lower.split() if len(w) > 4)

    # prior-receipt proxy: hits > 2 stands in for a real receipt probe
    # (see the PROXY comment in classify_match for the upgrade path).
    receipt_proxy = hits > 2

    route_name = classify_match(hits, beacon_match or lit_match, receipt_proxy)

    decision = {
        "task": task,
        "corpus_hits": hits,
        "beacon_match": beacon_match,
        "route": route_name,
        "lit_corridors": [a["name"] for a in artifacts] + lit_names,
        "evidence": {
            "corpus_hits": hits,
            "corpus_top": matches[:5],
            "beacon_match": beacon_match,
            "lit_map_match": lit_match,
            "receipt_proxy": receipt_proxy,
        },
        "decision_ledger_path": str(ledger_path()),
    }
    append_ledger({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task": task,
        "route": route_name,
        "evidence": decision["evidence"],
    })
    return decision


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
