# MOONSHOT-2 (wild-eye lens) on the surface-migration question, 2026-10-03

Schema: ractor.lens.v1 · lane: moonshot-2 of the 2026-10-03 surface-migration fire ·
all evidence personally read or run this sitting; ask-material numbers that I could
not re-derive from repo bytes are marked OWED, never asserted.

Topic: SHOULD THE ESTATE MIGRATE ITS PRIMARY ORCHESTRATION SURFACE from interactive
ZCode sessions to Hermes-launched headless rails (GLM-5.3-max via the Nous API
launching the standing workflows in headless agent surfaces like opencode)?

## VERDICT: HYBRID, with the rails-first inversion (and a sacred cow on the table)

The migration already happened by accident and nobody filed it. The estate's standing
work runs headless TODAY without any interactive seat: the descent driver is alive at
pid 86854 with driver.beat reading "BEAT 2026-10-03T19:30:08Z cycle=1676" and no STOP
file (tail read this sitting); the arena cron automation-b1ce1342 closed day 1 at
"$24.65 of the $25 cap, 10 dungeon + 12 tavern sessions, every one gwap-banked
chain-ok" (memory note arena-gwap-useful-shit-law-20261003, cycles 1-8 detailed);
drift-patrol runs daily as automation-a7c71ad1 (watch/inbox/DRIFT_PATROL_20261003.md:5);
MagImproveDaily / MagCensusPatrolDaily / MagFtsIndexDaily run on Task Scheduler
(AGENTS.md patrol bullets). What remains seat-bound is: steering rounds, judgment
courts, 50-wide Task-agent waves (the main-session retry path is the transport that
survived, watch/inbox/burn_claims_50wide_20261003.md:33-40), and the operator
relationship itself. So "migrate the surface" is the wrong axis. The right move:
name the rails the primary orchestration surface (they already are), demote the
interactive seat to steering console + wide-wave executor + judgment court, and do
NOT adopt an opencode-style external agent surface as primary, because the estate
already owns every organ a headless loop needs and proved it once: tools/overmind_loop.py
(SENSE -> DECIDE -> GATE -> EXECUTE -> VERIFY -> LEDGER, $1 cap, chain-sealed ticks,
docstring lines 1-22) ran 45 ticks on 2026-10-02 for $0.0072 cumulative (memory/runs/
overmind/ledger.jsonl, 45 rows, verbs 35 STAGE_ASK + 10 NOOP, last ts 01:58:35Z) and
was then left dark. The loop exists. The migration question re-litigates a build the
estate already landed and abandoned.

If an opencode-style surface is still wanted, it enters only as a rail CONSUMER:
no executor reads .env; everything funnels through mag/route_chat's fence (the
mag-rails spec already states the boundary: watch/inbox/mag_rails_plugin_spec_20261003.md:47
"the plugin never holds keys; route_chat reads .env/lane config as today").

## FINDINGS

### F1 (accuracy/logic, sharpest): the migration's scoreboard does not exist in bytes

The Frontier Delta Register on disk (watch/inbox/frontier_delta_register_20261003.json)
holds 14 rows whose every field is frontier_chars/cites/unver and flash_chars/cites/
unver plus contract_parts (I parsed it this sitting; the full key set is printed in my
session log). There is NO verdict column, NO win-rate, NO cost column, NO deepseek arm.
The judge pass it needs is admitted incomplete: queue/STANDING_RAILS.md:49-50 "the Delta
Register judge pass completes (30/50 lanes landed, ~20 killed by the interrupt before
the no-cancel law landed)". The ask-material figures "39 judged lanes" and "frontier
beat flash only 8-5" are OWED: I found no file carrying them. The ask's own arithmetic
does not reconcile: replay_flash holds exactly 13 deliverables (ls this sitting) and
13 x ~582K = 7.57M, not 9.5M. And the model the thesis names does not exist on the lane
it names: configs/providers.yaml:150-161 defines the nous lane with z-ai/glm-5.3-prime
and qwen3.8-max-prime; "5.3 max" appears only as the off_hours z_ai routing hint
(configs/off_hours.yaml:71, model glm-5.3). Routing the estate's dollars on this table
today is astrology with a ledger costume.
Falsifier: a register v2 with judge-verdict and per-arm-cost columns lands, or a
receipt reproduces the 39-lane / 8-5 census from named instruments.
Move (~45 min): finish the judge pass on the ~20 interrupted lanes (re-fire is
admitted cheap), add verdict + cost_usd columns sourced from memory/runs/hermes_burn/
usage.jsonl and the seat-side token figure banked at landing, and mint register v2.

### F2 (dogfood/operations, the strongest single fact): the headless loop is built, proven one hour, and dark

