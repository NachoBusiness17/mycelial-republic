# B2-284 receipt (2026-09-26)

## Verdict

LANDED. The Shared-file claim law now names shared test surfaces: the QUEUE.md header paragraph carries the B2-284 extension (claim the tests/ path itself, or the module with the test pair named in the reason), and the falsifier replay (B2_284_claim_replay.py, exit 0) proves the gap and its closure on temp copies of the real shared suite tests/test_census_drift_patrol.py: with tests/ silent, a targeted pytest against the half-written shared suite errors with no claim to detect; under the extension the second lane detects the foreign claim on the same board re-read, rebases, and both edits survive.

## Evidence file:line quotes

- The disease being closed: watch/inbox/burn_wave_20260926/B2_245_parser_order_20260926.md Evidence mid-lane paragraph (targeted pytest over the shared suite read "25 passed, 13 errors" on half-written bytes mid-lane); the codified law (QUEUE.md header, Shared-file claim law paragraph) named only `<repo-relative-path>` with module examples and never said tests/ was claimable, so a lane editing only the shared suite had no claim to file and no foreign claim to detect.
- QUEUE.md header after this lane's edit, appended to the law paragraph directly after the B2_250 replay sentence: "Test surfaces are in scope from 2026-09-26 (B2-284, self-fed by B2-250): a lane about to edit a shared tests/ file (or a module-plus-test pair edited together) claims the tests/ path itself, or claims the module and names the test pair in the reason ... replay: watch/inbox/burn_wave_20260926/B2_284_claim_replay.py".
- Replay scenario A (tests/ silent), on a temp copy built from the live suite bytes: half-write chosen as a truncation at a "\ndef test_" boundary with an unclosed def signature (provably failing compile; the first cut shape tried, ending in a complete-looking "assert tr" tail, parsed clean and was rejected as a fake half-write, which is itself evidence the observed "13 errors" shape needs a mid-statement cut); lane B's targeted pytest --collect-only against it returned the ERROR shape while the claim grammar (modules only) gave B no claim to detect.
- Replay scenario B (extended law): lane A claims "tests/test_census_drift_patrol.py" before touching it; lane B's queue re-read detects the foreign claim on the shared test surface, re-reads the completed bytes, rebases, and the targeted collection is clean with both lanes' edits present.

## Work done

1. Read the codified law paragraph and the B2_250 replay probe; kept the same temp-copy discipline (live bytes, no live-file mutation).
2. Built the replay with a genuine half-write: rejected my first truncation shape because it compiled clean (a complete-looking tail inside a parseable module), which sharpens the receipt's account of why the 13-errors interleave was real and not a fluke.
3. Extended the law text in the QUEUE.md header in the same breath as the replay passing (the edit arm of the brief: "extend the claim shape to accept a tests/ path or a module-plus-test pair").
4. The probe and this receipt are registered in the law paragraph so future lanes find the surface extension where the law lives.

## Falsifier

The brief's falsifier: replay the interleave with tests/test_census_drift_patrol.py as the shared surface and observe the second lane's targeted pytest reading a half-written other-lane fixture with no claim to detect. Scenario A reproduces exactly that (ERROR shape, detection surface empty). It stays reproducible while any lane treats the suite as unclaimable; the moment a lane follows the extended law, scenario B's detection fires (claim regex requires "- CLAIM " plus the path, and the path is the tests/ file itself). The extension fails if a lane claims the module but edits only the test file (the grammar covers that only via the module-plus-test pair wording in the reason), which is the named convention this receipt pins; the replay re-runs as-is and must keep exiting 0.

## Bibliography closed

- watch/inbox/burn_wave_20260926/QUEUE.md (Shared-file claim law paragraph, extended; B2_250 landing row 157 read)
- watch/inbox/burn_wave_20260926/B2_250_file_claim_replay.py + B2_250_file_claims_20260926.md (the module-surface precedent this extends)
- watch/inbox/burn_wave_20260926/B2_245_parser_order_20260926.md (the mid-lane symptom paragraph)
- tests/test_census_drift_patrol.py (live suite bytes, 566 lines, unmodified; temp copies only)
- watch/inbox/burn_wave_20260926/B2_284_claim_replay.py (new artifact, exit 0)
