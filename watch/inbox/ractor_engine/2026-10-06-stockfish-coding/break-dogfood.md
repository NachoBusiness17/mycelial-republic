# break-dogfood: hostile second pass on the stockfish-coding lens report (2026-10-06)

Seat: break-dogfood (workflow child). Every cite below was read or run this sitting on the working tree at HEAD-adjacent state (branch mag/run-beta1-factory-build-audi-20260806T231709Z). Interpreter: `./.venv/Scripts/python.exe` throughout. Anything I could not verify is marked NOT RUN or UNREPRODUCED, never asserted.

## Verdicts

### F1: the imp002 receipt pastes test output the instrument never printed - CONFIRMED (one byte correction to the lens)

- Byte-read this sitting: `watch/inbox/selfimp/imp002.md:27` is `tests/test_selfplay_orchestrator.py ..............            [100%]` with **15** dots (`lines[26].count('.')` -> 15; the lens said 14, off by one) and `:28` is `22 passed in 0.08s`.
- Named-instrument rerun: `.venv/Scripts/python.exe -m pytest tests/test_selfplay_orchestrator.py -q` printed 22 dots and `22 passed in 6.72s` this sitting.
- Impossibility bounds: the test file has exactly one commit, `158952f4e 2026-10-06 11:35:02 -0400` (git log), and the receipt landed 11 minutes later (`cb5c20edf 2026-10-06 11:46:52`), so the receipt describes this exact tree. `llama_cpp 0.3.36` is installed in the venv (probe: `import llama_cpp` -> 0.3.36), so `test_spawn_without_llama` (tests/test_selfplay_orchestrator.py:54-65, timeout=3) floors the suite near 3s on the writing machine. 15 dots vs 22 tests is impossible on any machine.
- Falsifier status: no stored log showing 15 dots + 0.08s for 22 tests was found anywhere I looked; the receipt is the only record and it contradicts the instrument.
- Wall time drifts between runs (6.72s mine, 5.87s lens); the count mismatch does not. Verdict unaffected by the 14-vs-15 correction.

### F2: the receipt's "zero matches" self-play grep claim is byte-false - CONFIRMED

- `git log --diff-filter=A -- tools/mountain_selfplay.py` -> ADD `0b846c01f 2026-09-30 19:20:42 -0400`; modified `785b1b139 2026-09-30 20:16:34`. Both six days before the receipt commit.
- `watch/inbox/selfimp/imp002.md:11` verbatim: "No existing self-play code was in the repo (grep confirmed: zero matches for selfplay/self_play/actor_reward/Elo)."
- Quantifier re-census (estate law): `git grep -cin elo -- tools/mountain_selfplay.py` -> 4; `git grep -cin self_play` -> 10; `selfplay` -> 0; `actor_reward` -> 0. Two of the four claimed-zero tokens are nonzero inside the claim's own scope.
- Lens nit: the phrase "MOUNTAIN COMPLETE" is in `785b1b139`'s message, not `0b846c01f`'s (which reads "R12 FIRST ACTION + D-wave lands..."). Hashes and dates in the lens evidence are correct; the label is swapped.
- Full-tree historical census of all four tokens at `cb5c20edf^`: NOT RUN; the single decisive counterexample was run instead.

### F3: filed but never wired; the shipped entry point can only emit hash-garbage - CONFIRMED, and strengthened

- Consumer census over all tracked files (git grep -ln "selfplay_orchestrator", this sitting): `mag/selfplay_orchestrator.py`, `tests/test_selfplay_orchestrator.py`, `memory/corpus/quantized_thought/graph_ghosts/forget_events.jsonl:1490`, `memory/knowledge_graph.json:1` (single-line file), plus two prose write-ups (`watch/inbox/ractor_engine/ractor-topic/dogfood.md`, `watch/inbox/selfimp/imp002.md`). No reference in `main.py`, `mag/lanes.py`, `mag/lane_runner.py`, or `memory/workflows/REGISTRY.jsonl`.
- `main()` (mag/selfplay_orchestrator.py:283-313) constructs the default bridge and never calls `spawn_server`; `LlamaCppBridge._available` starts False (mag/llama_cpp_bridge.py:50) and `generate_move` returns the sha256[:8] JSON fallback when unavailable (:158-166, :229-235).
- Probe reproduced the lens's hash exactly: sha256 of "Solve: What is 2+2? Answer with just the number." [:8] = `c5148f42`, and `_check_answer` on that fallback JSON returns True by substring luck ("4" in the hex).
- Strengthened beyond the lens: `memory/runs/selfplay/evidence_latest.json` (mtime Oct 6 16:30 -0400) contains real-model output ("17 x 23 = 381", actor_ms 2797-5297, scorer_ms 1953-5766, n_correct 5/8). The fallback path emits timing_ms=0 + `fallback_move` JSON, so this file was written by a bypass script driving a real model, not by the shipped `main()`. Running the front door today would clobber real evidence with fallback output.
- The bypass writer is not in the tracked tree: `git grep -l "d13-selfplay-run"` -> mag/llama_cpp_bridge.py, tests/test_selfplay_orchestrator.py, watch/inbox/MIRA_METAREASONING_20261006.md; none is a writer script.

