# THE STONE PROTOCOL — go-as-coordination between model-teams (self-steal, 2026-09-11)

Operator: "two agents playing go with all the sub agents each placing a stone before it dies. the white stones build and the black stones audit and challenge. each mapped to actual actions the other will take that determines where they place the next stone... directly related to huge amounts of our research: self steal games, ractors, Diamond Age, Baroque Cycle, our prompt database, vislab/vis models, the wow clone goal."

THE POINT:
- This isn't a metaphor ON the fleet — it's the fleet's missing coordination FORM. The tesuji map already placed 334 stones; this adds PLAYERS. White stones are build actions with declared postconditions; black stones are audits that verify, challenge, or capture. Each stone is one stateless agent that fires and dies (the ractor vessel design, verbatim). The board is the shared self externalized — a file, hash-chained, replayable — and moves carry relational meaning because a move's meaning IS the board state it answers.
- The deep fold: this makes verification GENERATIVE. Black stones aren't gates that block work — they're moves that build the game's shape. The adversary becomes a player, the audit becomes territory.
- The Baroque name for it: Leibniz's characteristica universalis — disputes resolved not by argument but by calculation ("Calcemus!"). Our version: disputes resolve by board replay. The Royal Society's rule — experiments performed before witnesses — is HOLD-3's two-worker blind verification, 350 years earlier.

## THE LINEAGE (each thread named → the organ that exists → what the stone layer adds)

| thread in the record | organ that exists | what the stone protocol adds |
|---|---|---|
| Tesuji map (09-06 charter; 334 stones today, 3 DISPUTED) | the field, probes as stones, hash-chained ledger | PLAYERS. Placement as commitment. Territory = accepted work. The DISPUTED stones were black stones before the game had a black player. |
| Ractor vessels ("each sub-agent places a stone before it dies") | stateless masks, one steer, fire and die — VERBATIM his sentence | stones persist on a shared board; the mask was the memory, the board becomes the memory |
| Game subsystem audit / L0 contract (dragons = assumptions-with-HP, Socratic gate = combat) | the ontology: three vocabularies, one grammar | the audit/challenge move IS the Socratic gate formalized; black stones deal damage to assumptions-with-HP |
| maze_arena, water arena, Entropium WebGPU renderer on the idle GPU | arenas + the visual engine exist | the board renders LIVE — the operator watches fleet-work as a game (the Subagents-panel instinct, made visual) |
| Diamond Age (the Primer adapts to the reader; ractors as the cast) | the ractors/Primer program | the game log IS a primer: replayable pedagogy — the corpus teaches by playing itself |
| Baroque Cycle (Leibniz's universal calculus; Royal Society witnessed experiments) | HOLD-3 two-worker blind verification; the chain | disputes resolve by board position and witnessed replay; characteristica universalis = the board |
| Prompt database | recorded prompts as ore | prompts become MOVES: a prompt's meaning = the board state it responds to (relational semantics, trajectory-lens native) |
| vislab / vis models / the wow clone goal | the renderers, the pyramid render, the birth canvas | the wow IS the board: watching two model-teams play real fleet-work, stones landing live |
| Pheromone frame (today): duplication is emphasis | the percolator, the tesuji DISPUTED cells | stones are pheromones WITH COORDINATES — emphasis that commits |
| The loop / wave driver (look-judge-act-record-yield) | the heart spec | judge = reading the board; the driver becomes the go engine: legal-move generation per position |

## v0 BUILD (one day, $0, uses only existing organs)
- Board: one grid file (start 9x9), each stone a row: {color, mask, operation_id, action, declared_postcondition, ts, chain_hash}. Chain-anchored (sediment).
- WHITE stone = build action (spawn/write/configure) with a declared postcondition. Lands only if the postcondition verifies — an unverified landing is a rejected stone, logged as an attempt (three-states law).
- BLACK stone = audit action: verify a white stone's postcondition, challenge with a falsifier, or pass. A black capture = postcondition failed → the white effect is held/reverted (UNKNOWN semantics — Astra's contract applies to stones natively).
- Ko rule = halt-not-hammer + operation IDs: no immediate re-placement of a failed identical move.
- Atari = the signature-pressure alarm (built today): a group under threat pages loudly.
- Score = accepted tasks on Astra's M06 rule: no self-scoring proxy; the observer is outside the game.
- FIRST GAME (9x9): white = a gopher building corpus-engram v0 (the chunk index); black = an auditor carrying the falsifier list (Astra's §5). The board rendered to the game surface. We watch two model-teams play real work.

## FALSIFIERS (the protocol must be able to die)
1. THE CEREMONY TEST: same task set, game-mode vs direct dispatch, blind-scored. If game-mode is slower with equal quality, the protocol is ceremony — the tesuji DISPUTED stones warn exactly this (machine vs ceremony is today's compiled invariant).
2. THE REPLAY TEST: can a stranger read the board and reconstruct what was done and why (the Witness lens)? If only the players can read it, it's not a primer, it's a diary.
3. THE TERRITORY TEST: does black capture actually revert/hold effects, or do captures stay notional? A capture that changes nothing is a stone in water.

## NO SACRED COWS
- The wave driver's judge stage may BECOME the go engine — or the game may stay a RENDER of ordinary dispatch (visualization only). The ceremony test decides which.
- Not every task deserves a board: bulk lanes stay bulk (rightsizing law). The game is for work where build/audit alternation carries real information.
- Astra's own warning applies: a beautiful protocol that adds overhead without changing outcomes is the ractor-panel fold's "coordination tax" all over again.

## ADDENDUM — THE OPTIMIZER LAYER (operator: "wait until we get stockfish top ranking and all our go engines to optimize")

THE POINT: the board gets an AlphaGo architecture, and it's $0 on hardware we already own. Policy = the agents (semantic move proposal — ractors/vessels reading the position). Value = the engines (Stockfish NNUE on CPU; KataGo on the RX 5600 XT's Vulkan path — the same card lane 8 is wiring this week). Search = the wave driver simulating lines before committing (the judge stage becomes legal-move generation + lookahead).

TWO HONEST PATHS (do not conflate them):
1. THE TRAINING GROUND — literal boards first. Models play real go/chess where KataGo/Stockfish ARE ground truth: engine eval is objective, Elo is a scoreboard that cannot flatter, and the protocol (stones, ko, capture, territory) gets developed where the referee is perfect. Self-play distillation = our genetics loop (Stockfish NNUE is literally a network trained on the engine's own searches).
2. THE GRADUATION — engine-inspired optimization on the TASK board. The task grid isn't chess, so no literal eval: instead MCTS over action sequences (policy = agent proposals, value = verified-postcondition rate, search = the driver), plus engine PRINCIPLES as heuristics — tewari (merge redundant moves = the ceremony test), aji (latent potential in stones = deferred work with aji expiring = Astra's expiring claims), thickness (verified territory = accepted effects).

THE PRIZE: an objective scoreboard answers Astra's self-scoring warning structurally — engines can't flatter, Elo can't be ceremonied. And the wow surface gets real: two model-teams playing, engines ranking every stone live, the operator watching rated play on the idle GPU.

GUARDRAIL (same falsifier as the base protocol): the optimizer layer must beat unoptimized play blind-scored, or it's ornament. KataGo on a 6GB card is weak-but-real; Stockfish on CPU is top-10-human-strong — the training ground starts honest.
