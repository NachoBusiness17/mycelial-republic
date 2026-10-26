# MOONSHOT LENS: the operator's founding thesis (Stockfish in charge of coding), 2026-10-06

Lens: moonshot-2. Topic: encode ONE estate programming-problem class as a chess/go-shaped
search space a silent expert engine can dominate, then port the wins back through an
explain layer. Everything below cites bytes I read or commands I ran this sitting
(moment 2026-10-06 ~19:30-20:05Z, working tree branch mag/run-beta1-factory-build-audi-20260806T231709Z).

## THE ENCODING MAP (the ractor answer, one class)

Class: dispatch/route selection (the driving ladder), the one estate problem class where a
silent expert already exists in measured, closed-form bytes.

- Board: one episode = (task queue with typed asks, L lanes with rolling-limit state, clock,
  budget). Finite, discrete, small: the measured envelope tables bound it (width 10 = 109.4M
  tok/h, no surfaced 1302s, per AGENTS.md fan-out width law).
- Moves: assign next ask to a lane, hold, or spawn/retire a server. Move space grows one axis
  at a time: route -> order -> concurrency.
- Reward: banked verified outcome (bouts over real problems is byte-real, tools/dungeon.py:5-6)
  minus USD cost minus 1302-storm penalty. Deterministic scoring from the cost tables.
- Silent expert: expectimax/greedy over the measured cost tables (B2-443 census, driving
  ladder receipts). O(1) per position, deterministic, dominates LM guessing by construction.
  This is the AlphaDev shape: I verified this sitting via web search that AlphaDev (Nature,
  June 2023) treats code optimization as a single-player AssemblyGame with MCTS and landed
  the result in LLVM libc++ (first change to that sort in a decade). The thesis has a
  production-landed precedent; the door is scale of the game abstraction, not its invention.
- Explain layer: the local actor (llama.cpp bridge, RX 5600 XT rung per
  configs/lane_profiles.yaml) renders the expert's plan as lane asks; QUEEN's Bellman analog
  = analyze positions after top candidate routes, consolidate, distill into a janitor prompt
  row (QUEEN receipt S3, watch/inbox/QUEEN_CHESS_LM_20261006.md:29).
- Port layer: the effect broker authorizes the dispatch (model text proposes, broker
  executes, mag/effect_broker.py:1-12); league/ranking state lives in the existing
  arena_learning organ (mag/arena_learning.py:9-14).

## THE 10x VERSION

The whole harness as a self-play league: MIRA-AC allocation picks the asks, the QUEEN weld
(silent expert + speaker) plays the dispatch game, token cues steer the free-lane fleet as
the population, arena_learning ranks by won bouts. The estate owns every organ already; what
is missing is the weld and the wiring, not the parts.

## FINDINGS (each: evidence I checked, falsifier, one-sitting move)

### M1: The estate's only self-play organ inverts the thesis in its reward channel

The "silent expert" leg of imp002 is a remote LM rater, not a deterministic engine.
mag/selfplay_orchestrator.py:157-168 builds a scorer_prompt asking a free-lane LLM
"Rate 0.0-1.0: is the answer correct and complete"; :173 parses that LM text as the reward;
:179 feeds it to the Elo update (`reward if correct else 0.0`). Meanwhile a deterministic
ground-truth checker exists in the same file (:270-278 `_check_answer`) and is used only for
the correct flag. QUEEN's whole mechanism is the opposite: the expert is silent, deterministic,
and plays; the LM explains. As banked (commit 158952f4e), the reward channel is LM opinion
gated by determinism, and the LM opinion adds nothing the gate does not already know.
Falsifier: if a re-run shows the LM rater's score carries measured signal beyond the binary
checker (e.g. partial credit that predicts Elo trajectory), the inversion claim weakens to
"redundant"; as the code stands, the checker fully determines the Elo feed's gate.
Move (~30 min): feed Elo from `_check_answer` only, demote the LM rater to the explain layer,
re-run the 8-problem session, bank the delta. CONVERGENT in spirit with operations F2 (fallback
blindness) but distinct: ops found the dead-scorer path is indistinguishable from live; I found
the LIVE path itself is thesis-inverted.

### M2: The league the thesis needs is a one-game stadium, and its one player repeats an illegal move

