# BURN rsi-harness _b - 2026-09-26

## Verdict
steal

## Evidence
- configs/workflow_gate_scenarios/ holds exactly 7 cards, G1_multiplicity through G7_laws, one per gate, each with scenario_description, expected_verdict, cited_fail_row, regression_criterion, rollback_note.
- Cross-check vs memory/workflows/REGISTRY.jsonl: G6 cites line 1 (tree-doctrine-dig, 18:52:02Z, G6 ok=false): exact match. G3 and G7 cite line 3 (mickey17-v2): exact match. G4 cites line 5 (the-gala), G2 and G5 cite line 12 (the-50): match. Six of seven cite genuine fleet FAIL rows.
- G1 card, citation_provenance: "No G1 FAIL row existed in REGISTRY.jsonl when the clause was filed 2026-09-26: rows 1 through 17 all show G1 ok=true... the row is real gate output, disclosed here rather than synthesized." Verified: row 18 is scenario-g1-fixture, FAIL; rows 1-17 all show G1 ok=true.
- Suite run this pass: tools/workflow_gate.py check --scenarios printed "SCENARIOS: 7 cards validated read-only (no registry row written)", exit 0, pass_control all seven clean.
- REGISTRY.jsonl line 19: "law12-genesis-repass", 2026-09-26T12:00:01Z, tree-doctrine-dig, PASS, all seven checks ok.
- memory/law/registry.json read this pass: LAW-13 present, no LAW-12 row.
- Web search 2026-09-26, snippet level, no fetchable URLs: "Agent Harness Engineering" (github.com, Aug 2026): "the useful unit of evaluation is the model-harness pair rather than a raw LLM"; Cekura (Sep 4 2026) lists "Scenario", simulated conversations scored by LLM judges; devopsschool.com ARE blueprint: "regression tests derived from production failures". Fetches owed.

## Steal or Vacuous
Steal: genesis state plus amended drill score.
Genesis: DISCHARGES on its own terms. Deadline met (cards landed day 0, the date the clause was filed; mtimes 07:58 local, fixture row 11:57:07Z, repass row 12:00:01Z). Cards real: six of seven citations byte-verified against genuine FAIL rows. Repass recorded (line 19). Suite green by direct run. Neither death condition fired: cards cite rows, and the one soft-warn (G6) now carries its required scenario record with no new unrecorded warn.
Amended LAW-12 drill (was 3 of 5 failed):
1. Scenario cards: HOLDS. 7 cards, trace pointers, fixtures. Caveat: G1's trace is self-minted, fixture-first, disclosed.
2. Non-compensatory admission: HOLDS, unchanged; G6 soft branch pinned by a card that goes red on spread.
3. Runtime: HOLDS via the _c checklist's explicit single-runtime branch: every card carries rollback_note naming trigger and restore path. Dual-runtime stays unexercised; the gate is a static checker.
4. Incumbent default: HOLDS, unchanged.
5. Regression criterion: EXISTS now. Per-card regression_criterion plus read-only scenario mode, run after any gate change, suite must stay green.
Score: 5 of 5 hold, up from 2 of 5, with two named caveats: the G1 self-mint and the unexercised runtime pair.
Residue: the discharged clause covered a law never registered. Filing LAW-12 with the card suite as its regression set is the open half.

## Falsifier
none proposed

## Bibliography
1. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md s4, read 2026-09-26
2. memory/law/registry.json, read 2026-09-26
3. watch/inbox/BURN_rsi-harness_20260925.md, _b.md, _c.md, 20260926.md, read 2026-09-26
4. configs/workflow_gate_scenarios/ (7 cards), read 2026-09-26
5. memory/workflows/REGISTRY.jsonl, read 2026-09-26
6. tools/workflow_gate.py check --scenarios, run 2026-09-26, exit 0
7. Web search 2026-09-26 (snippet level: github.com Agent Harness Engineering, Cekura Scenario, devopsschool.com ARE blueprint; URLs not surfaced, fetches owed)
