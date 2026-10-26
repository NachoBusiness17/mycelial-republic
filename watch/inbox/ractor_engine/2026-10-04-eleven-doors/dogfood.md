# DOGFOOD LENS - the eleven remaining doors, organ-mapped (2026-10-04)

Seat: lens-dogfood (organ mapper) of the ractor on the 24-wide dig's eleven
remaining doors. Material read this session in full: the reviser receipt
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md (320 lines), the door-1 landing
watch/inbox/GWAP_INDEPENDENT_COP_20261004.md, state/CURRENT.md. Every organ
claim below carries a path:line I read or a command I ran this session; the
live tree moved under me twice and both movements are reported as findings.
Laws honored: no em-dashes, no fabrication, absence claims name instrument and
scope.

## Door-state ledger (tree truth as of 2026-10-04 ~12:45 ET)

1. ARENA-BENCH CI TRIPWIRE: LANDED mid-session by a sibling seat, commit
   00cb15c77 at 12:39:31 -0400 ("ARENA BENCH TRIPWIRE (door 2)"). The
   receipt's "shape drift" diagnosis was wrong-detail-right-symptom: the real
   cause was a stale path onto a 459-byte redirect stub
   (dashboard/static/arrakis.html, 459 bytes, zero gates by my python count)
   left by the 2026-09-22 surfaces dedupe, while the canonical surface lives at
   dashboard/static/games/arrakis.html (17,501 bytes). My session-start Read of
   mag/arena_bench.py:66 showed the stub path; post-landing grep reads :73 as
   the games/ path; git diff is empty because the fix is committed.
2. CLIPPY-AS-PROBER: the estate already probes recall at boot. tools/zknot.py
   computes "METER self-steal+forgot per 1000 human prompts" over trailing 7d
   windows (tools/zknot.py:198-211, read this session). The FSRS card-state
   layer is genuinely absent: `grep -rn -i -l "fsrs|spaced repetition"` over
   .agents/skills + memory/rib returned zero files (my run), matching the
   receipt's rg zero over mag/tools/tests. The door is a WIRE onto zknot's
   existing probe surface, not a new prober organ.
3. NIGHT-CYCLE CHECKPOINT LEGS: largely pre-empted by commit d349ce7d2
   (2026-10-04 05:50 ET, the GO WAVE). _save_state is now atomic
   tmp+os.replace and its comment names the exact 5x CYCLE_FAIL class the door
   targets as cured (mag/lane_runner.py:124-144, read this session); the
   trail-before-persist reorder sits at :932-938; march honest-skip is rc=2
   (:925-931). Residual per-leg resume flags guard a class with no measured
   recurrence post-cure.
4. MONOCULTURE AGREEMENT-RATE PROXY: MoA already computes convergence and
   dissent_preserved per run (mag/mixture_of_agents.py:74, :91) and its
   synthesizer gates at 0.7 (:125). The alert surface (memory/attention.md)
   and the dedup pattern (tools/instance_guard.py, CURRENT.md wave-1 alarm
   dedup) both exist. The door is one alert producer, ~2h.
5. PHEROMONE METABOLISM: the capability table is ALREADY a mutable UPDATE
   rollup, not an append-only store: INSERT at tools/gps_mcp/ledger.py:422-428,
   UPDATE at :444-448, with last_measured timestamps and a momentum floor
   (:434-443). Decay is an age-weighting change to that rollup (or a read-time
   transform); the append-only verdict_log INSERT at :450-454 is untouched.
   The receipt sized this as a new organ; it is a formula change on an
   existing UPDATE plus lineage stamps.