Commands run this sitting: `grep -o '"event": "[a-z_]*"' memory/runs/arena_learning_trail.jsonl
| sort | uniq -c` returns 49 illegal_move + 1 game_end; `grep -o '"kind": "[a-z_]*"'
memory/training/arena_profiles.jsonl | sort | uniq -c` returns 300 move + 1 game; illegal:true
count 49. The league snapshot the surfaces read, memory/training/arena_league.json (read this
sitting), is stamped 2026-08-06 with every ranking row at games:0, yet mag/switchboard.py:381-391
embeds it and mag/nervous_system.py:215 consumes its routing_hint. The last 3 trail rows are the
same move "Qh5" from model qwen-desk across 3 different game_ids (2026-10-05). So: two months
of league life, one completed game, 49 illegal moves, a stale ranking surface feeding the
switchboard, and the estate's chess actor cannot produce legality. This is the thesis's best
proof-of-need, already banked in estate bytes: the actor needs the silent expert for the FIRST
duty of any encoder, the legal-move mask.
Falsifier: a league snapshot newer than 2026-08-06 with games>0 rows, or a legal-move masking
layer already present in mag/agent_arena.py (I did not read that file in full; ops F5 cites it
as the seat-vs-seat surface), kills the finding.
Move (~45 min): insert a python-chess legal-move filter between actor and board on the arena
path, run one bout, bank the illegal-rate delta. That is the minimal QUEEN weld in estate bytes:
deterministic engine supplies legality, the model chooses among legal moves, the ladder measures.

### M3: The door is already converged (ops F5 + logic L5); the moonshot adds the scaling axis and the wall-clock kill gate

