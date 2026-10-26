"""lawlog - the law gate's memory: one jsonl row per block, plus a weekly tally.

Cause (2026-10-03, watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md, change 3):
tools/seat_law_gate.py blocked tool calls but kept no record, so violations
were never metered ("blocks per law per week" had no baseline).

Writer: record(law, tool, path, reason, hook) appends to
memory/runs/lawlog.jsonl. Rows carry ts, law id, tool, hook, path, and a short
reason. Never the command text or payload (no secrets ride the log). The writer
never raises: a broken log must not break the gate (fail-open house rule).

Reader (CLI, read-only):
    .venv/Scripts/python.exe tools/lawlog.py            # blocks per law per ISO week
    .venv/Scripts/python.exe tools/lawlog.py --weeks 4  # last 4 weeks only
    .venv/Scripts/python.exe tools/lawlog.py --log PATH # another log file
Prints "0 blocks" when the log is missing or empty. No daemon, no schedule.
LAWLOG_PATH env var overrides the log path (tests).
"""
import argparse
import datetime as dt
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "memory" / "runs" / "lawlog.jsonl"
REASON_CAP = 160
PATH_CAP = 200


def log_path() -> Path:
    env = os.environ.get("LAWLOG_PATH")
    return Path(env) if env else DEFAULT_LOG


def _short_path(path: str) -> str:
    p = str(path or "").replace("\\", "/")
    root = str(ROOT).replace("\\", "/")
    if p.lower().startswith(root.lower() + "/"):
        p = p[len(root) + 1:]
    return p[:PATH_CAP]


def record(law: str, tool: str, path: str = "", reason: str = "", hook: str = "") -> bool:
    """Append one block row. Returns True when written, False on any failure."""
    row = {
        "ts": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "law": str(law)[:60],
        "tool": str(tool)[:40],
        "hook": str(hook)[:40],
        "path": _short_path(path),
        "reason": " ".join(str(reason).split())[:REASON_CAP],
    }
    try:
        target = log_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
        return True
    except Exception:
        return False


def load(path: Path) -> list:
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            rows.append({"ts": "", "law": "UNPARSEABLE_ROW"})
    return rows


def iso_week(ts: str) -> str:
    try:
        d = dt.datetime.strptime(ts[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return "????-W??"
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def report(rows: list, weeks: int = 0) -> str:
    if not rows:
        return "0 blocks"
    table = defaultdict(Counter)
    for r in rows:
        table[iso_week(str(r.get("ts", "")))][str(r.get("law", "?"))] += 1
    keys = sorted(table)
    if weeks > 0:
        keys = keys[-weeks:]
    total = sum(sum(table[k].values()) for k in keys)
    out = [f"{total} blocks in {len(keys)} week(s)", "week      law                              blocks"]
    for k in keys:
        for law, n in sorted(table[k].items(), key=lambda kv: (-kv[1], kv[0])):
            out.append(f"{k:<9} {law:<32} {n:>6}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="blocks per law per week from the law gate log")
    ap.add_argument("--log", default="", help="log path (default memory/runs/lawlog.jsonl)")
    ap.add_argument("--weeks", type=int, default=0, help="only the last N weeks with blocks")
    a = ap.parse_args(argv)
    path = Path(a.log) if a.log else log_path()
    rows = load(path)
    print(report(rows, a.weeks))
    if not rows:
        print(f"(log empty or missing: {path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
