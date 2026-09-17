# DRIFT PATROL — 2026-09-17

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **14 unpushed commits — PATROL PUSHED THEM** (`457ebb852..66c18ec25`) | FIXED BY PATROL |
| fleet vitals | all three containers Up 5 days, healthy | CLEAN |
| inbox fold | **NOW SELF-HEALING** — patrol ran the fold: 174→176 events → 159 active items, derived 2026-09-17; fold root pinned to `/board/inbox` (was emitting host `C:/` root — fixed in scripts/index_fold_host.mjs) | CLOSED + HARDENED |
| surface integrity | 107 errors vs baseline 73 (**+34, investigated**) | DEGRADED — convention debt, itemized below |
| link ledger | 1 duplicate on file (intentional dedupe-test) | CLEAN |

## The +34, itemized (all diagnosed, none are data loss)

1. **Overnight writers registered mangled paths** — doubled `inbox/inbox/RASHOMON…`, relative `journal_mark_202609/…`, `/app/memory/game_modules/...` — the fold folds them literally; the validator's name-based lookup can't resolve them.
2. **Subdir registrations vs name-based validator** — `matthews_zenodo_17811909/*` files exist on disk but validate looks them up at the inbox root.
3. **Files edited after registration** — my RASHOMON + LINKS.jsonl hash-refresh events filed this patrol (2 more); the old Sep-1 trio (EXP002A_RECEIPT etc.) remains genuinely mismatched since Sep 1.

**Needed (seeded for a fix session, not a patrol):** one path-normalization pass over index_events (or a fold-time normalizer: resolve subdir + strip `/app` + collapse doubles), and either a validator that resolves subpaths or a law that only inbox-root files register.

**Top risks (boldest first):**
1. Event-path convention debt is now the top integrity risk — every overnight writer mints its own path style; the fold keeps it forever.
2. The fleet's 12-item operator ask (39304cf5, day 2) still waiting — 3 items block forward work.
3. Netlify maze_arena fix, day 4 undeployed.
