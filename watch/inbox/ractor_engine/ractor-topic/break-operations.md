# BREAK-OPERATIONS: hostile second pass on the operations lens (ractor-topic)

Pass: break-operations, 2026-10-06 ~20:50-21:15 EDT (2026-10-07T00:50-01:15Z).
Topic: the operations lens report on ractor-topic as handed to me in the ask.
Method: every evidence cite re-checked against the estate by running or reading
it myself this sitting; verdicts below; a check counts only if I ran it here.
No em-dashes. This slot previously held the 2026-10-02 round's pass; this
round's pass replaces it per the topic-slot convention.

## My moment (the tree moved during this pass)

- `git status --porcelain | wc -l` = 142 (the lens read 133; moving tree).
- Fresh census instrument, mine: `.venv/Scripts/python.exe -m pytest --collect-only -q`
  -> "4701 tests collected in 19.22s".
- HEAD 8dd34b388; no commit landed on the cure files during this pass.
- Workflow introspection: ListWorkflowRuns returns workflow_introspection_unavailable
  in my session too (capability gap, same one the morning relay named at
  operations.md:44-45). Not a choice; the surface is unreachable from folds.

## Verdicts

### F1 census carrier drift doubled to +290 - CONFIRMED, strengthened

- logs/census_patrol.log:338 "COLLECT-DRIFT - collected drift: pytest holds
  4648 vs carrier claim 4358 (delta +290, bar 20)" under the [2026-10-06
  08:30:02] START at :320, END exit=1 at :356. The lens's quote dropped the
  words "collected drift:"; every number is byte-exact.
- AGENTS.md:29 still carries "4,358 tests collected / 518 files (2026-10-04
  census" in the exact B2-249 carrier grammar, unrefreshed.
- Strengthened: THREE consecutive daily COLLECT-DRIFT exits 1 with no carrier
  refresh, not two: 10-04 +29 (:264, exit :282), 10-05 +133 (:301, exit :319),
  10-06 +290 (:338, exit :356). The 10-04 patrol ran after that morning's
  09:25Z refresh and still read +29.
- The falsifier (a fresh collect-only reading ~4,358) definitively fails: my
  own run reads 4701 collected in 19.22s, +343 vs carrier. The refresh move
  must name landings through tonight (patrol logs name 12 files grown 10-05 at
  :296 and 29 files grown 10-06 at :333), not just the patrol's 4,648.
- Convergent cite byte-checked: operations.md:95-99 carries "census drift +133
  ... unactioned at dawn" (the 10-05 figure; today's patrol had not fired at
  the 09:21Z fold moment). Move stands as written (~20 min).

### F2 uncommitted cures on a dirty tree beside 3 stashes - WEAKENED

Confirmed core (all mine, this sitting):
- `git diff --stat -- dashboard/server.py state/CURRENT.md
  dashboard/data/ESTATE_INDEX.pointer.json` = "3 files changed, 110
  insertions(+), 114 deletions(-)" (byte-exact); `git diff --cached --stat`
  prints nothing (nothing staged).
- `git status --porcelain -- dashboard/data/ dashboard/server.py
  state/CURRENT.md`: " D dashboard/data/ESTATE_INDEX.jsonl", " M
  dashboard/data/ESTATE_INDEX.pointer.json", " M dashboard/server.py", " M
  state/CURRENT.md", "?? dashboard/data/ESTATE_INDEX.jsonl.retired-20261006".
- git log -- dashboard/server.py: last commit e80f48b8f (2026-10-05); the
  pointer resolver is ADDED lines in the working diff and sits in the working
  tree at dashboard/server.py:193-221 (read), docstring "ouroboros r5 close,
  2026-10-06". Falsifier did not fire.
- The d06 canon refresh is in the working tree, uncommitted:
  state/CURRENT.md:8 reads "updated: 2026-10-06T18:30:00Z". Nuance the lens
  missed: CURRENT.md DID get a commit today (becb53618, R4B); only the latest
  refresh rides dirty.
Killed sub-claim:
- "two of which [the 3 stashes] capture the dashboard/data/ESTATE_INDEX.jsonl
  deletion" is FALSE on my instrument. `git ls-tree -l stash@{0}` /
  `stash@{1}` / `stash@{2}` -- dashboard/data/ESTATE_INDEX.jsonl: all three
  hold the file as MODIFIED BLOBS (2,523,006,985 / 4,150,418,528 /
  2,192,455,453 bytes). Creation stamps (attention.md:684-686: 10-05T23:00:20Z,
  10-05T10:54:22Z, 09-30T19:17:43Z) all predate today's retirement. The
  watcher's "(absent-from-tree, deletion captured)" phrasing at
  attention.md:685-686 describes the TREE side of the tension, not stash
  content. The lens's blind-spot list admitted stash contents were unaudited,
  and the finding asserted them anyway; the unaudited diff refutes the
  assertion. The pop-risk substance survives but inverted (see Addition A1).
