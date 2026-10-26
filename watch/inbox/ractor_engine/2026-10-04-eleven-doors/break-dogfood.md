# BREAK-DOGFOOD: hostile second pass on the eleven-doors lens (2026-10-04)

Writer: break-dogfood seat (hostile pass, workflow dwfrun lane). Target: the lens report on the 24-wide dig's 11 remaining build doors and their reviser-ordered sequence. Tree at pass: HEAD 00cb15c77 (door 2 landed mid-lens), last mag/lane_runner.py commit d349ce7d2 (GO WAVE 20261004, 05:50:05 -0400). Every check below was executed this session with the command named; nothing is carried from the lens's bytes without a rerun. Instrument note: commands ran via the Bash tool (GNU coreutils on win32); the pytest runs used the repo venv `.venv\Scripts\python.exe`.

## Verdicts

### F1 (door 2 arena-bench: landed by a sibling while the lens ran; defect and cure independently reproduced): CONFIRMED

Every byte-check passed, and the one check the lens never ran (the tripwire suite) is now green in this seat:

- Pre-landing path: `git show 00cb15c77^:mag/arena_bench.py` line 66 reads `ARRAKIS_PATH = ROOT / "dashboard" / "static" / "arrakis.html"` (static root). Post-landing mag/arena_bench.py:66-73 carries the cure comment block and repoints at `dashboard/static/games/arrakis.html` at :73. Both read this session.
- Stub vs canonical: `ls -la` gives dashboard/static/arrakis.html = 459 bytes (mtime Sep 22 02:57) and dashboard/static/games/arrakis.html = 17,501 bytes (mtime Sep 22 09:34). Python count this session: stub has 0 lowercase `blind` tokens and does contain `http-equiv` (meta refresh). All three lens figures reproduced.
- Ground truth: my run of `load_ground_truth()` (venv python, this session) printed gate_count 3, crown_number 50, ghost_name "ZCode", dungeon_room_count 6. Matches the lens's "PARSE OK gates=3, crown 50, ghost ZCode".
- Commit: 00cb15c773df7146636f78faabfde444f324e2c4 at 2026-10-04 12:39:31 -0400, 3 files (+9 mag/arena_bench.py, +94 tests/test_arena_bench.py, +52 watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md, which exists on disk).
- Test cites: tests/test_arena_bench.py:52 is the `gt = load_ground_truth()` call and :58 is `def test_surfaces_are_not_redirect_stubs():`; the stub detector asserts no meta-refresh and >4000 bytes at :66-68. Full file read this session (the lens only grepped it).
- Pre-landing test absence: `git grep -n arena_bench 00cb15c77^ -- tests/` returned zero output.
- The falsifier's green-run condition: `.venv\Scripts\python.exe -m pytest tests/test_arena_bench.py -q` -> `4 passed in 2.75s` (this seat, first execution of the suite in either pass). The synthetic-stub-shape half of the falsifier (would the detector miss a new stub shape?) was not exercised with a crafted stub: not run, noted as open but low-stakes given the two independent assertions (meta-refresh + min-size + strict parse + blind-gate presence).

### F2 (night-cycle checkpoint legs: harm already cured; census bullet promised a phantom test name): WEAKENED, split verdict

