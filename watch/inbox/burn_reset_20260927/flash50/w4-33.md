# w4-33: The Dream Cycle of the Estate (deep design)

Item: "Deep research: the dream cycle of the estate. Design what happens during idle periods:
memory consolidation, pruning, replay, induction. When does it trigger?" Banked 2026-09-28,
burn wave flash50, seat burn-w4-33.

## 0. Method

Read this session: mag/state_snapshot.py, tools/pile_classify.py, scripts/day_end_pile.ps1,
scripts/register_day_end_task.ps1, mag/offpeak.py, mag/percolator.py, mag/meta_percolate.py,
mag/verkle_compaction.py, mag/registry.py (attach_cold_core), mag/accumulator.py,
mag/rib_bus.py, mag/hermes_warm_boot.py, scripts/vision_nightly.py, mag/doctor.py
(check_scheduled_tasks + SCHEDULED_TASKS), mag/improve.py (module docstring), plus
logs/day_end_pile.log, logs/fts_index.log, logs/improve_daily.log tails and the pile,
invariants, explore and noise data files. Live probes run this session: the full schtasks
census (below), file counts, and log tails. The ask's own material is the item text above.

## 1. Thesis

The estate does not need a dream cycle built. It needs its dream cycle RECOGNIZED, given one
coherent clock, and handed the two organs it still lacks (a replay cadence and a prune
cadence). Four of the five canonical dream stages already exist as shipped code:

| stage | estate name | code | wired to a trigger? |
|---|---|---|---|
| encode | state snapshot | mag/state_snapshot.py:75-106 | yes, event (session close, escalation) |
| consolidate | pile classify | tools/pile_classify.py | barely: 20:00 task specced 2026-09-28, NOT registered (probe below) |
| induce | percolator + meta_percolate | mag/percolator.py, mag/meta_percolate.py | no idle trigger; folds ride live traffic |
| prune | verkle compaction | mag/verkle_compaction.py | no cadence; plan-only by law |
| replay | simulate / falsifier | mag/cache_router.py:16,:177, mag/accumulator.py:1-13 | no cadence at all |

The estate even owns the word: mag/meta_percolate.py:6 calls the raw percolation input
"the liquid dream". The dream cycle is the pump that keeps the liquid moving while the seat
sleeps. What follows is circadian architecture, not new mechanism, because the estate's own
laws already dictate the dream's grammar: dreams propose, the operator disposes.

## 2. The measured substrate

### 2.1 Live scheduler census (ran this session)

Command: `schtasks //Query //FO CSV` piped through `grep -i mag` (double slashes because Git
Bash mangles single-slash switches). 12 rows. The Ready band, next fire times:

- MagVisionNightly 02:30, MagCorpusRescanDaily 03:30, MagEndpointNewsDaily 06:30,
  MagQCaptionVerifyDaily 07:30, MagImproveDaily 08:00, MagCensusPatrolDaily 08:30,
  MagFtsIndexDaily 09:00, mag-docker-watchdog 22:20, MagSecretScanWeekly Sun 06:40.
- MagLabKit8765 and MagPrivateOffice8765 exist but Disabled.
- `schtasks //Query //TN MagDayEndPileDaily` returned: "ERROR: The system cannot find the
  file specified." The day-end consolidation organ is UNREGISTERED, one day after landing.

