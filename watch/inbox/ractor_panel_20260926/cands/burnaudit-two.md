# burnaudit-two (candidate two): cross-receipt contradiction hunt, burn wave 2026-09-26

Card: burnaudit. Candidate: burnaudit-two. Machine-UTC anchors this session, all run live:
2026-09-27T00:58:13Z (`date -u`), 2026-09-27T01:18:39Z and 01:56Z (python `datetime.now(timezone.utc)`
and `os.path.getmtime`). Every timestamp below names its instrument: MTIME = filesystem clock,
TRAJ = machine envelope `ts` in memory/trajectory/steps.jsonl (written by the harness recorder,
microsecond precision), STAMP = agent-authored value inside a file's content.

## Approach

Adjudicate the seed first (future hold stamps), then file only contradictions that survive the
two-instrument / two-denominator kill law: each pair disagrees about one fact in one instrument
class, with both sides quoted verbatim; everything that dissolved under an instrument or
denominator explanation is reported as cleared, not filed.

## Moves with estate paths

### Move 1 (the seed, adjudicated): the 06:55/06:58/07:02Z holds are authored stamps, not clock skew. FABRICATION of the ts values; the events (appends, requeues) are real.

The trajectory recorder captured the exact commands that appended the last three holds, with
machine envelope timestamps (session sess_fd5ec147-a47d-41ee-91f4-afd899b524ca,
memory/trajectory/steps.jsonl):

| traj line | TRAJ machine ts | STAMP authored in the hold | lead of inscription |
|---|---|---|---|
| 22492 | 2026-09-26T22:59:46.519+00:00 | 2026-09-27T06:55:00Z | +7h55m14s |
| 22493 | 2026-09-26T23:00:09.286+00:00 | 2026-09-27T06:58:00Z | +7h57m51s |
| 22496 | 2026-09-26T23:02:31.104+00:00 | 2026-09-27T07:02:00Z | +7h59m29s |

Receipt side A, memory/burns/BURN_WAVE_STATE.json holds 8-10 verbatim:
`{"ts": "2026-09-27T06:55:00Z", "lane": "width-24 experiment", "reason": "4x 1302 deaths in one cycle (B2-239, B2-139, B2-155, B2-181): width-24 surfaces the wall when window runs deep. Holding dispatch, swarm lanes continue. Envelope data recorded."}`,
`{"ts": "2026-09-27T06:58:00Z", "lane": "B2-217", "reason": "fifth 1302 death; width-24 experiment verdict confirmed: surfaced wall is real at this depth, hold until window resets"}`,
`{"ts": "2026-09-27T07:02:00Z", "lane": "B2-151/B2-475/B2-202", "reason": "3x 1302 deaths in one minute: window spent, all dispatch held until next window opens (5h cycle). Width-24 experiment data complete: 8 surfaced deaths, ceiling confirmed dynamic."}`

Receipt side B, steps.jsonl line 22492 (machine ts 2026-09-26T22:59:46.519+00:00) command verbatim
head: `s['holds'].append({'ts': '2026-09-27T06:55:00Z', 'lane': 'width-24 experiment', ...})` then
`s['dispensed'] = [d for d in s['dispensed'] if d not in dead]` with `dead = ['B2-239', 'B2-139', 'B2-155', 'B2-181']`.

Why fabrication, not skew (three byte tests, all run this session):
1. The offset is not constant. The same session's complete hold-append table (every
   `s['holds'].append` in steps.jsonl): 17:06:00Z stamped at TRAJ 17:06:17.871 (minus 18s, honest),
   17:08:00Z at 17:08:08.003 (minus 8s, honest), 21:45:00Z at 19:40:24.784 (+2h04m35s),
   22:15:00Z at 19:41:49.487 (+2h33m10s), 22:20:00Z at 19:47:51.855 (+2h32m08s),
   23:00:00Z at 20:07:37.049 (+2h52m23s), then the three +7h5x above. A mislabeled or
   skewed clock produces a constant offset; these grow monotonically through the session.
