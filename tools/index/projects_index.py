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
#   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl   master, 1 row per file (minus the
#                                           skip list below, r04#1 2026-10-05)
#   watch/ESTATE_INDEX/rollup.json          per-project: counts/temp/relations
#   watch/ESTATE_INDEX/last_run.json        state (delta detection)
#   dashboard/static/index_data/            rollup + last_run copies the page fetches
#   dashboard/data/ESTATE_INDEX.pointer.json  pointer naming the master; the full
#                                           master copyfile re-fattened a second
#                                           4.15GB copy every walk and was stopped
#                                           per r04#2 (2026-10-05). The estate-query
#                                           reader follows this pointer since the
#                                           ouroboros r5 close (2026-10-06,
#                                           dashboard/server.py _estate_index_source);
#                                           the frozen 2026-10-04 dashboard copy is
#                                           RETIRED (.retired-20261006, deleted after
#                                           sha256 receipt; the watch master holds
#                                           every byte).
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
DASH_MASTER_POINTER = REPO / "dashboard" / "data" / "ESTATE_INDEX.pointer.json"
DASH_ROLLUP = OUT_DASH / "rollup.json"
DASH_LAST_RUN = OUT_DASH / "last_run.json"

# Skip list (r04#1, curiosity register row 1 unit 1, landed 2026-10-05): the
# .mimosa hook-state subtrees are the artifact's bulk. 9,524,538 of 10,661,260
# indexed rows carry ext ".source" under some hook-state subtree (named root
# local_sovereign_agent\.mimosa\hook-state\ is 96.27% of .source rows, the
# '_mimosa' sibling lane 3.68%, other nested copies 0.06%; 2026-10-04 tier-2
# census, corpus/steal/MASTER_READ_ESTATE.md TS-07). That is queue-runner hook
# state, not estate surface: the walk never descends into a hook-state dir
# under a .mimosa ancestor (prune_hookstate) and the write path backstops any
# straggler row (is_skip_path). Pruning every hook-state subtree retires
# 89.34% of the artifact; a single-root exclusion would retire only 86.01%.
SKIP_ANCESTOR = ".mimosa"
SKIP_DIR_NAME = "hook-state"
SKIP_PATH_MARKERS = (".mimosa\\hook-state\\", ".mimosa/hook-state/")

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

def prune_hookstate(dirpath: str, dirnames: list) -> None:
    """Walk prune (r04#1 skip list, 2026-10-05): never descend into a
    .mimosa hook-state subtree. Mutates dirnames in place (os.walk topdown
    contract) so pruned files are never stat'd and never written. Fires only
    under a .mimosa path component, so a lookalike dir outside .mimosa is
    untouched. Covers the named root, the '_mimosa' sibling lane, and every
    nested hook-state copy."""
    if SKIP_ANCESTOR not in dirpath.replace("/", "\\").lower().split("\\"):
        return
    dirnames[:] = [d for d in dirnames if d.lower() != SKIP_DIR_NAME]

def is_skip_path(rel_str: str) -> bool:
    """Row backstop (r04#1 skip list, 2026-10-05): a hook-state row is skipped
    wherever the walk prune failed to reach it. Same subtree definition as
    prune_hookstate, matched on the written path string."""
    p = rel_str.replace("/", "\\").lower()
    return any(m in p for m in SKIP_PATH_MARKERS)

def main() -> None:
    t0 = time.time()
    OUT_WATCH.mkdir(parents=True, exist_ok=True)
    OUT_DASH.mkdir(parents=True, exist_ok=True)
    now = time.time()
    rows, skipped, skip_list_hits = [], 0, 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        prune_hookstate(dirpath, dirnames)
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
            rel_str = str(rel)
            if is_skip_path(rel_str):
                skip_list_hits += 1
                continue
            proj = re.sub(r"[^A-Za-z0-9_-]+", "_", parts[0])[:80] or "unnamed"
            age = max(0.0, (now - st.st_mtime) / 86400)
            rows.append({
                "path": rel_str, "proj": proj, "rel": relation(rel_str),
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
        "skipped": skipped, "skipped_skip_list": skip_list_hits,
        "seconds": round(time.time() - t0, 1),
    }
    with open(LAST_RUN, "w", encoding="utf-8") as f:
        json.dump(last_run, f, indent=1)

    # r04#2 fix (2026-10-05, curiosity register row 1 unit 1): the full
    # shutil.copyfile of MASTER into dashboard/data/ESTATE_INDEX.jsonl
    # re-fattened a second independent copy on every walk. Evidence fixed on:
    # both copies measured 4,150,418,528 bytes and two independent fsutil
    # hardlink-list runs each returned only the path itself (no hardlink), and
    # the 09-30 pointer dedup (tools/estate_index_dedup.py --apply) was
    # re-broken by exactly this line; receipt corpus/steal/MASTER_READ_ESTATE.md
    # TS-08 + D1. The dashboard side is now a small pointer naming the watch
    # master. The reader leg landed with the ouroboros r5 close (2026-10-06):
    # dashboard/server.py _estate_index_source follows this pointer, and the
    # frozen 2026-10-04 dashboard copy is retired (.retired-20261006, deleted
    # after sha256 receipt; receipt watch/inbox/ouroboros_20261005/
    # r5_land_close.md).
    # r5 close (2026-10-06, ouroboros): pointer fields renamed to kill the
    # field-name collision the r5 relay diagnosed. The old "rows"/"bytes"
    # read as the master jsonl's stats but were estate-wide walk totals:
    # "rows" was len(rows), which happens to equal the master line count, but
    # "bytes" was last_run["total_bytes"] - the 131 GB sum of indexed file
    # sizes - never the 346 MB master file. A pointer consumer that trusted
    # "bytes" as the master's size was off by 378x. Now master_rows/
    # master_bytes describe the master jsonl itself (master_rows == len(rows)
    # by the one-line-per-row write bijection above) and walk_files/
    # walk_bytes carry the estate-wide totals. last_run keeps the keys
    # total_files/total_bytes (the_index.html's page contract renders them as
    # the indexed estate, which is their true meaning).
    master_bytes = MASTER.stat().st_size
    DASH_MASTER_POINTER.write_text(json.dumps({
        "pointer": True, "master": "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl",
        "master_rows": len(rows), "master_bytes": master_bytes,
        "walk_files": len(rows), "walk_bytes": last_run["total_bytes"],
        "ts": last_run["ts"],
        "note": "full master copyfile stopped per r04#2 2026-10-05; read the watch master; "
                "fields renamed per r5 2026-10-06: master_rows/master_bytes = the master jsonl, "
                "walk_files/walk_bytes = estate-wide walk totals",
    }, indent=1) + "\n", encoding="utf-8")
    shutil.copyfile(ROLLUP, DASH_ROLLUP)
    shutil.copyfile(LAST_RUN, DASH_LAST_RUN)

    print(f"ESTATE INDEXED: {len(rows)} files / {len(rollup)} projects "
          f"/ {last_run['total_bytes']/1e6:.0f} MB in {last_run['seconds']}s "
          f"(skipped {skipped}, skip-list {skip_list_hits})")
    for proj, v in sorted(rollup.items(), key=lambda kv: -kv[1]["files"])[:10]:
        print(f"  {proj[:40]:42s} {v['files']:6d} files  newest {v['newest'][:16]}")

if __name__ == "__main__":
    main()
