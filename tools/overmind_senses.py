"""overmind_senses - the read layer (OVERMIND-2 gap 1's adapter leg, 2026-10-01).

Spec: watch/inbox/model_garden/OVERMIND_THEORY.md sec 1.1 + 2.2 step 1.
DFHack law: read the memory, don't interview the dwarf. Every sense is a
deterministic, $0, stdlib-only read; the model never invents state, it
reads rendered state. Lane order OVERMIND-2 names the four surfaces:
  - sense_sha_tail     git changed-path tail (SWARM_1's drift gate)
  - sense_driver_beat  state/shared_activity.jsonl rows since run start
  - sense_queue        queue/todo.md open items + handoff + wait_human + index
  - sense_landed       watch/inbox outputs newer than the run start
Missing surfaces degrade to honest zeros/missing flags, never raise.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SHARED_ACTIVITY = ROOT / "state" / "shared_activity.jsonl"
QUEUE_TODO = ROOT / "queue" / "todo.md"
QUEUE_HANDOFF = ROOT / "queue" / "handoff"
QUEUE_WAIT_HUMAN = ROOT / "queue" / "wait_human.md"
QUEUE_INDEX = ROOT / "queue" / "queue_index.jsonl"
INBOX_ROOT = ROOT / "watch" / "inbox"


def _parse_ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def sense_sha_tail(tail_n: int = 12) -> dict:
    """The drift gate sense: git changed-path tail + head commit."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"], cwd=str(ROOT),
            capture_output=True, text=True, timeout=60).stdout.splitlines()
    except (OSError, subprocess.SubprocessError):
        out = []
    paths = []
    for line in out:
        p = line[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ")[-1]
        paths.append(p)
    try:
        head = subprocess.run(
            ["git", "log", "-1", "--format=%h %s"], cwd=str(ROOT),
            capture_output=True, text=True, timeout=60).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        head = ""
    return {"changed_count": len(paths), "tail": paths[-tail_n:],
            "head_commit": head[:160]}


def sense_driver_beat(since_ts: str, path: Path | None = None,
                      tail_n: int = 6) -> dict:
    """The nerve-cord sense: shared_activity rows since the run started."""
    p = Path(path) if path else SHARED_ACTIVITY
    if not p.is_file():
        return {"missing": True, "rows_since_run_start": 0, "actors": {},
                "statuses": {}, "tail": []}
    since = _parse_ts(since_ts)
    rows, actors, statuses, tail = 0, {}, {}, []
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = _parse_ts(row.get("ts", ""))
        if since and ts and ts < since:
            continue
        rows += 1
        actor = row.get("actor") or "?"
        actors[actor] = actors.get(actor, 0) + 1
        st = row.get("status") or "?"
        statuses[st] = statuses.get(st, 0) + 1
        tail.append({"ts": row.get("ts"), "actor": row.get("actor"),
                     "status": st,
                     "goal": str(row.get("goal") or "")[:140],
                     "detail": str(row.get("detail") or "")[:140]})
    return {"missing": False, "rows_since_run_start": rows,
            "actors": actors, "statuses": statuses, "tail": tail[-tail_n:]}


def sense_queue(todo: Path | None = None, handoff: Path | None = None,
                wait_human: Path | None = None,
                queue_index: Path | None = None) -> dict:
    """The pressure sense: queue surfaces (todo open items, handoff count,
    wait_human size, index rows)."""
    todo_p = Path(todo) if todo else QUEUE_TODO
    handoff_p = Path(handoff) if handoff else QUEUE_HANDOFF
    wh_p = Path(wait_human) if wait_human else QUEUE_WAIT_HUMAN
    qi_p = Path(queue_index) if queue_index else QUEUE_INDEX
    missing = [str(p) for p in (todo_p, handoff_p, wh_p, qi_p)
               if not p.exists()]
    text = todo_p.read_text(encoding="utf-8", errors="replace") \
        if todo_p.is_file() else ""
    open_items = [l for l in text.splitlines() if l.strip().startswith("- [ ]")]
    handoff_n = len(list(handoff_p.glob("*.json"))) if handoff_p.is_dir() else 0
    wh_bytes = wh_p.stat().st_size if wh_p.is_file() else 0
    qi_rows = 0
    if qi_p.is_file():
        qi_rows = sum(1 for l in
                      qi_p.read_text(encoding="utf-8",
                                     errors="replace").splitlines()
                      if l.strip())
    return {"todo_open": len(open_items),
            "todo_open_tail": [l.strip()[:160] for l in open_items[-4:]],
            "handoff_items": handoff_n,
            "wait_human_bytes": wh_bytes,
            "queue_index_rows": qi_rows,
            "missing_inputs": missing}


def sense_landed(since_ts: str | None, root: Path | None = None,
                 cap: int = 20000, tail_n: int = 10) -> dict:
    """The output sense: files landed on the shared inbox since the run
    started (mtime truth)."""
    r = Path(root) if root else INBOX_ROOT
    since_epoch = 0.0
    if since_ts:
        dt = _parse_ts(since_ts)
        if dt:
            since_epoch = dt.timestamp()
    hits, n = [], 0
    if r.is_dir():
        for p in r.rglob("*"):
            n += 1
            if n > cap:
                break
            try:
                if p.is_file() and p.stat().st_mtime >= since_epoch:
                    hits.append(p)
            except OSError:
                continue
    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return {"count": len(hits),
            "tail": [str(p.relative_to(r)) for p in hits[:tail_n]],
            "scanned": n}


def collect_senses(run_start_ts: str) -> dict:
    return {"git": sense_sha_tail(),
            "beat": sense_driver_beat(run_start_ts),
            "queue": sense_queue(),
            "landed": sense_landed(run_start_ts)}
