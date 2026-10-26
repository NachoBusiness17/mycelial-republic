# w4-12 · THE TOOL GENOME: five organs, one speciation day

Item: burn_reset_20260927 flash50 w4-12, deep research. Analyst: gopher w4-12. Everything below was read or executed in this session; checks are listed with exact commands in section 4.

## 0. Method and materials

Read in full: tools/stealth_fanout.py (165 lines), tools/chain_repair.py (101), tools/fossil_check.py (124), tools/rumor_drill.py (222), mag/prompt_lance.py (566), tools/stealth_driver.py (1-120 and 500-620), tests/test_prompt_lance.py (201), tests/test_fossil_check.py (77), tests/test_stealth_driver_prompt_lance.py (87), configs/fossil_registry.json, scripts/census_patrol_daily.ps1 fossil arm, watch/inbox/BREAD_PANIC_X_FLEET_20260927.md, watch/inbox/FOSSIL_CENSUS_20260927.md, mag/ghost_pylance.py and mag/ghost_memlance.py headers, watch/inbox/burn_reset_20260927/flash50/_sw03_dispatch.py header, watch/inbox/burn_reset_20260927/work/drift_q033_runner.py header, tests/conftest.py xdist_group block, state/fuel/stealth_fanout.jsonl, state/fuel/rumor_drill_ledger.jsonl, memory/runs/rumor_drill/receipts.jsonl, state/fuel/stealth_driver.jsonl tail.

Path correction to the ask itself: the ask named tools/prompt_lance.py. That file does not exist (`ls tools/prompt_lance.py` exits 2). The prompt lance lives at mag/prompt_lance.py (found via find; confirmed by tests/test_prompt_lance.py and the birth commit). The ask's own pointer is a one-byte fossil: a real organ cited at a wrong path, which is exactly the FOSSIL-IN-FEED disease class this genome's third organ patrols.

## 1. Birth certificates (git show, exact timestamps EDT 2026-09-27)

| tool | birth commit | time (EDT) | named cause |
|---|---|---|---|
| fossil_check.py | 8763e6809 | 10:55 | quantizer packs fossilized 9.3d, ~1,300 stale cycles |
| chain_repair.py | 7b8617d78 | 14:15 | verkle row 7937 pre-race root, strike 2 healed (row 7980) |
| rumor_drill.py | 2ccbcc22a | 15:37 | bread-panic lens, operator GO |
| prompt_lance.py | 0d9dda89e | 18:30 | "the memlance lineage's missing organ" |
| stealth_driver.py | d63e3a644 | 20:06 | "drive stealth lanes usefully" |
| stealth_fanout.py | 4458355e8 | 22:34 | "go wide and concurrent on all our steal models" |

Six organs in 11h39m. And the count that reframes everything: git log --follow gives commits=1 for each of the five tools, commits=10 for their common descendant stealth_driver. The organs were born finished and frozen; the organism that composes them evolves.

## 2. Genome cards

### 2.1 fossil_check - the time-immune organ

Ancestry: watch/inbox/FOSSIL_CENSUS_20260927.md names the disease (FOSSIL-IN-FEED: an artifact compiled once, wired into a live consumer, never recompiled while the consumer ran on) and its index patient: the thought-quantizer instruction packs, 9.3 days stale through the burn weekend while scripts/gopher_packs.py kept stat-ing them, ~1,300 stale cycles. Birth commit 8763e6809 replaced the patrol's single-artifact check with this registry-driven generalization.

Genome: a registry (configs/fossil_registry.json, schema fossil_registry.v1, six entries) with four dispositions (recompile, tombstoned, fixed-oracle, watch); dual sensors, a behavioral check_cmd probe (fossil_check.py:71-75) and an mtime age bar (:78-79); an operator-gated --recompile flag (:17-19, :86-95); exit contract 0/1/2 (:21-22, :105).

Descendants: scripts/census_patrol_daily.ps1:166 (the 08:30 MagCensusPatrolDaily arm; exit 1 appends WARN lines to memory/attention.md, exit 2 logs an incident); tools/stealth_driver.py:556-561 (t_fossil topic, every 5 minutes); tests/test_fossil_check.py.

