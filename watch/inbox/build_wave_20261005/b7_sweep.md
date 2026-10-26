# b7_sweep - build-it-all wave lane B7, the filed-not-fixed sweep (2026-10-05)

Five filed-not-fixed items, each executed and banked. Moment window
2026-10-05T~06:50-07:45Z. Interpreter: .venv\Scripts\python.exe only. No git
commits (coordinator commits). No em/en-dashes landed (byte-scanned).

## Item 1 - tavern p2 re-fire: FIRED, CLEAN

- Scenario picked after ls + drift check: memory/plans/
  hermes_burn_playground_20261003/scenarios/hollow_crown_flash_dogfood.json
  (pressure 2, haiku 2-persona cast). The other p2, hollow_crown_p2.json, is
  the instrument lane 9 JUST fired as refresh B (clone at 084000Z, BRAWL r2);
  flash_dogfood's only prior fire (084146Z) is the corrupted double-DONE
  collision void, so this is its first CLEAN corpus row.
- Command: .venv/Scripts/python.exe tools/tavern.py --scenario
  memory/plans/hermes_burn_playground_20261003/scenarios/
  hollow_crown_flash_dogfood.json --rounds 10 --budget-usd 2
  --chain-tip 20261005T07-hour
- Run dir banked: watch/inbox/playground/tavern_20261005T071101Z (DONE +
  GWAP_BANKED + transcript 71 rows + play.md). FIRE-ATOMIC BANK: OK, CHAIN
  ok=True bad=None.
- Verdict: 10 full rounds, brawl=False, spend $0.0898 of $2, final
  escalations Maud 5/5 Pell 5/5 (cumulative 10 < trigger 14). NOTE for the
  p2 cell: with a 2-persona cast the p2 trigger 14 is unreachable (max cum
  10), so no-brawl is STRUCTURAL for this scenario, not a calibration miss;
  this row also fires the TAVERN_CURVE_AUDIT p2 falsifier prong (first p2
  no-brawl; prior p2 rows brawled r2).
- Stamp-collision fix held: single fire, fresh dir, coherent transcript
  (exactly 20 speech rows = 10 rounds x 2 personas), one DONE.

## Item 2 - seal-patrol triage: RUN, TRIAGED, 2 WORST FIXED

- Instrument: .venv/Scripts/python.exe tools/prepush_seal_patrol.py.
  Default window (last 150 rows): 4 real drifts. Task said 7; a --rows 1000
  sweep shows 17 real drifts + 21 CASE-ONLY false drifts (uppercase-hex seal
  rows vs lowercase actuals - a patrol comparison defect worth an owner fix;
  findings like DIGEST.md 5CAA5303B1C3 vs 5caa5303b1c3).
- Two worst FIXED (re-sealed through the owning writer
  tools/md_record_seal.py seal, append-only register/autoseal, never a hand
  edit; a12 law - living rows re-register, old rows untouched):
  1. corpus/steal/MASTER_READ_ESTATE.md - corpus master, autoseal-only
     coverage outside watch/inbox; new seal row sha a300da112158... matches
     actual bytes. Cleared from patrol (all windows).
  2. corpus/steal/MASTER_MICKEY17_V2.md - cited by AGENTS.md; drifted via
     lane 9's receipt-documented post-seal edit (go_wave tavern_refresh);
     new seal row sha 1207e4c4245f... matches bytes. Cleared.
- Remaining default-window drifts annotated (live-lane boards, not mine to
  re-seal; their owning writers re-seal on next append): frontier_olm_
  2026-10-04/steal/open-and-local-language-models via x.md,
  frontier_olm_2026-10-04/RECEIPT.md (lane still sealing, last 06:30Z
  today), ribvault_20261005/r06_free_probe.py (lane live, sealed 05:37Z
  today). Wider-window extras (NIGHT_SHIFT_20261004_CLOSE.md,
  X_INTEL_PAPERS_20261004.md, MAG_DANCE_SPEC_20261004.md, ractor_engine
  parked-decisions 4 files, frontier_olm sweep file, TASK_WALL/STEALTH/
  PACK_OFFLOAD legacy rows) left to their owners; none is sealed-deleted
  (a12 exempt class untouched - the patrol's 1-3 missing-on-disk skips are
  the expected seal-chain deletes).

## Item 3 - arena_gwap orphan scenes: FIXED, PROVEN

