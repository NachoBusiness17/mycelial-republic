# break-economics: hostile second pass on the economics lens

Seat: break-economics (ractor-engine, 2026-10-02-dogfood-48h). Filed ~11:30Z 2026-10-02.
Ask: byte-check every evidence cite in economics.md against the estate, verdict each finding, add what the lens missed. Laws held: no em-dash bytes, every claim carries path:line or command+output, everything unverifiable marked OWED. No file outside this receipt was edited.

Ground truth this pass ran on: HEAD = e3c7d341c (2026-10-02T03:31:54-04:00 = 07:31:54Z), confirmed `git rev-parse HEAD` + `git log --oneline -3`.

## Verdicts

### F1 citation-lint wiring: CONFIRMED (and widened)

Every leg re-ran byte-true:

- `git show --stat 3c83da5b0`: tools/citation_lint.py +333, tests/test_citation_lint.py +341 committed; githooks/pre-push NOT in the 53-file list.
- `git show HEAD:githooks/pre-push | findstr /c:"citation_lint"`: zero matches.
- Working tree githooks/pre-push:24-25 runs `.venv/Scripts/python.exe tools/citation_lint.py check --changed || exit 1`.
- `git diff --stat -- githooks/pre-push`: exactly 15 insertions, 0 deletions; `git status --porcelain` shows ` M githooks/pre-push`.
- `git log --oneline -3 -- githooks/pre-push` tops at f0768f3be (predates the wiring).

Width the lens missed: the disease is TWO organs, not one. `git show HEAD:AGENTS.md | grep -c "Citation lint at pre-push"` returns 0 and `git diff -- AGENTS.md | grep -c "^+.*[Cc]itation"` returns 2, so the law text (AGENTS.md bullet) is ALSO working-tree-only. A clean checkout at e3c7d341c gets neither the gate nor the doctrine that claims it.

### F2 paid-burn waste, fixes unproven live: CONFIRMED with two byte corrections

Re-ran the whole ledger math (`./.venv/Scripts/python.exe -c` over both jsonl files):

- memory/runs/hermes_burn/usage.jsonl: 236 rows, $37.7591, ts 2026-10-01T13:11:41Z to 21:53:52.578Z, zero rows after. Byte-true.
- memory/runs/model_garden/usage.jsonl: 725 rows, $3.4746 (note: this ledger lives under memory/runs/, not watch/inbox/model_garden/; it runs to 2026-10-02T03:34:25Z, so paid rows DO exist after 21:53Z on the garden rail; the "zero rows after 21:53Z" claim is hermes_burn-only).
- Sum $41.2337 = the lens's $41.23 = 0c9d72a06's "~$42 of ~$145" within rounding.
- Duplicate census: 24 dup (id,turn,model) keys over 189 rows. B2_drift_rows_attribution turn1 x6 at $1.4796 byte-exact. DUEL1_hidden_5 turn1 x46, N1_parables_songmap turn1 x42 (both named as the disease at tools/hermes_burn.py:29). 89 ok:False rows, all $0.
- tools/hermes_burn.py:20-33 law block byte-true: "$18.89 of $29.91" at :22, "A1 45x at $20.53" at :25, "DUEL2 fired 14 paid calls" at :32. ECON.md:22-23 carries the "~40%" inflation line (lens cited :24-26; off by two lines, content true).
- `./.venv/Scripts/python.exe -m pytest tests/test_carrier_patch_t1w1.py -q -p no:cacheprovider`: 10 passed in 0.66s. Collect-only shows all three fix classes covered: landed-beats-force (3 tests), refused-terminal (2), evidence-preflight (5).

Correction 1 (dollar attribution): A1_steer_antiforgery turn1 x49 is $20.9891 (55.6 pct of ledger), not "$21.8518 (58 pct)". $21.8518 is turn1+turn2 combined (49+3 rows). The finding's "~$21+" survives because the arc total is exactly the lens's number; the per-turn label was wrong.

Correction 2 (timing): "all fixes landed 7-11h AFTER the money burned" is wrong for the main guards. The carrier-patch laws landed in 5d2263f10 at 2026-10-02T00:46:30Z (git log -1 --format=%cI; `git show 1a1efc67f:tools/hermes_burn.py | grep -c "LANDED BEATS FORCE"` = 0, at 5d2263f10 = 1), which is 2h53m after the last burn row 21:53:52Z. Only the twins kill (e3c7d341c, 07:31:54Z, 9h38m) and FILL-BALL (06:54:04Z, 9h) reach the claimed range. The core claim stands: zero hermes_burn rows after the fixes, so no guard has seen a live paid fire.