Yet logs/day_end_pile.log shows the pipeline works: today 2026-09-28 15:00:27 a manual run
logged "CAPTURED True st-51de553794", then "pile=144 pending=1 classified_this_run=1
total_classified=144 errors=0", "END exit=0". So the consolidator ran once by hand, drained
the pile to 144/144 classified, and went back to sleep with no scheduler presence. The
estate's newest dream organ is dark on the clock that was built for it
(scripts/register_day_end_task.ps1 targets /SC DAILY /ST 20:00 and its header comment
explicitly slots it "after the working window, before the overnight free lanes, and disjoint
from MagImproveDaily 08:00 / MagCensusPatrolDaily 08:30 / MagFtsIndexDaily 09:00").

Logs confirm the morning band is alive today: logs/improve_daily.log "END exit=0" at
08:00:01; logs/fts_index.log "POST: exit=0 wall=0.637s" at 09:00:09 with
"deep: match" against catalog sha256 eb08f218...

### 2.2 Encode: the wake-time encoder

mag/state_snapshot.py capture_summary (:75-106) appends one structured row
(goal/outcome/tier/kind/lessons) to memory/pile/state_summaries.jsonl, deduped by a 16-hex
state_hash over (kind, tier, goal, outcome) (:71-72, :89-91). Kinds are fixed at :41
(session_end, escalation, run_close, autoaim, operator). This is encoding at the moment of
experience, deliberately cheap, "instead of re-deriving it later" (:9-10). Live pile: 144
rows, currently fully classified. The AGENTS.md Clippy block carries the habit law:
escalation/session-close -> capture_summary; overnight -> pile-classify.

### 2.3 Consolidate: the overnight classifier

tools/pile_classify.py announces itself as "the long overnight classification job" (:1) and
"designed to run during downtime: on the scheduler, a night task, or GitHub Actions" (:6-8).
Mechanics: pending = rows whose id is neither in classified.jsonl nor flagged classified
(:88-90); each row goes to a LOCAL model via tools.pupeteer_gauntlet.local_chat (:77-80)
under a strict-JSON system contract (:41-48); output folds into case law via
mag.skill_ledger.record_decision (:162-174) and appends a training row feeding train/prepare.py
(:177-184); the source pile gets an atomic rewrite flagging classified=true (:125-150, tmp +
replace at :147-149). Failure semantics are honest: rows that fail classification are listed
in errors, never silently dropped (:104-105, :121).

Note the tier economics: the classifier is gemma4, a local janitor, per the tier ladder and
the driving ladder (AGENTS.md): the funded specialist verifies, it never consolidates. The
dream runs at $0 by construction.

### 2.4 Induce: percolator and meta_percolate

mag/percolator.py's header (:1-27) is already an induction engine spec: sentences are
classified SIGNAL / THEATER / NOISE by a deterministic lexicon (SIGNAL_HINTS at :60+); noise
goes to the noise file; a canonical fingerprint seen before becomes a REPEAT and is
"compiled to INVARIANT (recurrence = stable truth worth compiling)"; a first-time signal is
NOVEL and lands in the explore queue (:10-19). Live counts, this session: 366 invariants in
memory/percolator/invariants.json (grep -c '"count":'), the top one ("deliberate ask: frozen
prefix + tight ask + output contract") at count 232214, first_seen 2026-08-30; explore.jsonl
at 1,669 rows / 1,703,827 bytes; noise files at 347,539 total rows, dominated by
ox_artifact.jsonl (114,478 lines). Two false-positive ledgers (behavioral.fp.jsonl,
ops.fp.jsonl) exist so a bust can be retracted, "a false positive is logged, never carried
forward as truth" (:25-27).

mag/meta_percolate.py (:1-11) inducts AGAIN: the top invariants percolate into a single root
invariant, a Merkle root over invariant hashes plus the deepest shared text, "turtles all the
way down". This is two-level induction: instance repetition -> law; law convergence ->
constitution.

### 2.5 Prune: compaction with a protected core

mag/verkle_compaction.py (:1-21) folds chain rows "whose session evidence is ALREADY GONE":
orchestrator-noise sessions whose knot file is absent (the dangling definition
mag/chain_guard.py:72 uses) into ONE counter leaf carrying a Merkle root over every folded
leaf hash. Rows whose knot still exists are KEPT and REPORTED; "deleting live evidence is a
separate operator decision, never a rider on this pass (the fossil-99 law: no silent partial
coverage)" (:9-13). The module ships plan-only, "apply(execute=False) writes NOTHING, no CLI
flag is wired here", execute waits on operator GO (Q-001) (:17-21). The counterpart that
makes pruning safe is mag/registry.py attach_cold_core (:121-125): the "core block that
amend cannot strip", Steiniger-shaped, protecting the residual seed. Prune therefore has its
full anatomy already: what may die (dead-evidence rows), what may never die (cold core), who
decides (operator), and what the grave marker looks like (a counter leaf with a hash chain
back to the victims).

### 2.6 Replay: three replayers, no stage

The estate replays in three registers. (1) Measurement: mag/accumulator.py's falsifier is
"stale-facts-per-100-turns vs a full-log baseline, replayed from room.jsonl traces" (:1-6);
its head stub returns {"value", "quiescent"} and :181 computes quiescent = abs(v) < 0.1,
explicitly "UNTRAINED placeholder". (2) Simulation: mag/cache_router.py "simulate() -
replay the log under the router" (:16), implemented at :177. (3) Verification:
mag/claims_desk.py replay (:117-147) rederives a state machine from an empty start to prove
each play's effect. And rib_bus knots are "durable, content-addressed, replayable" by
construction (mag/rib_bus.py:14-18), so the substrate is replayable even where no replay
function exists. What does not exist anywhere: a scheduled stage that calls any of these at
night.

### 2.7 The economic clock

mag/offpeak.py: weekday Beijing 09:00-12:00 and 14:00-18:00 is peak (2x); nights, the lunch
gap, and weekends are off-peak (:12-16, :43-49); defer_if_peak (:121-138) tells a cadence
tick to defer heavy NEW work, with MAG_ALLOW_PEAK as override (:127). The operator sits in US
Eastern, so the machine renders the windows in local time (:86-105). Two clocks therefore
coexist: the human circadian (the schtasks band) and the provider circadian (offpeak). The
deep observation: the economic clock CREATES the idle. Every heavy task that defers to
off-peak is a task that will be idle-waiting at 20:00 or 03:00, which is exactly when the
dream stages should run. Idle is not an accident the dream exploits; idle is scheduled
deferral, and the dream is the consumer of that deferral.

### 2.8 Wake

mag/hermes_warm_boot.py (:1-20) loads the verkle chain tip, deployment registry and session
brief into memory/warm_state.json at session start, "closes the Hermes forgets everything
between sessions gap". Paired with the freshness law (boot docs go stale at >7d while the
repo has a heartbeat, tools/freshness_check.py), waking is itself a gated protocol: load
ribs, load state, then act (AGENTS.md driving ladder). A dream cycle is only half a cycle
without a defined wake; the estate has one.

## 3. Theory: the estate's dream in the literature's terms

(These citations are from prior knowledge, not fetched this session; the code mappings are
first-hand. Flagged per the no-fabrication law.)

Complementary learning systems (McClelland, McNaughton and O'Reilly, 1995) says a fast
episodic learner and a slow statistical learner need interleaved offline replay to avoid
catastrophic interference. The estate's pair is verkle chain + pile (fast, append-only,
episodic) against the invariant registry + skill_ledger case law (slow, compiled,
semantic). The pile -> case-law fold is likewise the hippocampal-to-cortical transfer of
standard consolidation theory (Squire and Alvarez, 1995): episodic rows are re-coded into
generalized law, then flagged in place (:125-150 write-back) exactly as trace reorganization
frees the hippocampus.

Replay has a direct neuroscience referent: Wilson and McNaughton (1994) and Lee and Wilson
(2002) showed waking trajectories re-fire during slow-wave sleep. cache_router.simulate and
the accumulator falsifier are literally that: re-run recorded trajectories offline under a
changed rule set, and measure what the change would have done. The estate's version is
cheaper and sounder than generative replay (Shin et al., 2017): because everything is
content-addressed and append-only (rib_bus, verkle chain), it replays REAL traces
deterministically instead of synthesizing them.

Active systems consolidation (Rasch and Born, 2013) frames sleep as a coupled oscillator
driving transfer. The estate's spindle coupling is visible in the measured band: rescan at
03:30 produces the corpus state that FTS index at 09:00 then verifies "deep: match"; encode
all day, classify at 20:00, improve/census/FTS in the 08:00-09:00 window. The stages already
feed each other in order; only the ledger that says so is missing.

Synaptic homeostasis (Tononi and Cirelli, SHY) holds that sleep downscales weak synapses
while protecting strong ones. verkle_compaction + attach_cold_core is the same shape with a
legal frame: downscale dead-evidence rows, never touch the cold core, operator signs the
amputation. The design rule that falls out: prune by evidence-age (knot absent), never by
calendar. The estate learned this the hard way in the fossil-99 law's "no silent partial
coverage".

Threat-simulation theory (Revonsuo, 2000) claims dreams rehearse dangers cheaply. The night
band already does: endpoint news at 06:30, qcaption verify at 07:30, secret scan weekly, and
the B2-106 provider-health probe (mag/improve.py:21-28, cadence 7 days) that pings every
(base_url, model, key) triple and banks the classes QUOTA-DEAD / AUTH-DEAD / DEGRADED /
FENCED / REMOTE-UNVERIFIED. The estate dreams of its providers dying, then files the autopsy
classes before the operator's first coffee.

Day residues (Freud's term; Wamsley and Stickgold's finding that dreams incorporate recent
experience) map onto explore.jsonl: 1,669 novel signals, the day's unassimilated residue,
appended by every percolate call and drained by no idle habit. Ten modules reference
EXPLORE_QUEUE (grep: emergence.py, evolving_wave.py, fuel_feed.py, ghost.py, ladder.py,
lens_knot.py, orphan_sense.py, ox_percolate.py, ontology_compiler/extract.py, percolator.py)
but the drain rides live traffic, not a cycle. The residue grows while the dream that should
incorporate it is asleep.

Engineering twins worth naming: LSM-tree and Kafka log compaction, Postgres VACUUM, all
idle-time merges trading idle CPU for read health. The estate's distinctive move over all of
them is that its compaction units carry case law and invariants, not just key ranges, so
"dream output" is doctrine, not page layout.

## 4. The design: DREAM-1, a trigger architecture

### 4.1 Trigger taxonomy (the contribution)

The ask's real question is "when does it trigger". The estate already instantiates four
trigger classes; a complete dream cycle needs five:

1. EVENT: session close, escalation, run close (state_snapshot kinds :41; Clippy pile habit).
   Fires at the moment of experience; costs one append.
2. WALL CLOCK: the schtasks band, measured above. Disjoint slots are deliberate
   (register_day_end_task.ps1:1-5). Wall-clock triggers are for maintenance whose input
   arrives regardless (rescan, index, patrol).
3. ECONOMIC: offpeak defer_if_peak. Governs which waking work defers; the deferral queue IS
   the dream's ticket inventory. A deferred heavy job and a dream stage compete for the same
   idle hour; policy: local $0 dream stages never defer, funded work does.
4. PRESSURE: threshold-on-queue-depth, the corrective when a nightly run was not enough.
   Precedents: B2-465's FTS silt law (catalog outgrows index -> scan fallback -> daily task
   rebuilds through one sanctioned writer; "an exit 2 after a rebuild is an incident") and
   day_end_pile.ps1's attention.md alert on exit >= 2. Rule: any dream queue (pile
   unclassified, explore depth, foldable chain rows) gets a pressure threshold that fires the
   stage out-of-band rather than waiting for its slot.
