# DOGFOOD LENS: the Stockfish-coding raction, 2026-10-06

Seat: dogfood lens, ractor-engine. Jacket: the finding filed but never wired.
Topic: the operator's founding thesis ("put Stockfish in charge of coding by
encoding programming problems in chess, then to AlphaGo", QUEEN receipt
watch/inbox/QUEEN_CHESS_LM_20261006.md:7) against the estate's bytes.

Method: every claim below was read or run this sitting. Checks run: the
selfplay test suite (`.venv/Scripts/python.exe -m pytest
tests/test_selfplay_orchestrator.py -q` -> `22 passed in 5.87s`), two
non-destructive orchestrator probes (default path play_one on answers 4 and
7), an EloEngine baseline probe, `import chess` (1.11.2), `where stockfish`
(not found), `git log --follow tools/mountain_selfplay.py`, scoped rg greps
for selfplay wiring (globs named per finding). Things I did not do are in
blind spots, never filled.

## The encoding map (what runs tonight, one seat one sitting)

Problem class: gate-debt clearance on prose and citations, the exact class
the pre-push wall blocks on. All components byte-verified on disk tonight:

- Board: one document position (sentence tokens + citation claims + the
  lint findings on them). Finite, small, fully observable.
- Moves: repair edits. Re-cite a real path, fix the cited range, delete or
  downgrade the quantity claim, accept by name into the lint baseline.
- Reward: `tools/citation_lint.py check --files <doc>` exit code with
  violation_ratchet debt not increased (tools/citation_lint.py and
  tools/violation_ratchet.py both exist on disk, verified tonight; the CLI
  help prints `check [-h] (--changed | --files FILES ...)`). Deterministic,
  byte-exact, seconds per verdict: this is the silent expert, not a chess
  engine. The estate has no stockfish binary (`where stockfish` -> not
  found) but it owns a shelf of exact evaluators; that is the point of the
  door.
- Actor: the local janitor through the llama_cpp bridge that imp002 already
  landed (mag/llama_cpp_bridge.py, llama_cpp importable, probe confirmed
  `_llama_available=True`).
- Explain layer: QUEEN's QA curriculum shape. Every accepted move must
  produce the fix-comment-with-receipt (the estate's own build law), so the
  model learns why the citation failed, not just that it did.
- Port layer: winning repair sequences distilled into lint fixtures plus a
  rib row plus the quantizer pack. That is the fold loop the estate already
  runs; QUEEN receipt S3 names it the distill-back probe
  (QUEEN_CHESS_LM_20261006.md:29).

Convergent (accuracy lens F4, independently re-derived by me tonight):
python-chess 1.11.2 installed, mag/agent_arena.py:20
SUPPORTED_GAMES = frozenset({"chess"}), START_FEN at :30, no chess engine
binary on the machine. The chess board exists; the chess engine does not.
The estate's silent experts are its gates and deterministic instruments,
exactly as the QUEEN receipt S1/S2 mapped (QUEEN_CHESS_LM_20261006.md:27-28).

## F1. The imp002 receipt's own pasted instrument output is not what the instrument printed

watch/inbox/selfimp/imp002.md:27-28 pastes
`tests/test_selfplay_orchestrator.py .............. [100%]` and
`22 passed in 0.08s`. Fourteen dots cannot be twenty-two tests, and my run
of the same file tonight printed `22 passed in 5.87s`, 73x the claimed wall
time. The count happens to be right; the pasted output is hand-altered or
from a different instrument moment. This is the census disease in receipt
form: never paste a count without the instrument line, and never paste an
instrument line you did not copy from the instrument.
Falsifier: a stored log showing the suite printing 14 dots and 0.08s for 22
tests. Move (10 min): repaste the receipt's Test numbers block from a fresh
pytest run and name the run's moment.

## F2. The receipt's "no existing self-play code" grep claim is byte-false, and the real self-play organ was left unreferenced

imp002.md:11 claims "No existing self-play code was in the repo (grep
confirmed: zero matches for selfplay/self_play/actor_reward/Elo)". Git
truth: `git log --follow tools/mountain_selfplay.py` shows the mountain
organ landed 2026-09-30 19:20:42 (0b846c01f, "MOUNTAIN COMPLETE (5 commits
c38ded6)") and grew same-day (785b1b139 20:16:34, "SELF-PLAY (greedy ties
optimal default, DNFs traps ...)"), six days before imp002 landed
(158952f4e, 2026-10-06 11:35:02). tools/mountain_selfplay.py is the estate's
real self-play surface: four deterministic boards (mountain, shrine, foundry,
spelunk, docstring :39-53), a seeded strategy ladder (random, greedy,
heuristic, :13-37), a real wire with SRP6 and a hash-chained log verified
from disk (:1-11). The new orchestrator references it nowhere. Two self-play
organs, one week apart, zero cross-reference, and the one with the honest
evidence ladder got no link from the receipt that claimed it did not exist.
Falsifier: proof mountain_selfplay.py was absent from the working tree at
2026-10-06 11:35 (it would have to be an untracked deletion restored after;
git says otherwise). Move (15 min): correct imp002.md:11 and wire the
mountain boards into the door card as the skill-separation reference the
fixture ladder will be judged against.

## F3. Filed but never wired: the orchestrator's shipped entry point can only produce hash-garbage evidence

