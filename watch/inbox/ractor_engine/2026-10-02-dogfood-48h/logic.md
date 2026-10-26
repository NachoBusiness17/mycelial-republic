# LOGIC LENS: instrument theory of the 48h window (2026-09-30T20:00Z to 2026-10-02T11:00Z)

Run: ractor_engine / 2026-10-02-dogfood-48h. Lens: logic (instrument theorist).
Jacket: two instruments disagreeing with no adjudicator. Method: every claim below
was checked this sitting on this host, commands named inline; anything not verified
is marked OWED, never asserted. Prior synthesis
(watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md) was read first and is not
re-derived; everything here extends or contradicts it on fresh bytes.

## The inference rules the window actually runs

The estate's exit contracts are real and consistent at the hook:
githooks/pre-push:10 runs violation_ratchet check --changed, :25 runs
citation_lint check --changed, :91 runs census_drift_patrol with WARN-only stale
and exit-2 blocks (all three grepped this sitting). The contradiction is one
level up: the instruments that STATE estate truth (GAP_REGISTER, commit
messages, the AGENTS.md carrier) have no exit contract at all. Three verdict
levels exist in bytes (blocking, warn, OWED-prose) but the broadcast channel
chooses its own level per sentence. Findings below are that choice misfiring.

## F1. The gap-state instrument and the commits that cite it disagree, and the register is write-once (jacket instance)

