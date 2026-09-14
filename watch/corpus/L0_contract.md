# L0 Universal Game Contract (SELF-BUILT-CORPUS)

STATUS: SELF-BUILT-CORPUS (fallback draft; not builder-original)
SCHEMA: l0_contract.v1
ROLE: W1 insurance — L0 static contract for the gauntlet.

## 1. Core Six Functions

A conformant game MUST expose exactly six functions:

1. `setup(seed, players, opts) -> GameState`
   - Deterministic given seed, players, opts.
   - Initializes RNG from seed (sec 2), deals/initializes state.
2. `turn(state, actor) -> nextState`
   - Advances turn to the given actor; validates actor is legal for current phase.
3. `move(state, actor, action) -> nextState | ERROR(code)`
   - Applies a single legal action by actor. Rejects illegal actions.
4. `legal(state, actor) -> [action]`
   - Enumerates all legal actions for actor in current state. Empty iff actor has no legal action.
5. `evaluate(state) -> VERDICT`
   - Assesses terminal state -> {PASS, FAIL, TIE} + reason code (sec 4).
6. `render(state) -> View`
   - Produces the public observable view (no hidden info unless spec allows).

Invariants:
- All six are pure: same inputs -> same outputs.
- `legal(state, actor)` is authoritative; `move` MUST reject any action not returned by `legal`.
- No function has side effects or depends on wall-clock time.

## 2. RNG Protocol (seeded, auditable)

- RNG = deterministic PRNG keyed by a seed (integer or byte string).
- `seed` is fixed at `setup` and never mutated during a run.
- Every random draw advances a single monotonic stream `S`:
  - `rand(stream) -> value`; stream index `i` is the number of prior draws.
  - Reproducibility: same seed + same action history => same stream of draws.
- Audit: any verifier can replay the full game given `seed` + action log
  (each `move` records the stream index consumed and held values).
- Divergence from the committed stream => FAIL(code RNG_DIVERGE).
- No cryptographic RNG required; the contract only requires determinism + replay audit.

## 3. Verifier Vocabulary

Verdict type: `{result, reason_code, detail?}`

- `PASS` — actor met the win condition (or contract requirement satisfied).
- `FAIL` — actor violated a rule or failed to meet the requirement on a terminal state.
- `TIE` — terminal state with no unique winner / no applicable judgment.

### Reason codes
- `RNG_DIVERGE` — replay stream did not match committed draws.
- `ILLEGAL_MOVE` — `move` accepted an action outside `legal`.
- `ILLEGAL_TURN` — `turn`/`move` acted out of legal turn order.
- `WIN_CONDITION` — PASS: win condition met.
- `VIOLATION` — FAIL: explicit rule broken (see contract-specific codes).
- `STALEMATE_TIE` — TIE: no legal action for any actor and no win.
- `PROVISIONAL` — state non-terminal; evaluate called early (verifier flags as inconclusive).

Convention: contract-specific reason codes extend this base set. All codes are
stable strings; `detail` is optional structured data (never freeform prose).

## 4. Contract Extensibility

- L1/L2 games are written as L0 instantiations: same six functions, game-specific
  `reason_code` additions, game-specific render view.
- A verifier that enforces L0 shapes can enforce any L1/L2 built on these six
  functions without new tooling for the skeleton.
