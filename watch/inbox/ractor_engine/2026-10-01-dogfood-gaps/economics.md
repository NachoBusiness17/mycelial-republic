# ECONOMICS LENS: GAP_REGISTER dogfood (2026-10-01, late EDT)

Lens: EV-per-cost pricer. Jacket I am sworn to avoid: hoarding or burning
without a banked usage line. Topic: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md
(16,660 bytes, mtime Oct 1 18:41). Method: every load-bearing row re-priced
against on-disk truth this session. All commands were run by me, this session,
in this repo. No em-dashes per law; every claim carries path:line or a command
and its output.

## Re-priced table (register claim vs on-disk truth at probe)

| rank | register says | I checked | verdict |
|---|---|---|---|
| 1 | EstateWalkDaily red, repeats 10-02 09:15 same defect (GAP_REGISTER.md:74) | scripts/estate_walk_daily.ps1:5-13 carries the PATH LAW fix (absolute $repo, log, alarm); logs/estate_walk_daily.log ends "END 2026-10-02T00:37:54Z exit=0" (Oct 1 20:37 EDT smoke run) with a full bake line | FIXED POST-AUDIT, register stale |
| 2 | elder lens unbanked, clock closes ~10-02 (line 75) | queue/lanes/elder/inbox.jsonl: 0 bytes, mtime Sep 4 10:43 | REAL, highest time-decay row |
| 3 | citation_lint absent (line 76) | tools/ holds config_seal.py, md_record_seal.py; no citation_lint.py | REAL |
| 4 | 191.8M phantom (line 77) | grep "191.8" hits watch/inbox/48h_synth/STORY.md:240; grep -c "191" on its named source frontier_olm_20260928/DIGEST.md = 0; no ERRATA.md in watch/inbox/48h_synth/ (dir holds STORY, lattice, laws, measure, next, steals only) | REAL, phantom live in a consumed record |
| 5 | seal gates unarmed (line 78) | ls mag: percolator.py, seed_percolator.py, steer_seal.py, no seed_seal.py; find . -name "*.seal" = 0 sidecars; C:\Users\foste\.mag holds only steer_seal_seen | REAL but mispriced (F5) |
| 6 | percolator --candidates absent (line 79) | grep -c "percolate" mag/percolator.py = 9, grep -c "candidates" = 0 (no-match against a greppable file) | REAL |
| 7 | day-1 fold missing (line 80) | watch/inbox/frontier_olm_2026-09-30 holds only lens/, steal/, sweep/ subdirs, no DIGEST | REAL |
| 8 | day-2 outputs unindexed (line 81) | INDEX.json: 38 hits for frontier_olm_2026-10-01 but 0 for "2026-10-01/DIGEST", 0 for "2026-10-01/RECEIPT", 0 for "2026-10-01/quantization-compression" | REAL |
| 9 | KVarN line missing (line 82) | ARXIV_REGISTER.json exists (233,406 bytes, mtime Sep 29 05:59); grep "2606.03458\|KVarN" = no match | REAL |
| 11 | zero tickets minted (line 84) | grep -c "SS-1\|CP-1\|R2-1" on watch/inbox/hermes_burn/TICKET_LEDGER.md = 0 | REAL |
| 12 | Move 1 unfired (line 85) | watch/inbox/spiking_wide/ holds the 8 original files, no Vulkan receipt | REAL, $0, this box (queue/todo.md:234 proves the RX 5600 XT Vulkan path, GPU 53% sampled) |

Dogfood score: 10 of 11 non-rank-1 rows still real, rank 1 already fixed.
The register's row-level accuracy is high. Its failures are all above the
row level: closure, coverage, cost, and its own consumption surface.

## Findings

