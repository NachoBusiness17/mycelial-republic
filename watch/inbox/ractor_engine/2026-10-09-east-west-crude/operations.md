# OPERATIONS LENS: the east-west crude ractor (2026-10-09)

Lens: operations (orchestration surgeon). Jacket: the theater surface, running
output nobody consumes. Topic: THE EAST-WEST ARGUMENT, the October 2026 flow of
~1.6M mt of low-sulfur fuel oil from the Atlantic basin into Singapore on
arb economics, record VLCC freight, Brent-Dubai vs freight vs the LSFO
differential. My ground is not the trade; it is how the estate ran the work
that racts it, and what the run's own instruments say about dispatch shape,
fold integrity, commit races, silent failures, cadence health.

Instruments I personally ran this sitting (2026-10-09 evening EDT):
registry greps on memory/workflows/REGISTRY.jsonl (160 rows, zero rows dated
2026-10-08 or 2026-10-09), sha256 dual-hash of .zcode/workflows/ractor-engine.dwf.ts
under both conventions, byte-diff of the saved script vs .zcode/workflow-drafts/
ractor-engine-4.dwf.ts (IDENTICAL), tail/grep of logs/census_patrol.log,
logs/fts_index.log, logs/disk_smith.jsonl, memory/attention.md,
memory/runs/fold_locks/workflow-fold.lock.log, schtasks state query of the
three churn tasks + boot time, and scoped topic-absence greps over
memory/press/, watch/inbox/STEALTH_MINED_FINDINGS.jsonl, the economist and
research trails, and dashboard/static/x_radar.json.

## Finding 1 (high): the fleet census permanently misreads the ractor engine
as "unknown" because two digest conventions disagree with no adjudicator

memory/workflows/REGISTRY.jsonl rows 125 (2026-10-06T18:53:21Z) and 154
(2026-10-07T08:41:27Z) both classify ractor-engine.dwf.ts as status "unknown"
with digest_matches_latest_row false: the status pass hashes the saved script
to 403c5076482f while the latest gate PASS row (131, 2026-10-06T22:29:05Z)
carries d8d63f619ab9. I hashed the file myself both ways: raw bytes give
403c5076482f, but the gate's convention (tools/workflow_gate.py:704 reads with
encoding="utf-8" universal newlines, :714 hashes text.encode("utf-8"), i.e.
LF-normalized) gives exactly d8d63f619ab9. So today's dispatch IS byte-gated
(the saved script and today's draft ractor-engine-4.dwf.ts diff IDENTICAL),
and the "unknown" is a false standing alarm: the status tool's raw-byte digest
can never equal a gate digest on any CRLF file. olm-mine reads "active" only
because its bytes are LF. Impact: the census that stop-cert and fleet
retirement consume (row 154 names reclass_pass dogfood2-20261007/d03-stopcert-rows)
will forever see the estate's standing ractor as uncertifiable.
Falsifier: the STATUS-ROW writer actually hashes LF-normalized text and the
403c readings came from different bytes present at those two moments (mtimes
do not support that; saved file mtime Oct 5 20:53 predates all four rows).
Move (10 min): make the status pass hash with the gate's read_text convention
(or record both digests per row) and re-run it; the engine flips to active and
the retirement census stops carrying a phantom.

## Finding 2 (high): the engine's receipt check cannot ever confirm, and the
run's return object claims it as "verified"

.zcode/workflows/ractor-engine.dwf.ts:325 checks the synthesis receipt with
files.glob(OUT + "/SYNTHESIS.md"), a literal no-wildcard path, the exact
sandbox-rejection class the engine's own lens ask warns against at :185-187
(the OLM 2026-10-03 law). The catch at :327-329 then sets receiptBanked false
unconditionally under that class, :330-332 fires a repair ask asserting the
file "does not exist" whether or not it exists, and the return object at
:350-355 asserts "receipt existence verified via a journaled files.glob before
publishing" under "verified". On this sandbox class that verified-claim is
false by construction on every run. The fail-tolerant routing itself is right
(the 2026-09-30 OLM fix, comment at :320-322); the smell is the verified line
and the unconditional nonexistence assertion in the repair ask.
Falsifier: files.glob on a literal path succeeds in this sandbox (I could not
execute files.glob from this seat; instrument gap named below).
Move (5 min): swap the check to files.read inside try/catch and reword the
return line to what actually ran ("receipt check attempted; repair fired on
rejection").

## Finding 3 (high): the tip witness is dark through the heaviest commit
churn window

memory/attention.md carries "Tip witness fired (2026-10-09 09:30:02),
verdict: WITNESS: cannot verify: SCOPE - token cannot create gists (HTTP
403)", with the task list above it showing MagTipWitnessDaily last result 2
at 10/8 9:30 AM, i.e. a second consecutive dark day. Meanwhile the working
tree snapshot for this session shows 60+ modified files including
memory/law/registry.json and the law-enforcement trail, and sibling commits
landed today (45b15c477 and later). The witness is the instrument that makes
a chain rewrite visible; it is exactly offline while the most state-bearing
files in the estate are in motion. The alert did land (the response guidance
in attention.md is correct), so this is not silent; it is unfixed.
Falsifier: tomorrow's 09:30 run fires green after the PAT scope fix (Gists
read+write) with no rewrite detected.
Move (5 min, operator): fix the PAT scope; until then every receipt that
would cite the tip carries "unwitnessed" honestly.

## Finding 4 (medium, AMENDED after hostile pass): burn cadence outran the
disk-crisis orders; the ordering violation stands, my original refill
attribution did not

AMENDMENT (2026-10-09, post hostile pass): the breaker verdicted the original
weakened on two causal limbs and both breaks check out against the bytes:
(a) the 12:50Z smith row is NOT exec-refill evidence, seats.zcode_cache reads
100.42GB flat in both the 02:16Z and 12:50Z rows (no delta entry) while the
actual delta growers are hermes_local +8.87, repo_logs +8.66, appdata_temp
+2.91, repo_memory +0.67, summing ~21.1GB against free_gb -36.2, leaving
~15.1GB of the drop outside the smith's named buckets; (b) the row predates
both workloads' main output windows (the burn's fold cycles 21:32-21:58Z and
this ractor), so it cannot measure their cost. The corrected finding:

