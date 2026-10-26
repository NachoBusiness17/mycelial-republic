# BREAK-ACCURACY - hostile second pass over the accuracy lens (2026-10-02, ~11:10Z)

Target: watch/inbox/ractor_engine/2026-10-02-dogfood-48h/accuracy.md (mtime
2026-10-02T10:54:14Z). The ask's copy of finding 5 arrived truncated mid-JSON;
the complete finding was read from the lens's own filed write-up
(accuracy.md:105-119) and verdicted from that. Every check below ran this
sitting; commands named. No em-dash bytes.

## Verdicts

### F1 kpi.jsonl unrotated and growing: CONFIRMED

- python os.stat this sitting: logs/kpi.jsonl = 753,243,806 bytes, mtime
  2026-10-02T11:06:49Z. That is +397,530 bytes PAST the lens's 752,846,276
  (10:42Z): the growth is live at a second moment, not a stale read.
- Writer verified: mag/records.py:138 (def write_kpi) with the sole path
  constant KPI_LOG at mag/records.py:17. Repo-wide grep for "kpi.jsonl" over
  mag/ tools/ scripts/ githooks/ finds only records.py, a mimosa hook-state
  baseline cache of an old session's source, and commentary in
  tools/gap_sentinel.py:14 and :255 (a reader naming the disease, not a
  writer).
- Zero rotation: grep -in "rotat" mag/records.py = zero hits.
- Lens delta arithmetic checks: 752,846,276 - 748,222,017 = 4,624,259.

### F2 awareness layer dark, 4 of 8 synthesis moves unpaid: CONFIRMED

- mtimes (python os.stat): NIGHT_CLOSE_20261002.md 2026-10-02T05:14:18Z
  (= 01:14 EDT, its creation); scripts/invisible_runner.vbs
  2026-09-30T14:59:12Z (= 10:59 EDT); queue/todo.md 2026-09-29T10:53:55Z
  (= 06:53 EDT); state/CURRENT.md 2026-09-30T11:56:08Z.
- state/CURRENT.md read whole (485 bytes): :8 "updated:
  2026-09-30T11:56:08.790449+00:00"; :20 Latest result =
  watch/inbox/last_mile_20260930/AC_WAVE_SYNTHESIS.md. The live-truth
  pointer predates all six commits.
- Move 3 unpaid: grep -in "erratum" NIGHT_CLOSE_20261002.md = zero.
- Move 6 unpaid: grep -inE "audit|jsonl" scripts/invisible_runner.vbs = zero.
- Move 7 unpaid: grep -inE "commit.queue|commit_queue" over queue/todo.md,
  memory/law/registry.json, and the CORRECT ledger path
  watch/inbox/hermes_burn/TICKET_LEDGER.md = zero rows. Path note: the ask's
  evidence list names memory/runs/hermes_burn/TICKET_LEDGER.md, which does
  not exist on disk; my first grep aborted on it (exit 2, no such file). The
  ledger lives at watch/inbox/hermes_burn/TICKET_LEDGER.md; its :157 row two
  reads "issued 65 / run 48 / parked 17", also byte-verifying the lens's
  true-claim list.