### F1: Rank 1 is fixed and smoke-passed; the register has no closure mechanism, so its top S1 is now a false positive
Evidence: GAP_REGISTER.md:74 prices rank 1 as an open S1 repeating 10-02
09:15. scripts/estate_walk_daily.ps1:5-13 hardcodes $repo and absolute
log/alarm paths under a PATH LAW comment naming this exact defect.
logs/estate_walk_daily.log contains "END 2026-10-02T00:37:54Z exit=0"
(Oct 1 20:37:54 EDT) plus a baked-tapestry line. The fix lives in the commit
message (5d2263f10) and the script, never in the register; the register has
no STATUS column and its only amendment clause (lines 14-15) covers late
lanes, not completed fills. Every future reader re-buys the estate's top S1.
Falsifier: the 10-02 09:15 scheduled fire returns LastTaskResult != 0, or the
attention.md alarm channel fails an injected-failure test (the fix is
smoke-proved, not schedule-proved; I could not verify a fire that has not
happened yet).
Move: 5-minute edit. Strike rank 1 or add a STATUS column: "FIXED 10-01,
evidence logs/estate_walk_daily.log END 2026-10-02T00:37:54Z exit=0;
re-verify after the 10-02 09:15 fire."

### F2: The register is itself mined-never-scheduled: the dominant meta-gap class includes its own author
Evidence: GAP_REGISTER.md:5-6 promises the file "tells that job what to fire,
in what order, at what cost, and who owns it." Nothing consumes it:
grep "GAP_REGISTER" on queue/todo.md = no output; grep -c "gap_analysis" on
watch/inbox/INDEX.json = 0. The register's own meta-gap 1 (lines 44-49,
"MINED-NEVER-SCHEDULED (dominant class)") is therefore freshly instantiated
by the register: banked at 18:41, on zero execution surfaces. Line 247
volunteers "Nothing in this register is a fill claim": true, and nothing
schedules the fills either.
Falsifier: a todo.md line or INDEX.json row naming GAP_REGISTER.md or the
gap_analysis_20261001 window.
Move: 10 minutes. One todo.md line binding the next window to the register's
fill order, plus registration through the sanctioned shared-surface writer.

### F3: Coverage is 8 of 15, and the unmerged a13 lane carries a live four-task silent kill that outranks every row in the table
Evidence: GAP_REGISTER.md:13-15 and :237 claim lanes a09-a14 produced no
files at the ~18:30Z poll. The lanes dir now holds 32 files including
a09-balls (18:49), a10-drops (18:53), a11-build-queue (18:45), a12-commits
(18:54), a13-cadence (19:30), a14-coverage (18:48), all Oct 1. The register
froze at 18:41, minutes before the harvest. a13-cadence.json documents
invisible_runner.vbs never launching its child; I reproduced the damage live:
schtasks MagFtsIndexDaily: Last Run Time 10/1/2026 9:00:01 AM, Last Result 1,
Task To Run = wscript.exe ...invisible_runner.vbs "powershell.exe" ...
-File ...fts_index_daily.ps1; schtasks MagCensusPatrolDaily: Last Result 1
at 8:30:01 AM. logs/fts_index.log, logs/census_patrol.log and
logs/improve_daily.log all end at their Sep 30 morning runs: zero Oct 1
lines. Root cause readable in the code: scripts/invisible_runner.vbs:27
builds shell.Run("cmd /c " & quoted-command), the classic cmd /c
quote-strip that turns the line into garbage, rc 1, stderr swallowed by the
hidden window. Four enforcement gates (improve 08:00, census patrol 08:30,
FTS index 09:00, leave protocol 08:00) are dark while the register's rank 1
(one dead task, since fixed) took the table's top slot. Note the surface
half-life: a13's "FTS index is STALE right now" was true at 19:30Z and false
at my probe; I ran tools/corpus_fts_rebuild.py --check --deep myself and it
returned index_state fresh, RC=0, on a new catalog sha (bcb60eda...), so a
seat healed the index out-of-band while the scheduled gate stayed dead.
Falsifier: task actions provably not routed through the vbs, or an Oct 1
log line in any of the three logs from another writer.
Move: one sitting. Amend the register per its own clause (lines 14-15) with
the six lanes, insert wrapper-kill at rank 1, and fix vbs line 27 (drop the
cmd /c prefix, Run the powershell.exe path directly, window style 0), proved
with a13's own exit-7 Set-Content probe before re-arming.

