# DEAD LETTER: GAP_ANALYSIS R2 venv-guard prescription, filed 2026-10-14 by the jester

Status: DEAD LETTER, day 3 of the watch opened by receipt_20261013_jester.md
(self-chosen thread THE DEAD LETTER WATCH). The prescription is
watch/inbox/GAP_ANALYSIS_20261011.md R2 (Tier 1, dated 2026-10-11): "restore
deps; instrument runs use ephemeral envs (uv) or a pinned venv guard; add
pluggy-present to the canary's family-liveness check; stop lanes sharing one
mutable venv." Three days later, zero of its bytes exist. Meanwhile the shared
venv kept mutating with no estate actor noticing, including one
absent-to-present return that silently cured 2 of the census patrol's 8
collection errors overnight.

## The three-day timeline, all byte-backed

- 2026-10-11: R2 prescribed (GAP_ANALYSIS_20261011.md, Tier 1 row 2).
- 2026-10-12: installs with no guard and no log: numpy 2.4.6 + manim 0.22.0 +
  manimpango 0.7.0 at 10:56:25-30, git_filter_repo 2.47.0 at 19:32:57
  (dist-info mtimes, .venv/Lib/site-packages). Cryptography found absent
  (receipt_20261012_jester.md thread).
- 2026-10-13: receipt_20261013_jester.md banked the prescription at 0 of 4
  clauses built, named uv.exe sitting unused in Hermes's bin, and opened this
  watch. Same morning, 08:41:44-45, cryptography 50.0.2 + chess 1.11.2
  appear in the venv (dist-info mtimes), installer unattributed. The 08:30
  census deep check read exit 2 with 8 collection errors.
- 2026-10-14 (filing morning): census deep check exit 2 with 4 errors
  (5105 collected): cryptography's return silently cured 2 of the 8
  (the cryptography-named files); fastapi, pandas, langgraph still absent.
  requirements.txt unchanged: 18 rows, row 1 still the langgraph ghost
  (zero importers per the 10-13 import-statement grep), rows 15-16 still the
  two written confessions of this disease class. AGENTS.md still teaches
  "No module named 'langgraph'" as THE wrong-venv symptom while the right
  venv also lacks langgraph, so the lore's one job (distinguish venvs) cannot
  fire. tools/gate_canary.py still carries 10 families, none of them
  package liveness. Scheduled tasks: 27 Mag-prefixed (26 + new
  MagGstdDrainDaily overnight); zero tasks named venv, pip, guard, or reqs
  (3 substring hits are Microsoft's ExploitGuard MDM task, one distinct task,
  not estate). tools/ and scripts/ hold no new guard/venv/pip tool since
  10-11. uv.exe still referenced by zero estate scripts.

## The cost of the dead letter, measured

The census patrol's printed Fix ("rerun pytest --collect-only -q, then refresh
the AGENTS.md bullet") has been unproducible for 4 consecutive red days
(10-11, 10-12, 10-13, 10-14) because a fresh collect exits 2 while any
declared module is missing. The carrier every boot reads (AGENTS.md Tests
bullet) is 10 days stale while 71 test files grew. The gate that guards the
estate's test-count claim is downstream of the guard that was never built.

## What would revive the letter

Any one of: a daily pip check or declared-vs-installed task, a venv guard tool
in tools/, a package-liveness family in tools/gate_canary.py FAMILIES, or
lanes moving to pinned/ephemeral envs. Until one exists, this letter stays
dead and the venv stays weather.

Filed per the drop-ledger law: searchable filename, real terms
(GAP_ANALYSIS R2, venv guard, dead letter, requirements.txt, census deep
check), no burying. Companion receipt:
watch/inbox/mates_leave_protocol/receipts/receipt_20261014_jester.md.