6. MYCELIUM-V2 BI-TEMPORAL: mag/republic.py already enforces the supersession
   vocabulary as house-chain law: header law at :15 ("superseded_by another,
   never deleted or edited"), the field set-once at :114, and re-pointing
   supersession raises AppendOnlyViolation at :209-218 (all read this
   session). The mycelium side is as the receipt says: contradict() bumps
   counters with no lineage (mag/mycelium.py:188-198) over a full-file
   open("w") rewrite (:183, :201-205).
7. MCP-LATTICE-SHIM: mag/mcp_server.py is live and wired but its tool map
   serves corpus/research/estate-bridge read tools and mutating shell tools
   only (mag/mcp_server.py:144-170, read this session); no memory_recall, no
   context-pack, no lattice tool exists in the map. token_budget exists only
   at mag/local_usable.py:205. The door survives as an extension of the
   existing server, gated on the reconciliation pass
   (X_INTEL_AIENG_SCRATCH_20261004.md:92-94 per the receipt).
8. THREE-SIGNAL-QUERY-BROKER: tools/estate_query.py is already the estate's
   join organ over four surfaces by corr_id (tools/estate_query.py:55-60,
   read this session), with tests (tests/test_estate_query.py). The broker is
   a fusion layer over estate_query + lattice_query + FTS; the embedding lane
   is the only new dependency. Its recall@5 falsifier harness can reuse the
   estate_query join shape instead of being built fresh.
9. WELD DOOR: its named gate (the cop fix) is cleared by bb0f34586; the
   playground organs ran live today (watch/inbox/playground/dnd0_20261004*,
   tavern_20261004* in git status) and the GWAP receipt banks 529 v3 payloads
   across them. This is the next ungated big build, and the only door that
   closes teach/verify/adapt on one content per the receipt's own
   differentiator.
10. BUILD-ONCE CALIBRATOR: tools/oracle_calibration.py already computes
    ECE/MCE/Brier (:124, :144-:174) with a self-check
    brier_perfect_calibrated (:376), and has ZERO consumers: git grep -ln
    oracle_calibration over mag tools tests scripts configs returns only
    configs/violation_baseline.json and the file itself. The calibration-flag
    half of this door needs no model download; the Gero-4B download half
    stays gated (no published evals, per the receipt's own card read).
11. CONSUME-THE-LEDGER WIRE: real absence inside my scoped instrument:
    git grep "gps_mcp|capability" over mag/flock_steal.py, mag/steal_steer.py,
    mag/swarm_control.py, mag/coordination.py returns zero hits. The flock is
    load-bearing, not a toy: git grep -ln flock_field over mag tools tests
    scripts lists 16 consumer files (flock_job, flock_scheduler, verkle_lance,
    swarm_control, steal_steer, window_bus among them). steer() is
    instantaneous-only over a static PhiField (mag/flock_field.py:158-170).

## Findings

F1 (CONVERGENT): Door 2 landed by a sibling seat WHILE this lens ran, and my
independent run reproduced both the defect and the cure. Evidence: my
session-start Read showed mag/arena_bench.py:66 pointing at the stub; my
python count: dashboard/static/arrakis.html = 459 bytes, 0 "blind" tokens, 0
gates; my direct run of load_ground_truth() after the landing printed "PARSE
OK gates= 3" off dashboard/static/games/arrakis.html (17,501 bytes, ARRAKIS_PATH
at mag/arena_bench.py:73), crown 50, ghost ZCode; commit 00cb15c77 (12:39:31
-0400) carries the path repoint, a 4-test tripwire, and the receipt
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md; tests/test_arena_bench.py exists
(ls). Pre-landing, git grep -n arena_bench over the tracked repo found zero
tests/ references (only the dist_audit copy, docs/rd_history/INDEX.md:46,
scripts/vast_paces_full.py:46, watch/ARENA_BENCH_V0_20260905.md). Falsifier:
closed by check: tests/test_arena_bench.py DOES assert the real-surface parse
(test_ground_truth_parses_the_canonical_surfaces calls load_ground_truth() at
tests/test_arena_bench.py:52, plus test_surfaces_are_not_redirect_stubs at :58
and the selftest split proof at :30-44, verified by grep this session). Move
(0 min): mark door 2 CLOSED in the sequence; the reviser's order advances to
clippy-as-prober, re-scoped per F5.

F2: The NIGHT-CYCLE CHECKPOINT LEGS door (receipt rank 4, sized 2-4h) targets
a harm the same morning's GO WAVE already cured, and the census bullet that
promised its test file carries a phantom name. Evidence: the Errno-22 cure
comment names the 5x CYCLE_FAIL class and dates it 2026-10-04
(mag/lane_runner.py:128-139), atomic tmp+os.replace at :140-143, trail
reorder at :932-938; the last commit touching mag/lane_runner.py is d349ce7d2
(2026-10-04 05:50:05 -0400); ls shows tests/test_monitor_lane_rotation.py and
tests/test_worldline_compact.py exist but tests/test_night_march_cure.py does
NOT (AGENTS.md census bullet names it as a landed night-shift test file with
the "some untracked at this census moment" hedge; it is absent on disk now).
Falsifier: a post-2026-10-04 lane_scheduler.log entry showing a completed leg
re-run after a mid-cycle daemon death (the residual class per-leg flags would
cure). Move (30 min): re-scope door 3 to a 1h idempotency test (monitor re-run
is a read; march is rc=2-guarded) or drop it from the sequence; do not spend
the receipt's 2-4h on it.

F3: The decay family's "define valid_at/invalid_at/superseded_by ONCE" order
proposes minting a vocabulary the estate already enforces once, in
mag/republic.py. Evidence: mag/republic.py:15 (house chain law: superseded,
never deleted or edited), :57 (frozen-field law naming superseded_by), :114
(set once by supersede()), :209-218 (AppendOnlyViolation on re-pointed or
dangling supersession). The receipt's own law-51 ruling ("one bug many
jackets, applied in advance", receipt line 33) warns against exactly this
dialect split. Mycelium's contradict() is the unwired side (counters, no
lineage, full rewrite: mag/mycelium.py:188-198, :201-205). Falsifier: if
republic's supersede() semantics (integer letter IDs inside a book dump)
cannot carry mycelium's string src/dst edges without an adapter heavier than
a fresh schema, the steal costs more than the mint; check by sketching the
edge-to-letter mapping. Move (1h): spec sketch mapping mycelium edge
supersession onto the republic shape BEFORE any decay-family build; the
pheromone half needs no new vocabulary at all (the capability rollup already
UPDATEs in place with timestamps, tools/gps_mcp/ledger.py:444-448).