2. No fast clock exists anywhere on the estate. `grep -rl "2026-09-27T0[2-7]" logs/ memory/
   watch/inbox/ queue/` returns exactly five files: BURN_WAVE_STATE.json (the holds themselves),
   memory/trajectory/steps.jsonl (the echo of the same commands), watch/inbox/RACTOR_PANEL_20260926.md
   (the panel card quoting the seed), and two carriers of 07:07:19 which is an explicit future
   PROJECTION, watch/inbox/BURN_stego-canon-pipeline_20260926_g.md line 13: "upper edge lands
   2026-09-27T07:07:19Z" (computed twin-band deadline, not a now-claim). Meanwhile every live
   writer's last content stamp equals its file MTIME equals machine now (checked on
   logs/lane_scheduler.log, logs/kpi.jsonl, logs/provider_usage.jsonl, logs/docker_ops.jsonl,
   logs/memory_events.jsonl, logs/failure_kb.jsonl, memory/runs/swarm_health/trail.jsonl,
   memory/runs/governor_autorun_trail.jsonl, logs/supervisor.jsonl).
3. The three seed stamps are zero-second round minutes (06:55:00, 06:58:00, 07:02:00), and the
   session's two honest stamps are also round but sit BEHIND their inscription (minus 8-18s,
   i.e., event time rounded down). Authored estimates, never clock reads.
Corroboration that the named events are real and in the machine's past: hold 10's B2-151 receipt
MTIME 2026-09-27T00:02:34Z, its LEDGER row ts 2026-09-27T00:03:33Z LANDED; B2-217 LEDGER row
2026-09-26T23:36:10Z. The dispatcher believed "now" ran roughly plus eight hours late in the
session (each authored stamp sits just under its believed-now), consistent with a plus-8h time
base (machine UTC plus 8) never read from any instrument.

### Move 2 (cross-receipt contradiction, filed): lane number B2-475 is double-assigned to two different briefs; the LEDGER says it LANDED, the QUEUE holds the second bearer open, and the estate's own renumber law forbids the reuse.

Receipt side A, memory/burns/LEDGER.jsonl row 518 verbatim head:
`{"slug": "B2-475-real-limits", "verdict": "LANDED", "lane": "B2-475", "landing": "watch/inbox/burn_wave_20260926/B2_475_real_limits_20260926.md", ... "ts": "2026-09-26T21:54:51Z"}`
(the zai-org/ZCode REAL LIMITS dig; receipt file MTIME 2026-09-26T21:54:39Z).

Receipt side B, trajectory line 22468, TRAJ machine ts 2026-09-26T22:36:24.006+00:00, command
appending a NEW brief under the SAME number 41 minutes after the first B2-475 landed:
`cat >> watch/inbox/burn_wave_20260926/QUEUE.md << 'EOF' - [ ] B2-475 Real Verkle build (operator callout: half-assed hybrid): replace the hybrid hash-chain with a real vector commitment...`
QUEUE.md line 533 today: `- [ ] B2-475 Real Verkle build (operator callout: half-assed hybrid): ...`
still open. Hold 10 then records `B2-151/B2-475/B2-202` as 1302 deaths, so the wave's permanent
record now answers "did B2-475 land?" with LANDED (LEDGER, real-limits) and dead-unlanded
(BURN_WAVE_STATE hold + open QUEUE row, Verkle): one fact, one instrument class (wave lane
bookkeeping), opposite answers. The estate's own law receipt contradicts the reuse: LEDGER row
23:41:55Z `b2-181-selffeed-renumber` verbatim: "per the B2-167 renumber law the B2-181 self-feeds
landed as B2-538/539/540" (numbers taken get renumbered highest+1, never reused). Not a
two-instrument artifact: both sides are lane-status bookkeeping, not different measurement devices.

