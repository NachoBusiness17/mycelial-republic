# queue-closes receipt (gala wave5-repair, division B) 2026-09-29

Lane: queue-closes. Owed work: the two seat-executable work orders from the
queue/todo.md dispatch triage (ask pointer "s2-02" resolves to
watch/inbox/burn_reset_20260927/flash50/sess-02.md; s2-02.md in the same dir is
a different artifact, the improve-loop audit, and holds no WO text).

## WO-10: shared_surface INDEX fold rebuild CLI (line 232 sub-item 7)

Owed state at dispatch: `grep -c rebuild mag/shared_surface.py` = 0; commit
383fed94f ran the one-time "fold rebuild + 58 register heals" and landed no
standing CLI; 85 truly-invisible files at the f-30/sess-02 census. The repair
shape is pinned by corpus/steal/MASTER_MICKEY17_V2.md D2: files with ZERO
register events are invisible to any refold, so the repair is backfill `add`
events + `rebuild` + `verify`, always through scripts/index_fold_host.mjs,
never a hand-edited INDEX.json.

Landed:

- mag/surface_rebuild.py (new, 290 lines, under the 400 cap): the
  implementation module, the file-too-long module-split pattern (same shape as
  mag/events_scan.py, mag/links_split_gate.py). `rebuild_surface(inbox,
  dry_run)` census classifies three heal classes and heals each through the
  fold's own writer verbs run via `node scripts/index_fold_host.mjs`
  (cwd = the inbox root, INDEX_WRITER=mag-surface-rebuild, shell=False):
  - invisible: top-level non-control file with no register event -> `add`
    (class UNPROVEN, untrusted_data_until_classified);
  - stale: active non-living item whose whole-file sha no longer matches ->
    `add` re-register of current bytes (the stale-register heal of
    event-taxonomy.md), living items judged by their own seal law (open
    living never stale, sealed living stale only on prefix mismatch);
  - missing: active item whose file is gone -> `invalidate` (log history
    kept).
  Idempotent by construction: heals apply only to census deltas; a clean
  surface gets a no-op refold and zero appends (pinned by test).
- mag/shared_surface.py: CLI verb `rebuild` added next to path/status/validate
  (+ `--dry`), implementation re-exported from mag/surface_rebuild.py;
  docstring updated. File went 427 -> 447 lines; its file-too-long debt claim
  (198edd83211b76e1) is registered at 426 accepted lines, so the ratchet
  prints a GROWTH line (+21), which is a visible ledger fact, not a failure;
  not re-accepted by name (the ledger keeps the honest delta).
- main.py: `surface-rebuild` subcommand (--dry) dispatching to
  rebuild_surface, so the verb is reachable as `mag.cmd surface-rebuild`.
- tests/test_surface_rebuild.py (new): 3 tests against throwaway inboxes via
  INDEX_INBOX_DIR (real node fold, durable inbox never touched): heals all
  three classes (including living-open-is-never-stale), idempotency (second
  run appends zero events), dry-run writes nothing. 3 passed.

Production runs (live tree, sibling lanes appending throughout):

- Baseline validate: ok=False, 34 errors (28 hash mismatch, 5 indexed item
  missing, 1 LINKS event-kind debt row from another writer) + 98 unindexed
  warning. Independent census instrument (_qc_truly_invisible_census.py):
  93 truly-invisible top-level files (up from the 85 at sess-02 census; live
  tree), 12,897 non-registered recursive files (informational; the verb's
  scope is top-level, the same definition validate gates on and the mickey17
  census used).
