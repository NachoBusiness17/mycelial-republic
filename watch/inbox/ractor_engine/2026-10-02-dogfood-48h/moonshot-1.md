# MOONSHOT-1 - dogfood the 48h window (2026-09-30T20:00Z to 2026-10-02T11:00Z)

Filed by the moonshot-1 lane of the ractor-engine 2026-10-02-dogfood-48h run.
Read before writing: watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md (whole),
state/CURRENT.md, watch/inbox/census_refresh_20261002.md (whole). Nothing below
re-derives the prior synthesis; every claim here was checked this sitting on the
current tree unless marked NOT RUN. No em-dash bytes.

## What I ran (verification stamp)

git log timestamps of the six commits; Read mag/records.py, scripts/descent_driver.sh,
scripts/astra_convo_loop.sh, scripts/start_autorun.sh, scripts/invisible_runner.vbs,
watch/inbox/census_refresh_20261002.md; grep pidfile/lock/claim across tracked files;
schtasks /Query (MSYS_NO_PATHCONV) on MagCensusPatrolDaily, MagFtsIndexDaily,
MagImproveDaily, MagLeaveProtocolDaily, EstateWalkDaily, Estate Ratchet, Estate Librarian,
Estate Gopher plus a CSV sweep for the task families; pytest --collect-only -q on
test_inference_budget (19), test_code_swarm (9), and the six garden files (91 total);
git show --name-only/--stat on 962e41054, 0c9d72a06, 3c83da5b0; a written scan
(moonshot1_cost_scan.py in this folder) plus inline python over
memory/runs/hermes_burn/usage.jsonl (236 rows) and memory/runs/model_garden/usage.jsonl
(725 rows); ListSavedWorkflows (ractor-engine definition read back); grep of TICKET_LEDGER
(at watch/inbox/hermes_burn/, the ask's memory/runs/ path does not exist), queue/todo.md,
memory/attention.md, state/CURRENT.md for commit-queue; stat logs/kpi.jsonl,
watch/inbox/NIGHT_CLOSE_20261002.md, memory/percolator/candidates.jsonl; head of the
.arc_seeds .seal artifact; tail of logs/ratchet_daily.log; git status --porcelain tests/;
git diff --stat tools/code_swarm.py. HOSTILE-PASS REVISION SITTING added: a
tail -c 4000000 logs/kpi.jsonl source census (232 of 232 rows "source":
"summarize", zero "api"); Read of mag/biography.py:580-596; a per-row dump of
every T1W2_* usage row with ts and cost_usd (10 rows; episode cuts
$0.2495 / $0.8970 / $1.1465). NOT RUN: ListWorkflowRuns (unreachable from this
child: workflow_introspection_unavailable), WMI/USN, full pytest -q, SW1 ticket tests.

## F1. The 42-test phantom is still breeding in fresh receipts

Commit 0c9d72a06 claims "inference_budget 42 tests".
watch/inbox/census_refresh_20261002.md:26-27 repeats "the inference_budget 42-test
battery" inside the receipt that concludes "no fabrication smell" (:38).
Byte truth: tests/test_inference_budget.py collects 19 tests now AND at its landing
commit (19 def test_, zero parametrize, git show 0c9d72a06 copy counted). The six
garden-night test files collect 9+9+19+13+21+20 = 91; no subset sums to 42. The only
"42" in the estate's own record is memory/rib/RIB_INFERENCE_BUDGET_20261001.md:78,
"42 green with the two carrier suites", a run-moment figure with no surviving
reproduction. So two landed records (one commit message, one same-morning receipt)
carry a number no current instrument can emit. The disease is structural: the census
refresh VERIFIES its denominator (4,147 total, reproduced independently) but
hand-copies the attribution figures. Denominators get verified; attributions get
trusted. Falsifier: any tree or receipted moment where pytest collects 42 across the
budget-related suites, or an untracked-draft file list proving the 42 existed at the
night moment and was trimmed unrecorded (which converts phantom to unrecorded decay,
still a finding). Move (one sitting, ~40 min): tools/collect_attribution.py emitting
per-file collected counts from pytest --collect-only -q, and make the census-refresh
receipt quote its per-landing rows from that output instead of hand-typing; wire it
next to the B2-244 --collect deep check in scripts/census_patrol_daily.ps1.

## F2. The double-spend fix guards one door; the vault is still open

descent_driver.sh:13-23 carries the new pidfile (exit 3 second instance, stale-pid
reclaim, trap cleanup; read this sitting, byte-true to the commit claim). But the
guard sits on the CALLER. tools/hermes_burn.py, the shared drain every caller hits,
has no lock, claim, flock, or pid mechanism (grep across the file: zero code hits;
the only "lock" matches are prose). The estate already owns the right pattern in
mag/lane_runner.py:1089-1099 (daemon refuses when pidfile held). The ledger proves
three distinct double-fire episodes, only one of which a driver pidfile can stop:
(a) 13:11-13:53Z re-fires (A1 x3 before 13:34, B2 x3, C1 x3) root-caused later to a
stale boolean; (b) 19:17:38-19:18:33Z T1W2 S5/S6/S7/S8 pairs (deltas 0.95s to 22s),
cause unattributed, predating the twins; (c) 21:28-21:53Z the twins plus pre-twin
single fires at 21:28-21:31Z. Kill the twins and class (c) dies; classes (a) and
(b) re-arm the moment any seat hand-fires hermes_burn.py while another grind is
alive. scripts/astra_convo_loop.sh and scripts/start_autorun.sh also have no pidfile
(astra is bounded 4 rounds, autorun delegates to main.py, so the live risk is the
queue, not these). Falsifier: demonstrate a concurrent second hermes_burn.py
invocation today that safely no-ops (it will not; nothing serializes it). Move (one
sitting, ~45 min): claim-lock inside tools/hermes_burn.py itself, per-queue .claim
file (pid+ts, stale reclaim, exit 4 on contention), self-stealing the lane_runner
pattern. One organ protects every door.

## F3. The OWED ledger compounds: surgery gets executed, bookkeeping decays

The two moves that stopped live bleed were executed same-sitting; registration is
byte-true but liveness is only half-proven (REVISED on hostile pass; the draft said
"verify green", overstating): schtasks read-back this sitting shows census, FTS,
improve, MagLeaveProtocolDaily all direct (powershell -File or python, no VBS), and
the census loop closed end-to-end (03:29:15Z proof fire exit 1 COLLECT-DRIFT per
census_refresh_20261002.md:3-7, answered 10:08Z with a reproduced 4,147 claim);
but at audit time all four still showed Last Result 1 from their 10-01 fires, and
FTS, improve, leave had ZERO direct fires yet (first direct fires still future at
11:00Z).
Every memory-repair move from the prior synthesis decayed instead:
- NIGHT_CLOSE_20261002.md erratum UNPAID: mtime equals its creation 2026-10-02
  05:14:18Z (NTFS, stat this sitting), grep for erratum/1.0077/10.0031 finds nothing.
- Commit-queue law (named OWED in 2093ca518): zero rows in
  watch/inbox/hermes_burn/TICKET_LEDGER.md, queue/todo.md, memory/attention.md,
  state/CURRENT.md (grep rc=1).
- logs/kpi.jsonl GREW from 748,222,017 bytes (synthesis reading ~06:58Z) to
  752,885,507 at 10:45:26Z (stat this sitting): +4.66 MB in under 4 hours, still
  growing during this audit. Hot writer CORRECTED on hostile pass (the draft named
  dashboard h_kpi; wrong organ): a tail census of the last 4 MB this sitting counts
  232 rows, 232 of them "source": "summarize", zero "api"; the hot writer is
  mag/biography.py:589-591, where summarize_session calls
  write_kpi(source="summarize") and each appended row drags the entire
  mag-agent-orc-* incomplete_ids list (visible in the file tail) through
  mag/records.py:166-167, with no rotation anywhere. What loops summarize_session
  this hot at 10:45-11:09Z is unattributed (OWED).
- scripts/invisible_runner.vbs still writes one overwritten
  %TEMP%\invisible_runner_rc.log (read this sitting); no append-mode audit jsonl;
  the 23:32:51 EDT launch stays unattributed.
Plus one NEW member of the class the window never touched: Estate Ratchet
(direct-registered all along, so not a VBS case) is red on its last fire
(10-01 09:45, Last Result 1) with logs/ratchet_daily.log (UTF-16) ending
"RATCHET: FAIL" over unaccepted GROWTH debt: concept_predictor.py 513 to 667,
duel_harness.py 461 to 581, env_contract.py 563 to 743 lines. The ratchet is
naming the uncommitted working tree's growth and the accept-or-fix protocol is
not being run. Falsifier: an existing mechanism that ages OWED items or forces
erratum payment (grep found none). Move (one sitting, ~60 min): the OWED-DECAY
gate, tools/owed_register.py reading machine-readable OWED rows (id, date, owner)
from memory/attention.md, blocking pre-push at 24h age without a receipt or named
deferral; same self-steal class as citation_lint, which already changed behavior
(githooks/pre-push:24-25 verified wired). Rotate kpi.jsonl in the same sitting at
mag/records.py:166 (size cap + rename), and throttle the real hot writer: write the
append only when pack state changed, at the mag/biography.py:589-591 call site.

## F4. Built-once instruments: only the engine itself got a second mission

Dogfood census of the window's new instruments, each checked this sitting:
- citation_lint: WIRED (githooks/pre-push:25) and fired on real prose same-day
  (SYNTHESIS.md stamp). Dogfooded.
- seed_seal: fired ONCE for real at 2026-10-02T04:10:34Z
  (watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal, schema seed_seal.v1,
  key state/keys/seed_seal_key present). Zero non-test consumers: git grep shows
  only self-references in mag/seed_seal.py; nothing verifies seals anywhere. Built,
  fired once, unconsumed.
- percolator --candidates: memory/percolator/candidates.jsonl holds 16 rows, mtime
  2026-10-02 04:17:43 EDT-moment (04:17:43 -0400 local stamp), never written again.
  Landed, single-shotted.
- code_swarm: one production run (50 clusters), tests landed (9 collected), and
  UNCOMMITTED +49-line edits in the working tree (git diff --stat) plus untracked
  tests/test_sw1_tickets.py (git status "??" on tests/): someone is iterating but
  nothing has banked. Active, un-landed.
- ractor-engine: the counterexample. Saved workflow read back via ListSavedWorkflows:
  topic is now a REQUIRED arg, gate digest moved from the commit's 912a34520349
  (f4cfcdf9b) to 5253afd2d68d (post-landing amendment, the metadata repair), and THIS
  run rides a real topic string (the fix held; the ask text itself is the evidence,
  plus the amended definition). Second mission in flight right now. Dogfooded twice.
  One residue: the saved moonshots default reads "2\r" (a CRLF artifact in the
  engine's own metadata, same churn class TICKET_LEDGER:159-160 names).
Falsifier: a second real firing of percolator --candidates or a verifying consumer
of any seed_seal.v1 seal outside tests (none found). Move (one sitting, ~30 min):
the LAND-TWICE LAW, wired into tools/workflow_gate.py's published-deliverable
predicate: a commit landing a new instrument must carry (a) one real firing receipt
and (b) a named next consumer (gate, cron, or seat), else the landing auto-registers
its dogfood debt into the F3 OWED register.

## F5. Cost truth: no paid row after 03:34:25Z; the window's receipts trail its burn

HEADING REVISED on hostile pass (the draft claimed all spend preceded the first
commit; true only of the hermes lane). Re-summed both ledgers this sitting
(moonshot1_cost_scan.py + inline python): hermes 236 rows, $37.7591, first
2026-10-01T13:11:41Z, last 2026-10-01T21:53:52Z, so the hermes lane went silent
2h53m before the first commit (00:46:30Z); garden 725 rows, $3.4746, 22:10:27Z to
03:34:25Z (byte-matches NIGHT_CLOSE:52-54), OVERLAPPING the first three commits
(00:46:30Z, 00:54:07Z, 01:57:07Z) and ending 44m02s before its own commit 04:18:32Z.
Window paid total $41.23, consistent with the commit's "Ledger ~$42 of 145". The
last three commits (04:18Z, 06:54Z, 07:31Z) are pure receipt: zero paid rows after
03:34:25Z in either ledger.
Composition of the $37.76 hermes side: A1_steer_antiforgery turn1 fired x49 for
$20.99, 55.6 pct of the whole hermes window, pure re-fire theater per the estate's
own RIB (memory/rib/RIB_INFERENCE_BUDGET_20261001.md:33, "$20.53 of $29.91 was
re-fire theater"); the stale-boolean fix landed in 43f50ed71 at 21:41Z, AFTER the
last A1 fire at 20:17:25Z, so it never proved itself in-ledger. Twin doubles sum to
exactly $2.2521 (commit's "$2.25 vs $1.09" byte-true). T1W2 S5-S8 CORRECTED on
hostile pass (the draft's "~$0.79" matched no clean cut; per-row dump this
sitting): the unattributed 19:17:38-19:18:33Z double-fire episode cost $0.2495
exactly (7 rows), the 21:28:40-21:30:54Z single re-fires cost $0.8970, all-in
$1.1465. Free-lane grind made visible:
DUEL1_hidden_5 x46 and N1_parables_songmap x42 at $0.0000 per row (refusal-retry
grind). What survives the week, verified on this tree: 91 collected tests across
the six garden files, +802 fill-ball test lines (census receipt :28-29), citation
lint wired, seed seal keyed, 61 primaries (90.6MB, receipted in 962e41054's
watch/inbox/librarian_exp/ tree), GAP_REGISTER.md, the engine, patrols re-registered
direct with one closed detect-respond loop. The 10x swing lives inside the F2 organ:
a re-fire ceiling in tools/hermes_burn.py (refuse the 4th fire of the same (id,turn)
key in 24h without a --force naming why) caps the next A1-class burn at x3 and would
have saved about $19.60 this window, half the paid spend, in ~20 lines. Falsifier
(tightened on hostile pass): any paid row timestamped after 03:34:25Z in either
ledger, or a receipt showing the x49 fires were deliberately purchased (none
exists; the estate's own RIB calls them theater).

## Blind spots

- ListWorkflowRuns is unreachable from this child (capability gap,
  workflow_introspection_unavailable): the 63.1M / 37.6M / 54.0M / 68.7M token
  figures and Salon-mine-20deep's provider stop are cited from the ask, NOT verified.
- No WMI or USN journal access run: twin liveness at this hour, the 23:32:51 EDT
  invisible_runner launch, and the 19:17Z double-fire cause remain unattributed.
- Full pytest -q not run; SW1's 17-passed not re-executed (test_sw1_tickets.py is
  untracked on disk; I collected nothing from it).
- The zcode-side token cost of the six commits has no local ledger I could find;
  dollars verified only for the two paid lanes.
- Estate Gopher shows "Multiple actions" uninspected; the wider Estate* task family
  sampled at four of about ten names.
- The 61-primaries 90.6MB claim was receipt-checked only (rows2.jsonl 975 rows in
  commit stat), not re-hashed file by file.