Confirmed half, the door redundancy:
- mag/lane_runner.py:124-149 read this session: the Errno-22 cure comment names the 5x CYCLE_FAIL 2026-10-03 class and the ~100s re-run loop; atomic tmp + `os.replace` at :140-143. March honest rc=2 comment and tail-keep at :925-931. Trail-before-persist reorder at :932-938. All six lens cites byte-true.
- Last commit touching mag/lane_runner.py: d349ce7d2, 2026-10-04 05:50:05 -0400, subject "GO WAVE 20261004" (the lens's "same morning's GO WAVE" framing is exact).
- The lens's falsifier, settled by log bytes this session: logs/lane_scheduler.log shows the 2026-10-03 storm (four `[Errno 22]` loop-exc rows 23:02:01Z to 23:08:05Z, success 23:10:56Z) and then post-cure 2026-10-04T08:50:08Z `lane=night result=monitor rc=0; march rc=2 :: MARCH SKIP rc=2: no key ...` with no re-run loops after it; the log tail (16:46-17:04Z) shows normal cycles. Absence of the residual pattern holds, so by the falsifier's own terms the door's harm is dead. The lens's move (re-scope to a 1h idempotency test or drop; do not spend 2-4h) survives.

Killed half, the "phantom name":
- tests/test_night_march_cure_20261004.py EXISTS: tracked (`git ls-files`), added in commit 9718e812d at 2026-10-04 04:55:21 -0400, ancestor of HEAD, 130 lines, 7 tests per the commit message, companion receipt watch/inbox/night_shift_20261004/night_march_cured.md (+123 lines, same commit). That commit predates every moment the lens read the tree (it saw d349ce7d2 at 05:50 as an earlier mover), so the file was on disk during the lens's ls; the lens queried the exact unsuffixed name `test_night_march_cure.py` only and missed the suffixed sibling one `ls tests/ | grep night_march` would have returned.
- What remains true: AGENTS.md:29's census bullet names the unsuffixed `test_night_march_cure` inside the night-shift attribution clause. That is a suffix-drifted hand-copied name (the bullet's own law: never trust a hand-written count), not a phantom file. The lens's "carries a phantom name" clause is killed; the defect is real but one order smaller: a naming erratum in AGENTS.md, not a missing test.

### F3 (decay family should steal republic.py's supersession, not mint a second dialect): CONFIRMED, strengthened

- mag/republic.py:14-16 (house chain law, "superseded_by another, never deleted or edited"), :57-60 (FROZEN tuple, "superseded_by and trail are the only two mutable fields"), :114 (`superseded_by: int | None = None   # set once, by supersede(); never edited`, verbatim), :195-218 (AppendOnlyViolation on delete, frozen-field edit, trail edit, re-pointed supersession :209-213, dangling supersession :214-218). All read this session.
- The lens's admitted blind spot (supersede() itself never read) is cured and the claim gets stronger: `def supersede(book, letter_id, by, reason)` EXISTS at mag/republic.py:396-416, mints a RETRACTION letter, sets `old.superseded_by = ret.id` at :414, appends trail events (:410, :415-416), refuses double-supersession (:403-405), and reply-to-superseded and forward-of-superseded are rejected downstream (:341-344, :376-379). The file even self-probes the law (F1 probe :624-655, F2 probe :687-697).
- mag/mycelium.py:183 carries the violated-law comment verbatim ("jsonl is append-only; replace by rewriting the file"); contradict() at :188-198 bumps counters with no lineage; _rewrite_edges full-file open("w") at :201-205. Confirmed.
- PRIMER_ADJACENT_24WIDE_20261004.md:33 carries the law-51 two-dialects ruling exactly as the lens cited it.
- Falsifier sharpened by this pass: republic supersession binds integer letter ids inside one JSON book dump; mycelium edges are (src, dst) string-keyed jsonl rows with no stable per-edge id, so an adapter must first mint edge ids. The steal is a law steal plus a keying adapter, not a drop-in; the lens's 1h spec-sketch move stands with the mapping question now concrete.

### F4 (build-once calibrator splits into an owned 2h wire and gated Gero-4B cargo): CONFIRMED, with the falsifier settled adversely to the 2h figure

