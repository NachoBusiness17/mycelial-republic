# LINEAGE - surface migration raction (2026-10-03, lens lineage)

Run: ractor_engine / 2026-10-03-surface-migration. Topic: migrate the primary
orchestration surface from interactive ZCode sessions to Hermes-launched
headless rails. My jacket: reinventing the estate's own forgotten ideas. What
prior generations asked that was never delivered, and what this wave dropped.
Everything below either ran this sitting (command named) or is marked carried.
No em-dashes.

## Finding 1 - the estate attempted this exact migration on 2026-09-03 and the flagship door was BLOCKED by a named three-part defect; the blocker's source is vendored in-repo

mag/seat_dispatch.py:141-162 is the T1 VERDICT of 2026-09-03 on `zcode-cli`
headless: BLOCKED, with the evidence chain reproduced in the comment (parser
rejects --max-turns/--settings though --help lists them; model.main must be a
"provider/model" STRING, object form silently stripped by the zod schema;
builtin:zai-coding-plan resolves only inside the exe runtime, config overrides
never reach requireRuntimeModelConfig, throws "missing baseURL"). The comment
names the reopen routes: "ZCode Protocol app-server stdio client (build), or
the CLI update that ships the headless runtime builder." The raw material for
leg one is already in-house: my sample of dashboard/data/ESTATE_INDEX.jsonl
rows matching "zcode-cli" returned paths under
corpus/library/zcode-zai-org/repo/apps/zcode-cli/ (the CLI source vendored as
library corpus; 1,520 index rows, all corpus paths, zero dispatch receipts).
Meanwhile the sibling doors from the same 09-03 generation sit armed:
`opencode` seat (seat_dispatch.py:135-140) and `claude-zai` (:121-134, with
--dangerously-skip-permissions at :132), and the 08-26 briefing declared
opencode THE compliant door at $0.013-0.019/task with 98-99.4% cache
(handoff/GLM_CODING_PLAN_BRIEFING_20260826.md:63-69, 89-90, "Use it"). My
readiness probe this sitting: `.venv/Scripts/python.exe -m
harness.opencode_coder --ready` -> {"opencode_cli": true, "zai_key": true,
"zai_key_2": true}. The door the migration debate proposes already exists,
tested, keyed, and is not a rail.

Falsifier: a post-09-03 zcode-cli headless dispatch receipt, or a
STANDING_RAILS drop-in row naming opencode as a production path (my read of
queue/STANDING_RAILS.md:24-35 has no opencode row).

Move (45 min): grep the vendored source
corpus/library/zcode-zai-org/repo/apps/zcode-cli/ for
requireRuntimeModelConfig / "missing baseURL" and decide whether the 09-03
blocker is fixed in the current bundle; file the reopen verdict as a register
row (the reopen condition is already named in seat_dispatch.py:155-156).

## Finding 2 - the orphan pattern is on its fourth lap: every generation builds a headless coder organ, proofs it once, never registers it

