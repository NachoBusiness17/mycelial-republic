# B2-485 Verify the B2-164 scenario-suite-at-pre-push landing (2026-09-26)

## Verdict

LANDED (bytes-only verification): the B2-164 row STANDS. The pre-push hook carries the wired suite invocation (githooks/pre-push:280-306, "PUSH-GATE: workflow_gate_scenarios (conditional, enforcing)", trigger arms in the same --changed shape as the caption/refold blocks scoped to tools/workflow_gate.py changes, output arms ok/BLOCKS/skipped), the suite runs green in the hook's own invocation shape (`workflow_gate.py check --scenarios configs/workflow_gate_scenarios` => rc 0, "SCENARIOS: 7 cards validated read-only", all seven gates clean: G1-G5/G7 fail-expecting fixtures confirmed FAIL exit 2, G6 PASS exit 0), and a red card BLOCKS: with G6_receipts flipped to expect FAIL/exit 2 the same invocation exits 2 with "SCENARIOS: 1 of 7 cards red", which the hook maps to "PUSH-GATE: workflow_gate_scenarios BLOCKS the push" next to the violation ratchet. The card file was restored byte-faithful and the suite re-verified green (rc 0) after the flip experiment. No erratum needed; the B2-163-era suspicion (row checked, zero wiring) does not survive today's bytes.

## Evidence

- githooks/pre-push:280 `echo "PUSH-GATE: workflow_gate_scenarios (conditional, enforcing)"`; :296 `out=$(.venv/Scripts/python.exe "$WGATE" check --scenarios configs/workflow_gate_scenarios 2>&1) || true`; :299 ok arm; :301 "BLOCKS the push (gate changed but the card suite is red)"; :306 skip arm; trigger-arm comments at :240-257 (the card dir deliberately out of the trigger arms: untracked, so an arm would fire on every push)
- tools/workflow_gate.py:210 run_scenarios; :43 SCENARIO_DIR_DEFAULT configs/workflow_gate_scenarios
- Green run (this lane, hook shape): 7 "SCENARIOS ok" lines + "SCENARIOS: 7 cards validated read-only (no registry row written)", rc=0
- Red run (this lane): G6 expectations flipped -> "SCENARIOS ERROR ... expected_verdict.overall must be PASS or FAIL" on an invalid flip (fail-closed, rc 2), then the semantic flip -> rc=2, "SCENARIOS: 1 of 7 cards red (read-only run, no registry row)"; restored from byte copy, green rc=0
- configs/workflow_gate_scenarios/: 7 card JSONs + fixtures/ (G1_multiplicity ... G7_laws)
- watch/inbox/burn_wave_20260926/B2_163_law12_register_20260926.md (the indictment; superseded by today's bytes)

## Work done

Grep-verified the hook bytes for the wired invocation (the B2-163 finding of zero references no longer holds: the block sits at pre-push:240-306 with trigger arms, output parsing, and fail-closed red arm). Ran the suite once exactly as the hook invokes it. Proved the red-blocking contract twice: an invalid card mutation fails closed (rc 2 with the schema error), and a semantically valid red card exits rc 2 with "1 of 7 cards red". Restored the card from a byte copy and re-verified green. Receipt + LEDGER row filed; queue row note applied.

## Falsifier

The verification dies if: (1) the hook block is removed or rearmed (`grep -c "workflow_gate_scenarios" githooks/pre-push` drops, or the trigger arm changes shape without a receipt); (2) a red card stops blocking: flip any card's expectation and the invocation must exit 2; rc 0 on a red suite means the wiring is broken; (3) the suite silently passes on missing cards: delete a card file and the runner must count it (the "7 cards" language in run_scenarios output makes count drift visible). Conversely, if a card fixture's production behavior changes (a gate's real exit code shifts), the matching card goes red and BLOCKS pushes until the card is updated with its own receipt - that is the gate working.

## Bibliography closed

githooks/pre-push (read 235-310, unchanged); tools/workflow_gate.py (read 26-43, 210+ invocation surface, unchanged); configs/workflow_gate_scenarios/ (7 cards + fixtures; G6_receipts.card.json temporarily mutated for the red proof and restored byte-faithful); watch/inbox/burn_wave_20260926/B2_163_law12_register_20260926.md (read via brief pointer, unchanged); QUEUE.md (B2-164 row, claim lines, row note); memory/burns/LEDGER.jsonl (appended); watch/inbox/burn_wave_20260926/B2_485_scenarios_verify_20260926.md (this receipt).