- tools/oracle_calibration.py:118-175 is bin_reliability computing binned ECE/MCE/Brier (docstring names all three at :123-124; brier at :144, :152, :174); :376 is `check("brier_perfect_calibrated", ...)` verbatim. Confirmed.
- Scoped census rerun, untruncated: `git grep -ln oracle_calibration -- mag tools tests scripts configs` returns exactly configs/violation_baseline.json and tools/oracle_calibration.py. The lens's zero-code-consumer claim holds in its named scope. The full tracked tree (`git grep -ln oracle_calibration`) adds only data and receipt mentions (catalog/catalog.jsonl, watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json, the PRIMER receipt itself, audit files), which are mentions, not consumers.
- mag/mixture_of_agents.py:48 (AgentVote.confidence) and :73-74 (MoAResult confidence, convergence). Confirmed.
- Commit 993a5977b (2026-10-04 08:36:36 -0400) exists and its message carries "the v4 door is a proper-scoring layer" over agreement_score as raw hit-fraction. The PRIMER receipt's HEAD-993a5977b cite is real.
- Gero-4B: watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-46 holds the card bytes (huggingface.co/vixhal-baraiya/Gero-4B, Apache 2.0, 50 downloads, "No published evals on the card" at :45). External corroboration this session: a web search returns the vixhal-baraiya/Gero-4B Hugging Face page with the proper-scoring reward text matching the card bytes. Existence and mechanism now two-sourced; the no-published-evals absence stays scoped to the card read (named instrument: the receipt's fetch).
- The lens's open falsifier (is there a joinable outcome stream for MoA confidences?) is settled this session, against the 2h: MoAResult rows persist only via `_log_result` at mag/mixture_of_agents.py:352-360 into memory/moa/moa_log.jsonl, and `ls memory/moa/` returns "No such file or directory": the log has ZERO rows ever (the sole reader is mag/data_refinery.py:590). There is nothing to join; per the falsifier's own terms the wire needs a data-generating leg first and the 2h doubles. The finding's split-and-own claim survives; its sizing does not.

## What the lens missed (additions)

1. The phantom is a suffix drift, and the test file predates the lens's read. tests/test_night_march_cure_20261004.py: tracked, commit 9718e812d (2026-10-04 04:55:21 -0400), ancestor of HEAD, 130 lines covering both night-march defects (march rc=2 skip at :46-71; trail-before-persist and atomic save at :82-130). AGENTS.md:29 carries the unsuffixed hand-copied name. Falsifier: `ls tests/ | grep night_march` returning the file. Move: 5-minute AGENTS.md erratum fixing the name inside the attribution clause only (the B2-249 carrier grammar, the parenthesized "N tests collected / M files (YYYY-MM-DD census" clause, must not be touched).
2. The calibrator wire's data side is empty. memory/moa/ does not exist; writer mag/mixture_of_agents.py:352-360 fires only on real (non-dry-run) moa_query calls; reader mag/data_refinery.py:590. Either fire one real MoA run to open the log, or point the calibration join at the gwap verdict ledger (memory/runs/gwap/arena-capability.jsonl, 613+ rows per the door-1 receipt), which actually has outcomes. Falsifier: existence of memory/moa/moa_log.jsonl with rows. Move: 10 minutes, gate note in the door spec.
3. CONVERGENT prior art on the dead scorer (duplication is emphasis): the 2026-09-26 dead-instruments audit already rows `oracle_calibration.py | 0 | 16 | NO | 2026-09-19 | ORPHAN` (watch/inbox/audit_20260926/LANE2_DOGFOOD_TOOLS.md:292), and THE50_W6_T30_POLICY_EVAL.md:249 and :429 already codify the honest-absence contract ("calibration numbers ... absent a ledger they are omitted, never invented"). Two prior runs banked the orphan fact the lens re-derived; the door spec should cite both rather than re-derive a third time. Falsifier: a functional consumer appearing in mag/tools/tests/scripts/configs (the census above says none).
4. The two receipts contradict each other on build order, and the lens inherited the wrong one. GWAP_INDEPENDENT_COP_20261004.md:82-83 orders the next doors "arena-bench CI tripwire (1-2h), clippy-as-prober (2-4h), night-cycle checkpoint legs (2-4h)", but the PRIMER's own ranked table (PRIMER_ADJACENT_24WIDE_20261004.md:236-242) ranks EG-20 pass@K at 3 (2h, the only measured figure, specced at watch/inbox/ESTATE_GAP_DIG_20261004.md EG-20 row and table row 9 "Coverage column (pass@K, large K) beside win rate in arena/gwap | 2h"), night-cycle at 4, monoculture proxy at 5, pheromone at 6, and clippy-as-prober at 7 behind the decay-family schema. With door 2 landed (its commit message says "the pass@K diagnostic rides it") and night-cycle's harm dead per F2's settled falsifier, the honest next build by EV-per-hour is EG-20 pass@K (2h measured, specced, newly unblocked), not clippy-as-prober. Falsifier: reading the two orderings side by side (done, cites above). Move: 0 minutes, sequence correction in the eleven-doors order; EG-20 next.
5. Door-state summary after this pass (the ask's sequence question): door 1 LANDED (bb0f34586, receipt read this session); door 2 LANDED (00cb15c77, tripwire 4 passed this session); night-cycle harm DEAD per falsifier (residual: 1h idempotency test or drop); EG-20 pass@K next by EV; clippy-as-prober stays behind the decay-family schema per the PRIMER table; calibrator wire blocked on its empty data side (addition 2) with Gero-4B still gated; the receipt's five design-gated doors (three-signal, MCP-lattice, weld, calibrator, consume-the-ledger) remain gated, and with F4's empty-log fact the calibrator's wire half is cargo until data exists. Monoculture proxy (rank 5) was not in the lens's findings and was not examined beyond the receipt's bytes this pass: not run, open.

## Blind-spot spot-checks (the lens's own named gaps, closed where cheap)

- tools/gps_mcp/ledger.py:414-449 read this session: running-mean dilution at :433 (`new_rate = (old_rate * old_size + v) / new_size`), mom floor at :434-443 with the honest floor comment. The lens's :415-455 window reads true; the receipt's 1/n cite is byte-accurate.
- Consume-the-ledger 4-file scope: `grep -n -i "ledger|gps|capability|pass_rate"` over mag/flock_steal.py, mag/steal_steer.py, mag/swarm_control.py, mag/coordination.py returns a single hit, mag/flock_steal.py:18, a docstring mention of skill_ledger (a different organ). No GPS-ledger consumption in the lens's named scope; the claim was already honestly scoped and survives.
- The lens's F1/F2 session-moment caveats (tree moving under it) were real: 00cb15c77 landed 12:39:31 -0400 and 9718e812d landed 04:55:21 -0400; the working tree still carries untracked churn (memory/arena_bench receipts et al.).

## Instrument table (what this pass ran)

| Check | Command | Result |
|---|---|---|
| Tripwire suite | `.venv\Scripts\python.exe -m pytest tests/test_arena_bench.py -q` | 4 passed in 2.75s |
| Ground truth | venv python `-c "... load_ground_truth()"` | gate_count 3, crown_number 50, ghost_name ZCode |
| Stub counts | venv python byte count | 459 bytes, 0 blind tokens, meta-refresh present |
| Pre-landing path | `git show 00cb15c77^:mag/arena_bench.py` (sed 60-70) | line 66 static-root path |
| Pre-landing tests | `git grep -n arena_bench 00cb15c77^ -- tests/` | zero output |
| Night-march file | `git ls-files tests/`, `git log --all -- tests/test_night_march_cure_20261004.py` | tracked; 9718e812d 04:55:21 -0400, ancestor of HEAD |
| Re-run falsifier | `grep CYCLE_FAIL|night logs/lane_scheduler.log` | storm 10-03 23:02-23:08Z; post-cure 10-04 08:50:08Z honest rc=2 skip; no re-runs |
| Scorer census | `git grep -ln oracle_calibration -- mag tools tests scripts configs` | baseline + self only |
| MoA join | `git grep moa_log`, `ls memory/moa/` | writer :352-360, reader data_refinery:590, log absent (zero rows) |
| Gero-4B external | web search vixhal-baraiya Gero-4B | HF page exists, proper-scoring text matches card bytes |

## Honesty

Not run this pass: the synthetic-stub detector probe (F1 falsifier half), the monoculture-proxy door's bytes beyond the receipt, the consume-the-ledger claim beyond the lens's 4-file scope, and any Gero-4B download/eval. The lens's F5 (pheromone metabolism re-scope) arrived truncated in the handed-down report; its visible references (mom-floor window, steering-file scope) were checked as blind spots above, but no F5 verdict is claimed. External Gero-4B corroboration is one search snippet; the model card itself was not fetched.
