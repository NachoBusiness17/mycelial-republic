# OUROBOROS R3 LAND: CONSENSUS DEGENERACY REFUSED + SEAL PATROL TAMPER-PROOFED

Seat: R3-L3 landing lane (ouroboros round 3, moves 3 and 4 of the fold).
Moment: 2026-10-05T23:19Z. Fold:
`watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md`
(blindness rows 3 and 4). All numbers below byte-derived from the runs named
beside them; interpreter `.venv\Scripts\python.exe` throughout; no commit made.

## Move A: the four degenerate consensus shapes now refused

1. UNANIMITY OF ONE (consensus_gate.py): `verdict()` now honors
   `sample_count` with an n>=2 floor; the effective n is
   `min(real answer pool, sample_count)`, so a claim can lower the count but
   never inflate it. The fold's exact probe
   `verdict(["the answer is 42"], model_params_b=27)` returns UNVERIFIED
   (was CONFIRMED); a claimed `sample_count=5` behind one answer stays
   UNVERIFIED; two real agreeing samples at 30B still CONFIRM.
2. REFUSAL-SHAPE UNANIMITY (consensus_gate.py): leading-anchored refusal
   classification (`REFUSAL_PREFIXES` + `_is_refusal`); refusal-shaped
   responses are stripped before unanimity, so a refusal triplet at 27B is
   UNVERIFIED (was CONFIRMED), a mixed refusal+2-agreeing pool still
   confirms, and a mid-sentence "I don't know why" in a real answer is not
   stripped. All-refusal is never DISPUTED (a refusal abstains).
3. BYTE-IDENTICAL WITNESS INFLATION (memweave.py consensus_quality): the
   `independent` boolean is demoted to advisory; correlated (incl
   byte-identical) answers count as ONE witness regardless of flags. The
   fold's exact probe `consensus_quality(["x"]*4, independent=[True]*4)`
   returns n_effective 1.0 / correlated_weak (was 4.0 / strong).
4. STRONG PATH WITHOUT EVIDENCE (memweave.py): new `construction` param
   carries a per-answer construction token (a distinct ask digest or a
   cross-family stamp); a correlated answer joins the witness set only when
   its token differs from every correlated witness's token AND both sides of
   the pair carry tokens (one token against a tokenless witness is still a
   ticket). Four identical answers with four distinct tokens = 4 witnesses
   strong; duplicate or empty tokens = 1 witness. `consensus_merge` passes
   `construction` through.
   - Caller compat: `mag/claims_verify.py` now supplies REAL construction
     evidence (sha256 of each code path's own source: `replay` vs
     `_independent_reconstruct`), so its byte-identical dual roots still
     certify strong (verified: n_effective 2.0) on evidence instead of a
     boolean.
   - Preserved B3 semantics: unanimous unflagged pool = correlated_weak;
     dissenting pool = strong; rho closed form untouched.

Tests: `tests/test_consensus_degeneracy_20261005.py` (19 tests, one per
degenerate shape plus preserved legit paths). Existing consensus carrier
tests green: `tests/test_b3_merge_actor_20261005.py` (8 tests).

## Move B: the seal patrol certifies bytes, order, and chain

`tools/prepush_seal_patrol.py` reworked (397 lines, ratchet clean):

- MAX-TS SELECTION: operative seal per file = newest parseable ts (ties by
  ledger line). The fold's backdated-mask shape (CLEAN on a violated newest
  seal under last-row-wins) now alarms; forged-fresh-row shape now alarms
  through the witness rule: a row with no writer and no same-file same-sha
  register partner cannot clear a file whose witnessed seals are
  prefix-broken (class `unwitnessed`).
- APPEND/REWRITE TAXONOMY: the autoseal `bytes` stamp (register rows inherit
  it from their same-sha pair) plus a one-pass incremental prefix hash
  (`_digest_checkpoints`: digest snapshots at every sealed length) classify
  prefix-pure APPEND (quiet, counted in the head line) vs prefix-broken
  REWRITE (alarm naming ledger line + stamped sealed length + file size).
  No stamp anywhere = unknown-class drift, still visible (old behavior).
  A proper rewrite-then-re-seal stays quiet (newest seal exact-matches).
- CHAIN VERIFY (exit 2): per writer, nonce/seq must never step backward in
  the window (backward = forged/reordered row); rows carrying `prev` must
  digest-chain (`_row_digest`) to the immediately preceding sha-bearing row.
  Batch seals sharing a nonce (10 measured duplicate steps in the live
  window's md-record-seal rows) and forward gaps (multi-surface writer
  history, measured across the ledger census in this receipt's working
  notes) are never fatal. Chain break outranks drift: exit 2.

Tests: `tests/test_seal_patrol_tamper_20261005.py` (13 tests: both forged
shapes, append quiet, rewrite evidence, shrink, re-seal quiet, register
bytes inheritance, backward nonce/seq exit 2, prev-digest good+bad,
batch+gap quiet, max-TS unit). Existing `tests/test_seal_patrol.py` (7
tests) green unchanged, including the ts-less fixtures (last-row-wins
fallback among ts-less rows) and the uppercase-seal case law.

## The --rows 1000 rerun (moment-bound, the board is live)

Baseline pre-landing (2026-10-05T22:5xZ, old organ): 324 distinct files,
300 match, 13 drift, exit 1. Post-landing (2026-10-05T23:19:14Z): 325
distinct, 298 match, 1 append-quiet, 11 missing-on-disk, 15 drift findings
(12 rewrite + 3 unknown), 0 chain breaks, exit 1. The population moved
between the two moments (sibling seats live-sealing and editing boards; the
ledger grew 10940 to 10944 sha rows during this sitting), which is the
fold's own finding: a moving surface needs moment-named numbers, not a
constant. The two true divergences the fold weighted are named rewrites:
`watch/inbox/ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl` and
`corpus/steal/MASTER_EXECUTE_REGISTER.md`. The ask's 10 drifts (the hostile
pass's 12 = 3 byte-pure appends + 9 rewrites) resolve exactly through the
new taxonomy: every rewrite-class stays visible with prefix evidence;
append-class boards go quiet by design; re-seal of the rewrite-classed
boards remains the operator call the fold left open.

## Gates

- pytest: 56 passed, 0 failed across tests/test_seal_patrol_tamper_20261005.py
  + tests/test_seal_patrol.py + tests/test_consensus_degeneracy_20261005.py
  + tests/test_b3_merge_actor_20261005.py + tests/test_kv_seal.py +
  tests/test_md_record_seal.py (the estate has no other consensus_gate or
  seal-patrol test carriers; blast radius grep over tests/ + tools/gps_mcp).
- Ratchet: `tools/violation_ratchet.py check --changed` = PASS, NEW=0 (the
  first cut tripped file-too-long at 424 lines; cured by docstring/ dead
  `file_sha256` removal, 397 lines; never baselined).
- Dash law: zero em/en-dashes on every line this lane added (4 in drafted
  comments caught and fixed pre-receipt; pre-existing prose untouched).
- No git commit (lane law).

## Incident note (the live-repo hazard, filed not hidden)

At 19:00 local (23:00Z) a sibling process reverted `mag/` to HEAD mid-sitting
(equivalent of `git restore mag/`), wiping this lane's first
consensus_gate/memweave/claims_verify edits while tools/ and tests/
survived; caught by the gate rerun (11 test failures), re-applied, and the
final numbers above are from the re-applied bytes. Nothing in this receipt
rides on the wiped intermediate state.
