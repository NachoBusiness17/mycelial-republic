# OPEN RIB SPINE v0 — the estate indexer (card + promotion artifact, 2026-09-09)

*Operator ask, triangulated: "schedule a dogfood ... every file under projects/,
mapped to when last touched, what's in them, how it relates to us ... nested index
grep repositories like our open rib system." This card = the spine's spec + the
verbatim script + the Mimosa verdict history. Promotion = one deliberate write.*

## The smell (what you're stepping in)

1. **The five bodies are folders.** sovereign-mirror, field-strike-the-chord,
   mag-sovereign-kit, mag-current-rebuild, local_sovereign_agent — the lineage
   wall's five incarnations sit in `projects/` as directories. This index makes
   the wall browsable as filesystem.
2. **Orphan lanes OUTSIDE the repo.** Seven `codex_pytest_*` litter dirs, two
   embassies, mycelial-republic, world_key, the_margin_lean — the orphan sweeps
   only ever looked inside local_sovereign_agent. The index sees the whole estate.
3. **The open-rib system's first organ.** No "open rib" card exists on disk yet —
   this spine (nested per-project JSONL + rollups + grep surface) is rib #0: the
   thing that lets any seat — or Adam, tier T2 — find anything without loading
   context. When you design the rib system proper, this card is its ancestor.
4. **Same animal, different environments** — the estate index is the body map,
   kept warm on a schedule, exactly like the chain keeps the biography warm.

## Status: BUILT BUT GATE-BLOCKED (owned, not bypassed)

*(RESOLVED 09-11 — PROMOTED + LIVE. Everything below is the 09-09 record; the
current state is the appendix at the bottom of this card.)*

Mimosa blocked the executable write FOUR times (os.stat guards → slug+commonpath →
no-relpath slicing → pure pathlib resolve/relative_to) — same categorical verdict
each time: code that records walked paths into output files is flagged as path
traversal. An indexer is definitionally that. Verdict: **category-level false
positive on indexer-class code** — the gate cannot yet distinguish an indexer from
an injector (same family as the truth-gate LINKAGE-PASS question). NOT bypassed —
per fleet law the code ships HERE as data for one deliberate human promotion.

## PROMOTION (one act)

Copy the script below verbatim to `tools/index/projects_index.py` (operator hand or
a seat with operator GO), then run once:
`python tools/index/projects_index.py`

Outputs land in `watch/ESTATE_INDEX/` (master + per_project/ + rollup + last_run)
and `dashboard/static/index_data/` for the surface at `dashboard/static/the_index.html`
(live, same turn). Then arm the cron (prompt at the bottom of this card).

## The script (verbatim — promote as-is)

