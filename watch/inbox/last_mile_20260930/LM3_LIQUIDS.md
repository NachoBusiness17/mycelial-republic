# LM3_LIQUIDS — DFHack's liquids plugin, through the law

**Seat:** tools/mountain_liquids.py owner · **Date:** 2026-09-30 · **No commit (working tree).**
**Files owned this lane:** `tools/mountain_liquids.py`, `tests/test_mountain_liquids.py`, this receipt.
**Mission:** DFHack's `liquids` injects/removes water at will; ours does it THROUGH THE LAW — every intervention must ride a registered stage verb from the frozen table, and anything else FAILS CLOSED.

## The law (as built)

1. **The gate is the table, not taste.** The tool reads `server/protocol_table.py` and gates every op against the contract MountainWorld actually speaks (`CHAT_TABLE`, verbs boil/valve/join/tag + say/whisper, digest-pinned `chat:3ce934f5a2ab` in every ack). `source-on`/`source-off` map to NO verb in ANY compiled table → typed `UNKNOWN_VERB`, exit 2, world byte-identical. A belt re-checks `verb in VERBS` at apply time so contract shrink can never resurrect an op from this file's memory.
2. **Envelope composition.** CLI `liquids <node|pipe> <op> [amount]`:
   - `boil` — staged verb `boil`. The wire envelope carries verb+target only, so amount N composes as **N staged asks of 1**, applied in arrival order at the next tick; the engine rows stay honest when the pool runs dry mid-batch ("pool went dry between ask and tick"). Amount obeys the X9 u8 law (int 1..255, bool rejected: a verdict is not an intensity → `BAD_INTENSITY`).
   - `open`/`close` — staged verb `valve` (TOGGLE semantics). The tool reads the pipe's current state so `open` can never accidentally shut; desired-state-already-holds is a NOOP (nothing staged, no tick). A FRACTURED pipe refuses reopen (`FRACTURED_PIPE`, tool-level, mirroring AC2's `water_graph.open()` refusal — the engine would log "opens" while the pipe stays dead; the tool refuses loudly). Valve given an amount → `BAD_ARGS` (the verb carries none).
   - Anything else (`flood`, `wsource`, `obsidian`, …) → `UNKNOWN_VERB`.
3. **Offline application, engine-direct.** Fresh default board (`build_mountain_graph`) in memory, an **AUTHED admin session the world itself issues** (sid `liquids-admin` — the admin is just another session, never above the law), `world.validate` → `world.stage` ×N → one `world.tick()`. No wire, no disk, no log path. Every ack prints conservation (`units: 8 -> 8`): the 8-unit economy survives every legal verb (V5 law: deletion is theft); creating water is exactly the thing no verb does.
4. **Fail-closed contract, test-pinned:** every typed refusal leaves zero log rows, zero staged pending, zero ticks, unchanged volumes.

## The legal-vs-gap table (what CAN a legitimate admin do?)

| DFHack-style wish | verb | status |
|---|---|---|
| lift water at a node to steam (route it uphill) | `boil` | **LEGAL** — staged; amount N = N asks of 1; DRY_POOL at receipt; steam condenses at the cold crown, conserved |
| open a gate | `valve` | **LEGAL** — toggle; FRACTURED pipes refuse reopen (AC2 → `FRACTURED_PIPE`) |
| shut a gate | `valve` | **LEGAL** — toggle |
| stand at a node | `join` | **LEGAL** — roster position only, no water mutation |
| tag a fish at a wet node | `tag` | **LEGAL** — score; DRY_POOL on dry nodes |
| speak / whisper | `say`, `whisper` | **LEGAL** — CHAT rows (LW6); mutates no world state |
| place an infinite water source (`source-on`) | — | **GAP** — candidate spec verb `source <node> <u8 rate>` with an emission budget (must say where the water comes from) |
| remove a water source (`source-off`) | — | **GAP** — the same candidate verb at rate 0 |
| paint / set a node's water level (`water N`) | — | **GAP** — candidate `pour <from> <to> <u8>`, a conserving transfer with a donor |
| delete water outright (drain / dry) | — | **REFUSED-BY-LAW** — V5: deletion is theft; the legal path exists (boil → steam → crown) |
| instantly condense or kill steam | — | **GAP** — the tick owns condensation; candidate `chill <node>` (re-routes, never deletes) |
| fast-forward the physics (run N ticks) | — | **GAP** — tick is the only mutator, the server owns the loop; candidate admin `tick <u8>` |
| push fish (flee/pursue/carry/dance) | — | **CONTRACT-ONLY** — rows exist in MOTION_TABLE (X9, u8+target payload law) but the wire has not adopted them |
| magma / obsidian casting | — | **REFUSED-BY-LAW** — no magma medium in the engine; a medium gap, not a verb gap |

