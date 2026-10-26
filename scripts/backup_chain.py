"""backup_chain.py - standing daily backup of the verkle ground truth (2026-08-25).

Sacred-cow fix: `memory/biography/**` is gitignored for opsec, which is right - but that meant
the chain + knots had ZERO backup, and the Aug 8-13 lost-update race turned ~1,040 rows into
`evidence_lost`. The backup pattern already exists (`memory/biography_backup_20260825`, by the
zcode seat); this makes it STANDING and rotating.

- Rotates to `memory/biography_backup/biography_backup_YYYYMMDD/`
- Runs under `verkle_lock` so we never copy mid-append
- Idempotent: skips if today's backup already exists AND verified complete (--force overrides)
- Prunes to the newest N (default 7) VERIFIED-COMPLETE backups

COMPLETENESS (2026-10-15, after the 20261014 / 20261015 folders held 3,370 and 219 of ~48k
knots and nothing noticed): a backup is only real once it has been verified against the source.
- An INCOMPLETE marker (BACKUP_INCOMPLETE.json) is written into the folder BEFORE any copy, so a
  process that is killed mid-copy (no except/finally runs) still leaves the folder marked.
- After copying, verify(): chain sha256 and tip sha256 must equal the source; knot file count and
  knot bytes must be >= 99% of the source. Pass -> BACKUP_COMPLETE.json manifest, marker removed.
  Fail -> marker kept (state=failed_verification) and BackupIncomplete is raised (CLI exit 2).
- A folder without BACKUP_COMPLETE.json is never "already done": the next run RESUMES into it
  (copies only missing / size-mismatched knots, refreshes chain + tip) and re-verifies. So a
  truncated copy is no longer frozen for the rest of the UTC day.
- Only verified-complete folders count toward KEEP and only they are ever pruned. Unverified
  folders (legacy pre-2026-10-15, or incomplete) are never auto-deleted.
- alarm() appends an alert block to memory/attention.md (the same channel the census / meter /
  tip-witness patrols use) and a line to logs/backup_chain.log.

PINNED (2026-10-15): biography_backup_20261004 is never pruned and never counted.

CLI:
  python scripts/backup_chain.py            # backup if due; resumes an unverified folder
  python scripts/backup_chain.py --force    # re-copy + re-verify today's folder now
  python scripts/backup_chain.py --status   # list backups + verification state, no writes
  exit 0 = verified complete, 2 = INCOMPLETE (alarm written)
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BACKUP_ROOT = ROOT / "memory" / "biography_backup"
ATTENTION = ROOT / "memory" / "attention.md"
LOG = ROOT / "logs" / "backup_chain.log"
KEEP = 7
PREFIX = "biography_backup_"
INCOMPLETE_MARKER = "BACKUP_INCOMPLETE.json"
COMPLETE_MANIFEST = "BACKUP_COMPLETE.json"
KNOT_MIN_RATIO = 0.99
# PINNED (2026-10-15): never pruned and not counted toward KEEP.
# biography_backup_20261004 is the last known-good chain (11,218 rows, verifies
# OK) from before the 2026-10-07/09 test-fixture overwrite; it is the restore base in
# CHAIN_RESTORE_PLAN.md (vault copy: C:\MagChainVault\20261014). Unpin only after
# the restore is done and verified, by operator decision.
PINNED = frozenset({"biography_backup_20261004"})


class BackupIncomplete(RuntimeError):
    """The backup folder does not match the source; it is marked and not counted."""

    def __init__(self, summary: dict):
        self.summary = summary
        super().__init__("chain backup INCOMPLETE: " + "; ".join(summary.get("problems") or ["?"]))


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _backup_dirs() -> list[Path]:
    if not BACKUP_ROOT.is_dir():
        return []
    out = []
    for p in BACKUP_ROOT.iterdir():
        if p.is_dir() and p.name.startswith(PREFIX) and re.fullmatch(r"biography_backup_\d{8}", p.name):
            out.append(p)
    return sorted(out)


def is_complete(d: Path) -> bool:
    """Verified-complete: has the manifest and no leftover incomplete marker."""
    return (d / COMPLETE_MANIFEST).is_file() and not (d / INCOMPLETE_MARKER).is_file()


def _sha256(p: Path) -> str | None:
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _knot_stats(d: Path) -> tuple[int, int]:
    """(count, bytes) of top-level regular files - the same set backup() copies."""
    n = b = 0
    if d.is_dir():
        for k in d.iterdir():
            if k.is_file():
                n += 1
                b += k.stat().st_size
    return n, b


def _write_json(p: Path, obj: dict) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")
    os.replace(tmp, p)


def verify(dest: Path, chain: Path, knots: Path) -> dict:
    """Compare a backup folder against the source. Read-only on both sides."""
    tip = chain.parent / "verkle_tip.json"
    src_chain, bak_chain = _sha256(chain), _sha256(dest / chain.name)
    src_tip, bak_tip = _sha256(tip), _sha256(dest / tip.name)
    src_n, src_b = _knot_stats(knots)
    bak_n, bak_b = _knot_stats(dest / "knots")
    problems = []
    if src_chain is None:
        problems.append("source chain missing")
    elif bak_chain != src_chain:
        problems.append("chain sha256 differs")
    if src_tip is not None and bak_tip != src_tip:
        problems.append("tip sha256 differs")
    if src_n and bak_n < KNOT_MIN_RATIO * src_n:
        problems.append(f"knots {bak_n}/{src_n} files (< {KNOT_MIN_RATIO:.0%})")
    if src_b and bak_b < KNOT_MIN_RATIO * src_b:
        problems.append(f"knots {bak_b}/{src_b} bytes (< {KNOT_MIN_RATIO:.0%})")
    return {"ok": not problems, "problems": problems, "verified_at": _now(),
            "chain_sha256": {"source": src_chain, "backup": bak_chain},
            "tip_sha256": {"source": src_tip, "backup": bak_tip},
            "knots": {"source_files": src_n, "backup_files": bak_n,
                      "source_bytes": src_b, "backup_bytes": bak_b,
                      "file_ratio": round(bak_n / src_n, 4) if src_n else None}}


def _log(msg: str) -> None:
    line = f"[{_now()}] {msg}"
    print(f"[backup-chain] {msg}", flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def alarm(verdict: str, detail: dict | None = None) -> None:
    """Loud + visible: log line + alert block in memory/attention.md (census/meter patrol channel)."""
    _log(f"ALARM {verdict}")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d = detail or {}
    block = (
        "\n---\n\n"
        f"### Chain backup patrol fired ({stamp})\n\n"
        f"- verdict: {verdict}\n"
        f"- folder: {d.get('dest', '?')}\n"
        f"- check: {json.dumps(d.get('verify') or d.get('marker') or {}, default=str)[:600]}\n"
        "- log: logs/backup_chain.log\n"
        "- response: run `.venv\\Scripts\\python.exe scripts\\backup_chain.py` by hand; it resumes the "
        "unverified folder and exits 0 only when chain + tip sha256 match and knots >= 99% of source. "
        "An incomplete folder is never counted toward keep-7 or pruned; do not treat it as a restore base.\n"
    )
    try:
        ATTENTION.parent.mkdir(parents=True, exist_ok=True)
        with ATTENTION.open("a", encoding="utf-8") as f:
            f.write(block)
    except OSError as e:
        _log(f"could not append alarm to {ATTENTION}: {e}")


def _copy_if_needed(src: Path, dst: Path) -> bool:
    try:
        if dst.is_file() and dst.stat().st_size == src.stat().st_size:
            return False
    except OSError:
        pass
    shutil.copy2(src, dst)
    return True


def backup(*, force: bool = False) -> dict:
    """Copy chain + knots to today's backup dir, verify it, prune. Raises BackupIncomplete."""
    from mag.verkle_knot import CHAIN, KNOTS, verkle_lock

    with verkle_lock():
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        dest = BACKUP_ROOT / f"{PREFIX}{_today()}"
        resumed_from = None
        if dest.is_dir():
            if is_complete(dest) and not force:
                _log(f"SKIP {dest.name} already verified complete today")
                return {"ok": True, "skipped": "already_today", "dest": str(dest), "verified": True}
            marker = dest / INCOMPLETE_MARKER
            if marker.is_file():
                try:
                    resumed_from = json.loads(marker.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    resumed_from = {"state": "unreadable marker"}
            elif not is_complete(dest):
                resumed_from = {"state": "unverified folder (no manifest)"}
        dest.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            (dest / COMPLETE_MANIFEST).unlink()
        marker = dest / INCOMPLETE_MARKER
        _write_json(marker, {"state": "copying", "pid": os.getpid(), "started": _now(),
                             "resumed_from": resumed_from})
        files = 0
        try:
            # the chain + tip are always refreshed (they may have moved since a partial attempt)
            if CHAIN.is_file():
                shutil.copy2(CHAIN, dest / CHAIN.name)
                files += 1
            for pat in ("verkle_tip.json", "verkle_evolution.jsonl", "verkle_roots.jsonl"):
                p = CHAIN.parent / pat
                if p.is_file():
                    shutil.copy2(p, dest / p.name)
                    files += 1
            # knots: copy missing or size-mismatched (a kill can leave a short last file)
            if KNOTS.is_dir():
                (dest / "knots").mkdir(parents=True, exist_ok=True)
                for k in KNOTS.iterdir():
                    if k.is_file() and _copy_if_needed(k, dest / "knots" / k.name):
                        files += 1
        except BaseException as e:  # noqa: BLE001 - mark, then re-raise (incl. KeyboardInterrupt)
            with contextlib.suppress(Exception):
                _write_json(marker, {"state": "copy_failed", "pid": os.getpid(), "error": repr(e)[:300],
                                     "at": _now(), "resumed_from": resumed_from})
            raise
        v = verify(dest, CHAIN, KNOTS)
        summary = {"ok": v["ok"], "dest": str(dest), "files_copied": files, "verify": v,
                   "problems": v["problems"], "resumed_from": resumed_from}
        if not v["ok"]:
            _write_json(marker, {"state": "failed_verification", "pid": os.getpid(), "at": _now(),
                                 "verify": v, "resumed_from": resumed_from})
            summary["counted"] = False
            raise BackupIncomplete(summary)
        _write_json(dest / COMPLETE_MANIFEST, {"schema": "backup_chain.complete.v1", **v,
                                               "files_copied": files, "resumed_from": resumed_from})
        marker.unlink()
        # prune to newest KEEP verified-complete backups (pinned + unverified are exempt, uncounted)
        all_b = [d for d in _backup_dirs() if d.name not in PINNED and is_complete(d)]
        removed = []
        for old in all_b[:-KEEP] if len(all_b) > KEEP else []:
            shutil.rmtree(old, ignore_errors=True)
            removed.append(old.name)
        summary.update({"removed": removed, "kept": len(_backup_dirs()), "counted": True})
        _log(f"COMPLETE {dest.name} knots {v['knots']['backup_files']}/{v['knots']['source_files']} "
             f"chain {str(v['chain_sha256']['backup'])[:12]} tip {str(v['tip_sha256']['backup'])[:12]} "
             f"copied {files} pruned {removed or '-'}")
        return summary


def status() -> dict:
    rows = []
    for d in _backup_dirs():
        n = sum(1 for _ in d.rglob("*") if _.is_file())
        state = ("PINNED" if d.name in PINNED else "complete" if is_complete(d)
                 else "INCOMPLETE" if (d / INCOMPLETE_MARKER).is_file() else "unverified")
        rows.append({"dir": d.name, "files": n, "state": state})
    return {"ok": True, "backups": rows}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="backup-chain")
    ap.add_argument("--force", action="store_true", help="re-copy + re-verify today's folder")
    ap.add_argument("--status", action="store_true", help="list backups, no writes")
    a = ap.parse_args()
    if a.status:
        print(json.dumps(status(), indent=2, default=str))
        sys.exit(0)
    try:
        res = backup(force=a.force)
    except BackupIncomplete as e:
        alarm(f"INCOMPLETE: {'; '.join(e.summary.get('problems') or ['?'])}",
              e.summary)
        print(json.dumps(e.summary, indent=2, default=str))
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        alarm(f"FAILED: {type(e).__name__}: {str(e)[:200]}", {})
        raise
    if res.get("resumed_from"):
        alarm(f"RECOVERED: previous attempt left an unverified folder; resumed and verified OK "
              f"({res['verify']['knots']['backup_files']}/{res['verify']['knots']['source_files']} knots)", res)
    print(json.dumps(res, indent=2, default=str))
    try:
        from mag import chain_guard
        print("--- chain canary ---")
        print(json.dumps(chain_guard.check(), indent=2, default=str))
    except Exception as e:  # noqa: BLE001
        print("canary check failed: " + str(e))