### F3 seed_seal never sealed anything: CONFIRMED with one literal correction

- mag/seed_seal.py = 295 lines, tests/test_seed_seal.py = 262 lines (wc -l; both in 3c83da5b0's stat).
- Whole-tree `find . -name "*.seal"`: .seal files DO exist, but exclusively under agents/pytest-tmp-*/ test sandboxes (e.g. agents/pytest-tmp-10040/test_forge_drill_seed_body_tam0/arc_seed_sess_testdril_20260101_0000.seal). The lens's claim "zero .seal sidecars on the whole tree" is literally false; the true statement is zero outside pytest sandboxes, i.e. zero production seals. The lens's own evidence (`ls corpus/*.seal mag/*.seal`) checked two directories, not the tree.
- sha256(seed/engines/key_law.py) = fd2a0b2742933540bbd6a6c1d2036c3321d95a25a06e8f3504bb1ebb93dfaedd, equal to the seed/MANIFEST.sha256 row; `git status --porcelain seed/` empty.
- The hand-heal is proven by history: seed/MANIFEST.sha256 last changed in a331069c7 (2026-09-30T08:09:47-04:00) while seed/engines/key_law.py last changed in d15bc960d (2026-09-27), and seed_seal.py only landed 2026-10-02. w4-20.md:17 records the pre-heal contradiction (actual fd2a0b27 vs manifest 71f95e2d inside one clean commit). The instrument did not heal it; a hand manifest rebuild did.

### F4 OWED list "4-live / 2-paid": WEAKENED (miscount + phantom path; substance survives)

The prior synthesis's OWED list is SYNTHESIS.md:124-160 (watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md). Against current bytes:

Live (5, not 4):
- kpi.jsonl unrotated: logs/kpi.jsonl = 753,304,436 bytes at 2026-10-02T11:11:51Z (os.stat), +5.08MB past the synthesis's 748,222,017 (SYNTHESIS.md:90) and still growing past the lens's own 752,885,507. Writer mag/records.py:138 (write_kpi) untouched (`git status --porcelain mag/records.py` empty).
- invisible_runner audit jsonl: absent; `find` shows only scripts/invisible_runner.vbs itself.
- T1W2 19:17-19:18Z double-fire cause: still unattributed (SYNTHESIS.md:126). The lens DROPPED this live item from its count while admitting it in blind_spots.
- NIGHT_CLOSE_20261002.md erratum: unpaid. `grep -in "erratum" watch/inbox/NIGHT_CLOSE_20261002.md` = zero hits; mtime 05:14:18Z (unchanged since filing). The owed erratum is SYNTHESIS.md:145 (re-scope the "never existed" line). The :40 and :55 cites byte-check exactly.
- commit-queue law: ticketed nowhere. Zero rows across queue/todo.md, memory/law/registry.json, AND the real TICKET_LEDGER (below).

Paid (1, not 2): the engine topic defect. .zcode/workflows/ractor-engine.dwf.ts carries `topic` as `required: true` (args schema ~:29, Args comment ~:45); this run's asks carried the topic verbatim; REGISTRY.jsonl's latest ractor-engine gate row is PASS at 2026-10-02T10:38:16Z. The census refresh is a B2-246 patrol response (watch/inbox/census_refresh_20261002.md, mtime 10:10:13Z, claim 4,147/496 at 10:08Z), not an OWED row; counting it as a paid OWED is how the lens reached "2-paid".

Path defect: TICKET_LEDGER.md does NOT exist at memory/runs/hermes_burn/TICKET_LEDGER.md (grep: No such file or directory; the ask's evidence list carries the same wrong path). The real file is watch/inbox/hermes_burn/TICKET_LEDGER.md (find), and it also has zero commit-queue rows. The lens's "full read of TICKET_LEDGER.md" cites a nonexistent path; the conclusion happens to hold against the real one.

## What the lens missed (additions)

1. The money organ has no twin guard. `grep -in "pidfile|flock|singleton" tools/hermes_burn.py tools/code_swarm.py tools/rib_swarm.py` = zero hits. Guards exist only on scripts/descent_driver.sh:10-23 (the launcher, landed e3c7d341c) and mag/lane_runner.py:52,1089-1098 (the lane daemon). The proven twin disease (descent twins, 13 doubled keys, $2.25 vs $1.09 per e3c7d341c; T1W2 near-simultaneous pair 19:17-19:18Z per SYNTHESIS.md:72) can recur directly on the $37.76/window driver: LANDED-BEATS-FORCE checks the output file before firing, and two concurrent drivers both pass preflight before either lands. Move: port the descent guard shape (write-pid, stale-reclaim, trap cleanup) into tools/hermes_burn.py, ~20 min.
2. MOVE 2 is byte-true on live state, which the lens never checked. PowerShell Get-ScheduledTask: MagCensusPatrolDaily, MagFtsIndexDaily, MagImproveDaily all exec `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <abs path>.ps1`, MagLeaveProtocolDaily execs the venv python on tools/leave_dispatcher.py. No action references invisible_runner.vbs. Observation, not verdict: the three PS tasks show LastTaskResult 1 (census's is the expected COLLECT-DRIFT exit that triggered the 10-02 refresh; fts/improve unexamined this sitting, OWED a log look).
3. ListWorkflowRuns is a capability wall in BOTH sessions, not just the lens's. This pass called it and got `workflow_introspection_unavailable: this session cannot read workflow runs`. The 223.4M-token free-lane figure and the per-run counts (63.1M / 37.6M / 54.0M / 68.7M) remain ask-text-only; the swarm cannot audit its own token spend from inside. Blind-spot 1 of the lens is therefore confirmed as structural.
4. Blind-spot 5 adjustment: a third and fourth usage ledger exist (logs/usage.jsonl, memory/runs/grok_free/usage.jsonl) but neither prices this window: grok_free spans 2026-08-09 to 2026-09-21 (540 rows, cost_est_usd), logs/usage.jsonl is a lane-action log since 2026-07-20 (not a cost meter). The z.ai and grok-4.7 window spend is genuinely unmetered; Salon-mine-20deep stays unpriceable from here.
5. Dogfood-Q5 quick status (built vs fired), receipts on disk: code_swarm (watch/inbox/model_garden/SWARM_1.md), rib_swarm (RIB_SWARM_1.md), water computer (FIELD_EXPERIMENT_RESULT.md) fired during the night; citation_lint fired on the prior synthesis's own output (SYNTHESIS.md:174); percolator --candidates landed live data (memory/percolator/candidates.jsonl, 16 rows, committed 3c83da5b0); seed_seal is the lone built-never-fired-in-production instrument (F3); ractor-engine is dogfooding itself right now (this pass is its hostile stage).

## Command ledger (what this pass ran)

- git rev-parse HEAD; git log --oneline -3; git log -1 --format=%cI on HEAD, 3c83da5b0, 0c9d72a06, 5d2263f10, 962e41054, 1a1efc67f, f4cfcdf9b
- git show --stat 3c83da5b0; git show HEAD:githooks/pre-push | findstr; git diff --stat -- githooks/pre-push; git log --oneline -3 -- githooks/pre-push; git status --porcelain (targeted)
- python over memory/runs/hermes_burn/usage.jsonl and memory/runs/model_garden/usage.jsonl (rows, sums, ts bounds, dup census, ok:False)
- git show 1a1efc67f:tools/hermes_burn.py | grep -c "LANDED BEATS FORCE" (0); same at 5d2263f10 (1)
- ./.venv/Scripts/python.exe -m pytest tests/test_carrier_patch_t1w1.py -q -p no:cacheprovider (10 passed in 0.66s); --collect-only -q (10 named)
- find . -name "*.seal"; wc -l mag/seed_seal.py tests/test_seed_seal.py; sha256 vs seed/MANIFEST.sha256; git log -1 -- seed/MANIFEST.sha256 seed/engines/key_law.py
- os.stat on logs/kpi.jsonl, census_refresh_20261002.md, NIGHT_CLOSE_20261002.md; grep erratum/commit-queue/invisible across the three ledgers; find TICKET_LEDGER
- grep pidfile across scripts/ tools/ mag/; PowerShell Get-ScheduledTask x4; ListWorkflowRuns (capability error, quoted above)
- grok_free and logs usage.jsonl bounds check

## OWED from this pass (never asserted)

- The 223.4M / per-run token figures: operator-side run history only.
- Nous balance: $47.54 is still commit-0c9d72a06-cited; no API query this sitting.
- WMI / USN journal: not re-run; the 06:11:22Z twin reading stands as of its moment.
- fts/improve patrol LastTaskResult 1 log look.
- Garden per-instrument dollar re-sums ($0.22 / $0.075 / $0.0017 / $0.69): receipts exist, internals not re-added this sitting.

Filed by break-economics. No em-dash bytes (grep-verified while writing).
