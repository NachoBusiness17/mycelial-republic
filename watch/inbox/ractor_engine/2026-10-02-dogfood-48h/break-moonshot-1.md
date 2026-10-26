# BREAK-MOONSHOT-1 - hostile second pass on moonshot-1

Filed by the break-moonshot-1 lane of the ractor-engine 2026-10-02-dogfood-48h run.
Every check below was executed this sitting on the current tree unless marked NOT RUN.
No em-dash bytes. The lens report under review was recovered in full from
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/moonshot-1.md (the delivered JSON was
truncated mid-F4; the disk copy carries all five findings).

## Verification stamp (what I ran)

pytest --collect-only -q -p no:cacheprovider on tests/test_inference_budget.py (19)
and on each of the six garden files individually (9, 9, 19, 13, 21, 20) and on
tests/test_burns_verdict_enum.py (46); grep of "def test_" and "parametrize" in the
0c9d72a06 copy of tests/test_inference_budget.py (19, 0); pytest -q run of
tests/test_sw1_tickets.py (17 passed, 0.53s); an independent python scan of
memory/runs/hermes_burn/usage.jsonl (236 rows) and memory/runs/model_garden/usage.jsonl
(725 rows) written fresh for this pass (no reuse of moonshot1_cost_scan.py); Read of
scripts/descent_driver.sh, mag/lane_runner.py:1080-1110, dashboard/rest.py:2955-2974,
mag/records.py:125-168, mag/biography.py:578-602, mag/seed_seal.py:225-296,
scripts/invisible_runner.vbs, githooks/pre-push:1-35, watch/inbox/NIGHT_CLOSE_20261002.md
(whole), memory/rib/RIB_INFERENCE_BUDGET_20261001.md (whole),
watch/inbox/census_refresh_20261002.md (whole), watch/inbox/model_garden/BATTERY.md;
grep lock/claim/flock/pid over tools/hermes_burn.py (prose hits only) and over
scripts/astra_convo_loop.sh + scripts/start_autorun.sh (rc=1, nothing); git grep
seed_seal consumers; seed-seal verify fired twice (wrong args then correct args);
git show -s --format=%cI on the eight commits; stat (PowerShell, UTC) on
logs/kpi.jsonl, NIGHT_CLOSE_20261002.md, memory/percolator/candidates.jsonl;
a 400-row source census of logs/kpi.jsonl tail; tail of logs/ratchet_daily.log (UTF-16,
via PowerShell); schtasks /Query /V on the four patrols, Estate Ratchet,
mag-docker-watchdog, vast-bargain-loop, Estate Gopher; a Get-ScheduledTask sweep of ALL
task actions for vbs/wscript wraps; Get-Process on twin PIDs 54504 and 40632; git
status --porcelain on tests/ and watch/arc_seeds/; git diff --stat tools/code_swarm.py;
wc -l on the four ratchet-growth files; ListSavedWorkflows read-back; ListWorkflowRuns
attempted (same capability gap as the lens hit).

## Verdicts

### F1 "the 42-test phantom" - CONFIRMED (one evidence line corrected, see Addition 2)

Every leg re-derived independently: tests/test_inference_budget.py collects 19 now AND
at its landing commit (19 "def test_", zero "parametrize", counted in the 0c9d72a06
copy; only commit touching the file is 0c9d72a06 itself, so no recorded trim exists);
census_refresh_20261002.md:26-27 repeats "the inference_budget 42-test battery" inside
the receipt that concludes "no fabrication smell" at :38; RIB_INFERENCE_BUDGET
20261001.md:78 is the sole origin ("42 green with the two carrier suites"), and the two
carrier suites have no separate files: their tests live INSIDE test_inference_budget.py
(test_hermes_* at :199-238, test_garden_* at :280-322 of the current file). My wider
sweep found no budget-related 42 in any receipt: watch/inbox/model_garden/BATTERY.md is
the probe-grid spec (zero 42-test language), and the only other "42" in the estate
record is an unrelated "AG5+AH19+compaction+audit suites 42/42 green" at
watch/inbox/hermes_burn/T1W1_RACTOR.md:186 (a 09-30 suite count, not the battery
figure). Correction the lens must carry: "no subset sums to 42" is false arithmetic
(9+13+20=42); the true statement is that every 42-subset EXCLUDES test_inference_budget
.py itself (19 plus 23 is unreachable: the largest pair among 9,9,13,21,20 is 22), so
no coherent reading of "the inference_budget battery" reaches 42 and the finding
survives its own defective line.

