# LANE 3 — GATE ENFORCEMENT AUDIT

**Stamp:** 2026-09-26 · **Host:** DESKTOP-7C70KSC · **Repo:** `C:/Users/foste/Documents/projects/local_sovereign_agent`
**Lane question:** is the enforcement between "a gate exists" and "a gate runs" real?
**Machine-readable twin:** `memory/audit_20260926/lane3_gates.json`

---

## Verdict

The gates are not missing. They are **armed, mostly correct, and red while nobody reads them.**

Three findings carry the lane:

1. **The pre-push hook has never fired against a real push.** Both of its enforcing
   gates (`violation_ratchet`, `config_seal`) were already red when the hook was
   wired on 2026-09-25, so every push since has been blocked. The hook is
   fail-closed, and right now fail-closed is indistinguishable from *dead*.
2. **The census gate cited as proof of enforcement is the one instrument the hook
   deliberately does not run.** The hook calls `census_drift_patrol.py` *without*
   `--collect` — so it reads the carrier's own number back to itself and cannot
   see the drift it was built to catch. The stated reason for the omission
   ("needs the venv") is false: the hook's own `.venv` interpreter is what
   invokes it.
3. **Three scheduled tasks have never executed once** — `Last Result: 267011`
   (`0x41303` = `SCHED_S_TASK_HAS_NOT_RUN`). The weekly secret scan is among
   them.

The 1,910-vs-2,288 headline is therefore not a detector failure. The detector was
**right** at 11:34 when it said green. It is a **cadence** failure: the estate
lands ~42 tests/hour and the deep check runs once a day.

---

## A. Enforcement inventory — every gate the repo claims

Nine gates in `githooks/pre-push` (17,853 bytes, git-tracked, `core.hooksPath=githooks`),
plus two scriptable tools and eight scheduled tasks.

| # | Gate | Trigger | Automatic? | Blocks? | Fails closed? | Verdict today |
|---|---|---|---|---|---|---|
| E1 | `violation_ratchet check --changed` (hook:10) | pre-push | **yes** | **YES** | yes | 🔴 **RED** — 6 NEW, exit 1 |
| E2 | `config_seal verify` (hook:12) | pre-push | **yes** | **YES** | yes | 🔴 **RED** — 6 modified + 4 unsealed, exit 1 |
| E3 | `description_pin` (hook:21) | pre-push | yes | no — `\|\| true` | **no** | ⚪ **SKIPPED** — `configs/tools/` absent |
| E4 | `freshness_gate` receipts (hook:41) | pre-push | yes | no — `\|\| true` | **no** | 🟡 WARN-ONLY, 5-receipt cap |
| E5 | `census_drift_patrol` (hook:88) | pre-push | yes | exit 2 only | **partly** | 🟢 **GREEN AND WRONG** — no `--collect` |
| E6 | `checkbox_receipt_gate` (hook:112) | pre-push | yes | no — `\|\| true` | **no** | 🟡 needs 2 files to arm |
| E7 | `caption_ledger_verify` (hook:140) | pre-push, conditional | yes | no — `\|\| true` | **no** | 🟡 WARN-ONLY |
| E8 | `refold_gate` (hook:203) | pre-push, conditional | yes | no — `\|\| true` | **no** | 🟡 WARN-ONLY |
| E9 | `workflow_gate check --scenarios` (hook:280) | pre-push, conditional | yes | **YES** | yes | ⚫ **UNREACHABLE** — arms never fire |
| E10 | `tools/freshness_check.py` | manual only | **NO** | no | n/a | 🟢 PASS |
| E11 | `census_patrol_daily.ps1 --collect` | `MagCensusPatrolDaily` 08:30 | **yes** | no (alerts) | yes | 🟡 fired 11:34, green, now +378 stale |

**Automatic vs. remembered:** 10 of 11 fire without a human. That part is fine.
The failure is downstream — an automatic gate nobody consults is the same as no
gate. E1 and E2 are automatic, red, and have been for the life of the hook; E10
(PASS) only has a reader because this audit ran it.

---

## B. schtasks evidence — verbatim

`powershell.exe -NoProfile -Command "Get-ScheduledTask | Where-Object {$_.TaskName -like '*Mag*'} | Select TaskName,State"`:

```
TaskName                     State
--------                     -----
mag-docker-watchdog          Ready
MagArmC200                   Ready
MagCensusPatrolDaily         Ready
MagCorpusRescanDaily         Ready
MagEndpointNewsDaily         Ready
MagFtsIndexDaily             Ready
MagImproveDaily              Ready
MagLabKit8765                Disabled
MagMimoWatchClose            Ready
MagMimoWatchHourly           Ready
MagPrivateOffice8765         Disabled
MagQCaptionVerifyDaily       Ready
MagSecretScanWeekly          Ready
MagVisionNightly             Ready
ThemesSyncedImageDownload    Ready
```

