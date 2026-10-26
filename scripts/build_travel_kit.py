"""Build the travel kit: the portable bag a cold machine boots the fleet from.

Tier 1 of watch/inbox/TWO_MACHINE_SYNC_20260919.md: code + live ledgers + packs
+ .env. Ore (corpora, vendored repos, media) and debris (machinery state, knot
backups, run exhaust) stay archived on the main host and answer by bounded
pointer: path + sha256. The kit carries the pointers, never the ore.

Output:
    memory/portable_bags/travel_kit_<ts>.zip            the bag (gitignored)
    memory/portable_bags/travel_kit_<ts>.manifest.json  every file + sha256,
                                                        every pointer (receipt)

Usage:
    .venv/Scripts/python.exe scripts/build_travel_kit.py           # build + verify
    .venv/Scripts/python.exe scripts/build_travel_kit.py --verify  # verify newest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "memory" / "portable_bags"
MAX_FILE_BYTES = 8 * 1024 * 1024          # per-file cap for state/ledger files
POINTER_HASH_LIMIT = 64 * 1024 * 1024     # hash pointers up to this size, list bigger bare

# Whole-tree includes: code and small durable surfaces.
DIR_INCLUDES = [
    "mag", "scripts", "tools", "configs", "queue", "docs", "tests", "prompts",
    "packs", "handoff", "research", "dashboard", "training", "models",
]
# memory/ subdirs auto-include when small enough; these are kept regardless.
MEMORY_ALLOW = {"briefs"}
MEMORY_EXCLUDE = {
    "agent_state", "agent_sessions", "agent_uploads", "archive", "archaeology",
    "biography", "biography_backup", "biography_backup_20260825", "corpus",
    "dead_drops", "ghost", "ingest", "interaction_logs", "runs", "seals",
    "spore_seeds", "trash", "vault",
}
MEMORY_SMALL_FILE_LIMIT = 4000
MEMORY_SMALL_BYTES_LIMIT = 8 * 1024 * 1024

EXCLUDE_NAMES = {"__pycache__", "node_modules", ".mimosa", ".pytest_cache"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".zip")

ARCHIVE_TIERS = """\
Archive slices that stay on the main host (fetch by path + sha256 when needed):
  debris : .mimosa (390,679 files), memory/biography* + memory/ghost (441,558),
           memory/runs + agent_state + logs (~95,000)
  ore    : mine/raw (vendored repos), corpus/, memory/corpus, watch media
           (watch/inbox/mrpool_export 3.40 GB), dashboard/data fat,
           training/events.jsonl and other over-cap ledgers, .git history
