"""Brief reaper: ingest watch/inbox *BRIEFS*.md boards into the stealth
work queue (Mickey17 W1, 2026-09-29).

Problem (wave ledger return 15, watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md):
all 10 FL briefs sat armed on FREE_LANE_BRIEFS.md, zero fired, because
tools/stealth_driver.py consumes only JSONL rows in
state/fuel/stealth_work_queue.jsonl and .md boards are invisible to it;
the t_backlog topic counts the drained queue, not the live brief boards.

Fix: scan watch/inbox/**/*BRIEFS*.md, parse "## BRIEF FL-N - TITLE"
headers, emit queue rows in the exact shape the driver's own appenders
already write (id, ask, tier, status, queued_ts, depth, parent_id,
source), dedupe on the brief id as the stable key, append idempotently,
and print a backlog census of the live brief boards. This tool fixes
t_backlog's blindness by existing alongside it; stealth_driver.py is
untouched (read-only law).

The ask text is self-contained per estate law: board preamble (context
capsule) + brief title + brief body, so no conversation context is
needed downstream.

Usage:
    python tools/brief_reaper.py --dry     # census only, no writes
    python tools/brief_reaper.py           # append new rows
    python tools/brief_reaper.py --queue other.jsonl --root other/inbox
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = ROOT_DEFAULT = Path(__file__).resolve().parents[1]
QUEUE_DEFAULT = ROOT_DEFAULT / "state" / "fuel" / "stealth_work_queue.jsonl"
SCAN_ROOT_DEFAULT = ROOT_DEFAULT / "watch" / "inbox"

# Board discovery: any .md under the scan root whose name contains BRIEFS.
BOARD_GLOB = "*BRIEFS*.md"

# Brief header. Boards use "## BRIEF FL-1 <sep> Title" where <sep> is an
# em dash in the live board; accept hyphen too so hand-edited boards parse.
# Written as \u2014 escape so this file itself stays em-dash free (W1 law).
HEADER_RE = re.compile(
    r"^##\s+BRIEF\s+(?P<bid>\S+)\s+[-\u2014]\s+(?P<title>.+?)\s*$",
    re.MULTILINE,
)

# Keys every appended row carries. Mirrors the queued-row schema the
# driver's own appenders write (verified 2026-09-29 against live
# stealth_work_queue.jsonl rows): selffeed roots carry
# ask/depth/id/parent_id/queued_ts/selffed_ts/status/tier, impfeed rows
# carry id/ask/tier/status/queued_ts/source/depth. Brief rows follow the
# impfeed analog (external producer): queued_ts + source, no selffed_ts,
# because that stamp marks selffeed provenance and is operator property
# (stealth_driver.py line ~1034). parent_id None marks a root row.
ROW_KEYS = (
    "id", "ask", "tier", "status", "queued_ts",
    "depth", "parent_id", "source",
)

SOURCE_TAG = "brief_reaper"


def _now_iso() -> str:
    """UTC timestamp in the same isoformat shape the driver stamps."""
    return datetime.now(timezone.utc).isoformat()


def discover_boards(scan_root: Path) -> list[Path]:
    """All brief board files under scan_root, sorted for stable output."""
    if not scan_root.is_dir():
        return []
    return sorted(
        p for p in scan_root.rglob(BOARD_GLOB)
        if p.is_file()
    )


def parse_board(path: Path) -> dict:
    """Parse one board file into {"board", "preamble", "briefs": [...]}.

    preamble: text before the first brief header (the shared context
    capsule every brief inherits). briefs: [{"id", "title", "body"}].
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = list(HEADER_RE.finditer(text))
    preamble = text[: matches[0].start()].strip() if matches else text.strip()
    briefs = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end(): end].strip()
        briefs.append({"id": m.group("bid").strip(),
                       "title": m.group("title").strip(),
                       "body": body})
    return {"board": path.as_posix(), "preamble": preamble, "briefs": briefs}


def _load_queue_ids(queue_path: Path) -> set:
    """Every id ever present in the queue file (stable dedupe key:
    a brief already sensed or done must never be re-asked)."""
    ids = set()
    if not queue_path.is_file():
        return ids
    for line in queue_path.read_text(encoding="utf-8",
                                     errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rid = json.loads(line).get("id")
        except ValueError:
            continue
        if rid:
            ids.add(str(rid))
    return ids


def _row_for(board: dict, brief: dict) -> dict:
    """Queue row in the driver's queued-row schema (see ROW_KEYS).

    ask is self-contained: capsule + title + body. queued_ts is the TTL
    anchor the verify sweep reads first (queued_ts or selffed_ts);
    parent_id None marks a root (no parent ask).
    """
    ask = board["preamble"]
    if ask:
        ask += "\n\n"
    ask += f"BRIEF {brief['id']}: {brief['title']}\n\n{brief['body']}"
    return {
        "id": brief["id"],
        "ask": ask,
        "tier": "free",
        "status": "queued",
        "queued_ts": _now_iso(),
        "depth": 0,
        "parent_id": None,
        "source": SOURCE_TAG,
        "brief_file": board["board"],
        "brief_title": brief["title"],
    }


def reap(scan_root: Path, queue_path: Path, dry: bool = False) -> dict:
    """Scan boards, dedupe against queue ids, append new rows.

    Returns a census dict: boards, briefs (total headers found), armed
    (ids already in the queue), new (rows appended this run),
    appended (ids), rows_in_queue (post-run id count).
    """
    boards = [parse_board(p) for p in discover_boards(scan_root)]
    briefs = [b for bd in boards for b in bd["briefs"]]
    known = _load_queue_ids(queue_path)
    new_rows = []
    seen_here = set()
    for board in boards:
        for brief in board["briefs"]:
            bid = brief["id"]
            if bid in known or bid in seen_here:
                continue  # stable key: id already queued, never re-ask
            seen_here.add(bid)
            new_rows.append(_row_for(board, brief))
    if new_rows and not dry:
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        with queue_path.open("a", encoding="utf-8") as f:
            for row in new_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {
        "boards": len(boards),
        "briefs": len(briefs),
        "armed": sum(1 for b in briefs if b["id"] in known),
        "new": len(new_rows) if not dry else len(new_rows),
        "appended": [r["id"] for r in new_rows],
        "dry": dry,
        "rows_in_queue": len(known | seen_here),
    }


def _fmt_census(c: dict) -> str:
    mode = "DRY (no writes)" if c["dry"] else "APPENDED"
    lines = [
        f"brief_reaper census: boards={c['boards']} briefs={c['briefs']} "
        f"armed(in-queue)={c['armed']} new={c['new']} [{mode}]",
        f"queue ids after run: {c['rows_in_queue']}",
    ]
    if c["appended"]:
        lines.append("appended: " + ", ".join(c["appended"]))
    else:
        lines.append("appended: none (board fully armed or empty)")
    return "\n".join(lines)


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry", action="store_true",
                    help="census only; do not write to the queue")
    ap.add_argument("--root", type=Path, default=SCAN_ROOT_DEFAULT,
                    help=f"scan root (default {SCAN_ROOT_DEFAULT})")
    ap.add_argument("--queue", type=Path, default=QUEUE_DEFAULT,
                    help=f"queue jsonl (default {QUEUE_DEFAULT})")
    args = ap.parse_args(argv)
    census = reap(args.root, args.queue, dry=args.dry)
    print(_fmt_census(census))
    return 0


if __name__ == "__main__":
    sys.exit(main())
