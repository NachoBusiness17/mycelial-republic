#!/usr/bin/env python
"""harness_eval.py — two-stage harness scorer for the fleet's own organs.

Adapted from HarnessDev (arXiv 2609.01437): evaluation shifts from task outputs
to runnable infrastructure. Fixed "weights" (the organs are static files), two
stages:

STAGE 1 (visible battery) — checks the organs were BUILT against:
  queue:  todo.md checkbox status counts parse; queue_events.jsonl rows parse
          with ts+event; drain task_ids nonempty.
  room:   every watch/room.jsonl row parses as JSON; required identity keys
          present (ts, and a thread-or-event key, and a type-or-event key —
          older rows use "event" as the type slot; lenient union documented);
          no duplicate consecutive identical rows.
  falsifiers: dashboard/static/{lattice_check,chain_check,claim_check}.html
          served with HTTP 200 on 127.0.0.1:8765 and contain their marker
          strings ("Legendre", "leaf:", "launched law").

STAGE 2 (held-out battery) — DIFFERENT checks on DIFFERENT slices, per the
paper's finding that self-improvement gains fail to generalize to unseen
tasks. Nothing here was a build-time invariant:
  queue:  deeper slice — queue/handoff/cloud-*.json handoffs: schema field,
          parseable ts, unique run_ids, stale (>30d) handoffs flagged.
  room:   different date range — rows BEFORE 2026-09-03 (the first half of
          the log) re-checked for keys, ts ISO-parseability, and global
          timestamp monotonicity.
  falsifiers: different surface — markers verified in the FILES ON DISK
          (server-independent) plus <title> well-formedness, instead of HTTP.

STAGE 1 score may be near-perfect while STAGE 2 diverges; that divergence is
the brittle-generalization signal the paper measures. Measure, never fix.

Usage: .venv/Scripts/python.exe scripts/harness_eval.py
Output: JSON to stdout; appended to memory/runs/harness_eval/eval_<ts>.json.
Zero deps beyond stdlib.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_EVENTS = ROOT / "logs" / "queue_events.jsonl"
QUEUE_TODO = ROOT / "queue" / "todo.md"
QUEUE_CLAIMS = ROOT / "logs" / "queue_gate_claims.jsonl"
QUEUE_HANDOFF = ROOT / "queue" / "handoff"
ROOM = ROOT / "watch" / "room.jsonl"
BASE = "http://127.0.0.1:8765"
STALE_HOURS = 48
HANDOFF_STALE_DAYS = 30
HELD_OUT_CUTOFF = "2026-09-03"  # stage-2 room slice: strictly before this date

FALSIFIERS = [
    ("lattice_check", "Legendre"),
    ("chain_check", "leaf:"),
    ("claim_check", "launched law"),
]


def _check(name, ok, detail=""):
    return {"check": name, "pass": bool(ok), "detail": str(detail)[:300]}


def _read_jsonl(path: Path):
    rows, bad = [], 0
    if not path.exists():
        return rows, bad, 0
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                bad += 1
    return rows, bad, bad + len(rows)


# ---------------------------------------------------------------- queue
def queue_stage1():
    checks = []
    todo = QUEUE_TODO.read_text(encoding="utf-8", errors="replace") if QUEUE_TODO.exists() else ""
    done = len(re.findall(r"^- \[x\]", todo, re.M))
    open_ = len(re.findall(r"^- \[ \]", todo, re.M))
    checks.append(_check("todo_status_counts", done + open_ > 0,
                         f"done={done} open={open_}"))
    rows, bad, total = _read_jsonl(QUEUE_EVENTS)
    checks.append(_check("events_parse", total > 0 and bad == 0,
                         f"{len(rows)}/{total} rows parse, {bad} bad"))
    ids = [r.get("task_id") for r in rows if isinstance(r, dict)]
    missing = sum(1 for i in ids if not i)
    checks.append(_check("task_ids_present", len(ids) > 0 and missing == 0,
                         f"{len(ids)} task_ids, {missing} empty"))
    counts = {}
    for r in rows:
        if isinstance(r, dict):
            counts[r.get("event", "?")] = counts.get(r.get("event", "?"), 0) + 1
    checks.append(_check("status_counts_computable", bool(counts), json.dumps(counts)[:200]))
    return checks


def queue_stage2():
    checks = []
    handoffs = sorted(QUEUE_HANDOFF.glob("cloud-*.json"))
    parsed, bad_schema, bad_ts = [], 0, 0
    now = time.time()
    stale = []
    for p in handoffs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if d.get("schema") != "cloud_handoff.v1":
            bad_schema += 1
        else:
            parsed.append(d)
        ts = d.get("ts")
        try:
            age_days = (now - datetime.fromisoformat(ts).timestamp()) / 86400
            if age_days > HANDOFF_STALE_DAYS:
                stale.append(p.name)
        except (TypeError, ValueError):
            bad_ts += 1
    checks.append(_check("handoff_schema", bool(handoffs) and bad_schema == 0,
                         f"{len(parsed)}/{len(handoffs)} ok, {bad_schema} wrong schema"))
    run_ids = [d.get("run_id") for d in parsed]
    dups = len(run_ids) - len(set(run_ids))
    checks.append(_check("handoff_run_ids_unique", dups == 0,
                         f"{len(run_ids)} handoffs, {dups} dup run_ids"))
    checks.append(_check("handoff_ts_parseable", bad_ts == 0, f"{bad_ts} unparseable ts"))
    checks.append(_check("handoff_not_stale", len(stale) == 0,
                         f"{len(stale)} handoffs older than {HANDOFF_STALE_DAYS}d"))
    # stale gate claims (different slice than events)
    claims, cbad, ctotal = _read_jsonl(QUEUE_CLAIMS)
    stale_claims = 0
    for c in claims:
        try:
            age_h = (now - datetime.fromisoformat(c["ts"].replace("Z", "+00:00")).timestamp()) / 3600
            if age_h > STALE_HOURS:
                stale_claims += 1
        except (KeyError, TypeError, ValueError):
            stale_claims += 1
    checks.append(_check("claims_not_stale", stale_claims == 0 and ctotal > 0,
                         f"{stale_claims}/{ctotal} claims stale>{STALE_HOURS}h or malformed"))
    return checks


# ---------------------------------------------------------------- room
def _room_identity(row):
    return ("ts" in row and ("thread" in row or "event" in row)
            and ("type" in row or "event" in row))


def room_stage1():
    checks = []
    rows, bad, total = _read_jsonl(ROOM)
    checks.append(_check("rows_parse", total > 0 and bad == 0, f"{len(rows)}/{total} parse"))
    missing = sum(1 for r in rows if not _room_identity(r))
    checks.append(_check("required_keys", missing == 0, f"{missing}/{len(rows)} missing identity keys"))
    raw = [l for l in ROOM.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    dup_consec = sum(1 for a, b in zip(raw, raw[1:]) if a == b)
    checks.append(_check("no_dup_consecutive", dup_consec == 0, f"{dup_consec} dup consecutive rows"))
    return checks


def room_stage2():
    checks = []
    rows, _, _ = _read_jsonl(ROOM)
    held = [r for r in rows if str(r.get("ts", "")) < HELD_OUT_CUTOFF]
    checks.append(_check("heldout_slice_nonempty", len(held) > 100,
                         f"{len(held)} rows before {HELD_OUT_CUTOFF}"))
    missing = sum(1 for r in held if not _room_identity(r))
    checks.append(_check("heldout_required_keys", missing == 0,
                         f"{missing}/{len(held)} missing identity keys"))
    bad_ts = 0
    for r in held:
        try:
            datetime.fromisoformat(str(r["ts"]))
        except (KeyError, TypeError, ValueError):
            bad_ts += 1
    checks.append(_check("heldout_ts_iso", bad_ts == 0, f"{bad_ts} unparseable ts"))
    tss = [r.get("ts", "") for r in held if isinstance(r.get("ts"), str)]
    mono = all(a <= b for a, b in zip(tss, tss[1:]))
    checks.append(_check("heldout_ts_monotonic", mono,
                         "append order is timestamp order" if mono else "out-of-order ts found"))
    return checks


# ---------------------------------------------------------------- falsifiers
def falsifiers_stage1():
    checks = []
    for name, marker in FALSIFIERS:
        try:
            with urllib.request.urlopen(f"{BASE}/static/{name}.html", timeout=5) as resp:
                code, body = resp.status, resp.read().decode("utf-8", "replace")
        except Exception as e:
            checks.append(_check(f"{name}_http200", False, f"error: {e}"))
            continue
        checks.append(_check(f"{name}_http200", code == 200, f"HTTP {code}"))
        checks.append(_check(f"{name}_marker", marker in body, f"marker {marker!r}"))
    return checks


def falsifiers_stage2():
    checks = []
    for name, marker in FALSIFIERS:
        p = ROOT / "dashboard" / "static" / f"{name}.html"
        if not p.exists():
            checks.append(_check(f"{name}_on_disk", False, "file missing"))
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        checks.append(_check(f"{name}_marker_on_disk", marker in text, f"marker {marker!r}"))
        m = re.search(r"<title>([^<]*)</title>", text)
        ok = bool(m) and "Check" in m.group(1) and len(text) > 1000
        checks.append(_check(f"{name}_title_wellformed", ok,
                             m.group(1) if m else "no <title>"))
    return checks


def score(checks):
    return round(sum(1 for c in checks if c["pass"]) / len(checks), 4) if checks else 0.0


def main():
    organs = {
        "queue": {"stage1": queue_stage1(), "stage2": queue_stage2()},
        "room": {"stage1": room_stage1(), "stage2": room_stage2()},
        "falsifiers": {"stage1": falsifiers_stage1(), "stage2": falsifiers_stage2()},
    }
    for o in organs.values():
        o["score_stage1"] = score(o["stage1"])
        o["score_stage2"] = score(o["stage2"])
    s1 = score([c for o in organs.values() for c in o["stage1"]])
    s2 = score([c for o in organs.values() for c in o["stage2"]])
    out = {
        "schema": "harness_eval.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "protocol": "HarnessDev arXiv 2609.01437 two-stage, fixed weights",
        "organs": organs,
        "stage1_score": s1,
        "stage2_score": s2,
        "harness_score": round((s1 + s2) / 2, 4),
    }
    print(json.dumps(out, indent=2))
    d = ROOT / "memory" / "runs" / "harness_eval"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"eval_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