F4: The BUILD-ONCE CALIBRATOR door splits into a 2h wire the estate already
owns and a gated model download that is cargo today. Evidence:
tools/oracle_calibration.py computes ECE/MCE/Brier (:124-:174) and self-checks
(brier_perfect_calibrated, :376) with zero consumers (git grep -ln
oracle_calibration over mag tools tests scripts configs: only
configs/violation_baseline.json + itself); MoA already logs per-vote
confidence (mag/mixture_of_agents.py:48, :73-74) and the receipt itself names
the v4 proper-scoring door at HEAD 993a5977b. The Gero-4B half carries no
published evals (receipt card read, watch/inbox/X_INTEL_PROPER_SCORING_20261004.md
per the receipt) so its download-and-eval gate stands. Falsifier: if no
joinable outcome stream exists for MoA confidences (votes banked without a
later-verified outcome row), the wire needs new logging and the 2h doubles;
grep where MoAResult rows are persisted and whether any verdict joins them.
Move (2h): wire oracle_calibration over one existing confidence+outcome pair,
bank the first Brier on real rows, defer Gero-4B behind its eval gate.

F5: The honest build order by EV-per-hour, after today's landings, diverges
from the receipt's table at three ranks. Doors 1 (bb0f34586) and 2 (00cb15c77)
are landed; night-cycle drops to a re-scope (F2). Next by EV/hour:
(a) clippy-as-prober as a zknot wire (the meter exists, tools/zknot.py:198-211;
the FSRS state layer is the only new bytes, ~2h, and it banks the ~1k probes
the FSRS lane needs); (b) monoculture proxy as one alert producer on the
existing MoA convergence + attention surface (~2h); (c) pheromone metabolism
as a rollup-formula change with republic-lineage stamps (~2-4h, down from
4-8h); then the design-gated tail in receipt order (three-signal, MCP shim,
weld, consume-the-ledger, calibrator-model). Cargo verdict: the Gero-4B
download (gated, zero evals, self-steal exists), night-cycle-as-specced
(pre-empted), and the receipt's mint-a-shared-schema framing for the decay
family (republic.py holds it). No sacred cows cut the other way: the 24-wide
receipt's own rank-2 premise ("broken today") was 12 days stale in cause
(stub since 09-22) and its rank-4 sizing was pre-empted same-morning; its
instrument table remains the best map in the estate and doors 5-11 survive
hostile pass with the re-scopes above.

