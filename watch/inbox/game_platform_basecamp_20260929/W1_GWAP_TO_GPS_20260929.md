# W1: gwap_to_gps -- the fail-closed bridge (2026-09-29)

Mickey17 Wave 1 lane. Closes the "missing dogfood" from wave ledger return 3
(watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md): gwap_payload mints hash-chained
verdicts, gps_mcp prices models by verdicts, nothing connected them. Now one
metabolism feeds both organs.

## Files

- `mag/gwap_to_gps.py` (287 lines) -- `feed_session(session_path, gps, *, task_shape, scene_to_model, participant_to_model)` walks one gwap session JSONL, verifies the whole chain first, plans every row, then feeds `tools/gps_mcp/ledger.py record_verdict`. Accepts a `CapabilityLedger` or a sqlite path.
- `tests/test_gwap_to_gps.py` (342 lines) -- 15 tests: clean feed, evidence-hash identity, tampered chain refuses with zero writes, missing file refuses, empty file feeds zero, unknown verdict refuses on a chain-valid file, all four verdict branches, skip-only sessions never touch the capability table, collusion downgrade lands as skip, participant map / scene precedence / unmapped / no-map refusals, custom task_shape.

## The three disagreements, resolved

1. **Verdicts, 4-valued vs binary.** VERIFIED_AGREE -> verdict 1 (pass); DISPUTE -> verdict 0 (fail); CHALLENGE and BLOCKED are skips: counted in the returned report (`by_verdict`, `skipped`), never sent to record_verdict, so judge-owed and tabooed rows can neither inflate nor deflate a pass_rate. The v1 collusion downgrade lands on CHALLENGE, so tainted rows skip too: collusion has no priced consequence until a judge promotes the row, and the router sees only clean signal meanwhile.
2. **Evidence hash.** `row_sha256` (chain position), not `meter_credit.receipt_sha256` (build-time body receipt): the receipt does not identify a ledger position and identical payloads in two sessions share it, while row_sha256 binds seq + ts + payload + prev, so an auditor can re-walk `verify_chain_file` straight to the exact row that earned the verdict. Pinned by `test_evidence_hash_is_row_sha_not_receipt`.
3. **Key mapping (the invention).** gps is keyed `(model_id, task_shape)`; gwap rows carry scene_id + participants. Decision: `task_shape` is a caller argument defaulting to `gwap-agreement-v1` (one shape per verdict source). `model_id` resolves by strict precedence: (1) caller `scene_to_model` map on scene_id (scene is the unit the payload keys itself by); (2) else caller `participant_to_model` map consulted for the intent author, the robber: the robber's intent is the work product under verification, cop/witness are instruments, so the robber is the model under test. NO identity fallback (scene_id-as-model, first participant): a guessed key quietly seeds some other model's capability row and routing dollars follow. A miss raises `UNMAPPED_SCENE` / `UNMAPPED_PARTICIPANT` / `NO_KEY_MAP`.

## Fail-closed shape (a mid-run finding, fixed)

First cut fed rows inside the walk, so an unmapped scene on row 2 left row 1 already scored -- exactly the partial-feed damage the chain law forbids for tampered files. Fixed with a two-pass feed: pass 1 validates schema + verdict + key-map for EVERY row into a plan; pass 2 executes record_verdict only after the whole plan holds. Any refusal (BROKEN_CHAIN, MISSING_SESSION, BAD_PAYLOAD, UNKNOWN_VERDICT, unmapped keys) now leaves the gps ledger byte-untouched. Tests pin all three original failures.

## Proof

- `pytest tests/test_gwap_to_gps.py -q` -> **15 passed in 0.90s** (repo venv `.venv/Scripts/python.exe`, 2026-09-29).
- `python -m mag.gwap_to_gps` demo: 2-row session (1 pass, 1 fail) -> capability row `pass_rate 0.5, sample_size 2`, skips 0.
- Ratchet `check --changed`: zero findings in these files (two pre-existing flags in other lanes' changed files: `tools/regen_front_door.py`, `mag/corpus_selfsteal.py`).
- Em-dash count in both new files: 0 (`grep -c` byte truth).

## Ownership

New files only: `mag/gwap_to_gps.py`, `tests/test_gwap_to_gps.py`, this receipt. No git commit (per lane order). Downstream debts: the judge queue that promotes CHALLENGE rows, and wave return 19's ledger registry mount for cross-ledger evidence lookup by row_sha256.
