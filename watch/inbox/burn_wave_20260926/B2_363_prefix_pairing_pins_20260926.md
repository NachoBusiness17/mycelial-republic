# B2-363 receipt: pin the remaining pre-push prefix pairings (2026-09-26, lane SW-03)

## Verdict

DONE. The sh-replay pairing pattern (B2-338, census only) is factored into one shared helper (tests/hook_pairing.py) and extended to EVERY pre-push ok case-arm: FRESHNESS-GATE: ok (live green+stale subprocess band), CENSUS-PATROL: ok (enumerated here; live band remains B2-338's), REFOLD-GATE: ok, RESULT: PASS, SCENARIOS ok (each pinned static-source-plus-replay with a case-mutated sample that must fall to WARN_ARM). The brief's falsifier is now answered in tests: a mutated emitter ok token case goes red (live band for freshness, source-literal assert for refold/caption/scenarios, and the mutated-case replay proves the arm is case-sensitive in both directions). 7/7 new tests pass; census (72) + freshness-gate test files still 77 passed.

## Evidence file:line quotes

- githooks/pre-push:51: `"FRESHNESS-GATE: ok"*) : ;;` (the freshness block case-matches START, WARN-only otherwise)
- githooks/pre-push:82: `"CENSUS-PATROL: ok"*) : ;;` (the only pairing previously pinned, B2-338)
- githooks/pre-push:201: `"REFOLD-GATE: ok"*)`; :133: `*"RESULT: PASS"*`; :272: `"SCENARIOS ok"*)` (the three unpinned consumers this brief named or the every-consumer law sweeps in)
- tools/freshness_gate.py:298-299: `label = "ok" if result["ok"] else "FAIL"; print(f"FRESHNESS-GATE: {label} {args.receipt} ({result['reason']})")` (the emitter side of arm 51)
- tools/refold_gate.py:133: `f"REFOLD-GATE: ok ({PINS.as_posix()} ran against {HOST.as_posix()}: "` ; scripts/the50_t21_q_caption_ledger_verify.py:480: `print(f"RESULT: {'PASS' if ok else 'FAIL'} - {len(rows)} rows, "` ; tools/workflow_gate.py:239: `print("SCENARIOS ok   pass_control: all seven gates clean")` (emitter sides)
- tests/test_census_drift_patrol.py:500-535 (the B2-338 pattern being factored): "the ok-arm PATTERN is read from the real githooks/pre-push bytes at test time and evaluated by real sh against the tool's captured output (2>&1, exactly what the hook does)"

## Work done

- tests/hook_pairing.py (new, not pytest-collected): hook_arm_pattern() reads the arm pattern from real pre-push bytes and asserts exactly-one arm per literal; sh_arm_decision() replays a captured line through real sh case matching (the hook's own routing); source_ok_literal() pins the emitter's source bytes for emitters whose green run is expensive; CONSUMERS maps all five arms to their emitter files.
- tests/test_hook_prefix_pairing.py (new, 7 tests): registry completeness (any new ok arm in the hook without a pin fails collection of the enumeration test), freshness LIVE green -> OK_ARM and stale -> WARN_ARM through real subprocess + real sh, freshness case-mutation (FRESHNESS-GATE: OK) -> WARN_ARM, and the refold/caption/scenarios pairings each with an OK_ARM sample and a case-mutated WARN_ARM sample.
- Census live band left untouched in tests/test_census_drift_patrol.py (B2-338 owns it); the shared helper lists the census consumer so the enumeration stays complete.
- No hook or emitter bytes changed: the pairing is pinned, not reformed (the arms were all correct today; the disease was the absence of tests).

## Falsifier

The brief's falsifier, restated executable: mutate an emitter's ok token case and no gate test goes red. Now: (a) freshness emitter case drift -> test_freshness_green_run_takes_ok_arm_live red (startswith assert on live output); (b) refold/caption/scenarios emitter drift -> source_ok_literal red; (c) hook arm case drift -> the exactly-once pattern extraction red and the live/replayed OK_ARM samples falling to WARN_ARM red; (d) a new ok arm added to the hook without a pin -> test_every_pre_push_ok_consumer_is_enumerated red. Remaining honest gap: refold/caption/scenarios green outputs are replayed from literals, not live tool runs (their green runs are expensive or conditional); the census band keeps the live-run standard and B2-338 demonstrates it.

## Bibliography closed

- githooks/pre-push (freshness block lines 41-56, census block 58-86, caption block 110-140, refold block 142-210, scenarios block 265-281)
- tools/freshness_gate.py (main/label print, self-test cases)
- tools/refold_gate.py (docstring lines 32/49-50, ok print 133)
- scripts/the50_t21_q_caption_ledger_verify.py (RESULT print 480)
- tools/workflow_gate.py (SCENARIOS ok prints 227/239)
- tests/test_census_drift_patrol.py (B2-338 sh replay band, pattern source)
- tools/census_drift_patrol.py (ok print 312, census emitter)
