# FW-19 — Event-path convention debt: burn the first 10 of the itemized +34

- **class:** RECEIPT · **writer:** queue-gopher2-q023 · **board:** memory/plans/fifty_wide_20260917.md §D · **date:** 2026-09-28
- **verdict:** SUPERSEDED-BY-CLOSURE — the +34 were burned wholesale on 2026-09-19, eleven days before this ask ran. Verified byte-level today; the only surviving member class (files-edited-after-registration, 4 live races) was burned by this session via fold re-registers.

## What the +34 were (watch/inbox/DRIFT_PATROL_20260917.md)

Surface integrity read **107 errors vs baseline 73 (+34)**, itemized as three classes:
(1) mangled writer paths (doubled `inbox/inbox/`, relative `journal_mark_202609/…`, `/app/memory/...`),
(2) subdir registrations the name-based validator couldn't resolve (`matthews_zenodo_17811909/*`),
(3) files edited after registration (hash mismatches, e.g. the Sep-1 EXP002A trio).

## How they were burned (not by this ask — by the 09-19 patrol)

watch/inbox/DRIFT_PATROL_20260919.md ("THE SURFACE IS CLEAN"): first 0-error validate since Sep 1, via
(1) fold-time path normalizer in scripts/index_fold_host.mjs (`/board/inbox/`, `/app/inbox/`, `inbox/inbox/` prefixes collapse; outside registrations counted and dropped),
(2) validator resolves real subpaths (mag/shared_surface.py:289-295),
(3) last-register-wins hash-refresh in the fold,
(4) retirement sweep: 73 invalidate + 27 hash-refresh events. The "baseline 73" was retired as fossils+convention-noise; new steady state 0.

Code verified this session: normalizer `normInboxFile` + `OUTSIDE_RE`/`isUnresolved` at scripts/index_fold_host.mjs:201-233; subpath resolution comment at mag/shared_surface.py:294.

## Today's byte-level census (proving the burn holds)

From watch/inbox/INDEX.json (folded 2026-09-28T18:13:14Z, 4,671 events → 1,409 items):
- **Class 1 (mangled paths): 0 active items** match `^(inbox/inbox|app/|/app/)` or contain `C:/`.
- **Class 2 (subdirs): 254 subdir-registered active items, all resolving**; `matthews_zenodo_17811909/*` 10/10 exist on disk; `journal_mark_202609/*` resolve as proper subpaths.
- **Class 3 relic clean:** `EXP002A_RECEIPT_20260901.md` (the "genuinely mismatched since Sep 1" trio member) is active and hash-clean today.

## The class-3 burn this session did execute

The one itemized class that still recurs is (3) — live-writer races (files edited after their last register; autoseal writers self-register mid-edit per DRIFT_PATROL_20260928.md). Today's validate showed 4 members. All four burned by hash-refresh re-register through the sanctioned fold script (`node scripts/index_fold_host.mjs add`, writer `queue-gopher2-q023`, inbox-relative paths; first attempt with `watch/`-prefixed argv was correctly refused by the B2-147 writer guard):

| file | registered | edited | burned (seq, decimal-string per B2-40) |
|---|---|---|---|
| FIFTY_WIDE_BOARD_20260915.md | 09-19T12:10:44Z | 09-28T18:13:58Z | 1790458967636140351 |
| STEALTH_SWEEP_LATEST.md | 09-28T12:08:04Z | 09-28T13:50:15Z | 1790458967636140352 |
| DRIFT_PATROL_20260928.md | 09-28T12:10:54Z | 09-28T12:24:21Z | 1790458967636140353 |
| burn_reset_20260927/queue/Q-041.md | 09-28T17:01:17Z (md-record-seal) | 09-28T17:07:46Z | 1790458967636140354 |

Plus the law-named repair of a living downgrade: `burn_wave_20260926/QUEUE.md` re-registered with `--living` size-seal 483,723 (seq 1790458967636140355) per LIVING_HASH_LAW_20260926.md section 5.

Post-burn validate: errors 5 → 1 (the 1 is the scout lane's LINKS kind-gate debt, not path-convention — see FW21_inbox_validate.md). Not attempted here: nothing of the literal 09-17 +34 remained to burn; "first 10" is therefore reported as closed-by-supersession, not executed item-by-item.