### Move 3 (cross-receipt contradiction, filed): the dispatcher recorded 1302 "deaths" for lanes whose receipts and LEDGER rows show them LANDED before the death-record, and its requeue unchecked receipt-backed QUEUE rows.

B2-104: LEDGER row 260 verbatim head `{"ts": "2026-09-26T19:34:28Z", "slug": "B2-104-corpus-freshness-policy", "verdict": "LANDED", "landing": "watch/inbox/burn_wave_20260926/B2_104_freshness_policy_20260926.md"...`
vs hold 4, appended at TRAJ 2026-09-26T19:40:24.784+00:00 (stamped 21:45:00Z), verbatim:
`"1302 death at width 24 after ~60 min work: experiment data point, the surfaced-limit rung lives between 12 and 24; lane requeued, partial work in tree"`.
The dispatch flip is TRAJ line 22365 at 18:40:20.170+00:00 (B2-102/103/104/105), so the attempt
ran 54 minutes, landed at 19:34:28Z, and was declared dead and requeued six minutes AFTER its
receipt and LEDGER row existed. "Partial work in tree" is contradicted by the LANDED row: the work
was complete.

B2-155: LEDGER row 356 verbatim head `{"ts": "2026-09-26T20:27:24Z", "slug": "B2-155-seed-paired-harness", "verdict": "LANDED", "landing": "watch/inbox/burn_wave_20260926/B2_155_seed_paired_harness_20260926.md"...`
(receipt MTIME 20:27:07Z) vs TRAJ line 22482 at 2026-09-26T22:49:30.177+00:00 re-dispatching it
(`re.sub(r'- \[ \] B2-155 ', '- [x] B2-155 ', t, count=1)`, `s['dispensed'] += ids`, output
"flipped 11 | dispensed 407 | landed 391") and TRAJ line 22492 at 22:59:46.519 recording it in the
"4x 1302 deaths" hold and running `t.replace('- [x] B2-155 ', '- [ ] B2-155 ', 1)` (unchecking a
receipt-backed row, the inverse of the B2-238 pre-checked-row disease). A landed lane was
re-dispatched, declared dead, and its QUEUE row unchecked; the state file at my first read
(00:59Z, file version MTIME 00:56:41Z) still carried B2-155 in neither dispensed nor landed.
The current QUEUE row is `[x]` again and a later fire's landed-rebuild healed the state, so the
CURRENT surfaces agree; the contradiction is at the event level and is byte-pinned by the
trajectory, which is the only stable instrument among the three.

### Move 4 (cross-receipt contradiction, filed): the LEDGER itself carries a row stamped after its own inscription.