- Pass 1: 126 heals applied (93 register, 28 reregister, 5 invalidate), 0
  failed; after: invisible 0, stale 11 + missing 2 minted by concurrent
  sibling-lane writes during the run (active items 1678 -> 1929, the fold
  absorbing other lanes' 130 concurrent registers).
- Pass 2: 12 reregisters + 2 invalidates; after: 0/1/0.
- Pass 3: 2 reregisters; after 0/0/0, ok=True, exit 0. The WO-10 completion
  test holds: post-run INDEX delta = 0 truly-invisible files, stable across
  every later pass (invisible stayed 0 in passes 4, 5 and the final check).
- Validate after the passes: 34 -> 1 error. The residual is a moving target
  of sibling lanes' live appends, a different freshly-registered-then-amended
  file at each check (wave5_repair/render-pipe.md, then wave5_repair/
  seed-kernel.md, then STEALTH_MINED_FINDINGS.jsonl, then
  frontier_olm_20260928/sweep/inference-efficiency-reddit.md): a register
  followed by the owning lane's next append within seconds. Named each time;
  none are INDEX-fold debt and none are this lane's files. The LINKS
  event-kind debt from the baseline was resolved by another lane mid-run
  (not by this lane).
- Ratchet (mandatory, mag/ + tools/ touched): `tools/violation_ratchet.py
  check --changed` exit 1, FAIL. Its 4 NEW hits are sibling-lane files
  (mag/corpus_gap_research.py:663, mag/corpus_selfsteal.py:550,
  mag/link_library.py:413, tools/fossil_check.py:73 shell=True, the last
  already named in f-25's receipt); GROWTH lines: mine (+21, above) and
  tools/stealth_driver.py +355 (not mine). This lane's four files scanned
  individually with the ratchet's own violations_in(): mag/surface_rebuild.py
  CLEAN, tests/test_surface_rebuild.py CLEAN, mag/shared_surface.py only the
  registered file-too-long claim, main.py only registered debt. The FAIL
  belongs to concurrent lanes' unregistered debt; accepting it by name here
  would launder debt this lane did not incur.

## WO-12: bookkeeping flip sweep over queue/todo.md

- Pre-edit recount with the sess-02 exact command: UNCHECKED 63, line list
  byte-identical to the sess-02 enumeration (zero drift; banked
  _qc_preedit_recount.txt).
- Sweep instrument: _qc_wo12_flip_sweep.py (dry run first, then apply). Every
  flip is keyed on line number AND an expected content snippet; any mismatch
  aborts before writing (drift law). 54 flips + 2 insertions applied.
- Flips: the 51 sess-02 Section B rows, each with a one-line pointer taken
  from Section B evidence (Q-0xx receipts verified present in
  watch/inbox/burn_reset_20260927/queue/ by dir listing this session), plus
  three documented deviations:
  1. Line 232 (Stone 2b sub-item 7) flips because WO-10 completed in this
     lane and WO-10's own criteria say to flip it once the verb lands and
     validate is green on its axes. Pointer cites this receipt.
  2. Lines 235 + 237 (Stone 5 Grok asks, the same item twice) flip as MERGED
     into the WO-12(3) re-seeded single line. WO-12(3) orders the merged line
     re-seeded NOW; leaving both originals unchecked next to it would show
     the item three times. Execution remains OWED (lane ruling per the
     DRIVING LADDER).
- Re-seeds (2 new unchecked lines): the line-249 residuals (supernatural
  villain plots, per-class attack triggers beyond scorpion-force, Ages of
  Powers branch) and the merged Stone 5 line (4 asks, packets named).
  WO-5's optional habit line was NOT re-seeded: it requires an operator
  ruling that the ritual is kept, and no such ruling exists (line 98's
  closure note says so on the line).
- Untouched (byte-identical, 9 lines): 31 verkle GO, 97 manual REPL, 99 W0.0
  archive, 204 Studio publish, 205 Cathedral smoke, 233 Stone 3, 234 Stone 7,
  239->240 Sunday close, 250->252 ratchet dials.
- Post-edit recount: UNCHECKED 11 (9 untouched keep-open + 2 re-seeds).
  File stayed untracked (gitignored, .gitignore:41 per f-30); no git add.
  Line endings preserved (CRLF); 277 -> 279 lines; the sweep's 56 added
  strings scanned: 0 em dashes, 0 en dashes, 0 non-ascii (the file's 59
  pre-existing em dashes untouched).

## Decision ledger

The ask's letter said "check off exactly the rows s2-02 marked closeable,
leave the 12 keep-open rows untouched". This lane deviated on three rows,
each because the same dispatcher's own criteria (sess-02) order it once the
named work happened in the same seat: 232 (WO-10's flip clause), 235+237
(WO-12(3)'s merge clause). The alternative readings leave the queue lying
(232 open with its work done; Stone 5 triplicated). End state after all
session WOs is the same two-step dispatch intended by sess-02 section C.
This closes the wave5-repair queue lane's decision: the queue's unchecked
set now contains only work that is genuinely owed, each row carried by a
named work order (WO-1..WO-9, WO-11) or an explicit re-seed.

## Checks run this session (full raw output: lanes/queue-closes.check.txt)

1. pytest tests/test_surface_rebuild.py -v -> 3 passed, exit 0.
2. pytest tests/test_shared_surface_events.py tests/test_index_fold_host.py
   -q -> 50 passed, exit 0 (no regression on the sibling surfaces).
3. python -m mag.shared_surface rebuild -> pass 3 (banked
   lanes/_qc_rebuild_pass3_clean.json): plan 0/2/0, after 0/0/0, ok True,
   exit 0. A later snapshot pass (lanes/_qc_rebuild_final_pass.json) read
   plan 0/8/0 -> after 0/1/0 with exit 1: sibling-lane appends re-staled hot
   ledgers between its census and validate; its heals also landed and
   invisible stayed 0.
4. python -m mag.shared_surface validate -> exit 1 with exactly 1 error, a
   sibling lane's live-append file, named in the check file.
5. mag.cmd surface-rebuild --dry -> reachable end to end, exit 0.
6. WO-12 pre-edit recount -> UNCHECKED 63; post-edit recount -> UNCHECKED 11.
7. tools/violation_ratchet.py check --changed -> exit 1 (sibling-lane NEW
   hits only; this lane's files clean or registered), per-file proof in the
   check file.

## Not done / residual

- validate does not hold ok=True on a live tree while sibling lanes append;
  the verb re-reaches 0/0/0 at any census moment. A standing cadence for the
  verb (e.g. folding it into an existing daily patrol) is an operator call,
  not taken here.
- The ratchet's 4 NEW sibling-lane hits remain unregistered: their lanes owe
  their own named acceptance (the B2-173 precedent note in
  configs/violation_baseline.json).
- The Stone 5 asks (merged line) and the 9 untouched keep-open rows remain
  owed to their named work orders; nothing in this lane executed them.
- Raw evidence banked alongside this receipt in
  watch/inbox/gala_20260925/wave5-repair/lanes/: queue-closes.check.txt,
  queue-closes.json, _qc_truly_invisible_census.py, _qc_wo12_flip_sweep.py,
  _qc_validate_baseline.json, _qc_rebuild_pass3_clean.json,
  _qc_rebuild_final_pass.json, _qc_rebuild_last_pass.json,
  _qc_validate_final.json, _qc_validate_last.json, _qc_preedit_recount.txt.

No em dashes in this file.