**The three claimed tasks all exist and are enabled.** But `schtasks /Query /TN <name> /FO LIST /V`
separates *registered* from *fires*:

```
--- MagCensusPatrolDaily ---
Next Run Time:                        9/27/2026 8:30:00 AM
Status:                               Ready
Last Run Time:                        9/26/2026 11:34:24 AM
Last Result:                          0
Task To Run:                          powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\census_patrol_daily.ps1
Scheduled Task State:                 Enabled
Logon Mode:                           Interactive only
Power Management:                     Stop On Battery Mode, No Start On Batteries

--- MagImproveDaily ---
Next Run Time:                        9/27/2026 8:00:00 AM
Status:                               Ready
Last Run Time:                        9/26/2026 8:00:00 AM
Last Result:                          1                      <-- RED, unattended
Task To Run:                          powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...\scripts\improve_daily.ps1
Scheduled Task State:                 Enabled

--- MagFtsIndexDaily ---
Next Run Time:                        9/27/2026 9:00:00 AM
Status:                               Ready
Last Run Time:                        9/26/2026 3:45:14 PM
Last Result:                          0
Task To Run:                          powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...\scripts\fts_index_daily.ps1
Scheduled Task State:                 Enabled
```

### Registered but never executed — the top-tier finding

```
--- MagCorpusRescanDaily ---
Next Run Time:      9/27/2026 3:30:00 AM
Last Run Time:      11/30/1999 12:00:00 AM
Last Result:        267011                     <-- 0x41303 = SCHED_S_TASK_HAS_NOT_RUN

--- MagQCaptionVerifyDaily ---
Next Run Time:      9/27/2026 7:30:00 AM
Last Run Time:      11/30/1999 12:00:00 AM
Last Result:        267011

--- MagSecretScanWeekly ---
Next Run Time:      9/28/2026 6:40:00 AM
Last Run Time:      11/30/1999 12:00:00 AM
Last Result:        267011
```

`11/30/1999` is the Task Scheduler never-ran sentinel. All three were registered
**today** (15:20, 16:23, 16:53) and none has fired. `MagSecretScanWeekly` is the
one that matters most: a weekly secret scanner that has never run is a gate that
does not exist.

**Naming trap:** `scripts/register_ratchet_task.ps1` registers the task as
`Estate Ratchet` (with a space, line 6), **not** a `Mag*` name. A `Mag*` glob
misses it entirely. It exists, is Ready, and its log ends
`[2026-09-26 09:45:03] END seal=1 freshness=0 ratchet=1` — **fired, and red.**

`Logon Mode: Interactive only` on all daily tasks plus `No Start On Batteries`
means every gate here is dark whenever the box is off, asleep, or unplugged, with
no catch-up run. The `Estate *` tasks inherit the same constraint.

---

## C. Do the logs show today's run?

| Task | Log | Today START | Today END | Surface |
|---|---|---|---|---|
| MagCensusPatrolDaily | `logs/census_patrol.log` | 2 | 2 | 🟢 lit |
| MagFtsIndexDaily | `logs/fts_index.log` | 15 | 14 | 🟢 lit (one open) |
| MagImproveDaily | `logs/improve_daily.log` | 1 | 1 | 🟡 lit, **exit 1** |
| MagVisionNightly | `logs/vision_nightly.log` | 2 | 2 | 🟢 lit |
| MagEndpointNewsDaily | `logs/endpoint_news.log` | 1 | 1 | 🟢 lit |
| Estate Ratchet | `logs/ratchet_daily.log` | 1 | 1 | 🟡 lit, **red** |
| MagCorpusRescanDaily | — | — | — | 🔴 **no log file** |
| MagQCaptionVerifyDaily | — | — | — | 🔴 **no log file** |
| MagSecretScanWeekly | — | — | — | 🔴 **no log file** |

### The census log, in full, is the whole case

```
[2026-09-26 11:33:20] CENSUS-PATROL: COLLECT-DRIFT - pytest holds 1910 vs carrier claim 1879 (delta +31, bar 20)
[2026-09-26 11:33:20] ALERT appended to memory/attention.md
[2026-09-26 11:33:20] END exit=1
[2026-09-26 11:34:24] CENSUS-PATROL: OK - census 2026-09-26 (1910 collected / 303 files)
[2026-09-26 11:34:24] CENSUS-PATROL: collect ok - collected claim within bar: pytest 1910 vs carrier 1910 (delta +0, bar 20)
[2026-09-26 11:34:24] END exit=0
```

**The alert append is claimed in the log and absent from the file** —
`grep CENSUS memory/attention.md` returns nothing. A gate that says it alerted
and did not is worse than one that stays silent, because the log reads as
evidence of a working alert path.