5. QUIESCENCE: the missing class, with a stub already computed and read by nobody:
   accumulator.py:181 quiescent = abs(v) < 0.1. Generalize: a stage may fire when its input
   organ has had zero writers for N minutes AND no deferred funded work is pending. This is
   the only trigger that makes "idle" a first-class predicate instead of a guess from the
   wall clock, and the estate owns both halves (a quiescence function, and the writer
   registries it would watch).

### 4.2 The circadian layout

Measured band (live probe, next-fire times): 02:30 vision, 03:30 rescan, 06:30 endpoint
news, 07:30 qcaption, 08:00 improve, 08:30 census patrol, 09:00 FTS, 22:20 docker watchdog.
Proposed dream additions, each reusing an existing organ:

- 20:00 CONSOLIDATE: MagDayEndPileDaily, already specced in day_end_pile.ps1 (snapshot +
  drain, limit 50, gemma4, idempotent). Register it. Nothing new to build.
- ~04:00 REPLAY THEATER (new wiring, zero new science): after corpus rescan, run
  cache_router.simulate over the day's cache log and the accumulator falsifier over the
  day's room.jsonl traces; emit ONE receipt (rows replayed, projected savings, stale-facts
  delta vs the previous night). Plan-only: the receipt banks, nothing applies. This converts
  the estate's two orphan replayers into a nightly habit and gives the operator a daily
  counterfactual: "had yesterday run under today's rules, X would have happened."
