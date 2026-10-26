# PROCESS IMPROVE WAVE 1 - 2026-10-03 (the 5.3 strategy window)

Operator order: two flash windows running heavy subworkflows; this GLM-5.3
window strategizes: 7-day full-estate catch-up, all sessions front-backwards,
then "begin on improving the function of all involved processes."

Seat: zcode GLM-5.3 strategy window (sess_a8c2ebd2). Read-only on sibling
surfaces; all cures additive; nothing killed; flash windows untouched.

## CATCH-UP (the 7-day fold, evidence in git + trails)

359 commits 09-26..10-03 (12/53/143/52/45/23/21/10 per day). Arc:
repair-and-codify (09-26/27: gala close, quantizer, gates) -> total
self-census (09-28, 143 commits) -> outward build (09-29/30: MaNGOS, auth
trinity, routing) -> meta discipline (10-01/02: descent protocol, ractor
arc, ouroboros, blind audits) -> generative play (10-03: arena day, D&D
dice-law dungeon, THE GENOME). Live at seat start: 6 sibling workflows
running (gap-analysis pair, Build-it-all, two ractor metas, OLM mine at
153M tokens); lanes builder/day_work/research HOT; elder 429-down since
10-01; hermes burn 2026-10-03 = $25.62 across 1,034 rows (233 ok:false).

## THE FINDING (one disease, five symptoms)

The estate's own named UNWIRED-ORGAN disease, again, in the burn/dispatch
plumbing: fixes landed where pain hit (doubled-key tripwire, key-failover
in one lane), siblings never adopted them.

1. **False re-fire storm (DND0/TAVERN/CAMP)**: dungeon.py and tavern.py
   minted burn-ledger ids from the turn number alone (`DND0_beat7_dm`,
   `TAVERN_r3_JUDGE`, `"turn": 1` hardcoded), so every session after the
   first re-rows the same (id, turn) key and trips the instance_guard
   doubled-key alarm. Arena day played several sessions: 217 ok:false rows,
   204 falsely flagged re-fires, 800 duplicate alarm lines burying
   memory/attention.md (the estate alarm surface). Tavern's own docstring
   law (`TAVERN_<run>_r<round>_<actor>`) was never in the code.
   Note: the ok:false rows themselves are the banked Nous content-filter
   voids (the known opus-5.5 combat-beat filter disease, 3-try retry +
   void-not-crash worked as designed; 99 beats DID land). The alarm flood
   was the defect.
2. **Alarm had no dedup**: one attention.md line per fire, no per-key cap.
3. **Worldline seed spray**: knot_at_close emits a full W1 death-rite seed
   per closing session; the flash-window fleet's actor children close as
   sessions: 2,156 near-identical SEED.json (~45MB, each hashing AGENTS.md
   + MEMORY.md + full tape + 11k-row chain) in ~2 days. Gap-sentinel
   growth alert red (29.5 GiB/day claim; steady-state bulk is watch/ 11G,
   models/ 9.8G, corpus/ 8.3G, no >50MB file landed in 48h; the unbounded
   per-actor emission was the addressable driver).
4. **x_radar dark 4 days**: MagXRadarDaily exit 2 daily since 09-30.
   `mag/x_reply_radar.py` primary path was a `.grock` TYPO dir, fallback
   lacked `.exe`; the grok CLI update ships `grok.exe` (with
   `grok.exe.old` beside it). The ps1 probe had the same no-.exe shape.
5. **Lane starvation**: elder CYCLE_FAIL 429 daily since 10-01 (12:00
   slot), harvest 429 on 10-02. `mag/lane_runner.flash_call` is the single
   z.ai Lite door; the flash windows saturate that lane all day and the
   sensing lanes die on it with zero failover.

## THE CURES (all landed + tested this sitting)

