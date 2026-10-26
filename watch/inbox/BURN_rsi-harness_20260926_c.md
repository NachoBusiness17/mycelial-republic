# BURN rsi-harness _c - 2026-09-26

## Verdict
steal

## Evidence
- memory/law/registry.json read this pass: LAW-12 present. "registered_ts": "2026-09-26T18:26:53.896974+00:00", "name": "amendment_gate", "tier": "T0", "registered_by": "B2-163 flash-lane burn wave 2026-09-26". The _b residue ("LAW-12 itself UNREGISTERED") is discharged.
- Verbatim check: the registry falsifier field equals the BURN_rsi-harness_20260926.md line 25 clause minus its "Pre-registered genesis clause:" lead-in, byte for byte; "window": "registered 2026-09-26; 14-day clause window closes 2026-10-10".
- Registration receipt watch/inbox/burn_wave_20260926/B2_163_law12_register_20260926.md: "Inserted the LAW-12 entry by anchored edit between LAW-11 and LAW-13"; LEDGER.jsonl carries the matching row. B2_255_double_spend_20260926.md table: "B2-163 | LAW-12 registration | Estate MCP on docker", collision resolved in the registration's favor, the other claimant moved to B2-291.
- Advancement since _b: githooks/pre-push lines 210 to 280 now wire the suite (B2-164): "PUSH-GATE: workflow_gate_scenarios (conditional, enforcing)", payload "workflow_gate.py check --scenarios configs/workflow_gate_scenarios", read-only, blocks the push when the gate changes and the suite is red. B2-163's named gap (enforcement CLI-only) is closed.
- SIX_DROPS s4 (muratcan): "Accept only if every scenario passes in both runtimes", the survivors rule the registered dual_runtime_regression axis encodes.
- Drift found: the registered axes carry no "pre-existing" requirement. trace_provenance reads "scenario cards exist and each cites a real failing trace by pointer (receipt path or ledger row id); no trace, no card". The self-mint patch this pass prescribes (traces must pre-date the proposal) entered neither the _c checklist, the draft row, nor the registered row; the falsifier still reads "minted from real REGISTRY.jsonl FAIL rows", satisfiable fixture-first. The _b caveat rode into the law unpatched.
- Condition drift, disclosed: registered condition "all_five_gate_axes_nonzero_and_scenario_suite_green" alters the _c draft "all_five_gate_axes_nonzero_and_dual_runtime_pass_recorded"; dual-runtime survives as an axis with the rollback-note branch.
- Web search 2026-09-26: no relevant results; nothing fetched.

## Steal or Vacuous
Steal: the registration verified, plus one residual gap named with drafted patch text.
1. LAW-12 amendment_gate is registered, byte-backed, falsifier verbatim, hook-enforced via B2-164, window live to 2026-10-10 with B2-424 binding the verdict filing.
2. Residual gap: registered trace_provenance permits fixture-first provenance. Drafted patch, not filed, registry untouched, amend trace_provenance to: "scenario cards exist and each cites a real failing trace by pointer (receipt path or ledger row id) that pre-dates the proposal; no pre-existing trace, no card; fixture rows satisfy only genesis-clause births and must cite their minting receipt." The patch is itself a LAW-12 amendment and must pass the five axes it amends.
3. Clause green mid-window: cards day 0, repass row 19 (law12-genesis-repass), neither death condition fired.

## Falsifier
none proposed

## Bibliography
1. memory/law/registry.json, read 2026-09-26
2. watch/inbox/BURN_rsi-harness_20260926.md line 25, read 2026-09-26
3. watch/inbox/BURN_rsi-harness_20260925_c.md, read 2026-09-26
4. watch/inbox/BURN_rsi-harness_20260926_b.md, read 2026-09-26
5. watch/inbox/burn_wave_20260926/B2_163_law12_register_20260926.md, read 2026-09-26
6. watch/inbox/burn_wave_20260926/B2_255_double_spend_20260926.md, read 2026-09-26
7. githooks/pre-push, read 2026-09-26
8. memory/burns/LEDGER.jsonl, LAW-12 rows, read 2026-09-26
9. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md s4, read 2026-09-26
10. Web search 2026-09-26, no relevant results, nothing fetched
