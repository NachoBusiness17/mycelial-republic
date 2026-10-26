# B2-361 FKB index drift tripwire, 2026-09-26

## Verdict

LANDED. `python -m mag.failure_kb verify` now recounts the log by sig (the rebuild_index oracle, read-only, no write) and names every violation of the two owned classes: index-above-log (index count exceeds log count, including index sigs with zero log rows) and first_seen mismatch (index first_seen differs from log-derived first_seen for a sig in both). Log sigs absent from the index are expected drift per the rebuild policy (count-1 sigs log-only by design) and are never violations, exactly the brief's carve-out. Wired into a recurring surface: every `improve --status` read (mag/improve.py status_summary) now carries a failure_kb {ok, violations} block, so a mutated or clobbered signatures.json is named at every status read, not only at the next gate edit. Live run on production bytes: ok true, 0 violations, 1,435 index sigs, 7,316 log sigs, 109,759 log rows parsed, exit 0. Falsifier arms proven on sandboxed copies of the real log: count+1 mutation -> ok false, violations 1, named "autorun_detached.log:18dfe1cd03bf" index_count 2 log_count 1; backdated first_seen -> named with both timestamps. Exit contract: 0 clean / 2 violations (house convention). The next rebuild heals every named violation by design (log bytes win); verify names, never mutates.

## Evidence file:line quotes

- mag/failure_kb.py verify() docstring (post-edit): "B2-361 (2026-09-26): index-vs-log drift tripwire, READ-ONLY. ... index-above-log ... first_seen mismatch ... Log sigs missing from the index are EXPECTED drift ... never violations. The next rebuild heals every listed violation by design (log bytes win), so this command names, it never mutates."
- _cli wiring: `if argv[0] == "verify": ... return 0 if r["ok"] else 2` with the comment "B2-361: index-vs-log recount; exit 0 clean, 2 violations (house fresh/exit-2 convention). Read-only, never mutates."; usage string updated to include verify.
- Live production run (2026-09-26 21:1xZ): {"ok": true, "violations": 0, "index_sigs": 1435, "log_sigs": 7316, "log_rows_parsed": 109759}, exit 0.
- Sandbox falsifier arms (real log sliced to 5,000 rows, tmp index): count+1 -> {"ok": false, "violations": 1, "index_above_log": [{"sig": "autorun_detached.log:18dfe1cd03bf", "index_count": 2, "log_count": 1}]}; first_seen backdated to 2000-01-01 -> {"first_seen_mismatch": [{"sig": "autorun_detached.log:18dfe1cd03bf", "index_first_seen": "2000-01-01T00:00:00Z", "log_first_seen": "2026-08-08T18:08:26.107568+00:00"}]}. Production signatures.json never mutated.
- Recurring surface (mag/improve.py status_summary, post-edit): "failure_kb": (lambda v: {"ok": v.get("ok"), "violations": v.get("violations")})(fkb_verify()) with the B2-361 comment "so a mutated/clobbered signatures.json is named here, not only at the next gate edit"; live: "failure_kb: {'ok': True, 'violations': 0}".
- Continuity basis: index rebuild_receipt {"ts": "2026-09-26T17:11:32...", "reason": "B2-87 continuity repair: reconcile index counts reset 2026-09-22T14:54Z against append-only log history"} — the reset this tripwire watches for.
- Pointer receipt: watch/inbox/burn_wave_20260926/B2_87_fkb_continuity_20260926.md (the 2026-09-22T14:54Z reset that hid 4 days).

## Work done

- Claim law: CLAIM SW-00 for mag/failure_kb.py (working-tree-modified) before editing; retired at landing.
- Read rebuild_index's aggregation (the oracle), stats(), _cli, and the index field names (count/first_seen from the B2-87 receipt block); implemented verify() reusing the same parse loop read-only, plus the CLI arm and usage update.
- Wired the summary block into status_summary under the same lane (one claim line covers both files; the mag/improve.py claim covers this edit and the B2-493 block filed separately).
- Live production verify (clean) + sandbox proof of both violation arms; tests touching the surfaces stay green (tests/test_improve_provider_probe.py 14 passed, tests/test_improve_status_scheduled_task.py 4 passed); py_compile clean; added lines em-dash 0.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Mutate one count in signatures.json (the brief's falsifier): `python -m mag.failure_kb verify` must exit 2 naming that sig with index_count above log_count; the sandbox arm proves the shape, the production file stays untouched.
- A first_seen edit on any sig present in both index and log must name the divergence; proven above.
- A clobbered log (file truncated below index counts) must light index-above-log across the affected sigs at the next verify or improve --status.
- Log rotation, if ever introduced, would make index-above-log fire for rotated-away rows: that residual is named here, not handled (rotation does not exist in the module today).
- If status_summary is ever called with failure_kb import broken, the block reads {ok: null, violations: null} — a null is a visible absence, never a fake clean.

## Bibliography closed

mag/failure_kb.py (rebuild_index oracle, stats, _cli, new verify; post-edit); mag/improve.py (status_summary pre/post-edit); memory/failure_kb/signatures.json (rebuild_receipt, 1,435 sigs, untouched); logs/failure_kb.jsonl (109,759 rows parsed read-only); watch/inbox/burn_wave_20260926/B2_87_fkb_continuity_20260926.md; sandbox probe transcripts quoted above. No web sources. Em-dash count 0.
