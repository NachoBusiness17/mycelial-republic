# BURN build-fold-verify 20260926 c (the window's new builds: probe20 stamp/run, mseat grader, bib launder, hermes dual)

## Verdict
steal

## Evidence
1. (a) `.venv/Scripts/python.exe tools/probe20_stamp.py --dry`, exit 0: "SKIP P20A: no series on disk (nothing to bridge; refusing to synthesize)" / "SKIP P20B: no series on disk (nothing to bridge; refusing to synthesize)" / "dry: 0 stamp(s) + 0 referents row(s) printed, nothing written (--apply is the operator-gated append; 2 pair(s) missing series)".
2. (b) `tools/probe20_run.py --demo`, exit 0, "drift import from tools/drift.py: True". demo1-aligned: "verdict": "ALIGNED", corr 1.0. demo2-one-flip-escape: raw "INVERTED" (corr -0.5748) overridden to "INSUFFICIENT", "runner_override": "noise floor: net |delta referent| 0.050 < 0.10 across window; one-flip VACUOUS escape blocked (BURN _c)". demo3-true-vacuous: native "VACUOUS", note ends "[runner: flat referent, native kill stands]".
3. (c) `mseat_drift_grade.py watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json <extracted example-A-pass>`, exit 0: "accuracy: 19/20 = 0.95 (alive >= 0.85, flag < 0.70)" / "delta_raw: 0 (flag > 1)" / "narrated rate: narrated 0 vs authoritative 2 = 0.00x (limit 2x)" / "receipt-flag agreement: 20/20 claims; expectation grounding: all grounded" / "disposition: PASS" / "trail_event: PROBE_PASS".
4. (d) `bib_launder_check.py roblox/prompts/DETAIL.prompt.md roblox/prompts/DETAIL.prompt.md`, exit 0: "marker ## FACTS", seed and uplifted sha256 both "68d44c02c92ca2b0d9ebba804454f86795fa3e5edfb814e6959b69273e3e2d57", "MATCH", "VERDICT: MATCH (all invariant blocks byte-identical to seed)".

## Steal or Vacuous
- probe20_stamp.py --dry: VERIFIED. Exit 0, both pairs SKIP with 0 series, nothing written; matches the docstring law "DEFAULT IS DRY ... --apply refuses when a pair's series file is absent".
- probe20_run.py: VERIFIED on --demo (all three verdict paths fire as specced) and on the --live failure branch: "LIVE-UNREACHABLE: http://127.0.0.1:8080/completion ([WinError 10061] ...)", exit 3, and memory/runs/probe20 stayed empty (no series row written, the pre-registered "instrument-missing aborts, no fallback margin" behavior). --live success path NOT RUN: netstat shows nothing listening on 8080, so the llama-server happy path and the owed n_probs naming check are unproven against a real server.
- mseat_drift_grade.py: VERIFIED on fixture example A (exit 0 PASS, numbers byte-match the fixture's embedded grading block). Bonus actual: the arm0 lookup receipt grades "accuracy: 20/20 = 1.00 ... disposition: PASS", exit 0, which is the receipt's own pre-registered cheat expectation ("Arm 0 is expected to grade PASS ... The grader alone cannot detect lookup"); grounding_trace is spec-only, the grader does not enforce it.
- bib_launder_check.py: VERIFIED on the self-compare. The launder-detection path (exit 2 on an altered candidate) was not exercised this pass.
- hermes_dual_burn_20260926.py: NOT RUN (remote Hermes spend not in this pass's charge). Actual state: logs/hermes_dual_20260926/output.jsonl read 3 ok rows at first count and 4 ok ids seconds later (0 failed) against 150 brief jobs; the count grew between two reads, so a writer appears active elsewhere. Verify completion from that session, not this receipt.

## Falsifier
none proposed. Standing residuals unchanged: t74 live-DataStore check at playtest P3 (Sep-29); probe20 --live happy path and the bib_launder FAIL path remain unproven against real counterparts.

## Bibliography (closed)
watch/inbox/BURN_build-fold-verify_20260926.md · watch/inbox/BURN_build-fold-verify_20260926_b.md · tools/probe20_stamp.py · tools/probe20_run.py · watch/inbox/mseat_drift_grade.py · watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json · watch/inbox/MSEAT_ARM0_LOOKUP_RECEIPT.json · watch/inbox/bib_launder_check.py · roblox/prompts/DETAIL.prompt.md · watch/inbox/hermes_dual_burn_20260926.py · logs/hermes_dual_20260926/output.jsonl