- Moves 1, 2, 4 paid, verified live: MSYS_NO_PATHCONV=1 schtasks /Query /V
  this sitting shows all four tasks DIRECT (MagCensusPatrolDaily,
  MagFtsIndexDaily, MagImproveDaily -> powershell -File scripts/*.ps1;
  MagLeaveProtocolDaily -> .venv python tools/leave_dispatcher.py), zero
  wscript actions, Status Ready, Last Result 1 on all four (the census
  task's 1 is the designed 03:29Z COLLECT-DRIFT trip per
  census_refresh_20261002.md:3-7; the other three are pre-fix red fires;
  first post-fix scheduled fires are 12:30Z/13:00Z today, after this pass).
- 23:32 launch still unattributed: grep -rn "23:32" over watch/inbox +
  scripts (excluding bearableguy) hits only unrelated burn_reset_20260927
  mtime strings.

### F3 guard on the launcher, not the drain: CONFIRMED (one evidence-line correction)

- tools/hermes_burn.py: the only "claim" hit is prompt prose at :156
  (byte-exact as the lens said); the only lock-pattern hits (:152, :155,
  :226) are the substring "block" in prose ("estate-law block", "EVIDENCE
  block"), zero lock mechanism.
- tools/ds_workhorse.py: zero hits for claim|lock|pidfile|mutex|.pid.
- scripts/astra_convo_loop.sh and scripts/vast_ollama_bootstrap.sh: zero
  pid/lock hits.
- Guard verified: scripts/descent_driver.sh:10-23 (pidfile, second instance
  exit 3, stale-pid reclaim, trap cleanup); git log -S "PIDFILE GUARD" lands
  only e3c7d341c.
- Doctrine line verified: mag/autodrain.py:6 "SINGLE INSTANCE (pid lock) -
  two loops = double cadence + CPU hog (the known failure)"; commit
  47d3907e3 dated 2026-08-25 20:43:35 -0400. scripts/descent_driver.sh:2 is
  dated 2026-10-01, about five weeks later.
- CORRECTION (evidence line, not verdict): the lens's submitted evidence
  says grep "19:17" across watch/inbox "hit only unrelated burn_reset_20260927
  files". False as a grep result: grep -rln "19:17" watch/inbox hits about
  40 files, including watch/inbox/hermes_burn/T1R1_roast_descent_protocol.md:13
  documenting T1W2_S5's first fire at 19:17:38 (prompt 554, evidence []) and
  its 21:28:40 re-run, plus DAY1_CROSS_RACTOR.md:285 naming "T1W2 (19:17Z)".
  None of the hits attributes a CAUSE, so the finding's core (cause
  unattributed, double-fire class predates the twins) survives; the lens's
  grep-report sentence is the evidence-precision disease it hunts.

### F4 "inference_budget 42 tests" vs 19 collected: CONFIRMED and STRENGTHENED

- Ran: .venv/Scripts/python.exe -m pytest --collect-only -q -p
  no:cacheprovider tests/test_inference_budget.py -> "19 tests collected in
  0.62s".
- No drift anywhere: git diff HEAD --stat on the file = empty (exit 0);
  git log 0c9d72a06..HEAD on the file = empty; def-count at the commit tree
  (git show 0c9d72a06:tests/test_inference_budget.py | grep -c "def test_")
  = 19. The file never held 42 test functions at any reachable tree moment.
- Falsifier hunted, unsatisfied: grep across watch/inbox/model_garden for
  "42 test", "tests: 42", "42/42", "42 passed" = zero hits; BATTERY.md's
  only "42" matches are sha256 hex; per-file collects of all six garden
  test files (claritas 9, code_swarm 9, inference_budget 19, model_garden
  13, overmind 21, rib_swarm 20; total 91) admit no inference_budget-
  including combination that reads 42.
- Downstream repeats verified: watch/inbox/census_refresh_20261002.md:26 and
  AGENTS.md:27 both carry "42-test battery" with no instrument named.

### F5 window cost and survival: WEAKENED (core confirmed, one sub-claim killed)

Confirmed by exact re-derivation (heredoc python over both ledgers):

- memory/runs/hermes_burn/usage.jsonl: 236 rows, sum cost_usd 37.7591,
  first ts 2026-10-01T13:11:41.335449Z, last ts
  2026-10-01T21:53:52.578003Z. All four lens figures byte-exact.
- prompt+completion = 4,368,123 (2,873,299 + 1,494,824). Byte-exact.
  (Disclosure: my own first pass mis-summed by returning only the first
  matching key per row; the corrected script reproduces the lens's figure.
  The error was mine, not the lens's.)
- Night window (ts >= 2026-10-01T21:31:24): 43 rows, $5.5208, p+c+r
  1,081,794. Byte-exact.
- Drain idle since 21:53:52Z on this ledger (the kill held).

KILLED sub-claim: "the night close's 5,547,496 ... an instrument-mix the
receipt does not name". The receipt names its mix:
NIGHT_CLOSE_20261002.md:50 says "usage ledgers" (plural) and :52-54 itemizes
both files (hermes 43 rows $5.5208; garden 725 rows $3.4746). My re-sum of
exactly those two ledgers' night windows = $8.9954 and p 3,515,869 /
c 1,202,028 / r 829,599, total exactly 5,547,496. The figure is the exact
sum of the two instruments named two lines above it; the "exceeds this
ledger's night p+c+r" comparison is true arithmetic against a claim the
receipt never made.

## What the lens missed (additions)

1. The adjacent uninstrumented number: commit 0c9d72a06's message ends
   "Ledger ~$42 of 145". Exact combined sum of the two ledgers = 37.7591 +
   3.4746 = $41.2337. The "~" hedges, but this number sits in the exact
   class the lens was sweeping and went unflagged while a well-formed
   number (5,547,496) was charged.
2. The blind head is longer than reported: memory/runs/model_garden/
   usage.jsonl first row 2026-10-01T22:10:27Z. Both usage ledgers are blind
   for the window's first ~26 hours; the GAP ANALYSIS and LIBRARIAN days
   are unpriced by any usage ledger.
3. LINKS 250->257 RESOLVED (the lens's OWED): memory/corpus/LINKS.jsonl =
   257 lines this sitting (wc -l). The live counter exists and reads 257.
   (watch/inbox/LINKS.jsonl is a different surface, 400 lines.)
4. seed_seal has never fired in production: grep for callers across mag/
   tools/ scripts/ githooks/ main.py finds zero outside tests (only the
   module's own pyc); the only .seal sidecars on disk are pytest fixtures
   (agents/pytest-tmp-10040/*). Live re-run this sitting:
   pytest tests/test_seed_seal.py -q -> 14 passed in 0.91s. Built, tested,
   unwired: of the fillball instruments only citation_lint is wired
   (githooks/pre-push:24-25, verified in the working tree); percolator
   --candidates also has zero callers (grep over scripts/, tools/, main.py;
   scripts/percolate_reconcile.py carries no "candidat" hit).
5. The 19:17 grep evidence-line is false as stated (see F3 correction):
   about 40 files hit, including the T1W2 phenomenon documentation in
   T1R1_roast_descent_protocol.md:13. The conclusion survives; the accuracy
   lens's own grep report fails byte-check, the B2-216 disease it hunts.
6. Working tree moved 110 -> 118 (git status --porcelain | wc -l this
   sitting): both readings are moment-scoped and true at their moments;
   tree readings drift by the hour on this estate.
7. ListWorkflowRuns reproduces the identical error in this session
   (workflow_introspection_unavailable): the four workflow token counts
   (63.1M / 37.6M / 54.0M / 68.7M) remain ask-given. The lens's top blind
   spot is an environment fact, now double-confirmed, not a lens omission.

## Not run (and why)

- Nous live balance re-probe (paid call). WMI process-birth and USN journal
  (transient/admin instruments). The 61-primaries census beyond the lens's
  2-file sample: I counted the holding dir
  corpus/papers_reference_nonredistributable = 80 files / 138,943,312 bytes,
  which predates the expedition and cannot split the 61/90.6MB claim either
  way. First scheduled post-fix patrol fires (08:30/09:00 EDT = 12:30/13:00Z)
  fall after this pass.

Filed by break-accuracy, ractor run 2026-10-02-dogfood-48h.
