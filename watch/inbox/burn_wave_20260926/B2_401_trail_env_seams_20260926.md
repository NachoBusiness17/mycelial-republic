# B2-401 Seat-registry and orchestrator test-to-production trail pollution, 2026-09-26

## Verdict

LANDED. Both writers gained env seams in the MAG_SEAT_CRASH_LOG shape (B2-86 pattern): mag/seat_registry.py _trail_path() honors MAG_SEAT_REGISTRY_TRAIL, mag/orchestrator.py _trail_path() honors MAG_ORCHESTRATOR_TRAIL; no env set = the production path, byte-identical behavior. Both test files point the writers at tmp via autouse fixtures, and the proof is byte-level: a full run of tests/test_seat_registry.py + tests/test_orchestrator_queue.py leaves BOTH production trails byte-still (cmp equal across the run). The historical pollution is annotated in place per the B2-79 no-erase pattern: 114 seat-trail rows (parent=pytest) and 623 orchestrator-trail rows (tag q-test or _pytest-bearing, deduped union) each gained a dated pollution field naming the cause; 0 annotated rows fail to parse; all other rows byte-identical. Counts vs the brief's census: brief said 111 pytest-parent seat rows and 565 q-test rows; at annotation time the live files held 114 and 623 matches (the files kept growing from a still-active writer class; my own first pre-fixture test run added some, all caught by the annotation pass). Disclosed honestly: (1) the seat-test fixture needed BOTH seams because mesh_peers exercises orchestrator touch_external — the first byte-still attempt failed until the second env was added; (2) 13 pre-existing unparseable fragment rows exist in orchestrator_trail.jsonl (null-padded/truncated lines, not this lane's bytes, left untouched and excluded from annotation); (3) one stale pre-existing assertion in tests/test_seat_registry.py (timeout_for_goal "api" expecting the bare 900 constant) was rebased to the landed temperature-stack value 600 with a dated comment, unrelated to the seam.

## Evidence file:line quotes

- mag/seat_registry.py (post-edit): _trail_path() "B2-401 (2026-09-26): MAG_SEAT_REGISTRY_TRAIL overrides the sink ... (111 pytest-parent rows were on disk at fix time). No env set = same path."; _trail uses `path = _trail_path()` for mkdir + append.
- mag/orchestrator.py (post-edit): _trail_path() "B2-401 (2026-09-26): MAG_ORCHESTRATOR_TRAIL overrides the sink ... (571 q-test rows were on disk at fix time)."; _trail appends through `path = _trail_path()` with mkdir.
- tests/test_seat_registry.py: autouse fixture _isolate_seat_trail setting MAG_SEAT_REGISTRY_TRAIL and MAG_ORCHESTRATOR_TRAIL to tmp_path files, with the comment "mesh_peers exercises orchestrator touch_external, which writes the orchestrator trail; isolate both seams in one fixture."
- tests/test_orchestrator_queue.py: autouse fixture _isolate_orchestrator_trail setting MAG_ORCHESTRATOR_TRAIL ("571 q-test rows were on disk at fix time").
- Byte-still proof (this lane, after fixtures): pytest 9 passed; `cmp /tmp/sr2 memory/runs/seat_registry_trail.jsonl` and `cmp /tmp/ot2 memory/runs/orchestrator_trail.jsonl` both silent-equal -> "BOTH-TRAILS-BYTE-STILL". (The first attempt failed cmp on the orchestrator trail with 6 new register_external/done rows at 21:18:29-34Z from the seat tests' mesh_peers calls — the evidence that motivated the both-seam fixture.)
- Annotation (in-place, B2-79 pattern): seat trail 114 rows gained "pollution": "2026-09-26 (B2-401 test pollution: written by tests/test_seat_registry.py register/unregister with parent=pytest before the MAG_SEAT_REGISTRY_TRAIL env seam landed; no-erase law, row content otherwise unchanged)"; orchestrator trail 623 rows gained the same-shaped field naming test_orchestrator_queue.py real enqueues; parse check "orchestrator pollution rows 623 unparseable among them 0" and seat file "rows 234 unparseable 0"; the 13 pre-existing unparseable orchestrator fragments left as-is.
- Stale-assertion rebase (tests/test_seat_registry.py): "rebased 2026-09-26 (B2-401, claim-law rebase on already-landed bytes): timeout_for_goal defers to the temperature-stack YAML heat band before the DEFAULT_TIMEOUT fallback, so tag api resolves to the stack value (600)"; assertion now == 600; failure reproduced before the rebase ("assert 600 == 900").

## Work done

- Verified all four files committed-clean (no claim line required for them; the QUEUE flips are this lane's own).
- Implemented both _trail_path() seams with dated law comments; converted the append sites; callers untouched.
- Added autouse isolation fixtures to both test files; discovered via the byte-still falsifier that the seat tests also write the orchestrator trail (mesh_peers -> touch_external) and extended the fixture; second run proves both trails byte-still.
- Rebased one pre-existing stale timeout assertion with a dated cause comment (9/9 pass).
- Annotated the historical pollution in place with a .venv python script: deterministic signatures only (parent=pytest; tag q-test or _pytest-bearing), dated cause field, every rewritten line still parses, unmatched lines byte-identical, including rows my own first pre-fixture run added (self-caught).
- py_compile clean; em-dash 0 in added lines. Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- A fresh run of tests/test_seat_registry.py or tests/test_orchestrator_queue.py that appends any row to either production trail kills the landing (the cmp proof above reruns in seconds).
- An annotation that erased or re-ordered any pre-existing row kills the no-erase claim; the 13 pre-existing unparseable fragments are the control — they are byte-unchanged.
- If a third writer appends to these trails from another module holding the TRAIL constant directly (importers of the constant bypass the seam), those appends still land in production: the seam covers the module's own _trail writers, and a constant-importing writer would be a follow-up finding.
- Deleting the env in a shell and running the tests (fixture removed) would reproduce the pollution: the fixture, not the seam alone, is what the tests rely on.

## Bibliography closed

mag/seat_registry.py (_trail pre/post-edit); mag/orchestrator.py (_trail pre/post-edit; timeout_for_goal read for the rebase); tests/test_seat_registry.py, tests/test_orchestrator_queue.py (fixtures + rebase); memory/runs/seat_registry_trail.jsonl (234 rows, 114 annotated, parse-clean); memory/runs/orchestrator_trail.jsonl (31,400 rows incl. 13 pre-existing fragments, 623 annotated, parse-clean); mag/agent_cli.py:2500-2525 (B2-86 seam shape); watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md (in-place annotation pattern); watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md. No web sources. Em-dash count 0.
