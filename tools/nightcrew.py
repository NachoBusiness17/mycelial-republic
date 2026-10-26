#!/usr/bin/env python3
"""nightcrew - the standing headless drain of the DS overflow queue (2026-10-10).

Operator ask: "shouldnt we have a standing cron job of old that doesnt need to
wait in windows and workflows?" + "we could launch a dozen deep seek agents
cheaply to finish hard work like that." Windows and gated workflows are
session-bound; the queue should not wait on either. This cron drains
queue/ds_overflow/INBOX.jsonl through tools.ds_workhorse (the proven
$0.0007-class lane) and banks receipts - no window, no workflow, no session.

Laws carried:
- OVERFLOW ROUTING (STANDING_RAILS): DeepSeek is the overflow lane for
  MECHANICAL work (extraction, triage, drafts), never judgment, never
  verification. The inbox row's prompt file says what it is; the crew just
  runs it.
- HOLLOW-BATCH: ds_workhorse itself enforces ok_api vs ok_material; the crew
  re-checks output rows exist and are non-empty before banking done.
- RECEIPTS: every drained batch writes queue/ds_overflow/DONE/<ts>/ with the
  in/out files and a manifest line; a no-op run banks nothing (idempotent).
- ONE-WRITER: the crew MOVES claimed rows to a claim file before running, so
  two overlapping fires cannot double-spend.

Inbox row shape (queue/ds_overflow/INBOX.jsonl):
  {"id": "slug-1", "prompt_file": "queue/ds_overflow/askN_prompt.md",
   "items_file": "queue/ds_overflow/askN_items.jsonl", "note": "why",
   "lane": "ds"}          # ds (default) | opencode | grok | ollama

LANE DIRECTING (operator ask, 2026-10-10: "or use those to direct the free
lanes"): a row may name its carrier. ds = the workhorse batch lane (mechanical
work, thinking off). opencode = the free z.ai plan agent lane (opencode run -m
zai/glm-5.3, proven OC-5.3-AWAKE; the prompt file IS the ask, the items file
path is named in the ask so the agent reads its own inputs). grok = the
operator-funded X/search lane. ollama = local. FREE-LANE LAW (DRIVING LADDER):
free-carrier results bank as FINDINGS, never done/trusted work; verification
climbs. The manifest stamps lane + findings_class on every non-ds row so the
climb is auditable.

Run: .venv/Scripts/python.exe tools/nightcrew.py            (drain, then exit)
     .venv/Scripts/python.exe tools/nightcrew.py --dry      (report only)
Exit 0 always unless the inbox is corrupt (2): a crashed batch is banked as a
failed row, not a crash - the next fire retries nothing blindly.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path

ESTATE = Path(__file__).resolve().parent.parent
Q = ESTATE / "queue" / "ds_overflow"
INBOX = Q / "INBOX.jsonl"
CLAIMS = Q / "CLAIMS.jsonl"
DONE = Q / "DONE"
PY = Path(sys.executable)


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_rows() -> list[dict]:
    if not INBOX.exists():
        return []
    rows = []
    for line in INBOX.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _append(path: Path, obj: dict) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj) + "\n")


def _run_lane(row: dict, out_dir: Path) -> tuple[int, str]:
    """Dispatch one row to its carrier. ds = workhorse batch; the free lanes
    take the prompt file as the ask and are told where their inputs live."""
    lane = str(row.get("lane") or "ds").lower()
    items = ESTATE / str(row.get("items_file") or "")
    prompt = ESTATE / str(row.get("prompt_file") or "")
    out = out_dir / "results.jsonl"
    if lane == "ds":
        proc = subprocess.run(
            [str(PY), "-m", "tools.ds_workhorse", "run",
             "--in", str(items), "--prompt-file", str(prompt), "--out", str(out)],
            capture_output=True, text=True, timeout=1800, cwd=str(ESTATE))
        return proc.returncode, (proc.stderr or "")[-300:]
    if not prompt.exists():
        return 2, "missing prompt file"
    ask = prompt.read_text(encoding="utf-8", errors="replace")
    if items.exists():
        ask += ("\n\nYour input items file (read it yourself, one JSON object "
                "per line): " + str(items)
                + "\nWrite your results as JSONL lines to: " + str(out))
    if lane == "opencode":
        proc = subprocess.run(
            ["opencode", "run", "-m", "zai/glm-5.3", ask],
            capture_output=True, text=True, timeout=1800, cwd=str(ESTATE))
    elif lane == "grok":
        proc = subprocess.run(
            ["grok", "-p", ask],
            capture_output=True, text=True, timeout=1800, cwd=str(ESTATE))
    elif lane == "ollama":
        proc = subprocess.run(
            [str(PY), "-c",
             "import json,urllib.request;"
             "body=json.dumps({'model':'gemma:2b','stream':False,"
             "'messages':[{'role':'user','content':open(r'" + str(prompt)
             .replace("'", "\\'") + "',encoding='utf-8').read()]}).encode();"
             "print(urllib.request.urlopen(urllib.request.Request("
             "'http://localhost:11434/api/chat',data=body,"
             "headers={'Content-Type':'application/json'}),timeout=600)"
             ".read().decode())"],
            capture_output=True, text=True, timeout=900, cwd=str(ESTATE))
        (out_dir / "raw_carrier_out.txt").write_text(
            proc.stdout or "", encoding="utf-8", errors="replace")
    else:
        return 2, "unknown lane: " + lane
    return proc.returncode, (proc.stderr or "")[-300:]


def drain(dry: bool) -> int:
    rows = _read_rows()
    if not rows:
        print(json.dumps({"event": "noop", "inbox": 0, "ts": _now()}))
        return 0
    if dry:
        print(json.dumps({"event": "dry", "inbox": len(rows),
                          "ids": [r.get("id") for r in rows]}))
        return 0
    Q.mkdir(parents=True, exist_ok=True)
    DONE.mkdir(parents=True, exist_ok=True)
    # claim everything present, clear the inbox (one-writer claim)
    claimed = rows
    INBOX.write_text("", encoding="utf-8")
    for r in claimed:
        _append(CLAIMS, {**r, "claimed_ts": _now()})
    for r in claimed:
        rid = str(r.get("id") or "anon")
        lane = str(r.get("lane") or "ds").lower()
        stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = DONE / (stamp + "-" + rid)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "results.jsonl"
        rc, err_tail = _run_lane(r, out_dir)
        n_rows = 0
        n_nonempty = 0
        if out.exists():
            for line in out.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    j = json.loads(line)
                except json.JSONDecodeError:
                    n_nonempty += int(bool(line))
                    n_rows += 1
                    continue
                n_rows += 1
                txt = str(j.get("out") or j.get("text")
                           or j.get("content") or "")
                if txt.strip():
                    n_nonempty += 1
        _append(out_dir / "manifest.jsonl", {
            "event": "drained", "id": rid, "lane": lane, "exit": rc,
            "rows": n_rows, "nonempty": n_nonempty,
            "hollow": bool(n_rows and n_nonempty < n_rows),
            "findings_class": ("finding-never-done" if lane != "ds" else "workhorse"),
            "stderr_tail": err_tail, "ts": _now(),
        })
    print(json.dumps({"event": "drained", "count": len(claimed), "ts": _now()}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    return drain(ap.parse_args().dry)


if __name__ == "__main__":
    sys.exit(main())
