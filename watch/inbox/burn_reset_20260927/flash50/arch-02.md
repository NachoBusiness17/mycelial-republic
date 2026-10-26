# arch-02: Godot port architecture for the water graph (mag/water_graph.py)

- Item: arch-02, flash50 wave, 2026-09-28. Source module: `mag/water_graph.py` (274 lines, read fully this session).
- Grounding: every code claim below cites a line I read this session. Every check reported was executed this session with the repo venv (`.venv/Scripts/python.exe`). Godot-specific machinery (scene tree, signals, shader model) is design, marked as such; no Godot binary exists on this host, so no Godot runtime check was run and none is claimed.
- The ask: read mag/water_graph.py fully; design the Godot port: what maps to GDScript nodes, what maps to signals, what maps to shaders, how a player interacts; bank the architecture.

## 1. What the engine is (receipts)

The water graph is the estate's physics-based computation engine by operator order 2026-09-27: "routing as physics, not a hardcoded pair" (`mag/water_graph.py:1-4`). Its laws, each cited:

- L1 Gravity-only: `head_ok = src.elev > dst.elev` gates every pipe (`mag/water_graph.py:203,223`); check-valve law "never uphill" is the comment at `mag/water_graph.py:233-234`.
- L2 Integer capacity: `flow = min(p.cap, src.volume)` per tick (`mag/water_graph.py:231,235`); integer volumes, no floats, no RNG, insertion-ordered pipes (`mag/water_graph.py:24`).
- L3 Siphon prime-and-break: primes at `crest` volume with head ok (`mag/water_graph.py:206-211,225-230`), breaks when the intake runs dry (`mag/water_graph.py:219-221`). Integerized from `mag/hydro_xor_sim.py:48-50` (SIPHON_RATE/INTAKE_BREAK).
- L4 Hydraulic XOR: a `xor` junction delivers only when EXACTLY one inlet delivered this tick; both inlets is overflow (`mag/water_graph.py:156,165-166`).
- L5 Hydraulic AND: a `sill` junction delivers at `len(inlets) >= max(1, sill)` (`mag/water_graph.py:156-157`); `any` is OR by the same counter (kind list `mag/water_graph.py:39`).
- L6 Steam as a second routing medium: `boil()` lifts volume to steam (`mag/water_graph.py:86-93`); each tick all steam condenses at the HIGHEST `cold` node, ignoring pipes (`mag/water_graph.py:95-105`), else falls back to origin (docstring `mag/water_graph.py:19-22`).
- L7 Starvation law (2026-09-28): under-gate inflow HELDS and pools (`mag/water_graph.py:170-179`); a pool that dies with zero new inflow spills and emits a STARVED line naming node, units, and gate (`mag/water_graph.py:180-186`). Origin: operator, "this whole starve out thing is bullshit and our water computer spec should have picked it up" (`mag/water_graph.py:141-150`).
- L8 Deterministic three-phase tick: condense steam, then plain pipes plus gated-junction inflows deferred uncommitted, then gate evaluation and gated outflow (`mag/water_graph.py:108-196`; the phase split exists because the first cut let gated outflow drain in the same pass, `mag/water_graph.py:110-116`).
- L9 Exact spec roundtrip: `to_spec`/`from_spec` over schema `water_graph.v1` (`mag/water_graph.py:248-274`), pinned by `tests/test_water_graph.py:110-117`.
- L10 Honest waste: a `waste` node swallows flow and reports it; volume never accumulates (`mag/water_graph.py:237-239`).
- L11 Win honesty and proof: graph state persists as a JSON dict in campaign flag `water:graph` (`mag/water_computer.py:42-43,123-132`); every action is load-spec, mutate, save-spec (`mag/water_computer.py:112-120`); the win node's volume mirrors to `water:out` plus the `flowed` flag so the legacy verdict governs (`mag/water_computer.py:307-323`); a win anchors a sha256 proof (claim + spec + final volumes) to the verkle chain, never breaking play on chain failure (`mag/water_computer.py:227-286`, hash at 241-243).
- L12 The room-to-pipe valve contract: `spec["valves"][room_id]`, else the first pipe whose src node is named after the room, else NO valve: "an unmapped room must not grow a surprise valve" (`mag/water_computer.py:170-178`, comment 118-120).

The play surface already exists: `memory/game_modules/water_graph.v1.json` is the Five-Node Graph keep (nodes 31-37: source elev 5 vol 6, reservoir elev 4 vol 2, xor junction elev 2, out elev 1, waste elev 0; pipes 39-43; room valve map 44-49; win_node "out" line 50). The out_cistern room carries the Bucket anti-cheat: "pour bucket to fake a height. That is not computation" (`memory/game_modules/water_graph.v1.json:109-122`), matching "there is no pour API" (`mag/hydro_xor_sim.py:14`).

