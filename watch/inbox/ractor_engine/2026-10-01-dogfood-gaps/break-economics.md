# break-economics: hostile second pass on the gap-analysis lens report

2026-10-01, ractor engine dogfood (watch/inbox/gap_analysis_20261001/GAP_REGISTER.md is the topic).
Method: every evidence cite in the economics lens report was re-executed against the estate this
session. Nothing below is adopted from the lens without a fresh byte check. Commands run are listed
at the bottom. Anything not executed here is marked NOT RUN / OWED.

## Verdicts

### F1 "Register rank 1 (EstateWalkDaily) already fixed and smoke-passed; no closure mechanism" - CONFIRMED

- GAP_REGISTER.md:74 carries the rank 1 row as the lens quoted (result 1 at 10-01 09:15:15, repeats 10-02 09:15).
- scripts/estate_walk_daily.ps1:5-13: PATH LAW comment (2026-10-01 repair) + absolute `$repo`, `$log`, `$alarm` at lines 11-13. Byte-confirmed.
- logs/estate_walk_daily.log:6: `END 2026-10-02T00:37:54Z exit=0` with full bake lines at :4-5 (window 2026-08-04..2026-10-02). File mtime Oct 1 20:46:30 EDT. Note: the stamp is the run START (ps1:14 sets `$stamp` before the bake), END is appended after the ~9 minute bake, so stamp vs mtime discrepancy resolves; one run, success path.
- GAP_REGISTER.md mtime 2026-10-01 18:41:58 EDT; table header at :72 has no STATUS column (rank/gap/lane/sev/fill cost/owner only); amend clause at :14-15 byte-present.
- Lens underclaim found: the smoke run proved the SUCCESS channel only. memory/attention.md has ZERO `ESTATE-WALK-BAKE-FAILED` lines ever (grep count 0), so the alarm channel has never fired, and fill 1's own demanded receipt beside watch/inbox/48h_synth/ never landed (all six files in that dir have mtime Sep 30, 17:35-18:11 EDT; no ERRATA.md either). Fix is smoke-proved, not failure-proved, not receipted.
- Cross-check the lens never ran: schtasks EstateWalkDaily action is `powershell -NoProfile ... -File ...\estate_walk_daily.ps1` run DIRECTLY, NOT routed through invisible_runner.vbs, Last Result 1 (the pre-fix 10-01 09:15:01 fire), Next Run 10/2 9:15 AM. The 10-02 fire is therefore not hostage to the wrapper bug (see F3). Falsifier (the scheduled fire) is intact and untestable today: OWED to the 10-02 09:15 fire.

### F2 "The register is itself mined-never-scheduled; meta-gap 1 now covers its own author" - CONFIRMED

- queue/todo.md: grep GAP_REGISTER|gap_register = no output, exit 1. Byte-confirmed.
- watch/inbox/INDEX.json: grep -c gap_analysis = 0 and grep -c GAP_REGISTER = 0. Byte-confirmed.
- GAP_REGISTER.md:5-6 (lane-table promise), :44-49 (meta-gap 1 MINED-NEVER-SCHEDULED, dominant class), :247 ("everything else is specced, not done"): all read as cited.
- Timing nuance the lens missed: INDEX.json mtime is 18:00:56, 41 minutes BEFORE the register landed (18:41:58), and queue/todo.md mtime is 2026-09-29 06:53. The zero-consumption claim holds at probe time, but the INDEX leg is a stale-writer artifact, not an active snub; the todo leg is the stronger one (untouched for 2+ days).

### F3 "Coverage 8 of 15 is stale; unmerged a13 carries a live four-task silent kill outranking the table" - CONFIRMED and strengthened