- Receipt read first (watch/inbox/go_wave_20261004/gps_dedupe.md blocker 1).
- Defect confirmed live pre-fix: exactly 6 chain scenes uncovered (all from
  the quarantined void_stamp_collision_tavern_20261004T083959Z; scene ids
  carry the ORIGINAL run name tavern_20261004T083959Z, the quarantine rename
  loses it from the dir name).
- Fix in tools/arena_gwap.py: _quarantined_run_dirs() (one-level walk under
  staging/quarantine roots) + _original_run_name() (byte-backed recovery
  from the BURN-ID law tag TAVERN_<kind>_<stamp>_r<round>_<actor>, no
  rename-convention parse; unparseable tag = refuse rather than guess) +
  _quarantine_scene_map() + feed_scene_map() factored out of main() so the
  map covers live dirs AND quarantined dirs keyed by pre-quarantine names.
  BANK walk stays top-level-only: quarantined runs are never re-banked.
- Proof: live chain 597 scenes, map covers 597, UNCOVERED=0 (pre-fix 6).
  End-to-end feed through the bridge (documented caller arg, idempotent):
  GPS FEED RECEIPT rows_seen=730 fed=0 skipped=269 distinct=461
  duplicate_skipped=461 - the whole-file walk including the 6 quarantined
  scenes ran with ZERO UNMAPPED_SCENE (pre-fix it raised GwapToGpsError at
  the first quarantined scene). Receipt's chain-native-identity preference
  (a04 row 6 shape) remains the long-term owner fix; this filesystem fix
  unblocks the feed today.
- Test added: tests/test_gwap_independent_cop_20261004.py
  test_feed_scene_map_covers_quarantined_dirs (tmp PLAY_DIR, quarantined
  dir keyed by ORIGINAL name, quarantined-name id asserted ABSENT).

## Item 4 - deepseek-chat alias probe: MEASURED, BANKED

- Script: watch/inbox/go_wave_20261004/d4_alias_probe.py (clone of d4_probe,
  MODEL=deepseek-chat per tools/ds_workhorse.py:64 alias). 3 arms, one ask
  each, ONLY the thinking key varied. Spend ~$0.00004 (50 in + 23 out).
- Verdict banked: watch/inbox/go_wave_20261004/d4_alias_thinking_probe.md
  (next to d4_thinking_probe.md). THE LINE: deepseek-chat DOES NOT think by
  omission - the omission default is OFF (0 reasoning chars, 2 completion
  tokens, byte-identical to explicit disabled; enabled arm drives 16
  reasoning tokens so the param works both ways). OPPOSITE of canonical
  deepseek-v4-flash. Consequence: d4 consequence 1 ("every ds batch ran
  thinking-ON") does NOT extend to ds_workhorse batches (they ride the
  alias); providers.yaml's v4-ON claim is name-scoped, not family-scoped.

## Item 5 - LANE4 row-16 erratum: APPENDED

- watch/inbox/audit_20260926/LANE4_TEST_ROBUSTNESS.md row 16 (line 69)
  carries the one-line ERRATUM: verdict refuted, product carried the typo,
  test pin was correct per the module's frozen spec, fixed in code not the
  test, citing watch/inbox/burn_reset_20260927/no_win.md + commit 750259531
  (verified live: git log -1 750259531, 2026-09-27 19:14:21 -0400). Original
  row text intact (append, never rewrite).

## Gate contract numbers

- pytest (tavern + gwap touched paths): tests/test_burn_id_uniqueness.py +
  tests/test_gwap_independent_cop_20261004.py + tests/test_gwap_to_gps.py +
  tests/test_gps_dedupe.py -> 40 passed, 0 failed, 4.08s.
- Ratchet: python tools/violation_ratchet.py check --changed ->
  PASS, NEW=0 (first run flagged file-too-long arena_gwap.py:401; fixed by
  compacting my docstrings to 399 lines, debt NOT registered, hook NOT
  loosened).

## Blockers

- None blocking. Filed for owners: (a) seal patrol case-only false drifts
  (21 rows, uppercase-hex seals); (b) patrol finding count differs from the
  task's 7 (4 at default window, 17 real at --rows 1000; triaged both); (c)
  remaining live-lane drifts re-seal via their owning writers; (d) the 6
  collision scenes still ride a void-stamped carrier (lane-2 flag stands).
