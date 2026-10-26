# ECONOMICS LENS: the 11 remaining doors, repriced (2026-10-04)

Writer: lens-economics (ractor seat), topic: the 24-wide dig's 11 remaining
build doors and their reviser-ordered sequence. Inputs read this session:
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md (full, incl. the 13-row door
table at :233-249), watch/inbox/GWAP_INDEPENDENT_COP_20261004.md (door 1
landed, bb0f34586), state/CURRENT.md, and the organ bytes cited below. All
checks I ran are named; everything I did not run is named too. No em-dashes.

## The one-sentence verdict

The reviser's order is directionally right but stale in three priced places:
the only measured-effort door fell out of both successor sequences, one
2-4h door was partially cured the same date it was sized, and the decay
family's shared-schema gate would re-mint vocabulary the estate already
holds in mag/republic.py.

## Repriced build order (EV per hour, certainty-adjusted)

1. ARENA-BENCH CI TRIPWIRE (1-2h). Verified live defect: the GATES parse
   raise at mag/arena_bench.py:110 ("arrakis.html GATES parse came back
   empty"), and zero tests reference the file (my grep of tests/ for
   "arena_bench" returned nothing). The bench's own docstring (:98-101)
   says it refuses to fabricate on parse failure, so capability eval is
   dark, honestly. Cheapest conversion of silent rot into pre-push failure.
   Steal shape: the pytest -q before-done discipline plus the existing
   pre-push hook chain (githooks/pre-push already runs ratchet + citation
   lint + scenario suite per AGENTS.md). No new organ.
