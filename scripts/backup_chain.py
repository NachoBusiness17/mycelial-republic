"""backup_chain.py — standing daily backup of the verkle ground truth (2026-08-25).

Sacred-cow fix: `memory/biography/**` is gitignored for opsec, which is right — but that meant
the chain + knots had ZERO backup, and the Aug 8-13 lost-update race turned ~1,040 rows into
`evidence_lost`. The backup pattern already exists (`memory/biography_backup_20260825`, by the
zcode seat); this makes it STANDING and rotating.

- Rotates to `memory/biography_backup_YYYYMMDD/`
- Runs under `verkle_lock` so we never copy mid-append
- Idempotent: skips if today's backup already exists (--force overrides)
- Prunes to the newest N (default 7)

CLI:
  python scripts/backup_chain.py            # backup if due (once per day)
  python scripts/backup_chain.py --force    # always backup now
  python scripts/backup_chain.py --status   # list existing backups, no writes
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BACKUP_ROOT = ROOT / "memory" / "biography_backup"
KEEP = 7
PREFIX = "biography_backup_"


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _backup_dirs() -> list[Path]:
    if not BACKUP_ROOT.is_dir():
        return []
    out = []
    for p in BACKUP_ROOT.iterdir():
        if p.is_dir() and p.name.startswith(PREFIX) and re.fullmatch(r"biography_backup_\d{8}", p.name):
            out.append(p)
    return sorted(out)


def backup(*, force: bool = False) -> dict:
    """Copy chain + knots to today's rotating backup dir. Returns a JSON summary."""
    from mag.verkle_knot import CHAIN, KNOTS, verkle_lock

    with verkle_lock():
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        dest = BACKUP_ROOT / f"{PREFIX}{_today()}"
        if dest.is_dir() and not force:
            n = sum(1 for _ in dest.rglob("*") if _.is_file())
            return {"ok": True, "skipped": "already_today", "dest": str(dest), "files": n}

        # copy the chain file(s) first (the ground truth), then the knots
        dest.mkdir(parents=True, exist_ok=True)
        files = 0
        for src in (CHAIN,):
            if src.is_file():
                shutil.copy2(src, dest / src.name)
                files += 1
        # tip / evolution files if present
        for pat in ("verkle_tip.json", "verkle_evolution.jsonl", "verkle_roots.jsonl"):
            p = CHAIN.parent / pat
            if p.is_file():
                shutil.copy2(p, dest / p.name)
                files += 1
        # knots: copy any knot files not already present (idempotent re-run safe)
        if KNOTS.is_dir():
            (dest / "knots").mkdir(parents=True, exist_ok=True)
            for k in KNOTS.iterdir():
                if k.is_file():
                    t = dest / "knots" / k.name
                    if not t.exists():
                        shutil.copy2(k, t)
                        files += 1
        # prune to newest KEEP
        all_b = _backup_dirs()
        removed = []
        for old in all_b[:-KEEP] if len(all_b) > KEEP else []:
            shutil.rmtree(old, ignore_errors=True)
            removed.append(old.name)
        return {"ok": True, "dest": str(dest), "files": files, "removed": removed,
                "kept": len(_backup_dirs())}


def status() -> dict:
    dirs = _backup_dirs()
    rows = []
    for d in dirs:
        n = sum(1 for _ in d.rglob("*") if _.is_file())
        rows.append({"dir": d.name, "files": n})
    return {"ok": True, "backups": rows}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="backup-chain")
    ap.add_argument("--force", action="store_true", help="backup even if today's exists")
    ap.add_argument("--status", action="store_true", help="list backups, no writes")
    a = ap.parse_args()
    if a.status:
        print(json.dumps(status(), indent=2, default=str))
    else:
        res = backup(force=a.force)
        print(json.dumps(res, indent=2, default=str))
        try:
            from mag import chain_guard
            print("--- chain canary ---")
            print(json.dumps(chain_guard.check(), indent=2, default=str))
        except Exception as e:  # noqa: BLE001
            print("canary check failed: " + str(e))