## Blind spots

I fetched no external sources this session (Gero-4B card, agentmemory repo,
mem0): those claims ride the receipt's fetched bytes, marked as such. I read
tools/gps_mcp/ledger.py only at :415-455, not the whole routing surface. I
inspected the sibling's tests/test_arena_bench.py by grep only (test names +
the load_ground_truth import and call), not a full read. The MoA
outcome-join feasibility in F4 is asserted from schema reads, not from a
live joined run. My consume-the-ledger absence claim covers 4 steering files,
not all 16 flock consumers (scope named in the ledger above). I did not run
the bench live lane or vast_paces. The republic.py read covered :95-137 and
:196-225; supersede() itself I cited from its enforcement sites, not a full
function read. tests/test_night_march_cure.py absence is a working-tree ls
at one moment on a live tree; a sibling could land it after this write.

## Correction (hostile second pass, same day)

F2's phantom-test-name half is WITHDRAWN. tests/test_night_march_cure_20261004.py
EXISTS: 5,773 bytes, 130 lines, tracked under commit 9718e812d (2026-10-04
04:55:21 -0400, NIGHT SHIFT lane 7/10), verified by ls + git log this pass.
The AGENTS.md census bullet's unsuffixed "test_night_march_cure" is a
suffix-drifted hand-copied name (an erratum in the bullet), not a phantom
file. My instrument error: I queried the exact unsuffixed literal instead of
a wildcard (ls tests/test_night_march*), the exact WORLD-READ-LAW class the
tasking warned about.

F2's cured-harm half is CORRECTED AND STRENGTHENED. Night composite: dead by
its own falsifier, now verified on the correct surface (the lane trail, not
the scheduler log): queue/lanes/night/trail.jsonl carries the last
CYCLE_FAIL at 2026-10-03T23:08:04Z (pre-cure), then the 23:10:55Z success and
the 2026-10-04T08:50:01Z clean composite (monitor rc=0; march rc=2 honest
skip; the same row at logs/lane_scheduler.log:9941), zero night CYCLE_FAIL on
10-04. BUT the per-leg harm class is NOT dead estate-wide: the research lane
hit the same Errno-22 class TODAY 12:23:41Z-12:31:37Z, AFTER the 05:50
atomic cure (five rows, logs/lane_scheduler.log:10021-10025), each as a
MONITOR(rc=0, rotation epoch 76+) then CYCLE_FAIL pair in
queue/lanes/research/trail.jsonl: a completed leg lost at the state write and
re-attempted ~2min later. The atomic cure cannot close the class because the
except OSError re-raises (mag/lane_runner.py:144-149: unlink tmp, raise):
when the external lock catches the replace too, the cycle still dies
post-leg. The door therefore RE-SCOPES to the general per-leg-checkpoint
class (any lane whose legs precede the state write; today's research burst
is the measured recurrence), sized 1-2h; it does not drop. Tightened
falsifier: the re-scoped door dies only if a trailing 14-day window over ALL
per-lane trail.jsonl files shows no post-leg CYCLE_FAIL recurrence
(instrument named: per-lane trail CYCLE_FAIL rows preceded by a same-cycle
leg row); that test already fails once today.

Writer: lens-dogfood (ractor, 2026-10-04-eleven-doors)
fetched: 2026-10-04
