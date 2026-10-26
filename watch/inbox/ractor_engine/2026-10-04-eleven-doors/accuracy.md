# ACCURACY LENS - the 11 remaining doors, byte-checked (2026-10-04)

Lens: accuracy (falsifier-hunter). Anchor bytes read this session:
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md (full, 320 lines),
watch/inbox/GWAP_INDEPENDENT_COP_20261004.md (full),
watch/inbox/NIGHT_SHIFT_20261004_CLOSE.md (full), state/CURRENT.md (full),
plus the code reads and command runs cited inline. Every claim below is
something I read or ran this session; anything else is named OWED.

## Finding 1: the "11 remaining" frame is stale by two doors, verified live

Door 2 (arena-bench CI tripwire) LANDED while I was checking it: HEAD moved
from bb0f34586 to 00cb15c77 mid-session. I ran the instrument myself:
`.venv/Scripts/python.exe mag/arena_bench.py --selftest` exits 0 with both
synthetic verdicts (PASS case score 1.0 in the minted receipt JSON); the
4-test tripwire tests/test_arena_bench.py is tracked under 00cb15c77; the
receipt watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md exists. Note the
24-wide receipt's diagnosis was wrong in one particular: the killer was not
"shape drift" but a 459-byte redirect stub (dashboard/static/arrakis.html,
mtime 09-22, canonical 17,501-byte copy at dashboard/static/games/arrakis.html;
repoint at mag/arena_bench.py:73, stub-disease comment at :66-68).

Door 4 (night-cycle checkpoint legs): the harm class it targets is already
cured. Commit 9718e812d (night shift lane 7) landed atomic tmp+os.replace
state saves, trail-before-persist, and the honest rc=2 march skip; I read
the code at mag/lane_runner.py:932-938 (the 2026-10-04 comment documents the
5x CYCLE_FAIL cure) and tests/test_night_march_cure_20261004.py exists on
disk. The door's un-built remainder is per-leg resume after a mid-cycle
crash of two $0 legs (monitor re-run + a named skip), which is near-zero EV.
The receipt ranked it 4th of 13 anyway, one day after the cure.

Falsifier: CYCLE_FAIL re-run rows accruing in queue trails after 9718e812d,
or evidence the per-leg flags exist (I read cycle_night whole; no leg flags).
Move (5 min): strike doors 2 and 4 from the build list; the honest remaining
count is 9, and any plan that schedules them buys back landed work.

## Finding 2: EG-20 pass@K was dropped from the door list without a record