Live receipts this session (commands in section 9):

- `python -m pytest tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py -q` -> `20 passed in 33.36s`.
- A scripted 3-tick run of the five-node keep plus a cold attic and an uphill siphon printed exactly the event grammar the port must preserve: `main: 1 source->junction.`, `Junction junction passes (main sole inlet).`, `spout: 1 junction->out.`, `Junction junction holds 2 below gate (2 inlets); pooling.`, `Steam condenses at cold_attic (+1).`, and a final `to_spec()` JSON at tick 3 (schema `water_graph.v1`).

## 2. Design axioms for the port

A1 The engine is NOT the scene tree. Godot nodes carry transforms, floats, and draw state. The deterministic integer core ports as pure GDScript `RefCounted` classes (`WaterGraphCore`, `TankData`, `PipeData`) with zero Node ancestry. Rationale: L2 and L8 (determinism) and L9 (exact JSON roundtrip) are the product; scene-tree iteration order and float transforms would poison both. This mirrors the Python split where `water_graph.py` is stdlib-only (`mag/water_graph.py:24-25`).

A2 The spec is the only save format. Godot saves and loads the identical `water_graph.v1` JSON (L9). A campaign seeded by Python (`mag/game_campaign.py:70` routes module_id `water_graph` through `mag.water_computer`; `mag/game_campaign.py:364` notes `water_graph.v1.json` campaigns route through WaterGraph) must play in Godot and vice versa, byte-identical.

A3 Presentation is a pure function of state deltas. Signals fire after commit, in the engine's event order. Shaders and particles never write back. No shader uniform is ever read into state. This is L2 applied to rendering.

A4 Godot's physics engine is not used for the water. Godot physics is float and platform-nondeterministic; the estate's water is mark-based integer physics ("gravity takes a mark each wait", `mag/hydro_xor_sim.py:7-9`). RigidBody fluid sims are decoration at most, never the routing truth.

A5 Insertion order is load-bearing (L8). Godot 4 Dictionaries preserve insertion order, but the port pins this with a determinism test (section 7) rather than trusting it; if any Godot version reorders, the core falls back to an Array-of-names index. Honest note: this Godot behavior is design knowledge, not something verifiable on this host.

## 3. What maps to GDScript nodes

| Python thing (citation) | Godot scene | Notes |
|---|---|---|
| `Node` dataclass, fields name/elev/kind/sill/volume/steam (`mag/water_graph.py:35-42`) | `TankData` (RefCounted, in core) AND a `Tank.tscn` (`Node2D`) visual twin | The core holds truth; the scene holds pixels. The visual reads the core each tick. |
| `Pipe` dataclass, fields name/src/dst/cap/siphon/crest/primed/open (`mag/water_graph.py:45-54`) | `PipeData` (RefCounted) AND a `Pipe.tscn` (`Node2D` with a `Line2D`) | One scene per pipe; the Line2D endpoints derive from the two tanks' positions. |
| `WaterGraph` + `tick()` (`mag/water_graph.py:57-61,108-196`) | `WaterGraphCore.gd` (RefCounted) | Three-phase tick ported line-faithful; returns `Array[String]` events exactly as Python does. No signals inside the core; the world adapter converts events to signals (section 4). |
| `add_node`/`add_pipe` KeyError guard (`mag/water_graph.py:63-77`) | same guard in `WaterGraphCore` | Unknown endpoint stays a hard error; the MUD law "no surprise valve" (L12) generalizes to "no surprise edge". |
| `to_spec`/`from_spec` (`mag/water_graph.py:248-274`) | `WaterGraphCore.to_spec()/from_spec()` over Dictionary | JSON via `JSON.stringify`/`JSON.parse_string`; schema key `water_graph.v1` unchanged. Spec-only keys (`valves`, `win_node`, node `sill`) survive Godot saves the way `_save_graph` overlays them Python-side (`mag/water_computer.py:181-202`). |
| Node kinds `cold` / `waste` (`mag/water_graph.py:39,237-239`) | `ColdTank.tscn` (condensation target glow), `WasteDrain.tscn` (no accumulating gauge) | The engine picks the highest cold node (`mag/water_graph.py:97-99`); the world highlights exactly that tank so the player can see where steam will land. |
| Junction kinds `xor` / `sill` (`mag/water_graph.py:39,151-168`) | `XorJunction.tscn` (two inlet lamps, "exactly one" plate), `SillDam.tscn` (a ruler mark at `sill`) | Gate state renders from the same committed counts the engine used (`mag/water_graph.py:152-158`). |
| Steam per node (`mag/water_graph.py:42,86-93`) | `GPUParticles2D` wisp child on each tank | Particle count scales with the integer `steam` field; it is a gauge, not a simulation. |
| Siphon crest (`mag/water_graph.py:206-211`) | drawn crest arc on the pipe Line2D | The arc's apex height encodes `crest` in marks; primed state animates flow. |
| The glass: `_render_glass` (`mag/water_computer.py:289-296`) | `GlassPanel.tscn` (section 5 shader) plus the same text line in a Label | Text glass and schematic glass render from one `to_spec()` snapshot. |
| Valve map and win node (`mag/water_computer.py:160-166`, json 44-50) | `ValveWheel.tscn` levers placed in room scenes; `win_node` flag on the goal tank | The lever-to-pipe binding is read from the spec at load, never hand-wired in the scene. |
| Campaign room layer (`memory/game_modules/water_graph.v1.json:52-122`) | the keep's walkable rooms (hub gallery + four cisterns) as a 2D side-view map | Room Y derives from the graph elevations (A-section geometry below), so walking west into source_cistern literally walks to elevation 5. |

