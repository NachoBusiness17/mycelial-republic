# LM2 — mountain_reveal: DFHack overlay for the Mountain, closed (2026-09-30)

Lane origin: wave-3 last-mile refire, killed by a 1302 at 02:12Z
(`AH_REFIRE_QUEUE.md`). The tool landed anyway (commit 066ba7ef0) and the
orchestrator repaired its death-glue — the replay anchor fix documented
below. This receipt is LM2's close-out: tests green + design intent filed.
Owner: `tools/mountain_reveal.py` · tests: `tests/test_mountain_reveal.py` ·
venv `.venv/Scripts/python.exe` · $0, stdlib, read-only.

## The design intent (why DFHack)

DFHack's `reveal` shows the hidden map; `prospect` surveys what's in the
stone. The Mountain (server/world.py's board over mag/water_graph physics)
ran in the dark: a client sees its pool, the operator the dashboard, and
NOTHING dumped the whole world from the live board or a replay log. This
tool is that overlay — an operator/agent truth instrument, not a game
surface:

- **reveal** — full dump: nodes (type/elev/volume/steam + derived incident
  pipe stress), pipes (from/to/cap/flow/stress/threshold/fractured/state),
  junction gate readings (rule, inlet states, projected PASS/HOLD verdict),
  waste/boil block. `flow` is a read-only projection of what the pipe
  carries THIS tick (the availability law: closed/fractured/no-head/no-water
  -> 0; siphon primed or primable) — no mutation, no priming side-effects.
- **prospect** — conservation + risk: total water vs the board endowment
  with named **drift**, per-node distribution, fracture-risk ranking (stress
  over the B1 hash band [200, 400], full-bore ticks-to-burst), boil
  capacity (steam condenses at the highest cold node).
- **events N** — last N world events with tick + chain seq (tick rows
  unfold; actions/whispers carry their line).

Sources: default is the offline board (`--ticks N` runs physics forward
first). `--from-replay FILE` chain-verifies first (tamper = exit 2), then
replays through the world's own machinery (`persistence._replay_row`,
byte-equality). `--json` everywhere for machine consumption.

## Drift-honesty law (the point of the tool)

The overlay never invents truth. Three honesty paths, all tested:

1. **Tamper** — chain verify fails -> exit 2, hard refusal.
2. **Physics drift** — a chain-valid log whose tick rows predate current
   physics (e.g. pre-V5 logs whose waste DELETED water) diverges on replay
   -> degrade to `mode: partial`, volumes from the last tick row, stderr
   `PHYSICS DRIFT` banner, exit 0. Prospect then NAMES the theft: the
   pre-V5 fixture reads `drift: -8` (the full endowment vanished).
3. **Unanchored tail** — seq starts mid-history with no snapshot anchor ->
   partial, honestly labeled.

Derived numbers are labeled as derived: node `stress` is the sum of
incident pipe load (the engine loads pipes, not nodes); gated-junction
outflow carries `waits_gate: true` rather than guessing the verdict.

## The repaired death-glue (why the lane's tool almost didn't run)

`_anchor_replay`'s anchor: `persistence._apply_graph_spec` restored only
open/primed, DROPPING the spec's stress/fractured — so an anchored replay
with accrued load byte-diverged at the next snapshot row (the gap also
reddening tests/test_server_persist.py at HEAD). The repair adopts the
spec's stress/fractured after applying it (LW5 roundtrip law). Proof:
`test_replay_anchor_restores_pipe_stress` — save_interval=1 log, two
unsaved post-anchor ticks, replay byte-clean, pipe stress/fractured exact.

## Test evidence (2026-09-30T20:47Z, byte-run)

`pytest tests/test_mountain_reveal.py` — **17 passed in 1.00s**, zero
skips. Coverage per the mission:

- reveal/prospect/events on the default board (offline, tick 0 and
  ticked; numbers asserted against a reference `MountainWorld`'s own
  state, never hand-copied — `test_reveal_offline_ticks_match_engine_truth`,
  `test_prospect_fracture_risk_ranking`)
- json mode (every payload test) + text render smoke (all three banners)
- drift-honesty (tamper exit 2; pre-V5 drift -8 named; partial modes)
- replay roundtrip, snapshot anchor shortening, anchor stress restore
- CLI guard: `--ticks` with `--from-replay` rejected

Historical note baked into the tests: the seam LM2 originally flagged —
gated inlets never stressed — was closed by B1 (receipt
`B1_FRACTURE_REACH.md`); `test_node_stress_is_incident_pipe_load` asserts
the closed law (3 ticks -> p_spring AND p_drain at stress 3).

## Verdict

Lane was killed by a 1302, not by design failure. The tool delivers the
intent: whole-world truth, chain-verified replays, honest degradation, $0
read-only. LM2 CLOSED.
