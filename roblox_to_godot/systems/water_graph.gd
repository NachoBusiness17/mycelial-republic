extends Node
## Water Graph — ported from mag/water_graph.py
## The estate's hydraulic computation engine: gravity-fed directed graph
## with check valves, siphon crests, XOR/SILL junction gates, and steam
## condensation. Deterministic. No floats. No RNG.
##
## Roblox origin: mag/water_graph.py + roblox/src/shared/Flock.luau companion
## Godot idiom: Node-based, signals for events, typed GDScript
##
## FIX 2026-09-29 (zcode-seat): inner data classes were named Node2D and Pipe,
## shadowing Godot's built-in Node2D and clashing with built-in Node in the
## `: Node` annotations inside tick()/boil()/move paths — first tick would
## have crashed with a runtime type-assignment error. Renamed WNode / WPipe
## and corrected annotations. The committed port had never been executed.
##
## Z10 2026-09-30 (hydrology port): mag/hydrology.py rung 1 mirrored here
## ADDITIVELY. HydroNode adds cross_section -> depth -> Q8 head to the node
## shape; the `hydrology` flag + `conductance` pick the law: flag on ->
## _pipe_flow/_available/_move use graded dHead (flow = mini(cap, src.volume,
## (dHead * conductance) >> 8)); flag off -> the boolean verdict path is
## byte-unchanged (water_graph.py stays the regression suite for it).
## game.gd's H key flips the flag live; MAG_HYDROLOGY=1 sets it at boot.
##
## V5 2026-09-30 (economy mirror of mag/water_graph.py 2026-09-29, Z14 flaw):
## waste is a basin, never a void. _move accumulates into waste under BOTH
## head laws, and the STARVED spill routes to the FIRST waste node in
## insertion order (held at the junction when the graph has no waste), so
## pooled units stay boilable: boil at waste -> steam -> condenses at the
## cold Crown. The old mirror deleted both — client and server diverged.
##
## AC2 2026-09-30 (pipe-fracture mirror of mag/water_graph.py, receipt
## watch/inbox/last_mile_20260930/AD1_FRACTURE.md; reach retuned B1
## 2026-09-30, B1_FRACTURE_REACH.md): full-bore flow (flow == cap)
## accumulates stress as cumulative VOLUME; past 200 + djb2(name) % 201
## (= [200, 400] volume units — 200-400 ticks of sustained full bore on
## this board's cap-1 pipes, the operator's design window) the pipe
## FRACTURES — closed forever (open_pipe refuses a burst; the valve verb
## cannot reopen it) — and that tick's flow sprays to the lowest-elevation
## node other than dst (first-min in insertion order). Carried by BOTH head
## laws: a stressed pipe does not care whether the boolean or graded law
## computed its flow. name_hash() is djb2-identical to the Python engine's
## (Python's builtin hash() is per-process salted and could never agree);
## mag/hydrology.py's graded _move override rides the inherited hook and
## inherits the retune automatically.
##
## R8 2026-09-30 (int-domain mirror of mag/water_graph.py, receipt
## watch/inbox/last_mile_20260930/R8_INT_DOMAIN.md): GDScript ints are
## 64-bit; Python's are unbounded. The depth product volume * DEPTH_SCALE
## crossed 2^63 SILENTLY here (HydroNode.depth, and to_dict feeds the
## render layer) while the Python engine computed it exactly. POLICY (one
## law, both engines): the volume domain is BOUNDED at VOLUME_SAT —
## derived so volume * DEPTH_SCALE and elev * HEAD_SCALE + depth stay
## inside signed int64 for any in-domain board — every increment flows
## through one saturating _receive() that CLAMPS at the ceiling and NAMES
## the absorbed amount ("Node X SATURATES: ..."), and ingestion (add_node)
## clamps into the domain. Saturation is policy-declared deletion with a
## sensor, never a silent wrap. This file clamps on BOTH head laws (the
## Python hydrology.py _move override still adds raw — unowned file, named
## residual in the receipt; adopting _receive there is a one-line swap).
##
## VORTEX 2026-10-10 (rotor mirror of mag/water_graph.py, mariner cycle 3,
## receipt watch/inbox/mates_leave_protocol/receipts/receipt_20261010_mariner.md;
## seed: the skyrmion steal, PRX 16, 031078): kind "vortex" is a rotor
## junction. Inflow side plain; outflow side a METERING WHEEL over
## k = live outflow pipes (not fractured, open) in insertion order. One
## outlet emits per tick, the pipe at index rot % k; delivery is ordinary
## _move under BOTH head laws. rot advances only when volume left through
## the chosen pipe (blocked or dry parks the rotor; a burst on its tick
## still turned it). Stored rot stays in [0, k): tiny, int64-safe,
## zero RNG. Vortex outflow rides the gated-outflow phase slot, after
## gate verdicts; emission order across vortices is first-live-outlet
## pipe insertion order. to_dict carries rot for spec parity.
##
## LATCH 2026-10-12 (mirror of mag/water_graph.py, mariner cycle 5, receipt
## watch/inbox/mates_leave_protocol/receipts/receipt_20261012_mariner.md;
## the cycle-4 receipt's self-chosen NEXT THREAD): kind "latch" is a
## POOL-LEVEL gate, the water computer's first memory element. Its sill
## field is its LEVEL (clamped >= 1 at evaluation; wire format unchanged).
## The gate verdict reads the POOL (standing volume plus this tick's
## deferred inflow) against the level. PASS: inflow lands and the outflow
## pipes drain under the ordinary gated-outflow phase ("Latch X opens
## (pool P >= level L).", per-tick while charged, the sill's grammar).
## FAIL: inflow lands ("Latch X holds pool P below level L; pooling.")
## and THE POOL KEEPS: a latch NEVER STARVED-spills (the sill drains its
## pool on the first dry tick; the latch is that pin's standing
## contrast). A charged latch discharges on a dry tick: the only gate
## whose verdict can pass with zero inlets. Below level on a dry tick it
## is silent. Computes: integrator with a release threshold, hysteresis
## floor of L-1, regulator under continuous feed, divider under a rotor
## feed (the rotor sets the division, one charge per k swirl emissions;
## once ramped the latch passes one unit per charge, per the cycle-5
## divider pin's trace); latch chains are pipelines of integrators
## (rotor + latch = finite-state machines). Committed deliveries (a
## gate's or vortex's outflow) charge a latch without a verdict, same
## as vortex-into-xor.
##
## RIPPLE COUNTER + DIFFERENCE DETECTOR 2026-10-13 (mirror of
## mag/water_graph.py, mariner cycle 6, receipt
## watch/inbox/mates_leave_protocol/receipts/receipt_20261013_mariner.md;
## composition laws over the kinds above, no new kinds, zero engine
## bytes, mirrors the Python header for parity): (1) a chain of k=2
## vortices, each stage's first outlet a digit sink and its second
## outlet the next stage, is a BINARY RIPPLE COUNTER: fed one unit per
## tick, rot_i = bit i of the tick count (T=13 reads 1,1,0,1 = 1101),
## digit sinks hold the divided streams (7, 3, 2, 1 after 13), the
## carry crosses every stage within one tick (full cascade exactly on
## the powers of two), and the count is pure state (a closed feed
## mid-run leaves the resumed end state byte-identical to an unbroken
## run). (2) COMMITTED-LANDING INTERFACE LAW: vortex and gate outflows
## are committed deliveries while a gate's verdict reads only DEFERRED
## inlets, so a rotor feeding a gate directly can never pass its
## verdict (the units pool and STARVED-spill); the plain PULSE TANK (a
## one-unit plain node between rotor and gate) re-enters the train
## into the verdict economy one tick later. (3) two tanked wheels, one
## xor, and a level-1 latch with a head-blocked outflow make a
## DIFFERENCE DETECTOR: the latch's pool accumulates exactly the ticks
## where exactly one wheel delivered; phase-locked wheels hold the
## pool at 0 forever (the double-fire volume reads at the waste),
## k=2 vs k=3 drift accumulates pool 6 with coincidence waste 4 in 12
## ticks.
##
## WEATHER + SIPHON PRIME 2026-10-13 (mirror of mag/water_graph.py,
## mariner cycle 7, receipt
## watch/inbox/mates_leave_protocol/receipts/receipt_20261013_mariner.md;
## documentation pins, zero engine bytes): (1) the steam lift crosses a
## CLOSED valve without opening it (boil at a sealed source, condense
## at the cold crown, drain on: the sealed pipe never moves and never
## leaks; the water escapes as weather). (2) the siphon break lives in
## the _move path only: a siphon feeding a GATED junction is probed
## through _available, which delivers 0 on a dry intake but never
## breaks the prime, so the gate-side siphon holds its crest across dry
## spells and delivers a BELOW-CREST refill when water returns, while
## the same siphon into a plain dst breaks on the first dry tick and
## refuses the refill: the dry-spell hysteresis belongs to the dst
## kind, not the pipe.
##
## THE BOILER'S TOLL 2026-10-15 (mirror of mag/water_graph.py, mariner
## cycle 9, receipt watch/inbox/mates_leave_protocol/receipts/
## receipt_20261015_mariner.md; composition laws, no new kinds, zero
## engine bytes): (1) THE SHOVEL ECONOMY: on a cap-1 descent a batch
## lift (one boil of k) and a stream lift (k acts of 1) deliver their
## last unit on the SAME tick; the actuation count is the whole cost
## (1 vs 4 on a 4-unit lift); the cold crown is a free buffer (a cold
## node never spills and never starves). (2) THE ONE-BUS SKY: every
## cloud condenses at the ONE highest cold node, so a lower cold crown
## is shadowed while any higher exists (crowns at 8 and 10, boil both,
## the 8-crown stays 0 forever). (3) THE DEAD LIFT: boiling the top
## cold node itself is a one-tick no-op round trip; end volumes
## byte-match a no-boil control, the only trace is the extra condense
## line. (4) THE LATCH-GATED WEATHER: rotor drips charge a level-2
## latch, the operator reads the verdict at end of tick T and shovels
## between T and T+1, the rain condenses at T+1 and the crown drains
## the same tick; a rotor landing commits AFTER its tick's verdict
## phase, so the first open lags the pool reaching level by one tick
## (pool 2 at t4, first open t5); shovels == opens == delivered.
## (5) THE WORLD VERB LAYER has zero lift latency: a staged boil
## applies at tick start before condense, so one tick row carries the
## boil line and the rain line; same-beat shovels merge into one rain
## line. (6) THE PHASE FLIP AND THE FORGETFUL MASS: a plain two-hop
## leg chains same-tick (+0) when the inlet hop precedes the outlet
## hop in pipe insertion order and delays one tick (+1) when the
## outlet hop is created first; zero-lag, +0, B-lagged and A-lagged
## drift boards all end pool 6 waste 4 after 13 ticks, only the
## accrual tables differ tick by tick: the offset is readable
## mid-window and only mid-window. Signed detection is a WINDOWED
## read, never a completed total.
##
## THE THERMOSTAT 2026-10-16 (mirror of mag/water_graph.py, mariner
## cycle 10, receipt watch/inbox/mates_leave_protocol/receipts/
## receipt_20261016_mariner.md; composition laws, no new kinds, zero
## engine bytes): the closed weather loop (drain -> waste -> boil ->
## crown -> receiver -> drain), only input the operator's shovel.
## (1) THE PRIME: a governor wheel (waste basin, cold crown, latch,
## crown->latch sense leg, latch->waste return) starts only on an
## UNCONDITIONED first act: the latch cannot open before the first
## lift, so a serve loop that waits for an open before the first
## shovel never starts. (2) THE SERVE LAW: one shovel per "Latch L
## opens" line runs the wheel at one four-line tick per act, shovels
## == opens == turns, the sump rides [B-1, B], total mass never
## moves: the steady state HOLDS A LEVEL and spends acts, not water.
## Stop serving and the wheel parks one MOMENTUM tick later (the
## in-flight steam turns it once), then silent at the birth state
## (waste B, crown 0, L 0). (3) THE SETPOINT: the sill is the dial:
## sill 1 rides the sump at [B-1, B], sill 2 at [B-2, B-1]; the park
## SLEEPS CHARGED at pool sill-1 and a HALF prime (the missing
## residual) restarts the wheel at full period next tick: the
## residual is the phase. (4) THE WHEEL RATE IS THE SENSE LEG:
## over-shoveling does not speed the wheel; the surplus pools at the
## cold crown (1->4 over four served ticks), the sump drains to 0,
## and at sump 0 the circuit converges to the honest wheel (shovel 1
## == return 1). After the shovel dies the wheel turns on the
## crown's stock, one momentum tick per stored unit, and the board
## still parks at its birth state: the sky spends itself last.
## (5) RAIN CHARGES THE LATCH (cycle-7 residual g, closed): a cold
## crown ABOVE a latch feeds it through its drain: hold pool 1,
## open, open, silent at pool 1 for a batch lift of 3 at sill 2; a
## latch itself can never be the crown (kind "latch" is not "cold").
## (6) THE LAP IS PIPE ORDER: the recirculation lap is ONE tick when
## the crown leg is created before the drain leg (rider chains
## straight to waste, +0) and TWO ticks when the drain leg is first
## (rider rests at the receiver one tick, +1); one act per lap
## either way, conserved at every lap boundary. Zero losses in the
## pin set: saturation is the only deletion port and none of these
## boards reach it.
##
## THE WINDING CLOCK 2026-10-17 (mirror of mag/water_graph.py, mariner
## cycle 11, receipt watch/inbox/mates_leave_protocol/receipts/
## receipt_20261017_mariner.md; composition laws, no new kinds, zero
## engine bytes): the cold crown is a WINDED DELAY LINE: units stored
## in the sky are ticks of autonomous wheel rotation after the shovel
## dies. (1) STORE-THEN-COUNT: one batch lift of N at the basin on an
## unprimed governor wheel and the wheel opens EXACTLY N times (tick 1
## carries the merged condense +N plus the first turn, ticks 2..N the
## bare three-line wheel, tick N+1 silent, park at the birth state);
## pinned N 0, 1, 3, 5. The sky holds a number. (2) THE CLOCK CANNOT
## READ THE SHOVEL: a batch wind (one boil of N) and a stream wind (N
## acts of 1) drive BYTE-IDENTICAL clock runs: the physics sees steam
## totals, never act counts. (3) THE BAND: the sense leg's cap sets
## WHERE the surplus waits, never the wheel's rate. Steady serve, cap-2
## leg under sill-2 vs cap-1: identical four-line shape, different RAMP
## (the wide leg carries the whole prime through on tick 1, no HOLD;
## the narrow leg parks the ramp unit at the crown forever, a hostage,
## sump riding one lower: [1, 2] vs [2, 3] on B=4). Under a wind the
## wide leg moves the buffer INSIDE the latch (THE BALLOON): crown
## never parks, the pool balloons +1 per tick over the drain cap, the
## open run is unbroken from first open through sky-death to
## balloon-drain (pinned: B=6, prime 2, three batch-2 shovels, opens
## t1-t7, pool 1->4 then drains to the sill-1 floor; the cap-1 sill-1
## control spends the same 8 units as 8 opens from crown stock and
## parks at the birth state: the floor is the difference, the
## balloon's 8th unit never opens and is never lost).
## (4) THE WORLD-VERB WIND: the world verb layer winds the win meter
## zero-latency: two same-beat staged pairs at the spring read crown 2
## then crown 4, one merged rain line (+2) per beat in the same tick
## row as the boil lines, winner true on the crossing beat, board
## conserved 8 at every tick.
##
## THE READING GLASS 2026-10-18 (mirror of mag/water_graph.py, mariner
## cycle 12, receipt watch/inbox/mates_leave_protocol/receipts/
## receipt_20261018_mariner.md; composition laws, no new kinds, zero
## engine bytes): the balloon holds (wind minus drain) as readable
## state, so the clock can read itself back. (1) THE DROPPER GAUGE: a
## cap-1 tap leg from a ballooned pool into a reader latch (sill 1)
## with a counter sink. THE GAUGE CLAMPS THE BALLOON: a tap open from
## birth converts the integrator into a pass-through wire (pool rides
## [2 at verdict, 0 after]; on 8 wound units the tap passes 4 while
## the open drain takes 4 back). Drain shut: the store pools net +1
## per tick and the tap reads it live, sink ends at wind minus the
## floor (5 of 6 on B=6, sill 2). THE STORED READ: wind with the tap
## shut, then open the valve: 1 per tick while pool >= level; the
## floor (level minus 1) is the blind spot: a stored 6 reads as 5 at
## sill 2, a sill-1 balloon reads the full 6 to pool 0; the
## resolution is the balloon's OWN sill, never the tap's.
## (2) THE 2-TICK LATENCY: a gate's outflow into a gate is a COMMITTED
## LANDING (cycle-6 interface law): the reader's verdict never sees
## same-tick inflow; a tap unit leaves at T, the sink reads it at
## T+1, one tick per gate hop; the reader outlives the wind by one
## tick (the afterbeat drains on the first silent tick).
## (3) THE PARK FORGETS THE STORAGE SITE: B=8, sill 2, prime 2 plus
## three 2-shovels: the cap-1 hostage board and the cap-2 balloon
## board end IDENTICAL (waste 7, crown 0, pool 1) with the SAME open
## count (7: the narrow board's t1 HOLD line is not an open), yet the
## accrual tables are disjoint (crown 1,2,3,4,3,2,1,0 vs 0 forever;
## pool flat 1 vs 1,2,3,4,3,2,1; waste tables differ t1-t7): the
## storage site is unreadable at the park, readable only mid-window
## (cycle-9 windowed law, fed); the wide board parks one tick sooner
## (t8 vs t9). (4) THE CEILING IS THE BALLOON'S ONLY PORT: a latch
## pool at VOLUME_SAT absorbs the next inflow with the named amount
## (1 absorbed at 9223372036586340), the verdict still passes (the
## 16-digit pool in the open line), the drains pull it straight back
## down (SAT, SAT-1, SAT-2 on a cap-1 drain): a clamp, not a freeze;
## mass loss is exactly the named absorbed unit, the engine's only
## deletion port. (5) THE READ IS A DRAIN: every moving tap needs
## head (src.elev strictly above dst.elev): uphill and equal taps
## move zero forever, no non-destructive read exists; the head law
## is the privacy law.
##
## THE BANKED GOVERNOR 2026-10-20 (mirror of mag/water_graph.py,
## mariner cycle 13, receipt watch/inbox/mates_leave_protocol/
## receipts/receipt_20261020_mariner.md; composition laws, no new
## kinds, zero engine bytes): the reader's pulse train drives the
## staged boils, one shovel per reader open, the serve trigger moved
## to the gauge line. (1) THE GAUGE-LINE SERVE: one prime shovel,
## then one per reader open, runs unattended at one serve per TWO
## ticks (the verdict lag stretches the period, eats nothing: bank 6,
## sill 1, sink ends at 6, bank empty, silence from t13). (2) THE
## PRIME LAW HOLDS AT THE GAUGE: a sub-level prime strands the bank
## (one shovel under sill 2: pool 1 holds, 7 ticks, zero serves).
## (3) THE FLOOR TAX: the primed sill-2 governor serves N-1 and
## parks pool 1 in the store; the 2-prime through a cap-1 sense leg
## hosts one unit at the crown one tick (wheel starts t2, first
## open t3). (4) THE DRY KNOCK: the train asks one serve past the
## bank: the last open stages a shovel the empty basin rejects
## (DRY_POOL), exactly 1 knock on every spent bank. (5) THE ORDER
## IS THE METER: cap-2 tap on the live-wire board: drain-first
## keeps the balance split (4 of 8: the drain takes its unit, the
## tap passes min(cap, remainder)), tap-first meters the FULL
## stream (8 of 8) and the reader balloons +1/tick (pool 2,3,4,5),
## draining the backlog after the wind dies. (6) THE METER'S
## FLOOR: the terminal pool is the first value below the level in
## the descent bank, bank-cap, bank-2cap, ...: cap-1 floors at
## level-1 (stored 6 reads 5), cap-2 reads to the residue mod the
## cap (stored 6 reads 6; stored 5 reads 4; stored 7 reads 6).
## (7) THE CROSS-ENGINE VERDICT: the governor board runs both
## engines through the rule_parity harness: 12 ticks, state hashes
## and verdict rows identical, including a reject:RATE_CAP row both
## engines agree on.
##
## THE ORBIT 2026-10-23 (mirror of mag/water_graph.py, mariner cycle
## 14, receipt watch/inbox/mates_leave_protocol/receipts/
## receipt_20261023_mariner.md; composition laws, no new kinds, zero
## engine bytes): a vortex whose outlets all RETURN to the basin
## closes a recirculation lap, the engine's first mass-free computer.
## (1) THE ORBITAL CLOCK: one shovel per wheel emission, keyed on the
## OUTLET PIPE NAME (a returning leg's line reads "ra: 1 to waste at
## waste.", the waste-hold grammar, never "src->dst"), runs the wheel
## at one turn per tick: serves == turns == ticks, mass B at every
## tick boundary, rot = serves mod k, and never a dry knock (the
## both-return lap returns everything). (2) THE ORBIT'S SHAPE: the
## return depths are the waveform (depth 1 + depth 2 alternate the
## basin between full and one unit in the rest tank). (3) THE SKY MOD
## K: a batch wind of N turns the wheel exactly N times and parks
## byte-identical to birth except rot = N mod k (N=5 reads rot 2,
## N=6 reads rot 0 on k=3): a modulus computed for no water. (4) THE
## DAMPED ORBIT: one export leg leaks one unit per k turns (bank B
## spends in 2B turns at k=2, exactly 1 dry serve past the spent
## basin). (5) THE PARK IS THE BIRTH STATE: stop staging and the
## wheel turns one momentum tick on the in-flight serve, then silent;
## only the register differs. (6) THE CROSS-ENGINE ORBIT: the board
## runs the rule_parity harness as its first vortex-kind sequence;
## NAMED LIMIT (cycle 14): the parity state hash covered no rot field
## (the py state_hash and this runner's nodes_out alike), so the
## harness proved volume and verdict parity, never register parity.
## CLOSED cycle 15 (2026-10-24, THE REGISTER ON THE WIRE, receipt
## receipt_20261024_mariner.md; instrument bytes, zero engine bytes):
## the hash ends at rot on both sides, the state diffs carry rot, and
## both ingestion paths install a spec's initial register, so a twin
## that agreed on every volume while rotating its wheel differently
## now reads parity-false.

