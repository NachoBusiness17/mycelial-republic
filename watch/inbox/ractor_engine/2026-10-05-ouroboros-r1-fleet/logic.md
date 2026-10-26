# LOGIC LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Seat: lens-logic (instrument theorist; jacket: two instruments disagreeing with no
adjudicator). Topic: dogfood the standing WORKFLOW FLEET, steal the improvements
back into the definitions. Findings on the ENGINES: the inference rules the fleet
actually runs, and where they are tautological, contradictory, or write-only.
Everything below was read or run this sitting at
C:/Users/foste/Documents/projects/local_sovereign_agent with Read,
.venv/Scripts/python.exe censuses, and grep. No em-dashes. What I could not verify
is marked OWED. Sibling lenses (operations.md, accuracy.md, economics.md in this
folder) were read in full this sitting; agreements are flagged CONVERGENT with the
duplication-is-emphasis law.

Evidence base I personally checked: tools/mickey17_v2_fold.py (full read, 235
lines); tools/workflow_gate.py (lines 1-60 grep map + 320-384 full + soft/G6/G8
grep hits); .zcode/workflows/ractor-engine.dwf.ts (full read, 353 lines);
memory/workflows/REGISTRY.jsonl (88 rows, my own census, commands below);
memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ (in-flight decode); both spec
addenda (watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md,
watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md); corpus/steal/MASTER_READ_ESTATE.md;
corpus/steal/MASTER_MICKEY17_V2.md headers via the addenda (not re-read this
sitting); the three sibling lens files; state/CURRENT.md. The OLM mines and the
parked-decisions receipts were NOT read by this lens (blind spot).

## F1 (rank 1). The fold's integrity check is a tautology, and the fleet's
## consensus amendment would fix the wiring in the direction the estate's own
## contradiction-tier law forbids

Two separable logic defects in tools/mickey17_v2_fold.py:179-202, both mine:

1. THE INVARIANT CANNOT FAIL. The exclusion loop at :187-193 increments exactly
   one of {excluded[reason], included} per row of all_rows; identified is
   defined as len(all_rows) at :194. Therefore the assert at :200-201
   (identified == included + sum(excluded)) is true by construction on every
   possible input, including corrupt ones. Every archived fold prints
   "invariant HOLDS" (both addenda recount it) - a verification line that
   carries zero bits. The fold has never had a working integrity check; it has
   a decoration shaped like one. Note the one reachable exclusion branch
   (:186, :189: a lane landing exactly 1 row is auto-excluded as "1
   phantom-source (dead-lane negative row)") - an undocumented genre
   assumption (in an execute genre a healthy 1-row lane is plausible) that has
   never fired only because every lane so far landed 5+ rows.
2. THE CONSENSUS FIX RESOLVES AN ADJUDICATION THE WRONG WAY. All three sibling
   lenses propose wiring deep_tier2 unconfirmed verdicts into PRISMA
   "excluded" under code 9 (operations amendment row 1; accuracy row 1;
   economics row 1). But PRISMA exclusion means removal from included, while
   the estate's contradiction-tier law (LAW 3, "HELD, best evidence for the
   law" in both addenda; MASTER_READ_ESTATE section 10 "corrections rule, the
   original counts do not") requires contradicted rows to REMAIN VISIBLE with
   their measured corrections. Two instruments - the PRISMA flow and the
   contradiction-tier law - disagree about the disposition of a contradicted
   row, and no adjudicator exists. Implemented as the siblings wrote it, the 6
   rows that rode included as excluded:0 (run-0 a08 r9; read-estate r04#1,
   r05#0-#3 - the 910/28/250/86.01 corrections, D5-D10) would vanish from the
   included count and from every downstream reader of it: the wrong-way fix
   hides the run's most substantive rows.

Falsifier: (1) exhibit any input archive for which the :200 assert fires -
impossible by the counter-partition argument, which is the finding; (2) point
to an estate instrument that renders code-9-excluded rows in the fold file
today (none exists: PRISMA prints only counts at :198).

One-sitting move (~20 min, lands inside the amendment every sibling already
ranked first, so it must ride THIS round or the wrong-way fix lands first):
in the shared fold edit, (a) route code-9 exclusions to a rendered
"## CORRECTIONS (code 9: carried, not dropped)" section printing row_key,
verdict, and the evidence head; (b) replace the tautological assert with a
reachable one: no included row may carry a persisted deep_tier2 verdict in
{unconfirmed, crashed} - violation aborts the fold with a nonzero exit; (c)
stamp folded_at into the header (E7, demanded in both addenda, 5 folds
unstamped).

## F2 (rank 2). The registry row is two instruments disagreeing inside one
## JSON line, and the warn layer that resolves them is write-only

My census (commands in the checks section): 88 rows; verdict PASS 75 / FAIL
13; but 74 check-level failures exist inside them (G6 28, G3 16, G4 7, G7 6,
G2 6, G5 5, G1 4, G8 2 instances). 32 soft-false checks ride under PASS
verdicts; the precedence rule (soft:true downgrades the check without
affecting the verdict) lives only in the gate source
(tools/workflow_gate.py:192 "failed = [r['id'] for r in rows if not r['ok']
and not r.get('soft')]", :176-184 soft creation, :354 verdict derivation) -
the row itself records no warning trace on the verdict string. All 17
ractor-engine rows are PASS and all 17 carry G6 ok:false with the identical
reason "receipt mention lacks a dated stamp": a warning that fires 17 of 17
times on this engine is a constant function - zero information per fire
(CONVERGENT with economics' 28-of-89 de-calibration count; mine adds the
17/17 per-engine saturation and the reader census). Reader census, scoped:
grep for REGISTRY.jsonl across tools/ mag/ scripts/ names 6 consumers
(gate_canary.py, visor.py, workflow_gate.py, worldline_compact.py,
mag/improve.py, mag/seed_registry.py); a "checks" grep over those six shows
none reads the registry's checks[].ok (seed_registry's checks are its own W1
verify; gate_canary matches cards against verdict/digest). The warn layer is
written 74 times and read zero times: two instruments (verdict aggregate,
per-check booleans) with no consumer adjudicating them.

Falsifier: name a consumer that reads checks[].ok from REGISTRY.jsonl and
acts on soft rows (scope: the 6 files above, grep this sitting); or show a
registry PASS row whose verdict string carries its warn count.

One-sitting move (~10 min): in tools/workflow_gate.py:354-375, when the
warned list (:193) is non-empty print "workflow_gate PASS (N warns)" and add
a top-level "warns": [ids] array to the registry row; then one G6 stamp
comment line per standing workflow (economics amendment row 3b, CONVERGENT)
retires the 17/17 saturation at its source.

## F3 (rank 3). The ractor engine fabricates the verdict value in its own
## return contract and drops withdrawals - the instrument auditing
## instruments mints its verdicts as constants

.zcode/workflows/ractor-engine.dwf.ts:334-340 maps every ranked move to
status: "verified" as const and severity: "medium" as const - the verdict
field is hardcoded, not computed from the hostile pass. The verified[] claims
at :341-346 include "each lens finding survived a hostile second pass that
byte-checked its evidence" - but :290 (survivors.push(...s.value.pass.additions))
injects breaker-authored findings that by construction never faced any
hostile pass; for them the claim is false as stated. The steering revision
(:253-273) is merged in memory and never banked: a withdrawal (the lens
explicitly retracting a weakened finding) exists nowhere on disk - the
notCovered note (:349) covers KILLED findings living in break files, but
weakened-then-withdrawn findings live nowhere. That is the negative
-first-class law (both engine runs' strongest law) violated by the ractor
engine itself. Same disease class as G8 passing the fleet that built it
(CONVERGENT, all three siblings) and the parked-decisions
test-pins-enforcing-the-bug catch: the instrument exempts its own output.
Also verified: the lens phase has no bank check - only SYNTHESIS.md is
glob-checked (:316-323); the per-lens OUT/<id>.md bank ask (:188) is
ungated (CONVERGENT with economics amendment row 3a). This lens banks its
own file before submitting, by hand, because no gate asks.

Falsifier: a survivor that entered via :290 and carries status "verified"
while no breaker ever confirmed it - the return block does this on every run
with additions; or a file under OUT/ recording a steering withdrawal from
any prior ractor run (grep this sitting: none exists in this round's folder).

One-sitting move (~30 min): in ractor-engine.dwf.ts, (a) compute status from
the breaker verdicts (verified only when confirmed; "proposed" otherwise);
(b) scope the verified[] line to pass-confirmed findings; (c) bank each
revision response to OUT/<id>.rev.md and withdrawals to OUT/WITHDRAWALS.md;
(d) add the per-lens bank check mirroring :316-323 after the lens phase.

## F4 (rank 4). The tier-1 instrument measures genre, not fidelity - cross
## run ratio comparison is confounded, and the fold prints the ratios as run
## quality numbers

My run-3 decode (in-flight archive, moment-read, B2-216 applies): 8 lane
files, 7 checks files (e06 has none yet), tier-1 verdict-bearing entries 35:
26 yes / 9 no = 26 percent no - against run-0's 84 percent (63/12) and
read-estate's 80 percent (48/12). Same instrument, three genres (audit /
estate-read / execute), three wildly different rates; the execute genre's
rows carry their own byte-proof so quote-entails-claim holds. CONVERGENT with
operations ("the no-rate is genre-dependent, not instrument calibration") -
independently decoded by this seat. Consequence: both addenda's E6 reading
("demotion-rule-instead-of-demotion persists") treated the no-rate as an
instrument-behavior fact; run 3 falsifies that as a cross-genre claim. Any
gate or threshold on tier-1 ratios is genre-confounded. Compounding: the
key-name lottery ran a THIRD consecutive time (my decode: supports 15,
checks 10, entries 5, rows 5 - four names in one run), despite
execute-register.dwf.ts typing the field (accuracy verified :47), so even
per-run tallies depend on which keys lanes invented. Tier-2 side (attributed,
not re-measured by me): economics read the 12-row deep-check cap at
mickey17-v2.dwf.ts:244-245; both addenda confirm 12 sampled, 5 wrong in
read-estate - at that sampled rate the 48 unchecked rows would carry ~20
undetected corrections (conditional on representativeness; the checker
selects rows, so stated as implication, not estimate). The fold prints
coverage without the error-rate beside it: a number that reads as
reassurance and is an alarm. Also verified at my read moment: deep_tier2
total 0 across all 7 checks files - run 3 has not persisted ANY tier-2 layer
yet; when its fold fires on the siblings' row-1 amendment it will exercise
the new wiring against a live archive.

Falsifier: a fourth genre whose rows carry no intrinsic proof landing at
~80 percent no again under the same checker (would support instrument
calibration over genre); or a checks file whose list keys are validated
against the runner's typed field (no validator exists estate-side).

One-sitting move (~10 min in the same fold edit): beside the verifier-table
length sums (:154-166), print the verdict-VALUE decode, the per-key name
census, the lane genre/topic tag, and "tier-2 coverage N/M with X corrections
among N" - so no reader compares ratios across genres untagged again.

## F5 (rank 5). The promotion joint is where work still dies: the E-ledger
## is prose in rolling paths, no byte reads it, so five consecutive folds
## folded blind through their own banked defects

Stat pair, mine: tools/mickey17_v2_fold.py mtime 2026-09-25T23:21Z -
unchanged across two spec addenda, 35 E-items (E1-E35), and both mega-burn
folds - while tools/workflow_gate.py mtime is 2026-10-05T05:39Z, amended
same-day twice this week (G8). The estate's promotion rule in practice: law
banked as prose (addenda, SYNTHESIS cards, E-items) -> a seat must happen to
read it -> a seat must manually execute -> sometimes bytes. No queue, no
dead-letter, no re-surfacing. The ledger that names the fold's defects lives
in the very rolling-path addenda that already ate one filing (MICKEY17_V2
addendum :10-15, its 10-03 predecessor overwritten uncommitted; survivors
only at commit 0c9d72a06). Result measured: OPERATING ENVELOPE absent from 5
consecutive folds (both addenda, fixed-string 0 hits), no fold timestamp in
5 folds, E20 recurred at 5x, E5 at 5 recurrences. CONVERGENT with all three
siblings on the frozen-organ fact; my addition is the mechanism: the
instrument cannot report its own known defects because knowledge of them
lives outside every instrument, in prose the instruments never read.

Which laws earned promotion this week, by the duplication-is-emphasis
census: E20/E5 (wiring + verdict-value blindness) re-derived by 2 SPEC seats
+ 3 sibling lenses + this lens = strongest convergence on the board; E7
moment-stamping (B2-216 demanded for import into section 7 twice, never
imported); the tier-1 merge clause (E26: the runner's persist phase already
does merge-not-overwrite - the behavior exists, the tier-1 instruction never
absorbed it; accuracy's byte-read at mickey17-v2.dwf.ts:145-146 vs :278-284,
CONVERGENT). Anti-promotion example: G8 was promoted into an instrument that
cannot bind its subject (declaration-layer regex vs parameter-layer
dispatch; all three siblings, CONVERGENT) - promotion without a binding
surface is bytes wearing law's shape.

On the ask's skeleton question: yes, the thrice-reused skeleton should be
ONE parameterized saved workflow - CONVERGENT with all three siblings (their
drift measurements stand; not re-measured here). The logic-lens reason is
stronger than economy: with three forks, the instruction sets (tier-2
instrument, master name, key-name typing, slug formula) all drift, so NO
single instrument can bind the engine; one def gives one digest, one gate
row, and a registry join that means something (see F2's reader census - the
digest join key already exists in every row).

Falsifier: a fold that names its own open defect flags in its output header
(any run, anywhere); or an instrument-side reader of the E-ledger (grep:
none).

One-sitting move (~15 min, cheapest on the board): give the fold a
KNOWN_DEFECTS constant (ids: E3, E5, E7, E20, E24) and print
"KNOWN-DEFECT <id>" lines into the FOLD_SECTIONS.md header, deleting each
line as its fix lands. Ten lines; every future fold confesses until cured;
the promotion of prose law into script bytes at the minimum possible price.

## THE RANKED AMENDMENT TABLE (executable against .zcode/workflows/*.dwf.ts
## plus the two organs every burn invokes)

| # | File | Exact edit | Defect prevented | Evidence row |
|---|------|-----------|------------------|--------------|
| 1 | tools/mickey17_v2_fold.py:186-202 | Route code-9 exclusions to a rendered "## CORRECTIONS (carried, not dropped)" section (row_key + verdict + evidence head); replace the :200 tautological assert with the reachable assertion that no included row carries a persisted deep_tier2 verdict in {unconfirmed, crashed}; stamp folded_at in the header | Invariant theater (assert cannot fire on any input); the wrong-way E20 fix that would hide law-3 rows from included; 5 unstamped folds | fold :187-202 read this sitting; run-0 addendum 1.2 + read-estate addendum 1.1 (6 rows rode included); MASTER_READ_ESTATE D5-D10 |
| 2 | .zcode/workflows/ractor-engine.dwf.ts:330-352 (+ lens-phase tail, + :253-273) | Compute status from breaker verdicts (verified only if confirmed, "proposed" otherwise); scope the verified[] claim to confirmed findings; bank revision responses to OUT/<id>.rev.md and withdrawals to OUT/WITHDRAWALS.md; add per-lens bank check mirroring :316-323 | Fabricated verdict constants in the return contract; silent withdrawal drops (negative-first-class violated by the engine); unbanked lens write-ups | ractor-engine.dwf.ts:290, :338, :253-273, :316-323 read this sitting |
| 3 | tools/workflow_gate.py:354-375 | Print "PASS (N warns)" when warned non-empty and write a top-level "warns" array into the registry row | PASS verdict masking 32 soft-false checks; write-only warn layer (0 of 6 consumers read checks) | my registry census (88 rows, 32 soft-under-PASS, 17/17 ractor-engine G6); gate :192-193, :354 |
| 4 | tools/mickey17_v2_fold.py:154-166 | Beside the length sums: print verdict-VALUE decode, per-key name census, lane genre/topic, and tier-2 coverage-with-corrections count | Genre-confounded tier-1 ratio comparison (84/80/26 percent no across genres); key-name lottery printed as a tally; coverage read as reassurance | my run-3 decode (26/9 of 35; supports 15/checks 10/entries 5/rows 5); both addenda |
| 5 | tools/mickey17_v2_fold.py (header block) | KNOWN_DEFECTS constant (E3, E5, E7, E20, E24); print "KNOWN-DEFECT <id>" lines into FOLD_SECTIONS.md until each is fixed | 5 consecutive folds blind to their own banked defects; law knowledge living only in prose the instruments never read | fold mtime 2026-09-25T23:21Z vs gate mtime 2026-10-05T05:39Z (my stat); OPERATING ENVELOPE 0 hits x 5 folds |
| 6 | .zcode/workflows/mickey17-v2.dwf.ts:145-146 + both draft forks' tier-1 persist lines | Insert merge clause into the tier-1 persist instruction (keep every existing key incl. deep_tier2; replace only lane/supports/counts) - CONVERGENT, byte-read by the accuracy lens this round, not re-read by this seat | Refire tier-1 rewrite destroying persisted tier-2 verdicts (E26 root cause) | accuracy.md finding 2 (mickey17-v2:145-146 vs :278-284); run-0 addendum 2.1 |

Kill verdict (no sacred cows): no saved workflow earns death on THIS lens's
evidence (its instruments are the subject, not the members); the retirement
candidates ride the 10-02 fleet card and the siblings' rows. The three
mega-burn drafts should not be saved as-is: one parameterized def replaces
all three (CONVERGENT, all siblings).

## Checks run this sitting (exact instruments)

1. Read in full: tools/mickey17_v2_fold.py (235 lines);
   .zcode/workflows/ractor-engine.dwf.ts (353 lines);
   tools/workflow_gate.py:320-384; both spec addenda; MASTER_READ_ESTATE.md;
   the three sibling lens files; state/CURRENT.md.
2. Registry censuses (.venv/Scripts/python.exe over memory/workflows/REGISTRY.jsonl):
   88 rows; PASS 75 / FAIL 13; check-failure frequency G6 28 / G3 16 / G4 7 /
   G7 6 / G2 6 / G5 5 / G1 4 / G8 2; soft-false under PASS 32, under FAIL 2,
   hard-false 40; 17 ractor-engine rows, all PASS, all G6:false; row keys
   {ts, name, digest, script, verdict, checks}.
3. Run-3 in-flight decode (same interpreter over
   memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/): 8 lanes, 7 checks;
   key lengths supports 15 / checks 10 / entries 5 / rows 5; 35 verdict
   bearing entries, 26 yes / 9 no; deep_tier2 total 0.
4. Consumer census: grep REGISTRY.jsonl across tools/ mag/ scripts/ -> 6
   files; grep "checks" over those six -> none reads the registry's
   checks[].ok.
5. Gate grep map: soft/G6_STAMP_RE/G8/exit lines (workflow_gate.py:10, :104,
   :112, :147, :176-184, :192-193, :253, :296, :348, :354-360, :365-375).
6. Stat: fold script mtime 2026-09-25T23:21Z; gate mtime 2026-10-05T05:39Z.

NOT run, stated: I did not execute tools/mickey17_v2_fold.py (it rewrites
FOLD_SECTIONS.md in place and would mutate the archives under audit) and did
not run the gate's --script mode (it appends a registry row; the scenario
suite was run by the accuracy lens, exit 0, not by me). No workflow was
fired by this seat. The tier-2 12-row cap cite (mickey17-v2.dwf.ts:244-245)
is economics' byte-read; MASTER_MICKEY17_V2.md was read only through the
addenda's quotes.

## Blind spots (honest)

- The 13 saved workflows I did not open (the-50, the-gala, game-dig family,
  olm-mine, salon-mine, drop-dig, wide-dig, music-cut, fill-ball,
  librarian-expedition, tree-doctrine-dig, gap-analysis) are outside this
  lens's reads; fleet-death verdicts ride the siblings and the 10-02 card.
- Run 3 is in flight: e09-e12 unlanded, tier-2 not persisted, e06 checks
  absent at my moment; every run-3 number here is a moment-read.
- The OLM mines (32/32, 22/24, daymora, zero-overlap) and the
  parked-decisions ractor receipts were not read; those claims ride the ask.
- Token figures (100M / 60M) ride the operator order, not my census.
- ListWorkflowRuns was not attempted from this seat; the run's harness-side
  state is unread by me.
- The fold_run.sh wrapper (outside the repo) was not read.
- The 42-percent-among-sampled implication in F4 is conditional on checker
  selection being representative; it is flagged as implication, not a
  measured estimate.