### F4: the loop's reward and ground-truth legs are unsound - CONFIRMED

- Elo probe byte-reproduced: `EloEngine(baseline=1200).update(1.0)` -> 1207.7 (raw 1207.688...); `inspect.getsource(EloEngine.update)` confirms it uses the class constant `self.BASELINE_RATING` (1000.0, mag/selfplay_orchestrator.py:86, used at :97) and there is no stored-baseline attribute (probe: `self.baseline` in source -> False).
- `_check_answer` substring fallback confirmed at mag/selfplay_orchestrator.py:270-278 (float-parse first, then `str(expected) in move_str`).
- End-to-end fallback benchmark run this sitting (unspawned bridge, all 8 MATH_PROBLEMS through generate_move + _check_answer): 0/8 correct. On this problem set the hash coin lands all-false; the coin-flip mechanism is real, the outcome here is deterministic False.
- Scorer sample always ok=True confirmed at mag/selfplay_orchestrator.py:170, appended unconditionally after the try/except at :164-168.
- The winning coin side is pinned by the suite: tests/test_selfplay_orchestrator.py:109 asserts `result.correct is True` under the comment "fallback move won't match; but check structure". The comment is byte-false: the hash contains the digit (probe above), so the assertion holds by hash luck.
- UNREPRODUCED sub-evidence: the lens's second coin example (answer 7 -> hash `d69e6da2` -> correct=False). sha256(b"7")[:8] = `7902699b`, which itself contains "7" (would read correct=True). I could not identify the prompt yielding `d69e6da2`. The mechanism stands on the reproduced `c5148f42` example; treat the `d69e6da2` cite as unverifiable as stated.

### F5: the door runs tonight on the estate's own gate oracle, not a chess engine - CONFIRMED on every checkable cite

- `where.exe stockfish` -> "Could not find files for the given pattern(s)". No stockfish binary.
- `.venv/Scripts/python.exe -c "import chess; print(chess.__version__)"` -> python-chess 1.11.2.
- mag/agent_arena.py:20: `SUPPORTED_GAMES = frozenset({"chess"})` (read via sed 18,24).
- `tools/citation_lint.py` and `tools/violation_ratchet.py` both on disk (ls).
- citation_lint rerun on the lens's banked dogfood.md reproduces their exact output line: `CITATION-LINT: ok records=1 anchors=13 numbers-checked=0 blocking=0 warns=7`.
- Caveats: the finding text arrived truncated mid-word ("...whi"), so its final clause could not be byte-checked; this verdict covers the visible claims only. The falsifier's second leg (30 fixture bouts showing no repair gradient over unguided repair) was NOT RUN by me and remains untested, as the lens itself disclosed.

## Blind-spot closures (checks I ran that the lens cancelled or deferred)

