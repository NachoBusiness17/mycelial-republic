# B2-365 receipt: census_drift_patrol.py ratchet-cap split (2026-09-26)

## Verdict

LANDED. The --collect collectors block (COLLECT_TAIL_RE, parse_collect_tail, parse_collect_files, collect_report) moved verbatim into the new sibling tools/census_collect.py per the B2-248 split precedent; tools/census_drift_patrol.py dropped from exactly 400/400 ratchet lines to 382 with its public attribute surface frozen (thin delegating defs keep cdp.parse_collect_tail / cdp.parse_collect_files working for the self-test and the test suite, and run() reaches collect_report through the same lazy sibling import the B2-248 delegation established). Behavior frozen: self-test 30/30 PASS exit 0, tests/test_census_drift_patrol.py 46 passed, py_compile clean on both files. The brief's falsifier act (append 2 lines, run the ratchet) no longer produces NEW file-too-long for this file: with the split, +2 lines lands 384, under the bar; verified live with the file restored byte-identical afterward (sha 87b953875a310353 before and after the falsifier act).

## Evidence file:line quotes

- Brief (QUEUE.md B2-365 row): "rides the ratchet cap at exactly 400 of 400 lines ... the next touch that adds more lines than it removes blocks pre-push on NEW debt; falsifier: append 2 lines to tools/census_drift_patrol.py and run tools/violation_ratchet.py check --changed, it shows NEW file-too-long".
- Pre-split bytes: wc -l = 400 exactly, sha256 head ffe096be (the same pin the B2-469 receipt recorded as "zero-touch"; the claim line for this edit was appended to QUEUE.md BEFORE the file bytes were read, per the shared-file claim law, ts 19:54:42Z).
- tools/violation_ratchet.py:44 "FILE_LINE_CAP = 400" and :135-136 "if n_lines > FILE_LINE_CAP: found.append({\"rule\": \"file-too-long\", ...})".
- Post-split measurement: wc -l = 382 (census_drift_patrol.py) and 84 (census_collect.py); ratchet check --changed after the +2-line falsifier act flagged no census file (the only NEW row in scope, mag/shared_surface.py file-too-long, belongs to another lane's in-flight edit and is untouched by this lane).
- tools/census_collect.py docstring: "This module imports nothing from census_drift_patrol (no circular edge)" and "collect_report ... CollectError ... census_drift_patrol.run() maps it to exit 2 exactly as it maps its own PatrolError".
- tools/census_drift_patrol.py run() collect branch now: `collectors = _collect_mod()` / `except collectors.CollectError as exc:` -> "CENSUS-PATROL: cannot verify collect deep check" exit 2, the same cannot-verify contract as before the split.

## Work done

1. Claimed the file (QUEUE.md CLAIM line SW-05, ts 19:54:42Z, naming pre-write sha ffe096be) before reading the bytes to edit, per the shared-file claim law; the file is git-untracked and hot (B2-244/B2-245 co-edit history, B2-469 zero-touch pin).
2. Created tools/census_collect.py (84 lines) holding the moved block verbatim with CollectError defined locally so the sibling has no reverse dependency; updated docstrings on both sides naming the split, the cause (400/400 cap) and the frozen surface.
3. Edited census_drift_patrol.py: removed the moved block, added _collect_mod() (lazy import, script-dir-first, the B2-248 context rule), two delegating defs, and the CollectError-aware collect branch in run(). COLLECT_DRIFT_TOLERANCE stays in the patrol (CLI default).
4. Verified: py_compile both files; census self-test PASS (30 check groups incl. the 5 collect-tail/files/patrol groups now exercising the delegated path); pytest tests/test_census_drift_patrol.py 46 passed in 12.64s; falsifier act (+2 lines, ratchet, restore) with sha proven identical across the act.
5. Retired the claim line (CLAIM -> CLAIMED with this receipt pointer) at landing.

## Falsifier

The brief's falsifier was the disease proof: at 400/400, +2 lines showed NEW file-too-long. After the split the same act is clean (382+2 = 384 < 400), and the split dies if any of: (a) the attribute surface breaks, i.e. census_patrol_selftest or tests/test_census_drift_patrol.py can no longer reach cdp.parse_collect_tail / cdp.parse_collect_files / cdp.collect_report; (b) the deep check's cannot-verify contract changes, i.e. a pytest --collect-only failure surfaces as anything but "CENSUS-PATROL: cannot verify collect deep check" with exit 2; (c) census_collect.py grows past 400 lines itself (84 today, the same disease one sibling over); (d) the --collect behavior drifts, i.e. a rerun of `.venv/Scripts/python.exe tools/census_drift_patrol.py --collect --root <root>` prints a different verdict shape than the pre-split head/fix lines (B2-338's lowercase ok prefix included).

## Bibliography closed

All read this lane: tools/census_drift_patrol.py (in full, pre + post), tools/census_collect.py (new, this lane), tools/census_patrol_selftest.py (collect-tail/files/patrol check groups, injection pattern), tests/test_census_drift_patrol.py (import shape, attribute access, 46 tests run), tools/violation_ratchet.py (FILE_LINE_CAP), QUEUE.md (B2-365 row, claim law text, CLAIM line appended and retired), memory/burns/LEDGER.jsonl B2-469 row (ffe096be pin), B2_220_dotted_guards_20260926.md (co-edit history context via QUEUE pointers), configs/violation_baseline.json (checked for census entries, none touched).
