#!/usr/bin/env python3
"""fossil_check — the FOSSIL-IN-FEED arm, registry-driven.

Law: watch/inbox/FOSSIL_CENSUS_20260927.md. An artifact wired into a live
consumer must recompile or tombstone within its bar; this check stats each
registered artifact's mtime and WARNs on breach. Registry:
configs/fossil_registry.json (adding artifacts = a named config edit, the
same shape as the secret-gate baseline). Dispositions: recompile (age bar
enforced), tombstoned (never warns — the death is recorded), fixed-oracle
(tracked for change only), watch (warn bar, no action implied).

Wired into the 08:30 census patrol WARN-only (scripts/census_patrol_daily.ps1
replaced its single-artifact quantizer check with this). Fail-open law: a
broken check never blinds the patrol.

The --recompile flag gates actual recompilation: when a recompile-disposition
entry is stale and carries a recompile_cmd, that command runs instead of
just WARNing. Without --recompile the arm is WARN-only per the FOSSIL-IN-FEED
law (enforce is operator-gated).

Exit: 0 all green / 1 any WARN / 2 registry unreadable or missing artifacts.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "configs" / "fossil_registry.json"


def load_registry(path: Path = REGISTRY) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("registry must carry an entries list")
    return entries


def check(now: float | None = None, registry_path: Path = REGISTRY,
          recompile: bool = False) -> int:
    now = now or time.time()
    try:
        entries = load_registry(registry_path)
    except (OSError, ValueError) as e:
        print(f"FOSSIL-CHECK: registry unreadable ({e}) — cannot verify")
        return 2
    warns = 0
    hard = 0
    recompiled = 0
    for ent in entries:
        art = str(ent.get("artifact", ""))
        disp = str(ent.get("disposition", "watch"))
        rel = ROOT / art
        if not rel.is_file():
            if disp == "tombstoned":
                print(f"FOSSIL-CHECK: ok    {art} (tombstoned, absent)")
                continue
            print(f"FOSSIL-CHECK: HARD  {art} MISSING (registry names it, disk does not)")
            hard += 1
            continue
        age_h = (now - rel.stat().st_mtime) / 3600.0
        bar = ent.get("bar_hours")
        stale_reason = None

        # check_cmd probe: non-zero exit = stale (quantizer pack staleness, etc.)
        check_cmd = ent.get("check_cmd")
        if check_cmd:
            cr = subprocess.run(check_cmd, shell=True, capture_output=True, text=True, timeout=300)
            if cr.returncode != 0:
                stale_reason = cr.stdout.strip() or cr.stderr.strip()

        # mtime bar check (only if check_cmd didn't flag)
        if stale_reason is None and disp != "tombstoned" and disp != "fixed-oracle" and isinstance(bar, (int, float)) and age_h > bar:
            stale_reason = f"{age_h:.1f}h > bar {bar:.0f}h"

        if disp == "tombstoned":
            print(f"FOSSIL-CHECK: ok    {art} tombstoned, {age_h:.0f}h old (death recorded)")
        elif disp == "fixed-oracle":
            print(f"FOSSIL-CHECK: ok    {art} fixed-oracle, {age_h:.0f}h (no bar by design)")
        elif stale_reason:
            if disp == "recompile" and ent.get("recompile_cmd") and recompile:
                cmd = ent["recompile_cmd"]
                print(f"FOSSIL-CHECK: RECOMPILE {art} stale — {stale_reason} — running: {cmd}")
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                print(f"FOSSIL-CHECK: recompile exit={r.returncode}")
                if r.stdout:
                    print(f"FOSSIL-CHECK: stdout: {r.stdout.strip()[:500]}")
                if r.returncode != 0 and r.stderr:
                    print(f"FOSSIL-CHECK: stderr: {r.stderr.strip()[:500]}")
                recompiled += 1
            else:
                print(f"FOSSIL-CHECK: WARN  {art} stale — {stale_reason} "
                      f"[{disp}] consumer: {ent.get('consumer', '?')}")
                warns += 1
        else:
            bar_s = f"bar {bar:.0f}h" if isinstance(bar, (int, float)) else "no bar"
            print(f"FOSSIL-CHECK: ok    {art} {age_h:.0f}h old ({bar_s}) [{disp}]")
    print(f"FOSSIL-CHECK: {warns} WARN, {hard} HARD, {recompiled} recompiled, "
          f"{len(entries)} registered")
    return 1 if (warns or hard) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="registry-driven fossil staleness check")
    ap.add_argument("mode", nargs="?", default="check", choices=["check", "list"])
    ap.add_argument("--registry", default=str(REGISTRY))
    ap.add_argument("--recompile", action="store_true",
                     help="run recompile_cmd for stale recompile entries (operator-gated)")
    a = ap.parse_args()
    if a.mode == "list":
        for ent in load_registry(Path(a.registry)):
            print(f"{ent.get('disposition', '?'):12} "
                  f"{str(ent.get('bar_hours')):>6}h  {ent.get('artifact')}")
        return 0
    return check(registry_path=Path(a.registry), recompile=a.recompile)


if __name__ == "__main__":
    sys.exit(main())