GAP_REGISTER.md last write is 2026-10-01T22:41:58Z UTC (powershell Get-Item,
this sitting). Its table (:73-84) carries 12 ranked rows and NO status column;
no row is annotated closed. Commit 3c83da5b0 (git log, 10-02 02:54Z) claims
"all 7 register gaps CLOSED" against a 12-row register whose closure state is
unrecordable from its own bytes; the denominator 7 is not derivable from the
instrument. The register's row 1 still says the EstateWalkDaily defect "repeats
10-02 09:15" while 5d2263f10's own message claims the script rewritten with
absolute paths and smoke-proved (the 10-02 09:15 EDT fire is 13:15Z, after the
window end; untestable, OWED). The dogfood run's own accuracy lens named this
at landing ("the register itself converted zero rows",
watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/accuracy.md verdict block);
12h later the bytes are unchanged. Two instruments disagree (register: 12 open
rows; commits: closed) and no adjudicator exists; the fillball receipts ARE
index-registered (grep -c fillball watch/inbox/INDEX.json = 11) but the index
does not feed the register.
Falsifier: a status column or closure annotations found in GAP_REGISTER.md, or
a fillball receipt that rewrites register rows.
Move (~30 min): one annotation pass over GAP_REGISTER.md marking rows
2,3,4,6,7 and the row-11 SS-1 part CLOSED with receipt links (fillball/*.md),
re-ranking the live rows; or the register declares its successor instrument.

## F2. The citation lint's blocking teeth bind only to path:line anchors; the carrier class is structurally outside them

I ran ./.venv/Scripts/python.exe tools/citation_lint.py check --files AGENTS.md:
"CITATION-LINT: ok records=1 anchors=0 numbers-checked=15 blocking=0". Zero
anchors extracted from the estate's most citation-dense record, because
ANCHOR_RE (tools/citation_lint_io.py:70-72) requires a :line suffix; AGENTS.md
cites bare paths (tests/test_sw1_tickets.py, scripts/census_patrol_daily.ps1,
receipt paths) almost exclusively. Synthetic probe (run this sitting): a temp
record citing a nonexistent file bare AND the same class with :line returned
"blocking=1 PATH-MISSING tools/nope_missing_probe.py" for the :line form and
nothing for the bare form; the bare nonexistent path passed. So the
191.8M-class phantom disease's home grammar (bare path + number sourced to a
receipt) is unreachable by the blocking check, and commit messages, where
0c9d72a06's false "position channel half-channel banked" lived (prior
synthesis :54-58), are not files at all and covered by nothing. New instance
minted in the window: e3c7d341c claims "8 lenses + 2 moonshots rode" while the
run banked exactly 6 lens + 2 moonshot rider files (ls of
watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/), and its "88 findings
survived" is not countable from any banked receipt (OWED); the same commit's
"8 ranked moves" IS byte-true (8 numbered items under "## Ranked moves" in
that SYNTHESIS.md, counted this sitting). The ungoverned channel mixed true and
false counts in one sentence pair.
Falsifier: a bare-path existence check anywhere in citation_lint's blocking
path (it would have flagged my probe's bare cite), or commit-message coverage
by any instrument (none found by grep).
Move (~45 min): add a PATH_RE-based bare-path existence check (blocking) to
citation_lint for changed prose records plus one test row; the probe file
pattern is already written above and reproducible.

## F3. The twin fix is instance-level where the disease is path-level, and its efficacy claim has zero observations

My whole-file scan of memory/runs/hermes_burn/usage.jsonl (236 rows, python,
this sitting) finds 29 sub-60s same-(id,turn) pairs. Beyond the synthesis's
T1W2_S5/S7/S8 (19:17-19:18Z) and the 13 twin-window keys (21:39-21:53Z), the
pre-twin class also hit A1_steer_antiforgery, N1_parables_songmap and
DUEL1_hidden_5 in tight pairs at 19:20:30-38, 19:53, 19:58 and 20:01Z; both
copies carry real cost (A1 turn 1: cost_usd 0.3323 then 0.3715, 7.47s apart;
T1W2_S7: 0.0493 then 0.0669, 0.95s apart). So the double-fire predates any
twin by 80+ minutes on at least 6 keys and the OWED "cause unattributed"
extends. The installed guard (scripts/descent_driver.sh:10-23, read this
sitting) prevents twin descent_drivers only; the drain path itself has no
claim lock (grep -n "lock|claim" tools/hermes_burn.py matches only prose
comment lines :152-156,:226), so any second consumer of the queue reproduces
the double-drain. And the ledger's last row is 2026-10-01T21:53:52Z: there
has been NO paid dispatch since, so the guard has zero post-fix observations;
its efficacy is unfalsified, not proven.
Falsifier: a post-guard dispatch window with zero near-simultaneous same-key
pairs (proves the guard sufficient for the twin class), or any claim-lock in
the queue writer (grep finds none).
Move (~40 min): atomic claim row keyed by (id,turn) at the drain in
tools/hermes_burn.py, second claimant skips and logs; the next driver session
then either double-fires (cause elsewhere, guard insufficient) or does not.

## F4. The last-mile disease collected three more convictions THIS morning, including the engine's own younger synthesis

Of ractor-topic SYNTHESIS.md's 8 ranked moves (filed ~06:58Z), the unpaid set
at ~12:00Z is byte-checkable: move 3, no erratum landed in
watch/inbox/NIGHT_CLOSE_20261002.md (grep for ERRAT|10.0031|1.0077|55.2: zero
hits; LastWriteTimeUtc still 05:14:18Z, its creation moment); move 7, the
commit-queue law named OWED in 2093ca518's message has zero rows in
watch/inbox/hermes_burn/TICKET_LEDGER.md, queue/todo.md and
memory/law/registry.json (grep, this sitting); move 5, logs/kpi.jsonl GREW
from the synthesis's 748,222,017 bytes to 752,846,276 (Get-Item, this sitting)
with no rotation at the mag/records.py:138 writer. New same-class instance:
the receipt the AGENTS.md carrier now cites as its authority,
watch/inbox/census_refresh_20261002.md (read this sitting; it adjudicates
patrol 4,188 vs carrier 3,550 vs fresh 4,147 at 10:08Z), is itself
unregistered: grep -c census_refresh_20261002 watch/inbox/INDEX.json = 0, as
is NIGHT_CLOSE (0). The receipts that reconcile instrument disagreements sit
outside the shared index, so the next reader's map again says nothing is
there. The engine executed the dogfood-gaps synthesis's moves (04:36Z, via
e3c7d341c 07:31Z) and shelved its own younger synthesis's moves; my own
jacket: two engine receipts disagree about what is owed and no adjudicator
tracks either.
Falsifier: an erratum banner in NIGHT_CLOSE, a commit-queue row in any of the
three ledgers, kpi.jsonl smaller than 748MB, or INDEX rows for the two
receipts.
Move (~45 min): execute synthesis moves 3+7 as one sitting (erratum text
already drafted in the synthesis; ticket row text exists in 2093ca518), and
register both receipts through the sanctioned index writer.

## F5. Instrument dogfood census: what was fired in anger vs built and shelved

Fired in production: code_swarm (SWARM-1, 50 real clusters, per 0c9d72a06;
tests/test_code_swarm.py exists), rib_swarm (test_rib_swarm.py), water computer
(test_water_swarm.py), percolator --candidates (the producer file
watch/inbox/frontier_olm_2026-10-01/percolator_candidates.jsonl exists and
memory/percolator/candidates.jsonl holds 16 rows written 2026-10-02T04:17:43Z,
AFTER the 02:54Z landing: the arc fired post-landing), and the ractor engine
(this run; my own ask carries a bound topic, so the front-door fix held for
n=1). Built and shelved: mag/seed_seal.py has zero callers outside its own
file and test (grep across mag/ tools/ githooks/ scripts/), and its
operator-gated enforcing flip is ticketed nowhere (grep seed.seal in
queue/todo.md and TICKET_LEDGER.md: zero) = a gate that cannot fire unless a
human remembers unaided. The engine's topic fix is metadata-only:
.zcode/workflows/ractor-engine.dwf.ts:29-32 marks topic required:true, but the
runtime still coerces (String(args.topic) at :84, :141, :226; the only throw
in the file is a rethrow at :196); a rerun or amendment that omits topic would
still ride "The topic: undefined" exactly as ractor-topic did. The fix lives
at the front door, not in the house.
Falsifier: a caller of seed_seal in production bytes, a ticket naming the
flip, or a runtime topic validation in the engine file.
Move (~30 min): add 3 lines to the engine before SLUG construction: if
(!args.topic) throw new Error("topic required (ractor-topic 2026-10-02
defect)"); plus one ticket row naming the seed-seal flip decision date.

## Cost and what survives (my slice; full dollars are the economics lens's beat)

Workflow tokens this window (from the run list in the ask): Gap 63.1M,
Librarian 37.6M, Dogfood 54.0M, Fill-ball 68.7M. Surviving capital I can touch
today: 6 new test files (test_seed_seal, test_citation_lint,
test_percolator_candidates, test_code_swarm, test_rib_swarm, test_water_swarm,
all ls-verified), the pidfile guard, the re-registered patrol tasks, and the
pre-push lint+ratchet wiring. Not yet surviving: register annotations (F1),
bare-path lint teeth (F2), the claim lock (F3), the erratum and two index rows
(F4), the seed-seal flip (F5).

## OWED (never asserted)

- The "88 findings survived" count in e3c7d341c: not countable from the banked
  receipts by me this sitting; the 6+2 rider files use mixed finding formats.
- Whether the 10-02 13:15Z EstateWalkDaily fire passes: after the window.
- The 19:17-20:01Z pre-twin double-fire cause: unattributed and currently
  unobservable (ledger dark since 21:53:52Z).
- Harness enforcement of required:true engine args: not tested (would need a
  deliberate topic-less fire; refused to spend it).
- The system-reminder snapshot of AGENTS.md I was handed showed
  tests/test_swarm1_tickets.py while the working tree correctly says
  tests/test_sw1_tickets.py (grep counts 0 vs 1); the snapshot, not the file,
  is wrong; no action.

## Blind spots (honest)

- I did not re-run WMI/process census, the full pytest suite, or any paid
  dispatch; all liveness claims about processes are from bytes and receipts.
- I did not read the fillball lane archives end to end (7 receipts, titles
  only) so a closure annotation existing in a lane file but not the register
  would soften F1's denominator claim, not its adjudicator claim.
- Census adjudication prose (AGENTS.md carrier) was read as given in the
  session snapshot plus targeted greps; I did not re-verify the 4,188 patrol
  number from logs/census_patrol.log myself (the receipt quotes it; the log
  was not opened this sitting).
- Economics per commit in dollars: outside my lens this sitting; hermes ledger
  ~$42 figure is from the ask, not re-summed.

Filed by the logic lens. No em-dash bytes in this file (composed without them).
citation_lint self-run on this file: not run (it would check only :line
anchors per F2; noted as irony, not as a pass).