- All four tasks re-queried live with `schtasks /Query /TN <task> /V /FO LIST`:
  - MagFtsIndexDaily: Last Run 10/1/2026 9:00:01 AM, Last Result 1, Next Run 10/2 9:00 AM.
  - MagCensusPatrolDaily: Last Run 10/1/2026 8:30:01 AM, Last Result 1, Next Run 10/2 8:30 AM.
  - MagImproveDaily: Last Run 10/1/2026 8:00:01 AM, Last Result 1.
  - MagLeaveProtocolDaily: Last Run 10/1/2026 8:00:01 AM, Last Result 1.
  - All four Task To Run values route through `wscript.exe ...\scripts\invisible_runner.vbs`. The four-task count is byte-true (the lens named only two plus the improve log).
- scripts/invisible_runner.vbs:27 byte-exact: `rc = shell.Run("cmd /c " & cmd, 0, True)`. Line 22-24 wrap every argument in quotes, so the task action (6 quoted args) hits cmd /c's strip-first-and-last-quote rule. vbs mtime still 2026-09-30 10:59:12: UNFIXED.
- logs/fts_index.log mtime Sep 30 09:00:21, logs/census_patrol.log Sep 30 08:30:28, logs/improve_daily.log Sep 30 08:01:53: all three end at their last pre-wrapper fire. Byte-confirmed.
- Lanes a09-a14 all on disk, mtimes 18:45:43 to 19:30:04 EDT, i.e. AFTER the register's 18:41:58 write. The register's negative finding (:13-15, :237-239 "no late landings appeared") was true at its moment and is stale now; the amend clause (:14-15) applies. Byte-confirmed.
- Probe UPGRADED: the lens admitted it never ran a13's exit-7 probe. I reran it this session: `wscript.exe scripts\invisible_runner.vbs "powershell.exe" -NoProfile -Command "Set-Content ... break_econ_probe.txt ...; exit 7"` returned wscript exit=1, %TEMP%\invisible_runner_rc.log holds `1`, and the probe file was never created. The child never executes. This is now a repro executed in this ask, not a code reading.
- Two nuances the lens dropped:
  1. The "live damage" half of a13's row is already healed out of band: `.venv\Scripts\python.exe tools\corpus_fts_rebuild.py --check --deep` returned exit 0, `index_state: fresh`, `deep: match`, catalog sha bcb60edaff407fa44c2327aeda540ed9746e5f57a812b5b8bbad320a60af9ab5. The SCHEDULER half is still live; the corpus half is not.
  2. a13's own tier-1 check scored its rows 0/5 on quote-entailment (a13-cadence.checks.json:47-51, method line :4 states no repo files were read). The wrapper-kill row survives on the probe plus the schtasks evidence, not on its quote (a13's own quote_note at a13-cadence.json:11 concedes the quote cuts against the claim). A consumer treating .checks.json "no" as a row-killer would discard the register's most valuable unmerged row.

### F4 "Audit banked zero usage rows; 191.8M fails its byte check; next job has no cost baseline" - CONFIRMED and strengthened