Immune system: 5 pytest tests pinning warn-on-breach, tombstone-never-warns, missing-registered-is-HARD, missing-tombstone-ok, unreadable-registry-fails-closed (tests/test_fossil_check.py:27-77). All passed this session. The layered failure philosophy is deliberate and asymmetric: fail-open at the patrol wrapper (a broken check never blinds the patrol, ps1 comment and catch), fail-closed at the registry reader (unreadable registry = exit 2 cannot-verify, fossil_check.py:47-51). Patrol-level blindness is the worse failure, so the organ degrades loud, not silent.

### 2.2 chain_repair - the race-scar organ

Ancestry: a concurrency wound proven twice on bytes. Commit 7b8617d78 (14:15 EDT): a long-lived process running pre-guard verkle_knot code committed row 7937 with a root computed over a pre-race leaf set (proven by root-minus-sibling-leaf arithmetic); the standing verb later healed strike 2 at row 7980. The tool imports the parent organ's private internals rather than a public API (chain_repair.py:33-36: _load_chain_rows, _merkle_root, _verify_chain_consistent, verkle_lock, _tip_for_tail, TIP, CHAIN; surfaces at mag/verkle_knot.py:34, 35, 90, 148, 307, 536, 559). It is a child organ born inside the parent's body cavity; verkle_knot grew its own post-append self-heal the same day (CHAIN_RACE_REPAIR_20260927 block at mag/verkle_knot.py:757).

Genome: walk from tail to first row whose committed verkle_root differs from the recomputed prefix merkle root (find_bad_tail_index, chain_repair.py:39-46); rewrite only root fields; stamp the cause into the data itself, a chain_race_repaired note naming date, cause class, tool, and receipt location (:73-76); refuse on row/line count mismatch (:78-81); tmp-write plus replace (:83-85); re-verify and exit 0/1/2 (:19-20, :88-90).