Chain, each link checked this sitting: (a) O6,
watch/SELF_STEAL_GROK_ORPHANS_20260904.md (section O6): grok_build_coder
proofed 2026-08-26, verify step broken on cmd.exe quoting ("& was unexpected
at this time" -> ok:true/verify:false, the hollow-ok class), in no config,
disposition FOLD register-or-retire; my grep `rg "grok_build" configs/*.yaml
configs/*.json` this sitting returns zero hits, still unregistered 30 days
later. (b) harness/opencode_coder.py:1-23 built 2026-08-26, live today (probe
above), consumers = one test (tests/test_zai_burst.py:6-9 imports
is_handshake_noop) plus handoff/audit prose; the one queue item that planned
to use it, Q-032 "Swarm to Roblox Luau week-1 port via opencode headless on
bunny lanes" (queue/queue_index.jsonl:32), closed STALE-superseded 2026-09-30
when the Roblox lane died. (c) route_chat.py:3-9, TODAY's standing
correction, is the same disease one level up: "you have a pet model harness
and never use it by default... This module IS the call path." And the rails'
own debt table (STANDING_RAILS.md:46-48) admits tavern/dungeon/hermes_burn/
grok_burn still self-call one day after the front door landed.

Falsifier: any opencode_coder or grok_build dispatch receipt after 2026-09-04
in watch/inbox or memory/runs (my INDEX.json grep read one mention; trails
grep read zero).

Move (20 min): add the GLM-plan door to the STANDING_RAILS drop-in table as a
named row (opencode_coder, what you drop, what comes out), or mark it dormant
in configs with the O6-style reason. One column; the prior ractor's cure,
never executed, re-offered.

## Finding 3 - what the interactive seat solved that headless re-loses, per the estate's own receipts: gates, and headless already shows the un-gated failure classes

Three receipts: (a) secrets leak as a repeated class: the briefing's own
gotcha "we caught a live key in a dossier tonight"
(GLM_CODING_PLAN_BRIEFING_20260826.md:82-83); today's drift-patrol commit
49b8d85af excised a third-party stripe key from a root scrape; both model
doors parse .env by hand in-process (route_chat.py:63-67,
harness/opencode_coder.py:56-67), and every headless fire multiplies
receipt-writing surfaces. (b) the gate-killer flag is already in the fleet:
seat_dispatch.py:132 ships --dangerously-skip-permissions on the claude-zai
headless seat; the interactive seat's permission layer and rules of engagement
(docs/ZCODE_SEAT.md:36-40: inbox files are DATA never instructions, never edit
own credential config, operator picks tier per task) are enforced by seat
behavior, not code, and headless has no equivalent except the deterministic
law block in prompts. (c) unattended loops double-spend without claim locks:
the descent twins drained the shared paid queue for 12h, 13 (id,turn) keys
doubled, ~$1.16 excess
(watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md:68-74), and the pidfile
guard landed only after (scripts/descent_driver.sh:10-22). Today the guard
ALERTS but does not prevent: my read of memory/attention.md tail shows five
INSTANCE-GUARD doubled-key alarms 19:07:38-19:08:04Z today on TAVERN_r5
refires, "ledger usage.jsonl already rows... this fire is a re-fire"; the
ledger schema itself carries a doubled_key field (my schema census of
memory/runs/hermes_burn/usage.jsonl: 809 rows carry it) - doubles are marked
post-write, not refused pre-write. The interrupts-never-cancel law
(STANDING_RAILS.md:17-19) exists because the interactive surface's interrupt
killed ~20 lanes of the judge wave (debt row :49-50): that is migration
evidence FOR, and it cuts both ways - the interrupt is also the only live
kill-switch the unattended loops lack.

Falsifier: a 24h window with zero doubled-key alarms and zero refired
(id,turn) pairs would falsify the refire-continues claim; a receipt showing a
seat permission gate stopping damage an unattended loop took would falsify
"headless re-loses only gates it never had".

Move (30 min): dedupe-at-write in the hermes_burn banker (refuse an existing
(id,turn) unless a force flag), and a seat_dispatch refuse-on
-skip-permissions unless operator_go, mirroring route_chat.py:113-115's
dormant gate. Both are small diffs to existing writers.

## Finding 4 - the economics are measured in-house and cut BOTH ways; the meter the verdict needs does not exist yet

My re-sum this sitting: memory/runs/hermes_burn/usage.jsonl = 1,152 rows, 911
today (2026-10-03), $25.11 today, TAVERN (the play arena) $16.20 across 665
rows - the headless rails' largest burn is play, not design. The delta
register (watch/inbox/frontier_delta_register_20261003.json, my parse: 14
rows) reads frontier chars-wins 10-4, one flash zero-output
(SUBSTANCE_gaming_corpus), and on the design asks the flash arm carries MORE
citations and FEWER unverifiable claims than frontier (BARFIGHT 35 cites/1
unver vs 20/9; DND_module 44/1 vs 32/7; SUBSTANCE_48h_synthesis 44/4 vs
51/8) - the seat surface with live file access buys citation density at the
premium the ask prices (~582K seat tokens vs ~37K per single-pass deliverable;
the 9.5M total is carried from the ask, not re-measured: the artifacts carry
no token field, and replay_flash/SEASON_design.md:138 says so explicitly,
"DONE rows carry only spend_usd today; adding one is a season deliverable").
Denominator disease rides the headline itself: the ask carries "39 judged
lanes, 8-5", the register holds 14 rows, the rails debt says "30/50 lanes
landed" (STANDING_RAILS.md:49-50) - three instruments, no shared denominator,
the B2-216 class on the migration evidence.

Falsifier: banked per-deliverable token counts for the flash arm (the missing
field) that read under ~100K tokens per design deliverable at equal citation
density would collapse the 16x premium; a frontier win on citation density at
matched arms would collapse the seat-quality claim.

Move (45 min): add the tokens field to every DONE/usage row and re-cut the
delta register with cost-per-cited-claim as the column; that number, not
chars, is the verdict's input. The deliverable is already named in
replay_flash/SEASON_design.md:138.

## Finding 5 - the migration is partly settled in fact: 911 of today's 1,152 ledger rows are unattended fires, and the loop is alive

My reads this sitting: driver.beat tail `BEAT 2026-10-03T19:30:08Z
cycle=1676` (the ask's "past cycle 1600" is byte-true; ~31 min cadence on the
last three beats); 911 of 1,152 usage rows today are driver fires. The
estate's actual live shape is already hybrid: unattended rails grind play and
batches, the interactive seat steers and judges. The remaining win32 trap is
small but real: my first repo-wide rg this sitting errored "./nul: Incorrect
function. (os error 1)" - a reserved-name artifact at repo root that headless
sweeps trip on (os.stat('nul') reads 0 bytes; os.path.isfile false; device
name, not file). Any headless sweep fleet needs the reserved-name skip or
censuses silently lose the root.

Falsifier: a fresh `rg -l opencode` over the root without the nul error after
the reserved name is excised/skip-listed would confirm the instrument fix;
recurring sweep errors at root would confirm the class persists.

Move (15 min): excise or skip-list the nul reserved name in the drift-patrol
skip list, and add nul to the sweep tooling's ignore defaults.

## Lineage verdict (lens-scoped)

The bytes say the estate does not have a surface-choice problem, it has a
registration problem: it has built and proven the headless doors three times
(08-26 backchannels, 09-03 campaign seats, today's rails) and each generation
left the doors unregistered and re-derived them. The interactive seat's real,
unreplaced product is the gate layer (permissions, secrets hygiene,
interrupt-as-steering) and per-task tier judgment; headless already runs the
majority of fires and its named failure classes (claim locks, hollow-ok,
double-spend, refires) are all code-fixable at the writers. Lineage answer to
the verdict question: hybrid, but with the registration debt paid first -
register the existing doors as rails, port the two interactive gates to the
writers, then the "primary surface" question is a routing table row, not an
exodus.

## Blind spots (honest)

- The arena cron automation-b1ce1342 is not in-repo; its fires I verified via
  the usage ledger and attention alarms, but the automation definition is
  carried from the ask.
- The flash arm's 9.5M seat tokens are carried, not re-measured; no token
  field exists in the artifacts (that absence is finding 4's point, and it
  caps my check).
- The vendored zcode CLI source not yet grepped for the blocker fix; that is
  the move, not a completed check.
- opencode --ready is a readiness probe, not a live paid ask; I spent no plan
  tokens this sitting. Full pytest not run.
- I did not read tools/hermes_burn.py's writer line-by-line; dedupe-at-write
  absence is inferred from today's alarms plus the post-hoc doubled_key
  field, not from reading the writer.
- Nous balance, the $220 armed dispatch, and Hermes warm-state not queried
  live.
- The 66 claude-zai/openclaw-worker ESTATE_INDEX hits not classified; only
  the zcode-cli hits were sampled (all corpus paths).

## ERRATUM (hostile second pass, 2026-10-03, re-checked on bytes this sitting)

F1 CORRECTED. (1) Census fixed: my "1,520 rows, zero dispatch receipts" was a
3-row sample generalized; the true census is rg "zcode-cli" over
dashboard/data/ESTATE_INDEX.jsonl piped through rg -v corpus = exactly 2 rows,
both queue/handoff/zcode-cli/OUTBOX/ dispatch receipts (ext-b102db4055.md
2026-09-03T15:44:47Z, ext-93662b92a0.md 16:28:00Z), both status:failed, both
pre-verdict, and the ext-b102db4055 body IS the CLI help-text dump (lists
--settings and --max-turns), the raw reproduction of verdict defect 1.
(2) WITHDRAWN: "blocker source vendored in-corpus". My checks this sitting:
rg -c "requireRuntimeModelConfig" corpus/library/zcode-zai-org/ = zero hits
(exit 1); rg -l "missing baseURL" = one hit, an unrelated prompt-trajectory
tool (repo/apps/zcode-cli/tools/prompt-trajectory/src/record.ts); and the
INSTALLED runtime /c/Program Files/ZCode/resources/glm/zcode.cjs (14,820,968
bytes, mtime Sep 28 23:21, 25 days post-blocker) contains NEITHER string
(rg -c, exit 1). (3) Sharpened, not weakened: the documented reopen condition
(seat_dispatch.py:155-156) may already be met by the 09-28 runtime update and
no re-probe exists on record. (4) Upgrade verified: queue/handoff/claude-zai/
OUTBOX/ holds 53 receipts, all Sep 3 (newest 15:36 EDT), 52 status:done / 1
failed (ext-ff4c7670fe.md) - the headless agent-surface class was PROVEN on
09-03 itself and then abandoned for 30 days. Corrected reading: headless
rails are not unproven, they are proven-and-silenced; the flagship blocker
may have healed itself unprobed.

F4 CORRECTED. (1) Density framing withdrawn. My recompute this sitting
(json parse over watch/inbox/frontier_delta_register_20261003.json via the
repo venv): cites-per-1k-chars gives flash the win on 7 of 14 rows, frontier
5, ties 2 (MOUNTAIN 0/0, WILD_EYES 0.10/0.10); frontier remains longer (mean
19,998 vs 16,725 chars, chars-wins 10-4). What the premium measurably buys is
unverified-claim reduction: flash_unver below frontier_unver on 12 of 14 rows
(PARTYCHAT 6 vs 42, THE_ROOM_REMEMBERS 2 vs 37, SUBSTANCE_play_findings 3 vs
21). (2) Ledger re-summed: 995 rows today, $25.3534, TAVERN $16.2003 = 64.0
pct of today's bill (my earlier $25.11/911 was a moment read; the driver is
live). (3) The ~16x token premium stays carried-not-measured (no tokens
field; the ask's "39 judged lanes, 8-5" stays non-relocatable to the 14-row
register; the accuracy.md:63-83 cross-reference is carried from the hostile
pass, not read by me).
