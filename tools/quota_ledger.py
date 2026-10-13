#!/usr/bin/env python3
"""quota_ledger.py — window-quota ledger v0 (2026-09-30).

The lensing this meters (full narrative + method: watch/inbox/QUOTA_LEDGER.md):
dollars are metered to the cent while the BINDING currency — the provider
5-hour window quota on account:zai-individual-coding-plan — is invisible.
2026-09-30 burned a 20-wide fire into the 1308 5-hour wall after five 1302
contacts while the day's spend field read $0.18. The estate optimizes what it
meters; this meters the window.

Byte truth first, receipts second: lane fires = subagent records
<agents_root>/sess_*/agent_*/metadata.json (createdAt, lane, usage tokens);
walls = failed subagents whose output.txt carries [1302]/[1308] (1308 reset
time verbatim; request-id stamps UTC+8 inferred, cross-check only);
DROP_LEDGER.jsonl is date-granular context; watch/inbox receipts secondary.
Verdict envelopes are receipt-shaped: 8-12 sustained = green, ~15 = first
1302s, 19+ at once = red (AH_REFIRE_QUEUE, ENVELOPE_50W_HIT, AFTERPARTY_CLOSE
B2-476). HONESTY: tokens are harness-recorded only (failed/running carry
none — the lanes that died ON the wall are exactly the unrecorded ones),
cache-inclusive, fire-time attributed, main-session turns invisible; the
exact instrument is provider-side usage fields + the account snapshot inside
every 1302/1308 payload. Exit 0 GREEN/AMBER, 1 RED, 2 cannot verify.

Usage: .venv/Scripts/python.exe tools/quota_ledger.py [--day YYYY-MM-DD]
       [--hours 5] [--agents-root PATH] [--repo-root PATH] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:  # direct `python tools/quota_ledger.py` execution
    sys.path.insert(0, str(ROOT))

# receipt-side secondary evidence + rendering live in the sibling module
# (split for the 400-line cap, census_patrol_selftest pattern B2-248)
from tools.quota_ledger_report import (  # noqa: E402  (re-exported API)
    grep_receipts, load_drop_rows, render_json, render_markdown)

# --- constants shaped by receipts, not vibes -------------------------------
WINDOW_HOURS_DEFAULT = 5          # the provider wall is 5-hour (1308 payload text)
GREEN_CEILING = 12                # proven clean sustained width (AFTERPARTY_CLOSE B2-476)
FIRST_1302_WIDTH = 15             # "ceiling at ~15 (two 1302 deaths)" envelope-probe 9/25
RED_WIDTH = 19                    # 19-at-once slammed the wall (AH_REFIRE_QUEUE refire law)
HOLD_BURST_WIDTH = 16             # no NEW waves at >=16 trailing fires (recommendation)
WALL_CLUSTER_GAP = timedelta(minutes=10)   # deaths within 10 min = one wall moment

CODE_RE = re.compile(r"\[(130[28])\]")
RESET_RE = re.compile(r"Your limit will reset at ([0-9\-: ]+)")
REQID_RE = re.compile(r"\[(\d{14})[0-9a-f]+\]")

# --- data model -------------------------------------------------------------
@dataclass
class Fire:
    """One lane fire = one subagent dispatch on the tethered account."""
    ts: datetime                      # createdAt (UTC)
    done_ts: datetime | None          # completedAt/updatedAt (UTC), None while running
    lane: str                         # description (lane name) or ""
    session: str                      # parent session id
    status: str                       # completed | failed | running | other
    tokens: int | None                # usage.totalTokens where recorded
    code: str | None                  # "1302"|"1308" if the death payload carries it
    reset_at: str | None              # 1308 reset time (provider clock, verbatim)
    provider_stamp: datetime | None   # request-id timestamp (provider clock, UTC+8 inf.)

    @property
    def wall_coded(self) -> bool:
        return self.status == "failed" and self.code in ("1302", "1308")

@dataclass
class WallMoment:
    """A cluster of wall-coded deaths — one contact with one wall."""
    ts: datetime                      # first death's done_ts in the cluster
    codes: set[str]
    lanes: list[str]
    reset_at: str | None = None       # 1308 payload reset (provider clock)
    provider_stamp: datetime | None = None
    window_ended: str = ""            # best-effort provider window label
    last_ts: datetime | None = None   # newest death in the cluster (internal)

@dataclass
class Report:
    day: str
    fires: list[Fire] = field(default_factory=list)
    walls: list[WallMoment] = field(default_factory=list)
    receipt_hits: list[dict] = field(default_factory=list)
    drop_rows: list[dict] = field(default_factory=list)
    verdict: str = ""                 # GREEN | AMBER | RED (day shape)
    hold_line: str = ""
    stats: dict = field(default_factory=dict)

def _parse_ts(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None

def _load_fire(agent_dir: Path) -> Fire | None:
    mf = agent_dir / "metadata.json"
    if not mf.is_file():
        return None
    try:
        meta = json.loads(mf.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    ts = _parse_ts(meta.get("createdAt"))
    if ts is None:
        return None
    done_ts = _parse_ts(meta.get("completedAt") or meta.get("updatedAt"))
    tokens = (meta.get("usage") or {}).get("totalTokens")
    code = reset_at = provider_stamp = None
    text = ""  # unreadable output.txt reads as no wall payload, not as silence
    if (out := agent_dir / "output.txt").is_file():
        try:
            text = out.read_text(encoding="utf-8", errors="replace")[:2000]
        except OSError:
            text = ""
    m = CODE_RE.search(text)
    if m:
        code = m.group(1)
    m = RESET_RE.search(text)
    if m:
        reset_at = m.group(1).strip()
    m = REQID_RE.search(text)
    if m:  # provider request-id leading 14 digits = provider-local stamp
        try:
            provider_stamp = datetime.strptime(m.group(1)[:14], "%Y%m%d%H%M%S")
        except ValueError:
            provider_stamp = None
    return Fire(ts=ts.astimezone(timezone.utc),
                done_ts=done_ts.astimezone(timezone.utc) if done_ts else None,
                lane=(meta.get("description") or "").strip(),
                session=(meta.get("parentSessionId") or agent_dir.parent.name),
                status=(meta.get("status") or "unknown"), tokens=tokens, code=code,
                reset_at=reset_at, provider_stamp=provider_stamp)

def load_fires(agents_root: Path, day: str, sessions: Iterable[Path] | None = None) -> list[Fire]:
    """Fires whose createdAt (UTC) falls on `day`. A session older than day-1
    (dir mtime) cannot host a day fire — cheap prefilter, bytes still rule."""
    if sessions is None:
        sessions = sorted(p for p in agents_root.glob("sess_*") if p.is_dir())
    day_start = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)
    day_end = day_start + timedelta(days=1)
    cutoff_lo = day_start - timedelta(days=1)
    fires: list[Fire] = []
    for s in sessions:
        try:
            if datetime.fromtimestamp(s.stat().st_mtime, tz=timezone.utc) < cutoff_lo:
                continue
        except OSError:
            continue
        for agent_dir in sorted(s.glob("agent_*")):
            f = _load_fire(agent_dir)
            if f and day_start <= f.ts < day_end:
                fires.append(f)
    fires.sort(key=lambda f: f.ts)
    return fires

def cluster_walls(fires: list[Fire]) -> list[WallMoment]:
    """Wall-coded deaths within WALL_CLUSTER_GAP of each other = one moment."""
    dead = sorted((f for f in fires if f.wall_coded and f.done_ts),
                  key=lambda f: f.done_ts)
    walls: list[WallMoment] = []
    for f in dead:
        if walls and f.done_ts - (walls[-1].last_ts or walls[-1].ts) <= WALL_CLUSTER_GAP:
            w = walls[-1]
            w.codes.add(f.code)
            w.lanes.append(f.lane)
            w.last_ts = f.done_ts
            w.reset_at = w.reset_at or f.reset_at
            w.provider_stamp = w.provider_stamp or f.provider_stamp
        else:
            walls.append(WallMoment(ts=f.done_ts, codes={f.code}, lanes=[f.lane],
                                    reset_at=f.reset_at,
                                    provider_stamp=f.provider_stamp, last_ts=f.done_ts))
    for w in walls:
        # which provider window a wall ENDED: 1308 names the reset, so the
        # burned window is reset-5h (provider clock, converted for display)
        if w.reset_at:
            try:
                reset = datetime.strptime(w.reset_at, "%Y-%m-%d %H:%M:%S")
                opened = reset - timedelta(hours=WINDOW_HOURS_DEFAULT)
                w.window_ended = (f"window {opened.strftime('%m-%d %H:%M')}"
                                  f"->{reset.strftime('%H:%M')} provider")
            except ValueError:
                w.window_ended = f"reset {w.reset_at} (provider clock)"
        else:
            w.window_ended = "window anchor unknown (no reset payload)"
    return walls

def window_count(fires: list[Fire], end: datetime, hours: int) -> int:
    start = end - timedelta(hours=hours)
    return sum(1 for f in fires if start <= f.ts <= end)

def peak_width(fires: list[Fire], hours: int) -> tuple[int, datetime]:
    """Max lane fires inside any rolling `hours` window (evaluated at each fire)."""
    best, best_ts = 0, datetime.min.replace(tzinfo=timezone.utc)
    for f in fires:
        n = window_count(fires, f.ts, hours)
        if n > best:
            best, best_ts = n, f.ts
    return best, best_ts

def peak_concurrency(fires: list[Fire]) -> tuple[int, datetime]:
    """Max lanes simultaneously in flight (createdAt <= t < done_ts)."""
    events: list[tuple[datetime, int]] = []
    for f in fires:
        end = f.done_ts or datetime.now(timezone.utc)
        events += [(f.ts, 1), (max(end, f.ts), -1)]
    events.sort(key=lambda e: (e[0], e[1]))  # starts before ends at equal ts
    cur = best = 0
    best_ts = datetime.min.replace(tzinfo=timezone.utc)
    for ts, delta in events:
        cur += delta
        if cur > best:
            best, best_ts = cur, ts
    return best, best_ts

def token_estimate(fires: list[Fire]) -> dict:
    """Recorded vs extrapolated. Recorded = harness bytes; extrapolated applies
    the completed-agent mean to unrecorded fires (failed/running carry None)."""
    recorded = [f for f in fires if f.tokens is not None]
    unrecorded = [f for f in fires if f.tokens is None]
    total = sum(f.tokens for f in recorded)
    mean = total // len(recorded) if recorded else 0
    return {"recorded_tokens": total, "recorded_fires": len(recorded),
            "unrecorded_fires": len(unrecorded), "mean_per_recorded": mean,
            "extrapolated_unrecorded": mean * len(unrecorded),
            "estimated_total": total + mean * len(unrecorded)}

def current_shape(running_now: int, walls_recent: list[WallMoment],
                  now: datetime | None = None) -> str:
    """Live signal: running width + walls in the LAST HOUR only (decay law: a
    3-hour-old wall does not HOLD a clean window). Filter lives here."""
    now = now or datetime.now(timezone.utc)
    last_hour = [w for w in walls_recent if w.ts > now - timedelta(hours=1)]
    if last_hour and any("1308" in w.codes for w in last_hour):
        return "RED"
    if last_hour or running_now >= FIRST_1302_WIDTH:
        return "AMBER"
    return "GREEN"

def verdict_for(current_count: int, current_running: int, walls_in_window: list[WallMoment],
                peak_window: int, peak_conc: int, hours: int) -> tuple[str, str]:
    """Day-shape verdict from the measured envelopes (the exit-code carrier);
    RED = the day's dispatch shape needs correction, not necessarily a HOLD
    this second (see current_shape for the live signal)."""
    shape_width = max(peak_conc, current_running)
    saw1308 = any("1308" in w.codes for w in walls_in_window)
    saw1302 = any("1302" in w.codes for w in walls_in_window)
    if saw1308 or shape_width >= RED_WIDTH or peak_window >= RED_WIDTH + 4:
        verdict = "RED"
    elif shape_width >= FIRST_1302_WIDTH or saw1302 \
            or peak_window >= HOLD_BURST_WIDTH + 4:
        verdict = "AMBER"
    else:
        verdict = "GREEN"
    hold_line = (f"HOLD threshold: no new waves when trailing-{hours}h fires >= "
                 f"{HOLD_BURST_WIDTH} or any 1302/1302-adjacent death inside the last "
                 f"hour; stagger 6-8 wide; proven clean shape 8-{GREEN_CEILING} "
                 f"sustained (RED at {RED_WIDTH}-at-once; first 1302s ~{FIRST_1302_WIDTH}"
                 f"-wide).")
    return verdict, hold_line

def build_report(agents_root: Path, repo_root: Path, day: str, hours: int,
                 now: datetime | None = None) -> Report:
    now = now or datetime.now(timezone.utc)
    fires = load_fires(agents_root, day)
    if not fires:
        raise SystemExit(2)
    walls = cluster_walls(fires)
    rep = Report(day=day, fires=fires, walls=walls,
                 receipt_hits=grep_receipts(repo_root, day),
                 drop_rows=load_drop_rows(repo_root, day))
    window_start = now - timedelta(hours=hours)
    in_window = [f for f in fires if f.ts > window_start]
    running = [f for f in fires if f.status == "running"]
    walls_in_window = [w for w in walls if w.ts > window_start]
    pw, pw_ts = peak_width(fires, hours)
    pc, pc_ts = peak_concurrency(fires)
    rep.verdict, rep.hold_line = verdict_for(len(in_window), len(running),
                                             walls_in_window, pw, pc, hours)
    rep.stats = {
        "current_window_fires": len(in_window),
        "current_window_start": window_start.isoformat(),
        "running_now": len(running),
        "current_shape": current_shape(len(running), walls, now),
        "walls_last_hour": sum(1 for w in walls if w.ts > now - timedelta(hours=1)),
        "fires_today": len(fires),
        "completed": sum(1 for f in fires if f.status == "completed"),
        "failed": sum(1 for f in fires if f.status == "failed"),
        "peak_window": pw, "peak_window_at": pw_ts.isoformat(),
        "peak_concurrency": pc, "peak_concurrency_at": pc_ts.isoformat(),
        "walls_today": len(walls), "wall_deaths_today": sum(len(w.lanes) for w in walls),
        "tokens": token_estimate(fires),
    }
    return rep

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="window-quota ledger v0")
    ap.add_argument("--day", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--hours", type=int, default=WINDOW_HOURS_DEFAULT)
    ap.add_argument("--agents-root", default=str(Path.home() / ".zcode" / "cli" / "agents"))
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    agents_root, repo_root = Path(args.agents_root), Path(args.repo_root)
    if not agents_root.is_dir():
        print(f"cannot verify: agents root missing: {agents_root}", file=sys.stderr)
        return 2
    try:
        rep = build_report(agents_root, repo_root, args.day, args.hours)
    except SystemExit as e:
        if e.code == 2:
            print(f"cannot verify: no lane-fire records on {args.day}", file=sys.stderr)
        return 2
    if args.json:
        print(render_json(rep))
    else:
        print(render_markdown(rep, args.hours))
    return 1 if rep.verdict == "RED" else 0

if __name__ == "__main__":
    raise SystemExit(main())
