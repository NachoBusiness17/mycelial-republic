# OPERATIONS LENS - surface migration raction (2026-10-03)

Lens: how the work was actually run today. Question under raction: migrate the
primary orchestration surface from interactive ZCode sessions to Hermes-launched
headless rails. Every number below was read or computed in this sitting; nothing
is hand-copied. Instrument named per claim per the quantifier law.

## THE HEADLESS ESTATE ALREADY EXISTS (dogfood leg is proven, not pending)

Instrument: `cmd //c "schtasks /Query /FO CSV"` piped to `grep -i "mag"` this
sitting: 16 Mag-owned tasks registered, 14 state Ready (MagCensusPatrolDaily,
MagFtsIndexDaily, MagImproveDaily, MagVisionNightly, MagXRadarDaily,
MagSecretScanWeekly, MagGapSentinelDaily, MagGateCanaryDaily,
MagQCaptionVerifyDaily, MagTipWitnessDaily, MagCorpusRescanDaily,
MagEndpointNewsDaily, MagLeaveProtocolDaily, mag-docker-watchdog; MagLabKit8765
and MagPrivateOffice8765 Disabled). On top of those: the descent driver is live
RIGHT NOW (state/descent_driver.pid reads 86854; driver.beat last lines
`BEAT 2026-10-03T18:27:45Z cycle=1674` / `19:30:08Z cycle=1676`, 2,740 beat
lines total), and the arena cadence spawned 38 paid play run dirs today under
watch/inbox/playground/ (16 tavern_ + 22 dnd0_, counted by
`ls | grep -c`). So the migration debate is not "whether headless works" -
most of the estate's bytes already move without the seat. What the seat added
today was exactly the headless-mode repair layer: the interrupts-never-cancel
law (queue/STANDING_RAILS.md:17-18, after ~20 judge lanes died mid-turn,
STANDING_RAILS.md:49-50) and the twin-drain cure (tools/instance_guard.py:4-10,
born from $25.53 of $37.76 re-fire excess in the dogfood-48h window).

## FINDING 1 - identity-collision re-fire is 61% of today's paid ledger, one day after the cure landed

Census this sitting: memory/runs/hermes_burn/usage.jsonl carries 1,152 rows,
809 with `doubled_key: true`. Today's rows split $15.26 doubled vs $9.85 clean
(awk sums over `grep 2026-10-03` cost_usd fields). Mechanism verified in bytes:
tools/tavern.py:157 and :174 build the ledger id as `f"TAVERN_r{rnd}_{actor}"`
and `TAVERN_r{rnd}_JUDGE` - no session-unique component - so every cron-fired
session re-pays the same (id, turn) keys. The docstring's no-replay law
(tavern.py:18, "a run dir with DONE never replays") is per-run-dir and each
fire creates a fresh timestamped dir (tavern.py:81-84), so it never triggers
across fires. The ingest tripwire (tools/hermes_burn.py:149-156,
doubled_key_check) flags only AFTER the paid call returns; it cannot refund.
The guard sweep (state/CURRENT.md "swept to 5 surfaces": hermes_burn,
ds_workhorse, wave_driver, run_stealth_driver, run_autorun_loop) never touched
the play carriers - instrument: `grep -n "instance_guard\|claim_ask\|
guard_or_exit" tools/tavern.py tools/dungeon.py tools/arena_gwap.py` returned
zero hits this sitting. Per-ID inflation: 665 TAVERN ledger rows today over 70
unique TAVERN ids (~9.5 fires per id; r1 alone has 105 rows). This is the
founding twin-drain disease recurring through the estate's MOST headless rail.
The migration thesis inherits this: headless width multiplies until identity
is unique-per-fire and claims are taken BEFORE the call, not alarmed after.

Falsifier: scope a session-unique prefix into tavern/dungeon ids and re-census
tomorrow - if the doubled share collapses below ~5%, the mechanism stands; if
doubled rows persist while no tavern session fires, my attribution is wrong.

Move (one sitting): prefix ids with the run stamp that already exists at
tavern.py:81-83; same for dungeon.py:180. Three lines plus a census re-run.