The 3-move d13 dispatch game (spawn+query vs in-process vs fallback, measured reward table,
exhaustive search) is the right first encoding and two sibling lenses independently landed on
it; per the duplication law it outranks any novel alternative I could propose. The moonshot
additions: (a) grow the move space one axis at a time (route -> order -> concurrency) so the
same encoding class scales without a rewrite; (b) state the wall-clock kill gate per class:
the thesis survives only over classes whose position evaluation is closed-form or O(1)-ish.
Dispatch qualifies (measured tables). Patch sequencing does not on this hardware: one pytest
run per position, times ~N positions, times 7 Bellman iterations, exceeds one night on the
RX 5600 XT + free-lane estate, while QUEEN's 900 Elo came from 7 iterations over
millisecond-eval chess positions (QUEEN receipt :13-15, the paper's own numbers, not
re-measured). Open-ended code generation has no board at all.
Falsifier: time one position eval per class tonight; if a dispatch eval is not orders of
magnitude cheaper than a test-suite eval, my cost model is wrong.
Move (endorse ops F5's ~60 min move, plus ~10 min): run the 3-move game, then add the
eval-cost-per-class row to the door card as the admission test for any future class.

### M4: The receipt's prior-art row names two phantom laws; the bytes exist under other names

My census this sitting (instrument: `grep -rli` over memory/rib/ + corpus/, moment ~19:5xZ,
scope named per the quantifier law): "gladiator" hits only corpus/library/mod-playerbots game
SQL/cpp (NPC broadcast text); "magnetic" hits only memory/rib/RIB_MOSAIC_SEED_20260921.md and
library course files; no rib carries the gladiator stakes law or magnetic-field doctrine under
those names. CONVERGENT x2 with logic L4 and accuracy F5 (theirs ran earlier today, same
absences). But the CONCEPTS are byte-real: tools/dungeon.py:5-6 names gladiatorial bouts over
real problems and :12-15 carries the dice law (chain-tipped sha256, roll committed before the
actor speaks, actors never see it), which is exactly a silent expert supplying stochasticity.
Move (~10 min): amend watch/inbox/QUEEN_CHESS_LM_20261006.md:23 to cite tools/dungeon.py:12-15
as the prior-art bytes instead of the phantom law names.

### M5: The estate already extracted a game engine's bones once and never pointed the pattern at this thesis

Byte-real: docs/ref/WOW_ACORE_STEAL_MAP_20260915.md (13,574 bytes, 2026-09-15) states the
method ("you do not map 10,409 files. You map the six L0 slots") and mag/wow_bones.py:1-8 is
the extraction ("take the BONES of AzerothCore out of the C++ and make them runnable +
testable"). The corpus library also vendors mod-playerbots (corpus/library/mod-playerbots/,
full game-AI framework tree listed this sitting). The moonshot: run the same six-slot
extraction on a chess/go engine so the silent expert becomes a vendored, testable, runnable
organ (the wow_bones pattern), not an API dependency; encode the dispatch board against it.
The two halves (engine-bones extraction, chess-encoding thesis) sit in one repo, unjoined.
Falsifier: if a chess engine extraction already exists under another name, the finding dies;
my search was scoped (grep for engine extraction named in AGENTS.md organs + the WOW map), not
a full-tree census.
Move (~50 min, next sitting): write the six-slot extraction card for a small chess engine
(python-chess + a compact UCI engine), one slot per organ, with the M2 legal-move masker as
slot one.

## KILL CRITERION (the whole door)

The door dies for a class when eval_cost_per_position x positions_per_iteration x 7 exceeds
one night of estate compute, or when the exhaustive search's pick fails to beat the route
actually taken on the same measured reward table (the d13 game already has a known answer to
beat: the lane took the dead-endpoint path, ops F1/logic L2). Verdict grammar per logic L5:
that is ROUTE_DEAD for the class, a verdict not a failure; re-encode the next class or wait.

## BLIND SPOTS (honest)

- I did not read mag/agent_arena.py in full (the arena bout runner); M2's falsifier names what
  there could kill it. I did not re-run any pytest this sitting; all test numbers cited are the
  receipts' own (imp002.md:26-29) and flagged as such.
- The QUEEN 900-Elo numbers are the paper's abstract claims transcribed through the receipt
  (watch/inbox/QUEEN_CHESS_LM_20261006.md:36 says so itself); arXiv id and repo remain OWED.
- The AlphaDev verification is a web-search summary this sitting, not a Nature page fetch;
  secondary-source confidence only.
- I did not measure a real dispatch eval cost (the M3 falsifier is proposed, not run); the
  wall-clock gate is arithmetic from the measured tables, not a timing run.
- The steps.jsonl denominator question (logic L3: 109 rows vs MIRA's ~37k claim) I did not
  re-derive; I inherit the two-lens convergence and did not check a third path.
- I did not inspect the mod-playerbots AI module internals; M5's "game-AI framework" reads its
  top-level tree only.

## REVISED ON HOSTILE SECOND PASS (2026-10-06, this lens re-verified every claim itself)

### M2 REVISED. Withdrawn: the mask move, the stale-surface framing, "one-game stadium". Sharpened: legality is built and non-binding, and the chess league has ZERO completed games

My own re-checks this pass (all commands rerun, not inherited from the verdict): sed of
mag/agent_arena.py:200-240 shows apply_move validates `mv not in board.legal_moves` and
records the illegal row via arena_learning; sed of :315-330 and :385-395 shows
_llm_pick_move builds the prompt WITH "Legal moves (SAN): ..." plus "Pick EXACTLY ONE move
from the legal list." and :369 calls chat(..., temperature=0.2), :404 wires it into
actor_move before apply_move. So the critique is right: a legal-move filter is a NO-OP move,
the layer exists twice (post-hoc rejection + prompt context). sed of mag/arena_learning.py:289-297
shows league_snapshot short-circuits to the on-disk JSON whenever data.game matches and
rankings is non-empty: the August snapshot serving games:0 rows is BY DESIGN, not drift.
The game row grep: the only game_end (probe-f56baf358c, 2026-08-05, moves:10) has profile
row game "TicTacToe-v0" in memory/training/arena_profiles.jsonl, so the chess league has
ZERO completed games; and grep -c 'Qh5' on the trail returns 49: EVERY recorded chess move
attempt in the arena's life is the identical illegal queen move. Sharpened core: the silent
expert's first duty (legality) is byte-real, served in the actor's own prompt, and 49/49
ignored; context is present and non-binding, which is the precise gap QUEEN's
cross-attention-into-encoder-representations closes. Corrected move (~40 min): no new mask;
run one bout with index-pick over the served legal list (or rejection-retry from the echo),
add a prompt hash per trail row, and bank the first COMPLETED chess game plus the
illegal-rate delta. Tightened falsifiers: (1) if the rows' probe_type/ocean fields prove a
bypass of _llm_pick_move's context, this downgrades to a wiring bug (the trail records no
per-row prompt hash today, which is itself the fix); (2) if a constrained-choice run still
cannot finish one chess game, the actor is unusable at any legality layer and the league's
population premise dies.

### M4 REVISED. Withdrawn: the "phantom laws" existence claim and the CONVERGENT x2 flag. Kept narrow: the receipt's named prior-art row is uncitable as named, and my original byte range was wrong

I re-read watch/inbox/ractor_engine/2026-10-06-stockfish-coding/accuracy.md this pass: its
F5 was REVISED on its own hostile pass ("all six named laws are byte-real; the gaps were
lens scope and instrument truncation"), so my convergence partner reversed before I banked
and the x2 flag is retracted per the duplication law. I re-read
memory/steal/STEAL_STOCHASTIC_DETERMINISTIC_20260814.md:10-18 myself: the magnetic row is
byte-real at :14 ("game.html FIELD / flock steal 2026-08-14: magnetic microbots, not
individually commanded") plus the party_subchain invariant quoted at :11, which is the
deterministic-field-steers-stochastic-seats doctrine; my census missed it because I scoped
to memory/rib + corpus and memory/steal was outside. git grep -l "gladiator stakes" over
tracked files returns exactly one file (the QUEEN receipt itself) and grep -c over
memory/law/registry.json returns 0: the NAMED row resolves nowhere, which survives. And my
own cat -n re-read of tools/dungeon.py:5-16 confirms the dice law is :9-11 and my original
":12-15" cite was wrong (that range is golden vectors :12-13 and quirks :14+). Kept move,
corrected ranges (~10 min): amend watch/inbox/QUEEN_CHESS_LM_20261006.md:23 to cite
tools/dungeon.py:9-11 (dice law), :5-6 (bouts over real problems), and
memory/steal/STEAL_STOCHASTIC_DETERMINISTIC_20260814.md:14 (magnetic doctrine row).