### F2 "one door guarded, the vault open" - CONFIRMED

scripts/descent_driver.sh:10-23 carries the guard byte-true to the commit claim (exit 3
second instance at :18, stale-pid reclaim at :20, trap cleanup at :23; the lens cited
13-23, the block starts at 10). grep of tools/hermes_burn.py for lock/claim/flock/pid
hits prose only (:152-156 the estate-law block, :226 an ask note): zero serialization.
mag/lane_runner.py:1086-1099 holds the daemon-refuse pattern to self-steal.
scripts/astra_convo_loop.sh and scripts/start_autorun.sh grep rc=1: no pidfile. My
independent ledger scan reproduced all three episodes: (a) 13:11-13:53Z re-fires
(A1 at 13:11:41/13:26:52/13:34:09, B2 at 13:18/13:29/13:37/13:53, C1 at
13:19/13:30/13:39); (b) T1W2 pairs 19:17:38.2/19:18:00.9 (S5, 22.6s),
19:17:54.2/21:29:22 (S6), 19:18:24.8/19:18:25.7 (S7, 0.95s), 19:18:29.0/19:18:33.7
(S8, 4.7s) - the "0.95s to 22s" deltas byte-true; (c) twin window 21:28-21:53Z: 13
in-window doubled keys (DUEL2_train 02-06 and 08-14, N1R_parables_songmap) summing to
exactly $2.2521, byte-exact to the commit's "$2.25". Twin liveness closed by execution:
Get-Process on PIDs 54504 and 40632 returns nothing, both dead at this hour. The
falsifier (a concurrent second hermes_burn.py invocation) was deliberately NOT RUN:
it would double-drain a paid queue; the code read is the evidence.

### F3 "the OWED ledger compounds" - WEAKENED (all decay items byte-true; the named
hot writer is not the pump, and "verify green" overstates; see Additions 1 and 4)

