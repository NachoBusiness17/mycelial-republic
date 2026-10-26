# BURN rsi-harness _e - 2026-09-26

## Verdict
steal

## Evidence
- memory/law/registry.json read this pass: axes.trace_provenance still reads "scenario cards exist and each cites a real failing trace by pointer (receipt path or ledger row id); no trace, no card". Byte checks: grep -c 'LAW-12-AMD-1' = 0, grep -c 'pre-existing' = 0, and _d's OLD line matches the current file with grep -F count exactly 1. AMD-1 is unapplied.
- Registry changed since _d: LAW-12 now carries a clause_verdict block ("verdict": "pass", "date": "2026-09-26", "fail_rows_standing": 8, receipt watch/inbox/burn_wave_20260926/B2_484_law12_clause_verdict_20260926.md). No such block exists in _d.
- Suite run this pass (actual): exit 0, "SCENARIOS: 7 cards validated read-only (no registry row written)", "pass_control: all seven gates clean". G1, G2, G3, G4, G5, G7 fixtures each returned the expected FAIL exit 2; G6 soft fixture returned the expected PASS exit 0.
- Web search 2026-09-26: IETF draft-smith-opsawg-ai-network-governance-00 (expires 2026-09-25) carries a Self-Modification Prohibition, agents "MUST NOT modify their own..." rules, per the search snippet; direct fetch of the datatracker page returned 404, so the snippet is unverified beyond the summary. Nothing surfaced matches LAW-12's gated five-axis amendment shape; no late-September 2026 prior art found.

## Steal or Vacuous
Steal: AMD-1 still unfiled, diff re-verified and re-filed. Genesis countdown: registered 2026-09-26, window closes 2026-10-10, 14 days remaining as of today. The clause verdict was filed pass at day 0, but under the un-amended provenance axis, so the pass inherited the fixture-first gap AMD-1 closes. Scenario suite green (exit 0) this pass.

PASTE 1, byte-exact swap inside LAW-12 axes (6-space indent, trailing comma kept; verified against current bytes by grep -F count 1):
OLD:
      "trace_provenance": "scenario cards exist and each cites a real failing trace by pointer (receipt path or ledger row id); no trace, no card",
NEW:
      "trace_provenance": "scenario cards exist and each cites a pre-existing fleet FAIL row by pointer (receipt path or ledger row id) that pre-dates the proposal; no pre-existing trace, no card; fixture-minted rows satisfy format only and are disclosed as such, count only for genesis-clause births, and must cite their minting receipt",

PASTE 2, amendment metadata row inserted between LAW-12's closing brace and the "LAW-13" key (comma after the closing brace):
  "LAW-12-AMD-1": {
    "id": "LAW-12-AMD-1",
    "name": "trace-provenance-preexisting",
    "file": "watch/inbox/BURN_rsi-harness_20260926_d.md",
    "law": "trace_provenance requires a pre-existing fleet FAIL row that pre-dates the proposal; fixture-minted rows satisfy format only and are disclosed as such",
    "born": "2026-09-26",
    "by": "Mickey17-wave paper agent, BURN rsi-harness _d",
    "extends": "LAW-12 amendment_gate axes.trace_provenance"
  },

Both pastes are byte-identical to _d: the clause_verdict addition did not move the OLD line or the insertion anchor. Registry untouched this pass (B2-163's lane owns it; concurrent-claim law).

## Falsifier
none proposed

## Bibliography (closed)
1. memory/law/registry.json, read 2026-09-26
2. watch/inbox/BURN_rsi-harness_20260926_c.md, read 2026-09-26
3. watch/inbox/BURN_rsi-harness_20260926_d.md, read 2026-09-26
4. tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios, run 2026-09-26, exit 0
5. Web search 2026-09-26: IETF draft-smith-opsawg-ai-network-governance-00 snippet, datatracker fetch 404
