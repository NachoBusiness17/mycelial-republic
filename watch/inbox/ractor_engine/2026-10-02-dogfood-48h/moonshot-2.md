# MOONSHOT-2 - dogfood the 48h window (2026-10-02, filed this sitting)

Lens: moonshot (no sacred cows, every swing grounded in one organ). Read first:
watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md (whole, this sitting); this
write-up goes beyond it on four axes it did not touch: the push boundary, the
LANDED-vs-git split, the built-never-swept instrument census, and the ledger
split. All checks below were run by me this sitting on the current tree.

## The frame the synthesis stopped one step short of

The synthesis proved the night receipt's numbers true and its neighbor claims
false, then blamed the last mile of every handoff. One level up: the estate's
TRUTH surface and its ENFORCEMENT surface are different disks. Receipts land in
watch/inbox/ and queue/ (never gated, committed or not), gates fire at git push
(a boundary crossed last at 2026-10-01 12:12:30Z), and the ledger that says
LANDED points at bytes git has never accepted. The theater is not lazy seats;
it is architecture. Every finding below is that one sentence wearing a costume.

## F1. The gates guard a door nobody has opened since 10-01 12:12Z

githooks/pre-push:10 wires the ratchet, :24-25 wires citation_lint ("PUSH-GATE:
citation_lint check --changed"), :91 the census patrol. git for-each-ref
refs/remotes shows exactly one remote ref, local/run-beta1-factory-audit-20260914,
committerdate 2026-10-01 08:12:30 -0400 (12:12:30Z). `git branch -r --contains
e3c7d341c` returns empty: no remote contains ANY of the six window commits
(git log %cI: 5d2263f10 at 10-01T20:46Z through e3c7d341c at 10-02T03:31Z EDT).
So citation_lint, landed 02:54 EDT 10-02 with the claim "changed prose
byte-checked at pre-push", has executed zero times on window prose. The
ratchet, the carrier tripwire, and the scenario suite are in the same boat,
and 116 files sit uncommitted (git status --porcelain, counted this sitting)
on a machine whose only backup remote is 8 commits stale. Falsifier: any
remote ref containing e3c7d341c, or a log line showing citation_lint exit on
window files. Move (~40 min): chain the same three gate invocations into a
pre-commit hook (githooks/pre-commit via core.hooksPath); push stays backstop.

## F2. The redemption ledger says LANDED; git says it never happened

TICKET_LEDGER tail rows SW1-01 through SW1-10 all read "LANDED-with-test"
(watch/inbox/hermes_burn/TICKET_LEDGER.md). The bytes they certify are dirty:
git status marks M tools/ocean_v2_pilot.py, tools/reverse_map.py,
tools/tier_probe.py, tools/task_wall.py, mag/preload_selector.py,
mag/desk_model_probe.py, mag/gpu_ghost.py, mag/gopher_lite.py,
scripts/handoff_escalation_watcher.py, and the test half is UNTRACKED
tests/test_sw1_tickets.py (named on disk in
watch/inbox/census_refresh_20261002.md). LANDED now means "on my disk". One
crash and the ledger certifies vapor. Falsifier: `git diff --stat` empty on
those ten paths. Move (~25 min): run the SW1 test file, commit the ten files
plus the test, cite the ledger rows in the message.

## F3. Instruments that enforce get armed once and never wired to a consume
site (corrected after the hostile pass caught my truncated census)

CORRECTION ON THE RECORD: my first draft claimed "production seals nothing,
no .seal sidecars beyond pytest tmp". That was false and the error was mine:
my `find . -name "*.seal" | head -3` truncated the census, the two pytest-tmp
hits filled the window, and I read a truncated list as the world. The hostile
pass caught it. Re-checked untruncated this sitting: exactly one production
sidecar exists, watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal
(sealed_at 2026-10-02T04:10:34.819160Z, sealed_by "mag/seed_seal.py
seed_seal.v1 (SS-1)", both grepped from the sidecar this sitting), and I
re-ran the verify myself: `.venv/Scripts/python.exe -m mag.seed_seal verify
watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.md` exit 0, seed_root
426b74e1...c440c1, matching watch/inbox/fillball/seed-seal.md:42-57 (sign +
verify exit 0, 14-test forge drill) and :103-105 (the c424b80a seed stays
deliberately unsealed). So the instrument is NOT built-never-dogfired; it is
armed, hand-dogfired once on a real artifact, and re-verified live by me.

What survives the correction, all re-checked untruncated this sitting:
seed_seal has ZERO consume-site callers (grep for seed_seal/verify_seed over
mag/ tools/ scripts/ main.py tests/, excluding the module and its own test:
zero matches; watch/inbox/fillball/seed-seal.md:58-64 confirms nothing in
mag/arc_seed.py or any consumer refuses an unsealed seed, the enforcing flip
documented operator-gated). tools/code_swarm.py and tools/rib_swarm.py:
zero .py callers, zero mentions in memory/workflows/REGISTRY.jsonl, zero
scheduled-task actions; each fired once in the garden night and never again.
Contrast mag/water_computer.py, which IS wired (mag/game_campaign.py:21,
:70). The G6-receipts warn leg, corrected UPWARD by my own census this
sitting: 19 ok:false rows in the registry since 2026-09-25T18:52:02Z, 16 of
them soft warns riding PASS verdicts (13 in-window), chronically unacted;
the other 3 (rows 1, 36, 39) are non-soft because they belong to FAIL
verdicts (tree-doctrine-dig, seatlaw scenario rows), which is the gate
working, not the disease. Falsifier: any consume site calling verify_seed
and refusing ok=False; a second .seal over the c424b80a seed; a second
code_swarm or rib_swarm invocation (registry row, task, or caller) after
10-02. Move (~30 min): wire ONE consume site, the arc_seed load path calls
verify_seed fail-closed for sidecar-bearing seeds while c424b80a passes as
armed-not-enforced, or park the flip with a dated operator row in
queue/todo.md.

## F4. OWED status: commit-shaped moves landed in hours, chore-shaped moves untouched, and the fix class already bred a sibling

Verified DONE this sitting: pidfile guard exists (grep -l pidfile scripts/
returns only scripts/descent_driver.sh), the four patrol tasks are DIRECT
(Get-ScheduledTask Mag* shows powershell -File / pythonw actions, census fired
03:29Z per census_refresh_20261002.md), the carrier bullet refreshed. Verified
STILL OPEN: NIGHT_CLOSE erratum unpaid (grep ERRATUM and 1.0077 over
watch/inbox/NIGHT_CLOSE_20261002.md: zero hits); kpi.jsonl unrotated and GROWN
to 752,846,276 bytes (stat this sitting; the prior reading grew to 748,222,017
bytes per watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md:90),
write_kpi at mag/records.py:138 is still its only writer; scripts/
invisible_runner.vbs:28 still CreateTextFile(...,
True) overwrite mode with no audit jsonl, and the 23:32:51 EDT launch remains
unattributed; commit-queue law ticketed nowhere (grep over queue/todo.md,
memory/law/registry.json, TICKET_LEDGER.md: zero rows); T1W2 19:17-19:18Z
double-fire cause still unattributed (only unrelated 19:17:50 mtime mentions
in ractor_engine receipts). NEW SIBLING of the cured disease: task
mag-docker-watchdog still rides wscript.exe watch\docker_watchdog.vbs
(Get-ScheduledTask row 1) while its four invisible_runner siblings were
converted to direct, the exact unwrapped-organ class e3c7d341c claims to have
killed. Falsifier: an ERRATUM banner, a rotation receipt under logs/, a direct
docker-watchdog action. Move (~60 min, one sitting): erratum + commit-queue
ticket row + docker-watchdog re-register + rotation at the records.py writer.

## F5. The money is honest where the ledger is the named carrier, split where it is not

The hermes ledger is memory/runs/hermes_burn/usage.jsonl. Computed this sitting
by a python row-sum over its 236 rows: $37.7591 total, 2,873,299 prompt tokens,
1,494,824 completion tokens, first row 2026-10-01T13:11:41Z, last 21:53:52Z. memory/runs/model_garden/usage.jsonl =
725 rows, $3.4746, last 2026-10-02T03:34:25Z (byte-matches NIGHT_CLOSE's
garden figure). Combined $41.2337 against commit 0c9d72a06's "~$42 of 145".
The descent protocol leg 8 names hermes_burn/usage.jsonl as THE carrier, so
any tool summing the lawful carrier undercounts the window by 9 percent.
Subscription side (ask-given, NOT re-run by me): 223.4M tokens across the four
completed workflow runs. What the money bought that survives: the arc
GAP_REGISTER (watch/inbox/gap_analysis_20261001/GAP_REGISTER.md, 247 lines) to
7/7 gaps closed (3c83da5b0) to a dogfood run that caught live state beyond its
brief (e3c7d341c), and the arc synthesis-OWED to moves 1, 2, 4 executed
same-day. A self-correcting loop that fired twice in 36h is the window's real
product; everything else is receipts about receipts. Falsifier: a garden row
banked into hermes_burn, or a register gap with no downstream fix or ticket.
Move (~20 min): make the garden writer append to hermes_burn (or amend leg 8
to name both), and compute NIGHT_CLOSE's window total from both files.

## Blind spots (honest)

Not run: WMI process census (twins already dead per commit message), pytest
suites, the 107-check gate reproduction, sweep-2 rerun. Not verified: LINKS
250 to 257 (provenance not found in my greps), sweep-2 keyword list (still
unbanked per the synthesis), the 61 primaries' bytes, subscription dollars,
docker-watchdog LastTaskResult (query returned no rows; registration shape
verified only), the engine FAIL-ledger passthrough fix (synthesis move 8) in
script bytes, and whether D1-D3 instrument diseases from 962e41054 were fixed
or only named.

Filed by moonshot-2. No em-dash bytes.