## FINDING 2 - the alarm surface is flooded 809-deep and pre-acknowledged; a headless estate would be flying blind on its one escalation channel

memory/attention.md holds 809 "doubled-key alarm" lines (grep -c this
sitting), 815 lines mentioning today. The tail shows 30+ alarms in the single
19:04-19:08Z window, and the alarms did not stop the bleeding: tavern kept
re-firing from 11:39Z to 19:08Z while they accumulated. Worse, the alarm
writer pre-checks its own box: tools/instance_guard.py:203 writes
`- [x] INSTANCE-GUARD doubled-key alarm ...` - an alarm born already
acknowledged. And the channel head shows probe alarms pointing into test-run
temp trees (agents/pytest-tmp-54164/... and AppData/Local/Temp/suite-burn-*)
- pytest leakage writing into the estate alarm surface, i.e. test noise and
money alarms share one undifferentiated channel. The dawn-report steering
shape the migration assumes presumes this channel works. Today its
noise-to-action ratio is effectively infinite: zero of 809 alarms produced a
same-day fix (the fix would have been a 3-line id change; it has not landed).

Falsifier: if an attention.md sweep/ack consumer exists that I did not find,
the flood is being processed and this finding overstates. I searched tools/
and scripts/ for a consumer and found none - searched, not exhaustive.

Move (one sitting): in doubled_key_check, collapse repeats to one row per
(ledger, id) per hour with a count, and emit `[ ]` not `[x]`.

## FINDING 3 - the one front door has no traffic: 6 rows, all smoke tests; and the door itself carries no re-fire protection

memory/runs/route_chat/usage.jsonl read whole this sitting: exactly 6 rows,
all from today 16:44-18:49Z, goals "route_chat smoke" / "smoke v2" / "smoke
v3" / "nous failover smoke". The door mag/route_chat.py declares itself the
only call path (route_chat.py:1-9) and STANDING_RAILS.md:46-48 registers the
debt that tavern/dungeon/hermes_burn/grok_burn still self-call - confirmed:
every one of today's 1,152 paid hermes rows went through hermes_burn._call,
not the door. Operational gap the drop-in table hides: route_chat._bank
(route_chat.py:82-85) appends rows plain - no doubled_key_check, no ask
claim, no landed-skip (those live in the hermes_burn ask flow,
hermes_burn.py:206-227). The table sells `mag.route_chat(lane=, goal=)` for
"any one model call" (STANDING_RAILS.md:26); a wide wave of direct calls
through it would reintroduce double-pay with no tripwire. The MAG-RAILS
plugin spec (watch/inbox/mag_rails_plugin_spec_20261003.md:10-13) makes this
door THE default tool - wiring the harness permission system in front of an
unexercised, unprotected door.

Falsifier: a week of route_chat rows from production carriers falsifies the
no-traffic claim; adoption without doubled_key_check landing first falsifies
the gap claim (harmlessly).

Move (one sitting): port doubled_key_check into route_chat._bank, then point
grok_burn (the smallest self-caller) through the door per the one-per-sitting
debt rule.

## FINDING 4 - win32 headless traps are live debris, already needing device-path surgery

A literal `nul` file sits at repo root right now: `ls -la ./nul` reads 127
bytes, mtime Oct 3 14:41 today; `cat ./nul` prints
`ls: cannot access '.../watch/inbox/dd_dogfood/': No such file or directory`
- a `2> nul` redirect executed under Git Bash, where nul is a plain file, not
the Windows device. tools/estate_cleanup.py:19-24 documents the cost: the
file cannot be removed by os.remove (Win32 resolves dir\nul to the NUL
device) and needs `cmd /c del \\.\C:\...\nul` device-path syntax, plus
scandir-not-os.path.exists for its existence checks. The same class leaks
test trees into the repo (agents/pytest-tmp-54164/ visible in alarm paths,
agents/b2_522_tmp in `ls agents/`). Each additional headless rail multiplies
script-hours under shells whose nul/dev/null semantics differ; nobody is
watching when the debris lands. Note: dd_dogfood appeared in my first
watch/inbox listing and was gone when probed later - the tree moved under
this audit; unresolved, marked OWED, not asserted either way.