Confirmed by execution: NIGHT_CLOSE_20261002.md mtime equals creation
(2026-10-02T05:14:18Z both), full read contains no erratum/1.0077/10.0031 text;
commit-queue grep rc=1 across the four named ledgers (my wider sweep found it named in
prose at watch/inbox/RACTORSWARM_MAP_20261001.md:50-52, "the commit-queue law owed from
tonight's lock churn is the third external step" - still ticketed nowhere);
logs/kpi.jsonl grew 752,885,507 (lens, 10:45:26Z) to 753,284,197 bytes at
mtime 11:09:29Z during MY audit, still growing; mag/records.py:166-167 appends the
full row (write_kpi def at :138), no rotation anywhere; scripts/invisible_runner.vbs
:28 writes the rc log in overwrite mode (CreateTextFile(..., True));
logs/ratchet_daily.log ends "[2026-10-01 09:45:02] END seal=0 freshness=0 ratchet=1"
with GROWTH rows concept_predictor 513 to 667, duel_harness 461 to 581, env_contract
563 to 743, all verified live on today's tree by wc -l (667/581/743), plus a fourth
row the lens missed (Addition 3). Damage: (1) the lens's hot-writer attribution
(dashboard/rest.py:2964-2967 h_kpi, "every API hit") does not describe the current
bleed: my 400-row tail census reads 400 of 400 rows source="summarize" across
01:07:03Z to 11:17:22Z (about one row per 91 seconds), zero api rows; the pump is
mag/biography.py:589-591 (write_kpi(source="summarize") inside summarize_session, def
at :395), so the lens's prescribed move "stop h_kpi appending per poll" would leave
the bleed running untouched; the records.py:166 rotation half of the move stands.
(2) "executed same-sitting and verify green" overstates the patrols: all four read
back DIRECT (powershell -File or python.exe, no VBS) but all four still show Last
Result 1 with their first direct fires still in the future (08:00/08:30/09:00 EDT
today; audit ran 07:1x EDT). Registration verified; a green fire is not yet banked.

### F4 "built-once instruments" - CONFIRMED (two blind spots closed by execution)

ListSavedWorkflows read-back verbatim: topic arg REQUIRED; description carries
"workflow_gate PASS digest 5253afd2d68d G1-G7" (vs 912a34520349 in f4cfcdf9b's commit
message: post-landing amendment confirmed); moonshots default literally "2\r". THIS
run rides a real topic string: the fix held. githooks/pre-push:24-25 wires
citation_lint byte-true, and the same-day firing stamp is real
(watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md:174: "blocking=0, 26 anchors, 9
warn-only token misses"). seed_seal: the seal exists (seed_seal.v1, sealed_at
2026-10-02T04:10:34.819160Z, ed25519, key_id de5fc05e962c43ab), state/keys/
seed_seal_key present (64 bytes), git grep shows only AGENTS.md prose, the module
itself, tests, and receipts: zero production consumers. I dogfooded the verifier:
with correct args (verify seed.md chain.json seal) it returns ok=true rc=0 on the one
real seal; note the arg-order hazard, "verify <seal-path>" as first arg silently
treats the seal as the seed and reports "seed bytes tampered" instead of a usage
error. memory/percolator/candidates.jsonl: 16 rows, mtime 2026-10-02T04:17:43Z, never
written again. code_swarm: git diff --stat tools/code_swarm.py = 48 insertions, 1
deletion, uncommitted; tests/ porcelain shows only ?? tests/test_sw1_tickets.py. The
lens's biggest NOT RUN is now banked green: I executed tests/test_sw1_tickets.py:
17 passed in 0.53s, so NIGHT_CLOSE_20261002.md:29's "17 passed" is byte-true today and
F4's "active, un-landed" upgrades to "green and one commit from banked". Minor cite
correction: the TICKET_LEDGER CRLF-churn note lives at :161-163, not :159-160.

### F5 "cost truth" - WEAKENED (every number reproduced byte-exact; the heading is
contradicted by the lens's own timestamps)

Independently re-summed, all byte-true: hermes 236 rows $37.7591, first
2026-10-01T13:11:41Z, last 21:53:52Z; garden 725 rows $3.4746, 22:10:27Z to 03:34:25Z
(NIGHT_CLOSE_20261002.md:52-54 matches at "43 rows, $5.5208" and "725 rows, $3.4746");
A1_steer_antiforgery turn 1 fired 49 times for $20.9891 (55.6 percent of the hermes
window; RIB_INFERENCE_BUDGET_20261001.md:33 quote exact); twin doubles $2.2521;
DUEL1_hidden_5 x46 and N1_parables_songmap x42 at $0.0000 per row; 43f50ed71 committed
2026-10-01T21:41:17Z, after the last A1 fire at 20:17:25Z. Damage: the heading "the
window's paid spend finished before its first commit landed" is false as stated:
git %cI puts the six commits at 2026-10-02T00:46:30Z through 07:31:54Z, and garden
paid rows run to 03:34:25Z, so $3.47 of paid spend flowed AFTER the first commit
landed and only 44 minutes before the garden commit 0c9d72a06 itself (04:18:32Z);
the claim holds only for the hermes lane ($37.76, ended 21:53Z). The "~$0.79" T1W2
figure matches no clean ledger cut I could reproduce (S5-S8 all-in $1.1465; the
19:17Z first-episode rows $0.2495; the tripled keys' once-cost $0.7749).

## What the lens missed (additions)

1. THE KPI PUMP IS summarize_session, NOT THE API ROUTE. The last 400 rows of
logs/kpi.jsonl (01:07:03Z to 11:17:22Z) are 400 of 400 source="summarize", about one
~30KB row (673-item incomplete_ids list) per 91 seconds, zero api rows; the writer is
mag/biography.py:589-591 inside summarize_session (def at :395). The lens's fix (stop
h_kpi per-poll) would not slow the bleed at all. Falsifier: produce an api-source row
in the tail 400, or show summarize_session is not the ~91s cadence caller. Move
(~25 min, folds into F3's sitting): skip write_kpi inside summarize_session when the
pack_report digest is unchanged, plus the rotation at mag/records.py:166.

2. THE PUBLISHED SUBSET-SUM LINE IS REFUTABLE ARITHMETIC. 9+13+20=42 among the six
garden files (claritas_faces or code_swarm, plus model_garden, plus rib_swarm); every
42-subset EXCLUDES test_inference_budget.py (19+23 needs a 23; the max pair among the
rest is 22), so the phantom verdict survives, but the line as printed hands any
operator a one-multiplication kill of the whole finding. Falsifier: a 42-subset that
contains the budget suite (none exists). Move (~5 min): restate the line as "no subset
containing the budget suite sums to 42" and let the proposed collect_attribution tool
emit per-file rows so receipts stop carrying hand arithmetic.

3. THE RATCHET'S RED IS BIGGER THAN FILED, AND ITS OTHER HAND ADMITS NEW DEBT. The
same 2026-10-01 09:45:02 run carries a FOURTH unaccepted growth row,
mag/estate_bridge.py 442 to 544 (+102), live on today's tree (wc -l = 544), and in
the same run a NEW debt entry "013cbb63c8c4912e ... except-pass: tools/hermes_burn.py
:237 silent except ...: pass" was passed by exception: the ratchet FAILS on growth
while except-passing new silent-except debt in the same breath, and neither side ran
the accept-or-fix protocol. Falsifier: a later ratchet_daily.log run where
estate_bridge growth is accepted by name or pruned and no new except-pass row appears.
Move (~10 min): add both names (estate_bridge growth, hermes_burn silent-except) to
the F3 OWED sitting's accept-or-fix list.

4. THE PATROL CURE IS REGISTERED BUT UNPROVEN, AND invisible_runner.vbs IS NOW
ORPHANED. All four direct tasks still show Last Result 1 with first direct fires due
08:00/08:30/09:00 EDT today (future at audit time); a Get-ScheduledTask sweep of ALL
task actions shows ZERO remaining tasks referencing invisible_runner.vbs (the other
VBS wraps: mag-docker-watchdog, green, last ran 11:15Z today exit 0; vast-bargain-loop,
disabled since 08-27; OpenClaw gateway, outside the estate; GatherNetworkInfo, a
Windows system task). So the dark-patrol class is cured at the task layer and the
23:32:51 EDT launch has no remaining scheduled vector, though the event itself stays
unattributed (no WMI run, NOT RUN by either pass). Estate Gopher's "Multiple actions"
inspected: two direct python chores (gopher_lite.py --chore census and --chore
label-farm), Last Result 0, last run 10-01 09:25 EDT: benign. Falsifier: any of the
four patrols returning nonzero after today's first direct fire. Move (~5 min at
13:05Z): one Last-Result check across the four; green closes the item for good.

## Blind-spot closures and not-runs

- ListWorkflowRuns: attempted, same error as the lens (workflow_introspection
_unavailable): the 63.1M / 37.6M / 54.0M / 68.7M token figures and the
Salon-mine-20deep provider stop remain ask-sourced, now double-unverifiable.
- Twin liveness: CLOSED, both PIDs dead (Get-Process empty).
- SW1 tests: CLOSED, 17 passed (run this sitting).
- WMI attribution of the 23:32:51 EDT launch: NOT RUN (no event-log access taken).
- The 61-primaries 90.6MB claim: NOT re-hashed (receipt-checked by the lens only).
- The concurrent-hermes_burn falsifier: deliberately NOT RUN (would double-drain a
paid queue; code read stands as the evidence).
- zcode-side token cost of the six commits: no local ledger found by either pass.

Filed by break-moonshot-1, 2026-10-02. No em-dash bytes.
