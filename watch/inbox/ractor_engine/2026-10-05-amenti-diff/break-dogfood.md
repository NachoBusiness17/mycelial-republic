# BREAK-DOGFOOD - the hostile pass on the dogfood lens (2026-10-05)

Seat: break-dogfood (ractor, same family as the lens it breaks; the monoculture critique below applies to this pass too). Scope: every byte-cite in the lens report re-checked against the tree this sitting; the lens's own declared blind spots closed where cheap (suites rerun, ledger censused, replay receipts opened). No subprocess spawned by my own code (harness tool calls only), so the win32 CREATE_NO_WINDOW law had no code surface here; commands were run via the session shell with `.venv/Scripts/python.exe`.

## 1. Verdicts on the lens's findings

### F1 (T3 coldest vertex, cheapest organ port) - CONFIRMED, denominator corrected

Byte-checks, all this sitting:
- mag/arena_bench.py:487 = `fixture_maru_sycophant` (read; the labeled synthetic CONFIRM-everything failure). :229 `parse_verdict`, :243 `score_transcript` (read). mag/guardrail_sentinel.py:53 = `anti_sycophancy ... default low` (read; module header :49 "all PING-ONLY, none PREVENT"). tools/behavior_cards_x.py:238 = LAW 25 "prefers disagreement to sycophancy" (read; a mapping card, not a measurement). RESEARCH_SUMMARY_arena_days_one_two_20261005.md section 1 carries the $0 proof cycles and cap law (read).
- Nuance the lens missed: both live paths hardcode `"turns": 1` (mag/arena_bench.py:403, :458) and flash_call is a stateless single-shot, so the multi-turn stage is real new code, but threading repetition turns into the prompt text is trivial; the ~60 min estimate stands.
- Denominator correction: "three organs of lore" undercounts. My census (`grep -ril sycophancy mag/ tools/ tests/`) finds six code organs: also mag/egregore_steal.py:64, mag/field_steal.py:63-65 (regex doctrine detector for EXTERNAL text), mag/shadow_work.py:54, mag/scale_salon.py:128, plus the fired trail memory/runs/guardrail_sentinel/trail.jsonl (31 rows, 2 anti_sycophancy: 2026-08-10 "Watcher tempted to flatter the operator" and 4 minutes later "sentinel self-test"). Both trail rows are prose pings, not measurements.
- The absence claim survives the wider net: zero drift-measurement instruments exist (instrument: the grep census above plus the trail read; scope: mag/, tools/, tests/, memory/runs/guardrail_sentinel/). T3 stays the coldest measured-nowhere target.

### F2 (T5 corpus real, falsifier must split) - WEAKENED, the error runs the other way

