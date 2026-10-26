# B2-402 Improve-loop and workday tests write real bytes

## Verdict

LANDED. Both test files now run with injected write roots (module-constant monkeypatch, the surface-fixture shape): (1) tests/test_improve_loop.py redirects mag.improve_loop.HANDOFF_DIR and TRAIL plus mag.operator_inbox.EVENTS_PATH to tmp_path via an autouse fixture - proven live: queue/handoff/ held 183 files before and 183 after a full test run (pre-fix: +1 cloud-*.json per run); (2) tests/test_chat_source_agent_workday.py redirects mag.registry RESIDUAL_DIR/DERIVED_DIR/REGISTRY/LATEST_SESSION, mag.biography.SUMMARIZED, and stubs mag.verkle_knot.append_verkle_knot so the test never touches the real chain; its residual assert now points at the injected dir. Falsifier inverted on both arms: a fresh test_improve_loop run no longer grows queue/handoff/, and the workday test leaves no residual file on bytes. Residue disposition: 51 pytest-source handoff files DELETED (file-shaped, reclaimable) plus the stale mag-agent-_pytest_agent_wd.json residual (36,827 B) DELETED; the append-only rows are REGISTERED, not erased: 61 source=pytest rows in logs/behavioral_events.jsonl, 88 in memory/runs/improve_loop_trail.jsonl, 1 pytest-session row in memory/biography/registry.jsonl (reclaimable debt, reclaim needs a dated compaction policy, not a lane edit). Suites: 5 passed across both files.

## Evidence file:line quotes

- tests/test_improve_loop.py (post-fix) module docstring: "every run dropped a real cloud-*.json into queue/handoff/ (55 -> 56 in the B2-359 probe window; 43 pytest-source files on bytes) and appended real source=pytest rows to logs/behavioral_events.jsonl (53) and memory/runs/improve_loop_trail.jsonl (72)" with the autouse _isolated_write_roots fixture (HANDOFF_DIR, TRAIL, EVENTS_PATH).
- tests/test_chat_source_agent_workday.py (post-fix) test_resolve_and_file_agent_session: the B2-402 comment block + reg/bio/vk patches; the residual assert redirected to reg.RESIDUAL_DIR.
- Live proof: "handoff files before: 183 after: 183"; post-cleanup re-run "5 passed" with queue/handoff count unchanged (132 remaining files are non-pytest content) and zero pytest matches in memory/biography/residual/.
- Residue census (this lane): behavioral_events source=pytest 61, improve_loop_trail source=pytest 88, registry pytest-session 1; removed: 51 cloud-*.json + 1 residual file.

## Work done

1. Read the two test files and traced every write surface (improve_loop HANDOFF_DIR/TRAIL, operator_inbox EVENTS_PATH, registry RESIDUAL_DIR/REGISTRY/DERIVED_DIR/LATEST_SESSION, biography SUMMARIZED, verkle_knot.append_verkle_knot).
2. Added the autouse isolation fixture to test_improve_loop.py with the cause-carrying docstring; proved the handoff dir stops growing (183/183).
3. Injected the biography roots + verkle stub into the workday test and redirected its residual assert to the injected dir; 3 passed.
4. Dispositioned the residue: 51 pytest-source handoff files + 1 stale residual DELETED (file-shaped debt); 150 append-only rows REGISTERED here by name and count (reclaim = a dated compaction policy, deliberately not done in-lane on append-only surfaces).
5. Re-ran both suites (5 passed) and re-verified zero new residue; filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "a fresh run of tests/test_improve_loop.py grows queue/handoff/ by one cloud-*.json today and tests/test_chat_source_agent_workday.py leaves its residual file on bytes after the run." Both arms INVERTED: handoff count 183 before and after a fresh run; no residual file appears (residual dir pytest matches 0 post-run). Reproduction: run the two suites and recount (queue/handoff file count unchanged; `ls memory/biography/residual | grep -c pytest` = 0). A new pytest-source file or residual row after a test run inverts this receipt.

## Bibliography closed

- tests/test_improve_loop.py + tests/test_chat_source_agent_workday.py (both patched)
- mag/improve_loop.py (HANDOFF_DIR, TRAIL), mag/operator_inbox.py (EVENTS_PATH), mag/registry.py (RESIDUAL_DIR/REGISTRY/DERIVED_DIR/LATEST_SESSION), mag/biography.py (SUMMARIZED), mag/verkle_knot.py (append_verkle_knot stub target)
- queue/handoff/ + memory/biography/residual/ (51 + 1 files removed), logs/behavioral_events.jsonl + memory/runs/improve_loop_trail.jsonl + memory/biography/registry.jsonl (150 rows registered)
- watch/inbox/burn_wave_20260926/B2_359_writer_census_20260926.md (the census that framed the brief)
- Owed: a dated compaction policy for the 150 registered pytest-source rows (operator decision: reclaim vs permanent residue).