signal water_event(text: String)

# Z10 hydrology constants (mag/hydrology.py mirror)
const HEAD_SCALE := 256            # Q8: one elevation unit = 256 head units
const DEPTH_SCALE := 1000          # depth = volume * 1000 / cross_section
const DEFAULT_CROSS_SECTION := 1000

# R8 INT DOMAIN LAW (2026-09-30, mag/water_graph.py mirror): the volume
# domain ceiling. Derived there as (INT64_MAX - ELEV_SAT * HEAD_SCALE)
# // DEPTH_SCALE so volume * DEPTH_SCALE (worst case cross_section 1) and
# elev * HEAD_SCALE + depth both stay inside signed int64 — pinned by
# tests/test_water_graph_int_domain.py on both engines' shared literal.
const INT64_MAX := 9223372036854775807
const ELEV_SAT := 1048576          # 1 << 20: elevation domain ceiling
const VOLUME_SAT := 9223372036586340


static func name_hash(s: String) -> int:
    ## AC2: djb2 32-bit — byte-identical loop to mag/water_graph.py
    ## name_hash() so the fracture threshold agrees across engines.
    var h := 5381
    for i in s.length():
        h = (h * 33 + s.unicode_at(i)) & 0xFFFFFFFF
    return h


static func fracture_threshold(pipe_name: String) -> int:
    ## AC2 + B1 (2026-09-30): volume a pipe survives at full bore:
    ## 200 + hash(name) % 201 -> [200, 400] VOLUME units — stress accumulates
    ## as cumulative throughput (stress += flow each full-bore tick), so a
    ## cap-1 pipe bursts after 200-400 ticks of sustained full bore and a
    ## cap-k pipe after threshold/k ticks. Deterministic, zero RNG (no hash
    ## randomization exists in GDScript, but the loop above is what pins
    ## cross-language parity).
    return 200 + name_hash(pipe_name) % 201


