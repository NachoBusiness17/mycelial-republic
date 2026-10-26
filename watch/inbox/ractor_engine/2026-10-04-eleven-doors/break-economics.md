# BREAK-ECONOMICS: hostile second pass on the economics lens (2026-10-04)

Run: dwfrun-3b5af1ac (the ractor-engine pass the ARENA_BENCH_TRIPWIRE receipt itself names at watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:4-5). Seat: break-economics. Instruments: read-only byte reads plus the greps named inline; no builds, no tests, no bench executions were run by this seat, so every "landed/live" claim rides git metadata and receipt bytes, not a run of mine.

## 0. The frame-breaker: the tree moved under the lens

The lens ranked its build order against a tree that no longer exists. Two doors of the 13-row primer table (watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:233-249) landed TODAY before this pass read the tree:

- door 1, INDEPENDENT-COP: commit bb0f34586 at 2026-10-04 12:23:16 -0400 (git show -s, this session), receipt watch/inbox/GWAP_INDEPENDENT_COP_20261004.md (known to the lens).
- door 2, ARENA-BENCH CI TRIPWIRE: commit 00cb15c77 at 2026-10-04 12:39:31 -0400 (git show -s, this session), stat: mag/arena_bench.py +9, tests/test_arena_bench.py +94 (new file), watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md +52. The bench is demonstrably minting again: 28 receipt_run_fixture-honest-ghost files timestamped 2026-10-04T16:33Z through 16:59Z+ in memory/arena_bench/ (ls + grep -c, 33 total matching files of which 5 are 2026-09-05).

Consequences the lens could not see: the ask's "11 remaining build doors" is now 10 remaining (13 primer rows minus doors 1 and 2), or 11 with EG-20 pass@K restored; the lens's slot-1 move ("Land arena-bench tripwire") is already executed; and its evidence clause "zero tests referencing the file" is false on the current tree (git grep -l arena_bench -- tests/ returns tests/test_arena_bench.py, this session).

## 1. Verdicts on the lens's five findings

### 1.1 EG-20 pass@K silently dropped from both successor sequences: CONFIRMED

Every byte verified. ESTATE_GAP_DIG row 9 is real and carries the only measured effort plus a success meter: watch/inbox/ESTATE_GAP_DIG_20261004.md:79 ("Coverage column (pass@K, large K) beside win rate in arena/gwap | 2h | column present; predicts the mesh vs frontier routing on one batch"), gap row EG-20 at :63. Primer rank 3 with "2h (measured at spec)" at watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:237. The door-1 receipt's next-doors line names only arena-bench/clippy/night-cycle at watch/inbox/GWAP_INDEPENDENT_COP_20261004.md:82-83. The ask's own 11-door list omits pass@K (counted from the ask text). My re-census, untruncated: git grep -n -i -E "pass@k|pass_at_k" -- tools/ mag/ tests/ exits 1, zero hits on the tracked tree. The lens's falsifier (a sibling landing a coverage column in tools/arena_gwap.py) did NOT fire: git log --oneline -3 -- tools/arena_gwap.py shows bb0f34586, a5a2aa8be, d349ce7d2, none a coverage column.

Sharpened past the lens: the drop is now three-deep (the ask, the door-1 receipt, and this run's own tasking), while a third receipt explicitly re-carries the item: watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:46-47 "The bench is live again for the pass@K diagnostic (EG-20, the dig's only measured-effort item rides this instrument)". And the item's blocker is cured, so the 2h build is cheaper now than at spec time. The lens's move stands and improves: restore EG-20 to the next build slot; the arena-bench leg it sat behind is done.

### 1.2 Decay-family shared-schema gate would re-mint held vocabulary: CONFIRMED (sharpened)

All cites byte-true. mag/republic.py:114 "superseded_by: int | None = None   # set once, by supersede(); never edited"; house chain law at mag/republic.py:14-16 ("a retracted letter is superseded_by another, never deleted or edited, house chain law, enforced at save time"); supersession guards (re-point refused, target-must-exist) at mag/republic.py:209-218. tools/gps_mcp/ledger.py:433-443 carries the 1/n dilution and the momentum-rising fail-absorbing floor with the literal floor_applied = True at :442 and the named-honesty comment at :437-440. mag/mycelium.py:273-274 stamps e["decayed"] = True / e["decayed_at"] = _now() inside decay() (:265-277). The primer's gate text is at watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:216-222 and :240 ("decay-family shared schema (valid_at/invalid_at/superseded_by) defined once, first").