tools/overmind_loop.py IS the Hermes-question answered in python a day before it was
asked: a fail-closed verb table, sanctioned surfaces only, read-back verify,
hash-chained ledger, hard cap checked per dispatch, "ONE glm-flash loop-hour
unattended" as its own falsifier (docstring lines 3-22). The ledger proves the hour
ran (memory/runs/overmind/ledger.jsonl, 45 rows, cumulative_usd 0.0072, 2026-10-02
01:00-01:58Z). Nothing fired it since. Meanwhile the estate keeps hand-rolling
loop-shaped one-offs: descent_driver.sh (bash while-loop, cycle 1676), the arena
automation, two mag orchestrators (mag/afk_orchestrator.py, mag/desk_orchestrator.py),
and now a proposed opencode surface that would be a fifth executor with unknown claim
semantics. The claim locks those executors need were minted yesterday
(tools/instance_guard.py: claim_process exit-3 singletons, O_EXCL claim_ask at the
fire path, doubled_key ingest tripwire; docstring lines 5-22) and are wired into
hermes_burn, ds_workhorse, wave_driver, run_stealth_driver, run_autorun_loop
(state/CURRENT.md:47-49).
Falsifier: overmind_loop re-fired for 24h under the cap law stalls within hours of
the interactive seat dying, or its NOOP rate exceeds ~80% because the verb table
cannot express the drop-in table; either result kills the rails-kernel verdict.
Move (~90 min): wire the loop's DECIDE ask through route_chat (it currently names
the model_garden rail), stage the drop-in table's rows as verbs, and run the 24h
falsifier from a cron so the proof does not depend on a live seat.

### F3 (operations/communication): the headless estate's only alarm channel is 71 percent wolves