1. Dash hygiene (lens cancelled mid-run): programmatic count on watch/inbox/selfimp/imp002.md -> 9 U+2014 em-dashes, 1 U+2013 en-dash. The lens's own banked files (dogfood.md, break-accuracy.md in this directory) -> 0 and 0. See addition A1.
2. knowledge_graph.v2 node + forget row (lens had rg -l only): python json parse of memory/knowledge_graph.json -> `module:selfplay_orchestrator.py` is LIVE in `nodes[]`; `memory/corpus/quantized_thought/graph_ghosts/forget_events.jsonl:1490` logs a "forget" of the same module at the same graph ts `2026-10-06T18:06:27.608164Z` with pointer-law "demoted-not-deleted (S9 ARC)" pointing at `graph_ghosts/module/selfplay_orchestrator.md`; `ls` that path -> "No such file or directory". See addition A2.
3. evidence_latest.json writer (lens unresolved): bounded, not closed. Content shape proves live-model provenance (F3 above); the writer script itself is unidentified in the tracked tree. See addition A3.
4. flash_call internals (lens confirmed existence at :684 only): read the head, mag/lane_runner.py:684-690: `def flash_call(system, user, max_tokens=1536)`, LAW-058 AMENDED 2026-10-03, the env-pinned OPENROUTER door (OPENROUTER_MODEL + OPENROUTER_API_KEY), z.ai lane pulled from rotation 2026-10-03. Body past :690 not read.
5. citation_lint determinism across reruns (lens named as untested): two runs on the same fixed bytes of dogfood.md returned byte-identical output (`ok records=1 anchors=13 numbers-checked=0 blocking=0 warns=7`, same WARN list). One instrument, one file, two moments: deterministic on this sample. violation_ratchet determinism NOT RUN (needs changed-file state).
6. QUEEN arXiv fetch (lens deferred to the accuracy lens): WebFetch of arxiv.org/abs/2610.03695 this sitting -> "Language Models that Play Chess and Explain Their Moves", Bhaskar, Cheng, Chen, submitted 2 Oct 2026; abstract states over 900 Elo (1782 to 2697), 4B params, silent expert chess encoder via cross-attention, natural-language Bellman update. Byte-matches the estate receipt's card verbatim (watch/inbox/QUEEN_CHESS_LM_20261006.md:11-15). The receipt's OWED arXiv id (:6) is curable with 2610.03695. The receipt's own caution stands (:36): the Elo numbers are the paper's claims, not re-measured here.

## Additions (what the lens missed)

A1. The imp002 receipt violates the no-em-dash law and documents bypassing the estate's own hook. Evidence: 9 U+2014 + 1 U+2013 counted programmatically in watch/inbox/selfimp/imp002.md; imp002.md:52 confesses "Pre-commit hook broken ... bypassed with --no-verify; files manually verified clean." Falsifier: a recount showing 0 em-dashes, or a law amendment licensing them in receipts. Move: 10 min, strip the dashes and register the hook failure by name per AGENTS.md build discipline (never silently bypass).

A2. The graph-ghost forget row for the module dangles in both directions. Evidence: forget_events.jsonl:1490 claims demotion with a pointer file that is absent on disk, while the live `nodes[]` of memory/knowledge_graph.json still carries the module at the identical ts. Falsifier: the pointer file exists at another path, or the graph regen job re-admits forgotten nodes by design. Move: 15 min, write the ghost pointer or strike the forget row, and add a dangling-pointer tripwire to the demotion pipeline.

A3. The d13 evidence file postdates its own bank receipt by ~4.7 hours and carries no provenance. Evidence: memory/runs/selfplay/evidence_latest.json mtime Oct 6 16:30 -0400 vs receipt commit cb5c20edf 11:46:52; the JSON has no model name, command, or writer id; content proves a live run (F3). Falsifier: a committed writer script that spawns the bridge and stamps provenance (census found none). Move: 10 min, add writer/model/cmd fields to the evidence schema and repoint the receipt at the real evidence moment.

A4. The orchestrator suite is not hermetic: it rides the live paid API door with no mock. Evidence: mag/selfplay_orchestrator.py:163-166 imports and calls `flash_call` inside play_one; `git grep -n flash_call tests/conftest.py tests/test_selfplay_orchestrator.py` -> zero hits (no mock); flash_call is the OPENROUTER env door (mag/lane_runner.py:684-690). My run had OPENROUTER_API_KEY unset (probe: False), so tests exercised the except path; on a keyed machine the same suite fires real paid calls from 9 play_one invocations (1+3+1+4 across tests) and the Elo rewards ride API nondeterminism. Falsifier: an autouse network-blocking fixture my grep missed (conftest body not read; suite not run with a key set; both unchecked). Move: 10 min, monkeypatch flash_call in tests so the reward leg is deterministic and $0.

## Scope notes

- I did not read mag/lane_runner.py past :690, the full conftest body, the economics/operations lens files, or break-accuracy.md; convergence flags with other lenses are therefore not asserted anywhere above.
- The QUEEN receipt's S2 steal row (the encoding door ractor) is the frame this whole directory serves; my pass touches only the byte-truth of the lens report and the imp002/d13 artifact chain around it.