class WNode:
    var name: String
    var elev: int = 0
    var kind: String = "plain"  # plain | xor | sill | cold | waste | vortex | latch
    var sill: int = 0
    var volume: int = 0
    var steam: int = 0
    var rot: int = 0  # VORTEX: rotor position in [0, k)


class HydroNode extends WNode:
    ## Z10: the node shape with geometry (mag/hydrology.py HydroNode mirror).
    ## depth is milli-depth over cross_section (small tanks still grade with
    ## integer math); head is elevation in Q8 plus depth in the same integer
    ## space — filling a pool RAISES its head (backwater, equalization).
    ## Every node is a HydroNode; the boolean law never reads these fields,
    ## so its behavior is identical to the plain WNode port.
    var cross_section: int = DEFAULT_CROSS_SECTION

    @warning_ignore("integer_division")
    var depth: int:
        get:
            return volume * DEPTH_SCALE / cross_section

    var head: int:
        get:
            return elev * HEAD_SCALE + depth

class WPipe:
    var name: String
    var src: String
    var dst: String
    var cap: int = 1
    var siphon: bool = false
    var crest: int = 2
    var primed: bool = false
    var open: bool = true
    var stress: int = 0      # AC2: cumulative full-bore load
    var fractured: bool = false  # AC2: burst — closed forever

