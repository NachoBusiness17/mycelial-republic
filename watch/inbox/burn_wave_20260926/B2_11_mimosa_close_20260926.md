# B2-11 Mimosa L3 close 20260926

## Verdict

Close landed, with a count correction against the brief. The brief said 33 SSRF/path findings in archived 09-16 scripts; no sealed scan contains a 33 slice. Bytes: 30 HIGH occurrences in 19 files, all under watch/inbox/ (22 in moonshot_20260916 + wave_20260916, 8 in physical_computing/receipts + four_condition_battery). Both sealed scans (09-25, 09-26) agree on this count. All 19 files verified dead code, all 30 occurrences registered as 25 named claims in configs/violation_baseline.json (register 876 to 901), configs re-sealed by name, CONFIG-SEAL verify PASS. Zero findings in live mag/ code (mag/ has no ssrf/path findings at all), so nothing in scope is must-fix. The live-adjacent tail (tools/ 9, models/ 5) is named, NOT baselined, and fed to the queue. The brief's gate story was wrong in mechanism: the pre-push ratchet scans mag/+tools/ only (tools/violation_ratchet.py:34) and never sees watch/inbox; mimosa's own gate is a per-edit PreToolUse hook (145 status files: 136 clear, 8 inconclusive, 1 blocked on a Temp file). The current push blocker is tools/drift_pairs_stamp.py >400 lines (another lane's WIP), pre-existing and untouched by this lane.

## Evidence with file:line quotes

- watch/inbox/wave_20260916/u1_union_call.py:51 `with urllib.request.urlopen(req, timeout=300) as r:` (SSRF); :100 `open(OUT_PATH, "w", encoding="utf-8", newline="\n").write(text)` (path); :20 `from mag.flight_recorder import load_env` (it uses mag; nothing imports it back).
- watch/inbox/wave_20260916/D22_probe_pass2.py:113 `req = urllib.request.Request(base.rstrip("/") + "/models", headers=headers)`; :83 urlopen.
- watch/inbox/wave_20260916/e_union_alpha_20260916.py:202 `path = os.path.join(RUN_DIR, f"{tag}.py")` (model-tagged filename, run-once eval harness).
- watch/inbox/moonshot_20260916/tt3_union_fullsend.py:143 `with open(STATE_PATH, "w" ...)`; :148 `with open(out_path, "w" ...)`.
- watch/inbox/wave_20260916/d24_sweep2.py:64 `json.dump(results, open("watch/inbox/wave_20260916/d24_sweep2_out.json", "w" ...))` (cwd-relative write).
- watch/inbox/physical_computing/receipts/f6_fetch.py:117 urlopen; watch/inbox/four_condition_battery/w4_t16_build_battery.py:752 `with open(OUT, "w" ...)`.
- Dead-code proof: git grep -w of all 19 stems hits only catalog inventories (catalog/catalog.jsonl, watch/ESTATE_INDEX/ESTATE_INDEX.jsonl) and prose receipts; zero hits in mag/, tools/, scripts/, configs/, main.py; no __init__.py in any of the four dirs; AST check: 19/19 are main-guard or top-level one-shots, 0 classes.
- Baseline claim sample: rule "mimosa-path-traversal", file "watch/inbox/wave_20260916/rs_salon_witness_driver.py", accepted "2026-09-26", by "agent:B2-11 flash-lane burn 2026-09-26 (mimosa L3 close)", detail names lines + findingIds + scan id.

## Work done

1. Parsed both sealed scan finding sets; counted 30 watch/inbox ssrf/path occurrences (19 files, 25 file-class pairs); brief's 33 not reproducible, proceeded on bytes.
2. Read flagged lines in all 19 files; AST one-shot check; repo-wide reference grep; dead-code verified per file.
3. Registered 25 claims via watch/inbox/burn_wave_20260926/B2_11_baseline_update.py (fingerprints reuse the ratchet scheme, rules namespaced mimosa-ssrf / mimosa-path-traversal, note carries reason + scan id + prune caveat). Register 876 to 901.
4. Re-sealed configs by name per githooks/pre-push header; verify PASS (47/47).
5. Ratchet full check: NEW=1 on tools/drift_pairs_stamp.py (pre-existing, other lane, live code, NOT baselined here).
6. Not baselined, owed: tools/ 9 findings (projects_index x3, pupeteer_gauntlet x2, compaction_eval, fold_mickey17, ghost_tournament, steer_compare, tier_probe, wandr_selfeval), models/ 5 (providers x4, probe x1), scripts/ 43.

## Falsifier

This close is wrong if: any live path is later shown importing or executing one of the 19 scripts (grep stems again before deleting); a scan slice equalling 33 surfaces (produce the artifact); prune reaps the mimosa claims and nobody re-accepts them (check register size 901 after any prune); the mimosa PreToolUse gate blocks on one of these files despite the baseline registration (baseline is the ratchet's surface, mimosa's ledger is separate, hence B2-89).

## Bibliography

- .mimosa scan seal + findings + report, scan-2026-09-26T04-10-04.918Z-41fc75fa84c4 and scan-2026-09-25T18-15-58.463Z-fd400a18ce93
- tools/violation_ratchet.py, tools/config_seal.py, githooks/pre-push
- configs/violation_baseline.json (876 to 901), configs/.config_seal.json
- watch/inbox/MIMOSA_SCAN_20260925.md (prior triage: estate slice 102 path + 72 ssrf)
- .mimosa/hook-status/ 145 files; .mimosa/finding-ledger/v1/events 2060 files
- The 19 flagged files under watch/inbox/, read at the flagged lines

Bibliography closed.
