# ECONOMICS LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

observed_at: 2026-10-05. Seat: lens-economics of the ractor on
OUROBOROS ROUND 1 of 5 (dogfood the standing WORKFLOW FLEET, steal the
improvements back into the definitions). Findings on the ENGINES, not the
content. Every claim below cites bytes I read this sitting: the saved defs
(.zcode/workflows/mickey17-v2.dwf.ts, ractor-engine.dwf.ts,
gap-analysis.dwf.ts), the three draft forks (.zcode/workflow-drafts/
Gap-analysis-evening / read-the-estate / execute-register .dwf.ts), the fold
gate (tools/mickey17_v2_fold.py, all 235 lines), the submit gate
(tools/workflow_gate.py), the two run addenda (watch/inbox/
MICKEY17_V2_RUN_SPEC_ADDENDUM.md, READ_ESTATE_RUN_SPEC_ADDENDUM.md),
REGISTRY.jsonl (89 rows), and the run archives on disk. Token figures
(100M read-the-estate, 60M execute-register) are from the operator order, not
independently censused by me.

## The priced picture

The fleet's hottest asset is the mickey17_v2 skeleton: three mega-burns in
36h off one shape. Its actual usage pattern is FORK, not parameterize: burn
1 (run-0) ran under the SAVED .zcode/workflows/gap-analysis.dwf.ts, which my
`cmp` this sitting proves byte-IDENTICAL to the Gap-analysis-evening draft
(the saved def IS the frozen fork); burns 2-3 ran from drafts (registry rows
85-86 name those draft paths; the saved mickey17 def's `if
(TARGETS.length === 0) throw` at mickey17-v2.dwf.ts:107-109 means the
read-the-estate slug `2026-10-04-0` (targets length 0, addendum 1.2) cannot
have run under it). Each fork re-edits the same six dimensions by hand:
inline lane table (a01-a15 / r01-r12 / e01-e08), master fold name
(MASTER_MICKEY17_V2 / MASTER_READ_ESTATE / MASTER_EXECUTE_REGISTER),
spec-addendum filename, slug formula variant, tier-2 instrument (curl vs
Read+grep), width default. None of it flowed back. That is 3 x ~22KB of
near-identical bytes with zero absorption, and one measured data-loss event
already, INTRA-run: the spec-writer phase writes each run's addendum to ONE
rolling path (mickey17-v2.dwf.ts:346-347), so run-0's own refire-state SPEC
filing (10-04) overwrote its own uncommitted 10-03 first filing at that
path (addendum supersession note, lines 10-15: "uncommitted in the working
tree at supersession"; `git log -1 --` on the path read 0c9d72a06, the 10-01
MODEL GARDEN filing, at that moment). The destroyed 10-03 bytes are NOT
recoverable from git: 0c9d72a06 holds the earlier E1-E18 ledger, and E19-E24
survive only as restatements inside the current addendum's text (my `git
log --oneline -3 -- watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md` this
sitting: a7ca49be1, 0c9d72a06, 3752abae2). Read-the-estate did NOT collide
cross-run only because its fork hand-edited the addendum filename
(read-the-estate.dwf.ts:352 -> READ_ESTATE_RUN_SPEC_ADDENDUM.md, single
commit eb687f76a, verified by git log this sitting) - collision avoidance by
fork labor, not engine design.

The most expensive standing defect is the fold gate's verdict blindness, now
at its 5th recurrence across the two completed burns: the verifier table
counts list LENGTHS (mickey17_v2_fold.py:157-160, `vc[k] += len(v)`) and the
PRISMA exclusion block reads a top-level `unconfirmed` key with a `claim`
field (:181-183) that no runner-written file has ever carried (the runner
persists `deep_tier2` entries with `row_key`/`verdict`/`evidence` only; the
read-estate addendum 1.1 proves the shapes can never meet). Result: both
runs' substantive verification truth (tier-1 84%/80% no; tier-2 11/12 then
7/5 verified/unconfirmed; 6 substantive unconfirmations riding `included`
under `excluded: 0`) existed only because a full premium SPEC-seat sitting
hand-decoded it. Two addenda, ~400 careful lines each, are the receipt. One
~25-line fold patch (decode verdict values, feed deep_tier2 unconfirmed into
excluded, stamp a generated-at line) retires the whole class and pays for
itself on the next burn.

The tier system also misleads by sampling and by genre-blind pricing: tier-2
is capped at 12 rows regardless of width (mickey17-v2.dwf.ts:244-245 slice),
so read-the-estate byte-checked 12 of 60 rows and still found 5 wrong (42%
of those checked); meanwhile its deepAsk still prices every verify as a web
curl+grep agent (:150-158) when the estate-read genre's byte-check is a local
Read+grep, a steal the execute-register fork already made ("tier-2 deep
checks were mechanical (Read + grep byte-check)", its return block) that the
saved def never absorbed.

The brand-new G8 width gate (landed TODAY by execute-register lane e04,
SUITE_EXIT=0 green on 9 cards, registry rows 87-88 show the fixture failing
as designed) prices the DECLARATION, not the DISPATCH:
workflow_gate.py:156, "Scripts that declare no max_concurrency pass (the law
binds the declared dispatch shape)". The saved skeleton declares none and
fires `Promise.all` over firstWave 8 then ALL remaining lanes
(mickey17-v2.dwf.ts:229-230, default width 50), and the draft forks carry
the same shape (execute-register.dwf.ts:223-224). The engine that built the
gate is itself ungated by it: the same class as the parked-decisions
test-pins-enforcing-the-bug catch (LAND_d3_wire.md:46-56). CONVERGENT.

Soft-warn furniture: 28 of 89 registry rows (31%) carry the identical G6
soft-warn ("receipt mention lacks a dated stamp"), 17 of them on
ractor-engine/mickey17-fork scripts; every ractor-engine PASS since
2026-10-02 warns. A warning that always fires and never escalates
de-calibrates the instrument: it trains the reader to skip soft rows exactly
when G3/G6 reasons carry real content. The fix is one comment line matching
G6_STAMP_RE (workflow_gate.py:105-107: label `source-fetched|fetched|
observed_at` + colon + date), e.g. `// observed_at: 2026-10-05 ...`.

Death row: .zcode/workflows/gap-analysis.dwf.ts is a museum snapshot
wearing a runnable name: its lane table hardcodes the 2026-10-03 evening
audit (a01-a15, "the hourly arena cadence ... $25.11",
gap-analysis.dwf.ts:107-116). The generalized form of the same skeleton
already lives in mickey17-v2. Refire risk is real (17 saved workflows, the
prior dogfood cut 19 -> 7): a refire re-audits a dead evening at mega-burn
prices. Archive it.

## THE RANKED AMENDMENT TABLE (executable against .zcode/workflows/*.dwf.ts)

| # | File | Exact edit | Defect prevented | Evidence row |
|---|------|------------|------------------|--------------|
| 1 | tools/mickey17_v2_fold.py (shared by all three burns) | Replace :154-166 verifier block and :179-193 PRISMA block: walk `checks[lid].get("deep_tier2", [])`, match entries to rows by lane-id prefix on `row_key` + `norm(claim)[:40]` containment, count verdict VALUES (tier-1 yes/no via entry `supports`; tier-2 verified/unconfirmed/crashed), feed unconfirmed/crashed into `excluded` under code 9, and write a `generated_at:` header line | The `excluded: 0` lie and the verdict-blind table, 5th recurrence; retires the full-sitting SPEC-seat hand-decode every burn now pays | fold :157-160, :179-190; run-0 addendum 1.1-1.2; read-estate addendum 1.1 |
| 2 | .zcode/workflows/mickey17-v2.dwf.ts | (a) :346-347 spec-addendum path to `MICKEY17_V2_RUN_SPEC_ADDENDUM_<RUNSLUG>.md` (per-run, never rolling); (b) new arg `master_name` default `MASTER_MICKEY17_V2.md`, swap the literals at :321,:332,:338,:344,:351,:355; (c) comment `// envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md` beside :229-230 | (a) the rolling addendum path that already destroyed run-0's own 10-03 SPEC filing INTRA-run (refire second sitting over uncommitted first; not git-recoverable - 0c9d72a06 holds the earlier 10-01 ledger); (b) E33 master-name drift, the stated reason the read-the-estate fork existed; (c) G8 exposure of the 8+all-rest wave shape | mickey17-v2.dwf.ts:107-109,:321,:346-347; addendum header 10-15; git log a7ca49be1/0c9d72a06 this sitting; E33 |
| 3 | .zcode/workflows/ractor-engine.dwf.ts | (a) after the lens phase, add the fail-tolerant per-lens bank check mirroring :316-323 (glob `OUT/<id>.md`, re-ask the lens to bank if missing); (b) one line `// observed_at: 2026-10-05 lens chapters bank to watch/inbox/ractor_engine/<slug>/<lens>.md; slug carries YYYY-MM-DD` | (a) a lens that returns findings but never banks its .md loses the write-up with no gate noticing (only SYNTHESIS.md is checked, :316-323); (b) the standing G6 soft-warn on this engine's every gate row | ractor-engine.dwf.ts:188,:316-323; REGISTRY grep: 28 G6-false rows |
| 4 | tools/workflow_gate.py | g8_width_shape_ok :151-164: soft-warn when the script has `Promise.all(` over a slice of the target array, declares no `max_concurrency`, and carries no envelope-receipt stamp (undeclared is not unbounded); plus its scenario card | The width gate passing the exact unbounded fan shape it was built to police, including the skeleton and the forks that built it | workflow_gate.py:156; mickey17-v2.dwf.ts:229-230; execute-register.dwf.ts:223-224; registry rows 87-88 |
| 5 | .zcode/workflows/mickey17-v2.dwf.ts (deepAsk :150-158) | Branch on source prefix: estate-absolute path -> "Read the file and grep the quote" (execute-register's instrument); http -> keep curl -sL | Tier-2 priced like web-verify in the estate-read genre; raises the coverage headroom the 12-row cap now binds | mickey17-v2.dwf.ts:150-158; execute-register verified-list "Read + grep byte-check" |
| 6 | .zcode/workflows/gap-analysis.dwf.ts | DIE (archive or delete): the lane table is the frozen 2026-10-03 evening; the generic engine lives in mickey17-v2 | A refire of a museum snapshot re-auditing a dead evening at mega-burn cost; fleet 17 -> 16 | gap-analysis.dwf.ts:107-116 |

## Checks run this sitting

REVISION (post hostile pass, same day): the original filing's narrative
claimed read-estate overwrote run-0's addendum and that the destroyed bytes
survive in git - both WRONG, corrected above after re-verification (cmp,
git log on both addendum paths, re-read of the supersession note). Registry
greps (`grep -c` G6 rows: 88 check rows, 28 ok:false; ractor-engine
name census: 16 + 1 rows), diff of the saved def vs the read-the-estate fork,
`cmp .zcode/workflows/gap-analysis.dwf.ts .zcode/workflow-drafts/
Gap-analysis-evening.dwf.ts` -> IDENTICAL, `git log --oneline -3 --
watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md` -> a7ca49be1 / 0c9d72a06 /
3752abae2, `git log --oneline -2 -- watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md`
-> eb687f76a only,
greps of all three forks for MASTER/ADDENDUM/RUNSLUG/wave shapes, sed read of
execute-register's fold/review tail, e04 lane grep (SUITE_EXIT=0, 9 cards),
ls of the 2026-10-05-exec lanes dir (8 lanes banked by 02:38, no
FOLD_SECTIONS.md yet at my moment), ENVELOPE_50W_HIT_20260926.md existence
check (exists). NOT run: the fold script and the gate's --script mode (both
mutate evidence or add registry rows); ListWorkflowRuns (capability gap from
this seat, so the in-flight run's live tokens are unread by me).

## Blind spots

The other 13 saved workflows (the-50, the-gala, the game-dig family,
olm-mine, salon-mine, drop-dig, wide-dig, music-cut, fill-ball,
librarian-expedition, tree-doctrine-dig) were NOT read this sitting; the
amendment table covers only the four files I byte-read plus one death-row
row. Token/cost figures ride the operator order. The fold_run.sh wrapper
(lives outside the repo, WSOUT) was not read. The 5 tier-2 corrections in
read-estate were verified as persisted verdicts by the addendum's seat, not
re-measured by me.
