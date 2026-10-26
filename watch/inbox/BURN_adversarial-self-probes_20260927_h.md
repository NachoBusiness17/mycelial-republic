# BURN adversarial-self-probes pass h — 2026-09-27

## Verdict

green

## Evidence

Patrol run at `--rows 40` (largest sane draw), stdout: "PATROL: 40 rows, 20 mechanical checks, 0 warns (WARN-ONLY; log SPOT_PATROL.jsonl)". Zero warns fired, so the true mismatch vs extraction noise split is 0/0; there was no warn to grade.

Adversarial false-success check on the patrol itself: I re-verified all 20 "ok" findings independently. All 20 named paths stat EXISTS on disk (tools/prepush_paths_changed.py, githooks/pre-push, tests/test_icon_drop_fold.py, tools/provider_error_tally.py, scripts/path_pin.py, tests/test_spore_seed.py, memory/spore_seeds/testseat.jsonl, tests/test_icon_drop_escape.py, mag/win_powershell.py, memory/attention.md, scripts/union_fullsend_day.py, tests/test_union_driver_v2.py, mag/improve.py, tests/test_hunger_ledger_parity.py, configs/providers.yaml, tools/queue_row_census.py, tests/test_index_fold_host.py, configs/events_key_schema.json, configs/workflow_registry_baseline.json, tests/test_workflow_registry_append_only.py). The patrol emitted no false success of its own.

Two deeper hand grades beyond existence:
- B2-303 (memory/burns/LEDGER.jsonl): "12 pollution rows on file, growth now zero via monkeypatched SPORE_SEED_FILE". Disk truth: memory/spore_seeds/testseat.jsonl is exactly 12 lines. Claim holds byte-level days after landing.
- B2-427 (memory/burns/LEDGER.jsonl): "pins per-line sha256 of all 25 REGISTRY.jsonl rows". Disk truth: memory/workflows/REGISTRY.jsonl now 30 lines. Ruled consistent, not a true mismatch: claim polarity is a landing-time snapshot and B2-427's own test allows pure appends; 30 > 25 is the designed growth mode.

Coverage honesty: 25 of 40 drawn rows bound zero claims, the docstring's named blind class ("counts, row ids, prose ... reported as unchecked, never guessed"). This draw's one_lines are count-heavy (B2-488 "strict 466 / tolerant 466", B2-303 "39F/2164P/9S/1E on file"), structurally outside PATH_RE / BARE_PATH_RE / SHA_RE / BYTES_RE reach.

## Steal or Vacuous

The hunt drew clean: 0 true mismatches, 0 extraction noise warns across 40 LANDED ledger rows. In PROWL fold 3 terms the probe stayed near-distribution (real landed rows, no synthetic strawmen), the spot patrol mechanically verified 20 claims with every grade byte-true under independent re-check, and no false success surfaced to exploit. One clean draw cannot clear pass c's pre-registered vacuousness clock (two consecutive weeks of zero mismatches AND no lane acting on a warning); the clock keeps running, currently green.

## Falsifier

Pre-registered build proposal (pass i candidate): bind count claims ("N pins/tests/rows", "strict X / tolerant Y") against wc -l / grep -c on the single path named in the same one_line, reusing the bytes heuristic's arity guard. Acceptance thresholds inherited from pass g: additive-only, zero existing warns silenced, and the extension must move at least 10 of the current 25 zero-bound rows into checked territory or it is reverted. If count-binding also fails to raise warn yield over two weeks, the ledger's claim mass is prose-dominant and the patrol's honest ceiling is existence + sha256 + bytes.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md (read)
- tools/ledger_spot_patrol.py (read)
- memory/burns/LEDGER.jsonl, 15 one_lines read: B2-272, B2-412, B2-441, B2-438, B2-303, B2-413, b2-375, B2-494, B2-320, b2-418, B2-440, b2-445, B2-488, B2-380, B2-427
- memory/burns/SPOT_PATROL.jsonl, this run's 40-row tail (read)
- Disk stats: the 20 named paths, memory/spore_seeds/testseat.jsonl (12 lines), memory/workflows/REGISTRY.jsonl (30 lines)
- Web search "false positive triage audit tooling 2026": thin, no relevant 2026 sources (loose hits only: glama.ai MCP email batching, ResearchGate 2021 COVID imaging, dementia fall detectors)
