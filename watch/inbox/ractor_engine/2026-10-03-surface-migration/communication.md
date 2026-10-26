# communication lens - surface migration raction (2026-10-03)

Moment: checks run 2026-10-03T19:15Z..20:20Z by the communication lens
subagent, Git Bash on win32, all commands executed this sitting unless
marked not run. Topic: migrate the primary orchestration surface from
interactive ZCode to Hermes-launched headless rails. Lens question: how
does the operator steer a headless estate - what actually reaches the
operator versus what the receipts claim was communicated?

## Verdict lean (from this lens alone)

The WORK rails are headless-ready; the REPORT rails are not. Every
communication surface the operator would depend on under a headless-first
estate is either flooded with per-key noise (attention.md), unscheduled
(cycle_brief, attention_dam), wired to a nerve the rails never write
(overmind senses), split across two unjoined ledger families (cost), or
dormant since August (wait_human, handoff). Migrate the work; do not
retire the interactive seat until a scheduled, aggregated, one-line dawn
report exists. Nothing here disproves the migration thesis - it names the
build order the thesis implies.

## Findings

### F1 (CONVERGENT): the alarm channel is a per-key firehose with fabricated read state

- memory/attention.md is 1,137 lines; 809 of them (71%) are
  INSTANCE-GUARD doubled-key alarms fired 2026-10-03T11:51:05Z..19:08:04Z,
  one line per re-fired (id, turn) - burst rates of 7-10 lines/minute
  during arena cycles (`grep -c "INSTANCE-GUARD doubled-key"` = 809;
  per-minute `uniq -c` census run this sitting).
- The `- [x]` checkbox is written by the emitter itself:
  tools/instance_guard.py:203 hard-codes the prefix in the alarm
  template, so 809 alarms read as "checked" with zero triage having
  occurred. Any census that counts checkboxes as read receipts counts
  noise as answered - the key-census trap in alarm form.
- CONVERGENT with the 10-02 hostile pass
  (watch/inbox/ractor_engine/ractor-topic/break-communication.md finding
  2): same channel, no dedup in the append path, dam one-shot and
  unscheduled. Today's flood is a NEW emitter (instance_guard vs the old
  improve probe-alarm), so the structural hole re-proves across emitters;
  the convergent finding outranks any single-source novel claim.
- Migration implication: a headless estate steers through exactly this
  kind of file. 71% noise means the signal leg (a real money bug: the
  re-fire signature that cost $2.25 twin-window per the
  tools/hermes_burn.py:151-153 comment) drowns in its own tripwire.

Falsifier: an aggregation pass (one alarm per ask_id with a count
suffix) plus a scheduled attention_dam run that drops the doubled-key
ratio below 10% of the file kills this finding.
Move (one sitting, ~25 min): make instance_guard.doubled_key_check
aggregate per ask_id before append, and register tools/attention_dam.py
on a daily task (full scheduler sweep this sitting shows zero
attention_dam invocations).

### F2: THE STEERING SURFACE has never had a second dawn

- tools/cycle_brief.py:2 bills itself "v1 = THE STEERING SURFACE", the
  morning composer that assembles overnight organ output into the day's
  steering. Its only output is watch/inbox/CYCLE_BRIEF_20260930.md - 3
  days stale. Nothing since.
- Unscheduled at every level: the 16-task Mag* schtasks list (dumped this
  sitting) contains no cycle brief task, and a FULL scheduler sweep
  (Get-ScheduledTask over every task, actions matched on 'cycle_brief')
  returned zero hits. `grep -rln cycle_brief scripts/ tools/ main.py
  mag/` matches only the tool itself.
- Meanwhile the overnight rails DID run: descent driver beat cycle 1677
  at 2026-10-03T20:01:22Z (memory/runs/hermes_burn/driver.beat, pid 86854
  alive in `ps aux`, started Oct 2), arena cron left 38 playground dirs
  dated today (16 tavern_ + 22 dnd0_).
- Migration implication: the rails bank work all night, but the artifact
  the operator steers from in the morning is hand-run and 3 days old. A
  headless-first estate without a scheduled dawn report is an estate the
  operator steers by archaeology.

Falsifier: any CYCLE_BRIEF_2026100[1-3]* file appearing, or a scheduler
entry invoking cycle_brief, kills the "never had a second dawn" claim.
Move (~30 min): register MagCycleBriefDaily 07:30 EDT (the
census/fts/improve registration scripts are the in-repo pattern) with new
sections: driver beat age, arena bank rate, per-ledger day spend.