- QUIESCENCE-GATED PRUNE: nightly verkle_compaction.plan(execute=False) appended to the dream
  ledger; alert only when the foldable count grows week over week; execute remains
  operator-GO, monthly at most. Prune by evidence-age, never calendar.
- THRESHOLD-GATED INDUCE: on any day where percolator compiled a new invariant or an existing
  invariant crossed a count boundary (say the next multiple of 1,000), rerun
  meta_percolate; if the root hash moved, append one attention.md line: "the root invariant
  changed from X to Y". A dream's entire nightly output may be one sentence. That is
  correct: dreams compress, and the estate's dream should report in its own currency,
  compression.
- DREAM LEDGER: watch/inbox/dream/YYYYMMDD.md, five lines (one per stage), each either a
  receipt or "not run: <reason>" in the cannot-verify grammar day_end_pile.ps1 already
  established (exit 2 = "ollama down, gemma4 missing, or pile unreadable", fix what the log
  names).

### 4.3 Laws the dream inherits (none invented)

- Idempotency or death: pile_classify skips classified ids (:88-90); vision_nightly.py:8-10
  is "idempotent by construction ... a complete corpus is an honest no-op". Every dream stage
  must be safe to re-run after a crash mid-night.
- Unattended crons do not error-spam: vision_nightly.py:17-18, "env not ready = clean skip
  receipt, exit 0".