var nodes: Dictionary = {}  # name -> WNode (always HydroNode since Z10)
var pipes: Dictionary = {}  # name -> WPipe
var tick_count: int = 0

# Z10 head law: false = boolean verdict (water_graph.py), true = graded head
# (mag/hydrology.py). Flipped live by game.gd's H key; MAG_HYDROLOGY env at boot.
var hydrology: bool = false
var conductance: int = 8     # Q8: flow = dHead * conductance >> 8


func add_node(node_name: String, elev: int = 0, kind: String = "plain", sill: int = 0, volume: int = 0, cross_section: int = DEFAULT_CROSS_SECTION, rot: int = 0) -> void:
    # Z10: every node carries geometry (HydroNode); which head law reads it is
    # the `hydrology` flag, flippable mid-run. mag/hydrology.py raises
    # ValueError on cross_section < 1; the assert mirrors add_pipe's idiom.
    # R8 INT DOMAIN LAW: ingestion clamps into the declared domain (volume
    # <= VOLUME_SAT, |elev| <= ELEV_SAT) so the depth product can never wrap
    # this engine's int64. Construction-time saturation is silent BY DESIGN
    # — no event stream exists yet; the runtime sensor fires in _receive().
    # VORTEX (2026-10-10): rot rides the same ingestion clamp (runtime keeps
    # it in [0, k); the ceiling only guards a hostile spec).
    assert(cross_section >= 1, "cross_section must be >= 1, got " + str(cross_section))
    var n = HydroNode.new()
    n.name = node_name
    n.elev = clampi(elev, -ELEV_SAT, ELEV_SAT)
    n.kind = kind
    n.sill = sill
    n.volume = mini(volume, VOLUME_SAT)
    n.cross_section = cross_section
    n.rot = maxi(0, mini(rot, VOLUME_SAT))
    nodes[node_name] = n