Sharpening the lens overshot on: the ledger floor is metabolism prior art, NOT schema prior art. The GPS README's own limitations block concedes routing "does not decay stale measurements" (quoted in the primer at :186 from tools/gps_mcp/README.md:215-221), so citing floor_applied as vocabulary-already-held for the decay family overstates; it is a steal for the METABOLISM door (pheromone), not for the valid_at/invalid_at/superseded_by schema. The real schema steal is republic.py's set-once superseded_by with mutation guards, and the primer's two-graphs ruling (:33) already orders one vocabulary defined once but never names mag/republic.py as the source. The lens's 30-minute import-read move (read republic.py supersede() against ledger row shape before the family starts; import, do not define) is confirmed and is the correct family opener. The lens's own falsifier (letter semantics may not port to aggregate-stat rows) stays open and is exactly what the 30-minute read answers.

### 1.3 Demote night-cycle checkpoint legs below the monoculture proxy: KILLED (by the lens's own falsifier)

The evidence bytes are all accurate: watch/inbox/NIGHT_SHIFT_20261004_CLOSE.md:35 is the lane-7 row (9718e812d, "honest rc=2 skip + atomic state saves"); commit 9718e812d exists with the full cure narrative (git show -s this session: guarded key read, rc=2 MARCH SKIP, stderr tail kept, trail-before-persist, atomic tmp+os.replace, 7 tests, cage proof 08:50Z); mag/lane_runner.py:932-938 carries the trail-before-persist comment with the Errno-22 root cause and the 2026-10-03 5x-CYCLE_FAIL history in-code; primer rank 4 at :238.

But the demote's own stated condition, "build only if a new CYCLE_FAIL storm bank appears" (finding 3's falsifier), has FIRED, and I ran it: grep over queue/lanes/research/trail.jsonl counts 134 CYCLE_FAIL rows dated 2026-10-04 versus 27 dated 2026-10-03 (this session); the sampled tail rows (12:23:41Z through 12:31:37Z, five rows at ~2-minute cadence, all "OSError: [Errno 22] Invalid argument: '/app/queue/lanes/research/runner_state.json'") are 3.5 hours POST-cure-commit (9718e812d landed 04:55:21 -0400 = 08:55:21Z). The storm class is not a residual; it is the dominant day (134 today vs 27 yesterday), and it is not confined to the night composite (research-cage is a day lane). By the lens's own rule the rank is restored.

