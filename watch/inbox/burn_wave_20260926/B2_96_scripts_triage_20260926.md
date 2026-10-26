# B2-96 scripts/ mimosa ssrf/path triage 20260926

## Verdict

Triage landed with a clean live/dead split against bytes. The sealed scan scan-2026-09-26T04-10-04.918Z-41fc75fa84c4 holds exactly 43 ssrf/path occurrences under scripts/ (29 path-traversal + 14 ssrf) across 21 files, matching the brief's counts (wave_driver.py 7, fetch_training_pdfs.py 4, m12_pairing.py 4, desk_baseline_probe.py 4, rest singles/doubles). Classification: 26 occurrences in 17 files are one-shot, manual, or dormant with NO driver of any kind and are accepted by name as 20 claims in configs/violation_baseline.json (register 900 to 920, mimosa-ssrf / mimosa-path-traversal namespaced, B2-11 fingerprint scheme); configs re-sealed by name, CONFIG-SEAL verify PASS 49/49. 17 occurrences in 4 files are live runner-driven code and are NOT baselined; they file as must-fix. The scheduled-task axis is empty for ALL 21 files: schtasks /query /fo csv today is 332 tasks with zero stem hits, and configs/lanes.yaml has zero stem hits, so nothing on the estate's own two scheduling surfaces drives any flagged script. The live set is live through mag code and config gates, not through schtasks. The B2-96 row sat pre-checked [x] from birth with no receipt (the B2-238 disease shape); this landing earns the check.

## Evidence with file:line quotes

- LIVE, must-fix (17 occurrences, 4 files), each line read in bytes this lane:
  - scripts/desk_baseline_probe.py:42 and :53 `with urllib.request.urlopen(req, timeout=timeout) as resp:` inside `_http_get_json` / `_http_get_text` taking a caller URL; :218 and :231 same shape. Live drivers: configs/coding_session_loop.yaml:23 `cmd: python scripts/desk_baseline_probe.py --ui-only` (ui_smoke preflight gate), mag/coding_session_loop.py:241 `from scripts.desk_baseline_probe import run_desk_ui_smoke` (module import), mag/governor_autorun.py:374 `filled["trust_probe"] = "python scripts/desk_baseline_probe.py"`, mag/nervous_system.py:210 probe command string.
  - scripts/hunger_ledger.py:120 and :147 `with open(LEDGER, "w", encoding="utf-8") as f:` with LEDGER = os.path.join(WATCH, "HUNGER_LEDGER.md") at :40. Live driver: mag/lane_runner.py:543-545 runs watch/cage_bin/hunger_ledger.py first and falls back to `rc2, out2 = _run_script("scripts/hunger_ledger.py")` on rc 2 (cage copy exists but differs, sha e0c0ce77 vs c4a00b72, so the scripts/ canonical copy is a real conditional execution path of live mag product).
  - scripts/wave_driver.py:195 `with open(path, "w", encoding="utf-8") as fh:` (save_state over caller path), :417 task_path, :521 `with open(args.board, "w", ...)` (CLI-arg board path), :613 res_path, :745-746 and :755 kb/steers/telemetry writes. Live execution: tests/test_wave_driver.py (7 tests) and tests/wave_driver_test.py (12 tests) drive the real CLI via subprocess; the module is the LOOK/JUDGE/ACT/RECORD tick-loop driver organ with heartbeat TTL (HEARTBEAT_TTL_S = 900, driver presumed dead past TTL). The 2026-09-12 staged night cron (21:15 tick + 06:45 pairing per queue/handoff/zcode/CONVO.md) is ABSENT from today's 332-task schtasks census, so the driver currently runs under tests and manual launch only; it stays must-fix because it is a loop organ, not a one-shot.
  - scripts/m12_pairing.py:391, :398, :405, :438 `with open(...)` writes (base/steers/inbox_json). Live execution: imported guarded by scripts/wave_driver.py:84 `import m12_pairing` and counted per tick via `_m12_note`, so it executes inside every driver run with M12 available; same status as its host driver.
- ACCEPTED, one-shot/manual/dormant (26 occurrences, 17 files, 20 file-class claims), representative line quotes, all read in bytes:
  - scripts/fetch_training_pdfs.py:282 `with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:` over a fixed URL manifest (URL built at :280 `req = urllib.request.Request(url, headers=h)` from manifest entries); :464 `with open(os.path.join(OUT_DIR, fname), "wb") as f:` with fname = entry["id"] + "." + ext from the manifest itself; :474 and :546 manifest/index writes. One-shot fetcher, mtime 2026-09-16, refs are catalog/index inventories and a docstring mention only.
  - scripts/the50_w6_t28_miss_entropy.py:216 `with open(OUT, "w", encoding="utf-8") as f:` (script-local constant, no main guard, top-level one-shot, mtime 2026-09-25).
  - scripts/the50_w7_t32_gstd_probe2.py:56 urlopen + :441 OUT write; scripts/the50_t08_spectro.py:359/:418; scripts/the50_t23_reaction_sigs.py:300; scripts/the50_t24_symbol_correlation.py:198/:202. THE50 probe family, refs are ESTATE_INDEX/steps inventories only.
  - scripts/council_runner.py:435 `resp = requests.post(endpoint, json=body, headers=headers, timeout=timeout)`; scripts/steering_suite.py:775 same shape. Manual suites (mtime 2026-08-27), zero repo code refs.
  - scripts/vision_bench.py:95 urlopen(timeout=300); dashboard-deploy/static/operator_board.html:143 documents a manual run `python scripts/vision_bench.py`, not a driver.
  - scripts/handoff_escalation_watcher.py:86 and :134 urlopen (Ollama/cloud escalate endpoints, env-driven). Manual-launch watcher (docstring usage lines :8-:10), mtime 2026-08-07, zero scheduler or mag/config drivers today (dormant).
  - scripts/k17_pilot.py:148 `with open(tmp, "wb") as fh:`; executed only by tests/test_k17_holds.py (5 subprocess tests over the real CLI).
  - scripts/ack_reaper.py:55 `with open(tmp, "w", ...)` and :65 `with open(path, "w", ...)`; executed only by tests/ack_reaper_test.py. scripts/tg_harvest.py:73; scripts/vision_endowment.py:92 (binary write) and :210 (urlopen); scripts/chain_index_completion.py:177 (STATS_PATH constant); scripts/fetch_founding_law.py:120 (urlopen, pairs with scripts/finalize_founding_law.py); scripts/roadmap_gap_probe.py:28 (urlopen).
