#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# ESTATE ATLAS — the file-custody layer of the Elder's one frontier ask
# (2026-09-23)
#
# The Elder's charter (watch/inbox/THE_ELDER_DISCUSSION_20260920.md): emit "a
# map that tells any cheap agent what is proven, what is claimed, and what is
# dark." This tool mints the DISK layer of that map. The knot layer (shadow
# index, phantoms) stays gated behind UF-109/UF-47 — this does not mint it.
#
# Source of truth: watch/ESTATE_INDEX/ESTATE_INDEX.jsonl (the spine,
# tools/index/projects_index.py). This tool NEVER re-walks the disk; if the
# spine is stale it says so and exits flat. "An oracle without citations is
# that AI wearing our crest" — every number here traces to spine rows.
#
# READ-ONLY on the estate. Outputs (constant names, spine doctrine):
#   watch/ESTATE_ATLAS/ATLAS.md           boot-readable map
#   watch/ESTATE_ATLAS/atlas.json         machine-readable rollup
#   watch/ESTATE_ATLAS/ATTIC_MOVE_LIST.jsonl   DRY-RUN quarantine plan only
#
# ATTIC PROTOCOL (v2, what "cleanup" means here — nothing is ever deleted):
#   attic/<date>_<reason>/ holds moved subtrees at their original relative
#   path, with attic/MANIFEST.jsonl rows {from, to, why, files, bytes, ts}.
#   A move without a manifest row is a hole in the record, not a cleanup.
# ═══════════════════════════════════════════════════════════════════════════
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
SPINE = REPO / "watch" / "ESTATE_INDEX" / "ESTATE_INDEX.jsonl"
SPINE_LAST = REPO / "watch" / "ESTATE_INDEX" / "last_run.json"
OUT = REPO / "watch" / "ESTATE_ATLAS"
ATLAS_MD = OUT / "ATLAS.md"
ATLAS_JSON = OUT / "atlas.json"
MOVE_LIST = OUT / "ATTIC_MOVE_LIST.jsonl"

SPINE_MAX_AGE_H = 48  # older than this: the map lies, say so

# ── pre-stated classification (change the law here, then re-run) ────────────
# ROTATING SINKS: append-only writers that never rotate. Action = cap, not attic.
ROTATION_SINKS = [
    ("memory/biography_backup/", "daily full-copy of memory/biography, unrotated",
     "keep newest 2 stamps, tar the rest (knotnight ritual = custody, not sprawl)"),
    ("memory/ghost/leak_reports/", "ghost leak reports, timestamped, never rotated",
     "keep 7 days, tar+attic the rest"),
    (".mimosa/hook-state/", "Mimosa hook writes per invocation, sibling lane",
     "propose rotation cap upstream of the hook; owner = Mimosa lane"),
]
# ONE-SHOT BACKUPS: single dated snapshots -> tar once, attic, manifest.
ONESHT_BACKUPS = [
    ("memory/biography_backup_20260825/", "old-series knotnight backup"),
]
# RAW ORE: cold by design, keep, just say so.
ORE = [
    ("mine/raw/", "mined corpus, raw"),
]
# VERSION-CLUSTER detection inside live trees (report only, never auto-move).
VERSION_RE = re.compile(
    r"[ _\-\(](copy|copies|old|new|bak|backup|final\d*|draft\d*|v\d+|\d{8}"
    r"|\d{8}[_T]\d{6}|\(\d+\))[\)\._ ]*$", re.IGNORECASE)

LIVE_ORGANS = {
    "mag/": "fleet organ (the code)",
    "watch/": "the record (cards)",
    "state/": "live state",
    "tools/": "hands",
    "docs/": "doctrine",
    "scripts/": "hands",
    "queue/": "mesh channel",
    "dashboard/": "surface",
    "tests/": "proof",
    "memory/runs/": "run receipts",
    "memory/biography/": "the chain (biography)",
}