The ask's 11 doors are receipt-table rows 2-13 minus EG-20. EG-20 is the
receipt's rank 3, the ONLY door with a measured effort figure (2h) and a
success meter at spec (watch/inbox/ESTATE_GAP_DIG_20261004.md:79: "column
present; predicts the mesh vs frontier routing on one batch"), status
"open" (watch/inbox/ESTATE_GAPS_20261004.json:305-316), and zero code hits
(my `git grep -n -E "pass@k|pass_at_k" -- tools/ mag/ tests/` exit 1). The
door-2 commit itself names it next: "the pass@K diagnostic rides it". No
byte I can reach records why it left the enumeration. Caveat kept: EG-20's
motivating intel (Sharpening Tax, arXiv 2610.01509) is secondhand-unfetched;
the 24-wide receipt dropped that cite from its own record. The priority
claim here rides estate-side facts only (measured cost, defined meter, live
bench to ride).

Falsifier: a landed pass@K column (re-grep the three roots) or an owner note
dropping EG-20 by name. Move (2h): build EG-20 first among unbuilt doors.

## Finding 3: self-steal ledger, per door (greps untruncated this session)

- Monoculture agreement proxy: HALF-HELD. tools/env_contract.py already
  computes agreement_rate for the propagator (:580, :648, :706) and
  tools/overmind_judge.py:313 for judges. New work is only the cross-lane
  comparison plus the attention.md alert: a 1h wire, not a 2-4h build.
- Pheromone metabolism: QUARTER-HELD and premise re-verified. A momentum
  floor is already law in the ledger (tools/gps_mcp/ledger.py:88 docstring,
  :238-257 Momentum window, rising property; a fail absorbs, never rewards),
  so the build is alpha-decay plus drift-reset on an existing floor. The
  absence premise holds: my `git grep -n -i -E "decay|evaporat" -- tools/gps_mcp/
  mag/river.py mag/swarm_tools.py` returns only README aspirational text
  (:221, :229), zero code (CONVERGENT with the reviser's rerun).
- Clippy-as-prober: NOT HELD. Untruncated grep for
  fsrs|spaced.repetition|retrieval.practice|free.recall over memory/,
  .agents/, docs/, mag/, tools/, tests/ returns doctrine only (e.g. the
  forgetting-doctrine steal at memory/burns/LEDGER.jsonl:613, the Anthropic
  pyramid forgetting engine at mag/salon_50.py:56), zero scheduler code.
  Genuine build, with banked doctrine to cite instead of re-derive.
- Scale caveat the receipt never priced: the ledger's readable stores are
  tiny. tools/gps_mcp/receipts.jsonl = 11 rows (named the server's store at
  tools/gps_mcp/server.py:125), logs/duel/duels.jsonl = 80 rows (the feed,
  tools/gps_mcp/router.py:615). Alpha-decay over double-digit row counts can
  zero the signal; the falsifier needs a row/signal floor, and the door's
  value is gated on the gwap v3 backfill minting honest rows first.

Falsifier: a held FSRS/probe implementation under any name, or a larger
censused ledger store. Move (10 min planning): re-cost monoculture to 1h,
sequence pheromone after the backfill, keep clippy-prober as-is.

## Finding 4: two doors' own falsifiers are already in a checked state

- MCP-lattice shim: its gate says stop if agentmemory's grammar cannot be
  pinned to a tag. The local clone
  (C:/Users/foste/Documents/projects/library_parked/agentmemory) is grafted
  at c51bf3f with ZERO tags (`git tag` returns empty). The falsifier fails
  today as-written. Honest first move (30 min): unshallow/fetch tags or
  re-scope the gate to commit-hash pinning (c51bf3f). The wire surface
  survives independent of agentmemory: the spec's get_law/get_terrain/
  get_context tool shapes at watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md:28-33
  and PULL OVER DUMP at :36-37, both re-read this session.
- Build-once calibrator: precondition verified LIVE by fetch, not by receipt
  hand-off: huggingface.co/vixhal-baraiya/Gero-4B exists, Apache 2.0,
  Qwen3-4B base, safetensors, a classifier with no LM head returning
  calibrated probabilities, and still no published evals on the card, so the
  download-and-eval gate stays mandatory. The intel receipt's claims
  (watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-46) match the live card.
- Weld door: its gate ("needs the cop fix") is CLEARED by bb0f34586; the
  receipt's own ranking logic makes weld eligible now, which the ask's
  frozen gate list does not reflect.
- Context verified verbatim: frozen prices at tools/hermes_burn.py:70
  ("Captured from the live /v1/models pricing fields, 2026-10-01 probe.").

Falsifier: tags appearing in the clone, or an eval table on the Gero-4B card.
Move (30 min): run the two gate triages before spending any shim/calibrator
hour.

## Finding 5: cargo call and the hidden prerequisite node

Cargo (strike or park): night-cycle legs (cured, finding 1); arena-bench
(landed, finding 1); consume-the-ledger wire is the weakest surviving EV/h:
1-2 days for a semantics change on an organ with many live consumers
(mag/emergent_harvest.py:16, mag/flock_job.py:7-11, mag/flock_scheduler.py:155,
mag/rib_action.py:22, mag/rib_struct.py:20, mag/flock_steal.py:9), in tension
with the banked anti-recency design virtue, and it would consume a GPS feed
with zero honest v3 rows banked (the GWAP receipt: "the next --backfill of
NEW run dirs banks v3"; the 613 old rows, my own count of
memory/runs/gwap/arena-capability.jsonl, are the old instrument's record).
Three-signal query broker stays design-gated: mag/steal_steer.py:1-30
"embeddings" are sha256 hash-coordinates for repulsion, not semantic
vectors, so the embedding lane really is a new dependency class.

Hidden prerequisite neither the receipt table nor the door list names: the
gwap v3 backfill. EG-20 rides the arena it feeds, pheromone metabolism has
nothing honest to decay until it lands, and consume-the-ledger would read
its rows. It is one operator-green-lit backfill away, already specced in the
GWAP receipt's follow-ups.

Honest build order by EV-per-hour after this session's landings:
1. EG-20 pass@K (2h, measured, meter defined)
2. monoculture agreement wire (1h, reuses env_contract)
3. clippy-as-prober (2-4h, genuine build, banks the FSRS probes)
4. MCP-lattice gate triage (30 min) then shim (4-8h)
5. decay-family schema + pheromone metabolism (4-8h, after backfill)
6. mycelium-v2 bi-temporal (4-8h; violated append-only comment verified at
   mag/mycelium.py:183, contradict() counter-bump read at :188-198)
7. build-once calibrator (download-and-eval gate first; card verified live)
8. weld door (1-2 days; gate now cleared)
9. three-signal (falsifier first)
10. consume-the-ledger (last; needs backfill + pheromone first)

## Blind spots, named

## CORRECTION (hostile second pass, 2026-10-04: the scale clause of finding 3)

WITHDRAWN as stated: "the ledger's readable stores are tiny... receipts.jsonl
= 11 rows... duels.jsonl = 80 rows" as evidence that pheromone metabolism is
value-scale-gated, and the derived demotion "sequence pheromone after the
backfill". That cited the WRONG STORE: receipts.jsonl (11 rows) and
duels.jsonl (80 rows) are feed/receipt surfaces, not the ledger. The real
store, verified by my own instrument this pass: tools/gps_mcp/gps_ledger.db3
(the default at tools/gps_mcp/server.py:124), sqlite counts
`capability 30`, `verdict_log 593` (CONVERGENT with the second pass and with
commit d349ce7d2: "idempotence proven 593->593, 99 fed / 351 distinct").
The momentum-floor implementation cite is added too: the floor law lives at
tools/gps_mcp/ledger.py:435-440 with the UPDATE against the capability table
at :441-442 (I previously carried only the docstring at :88 and the window
class at :238-257).

What survives, rescoped by bytes I ran this pass:
- The mutation surface for pheromone metabolism is the 30-row capability
  table (model_id, task_shape keyed; pass_rate/sample_size), NOT the 593-row
  verdict_log, which is the append-only verdict record momentum never edits
  (LM7 at watch/inbox/model_garden/STEERING_FIELD_THEORY.md:147-148). A
  signal/row-floor clause in the falsifier still binds at the 30-aggregate
  grain; it does not bind at all on the dead 11/80 numbers.
- The demotion transforms rather than dies, on new evidence: my sqlite
  time-span query reads verdict_log min ts 2026-09-30T01:24:56Z, max ts
  2026-10-04T09:36:09Z, and zero rows at or after the cop fix's landing
  window (bb0f34586); capability last_measured/updated_at span the same
  window. ALL 623 stored rows are tainted-era, minted by the pre-fix
  instrument. Decay/slash/reset on that store is partially CURATIVE
  (flushing poisoned merit), so pheromone metabolism does NOT wait on the v3
  backfill as a value precondition; the backfill dependency belongs to
  consume-the-ledger (finding 5) alone. Pheromone's EV-per-hour was
  under-costed in my original order: it moves up beside the decay-family
  slot, gated only by the shared schema and its floor clause.
- Everything else in finding 3 stands unchanged: agreement_rate organs
  (tools/env_contract.py:580,:648,:706; tools/overmind_judge.py:313),
  decay-in-code absence re-verified, clippy-as-prober un-held now ALSO
  censused clean in the ZMEM harness store (`grep -ril fsrs` over
  C:/Users/foste/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory/
  exit 1, no files).

- I ran single checks only (one selftest, greps, counts, one web fetch); no
  pytest suite was fired, so "tests green" claims here are the commits' own.
- The GPS ledger store census covers receipts.jsonl (11) and duels.jsonl
  (80); if the ledger persists a larger state elsewhere, the scale caveat
  weakens. Not censused.
- The GWAP receipt's new-instrument figures (529 payloads; 161/88/64/216)
  were not re-derived; only its 613-row old-ledger count matches my count.
- ZMEM harness store and sibling untracked drafts beyond the named test
  files were not re-walked this session.
- The tree moved under me once (00cb15c77 landed mid-session); any sibling
  landing after that commit is outside my observation window.
- arXiv 2610.01509 stays unfetched (secondhand); EG-20's priority claim does
  not depend on it.