**And the green was true when written.** Measured now, both instruments agree:

```
$ .venv/Scripts/python.exe -m pytest --collect-only -q                                    -> 2288 tests collected in 8.44s
$ .venv/Scripts/python.exe -m pytest --collect-only -q -p no:cacheprovider --rootdir .  -> 2288 tests collected in 8.49s
$ .venv/Scripts/python.exe tools/census_drift_patrol.py --collect                         -> COLLECT-DRIFT delta +378, exit 1
```

The gatherer is not broken and the two summaries are identical. Between 11:34 and
now, the estate landed **378 tests in ~9 hours (~42/hour)**. A daily deep check
cannot track that. The gate is not stale-headline-blind; it is **cadence-blind**.

---

## D. The pre-push hook — can it fail open?

**Simulation (real, not reasoned):**

```
$ sh githooks/pre-push < /dev/null
PUSH-GATE: ratchet check --changed
RATCHET check: scope=101 changed files; hits=70; registered=64; NEW=6; expired-exceptions=0
  NEW 5ae40a2d649a9b92 except-pass: tools/ledger_lock.py:125
  NEW 3b1726dec4670996 except-pass: tools/openrouter_free_gate.py:84
  NEW f0d81bd311a1a15e file-too-long: tools/probe20_run.py:421
  NEW e3b7845ea79cf553 cwd-relative-path: tools/queue_dupes_check.py:33
  NEW 0dfc04119a40f245 except-pass: tools/transport_precheck.py:134
  NEW f2ce896c858aa404 except-pass: tools/visor.py:131
RATCHET: FAIL
HOOK EXIT=1
```

**The hook never reached gate 2.** Eight of its nine blocks are unreachable
behind a red gate 1. This answers "which of the 6 NEW ratchet violations would
it block on" — **all six, and it blocks on the first one before reading the rest.**
A 7th NEW violation (`8d41e611 file-too-long tools/census_drift_patrol.py:403`)
is invisible to `--changed` because the file is unchanged; the full check
(`scope=1188 files`) shows **NEW=7**.

### The fail-open surface

The hook is fail-closed on its two enforcing blocks, and deliberately fail-open
on five. Concretely, `|| true` / skipped-arms that swallow a failure:

| Line | Swallow | Effect when the check cannot run |
|---|---|---|
| 21 | `\|\| true` | description_pin never blocks; also skipped entirely when `configs/tools/` is missing (**it is**) |
| 49 | `\|\| true` | every freshness_gate invocation, unbounded |
| 113 | `\|\| true` | checkbox_receipt needs *two* files to arm — rename the queue and it vanishes |
| 157 | `\|\| true` | caption_ledger_verify |
| 225 | `\|\| true` | refold_gate |
| 88–99 | exit 1 → WARN arm | **census STALE cannot block a push** |
| 76–102 | `[ -f AGENTS.md ]` | delete/rename AGENTS.md and the census gate silently skips |

**E5 is the real fail-open, and it is demonstrable.** Its case arm matches only
`"CENSUS-PATROL: ok"*` on the *first line*. A missing or broken interpreter
produces shell noise, `census_rc` becomes **127**, the `if [ "$census_rc" -eq 2 ]`
test is false, and the push proceeds on a gate that never ran. Proven:

```
$ out=$(sh -c '.venv/Scripts/NOPE.exe tools/census_drift_patrol.py 2>&1') || census_rc=$?
census_rc=127
-> WARN arm (push PROCEEDS, no exit)
```

Only `exit 2` blocks. `exit 2` is the *blind* class (cannot-verify). `exit 1` —
the STALE/COLLECT-DRIFT class, which is **exactly the disease in this audit** —
is WARN-ONLY by design, per the `t40` "no lockouts without operator" precedent
that six blocks cite.

### The hook has never run against a real push

```
local HEAD:  6d417abd5dc1afd097000e58a4d3c95ec2ecc6cb
remote:      C:/Users/foste/Documents/projects/Mag-backup.git
backup HEAD: a4733004a 2026-08-06 18:29:43
backup, newest ref on this branch:  2026-09-19 21:53:04
$ git --git-dir=.../Mag-backup.git cat-file -t 6d417abd5...  -> fatal: could not get object info
$ git rev-list --count 6d417abd5... --not --all               -> 0
```

Local HEAD is **not in the backup object store at all.** The hook landed
2026-09-25 (`ea04ebc15` "ratchet wave 2: enforcement — pre-push gate wired");
the backup's newest ref on this branch is **six days older**. Both enforcing
gates were red at hook-landing, so no push could have succeeded since.

The reflog tells the story honestly if you read the newest entry:

```
5c6b1b4a5 HEAD@{2026-09-26 08:05:57}: commit: drift-patrol 2026-09-26: first zero-push morning;
             29 gala drifts healed; link library adopted (8 dupes caught); steady state 0 errors day 8
```

against the older ones claiming *"pushed 26 overnight commits"* (09-25) and
*"pushed 143 overnight commits"* (09-20). The 09-26 entry is the correction.

---

## E. Uncommitted-work exposure

`watch/` is **not** gitignored (`git check-ignore -v watch/` → exit 1), so
`git clean -fd` reaches all of it.

| Category | Count | Notes |
|---|---|---|
| **Untracked total** | **1,686** | ~2,181,953 bytes (≈2.1 MB) |
| `.md` (receipts) | 601 | cards, evidence |
| `.jpg` | 315 | binary assets |
| **`.py` (real code)** | **293** | ⚠️ **the answer to "how much code"** |
| `.json` | 282 | |
| `.txt` | 106 | |
| `.jsonl` (ledgers) | 35 | |
| `.html` | 19 | |
| `.ps1` | 8 | **task registration scripts — 7 of 8 untracked** |

### `.py` at risk = 293, and 100 of them are production surfaces

| Area | Untracked `.py` | Character |
|---|---|---|
| `watch/` | 185 | one-off falsifiers, receipts-as-code |
| **`tests/`** | **58** | **real test code — the census denominator itself** |
| **`tools/`** | **26** | **gate tools, including gates this audit names** |
| **`mag/`** | **12** | **production modules** |
| `scripts/` | 4 | incl. the daily-task drivers |
| `agents/` + other | 8 | |

**293 total, 100 of them in `tests/ tools/ mag/ scripts/`.** The 58 untracked
test files are why the count moved 1,910 → 2,288: **the drift that no gate
reported is itself uncommitted.** The 26 untracked `tools/*.py` include the
gate scripts (`description_pin`, `checkbox_receipt_gate`, and siblings of
`census_collect`) — a `git clean -fd` deletes the enforcement layer, and because
`githooks/pre-push` is git-*tracked* it would survive pointing at tools that no
longer exist, failing open on a missing file.

Also at risk: **7 of 8 `scripts/register_*.ps1` are untracked**, including
`register_census_patrol_task.ps1`, `register_fts_index_task.ps1`,
`register_ratchet_task.ps1`, and `register_improve_task.ps1` — the recipes for
every scheduled gate in section B. A lost disk means the tasks keep running (they
are registered in Windows, not in git) but **cannot be re-registered or audited
from the repo.**

---

## Dormant-but-armed — the requested list

**Never fired once (0x41303):**
1. `MagSecretScanWeekly` — weekly secret scan, fully dormant
2. `MagQCaptionVerifyDaily` — caption ledger, no scheduled verifier
3. `MagCorpusRescanDaily` — corpus rescan, dormant

**Fires, red, nobody reads:**
4. `MagImproveDaily` — exit 1 today at 08:00, unattended, no alert consumer
5. `Estate Ratchet` — 09:45 daily, `END seal=1 freshness=0 ratchet=1`
6. `violation_ratchet` at pre-push (E1) — 6 NEW, blocking all pushes since landing
7. `config_seal verify` (E2) — 6 modified + 4 unsealed, blocking all pushes

**Cannot block by construction:**
8. E3 `description_pin` — disarmed by a missing directory (`configs/tools/`)
9. E4 / E6 / E7 / E8 — `|| true`, WARN-ONLY by design, four `TODO-FLIP-TO-ENFORCE` notes awaiting an operator decision
10. E5 `census_drift_patrol` at pre-push — **structurally blind**: no `--collect`, so it verifies the carrier against itself and prints `ok` on a +378 drift

**Correct but unreachable:**
11. E9 `workflow_gate_scenarios` — enforcing in code, arms never fire because E1/E2 exit first
12. E11 `census_patrol_daily` — the one instrument that *does* catch the drift; daily cadence vs ~42 tests/hour

---

## What I did not verify

- Whether the 09-19 backup ref is the intended push target or a stale mirror;
  `Mag-backup.git` is a local bare repo with 40+ branches, most from 2026-08-06/07.
- `config_seal` intent for each of the 6 modified files — whether they are
  legitimate post-seal edits or unreviewed drift. Names only, per the law.
- `MagImproveDaily`'s exit-1 cause beyond the log: the log is UTF-16 with mojibake
  on the failing lines and the reason did not survive the decode. The START/END
  pair is confirmed, the cause is not.
- Whether `MagMimoWatchClose`/`MagMimoWatchHourly`, `MagArmC200`,
  `mag-docker-watchdog` (all Ready) are gates or unrelated instruments. Only the
  tasks whose actions point into this repo were treated as gates.