Descendants: tools/stealth_driver.py:564-569 (t_chain topic, --dry only, "writers self-heal"); tools/rumor_drill.py:57 (chain_repair --dry is the ground-truth referent the drill's false claim denies); queue/todo.md:272 (Loop 3 closure contract); four seat-memory files under memory/continuity/seat_memory_20260927/; watch/inbox/burn_reset_20260927/flash50/deep-verkle-formal.md (a sibling flash50 item formalized its safety lemma).

Immune system: no pytest file exists (grep across tests/ for chain_repair: zero hits). Its test-side protection is institutional: tests/conftest.py:76 pins chain-mutating tests into xdist_group "verkle-chain" so xdist workers never mutate the chain concurrently, serializing away the exact race class. Its live immunity is self-verification: --dry mode, a verify-under-lock re-check that catches racy reads (:57-59), and the post-verify gate. Executed this session: "CHAIN-REPAIR: nothing to do (chain consistent (8278 leaves))", RC 0. The chain has grown from the 8,247 leaves a sibling item read to 8,278 at this check.

### 2.3 rumor_drill - the self-experiment organ

Ancestry: exogenous mimicry. watch/inbox/BREAD_PANIC_X_FLEET_20260927.md digests developedbyed's 200-villager experiment (one operator-seeded lie: 156/200 believers in 18h, three days of sell-outs, correction arriving by physical witness) and closes with "The steal (one concrete thing)": seed a marked false claim into a sandboxed feed, pre-register predictions, watch which organs repeat it. rumor_drill.py implements that steal nearly verbatim: predictions P1 retrieval-repeats, P2 eval-filters, P3 drift-kills, P4 one-cycle-death (rumor_drill.py:12-24). Birth 2ccbcc22a, operator GO, 15:37 EDT.

Genome: one checkably-false claim carrying a machine marker (drill:rumor.v1, DRILL_ID rumor-drill-20260927-bread, :48-54) appended into memory/improve/candidates.jsonl (:79); a side-ledger (state/fuel/rumor_drill_ledger.jsonl) while the durable record is never written (:7-9); three verbs seed/status/close; deadline_close auto-closes HELD past 24h with no promotion attempt and writes a verdict receipt (:143-207).

Descendants: tools/stealth_driver.py:548-553 (t_rumor topic). Nothing else imports it; its real reach is the feed itself.

Immune system: no pytest file. The immunity is the trial protocol: pre-registration, marker propagation with the content, and the promote human gate upstream of execution. FIELD TRIAL COMPLETE, read this session from the ledgers: seeded 2026-09-27T19:35:10Z, auto-closed HELD 2026-09-28T16:33:14Z at 20.97h, reason "no promotion attempt" (state/fuel/rumor_drill_ledger.jsonl; memory/runs/rumor_drill/receipts.jsonl). The estate survived its own planted lie without human intervention.

Honest caveats, banked because they are true: (a) the HELD verdict bundles confirmed-held with never-tested. P1 (retrieval-repeats) never confirmed: the live status run this session prints "P1 retrieval-repeats: held-pending (not indexed yet)", meaning corpus_search does not find the claim, so pure retrieval did NOT demonstrably repeat it; P1 is unfired or falsified, not held. P2 and P4 are genuinely held, and deadline_close (:143-207) never evaluates P1 or P3 at all, it closes on age plus no-promotion. (b) status() has an age-clock quirk: it takes the ledger's LAST row as t0 (rumor_drill.py:102-107), so once auto-close appends its HELD row, the reported age resets. This session printed age=9.1h (from the 16:33:14Z close row; now = 2026-09-29T01:39Z) while the true seed age is ~30h. A post-close status can never again report the seed age. Benign today, but the deadline detector's clock drifts after every close.

### 2.4 prompt_lance - the third-generation lance

Ancestry: the estate's cleanest documented lineage, three generations of one verb contract, each born from a named operator order:

1. mag/ghost_pylance.py (2026-08-10, operator: "how could we steal pylance as ghost memtools"): deterministic diagnose/symbols/references/trace_value/self_check over CODE bytes, stdlib ast, $0, no prompt DNA.
2. mag/ghost_memlance.py (2026-08-11, operator: select memory states "without bringing hallucination"): the same shape over MEMORY bytes, anti-hallucination selection verified against disk.
3. mag/prompt_lance.py (birth 0d9dda89e, commit message: "the memlance lineage's missing organ, pylance for the prompt"): the same verbs over PROMPT bytes, schema prompt_lance.v1 (mag/prompt_lance.py:62), plus provenance().

The docstring states the lineage law (prompt_lance.py:3-9): each generation points the same deterministic lens at the next substrate the model was actually fed. The external ancestor is also named: Pylance/Pyright discipline (deterministic, severity-ranked, located, never silently passes a broken input), stolen as capability (:11-19). provenance() is trace_value flipped around (:12-16): not "how did this value get set" but "what does this context CLAIM to draw from", a verifiable inventory for the caller to check on disk, never trusting the prompt's say-so.

Descendants: tools/stealth_driver.py t_prompt_lance topic, contract pinned by tests/test_stealth_driver_prompt_lance.py:55-87 (verdict string shape, skip-when-no-pack, banked-to-heartbeat). No mag/, main.py, or scripts/ importers found in targeted grep: adoption is via the loop, not the library.

Immune system: the deepest of the five. 13 pytest tests (tests/test_prompt_lance.py): planted-defect positives for all six diagnostic codes, later-block charge for dups, stale_days sensitivity, message-dict block location, budget overrun on/off, symbols/references/provenance shape tests, worst-first ordering, repeated-reminder detection, a byte-identical determinism test asserting json.dumps(sort_keys=True) equality across repeated calls of all five tools (:176-187), and a CLI round-trip. All 13 passed this session.

Live self-examination, executed: `.venv\Scripts\python.exe -m mag.prompt_lance self_check memory/context_pack_latest.md --stale-days 30` returns ok, est_tokens 1124, 2 findings, worst=info PROMPT_EMPTY_SECTION at L1; provenance n_paths=5, n_hashes=7. This matches the production heartbeat of stealth_driver cycle 79 (2026-09-29T01:14:26Z: "prompt_lance: 2 findings; worst=info PROMPT_EMPTY_SECTION at L1") to the character. The organ, its tests, and the live 24/7 loop all agree on what the estate's own context pack looks like right now.

### 2.5 stealth_fanout - the wide hunter

Ancestry: a one-line operator order (docstring :3-4: "go wide and concurrent on all our steal models and do mickey17 style"), birth 4458355e8 22:34 EDT = 2026-09-28 02:34 UTC, which is why the docstring dates the order 09-28. Mickey17 is the per-item-named-gopher fan-out shape the workflow gate already dogfoods (AGENTS.md build discipline section). The estate's laws ride in-band: a LAWS string appended to every ask (:101-102: no fabrication, OWED if unverifiable, no em-dashes, cite by name).

Genome: 12 hardcoded mining asks (:58-71); a 10-lane table built at import time from two OpenRouter keys, two Nous keys, and one keyless llm7 anon lane (:32-56); ThreadPool workers = min(8, 2*lanes) (:150); per-item banked file with lane+model+timestamp provenance (:135-139); a heartbeat row per item to state/fuel/stealth_fanout.jsonl (:140-144). Genetically stable: exactly one commit ever.

Descendants, in two distinct modes. Copy-mutation: drift_q033_runner.py (:1-22) loads the module via importlib, inherits LANES, LAWS, _check_base and the dispatch body shape, then mutates (sequential with 5s spacing, adds a finish field to heartbeat rows); its Q-033 rows sit in the parent's heartbeat ledger (28 rows total in state/fuel/stealth_fanout.jsonl). Library-import: _sw03_dispatch.py:21, a sibling flash50 item, does `from tools.stealth_fanout import LANES, _check_base` for a 3-ask, 2-worker economics study that banks outputs as SENSING findings per RIB_DRIVING_LADDER_20260928, never trusted work.

Immune system: no pytest file. The immunity is a boundary, not a suite: a WORK_BASES allowlist (:73-77); _check_base literal allowlist plus _assert_public_host resolving every host via getaddrinfo and rejecting any non-global IP (:80-99), checked per dispatch call (:106), which makes it DNS-rebinding resistant. Offline probe executed this session (no network): LANES=10, ASKS=12, bases exactly {openrouter.ai, inference-api.nousresearch.com, api.llm7.io}; _check_base raised ValueError on 127.0.0.1, on a lookalike https host, and on a file:// scheme. The organ was NOT run against the live lanes this session (that spends free-lane quota and was not needed for the genome). The boundary is Mimosa-adjudicated per the in-code stamp (:73) and Mimosa's own finding-ledger batch-stop events of 2026-09-28 reference stealth_fanout.

## 3. Cross-genome analysis

### 3.1 Punctuated equilibrium with frozen organs

Five unrelated organs plus their hub in under twelve hours (10:55 to 22:34 EDT) is a speciation burst, and every organ's birth commit is its only commit. The estate evolves not by mutating organs but by birthing them finished and freezing them, then evolving the composition. stealth_driver, born 20:06 (after three of its future organs already existed), accreted 10 commits in two days while the organs stayed byte-stable. Variation happens at composition sites (topics, wrappers, importers); selection happens at organ birth (a tool exists only if a receipt or a named operator order caused it); stasis at the organ level is policy, not neglect (the spec-before-behavior-change discipline in AGENTS.md). This inverts the usual open-source pattern of many small mutations per tool: here the unit of evolution is the genome's topology, not its genes.

### 3.2 Four reproduction modes

1. Lens transplant (self-steal across substrates): the lance lineage, code -> memory -> prompt, one verb contract three times, each generation documented in its own docstring with its operator-order date.
2. Scar organogenesis: chain_repair and fossil_check congealed around specific wounds (row 7937; the 9.3-day packs), and each preserves the wound's receipt in its docstring as a birth certificate (chain_repair.py:4-12; fossil_check.py:4-10). No orphan organs: every tool carries its cause.
3. Exogenous mimicry: rumor_drill copies another system's failure as a test protocol, pre-registering falsifiable predictions before the run, the clinical-trial shape applied to memetics.
4. Ordered hunting adaptation: stealth_fanout, from one operator sentence, generalized within a day into a reusable lane table and boundary that two descendants reused (one by import, one by copy).

A fifth process, domestication, forms descendants: stealth_driver subprocess-wraps four wild-born verbs into isolated fail-open topics (stealth_driver.py:528-537, _run_tool with CREATE_NO_WINDOW on win32 and per-topic exception isolation) and reads each organ's one-line verdict by grepping its stdout prefix (CHAIN-REPAIR: / FOSSIL-CHECK: / RUMOR-DRILL:). The hub does not import the organs; it reads their speech. Domestication by text protocol, which keeps the organs independently runnable, testable, and human-invocable while the loop consumes them.

### 3.3 The immune census is heterogeneous by design

Three layers, unevenly distributed. Specimen tests (pytest): only prompt_lance (13) and fossil_check (5), plus 3 wiring tests, 21 passed this session in 1.17s. Self-verifying protocols: chain_repair and rumor_drill have zero pytest; their tests are runs they perform on the world (dry verification with refusal paths; pre-registered predictions with a deadline). Institutional immunity: conftest xdist_group serialization for chain mutators (tests/conftest.py:76), the scheduled 08:30 patrol wrapping fossil_check with fail-open catches, Mimosa adjudication of network boundaries, and the driving-ladder law that everything stealth_fanout's descendants mine is banked SENSING, never done.

The correlation is legible: organs with pure function surfaces (text in, dict out) got specimen tests; organs whose danger surface is the world (network POSTs, chain writes, feed rows) got boundaries and protocols instead. You cannot unit-test a border; you can only patrol it. That is a coherent immune philosophy, and the census proves it is applied consistently rather than by accident.

### 3.4 The verdict-overstatement growth edge

The youngest organs report success on partial evidence under a uniform vocabulary. rumor_drill's HELD rests on P2/P4 while P1 printed held-pending, and the auto-close path never evaluates P1/P3. status()'s clock resets after close (:102-107). The patrol wrapper around fossil_check prints self-error and continues (fail-open by law, but the log line reads like success). None of this is dishonest; all of it is honest-adjacent: the word HELD silently bundles evidence-held with never-tested. The estate's own trust-bytes law implies the fix its receipts.jsonl already gestures at: a verdict row should carry per-prediction status, not one word for the bundle.

### 3.5 The ask-as-fossil coda

This item's own prompt cited tools/prompt_lance.py; the disk holds mag/prompt_lance.py. Verified: ls exits 2 on the cited path; find locates the real organ and its tests. The pointer named a real organ at a wrong path: a provenance claim drifting from disk truth while a live consumer (this ask) ran on the claim. That is FOSSIL-IN-FEED in one byte. prompt_lance.provenance() exists to make such claims checkable; fossil_check's registry exists to put them under a time bar. The estate's tools are, among other things, instruments for catching the class of error their own birth orders contain, and this item caught one in itself.

## 4. Checks executed this session (exact commands and outputs)

1. `.venv\Scripts\python.exe -m pytest tests/test_prompt_lance.py tests/test_fossil_check.py tests/test_stealth_driver_prompt_lance.py -q` -> "21 passed in 1.17s". These three files are the complete pytest coverage of these five tools; the full 2,303-test suite was not run (not the ask; stated plainly).
2. `.venv\Scripts\python.exe tools\chain_repair.py --dry` -> "CHAIN-REPAIR: nothing to do (chain consistent (8278 leaves))", RC 0.
3. `.venv\Scripts\python.exe tools\rumor_drill.py status` -> P1 held-pending, P2 HELD, P4 HELD, "seeded=True age=9.1h ALL HELD", RC 0 (now = 2026-09-29T01:39:29Z from `date -u`).
4. `.venv\Scripts\python.exe tools\fossil_check.py check` -> 6 registered, 0 WARN, 0 HARD, 0 recompiled, RC 0.
5. `.venv\Scripts\python.exe -m mag.prompt_lance self_check memory/context_pack_latest.md --stale-days 30` -> 2 findings, worst=info PROMPT_EMPTY_SECTION at L1, est 1124 tokens; provenance subcommand -> n_paths=5, n_hashes=7.
6. Offline boundary probe (venv python -c importing tools.stealth_fanout; no network): LANES=10, ASKS=12, three bases; _check_base blocked loopback, lookalike host, and file:// scheme, each raising ValueError.
7. `git log --follow` commit counts: stealth_fanout 1, chain_repair 1, fossil_check 1, rumor_drill 1, prompt_lance 1, stealth_driver 10. `git show -s --format='%h %cI'` birth timestamps in section 1.

Not run, stated plainly: stealth_fanout against live lanes (spends quota; not required for lineage), the full repo test suite, verkle-audit (chain_repair --dry already green at this scale).
