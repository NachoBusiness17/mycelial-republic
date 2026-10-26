# DRIFT PATROL — 2026-09-21

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | 1 unpushed (yesterday's patrol receipt) — pushed (`250284f2a`) | CLEAN |
| fleet vitals | all three containers Up 2h (bounced again recently), healthy | CLEAN |
| inbox fold | self-healed + refolded: 374→384 events → 126 active items | CLEAN |
| surface integrity | caught 10 overnight drifts (5 registered-but-never-landed cathedral/curvature files, 4 post-edit hash drifts, LINKS.jsonl), healed: 6 invalidate + 4 refresh above max-seq → **0 errors, ok: True** | CLEAN (steady state holds, day 3) |
| link ledger | 3 duplicates on file (stable) | CLEAN |

**Overnight:** light — the free-resource scout filed its daily (Agnes-3.0-Flash open-weights preview: 262K ctx + vision + tools; open-weights gap shrunk to ~4 months; OpenRouter free roster rotates at 23). The cathedral/curvature registrations suggest a build window is mid-flight but its files never landed — watched.

**Top risks (boldest first):**
1. **The cathedral/curvature window registered 5 files that never landed on disk** — either a window died mid-build (the known failure mode) or it wrote to a temp dir; if the build matters, that window needs a recovery pass.
2. **Backup remote divergence merge still owed** (day 2) — one lineage, not two shadows.
3. **Seq-unit normalization in the fold still owed** — today's healing worked only because the patrol re-files above max-seq; until seq units are normalized, "last by seq" can silently prefer stale hashes.
