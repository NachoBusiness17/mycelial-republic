# burn lane no_win: test_reframe_keeps_invariant_changes_conditions root cause + fix

Date: 2026-09-27 · Lane: burn reset evening 4/10 (`watch/inbox/BURN_RESET_20260927_EVENING.md`)
Files touched: `mag/no_win.py` (code under test), this receipt. Test file NOT touched: the test
asserted the correct contract; the product code carried the defect.

## Root cause (proven from bytes)

`tests/test_no_win.py:33` asserts `"REFRAME" in r["move"]`. The move string in `mag/no_win.py`
emitted `REFRAIM[...]` — a misspelling, not a contract:

- The module's own frozen spec (docstring, lines 7-8) says "The move is to **REFRAME** the
  invariant". The primitive is named `reframe`; "reframe(s)" is the vocabulary of the docstring,
  the play string, and the test RIB. `REFRAIM` appeared exactly once in the live module (the move
  f-string) plus the `REFRAIMS` dict name — the signature of one typo event at module creation.
- A prior audit called the test pin stale: `memory/audit_20260926/lane4_robustness.json:151` and
  `watch/inbox/audit_20260926/LANE4_TEST_ROBUSTNESS.md:69` ("Product string is REFRAIM[...]; test
  pins REFRAME. One letter."). That call did not check the module's own docstring vocabulary; the
  bytes say the product string carried the typo. The job rule (fix the defect in the code under
  test; prove stale contracts from bytes) resolves in favor of REFRAME.

Second, latent, byte-proven defect in the same code path: `_classify` mapped the test's constraint
"this can't be verified deterministically" to the `not_enough` **default** instead of
`unverifiable`, contradicting the module's own mapping comment (`mag/no_win.py` ~line 43:
`"this can't be verified/done deterministically" -> shift the invariant`). Cause: the regex stem
`can't (be )?(prove|verify)` cannot match the inflected forms "verified"/"proven"/"proved"
(`re.search(r"can't (be )?(prove|verify)", "this can't be verified")` returned None, verified
before the fix). The test only pins `REFRAME in move` so this did not fail the assertion, but the
constraint was clearly written to exercise the unverifiable frame.

## Fix (`mag/no_win.py`)

1. `REFRAIM[` -> `REFRAME[` in the move f-string; dict `REFRAIMS` -> `REFRAMES` (module-internal,
   sole consumer is `frame()`; grep confirmed no other importer of `mag.no_win` in the repo outside
   its test). Fix comment names cause + evidence receipt.
2. unverifiable regex accepts inflections: `can't (be )?(prove|proven|proved|verify|verified)`.
   Fix comment names the cause and the mapping-comment contract.

Archived copies under `corpus/oral_history/.../mag-disk/mag/no_win.py` and
`dist_audit/nacho_business_audit_20260912T214050Z/mag/no_win.py` are historical receipts and were
intentionally not touched.

## Real numbers

- Before: `pytest tests/test_no_win.py -v` -> 1 failed, 3 passed in 0.79s
  (failure: `assert 'REFRAME' in "REFRAIM[not_enough]: more force inside the frame won't win; ..."`).
- After: `pytest tests/test_no_win.py -v` -> **4 passed in 0.52s** (file is the only importer of
  `mag.no_win`; grep-verified).
- Classifier post-fix: "this can't be verified deterministically" -> `unverifiable`,
  move = `REFRAME[unverifiable]: don't push harder to prove it; redefine the invariant so it can be
  proven.`; the five constraints in `test_reframe_never_refuses` still classify to distinct frames
  (unverifiable / no_adoption / too_costly / no_path / not_enough).
- CLI smoke: `python -m mag.no_win` -> ok:true, schema no_win.v1.
- Gate: `tools/violation_ratchet.py check --changed` -> PASS, hits=0, NEW=0 (scope=1 changed file).
- `pytest --collect-only -q tests/test_no_win.py` -> 4 collected.
