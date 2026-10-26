# B2-117 Build-lane error-class census mapping, 2026-09-26

## Verdict

LANDED. The implicit reviewer convention is now executable law: scripts/build_lane_game.py carries the frozen class mapping (KeyError 'choices' + explicit 200_error_body fold into 200-error-body; HTTP 404; empty_content; IncompleteRead; schema gate; BFS "exhausted @" -> merit) and a `--census` subcommand keyed to the frozen denominator 41. Run live this lane: frozen_source "git:3d12289f9", 71 committed rows, 41 FAIL rows, tally 200-error-body 16 / http-404 11 / empty_content 9 / schema-gate 2 / incomplete-read 1 / merit 2, reconciled: true, exit 0. The classifier reproduces B2-33's hand recount byte-exactly from committed bytes (no hand classification needed anymore). Live tallies ride along: 114 rows / 82 FAIL (http-404 grew 11 to 51 with the 09-26 pareto-window 404s, schema-gate 2 to 3), so future recounts are one command, not a lane.

## Evidence file:line quotes

- scripts/build_lane_game.py module docstring (post-edit): "CENSUS: .venv\\Scripts\\python.exe scripts\\build_lane_game.py --census" and "KeyError 'choices' ... fold into class 200-error-body (frozen 16 = 12 + 4) ... 16+11+9+1+2+2 = 41".
- scripts/build_lane_game.py constants: FROZEN_CENSUS_20260917 = {"200-error-body": 16, "http-404": 11, "empty_content": 9, "schema-gate": 2, "incomplete-read": 1, "merit": 2}; FROZEN_COMMIT = "3d12289f9"; COMMITTED_PREFIX_ROWS = 71 with the comment "B2-33: 71 rows committed at git 3d12289f9, 41 FAIL; a byte-prefix of the live file".
- _error_class mapping lines: `if "KeyError" in err or "200_error_body" in err: return "200-error-body"`; `if "404" in err: return "http-404"`; merit arm `gate.startswith("FAIL") and "exhausted @" in gate`; schema arm `gate.startswith("schema:")`.
- Live run output (this lane, 2026-09-26 19:5xZ): {"frozen_source": "git:3d12289f9", "frozen_window_rows": 71, "frozen_window_fail_rows": 41, "frozen_window_tally": {"200-error-body": 16, "http-404": 11, "empty_content": 9, "schema-gate": 2, "incomplete-read": 1, "merit": 2}, "reconciled": true, "live_rows": 114, "live_fail_rows": 82, "live_tally": {"http-404": 51, "empty_content": 9, "merit": 2, "200-error-body": 16, "schema-gate": 3, "incomplete-read": 1}}.
- B2_33_rejection_recount_20260926.md Evidence: "git 3d12289f9 ... Class tally from those committed bytes: 200-error-body 16 (12 "KeyError: 'choices'" + 4 explicit "200_error_body"), 404 11, empty_content 9, schema 2, IncompleteRead 1, merit 2. Sum 41 exact" and "committed 71 rows are a prefix of today's 111".
- Merit rows are BFS exhaustion, live file: gate "FAIL  [ruins_go_pack_cand_P-collapse-crank.json] P01 Paid Passage · exhausted @2" (ts 2026-09-17T14:28:44.928090Z) and "P08 Measured Sentry · exhausted @20" (P-spear-rhythm) — the 2 frozen merit rows.
- First _census draft keyed the frozen window by ts prefix 2026-09-17 and got 35 rows / reconciled false: the frozen window is the committed 71-row snapshot (through 2026-09-18T03:56Z commit time), not a calendar day; fixed to read the git blob with the prefix fallback.

## Work done

- Read B2_33_rejection_recount_20260926.md whole; read scripts/build_lane_game.py header, _call error paths (200_error_body, empty_content), transport-prune tuples, gate shapes; classified all live FAIL rows by hand-rule first to validate the mapping before writing it.
- Spec first: extended the module docstring with the CENSUS contract and the exact mapping before the code, same edit.
- Added FROZEN_CENSUS_20260917 / FROZEN_COMMIT / COMMITTED_PREFIX_ROWS constants, _error_class, _census (git-show preferred, 71-row prefix fallback, disclosed as frozen_source), and the --census argparse branch that returns before lock/env so the census never touches state or the network; read-only on proposals.jsonl.
- Ran --census live: reconciled true against the committed snapshot. py_compile clean. Ratchet check --changed: the only NEW hit is mag/shared_surface.py:407 file-too-long, a concurrent lane's in-flight file, zero edits from this lane; scripts/ is outside the mag/+tools/ ratchet scope. Em-dash count in added lines: 0 (the one + diff line carrying an em-dash, "primary — the run alternates", is HEAD-carried text from the concurrent lane's block, verified `git show HEAD` contains it).
- Claim law honored: CLAIM SW-00 line filed on QUEUE.md before editing the working-tree-modified script, retired at landing.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any future --census run printing frozen_window_tally different from FROZEN_CENSUS_20260917 while frozen_source is git:3d12289f9 kills the mapping (the committed bytes are immutable; only a classifier bug can move the tally).
- A FAIL row that is neither error-bearing nor "schema: " nor "exhausted @" lands in "unclassified": the mapping is exhaustive only over the observed classes; a new transport shape (e.g. a 429 body) will show there and must be mapped by a follow-up, not silently folded.
- The KeyError fold is reviewer convention, not wire truth: a 200-with-JSON-body whose "choices" KeyError came from a schema change (not an error body) would be miscounted into 200-error-body; the frozen window pins the convention, the live tally discloses the risk.
- Deleting or rewriting build_lane/proposals.jsonl breaks the prefix fallback and the git blob path (file renamed away from 3d12289f9's tree) — then the census honestly errors instead of reconciling.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_33_rejection_recount_20260926.md (whole); scripts/build_lane_game.py (header, _call error paths, transport tuples, main argparse; post-edit whole); watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl (114 rows classified this lane); git show 3d12289f9:watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl (71 rows, census source); tools/violation_ratchet.py check --changed output. No web sources. Em-dash count 0 in this receipt.