func add_pipe(pipe_name: String, src: String, dst: String, cap: int = 1, siphon: bool = false, crest: int = 2, is_open: bool = true, stress: int = 0, fractured: bool = false) -> void:
    assert(nodes.has(src), "unknown src node: " + src)
    assert(nodes.has(dst), "unknown dst node: " + dst)
    var p = WPipe.new()
    p.name = pipe_name
    p.src = src
    p.dst = dst
    p.cap = cap
    p.siphon = siphon
    p.crest = crest
    p.open = is_open
    p.stress = stress
    p.fractured = fractured
    pipes[pipe_name] = p


func open_pipe(pipe_name: String) -> void:
    # AC2 (2026-09-30): a FRACTURED pipe is closed for good — the valve verb
    # routes through here and must NOT be able to reopen a burst pipe.
    if pipes[pipe_name].fractured:
        return
    pipes[pipe_name].open = true


func close_pipe(pipe_name: String) -> void:
    pipes[pipe_name].open = false


func volume(node_name: String) -> int:
    return nodes[node_name].volume if nodes.has(node_name) else 0


func boil(node_name: String, units: int = 1) -> int:
    var n: WNode = nodes[node_name]
    units = mini(units, n.volume)
    n.volume -= units
    # R8: steam shares the volume domain (it condenses back into volume);
    # unbounded accumulation would wrap this engine's int64 long before
    # Python's unbounded ints noticed.
    n.steam = mini(VOLUME_SAT, n.steam + units)
    return units