Scoped wiring census (instrument: `rg -n "selfplay_orchestrator"` over the
whole tree minus watch/, memory/runs/, catalog/, dist_audit/, plus explicit
greps over main.py and memory/workflows/REGISTRY.jsonl, run tonight): the
only references are the module itself, its test file, a knowledge_graph.v2
node, and a graph-ghosts forget-events row. No CLI, lane, autorun, governor,
or workflow consumes it. The shipped entry (`python -m
mag.selfplay_orchestrator`, mag/selfplay_orchestrator.py:316) constructs
LlamaCppBridge() with model_path=None (:138), never calls spawn_server (no
call site outside tests in my grep), so `_available` is False forever and
generate_move returns the sha256 placeholder (llama_cpp_bridge.py:158-166).
Probe tonight: default-path play_one returned actor_move
'{"fallback_move": "c5148f42", "confidence": 0.0}'. The d13 lane got real
evidence by using its own probe script
(memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d13_selfplay_run_probe.py
exists; file content unread by me), bypassing the shipped CLI. Per the
estate's own no-orphan-behavior build law, the entry point either gets wired
or gets deleted.
Falsifier: any import or subprocess of mag.selfplay_orchestrator outside
tests, or a default-path run reaching a live model without spawn_server.
Move (30 min): wire the d13 probe's working invocation into mag/lanes.py as
a named lane, or remove the dead CLI main() so the front door cannot bank
fallback garbage over real evidence (last-write-wins on
memory/runs/selfplay/evidence_latest.json is the operations lens's F3
territory; I flag it, they own it).

## F4. The reward and ground-truth legs are unsound: correctness on fallback moves is a hash coin flip, and the Elo baseline parameter is half-ignored

Two probes tonight, same mechanism, opposite verdicts: answer 4 ("What is
2+2?") -> fallback hash c5148f42 -> `_check_answer` substring test finds "4"
inside the hex hash -> correct=True; answer 7 ("What is 1+6?") -> hash
d69e6da2 -> "7" absent -> correct=False
(mag/selfplay_orchestrator.py:270-278). tests/test_selfplay_orchestrator.py:109
pins the winning side of that coin
(`assert result.correct is True`). Second probe: `EloEngine(baseline=1200)`
after one win reads 1207.7, not 1216, because update() computes expected
against the class constant 1000 and the constructor stores nothing
(mag/selfplay_orchestrator.py:89-98; inspect: no `self.baseline` in update's
source). Third: the scorer BottleneckSample is appended ok=True
unconditionally (:170), so a dead scorer leg is indistinguishable from a
live one (CONVERGENT with operations lens F2; convergence outranks).
For the QUEEN door this is the load-bearing lesson: the weld's reward must
come from a deterministic byte-verifiable oracle, never a substring test or
an LLM rater, or the Bellman analogue distills noise while the ledger reads
green.
Falsifier: a rerun where correctness is float-parse-only (no substring
fallback), a baseline-respecting Elo, or scorer samples that mark fallback
as not-ok; any of those changes my verdict. Move (45 min): harden
_check_answer, mark scorer fallback ok=False, fix the Elo baseline bug,
re-run the suite, bank the fix comments with these probes as receipts.

## Kill criterion and the moonshot

Kill the gate-clearance door if: (1) citation_lint verdicts differ across
reruns on fixed doc bytes (oracle non-determinism kills the silent-expert
premise; not yet measured, named in blind spots); or (2) after about 30
fixture bouts, oracle-guided repair does not beat unguided repair (no skill
gradient, no learnable reward). The mountain ladder is the standard: it
already measured board-level skill separation ("greedy ties optimal default,
DNFs traps", 785b1b139), so fall back to its boards where the gradient is
proven. Moonshot (10x): the harness as a self-play league. MIRA's
meta-reasoner writes the work orders (banked 2026-10-06,
watch/inbox/MIRA_METAREASONING_20261006.md), the 50-wide envelope fleet is
the population, token-cue steering biases decode, every bout's verdict comes
from the silent-expert shelf (citation_lint, violation_ratchet,
workflow_gate scenarios, census patrol, verkle verifier, water_graph), the
QUEEN weld is the context-pack cross-attention mount, and the Elo ladder
ranks lanes by won bouts, not token spend (QUEEN receipt S4). The gap
between tonight and that league is not research; it is wiring, which is the
dogfood lens's whole point.

## Blind spots (honest)

- I did not read flash_call's internals (mag/lane_runner.py:684 confirmed
  to exist only) or the d13 lane files' contents; the scorer leg's real
  cost and the d13 run's exact mechanics belong to the economics and
  operations lenses.
- I did not fetch the QUEEN paper myself; the receipt's numbers ride on the
  accuracy lens's arXiv fetch (arXiv 2610.03695 per its F1).
- I did not run citation_lint on fixtures tonight, so the door's reward
  oracle is byte-verified to exist but not yet measured for the
  determinism premise; that measurement is the door's first step.
- I did not read the knowledge_graph node or forget-events row for
  selfplay_orchestrator, only confirmed they exist (rg -l).
- Whether memory/runs/selfplay/evidence_latest.json was written by the
  d13 probe or by hand I did not determine; the ops lens's
  last-write-wins finding covers the mechanism either way.
