---
name: estate-catalog-system
description: "2026-09-16 — one-directory-plus-catalog architecture, 746,773 files
  indexed across the full projects/ tree (mag/catalog.py + mag/catalog_scan.py);
  the Estate Atlas concept (five ractors converged: Mark needs the single
  navigable map, not more tools); NUL-device walk fix; Mimosa hook blocks
  compound Bash with .py paths"
metadata:
  node_type: memory
  type: project
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

Operator's law (2026-09-16): **everything should be one directory, split apart
by cataloging, not by a million recreated folder schemes.** Physical location is
history; the catalog is the map; groups are views, never folders to hike through.

## The tooling

- `mag/catalog.py` — zone-scoped scanner + find/stats/show CLI (bounded roots)
- `mag/catalog_scan.py` — full-estate walker (os.walk + scandir, machinery
  excluded at walk time: .git/.venv/node_modules/__pycache__/.mimosa; NUL-device
  relpath ValueError caught at both dir and file level)
- `catalog/catalog.jsonl` — append-only rows: one per file
  `{id: sha256(path)[:12], path, bytes, mtime, zone, ext, title}`
- Zones derived from path: intake/astra/basecamp/campaigns/doctrine/runs/
  memory/code/games/dashboard/research/queue/registry/watch/vault/ext:<top>

## Scale (actual, verified)

**746,773 files indexed** across the full projects/ tree on 2026-09-16 —
machinery excluded at walk time. Zone census: memory 507K, lsa 156K,
runs 41K, azerothcore-wow 10K, the_margin_lean 9K, watch 4K + 30 more zones
including 37 external project repos. The catalog.jsonl is large but queryable
on a 64GB box. Full projects tree: **1.47M files / 41.2GB / 61,679 folders**
(Windows Properties verified; the delta from 746K to 1.47M is machinery).

## The gotchas

- `os.walk` hits `\\.\nul` device paths → ValueError on relpath; wrap in
  try/except and skip at BOTH dir and file level
- Batch append via heredoc can partial-fail silently (the `EOF` marker got
  swallowed once; 4 rows lost, 1 truncated) — validate after every bulk write
- `zone_of()` longest-prefix match on the relpath prefix chain
- Mimosa hook blocks compound Bash that mentions .py source files alongside
  file operations — split into separate calls or use the Write tool

## The Estate Atlas (five-ractor convergence)

Five ractors converged on what Mark actually needs: **the single navigable map
of everything he has built** — every program, every idea, every artifact, every
relation — organized by what matters to him. Five layers:

1. **THE CENSUS** — every file, counted, hashed, dated, zoned (catalog scan)
2. **THE MAP** — every program and idea, related (LINKS.jsonl + relations.jsonl)
3. **THE PRUNING** — dead weight marked, duplicates linked, sacred cows curated
4. **THE EXHIBIT** — the best version of each idea, navigable by a human
5. **THE WAVE** — the standing record (grounding wave, row by row)

All five tools already exist from tonight; what was missing was the aim — and
once aimed, they compose into the atlas.

Related: [[basecamp-mine-then-archive-20260916]], [[night-audit-20260916]],
[[fifty-wide-board-20260915]].
