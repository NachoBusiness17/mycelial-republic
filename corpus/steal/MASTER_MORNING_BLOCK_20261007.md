# MASTER FOLD - MICKEY-17 v2.1 MORNING BLOCK, 2026-10-07

- genre: execute - slug: morning-block-20261007 - folded_at: 2026-10-07T11:37:12Z by the fold-counting script (sha256 58bd72c79c6d)
- casualty census: fired 8, landed 8, rows 36, excluded 0 (FOLD_SECTIONS.md, this run)
- archive: `memory/runs/mickey17_v2/runs/morning-block-20261007/lanes` (8 lane JSONs + 8 checks JSONs)
- authoritative sections: `memory/runs/mickey17_v2/runs/morning-block-20261007/FOLD_SECTIONS.md`
- copies: `corpus/steal/MASTER_MORNING_BLOCK_20261007.md` (estate) and `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_MORNING_BLOCK_20261007.md` (workspace)
- number law: every number is the counting script's unless tagged `carried` (lane-file or run-metadata material); every steal sentence carries lane id + row index.

The settlement in one paragraph: eight lanes woke to named gaps and filed in one grammar (claim, quote, estate_status, steal). Seventeen rows executed, two executed with named deviations, four are blocked with named unblocks. Thirteen rows wear "?" in the script's scoreboard because three lanes (m3-index-gap, m7-phantom-erratum, m8-boot-regen) filed an alternate row grammar with a `status` key and no `estate_status`/`leverage` fields, so the counter could not read them (carried: read of the eight lane files against the FOLD_SECTIONS.md counts). That grammar drift is itself a structural finding: the fold can only count what the row grammar carries. The fold's job is not praise; it is to let the structure speak - what ran, what is blocked, what failed, what is owed.

## CASUALTY HEADER (script, verbatim)

- fired: 8
- landed (parseable files): 8
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

No refills owed, no tombstones: the casualty arithmetic closes clean.

## SCOREBOARD (script, verbatim)

- rows: 36
- estate_status: executed 17, ? 13, blocked 4, executed-with-deviation 2
- leverage: high 13, ? 13, medium 8, low 2

### Fidelity, verifier, width (script, verbatim)

- rows with all of quote/source/steal/estate_status non-empty: 23/36 (63.9%)
- lanes with persisted checks: 8
- verdicts: deep_tier2 12 (verdict split: verified 12), supports 36 (supports split: no 6, yes 30)
- deep_tier2 join: 7/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 5
- rows/lane: median 5, max 5, min 3
- top-10 lanes share: 100.0%
- exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