- Cannot-verify is a named state: exit 2 + alert, never silence (day_end_pile.ps1 response
  block; B2-465 FTS grammar).
- Local janitors only: gemma4 class compute, $0; funded tier verifies (driving ladder).
- Plan-only default for anything destructive: verkle_compaction:17-21 is the precedent; a
  dream that deletes is not a dream, it is an incident.
- Self-announcing organs: "deliberate disablement is a known state: it must be announced at
  the seat, not only at doctor time" (mag/improve.py:6-8, t33/t73/t81 lineage).

### 4.4 Gaps, ranked

- G1 (open wound, one command): MagDayEndPileDaily unregistered. Fix:
  `powershell -ExecutionPolicy Bypass -File scripts\register_day_end_task.ps1`. I did NOT run
  it: it mutates system state (a scheduler registration), an operator/lane-scoped action; I
  ran read-only probes only.
- G2 (the doctor is blind in one eye): mag/doctor.py:1090 reads
  `SCHEDULED_TASKS = ("MagImproveDaily",)` - the silent-disablement probe watches ONE task
  while twelve exist. doctor.py:1141 already promises MISSING "is flagged as loudly as
  Disabled"; the fix is a tuple extension (plus generalizing the t47 intentional-disable
  marker beyond improve). Until then, eight dream organs can die silently and the estate's
  own alarm never sings. Today's G1 is the existence proof: the newest organ is already dark
  and no doctor check noticed.
- G3: no replay cadence: both replayers are functions without a habit.
- G4: no prune cadence: the foldable set only grows; plan() has no scheduled caller.
- G5: explore.jsonl (1,669 rows) has no idle-time drain that promotes old novel rows to
  invariants on repeat or to the FP ledgers on bust, even though both endpoints exist.
- G6: quiescence (:181) is computed and unread; wire it as class-5's gate.

## 5. What I did not run or verify

- The day-end task registration (G1): not run, system-state mutation, stated above.
- Any dream stage itself: pile is fully drained today (144/144 per the log), and the ask is
  design; running pile_classify or compaction plan() would have manufactured work to report.
- The neuroscience and CS literature citations: from prior knowledge, NOT fetched this
  session (this seat's earlier probes hit z.ai 1302 rate walls on web search, per the estate's
  envelope receipts; I chose not to spend the ask on a rate-limited fetch). All code, count,
  and schedule claims above are first-hand from this session's reads and probes.
- Counts are named with their instruments: invariants 366 via
  `grep -c '"count":' memory/percolator/invariants.json`; explore 1,669 rows / 1,703,827
  bytes via `wc -l` / `wc -c`; noise 347,539 rows via `wc -l memory/ghost/noise/*.jsonl`;
  schtasks census via `schtasks //Query //FO CSV | grep -i mag` (12 rows) at 2026-09-28,
  DESKTOP-7C70KSC.

## 6. Receipt

Banked as byte-identical twins: watch/inbox/burn_reset_20260927/flash50/w4-33.md and
watch/inbox/burn_reset_20260927/flash50/w4-dream.md (the ask named both paths). Em/en dash
and nonascii scan via the repo venv python after write; result recorded in the bank note.