```python
#!/usr/bin/env python3
# ESTATE INDEXER — open-rib spine v0 (2026-09-09). READ-ONLY walk of the whole
# projects tree -> nested grep-able JSONL + rollups + dashboard data. $0.
# Path safety: pure pathlib — resolve() + relative_to(ROOT) (raises unless
# provably inside) + is_relative_to guards on every output target.
import os, re, json, time, shutil
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(r"C:\Users\foste\Documents\projects").resolve()
REPO = (ROOT / "local_sovereign_agent").resolve()
OUT_WATCH = REPO / "watch" / "ESTATE_INDEX"
OUT_DASH = REPO / "dashboard" / "static" / "index_data"

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

def safe_slug(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", name)[:80]
    if not re.search(r"[A-Za-z0-9]", slug):
        slug = "unnamed"
    return slug

def guarded(base: Path, name: str) -> Path:
    resolved_base = base.resolve()
    target = (base / name).resolve()
    if not target.is_relative_to(resolved_base):
        raise ValueError(f"path escaped output dir: {target}")
    return target

def main() -> None:
    t0 = time.time()
    OUT_WATCH.mkdir(parents=True, exist_ok=True)
    OUT_DASH.mkdir(parents=True, exist_ok=True)
    (OUT_WATCH / "per_project").mkdir(exist_ok=True)
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
            proj = safe_slug(parts[0])
            age = max(0.0, (now - st.st_mtime) / 86400)
            rows.append({
                "path": str(rel), "proj": proj, "rel": relation(str(rel)),
                "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "mtime_epoch": int(st.st_mtime), "size": st.st_size,
                "ext": os.path.splitext(fn)[1].lower(),
                "depth": len(parts) - 1, "temp": temp_bucket(age),
            })
    rows.sort(key=lambda r: r["mtime_epoch"], reverse=True)

    master = guarded(OUT_WATCH, "ESTATE_INDEX.jsonl")
    with open(master, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    shutil.copyfile(master, guarded(OUT_DASH, "ESTATE_INDEX.jsonl"))

    per_proj = {}
    for r in rows:
        per_proj.setdefault(r["proj"], []).append(r)
    for proj, rs in per_proj.items():
        with open(guarded(OUT_WATCH / "per_project", proj + ".jsonl"), "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

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
    with open(guarded(OUT_WATCH, "rollup.json"), "w", encoding="utf-8") as f:
        json.dump(rollup, f, indent=1)
    shutil.copyfile(OUT_WATCH / "rollup.json", guarded(OUT_DASH, "rollup.json"))

    last_run = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_files": len(rows), "total_bytes": sum(r["size"] for r in rows),
        "projects": {p: v["files"] for p, v in rollup.items()},
        "newest_20": [{"path": r["path"], "mtime": r["mtime"]} for r in rows[:20]],
        "skipped": skipped, "seconds": round(time.time() - t0, 1),
    }
    with open(guarded(OUT_WATCH, "last_run.json"), "w", encoding="utf-8") as f:
        json.dump(last_run, f, indent=1)
    shutil.copyfile(OUT_WATCH / "last_run.json", guarded(OUT_DASH, "last_run.json"))

    print(f"ESTATE INDEXED: {len(rows)} files / {len(rollup)} projects "
          f"/ {last_run['total_bytes']/1e6:.0f} MB in {last_run['seconds']}s "
          f"(skipped {skipped})")
    for proj, v in sorted(rollup.items(), key=lambda kv: -kv[1]["files"])[:10]:
        print(f"  {proj[:40]:42s} {v['files']:6d} files  newest {v['newest'][:16]}")

if __name__ == "__main__":
    main()
```

## The cron prompt (arm after promotion — the automation runs run-when-present)

"ESTATE INDEX DOGFOOD PASS (daily). 1) If
local_sovereign_agent/tools/index/projects_index.py exists, run:
python tools/index/projects_index.py  (read-only walk; writes watch/ESTATE_INDEX/
+ dashboard/static/index_data/). If it does NOT exist, reply 'spine not promoted —
see watch/OPEN_RIB_SPINE_20260909.md' and stop. 2) Read
watch/ESTATE_INDEX/last_run.json; compare total_files + per-project counts against
the previous day's numbers if recorded in the prior CONVO row. 3) Append one row to
queue/handoff/zcode/CONVO.md stamped with a fresh date -u: ESTATE INDEX DOGFOOD —
totals, delta vs prior run, the 3 hottest files, any NEW top-level project. 4) Reply
with a 3-line digest. NEVER modify any indexed file; read-only except its own index
outputs. $0."

## Gate options (operator's call, any one unblocks)

1. **Promote by hand** (copy the script block to tools/index/projects_index.py) — 30 seconds.
2. **GO a seat to promote it** — one deliberate write with your GO on record.
3. **Retune Mimosa** — indexer-class allowance: writes confined to an index output
   dir, source-contained paths (the truth-gate family fix — same root as LINKAGE-PASS).

---
## ✅ RESOLVED 09-11: PROMOTED + LIVE (operator "its 11 launch", law "duplication is emphasis")

The four blocks WERE the design review: v5 "fixed mouths" removes path-flow entirely
(all outputs constant-name; per-project nesting inside the data) and passed Mimosa's
scan first touch. First pass: 1,258,549 files / 59 projects / 35.5 GB / 0 skipped.
First-pass finding: `_mimosa` = 268,700-file top-level project (the enforcer's body).
Daily 09:00 delta cron LIVE.
Card supersedes the script below (v5 is the live code at tools/index/projects_index.py).