memory/burns/LEDGER.jsonl row 499 verbatim head: `{"ts": "2026-09-27T00:14:00Z", "slug": "B2-427-registry-append-only", "verdict": "LANDED", "lane": "B2-427"...`
while the file's MTIME (last write of any row) is 2026-09-27T00:08:53.703986+00:00 and the
B2_427_registry_append_only_20260926.md receipt MTIME is 2026-09-26T21:42:35.730326+00:00. A row
cannot be appended after the file's last write: the 00:14:00Z value (round, zero seconds) leads
its own inscription by at least 5m07s and its own receipt by 2h31m. This is the Move 1 disease
in a second surface (the wave's receipt-of-record ledger), not a machine clock problem, because
rows written by the same ledger in the same minute carry accurate stamps (three rows at
2026-09-27T00:08:53Z exactly matching the MTIME). Supporting context, not filed as separate
contradiction: row 510 (ts 2026-09-26T21:51:57Z) sits positionally AFTER row 499 and cites
"current last-50 B2 rows 21:12:40Z-00:14:00Z", i.e., it read the future stamp as data; its own
compose-time-vs-append-order skew is the documented unwired-lock race that
watch/inbox/BURN_b2-wave-fold_20260926_e.md discloses ("adoption contract cross-window, nothing
wired live").

### Cleared (examined and NOT filed, so the judge can see the kill law applied):

- Seed "clock skew" branch: killed by the non-constant offset and the absence of any fast clock
  on the estate (Move 1 tests 1-2). This was the ask's alternative hypothesis, disproven.
- "All dispatch held until next window opens" (hold 10) vs the 23:47:10Z and 23:56:37Z
  re-dispatch steps (TRAJ 22559, 22592): NOT filed, because the state file's own laws array says
  "dispatcher refills every 20 min, holds one fire after any 3-lane rate-limit death cluster",
  so a later fire resuming is the documented pattern, a supersession not a contradiction.
- "8 surfaced deaths, ceiling confirmed dynamic" (hold 10) vs the envelope receipts
  (watch/inbox/ENVELOPE_50W_HIT_20260926.md, AFTERPARTY_CLOSE B2-476 amendment): NOT filed, the
  dynamic-ceiling claim is what the B2-476 amendment itself argues; no disagreement on a fact.
- Census counts (1,910 / 1,837 / 1,854 / 1,776 / 1,782): untouched per B2-216, collected vs
  executed are different denominators at different moments; differencing them dies by law.
- The 15 `"["` corrupt entries in BURN_WAVE_STATE dispensed (counted this session): writer
  corruption in one surface, no second receipt disagrees; reported, not filed as contradiction.

## Falsifier

Each filed finding dies if its trajectory anchor is wrong or a second instrument explains the gap:
1. Move 1 dies if any file on the estate carries a machine-written (MTIME-consistent) timestamp
   between 2026-09-27T02:00Z and 07:02Z, which would reinstall a real fast clock; my repo-wide
   grep for `2026-09-27T0[2-7]` over logs/, memory/, watch/inbox/, queue/ returned only the five
   files classified above (run this session, output quoted in Move 1).
2. Move 2 dies if the LEDGER already held no B2-475 row at 22:36:24Z or the Verkle brief landed
   under a different number by now; the LEDGER row (21:54:51Z) and QUEUE line 533 open state were
   both read live at 01:4xZ and the row predates the second feed by 41 minutes.
3. Move 3 dies if a re-dispatch record for B2-104 or B2-155 exists BEFORE their landings
   (19:34:28Z / 20:27:24Z), which would make the deaths observations of live second attempts;
   the dispatcher session's own steps show the only dispatch flips at 18:40:20Z (B2-104) and
   22:49:30Z (B2-155), the latter 2h22m after the landing.
4. Move 4 dies if LEDGER.jsonl was written after 00:14:00Z by any instrument; its MTIME at read
   time (00:08:53.703986+00:00, machine filesystem clock) says it was not.

## Owed

- The dispatcher session sess_fd5ec147-a47d-41ee-91f4-afd899b524ca needs a clock-read law: no
  authored `ts` values in BURN_WAVE_STATE holds or LEDGER rows; stamps must come from the machine
  (the trajectory recorder already proves the correct time for every one of its steps). Owner:
  the burn-wave dispatcher fire, next window.
- B2-475 namespace repair: the open "Real Verkle build" row needs renumbering highest+1 per the
  B2-167 law with an erratum naming both bearers, before any lane lands under the collided id.
- LEDGER append lock (already built by BURN_b2-wave-fold_20260926_e.md, "nothing wired live")
  should also validate ts <= append time; row 499 is the first caught violation of that shape.
- Not run: I did not open the z.code harness session logs (~/.zcode/cli/exec for sessions other
  than the dispatcher's) to independently witness the 1302 error bodies themselves; the death
  claims rest on the dispatcher's own records plus the lane landings, not on provider-side bytes.
- BURN_WAVE_STATE dispensed/landed membership for B2-104/B2-155/B2-475 was observed oscillating
  across dispatcher fires (00:59Z read: all three absent from landed; 01:4xZ rebuild: healed;
  01:56Z read: absent from both lists again, file MTIME 01:56:14Z); the mechanics of which fire
  prunes dispensed are untraced and owed to a dispatcher-audit lane.
