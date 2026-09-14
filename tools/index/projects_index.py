#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# ESTATE INDEXER — open-rib spine v5 "fixed mouths" (2026-09-09)
#
# Design note (duplication-is-emphasis): Mimosa blocked v0-v4 four times with
# one categorical finding — walked paths flowed into output PATHS (per-project
# filenames derived from directory names). v5 removes path-flow entirely:
# every output file has a compile-time constant name, so nothing from the walk
# ever becomes a path. The "nested repositories" live INSIDE the data: one
# master JSONL with a "proj" field per row (grep / jq extracts any project),
# plus a rollup with per-project sections. Same doctrine, passable shape.
#
# READ-ONLY walk of C:\Users\foste\Documents\projects -> constant-name outputs:
#   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl   master, 1 row per file
#   watch/ESTATE_INDEX/rollup.json          per-project: counts/temp/relations
#   watch/ESTATE_INDEX/last_run.json        state (delta detection)
#   dashboard/static/index_data/            the three copies the page fetches
# Never modifies any indexed file. $0. Idempotent. Safe on a daily cadence.
# ═══════════════════════════════════════════════════════════════════════════
import os, re, json, time, shutil
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(r"C:\Users\foste\Documents\projects").resolve()
REPO = (ROOT / "local_sovereign_agent").resolve()
OUT_WATCH = REPO / "watch" / "ESTATE_INDEX"
OUT_DASH = REPO / "dashboard" / "static" / "index_data"

# Every output path in this program is a constant. There are no others.
MASTER = OUT_WATCH / "ESTATE_INDEX.jsonl"
ROLLUP = OUT_WATCH / "rollup.json"
LAST_RUN = OUT_WATCH / "last_run.json"
DASH_MASTER = REPO / "dashboard" / "data" / "ESTATE_INDEX.jsonl"
DASH_MASTER.parent.mkdir(parents=True, exist_ok=True)
DASH_ROLLUP = OUT_DASH / "rollup.json"
DASH_LAST_RUN = OUT_DASH / "last_run.json"

RELATIONS = [
    ("watch\\estate_index", "estate index (self)"),
    ("\\watch\\", "watch card (the record)"),
    ("memory\\biography", "the chain (biography)"),
    ("\\memory\\", "memory estate"),
    ("\\queue\\", "mesh channel"),
    ("\\mag\\", "fleet organ"),
    ("dashboard\\static\\", "surface (rooms/games)"),
    ("\\corpus\\", "mined ore"),
    ("\\tools\\", "hands"),
    ("\\configs\\", "config"),
    ("local_sovereign_agent", "body file"),
    ("\\sovereign-mirror\\", "ancestor body 1 (sovereign-mirror)"),
    ("\\field-strike-the-chord\\", "ancestor body 2 (strike-the-chord)"),
    ("\\mag-sovereign-kit\\", "ancestor body 3 (sovereign-kit)"),
    ("\\mag-current-rebuild\\", "ancestor body 4 (current-rebuild)"),
    ("\\mag-backup.git\\", "graveyard (ancestor backup)"),
    ("codex_pytest", "codex factory litter"),
    ("\\embassy-", "embassy (external hands)"),
    ("azerothcore-wow", "foreign port"),
    ("\\worktrees\\", "worktree lane"),
]

def relation(rel_path: str) -> str:
    p = "\\" + rel_path.lower()
    for k, v in RELATIONS:
        if k in p:
            return v
    return "lane (sibling project)"

def temp_bucket(age_days: float) -> str:
    if age_days <= 2:  return "HOT"
    if age_days <= 7:  return "WARM"
    if age_days <= 30: return "COLD"
    return "FROZEN"

def main() -> None:
    t0 = time.time()
    OUT_WATCH.mkdir(parents=True, exist_ok=True)
    OUT_DASH.mkdir(parents=True, exist_ok=True)
    now = time.time()
    rows, skipped = [], 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            try:
                resolved = Path(dirpath, fn).resolve()
                rel = resolved.relative_to(ROOT)  # raises unless inside the root
                st = resolved.stat()
            except (OSError, ValueError):
                skipped += 1
                continue
            parts = rel.parts
            if not parts:
                skipped += 1
                continue
            proj = re.sub(r"[^A-Za-z0-9_-]+", "_", parts[0])[:80] or "unnamed"
            age = max(0.0, (now - st.st_mtime) / 86400)
            rows.append({
                "path": str(rel), "proj": proj, "rel": relation(str(rel)),
                "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "mtime_epoch": int(st.st_mtime), "size": st.st_size,
                "ext": os.path.splitext(fn)[1].lower(),
                "depth": len(parts) - 1, "temp": temp_bucket(age),
            })
    rows.sort(key=lambda r: r["mtime_epoch"], reverse=True)

    # All opens below use the constant names. Walked data enters files as
    # JSON content only — never as a path.
    with open(MASTER, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    per_proj = {}
    for r in rows:
        per_proj.setdefault(r["proj"], []).append(r)

    rollup = {}
    for proj, rs in per_proj.items():
        rollup[proj] = {
            "files": len(rs),
            "bytes": sum(r["size"] for r in rs),
            "newest": rs[0]["mtime"],
            "oldest": rs[-1]["mtime"],
            "temps": dict(Counter(r["temp"] for r in rs)),
            "relations": dict(Counter(r["rel"] for r in rs).most_common(6)),
        }
    with open(ROLLUP, "w", encoding="utf-8") as f:
        json.dump(rollup, f, indent=1)

    last_run = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_files": len(rows), "total_bytes": sum(r["size"] for r in rows),
        "projects": {p: v["files"] for p, v in rollup.items()},
        "newest_20": [{"path": r["path"], "mtime": r["mtime"]} for r in rows[:20]],
        "skipped": skipped, "seconds": round(time.time() - t0, 1),
    }
    with open(LAST_RUN, "w", encoding="utf-8") as f:
        json.dump(last_run, f, indent=1)

    shutil.copyfile(MASTER, DASH_MASTER)
    shutil.copyfile(ROLLUP, DASH_ROLLUP)
    shutil.copyfile(LAST_RUN, DASH_LAST_RUN)

    print(f"ESTATE INDEXED: {len(rows)} files / {len(rollup)} projects "
          f"/ {last_run['total_bytes']/1e6:.0f} MB in {last_run['seconds']}s "
          f"(skipped {skipped})")
    for proj, v in sorted(rollup.items(), key=lambda kv: -kv[1]["files"])[:10]:
        print(f"  {proj[:40]:42s} {v['files']:6d} files  newest {v['newest'][:16]}")

if __name__ == "__main__":
    main()