Geometry rule: world Y = `BASE_Y - elev * MARK_SPACING`, X is a hand-laid DAG layout. Elevation IS visible: a player can read L1 off the screen, because a pipe only ever flows downhill. This makes the check-valve law (`mag/water_graph.py:203,223`) player-legible without a tutorial.

## 4. What maps to signals

Python's tick returns `list[str]` events; live grammar captured this session (section 1). The port converts each event class into a typed signal on `WaterGraphWorld` (the scene root that owns the core), emitted in event order, after commit:

- `flowed(pipe: StringName, units: int, src: StringName, dst: StringName)` from the `"{p.name}: {flow} {src}->{dst}."` events (`mag/water_graph.py:164,242`). Drives drop tweens along the pipe Line2D.
- `gate_passed(junction: StringName, via: StringName)` from "Junction X passes (P sole inlet)." (`mag/water_graph.py:166`) and `gate_opened` from "sill reached (N inlets)." (`mag/water_graph.py:168`).
- `gate_held(junction: StringName, held_units: int, reason: String)` from "holds N below gate (...); pooling." (`mag/water_graph.py:178-179`). HUD shows a pooling indicator on the junction; pooled volume is real state and must be visible (it can still win later, `tests/test_water_graph_starvation.py:54-62`).
- `junction_starved(junction: StringName, spilled: int, reason: String)` from the STARVED line (`mag/water_graph.py:185-186`). First-class alarm: red toast, drain-glug sound, and a run-log entry. This is the sensor the operator demanded (`mag/water_graph.py:141-150`); the sibling bank file `watch/inbox/burn_reset_20260927/flash50/deep-starvation-sensor.md` generalizes it further and records a latent engine double-spend when one source feeds two gated junctions (its section 2, repro in file). Port decision: inherit the Python semantics as-is for parity, and gate any fix behind updating the Python tests first (spec-before-behavior, AGENTS.md build discipline); the Godot core carries the same `# CAVEAT` comment pointing at that finding.
- `siphon_primed(pipe: StringName, crest: int)` and `siphon_broke(pipe: StringName)` from "primes at crest (N)." / "breaks (intake dry)." (`mag/water_graph.py:208,221,228`).
- `steam_condensed(target: StringName, units: int)` from "Steam condenses at X (+N)." (`mag/water_graph.py:103`).
- `waste_received(pipe: StringName, units: int)` from "{p}: {flow} to waste at {dst}." (`mag/water_graph.py:238`).
- `valve_changed(pipe: StringName, is_open: bool)` from `open()/close()` (`mag/water_graph.py:79-83`).
- `tick_completed(n: int, events: Array[String])` after phase 3; the animation queue IS this event list, replayed in order, so even the presentation stays deterministic (A3).
- `won(win_node: StringName, volume: int)` when the win mirror fires (`mag/water_computer.py:316-335`): the legacy verdict `won()` governs graph mode (`mag/water_computer.py:308-310`), and the proof flow (section 6) hangs off this signal.

Conversion rule: the world adapter parses the event strings OR (better) the core is ported to emit structured event dicts from the start, with the Python-side string grammar kept as a rendering of the same dicts. Either way the ORDER is the contract; signals are visuals' only input.

## 5. What maps to shaders

All shaders are canvas_item shaders fed by uniforms set from `to_spec()` each tick. None read back. None accumulate state.