Byte-checks that reproduce exactly:
- `find memory/runs -path "*salon*" -type f | wc -l` = 713; `find memory/runs/salons -type f | wc -l` = 587 (rerun this sitting).
- mag/lane_salon.py:13 docstring "token overlap = the consensus"; :124 `_consensus` word-bag intersection; :190-191 typed `n_witnesses`/`n_up` + witnesses list with per-witness provider (read).
- My provider census over memory/runs/lane_salon/*.json (33 files, 177 witness rows, all schema lane_salon.v1): groq 31, deepseek 29, cerebras 29, openrouter 28, nvidia 27, together 25, None 8. Byte-identical to the lens's numbers.

Where it breaks:
- The finding asserts "agreement density is typed". False in the opposite direction: NOTHING density-like is typed. `n_up`/`n_witnesses` is lane AVAILABILITY (which providers were up that minute), and the consensus is a string truncated to 400 chars (mag/lane_salon.py:132). The lens's own T5a move ("mine n_up/n_witnesses ... per fold") would test provider uptime, not coherence; any held-vs-falsified separation on that axis is confounded by infra and cannot operationalize her "enough coherence".
- "empty verdict fields" is not universal: 9 of 33 artifacts carry non-empty monitor verdicts (the monitor seat tri-states witnesses SUPPORTED/DISPUTED/UNPROVEN into the typed verdict field, mag/lane_salon.py:177-187). 24/33 empty.
- Byte detail: the fold's post_S5.md does not exist (memory/runs/salons/agent_mesh_triangulation/ holds S1,S2,S3,S4,S6,S7); "post_S1..S7" cites a gap.

Corrected split: T5 needs THREE pieces, not two. First type the agreement density itself (shared-token count per fold, or Jaccard over witness token sets, computed from the witnesses' answers already stored in each artifact), THEN T5a density census, THEN T5b label join (labels still prose-only; that part of the finding stands).

### F3 (T1 channel absent, A/B unscorable from ledgers) - CONFIRMED, move amended by a red gate

Byte-checks, all reproduced:
- memory/runs/mesh_v2/feeds/ holds exactly zcode.jsonl + zcode.key (ls this sitting): one writer, no operator feed.
- mag/state_snapshot.py:207-217 types exactly goal/outcome/tier/kind/lessons/source/session_id/state_hash (read); `grep -i -E "sleep|energy|focus" mag/state_snapshot.py` exits 1, zero hits.
- memory/runs/hermes_burn/usage.jsonl head rows are {ts,id,model,turn,prompt_tokens,completion_tokens,cost_usd,ok} (read; 3010 lines): `ok` is transport-level, no verdict-quality or wasted-ask column. The two-week A/B is unscorable today, as claimed.
- mag/mesh/feeds.py:23 `RATE_PER_MIN = 30`; :73-83 `_check_rate` (read).

Amendment: the move ("bank the typed operator feed via feeds.py append") rides an organ that is RED in suite right now (see A1): room_view sorts by (ts, writer, seq) at mag/mesh/feeds.py:144, and a second writer appending in the same clock tick reorders the room. An operator+zcode pair under burst is exactly that shape. Fix the tie-break first (~15 min: global monotonic seq or knot-stamped ts), then land the feed and the burn-ledger verdict column in the same sitting.

### F4 (loop's weak legs: prose feedback edge, monoculture adjudication) - CONFIRMED

- tools/freshness_check.py:41-46: CRITICAL_DOCS = BOOT_4_7.md + state/CURRENT.md + state/START_BRIEF.md + state/HANDOFF.md (read). DIFF_TARGETS.md is on no watch list and carries no freshness stamp (read in full this sitting; a title date only).
- MESH_V2_SELFSTEAL_LANDED_20261005.md line 29 carries the witness law ("N seats from M families = max M witnesses").
- The monoculture point compounds beyond what the lens said: this ractor dir holds 8 same-family passes filed the same hour (accuracy, communication, dogfood, economics, logic, moonshot-1, moonshot-2, operations, ls this sitting), and this break pass is the same family again. The second-family re-adjudication falsifier is the right one and remains unfired.

## 2. What the lens missed (additions)

### A1 (sharpest): the mesh v2 suite is 10/11 on today's tree, and the failing law is the merge law

Ran `.venv/Scripts/python.exe -m pytest tests/test_mesh_v2.py -q`: "1 failed, 10 passed", twice, deterministically. Failure: tests/test_mesh_v2.py:34 `test_two_writers_merged_room`, room order came back ['first', 'third', 'second']. In isolation the test passes. Cause: mag/mesh/feeds.py:144 sorts merged rows by (ts, writer, seq); two writers appending within one `time.time()` tick tie on ts and fall to writer-name order; the warm suite process makes the tie deterministic. The landing receipt's "All tests green" (MESH_V2_SELFSTEAL_LANDED_20261005.md) and the map's PRESENT "(built + tested)" cell (DIFF_TARGETS.md line 9) both need the asterisk. For contrast the other two suites DO reproduce: tools/gps_mcp 41 passed in 6.52s, tests/test_query_broker_20261005.py 10 passed in 3.40s (both rerun this sitting). This also feeds F3: the exact organ T1 would daily exercise is the one that is red.
- Falsifier: after the tie-break fix, 5 consecutive full-suite runs green plus a same-tick double-writer burst test (two appends with faked equal ts asserting stable order).
- Move: ~15 min fix in feeds.py (global monotonic sequence at append time), then re-run the suite.

### A2: T4 has zero consumers of the flag it would A/B, and no pin mechanism

tools/query_broker.py:247 derives `frozen` from a 30-day mtime gap on the catalog pair; gps_mcp/server.py and the mesh door attach the same header (per MESH_V2 receipt section 2). Grep for `"frozen"` consumers outside the three producers finds only unrelated frozen concepts (mag/brief_local.py:173, mag/chord.py:80, mag/context_pack.py:523, mag/diary_node.py:483+): no caller branches on the flag, and `frozen` is derived, not settable, so there is no way to SERVE a frozen corpus on demand. T4 is therefore even colder than the lens's framing: not just unmeasured, unconsumed. Cheapest machine-checkable falsifier the lens never named: pin the catalog (copy the pair, backdate mtime > 30d, point the broker at it), ask the same N questions through both arms, grade both arms' answers with the existing citation_lint tool (path-missing / line-past-EOF / phantom-number over each answer): citation resolvability delta IS the photocopy-quality delta, scored by an organ we already bank.
- Falsifier: no citation-lint defect-rate delta between live and frozen arms at N=30 questions means the freshness header is behaviorally ceremony through this door.
- Move: ~60 min, free lanes (ds/flash for answering, citation_lint for grading).

### A3: T2's "already measured" leg has a broken receipt chain, and the temperature axis has zero instrumentation

The lens's blind spot said it trusted the summary on watch/inbox/replay_deepseek_thinking/. I opened the dir (17 spec/receipt files, ls this sitting) and grepped it for the filter law's own vocabulary: "trust bytes", "4-for-4", "authority.override", "bisect" all zero hits in that dir; the only "410" matches are a line-number cite (WIRE_PLAN.md:48) and HTTP-410 platform notes; the phrases live only in RESEARCH_SUMMARY_arena_days_one_two_20261005.md section 4 and as doctrine at state/GENOME.md:34-35. The 7-variant/$0.10 opus bisect raw rows are OWED, not on disk at the cited pointer. Separately, `grep -c -i temperature` over mag/arena_bench.py, mag/lane_salon.py, tools/arena_gwap.py, memory/runs/arena_learning_trail.jsonl, memory/runs/arena_strategy_trail.jsonl = 0 everywhere (all greps exit 1): the temperature axis of T2's grid has no instrument at all. Adjudication of T2: the steal is real but narrower than a grid; the register axis is half-measured (block-behavior only, one law, broken raw chain), the positive axis (disagrees unprompted, holds verdict) is unmeasured, and T3 is literally the first cell of the T2 grid (repetition is one register pressure). Run T3 first and T2 inherits its first row.
- Falsifier: unchanged from DIFF_TARGETS (variance beyond noise across the grid), but the grid must be built after T3's cell exists.
- Move: OWED first (re-locate or re-fire the bisect raw rows), then extend the T3 harness to a (family x register) sweep; temperature passthrough through chat_provider unverified, I did not check it exists.

### A4: the GPS ledger blind spot, censused

sqlite over tools/gps_mcp/gps_ledger.db3 this sitting: verdict_log = 703 rows, capability = 30. The commit-message "593+" is superseded (ledger grew); the summary's "266 rows banked, 178 verdicts fed" is the arena-fed denominator, not the table. Blind spot closed: the ledger is real and larger than claimed.

### A5: the loop has a third weak leg: zero completed circuits

The loop's bank step has run exactly once (blob #1, the triangulation steal receipt, MESH_V2_SELFSTEAL section 3), and no cold-vertex probe has ever fired (the lens's own first blind spot). So "repeatable" is untested as a claim: one rider (her system), zero end-to-end circuits, and the substrate under the loop just showed a green-claim that does not reproduce (A1). The loop's shape is sound; its circuit is unproven, and its organs need the same tripwire culture the estate already applies to census claims.

## 3. The ask's questions, answered straight

- Steal real? T3 yes (coldest, no instrument anywhere, new signal, plus the injection-defense value). T4 yes (zero consumers, nobody has the number, DIFF_TARGETS is right). T1 yes-as-channel but its value is conditional on the A/B moving burn outcomes; land the ledger column first. T2 partial (filter law already banked as doctrine; grid and temperature axis unmeasured; raw receipts OWED). T5 not yet (the variable her claim needs, agreement density, is untyped; the archive is uptime telemetry until that is typed).
- Coldest vertices: T3 (zero measurements, zero instruments), then T4 (zero consumers of an existing flag), then T2-temperature (zero instruments), then T1 (organ exists, channel absent), then T5 (archive exists, variable absent).
- Cheapest machine-checkable falsifiers: T3 = arena_bench multi-turn stage, verdict drift at N=10 (CONFIRM-everything already scoreable via fixture path); T4 = pinned-catalog A/B graded by citation_lint; T1 = burn-ledger verdict column THEN two-week A/B; T2 = T3's cell plus a register sweep; T5 = type Jaccard/shared-token density first, label join last.
- Free-lane order: (0) feeds.py tie-break fix, 15 min, unblocks T1 and repairs the map's PRESENT cell; (1) T3, ~60 min; (2) T4 pin + citation-graded A/B, ~60 min; (3) T1 columns, ~50 min, A/B is the tail; (4) T2 sweep on top of T3's harness; (5) T5 density typing, only then the census.
- What breaks the loop: the prose feedback edge (F4, confirmed), monoculture adjudication (F4, compounded by 8 same-family passes plus this one), zero completed circuits (A5), and green-claims that do not reproduce on rerun (A1). None kill it; all four are fixable this week.

## 4. Laws kept

No em-dashes above. Every claim carries a path:line, a command with its output, or an OWED mark. Universal claims name instrument and scope inline. No file outside this receipt was edited; no probes were fired (this pass is byte-checks and reruns only, per the hostile-pass role).