Falsifier: if `nul` reappears at root after the next estate_cleanup pass, a
live generator script exists and this is a source-fix item, not debris.

Move (one sitting): grep scripts/*.sh and tools/*.py for `> nul` / `2> nul`
redirects and subprocess arg lists, convert to /dev/null, name the generator
in the fix comment per the build-discipline law.

## FINDING 5 - headless silent-green is the real migration risk: ok:true rows with content_chars:1 banked at $0.25, caught only because a human-class reader scanned the ledger

Ledger row read this sitting (memory/runs/hermes_burn/usage.jsonl tail):
`{"ts": "2026-10-03T19:25:23Z", "id": "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003", "model": "z-ai/glm-5.3-prime", "finish_reason": "length", "channel": "reasoning-dump (content stub; raw reasoning banked)", "cost_usd": 0.2502604, "ok": true, "content_chars": 1}`.
ok:true, one content char, $0.25 - the reasoning channel ate the whole
max_tokens budget and the deliverable is a stub. The recovery (STAGE_B row at
19:33Z, $0.21, finish stop) happened only because something re-fired the ask
by hand-shape. No instrument in the fire path raises on green-with-empty
content: hermes_burn banks ok from the HTTP shape, the same hollow-batch
shape STANDING_RAILS.md:13-16 declares VOID for batches. On the interactive
seat, a seat scanning the transcript catches this class within minutes; in a
migrated headless world at 3x the width, silent-green rows are the default
failure and the dawn report is the only net. The GALA row is one instance
caught today; the register JSON (watch/inbox/frontier_delta_register_20261003.json)
also carries a flash arm with `flash_chars: 0` (SUBSTANCE_gaming_corpus) -
another empty deliverable banked into a judged comparison, which means the
routing table's denominators themselves are polluted by silent-green rows.

Falsifier: a headless week where the dawn-report (no mid-day seat) surfaces
every content_chars<=1 row at fire time would falsify the "detection is
post-hoc only" claim.

Move (one sitting): in hermes_burn._bank, flip ok to false and alarm when a
row claims ok with content_chars <= 1 (or channel reasoning-dump with a
content stub), so the class can never bank green again.

## VERDICT-BEARING OPERATIONS SUMMARY (for the synthesis lens)

The bytes support HYBRID with a hard precondition order, not a clean migrate:
headless already carries the recurring load (14 tasks, driver at cycle 1676,
38 play sessions today) and the seat's irreplaceable contribution today was
headless-failure repair (interrupt law, twin-drain cure, nul surgery,
silent-green catches). Migrating the primary surface before findings 1, 2 and
5 land would multiply the exact failure classes the seat keeps hand-mopping:
identity collisions scale with width, a flooded alarm channel scales with
cadence, and silent-green scales with every new unattended fire path.

## OWED / NOT RUN

- automation-b1ce1342's own definition: not found in-repo. Instrument:
  `grep -rl "b1ce1342"` over memory/ queue/ watch/inbox/ state/ docs/
  configs/ tools/ mag/ scripts/ returned zero hits (scoped search, not
  whole-tree; a whole-tree grep was started and killed for time). The "8
  cycles today" figure in the raction brief is therefore taken from the ask,
  not verified against the automation's log; I verified effects instead (38
  run dirs, 665 tavern rows). A ~/.zcode deep grep was also killed for time;
  a top-level listing of C:/Users/foste/.zcode (cli, v2, workspace, skills,
  tmp, plugin-workspace) shows no automation store at the surface, so the
  cron's definition bytes remain UNVERIFIED, effects-only.
- The flash replay arm's 9.5M-seat-token / ~582K-per-deliverable figures come
  from the ask brief; I verified the 13 replay_flash deliverable files exist
  (ls count) but found no in-repo receipt carrying the token total.
- opencode/Hermes-launch surface internals: nothing read; all claims about
  what a new surface adds or breaks are inherited from the brief, not
  verified here.

Filed by the operations lens, 2026-10-03. Zero em-dash bytes.