- Tank fill (`TankFillShader`): `fill` uniform = integer volume over a declared gauge max; sine wobble on `TIME` for the surface line; color ramps by kind (cold gets a frost tint, waste renders as an open grate with no fill). The integer boundary matters: fill level is set from an int, never integrated in-shader, so a rewound tick cannot leave residue (A1, L2).
- Pipe flow (`PipeFlowShader`): a scrolling-dashes shader on the Line2D texture; `flowing` and `dir` uniforms set per `flowed` signal; scroll speed proportional to `cap` (L2); siphon pipes add a crest-arc uniform that lights up on `siphon_primed` and dims on `siphon_broke`. Closed valve: speed zero and a wheel overlay.
- Steam (`SteamWispShader` on GPUParticles2D): upward-drifting billboard smoke; altitude fade encodes "rises regardless of pipes" (`mag/water_graph.py:19-22`) as pure visuals; the condensation target gets a rain-drip particle burst on `steam_condensed`.
- Glass panel (`GlassShader`, the `_render_glass` port, `mag/water_computer.py:289-296`): a full-screen overlay drawing the schematic, nodes as boxes stacked by elevation, pipes as lines with open/shut ticks, volumes as segmented integer bars, plus the literal GLASS caption line. Uniforms come from one spec snapshot per tick; this is the honest sight-glass the keep's plaque promises (`memory/game_modules/water_graph.v1.json:66-68`).
- Starve effect (`StarveShader`): on `junction_starved`, the junction desaturates and its pooled bar drains into the waste grate; on `gate_held`, a slow pulse marks pooled water as alive. Two distinct visuals because the engine distinguishes them (`mag/water_graph.py:178-186`).
- Junction gates: XOR plate shader shows inlet lamps lit from the committed inflow count (1 lamp green, 2 lamps red); sill dam shader draws the threshold ruler at `sill` marks and fills to it (`mag/water_graph.py:156-157`).

## 6. How a player interacts

The verbs are the MUD's verbs, made physical:

- Walk the keep. The five rooms of `memory/game_modules/water_graph.v1.json` (gallery hub 53-71, source_cistern 72-84, gallery_reservoir 85-94, work_gallery 95-108, out_cistern 109-122) become a side-view 2D map at elevation bands. Reading the network is walking.
- Turn valves: click a `ValveWheel` or press the interact key at a lever; resolves through the L12 contract (`spec["valves"]` room map, `mag/water_computer.py:170-178`). No lever in a room means no valve, faithfully.
- Wait: Space or a bell-pull advances exactly one tick ("wait = season", the keep doctrine in the fireball-cycle skill; `mag/water_computer.py` routes wait/tick through WaterGraph in graph mode, `mag/water_computer.py:5-9`). The world then replays that tick's event list as animations. Waiting is the turn; the engine does the physics.
- Watch the glass: Tab holds the schematic overlay (section 5). The tank gauges and glass always agree because both render one spec snapshot.
- Boil: at a heat interactable, the boil action calls `boil()` (`mag/water_graph.py:86-93`) on that node. Fireball law (fireball-cycle skill): fire changes phase and creates a tool; here heat is the phase-change tool that loads water onto the steam route to the highest cold room.
- The Bucket stays a cheat: out_cistern holds a bucket item (json 117-119). Picking it up is flavor. Any pour gesture at a tank sets a run-level `disputed` flag and plays the DISPUTED sting; it NEVER writes engine volume. This preserves "output arrives only through pipes; there is no pour API" (`mag/hydro_xor_sim.py:14`) and the win mirror's honesty (`mag/water_computer.py:316-323` only credits `flowed` runs).
- Win: `won` fires when the win node's height is reached by gravity (`mag/water_computer.py:327-328`). The win screen shows the proof payload exactly as `proof_payload` builds it: claim, graph_spec, final volumes (`mag/water_computer.py:209-224`). Chain anchoring stays OUT of the game binary: Godot exports `water_proof.v1` JSON; the Mag side anchors via `anchor_proof` (`mag/water_computer.py:227-286`). Rationale: keep verkle writes on the estate side of the shared-artifact boundary (AGENTS.md inbox contract); the game ships evidence, the harness commits it.
- Persistence: save = campaign flags including the `water:graph` spec (`mag/water_computer.py:135-141`); load = `from_spec`. A run started in the terminal MUD continues in Godot on the same JSON.
- Level editor (stretch): because the spec is the only truth, an editor is a spec editor: drag tanks to elevation bands, wire pipes, toggle siphon/crest/cap, export `water_graph.v1`. The valve map is just naming rooms after pipe srcs or writing `spec["valves"]` (L12). Custom keeps then run in BOTH runtimes with zero engine changes.