2. EG-20 PASS@K (2h, MEASURED at spec, watch/inbox/ESTATE_GAP_DIG_20261004.md
   row 9: "Coverage column (pass@K, large K) beside win rate in arena/gwap |
   2h | column present; predicts the mesh vs frontier routing on one
   batch"). See finding 1: it is unlanded and dropped from both successor
   lists. Restore it to slot 2.
3. CLIPPY-AS-PROBER (2-4h). Guaranteed consumer: clippy fires at every
   session start (main.py:1253-1257, standing reminders per AGENTS.md), so
   unlike every other door the usage line is certain from day one. Concept
   prior art already banked: .agents/skills/fireball-cycle/SKILL.md:9 ("a
   skill is a one-time conversion that becomes free recall") states the
   exact mechanism as prose; no FSRS/retrieval-state code exists anywhere
   (my git grep -i "fsrs|spaced.?repetition|retrieval.?state" over mag/
   tools/ tests/ hit only a Godot binary). Genuine build, banked concept,
   and it banks the ~1k graded probes the decay family's third store needs.
4. MCP-LATTICE RECONCILIATION PASS (the gate itself, ~1-2h read pass) before
   any shim build. The receipt orders it verbatim (X_INTEL_AIENG_SCRATCH_
   20261004.md:90-94: reconciliation "BEFORE any lattice building starts,
   the wire-don't-build law", corpus already cloned). The 4-8h shim only
   proceeds on an adopt/steal verdict. mag/mcp_server.py is a live tool-map
   server (ROLE_TOOLSETS at :67, verdict-gated NEW/PINNED manifests :370),
   so the shim is an extension, not a server build.
5. PHEROMONE METABOLISM (4-8h), self-stolen: see finding 2.
6. MONOCULTURE AGREEMENT-RATE PROXY (2-4h), but wire it beside
   tools/blind_audit.py (ESTATE_GAP_DIG row 10, "cross-contradiction gate
   before every ractor synthesis", half day, THEATER verdicts 5 to 0) rather
   than as a new organ: both detect correlated same-source error across
   lanes. Two rows, one instrument family.
7. MYCELIUM-V2 (4-8h) and the design-gated five: unchanged from the
   reviser's table, with the cargo notes below.

## Findings (with falsifiers)

F1. SEQUENCE DRIFT AT DOOR 1: EG-20, the only measured-effort door (2h,
success meter defined), is excluded from the ask's 11-door list AND from the
landed door-1 receipt's next-doors line (GWAP_INDEPENDENT_COP_20261004.md:82-83
names arena-bench, clippy, night-cycle only; the primer's own rank-2 pairing
at :219 is arena-bench AND EG-20). Unlanded: my git grep for pass@K /
pass_at_k over tools/ mag/ tests/ returned zero hits. A 2h measured door
outranks every 2-4h estimate on certainty alone. Falsifier: a sibling commit
landing pass@K (check git log for a coverage column in tools/arena_gwap.py).
Move: restore EG-20 to slot 2 in the sequence (10 minutes to re-issue the
order; 2h to build).

F2. SELF-STEAL: the decay family's shared-schema gate is half-solved on disk.
mag/republic.py:114-115 already defines superseded_by ("set once, by
supersede(); never edited") under the house chain law (:15), with an
append-only trail and mutation guards (:209-215). The GPS ledger already has
a partial metabolism seed: the momentum-rising fail-absorbing floor inside
the 1/n update (tools/gps_mcp/ledger.py:433-447, floor_applied,
"a fail absorbs, it never rewards"). And mycelium decay() already stamps
decayed/decayed_at (mag/mycelium.py:271-276) with no successor. So the
primer's gate "define valid_at/invalid_at/superseded_by once, first" should
be "import superseded_by from republic.py, mint only the two timestamps".
Falsifier: if republic.py's supersede() semantics conflict with ledger-row
supersession (rows are aggregate stats, not letters), the import fails and
the vocabulary is genuinely new. Move: 30-minute read of mag/republic.py
supersede() against ledger.py row shape before the family starts.

F3. REPRICED DOWN: NIGHT-CYCLE CHECKPOINT LEGS (rank 4 in the table, 2-4h)
was sized against the 2026-10-03 5x CYCLE_FAIL class, but the same-date
night shift landed the honest rc=2 march skip + atomic state saves
(watch/inbox/NIGHT_SHIFT_20261004_CLOSE.md:35, commit 9718e812d), and
cycle_night now trails the composite BEFORE persisting last_night with the
Errno-22 root cause documented in-code (mag/lane_runner.py:923-938). The
march leg now returns a named rc=2 skip every night without a state-write
storm; residual harm is monitor re-runs during cage-mount Errno-22 windows
only. The door's harm denominator shrank after the ranking was written.
Falsifier: a fresh Errno-22 storm re-running full cycles after 2026-10-04
(grep queue/lanes trails for CYCLE_FAIL clusters). Move: demote below the
monoculture proxy; build only if a new storm bank appears.

F4. CARGO VERDICTS (as specced): (a) CONSUME-THE-LEDGER's headline premise
("nothing consumes the ledger at decision time") is refuted by the estate's
own router: tools/gps_mcp/router.py:5-11 routes on measured pass-rate +
cost + records calibrated confidence on every ask receipt, and :44-50 adds
the MOMENTUM_RANK momentum tiebreak, all reading ledger history at decision
time. The door's true residue (a flock g_best term, runner claims section)
carries no measured harm beyond the ToM lane's theoretical sibling-churn.
(b) THE WELD DOOR (1-2 days) names no learner or consumer surface and builds
no controlled instrument, while the dig's own law (primer chapter: any tutor
claim must benchmark against the 0.37-0.79 band with a controlled instrument)
makes its efficacy unmeasurable as specced; a toy that cannot be evaluated
is spend theater by the receipt's own standard. (c) THREE-SIGNAL's falsifier
("50 estate questions with known answer files", recall@5 vs BM25 baseline)
requires a harness that does not exist, so the 1-2 day estimate hides the
eval build, and the embedding lane is a new dependency class (local
lm_studio knows of embedding-only models, mag/lm_studio.py:63, but no
estate embedding lane is wired). Falsifier for the cargo verdicts: a named
consumer for the weld door, a measured harm case for flock g_best, or an
existing recall@5 harness would flip each. Move: cut the three from the
build sequence; keep their steal-shaped residues (beat_map rows exist,
tools/beat_map.py; router pattern exists) as design notes.

F5. THE TOP TWO DOORS ARE ALSO THE CHEAPEST: arena-bench tripwire (live
ValueError verified at mag/arena_bench.py:110, zero tests) and
clippy-as-prober (guaranteed session-start consumer, banked concept, zero
existing state) both convert under 3h each into permanent instruments, and
neither requires the paid lane. For scale: the dig behind these doors cost
48.3M tokens (commit 0838e150e) and the doors' yields are seat-time only;
the first two doors plus EG-20 total ~5-7h for three standing instruments,
the best ratio in the table. Falsifier: if the tripwire's ground-truth fix
(arrakis.html shape) turns out to need a redesign rather than a regex repair,
the 1-2h estimate breaks. Move: land the tripwire + EG-20 + clippy-as-prober
as the next three sittings, in that order.

## Hostile second pass, corrections appended (same session)

Two findings were verdicted weakened; both re-checked against the live tree
and corrected rather than withdrawn.

F4 CORRECTED (cargo verdicts overreached; none of the three is cargo as
specced). (a) The router refutes only the primer's heading universal
("nothing consumes the ledger at decision time", PRIMER:192); the body's
operative claim (:194, decentralized actors do not read it) survives, and
the target absence is real: my grep -n -E "g_best|p_best" mag/flock_field.py
exits 1, zero matches. The door was already ranked last with a design gate,
so my "cut" was a no-op; the honest economics verdict is leave gated last.
(b) The weld door HAS a meter: its spec banks arena_gwap agreement_score
(PRIMER:124), execution-verified per :106. What is missing is a learning-gain
control per the :84 law, and the estate already holds the control substrate:
the corpus's quiz pre/post stages are banked-but-dead data (PRIMER:100, "no
skill ever consumes stage=='pre' or 'check'"), so the control is a consumer
for bytes that exist, a spec add of roughly one sitting, not a cut.
(c) Three-signal's falsifier harness exists in executed form: Q-031
(tools/queue_close.py:127, 2026-09-28) ran a held-out 50-question eval,
accuracy@1 0.48 / accuracy@10 0.76, results JSON with sha-pinned catalog.
The eval cost is adaptation of a tag-retrieval instrument (hours), not
build-from-zero; the embedding dependency class stays the only real gate.

F5 CORRECTED (the top slot rotated mid-claim; EV logic validated by events).
Door 2 landed at 00cb15c77, 2026-10-04 12:39:31 -0400 (git show --stat:
mag/arena_bench.py +9, tests/test_arena_bench.py +94, receipt
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md +52). My "zero tests
referencing the file" was true at my read moment and false hours later on
the live tree; the ValueError moved :110 -> :109. The landing's own
diagnosis (a 459-byte redirect stub at static/ root since the 09-22 surfaces
dedupe, canonical at games/arrakis.html, bench raising "into the void for
12 days") confirms the pricing: a sibling took the door within hours of it
being ranked cheapest. The live remainder is clippy-as-prober, now the
cheapest unlanded door (re-verified this session: git grep -i
"fsrs|retrieval/state|free.?recall.?probe" over mag/ tools/ main.py returns
only the Godot binary; memory/retrieval/ does not exist), and the door-2
commit names "the pass@K diagnostic rides it", giving EG-20 a rider on the
now-live bench. Discipline carried forward: any "unlanded" claim on this hot
tree names its instrument and moment (the census-denominator law B2-216,
applied to doors). Not verified by me: the passer's "28 receipts minted by
16:59Z" (memory/runs/arena_bench does not exist; grep for "28|receipts" in
the tripwire receipt returns no matches), and the tripwire's 4-test green
status rides the commit message, not my own run.

## Blind spots

- I ran no builds, tests, or the arena bench itself; read-only lens. All
  harm claims ride the receipts plus my byte reads of the named lines.
- Effort figures are the reviser's estimates except EG-20 (measured at
  spec); I did not measure any.
- I read state/CURRENT.md, the primer, the door-1 receipt, ESTATE_GAP_DIG
  rows, X_INTEL PRIMER/PROPER_SCORING/AIENG_SCRATCH excerpts, NIGHT_SHIFT
  close greps, and the organ bytes cited; I did NOT exhaustively census all
  last-48h watch/inbox receipts, and the tree is hot (25+ modified files at
  session start), so sibling cures beyond the night shift may exist unseen.
- No cost model for the Gero-4B download/eval (build-once calibrator stayed
  design-gated; its EV unpriced beyond the gate).
- hermes_burn pricing read only from the live tail (a $0.0076 haiku row and
  a $0.0514 opus row, 2026-10-04T16:09Z); no aggregate spend figure computed.
