# LM5_LEGENDS — Legends Mode for the Mountain, landed

**Seat:** `tools/mountain_legends.py` + this receipt · **Date:** 2026-09-30 · **No commit (working tree).**
**Spec source:** operator mission (DFHack style): Dwarf Fortress legends mode renders world history as a browsable chronicle; ours renders the Mountain's hash-chained replay log (`server/world.py` JSONL) as markdown with epochs, notables, per-node sagas, an ASCII timeline, and chain verification while rendering.

## What was built

`tools/mountain_legends.py` (397 lines, stdlib + `server.world` imports only):

- `replay PATH` — renders an existing hash-chained JSONL; chain verified row by row WHILE rendering: seq strictly increments, prev links, `sha` = sha256 of the row minus its own sha (reuses `server.world.row_sha`/`GENESIS`, no reimplementation).
- `run --ticks N [--actors demo] [--log PATH]` — renders a fresh run on the default mountain board (`MountainWorld`), optionally persisting the chain (`--log` appends; an existing file is continued, never truncated).
- **Epochs** (phase transitions of the water economy): First Boil, The Rupture (first fracture), Siphon Wakes/Breaks, First Verdict (first XOR resolution), First Rain (condensation), The Starving, The Crown Drinks (first crown fill), The Crowning (WIN), The Spring Fails, The Still World (quiescence). "never: ..." rows are honest — an epoch that never fired is rendered as never, with its reason.
- **Notables:** every fracture with its stress count, siphon breaks, starvations, firsts (first XOR pass, first rain), verbs, whispers.
- **Sagas:** per node — first water, peak+tick, final, net gains; the COLD crown gets its own verse (no outlet, every gain forever, crowning tick).
- **Timeline:** ASCII, bands of ticks; digits = max units of water per band per node, a SUM lane (the conservation story), an epochs marker row (letters, drift right on collision).
- **Stats:** rows by kind, ticks, events by type (regex classifier over the exact event grammar of `mag/water_graph.py` + action echoes that ride inside tick event lists), water ledger.
- **Forged history:** any break (seq gap / prev mismatch / sha mismatch) or unparseable line → `FORGED HISTORY DETECTED` naming the row and the why, chronicle stamped untrusted, **exit 2** (the gate convention). Exit 0 = verified.

## The chronicle of the default board, 500 ticks (the mission ask, verbatim)

`run --ticks 500` (pure physics, no actors). Chain verified over 500 rows, tip `7fa7480a2825`.

```markdown
## Epochs

| marker | tick | age | what happened | row |
|---|---|---|---|---|
| B | - | The First Boil | never: no hand ever lifted steam | - |
| F | - | The Rupture | never: no fracture event in this history | - |
| P | - | The Siphon Wakes | never: no siphon_prime event in this history | - |
| S | - | The Siphon Breaks | never: no siphon_break event in this history | - |
| X | 1 | The First Verdict | Junction gate1 passes (p_spring sole inlet). | 1 / `218cdfdd03a3` |
| R | - | First Rain | never: no condense event in this history | - |
| V | - | The Starving | never: no starved event in this history | - |
| C | - | The Crown Drinks | never: the crown stayed dry all age | - |
| W | - | The Crowning | never: the win was never reached | - |
| D | 6 | The Spring Fails | spring volume hits 0 at tick 6 | 6 / `98a5b50fcabc` |
| Q | 9 | The Still World | from tick 9 no pipe moves, no gate speaks: quiescence | 9 / `342b811dd554` |

## The Timeline (digits = units of water, max per band)

    +---------+---------+---------+---------+---------+---------+---------+---------+--|
tick1         61        121       181       241       301       361       421       481
spring   500000000000000000000000000000000000000000000000000000000000000000000000000000000000
terrace  000000000000000000000000000000000000000000000000000000000000000000000000000000000000
gate1    000000000000000000000000000000000000000000000000000000000000000000000000000000000000
hollow   210000000000000000000000000000000000000000000000000000000000000000000000000000000000
waste    688888888888888888888888888888888888888888888888888888888888888888888888888888888888
crown    000000000000000000000000000000000000000000000000000000000000000000000000000000000000
SUM      888888888888888888888888888888888888888888888888888888888888888888888888888888888888
epochs   XDQ

## Notable events

- tick 1 [first xor_pass] Junction gate1 passes (p_spring sole inlet).

## Sagas of the nodes

### waste (the drain basin, elev 0)
- first water tick 1; peak 8 at tick 8; final 8; gained 7 over the age
### crown (the COLD crown, elev 14) — the COLD crown's journey
- dry the whole age (no water ever arrived); peak 0; final 0; gained 0 over the age
- the crown drinks steam and keeps it: no outlet, so every gain is forever. never crowned.

## Stats

- rows: 500 total — 500 tick
- ticks chronicled: 500 (tick 1..500)
- events by type: 12 flow, 8 to_waste, 6 xor_pass
- water ledger: 8 units at genesis; final row-sum 8 (deletions are theft; steam in flight is invisible to row sums)
```