memory/attention.md is 1,137 lines and 809 of them are INSTANCE-GUARD doubled-key
false alarms (grep -c this sitting), all minted 19:04-19:08Z today, one per tavern
fire. Root cause is byte-true: tools/tavern.py:157 emits f"TAVERN_r{rnd}_{p['name']}"
while its own docstring line 10 promises TAVERN_<run>_r<round>_<actor>; the run id is
dropped, so every replayed round re-collides on banked ids and the tripwire fires.
The hermes-economics lane handed this exact defect forward this afternoon
(watch/inbox/dd_dogfood/hermes-economics.md:96-104: "809 of 1,150 ledger rows carry
doubled_key: true and 809 false INSTANCE-GUARD alarms spam memory/attention.md ...
the ingest tripwire is blinded by false positives"). A headless-primary estate lives
or dies by this channel; today an operator reading attention.md cannot see a real
alarm behind 809 wolves, and every migration (more unattended lanes) multiplies the
channel's load while its signal is zero.
Falsifier: fix the tag to include the run id; if doubled-key alarms still fire on
new rounds, the collision diagnosis is wrong.
Move (~20 min): add the run id at tools/tavern.py:157 and the dungeon twin, then
fold or quarantine the 809 rows out of attention.md so the channel reads clean
before any widening.

### F4 (economics): the meters invert the thesis; migrate ask classes, not surfaces

Bytes from this sitting: the hermes ledger lifetime is $64.05 over 1,152 rows, of
which $25.9998 (40.9 percent) was quantified waste, goodput $37.58, cost per usable
finding $0.49 gross / $0.29 productive (independently re-summed day/channel/id this
sitting; the audit's numbers confirmed at watch/inbox/dd_dogfood/hermes-economics.md:
13-22). Today's single-pass design asks cost $0.59-0.78 each at 37-72K tokens
(register ids in usage.jsonl: BARFIGHT_spec 37,475 tok $0.59, THE_ROOM_REMEMBERS
71,015 tok $0.78, PARTYCHAT_spec 71,671 tok $0.69). The arena bought 22 play sessions
for $24.65 cash. The seat arm: 50 independent byte-checks for ~1.5M subagent tokens
and "$0 cash (seat tier)" (watch/inbox/burn_claims_50wide_20261003.md:40), and the
seat quota is a fixed window already being maxed (109.4M tok/h at width 10 per
AGENTS.md). So: wide verification work is cheapest on the quota license; single-pass
judgment asks are cheapest on Nous cash; agentic flash loops (~582K window tokens per
deliverable, ~16x a single pass per the ask material, OWED as an exact figure) are
the most expensive shape on every meter and should be reserved for asks single-pass
provably fails. Cash cannot buy the seat's window back; the window cannot do
unattended cadence. Each meter owns an ask class.
Falsifier: a judged week where rails deliverables per cash-dollar beat seat-window
deliverables per quota-token on the same ask classes; or the inverse for the wide class.
Move (~30 min): mint the Delta Register cost column from both ledgers (hermes rows
carry cost_usd natively; the seat arm banks its window tokens at landing time), so
every future routing row carries both meters by construction.

### F5 (security/lineage): a headless primary inherits a 55-key .env with a 16-day unblinded-past and one fence

.env is gitignored (git check-ignore confirms) and carries 55 assignments including
HERMES_API_KEY_1/2 (the failover chain route_chat reads) and existing OPENCODE /
OPENCODE2 slots, meaning opencode surfaces are already half-wired for keys. The
estate's own history: 7 live keys sat in HEAD for 16 days, found by an EXTERNAL audit,
rotated and purged and gated in one day (watch/inbox/DAY_SYNTHESIS_20260930.md
section 1); the pre-commit secret gate caught a third-party Stripe key in a root
scrape TODAY (watch/inbox/DRIFT_PATROL_20261003.md:28-30, "three catches in three
days, all third-party"). The single fence standing between the rails and that blast
radius is route_chat's endpoint fence plus hermes_burn's (mag/route_chat.py:71-79;
tools/hermes_burn.py fence block around lines 91-110). Every additional headless
executor that reads .env directly is a second unobserved process holding all 55 keys.
The lineage answer the ask wants: the VS-Code-era interactive surface solved key
custody by keeping a human in the loop for every call; headless removes the human, so
the fence becomes the custody. One door or many doors is a security decision, not a
style choice.
Falsifier: any fire from a proposed surface that touches an endpoint outside the
providers.yaml allowlist; route_chat's fence raises on it (mag/route_chat.py:73-79),
a hand-rolled carrier would not.
Move (~25 min): write the boundary as law row 5 in queue/STANDING_RAILS.md
("no executor reads .env; all model calls ride route_chat or name a written fence
reason", generalizing registered debt item 1), plus a ratchet check that fails any
NEW file under mag/ or tools/ opening .env outside route_chat's _keys_for
(tools/violation_ratchet.py plumbing already exists).

## THE CIRCULARITY, named (logic lens)

"The estate outgrew the interactive surface" is currently unfalsifiable as stated:
its supporting evidence is that the estate built headless rails, but building the
destination is not evidence the origin failed. The falsifiable cores that WOULD
decide it, none yet banked: (1) a census of interactive-seat casualties that queue
behind seat death (the 20 interrupt-killed judge lanes and the maxAttempts-0 workflow
children are the only banked casualties so far, both operator-interrupt or
dispatch-shape kills, not seat unavailability); (2) a fired opencode arm losing to
the rails arm on the same 14 asks. Until one exists, the honest verdict is the one
the bytes already support: formalize what runs, steer from the seat, judge from the
seat, and let the loop organ eat the cadence.

## WHAT STAYS INTERACTIVE AND WHY

Steering rounds (revision.md is the headless analog and it exists, mag/hermes_steering.py
cmd_steer at :262 with the A1 steer-seal gate, 31 steer rows banked in
memory/runs/hermes_dispatch_log.jsonl, 119 rows total, 88 exit 0 / 29 exit 1, a 75
percent reliability carrier too weak to be primary), judgment courts and judge waves,
50-wide Task-agent waves (the retry path rides the main session; workflow children
maxAttempts 0 die on first contact per the width law), sacred-cow probes, and the
delight surface: the operator's verdict on the headless arena arc was "i have no idea
what is happening and i love it" (arena memory note), which is a communication product
only the steering seat composes. The dawn-report shape already exists and is stale:
tools/cycle_brief.py built the steering surface v1 on 2026-09-30
(watch/inbox/CYCLE_BRIEF_NEXT.md, animal profiles + doctrine scorecard + quota HOLD/GO
+ climb queue); nothing has regenerated it in 3 days. That staleness, not a new agent
surface, is the actual communication gap.

## FALSIFIERS FOR THE HYBRID VERDICT (collected)

1. Rails-kernel: 7 days of driver.beat + a 24h overmind re-fire with zero interactive
   sessions alive, deliverables passing gwap banking; if cadence stalls within hours
   of seat death, the seat is load-bearing and this verdict collapses to stay.
2. Opencode-flip: an opencode-headed arm beats the rails arm on the same 14 judged
   asks (complete deliverables, gwap verdicts, cost per deliverable under $0.29) over
   N >= 3 replays. Not run; nobody has fired the comparison, which is why the
   migration thesis is presently unfalsifiable.
3. Communication: if a cleaned attention channel plus a daily cycle_brief still
   leaves the operator disoriented (the 10/1 marathon-disorientation register vs the
   10/3 delight register is the A/B already banked), headless scale-up is premature
   regardless of cost.

## Blind spots (honest)

- I did not probe provider credit balances or fire any paid call this sitting; all
  spend numbers are ledger re-sums, not API truth. The "$220 armed" figure remains
  three-coexisting-prose (prior economics lens, ractor-topic/economics.md Finding 4).
- The seat arm's 9.5M window-token figure is OWED: no repo ledger meters z.ai seat
  window tokens that I found; my 13 x 582K arithmetic tension with the ask's total
  is flagged, not resolved.
- I read no opencode source: what its claim locks, logging, and telemetry paths
  actually do is unverified; F5 reasons from the estate's own history, not from
  opencode bytes.
- The 39-lane / 8-5 Delta Study figures and the deepseek thinking-on re-run status
  ride in the ask; I verified the register's 14 rows and the interrupted judge pass,
  not the study's headline score.
- I ran no pytest and no gate end-to-end; this sitting's instruments were python
  ledger parses, file reads, grep, git check-ignore, and one ls-based census.
- The desearch arm: replay_deepseek_thinking holds 4 files to flash's 13; I did not
  verify why (cap said 6000 chars, ask says re-runs pending) beyond the file counts.

Filed by moonshot-2, surface-migration fire of 2026-10-03. No em-dash bytes.