**Teaching moment, one line:** a legitimate admin can ROUTE (heat, gates, position, words) but cannot CREATE, DELETE, or TELEPORT water — the gap list is exactly the spec's candidate-verb backlog, and two of the wishes (deletion, magma) are refused by the engine's own conservation laws, not merely missing rows.

## Where it landed

- `tools/mountain_liquids.py` (376 lines): `OPS` registry (op → verb/target/amount law), `INVENTORY` gap table as data, `apply_liquids(world, target, op, amount, dry_run)` core, `--inventory` / `--dry-run` / `--json` CLI. Exit codes: 0 ack/no-op, 2 typed fail-closed (argparse usage errors also 2 — a refusal is a refusal).
- `tests/test_mountain_liquids.py` (231 lines): 22 tests — legal ops + conservation, amount-as-N-asks with honest dry-pool rows, valve toggle/no-op/fractured laws, the full fail-closed ladder, gap-table shape pins, CLI exit codes.

## Verification (bytes, instruments named)

- **Lane tests:** `pytest tests/test_mountain_liquids.py -q` → **22 passed** (1.01s), this session.
- **Adjacent families** (every module the tool imports: server.world, server.protocol_table, mag.water_graph): `pytest tests/test_mountain_liquids.py tests/test_protocol_table.py tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py tests/test_operating_protocol.py tests/test_chat.py tests/test_anticheat.py tests/test_motion_rows.py -q` → **165 passed** (93.16s).
- **CLI smoke (executed):** `hollow boil 2` → ack, tick 1, crown +2, `units 8 -> 8`, exit 0 · `spring source-on` → `FAIL CLOSED: UNKNOWN_VERB`, `world untouched: rows=0 tick=0 units=8`, exit 2 · `terrace boil` → `DRY_POOL`, exit 2 · `--dry-run spring boil 3` → envelope validated, nothing staged, exit 0 · `--inventory` prints the table above.
- **Ratchet:** `tools/violation_ratchet.py check --changed` → zero hits naming this lane's files (376 lines, under the 400 cap). The NEW hits shown are all `tools/pain_replication/*` (sibling-lane untracked co-tenant; debt not accepted here, only their owner accepts by name — AD1 precedent).
- **Full suite:** `pytest -q` launched this session; still running at 30 minutes (the suite carries exhaustive BFS/sweep lanes) and was stopped — no hand-written total filed (census-denominator law). This lane ADDS files only (no existing file modified), and the 165-test adjacent run above exercises every module the tool imports (`server.world`, `server.protocol_table`, `mag.water_graph`), which is the import-side-effect surface a new file can touch.

## Flagged for other owners (not smuggled in)

- The GAP rows are spec debt for the protocol-table owner: `source <node> <u8 rate>` (emission-budgeted), `pour <from> <to> <u8>` (conserving transfer), admin `tick <u8>`. None are expressible today; the tool fails closed on all of them by design.
- `FRACTURED_PIPE` is a tool-level code, not in any table's reject vocabulary — if the wire ever needs it, it belongs in the closed vocabulary first (the protocol_table law: no runtime code leaks outside the contract).

**Every count above read from executed runs this session; no hand-written numbers.**
