# MOONSHOT-1 - dogfood the standing fleet: raction the saved workflows themselves

Filed by the moonshot-1 lane of ractor-engine run "Ractor-dogfood-workflows"
(dwf_run row, status running, 2026-10-04 02:21Z). The ask names 12 saved
workflows; the fleet on disk is 19 (ListSavedWorkflows count=19 this sitting).
Instrument notes up front: ListWorkflowRuns is unreachable from this seat
(workflow_introspection_unavailable, capability gap), so the fire census below
is sqlite3 read-only over C:/Users/foste/.zcode/cli/db/db.sqlite, table dwf_run,
all 138 rows censused untruncated by a python query I ran this sitting (the
same source the operator dive used, OPERATOR_WORKFLOW_DIVE_20261003.md:4).
Duplication check: grep -c for all 12 workflow names across ractor-topic/
SYNTHESIS.md, 2026-10-01-dogfood-gaps/SYNTHESIS.md + dogfood.md, and
2026-10-02-dogfood-48h/dogfood.md returned 0 in every file: no prior lens has
ractioned the fleet as a fleet. The failure-rate finding is CONVERGENT with the
operator dive (independent re-derivation, flagged where used). No em-dashes.

## The census I ran

- dwf_run full census: 138 runs, 5,053,454,181 tokens total, statuses 77
  completed / 35 failed / 23 cancelled / 3 running = 58 of 138 (42.0%) failed
  or cancelled.