func _receive(n: WNode, gain: int, events: Array[String]) -> void:
    ## R8 INT DOMAIN LAW receiver (mag/water_graph.py _receive twin): every
    ## volume increment lands here (or at the add_node/boil ingest clamps)
    ## so `volume <= VOLUME_SAT` holds on every tick and
    ## volume * DEPTH_SCALE can never cross 2^63 in EITHER engine. A gain
    ## that would cross the ceiling CLAMPS and NAMES the absorbed amount —
    ## policy-declared deletion with a sensor, never a silent wrap. Both
    ## operands stay <= VOLUME_SAT, so the arithmetic itself is int64-safe.
    if gain <= 0:
        return
    var room: int = VOLUME_SAT - n.volume
    if gain <= room:
        n.volume += gain
        return
    n.volume = VOLUME_SAT
    events.append("Node %s SATURATES: %d absorbed at the volume ceiling %d (int64 depth domain, R8)." % [n.name, gain - room, VOLUME_SAT])


func tick() -> Array[String]:
    tick_count += 1
    var events: Array[String] = []
    events.append_array(_condense_steam())

    var gated_kinds := ["xor", "sill", "latch"]
    var out_kinds: Array = gated_kinds + ["vortex"]
    var deferred_in: Dictionary = {}  # node_name -> [{pipe, src, flow}]
    var gated_out: Array[WPipe] = []
    var vortex_out: Dictionary = {}  # node_name -> [WPipe] (VORTEX)

    for p: WPipe in pipes.values():
        if p.fractured or not p.open:
            continue
        var src: WNode = nodes[p.src]
        var dst: WNode = nodes[p.dst]
        if src.kind in out_kinds:
            gated_out.append(p)
            if src.kind == "vortex":
                if not vortex_out.has(src.name):
                    vortex_out[src.name] = []
                vortex_out[src.name].append(p)
            continue
        if dst.kind in gated_kinds:
            var flow := _available(p, src, events)
            if flow > 0:
                # B1 SEAM FIX mirror (2026-09-30, B1_FRACTURE_REACH.md):
                # full-bore flow INTO a gated junction stresses the pipe AT
                # PROBE TIME (the water left the source through the pipe
                # section). The first cut loaded pipes only in _move, so
                # gated inlets never stressed and the default Mountain's
                # main artery (p_spring -> xor gate1) could NEVER burst.
                # On burst the probe-time flow sprays (conserved; the burst
                # helper itself does src -= flow) and the gate never sees
                # the inlet — same shape as the engine's gated branch in
                # mag/water_graph.py tick(). No probe-time reserve here:
                # this mirror decrements the source at GATE phase (its LW5
                # shape), so the only probe-time volume move is the burst's.
                if _fracture_if_past_threshold(p, src, dst, flow, events):
                    continue
                # NEG-VOLUME LAW port (2026-09-30, V5/D1 parity fix, receipt
                # watch/inbox/last_mile_20260930/V5_PARITY.md): the deferred
                # flow is RESERVED at PROBE time — else a sibling pipe from
                # the same source re-spends it in the same tick and the gate
                # phase below double-decrements src. The old mirror deferred
                # without reserving (29/100 parity sequences diverged; the
                # twin manufactured water and double-spent springs). The
                # gate-phase decrements are GONE — the volume left at probe.
                src.volume -= flow
                if not deferred_in.has(dst.name):
                    deferred_in[dst.name] = []
                deferred_in[dst.name].append({"pipe": p.name, "src": p.src, "flow": flow})
            continue
        _move(p, src, dst, events)

    # Junction gates
    var gate: Dictionary = {}
    for node_name: String in nodes:
        var node: WNode = nodes[node_name]
        if not (node.kind in gated_kinds):
            continue
        var ins = deferred_in.get(node_name, [])
        var allow: bool
        if node.kind == "xor":
            allow = ins.size() == 1
        elif node.kind == "latch":
            # LATCH LAW mirror (2026-10-12, cycle 5): the gate reads the
            # POOL (standing volume plus this tick's deferred inflow)
            # against the LEVEL in node.sill (clamped >= 1). The only gate
            # that can pass with zero inlets: a charged latch discharges
            # on a dry tick.
            var pool: int = node.volume
            for entry in ins:
                pool += entry.flow
            allow = pool >= maxi(1, node.sill)
        else:
            allow = ins.size() >= maxi(1, node.sill)
        gate[node_name] = 1 if allow else 0
        if allow:
            for entry in ins:
                # volume already reserved at probe time (D1 parity port);
                # the gate only DELIVERS it onward now. R8: saturating.
                _receive(node, entry.flow, events)
                events.append("%s: %d %s->%s." % [entry.pipe, entry.flow, entry.src, node_name])
            if node.kind == "xor":
                events.append("Junction %s passes (%s sole inlet)." % [node_name, ins[0].pipe])
            elif node.kind == "latch":
                events.append("Latch %s opens (pool %d >= level %d)." % [node_name, node.volume, maxi(1, node.sill)])
            else:
                events.append("Junction %s sill reached (%d inlets)." % [node_name, ins.size()])
        else:
            var held_now: int = 0
            for entry in ins:
                held_now += entry.flow
                # volume already reserved at probe time (D1 parity port);
                # R8: saturating receive.
                _receive(node, entry.flow, events)
            var why: String = "%d inlets" % ins.size() if node.kind == "xor" else "%d < sill %d" % [ins.size(), node.sill]
            if node.kind == "latch":
                # MEMORY LAW mirror (2026-10-12, cycle 5): a below-level
                # latch KEEPS its pool across dry ticks, NEVER
                # STARVED-spills (the sill drains on the first dry tick;
                # the latch is that pin's standing contrast). Below level
                # with no inflow it is silent: no state change, no event.
                if held_now > 0:
                    events.append("Latch %s holds pool %d below level %d; pooling." % [node_name, node.volume, maxi(1, node.sill)])
                continue
            if held_now > 0:
                events.append("Junction %s holds %d below gate (%s); pooling." % [node_name, held_now, why])
            if node.volume > 0 and held_now == 0:
                # V5 ECONOMY LAW mirror (2026-09-29 Python fix; evidence:
                # tests/test_water_graph_starvation.py V5 block): the old cut
                # zeroed volume with NO destination while its event string
                # claimed "spilled to waste" — deletion. The spill ROUTES to
                # the first waste node in insertion order (Dictionary
                # preserves it — same determinism as Python's values()), and
                # waste HOLDS it as a boilable basin. No waste node in the
                # graph: HOLD at the junction, never delete.
                var spill := node.volume
                var basin: WNode = null
                for n: WNode in nodes.values():
                    if n.kind == "waste":
                        basin = n
                        break
                if basin != null:
                    _receive(basin, spill, events)  # R8
                    node.volume = 0
                    events.append("Junction %s STARVED: %d pooled units spilled to waste at %s (%s; no inflow reached the gate; boil %s to recover them)." % [node_name, spill, basin.name, why, basin.name])
                else:
                    events.append("Junction %s STARVED: %d pooled units held at the junction (%s; no inflow reached the gate; no waste node to receive them)." % [node_name, spill, why])

    # Gated outflow
    for p: WPipe in gated_out:
        if gate.get(p.src, 0) == 0:
            continue
        _move(p, nodes[p.src], nodes[p.dst], events)

    # Vortex rotor emissions (VORTEX mirror, 2026-10-10): after gate
    # outflows, one outlet per vortex per tick, the live pipe at
    # rot % k in insertion order; delivery is ordinary _move under both
    # head laws; rot advances only when volume left through the chosen
    # pipe (metering wheel, never a free-spinning clock). Dictionary
    # iteration preserves insertion order (same determinism as Python).
    for node_name: String in vortex_out:
        var vnode: WNode = nodes[node_name]
        var outlets: Array = vortex_out[node_name]
        var vp: WPipe = outlets[vnode.rot % outlets.size()]
        var before: int = vnode.volume
        _move(vp, vnode, nodes[vp.dst], events)
        if vnode.volume < before:
            vnode.rot = (vnode.rot + 1) % outlets.size()

    return events


