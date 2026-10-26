# B2-451 scenario-gate hook pairing pin (2026-09-26)

## Verdict

LANDED. tests/test_scenarios_gate_hook_pin.py (4 pins, all green) now reads
the B2-164 block's contract from the REAL githooks/pre-push bytes and
replays it with real sh, the B2-338 pattern applied to the scenario gate:
(1) the block's shape from bytes (lowercase-ok arm present, enforcing exit 1
present, unchanged-arm skip line present, no uppercase OK token anywhere);
(2) a real green run of tools/workflow_gate.py check --scenarios over the
landed 7-card suite opens "SCENARIOS ok" AND matches the hook's extracted
case-arm pattern; (3) an error fixture (malformed card JSON -> "SCENARIOS
ERROR" first line) falls to the BLOCK arm; (4) the brief's exact falsifier
is pinned as a test: flipping the pattern to "SCENARIOS OK" makes the green
first line STOP matching, so a case regression in the hook lands loudly.
Disclosure: one combined-run batch showed teardown PermissionErrors on tmp
dirs (WinError 5, the same host-environment disease B2-439 disclosed on
agents/pytest-tmp); both files pass clean on rerun (46 passed), and each
pin passes standalone.

## Evidence file:line quotes

- The block under pin, githooks/pre-push:302-309 (real bytes): case arm
  `"SCENARIOS ok"*)` -> ok echo; `*)` arm -> "BLOCKS the push" + `exit 1`;
  else arm "workflow_gate_scenarios skipped, gate script unchanged"; the
  block comment (lines 277-283) states the first-line contract this pin
  freezes ("run_scenarios' FIRST printed line is a per-card 'SCENARIOS ok
  ...' row; red runs open with 'SCENARIOS FAIL', errors with 'SCENARIOS
  ERROR' ... the case arm matches the lowercase-ok first line and is never
  widened").
- Pin 2 (green, real): the 7-card suite runs clean, first line starts
  "SCENARIOS ok", and the pattern extracted from hook bytes via
  OK_LINE_RE (group 2 = `"SCENARIOS ok"*`) replays OK_ARM under
  `sh -c 'case "$1" in <pattern>) echo OK_ARM ;; *) echo BLOCK_ARM ;; esac'`.
- Pin 3 (red, fixture): a tmp cards dir holding broken.card.json ("{not
  json") makes run_scenarios open "SCENARIOS ERROR"; the replay lands
  BLOCK_ARM (in the hook: exit 1).
- Pin 4 (the brief's falsifier, byte-true): pattern.replace("SCENARIOS ok",
  "SCENARIOS OK") no longer matches the green first line -> BLOCK_ARM, so
  the case regression cannot land silently.
- Mid-lane corrections, named because they shaped the pin: the first regex
  copied the census block's `("..."*) : ;;` tail which this block does not
  have (its arm body runs echoes, not `: ;;`), and the leading literal `(`
  in my first pattern does not exist in the arm (the sh pattern is
  `"SCENARIOS ok"*` alone); fixed to `^(\s*)("(?:SCENARIOS ok)"\*)\)\s*$`
  with re.M and group(2). A block-shape assertion originally cut on the
  skip line before reading it; split moved to the `else` boundary.

## Work done

1. Read the real block bytes (githooks/pre-push:210-311) and the B2-338
   replay pattern in tests/test_census_drift_patrol.py:525-570.
2. Wrote the 4 pins fixture-first (real hook bytes, real tool runs, real sh
   replay; no synthetic contract).
3. Iterated the arm-extraction regex against real bytes until the census
   pattern's shape and this block's shape were both handled; corrected two
   wrong assumptions (documented above).
4. Ran: 4 passed standalone; combined with the census sibling suite 46
   passed on rerun after disclosing the transient tmp-teardown flake.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

These pins are inverted if any of the following holds: (a) changing
"SCENARIOS ok" to "SCENARIOS OK" (or any quote/case/exit regression) in the
hook block and running this file does NOT go red (the extraction regex
over-matches; that would be the pin crying wolf in reverse);
(b) the real card suite goes red for an unrelated reason and pin 2 starts
failing without any hook change (the pin is fine but the SUITE is red -
which is exactly what the hook exists to catch, so the pin failing here is
the system working); (c) the skip line or exit 1 is removed from the block
and test_hook_block_shape_from_real_bytes stays green (the block-split
boundary drifted from the real bytes).

## Bibliography closed

githooks/pre-push (real bytes read: caption/refold blocks for the --changed
shape, scenarios block for the contract); tests/test_census_drift_patrol.py
(B2-338 replay pattern read and mirrored); tools/workflow_gate.py
(run_scenarios first-line contract read: lines 210-265); configs/workflow_gate_scenarios/G1_multiplicity.card.json
(card shape read); live tool runs (2 green + 1 error fixture). No network
calls.
