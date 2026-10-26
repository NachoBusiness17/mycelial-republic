# BREAK-DOGFOOD: hostile second pass on the ractor-topic dogfood lens (2026-10-02)

Lens under break: `watch/inbox/ractor_engine/ractor-topic/dogfood.md` (mtime Oct 2 02:03; self-stamped run moment 01:52 EDT at dogfood.md:10).
Pass moment: 2026-10-02 02:23:08 -04:00 (`powershell Get-Date`). All counts are one tree at that moment per B2-216; the fillball lane may still be moving.
The ask's copy of the lens report was truncated mid-F4 evidence; verdicts below were made against the full on-disk dogfood.md (5 findings F1-F5 + OWED section, read whole).
Every check below was run THIS pass by the named command. Anything I did not run is marked NOT RUN. No files were edited (one Mimosa hook refusal on a `sed -n` read of server/server.py pattern-matched as a write; the range was re-read with the Read tool instead).

## Verdicts

### F1 (wiring census 0-for-13, 0-for-3, 12h after commit): WEAKENED

The substance survives and my extended checks strengthen it, but three quantities in the finding are byte-wrong.

Confirmed by reproduction and extension:
- `ls tools/wiring_sweep.py` = No such file or directory. Patrol item 2 (census:229-233) unbuilt.
- `grep -c SIBLINGS githooks/pre-push tools/workflow_gate.py` = 0 and 0; case-insensitive `grep -ci siblings` also 0 and 0. Patrol item 1 (census:217-225) enforced nowhere.
- `grep -n inference_budget` over the 8 carriers (mag/lane_runner.py, mag/tesuji_fire.py, mag/gopher_lite.py, mag/brain.py, mag/janitor.py, mag/daemon.py, mag/research_fanout.py, mag/scale_salon.py) = exit 1, zero hits in all 8 (census row 9, lines 148-167, stands). The census's two wired carriers are honest: `grep -c inference_budget tools/hermes_burn.py tools/model_garden.py` = 1 and 1.
- `grep -n maxsize server/server.py` = exit 1; Read server/server.py:440-446 shows `peer["queue"] = asyncio.Queue()` unbounded at :442 exactly as census row 1 (lines 13-26) filed it.
- Extension (the lens ran none of these): row 2 `grep -c frame_mac server/ws_door.py` = 0; row 3 `grep -n "exclusive\|store_io" tools/workflow_gate.py` = exit 1; row 5 `grep -c nonce mag/events_scan.py` = 0; row 6 `ls mag/fetch_util.py` = No such file and `grep -c "User-Agent" tools/ds_workhorse.py tools/hermes_burn.py tools/model_garden.py` = 0, 0, 0; row 7 `ls tools/standing_task_liveness.py` = No such file; row 10 `grep -c claritas` over the 8 carriers = all 0; row 11 `grep -rln persona_key mag tools server main.py` = mag/persona_key.py only (the mag/.mimosa hook-state hits are scanner artifacts, not callers); row 12 `ls mag/usage_bank.py` = No such file. Row 4 (effect-broker producers) NOT RUN.
- Patrol item 3 also dead, which the lens never checked: `powershell Get-ScheduledTask` filtered on wiring|sweep|caller matches only the unrelated "Estate StealthSweep"; `ls scripts/ | grep -iE "wiring|sweep|caller"` = no matches. Patrol is 0 for 3, fully verified.
- Contrast cites all verified: citation_lint gate at githooks/pre-push:24-25 (grep -n exact); ERRATA strike spans STORY.md:238-242 naming watch/inbox/48h_synth/ERRATA.md; percolator --candidates at mag/percolator.py:23-25, 67-73, 484-485; memory/percolator/candidates.jsonl = 39163 bytes (ls -la); watch/inbox/model_garden/lens1/lens1_results.json exists. "GAP_REGISTER closed six rows" is consistent with bytes: ranks 3, 4, 5 (seat half), 6, 7 landed (rank 7's DIGEST.md, register.jsonl, percolator_candidates.jsonl all in git status) and rank 1 is half-closed (hand smoke END 2026-10-02T00:37:54Z exit=0, scheduled fire pending).

Byte-failures in the finding as stated:
1. Denominator: "0 for 13 on its own one-sitting fixes" overcounts. Census line 213: 13 total rows = 12 disease instances + 1 resolved counter-example (row 13); row 8 (census:142-146) says "No new bytes needed here". Fixable rows = 11 (1-7, 9-12). Honest statement: 0 for 11, of which this pass verified 10 unlanded and 1 (row 4) not run.
2. Timeframe: "twelve hours after commit 0c9d72a06" is wrong on both anchors. `git log -1 --format="%h %ci" 0c9d72a06` = 2026-10-02 00:18:32 -0400, and 0c9d72a06 is the only commit touching the census (`git log --oneline -- watch/inbox/WIRING_DEBT_CENSUS_20261001.md`), so commit-to-lens-run (01:52) is 1h34m; census file mtime is Oct 1 19:09, so landing-to-run is 6h43m. Neither is 12h. The shorter window makes the neglect charge weaker, not stronger.
3. "The census's only external reference is scripts/tmp_land_grid_unique.py:26 and :88" is false as written: `grep -rln WIRING_DEBT_CENSUS` over mag tools server scripts queue memory corpus watch also hits ~19 paid-ask fixtures at memory/plans/garden_battery/capmatrix/bare-q*-r*/ask.json and baref-q*-r*/ask.json (prompt payloads, not wiring surfaces; verified nature via grep -o on bare-q1-r1/ask.json). tmp_land_grid_unique.py:26 and :88 themselves verified, including RECALL-90 = 0 and checks 4/5.
4. Organ-map detail: the lens's grep claim "matched only elder surface history at surface.md:69" missed queue/todo.md:194 ("input wiring" inside a CLOSED 2026-09-29 roblox row). Substance survives (no open wiring-debt row in todo.md); the reported grep output does not. surface.md:69 itself verified ("58 surfaces built, 40 linked").

### F2 (ticket mint unplayed: zero SS-1/CP-1/R2-1 rows in TICKET_LEDGER.md): CONFIRMED

- mag/seed_seal.py:4-5 read directly: "ticket SS-1 = GAP_REGISTER rank 5 (watch/inbox/gap_analysis_20261001/GAP_REGISTER.md)". Verified.
- `grep -n "SS-1\|CP-1\|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md` = exit 1 (zero hits), reproduced at 02:2x EDT; `grep -c "^| "` = 31, matching the lens. Ledger mtime 01:13, i.e. updated before the lens ran and still blind to the three tickets.
- Ledger path verified: `git ls-files "*TICKET_LEDGER*"` = watch/inbox/hermes_burn/TICKET_LEDGER.md only; no copy in watch/inbox/gap_analysis_20261001/ (nothing untracked shows there in git status). The lens's path self-correction is right.
- NIGHT_CLOSE_20261002.md:31-32 (inside the lens's cited 31-33) carries "TICKET_LEDGER row two: issued 65 / run 48 / parked 17 / dropped 0 (73.8 pct". Micro-note: the only NIGHT_CLOSE_20261002.md is at watch/inbox/, not under hermes_burn/ (hermes_burn ls has no such file); the lens's bare filename cite resolves fine but the adjacency to the hermes_burn ledger path could mislead.
- Register side verified: GAP_REGISTER.md:84 (rank 11) names SS-1/CP-1/R2-1 as "none ticketed anywhere", and fill spec 11 (GAP_REGISTER.md:134-138) already writes the exact three rows' content. The docstring's "rank 5" pointer is not drift: fill spec 5 (GAP_REGISTER.md:105-110, "ARM THE SEAL GATES") covers the seed_seal port.
- Falsifier (three rows appear in the ledger) not triggered at my moment.

### F3 (seal organ half-armed: no forge-drill test, no keyfile, never tripped): KILLED

Three of the finding's evidence legs are false on bytes, one by execution:
1. The forge drill exists and passes. tests/test_seal_forge_drill.py does not exist under that exact name (ls = No such file, TRUE leg), but tests/test_seed_seal.py (12610 bytes, mtime Oct 2 00:09, i.e. 1h43m BEFORE the lens's 01:52 run) is the drill: line 1 self-describes "SS-1 forge drill", lines 86-141 are tamper-bytes-plus-full-rehash refusal cases, 144-155 stripped-signature, 183-203 self-consistent key swap, 249-262 the real-seal verify leg. I ran it: `.venv/Scripts/python.exe -m pytest tests/test_seed_seal.py -q -p no:cacheprovider` = "14 passed in 1.03s". The claim "nothing demonstrates rejection of a tampered export" is false by execution.
2. The keyfile exists at the module's own custody path. The lens probed ~/.mag (only steer_seal_seen, TRUE for that directory) but mag/seed_seal.py:56-57 puts KEY_FILE at ROOT/state/keys/seed_seal_key, and `ls -la state/keys/` shows seed_seal_key, 64 bytes, Oct 2 00:07: mint-on-first-use DID trip, before the lens ran. ~/.mag is steer_seal's custody; GAP_REGISTER.md:78 (rank 5 row) is the steer_seal organ. The lens mapped one seal organ onto the other's finding.
3. A real seal was minted: watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal, 748 bytes, Oct 2 00:10 (also in git status as ??), and the drill's real-seal leg verified it in my pytest run.
Residual truth (not the finding as stated): the consume-site enforcement flip is deliberately not landed (mag/seed_seal.py:36-40: nothing refuses an unsealed or forged seed until the operator's gated flip), and there is no --status subcommand (CLI is sign|verify|keyinfo, mag/seed_seal.py:258-291). pam.md exists and carries the spec anchor: watch/inbox/localfirst/pam.md:65 "## The estate port: Ed25519-signed arc-seed export (the seed-seal slot)", which upgrades the lens's OWED on pam.md existence, not its contents in full.

### F4 (wired but not durable: the fresh wiring wave is uncommitted): CONFIRMED

- `git status --short` at my moment reproduces the lens exactly: ?? tools/citation_lint.py, tests/test_citation_lint.py, mag/seed_seal.py, memory/percolator/candidates.jsonl, watch/inbox/model_garden/lens1/lens1_results.json + lens1_samples.jsonl + lens1_stage.jsonl; M githooks/pre-push, mag/percolator.py, watch/inbox/hermes_burn/TICKET_LEDGER.md, lens1_row_zero.py, lens1_run_log.txt.
- Falsifier not triggered: `git log --oneline --all -- tools/citation_lint.py mag/seed_seal.py` = empty (no commit on any ref ever carried them); HEAD is 0c9d72a06.
- NIGHT_CLOSE_20261002.md:73-75 verified: "(seed_seal.py, citation_lint.py, corpus folds, tests) still uncommitted: that lane was mid-flight all shift; committing its work is the morning's call, not a night lane's."
- Positive-half cites verified: pre-push:24-25 gate line; STORY.md:238-242 ERRATA; percolator 23-25/67-73/484-485; STOCHASTIC_LENSING.md:208 "## 6. RESULTS (lens-rz1, landed post-run)" exact.

### F5 (EstateWalkDaily 09:15 fire must not be scored before it happens): CONFIRMED

- Reproduced exactly: `powershell Get-ScheduledTaskInfo EstateWalkDaily` = LastRunTime 10/1/2026 9:15:15 AM, LastTaskResult 1, NextRunTime 10/2/2026 9:15:15 AM.
- `tail -5 logs/estate_walk_daily.log` ends "END 2026-10-02T00:37:54Z exit=0" with window 2026-08-04..2026-10-02: the by-hand smoke run, as the lens said.
- My moment 02:23:08 -04:00 is before 09:15, so the falsifier remains untestable now; scoring it would be fabrication. The lens's discipline here is correct and stands.
- Organ-map claim verified: no EstateWalk row in queue/todo.md (grep found none; the only "wiring" hit is the closed roblox row at todo.md:194).

## Additions (what the lens missed)

1. F3's own falsifier was already satisfied on disk at the lens's run moment: the drill test existed (00:09) under the ticket's name-shaped file (tests/test_seed_seal.py) and passes. The lens ls'd only the filename its own move proposed and never grepped tests/ for seed_seal.
2. The lens audited the wrong custody directory: ~/.mag belongs to steer_seal (GAP_REGISTER rank 5's row); seed_seal's key lives at state/keys/seed_seal_key (mag/seed_seal.py:56-57) and was minted 00:07 with a real .seal at 00:10. Two organs share rank 5's fill spec; the lens mapped one and reported on the other.
3. Census arithmetic: 11 fixable rows, not 13 (census:142-146 row 8 "No new bytes", census:213 row 13 resolved counter-example). With this pass's extensions, 10 of 11 verified unlanded, row 4 not run; patrol 0 for 3 including the scheduled-task absence the lens never checked.
4. The "twelve hours" frame is wrong ~10x (1h34m after commit 0c9d72a06 at 00:18:32; 6h43m after the census's 19:09 mtime). The honest framing is "the same night", which changes the rhetoric of neglect but not the 0-for facts.
5. seed_seal's real open gap is the deliberately-unlanded consume-site enforcement flip (mag/seed_seal.py:36-40) plus a missing --status query subcommand; the 45 minutes the lens budgeted for a duplicate drill test belong there instead.
6. Lens self-receipt checks out on its own laws: grep -c for U+2014 em-dash in dogfood.md = 0, and its census line cites (148-167, 13-26, 217-225, 229-233) all land on the claimed content.

## OWED (this pass, could not or did not verify)

- Census row 4's fix (the ~10 standing effect producers routed through execute()) NOT RUN.
- Row 3's verkle_knot EVOLUTION/LATEST write_text legs not re-checked (only the workflow_gate leg of row 3).
- GAP_REGISTER rank 12 (Vulkan probe) and the KACHE 60-position ledger: not re-checked, inherited OWED from the lens.
- pam.md read only at its section header (line 65); its verify()-with-no-key-returns-True claim not independently re-proven.
- The exact "six rows closed" set in GAP_REGISTER is inferred from landed artifacts (ranks 3, 4, 5 seat-half, 6, 7, plus rank 1 half); the register itself does not carry a per-row status column, so the count is reconstruction, not a register field.

## Command receipt (all run this pass)

ls / grep -c / grep -n / grep -rln / grep -ci over: tools/wiring_sweep.py, githooks/pre-push, tools/workflow_gate.py, the 8 carriers, server/server.py, server/ws_door.py, mag/events_scan.py, mag/fetch_util.py, tools/standing_task_liveness.py, mag/usage_bank.py, tools/ds_workhorse.py, mag/persona_key, state/keys/, watch/arc_seeds/, ~/.mag, tests/test_seal_forge_drill.py, tests/test_seed_seal.py, watch/inbox/hermes_burn/TICKET_LEDGER.md, watch/inbox/gap_analysis_20261001/GAP_REGISTER.md, memory/runs/corpus_gap_research/ARXIV_REGISTER.json, memory/plans/garden_battery/capmatrix/bare-q1-r1/ask.json, scripts/; git status --short, git ls-files, git log (-1, --all, per-file); powershell Get-Date, Get-ScheduledTaskInfo EstateWalkDaily, Get-ScheduledTask; tail logs/estate_walk_daily.log; Read of dogfood.md, WIRING_DEBT_CENSUS_20261001.md, seed_seal.py, test_seed_seal.py, GAP_REGISTER.md, server/server.py:440-446, queue/lanes/elder/surface.md:68-70; and `.venv/Scripts/python.exe -m pytest tests/test_seed_seal.py -q -p no:cacheprovider` = 14 passed in 1.03s. No em-dash bytes in this file.

---

# BREAK-DOGFOOD pass 2 (2026-10-06 evening): the ractor-topic dogfood lens rerun

Seat: break-dogfood (hostile second pass). The ask's copy of the lens was TRUNCATED
(finding 4's move cut off, finding 5 absent entirely): verdicts below were made against
the full on-disk lens at watch/inbox/ractor_engine/ractor-topic/dogfood.md (mtime
Oct 6 20:19, 9,976 bytes, 5 findings + method note + blind spots, read whole). The
same truncation hit the 10-02 pass above. Pass moment: 2026-10-06 late evening EDT.
Branch mag/run-beta1-factory-build-audi-20260806T231709Z, HEAD cb40977b4 (10-06
21:21:15 -0400); sibling lanes landed commits under this pass, so every count is
stamped to my moment. Instruments: git-bash shell, .venv/Scripts/python.exe only; my
one subprocess spawn (the pytest wrap) passed CREATE_NO_WINDOW 0x08000000. The 10-02
pass above is preserved verbatim; this section appends. No em-dash bytes authored
below; the one dash-looking quote is rendered as [U+2014] by codepoint name.

## Verdicts (5 findings)

| lens finding | verdict | reason |
|---|---|---|
| F1 census carrier +343 stale, patrol red unactioned since 10-05 (CONVERGENT) | CONFIRMED | every cite byte-reproduced by my own instruments; falsifier did not fire |
| F2 receipt F3 mis-wired: the em-dash law rides _system_for, the real gap is no output scan | CONFIRMED, strengthened | law byte-present at tools/hermes_burn.py:181, prompt-wired at :326; my scan found A2's banked output carrying 4 real U+2014 bytes, upgrading the receipt-claimed leak to byte-proven; the law has ridden since 10-01 (b2ca54422), not 10-04 |
| F3 premium rung 402, one-key-per-run carrier, first production fire burned its alert | CONFIRMED | code bytes, log fire, attention row, and receipt F1 all byte-match; convergent with the estate's own filed F1 |
| F4 stop-cert armed, zero teeth in production | CONFIRMED, sharpened | full-file registry census: zero retired/superseded status rows; sharpening: zero test files and zero scenario cards exercise the cert either, and its only proof is a commit-message claim |
| F5 publish-time re-derivation law has no instrument, recurred same day (dropped from the ask, restored here) | CONFIRMED, sharpened | law byte-present at state/CURRENT.md:55-56, zero citation_lint wiring in the fold/gate/governor surfaces, recurrence byte-present at DAWN_REPORT:197-199; sharpening: the instrument now exists on disk unwired (tools/publish_recheck.py), so the live gap is the caller, not the tool |

## Cite-by-cite byte-check

### F1 (CONFIRMED)

| lens cite | my byte-check |
|---|---|
| own collect 4701 / EXIT=0 (~20:05 EDT) | MY RUN, same instrument (`pytest --collect-only -q -p no:cacheprovider` via the venv python, CREATE_NO_WINDOW wrap): `4701 tests collected in 21.98s`, EXIT= 0, stderr empty. Same count at my later moment; 4701 - 4358 = +343. |
| AGENTS.md Tests bullet 4,358/518 (2026-10-04 census) | CONFIRMED on disk at AGENTS.md:29. Falsifier probe: `grep -no "2026-10-0[0-9] census" AGENTS.md` returns only `29:2026-10-04 census` and `29:2026-10-03 census`; `grep -c "4,701" AGENTS.md` = 0. |
| logs/census_patrol.log [2026-10-06 08:30:02] drift 4648 vs 4358 (+290, bar 20), END exit=1, ALERT appended | CONFIRMED: log shows START census deep check (--collect), ten grew: lines, `ALERT appended to memory/attention.md`, `END exit=1`, all stamped 2026-10-06 08:30:02. Exact verdict string at memory/attention.md:646 under header `### Census collect patrol fired (2026-10-06 08:30:02)`. |
| operations.md:26 "+133 red has fired daily unactioned since 10-05" | CONFIRMED byte-exact at watch/inbox/ractor_engine/2026-10-06-ouroboros-r5-relay/operations.md:26-27 incl its attention.md:586-591 pointer. |
| attention +133 dated 10-05 | CONFIRMED: attention.md:585 header `(2026-10-05 08:30:01)`, :588 verdict `pytest holds 4491 vs carrier claim 4358 (delta +133, bar 20) (exit 1)`. The alert body carries the refresh instruction (`refresh the AGENTS.md **Tests:** bullet with the real counts and today's date`), executed by nobody. |
| DAWN_REPORT_20261006.md:175 "a red firing with nobody actioning it" | CONFIRMED byte-exact at :175; context is the freshness red, which my own run shows cured. |
| freshness_check PASS EXIT=0 | MY RUN: `FRESHNESS: PASS - boot docs inside the bar.`, FRESHNESS_EXIT=0. Freshness twin cured; census twin not. |
| move detail "the 08:30 alert landed after the 07:33 page" | CONFIRMED: DAWN_REPORT mtime 2026-10-06T07:33:48 local; alert 08:30:02. |
| F1 attribution paragraph (truncated from the ask): tests/ status 7 lines, 6 named untracked + 1 modified | CONFIRMED EXACT at my later moment: `git status --porcelain tests/` = 7 lines; untracked test_freshness_machinery_exclusion, test_gap_gauges, test_publish_recheck, test_stash_sweep_watch, test_ws_mount, test_zknot_meter_alarm; modified test_selfplay_orchestrator.py. |

CONVERGENT flag verified: relay (operations.md:26) + dawn (DAWN_REPORT:175) + patrol
log + attention rows are four independent surfaces, all byte-checked by me.

### F2 (CONFIRMED, strengthened)

| lens cite | my byte-check |
|---|---|
| tools/hermes_burn.py:171-185 law block, :181 "No em-dashes anywhere. Plain hyphens only." | CONFIRMED verbatim at :181 inside `_system_for` (:171-185). |
| :326 builds every prompt from `_system_for(model)` | CONFIRMED: `prompt = (_system_for(model) + "=== CONTRACT ===" ...` at :326-328. |
| scripts/hermes_burn_247.ps1:11-12 routes through the carrier | CONFIRMED: :11 $Py, :12 $Carrier, fire at :22. |
| git last touch 03da1ee56 2026-10-04 11:13:01 -0400, tree clean | CONFIRMED both at my read. |
| OWED: A2 output bytes not found | RESOLVED AGAINST THE LENS: the bank is OUT_DIR = watch/inbox/hermes_burn (tools/hermes_burn.py:65) with out_path = OUT_DIR / f"{meta['id']}.md" (:303). watch/inbox/hermes_burn/H247_A2_TOKEN_CUE_FAMILY_TABLE.md exists: 8,246 bytes (byte-matches receipt :17's "8,246 bytes"), mtime Oct 6 19:55 = the 23:55:08Z usage row. The lens looked in queue/ and usage.jsonl and stopped one directory short of the bank. |
| leak itself receipt-claimed | UPGRADED TO BYTE-PROVEN: my U+2014 scan counts 4 em-dashes in A2 (first context: "Token cue is a measured per-animal harness axis [U+2014] a fixed starting phrase prepended to reasoning asks"); A3 (H247_A3_QUEEN_WELD_MAP_DRAFT.md, 5,438 bytes) counts 0. Same model (haiku-4.5), same law, stochastic compliance: the enforcement gap is the real one. |
| receipt :23 quote + "19:58 tonight" | CONFIRMED byte-exact; receipt mtime 2026-10-06T19:58:33. Also confirmed: A2's ask.json restates the law in its contract (emdash_law_in_ask: True, queue/hermes_247/A2_token_cue_family_table/ask.json), so the law rode BOTH faces and leaked anyway; the receipt's prescribed amendment (append the law line to the system face) is a verified no-op. |
| falsifier "a commit predating 10-04 introducing :181" | FALSIFIER FIRED, STRENGTHENING THE FINDING: `git log -S "No em-dashes anywhere" -- tools/hermes_burn.py` = b2ca54422 2026-10-01 09:43:46 -0400 (THE DESCENT PROTOCOL MADE LAW). The law has ridden since 10-01; receipt F3 is even more wrong than the lens claimed. |
| move precedent commit 28e7bddbf (substance gate) | CONFIRMED real: 2026-10-03 21:33:18 -0400, content_chars + finish_reason banking, fail ok when hollow. |

### F3 (CONFIRMED)

| lens cite | my byte-check |
|---|---|
| tools/hermes_burn.py:83-93 `_hermes_key` loops KEY_2/KEY_1, first found, no 402 retry | CONFIRMED byte-exact (:83-93); :84-85's comment records the 10-01 probe receipt F1 says has aged out. |
| logs/hermes_burn_247.log [2026-10-06T23:54:15Z] FAIL A1 HTTP 402, "FAIL - 2/3 asks", exit 1 | CONFIRMED, instrument note: the log body is UTF-16LE (receipt F4), raw bytes \x00-spaced; decoded: FAIL A1_mira_lane_forecaster RuntimeError "transport failed after 2 tries: HTTPError 402 'Paymen[t Required]'", OK A2 cost=$0.02, OK A3 cost=$0.01, `HERMES-BURN: FAIL - 2/3 asks; ledger total $94.64`, exit 1. The log holds exactly one fire (first ts = last ts = 2026-10-06T23:54:15Z); that logged fire IS the receipt's proof fire (on-disk A2 8,246 / A3 5,438 bytes match receipt :17; usage rows 23:55:08Z / 23:55:27Z). |
| attention.md 2026-10-06T23:55:27Z MagHermesBurn247 exit 1 | CONFIRMED byte-present. |
| F1 at receipt :21 filed and unfixed | CONFIRMED byte-exact incl the cross-key failover amendment clause. CONVERGENT: the estate's own receipt names the defect; the finding is the unactioned part. |

### F4 (CONFIRMED, sharpened)

| lens cite | my byte-check |
|---|---|
| tools/workflow_gate.py:128 STOPCERT_STATUSES = ("retired", "superseded") | CONFIRMED exact. |
| :419 load_stopcert_index | CONFIRMED (:419-445). |
| :448 stop_cert_reason | CONFIRMED (:448-460). The lens did not cite the invocation site: :636-641 mints verdict "BLOCKED-STOPCERT", exit 2. |
| grep -c retired = 0, superseded = 0 in REGISTRY.jsonl | CONFIRMED by a stronger instrument: full-file JSON census of memory/workflows/REGISTRY.jsonl, all 131 lines parsed: status field counts {missing: 111, unknown: 15, active: 5}; loose substring counts: "retired" 20 (all inside status_basis booleans/desc text), "superseded" 0; zero STOPCERT-mention rows. |
| REGISTRY tail STATUS-ROW rows read "status": "unknown" | CONFIRMED (tree-doctrine-dig.dwf.ts and wide-dig.dwf.ts, verdict STATUS-ROW). |
| state/CURRENT.md:47-49 "stop-cert armed but UNLOADED (zero registry status rows minted)" | CONFIRMED; exact phrase at :50 (bullet spans :47-50; one-line drift, immaterial). |
| scenario suite 9/9 green exit 0 | MY RUN: `SCENARIOS: 9 cards validated read-only (no registry row written)`, SUITE_EXIT=0. |
| "the cert has only ever bitten fixtures" | SHARPENED AGAINST THE LENS: there are no stopcert fixtures. `grep -rln "BLOCKED-STOPCERT\|stop_cert" tools/ tests/ configs/ scripts/` hits only tools/workflow_gate.py (+ .pyc); zero test files; the 10 fixtures are fail_g1-g5, g7, g8, pass_control, pass_g8_envelope, soft_g6. The only proof ever taken is commit 4992d4085 (2026-10-05 13:57:16 -0400) claiming "proven end-to-end" - an ephemeral proof leaving no re-runnable artifact. The cert has never bitten anything the repo can reproduce. |
| move (truncated in the ask, recovered from disk): sign the four fleet verdicts, mint the status rows, one real check --script on a named-retired script | Sound; note the cert's blocking path exists and is unwired only because no status rows exist. |

### F5 (CONFIRMED, sharpened) - dropped from the ask, restored from disk

| lens cite | my byte-check |
|---|---|
| state/CURRENT.md:55-56 law text | CONFIRMED exact: "publish-time re-derivation law (R5 communication lens): every fold deliverable re-derives its own citations before publishing". |
| grep re-deriv|rederiv over mag/ tools/ --include=*.py "returned only unrelated comments" (4 named) | PARTIALLY CONFIRMED with a quantifier note (QUANTIFIER LAW): my uncut re-run reads 207 matching lines. All four named cites byte-match (mag/agent_cli.py:2602, mag/aos_agent.py:7, mag/arrival.py:85, mag/bay_organs.py:30). I audited the first 20: all unrelated contexts (claim roots, caches, catalogs, AOS comments). Line-by-line audit of all 207 NOT RUN; no citation instrument in the sample. "Only" hid the set size; the substance (no instrument) held in everything I read. |
| grep citation_lint in tools/fold_gate.py tools/workflow_gate.py mag/governor_autorun.py = zero | CONFIRMED: exit 1, no hits; tools/fold_gate.py exists (real scan). githooks/pre-push:24-25 runs citation_lint check --changed at pre-push only. |
| DAWN_REPORT_20261006.md:197-199 fresh rot | CONFIRMED byte-exact: the next-window-handoff.md:69 cite rotted when the economics append landed above it, the XAI 403 anchor now at line 80 (quoted anchor "XAI 403 console check"). |
| falsifier: a fold-close or publish step invoking citation_lint or any line-anchor re-check | DID NOT FIRE for citation_lint (zero wiring). For "any line-anchor re-check": tools/publish_recheck.py EXISTS on disk (15,714 bytes, mtime Oct 6 16:13 today) with tests (tests/test_publish_recheck.py, untracked, d16) replaying exactly this founding rot, but it has ZERO callers: `grep -rln publish_recheck tools/ mag/ githooks/ --include=*.py` hits the module only. No publish step invokes it. The falsifier's spirit still does not fire; its letter is overtaken by the unwired module (see addition 8). |

## What the lens missed (additions, this pass)

1. A2's output was findable; the OWED was a miss. The bank path is
   watch/inbox/hermes_burn (tools/hermes_burn.py:65,:303), not queue/ or
   usage.jsonl. Evidence: my U+2014 scan - A2 8,049 chars / 4 em-dashes, A3
   5,401 chars / 0; A2 byte size 8,246 matches receipt
   HERMES_247_WIRED_20261006.md:17. Falsifier: OUT_DIR redirected elsewhere or
   stale copies. Move: 5 min - append the byte-scan to the F3 record; A2 is now
   the standing fixture a bank-path scan must catch.
2. The em-dash law predates the lens's "since Oct 4" by three days. Evidence:
   git log -S "No em-dashes anywhere" -- tools/hermes_burn.py = b2ca54422
   2026-10-01 09:43:46 -0400. Falsifier: a pickaxe miss (line introduced under
   different bytes). Move: 2 min - correct the record line in the F3 fold.
3. The stop-cert's only proof is a commit message. Evidence: zero stopcert
   references under tests/ configs/ scripts/ (grep instrument named above),
   10 fixtures all G1-G8, zero status rows (131-line registry census), versus
   4992d4085's "proven end-to-end". Falsifier: a stopcert card or test outside
   tools/tests/configs/scripts. Move: 15 min - add a stopcert scenario card
   (synthetic retired row + fixture script) so the 9/9 suite exercises the
   cert; tonight's green proves G1-G8 only.
4. AGENTS.md carries a second stale count: "seven per-gate scenario cards" vs
   9 cards on disk (G1-G7 plus the two G8-width cards), stale since at least
   4992d4085 (10-05: "scenario suite 9/9 green incl e04's G8-width cards").
   Evidence: my suite run (9 cards) vs the AGENTS.md scenario paragraph.
   Falsifier: a seven-card reading at another moment. Move: 0 extra min - fold
   into F1's AGENTS.md refresh; same organ, same pen.
5. Registry row 75 is the production instance of the zero-teeth gap.
   Evidence: row 75 = tree-doctrine-dig.dwf.ts, digest d2a6783b55be, verdict
   PASS, 2026-10-04T02:34:06Z; state/CURRENT.md:47-48 names tree-doctrine-dig
   for operator fleet retirement; operations.md:28 already waved at it. The
   gate minted a fresh PASS for a to-be-retired workflow because no status row
   could stop it. Falsifier: a status row for tree-doctrine-dig predating that
   PASS. Move: fold into the dawn-close wiring - the operator's
   fleet-retirement pen mints the rows that arm the cert
   (tools/workflow_gate.py:125-127 says exactly this).
6. Both unactioned reds share one root: the operator's unactioned dawn list.
   Evidence: state/CURRENT.md:40-43 (dawn list: census refresh, fleet
   retirement), :47-50 (operator-gated stop-cert unload), DAWN_REPORT mtime
   07:33:48 vs the 08:30 patrol alert. Falsifier: a dawn-close leg already
   carrying the census refresh that still did not run. Move: 10 min - make
   "refresh the AGENTS.md census bullet + mint status rows for the
   retirement-named workflows" explicit dawn-close items.
7. The DAWN:179-184 caveat numbers (lens blind spot) are half stale-by-cure.
   Evidence: my stats - dashboard/data/ESTATE_INDEX.jsonl.retired-20261006 =
   2,523,006,985 bytes (byte-true to DAWN:182); live master
   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl = 363,012,458 bytes now (the caveat's
   dawn-time 346,683,794 B has grown); the pointer
   dashboard/data/ESTATE_INDEX.pointer.json was rewritten 2026-10-06T13:09:25Z
   (AFTER the dawn page's 07:33:48 local = 11:33Z mtime) with renamed fields
   (master_rows/master_bytes vs walk_files/walk_bytes) and no longer carries
   the caveat's 131,284,922,658 B / 1,164,604 rows claim. What the pointer
   said at dawn-read time is NOT RUN-verifiable from current bytes. Falsifier:
   a pointer rewrite predating the dawn page already carrying the renamed
   fields. Move: 0 min beyond a one-line erratum when the pointer-door fix
   lands.
8. F5's cure already exists, unwired. Evidence: tools/publish_recheck.py
   (15,714 bytes, mtime Oct 6 16:13 today) + tests/test_publish_recheck.py
   (untracked, d16, replaying the founding XAI 403 rot on pinned-mtime
   fixtures); `grep -rln publish_recheck` over tools/ mag/ githooks/
   --include=*.py hits the module only; githooks/pre-push:24-25 runs
   citation_lint, never publish_recheck. The lens's F5 greps could not see it
   (they searched re-deriv words and citation_lint refs in three files).
   Falsifier: a caller found under a different name (import alias). Move:
   20 min - wire publish_recheck into the fold banking step / fold_gate
   release instead of building a new instrument; the F5 move shifts from
   "build" to "plug in".

## Limits / NOT RUN (this pass)

- The unbounded BLOCKED-STOPCERT sweep over watch/inbox + memory was killed
  uncompleted twice (filesystem walk exceeded budget). All stopcert absence
  claims here are scoped to tools/ tests/ configs/ scripts/ plus the full
  REGISTRY.jsonl (131 lines, untruncated).
- The em-dash scan covers the two H247 bank files only, not the 3,010-row
  usage history.
- The 207-line re-deriv hit list was sample-audited (first 20), not
  line-by-line.
- Unread, blind spots standing not confirmed: .zcode/workflows/ractor-engine.dwf.ts
  (exists on disk; its REGISTRY row 2026-10-06T22:29:05Z digest d8d63f619ab9
  verdict PASS byte-verified by my registry census), mag/llama_cpp_bridge.py
  contents (still working-tree modified at my read: git status shows M),
  tools/query_broker.py, configs/lanes.yaml, the API-side hermes meter.
- No schtasks fire was run this pass; the win32 CREATE_NO_WINDOW law was
  honored in my own subprocess wrapper only.

## Command receipt (all run this pass)

`.venv/Scripts/python.exe -m pytest --collect-only -q -p no:cacheprovider`
(subprocess wrap, CREATE_NO_WINDOW) = 4701 collected / 21.98s / EXIT 0;
`python tools/freshness_check.py` = PASS EXIT 0; `python
tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` =
9 cards, SUITE_EXIT=0; full-file python census of
memory/workflows/REGISTRY.jsonl (131 lines, JSON status per line); python
U+2014/U+2013 scans of the two watch/inbox/hermes_burn/H247_*.md files;
python reads of logs/hermes_burn_247.log (UTF-16LE decoded), 
memory/attention.md (:584-592, :641-647), logs/census_patrol.log (10-05/10-06
block), dashboard/data/ESTATE_INDEX.pointer.json; git log -n 4 / git log -S
("No em-dashes anywhere", "BLOCKED-STOPCERT") / git status --porcelain
(tools/hermes_burn.py, mag/llama_cpp_bridge.py, tests/); grep -n/-rln/-no/-c
over AGENTS.md, tools/hermes_burn.py, tools/workflow_gate.py,
scripts/hermes_burn_247.ps1, watch/inbox/ractor_engine/ractor-topic/,
tests/ configs/ scripts/ githooks/; Reads of HERMES_247_WIRED_20261006.md,
DAWN_REPORT_20261006.md (:168-192, :193-204),
ractor_engine/2026-10-06-ouroboros-r5-relay/operations.md (:1-45),
state/CURRENT.md (:38-58), queue/hermes_247/A2_token_cue_family_table/ask.json,
tests/test_publish_recheck.py (head), dogfood.md (full lens). Two background
sweeps were stopped uncompleted (watch/inbox filesystem walks); one Write to
this file was hook-refused for an em-dash inside a quoted byte and re-authored
with the codepoint name. No em-dash or en-dash bytes authored in this section.