- Scheduling census bytes: `schtasks /query /fo csv` = 332 lines, zero hits for any of the 21 stems; `grep` over configs/lanes.yaml for all 21 stems = zero hits. Ast census: 21/21 files exist, 20/21 have `if __name__ == "__main__"` guards (the50_w6_t28_miss_entropy.py is a top-level one-shot), class counts 0-2.
- Baseline claim sample: rule "mimosa-path-traversal", file "scripts/k17_pilot.py", accepted "2026-09-26", by "agent:B2-96 flash-lane burn 2026-09-26 (scripts/ ssrf/path triage)", note names the test-only execution plus the B2-95 explicit-re-triage law.

## Work done

1. Parsed the sealed scan findings.json (5305 findings); filtered scripts/ ssrf/path: exactly 43 occurrences in 21 files (29 path-traversal + 14 ssrf), counts match the brief per file.
2. Read all 43 flagged lines in bytes; AST shape census (main guards, classes, mtimes) over all 21 files.
3. Classification evidence: schtasks /query /fo csv full census (332 tasks, zero stems, run via powershell because Git Bash mangles /query); configs/lanes.yaml grep (zero); repo-wide reference sweep per stem over code surfaces (mag/, tools/, configs/, main.py, scripts/ cross-refs, tests/) excluding archives/catalogs/inventories; verified the three real execution edges (coding_session_loop yaml+import, lane_runner fallback, wave_driver import of m12_pairing) at exact lines.
4. Registered 20 accepted claims via watch/inbox/burn_wave_20260926/B2_96_baseline_update.py (asserts 43 total, 26 accepted, 20 claims so the live set cannot leak in; fingerprints reuse the ratchet scheme, note carries per-file acceptance evidence + B2-95 law). Register 900 to 920.
5. Re-sealed configs by name per githooks/pre-push header; verify PASS (49/49).
6. Filed the live 17 as must-fix in this receipt; no code changes made to any flagged file (triage lane, not a fix lane).

## Falsifier

This triage is wrong if: any accepted file shows up in a future schtasks census, lanes.yaml row, or mag/config import (re-run the three censuses before trusting the acceptance); wave_driver or m12_pairing gets a scheduler entry and its flagged writes stay unfixed (the must-fix set must be re-triaged as urgent); the cage hunger_ledger copy is deleted so scripts/hunger_ledger.py becomes the PRIMARY executed path rather than fallback (re-check mag/lane_runner.py:543-545); a finding slice other than 43 in scripts/ ssrf/path surfaces from a sealed scan (produce the artifact); the register count 920 shrinks without an explicit re-triage receipt (B2-95 says external debt leaves only by explicit re-triage).

## Bibliography

- .mimosa scan findings, C:/Users/foste/.mimosa/security-scans/project-8af8c49a6c1b0282e16b1e73/scan-2026-09-26T04-10-04.918Z-41fc75fa84c4/findings.json (5305 findings, sealed)
- The 21 flagged scripts under scripts/, read at the 43 flagged lines plus context
- schtasks /query /fo csv full census 2026-09-26 (332 tasks); configs/lanes.yaml (zero stems)
- configs/coding_session_loop.yaml:23; mag/coding_session_loop.py:241; mag/governor_autorun.py:374; mag/nervous_system.py:210; mag/lane_runner.py:543-545; mag/falsifier_counter.py:524-529; scripts/wave_driver.py:76-95; queue/handoff/zcode/CONVO.md 2026-09-12 rows (staged 21:15/06:45 cron, absent today)
- tests/test_wave_driver.py, tests/wave_driver_test.py, tests/ack_reaper_test.py, tests/test_k17_holds.py; dashboard-deploy/static/operator_board.html:143
- configs/violation_baseline.json (register 900 to 920), configs/.config_seal.json, tools/violation_ratchet.py (DEFAULT_ROOTS + B2-95 prune law), tools/config_seal.py
- watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md (acceptance pattern), watch/inbox/burn_wave_20260926/B2_96_baseline_update.py (this lane's registration script)

Bibliography closed.