What stands (re-confirmed by my own runs this sitting): state/
DISK_CRISIS_20261008_CLOSE.md ordered (NEXT WINDOW steps 1-3, :33-35) AV
exclusions first, exec purge protocol, re-enable the churn tasks, reboot; the
three churn tasks (MagFreeLaneFleet, MagHermesBurn247, MagGauntletFree30)
are still Disabled (schtasks query), boot time is still Oct 8 8:27:24 PM
(reboot never fired), the AV fight is unresolved per :48, and two
multi-agent workloads fired anyway: the day-9 olm-mine burn (:49 names the
session dwfrun-ce3840bf; receipts through 17:58 EDT) and this ractor.

The workload cost, measured directly (the evidence the smith row could not
supply, per probe script _exec_probe.ps1 in this directory, run this
sitting): .zcode/cli/exec now totals 97.82GB across 6,150 session dirs
against the 76GB / 6,091-entry post-purge baseline (DISK_CRISIS :47), and
the day-9 burn session alone (sess_dwf-dwfrun-ce3840bf*) holds 23.57GB in 62
dirs with file mtimes spanning 10:18:25 AM to 5:10:47 PM today, i.e. the
entire 23.57GB is day-9 output; this ractor holds 0.04GB mid-flight. So one
day-burn writes ~24GB of exec log in seven hours, into the exact surface the
crisis doc named as THE monster (:11), on a machine whose purge protocol
(:34) requires a quiesced fleet that was never quiesced. The fold layer is
healthy (memory/runs/fold_locks/workflow-fold.lock.log shows clean
acquire/release cycles for olm-mine:2026-10-09 at 21:32-21:58Z, no stale
lock held now), so the corruption risk is contained; the recurrence risk is
capacity plus an unquiesced purge.
Falsifier (tightened): (1) tomorrow's 12:50Z smith row shows zcode_cache
absorbing roughly the measured 23.57GB AND free_gb stabilizing above ~400GB
under the same cadence (then per-burn exec output is below crisis class and
the ordering risk is capacity-tolerable); (2) the ordering cure lands (tasks
re-enabled or AV exclusions confirmed) making the violation moot; (3) the
burn's exec growth is offset elsewhere (e.g. the 7d purge deletes faster
than writes), which tomorrow's entry count versus today's 6,150 would show.
Move (10 min with the operator): land the AV exclusions and the re-enable or
hold decision BEFORE the next day-burn fires; add a smith alert on the
zcode_cache bucket's daily delta (the bucket already exists in each row and
today proved it can stay flat while a burn writes 24GB underneath it, so the
alert belongs on a direct .zcode/cli/exec walk, exactly what _exec_probe.ps1
does).