func _pipe_flow(p: WPipe, src: WNode, dst: WNode, events: Array[String]) -> int:
    ## Z10: flow a pipe would carry this tick under the graded head, no
    ## volume commit (mirrors mag/hydrology.py _pipe_flow exactly). The
    ## rung-1 change: dHead over node cross-sections in Q8, replacing the
    ## boolean `src.elev > dst.elev` verdict. Siphons keep their own law
    ## (prime at crest under positive dHead, then full bore); the prime
    ## latch + its event are authority side effects, same as the Python
    ## engine. Only called when hydrology is true.
    if src.volume <= 0:
        return 0
    var d_head: int = (src as HydroNode).head - (dst as HydroNode).head
    if p.siphon:
        if not p.primed:
            if src.volume >= p.crest and d_head > 0:
                p.primed = true
                events.append("Siphon %s primes at crest (%d)." % [p.name, p.crest])
            else:
                return 0
        return mini(p.cap, src.volume)
    if d_head <= 0:
        return 0  # check valve: gravity-only, never uphill
    # mini() is 2-arg in GDScript (Python min is variadic); nested calls are
    # the same min of three — mag/hydrology.py: min(cap, src.volume, dHead*8>>8).
    return mini(p.cap, mini(src.volume, (d_head * conductance) >> 8))


func _available(p: WPipe, src: WNode, events: Array[String]) -> int:
    if hydrology:
        # Z10: graded flow into gated junctions, no commit (mirrors
        # mag/hydrology.py _available override).
        if src.volume <= 0:
            return 0
        return _pipe_flow(p, src, nodes[p.dst], events)
    if src.volume <= 0:
        return 0
    var dst: WNode = nodes[p.dst]
    var head_ok: bool = src.elev > dst.elev
    if p.siphon:
        if not p.primed:
            if src.volume >= p.crest and head_ok:
                p.primed = true
                events.append("Siphon %s primes at crest (%d)." % [p.name, p.crest])
            else:
                return 0
        return mini(p.cap, src.volume)
    if not head_ok:
        return 0
    return mini(p.cap, src.volume)


func _spray_target(dst: WNode) -> WNode:
    ## AC2: the lowest-elevation node other than dst — first-min in insertion
    ## order (strict < keeps the first tie), mirroring the Python engine's
    ## min(..., key=elev) over dict insertion order.
    var spray: WNode = null
    for n: WNode in nodes.values():
        if n.name != dst.name and (spray == null or n.elev < spray.elev):
            spray = n
    return spray