Spec correction the lens missed (addition B below): the door as specced writes done flags "through the existing _save_state" (primer :171, :220), which is the exact write path that fails during storms. The bytes of the storm itself prove the right substrate: trail appends SUCCEED during the storm window (the CYCLE_FAIL rows are in the trail) while the runner_state.json write FAILS (the rows' own detail). Checkpoints must ride the trail, not _save_state.

### 1.4 Three doors are cargo as specced (consume-the-ledger, weld, three-signal): WEAKENED

Evidence bytes confirmed: tools/gps_mcp/router.py:5-11 carries the routing rules (measured pass-rate threshold 0.85, cost, calibrated confidence as cascade trigger); MOMENTUM_RANK with the LM7 tiebreak comment at tools/gps_mcp/router.py:44-50; door gates at watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:243, :245, :247. The FSRS-adjacent and recall greps re-ran clean (below).

But the three cargo verdicts overreach in different degrees:

- consume-the-ledger: the router refutes the primer HEADING's universal ("nothing consumes the ledger at decision time", primer :192), not the door's actual target. The primer body scopes it honestly at :194 ("Central stationary estimates exist; decentralized actors do not read them"), and the target absence is real and byte-checkable: grep -n "g_best\|p_best" mag/flock_field.py exits 1, zero hits (this session), confirming primer :194's cite that the steer force has no social terms. The door was also already parked last in the primer's own table behind a design gate (:247), so "cut from the build sequence" cuts nothing the primer had scheduled; the honest disposition is "premise sentence refuted, target real, keep gated last".
- weld: the door HAS a meter. Its own spec banks the learner's answers as arena_gwap agreement payloads (primer :124 "arena_gwap banks the agreement score"), which is execution-verified measurement, the estate's strongest instrument class per primer :106. What the door lacks is a learning-GAIN control (pre/post against the 0.37-0.79 band, the tutor-claim law at primer :84), and by that unmeasurability standard every door in the dig fails equally, including the lens's own beloved tripwires. The honest fix is to add the control to the spec, not to cut the dig's named differentiator (primer :124 "the only door that closes teach, verify, and adapt on the same content").
- three-signal: "a 50-question harness that does not exist" is refuted by the estate's own ledger: tools/queue_close.py:127 (Q-031) records a held-out 50-question eval EXECUTED 2026-09-28 ("accuracy@1 0.48, accuracy@10 0.76, results JSON with sha-pinned catalog"). It measured catalog-tag retrieval, not recall@5 over answer files, so adaptation is owed, but the question bank, held-out discipline, and results-JSON shape exist as steal; the eval-build cost hidden inside the 1-2 day estimate is smaller than the lens claims.

The lens's falsifier paragraph anticipated all three of these outs ("A named consumer for the weld door, a measured harm case for the flock g_best term, or an existing recall@5 harness would flip each individual cargo verdict"); I did not find a named weld learner or a measured flock harm case, so those two legs of the falsifier stay unfired, but the harness leg partially fired via Q-031. Verdict: the cut-three move is not earned; reprice three-signal down (harness precedent), keep weld gated on a spec-added control, keep consume-the-ledger gated last.

### 1.5 The two cheapest doors are the highest-EV-per-hour (arena-bench tripwire + clippy-as-prober): WEAKENED

Evidence bytes confirmed: main.py:1253-1261 is the clippy subparser (help text "It looks like you're trying to work on Mag. Would you like a reminder?" at :1255); .agents/skills/fireball-cycle/SKILL.md:9 carries "a skill is a one-time conversion that becomes free recall" verbatim; my re-census git grep -n -i -E "fsrs|spaced.?repetition|retrieval.?state" -- mag/ tools/ tests/ returns exactly one hit, "Binary file tools/godot/Godot_v4.3-stable_win64.exe matches" (tracked tree, this session), byte-identical to the lens's claim. That zero is also CONVERGENT: the primer's own P3 lane rg over mag/tools/tests for spaced/testing-effect/retrieval-practice returned zero (primer :100), two instruments, one verdict; flagging it per the duplication law.

But the finding's top move is consumed by events: the arena-bench tripwire landed at 00cb15c77 (12:39:31 -0400) with a 4-test tripwire, and the bench minted 28 receipts by 16:59Z (section 0). The sub-claim "zero tests referencing the file" is false on the tree this pass read (git grep -l arena_bench -- tests/ returns tests/test_arena_bench.py), and the ValueError's line moved to mag/arena_bench.py:109 post-patch (the lens said :110, the primer :102 pre-patch; the raise is real, the docstring's refuses-to-fabricate contract is at :99-103). The usage-line logic itself was VALIDATED, not refuted: the door was so obviously top-EV that a sibling seat took it within hours. The live remainder of the finding is clippy-as-prober alone, which stands confirmed as the cheapest unlanded door with a certain usage surface (session-start surface per primer :100; AGENTS.md standing clippy reminders).

## 2. What the lens missed (additions)

A. **Door 2 landed mid-flight; the sequence premise shifted.** git show --stat 00cb15c77 (3 files, +154/-1) plus 28 fresh bench receipts. Any reviser order built on the lens's ranking double-builds slot 1. Falsifier: git log or the receipts disappearing. Move: 5 minutes, re-base the order on 10 remaining doors (11 with EG-20 restored).

B. **The storm falsifier fired, with a substrate correction.** 134 CYCLE_FAIL rows on 2026-10-04 vs 27 on 2026-10-03 in queue/lanes/research/trail.jsonl (grep census this session); tail rows post-cure (12:23-12:31Z vs cure commit 08:55:21Z). Trail appends survive the storm while runner_state.json writes fail, so the checkpoint-legs door as specced (flags through _save_state, primer :171) aims at the substrate that dies; re-spec to trail-borne flags. Falsifier: a storm window in which trail appends also fail would void the substrate claim. Move: 10-minute spec amendment, then the door stays rank 3-4, not demoted.

C. **Q-031's executed 50-question held-out eval (tools/queue_close.py:127) reprices the three-signal falsifier.** Falsifier: reading the burn_reset 2026-09-28 receipt and finding the eval was not question-shaped after all. Move: 20 minutes to confirm reuse shape before any cut/build call on three-signal.

D. **The weld door's meter already exists (agreement_score), so its honest gate is a learning-gain control, not a cut.** Primer :124 (spec banks agreement) vs :84 (tutor-claim law). Falsifier: a reading of the weld spec showing it does NOT bank gwap payloads. Move: one spec line (pre/post control vs the 0.37-0.79 band) before build.

E. **Convergence flags the lens left unflagged.** The FSRS/retrieval-state zero is two-instrument convergent (primer :100 lane rg + this pass's git grep); the EG-20 measured-effort uniqueness is attested twice (primer :237 and the tripwire receipt :46-47). Per the duplication law these outrank the novel claims around them.

F. **The 24-wide receipt's own arena-bench line-number (:102) and the lens's (:110) are both stale on the post-patch tree (:109).** Trivial, but it is the citation-drift class the estate already laws (citation_lint blocks drifted line cites in changed prose); lens prose is outside that gate's scope, so hostile passes are the only catcher. Falsifier: none needed; byte-checked this session.

## 3. Honest build order by EV-per-hour, post-pass (10 doors remaining, 11 with EG-20)

1. **EG-20 pass@K coverage column**, 2h MEASURED (ESTATE_GAP_DIG:79): the only measured-effort item, dropped three-deep, blocker cured, bench live, column lands in tools/arena_gwap.py per the gap row's own self-steal source. Highest EV/h standing.
2. **clippy-as-prober**, 2-4h est: cheapest unlanded door, certain usage surface, zero existing code by two convergent censuses, banks the FSRS probe stream.
3. **checkpoint legs re-specced to trail substrate**, 2-4h est: rank RESTORED (storm live, 134 rows today), spec corrected per addition B.
4. **monoculture agreement proxy**, 2-4h est: unchanged from the primer, this dig remains its first test case.
5. **decay family**, opened by the lens's confirmed 30-minute republic.py supersede() import read, then pheromone metabolism (steal the ledger floor's fail-absorb shape), then mycelium-v2 reusing the imported vocabulary.
Gated, in order: MCP-lattice shim (reconciliation pass first, X_INTEL_AIENG_SCRATCH:92-94); weld (add the learning-gain control, then it is buildable); three-signal (reprice on the Q-031 harness precedent; embedding lane stays a new dependency class); build-once calibrator (no Gero-4B download/eval cost model exists anywhere, lens blind spot 2, unresolved this pass); consume-the-ledger (premise sentence refuted, target absence real, flock semantics change, keep last).

## 4. Not run / limits

- This seat ran no builds, tests, or bench executions; all landed/live claims ride git metadata (git show -s --format for each named commit), receipt bytes, and file listings.
- The 134-vs-27 CYCLE_FAIL census covers queue/lanes/research/trail.jsonl only (builder trail holds 370 lifetime rows, not date-split here; day_work zero); whether the research-cage daemon runs post-cure code (a process-restart question) is not determinable from bytes, but the rows prove the state-write class live after the cure commit either way.
- All lens effort figures remain reviser estimates except EG-20 (measured at spec); nothing new was measured this pass.
- The lens's finding-5 move text arrived truncated mid-sentence in my tasking ("Land arena-bench tripwire, EG-20 pass@K, and c..."); verdicts cover the verifiable prefix.

Writer: break-economics (hostile second pass), dwfrun-3b5af1ac. fetched: 2026-10-04.