### F3: the sensor layer reads a nerve the rails never write

- tools/overmind_senses.py:8 and :64-67: sense_driver_beat, the
  overmind's "nerve-cord sense," reads state/shared_activity.jsonl.
- scripts/descent_driver.sh:26,31-32: the driver writes only
  memory/runs/hermes_burn/driver.beat and driver.log. grep for
  shared_activity across tools/hermes_burn.py, tools/ds_workhorse.py,
  mag/route_chat.py, descent_driver.sh: zero matches. The only
  shared_activity writers are mag/coordination.py and siblings - its
  latest rows are governor_autorun ticks, not rail work.
- So the loop organ (tools/overmind_loop.py: the SENSE->DECIDE->GATE->
  EXECUTE->VERIFY->LEDGER tick, $1 hard cap) senses a beat channel that
  carries no descent-driver rows: it would report a silent estate while
  the driver grinds at cycle 1677. The overmind has exactly one real run
  (memory/runs/overmind/ledger.jsonl: 45 ticks, 10-02, cumulative
  $0.0072, all STAGE_ASK) and it ran against the wrong nerve.
- Migration implication: the estate's autonomous steering loop and its
  autonomous work loop have never seen each other. Wiring them is
  cheaper than building either - this is the highest-leverage wiring job
  in the migration.

Falsifier: a shared_activity row with actor=descent_driver/hermes_burn,
or sense_driver_beat repointed at driver.beat, kills it.
Move (~15 min): append one shared_activity row per hermes_burn bank
outcome (actor=hermes_burn, status=ok/skip/fail) - the write site
already exists at tools/hermes_burn.py:149-157 (_bank).

### F4: the money books are two unjoined families and the front door is empty

- mag/route_chat.py - the "ONE front door" (docstring line 1) whose
  drop-in-table row promises "text, usage banked" - has a ledger of 6
  rows (memory/runs/route_chat/usage.jsonl), every goal a smoke test
  ("route_chat smoke v2", "nous failover smoke"). The legacy carriers
  hold 2,456 rows across four other ledgers: hermes_burn 1,152 /
  model_garden 725 / grok_free 576 / xai_grok 3 (wc -l census this
  sitting). STANDING_RAILS.md:46-48 registers the debt honestly
  (tavern/dungeon/hermes_burn/grok_burn still self-call).
- tools/cost_rollup.py:29-33 - the "one read-only rollup over every
  scattered cost surface" - scans logs/duel, logs/mates,
  logs/hermes_gopher_burn_*, training/cost_ledger: none of the
  memory/runs/*/usage.jsonl family. So the two freshest cost schema
  families (the rails the migration would run on) are invisible to the
  estate's one cash rollup, and no surface answers "what did today cost
  across rails" in one read. The hermes_burn lifetime number ($63.83,
  driver.log tail "HERMES-BURN: PASS - 28/28 asks; ledger total $63.83")
  lives only in a redirected log line.
- Migration implication: interactive ZCode compensates by having a seat
  hand-assemble spend per sitting; headless cannot. License-window
  economics (tokens-per-deliverable on the z.ai seat) make the flash-arm
  seat tokens unmetered in ANY of these ledgers - the seat's own burn is
  the biggest missing row in the estate's cash picture.

Falsifier: cost_rollup extended to memory/runs/*/usage.jsonl, or a
route_chat ledger carrying non-smoke production goals, kills it.
Move (~40 min): add the usage.jsonl schemas as cost_rollup surfaces and
pipe its one-line total into cycle_brief's quota section.

### F5: formal escalation surfaces are dormant, and the no-cancel law's replacement gesture is unwired

- queue/wait_human.md has been frozen since 2026-08-09 (one T0 janitor
  ask, 55 days unanswered; mtime Aug 9 06:51). queue/handoff/ newest
  entry 2026-09-29. The formal estate->operator escalation channels have
  carried no live traffic while every real escalation of the last week
  traveled as watch/inbox prose or attention.md lines.
