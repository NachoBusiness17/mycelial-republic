# DFDIALS mixed-dial file census (necessity proof for the file-level tiebreak)

2026-09-26, revision session of dfdials-one. Purpose: the judge's critique bullet 4 asked that the file-level tiebreak clause carry a census, not four anecdotes: "153 files carry more than one dial under your mapping (judge-verified); file that 153 count as the necessity proof."

Command run (this session, raw script and raw output preserved beside this receipt):

```
cd C:/Users/foste/Documents/projects/local_sovereign_agent
./.venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/tmp_dfdials_census.py
```

Script: `watch/inbox/ractor_panel_20260926/tmp_dfdials_census.py` (read-only over `configs/violation_baseline.json` and the scanner in `tools/violation_ratchet.py`). Raw output: `watch/inbox/ractor_panel_20260926/tmp_dfdials_census.out`.

Dial mapping used (from the surviving card; total function of rule name; unknown rules fall to manual-only):

- always-on: parse-error, unreadable
- default-on: except-pass, bare-except, env-key-read, cwd-relative-path
- opt-in: file-too-long, shell-true
- manual-only: todo-undated, mimosa-ssrf, mimosa-path-traversal, mimosa-code-injection, mimosa-command-injection

Raw output (verbatim; the script prints ASCII only):

```
total claims: 933
rule counts: {'bare-except': 1, 'cwd-relative-path': 3, 'env-key-read': 22, 'except-pass': 652, 'file-too-long': 194, 'mimosa-code-injection': 2, 'mimosa-command-injection': 1, 'mimosa-path-traversal': 25, 'mimosa-ssrf': 29, 'shell-true': 3, 'todo-undated': 1}
dial counts: {'default-on': 678, 'manual-only': 58, 'opt-in': 197}
dial sum: 933
rows outside named rule table (fall to manual-only by clause a): 0
  always-on: 0 rows
  default-on: 678 rows
  opt-in: 197 rows
  manual-only: 58 rows
files with more than one dial among registered claims: 153
mixed-dial composition: {('default-on', 'manual-only', 'opt-in'): 1, ('default-on', 'opt-in'): 149, ('manual-only', 'opt-in'): 3}
  tools/pupeteer_gauntlet.py: 3 dials -> ['default-on', 'manual-only', 'opt-in']
  tools/wandr_selfeval.py: 2 dials -> ['manual-only', 'opt-in']
  tools/steer_compare.py: 2 dials -> ['manual-only', 'opt-in']
  tools/ghost_tournament.py: 2 dials -> ['manual-only', 'opt-in']
full-scope scan hits: 882 files_scanned=1190
parse-error hits: 0; unreadable hits: 0
NEW rows now: 7
  NEW 8d41e611f98d3fa5 file-too-long: tools/census_drift_patrol.py:403
  NEW 5ae40a2d649a9b92 except-pass: tools/ledger_lock.py:136
  NEW 3b1726dec4670996 except-pass: tools/openrouter_free_gate.py:84
  NEW f0d81bd311a1a15e file-too-long: tools/probe20_run.py:421
  NEW e3b7845ea79cf553 cwd-relative-path: tools/queue_dupes_check.py:33
  NEW 0dfc04119a40f245 except-pass: tools/transport_precheck.py:134
  NEW f2ce896c858aa404 except-pass: tools/visor.py:250
```

Findings:

1. The census confirms the judge's 153 on an independent run: 153 files carry more than one dial among their registered claims. Composition: 149 files are default-on + opt-in, 3 files are manual-only + opt-in, 1 file (`tools/pupeteer_gauntlet.py`) carries all three of default-on, manual-only, and opt-in.
2. The four anecdotes from the surviving card verify inside the census: `tools/pupeteer_gauntlet.py` at 3 dials; `tools/wandr_selfeval.py`, `tools/steer_compare.py`, `tools/ghost_tournament.py` at 2 dials each (manual-only + opt-in in all three cases).
3. Partition re-verified: 933 claims, dial counts default-on 678 / opt-in 197 / manual-only 58 / always-on 0, sum 933, zero rows outside the named rule table.
4. Always-on zero proof (used by the rewritten retirement condition 1): full-scope scan over 1190 files emitted 0 parse-error hits and 0 unreadable hits, and the register holds 0 claims on those rules.
5. NEW set at run time (used by the sequencing answer to critique bullet 3): 7 rows, fingerprints and current line numbers above. Two line numbers drifted from the judge's citation (ledger_lock 125 to 136, visor 131 to 250); fingerprints are detail-based (rule NUL file NUL detail, `tools/violation_ratchet.py:19-20,84-85`) so line drift does not change identity.
