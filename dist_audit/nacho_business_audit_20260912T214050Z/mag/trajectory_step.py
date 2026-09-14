"""trajectory_step — the base-freezing wrapper (trajectory spine build #1).

The tesuji (chord strike, 09-05): "freeze the base, let the workers report the
drift." Every Bash tool call in this harness becomes a TrajectoryStep row —
input + result + hash + timing — in ONE append-only stream. The Sep-20 vertical
(100 sealed steps/day) starts when this hook goes live, not on Sep 20.

Schema trajectory_step.v1 (schema_version MANDATORY — a write without it is
REJECTED; that is the drift killer from the trajectory_rib salon fold):

    {"schema_version": "trajectory_step.v1",
     "step_hash":  sha256(session|ts|command|result)[:16],
     "ts":         ISO-8601 UTC,
     "session_id": harness session or "unknown",
     "face":       "bash",
     "command":    the invoked command line,
     "result":     {exit: int|null, output_excerpt: str, truncated: bool}}

Stream: memory/trajectory/steps.jsonl — append-only, one row per line.
Louver law: the stream lives in the cage; the board shows counts, never payloads
beyond command lines already visible to the seat that ran them.

CLI:
    python -m mag.trajectory_step hook            # stdin JSON -> row (the hook door)
    python -m mag.trajectory_step verify          # recompute hashes, report orphans
    python -m mag.trajectory_step stats [n]       # today's steps + recent rows
    python -m mag.trajectory_step test-reject     # falsifier: schemaless write MUST fail

Falsifiers (fold order #1):
    COVERAGE  — a Bash call without a row kills the wrapper (check: stats during use).
    SCHEMA    — test-reject must show a schema_version-less write REFUSED.
    INTEGRITY — verify recomputes every step_hash; any mismatch = tampering or drift.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STREAM = REPO / "memory" / "trajectory" / "steps.jsonl"
SCHEMA_VERSION = "trajectory_step.v1"
EXCERPT_LIMIT = 400


def _utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def _excerpt(obj, limit: int = EXCERPT_LIMIT):
    if obj is None:
        return "", False
    text = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return text[:limit], len(text) > limit


def make_row(session_id: str, command: str, result, exit_code) -> dict:
    ts = _utcnow()
    excerpt, truncated = _excerpt(result)
    basis = "|".join([session_id, ts, command, excerpt])
    return {
        "schema_version": SCHEMA_VERSION,
        "step_hash": hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16],
        "ts": ts,
        "session_id": session_id or "unknown",
        "face": "bash",
        "command": command[:2000],
        "result": {"exit": exit_code, "output_excerpt": excerpt, "truncated": truncated},
    }


def append_row(row: dict) -> None:
    if not row.get("schema_version"):
        raise ValueError("SCHEMA REJECT: row without schema_version (drift killer)")
    if row["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"SCHEMA REJECT: unknown schema {row['schema_version']!r}")
    STREAM.parent.mkdir(parents=True, exist_ok=True)
    with open(STREAM, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract(event: dict):
    """Defensively pull (command, result, exit_code) out of a hook event payload."""
    tool_input = event.get("tool_input") or event.get("input") or {}
    command = tool_input.get("command") or tool_input.get("cmd") or ""
    resp = event.get("tool_response") or event.get("tool_result") or event.get("response") or {}
    if isinstance(resp, dict):
        result = resp.get("stdout") or resp.get("output") or resp.get("content") or resp.get("result") or ""
        exit_code = resp.get("exit_code", resp.get("exitCode"))
        if exit_code is None and isinstance(result, str) and result:
            exit_code = 0
    else:
        result, exit_code = resp, 0 if resp else None
    return command, result, exit_code


def cmd_hook(args) -> None:
    try:
        event = json.load(sys.stdin)
    except Exception as e:
        print(f"trajectory_step: bad event json: {e}", file=sys.stderr)
        return
    command, result, exit_code = extract(event)
    if not command:
        return
    row = make_row(event.get("session_id") or "unknown", command, result, exit_code)
    append_row(row)


def cmd_verify(args) -> None:
    if not STREAM.exists():
        print("stream empty — the base is not frozen yet")
        return
    total = ok = 0
    for line in STREAM.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            row = json.loads(line)
            basis = "|".join([row["session_id"], row["ts"], row["command"],
                              row["result"]["output_excerpt"]])
            if hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16] == row["step_hash"]:
                ok += 1
        except Exception:
            pass
    print(f"verify: {ok}/{total} rows hash-clean | stream {STREAM.stat().st_size} B")
    if ok != total:
        print("  !! tampering or schema drift — inspect the mismatched rows")


def cmd_stats(args) -> None:
    if not STREAM.exists():
        print("0 steps — the base is not frozen yet")
        return
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    rows = [json.loads(l) for l in STREAM.open(encoding="utf-8") if l.strip()]
    todays = [r for r in rows if r["ts"].startswith(today)]
    print(f"steps total: {len(rows)} | today (UTC): {len(todays)} | vertical pace: {len(todays)}/100")
    for r in rows[-(args.n or 5):]:
        print(f"  {r['ts'][11:19]}Z {r['step_hash']} $ {r['command'][:90]}")


def cmd_test_reject(args) -> None:
    """Falsifier: a write without schema_version MUST be refused."""
    bad = {"step_hash": "0" * 16, "command": "schemaless write attempt"}
    try:
        append_row(bad)
    except ValueError as e:
        print(f"falsifier SCHEMA: PASS — {e}")
        return
    print("falsifier SCHEMA: FAIL — the schemaless write LANDED (drift killer dead)")


def main():
    ap = argparse.ArgumentParser(prog="mag.trajectory_step")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("hook").set_defaults(fn=cmd_hook)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    s = sub.add_parser("stats"); s.add_argument("n", nargs="?", type=int, default=5); s.set_defaults(fn=cmd_stats)
    sub.add_parser("test-reject").set_defaults(fn=cmd_test_reject)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