- The interrupts-never-cancel law (queue/STANDING_RAILS.md:17-18) was
  minted today because the operator's steering GESTURE - the mid-turn
  interrupt - killed ~20 of 50 judge lanes (STANDING_RAILS.md:49-51).
  Headless removes the dangerous gesture, but its replacement is a file
  convention: the driver stops only when memory/runs/hermes_burn/
  DRIVER_STOP appears (descent_driver.sh:25,29). The plugin spec
  (watch/inbox/mag_rails_plugin_spec_20261003.md:10-24) exposes six
  tools - route_chat, stage_ask, arena_status, delta_register, gwap_bank,
  sacred_cow - and none of them stops, queries, or steers a running
  driver. mag_stage_ask drops work IN; nothing drops work OUT or HALTS.
- Migration implication: under headless, steering is the product. Today
  it is undocumented tribal knowledge (DRIVER_STOP), the formal channels
  for "I need a human" are dead letters, and the planned native handle
  is one-sided (feed in, no control out). A migration that lands without
  control-plane tools recreates the interrupt problem at a worse layer:
  the operator's only halt gesture would be killing processes.

Falsifier: a mag_driver_status/mag_driver_stop tool landing in the spec
and build, or post-migration traffic in wait_human.md/handoff, kills it.
Move (~20 min): add mag_driver_status (pidfile + beat age + last PASS/
FAIL line) and mag_driver_stop (touch DRIVER_STOP) to the plugin spec -
both wrap existing files, no new logic, per the spec's own build notes.

## Arena count note (the ask's own number, checked against bytes)

The ask states the arena cron ran "8 cycles today." At my moment the
playground dir held 38 cycle dirs dated 20261003 (16 tavern + 22 dnd0),
33 with GWAP_BANKED markers, 5 with DONE but no GWAP_BANKED (4 dnd0 + 1
tavern, listed by name this sitting). The 8 was likely true at ask
composition time; the cron kept firing. The 5 unbanked are not law
violations by the letter (law 4 counts DONE rows as receipts) but they
silently miss the gwap chain: "capability rows route the next ask's
dollars" (STANDING_RAILS.md:37-42) lost 5 inputs today with no alarm
anywhere. Bank-rate enforcement is the same communication hole as F1 in
miniature: DONE claimed in-band, downstream feed unenforced.

## Instrument note (a false dead that taught the lens something)

My first liveness check of the driver ran `tasklist //FI "PID eq 86854"`
- Windows returned no such process, and I nearly reported the driver
dead. `ps aux` in MSYS shows pid 86854 alive (bash, started Oct 2) and a
fresh beat (cycle 1677, 20:01:22Z) proves it: state/descent_driver.pid
holds an MSYS pid that Windows-side tools cannot see or test. Any
Windows-native monitor (a scheduled task, a PowerShell watcher) reading
that pidfile reads garbage. A headless-first estate monitored from the
Windows side needs either a Windows-visible pid receipt or a
beat-age-based liveness law (beat older than 2x cadence = down), which
is itself a dawn-report section (F2).

## Not run / OWED

- I did not run the overmind loop, cycle_brief, or cost_rollup to verify
  their outputs execute clean today - findings are from byte reads of
  code, ledgers, and file mtimes, not executions of those tools.
- I did not verify the arena cron automation-b1ce1342's definition (it
  lives outside the repo in ZCode automation config, not searched).
- I did not census non-attention.md alert channels for the 809 alarms
  (the same events may also land elsewhere; the census here is
  attention.md-scoped, instrument named).
- Token counts for the flash arm's seat burn (the unmetered money) were
  taken from the ask's framing, not re-measured - marked OWED to the
  economics lens.

## Blind spots

1. I cannot see what the operator actually READ. attention.md has no
   read receipts (the prior hostile pass named this too); I can prove
   what was emitted, never what was consumed. If the operator reads
   attention.md live in an editor, the noise cost is different from my
   model of it.
2. I read one 24h window (today) plus the 10-02 raction corpus. A
   quieter day might show the alarm channel at sane ratios; my 71% figure
   is a one-day census, not a distribution.
3. Hermes-side surfaces (the dispatch log, $220 armed, warm boot) were
   not examined - if Hermes already carries a dawn-report or escalation
   shape, findings F2/F5 overstate the gap. OWED to whoever holds the
   hermes_routing.json surface.
4. The four other ractor lenses may already cover the scheduling gap
   (F2) from the operations lens; I did not read their cards before
   writing mine, so convergences beyond the one flagged CONVERGENT are
   unmarked.
5. I evaluated the plugin spec as written, not any implementation - if
   a mag_driver_* tool is already drafted somewhere outside the spec
   file, F5's "unwired" claim narrows to "unspecced."
