"""breath_watchdog - alert when the newest breath (commit-sweeper sweep) is stale.

Read-only on git (uses `git --no-optional-locks log`, never takes index.lock).
Freshness source, in order: logs/breath_ledger.jsonl last row (fix 1), else the
last "sweep start" line of logs/commit_sweeper_task.log, else the newest
"commit sweeper:" commit time.
Alert organ: the existing fleet NOTICE channel (mag.fleet_report.file_report,
kind=NOTICE, category=lane_down) - no new channel. One NOTICE per stale
episode; on recovery files a cancelling NOTICE. Episode state lives in
logs/breath_watchdog.state.json (gitignored; outside the conftest fence).

CLI: python -m tools.breath_watchdog [--max-age-min 15] [--dry]
$0, no LLM, no network.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
LEDGER = ROOT / "logs" / "breath_ledger.jsonl"
TASK_LOG = ROOT / "logs" / "commit_sweeper_task.log"
STATE = ROOT / "logs" / "breath_watchdog.state.json"
SEAT = "breath-watchdog"
START_RE = re.compile(r"^=== (\S+) sweep start ===")


def _parse(ts: str) -> datetime | None:
    try:
        d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _tail_lines(path: Path, n_bytes: int = 65536) -> list[str]:
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - n_bytes))
            return f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return []


def newest_breath() -> tuple[datetime | None, str]:
    for line in reversed(_tail_lines(LEDGER)):
        try:
            d = _parse(json.loads(line).get("start", ""))
        except ValueError:
            continue
        if d:
            return d, "breath_ledger"
    for line in reversed(_tail_lines(TASK_LOG)):
        m = START_RE.match(line.lstrip("\ufeff"))
        if m and (d := _parse(m.group(1))):
            return d, "commit_sweeper_task.log"
    try:
        out = subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%cI",
                              "--grep=^commit sweeper:"], cwd=str(ROOT), capture_output=True,
                             text=True, timeout=60).stdout.strip()
        if out and (d := _parse(out)):
            return d, "git log"
    except (OSError, subprocess.SubprocessError):
        pass
    return None, "none"


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1), encoding="utf-8")


def _file_notice(report: dict, dry: bool) -> dict:
    if dry:
        return {"dry": True, "would_file": report}
    from mag.fleet_report import file_report
    return file_report(seat=SEAT, kind="NOTICE", report=report, model="none")


def check(max_age_min: float = 15.0, dry: bool = False, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    last, source = newest_breath()
    age_min = None if last is None else (now - last).total_seconds() / 60.0
    stale = age_min is None or age_min > max_age_min
    st = _load_state()
    out = {"now": now.isoformat(), "last_breath": last.isoformat() if last else None,
           "source": source, "age_min": None if age_min is None else round(age_min, 1),
           "stale": stale, "open_notice": st.get("open_notice")}
    if stale and not st.get("open_notice"):
        nid = "N-" + now.strftime("%Y%m%d") + "-breath-stale-" + now.strftime("%H%M")
        rep = {"notice_id": nid, "category": "lane_down",
               "subject": f"breath stale: newest sweep {out['age_min']} min old (>{max_age_min:g})",
               "affects": ["MagCommitSweeper", "tools/commit_sweeper.py", "git chain"],
               "action_required": ("Check `schtasks /Query /TN MagCommitSweeper /V`, the tail of "
                                   "logs/commit_sweeper_task.log, and whether .git/index.lock is "
                                   "held. Never remove the lock by force (seat-ops law)."),
               "in_force_until": "until_cancelled"}
        out["filed"] = _file_notice(rep, dry)
        if not dry:
            st["open_notice"] = nid
    elif not stale and st.get("open_notice"):
        nid = "N-" + now.strftime("%Y%m%d") + "-breath-ok-" + now.strftime("%H%M")
        rep = {"notice_id": nid, "category": "lane_down", "cancels": st["open_notice"],
               "subject": f"breath recovered: newest sweep {out['age_min']} min old",
               "affects": ["MagCommitSweeper"], "action_required": "none",
               "in_force_until": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
        out["filed"] = _file_notice(rep, dry)
        if not dry:
            st.pop("open_notice", None)
    st["last_check"] = out["now"]
    if not dry:
        _save_state(st)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-min", type=float, default=15.0)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    res = check(a.max_age_min, a.dry)
    print(json.dumps(res, indent=1, default=str))
    return 2 if res["stale"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