- memory/runs/hermes_burn/usage.jsonl: grep -c gap = 0 AND case-insensitive grep -ci gap = 0; tail shows live 10-01 rows with cost_usd (21:52:16Z DUEL2_train_14_r2 $0.0458; 21:53:42Z and 21:53:52Z N1R_parables_songmap $0.1571/$0.149). Byte-confirmed.
- find over memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15 for *usage*/*cost* (case-insensitive): zero files. Byte-confirmed.
- The lens's own flagged alternative is now CLOSED: memory/workflows/REGISTRY.jsonl grep gap-analysis = 0 rows. No cost rows live there either; F4 does not weaken to banked-in-the-wrong-ledger.
- watch/inbox/48h_synth/STORY.md:240 carries "191.8M tokens spent" byte-exact, and its named source watch/inbox/frontier_olm_20260928/DIGEST.md has grep -c 191 = 0 (exit 1). No ERRATA.md in watch/inbox/48h_synth/. Byte-confirmed; fill 4 (GAP_REGISTER.md:101-104) still undone.
- One evidence correction: "no cost numbers (three prose estimates only)" is over-broad. The register does carry $0 tags at :85 (rank 12, "one-sitting ($0)") and :156 ("one afternoon, $0"). What is absent is a per-row token/dollar baseline and any banked usage for the audit itself; the move (route + expected-cost columns) stands.
- Missed by the lens: the token scale itself. a14-coverage.json:48 flags that the "100M tokens" premise undercounts, and watch/inbox/CYCLE_BRIEF_20260930.md:33 carries the byte-exact ledger line: "Tokens (ROUGH): 714,810,462 recorded on 300 fires + 49 unrecorded x mean 2,382,701 = approx 831,562,811 total (cache-inclusive, fire-time attributed)" as of 09-30. The register's "next 100M-token job" framing (:1, :5) rides a scale roughly 8x below the brief's own rough ledger. The baseline hole is bigger than the lens priced.

### F5 "Rank 5 mispriced against ONE-WAVE; rank 12 misranked in its band" - WEAKENED

- Evidence: all byte-true. mag/ holds percolator.py, seed_percolator.py, steer_seal.py and NO seed_seal.py (also canon_seal.py, kv_seal.py, seal.py); find . -name "*.seal" over the repo = zero hits; C:\Users\foste\.mag holds only steer_seal_seen; GAP_REGISTER.md:26 ranking law ("severity x fill-ease, cheapest-cure-first") has no EV term; queue/todo.md:234 is the Stone 7 RX 5600 XT Vulkan line byte-exact.
- Why weakened:
  1. The ONE-WAVE definition is at GAP_REGISTER.md:38, not :37 (:37 is ONE-SITTING). Off-by-one cite.
  2. The register's own internal precedent prices build+test work as ONE-SITTING: fill 3 (:96-100, build tools/citation_lint.py + wire pre-push hook + prove on 12 cites) and fill 6 (:111-115, add --candidates flag + run over two files). Rank 5's seat half (one test file + land mag/seed_seal.py to a spec whose port section spans watch/inbox/localfirst/pam.md:65-103 inside a 134-line file + operator flip priced separately at :78) is consistent with that usage. ONE-WAVE in practice (:145-179) is reserved for cross-window, download, or gated-on-another-fill work.
  3. The rank-12 falsifier inverts in the register's favor: `ollama list` shows qwen2.5:7b (4.7 GB) already on the box, so fill 12's "one 7B Q4 GGUF" (:140-141) needs no download; the $0 tag holds.
- What survives: the register's ranking law (:26) has no EV term, so no rank ordering in the table is EV-derivable from the register's own grammar. That is the real finding, and it is a law gap, not a mispricing proof.

## What the lens missed

1. The wrapper kill's falsifier clock is 10-02 08:00, not 09:15. MagImproveDaily and MagLeaveProtocolDaily fire 08:00, census 08:30, FTS 09:00, all through the unfixed vbs (mtime Sep 30 10:59): four more silent rc=1 fires land BEFORE estate walk's 09:15. Evidence: schtasks Next Run Times this session + vbs mtime. Falsifier: the tasks stop routing through the vbs or the vbs is fixed before 08:00. Move: 30 min tonight: fix vbs line 27 (drop `cmd /c`, shell.Run the command line directly), re-probe exit 7 expecting rc=7, hand-run scripts/fts_index_daily.ps1 to keep the index fresh on the sanctioned path.
2. EstateWalkDaily is wrapper-independent (schtasks action runs powershell directly). The lens's move implies one rank 1 subsumes both kills; there are two independent rank-1-class surfaces. Evidence: schtasks Task To Run fields. Move: 0 min, evidence fact for the amend.
3. Fill 1's own receipt demand is unmet: no bake receipt beside watch/inbox/48h_synth/ (six files, all mtime Sep 30) and zero ESTATE-WALK-BAKE-FAILED lines ever in memory/attention.md. Even the DONE work is unregistered anywhere, which is meta-gap 1 again. Move: fold into the 5-min STATUS edit on GAP_REGISTER.md:74.
4. a13's other rows are register-misses the lens did not surface, two of them re-verified by me this session:
   - Ratchet-daily open debt: logs/ratchet_daily.log:135 (UTF-16LE section, decoded this session) reads `END seal=0 freshness=0 ratchet=1` at 2026-10-01 09:45:02 with `NEW=1` and `NEW 013cbb63c8c4912e except-pass: tools/hermes_burn.py:237` plus four GROWTH claims (estate_bridge 442, concept_predictor 513, duel_harness 461, env_contract 563). grep 013cbb63c8c4912e configs/violation_baseline.json = 0: debt NOT accepted, blocks the next pre-push. Working tree has since moved (git diff +13/-3) and carries a narrow except-pass at tools/hermes_burn.py:393-394; whether the named :237 debt is fixed in the working tree is NOT DETERMINABLE from the reads I made. This row is S1-class under the register's own :29-31 grammar (breaks a live gate at pre-push).
   - Tip-witness dark (PAT 403, exit 2 twice, unacted) and launch-refused night surfaces (0x800710E0) plus KeyAudit orphan GROK_API_KEY: carried in a13-cadence.json:42, :64, :65; I read them, did not re-probe each. Move: amend the register with a cadence band per its own :14-15 clause; one sitting.
5. The register's token scale premise: 831.5M rough cache-inclusive (CYCLE_BRIEF_20260930.md:33, byte-checked) vs the register's 100M framing (:1, :5). Any EV pricing for the next job starts from the wrong denominator until one line in the register header records both numbers. Move: 2-min header edit.
6. The tier-1 instrument itself: a13-cadence.checks.json scored 0/5 (all five rows "supports: no") because its method (:4) is textual entailment of thematic quotes with no repo reads. The quote-entailment "no" is not a row-killer; the engine's steering round should not read .checks.json zero-scores as salvage verdicts on probe-backed rows. Move: none in this pass; flag to the engine owner.
7. Arm C-200 zombie (a14-coverage.json:40,48-49, D12's 72.4 CPU-h): real history, NOT live waste. `tasklist /FI "PID eq 42364"` this session: no tasks match. The register has no row, but a live-waste framing would already be false; byte-check premises before promoting them (a14's own PHANTOM GAPS negative at :47 is the same lesson pointed at the ask).

## Meta-gap answer (dogfood question)

MINED-NEVER-SCHEDULED (GAP_REGISTER.md:44-49) dominates, and it now self-applies three ways: the register is on zero consumption surfaces (F2), its own fill 1 is done-but-unreceipted (addition 3), and its highest-value unmerged input (a13) sits outside the table it was supposed to amend (F3).

## NOT RUN / OWED

- The 10-02 08:00-09:15 scheduled fires: have not happened; unverifiable today. OWED to those fires.
- Injected-failure test of the estate walk alarm channel: not run (would require injecting a failure into a live script; chose not to modify it in this pass). The success-path smoke is the only proof that exists, per F1.
- a10-drops, a11-build-queue, a12-commits: not read in this pass either; the lens's blind spot 1 stands for the next seat.
- a13's KeyAudit orphan and tip-witness rows: read, not re-probed.
- Whether the :237 ratchet debt is fixed in the modified working tree: not determinable from reads; the baseline grep (=0) proves it is not ACCEPTED.

## Commands this pass

ls --full-time (register dir, logs, lanes, INDEX.json, todo.md, 48h_synth, vbs); grep/exit-code checks (todo.md GAP_REGISTER, INDEX.json gap_analysis, usage.jsonl gap x2, REGISTRY.jsonl gap-analysis, attention.md ESTATE-WALK-BAKE-FAILED, DIGEST.md 191, baseline 013cbb63c8c4912e); find (*usage*/*cost* in run dir; *.seal repo-wide); sed (STORY.md 238-242, todo.md 232-236, hermes_burn.py 233-240); schtasks /Query /V /FO LIST x5 (MagFtsIndexDaily, MagCensusPatrolDaily, MagImproveDaily, MagLeaveProtocolDaily, EstateWalkDaily); wscript exit-7 probe through invisible_runner.vbs (rc file 1, probe file absent); .venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep (exit 0, fresh, deep match); ollama list; tasklist PID 42364 (no match); python decode of logs/ratchet_daily.log UTF-16 section.