(Terrace/gate1/hollow sagas omitted here for space; full text is the tool's stdout. Every epoch that says "never" is the truth: without a hand, water only ever finds waste — the V5 law holds it there, SUM stays 8 all age.)

## The demo saga (same board, `--actors demo`, 500 ticks)

Urist the waste-boiler + Oddam the gate-disputer on a fixed deterministic script (say + valve p_bypass at t1, whisper at t2, boil every second tick). 511 rows, chain verified, tip `180d43e76eca`. Epochs fire: **P** tick 1 (siphon primes), **B** tick 2 (Urist boils waste), **R** tick 2 (first rain on the crown), **C** tick 2 (crown holds 1), **D** tick 3, **S** tick 4 (siphon breaks), **V** tick 5 (gate1 STARVED: 4 pooled units spilled to waste), **W** tick 8 (CROWNED, crown >= 4, sticky), **Q** tick 17 (Still World; all 8 units end at the crown, SUM 8 forever). Fracture honestly never: this board cannot feed any pipe 120+ full-bore ticks inside 500 (the fracture law's coverage lives in `tests/test_water_graph.py`, AD1).

## The real replay file

`replay logs/world_server.jsonl` (the only `*.jsonl` under server-adjacent dirs; 103 rows, pure tick rows): **CHAIN VERIFIED**, tip `dc0fb70a8389`. Epochs: First Verdict tick 1, Spring Fails tick 6, Still World tick 9; rest never. The ledger tells the era: `first-row sum 7, final 0, min 0, max 7` — this log predates the V5 economy law (waste deleted water instead of holding it): the chronicle watches all 8 units vanish from the row sums, which is exactly the theft the V5 law later outlawed. A legends mode that makes the loss visible in one line.

## Forged history detection (closed-corpus law, game form)

Both demos this session, real commands, real output:

- **Edited row:** row seq 50's `nodes.crown` flipped 0 → 3 in a copy → `FORGED HISTORY DETECTED at seq 50: sha mismatch: body does not hash to its seal (row edited after sealing)`, **exit 2**. The forger gave the dry crown a history of water; the chain refused it.
- **Erased row:** seq 30's line deleted from a copy → `FORGED HISTORY DETECTED at seq 31: seq 31 appears where 30 is due`.
- Roundtrip: `run --ticks 60 --actors demo --log` wrote 71 rows; `replay` re-rendered them verified — the persisted chain is byte-true across processes.

## Verification (bytes, instruments named)

- Renders executed this session (instrument: the tool itself, this venv): `run --ticks 500` (exit 0), `run --ticks 500 --actors demo` (exit 0), `replay logs/world_server.jsonl` (exit 0), forged copies (exit 2), roundtrip (exit 0).
- `tools/violation_ratchet.py check --changed`: zero hits on `tools/mountain_legends.py` (the 20 NEW hits are untracked sibling-lane `tools/pain_replication/*` files, debt not accepted here). File is 397 lines, under the 400 cap.
- **Tests, instruments named (all executed this session, this venv, `pytest -q`):**
  - Full suite, 3 attempts, all against the SHARED working tree mid burn-wave: attempt 1 died at ~22% (collection blocked by sibling `tools/mountain_reveal.py` SyntaxError, file still mid-landing, not this lane's); attempt 2 with `--ignore=tests/test_mountain_reveal.py` died at ~23% twice at the SAME spot — `tests/test_doctor_provider_endpoints.py::test_wired_into_examine` starts and never returns (network probe hang, provider keys unfunded per the driving ladder) — no full-suite number is claimable this window.
  - Adjacent families `tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py tests/test_server_v0.py tests/test_server_persist.py` → **48 passed, 7 failed**; `tests/test_gods_number.py` alone → **3 passed, 1 failed** (golden: 135,936 states, pinned 339,840). Every failure names a sibling lane's UNCOMMITTED working-tree change, not this lane: `git status` shows `mag/water_graph.py`, `server/protocol.py`, `server/protocol_table.py` modified and `server/auth_srp6.py` untracked (fracture/starvation/persist tests and the gods-number golden all read the engine those edits are moving). This lane modified NO runtime module: `tools/mountain_legends.py` is new, untracked, imported by zero tests (`grep -rl mountain_legends tests/` → 0), and imports `server.world` read-only.
- My footprint: `git status` shows exactly `?? tools/mountain_legends.py` + `?? watch/inbox/last_mile_20260930/LM5_LEGENDS.md` (this receipt). Nothing else touched.
- No behavior change to any existing module: the tool imports `server.world` (row_sha, GENESIS, MountainWorld) read-only; no source file touched.

**Every count above read from executed runs this session; no hand-written numbers except where a verbatim tool output is quoted.**