| # | Organ | Cure | Test |
|---|-------|------|------|
| 1 | tools/instance_guard.py `doubled_key_check` | alarm appends ONCE per (id, turn); repeat fires still stamp the row | tests/test_instance_guard.py::test_doubled_key_alarm_dedups_per_key |
| 2 | tools/dungeon.py | per-session `self.tag = dnd0_<stamp>` in every banked id (S0/S1 beats + CAMP S2-S4) | tests/test_burn_id_uniqueness.py |
| 3 | tools/tavern.py | `self.run = TAVERN_<kind>_<stamp>` prefix (the module's own docstring law, finally in code) | tests/test_burn_id_uniqueness.py |
| 4 | mag/x_reply_radar.py + scripts/x_radar_daily.ps1 | grok.exe-first candidate list (typo fixed); ps1 accepts .exe | hand-run: task exit 0, card + x_radar.json written 19:40 local (0 leaderboard rows today; watch the next 08:00 firing) |
| 5 | mag/knot_at_close.py `_worldline_seed_hook` | dwf-* actor children skip the rite (not seats; record lives in run journal + receipts); seat closes keep it | tests/test_worldline_seed_gate.py |
| 6 | mag/lane_runner.py `flash_call` | 429 -> 20s-paced retry -> env-pinned openrouter overflow (OPENROUTER_MODEL/KEY) before lane-down; lite_guard records only zai-served tokens; reasoning-budget rescue gated zai-only | compile + import proof; live proof rides the next elder 12:00 fire |

attention.md compacted 1216 -> 417 lines (800 dupes suppressed across 88
unique keys, first occurrence each kept; backup memory/attention.md.prededup-20261003.bak).

Census carrier refreshed: 4,211 collected / 502 files, moment
2026-10-03T23:47Z, 13.85s, zero collection errors. Attribution: BUILD-IT-ALL
af9aa05f6 (arena/DD test files, ~+50) + this wave (+2 files, +5 collected).

## LEFT AS FINDINGS (owner named, not cured this sitting)

- **MagTipWitnessDaily exit 2** (gist token 403, PAT lacks gist scope):
  OPERATOR: mint a token with gist scope or name a different publish
  surface; chain-tip external publish was already operator-gated in the
  48h synthesis.
- **MagLeaveProtocolDaily rc 1 / day_end_pile dark since 09-28**: needs a
  task-doctor pass; the leave register script targets a script whose log
  surface is ambiguous. Next window.
- **research lane degraded** (0/7 terms, openalex boxed): the lane's
  dedup-saturation blindness is a known memory; needs the poll rotation
  cure, not a patch here.
- **configs/mirrors.json seal churn**: the live stealth driver updates it
  (13:13Z today) after each patrol re-seal: live STATE living under
  configs/ fights the config-seal design. Proposal: move mirror runtime
  state to state/fuel/ or exempt-by-name; OPERATOR/design call (ball3's
  "config-seal trio" already ruled CODE never seals STATE; this is the
  same family).
- **2,156 existing dwf-* seed dirs**: left in place (never delete sibling
  data); compaction/tombstone is an operator call now that the writer is
  gated.
- **test_selffeed_integration.py zero-collect**: standing gap, unchanged.
- **DND dm-beat filter voids**: the deepseek-thinking sacred-cow commit
  (53f56d0f3) re-scoped thinking per-task; if opus-5.5 dm beats keep
  voiding, the dm role is a routing-classes candidate (haiku-4.5 ran clean
  as the janitor all day).

## Numbers (instrument-named, per B2-216)

- collected: 4,211 / 502 files, `pytest --collect-only -q`, 2026-10-03T23:47Z
- targeted: 14 passed (test_instance_guard + test_burn_id_uniqueness +
  test_worldline_seed_gate), 1.49s
- full suite `pytest -q`: fired 23:48Z, result appended to this receipt at
  close (see below)
- hermes burn 10-03 pre-fix census: 1,034 rows, $25.62, 233 ok:false (204
  doubled_key-flagged), prefixes DND0_* 217 / CAMP 10 / TAVERN 6


## FULL SUITE VERDICT (banked 2026-10-04 ~03:10Z, per the promise above)

`pytest -q -p no:cacheprovider` fired 2026-10-03T23:48Z, completed after
11,797.58s (3h16m) on the loaded box: **29 failed / 4,213 passed / 7
skipped / 3 errors**.

INSTRUMENT DEFECT (this seat's own): the run was piped through `| tail -5`,
so only the summary plus the last 4 FAILED names survived - the full
29-failure detail was destroyed by my own pipe. Law kept for the next
full run: never pipe a suite through tail; redirect full output to a log
file and read the tail of the FILE (same class as the census
instrument-naming law; self-inflicted variant).

Visible failures: test_zai_burst::test_fuel_feed_includes_lite_cache_lane
(MINE - asserted the pre-pull Lite world; flipped to pin the pulled world
same sitting), test_shared_surface_events baseline drift + two wave_driver
chain/selftest failures (sibling-owned surfaces, the shared-fold class).
The other ~25 are unattributed because the pipe ate the detail; the next
unpiped full run attributes them.

Post-verdict targeted blast over every change-surface test file of both
waves (zai_burst, zai_backoff_floor, lite_lane_pull, instance_guard,
burn_id_uniqueness, worldline_seed_gate, lane_runner_cluster, lane_budget,
lane_effort, build_lane_tripwire, dormant_gate_b2133, loop_death_guards,
concept_predictor, ah4_rib_fixes, room_tags): 136 passed; cost_truth pair
6 passed. One Windows flake (instance_guard stale-reclaim PermissionError)
passed on rerun.


## NIGHT ADDENDUM 2026-10-04 ~03:30Z (du task completed; findings closed)

- LEAVE-PROTOCOL finding closed: MagLeaveProtocolDaily IS registered and
  Ready (next fire 08:00 today); its rc-1 is script-level in
  tools/leave_dispatcher.py (the register script's /TR target). Owed: one
  hand-run of the dispatcher to read its exit-1 path. day_end_pile has NO
  schtask at all (the 09-28 run was a one-off) - scheduling it is an
  operator call per the no-timed-schedules law.
- BLOAT OWNERS NAMED (the >50M growing set, from the completed du):
  dashboard/data/ESTATE_INDEX.jsonl 3.2GB (the single biggest repo file,
  unbounded append - THE gap-sentinel growth driver; needs a
  compaction/rotation owner, NOT a 3AM rewrite), logs/backend_sv.log 84MB
  (pure /health 200 access lines - needs a uvicorn access-log filter or a
  slower poll), logs/behavioral_events.jsonl 65MB (telemetry append).
  Steady-state bulk (watch/ 11G, models/ 9.8G, corpus/ 8.3G incl ghidra +
  JDK zips) is not daily growth.
- WARNING-SPAM CURED: logs/dashboard_sv.err.log was 172MB of Python
  SyntaxWarnings - three '\$' invalid escapes in main.py f-strings,
  re-emitted on every server start. Fixed at source (main.py:2460/2520/
  2524, '$' needs no escape; parse verified zero-warning), log rotated to
  a 195KB tail.

## CORRECTION 2026-10-04 dawn (night addendum above named ESTATE_INDEX the
"unbounded append" growth driver - both halves corrected by the compaction
design lane, watch/inbox/night_shift_20261004/estate_index_compaction_design.md)

The writer does full snapshots (mode "w"), not appends; 8,803,599 rows ==
last_run.json total_files exactly. Growth = walk-scope growth, and 87.2%
of the 3.2GB is a gitignored regenerable .mimosa cache (7.4M rows); the
index without it is 437MB. The 29.5 GiB/day gap-sentinel figure measures
indexed CONTENT growth of the project. Trust the design lane's byte
numbers over this receipt's night addendum.