### F4: Zero usage banking on the audit that produced the register, and no cost numbers in it: the next 100M job has no cost baseline
Evidence: GAP_REGISTER.md:6 promises "at what cost". The table prices fills
only as classes; exactly three prose estimates exist ("Cost: minutes" line
92, "a 20-minute write" line 96, "15 minutes" line 104). The producing run
banked nothing: grep -c "gap" on memory/runs/hermes_burn/usage.jsonl = 0, and
find over memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15
for *usage* or *cost* files = 0 hits, against DESCENT leg 8 (AGENTS.md: every
turn banks tokens+cost to memory/runs/hermes_burn/usage.jsonl; the ledger is
otherwise alive, its tail shows 10-01 rows with cost_usd). The one hard cost
number in the chain, STORY.md:240's "191.8M tokens spent", fails its byte
check against its named source (0 "191" hits in frontier_olm_20260928/DIGEST.md,
re-grepped by me), so the estate cannot compute EV-per-token for the next
job: no denominator from the last job, and the numerator on offer is a phantom.
Falsifier: a usage.jsonl row whose id names the gap-analysis run, or a cost
file inside the run dir.
Move: 15 minutes. Add route (free-lane vs funded tier, per the driving
ladder) and expected-cost columns to the 12 fill rows, and bind the register
header to leg-8 banking so the next job's spend is countable.

### F5: Rank 5 is mispriced against the register's own cost grammar; rank 12 is EV-misordered inside its band
Evidence: rank 5 (GAP_REGISTER.md:78) is priced "one-sitting + operator flip"
but its seat half is a full Ed25519 port to the pam.md spec plus a
forge-drill test, which meets the register's own ONE-WAVE definition
(line 37: "multi-step, needs a build+test cycle"). Verified open: no
mag/seed_seal.py (ls mag shows percolator.py, seed_percolator.py,
steer_seal.py only), zero .seal sidecars repo-wide (find | wc -l = 0),
C:\Users\foste\.mag holds only steer_seal_seen. Under-pricing invites the
next job to schedule it as one sitting and silently partial-fill. Meanwhile
rank 12 is the only $0 row and the only one yielding new physical-world data
(Vulkan tok/s at 8k on the proven RX 5600 XT path, queue/todo.md:234, this
box), yet it sits last in the S2 band behind same-cost bookkeeping rows 7
and 8; the ranking law (line 26: "severity x fill-ease, cheapest-cure-first
inside a severity band") has no EV term to break cost ties.
Falsifier: the pam.md port spec is small enough that port plus test provably
fits one sitting, or the Vulkan probe needs a download that voids the $0 tag.
Move: 10-minute register edit: reprice rank 5 to ONE-WAVE, pull rank 12 to
the head of the S2 band.

## Which meta-gap class dominates

MINED-NEVER-SCHEDULED, and it got worse after the register froze. Fresh
instances the register could not see: the six unmerged lanes (mined 18:45 to
19:30, never folded), a13's wrapper-kill (mined, while its four gates stayed
dead through the evening), and the register itself (F2). The next 100M-token
job is a schedule-and-fire pass, exactly as the register says; the register
is currently the first thing that job must schedule.

## What the register itself missed

1. A closure mechanism (F1): fixes land in commits and scripts, never in the
   register, so rank truth decays hourly.
2. Its own consumption surface (F2).
3. The last 45 minutes of its own burst (F3): six lanes, one carrying a live
   S1 four-gate kill.
4. Cost physics (F4): zero banked usage, no route column, one phantom number.
5. EV tie-breaking inside bands (F5).

## Blind spots (honest)

- I read heads of a09, a13 and a14 only; a10-a12 are unexamined. The unmerged
  set may carry more live defects, or rows already fixed elsewhere.
- The rank-1 fix is smoke-proved only. The 10-02 09:15 scheduled fire and the
  alarm channel under injected failure are unverified by anyone so far.
- I did not run the a13 exit-7 probe or test any vbs fix; the cmd /c
  quote-strip root cause is a code reading corroborated by task evidence,
  not a repro I executed.
- I priced the next job's cost baseline as absent without opening
  memory/workflows/REGISTRY.jsonl to hunt for token rows; if rows live there,
  F4 weakens to "banked in the wrong ledger".
- FTS freshness flipped under me mid-session (stale at 19:30Z per a13, fresh
  at my probe via an out-of-band heal). Other lane claims may have similar
  half-lives I measured once.