- Drift: dirty count 142 at my moment vs 133 claimed.

### F3 stop-cert unloaded, zero retired rows - CONFIRMED (one row-citation corrected), CONVERGENT

- Untruncated census (mine, the QUANTIFIER LAW instrument):
  `.venv/Scripts/python.exe -c` json parse of ALL 131 REGISTRY.jsonl rows ->
  Counter({'<missing>': 111, 'unknown': 15, 'active': 5}). Zero rows carry
  status retired in any value, any spelling. The lens's Select-String variants
  also read 0 on my rerun; raw substring "retired" appears in 20 lines but
  never as a status value.
- CORRECTION: the lens spliced two adjacent rows. The status-unknown
  wide-dig.dwf.ts STATUS-ROW (fire_count 0, latest_registry_row_ts
  2026-10-04T02:33:58Z, digest_matches_latest_row false) is line 130 with ts
  2026-10-06T18:53:21Z; the true last line (131) is ractor-engine.dwf.ts, ts
  2026-10-06T22:29:05Z, verdict PASS, NO status field. The lens grafted line
  131's timestamp onto line 130's payload. Substance unaffected: 15
  status-unknown rows are accruing exactly as claimed.
- Relay cite byte-exact: operations.md:79-85 is the F3 block and quotes
  post_exec_queue.md:92-98 ("armed but unloaded: no registry row carries a
  status field yet"). CONVERGENT per the duplication law (independently
  re-derived from the morning relay). Move stands (~15 min).

### F4 fold instrument renders negative missing as fact - CONFIRMED (two corrections)

- tools/mickey17_v2_fold.py:249 "fired = a.fired or n_files", :254 "missing =
  fired - n_files", rendered raw at :271 "- missing (no file): {missing}" with
  no validation between. `grep -c fold_gate tools/mickey17_v2_fold.py` = 0
  (the lens's full-file claim confirmed on my instrument).
- Tonight's head byte-exact:
  memory/runs/mickey17_v2/runs/dogfood-100m-20261006/FOLD_SECTIONS.md:3-12
  (folded_at 2026-10-06T22:05:09Z, fired: 16, landed: 21, missing: -5). Its
  lanes dir holds 44 entries, 16 *.checks.json (`ls | wc -l`). Note the master
  memory/runs/mickey17_v2/FOLD_SECTIONS.md is a Sep 25 artifact (fired: 9,
  missing: -49), NOT tonight's file.
- No lock event spans the 22:05:09Z fold: workflow-fold.lock.log goes
  release 11:20:49Z -> nothing until 2026-10-07T00:18:37Z. CONFIRMED.
- CORRECTION 1: the lens's "last event 11:20:49Z release" is already stale at
  my read: olm-mine:2026-10-06 acquired 00:18:37Z, released 00:40:10Z,
  re-acquired 00:49:50Z and holds the lock now (log lines 7-9).
- CORRECTION 2: the exculpatory parenthetical "the gate charters the shared
  MASTER path, FOLD_SECTIONS.md is per-run scratch" has no byte support:
  tools/fold_gate.py contains zero references to FOLD_SECTIONS or MASTER on my
  grep of the full file; it is a path-agnostic named-lock service
  (memory/runs/fold_locks/, :34 and :52). Gate compliance is caller convention
  only, and the fold tool never acquires. The defect finding stands; the
  stated reason it is "by-design" does not. Move stands (~20 min), with the
  gate-scoping prose option added.

### F5 five unhealthy organs + gist-scope witness darkness - CONFIRMED (one precision note)

- logs/census_patrol.log:348 "[2026-10-06 08:30:02] TASK-DOCTOR: 5 unhealthy
  task(s) named, alert appended".
- memory/attention.md:655-659: MagBootRegenDaily 2 (10/6 7:15),
  MagGapSentinelDaily 1 (10/6 8:15), MagSecretScanWeekly 1 (10/5 6:40),
  MagTipWitnessDaily 2 (10/5 9:30), MagXRadarDaily 1 (10/6 8:00). Codes match
  the lens exactly.
- The ask's truncated "gist-s..." resolves to gist-scope:
  attention.md:666-671 (2026-10-06 09:30:01) "WITNESS: cannot verify: SCOPE -
  token cannot create gists (HTTP 403) ... (exit 2)", same verdict the day
  before at :608-613. The witness surface has been dark 6+ days per the relay
  (operations.md:27-28: "fired daily since 09-30").
- Other cited blocks byte-check: METER-ALARM WORSENED at :675-683 (14:44:06
  ET, last 7d 121 vs prior 110) and :690-698 (15:16:19 ET, 120 vs 111);
  STASH-SWEEP-WATCH 19:14:11Z at :684-686; tip-witness exit 2 convergent at
  operations.md:95-99.
- Falsifier fails: no gist-scope verification row exists; no scheduled result
  reads 0.
- PRECISION: SecretScanWeekly's 1 is stamped 10/5 6:40 AM (weekly task, did
  not fire today); strictly "returned nonzero today" holds for
  BootRegen/GapSentinel/TipWitness/XRadar, while TASK-DOCTOR named all five
  unhealthy today.

