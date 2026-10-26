# break-operations: hostile second pass on the operations lens (2026-10-06 stockfish-coding)

Seat: break-operations (subagent, dynamic workflow). Moment of pass: 2026-10-06T20:09:32-04:00.
Method: byte-check every evidence cite in the lens report against the estate; re-run the lens's own
grep; re-run the gates with honest exit capture; census the truncated finding's absence claim under
the quantifier law. No falsifier that destroys estate evidence was executed; each not-run check is
named below. One self-caught instrument error is filed (see "Instrument errata").

Note on input: the lens report arrived with finding 5 truncated mid-sentence ("...the Elo-ladder
half of the QUEEN stack alrea") and its evidence object missing. F5 is verdicted on its visible
claim only; its own cites could not be byte-checked.

## Verdicts

### F1 (spawned-but-never-queried expert server; banked bottleneck verdict measures the wiring, not the model): CONFIRMED

Every cite byte-verified this sitting:

- Lens grep reproduced exactly. Command: `grep -rn "8081\|/completion" mag/llama_cpp_bridge.py mag/selfplay_orchestrator.py`. Output: exactly two hits, `mag/llama_cpp_bridge.py:27` (`DEFAULT_PORT = 8081`) and `mag/llama_cpp_bridge.py:129` (endpoint string `http://{host}:{port}/completion`). Follow-up: `grep -n "urllib\|requests\|httpx\|urlopen"` on both files shows urllib confined to the readiness poll (`mag/llama_cpp_bridge.py:21,134,143`). `generate_move` (`mag/llama_cpp_bridge.py:152-196`) issues zero HTTP; it constructs a fresh in-process `Llama(model_path=...)` on every call (`:171-176`).
- The spawn receipt quote is real: `memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d13-selfplay-run.json:12` banks `SPAWN: {"ok": true, "pid": 15036, "fallback": false, "endpoint": "http://127.0.0.1:8081/completion"}`.
- The GGUF size claim is byte-true: `stat -c '%s'` on `C:\Users\foste\.ollama\models\blobs\sha256-c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12` reads `1678447520 bytes`, and `od -c` on the first 16 bytes shows the `GGUF` magic.
- The banked verdict numbers are real: `memory/runs/selfplay/evidence_latest.json` (read this sitting) holds `avg_actor_ms 3472.6 / avg_scorer_ms 2966.9 / bottleneck "actor"`, and `d13_selfplay_evidence.json` holds `wall_s: 56.8` (read via python this sitting).

The defect reading survives, with one nuance the lens under-credited: the in-process path is
disclosed, not concealed. The probe docstring says "generate_move then runs real in-process
inference" (`memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d13_selfplay_run_probe.py:8`),
and the receipt names the CPU-compute deviation (`d13-selfplay-run.json` rows[0]). What is NOT
disclosed anywhere is that the banked verdict is load-dominated: 8 problems mean 8 full loads of a
1,678,447,520-byte Q5_K_M model on CPU, and the module docstring still advertises the dead design
("generates self-play moves via its HTTP API", `mag/llama_cpp_bridge.py:2-3`), so the wiring
defect reading stands. Falsifier (reroute through the live endpoint, re-run, watch the verdict
flip) is sound and cheap; actor leg must drop to per-token HTTP latency once the model loads once.

Not run: the reroute re-run itself (45 min, real inference; out of this pass's scope; the static
byte-check already proves no HTTP client exists in the generation path).

Rider checked and dead: pid 15036 is not running (`tasklist /FI "PID eq 15036"` reads no tasks);
the probe shut the server down (`d13_selfplay_run_probe.py:109`). No leak.

### F2 (dead scorer silently falls back to neutral 0.5, recorded ok=True): CONFIRMED

- Code chain verified: `mag/selfplay_orchestrator.py:164-168` (bare `except Exception:` to `_fallback_score`), `:249-251` (`_fallback_score` returns `"0.5"`), `:170` (`BottleneckSample(leg="scorer", ms=scorer_ms, ok=True)` appended unconditionally).
- The d13 run really did have a live scorer: python read of `d13_selfplay_evidence.json` this sitting shows `usage_rows: 8`, first row carrying real OpenRouter cost fields (`cost 0.00012892`, `upstream_inference_cost` breakdown, `reasoning_tokens: 32`).
- The shape-is-identical claim is byte-true: same file shows `samples: 16, all_ok: True, Counter({'actor': 8, 'scorer': 8})`, and `d13-selfplay-run.checks.json:5` banks exactly the "16 BottleneckSamples (8 actor + 8 scorer, all ok...)" claim the lens cited.
- The meter-patch claim is verified: `mag/thought_bank.py:48-55` shows `bank_response` resolving the module-global `bank` at call time (`:52`), so the probe's `thought_bank.bank` patch intercepts; `mag/lane_runner.py:720-721` shows `flash_call` banking every response through `bank_response`.

Not run: the unset-OPENROUTER_API_KEY re-run. It is destructive in exactly the way F4 describes:
the probe writes both `d13_selfplay_evidence.json` and `memory/runs/selfplay/evidence_latest.json`
(`d13_selfplay_run_probe.py:130-153`), so running the falsifier clobbers the day's only real
evidence. The static read settles the question the falsifier would: with the key unset, `flash_call`
raises, line 168 substitutes `"0.5"`, line 170 still appends ok=True. The instrument cannot scream.

### F3 (organ ungated and partly uncommitted; --no-verify bypass; uncommitted fixes claimed as byte-proven): CONFIRMED, move amended

- Commits dated today: `git show -s` reads `158952f4e 2026-10-06 11:35:02 -0400` and `cb5c20edf 2026-10-06 11:46:52 -0400`. (Three link-drop commits landed after them, newest `33b596fa6` 18:28; the lens's "committed today" holds.)
- No upstream: `git rev-parse --abbrev-ref --symbolic-full-name @{u}` reads `fatal: no upstream configured for branch 'mag/run-beta1-factory-build-audi-20260806T231709Z'`.
- Diff stat byte-exact: `git diff --stat mag/llama_cpp_bridge.py tests/test_selfplay_orchestrator.py` reads `42 ++++++++++...` and `11 +++...`, summary `2 files changed, 41 insertions(+), 12 deletions(-)`. The uncommitted diff content is confirmed by grepping the diff: the `--n_ctx` rename, the DEVNULL fix, and the `/v1/models` poll are all `+` lines.
- `watch/inbox/selfimp/imp002.md:52` documents the bypass verbatim ("Pre-commit hook broken... bypassed with --no-verify").
- `state/CURRENT.md:51-52` carries the 3-stash risk and `git stash list` reads 3 stashes on this branch.

Amendment to the lens's move ("commit, set upstream, push once so the gates actually execute"):
the facts are confirmed, but the push will BLOCK at citation lint as the tree stands. See
addition A2. Also the scenario-suite leg of the move is moot for this organ: per the build
discipline (AGENTS.md, Build discipline section) the suite fires only when `tools/workflow_gate.py`
changes, and no evidence shows this organ touching it.

### F4 (evidence surface last-write-wins; unconfigured front door would clobber the day's only real evidence): CONFIRMED

- Write path verified: `mag/selfplay_orchestrator.py:289-291`, `evidence_path = Path("memory/runs/selfplay") / "evidence_latest.json"` then `write_text`, no timestamp, no history; `main()` at `:286` constructs `SelfPlayOrchestrator()` whose default actor is `bridge.LlamaCppBridge()` with no model_path (`mag/selfplay_orchestrator.py:138`), `_available` stays False (init `mag/llama_cpp_bridge.py:50`, never spawned in `main`), so `generate_move` rides the fallback branch (`:158-166`) returning the sha256 placeholder (`:228-235`).
- The at-risk file is real and currently holds the d13 numbers: read this sitting, `memory/runs/selfplay/evidence_latest.json` holds `accuracy 0.625 / elo 1033.1 / avg_actor_ms 3472.6`, mtime `2026-10-06 16:30:39 -0400`, 2143 bytes. The lens's "10/6/2026 4:30 PM local" matches.
- The analog cite holds: `dashboard/data/ESTATE_INDEX.pointer.json` is `pointer: true` with a `master` path, counts, and an explanatory note (read this sitting).

The lens under-claimed one direction: the destruction is not hypothetical. The d13 receipt admits
it already happened today on the probe-side file: "Three earlier probe runs today completed on the
designed fallback actor path... and their evidence files were overwritten by this final run"
(`d13-selfplay-run.json` rows[0], last sentence).

Not run: the lens's falsifier (`python -m mag.selfplay_orchestrator` unconfigured, then diff).
Destructive by construction: it would overwrite the very file the finding says is at risk. The
static byte-check proves the write path; the falsifier would add nothing the code does not state.

### F5 (S2 encoding door has zero bytes in the tree; Elo-ladder half already exists): WEAKENED

The finding arrived truncated mid-sentence with no evidence field, so its own cites are
unavailable for byte-check. The visible absence claim was re-censused under the quantifier law:

- Instrument: `git grep -ilE "chess|goban|forsyth|shogi" -- mag tools tests` (tracked files only; untracked files excluded; moment 2026-10-06T20:09:32-04:00). Result: 16 files hit.
- Inspection of the hits: all are seat-vs-seat game surfaces or teaching/tactical files, e.g. `mag/agent_arena.py:1-3` ("Agent arena: proof-of-concept game surface for seat vs seat (chess first)", python-chess board with UCI move parsing at `:81-96`). No hit encodes a programming-problem class as board + move space + reward for a silent expert. The door-bytes absence holds at this scope.
- The truncated existence half is consistent with the tree: `mag/agent_arena.py` plus `configs/arena_probes.yaml` plus the QUEEN receipt's S4 Elo-ladder row (`watch/inbox/QUEEN_CHESS_LM_20261006.md:30`) are the Elo-ladder half, present.

Weakened, not confirmed: without the lens's evidence field I cannot verify what instrument IT ran,
and the second half of its sentence is missing. The claim as visible is supported by my own census.

## Additions (what the lens missed)

### A1: the committed benchmark half of the organ is a tautology machine

`benchmark_bridge` computes its headline flag from a constant. `mag/llama_cpp_bridge.py:273`:
`"fallback": all(not r.get("ok", False) for r in [{"ok": False}] * rounds)` iterates the literal
list `[{"ok": False}] * rounds`, never the collected `results` (`:265`), so the flag is always
True by construction. And `benchmark_bridge` (`:259-266`) never calls `spawn_server`, so its
timings can only ever be the fallback path's `timing_ms: 0` (`:163`). The test pins only key
presence (`tests/test_selfplay_orchestrator.py:45-47` asserts `"avg_ms" in result`), so the fix is
unpinned and safe.
Falsifier: patch `:273` to iterate `results` and add one mocked ok:True row asserting the flag
flips; if the committed flag is already results-derived, this addition is wrong.
Move: 10 min.

### A2: the lens's F3 move cannot execute as stated; the changed tree fails citation lint right now

`.venv\Scripts\python.exe tools\citation_lint.py check --changed` ran this sitting with honest
exit capture: exit 1, exactly 7 blocking PHANTOM-NUMBER findings, 3 at `AGENTS.md:29` (4,188 /
4,147 / 100M against the last_mile census sources) and 4 in `memory/zknot/2026-09-*sess*.md`
files, matching `d13-selfplay-run.json` rows[3] verbatim ("7 blocking PHANTOM-NUMBER findings ALL
in files this lane never touched"). The push that would exercise the pre-push gates blocks at the
lint leg until the 7 sibling findings are fixed or accepted by name via
`configs/citation_lint_baseline.json`.
Falsifier: fix or baseline the 7 findings, rerun the tool; exit 0 unblocks the push and kills
this addition.
Move: +15 min on top of the lens's 15 (fix or owner-accept the 7 sibling citations first, then
commit and push).

### A3: the trigger's own provenance is OWED, and no lens finding surfaced it

The founding thesis's only on-record source is `watch/inbox/QUEEN_CHESS_LM_20261006.md`, and that
receipt banks its own gaps: `:6` "arXiv id + repo URL OWED (search index lag...)"; `:35` "OWED:
arXiv id, repo URL, weights"; `:36` "The Elo numbers and the GPT-5.6-Sol coherence comparison are
the paper's own claims, not re-measured here"; `:3-4` shows the provenance is an fxtwitter fetch
plus an abstract-card image. Commit `33b596fa6` repeats "arXiv id + repo OWED". All five lens
findings presuppose the 900-Elo / 1782-to-2697 numbers as ground truth; not one surfaced that the
trigger is single-source and unreproduced. The receipt is honest about this; the lens was not.
Falsifier: resolve the arXiv id and repo (the S5 watch row, `QUEEN_CHESS_LM_20261006.md:31,35`).
If both land with weights and the Elo curve is in the paper's own bytes, the gap closes.
Move: 20 min, one fetch sitting for arXiv id + repo before any S2 design byte is written.

### A4: the gate story has a wound: the ratchet tool executed destructively on --help today, and its residual debt is verified present now

`d13-selfplay-run.json` rows[3] files the INCIDENT: "passing --help to
tools/violation_ratchet.py baseline-update was ignored and the update EXECUTED, registering 2
debts attributed 'by: operator'"; `configs/violation_baseline.json` was reverted (verified: `git
status --porcelain tools/fold_gate.py configs/violation_baseline.json` is empty). The residual
debt is real in the current tree: `tools/fold_gate.py:110-111` reads `except FileNotFoundError:` /
`pass  # another waiter broke it first`, a silent-except shape outside today's ratchet scope
(the PASS ran over 10 changed files; `tools/fold_gate.py` is not among them). The lens's gate
narrative ("gates never ran on them") missed that a gate tool itself misfired today and that its
misfire left a named, unowned debt in committed code.
Falsifier: run the ratchet with `tools/fold_gate.py` in scope after registering or fixing the
debt; if no NEW fires, the residual is already owned.
Move: 10 min (fold_gate's owner fixes the two-line debt or accepts it by name; plus a --help
guard in `tools/violation_ratchet.py`).

## Instrument errata (self-filed)

First citation-lint run this sitting captured the exit code of `tail` through a pipe (read 0,
meaningless). Caught, rerun with output to a file and honest `$?`: exit 1. The 7-finding count
and the AGENTS.md/zknot distribution come from the corrected run.

## Checks not run (and why)

- F1 falsifier (reroute generate_move through the live endpoint, re-run the 8-problem session): real inference, ~45 min, out of pass scope; static byte-check already proves the no-client fact.
- F2 falsifier (unset OPENROUTER_API_KEY, re-run probe): destructive, overwrites both d13 evidence files via `d13_selfplay_run_probe.py:130-153`; static read settles the outcome.
- F3 falsifier (git stash, re-run probe on committed code): destructive to the working tree that F3 itself says is at risk from sibling stashes; not run.
- F4 falsifier (run `python -m mag.selfplay_orchestrator` unconfigured): destructive, clobbers `memory/runs/selfplay/evidence_latest.json`; not run.
- QUEEN external anchors (MIRA 2610.02525, token cues 2610.06851, ALoDLM 2610.04198 first-hand fetches): not re-fetched this sitting; the ask's trigger material and the estate receipts are cited as given.

## Instruments and moments

- All code reads: working tree at branch `mag/run-beta1-factory-build-audi-20260806T231709Z`, moment 2026-10-06T20:09:32-04:00.
- Census instrument for F5: `git grep -ilE "chess|goban|forsyth|shogi" -- mag tools tests`, tracked files only, 16 hits, same moment.
- Gates: `tools/citation_lint.py check --changed` exit 1 (7 blocking), `tools/violation_ratchet.py check --changed` PASS (hits=2, registered=2, NEW=0), same sitting.
- Probe/live-state: `tasklist /FI "PID eq 15036"` no match; GGUF stat 1,678,447,520 bytes with GGUF magic.