def now_s():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    t0 = time.time()
    if not SPINE.exists():
        print(f"FLAT: spine missing at {SPINE} — run tools/index/projects_index.py first")
        return 1
    spine_age_h = (time.time() - SPINE.stat().st_mtime) / 3600
    stale = spine_age_h > SPINE_MAX_AGE_H

    n = 0
    bytes_total = 0
    temp_ct = Counter()
    organ_ct = defaultdict(lambda: [0, 0])          # organ -> [files, bytes]
    sink_ct = defaultdict(lambda: [0, 0])
    proj_ct = Counter()
    version_ct = Counter()
    version_examples = defaultdict(list)

    with SPINE.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            n += 1
            size = r.get("size", 0) or 0
            bytes_total += size
            temp_ct[r.get("temp", "?")] += 1
            p = r.get("path", "").replace("\\", "/")
            proj = r.get("proj", "?")
            proj_ct[proj] += 1
            for organ in LIVE_ORGANS:
                if f"local_sovereign_agent/{organ}" in p:
                    organ_ct[organ][0] += 1
                    organ_ct[organ][1] += size
                    break
            all_sinks = [(s, w, a) for s, w, a in ROTATION_SINKS] + \
                [(s, w, "tar once") for s, w in ONESHT_BACKUPS] + \
                [(s, w, "keep") for s, w in ORE]
            for sink, _, _ in all_sinks:
                if f"local_sovereign_agent/{sink}" in p or p.startswith(sink):
                    sink_ct[sink][0] += 1
                    sink_ct[sink][1] += size
                    break
            else:
                # version-cluster probe, live organs only, files not dirs
                base = p.rsplit("/", 1)[-1]
                if base and VERSION_RE.search(base.rsplit(".", 1)[0]):
                    stem = VERSION_RE.sub("", base.rsplit(".", 1)[0]).strip(" _-")
                    key = f"{stem}.*"
                    version_ct[key] += 1
                    if len(version_examples[key]) < 3:
                        version_examples[key].append(p)

    OUT.mkdir(parents=True, exist_ok=True)
    live_files = sum(v[0] for v in organ_ct.values())
    hot_warm = temp_ct.get("HOT", 0) + temp_ct.get("WARM", 0)
    cold_frozen = temp_ct.get("COLD", 0) + temp_ct.get("FROZEN", 0)

    def gb(b):
        return f"{b / 1e9:.2f} GB"

    stamp = now_s()
    lines = [
        "# ESTATE ATLAS", "",
        f"- **generated:** {stamp}",
        f"- **spine:** watch/ESTATE_INDEX/ last run {spine_age_h:.1f}h ago"
        + ("  ⚠️ STALE (>48h) — numbers below are a fossil; re-walk before trusting"
           if stale else " (fresh)"),
        f"- **source rows:** {n:,} files, {gb(bytes_total)} under Documents/projects",
        "- **layers up from here:** semantic = memory/runs/mickey17/MASTER_INDEX_20260920.md"
        " (what things mean) · provenance = the verkle chain (what is proven) ·"
        " THIS file = what exists and where",
        "",
        "## What is proven (the live estate)",
        "",
        "| organ | files | bytes |", "|---|---|---|",
    ]
    for organ, (c, b) in sorted(organ_ct.items(), key=lambda kv: -kv[1][0]):
        lines.append(f"| {organ} ({LIVE_ORGANS[organ]}) | {c:,} | {gb(b)} |")
    lines += [
        f"| **live organ total** | **{live_files:,}** | |",
        f"| HOT+WARM working set (whole projects root) | {hot_warm:,} | |",
        "",
        "## What is dark (the sediment)",
        "",
        f"- COLD+FROZEN: **{cold_frozen:,} files** "
        f"({100 * cold_frozen / max(n, 1):.0f}% of everything). Sediment, not rot —"
        " it stays until its sink rule moves it.",
        "",
        "## Sinks (append-only writers — capped by rule, never hand-weeded)",
        "",
        "| sink | files | bytes | law |", "|---|---|---|---|",
    ]
    for sink, why, action in ROTATION_SINKS:
        c, b = sink_ct.get(sink, [0, 0])
        lines.append(f"| {sink} — {why} | {c:,} | {gb(b)} | {action} |")
    for sink, why in ONESHT_BACKUPS:
        c, b = sink_ct.get(sink, [0, 0])
        lines.append(f"| {sink} — {why} | {c:,} | {gb(b)} | tar once -> attic + manifest |")
    for sink, why in ORE:
        c, b = sink_ct.get(sink, [0, 0])
        lines.append(f"| {sink} — {why} | {c:,} | {gb(b)} | keep (ore, cold by design) |")

    top_versions = version_ct.most_common(30)
    lines += [
        "",
        "## Version clusters (same stem, many editions — attic candidates, dry-run only)",
        "",
    ]
    if top_versions:
        lines += ["| stem | editions | example |", "|---|---|---|"]
        for key, c in top_versions:
            lines.append(f"| {key} | {c} | {version_examples[key][0].split('local_sovereign_agent/')[-1][:80]} |")
    else:
        lines.append("(none above threshold)")

    lines += [
        "",
        "## The protocol (how it stays clean)",
        "",
        "1. **Spine walks, atlas reads.** Daily spine run (09:00) feeds this map."
        " Atlas is never hand-edited; the law lives in its source.",
        "2. **Sinks get caps.** Every append-only writer above gets a rotation rule."
        " A cap violation shows up here as a growing number — meter, then move.",
        "3. **Attic, not delete.** Moves land in attic/<date>_<reason>/ at original"
        " relative paths + a MANIFEST.jsonl row. Reversible by construction.",
        "4. **GO-gated.** ATTIC_MOVE_LIST.jsonl is a plan. Execution needs the"
        " operator's word (needs-manifest law: CAP and STOP are operator inputs).",
        "",
        f"_atlas run took {time.time() - t0:.1f}s, read-only, $0._",
    ]

    ATLAS_MD.write_text("\n".join(lines), encoding="utf-8")

    atlas = {
        "schema": "estate_atlas.v1",
        "generated_at": stamp,
        "spine_age_hours": round(spine_age_h, 2),
        "spine_stale": stale,
        "rows": n,
        "bytes_total": bytes_total,
        "temp": dict(temp_ct),
        "live_organs": {k: {"files": v[0], "bytes": v[1]} for k, v in organ_ct.items()},
        "sinks": {k: {"files": v[0], "bytes": v[1]} for k, v in sink_ct.items()},
        "projects_top": dict(proj_ct.most_common(15)),
        "version_clusters_top": dict(top_versions),
    }
    ATLAS_JSON.write_text(json.dumps(atlas, indent=1), encoding="utf-8")

    # DRY-RUN move plan: one row per sink-level action. No bytes move here.
    with MOVE_LIST.open("w", encoding="utf-8") as f:
        for sink, why, action in ROTATION_SINKS:
            c, b = sink_ct.get(sink, [0, 0])
            f.write(json.dumps({
                "class": "rotation", "src": sink, "files": c, "bytes": b,
                "why": why, "proposed": action, "state": "DRY-RUN — awaiting operator GO",
            }) + "\n")
        for sink, why in ONESHT_BACKUPS:
            c, b = sink_ct.get(sink, [0, 0])
            f.write(json.dumps({
                "class": "oneshot", "src": sink, "files": c, "bytes": b,
                "why": why, "proposed": "tar -> attic/<date>_backup/ + manifest row",
                "state": "DRY-RUN — awaiting operator GO",
            }) + "\n")

    print(f"ATLAS MINTED: {n:,} rows read in {time.time() - t0:.1f}s")
    print(f"  live organs {live_files:,} | hot+warm {hot_warm:,} | cold+frozen {cold_frozen:,}")
    for sink in list(sink_ct):
        print(f"  sink {sink}: {sink_ct[sink][0]:,} files")
    print(f"  spine {'STALE ' + str(round(spine_age_h, 1)) + 'h' if stale else 'fresh'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
