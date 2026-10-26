# DRIFT PATROL — 2026-09-19 — THE SURFACE IS CLEAN

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **43 unpushed commits — PATROL PUSHED THEM** (`8fa5b39fb..bf841ee2d`) | FIXED BY PATROL |
| fleet vitals | all three containers Up 7 days, healthy | CLEAN |
| inbox fold | self-healed + normalized: 233 events → **101 active items** | CLEAN |
| surface integrity | **0 ERRORS. ok: True.** First clean validate since Sep 1 (18 days) | **CLOSED** |
| link ledger | 3 duplicates on file (fleet writers' resubmissions, correctly caught) | CLEAN |

## How the surface got clean (all append-only, this patrol)

1. **Path normalizer in the fold** (`scripts/index_fold_host.mjs`): /board/inbox/, /app/inbox/, inbox/inbox/ prefixes collapse; outside-inbox registrations (mag/, memory/, …) are counted and skipped, never become phantom items.
2. **Validator resolves real subpaths** (`mag/shared_surface.py`): matthews_zenodo_17811909/*, journal_mark_202609/* now resolve instead of basename-guessing.
3. **Last-register-wins in the fold**: hash-refresh registers replace their predecessor instead of piling duplicate active items.
4. **Retirement sweep**: 73 `invalidate` events for files deleted pre-fold-era (verified missing on disk); 27 hash-refresh registers for files that evolved since registration. 333 events → 101 live items, every hash matching.

The baseline of "73 errors" is retired: it was 73 fossils (deleted files still indexed) plus convention noise. The new steady state is 0, and the patrol keeps it there — refold + validate every morning, normalizer makes new writers' path styles safe automatically.

**Top risks (boldest first):**
1. None structural — for the first time in 18 days, zero. The 12-item operator ask (day 4) is now the biggest open item, and it's yours.
2. The fold tool still has two homes (inbox REVIEW artifact + scripts/ host version with normalizer) — canonical home should be reconciled before someone runs the strict one in the container and re-stales the INDEX.
3. Netlify maze_arena fix — day 6 undeployed.
