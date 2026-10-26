# B2-13 scenario cards (LAW-12 genesis clause) - 2026-09-26

## Verdict
landed: all seven genesis scenario cards minted from real registry FAIL rows, cited, and enforced by a read-only scenario mode inside the 14-day window.

## Evidence
- Clause, watch/inbox/BURN_rsi-harness_20260926.md:25: "one scenario card per G1-G7 is minted from real REGISTRY.jsonl FAIL rows and workflow_gate.py re-passes all seven on a sample gated script; the clause dies if cards cite no FAIL row or a soft-warn recurs on a hard check without a scenario record."
- Registry FAIL rows cited (memory/workflows/REGISTRY.jsonl): line 1 ts 2026-09-25T18:52:02Z tree-doctrine-dig digest 25dff0842218 G6 ok=false (hard, pre-t69); line 3 2026-09-25T20:45:15Z mickey17-v2.dwf.ts digest f190bf31e2ef G3/G4/G7 false; line 5 2026-09-26T02:32:14Z the-gala.dwf.ts digest 2a9ae3707582 G4 sole fault; line 12 2026-09-26T05:30:44Z the-50.dwf.ts digest 0937eff9fdda G2/G3/G4/G5/G7 false.
- G1 honesty: no G1 FAIL row existed (registry rows 1-17 all show G1 ok=true). Row 18 was minted by running the real gate on the G1 card's own fixture (exit 2, digest 4be79ce0f674, single fault G1) and the provenance is disclosed in the card's citation_provenance field. Nothing synthesized.
- Read-only proof: registry line count was 18 before and after check --scenarios (exit 0, seven cards plus pass_control green, "no registry row written").
- Re-pass proof: gate on .zcode/workflows/tree-doctrine-dig.dwf.ts printed "workflow_gate PASS digest=d2a6783b55be", byte-identical to registry row 13's digest; the run registered row 19 (2026-09-26T12:00:01Z) with all_ok=True and no soft rows.
- Negative proof: a mutated G2 card expecting PASS returned "SCENARIOS FAIL G2_passoff.card.json: verdict FAIL != expected PASS", exit 2.

## Work done
- configs/workflow_gate_scenarios/: seven cards (gate id, cited FAIL row, citation provenance, scenario input, expected verdict, regression criterion, rollback note) plus fixtures/ holding seven single-fault fixtures and pass_control.dwf.ts. Every fixture was verified single-fault against the real CHECKS functions before use.
- tools/workflow_gate.py: docstring spec extended first, then check --scenarios landed read-only. validate_card pins every citation to a registry row with verdict FAIL and the card's gate ok=false; run_checks/split_rows are shared with the script path so the G6 soft logic has one implementation. AGENTS.md:106 documents the mode.
- tests/test_workflow_gate.py: three new tests (suite green + read-only, expectation mismatch exit 2, citation to a missing row errors); file passes 7/7.
- Owed: LAW-12 itself is still unregistered in memory/law/registry.json (only LAW-1 through LAW-11 present); the clause lives in the receipt falsifier. Registration is a separate operator act, not faked here. Self-fed as B2-71.
- Ratchet: my changed files carry zero new debt and zero em-dashes; the one NEW hit (tools/drift_pairs_stamp.py:471 file-too-long) belongs to another lane's working tree and is not accepted here.

## Falsifier
Run: .venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios
Clause execution is falsified if this exits non-zero on an unmodified tree, if any cited FAIL row is erased from REGISTRY.jsonl, if a gate change silences a fixture while the suite stays green (validator regression), or if soft-warn semantics spread beyond G6 without a new dated card.

## Bibliography (closed)
1. watch/inbox/BURN_rsi-harness_20260926.md, read 2026-09-26
2. tools/workflow_gate.py, read and edited 2026-09-26
3. memory/workflows/REGISTRY.jsonl, read 2026-09-26 (17 rows); rows 18 and 19 appended by this lane's real gate runs
4. memory/law/registry.json, read 2026-09-26 (LAW-12 absent)
5. tests/test_workflow_gate.py, read and extended 2026-09-26
6. AGENTS.md line 106, read and updated 2026-09-26
