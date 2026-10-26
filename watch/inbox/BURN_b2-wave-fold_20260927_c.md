# BURN b2-wave-fold 20260927 c: Q5 INDEX backfill (ATLAS fix queue)

## Verdict

LANDED. 63 rows backfilled through the sanctioned writer (62 missing files + this receipt); INDEX items 1123 -> 1187 after a log catch-up fold from a stale 1083; zero existing rows changed or dropped.

## Evidence

- Path-diff (.venv python glob vs INDEX items), 2026-09-27 ~01:57Z: 66 top-level *.md unindexed — not ATLAS's 99 (different moments; census-denominator law).
- The leak is TWO-component. (1) Derived-lag: 5 files were already registered in index_events.jsonl after INDEX derived_at 2026-09-26T23:19:26Z (on-disk INDEX stale against its own log); resolved by `index_fold_host.mjs rebuild` (1083 -> 1122, exit 2 on the known legacy WARN channel). (2) Never-registered: 61 files + 1 latecomer (BURN_b2-wave-fold_20260927_b.md, landed mid-task) backfilled via fold-host `add`, writer zcode-q5-backfill-20260927, class BACKFILL, purpose = first heading, sha256 from bytes. Mix: 42 burn / 19 session / 1 doctrine / 1 game-stub.
- Preservation falsifier: counterfactual fold (my events filtered out, refolded in a throwaway inbox) = 1123 items vs production 1185; diff = exactly my 62 rows, 0 changed, 0 dropped.
- `verify`: my rows hash-clean (surface: 38 mismatched + 1 missing, all pre-existing ractor/legacy). `mag.shared_surface validate`: ok:false on 44 PRE-EXISTING errors (LINKS.jsonl findings rows, old hash mismatches); none name my rows or writer; remaining warning = non-md files (out of scope).
- Deviation, cause-named: the ask said to write INDEX.json via python json load/dump; INDEX.json's header declares writers append events, never rewrite the file — a hand edit would be clobbered by the next fold. All state changes went through the fold host.

## Steal or Vacuous

Steal: the lag decomposes into registered-but-unfolded vs never-registered. ATLAS's single number hid the derived-lag half; a hand-edit backfill would widen it by desyncing derivations metadata.

## Falsifier

Counterfactual refold minus my events: 0 changed existing rows.

## Bibliography (closed)

watch/inbox/INDEX.json · scripts/index_fold_host.mjs · tests/test_index_fold_host.py · watch/inbox/ATLAS_SELF_STEAL_20260927.md · mag/shared_surface.py
