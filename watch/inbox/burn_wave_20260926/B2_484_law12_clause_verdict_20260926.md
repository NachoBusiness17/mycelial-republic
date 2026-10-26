# B2-484 File the LAW-12 clause verdict

## Verdict

LANDED (filed 2026-09-26, 14 days ahead of the 2026-10-10 deadline). The LAW-12 clause verdict is PASS: (1) the scenario suite re-ran exit 0 (7 cards G1-G7 validated read-only, no registry row written); (2) a sample gated script re-passed the gate (tools/workflow_gate.py check --script .zcode/workflows/tree-doctrine-dig.dwf.ts, exit 0) with its file digest d2a6783b55be3f9b matching its memory/workflows/REGISTRY.jsonl row exactly; (3) all 8 cited FAIL rows still stand in the registry; (4) the one soft-warn observed (G3-steering judge-model-undeclared, the B2-60 D2 soft-warn class) does NOT fire the die-condition because a scenario record covers the axis (the G3 card exists in the validated suite) - disclosed, not papered. memory/law/registry.json LAW-12 entry amended with a clause_verdict field (amend-not-rewrite: the field was added, no existing field changed, 11 other law entries intact).

## Evidence file:line quotes

- memory/law/registry.json LAW-12.falsifier (pre-amendment): "LAW-12 passes only if, within 14 days of registration, one scenario card per G1-G7 is minted from real REGISTRY.jsonl FAIL rows and workflow_gate.py re-passes all seven on a sample gated script; the clause dies if cards cite no FAIL row or a soft-warn recurs on a hard check without a scenario record".
- Scenario suite run: "SCENARIOS ok   pass_control: all seven gates clean / SCENARIOS: 7 cards validated read-only (no registry row written)", exit 0.
- Sample script run: "ok G5-deliverable ... / ok G6-receipts ... / ok G7-laws: no-fabrication and em-dash law carried inside the asks", exit 0; the single WARN: "G3-steering: ... [judge independence undeclared ...; soft-warn, not a hard block]".
- Digest match: REGISTRY row "tree-doctrine-dig.dwf.ts" digest d2a6783b55be == sha256 of the file on disk (d2a6783b55be3f9b...).
- Post-amendment: LAW-12.clause_verdict = {verdict: pass, date: 2026-09-26, evidence{scenario_suite, sample_script, fail_rows_standing: 8, soft_warn_disclosed}, receipt pointer}; registry loads clean with 12 law entries.

## Work done

1. Re-ran the scenario suite (exit 0, read-only, 7 cards).
2. Selected the newest REGISTRY row carrying a script digest, verified the digest matches the file's current sha256, re-passed check --script on it (exit 0).
3. Counted the standing FAIL rows (8) and inspected the run's warnings: exactly one G3 soft-warn, covered by the G3 scenario card, so the die-condition ("a soft-warn recurs on a hard check without a scenario record") does not fire.
4. Amended the LAW-12 registry entry with the clause_verdict field (add-only; the falsifier field, axes, and all other entries untouched); registry re-parsed clean.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

The owning falsifier (BURN_rsi-harness_20260926.md / registry LAW-12): "2026-10-10 lapses with no clause_verdict on the registered LAW-12 entry" - INVERTED: the clause_verdict field exists with verdict pass, dated 2026-09-26, 14 days before the deadline. The die-branch ("cards cite no FAIL row or a soft-warn recurs on a hard check without a scenario record") was checked and does not fire: the 8 FAIL rows stand, the lone soft-warn has a scenario record. Reproduction: the three commands above; any future rerun of the suite that goes nonzero, a cited FAIL row disappearing, or a hard-check soft-warn with no covering card reopens the clause and inverts this verdict.

## Bibliography closed

- memory/law/registry.json (LAW-12 entry, amended add-only)
- tools/workflow_gate.py (check --scenarios, check --script)
- configs/workflow_gate_scenarios/ (7 cards; the G3 card covering the observed soft-warn)
- memory/workflows/REGISTRY.jsonl (digest-matched sample row; 8 standing FAIL rows)
- watch/inbox/BURN_rsi-harness_20260926.md (the falsifier's pre-registration, named by the brief)
- watch/inbox/burn_wave_20260926/B2_13_scenario_cards_20260926.md (the cards' landing receipt)
- Nothing owed.
