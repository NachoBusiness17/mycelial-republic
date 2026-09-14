"""usage_meter_sweep — the nightly watchdog the usage-meter salon (09-04) called for.

LAW (salon verdict, memory/runs/salons/usage_meter_salon_20260904): no surface ever compared
BURN to OUTPUT. The zcode seat's own meter (~/.zcode/cli/db/db.sqlite — the usage tab) was
per-turn on disk the whole time while a zombie 10-min tick burned 740M no-op premium tokens.
This script is the fix: one pass, pure local, ZERO model calls, computes per-session
output-ratio and flags violators of the minted laws. Wired into the night shift (a $0 flash
session) — never a premium heartbeat, or it becomes the thing it watches for.

Laws enforced (thresholds = the salon's, first cut 2026-09-04):
  OUTPUT-RATIO   premium no-op turns (output<200 tok) >50% of a session's premium burn, or
                 useful_output/billed <0.01 over its last active day  -> FLAG retire
  PIN-EXPIRY     premium session with last useful post (CONVO/room/file write NOT checked
                 here — proxied by output>=1000 turns) older than 72h               -> FLAG demote
  CONTEXT-DEBT   compaction count >3x the session's big-output turns                 -> FLAG retire

Output: watch/usage_sweeps/USAGE_SWEEP_<date>.md + one room.jsonl row (kind: usage.sweep).
Exit 0 clean / 1 violations found (night shift logs, never blocks).
Schema: usage_meter_sweep.v1
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "watch" / "usage_sweeps"
ROOM = ROOT / "watch" / "room.jsonl"
SCHEMA = "usage_meter_sweep.v1"
PREMIUM = ("GLM-5.3",)  # paid models; flash family is the free lane


def sweep(now: datetime) -> tuple[list[dict], dict]:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT session_id, agent,
                  count(*) AS calls,
                  sum(computed_total_tokens) AS billed,
                  sum(CASE WHEN output_tokens < 200 THEN computed_total_tokens ELSE 0 END) AS noop_billed,
                  sum(CASE WHEN output_tokens >= 1000 THEN 1 ELSE 0 END) AS big_out_turns,
                  sum(CASE WHEN query_source = 'compact' THEN 1 ELSE 0 END) AS compacts,
                  max(started_at) AS last_ms
           FROM model_usage
           WHERE status = 'completed' AND model_id IN (%s)
           GROUP BY session_id HAVING billed > 10_000_000
           ORDER BY billed DESC""" % ",".join("?" * len(PREMIUM)),
        PREMIUM,
    ).fetchall()
    titles = dict(con.execute("SELECT id, title FROM session"))
    con.close()

    flags: list[dict] = []
    for sid, agent, calls, billed, noop, big_turns, compacts, last_ms in rows:
        if billed is None:
            continue
        noop_ratio = (noop or 0) / billed
        useful_ratio = max(big_turns, 1) * 2000 / billed  # ~2K tok per useful turn, floor 1
        age_h = (now.timestamp() * 1000 - (last_ms or 0)) / 3_600_000
        f = []
        if noop_ratio > 0.5:
            f.append(f"OUTPUT-RATIO: {noop_ratio:.0%} of premium burn was <200-tok no-ops (law: <50%)")
        if useful_ratio < 0.01:
            f.append(f"OUTPUT-RATIO: useful/billed ~{useful_ratio:.1e} (law: >=0.01)")
        if age_h > 72 and big_turns == 0:
            f.append(f"PIN-EXPIRY: premium, silent {age_h:.0f}h, zero big-output turns (law: demote at 72h)")
        if compacts > 3 * max(big_turns, 1):
            f.append(f"CONTEXT-DEBT: {compacts} compactions vs {big_turns} big-output turns (law: <=3x)")
        if f:
            flags.append({
                "session": sid, "title": (titles.get(sid) or "?")[:60], "agent": agent,
                "calls": calls, "billed_M": round(billed / 1e6, 1),
                "noop_pct": round(noop_ratio * 100), "age_h": round(age_h), "laws": f,
            })
    totals = {"premium_sessions_gt10M": len(rows),
              "premium_billed_B": round(sum(r[3] or 0 for r in rows) / 1e9, 2)}
    return flags, totals


def main() -> int:
    now = datetime.now(timezone.utc)
    flags, totals = sweep(now)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = now.strftime("%Y%m%d")
    lines = [
        f"# USAGE SWEEP {now.date()} ({SCHEMA})",
        f"premium sessions >10M tok: {totals['premium_sessions_gt10M']} · "
        f"premium billed: {totals['premium_billed_B']}B tok lifetime",
        "",
    ]
    if flags:
        lines.append(f"## FLAGS ({len(flags)}) — retire/demote by law")
        for fl in flags:
            lines.append(f"- `{fl['session'][:16]}…` **{fl['title']}** — {fl['billed_M']}M tok, "
                         f"{fl['noop_pct']}% no-op, age {fl['age_h']}h")
            for law in fl["laws"]:
                lines.append(f"  - {law}")
    else:
        lines.append("## FLAGS (0) — clean sweep, laws holding")
    (OUT_DIR / f"USAGE_SWEEP_{date}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    row = {"ts": now.isoformat(), "seat": "usage-meter-sweep", "kind": "usage.sweep",
           "thread": "usage_meter", "schema": SCHEMA,
           "text": f"flags={len(flags)} premium_billed={totals['premium_billed_B']}B "
                   f"sessions={totals['premium_sessions_gt10M']} "
                   + ("; ".join(f["session"][:14] + ":" + str(len(f["laws"])) for f in flags[:4])
                      if flags else "clean")}
    with ROOM.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")

    print("\n".join(lines))
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
