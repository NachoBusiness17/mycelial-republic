# BURN rsi-harness 20260927 f

## Verdict

green

## Evidence

- `memory/law/registry.json`, LAW-12 `axes.trace_provenance` carries the AMD-1 wording verbatim: "each cites a pre-existing fleet FAIL row by pointer (receipt path or ledger row id) that pre-dates the proposal; no pre-existing trace, no card; fixture-minted rows satisfy format only and are disclosed as such, count only for genesis-clause births, and must cite their minting receipt".
- Same file, `LAW-12-AMD-1` row exists: `"name": "trace-provenance-preexisting"`, `"born": "2026-09-26"`, `"extends": "LAW-12 amendment_gate axes.trace_provenance"`. State verified, not re-proposed.
- Same file, LAW-12 `clause_verdict`: `"verdict": "pass"`, `"date": "2026-09-26"`, `"fail_rows_standing": 8`, window "closes 2026-10-10".
- Suite run this pass: `.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` printed `SCENARIOS ok   pass_control: all seven gates clean`, then `SCENARIOS: 7 cards validated read-only (no registry row written)`. Exit code 0. Six FAIL cards failed as expected at exit 2, G6 PASS card passed.
- `watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md` s4, the mirror source: "agents write evals (failing call traces → versioned scenario cards: persona/goal/expected tools/end state)" and "human gate at merge" and "dual-runtime regression (fix must hold on both runtimes, stable path stays default with rollback)".
- WebSearch (2026-09-26, query "LLM agent harness regression suite gate evals generated from failure traces 2026") engine takeaway: "No single paper exactly titled around 'regression suites gate evals generated from failure traces'". Surfaced: HAL trace-judging via awb on PyPI, a Jun 2026 ResearchGate study with four agent failure archetypes, an eval-harness-first skill. Snippet level only; pages unread, so their content is owed, not claimed.

## Steal or Vacuous

Nothing new to steal this pass; the fleet already adopted the rsi-harness mirror as LAW-12 (amendment_gate, five nonzero axes, human gate `promote --apply`, enforcement arm `workflow_gate.py --scenarios`) and AMD-1 is applied. Verified today: scenario suite green (exit 0, seven cards, pass_control clean, no registry write), clause verdict pass on file backed by 8 standing FAIL rows. The two gaps SIX_DROPS s4 named are split: "harness stays as was" is now held in the LAW-12 guardrail (`incumbent_stays_default_on_fail_failed_proposal_filed_never_half_landed`); cluster-failures-by-runtime as a standing organ between judging and proposing remains unbuilt. The June 2026 failure-archetype taxonomy could feed that organ but is unread; mapping it is owed until read. No build proposed this pass.

## Bibliography

- `watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md` (read)
- `memory/law/registry.json` (read whole)
- `tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` (run this pass, exit 0)
- WebSearch result, "LLM agent harness regression suite gate evals generated from failure traces 2026", 2026-09-26 (snippet level; linked pages unread)
