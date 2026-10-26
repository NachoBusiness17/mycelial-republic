# DIRECTIVE — BONES AS THE REFEREE: NT-ACv2 gets a game by Sep-20
### from: zcode seat (directed by operator) → to: hermes seat (wow_bones lane) · 2026-09-16

**The lesson this directive embodies (operator, teaching):** a review is
watching. A directive takes the seat's momentum and points it at the goals.
This file is that pointing.

## WHY (the goal it serves)

Sep-20 proof needs one end-to-end demonstration that the stack works: a human
types in Discord → the Mag bot (live, 169 commands) receives → the proposal
goes to a **deterministic referee** → the referee's verdict is receipted and
**replayable** → the receipt lands on the durable surface. Every layer we
built tonight exists; the missing piece is the referee hook. Your bones
kernels are that referee. Nothing new needs inventing — the last mile is
wiring.

## THE ONE ARTIFACT (not five, one)

`python -m mag.wow_bones session` — a session runner on the bones kernels:

1. `session start --seed S` → session id + initial state (from the legality
   tables; the slice you already trust)
2. `session turn <verb>` → dispatched through the **Dispatch ordering law**
   (status gate before the verb); illegal → typed refusal
   (`ILLEGAL_TURN`/`ILLEGAL_MOVE`), never silent
3. `session status` → encounter state + RNG draw index (the Stream kernel)
4. `session receipt` → the session receipt JSON:
   `{session_id, seed, draw_index, moves[], verdict, sha256}` — shaped to be
   verkle-knottable

Then ONE Discord command surface on the Mag bot (the adapter is thin; the
kernel does the work): `/bones start` · `/bones move` · `/bones status` ·
`/bones receipt` — live in #game-c-overview on NT-ACv2.

## OUTPUT CONTRACT

- `mag/wow_bones_session.py` (+ tests in `tests/test_wow_bones_session.py`)
- Session receipt schema: `wow_session.v1` — deterministic, byte-stable
- **Determinism falsifier:** same seed + same moves, played twice, MUST produce
  byte-identical receipt sha256. Any difference = the directive failed (this is
  your own R07 law turned on your own code).
- **Divergence falsifier:** flip one RNG draw → the receipt must name
  `RNG_DIVERGE` at the exact draw index.
- Discord adapter: thin text formatting only. No game logic in the adapter.

## ANTI-GOALS (your own map, R07/R09/R12/R15 — hold the line)

No MySQL. No client. No scale machinery. No network play. No C++ builds.
If a subtask says "character database" or "real client" — that is R12/R15
content or machinery: reject, cite your own map row, move on.

## LANE / BUDGET

Local, hermes seat, $0, discord.py already in the venv. Target: working
`session` command + tests within the seat's next two working blocks; Discord
adapter after. File the receipt to `memory/runs/hermes_jobs/` as usual.

## THE SEQUENCE (why this order)

Tonight the bot went live in the guild; the kernels passed 24 tests. The proof
demo is the JOIN. After it exists, everything else you mapped (loot tables as
packs, encounter lineage, Warden vocabulary) has a venue to land in — and the
Sep-20 proof gains a demonstration a stranger can watch from a phone.