## Blind-spot audit

- "Stash contents unaudited": honest admission, then violated by the finding
  itself (see F2). This is the break of the round.
- "+290 carried from the patrol's instrument, collect-only not rerun": honest;
  I closed it with my own run (4701 in 19.22s, folded into F1).
- "Workflow run introspection not attempted": re-confirmed as a capability
  gap, not a choice: ListWorkflowRuns returns workflow_introspection_unavailable
  in my session too (operations.md:44-45 names the same).
- "Boot-regen result-2 cause unopened; OWED": OPENED by this pass, see A3.

## What the lens missed (additions)

### A1: the stash pop risk is corpse resurrection, not deletion capture
Evidence: git ls-tree -l shows stash@{0}/@{1}/@{2} hold ESTATE_INDEX.jsonl
blobs of 2,523,006,985 / 4,150,418,528 / 2,192,455,453 bytes; stash@{0}'s blob
is EXACTLY the frozen 2,523,006,985-byte corpse the pointer cure retires
(dashboard/server.py:201-202); the tree side holds the deletion (" D" +
ESTATE_INDEX.jsonl.retired-20261006). A pop of any of the three resurrects a
multi-GB stale master over the retired door.
Falsifier: a stash whose tree lacks the ESTATE_INDEX.jsonl blob, or the
watcher's source defining "deletion captured" as a stash-side D entry.
Move: before any sweep, drop or rewrite the ESTATE_INDEX.jsonl entry out of
the three stashes (or bank a never-pop note naming them), ~15 min.

### A2: the fold gate is convention-only, and the lock has already moved on
Evidence: tools/fold_gate.py greps zero for FOLD_SECTIONS and MASTER (it is a
path-agnostic named lock, :34/:52); tools/mickey17_v2_fold.py greps zero for
fold_gate; workflow-fold.lock.log lines 7-9 show olm-mine:2026-10-06
acquiring at 2026-10-07T00:18:37Z and 00:49:50Z (holding now), so concurrent
folds are live again tonight with nothing structural connecting gate to fold
tool.
Falsifier: a fold_gate.py line naming the master path, or a fold tool call
site that acquires the lock.
Move: one gate acquire in tools/mickey17_v2_fold.py before it writes shared
outputs, or one AGENTS.md line scoping which paths require the lock, ~20 min.

### A3: the BootRegen result-2 cause is a zknot timeout, opened this sitting and unactioned
Evidence: logs/boot_regen.log:106-107 "verdict": "step-failure", "reason":
"zknot exited 124: timeout after 300s"; :109 exit=2 wall=300.842s. Per the
response law (attention.md:621), a zknot step-failure is the S1
no-silent-truncation gate keeping the previous LATEST, so the operator-intent
recap is riding yesterday's file and nobody has rerun
scripts/boot_regen_daily.ps1 by hand.
Falsifier: a fresh boot_regen run exiting 0, or a receipt banking the manual
rerun.
Move: rerun powershell -ExecutionPolicy Bypass -File
scripts\boot_regen_daily.ps1 and file the exit, ~10 min.

### A4: MagHermesBurn247 failed once overnight and no finding owns it
Evidence: attention.md:699 "2026-10-06T23:55:27Z MagHermesBurn247 exit 1 -
hermes burn failed, inspect logs/hermes_burn_247.log (two consecutive
failures = both funded accounts hurt; check meter before refire)". One
failure row exists (grep over attention.md), so the consecutive-failure rule
is unmet at bank time, but the funded 24/7 burner's failure is unowned by any
lens finding.
Falsifier: a later row showing a clean refire, or a finding/receipt owning
the failure.
Move: read logs/hermes_burn_247.log tail, refire or annotate, ~10 min.

## Checks I did not run

- No pytest execution (collect-only only, per the falsifier instrument); no
  ratchet, citation-lint, or workflow-gate run (prose pass; the pre-push gates
  own those).
- logs/hermes_burn_247.log tail unread (A4's move, left for the owning seat).
- Browser render of the dashboard door: not attempted (byte-level only, same
  as the lens).
- post_exec_queue.md not read directly; the operations.md:79-85 quote of it is
  what I byte-checked.