## Finding 5 (medium, my jacket): the topic's bytes live nowhere in the
estate; this ractor rides operator-carried numbers over a dead press surface

Scoped censuses I ran: grep of memory/press/ for VLCC, Brent, Dubai,
arbitrage, 1.6M, fuel oil returns zero hits; STEALTH_MINED_FINDINGS.jsonl,
dashboard/static/trails/economist.jsonl, research.jsonl, and x_radar.json
return zero topical hits (the only "oil" match is the substring inside
"foils", research.jsonl:158). PRESS_DIGEST.md regenerates on cadence (header
2026-10-09T19:43:54Z) but its Pressing item is filed 2026-09-19: a live
surface carrying 20-day-old content, theater in my exact jacket sense. Net:
the biggest flow story of the operator's month had zero estate capture before
this ask; the regime numbers in the brief (Brent 104.82 vs WTI 91.02, VLCC
~1.3M USD/day, 1.5-1.6M mt LSFO) are operator-carried, so the hostile second
pass can only byte-check lens reasoning against the ask, not against banked
estate bytes. That weakens every downstream verdict on this topic.
Falsifier: the S&P Global Singapore LSFO story already banked in a corpus
corner outside my scoped greps (my full-tree grep did not complete; see blind
spots).
Move (15 min): aim one free-lane stealth cycle at S&P Global Platts
arb-flow coverage (Singapore LSFO receipts, Brent-Dubai, VLCC spot) banked to
memory/press/, so the next ractor on this topic cites estate bytes.

## Corrections of my own drafts (kept for the hostile pass)

1. I first read logs/disk_smith.log MISSING as a silent task failure; wrong
filename. The instrument writes logs/disk_smith.jsonl, has a 12:50:02Z row
today, and MagDiskSmithDaily reads Ready. The smith is healthy; my grep was
the defect.
2. I first framed Finding 1 as a gate bypass (bytes drifted past the PASS).
My own dual-hash experiment falsified that: the gate convention hashes the
exact saved bytes to the PASSed digest. The defect is the census instrument,
not the gating.
3. I first read the patrol's "alert appended" for 7 unhealthy tasks as not
landing (my grep terms were wrong); the alert block exists in
memory/attention.md with the named task list.
4. The hostile second pass verdicted my original Finding 4 refill story
weakened and it broke on the bytes: the 12:50Z smith row shows zcode_cache
FLAT (100.42GB, no delta entry), not exec refill, and the row predates both
workloads. I re-measured with a direct probe (_exec_probe.ps1, kept in this
directory): exec 97.82GB total vs the 76GB post-purge baseline, day-9 burn
session 23.57GB all written today (oldest file 10:18:25 AM). The corrected
finding above carries the ordering violation plus the direct measurement,
with the fabricated causal limb struck.

## Blind spots (honest)

- files.glob is not executable from this seat (no such tool here), so Finding
  2's sandbox-rejection premise rests on the ask's law citation and the
  engine's own comment at :320-322, not my own execution.
- The STATUS-ROW writer's identity is not pinned; my repo-wide writer grep
  did not complete before I stopped it (disk-churn discipline during the
  IO-sensitive window). The classification rule is quoted from registry row
  154.
- The full-tree topic-absence grep did not complete (stopped for the same
  reason); Finding 5's absence claim is scoped to the organs named above,
  instrument = the greps listed, per the quantifier law.
- I cannot see the parent session's CreateWorkflow call; "this run rides the
  saved bytes" rests on the byte-identical 18:08 draft, the diff, and the
  harness session naming, not on the dispatch record itself.
- Boot-time, task states, and lock states are single-moment readings; they
  can change after this sitting.
- The market substance of the east-west argument (Brent-Dubai vs freight vs
  LSFO differential, structural-vs-freight-window) is the economics lens's
  ground; I audited the run and the provenance, not the trade.