Player-facing difficulty comes free from the laws: the demo keep wins by opening main alone (XOR passes one voice; live run tick 1 delivered `spout: 1 junction->out.`) and loses water whenever both voices speak (`holds 2 below gate`, live run tick 2); the sill keeps in `tests/test_water_graph_starvation.py:20-30` teach pooling patience; siphon keeps teach priming cost. No scripted levels needed; the physics IS the puzzle, which is the whole point of "routing as physics" (`mag/water_graph.py:1`).

## 7. Port test contract (what must pass before the port is real)

Mirror the Python suites as GdUnit4/GUT cases, plus one cross-runtime check:

1. Gravity/check-valve, siphon prime-and-break, XOR, steam, determinism, roundtrip: port `tests/test_water_graph.py:28-117` (6 laws) case for case.
2. Pooling, STARVED naming, pool-still-reaches-gate, healthy path: port `tests/test_water_graph_starvation.py:33-69` (4 laws).
3. Campaign plumbing: valve contract, win mirror, spec-only-key overlay: port the operative cases of `tests/test_water_graph_campaign.py` (201 lines, read listing this session; 20 tests across the three files passed in Python at section 1).
4. NEW cross-runtime determinism check (the acceptance gate for A2): run N ticks in Python, dump `to_spec()` JSON; load the same JSON in Godot, run N more ticks, dump; the two runtimes' specs must be byte-identical modulo key order, and the event sequences must match class-for-class. Port of `test_deterministic_same_ticks_same_state` (`tests/test_water_graph.py:96-107`) across runtimes. NOT RUN this session (no Godot on host); it is the first thing the porting seat runs.

## 8. Build order

1. `WaterGraphCore.gd` + `TankData`/`PipeData`, ported line-faithful, with the section 7 Python-mirror tests. No scenes yet.
2. Cross-runtime determinism harness (section 7 item 4) green.
3. `WaterGraphWorld` adapter: spec JSON -> scene tree, event list -> signals, `GlassPanel`.
4. Five-node keep playable: levers, wait bell, glass, win screen with proof export.
5. Steam/boil interactable and a cold attic keep (engine supports it, demo keep does not use cold yet: json nodes 31-37 have no cold node; my live run exercised it).
6. Bucket/DISPUTED flavor layer, then the spec editor.

## 9. Checks run this session (exact commands)

- `python -m pytest tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py -q` -> `20 passed in 33.36s`.
- Live engine run (venv python, inline script): built the five-node keep plus `cold_attic` (elev 7, cold) and siphon `lift` (out->cold_attic, cap 1, crest 2); tick 1 with main open: `main: 1 source->junction.` / `Junction junction passes (main sole inlet).` / `spout: 1 junction->out.`; tick 2 with side also open: `Junction junction holds 2 below gate (2 inlets); pooling.`; tick 3 after `boil('out', 1)`: `Steam condenses at cold_attic (+1).` + the hold line again; final `to_spec()` printed at tick 3, schema `water_graph.v1`.
- `wc -l mag/water_graph.py mag/water_computer.py mag/hydro_xor_sim.py` -> 274 / 880 / 294.
- `git grep -l "water_graph"` (tracked files) -> live readers: `mag/game_campaign.py`, `mag/water_computer.py`, `mag/water_graph.py`, `tests/test_water_graph.py`, `tests/test_water_graph_campaign.py`, `tests/test_water_graph_starvation.py`, plus memory and flash50 bank files (list in session log).
- Read: `mag/water_graph.py` (full), `mag/hydro_xor_sim.py` (full), `mag/water_computer.py` lines 1-340, `tests/test_water_graph.py` (full), `tests/test_water_graph_starvation.py` (full), `memory/game_modules/water_graph.v1.json` (full), heads of `watch/inbox/burn_reset_20260927/flash50/deep-starvation-sensor.md` and `deep-mycelial-routing.md`.
- Em/en dash scan of THIS file: run post-write with the repo venv (result recorded in the commit message; both counts must be 0).

## 10. Limits stated

- No Godot binary on this host: the architecture is design, grounded in the read code; the Godot-side behaviors cited (Dictionary insertion order, GdUnit4) are named as port-time verification targets, not verified facts.
- The sibling-recorded double-spend (`deep-starvation-sensor.md` section 2) is inherited by parity, not fixed here; a fix is a semantic change owned by the Python suite first.
- `mag/water_computer.py` lines 341-880 (play loop, legacy 3-tank mode, proof CLI) were not read this session; the port covers the graph mode the ask names. The legacy mode stays Python-only by design (`mag/water_computer.py:8-9`).
