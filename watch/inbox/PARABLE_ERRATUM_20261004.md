# PARABLE ERRATUM - day one arena receipt, corrected against the meters (2026-10-04)

Filed by lane 6 (arena-cadence) of the GO wave, per corpus/steal/MASTER_MICKEY17_V2.md
section 9 GO item 6 (lane citations a01#0, a01#1, a01#5, a01#6, a01#7). This is a
NEW file by lane ownership: the parable itself (watch/inbox/parable_day_one_20261003.md)
is left byte-untouched. Every number below carries the command that produced it.
Filing moment: 2026-10-04T08:48:53Z. The arena tree is still moving (see the census
at the end); every count here is stamped to its read.

## 1. The cap is $25, not "$25.11"

The parable's meter verse (line 13) says "the $25.11 cap". The cap is $25; $25.11
was a meter reading misnamed as the cap.

Byte evidence (the automation's own fields, read 2026-10-04T08:2xZ via
`.venv\Scripts\python.exe` + sqlite3 over `C:/Users/foste/.zcode/v2/tasks-index.sqlite`,
automations row automation-b1ce1342-e449-4b33-b041-f8fbf4f69b0c):
- title: `Hourly arena cycle: dungeon + tavern + gwap bank, $25 daily cap`
- prompt step 1: `If today already exceeds $25, stop and report one line`

The $25.11 figure is the day-03 cumulative meter crossing $25 at 19:33:24Z:
recomputed with `.venv\Scripts\python.exe` summing cost_usd over the 2026-10-03 rows
of memory/runs/hermes_burn/usage.jsonl in ts order:
- crossing row: `{"ts": "2026-10-03T19:33:24.686865Z", "id": "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B", "model": "z-ai/glm-5.3-prime", ...}`
- cumulative at that row: $25.1134 (i.e. the "$25.11")

So the cap held nothing on day 03; the day CLOSED OVER CAP (see section 4).

## 2. The real ledgers and the filing-moment counts (line 12 and line 10)

The parable cites "the arena-sessions-v3 ledger (266 rows, chain ok)". No ledger of
that name exists: `git grep -rn "arena-sessions-v3" -- "*.py"` returns zero code hits;
the string appears only in the parable itself and in two later documents quoting it
(grep count in the parable: exactly 1). The real artifacts:

- memory/runs/gwap/arena-capability.jsonl - THE capability ledger the parable meant.
  Counts by moment: 314 rows at the a01 audit reads (~21:41Z and again ~03:3xZ
  2026-10-04 per the lane file); 459 rows / 326 distinct scene_ids at my 08:30:46Z
  read; 476 rows / 343 distinct scene_ids at the 08:48:53Z filing moment (the tree
  moves hourly). Chain (SessionLedger prev_sha256 linkage) verified ok by
  tools/arena_gwap.py during this wave's fire (`CHAIN ok=True bad=None`, 2026-10-04T08:41-08:42Z).
- memory/runs/gwap/arena-sessions.jsonl - its own named artifact: 60 rows, frozen,
  first ts 2026-10-03T12:51:31Z, last ts 2026-10-03T12:52:58Z (the day-one bar fight).

The parable's two figures are two stale moments of ONE counter, not day totals:
recomputed from arena-capability.jsonl hour buckets with `.venv\Scripts\python.exe`:
- hour-13 bucket (2026-10-03T13): 121 rows -> "121 chain-verified agreement rows from
  23 play sessions" (line 10) is the hour-13 bank snapshot.
- through hour-14 (13+14 buckets): 266 rows exactly -> "266 rows" (line 12) is the
  post-hour-14 moment (121+145).
Both are superseded by the counts above; quote them only with those moments.

## 3. The failed 13:00Z fire (line 9)

The parable's cadence verse says "the hourly arena cron, 8 cycles". Byte-true as the
fire count at its filing, but it hides the failure: the FIRST fire failed. Census via
sqlite3 over automation_runs for automation-b1ce1342 (read 2026-10-04T08:2xZ):
- 20 rows scheduled 2026-10-03T13:00:00Z through 2026-10-04T08:00:00Z
- outcomes: exactly 1 `failed` = the 2026-10-03T13:00:00Z first fire; 19 succeeded

## 4. The $0.62 over-cap close

Recomputed with `.venv\Scripts\python.exe` over usage.jsonl 2026-10-03 rows:
- day-03 total: 1034 rows, $25.6218
- over the $25 cap by: $0.6218 (the "$0.62 over-cap close")
The cap gate finally bit only at the 21:00Z fire (succeeded with zero session
activity) - after the 20:00Z fire had already run three dungeon sessions at
20:21-20:23Z post-crossing (a01#1, a01#7).

## 5. "held to 35 cents" is unbacked

No byte-exact ledger slice sums to $0.35. Nearest named slices (recomputed
2026-10-04T08:4xZ, `.venv\Scripts\python.exe` over usage.jsonl 2026-10-03 rows by id prefix):
- DND0 cron-hours 13:00-20:59Z: $0.3272 / 192 calls
- SEASON (1 row): $0.3897
- DND0 day-03 all: $0.7903 / 316 calls
- TAVERN day-03 all: $16.2003 / 665 calls
If the verse means the dungeon line, say "33 cents, DND0 cron-hours". Until the
operator names the intended slice, treat "35 cents" as unbacked (a01 negative finding).

## 6. Census at the filing moment (moving-tree stamp)

2026-10-04T08:48:53Z: arena-capability.jsonl 476 rows / 343 distinct scenes;
watch/inbox/playground 73 session dirs, 66 GWAP_BANKED, 7 unbanked (the hourly fires
keep minting; the bank now runs inside each carrier at exit per GO item 6, so fresh
dirs bank same-second - the 7 are pre-fix dirs from fires that fired before the fix).
Instrument: `.venv\Scripts\python.exe tools/arena_gwap.py --status` prints this line
with a per-dir banked_at column; tools/cycle_brief.py now carries it as the dawn
report's ARENA GWAP section (watch/inbox/CYCLE_BRIEF_20261004.md, lines 52-62).

## 7. GAP_REGISTER R1 addendum: "$25.11" IS the 20:00Z reading; the automation row is deleted (2026-10-10)

Filed by lane a01-arena-cadence-r1 of the owed waltz (watch/inbox/
gap_analysis_20261010/GAP_REGISTER.md row R1), one sitting, filing moment
2026-10-10T13:11Z. Every number below was produced by `.venv\Scripts\python.exe`
runs in this sitting (raw output banked beside the lane file as
a01-arena-cadence-r1.check.txt).

1. The 20:00Z identity, completing section 1 in R1's own words. Section 1 grounded
   $25.1134 at the 19:33:24.686865Z crossing row; R1 words the figure "the 20:00Z
   meter reading". Both are the same number: recomputed over the 2026-10-03 rows of
   memory/runs/hermes_burn/usage.jsonl in ts order (1034 rows, day total $25.6218),
   the crossing row (GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B,
   2026-10-03T19:33:24.686865Z, cumulative $25.1134) is also the LAST row before
   20:00Z, and the cumulative through the last pre-20:00Z row is $25.1134: zero
   rows fall between the crossing and the 20:00Z fire. So the parable's "$25.11
   cap" (parable line 13) names the 20:00Z meter reading; the cap is $25.

2. R1's prompt amendment is impossible as written: the automations row is DELETED.
   Read this sitting via sqlite3 over C:/Users/foste/.zcode/v2/tasks-index.sqlite:
   the automations table holds 18 rows, ZERO matching automation_id LIKE
   '%b1ce1342%'. Only the runs survive: automation_runs holds 43 rows for
   automation-b1ce1342-e449-4b33-b041-f8fbf4f69b0c, first scheduled
   2026-10-03T13:00:00Z outcome failed (section 3's first fire), 42 succeeded, last
   scheduled 2026-10-05T07:00:00Z; the unreceipted ~2026-10-05 deletion is already
   on record (corpus/steal/MASTER_MICKEY17_V2.md:228). There is no live prompt to
   amend, so the gate the amended step 1 was to carry is banked HERE, for any
   re-created arena cron to load: gate on the arena-family ids only (TAVERN / DND0
   / CAMP), summing cost_usd over the day's rows whose id carries that family
   prefix against the $25 cap, NOT the whole-account whole-day sum. Why it matters,
   this sitting's day-03 recompute by id family: the whole-day sum crossed $25 at
   19:33:24Z on a GALA_DD id (not an arena-family id) while the arena family closed
   the day at $17.2119 (TAVERN $16.2003 + DND0 $0.7903 + CAMP $0.2213) of the
   $25.6218 whole-account total: the old gate stopped arena play for the whole
   account's spend.

## 8. GAP_REGISTER R2 fill: the cadence census as failure rows, folded into the dawn feed (2026-10-10)

Filed by lane a01-arena-cadence-r2 of the owed waltz (GAP_REGISTER row R2),
filing moment 2026-10-10T13:2xZ. Section 3 carried counts ("20 rows scheduled
... exactly 1 failed"); R2 ordered the census itself folded into the receipts
because a count can hide a failure and a row cannot. Fresh read this sitting
via `.venv\Scripts\python.exe` + sqlite3 (mode=ro) over
C:/Users/foste/.zcode/v2/tasks-index.sqlite table automation_runs,
automation_id automation-b1ce1342-e449-4b33-b041-f8fbf4f69b0c (the 43-row
totals and the automations-row deletion are already section 7's; this
section adds the rows and the arithmetic):

- the one failed fire, as its own row (err=None is the table's own value: the
  failure reason is not recorded):
  `FAIL sched=2026-10-03T13:00:00Z outcome=failed run=automation-b1ce1342-e449-4b33-b041-f8fbf4f69b0c:1791032400000 err=None`
- the 43 rows are the full hourly span with ZERO gaps (11 fires 10-03
  13:00-23:00Z, 24 fires 10-04, 8 fires 10-05 00:00-07:00Z), so every earlier
  read is a clean prefix of one sequence: 9 rows at the 2026-10-03T21:55Z
  read (13:00-21:00Z; the parable's "8 cycles" = 8 of those 9 had fired at
  its ~20:36Z filing), 15 rows at the 03:3xZ read (through 03:00Z 10-04),
  20 rows at section 3's 08:2xZ read (through 08:00Z 10-04).
- the behaviors R2 says the count hid, byte-checked again this sitting over
  the 2026-10-03 rows of memory/runs/hermes_burn/usage.jsonl in ts order plus
  the playground tree:
  - the 20:00Z fire ran three dungeon sessions AFTER the $25 crossing
    (19:33:24.686865Z, cumulative $25.1134, section 1/7's crossing row):
    watch/inbox/playground/dnd0_20261003T202147Z, T202158Z, T202213Z all
    exist on disk; DND0 hour-20 calls = 48 ($0.0187).
  - the 21:00Z fire: succeeded with zero session activity - DND0 hour-21
    calls = 0 and no playground dir stamped 21xx on 10-03 - consistent with
    the cap gate finally stopping play; the gate reads at fire start, so the
    stop lands one fire late (R7's structural lag).

The census now rides the dawn feed itself: tools/arena_gwap.py --status
prints the ARENA CADENCE block (counts + span + every non-succeeded fire as
its own FAIL row; HONEST-GAP if the index is unreadable), and
tools/cycle_brief.py section_arena_gwap() carries those lines into the
CYCLE_BRIEF dawn report. Verified live 2026-10-10T13:16-13:18Z (raw output
banked beside the lane file as a01-arena-cadence-r2.check.txt): both the
--status output and the compiled section print the FAIL row above verbatim.

## 9. GAP_REGISTER R7 fill: day-04, the cap's second and last full day, closed over too (2026-10-10)

Filed by lane a01-arena-cadence-r7 of the owed waltz (GAP_REGISTER row R7), filing
moment 2026-10-10T13:28Z. Sections 1-6 covered day one and the day-04 morning filing
moment; sections 7-8 banked the automation-row deletion and the 43-run census. This
section closes the erratum over the cadence's FULL life: the day-04 close, the gate's
only true stops, and the fact that deletion, not the gate, ended the overspend. Every
number below was recomputed this sitting over memory/runs/hermes_burn/usage.jsonl
(3038 rows, first 2026-10-01T13:11:41Z, last 2026-10-07T09:21:35Z) with
`.venv\Scripts\python.exe`, cross-read against automation_runs (sqlite mode=ro over
C:/Users/foste/.zcode/v2/tasks-index.sqlite) and the fire exec logs under
C:/Users/foste/.zcode/cli/exec/sess_6334e346-5708-47bb-b8e5-3ca5b56e3701/
(raw output banked beside the lane file as a01-arena-cadence-r7.check.txt).

### 9.1 Day-04 closed $26.2921, over the cap by $1.2921

Day-04 sums to $26.2921 over 1448 rows: arena-family $23.6157 (TAVERN $22.2574 /
950 rows, dnd0 $1.1411 / 470, DND0 $0.2172 / 23) plus non-arena $2.6764 (THE
$0.7226, SEASON $0.6299, REPRINT $0.4961, COMPOSED $0.4145, PRIMER $0.4133).
Second over-cap close in two days (day-03 $25.6218, section 4). Even the arena
family alone came within $1.38 of the cap; the whole-account day crossed it.

### 9.2 The crossing landed mid-fire of the 22:00Z fire, $0.51 headroom at start

The whole-account day-04 cumulative crossed $25 INSIDE the 22:00Z fire, not at a
fire boundary:
- crossing row: 2026-10-04T22:06:53.865221Z, id TAVERN_tavern_20261004T220358Z_r4_
  Pell Quickfinger, cost $0.0741, cumulative $25.0074 (tavern round 4)
- the fire's first session row: 22:02:31Z (dnd0_20261004T220223Z_S0_dm); at fire
  start the day read $24.4905, headroom $0.5095 ($0.51)
- the fire kept minting past the crossing to 22:07:21Z (TAVERN r4_JUDGE, last
  arena row of the day)

Gate step 1 (section 1) reads "If today already exceeds $25, stop": $24.4905 does
not exceed $25, so the gate passed the 22:00Z fire and the crossing happened inside
it. The lag-by-one-fire is structural to that check (already named in section 8's
21:00Z stop): the gate reads at fire start, the crossing happens during the fire,
so the first fire the gate can stop is the NEXT one.

### 9.3 The dark afternoon: four scaffold-only succeeded fires 18:00-21:00Z

Zero account rows carry cost between 17:11:14Z (the 17:00Z fire's last tavern row,
TAVERN_tavern_20261004T170532Z_r7) and 22:02:31Z (the 22:00Z fire's first row):
cumulative before 18:02Z = $24.4905 and before 22:00Z = $24.4905, byte-identical.
The four fires between (18:00Z, 19:00Z, 20:00Z, 21:00Z) each succeeded in
automation_runs yet minted nothing. Their exec logs (83 bytes each, mtimes
18:02:42 / 19:02:38 / 20:04:20 / 21:02:27 UTC) all read the same two lines:

    tip staged 2026-10-04T18
    DUNGEON: budget $0.0 hit at dnd0_20261004T180242Z_S0_dm

(with 190238Z, 200420Z, 210227Z in the siblings). tools/dungeon.py:203 raises
exactly this line when spend >= budget, so those fires were passed budget $0.0 by
their scaffold and died at the first dungeon call. This stop is NOT the $25 gate
(the day read $24.4905, under cap); it is the dungeon budget line. Why the scaffold
passed $0.0 at 18-21Z but a live budget at 22:00Z is not separable from the
surviving meters (the automations row carrying the prompt is deleted, section 7):
observed, mechanism unproven.

### 9.4 The gate's only true stops, and the $1.22 that sailed past them

Exactly two zero-mint fires followed the crossing: 23:00Z (day-04) and 00:00Z
(day-05). Both succeeded in automation_runs; no account row exists between the
22:35:50Z day-04 THE row and the 01:01:34Z day-05 dnd0 row; neither fire left an
exec log (every minting fire has one; even the budget-stops above have 83-byte
logs). The 23:00Z stop is cap-consistent: the day read $25.0074+ at fire start.
The 00:00Z stop is byte-observed (succeeded, zero mint, no exec log) but its
mechanism is not provable from the surviving meters: a UTC-day read at 00:00Z
would see $0 for day-05 and pass the fire, and the prompt that would explain the
read died with the deleted row.

Because only the arena lane carried the gate, non-arena lanes kept spending after
the crossing: from minute 22:06Z to the day close the account holds 13 rows /
$1.4610 = REPRINT $0.4961 (22:16:21Z) + THE $0.7226 (22:35:50Z) + TAVERN $0.2423
(the 22:00Z fire's own tavern tail from 22:06:02Z on). The non-arena pair is the
claim's $1.22 ($0.7226 + $0.4961 = $1.2187). Predicate honesty: a strict
after-the-crossing-second slice (ts > 22:06:53.865221Z) is 6 rows / $1.2847 with
TAVERN $0.0660; this section quotes the minute slice (ts >= 22:06) because the
crossing fire itself owns the rows between the second and the minute.

### 9.5 Deletion, not the gate, ended the overspend: day-05 burned $3.76 more

Day-05 minted $3.7616 over 287 rows, every one an arena lane (TAVERN $3.5096 /
191, dnd0 $0.1949 / 90, DND0 $0.0571 / 6), fires 01:00Z through 07:00Z, last row
07:12:43Z (TAVERN r10_JUDGE). The gate never stopped day-05: the UTC day rolled,
the counter restarted under $25, and seven more fires burned. The cadence ends in
the meters exactly as sections 7-8 banked it: the 43-run series stops at the
07:00Z day-05 fire, no 08:00Z+ run exists, and the automations row is deleted -
deletion window 07:12:43Z to 08:00Z day-05. Overspend ended when the automation
was deleted, not when the gate bit; the gate's day-keying makes every over-cap
close a one-day reprieve.

### 9.6 The meter since

Per-day totals, same 3038-row ledger: day-04 $26.2921 / 1448 rows; day-05 $3.7616
/ 287; day-06 $0.0337 / 2; day-07 $0.1014 / 26 (last row 2026-10-07T09:21:35Z);
day-08 and day-09 zero rows. Near-dark from day-06, dark since 10-07 09:21Z.