The verifier table reads well: twelve deep tier-2 checks ran against this run and all twelve verified. Tier-1 quote-support read "no" on 6 of 36 rows; two of those six (m1-row0a#1, m1-row0a#2) were deep-verified anyway, and one (m6-graph-supersession#0) was judged quote-non-supportive at tier 1 while deep tier 2 verified the claim from code bytes. Lesson banked by the run's own structure: a thin quote does not sink a true claim, and a smooth quote does not save a false one; the bytes decide.

## PRISMA FLOW (script, verbatim)

- identified: 36
- screened: 36 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 36
- invariant: identified == included + excluded **HOLDS** (36 = 36 + 0)

## EXECUTIONS - script TOP-K with proof quotes (12 steals, all leverage high)

Deep tier-2 note: the fold gate's deepChecks carried 12 verdicts for this run, all "verified"; the tier-1 supports verdicts below are quoted where they differ from the deep result. Quotes are from the named lane JSON rows; the deep receipt is the fold gate's own deepChecks payload.

### E1 - [high] m1-row0a#1 - named gate run post-edit; zero new findings minted

- Claim: ran the ask's named gate (.venv/Scripts/python.exe tools/citation_lint.py check --files AGENTS.md) post-edit, then re-ran it on a reconstructed pre-edit copy: outputs byte-identical, so this lane's edit minted zero new findings; the red is pre-existing.
- Proof quote (lane m1-row0a.json row 1): "CITATION-LINT: FAIL records=1 anchors=4 numbers-checked=24 blocking=3 warns=2 enforce-tokens=False"
- Tier 1 supports: no (one output line cannot show the two-run comparison). Deep tier 2: verified - the gate was re-run on the current tree and the first line was byte-identical; reconstructed pre-edit copies still FAIL with the same blocking=3 / warns=2, so the red predates the edit wave.
- Steal (m1-row0a#1): residual - the 3 blockers pre-exist at AGENTS.md:29 and configs/citation_lint_baseline.json holds no AGENTS.md rows; githooks/pre-push:25 runs citation_lint check --changed with no baseline flag, so the coordinator's push of the already-modified AGENTS.md blocks until line 29 is fixed or baselined by name (carried).

### E2 - [high] m1-row0a#2 - negative first-class: the census bullet's phantom numbers pre-exist

- Claim: 3 PHANTOM-NUMBER blockers at AGENTS.md:29 (the census carrier bullet: 4,188, 4,147, 100M against the census receipts named in that sentence) plus 2 TOKEN-MISS warns at lines 5 and 45 pre-exist this lane's edit; not fixed here because the register row scope is exactly one edit and the census bullet is operator-owned carrier history.
- Proof quote (lane m1-row0a.json row 2): "AGENTS.md:29 PHANTOM-NUMBER 4,188 number appears in none of the sentence's named sources"
- Tier 1 supports: no (one line of three blockers). Deep tier 2: verified - HEAD line 29 is byte-identical to working line 29, the working diff touches only lines 5 and 44, and all three numbers grep zero hits in the three named census receipts (watch/inbox/last_mile_20260930/AG7_CENSUS_SEED.md, watch/inbox/last_mile_20260930/B17_CENSUS.md, watch/inbox/wave5_repair/patrol-fix.md).
- Steal (m1-row0a#2): fix AGENTS.md:29 by anchoring the census numbers to the receipt that holds them byte-level (watch/inbox/NIGHT_SHIFT_20261004_CLOSE.md per the Clippy bullet's own receipt trail) or accept by name via --baseline configs/citation_lint_baseline.json before the next push. Cross-filed in BLOCKED tier B1.

### E3 - [high] m2-todo-truths#0 - Stone 5 Grok asks 1-3 flipped done; ask 4 re-seeded open

- Claim: line 238 flip executed: Stone 5 Grok asks 1-3 marked done with the three xai_grok47 receipt pointers (GROK_PREREG_ADVERSARIAL_20261003.md, GROK_W4_RERUN_PROTOCOL_20261003.md, GROK_OCTOBER_FOLD_20261003.md, all dated 2026-10-03 grok-4.7), and ask 4 (BURN_* filings audit) re-seeded as its own open line bound to the GROK_ASK4_SCOPE_FREEZE_20260926.md 39-file scope; no ask-4 receipt exists in watch/inbox/xai_grok47/.
- Proof quote (lane m2-todo-truths.json row 0): "ask 1 GROK_PREREG_ADVERSARIAL_20261003.md (10 weaknesses on the stone-1 Arm C prereg + amendment 1, including the non-integer-solve flag that \"8.1/30\" and \"6.9/30\" equal 0.27*30 and 0.23*30 exactly"
- Tier 1 supports: no (fragment covers ask 1 only). Deep tier 2: verified - landed bytes at queue/todo.md:239-240, all three receipts on disk with grok-4.7 / 2026-10-03 line-1 stamps, directory holds exactly those 3 files (no ask-4 receipt), and the scope freeze card binds the 39-file surface.
- Steal (m2-todo-truths#0): residual - fire ask 4 as a LOCAL repo-byte gopher on the frozen 39-file surface (pick the 5 claims that would most embarrass us if false, byte-check each against its cited source). Cross-filed in NEXT REGISTER N10.

### E4 - [high] m2-todo-truths#1 - drain claim closed DRAIN DEAD on a byte census

- Claim: line 233 kill-and-reseed executed: the FIRED-drain claim closed as DRAIN DEAD with the byte census (20,578 parsed rows 09-24 to 10-06, zero ok:true, 20,432 [429] fails, 47 TimeoutError fails, last write 2026-10-06T13:39:33Z on nvidia-glm53/nvidia-dsv41) and an open re-seed line naming the schtask driver, the nvidia TimeoutError mode, the kill verb (schtasks /Change /DISABLE) and the repair options.
- Proof quote (lane m2-todo-truths.json row 1): "\"brief\": \"[fail:TimeoutError: The read operation timed out]\", \"ok\": false}"
- Tier 1 supports: no (raw row fragment carries no census). Deep tier 2: verified - every census number reproduced from `state/fuel/full_scan_ledger.jsonl` bytes (grep counts 0 / 20,432 / 47; 20,578 parsed rows), and queue/todo.md:233-234 carries the CLOSED checkbox plus the open re-seed naming the kill verb verbatim.
- Steal (m2-todo-truths#1): residual - the schtask "Estate FullScan" still fires daily 09:35 and burns the 429 storm; the kill-or-repair decision is the open re-seed line (kill = /DISABLE, repair = drop groq-llama33/groq2-llama33 lanes, 18,327 of the fail rows, or raise the nvidia timeout) (carried). Cross-filed in NEXT REGISTER N3.

### E5 - [high] m2-todo-truths#2 - box_burn_watch wired to its own nightly trigger (executed-with-deviation)

- Claim: line 234 sub-item (3) wire arm executed: box_burn_watch got its own nightly trigger because the register's assumed nightly burn driver does not exist (grounding_chain.jsonl dark since 2026-09-26T13:13:30Z) - scripts/box_burn_nightly.ps1 + scripts/register_box_burn_task.ps1 written, schtask MagBoxBurnNightly registered daily 22:00 with the carrier self-stopping at 07:00 (family-box law inside the tool), sub-item (3) rewritten to the new truth with the job-firing half kept open.
- Proof quote (lane m2-todo-truths.json row 2): "SUCCESS: The scheduled task \"MagBoxBurnNightly\" has successfully been created."
- Deep tier 2: verified - the task queried live (daily 22:00, enabled, Last Result 0), both scripts on disk, the rewritten sub-item on disk, and the 07:00 self-stop demonstrably fired. Verifier caveat: the quote is the canonical schtasks console message found only in the lane's own receipt JSON, not landed estate bytes; corrected in the receipt before the row is reused as a citation pattern.
- Steal (m2-todo-truths#2): deviation recorded - the register assumed wiring INTO a nightly burn driver; no live driver exists, so the watcher got its own trigger and the deviation is named in the rewritten sub-item (carried).

### E6 - [high] m2-todo-truths#3 - end-to-end fire proof: the ledger left its 11-day dark state

- Claim: schtasks /Run fired MagBoxBurnNightly and the ledger left its 11-day dark state - first row since 2026-09-26T10:59:18Z landed at 2026-10-07T08:42:44Z (cpu 64.2 mem 63.4), second row at 08:57:22Z (cpu 100.0), task Status Running, next scheduled fire 10/7 22:00; the 08:57 row carries a named gpu_error.
- Proof quote (lane m2-todo-truths.json row 3): "{\"ts\": \"2026-10-07T08:42:44.826454+00:00\", \"cpu\": 64.2, \"mem\": 63.4, \"disk_read_mb_s\": null, \"disk_write_mb_s\": null, \"gpu\": 0.0, \"gpu_error\": null,"
- Deep tier 2: verified - quote byte-exact at `state/fuel/box_burn_watch.jsonl` line 420, dark predecessor at line 419 (10d21h43m gap), live schtasks query corroborates the fire and the 22:00 next run. Three narrative defects named by the verifier, none load-bearing: the "second row" ordinal is wrong (second row is 08:44:23Z; the 08:57 row is the 10th), "Running" was stale at verify time, and "timed out" is interpretation of a truncated gpu_error repr.
- Steal (m2-todo-truths#3): done.

### E7 - [high] m4-hermes-rails#0 - TERMINAL rails landed in the burn carrier

- Claim: TERMINAL rails landed in tools/hermes_burn.py mirroring the refusal-law shape: transport failures bank as data rows (turn null, ok false, transport_error), the ask's trailing run of 2 consecutive transport failures mints <ask_dir>/TERMINAL with skip-on-sight entry, one EVIDENCE-PREFLIGHT failure mints immediately, and the main() summary splits paid/skipped/failed; pinned by tests/test_hermes_burn_terminal_rails.py (6 probes, 61 passed across the touched set) (carried).
- Proof quote (lane m4-hermes-rails.json row 0): "HERMES-BURN: PASS - paid 0 skipped 3 failed 0 of 3 asks; ledger total $94.64"
- Tier 1 supports: yes (live run output in the claimed new split format). Not deep-checked; code bytes are tier-2 material on any later dispute.
- Steal (m4-hermes-rails#0): done; A1 re-arm is operator-owned (edit ask bytes + delete the TERMINAL marker) (carried).

### E8 - [high] m4-hermes-rails#1 - decisive balance probe: the 402 is a reserve-cost wall

- Claim: decisive balance probe run (3 rounds, 20 banked PROBE rows in memory/runs/hermes_burn/usage.jsonl): the 402 is a reserve-cost wall, not account death and not per-model; all 8 candidate balance endpoints 404; provider returns usage.cost per call (rate_source openrouter_list); key-2 balance bounded [0.16, 0.17) USD (mt=16000 pays, mt=17000 402s), key-1 < 0.16; a sonnet A1-shaped ask reserves ~0.34 and 402s deterministically while haiku-shaped asks reserve ~0.13 and still fit.
- Proof quote (lane m4-hermes-rails.json row 1): "Key-2 balance is therefore bounded [0.16, 0.17) USD."
- Tier 1 supports: yes (decisive result line restating the pivotal finding). Not deep-checked; the 20-row count and endpoint census are tier-2 material.
- Steal (m4-hermes-rails#1): residual - operator top-up or A1 re-stage to haiku-class; instruments left rerunnable at memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/probe_nous_balance.py (--ladder) and memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/probe_a1_payload.py (carried). Cross-filed in NEXT REGISTER N9.

### E9 - [high] m4-hermes-rails#3 - refire-or-annotate executed as a live three-fire arc

- Claim: refire at 09:02:21Z banked A1 transport row 1 (exit 1, new split summary in logs/hermes_burn_247.log), the 09:11:39Z fire banked row 2 and the carrier minted the TERMINAL marker itself, and the next fire read paid 0 skipped 3 failed 0, PASS, exit 0; the hourly exit-1 attention.md flood ends and the clock is green.
- Proof quote (lane m4-hermes-rails.json row 3): "[TERMINAL terminal marker (2 consecutive transport failures), minted 2026-10-07T09:11:39.136276Z for ask id H247_A1_MIRA_LANE_FORECASTER_SPEC."
- Tier 1 supports: yes (the minted marker names cause, moment, and ask id). Marker on disk at `queue/hermes_247/A1_mira_lane_forecaster/TERMINAL`.
- Steal (m4-hermes-rails#3): done.

### E10 - [high] m5-fold-guard#0 - FIRED-BELOW-ARCHIVE gate: a negative missing count can no longer fold

- Claim: added the FIRED-BELOW-ARCHIVE gate at mickey17_v2_fold.py:258-262: exit 2 with a named message when --fired is below the lane-archive count (covers a directly negative --fired too), so a negative missing count can no longer fold into the casualty header as a computed fact; pure insertion, byte-verified.
- Proof quote (lane m5-fold-guard.json row 0): "FIRED-BELOW-ARCHIVE GATE: --fired {fired} < archive count {n_files} in {lanes_dir}; "
- Deep tier 2: verified - gate at exactly the claimed range in `tools/mickey17_v2_fold.py` (line 258 condition, 259-261 message, 262 exit 2), negative --fired covered by the comparison semantics, and the change is a pure insertion (13 added, 0 deleted).
- Steal (m5-fold-guard#0): done (residual: watch the first live trip for the incident receipt) (carried).

### E11 - [high] m5-fold-guard#1 - test file proves the negative-count render is dead

- Claim: new test file proving the negative-count render is dead: --fired 1 and --fired -5 against a 2-file tmp archive each exit 2 with the gate message and write no FOLD_SECTIONS.md; controls prove fired==count, fired>count, and default all still fold with nonnegative missing.
- Proof quote (lane m5-fold-guard.json row 1): "for fired in (1, -5):"
- Deep tier 2: verified - quote byte-present at `tests/test_mickey17_v2_fold_fired_below_archive.py` line 56; exit-2, no-write, and control assertions all mapped to landed bytes; verifier re-ran the file: 2 passed in 0.97s.
- Steal (m5-fold-guard#1): done.

### E12 - [high] m6-graph-supersession#0 - supersession is now a collector kind: it survives the weave's own rebuild

- Claim: superseded_rows/_superseded_wire parse the register ROWS table into superseded/superseder node pairs joined by superseded_by edges; _edges() regenerates the edge from the dead node's superseded_by field (maps_to precedent) and build() assembles the kind, so supersession survives the weave's own rebuild - the d04 lesson byte-proven: a rebuild wiped all 117 manual why_context edges to 0 on a copy.
- Proof quote (lane m6-graph-supersession.json row 0): "a superseded node carries its replacement's node id + the evidence cell, so the superseded_by edge regenerates on every build() instead of dying as a manual append."
- Tier 1 supports: no (prose, not execution evidence). Deep tier 2: verified - the quote is landed source prose at mag/knowledge_graph.py lines 301-303 and the code is real: SUPERSEDED_REL at :237, superseded_rows at :244-261, _superseded_wire at :264-289, _COLLECTOR_KINDS at :60-61, build() assembly at :609; a live parse minted 12 nodes / 6 edges with materialized endpoints.
- Steal (m6-graph-supersession#0): done.

The remaining 24 included rows are folded as script counts in the scoreboard and PRISMA sections above; their per-row receipts live in the lane JSONs and the run metadata's laneOut notes.

## BLOCKED TIER (4 rows; script scoreboard: blocked 4)

| # | row (lane#row) | leverage | why blocked | next-sitting unblock |
|---|---|---|---|---|
| B1 | m1-row0a#2 | high | AGENTS.md:29 census carrier bullet carries 3 PHANTOM-NUMBER blockers (4,188 / 4,147 / 100M) plus 2 TOKEN-MISS warns at :5 and :45; deep-verified pre-existing (HEAD line 29 byte-identical to working line 29); operator-owned carrier history outside the row's one-edit scope | anchor the census numbers to the byte source receipt or accept by name via --baseline configs/citation_lint_baseline.json before the next push; githooks/pre-push:25 runs the gate with no baseline flag, so the coordinator's push of AGENTS.md is blocked until cured (steal carried from m1-row0a#1/#2) |
| B2 | m2-todo-truths#4 | low | queue/todo.md carries PRE-EXISTING PHANTOM-NUMBER blocks at :30 (1302, 08-26 janitor row) and :232 (1031, 09-25 Stone 2b row); disjoint-lane law kept this lane's hands off other lines; the file is gitignored (.gitignore:51) so no push gate enforces them | whoever owns lines 30/232 next edits those rows' citations or registers a baseline accept; an operator pass over the ignored register's pre-existing lint debt is cheap (steal m2-todo-truths#4) |
| B3 | m5-fold-guard#4 | low | tools/mesh_delta.py measures 610 lines (carried) over the 400 cap with NO file-too-long entry in configs/violation_baseline.json at HEAD; the bystander's inadvertent registration was reverted - acceptance is the owning lane's to mint, never minted by a passerby | mesh-delta lane (or operator) runs baseline-update --by with a note naming the 610-line growth, or prunes the file; it surfaces as NEW on the mesh lane's next --changed run or the next full baseline-update (steal m5-fold-guard#4) |
| B4 | m6-graph-supersession#5 | medium | graph_heal's why_context edges are still wiped by any rebuild - the lane's own probe (build() on a copy) took 117 why_context edges (carried) to 0 surviving; curing heal durability is the graph_heal instrument's register item, not the supersession lane's | give why_context heals the same collector treatment (node-carried field + _edges branch in `tools/graph_heal.py` / `mag/knowledge_graph.py`) or a re-heal hook after build(); one seat, one sitting (steal m6-graph-supersession#5) |

## NEGATIVE RESULTS (counted reasons; tombstones: [])

Tombstones: none. Run metadata tombstoned: []; casualty header: parse errors 0, missing 0. Every negative below was filed, not buried.

| # | reason class | count | lanes / rows |
|---|---|---|---|
| 1 | Pre-existing citation-lint red on shared AGENTS.md (3 PHANTOM-NUMBER + 2 TOKEN-MISS, deep-verified pre-existing) | 1 | m1-row0a#2 (BLOCKED B1) |
| 2 | Pre-existing PHANTOM-NUMBER blocks on sibling prose rows (queue/todo.md:30 and :232; watch/inbox/RUN_CLOSEOUT_20261007.md:31 "37.7M" and :43 "136.3M", git-grep shows no repo byte source) | 2 | m2-todo-truths#4, m7-phantom-erratum deviation 2 |
| 3 | Gates/suites red on other writers' pre-existing defects (mag.shared_surface validate ok:false with 111 NEW-event-key errors, zero naming the lane's 22 items; adjacent pytest 2 failed / 67 passed on unknown keys + stale configs/links_kind_baseline.json; tree-wide citation lint red) | 3 | m3-index-gap rows 3-4, m4-hermes-rails negative 1 |
| 4 | Named runs not run, stated as not run (pytest -q twice where no code changed; the ~4.5h secret-scan end-to-end rerun substituted by the byte-planted cure probe plus the 10-12 next fire) | 3 | m1-row0a note, m2-todo-truths verification.not_run, m8-boot-regen negative 3 |
| 5 | Probe economics corrections (round-1 "wall healed" misread corrected by rounds 2-3; A1-payload probe under-banked real cost 0.0001 vs provider 0.0999, correction row appended) | 2 | m4-hermes-rails negatives 2-3 |
| 6 | Ops observations filed not fixed (twin-fire race 09:01-09:11Z banked sequentially; ratchet GROWTH note on tools/hermes_burn.py 428 to 552 lines) | 2 | m4-hermes-rails negatives 4-5 |
| 7 | Instrument/environment limits (repo-wide dead-cite sweep stopped at 2.5 min, scoped sweeps clean; ListWorkflowRuns unreachable from the seat so the d96545c9 disposition rides estate bytes; Mimosa hook false-positives blocked 3 of 6 file writes, worked around inline with no hook bypass) | 3 | m1-row0a note, m7-phantom-erratum deviation 1, m8-boot-regen negative 1 |
| 8 | Deviations executed and disclosed in the same sitting (baseline-update ran without --by during a --help probe and swept sibling debt, hand-corrected; watcher wired to its own trigger because no nightly driver exists; terminal disposition attributed to the coordinator-side ask verbatim; accuracy.md delta is the ERRATUM append only atop a prior-sitting rewrite) | 4 | m5-fold-guard#3, m2-todo-truths#2, m7-phantom-erratum row 3 + deviation 3 |
| 9 | Expected edit correctly not owed (conditional timeout raise at mag/boot_regen.py:50 not triggered because the rerun exited 0) | 1 | m8-boot-regen negative 2 |
| 10 | Pass-through findings outside lane scope, filed not fixed (zknot METER ALARM worsening 129 vs 102; 8.04 GiB/day repo growth over the 1.00 GiB/day bar; REDBOARD reds beyond the ask's named three: Estate Ratchet, MagTipWitnessDaily, MagCensusPatrolDaily, MagLeaveProtocolDaily, Estate KeyAudit, MagFreeLaneFleet) | 1 | m8-boot-regen negative 4 |

Total counted negative reasons: 22.

## NEXT REGISTER (top 10 residuals; one seat, one sitting each)

1. AGENTS.md:29 census bullet: anchor 4,188 / 4,147 / 100M to their byte-source receipts or accept by name via --baseline configs/citation_lint_baseline.json; the coordinator's push rides on it (m1-row0a#2; push-gate mechanics carried from m1-row0a#1).
2. watch/inbox/RUN_CLOSEOUT_20261007.md:31 and :43: name the instrument for "37.7M" and "136.3M" or baseline by name before the coordinator's push of that file (m7-phantom-erratum deviation 2).
3. Estate FullScan schtask: execute the open kill-or-repair line - schtasks /Change /TN "Estate FullScan" /DISABLE, or drop the groq-llama33/groq2-llama33 lanes (18,327 of the fail rows), or raise the nvidia timeout; the GLM deep-read + Cooper synthesis gate re-anchors on a ledger with ok:true rows (m2-todo-truths#1).
4. tools/mesh_delta.py 610-line debt: owning lane runs baseline-update --by naming the growth, or prunes the file under the 400 cap (m5-fold-guard#4).
5. why_context heal durability: give heals in tools/graph_heal.py the collector treatment (node-carried field + _edges branch) or a re-heal hook after build() (m6-graph-supersession#5).
6. Register the 6 unknown event keys (handoff, receipt, title, titles, verdict, verdicts; first lines 10637-10868 of watch/inbox/index_events.jsonl) in configs/events_key_schema.json with first-seen evidence; clears the 111-error shared_surface red (m3-index-gap owed_elsewhere).
7. Refresh configs/links_kind_baseline.json against the ~45 unregistered LINKS.jsonl kind rows from the scout/drop-ingest/operator-canon/olm-mine-cron writers (m3-index-gap owed_elsewhere).
8. Index the 39 still-unindexed inbox files through the same md-record-seal autoseal path that cured the ouroboros dir (m3-index-gap owed_elsewhere).
9. Nous key-2 wall: operator top-up or A1 re-stage to haiku-class; probe instruments rerunnable at memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/probe_nous_balance.py and memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/probe_a1_payload.py (m4-hermes-rails#1).
10. Grok Stone 5 ask 4: run the BURN_* filings audit as a local repo-byte gopher on the watch/inbox/GROK_ASK4_SCOPE_FREEZE_20260926.md 39-file surface - pick the 5 claims that would most embarrass us if false, byte-check each (m2-todo-truths#0).

Held for the operator, not a seat: spend_balance grand figure (231.0322 over 28,553 calls, carried from m4-hermes-rails#2) into the AGENTS.md money line; the 8.04 GiB/day growth decision; zknot METER ALARM trend (m8-boot-regen negative 4).

## FOLD LAW CARRIED FORWARD

1. Row grammar is destiny: 13 of 36 rows were uncountable for leverage because three lanes used a `status` key where the counter reads `estate_status` (carried: lane-file read vs FOLD_SECTIONS.md scoreboard). One grammar, or the fold undercounts the very lanes that filed the most prose.
2. Quotes are fingerprints, not proof: tier 1 read "no" on 6 rows, deep tier 2 verified the underlying claims anyway on 3 of them (m1-row0a#1, m1-row0a#2, m6-graph-supersession#0), and one verified-quoted row (m2-todo-truths#2) was found quoting console output that exists only in its own receipt. The two-tier structure is doing real work; keep both tiers.
3. Blockers are named, priced, and owned: all four blocked rows carry a leverage grade and a one-sitting unblock, and two of them gate the coordinator's push. The register does not owe vague debt.
