# B2-335 receipt (2026-09-26)

## Verdict

LANDED (flip arm). The test-born candidate gap-c4f076b1e0205c27 (memory/improve/candidates.jsonl line 95) no longer reads status "new": it is flipped to "rejected" through the repo's own update_candidate_status path with the B2-79 receipt named as evidence, on top of the B2-86 pollution annotation that was already on the row. The sweep for other test-born candidates is clean: the only other near-match (c-95d3b1cbb639, line 150) is a real crash-census candidate, not test-born. The brief's falsifier ("still reads status new and is promotable today") no longer holds.

## Evidence file:line quotes

- memory/improve/candidates.jsonl:95 BEFORE this lane (found already annotated, not erased): `"id": "gap-c4f076b1e0205c27", ..., "claim": "[loop gap] test_gap_unique_xyz: unit", "url": "tests", "source": "mag_temperature_gap", "status": "new", ..., "pollution": "annotated 2026-09-26 B2-86: test-injected row (tests/test_temperature_stack.py track_loop_gap force=True improve-candidate side sink, pre-isolation); writer isolated, receipt watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md"`.
- The promotable gap this brief named: mag/improve.py update_candidate_status (line 159-179) rewrites status with no pollution filter, and promote_apply (line 2546+) has no pollution check, so the B2-86 annotate-only arm left the row operator-promotable; status still read "new" at this lane's start, exactly the falsifier shape.
- memory/improve/candidates.jsonl:95 AFTER this lane: `"status": "rejected", ..., "note": "test-born candidate: never promote (B2-335 flip arm). Evidence: B2-86 pollution annotation on this row + watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md (force=True pre-fix test rows; writer isolated)."`, the B2-86 pollution field preserved byte-for-byte (no-erase honored; the flip is the codified in-place status path the promoter itself uses).
- Sweep: memory/improve/candidates.jsonl 155 rows; test-born pattern (claim contains test_gap, or url == "tests", or pollution field present) matches exactly 2 rows: line 95 (the flipped one) and line 150 c-95d3b1cbb639 "Seat crash log: real=52 ... test=372 ..." which is a REAL census candidate describing test-vs-real crash classification, not a test-injected row; left untouched. The loop_gaps join the brief asked for: memory/training/loop_gaps.jsonl holds ZERO rows naming test_gap today (the B2-79 pollution fix plus its B2-79 close-pass erratum, LEDGER row 176, cleaned the 17+1 rows); join against candidates yields no further test-born rows.

## Work done

1. Verified the row bytes and found B2-86's annotation arm already landed; checked whether annotation blocks promotion (it does not: no pollution read anywhere in the promote path), so the brief's falsifier still held through the annotate arm.
2. Took the brief's flip arm: status new -> rejected via mag.improve.update_candidate_status with the B2-79 evidence note; pollution annotation preserved.
3. Ran the sweep both ways the brief named (direct candidate pattern + loop_gaps join): no other test-born candidates exist; the one near-match is real work and stays.
4. Post-flip check: zero rows read status "new" while carrying a pollution field.

## Falsifier

The brief's falsifier ("the candidate still reads status new and is promotable today") is dead: the row reads rejected, and even a forced status reset would collide with the preserved pollution field plus the note naming the evidence. Re-arm conditions: a new test-injected candidate row (the writer isolation is supposed to prevent this; if a future row with url "tests" and a test_gap claim appears, this sweep reruns as-is and must find it). The flip itself falsifies if the B2-79 evidence is later overturned (the receipt proving the row was test-injected); overturning that would require showing test_gap_unique_xyz is a real estate claim, which the tests/test_temperature_stack.py provenance contradicts.

## Bibliography closed

- memory/improve/candidates.jsonl (155 rows; line 95 flipped, line 150 inspected and left)
- mag/improve.py update_candidate_status (159-179) and promote_apply (2546+) read; no pollution filter exists there, which is why the flip arm was taken
- watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md; watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md
- memory/training/loop_gaps.jsonl (zero test_gap rows at sweep; the fix already landed there)