"""


def _sha256(path: Path, limit: int | None = None) -> str | None:
    h = hashlib.sha256()
    total = 0
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(512 * 1024), b""):
                h.update(chunk)
                total += len(chunk)
                if limit is not None and total > limit:
                    return None
    except OSError:
        return None
    return h.hexdigest()


def _excluded(rel: Path) -> bool:
    if any(part in EXCLUDE_NAMES for part in rel.parts):
        return True
    if rel.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return any(part.startswith("travel_kit_") for part in rel.parts)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _memory_allowed_dirs() -> set[str]:
    mem = ROOT / "memory"
    allowed: set[str] = set()
    for d in sorted(mem.iterdir()) if mem.is_dir() else []:
        if not d.is_dir() or d.name in MEMORY_EXCLUDE:
            continue
        if d.name in MEMORY_ALLOW:
            allowed.add(d.name)
            continue
        files = [p for p in d.rglob("*") if p.is_file() and not _excluded(p.relative_to(ROOT))]
        size = sum(p.stat().st_size for p in files)
        if len(files) <= MEMORY_SMALL_FILE_LIMIT and size <= MEMORY_SMALL_BYTES_LIMIT:
            allowed.add(d.name)
    return allowed


def collect() -> tuple[list[Path], list[dict]]:
    """Return (included files, pointer rows) for the kit."""
    include: list[Path] = []
    pointers: list[dict] = []
    mem_allowed = _memory_allowed_dirs()

    def consider(p: Path) -> None:
        rel = p.relative_to(ROOT)
        if _excluded(rel) or rel.name.startswith("travel_kit_"):
            return
        try:
            size = p.stat().st_size
        except OSError:
            return
        if size <= MAX_FILE_BYTES:
            include.append(p)
            return
        row: dict = {"path": str(rel).replace("\\", "/"), "bytes": size}
        digest = _sha256(p, POINTER_HASH_LIMIT)
        if digest:
            row["sha256"] = digest
        pointers.append(row)

    for name in DIR_INCLUDES:
        base = ROOT / name
        if not base.exists():
            continue
        if base.is_file():
            consider(base)
            continue
        for p in base.rglob("*"):
            if p.is_file():
                consider(p)

    mem = ROOT / "memory"
    if mem.is_dir():
        for p in mem.iterdir():            # memory top-level files (ledgers, states)
            if p.is_file():
                consider(p)
        for name in sorted(mem_allowed):
            for p in (mem / name).rglob("*"):
                if p.is_file():
                    consider(p)

    for top in (ROOT / "watch", ROOT / "watch" / "inbox"):   # top-level files only
        if not top.is_dir():
            continue
        for p in top.iterdir():
            if p.is_file():
                consider(p)

    for p in sorted(ROOT.iterdir()):       # root files: AGENTS.md, main.py, .env, ...
        if p.is_file():
            consider(p)

    return sorted(set(include), key=lambda p: str(p)), pointers


def _readme() -> str:
    return (
        "TRAVEL KIT (built %s)\n\n"
        "This bag boots the fleet on a cold machine: code, live ledgers, packs, .env.\n\n"
        "Boot steps (Windows):\n"
        "  1. Unzip to the desired repo path.\n"
        "  2. powershell -ExecutionPolicy Bypass -File .\\scripts\\ensure_venv.ps1\n"
        "  3. mag.cmd doctor\n"
        "  4. mag.cmd lab  (dashboard on :8765)\n\n"
        "Ore and debris are NOT in this bag. They stay archived on the main host and\n"
        "answer by bounded pointer: every over-cap file is listed in the manifest with\n"
        "path (+ sha256 when under 64 MB). Ask the archive, verify the hash.\n\n%s" % (
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), ARCHIVE_TIERS)
    )


def build() -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    files, pointers = collect()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    zpath = OUT_DIR / f"travel_kit_{ts}.zip"
    manifest = {
        "schema": "travel_kit.v1",
        "built": _now(),
        "host": os.environ.get("COMPUTERNAME", "unknown"),
        "included": len(files),
        "pointers": len(pointers),
        "files": [],
        "pointer_rows": pointers,
    }
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("README_TRAVEL_KIT.txt", _readme())
        for p in files:
            arc = str(p.relative_to(ROOT)).replace("\\", "/")
            z.write(p, arc)
            manifest["files"].append({"path": arc, "bytes": p.stat().st_size, "sha256": _sha256(p)})
    mpath = OUT_DIR / f"travel_kit_{ts}.manifest.json"
    mpath.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"kit  : {zpath.name}  ({zpath.stat().st_size / 1048576:.1f} MB zip)")
    print(f"files: {len(files)} included, {sum(r['bytes'] for r in manifest['files']) / 1048576:.1f} MB unpacked")
    print(f"ptrs : {len(pointers)} over-cap files stay in the archive")
    print(f"manif: {mpath.name}")
    return mpath


def verify(mpath: Path) -> int:
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    zpath = mpath.parent / mpath.name.replace(".manifest.json", ".zip")
    if not zpath.is_file():
        print(f"zip missing: {zpath.name}")
        return 2
    bad = 0
    with zipfile.ZipFile(zpath) as z:
        names = set(z.namelist())
        for row in manifest["files"]:
            if row["path"] not in names:
                print(f"MISSING in zip: {row['path']}")
                bad += 1
                continue
            if hashlib.sha256(z.read(row["path"])).hexdigest() != row["sha256"]:
                print(f"HASH MISMATCH: {row['path']}")
                bad += 1
    print(f"verify: {len(manifest['files']) - bad}/{len(manifest['files'])} ok, {bad} bad")
    return 1 if bad else 0


def audit() -> int:
    """Grade the newest kit by last-touch age. Cold state = sacred-cow candidates:
    carried because some past ritual filed them, not because anything reads them."""
    import time as _time
    manifests = sorted(OUT_DIR.glob("travel_kit_*.manifest.json"))
    if not manifests:
        print("no kit found")
        return 2
    manifest = json.loads(manifests[-1].read_text(encoding="utf-8"))
    now = _time.time()
    buckets = [("hot 0-2d", 2), ("warm 2-14d", 14), ("cool 14-90d", 90), ("cold 90d+", None)]
    stats: dict[str, list[int]] = {}
    cows: dict[str, list[int]] = {}
    STATE_ROOTS = ("memory", "queue", "watch", "handoff", "research", "training")
    for row in manifest["files"]:
        p = ROOT / row["path"]
        try:
            age_days = (now - p.stat().st_mtime) / 86400
        except OSError:
            continue
        top = row["path"].split("/")[0]
        if top == "memory" and "/" in row["path"]:
            top = "memory/" + row["path"].split("/")[1]
        bucket = next(name for name, limit in buckets if limit is None or age_days < limit)
        s = stats.setdefault(bucket, [0, 0])
        s[0] += 1
        s[1] += row["bytes"]
        if age_days >= 90 and row["path"].split("/")[0] in STATE_ROOTS:
            c = cows.setdefault(top, [0, 0])
            c[0] += 1
            c[1] += row["bytes"]
    print("AGE GRADE (kit files):")
    for name, _ in buckets:
        n, b = stats.get(name, [0, 0])
        print(f"  {name:12} {n:7,} files  {b / 1048576:8.1f} MB")
    print("SACRED-COW CANDIDATES (cold 90d+, state roots):")
    for top, (n, b) in sorted(cows.items(), key=lambda kv: -kv[1][1])[:15]:
        print(f"  {top:36} {n:6,} files  {b / 1048576:8.1f} MB")
    return _git_touch_audit(manifest)


def _git_touch_audit(manifest: dict) -> int:
    """Content-age grade: days since git last touched each kit path. The tree is
    young (seeded 2026-08-04), so mtime is a restore artifact; git recency is the
    honest cow detector. seed-frozen = last touched by the seed commit only."""
    import subprocess
    import time as _time
    out = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--pretty=format:@%ct", "--name-only"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    last_touch: dict[str, int] = {}
    ts = 0
    first_ts: int | None = None
    for line in out.stdout.splitlines():
        if line.startswith("@"):
            ts = int(line[1:])
            if first_ts is None or ts < first_ts:
                first_ts = ts
        elif line.strip():
            last_touch[line.strip().replace("\\", "/")] = ts
    if first_ts is None:
        print("git log unavailable; content audit skipped")
        return 0
    now = _time.time()
    grades = {"active <=7d": [0, 0], "warm 7-21d": [0, 0], "stale 21d+": [0, 0], "seed-frozen": [0, 0]}
    cows: dict[str, list[int]] = {}
    STATE_ROOTS = ("memory", "queue", "watch", "handoff", "research", "training")
    for row in manifest["files"]:
        path = row["path"]
        lt = last_touch.get(path)
        days = (now - lt) / 86400 if lt else 9999.0
        if lt is None or days > 46:
            bucket = "seed-frozen"
        elif days <= 7:
            bucket = "active <=7d"
        elif days <= 21:
            bucket = "warm 7-21d"
        else:
            bucket = "stale 21d+"
        g = grades[bucket]
        g[0] += 1
        g[1] += row["bytes"]
        if bucket in ("seed-frozen", "stale 21d+") and path.split("/")[0] in STATE_ROOTS:
            top = "memory/" + path.split("/")[1] if path.startswith("memory/") and path.count("/") > 1 else path.split("/")[0]
            c = cows.setdefault(top, [0, 0])
            c[0] += 1
            c[1] += row["bytes"]
    print(f"GIT TOUCH GRADE (repo age {(now - first_ts) / 86400:.0f}d):")
    for name, (n, b) in grades.items():
        print(f"  {name:14} {n:7,} files  {b / 1048576:8.1f} MB")
    print("CONTENT COWS (seed-frozen/stale in state roots):")
    for top, (n, b) in sorted(cows.items(), key=lambda kv: -kv[1][1])[:15]:
        print(f"  {top:36} {n:6,} files  {b / 1048576:8.1f} MB")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="verify the newest kit instead of building")
    ap.add_argument("--audit", action="store_true", help="age-grade the newest kit (sacred-cow scan)")
    args = ap.parse_args()
    if args.audit:
        return audit()
    if args.verify:
        manifests = sorted(OUT_DIR.glob("travel_kit_*.manifest.json"))
        if not manifests:
            print("no kit found")
            return 2
        return verify(manifests[-1])
    return verify(build())


if __name__ == "__main__":
    sys.exit(main())