func _fracture_if_past_threshold(p: WPipe, src: WNode, dst: WNode, flow: int, events: Array[String]) -> bool:
    ## AC2 pipe-fracture law (mag/water_graph.py _fracture mirror): full-bore
    ## flow (flow == cap) loads the pipe; past 120 + djb2(name) % 240 it
    ## bursts — closed forever — and this tick's flow sprays to the lowest
    ## node other than dst. Volumes conserved: src -= flow, spray += flow.
    ## Returns true when the burst happened (caller returns).
    if flow != p.cap:
        return false
    p.stress += flow
    if p.stress <= fracture_threshold(p.name):
        return false
    p.fractured = true
    p.open = false
    src.volume -= flow
    var spray := _spray_target(dst)
    _receive(spray, flow, events)  # R8: even a burst's spray saturates
    events.append("Pipe %s FRACTURES (stress %d): spray to %s." % [p.name, p.stress, spray.name])
    return true


func _move(p: WPipe, src: WNode, dst: WNode, events: Array[String]) -> void:
    # Cycle-4 (2026-10-11): the write-only `delivered` dict is gone, same
    # deletion as mag/water_graph.py (created, written, never read by any
    # engine, test, or render layer; event lines carry the provenance).
    if hydrology:
        # Z10: commit the graded flow (mirrors mag/hydrology.py _move; same
        # event grammar as the boolean engine, so downstream reporters —
        # water_particles splash parsing included — do not branch).
        if src.volume <= 0:
            if p.siphon and p.primed:
                p.primed = false
                events.append("Siphon %s breaks (intake dry)." % p.name)
            return
        var graded: int = _pipe_flow(p, src, dst, events)
        if graded <= 0:
            return
        if _fracture_if_past_threshold(p, src, dst, graded, events):
            return  # AC2: burst — this tick's flow sprayed, not delivered
        src.volume -= graded
        if dst.kind == "waste":
            # V5 ECONOMY LAW mirror: waste HOLDS what it receives (both head
            # laws) — the old early-return skipped the accumulation, so every
            # unit piped to waste was deleted. Held waste is boilable.
            _receive(dst, graded, events)  # R8
            events.append("%s: %d to waste at %s." % [p.name, graded, dst.name])
            return
        _receive(dst, graded, events)  # R8 (hydrology branch clamps too —
        # Python's hydrology.py _move still adds raw; named residual, receipt
        # R8_INT_DOMAIN.md; THIS engine stays domain-total under both laws)
        events.append("%s: %d %s->%s." % [p.name, graded, p.src, p.dst])
        return
    if src.volume <= 0:
        if p.siphon and p.primed:
            p.primed = false
            events.append("Siphon %s breaks (intake dry)." % p.name)
        return
    var head_ok: bool = src.elev > dst.elev
    var flow: int
    if p.siphon:
        if not p.primed:
            if src.volume >= p.crest and head_ok:
                p.primed = true
                events.append("Siphon %s primes at crest (%d)." % [p.name, p.crest])
            else:
                return
        flow = mini(p.cap, src.volume)
    else:
        if not head_ok:
            return
        flow = mini(p.cap, src.volume)
    if _fracture_if_past_threshold(p, src, dst, flow, events):
        return  # AC2: burst — this tick's flow sprayed, not delivered
    src.volume -= flow
    if dst.kind == "waste":
        # V5 ECONOMY LAW mirror (2026-09-29 Python fix): waste HOLDS what it
        # receives — the old early-return skipped the accumulation, so every
        # unit piped to waste was deleted from the economy. Held waste is
        # boilable (steam ignores pipes, condenses at the cold crown).
        _receive(dst, flow, events)  # R8
        events.append("%s: %d to waste at %s." % [p.name, flow, dst.name])
        return
    _receive(dst, flow, events)  # R8
    events.append("%s: %d %s->%s." % [p.name, flow, p.src, p.dst])


func _condense_steam() -> Array[String]:
    var events: Array[String] = []
    var colds: Array = []
    for n: WNode in nodes.values():
        if n.kind == "cold":
            colds.append(n)
    if colds.is_empty():
        return events
    var target: WNode = colds[0]
    for n: WNode in colds:
        if n.elev > target.elev:
            target = n
    for n: WNode in nodes.values():
        if n.steam > 0:
            _receive(target, n.steam, events)  # R8 (event order twins Python)
            events.append("Steam condenses at %s (+%d)." % [target.name, n.steam])
            n.steam = 0
    return events


func to_dict() -> Dictionary:
    var result := {"tick": tick_count, "nodes": {}, "pipes": {}}
    for name: String in nodes:
        var n: HydroNode = nodes[name]
        # Z10: cross_section/depth/head added (hydrology.v1 node-dict parity;
        # a render layer can depth-tint off `depth`/`head` directly — the
        # X1 next-rung hook). Boolean consumers read the old keys only.
        # VORTEX (2026-10-10): rot rides for spec parity with to_spec.
        # LATCH (2026-10-12, cycle 5): sill rides too — the level is
        # runtime-essential gate state for kind "latch" and to_spec emits
        # it under the same additive-key family law (steam, rot, sill).
        result["nodes"][name] = {"elev": n.elev, "kind": n.kind, "sill": n.sill, "volume": n.volume, "steam": n.steam, "rot": n.rot, "cross_section": n.cross_section, "depth": n.depth, "head": n.head}
    for name: String in pipes:
        var p: WPipe = pipes[name]
        result["pipes"][name] = {"src": p.src, "dst": p.dst, "cap": p.cap, "open": p.open, "primed": p.primed, "siphon": p.siphon, "stress": p.stress, "fractured": p.fractured} # B1.0 fix 2026-09-29: siphon was missing (game.gd _draw reads it); AC2 2026-09-30: stress/fractured mirror the engine's to_spec keys
    return result
