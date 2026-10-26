# BREAK PASS: moonshot-1 (hostile second pass, break-moonshot-1)

Moment: 2026-10-07T14:09-14:35Z window. Instrument note: every check below was executed this sitting unless marked otherwise. Shell is git-bash on win32; `/flag` args get path-mangled to `C:/Program Files/Git/...`, so schtasks was invoked as `schtasks //Query ...` (the lens's sandbox could not enumerate schtasks at all; this break seat could, and did).

## Verdicts

### Finding 1 (MOONSHOT: OPA-style compile-time budget gate + LLMLingua-2 retires gaps 1+6) - CONFIRMED, two conditions added

Byte-checks that PASSED:
- `mag/context_pack.py:1486-1503` verified: `shed_order` list exists in that range; `"L0d rib vault amendments"` is `mag/context_pack.py:1501`; the stage-3 emit (`_emit_pack_offload(..., [_shed_name], 3)`) is `mag/context_pack.py:1514`. The lens's "rung 3" phrasing is the stage number, correct.
- d01 lane bytes verified verbatim at `memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/d01-seat-boot-pack.json:6,29-30`: live 08:29:23Z render, `total_chars 9471 > 7200`, shed `L0d rib vault amendments` at stage 3, MEASURED ON / Sybil / max_concurrency 0 hits, `1 failed, 41 passed` on the adjacent suite, schtasks MagLawPackDaily quote present at line 21.
- OPA claims re-fetched this sitting (https://www.openpolicyagent.org/docs/latest/management-bundles): signature failure = OPA "continues using its existing bundle and reports an activation failure via the status API"; revision in `.manifest`; ETag/If-None-Match/304 polling; "Delta bundles currently support updates to data only and not policies". All four lens claims byte-confirmed.
- LLMLingua claims re-fetched this sitting (https://github.com/microsoft/LLMLingua): MIT license; LLMLingua-2 = "token classification with a BERT-level encoder"; `compress_prompt(..., rate=0.55, ...)` and `force_tokens` both real API parameters. Confirmed.
- LIVE TEST RERUN (the check the move's acceptance names): `.venv/Scripts/python.exe -m pytest -q "tests/test_context_pack_quantized_laws.py::test_quantized_laws_section_renders_in_default_budget"` -> `1 failed in 8.20s`, `AssertionError: no known compiled law rode the pack`, render stamped mode=full 2026-10-07T14:09:36. Red live, not just per d01.
- FRESHNESS UPGRADE the lens did not have: `memory/context_pack_latest.md` was re-rendered at Oct 7 10:04 (after the lens's 08:29:23Z anchor), 7277 bytes, and greps 0 / 0 / 0 for MEASURED ON / Sybil / max_concurrency (`grep -c` each = 0). Third reproduction, current tree.
- `tools/thought_quantizer.py:118` `FLASH_MAX_CHARS = 220` verified; `compile_packs` at `tools/thought_quantizer.py:204`; d07 lane (`d07-hyperthink-quantizer.json:10`) names `.venv/Scripts/python.exe tools/thought_quantizer.py compile` as "the one sanctioned writer" and 625-row pack (kept=625, packed=625). Lens's sanctioned-writer cite confirmed.

CONDITION A (dropped by the lens): the 7200 budget is RENDERER-owned only. `grep -n "7200" mag/context_pack.py` -> line 165 `"max_chars": 7200`; `grep -n "7200|max_chars" tools/thought_quantizer.py` -> zero hits. The compile has no visibility of the render budget today, so "exit 1 when the pinned law set exceeds 7200" requires threading the budget into the compile (or gating at the pack boundary in the renderer). The estate's own d01 residual (lane JSON line 32) points renderer-side ("raise the full-mode budget or reprioritize L0d in mag/context_pack.py"); the lens's compile-time move is a real design change, not a tuning edit. Cost estimate survives (45 min is tight but plausible for the gate; the LLMLingua dependency add is extra).

CONDITION B (half-seen via d01, unaddressed by the move): `FLASH_MAX_CHARS = 220` (`tools/thought_quantizer.py:118`) is a SECOND loss point. Per d01 row 4, the MEASURED ON law rides only frontier fields (1796 / 2065 chars) while flash fields cut at exactly 220 before the mechanism byte. LLMLingua at rate 0.5 on the carrier fixes the stage-3 shed; it does nothing for the 220-char flash slice. The acceptance (MEASURED ON non-zero in a fresh render) plausibly passes via the surviving carrier alone, but the lens never states this dependency, and the rate-0.5 outcome remains a hypothesis (lens admitted; this break seat also did not pip-install or run llmlingua; not run).

Falsifier status: stands as stated (d01 two-day byte reproduction, now three-render with the 10:04 render). If a fresh `mag.cmd context-pack` greps non-zero for MEASURED ON in `memory/context_pack_latest.md`, the finding collapses to a tuning note.

### Finding 2 (git worktree makes the sibling-stash sweep class structurally impossible per seat) - CONFIRMED mechanism; falsifier CONFIRMED in the stronger form; one cite error

Byte-checks that PASSED (all live this sitting):
- Branch-exclusivity refusal: `git worktree add ../lsa_wt_probe_refuse mag/run-beta1-factory-build-audi-20260806T231709Z` -> `fatal: 'mag/...' is already used by worktree at 'C:/Users/foste/Documents/projects/local_sovereign_agent'`. The lens's "branch checkout refused in two worktrees" is now locally byte-verified, not just doc-fetched.
- Own HEAD/index: `git worktree add ../lsa_wt_probe_b -b wt-probe-break20261007` (56,904 files checked out), the worktree's `.git` file -> `gitdir: C:/Users/foste/Documents/projects/local_sovereign_agent/.git/worktrees/lsa_wt_probe_b`, containing `HEAD`, `ORIG_HEAD`, `index`, `refs`, `logs`, `commondir`. Own HEAD + index + shared object store confirmed. CLEANED UP: `git worktree remove --force` + `git branch -D`; `git worktree list` shows no probe residue.
- `tools/stash_sweep_watch.py` docstring verified: R3/R5 incident citation at lines 4-10 ("captured ALL working-tree modifications ... including another lane's eleven executor files"), "The tool has NO drop or pop verb by design" at lines 19-20 and census guard at line 218; tool is 285 lines total, matching the d02 full-read claim.
- d02 residual row verified at `d02-stash-seam.json` row `residual-cadence-open`: "no patrol cadence (schtasks or governor loop) runs stash_sweep_watch check mode".
- CITE ERROR: the lens cited `stash_sweep_watch.py:26` for `ROOT = Path(__file__).resolve().parents[1]`; ROOT is at `tools/stash_sweep_watch.py:34` (line 26 is `import json`). Content right, line wrong.

Falsifier RESOLVED, condition holds TODAY, in a form sharper than the lens stated: the estate's data plane is untracked single-instance.
- `git ls-files --error-unmatch memory/attention.md` -> "did not match any file(s) known to git" (UNTRACKED).
- `git ls-files --error-unmatch state/stash_sweep_watch_state.json` -> same (UNTRACKED).
- `git check-ignore -v watch/inbox/INDEX.json` -> `.gitignore:251` (GITIGNORED).
So a linked worktree seat gets the detector (tracked) but an ABSENT `memory/attention.md`, absent dedup state, and an empty inbox: its alerts land in a private attention.md the main seat never reads. The lens's own falsifier ("estate organs hard-bind ... worktrees fork the working surface and the cure costs more than the tripwire") is confirmed for the alarm surface; the 30-min probe as specified would come back RED unless the shared surface is relocated or per-seat alert routing exists first.

LENS MISS engaged here: `git worktree list` this sitting shows the estate ALREADY runs linked worktrees: `C:/Users/foste/Documents/projects/lsa_reboot_staging` (branch reboot-staging-20261003) and `C:/Users/foste/Documents/projects/worktrees/salon-arena-mvp` (branch codex/salon-arena-mvp), plus two detached temp worktrees (gate_canary, recovery_pack/baseline). The "one tree" premise is already practiced around; what is untested is whether an alarm-WRITING organ has ever run inside one.

### Finding 3 (gaps 3+4 are ONE runner law: billing/health state invisible in batch runners) - CONFIRMED and STRENGTHENED (two lens blind spots closed in the finding's favor)

Byte-checks that PASSED:
- `tools/hermes_burn.py:34-43`: "TERMINAL IS TERMINAL" at line 34; the 402-wall note at lines 40-43 ("fired MagHermesBurn247 hourly ~8 times, 402ing A1 twice per fire with nothing banked and no terminal state - the loop could not self-stop"). Receipt `watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md` EXISTS (6735 bytes, Oct 7 05:40).
- `tools/cost_rollup.py:305-328`: `build_spend_balance`, docstring "landed 2026-10-07" at line 306, `"schema": "spend_balance.v1"` at line 319. Confirmed.
- Falsifier checked and rejected: `tools/zknot_alarm.py` read in full. Meter windows are last-7d vs prior-7d (`tools/zknot_alarm.py:71-83`), alarm legs WORSENED / AT-OR-ABOVE-baseline (`:97-104`), explicitly WARN-only (`:26-28`). It is a self-steal-meter alarm on weekly windows evaluated at zknot rewrites, NOT a per-batch zero-yield signal. No existing estate alarm covers the runner law class; the falsifier does not hold.
- LiteLLM re-fetched (https://docs.litellm.ai/docs/proxy/customers): `/customer/info` returns a `"spend"` field; budget object "cached ... for 60 seconds"; `spend_tracked` webhook carries `"projected_spend"` and `"projected_exceeded_date"`. Confirmed. The exceeded-HTTP-status remains ABSENT from the page I fetched -> the lens's OWED marking stands (honest, still owed).
- Healthchecks.io re-fetched (https://healthchecks.io/docs/http_api/): `/fail` signals failure; `/<exit-status>` "interprets 0 as a success and all other values as a failure"; `/start` enables execution-time measurement and grace-time overrun detection; missing-ping alerts come from the check's schedule. The lens's "start-without-success alerts" is accurate as a composition, not a dedicated URL. Confirmed with that nuance.

BLIND SPOT CLOSED 1 (the storm receipt, "unlocated" per the lens): the storm is byte-verified live in `state/fuel/full_scan_ledger.jsonl`:
- `wc -l` = 20599 lines.
- `grep -c '"ok": true'` = 0 (ZERO ok rows in the whole ledger).
- `grep -c '"ok": false'` = 20579.
- `grep -c "429"` = 20433 rows carrying 429.
- First row: `{"ts": "2026-09-24T03:20:34.012832+00:00", "lane": "groq-llama33", ... "brief": "[429]", "ok": false}`.
- Last row: 2026-10-06T13:39:33Z, lane nvidia-glm53, fail TimeoutError.
The ask's summary numbers 20432/20578 are absent as literals: my census (`grep -rn "20432|20578"` over memory/ state/ queue/ watch/inbox/ tools/ scripts/ configs/, extensions .md/.json/.jsonl/.py/.ps1) hits ONLY coincidences (verkle leaf-hash fragments, `n_versions: 20432`/`20578` counters in memory/agent_state/versions/, microsecond timestamps). Live ledger reads exactly one row off each ask number (20433/20579 vs 20432/20578): consistent with a post-snapshot append or count-method difference; the class (multi-week 429 storm, zero yield) is byte-true regardless. The lens treated this as ask-borne authority; it is now tree-byte-borne.
- FULL_SCAN_REPORT_20260923.md:3 verified: "run 2026-10-06T13:39:33.090939+00:00 - records: 315 - ok: 221 - fail: 94" - and yes, a DIFFERENT surface (semantic catalog churn via state/fuel/record_briefs.jsonl) from the 429-storm ledger (lane intake sweeps). The lens's disambiguation holds; two surfaces share the "full scan" name.

BLIND SPOT CLOSED 2 (schtasks, which the lens's sandbox could not enumerate): live this sitting via `schtasks //Query //TN "Estate FullScan" //V //FO LIST`:
- Status: **Disabled** / Scheduled Task State: **Disabled** (the ask's "disabled 10-07" confirmed live).
- Schedule Type: Daily, Start Time 9:35:00 AM, Start Date 9/23/2026, Last Run 10/6/2026 9:35:01 AM, **Last Result: 0**.
That Last Result 0 on a storm run is the finding's exact class one layer UP the stack: the scheduler records process exit, never yield; the storm run "succeeded" at the schtasks layer. MagLawPackDaily live: Status Ready, Next Run 10/8/2026 9:30:00 AM (consistent with d01's quote; d01 could not observe the 10/7 9:30 fire because its ask ran 04:26-04:31 local).

## Truncation note

The lens JSON supplied to this break seat cuts off mid-finding-3 ("...every batch run). No findings 4+ bytes exist here. If the full moonshot-1 report carried verdicts for gaps 5-7 (fold-phase serialization / day-lag / GSTD-Herald-mesh asks), they were NOT verdicted in this pass: not in my bytes, not invented. The three findings above are the complete visible set.

## What the lens missed (additions banked to the structured result)

1. STORM LOCATED: state/fuel/full_scan_ledger.jsonl carries the gap-4 storm as 20599 rows, 0 ok, 20579 fail, 20433 with "429" (first 2026-09-24T03:20:34Z). A zero-yield gate is now a wc+grep away from an existing artifact; the runner law has its data already.
2. SCHEDULER-LAYER BLINDNESS: Estate FullScan Last Result 0 (live) on the storm run. The class extends above batch runners: schtasks Last Result is process exit, never yield. Any runner law should also cover task-scheduler success-on-zero-yield.
3. BUDGET OWNERSHIP: 7200 lives only at mag/context_pack.py:165; tools/thought_quantizer.py has zero max_chars/7200 references. Compile-time gating needs budget threading; the compile is currently budget-blind.
4. SECOND LOSS POINT: FLASH_MAX_CHARS=220 (tools/thought_quantizer.py:118) truncates flash fields before the mechanism byte; the rate-0.5 carrier fix does not touch it. Acceptance should assert BOTH carrier survival and flash-slice law bytes.
5. WORKTREE PRECEDENT: the estate already runs linked worktrees (lsa_reboot_staging on reboot-staging-20261003; worktrees/salon-arena-mvp on codex/salon-arena-mvp, live `git worktree list`). The finding should cite these as in-estate prior art; the open question is alarm-writing organs inside worktrees, not worktrees per se.
6. DATA-PLANE FORK IS THE REAL FALSIFIER: memory/attention.md untracked, state/stash_sweep_watch_state.json untracked, watch/inbox/INDEX.json gitignored (.gitignore:251). A worktree seat's alerts fork. The probe's green condition must first name where alerts land.
7. THIRD REPRODUCTION: memory/context_pack_latest.md re-rendered Oct 7 10:04 (post-lens-anchor), 7277 bytes, 0/0/0 on the three law markers. The render-time loss is now a three-render, two-day class, not a one-off.

## Instruments used (quantifier-law scope statements)

- Storm literal census: `grep -rn` for "20432" and "20578" over memory/, state/, queue/, watch/inbox/, tools/, scripts/, configs/ with includes *.md *.json *.jsonl *.py *.ps1 (binary memory/agent_state/chain.jsonl flagged as matching, not read). Absence claims are scoped to that census.
- Law-marker greps: `grep -c` on memory/context_pack_latest.md (single file, whole file).
- Ledger counts: wc -l + grep -c on state/fuel/full_scan_ledger.jsonl (whole file).
- Tests: only the one named acceptance test was run (`pytest -q tests/test_context_pack_quantized_laws.py::test_quantized_laws_section_renders_in_default_budget`, 1 failed in 8.20s). The d01 41-passed batch was NOT re-run; cited from d01 bytes.
- Not run: llmlingua compression on real L0d carrier bytes (rate-0.5 fit remains hypothesis); the d02 full 285-line re-read (this seat read the file in full once; cross-check against d02's row was by grep).
- External pages fetched this sitting: openpolicyagent.org management-bundles, github.com/microsoft/LLMLingua, docs.litellm.ai/docs/proxy/customers, healthchecks.io/docs/http_api/.
