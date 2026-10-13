"""secret_scan_weekly -- the B2-351 scheduled beat over B2_73's scanner.

CAUSE (B2-351, 2026-09-26): the scanner is a zero-cost local command and
nothing ran it on a schedule, so the next dump would land silently.
FIX: weekly schtask MagSecretScanWeekly (Monday 06:40 local) runs the B2-73
scanner, then (1) appends a summary row to watch/inbox/SECRET_SCAN_BEAT.jsonl
(append-only, one row per run: ts, critical/high counts, results path) and
(2) when any critical/high rule count is above zero, prepends a dated alert
line at the TOP of memory/attention.md so the standing-attention surface
names it.

LOG (m8-boot-regen, morning-block-20261007): the schtask action is bare
pythonw.exe with no console and no redirect, so both observed scheduled
fires (Monday 2026-09-28 and 2026-10-05 06:40, LastTaskResult 0x1) died
leaving ZERO evidence - REDBOARD read "no log found", no beat row, results
json untouched - while hand runs passed (beat rows 2026-09-28T11:05:40Z,
2026-10-05T12:08:13Z). Cause of the scheduled-context death remains
unidentified (pythonw None-stdout ruled out by probe: sys.stdout/stderr are
real TextIOWrappers under this venv's pythonw; scanner catches per-file
OSError). The wrapper now writes logs/secret_scan_weekly.log on
START/END/FAIL and appends a status=failed beat row on exception, so the
next red is autopsible. Exit contract unchanged: 0 ok, 1 failed.

RUN: .venv/Scripts/python.exe scripts/secret_scan_weekly.py
"""
from __future__ import annotations

import datetime
import io
import json
import runpy
import os
import sys
import traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANNER = os.path.join(REPO, "watch", "inbox", "burn_wave_20260926",
                       "B2_73_secret_scan.py")
BEAT = os.path.join(REPO, "watch", "inbox", "SECRET_SCAN_BEAT.jsonl")
ATTENTION = os.path.join(REPO, "memory", "attention.md")
LOG = os.path.join(REPO, "logs", "secret_scan_weekly.log")


def _log(msg: str) -> None:
    """Own log surface (m8-boot-regen, morning-block-20261007): the task
    wrote no log anywhere, so its scheduled-context exit 1s were unauditable.
    Best-effort by design: a log write must never mask the scan verdict."""
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
    except OSError:
        pass


def main() -> int:
    _log("START scan (B2-73 scanner in-process over corpus/ + watch/inbox/)")
    try:
        # run the scanner in-process (it writes its own results json)
        import importlib.util
        spec = importlib.util.spec_from_file_location("b273_scan", SCANNER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
        results = json.load(open(mod.RESULTS, encoding="utf-8"))
        counts = results.get("rule_counts", {}) or {}
        sev = {r[0]: r[1] for r in mod.RULES}
        crit = sum(n for rid, n in counts.items() if sev.get(rid) == "critical")
        high = sum(n for rid, n in counts.items() if sev.get(rid) == "high")
    except Exception as e:  # noqa: BLE001 (a dead beat must name its death)
        _log("FAIL: %s: %s\n%s" % (type(e).__name__, e,
                                   traceback.format_exc().rstrip()))
        ts = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        with open(BEAT, "a", encoding="utf-8") as f:
            f.write(json.dumps(
                {"ts": ts, "schema": "secret_scan_beat.v1",
                 "status": "failed",
                 "error": "%s: %s" % (type(e).__name__, e)},
                ensure_ascii=False) + "\n")
        return 1
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = {"ts": ts, "schema": "secret_scan_beat.v1",
           "critical": crit, "high": high,
           "files_with_rule_hits": results.get("files_with_rule_hits"),
           "results": os.path.relpath(mod.RESULTS, REPO).replace("\\", "/")}
    with open(BEAT, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row))
    if crit > 0 or high > 0:
        alert = ("- [ALERT %s] secret scan beat: critical=%d high=%d, rows %s "
                 "(see %s)\n" % (ts, crit, high, json.dumps(counts), row["results"]))
        # errors=replace (m8-boot-regen, morning-block-20261007): attention.md
        # is the hot multi-writer file and carried 2 non-UTF-8 bytes (0xc7 0xf6
        # at position 57526, CP1252 mojibake) - the strict read raised
        # UnicodeDecodeError AFTER the scan succeeded and the beat row landed,
        # exiting 1 on every fire since (scheduled rows 2026-09-28T11:05:40Z
        # and 2026-10-05T12:08:13Z in SECRET_SCAN_BEAT.jsonl; the 2026-10-07
        # hand rerun reproduced byte-identical). An alert append must never
        # die on another writer's encoding; replace cleans the bytes over time.
        with open(ATTENTION, encoding="utf-8", errors="replace") as f:
            body = f.read()
        with open(ATTENTION, "w", encoding="utf-8", newline="") as f:
            f.write(alert + body)
        print("ALERT line prepended to memory/attention.md")
    _log("END ok critical=%d high=%d" % (crit, high))
    return 0


if __name__ == "__main__":
    sys.exit(main())
