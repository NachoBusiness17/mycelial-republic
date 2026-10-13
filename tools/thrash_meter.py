"""thrash_meter -- the multi-front thrash instrument (THE 50 / W6 / T27, 2026-09-19).

Born from mag/behavior_catch.py's operator catch "thrash_multi_front":
"Open many fronts then rebuild the middle (sprint / catchup)". Until now that
pattern was caught in operator language only. This instrument measures the same
shape in the fleet's own body: the trajectory log (memory/trajectory/steps.jsonl,
schema trajectory_step.v1) records every step every seat takes, stamped and
session-tagged. Interleaving is visible in the ordering of fronts touched.

A FRONT is the repo area a step touches: the top-level segment of the first
repo-relative path in the command (watch, mag, memory, dashboard, queue, ...);
steps with no repo path take their executable name instead (git, rg, python,
...). This is a documented heuristic, not a truth instrument -- the honest
counterpart is tools/drift.py: a rate says "is it moving"; corr(delta-M,
delta-R) would say whether the motion is north. This meter only claims the
rate and shape of motion.

READINGS
  events          steps in the window (oldest to newest)
  fronts          distinct fronts touched
  sessions        distinct seats/sessions in the window
  switches        consecutive steps where the front changed
  switch_rate     switches / (events - 1), in [0, 1]
  revisits        switches BACK to a front already left earlier in the window
                  (the "rebuild the middle" signature)
  revisit_share   revisits / switches, in [0, 1]
  interleave_max  max distinct fronts inside any rolling 10-step window
  thrash_score    0-100: 100 * (0.5 * switch_rate + 0.5 * revisit_share)

VERDICT BANDS (documented thresholds, not learned):
  INSUFFICIENT   fewer than 10 events in window -- refuses to guess
  FOCUSED        score < 25
  STEADY         25 <= score < 45
  SWITCHY        45 <= score < 70
  THRASHING      score >= 70

KNOWN BIAS (filed honestly):
  - A single seat doing one task that legitimately touches many dirs scores
    higher than its focus warrants; the front heuristic cannot see intent.
  - Parallel sessions interleaving in the shared log raise switch_rate even
    when each seat is individually focused; sessions count is reported
    alongside so the reader can tell fleet parallelism from single-seat spin.
  - Score bands are flat priors; treat crossings as a prompt to look, not a
    verdict.

Pure reader: reads the trajectory log, writes nothing (the --out flag is an
explicit caller decision). Wire: registered in tools/__init__.py as
"thrash_meter", served live at GET /api/v1/thrash (dashboard/rest.py).

Run:  .venv/Scripts/python.exe tools/thrash_meter.py [--hours 6] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO / "memory" / "trajectory" / "steps.jsonl"

MAX_EVENTS_CAP = 50000          # hard ceiling on in-window events kept
ROLLING_WINDOW = 10             # rolling window for interleave_max
MIN_EVENTS = 10                 # below this: INSUFFICIENT, refuse to guess

DRIVE_RE = re.compile(r"^[A-Za-z]:$")
REPO_ANCHOR = "local_sovereign_agent"
KNOWN_DIRS = {"watch", "mag", "memory", "dashboard", "queue", "tools",
              "scripts", "training", "configs", "corpus", "catalog",
              "docs", "tests", "canon"}
GLUE_CHARS = set("&|;><()")


def assign_front(command: str) -> str:
    """Heuristic front label for one trajectory step's command string.

    Scans tokens: the first repo-relative path wins (top-level segment;
    launcher dirs like .venv are skipped so the script's dir counts);
    a bare known dir name wins; otherwise the first verb token falls back.
    """
    if not command:
        return "unknown"
    norm = command.replace("\\", "/")
    verb = None
    for raw in norm.split():
        tok = raw.strip("'\"(),;")
        if not tok or DRIVE_RE.match(tok) or tok.startswith("-"):
            continue
        if ">" in tok or "<" in tok or "=" in tok:
            continue  # redirects (2>&1, >>f) and inline code (x=path) are not fronts
        if set(tok) <= GLUE_CHARS:
            continue
        if REPO_ANCHOR in tok:
            after = tok.split(REPO_ANCHOR, 1)[1]
            segs = [s for s in after.split("/") if s and s != "~"]
            if segs:
                return segs[0][:40]
            continue
        if "/" in tok:
            first = tok.split("/", 1)[0]
            if first and not DRIVE_RE.match(first) and not first.startswith((".", "http")):
                return first[:40]
            continue
        if tok in KNOWN_DIRS:
            return tok
        if verb is None:
            verb = tok
    return (verb or "unknown")[:40].lower() or "unknown"


def _parse_ts(value) -> datetime | None:
    if not value:
        return None
    try:
        ts = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


def read_steps(source: Path, hours: float, max_events: int) -> list[dict]:
    """Stream the trajectory log, keep in-window steps, newest last.

    Bounded: at most max_events are kept (the newest ones); a malformed row
    is skipped, not fatal.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    kept: list[dict] = []
    with source.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _parse_ts(row.get("ts"))
            if ts is None or ts < cutoff:
                continue
            kept.append(row)
            if len(kept) > max_events:
                kept = kept[-max_events:]
    return kept


def thrash_reading(events: list[dict], hours: float, source: Path) -> dict:
    """Compute one thrash reading from ordered (oldest-first) trajectory steps."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base = {
        "schema": "thrash_reading.v1",
        "computed_at": now,
        "source": str(source).replace("\\", "/"),
        "window_hours": hours,
    }
    if not events:
        return {**base, "ok": False, "error": "no trajectory steps in window",
                "hint": "is memory/trajectory/steps.jsonl alive and inside the window?"}

    ordered = sorted(events, key=lambda r: _parse_ts(r.get("ts")) or datetime.min.replace(tzinfo=timezone.utc))
    fronts_seq = [assign_front(str(r.get("command") or "")) for r in ordered]
    n = len(fronts_seq)

    switches = 0
    revisits = 0
    seen: set[str] = set()
    for i in range(1, n):
        if fronts_seq[i] != fronts_seq[i - 1]:
            switches += 1
            if fronts_seq[i] in seen:
                revisits += 1
        seen.add(fronts_seq[i - 1])

    switch_rate = switches / max(n - 1, 1)
    revisit_share = revisits / max(switches, 1)
    score = round(100 * (0.5 * switch_rate + 0.5 * revisit_share))

    interleave_max = 0
    for i in range(n):
        chunk = set(fronts_seq[i:i + ROLLING_WINDOW])
        interleave_max = max(interleave_max, len(chunk))

    if n < MIN_EVENTS:
        verdict, note = "INSUFFICIENT", (f"only {n} events in window; need >= {MIN_EVENTS} to say anything")
    elif score >= 70:
        verdict, note = "THRASHING", "high switch rate with mostly revisited fronts: many fronts, rebuild-the-middle shape"
    elif score >= 45:
        verdict, note = "SWITCHY", "frequent front changes; check whether each front is reaching done before the next"
    elif score >= 25:
        verdict, note = "STEADY", "normal interleaving; fronts change but mostly move forward"
    else:
        verdict, note = "FOCUSED", "long same-front runs; little interleaving in this window"

    front_counts = Counter(fronts_seq)
    session_counts = Counter(str(r.get("session_id") or "unknown") for r in ordered)
    per_front = [
        {"front": f, "events": c, "share": round(c / n, 3)}
        for f, c in front_counts.most_common(12)
    ]
    per_session = [
        {"session_id": s, "events": c}
        for s, c in session_counts.most_common(8)
    ]

    return {
        **base,
        "ok": True,
        "tool": "thrash_meter",
        "events": n,
        "window_first_ts": str(ordered[0].get("ts")),
        "window_last_ts": str(ordered[-1].get("ts")),
        "fronts": len(front_counts),
        "sessions": len(session_counts),
        "switches": switches,
        "switch_rate": round(switch_rate, 4),
        "revisits": revisits,
        "revisit_share": round(revisit_share, 4),
        "interleave_max": interleave_max,
        "rolling_window": ROLLING_WINDOW,
        "thrash_score": score,
        "verdict": verdict,
        "note": note,
        "per_front_top": per_front,
        "per_session_top": per_session,
        "method": {
            "front": ("top-level segment of the first repo-relative path in the "
                      "step command, else the executable name (documented heuristic)"),
            "thrash_score": "100 * (0.5 * switch_rate + 0.5 * revisit_share)",
            "verdict_bands": {"FOCUSED": "<25", "STEADY": "25-44", "SWITCHY": "45-69",
                              "THRASHING": ">=70", "INSUFFICIENT": f"<{MIN_EVENTS} events"},
            "kin": "mag/behavior_catch.py thrash_multi_front; tools/drift.py",
        },
        "known_bias": [
            "single-seat work that legitimately touches many dirs scores higher than its focus warrants",
            "parallel sessions raise switch_rate in the shared log even when each seat is focused; read sessions alongside",
            "bands are flat priors: a crossing is a prompt to look, not a verdict",
        ],
    }


def thrash_cmd(hours: float = 6, max_events: int = 20000, source: str = "") -> dict:
    """Dict-in/dict-out wrapper for TOOL_MAP / REST callers."""
    src = Path(source) if source else DEFAULT_SOURCE
    if not src.is_file():
        return {"ok": False, "tool": "thrash_meter",
                "error": f"source not found: {src}".replace("\\", "/")}
    hours = min(168.0, max(0.1, float(hours)))
    max_events = min(MAX_EVENTS_CAP, max(10, int(max_events)))
    try:
        events = read_steps(src, hours, max_events)
    except OSError as e:
        return {"ok": False, "tool": "thrash_meter", "error": f"read failed: {e}"}
    return thrash_reading(events, hours, src)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="multi-front thrash reading from the trajectory log")
    ap.add_argument("--hours", type=float, default=6.0, help="window size in hours (default 6)")
    ap.add_argument("--max-events", type=int, default=20000, help="cap on in-window events kept")
    ap.add_argument("--source", default="", help="alternate trajectory jsonl path")
    ap.add_argument("--out", default="", help="also write the reading JSON here")
    args = ap.parse_args(argv)

    reading = thrash_cmd(hours=args.hours, max_events=args.max_events, source=args.source)
    print(json.dumps(
        {k: v for k, v in reading.items() if k not in ("method", "known_bias", "per_front_top", "per_session_top")},
        indent=2, ensure_ascii=False))
    if reading.get("ok"):
        print("top fronts:", ", ".join(f"{f['front']}={f['events']}" for f in reading["per_front_top"][:8]))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(reading, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {out}")
    return 0 if reading.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