- Template similarity: difflib.SequenceMatcher exact ratios run this sitting
  over .zcode/workflows/*.dwf.ts. The six 10-01-generation scripts (fill-ball,
  salon-mine, librarian-expedition, wide-dig, drop-dig, the-gala) share 93.95
  to 99.4 percent of their bytes: lowest exact pair salon-mine vs the-gala
  0.9395, fill-ball vs wide-dig 0.9506 exact (19 differing blocks of 39
  opcodes). quick_ratio puts gap-analysis at 0.913-0.923 and mickey17-v2 at
  0.947-0.950 against that family. ractor-engine sits furthest out (0.767
  quick vs gap-analysis).
- Key fire rows (name, status, tokens, UTC moment), from the same query:
  - "Tree Doctrine 50-wide dig (gated)" completed 106,564,604 at 2026-09-25
    18:59Z: tree-doctrine-dig has fired exactly once, ever.
  - "THE 50 - reset-day fullsend" completed 145.1M 2026-09-19 15:53Z and
    "THE 50 - full program relaunch" completed 54.8M 2026-09-25 18:53Z: the-50
    fired twice in its first week, then dormant 8+ days.
  - mickey17 lineage dormant since "Mickey17 Wave 3" 2026-09-28 20:38Z; the
    the-gala script declares itself the successor (the-gala.dwf.ts:3 "amended
    from mickey17-v2 lineage").
  - The 10-01 generation each has ONE clean completed fire: fill-ball
    ("Fill-ball-one-sittings" 10-02 03:51Z, 68.7M), librarian-expedition
    (10-01 22:57Z, 37.6M), drop-dig ("Localfirst-steal-wave" 10-01 08:56Z,
    41.9M), gap-analysis ("Gap-analysis-100m" 10-01 22:00Z, 63.1M; second
    clean fire "Gap analysis: arena day one" 10-03 21:18Z, 58.6M). wide-dig is
    the only member with two clean fires (SpikingBrain 10-01 18:14Z, 28.0M;
    "Wide dig: the Grok bot ecosystem" 10-03 20:18Z, 30.4M). salon-mine's main
    20-deep run NEVER completed (2 cancelled + 1 failed; only
    "Salon-vault-stragglers" 10-02 14:53Z, 66.3M, finished).
  - olm-mine is the only cadence organ: "Frontier OLM mine" x5 + "OLM mine
    daily burn" x7 across 09-29 to 10-03 (one still running as of 23:30Z),
    OLM family spent 1,523.7M of the fleet's 5,053.5M tokens (30.1%).
  - Game-dig family (the 5 vein clones): 34 attempts, 29 failed/cancelled
    (85%), 643.9M tokens, all inside 2026-09-26 22:22Z to 2026-09-27 05:36Z.
    Zero fires since; zero registry rows past 09-26.

## F1. The fleet is one template wearing 8 skins; "compose into mega-workflows" is really "consolidate to one shell"

The 12 named workflows are not 12 engines to chain. Ten of them are lane-table
variants of one ractor50-family shell (93.95+ percent shared bytes, measured,
instrument above), one is a daily miner, one is the audit loop. The inheritance
is not benign: gap-analysis.dwf.ts:82 and :91 still write to the mickey17
ancestor's filesystem (`C:/Users/foste/.zcode/workspace/default/mickey17_v2`
and `memory/runs/mickey17_v2/runs/`), so a 10-01-generation clone routes its
lane output through another workflow's workspace directory. Minimum viable
fleet: about 5 organs (olm-mine, ractor-engine, the-gala, one parameterized
template shell, music-cut), not 12, and the game-dig family folds into the
shell as one vein arg.
Falsifier: two of the six family scripts diverge below 0.85 exact ratio, or
the mickey17 path consts are dead code never used by the write path.
Move (one sitting, ~50 min): extract the shared shell into one parameterized
saved workflow (lanes JSON + fold contract as args), re-save the six clones as
parameter sets, and add a gate grep that fails any saved workflow writing into
another workflow's workspace dir.

## F2. Fire census: most of the fleet has fired clean exactly once; the gate registry cannot even count the fleet

Registry census (memory/workflows/REGISTRY.jsonl, 63 rows, all loaded this
sitting): fill-ball, salon-mine, librarian-expedition, and drop-dig have ZERO
gate rows ever, and the rows that exist use drifting names for the same script
("frontier-olm-mine" vs "frontier-olm-mine.dwf.ts", "tree-doctrine-dig" vs
"Tree-Doctrine-50-wide-dig.dwf.ts" vs "tree-doctrine-dig.dwf.ts"). So the
estate's own two instruments disagree about what exists: 12 names in the ask,
19 files on disk, 25 distinct name spellings across the registry, and run
labels in dwf_run that match no filename at all ("Fill-ball-one-sittings",
"Ball-20260929-dance2"). Fire-counting the fleet today requires fuzzy label
mapping, which is why "never fired twice" was never noticed.
Falsifier: a registry naming convention that round-trips run rows to saved
workflow files without a hand-maintained alias table.
Move (one sitting, ~30 min): make the gate write the script filename into the
dwf_run label convention (or add script_hash to the receipt) so every future
fire census is a group-by, not an archaeology dig. OWED, not asserted: the
exact cause of the 10-03 22:37-22:38Z trio (Ractor-fleet-meta cancelled,
Fill-ball-amend failed, Gap-analysis-amend cancelled, all at 0 tokens within
60 seconds) - three fleet-maintenance operations died at the same moment and I
did not trace the trigger.

## F3. The game-dig family is the fleet's theater-burner, and the ask's own census is stale

The fleet is 19 saved workflows, not 12: 7 uncounted (game-dig-coop-social,
game-dig-creature-farming, game-dig-horror-maze, game-dig-liveops-seasonal,
game-dig-roguelike-runs, game-mechanics-deep-dig, music-cut). The five vein
clones are byte-clones saved in the same minute (2026-09-27 07:21, 9.2-9.3KB
each) whose descriptions admit the shared defect ("PATCHED 2026-09-27:
producer-side shrink() bound" repeated five times - one bug, five hand-patches).
Measured burn: 643.9M tokens across 34 attempts for 5 completed vein digs, an
85 percent failure rate, all inside 7 hours on 09-26/27, then total silence
for a week. That is 12.7 percent of all fleet tokens ever, spent on the
highest-failure-shape in the census, with zero fires since.
Falsifier: a game-dig dwf_run after 2026-09-27, or a re-run of my family query
returning materially different totals.
Move (one sitting, ~25 min): collapse the five clones into one parameterized
workflow (vein + briefs_path args), retire the other four saves, and log the
643.9M in the GAP_REGISTER as the measured price of un-parameterized cloning.

## F4. The mega-workflow already exists as a file contract and prose; it has just never run as one script

fill-ball.dwf.ts:3,10-17: its arg IS "Path to the GAP_REGISTER.md a gap-analysis
run produced" and its whenToUse names the loop verbatim ("work -> gap-analysis
-> fill-ball -> (ractor-engine on anything ambiguous)"); gap-analysis.dwf.ts:13
answers from the other side ("the register this emits IS fill-ball's lane
table"). The handoff artifact is real and on disk:
watch/inbox/gap_analysis_20261001/GAP_REGISTER.md (ls this sitting). Three legs
have each fired at least once; the chain has never fired as one workflow, and
the 10-03 22:38Z amend attempts at both ends died at 0 tokens. The composition
answer to the ask: one 20-line wrapper (gap-analysis, hand its register path to
fill-ball, route ambiguous rows to ractor-engine) is the estate's standing
self-repair mega-workflow, and it needs zero new lanes.
Falsifier: fill-ball's script takes the register path as an arg but never
actually reads the file (I verified the arg exists at fill-ball.dwf.ts:15-17,
not the file-open; check before wiring).
Move (one sitting, ~45 min): save "repair-ball" chaining the two with the
register path auto-handed off, one receipt lineage, then fire it once on the
current register to prove the loop closes without a human carrying the file.

## F5. Keep list: olm-mine and ractor-engine are the only engines; tree-doctrine-dig and the-50 are the retire candidates

olm-mine: 12 attempts across 5 distinct days, the only sustained cadence in
the census, 30.1 percent of all fleet tokens. ractor-engine: the only member
with the hostile/break/steer anatomy (this run is an instance; 12 registry PASS
rows on 10-02), and one of only two scripts with zero sibling references in its
source (the other is olm-mine - the clones cross-reference each other, the
engines do not). the-gala stays as the owed-work executor (31 division markers,
genuine restructure, fired through 10-01). tree-doctrine-dig is a one-fire,
106.6M-token one-off whose shape is wide-dig at 50 lanes; the-50 is a
two-then-dormant executor whose job the-gala's B division absorbed (its own
header says so, the-gala.dwf.ts:3). Retire-or-fold both into the template;
deleting saves is an operator call, so this is a ranking, not an action.
CONVERGENT (flagged per the duplication law): the operator dive independently
read the same failure class at an earlier moment - 54 of 134 dwf runs failed or
cancelled (OPERATOR_WORKFLOW_DIVE_20261003.md:27) against my 58 of 138 (42.0%)
- and its dwflint proposal (change #6, lines 145-149) is the systemic fix my
F2 naming convention complements: lint before fire, names after.
Falsifier: another workflow shows multi-day cadence in dwf_run, or
ractor-engine's anatomy duplicated in a family clone.
Move (one sitting, ~20 min): fold this keep/retire ranking into the
GAP_REGISTER as ranked rows with the census query output attached, so the next
fill-ball lane can land the naming-convention fix and the consolidation in one
sitting.

## CORRECTION (hostile pass, 2026-10-04): F4's "file contract" leg is withdrawn

The hostile second pass verdicted F4 weakened and I re-ran its checks myself;
it is right on the contract leg. My greps this sitting: grep -c
"readFile|readTextFile|world.read|fs." fill-ball.dwf.ts = 0, and the only
args uses in the whole script are args.slug (:89) and args.lanes (:94), so
args.register, which the saved metadata declares REQUIRED, is read by no code
line: a declared-but-dead interface. gap-analysis.dwf.ts carries GAP_REGISTER
only as prose and lane-ask text (description :5-13, a15-rollup ask :121); no
script code writes a register file. The on-disk
watch/inbox/gap_analysis_20261001/GAP_REGISTER.md was a seat's discretionary
write, not script output. The surviving, now mechanism-named leg:
fill-ball.dwf.ts:95-96 throws "no lanes passed" when ALL is empty, and the
dwf_run failure_json for Fill-ball-amend (my sqlite query) reads
{"code":"DriverError","message":"no lanes passed"} - the one amend attempt at
the loop died at spawn on exactly the missing wiring. The mega-workflow is
prose-only at both ends: wiring to build, not a contract to light.

BONUS (resolves this card's OWED item): the 10-03 22:37-22:38Z trio is no
longer unattributed. failure_json (sqlite query, this sitting):
Ractor-fleet-meta = ProviderStop 1005 "exceed quota limit" on
account:zai-start-plan GLM-5.3-Flash (actor lens-lineage); Gap-analysis-amend
= same quota kill (actor lane-a03-tavern-curve); Fill-ball-amend =
DriverError "no lanes passed". A quota wall plus an unwired amend call, not
one mysterious trigger.

## Blind spots (honest)

- Run-label to workflow mapping is by name only. Uncertain pairs I did NOT
  assert: "Ball-20260929-dance2" as the-gala (probable, unproven),
  "Hitler-dig-full-dogfood" as drop-dig (unproven). The 12/19 name set may
  hide ad-hoc fires of the same scripts under labels I did not match.
- I audited resumed_from counts only in aggregate; per-run resume chains
  (amend-not-rewrite behavior inside dwf_run) were not traced.
- The 5 percent of bytes where family clones differ (lane tables, fold
  contracts) was sampled via grep, not read line by line for all 19 files.
- Whether the game-dig family's "wheel spec" deliverable ever landed was not
  traced; my theater verdict rests on burn and dormancy, not on the output.
- Three runs were still in flight at census moment (including this one); the
  counts are a snapshot, not a constant, per the census denominator law.
