"""water_graph — the flow-graph engine: routing as physics, not a hardcoded pair.

Operator order 2026-09-27 ("use the physics instead of fighting them" +
"Next"): the water_computer module hardcodes VALVE_AT = {two valves on one
line} — nothing to route WITH. This engine generalizes the family's real
laws (mag/hydro_xor_sim.py: one-way check valves, mark-per-tick, siphon
crests; mag/water_computer.py: gravity tick, honest OUT) onto an arbitrary
graph:

  - Nodes: tanks/junctions with integer elevation + volume; `cold` nodes
    condense steam; `waste` HOLDS spilled/overflow volume as a boilable
    basin (V5 economy law 2026-09-29: deletion is theft — see the
    STARVATION LAW note under tick()).
  - Pipes: one-way (check-valve law, no backflow by construction), integer
    capacity, optional siphon with a crest volume (primes at crest, runs
    until the intake breaks — hydro_xor_sim's semantics, integerized.
    Cycle-7 pin, 2026-10-13: the break lives in _move only, and a siphon
    feeding a GATED junction is probed through _available, which delivers
    0 on a dry intake but never breaks the prime. So the gate-side
    siphon holds its crest across dry spells and delivers a BELOW-CREST
    refill when water returns, while the same siphon into a plain dst
    breaks on the first dry tick and refuses the refill: the dry-spell
    hysteresis belongs to the dst kind, not the pipe).
  - Junctions: `plain` accumulates; `xor` delivers only when EXACTLY one
    inlet delivered this tick (both inlets -> overflow to waste — the
    hydraulic XOR); `sill` delivers only when total inflow >= a threshold
    (the hydraulic AND; sill 1 IS the hydraulic OR). The `any` kind
    promised on this line until 2026-10-11 never existed in the tick
    (cycle 1 finding 8: the cycle-1 probe read plain behavior; grep
    found zero production use) and is struck by the cycle-4 receipt
    (watch/inbox/mates_leave_protocol/receipts/receipt_20261011_mariner.md):
    sill 1 was already the OR; a redundant ghost kind is a spec lie.
  - Steam: `boil(node, n)` lifts volume to steam; each tick steam condenses
    at the highest `cold` node as rain (rises regardless of pipes - a
    second routing medium; falls back to its origin node when no cold node
    exists). Cycle-7 pin: the lift crosses a CLOSED valve without opening
    it (boil at a sealed src, condense at a cold crown, drain on: the
    sealed pipe never moves and never leaks; the water escapes as
    weather).
  - Fracture (AC2, 2026-09-30, watch/inbox/last_mile_20260930/AD1_FRACTURE.md;
    reach retuned B1 2026-09-30, B1_FRACTURE_REACH.md): a pipe running FULL
    BORE (flow == cap) accumulates `stress += flow` — cumulative throughput
    in VOLUME units — in `_move` AND at gated-inlet PROBE time (B1 seam fix:
    gated inlets load too, else the default Mountain's main artery can never
    burst); at `200 + name_hash(name) % 201` (= [200, 400] volume, the
    operator's sustained-full-bore design window) it FRACTURES — closed
    forever (`open()` refuses it; the valve verb cannot reopen a burst) —
    and that tick's flow sprays to the lowest-elevation node other than dst
    (first-min in insertion order). Conserved, never deleted, zero RNG.
  - Vortex (2026-10-10, mariner cycle 3, receipt
    watch/inbox/mates_leave_protocol/receipts/receipt_20261010_mariner.md;
    seed: the skyrmion steal, PRX 16, 031078, vortices that trap and
    rotate floating bodies): kind "vortex" is a rotor junction. Inflow
    side: a plain accumulator. Outflow side: a METERING WHEEL over
    k = its LIVE outflow pipes (not fractured, open) in insertion
    order. One outlet emits per tick, the pipe at index rot % k;
    delivery is ordinary _move, so head law, siphon law, fracture law,
    and the waste hold apply unchanged. rot advances by one ONLY when
    volume actually left through the chosen pipe (a blocked or dry
    outlet parks the rotor; a burst on its tick still turned it, the
    water left the hub). rot is stored in [0, k): tiny, R8-safe,
    deterministic from insertion order, zero RNG. Vortex outflow rides
    the gated-outflow phase slot (after gate verdicts), so a vortex
    never drains its own same-tick inflow ahead of the gates; across
    vortices the emission order is first-live-outlet pipe insertion
    order. What it computes (cycle-4 corrections, 2026-10-11, same
    receipt; the probes falsified the cycle-3 self-clock guess):
    round-robin demux (turns XOR overflow into alternating pass), a
    mod-k counter, and a RUN-DOWN CLOCK by chaining: a k1-wheel that
    feeds a k2-wheel on every k1'th tick drives the k2 wheel with
    period k1*k2 (pinned: 2->3 reads x,y,z,x,y,z on even ticks; a
    continuously fed k2 wheel collapses to period k2). There is NO
    self-clocking source: the DAG LAW (cycle 4) holds that every pipe
    must descend (a siphon primes only under the same head law), a
    direct self-loop outlet can never flow (equal elevation is no
    head; its own probe: 6 ticks, zero movement), and steam - the only
    lift in the engine - is actuated (boil()), never autonomous. Every
    rotor clock runs down when its pool drains; the graph is a
    descent, never a perpetual loop.
  - Latch (2026-10-12, mariner cycle 5, receipt
    watch/inbox/mates_leave_protocol/receipts/receipt_20261012_mariner.md;
    the cycle-4 receipt's self-chosen NEXT THREAD): kind "latch" is a
    POOL-LEVEL gate, the water computer's first memory element. Its
    `sill` field is its LEVEL (clamped >= 1 at evaluation; the wire
    format is unchanged). The gate verdict reads the POOL, not the
    inlets: standing volume plus this tick's arriving inflow against
    the level. PASS: the inflow lands and the outflow pipes drain
    under the ordinary gated-outflow phase (head, siphon, fracture,
    waste-hold laws unchanged), announcing "Latch X opens (pool P >=
    level L)."; the announcement is per-tick while charged, the same
    grammar as the sill's per-tick "sill reached" line. FAIL: the
    inflow lands ("Latch X holds pool P below level L; pooling.") and
    THE POOL KEEPS. A latch NEVER STARVED-spills: the sill drains its
    pool on the first dry tick (cycle-4 finding 6), the latch is that
    pin's standing contrast. A charged latch discharges on a dry tick
    (deliver-on-gate, keep-on-dry): it is the only gate whose verdict
    can pass with zero inlets. Below level on a dry tick it is SILENT
    (no state change, no event; the pool is state, not an event
    stream). What it computes: an integrator with a release threshold
    (charge to L, drain at outflow cap), a hysteresis floor of L-1
    (the residual a full discharge always leaves), a regulator under
    continuous feed (throughput caps at outflow cap per tick, the
    excess is stored, never spilled), and with a rotor feeding it, a
    DIVIDER (the rotor sets the division, one charge per k swirl
    emissions; once ramped the latch passes one unit per charge, per
    the cycle-5 divider pin's trace). Latch chains are
    pipelines of integrators: each stage delivers its pool minus the
    L-1 floor, so a charged chain carries state between reads, which
    is the rung where rotor + latch start computing finite-state
    machines. A latch's gate reads only deferred inlets and its pool;
    committed deliveries (a gate's or vortex's outflow landing
    directly) charge it without a verdict, the same shape as the
    vortex-into-xor committed landing (cycle 3, finding 2).
    Deterministic, zero RNG, R8 rides _receive as everywhere.
  - Ripple counter + difference detector (2026-10-13, mariner cycle 6,
    composition laws over the kinds above; receipt
    watch/inbox/mates_leave_protocol/receipts/receipt_20261013_mariner.md;
    no new kinds, zero engine bytes): (1) a chain of k=2 vortices, each
    stage's first outlet a digit sink and its second outlet the next
    stage, is a BINARY RIPPLE COUNTER. Fed one unit per tick, rot_i =
    bit i of the tick count T (pinned: T=13 reads rot 1,1,0,1 = 1101),
    the digit sinks hold the divided streams (7, 3, 2, 1 after 13
    ticks), and a tick's cascade length is the new count's trailing
    ones + 1: the carry crosses every stage within ONE tick (full
    cascade exactly on the powers of two). The count is pure state:
    close the feed mid-run, nothing moves, and the resumed end state
    is byte-identical to an unbroken run. (2) COMMITTED-LANDING
    INTERFACE LAW: vortex and gate outflows are committed _move
    deliveries, while a gate's verdict reads only DEFERRED inlets
    (plain-source pipes); a rotor feeding a gate directly can never
    pass its verdict, the landed units pool and STARVED-spill on the
    first inlet-free tick (pinned: 6 ticks, waste 5, one stranded, no
    pass line ever). The plain PULSE TANK, a one-unit plain node
    between rotor and gate, re-enters the train into the verdict
    economy one tick later: the rotor-to-gate adapter. (3) with two
    tanked wheels, one xor, and a level-1 latch carrying a
    head-blocked outflow, the graph is a DIFFERENCE DETECTOR: the
    latch's pool accumulates exactly the ticks where exactly one wheel
    delivered. Phase-locked wheels hold the pool at 0 forever
    (agreement is silence; the double-fire volume reads at the waste,
    12 in 12 ticks); k=2 vs k=3 drift accumulates pool 6 with
    coincidence waste 4 in 12 ticks.
  - THE BOILER'S TOLL (2026-10-15, mariner cycle 9, composition laws,
    receipt watch/inbox/mates_leave_protocol/receipts/
    receipt_20261015_mariner.md; no new kinds, zero engine bytes): the
    steam lift is the engine's only uphill route (the DAG law) and it
    is actuated, never autonomous. Six laws, probed then pinned:
    (1) THE SHOVEL ECONOMY: on a cap-1 descent a BATCH lift (one
    boil(node, k)) and a STREAM lift (k acts of 1) deliver their last
    unit on the SAME tick - the crown drains at its outflow cap after
    the rain lands, so the actuation count is the whole cost (1 vs 4
    on a 4-unit lift, both boards pinned); the cold crown is a FREE
    BUFFER: a cold node is a plain accumulator, it never spills and
    never starves, so batching is pure savings. (2) THE ONE-BUS SKY:
    every cloud condenses at the ONE highest cold node (max by
    elevation), so a lower cold crown is SHADOWED while any higher
    exists: two basins under crowns at elevations 8 and 10, boil both,
    the 8-crown stays 0 forever and the 10-crown drinks all 3 (pinned).
    Route lifts by crown elevation, never by basin proximity.
    (3) THE DEAD LIFT: boiling the top cold node itself is a one-tick
    no-op round trip (the steam condenses back into the same node
    before the pipes move): end volumes byte-match a no-boil control;
    the only trace is the extra "Steam condenses" line (pinned).
    (4) THE LATCH-GATED WEATHER: the first circuit where engine STATE,
    not physics, throttles the sky: rotor drips (committed landings)
    charge a level-2 latch, the operator reads the verdict at end of
    tick T and shovels between T and T+1, the rain condenses at T+1
    and the crown drains the SAME tick (verdict-to-rain latency: one
    act plus one tick). The verdict LAGS the pool: a rotor landing
    commits AFTER its tick's verdict phase, so the first open reads
    one tick after the pool reaches level (pool 2 at t4, first open
    t5; exact event lists pinned). On the pinned board shovels ==
    opens == delivered (2 == 2 == 2): when the feed died the latch
    went silent and the shovel stopped - the state, not the physics,
    gates the weather. (5) THE WORLD VERB LAYER has ZERO lift
    latency: a staged boil applies at tick start, before condense, so
    one tick row carries both the boil line and the rain line
    ("boils 1 at spring; it rises." + "Steam condenses at crown
    (+1)."); same-beat shovels merge in the origin node into one rain
    line (+2) (pinned through MountainWorld stage/tick). (6) THE PHASE
    FLIP AND THE FORGETFUL MASS: a plain two-hop leg (tankB -> tankB2
    -> X) chains SAME-TICK (+0) when the inlet hop precedes the outlet
    hop in pipe insertion order, and is a ONE-TICK DELAY (+1) when the
    outlet hop is created first: same topology, one dict order apart,
    and the whole drift signature moves (B's passes t5,t11 -> t3,t9;
    the hold ticks name the offset: zero-lag holds t2,t8, B-lagged
    t6,t12, A-lagged t5,t11). But the DRIFT MASS FORGETS IT: zero-lag,
    +0-chained, B-lagged and A-lagged boards all end pool 6 waste 4
    after the 13-tick window; only the accrual tables differ tick by
    tick ([0,0,0,1,2,...] vs [0,1,2,3,...] vs [0,1,2,2,...]): the
    offset is readable MID-WINDOW and only mid-window. A solo
    xor-latch leg is a marginal counter (one train's delivery count).
    Signed detection in this engine is a WINDOWED read, never a
    completed total.
  - THE THERMOSTAT (2026-10-16, mariner cycle 10, composition laws,
    receipt watch/inbox/mates_leave_protocol/receipts/
    receipt_20261016_mariner.md; no new kinds, zero engine bytes):
    the closed weather loop (drain -> waste -> boil -> crown ->
    receiver -> drain) whose only input is the operator's shovel.
    Six laws, probed then pinned: (1) THE PRIME: a governor wheel
    (waste basin, cold crown, a latch L, a crown->L sense leg, an
    L->waste return leg) starts only on an UNCONDITIONED first act:
    the latch cannot open before the first lift, so a serve loop
    that waits for an open before the first shovel never starts
    (pinned: 3 ticks, zero events). (2) THE SERVE LAW: after the
    prime, serving one shovel per "Latch L opens" line runs the
    wheel at one four-line tick per act ("Steam condenses at crown
    (+1)." / "cl: 1 crown->L." / "Latch L opens (pool 1 >= level
    1)." / "ol: 1 to waste at waste."), shovels == opens == turns,
    the sump rides [B-1, B], and total mass never moves: the steady
    state HOLDS A LEVEL and spends acts, not water. Stop serving and
    the wheel parks one MOMENTUM tick later (the in-flight steam
    still turns it once), then silent and byte-stable at the birth
    state (waste B, crown 0, L 0). (3) THE SETPOINT: the latch's
    sill is the dial: sill 1 rides the sump at [B-1, B], sill 2 at
    [B-2, B-1] (pinned: B=3, sill 2 holds [1,2], the wheel starts
    one tick later and the park SLEEPS CHARGED at pool sill-1); a
    HALF prime (the missing residual) restarts the parked wheel at
    full period on the next tick: the residual is the phase. (4)
    THE WHEEL RATE IS THE SENSE LEG: over-shoveling (batch 2 per
    open) does not speed the wheel: the cap-1 sense leg keeps the
    turns at one per tick, the surplus pools at the cold crown
    (1->4 over four served ticks), the sump drains to 0, and at
    sump 0 the circuit converges to the honest wheel (shovel 1 ==
    return 1: pure recirculation). After the shovel dies the wheel
    keeps turning on the crown's stock, one momentum tick per
    stored unit (pinned: 4 stored, 4 ticks), and the over-shoveled
    board still parks at its birth state: the sky spends itself
    last, and nothing is ever lost. (5) RAIN CHARGES THE LATCH
    (cycle-7 residual g, closed): a cold crown placed ABOVE a latch
    feeds it through its drain: condense at the crown, the drain
    probes the gate deferred, the latch pools to its level and
    opens (batch lift of 3 at sill 2: hold pool 1, open, open,
    silent at pool 1; the discharge residual is the level-minus-1
    hysteresis floor). The latch itself can never be the crown:
    kind "latch" is not "cold", the condense target never lands in
    it directly. (6) THE LAP IS PIPE ORDER: the recirculation lap
    (receiver -> drain -> waste -> shovel -> crown -> receiver) is
    ONE tick when the crown leg is created before the drain leg
    (the rider lands and chains straight to waste, +0) and TWO
    ticks when the drain leg is created first (the rider rests at
    the receiver one tick, +1): same topology, one dict order
    apart, one act per lap either way, conserved at every lap
    boundary. Zero losses on every board in the pin set: saturation
    is the only deletion port in the engine and none of these
    boards reach it.
  - THE WINDING CLOCK (2026-10-17, mariner cycle 11, composition laws,
    receipt watch/inbox/mates_leave_protocol/receipts/
    receipt_20261017_mariner.md; no new kinds, zero engine bytes): the
    cold crown is a WINDED DELAY LINE: units stored in the sky are ticks
    of autonomous wheel rotation after the shovel dies. Four laws,
    probed then pinned: (1) STORE-THEN-COUNT: one batch lift of N at
    the basin on an unprimed governor wheel (serve never started), and
    the wheel opens EXACTLY N times: tick 1 carries the merged condense
    +N plus the first turn, ticks 2..N the bare three-line wheel, tick
    N+1 silent, park at the birth state (pinned N = 0, 1, 3, 5; N=5
    reads condense +5, five opens t1-t5, silent t6-t7, waste back at
    its birth level, conserved throughout). The sky holds a number.
    (2) THE CLOCK CANNOT READ THE SHOVEL: a batch wind (one
    boil(node, N)) and a stream wind (N acts of boil(node, 1), all
    before any tick) drive BYTE-IDENTICAL clock runs, every event list
    equal for the whole window (the shovel-economy law's whole-run
    form: the physics sees steam totals, never act counts). (3) THE
    BAND: the sense leg's cap sets WHERE the surplus waits, never the
    wheel's rate. Steady one-shovel serve, cap-2 leg under a sill-2
    latch vs the cap-1 control: the four-line steady shape is
    identical, but the RAMP differs (the wide leg carries the whole
    prime through on tick 1: the latch opens on the first tick, no
    HOLD; the narrow leg parks the ramp unit at the crown forever, a
    hostage, and the sump rides one unit lower: [1, 2] vs [2, 3] on
    B=4). Under a wind the wide leg moves the buffer INSIDE the latch
    (THE BALLOON): crown never parks, the pool balloons +1 per tick
    over the drain cap, the open run is UNBROKEN from first open
    through sky-death to balloon-drain (pinned: B=6, prime 2, three
    batch-2 shovels, opens t1-t7, pool 1->2->3->4 then drains 4->1,
    park asleep at the sill-1 floor; the cap-1 sill-1 control spends
    the same 8 units as 8 opens from crown stock and parks at the
    birth state: the floor is the difference, the balloon's 8th unit
    never opens and is never lost). (4) THE WORLD-VERB WIND: the world verb layer
    (server/world.py: staged acts apply at tick start, before
    condense) winds the win meter zero-latency: two same-beat staged
    pairs at the spring read crown 2 then crown 4, each beat carrying
    two boil lines and ONE merged rain line (+2) in the same tick row,
    winner flips true on the crossing beat, the mountain's own
    gravity lines ride alongside, board conserved 8 at every tick
    (pinned through MountainWorld.tick; four single-act beats to the
    same win were already pinned by the v0 server suite).
  - THE READING GLASS (2026-10-18, mariner cycle 12, composition laws,
    receipt watch/inbox/mates_leave_protocol/receipts/
    receipt_20261018_mariner.md; no new kinds, zero engine bytes):
    the balloon holds (wind minus drain) as readable state, so the
    clock can read itself back. Five laws, probed then pinned:
    (1) THE DROPPER GAUGE: a cap-1 tap leg from a ballooned pool into
    a reader latch (sill 1) whose outflow is a counter sink. THE
    GAUGE CLAMPS THE BALLOON: a tap open from birth converts the
    integrator into a pass-through wire (the pool rides [2 at
    verdict, 0 after outflow] on the pinned 2-in board; on 8 wound
    units the tap passes 4 while the open drain takes 4 back: the
    sink counts the wind's balance over the drain). With the drain
    shut the store pools net +1/tick and the tap reads it live; the
    sink ends at wind minus the floor (5 of 6 on B=6, sill 2). THE
    STORED READ: wind with the tap shut, then open the valve: the
    tap emits 1/tick while the pool stays at or above level, and the
    floor (level minus 1) is the blind spot: a stored 6 reads as 5
    at sill 2; a sill-1 balloon reads the full 6 to pool 0. The
    resolution is the balloon's OWN sill, never the tap's.
    (2) THE 2-TICK LATENCY: a gate's outflow into a gate is a
    COMMITTED LANDING (the cycle-6 interface law), so the reader's
    verdict never sees same-tick inflow: a tap unit leaves at T and
    the sink reads it at T+1, one tick per gate hop, structural.
    The reader outlives the wind by one tick: its afterbeat drains
    on the first silent tick (pinned: sink's 4th unit arrives on the
    tick after the last served tick).
    (3) THE PARK FORGETS THE STORAGE SITE: B=8, sill 2, prime 2 plus
    three 2-shovels: the cap-1 hostage board (crown parks the ramp
    unit, cycle 11) and the cap-2 balloon board end IDENTICAL
    (waste 7, crown 0, pool 1) with the SAME open count (7: the
    narrow board's t1 HOLD line is not an open), yet their accrual
    tables are disjoint (crown stock 1,2,3,4,3,2,1,0 vs 0 forever;
    pool flat 1 vs 1,2,3,4,3,2,1; waste tables differ t1-t7): the
    sky-stock and the pool-stock are unreadable at the park and
    readable only mid-window (cycle 9's windowed law, fed by the
    balloon; the wide board also parks one tick sooner: t8 vs t9).
    (4) THE CEILING IS THE BALLOON'S ONLY PORT: a latch pool grown
    to VOLUME_SAT absorbs the next inflow with the named amount
    (pinned: 1 absorbed at the ceiling 9223372036586340), its
    verdict still passes (the open line carries the 16-digit pool),
    and the drains pull it straight back down (SAT, SAT-1, SAT-2 on
    a cap-1 drain): the ceiling is a clamp, not a freeze. Mass loss
    across the pinned window is exactly the named absorbed unit:
    the only deletion port in the engine, and none of the other
    reading-glass boards touch it.
    (5) THE READ IS A DRAIN: every moving tap needs head (src.elev
    strictly above dst.elev): uphill and equal-elevation taps move
    zero forever, so NO non-destructive read exists in the engine;
    the head law is the privacy law. A tap always consumes its
    specimen down to the floor.
  - THE BANKED GOVERNOR (2026-10-20, mariner cycle 13, composition
    laws, receipt watch/inbox/mates_leave_protocol/receipts/
    receipt_20261020_mariner.md; no new kinds, zero engine bytes):
    the reading glass closes the loop, so the wheel spends banked
    wind without the operator: the reader's pulse train (one open
    per stored unit) drives the world-verb layer's staged boils,
    one shovel per "Latch R opens" line, the cycle-10 serve law's
    trigger moved from the store's verdict line to the gauge line.
    Seven laws, probed then pinned:
    (1) THE GAUGE-LINE SERVE: one prime shovel, then one shovel per
    reader open, runs the wheel unattended at one serve per TWO
    ticks: the reader's verdict lag stretches the period but eats
    nothing (bank 6, sill 1: prime at t1, chases at t3,t5,t7,t9,t11,
    reader opens t2,t4,t6,t8,t10,t12, the sink ends at 6, the bank
    is empty, silence from t13). The first serve is never eaten:
    the prime is unconditional, the train chases it at period 2.
    (2) THE PRIME LAW HOLDS AT THE GAUGE: a sub-level prime strands
    the bank: one shovel under a sill-2 store pools 1 and holds,
    zero reader opens fire, the governor never starts (7 ticks,
    zero serves, bank 5 stranded; pinned).
    (3) THE FLOOR TAX: the primed sill-2 governor serves N-1 and
    parks the level-1 blind spot in the store (bank 6, prime 2:
    5 serves, the store sleeps at pool 1); the 2-prime through the
    cap-1 sense leg also parks one hostage at the crown for one
    tick, so the wheel starts at t2, not t1 (first open t3).
    (4) THE DRY KNOCK: the train always asks one serve past the
    bank: the last reader open stages a shovel the empty basin
    rejects at stage time (DRY_POOL): exactly 1 rejected knock on
    every spent bank (pinned at sill 1 and sill 2 alike).
    (5) THE ORDER IS THE METER: on the live-wire board with a
    cap-2 tap the drain-first insertion order keeps the balance
    split (4 of 8 to the sink: the drain takes its unit first, the
    tap passes min(cap, remainder), the cap is invisible behind
    the order), while the tap-first order meters the FULL stream
    (8 of 8) and the reader balloons +1/tick while the wind lasts
    (pool 2,3,4,5), draining the backlog 1/tick after the wind
    dies: the reader outlives the wind by the whole backlog (the
    sink's last unit 5 ticks after the last served tick).
    (6) THE METER'S FLOOR: the store read's terminal pool is the
    first value below the level in the descent bank, bank-cap,
    bank-2cap, ...: a cap-1 tap floors at level-1 regardless of
    the bank (stored 6 reads 5), a cap-2 tap reads past that
    floor to the bank's residue mod the cap (stored 6 reads 6,
    opens at 6, 4, 2; stored 5 reads 4; stored 7 reads 6; the
    level-1 residue sleeps).
    (7) THE CROSS-ENGINE VERDICT: the governor board runs both
    engines (tools/rule_parity harness, the Godot twin headless):
    12 ticks, per-tick state hashes and verdict rows identical,
    including a reject:RATE_CAP row (the receipt ladder's per-tick
    action cap ate the second prime) both engines agree on; ladder
    parity holds on a composition board, not just the stress
    family (end state waste 0, store 1, reader 1, sink 4, the
    fifth serve's unit in flight).
  - THE ORBIT (2026-10-23, mariner cycle 14, composition laws, receipt
    watch/inbox/mates_leave_protocol/receipts/receipt_20261023_mariner.md;
    no new kinds, zero engine bytes): the skyrmion seed's TRAP half,
    the one shape the rotor line never built. A vortex whose outlets
    all RETURN to the basin closes a recirculation lap (waste basin ->
    cold crown -> vortex hub -> outlet legs -> waste) and the lap is
    the engine's first mass-free computer. Six laws, probed then pinned
    in tests/test_water_graph_orbit.py:
    (1) THE ORBITAL CLOCK: one shovel per wheel emission runs the wheel
    at ONE TURN PER TICK for as long as the operator serves: serves ==
    turns == ticks, mass exactly B at every tick boundary, rot = serves
    mod k. The serve key is the OUTLET PIPE NAME, never the arrow
    grammar: a returning leg's line reads "ra: 1 to waste at waste."
    (the waste-hold wording), so a serve keyed on "src->dst" never
    fires on the lap leg and the wheel dies after the prime (probed:
    1 serve, silence from t2; pinned as the arrow-key control). The
    clock never knocks dry: the both-return lap returns everything
    (world-verb run: 12 served ticks, 13 serves, 0 rejects; contrast
    THE DRY KNOCK of the banked governor, which always asks one serve
    past the bank).
    (2) THE ORBIT'S SHAPE: the return depths are the waveform. Legs of
    depth 1 (direct) and depth 2 (one rest tank) alternate the basin
    between the full bank (odd ticks) and bank-1 with one unit parked
    in the rest tank (even ticks): the register's phase is readable
    from outside as the basin's refill cadence.
    (3) THE SKY MOD K: a batch wind of N (one boil(waste, N), no serve)
    turns the wheel EXACTLY N times over N ticks (the crown drains at
    cap 1/tick), the last rest tank drains one tick later, and the
    park is BYTE-IDENTICAL TO BIRTH except rot = N mod k (pinned N=5
    reads rot 2, N=6 reads rot 0 on the k=3 board): the graph computed
    a modulus and spent no water. Every descent counter consumed its
    stream (the ripple counter's digit sinks hold the divided water);
    the orbit's counter is mass-free.
    (4) THE DAMPED ORBIT: one export leg among k leaks the trap at one
    unit per k turns. Bank B spends in exactly 2B turns at k=2 (8
    serves == 8 turns at B=4, sink 4, waste 0, rot back at birth
    because 2B mod 2 == 0); the train asks one serve past the empty
    basin exactly once (silent at the engine layer, a rejected
    DRY_POOL stage in the world layer).
    (5) THE PARK IS THE BIRTH STATE: stop staging serves and the wheel
    turns ONE momentum tick on the in-flight staged serve (t13 after a
    12-served window), then silent: the park is byte-identical to
    birth except the register (rot 1 after 13 turns). The orbit's only
    witness is the rotor position.
    (6) THE CROSS-ENGINE ORBIT: the board runs both engines via the
    rule_parity harness, the FIRST vortex-kind sequence the instrument
    has run (no vortex node appears in any generator family or prior
    parity test): 8 boil frames, per-tick state hashes and verdicts
     identical, all ack, end waste 3 and rest tank 1. NAMED LIMIT
     (cycle 14): the parity state hash covered elev, kind, sill,
     volume, steam but NOT rot, so the harness proved volume and
     verdict parity, never register parity. CLOSED cycle 15
     (2026-10-24, THE REGISTER ON THE WIRE, receipt
     receipt_20261024_mariner.md; instrument bytes, zero engine
     bytes): the hash ends at rot on both sides
     (tools/rule_parity.py canonical_state_text + the runner's
     _state_hash), the state-field diffs carry rot, and both
     ingestion paths install a spec's initial register
     (HarnessWorld.add_node + the runner's add_node), so a twin that
     agreed on every volume while rotating its wheel differently now
     reads parity-false, and an orbit board can start at a nonzero
     register across the wire.
  - Int domain (R8, 2026-09-30, watch/inbox/last_mile_20260930/
    R8_INT_DOMAIN.md): Python ints are unbounded, GDScript ints are 64-bit;
    the depth product `volume * DEPTH_SCALE` (mag/hydrology.py HydroNode and
    water_graph.gd HydroNode.depth, the render layer's to_dict included)
    crosses 2^63 silently in the Godot twin on mega-volume boards while
    Python computes it exactly. POLICY: the volume domain is BOUNDED at
    VOLUME_SAT — derived so `volume * DEPTH_SCALE` and
    `elev * HEAD_SCALE + depth` both stay inside signed int64 for any
    in-domain board — and EVERY increment flows through one saturating
    receiver that CLAMPS at the ceiling and NAMES the absorbed amount
    ("Node X SATURATES: ..."). Saturation is policy-declared deletion with
    a sensor, never a silent wrap. Ingestion (add_node) clamps into the
    domain (construction has no event stream yet); elevation clamps at
    ELEV_SAT. hydrology.py needs no change: its formulas are int64-safe by
    construction once the domain holds at every increment site here.

Deterministic: insertion-ordered pipes, integer volumes, no floats, no RNG.
$0, stdlib. water_computer delegates its gravity tick here when a campaign
seeds a graph spec; legacy 3-tank mode is untouched (its tests are the
regression suite for the old path).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --------------------------------------------------- int domain (R8) ----
# R8 INT DOMAIN LAW (2026-09-30, receipt watch/inbox/last_mile_20260930/
# R8_INT_DOMAIN.md). Python ints are unbounded; GDScript ints are 64-bit.
# The deepest integer product in the estate is depth = volume * DEPTH_SCALE;
# past INT64_MAX // DEPTH_SCALE the Godot twin wraps silently while Python
# computes exactly — a cross-engine divergence with no crash and no sensor.
# The law bounds the volume domain so NO derived product can cross 2^63 in
# EITHER language: volume <= VOLUME_SAT keeps volume*DEPTH_SCALE in int64
# even at cross_section 1, and elev <= ELEV_SAT keeps the hydrology head
# (elev*HEAD_SCALE + depth) in int64 with room to spare. Both scales mirror
# mag/hydrology.py (pinned equal by tests/test_water_graph_int_domain.py).
INT64_MAX = (1 << 63) - 1        # 9,223,372,036,854,775,807
DEPTH_SCALE = 1000               # milli-depth per volume unit (hydrology mirror)
HEAD_SCALE = 256                 # Q8 head units per elevation unit (mirror)
ELEV_SAT = 1 << 20               # elevation domain ceiling (1,048,576 units)
VOLUME_SAT = (INT64_MAX - ELEV_SAT * HEAD_SCALE) // DEPTH_SCALE
# -> 9,223,372,036,586,340 (~9.223e15); the literal is pinned by test.


def name_hash(s: str) -> int:
    """djb2 32-bit string hash — the fracture threshold's entropy source.
    Python's builtin hash() is salted per process (PYTHONHASHSEED), so it
    could never be deterministic across runs NOR agree with the Godot
    mirror; this loop is byte-identical to water_graph.gd's name_hash().
    Still zero RNG: same name -> same threshold, always, everywhere."""
    h = 5381
    for ch in s:
        h = ((h * 33) + ord(ch)) & 0xFFFFFFFF
    return h


def fracture_threshold(pipe_name: str) -> int:
    """Volume a pipe survives at full bore: 200 + hash(name) % 201 ->
    [200, 400] VOLUME units (B1 2026-09-30, B1_FRACTURE_REACH.md): stress is
    cumulative throughput, so the threshold is denominated in volume — a
    cap-1 pipe bursts after 200-400 ticks of sustained full bore (the
    operator's window), a cap-k pipe after threshold/k. The old band
    120 + hash%240 had no design anchor (AJ4 finding 2: unreachable)."""
    return 200 + name_hash(pipe_name) % 201


@dataclass
class Node:
    name: str
    elev: int = 0
    kind: str = "plain"          # plain | xor | sill | cold | waste | vortex | latch
    sill: int = 0                # for kind == "sill"
    volume: int = 0
    steam: int = 0
    rot: int = 0                 # for kind == "vortex": rotor position in [0, k)


@dataclass
class Pipe:
    name: str
    src: str
    dst: str
    cap: int = 1                 # max units per tick
    siphon: bool = False
    crest: int = 2               # volume at src needed to prime (siphon only)
    primed: bool = False
    open: bool = True
    stress: int = 0              # AC2: cumulative full-bore load
    fractured: bool = False      # AC2: burst — closed forever


@dataclass
class WaterGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    pipes: dict[str, Pipe] = field(default_factory=dict)
    tick_count: int = 0

    def add_node(self, name: str, elev: int = 0, kind: str = "plain",
                 sill: int = 0, volume: int = 0, steam: int = 0,
                 rot: int = 0) -> Node:
        # R8 INT DOMAIN LAW: ingestion clamps into the declared domain so
        # `volume <= VOLUME_SAT` holds before the first tick (and with it,
        # volume*DEPTH_SCALE can never wrap the 64-bit GDScript twin).
        # steam and rot ride the same clamp: steam shares the volume
        # domain, rot is kept in [0, k) at runtime so the ingestion
        # ceiling only guards a hostile spec. Construction-time
        # saturation is silent BY DESIGN — there is no event stream yet;
        # the runtime sensor fires in _receive().
        n = Node(name=name, elev=max(-ELEV_SAT, min(ELEV_SAT, elev)),
                 kind=kind, sill=sill, volume=min(volume, VOLUME_SAT),
                 steam=max(0, min(VOLUME_SAT, steam)),
                 rot=max(0, min(VOLUME_SAT, rot)))
        self.nodes[name] = n
        return n

    def add_pipe(self, name: str, src: str, dst: str, cap: int = 1,
                 siphon: bool = False, crest: int = 2, open_: bool = True,
                 primed: bool = False, stress: int = 0,
                 fractured: bool = False) -> Pipe:
        for node in (src, dst):
            if node not in self.nodes:
                raise KeyError(f"unknown node {node!r}")
        p = Pipe(name=name, src=src, dst=dst, cap=cap, siphon=siphon,
                 crest=crest, open=open_, primed=primed, stress=stress,
                 fractured=fractured)
        self.pipes[name] = p
        return p

    def open(self, pipe_name: str) -> None:
        # AC2 (2026-09-30): a FRACTURED pipe is closed for good — the valve
        # verb routes through here (server/world.py _apply, dataset
        # engine_apply) and must NOT be able to reopen a burst pipe.
        # Valve-honesty law (2026-10-10, receipt receipt_20261010_mariner.md):
        # the refusal stays silent HERE on purpose; both valve call sites
        # (server/world.py _apply, water_computer._graph_set_valve) check
        # fractured FIRST and word the burst, so no event row ever claims
        # an open the engine refused (cycle 1 finding 4: the hash-chain
        # lie, probed on both paths).
        if self.pipes[pipe_name].fractured:
            return
        self.pipes[pipe_name].open = True

    def close(self, pipe_name: str) -> None:
        self.pipes[pipe_name].open = False

    # ------------------------------------------------------------- steam ----
    def boil(self, node_name: str, units: int = 1) -> int:
        """Lift volume to steam at a node (heat is a routing medium: steam
        ignores pipes and condenses at the highest cold node)."""
        n = self.nodes[node_name]
        units = min(units, n.volume)
        n.volume -= units
        # R8: steam shares the volume domain (it condenses back into
        # volume); unbounded steam accumulation would overflow the GDScript
        # twin's int64 long before Python's unbounded ints noticed.
        n.steam = min(VOLUME_SAT, n.steam + units)
        return units

    # -------------------------------------------------- int domain (R8) ----
    def _receive(self, node: Node, gain: int, events: list[str]) -> None:
        """R8 INT DOMAIN LAW receiver: every volume increment lands here (or
        at the add_node/boil ingest clamps) so `volume <= VOLUME_SAT` holds
        on every tick and volume * DEPTH_SCALE can never cross 2^63 in
        EITHER engine. A gain that would cross the ceiling CLAMPS and NAMES
        the absorbed amount — policy-declared deletion with a sensor (the
        same honesty as FRACTURES/STARVED), never a silent wrap. In-domain
        arithmetic is overflow-safe by construction: both operands stay
        <= VOLUME_SAT, so the sum and the absorbed amount fit int64 in the
        GDScript twin."""
        if gain <= 0:
            return
        room = VOLUME_SAT - node.volume
        if gain <= room:
            node.volume += gain
            return
        node.volume = VOLUME_SAT
        events.append(f"Node {node.name} SATURATES: {gain - room} absorbed "
                      f"at the volume ceiling {VOLUME_SAT} "
                      f"(int64 depth domain, R8).")

    def _condense_steam(self) -> list[str]:
        events: list[str] = []
        colds = [n for n in self.nodes.values() if n.kind == "cold"]
        if colds:
            target = max(colds, key=lambda n: n.elev)
            for n in self.nodes.values():
                if n.steam:
                    self._receive(target, n.steam, events)
                    events.append(f"Steam condenses at {target.name} (+{n.steam}).")
                    n.steam = 0
        return events

    # --------------------------------------------------------------- tick ----
    def tick(self) -> list[str]:
        """One physics tick. Deterministic three-phase structure:
        (1) condense steam; (2) plain pipes + pipes INTO gated junctions
        (the inflow LEAVES the source at probe time — reserved, so sibling
        pipes from the same source cannot re-spend it — but does not LAND
        at the junction until the gate verdict); (3) evaluate junction
        gates (XOR/sill/latch) from committed inflow counts, commit or
        overflow, then
        run gated junctions' outflow pipes under their gate. Gated-junction
        outflow MUST wait for the gate — the first cut let the outflow pipe
        drain the junction in the same pass its inflows arrived (the XOR
        delivered on both-inlet ticks; caught by tests, 2026-09-27)."""
        self.tick_count += 1
        events: list[str] = list(self._condense_steam())

        gated_kinds = ("xor", "sill", "latch")
        out_kinds = gated_kinds + ("vortex",)
        deferred_in: dict[str, list[tuple[str, Pipe, int]]] = {}
        gated_out: list[Pipe] = []
        vortex_out: dict[str, list[Pipe]] = {}

        for p in self.pipes.values():
            if p.fractured or not p.open:
                continue
            src = self.nodes[p.src]
            dst = self.nodes[p.dst]
            if src.kind in out_kinds:
                gated_out.append(p)
                if src.kind == "vortex":
                    vortex_out.setdefault(p.src, []).append(p)
                continue
            if dst.kind in gated_kinds:
                flow = self._available(p, src, events)
                if flow:
                    # B1 SEAM FIX (2026-09-30, B1_FRACTURE_REACH.md): full-
                    # bore flow INTO a gated junction stresses the pipe AT
                    # PROBE TIME — the water left the source through the
                    # pipe section = wear. The AC2 cut loaded pipes only in
                    # _move, so the default Mountain's main artery (p_spring
                    # -> xor gate1) could NEVER burst (evidence: tests/
                    # test_water_graph.py B1 seam tests). On burst the flow
                    # sprays (conserved); the gate never sees the inlet.
                    if self._fracture(p, src, dst, flow, events):
                        continue
                    # NEG-VOLUME LAW (2026-09-29, LW5 deferred-inflow
                    # double-count): the deferred flow is RESERVED here, at
                    # probe time — else a sibling pipe from the SAME source
                    # re-spends it and the gate phase double-decrements src
                    # (pinned repros + 1000 seeded graphs, test_water_graph.py LW5 block).
                    src.volume -= flow
                    deferred_in.setdefault(dst.name, []).append((p.name, p, flow))
                continue
            self._move(p, src, dst, events)

        # junction gates: commit or overflow from the ACTUAL inflow count.
        # STARVATION LAW (2026-09-28, operator: "this whole starve-out thing
        # is bullshit and our water computer spec should have picked it up"):
        # a gated junction that receives inflow below its gate and then dumps
        # that water to waste is SILENT STARVATION — the network eats water
        # in the middle while looking like a gate. Two changes:
        #   (1) under-gate inflow is HELD (not spilled this tick) so a later
        #       tick can still reach the gate — a real sill pools water;
        #   (2) any HELD volume that overflows a LATER tick (new shape
        #       changed the verdict) emits a STARVED line naming the node,
        #       the held amount, and the gate — the sensor the spec lacked.
        gate: dict[str, int] = {}
        for name, node in self.nodes.items():
            if node.kind not in gated_kinds:
                continue
            ins = deferred_in.get(name, [])
            if node.kind == "xor":
                allow = (len(ins) == 1)
            elif node.kind == "latch":
                # LATCH LAW (cycle 5, 2026-10-12): the gate reads the POOL
                # (standing volume plus this tick's deferred inflow) against
                # the LEVEL in node.sill (clamped >= 1 like a sill
                # threshold). Only the latch can pass with ZERO inlets: a
                # charged latch discharges on a dry tick.
                allow = (node.volume + sum(flow for _, _, flow in ins)
                         ) >= max(1, node.sill)
            else:
                allow = len(ins) >= max(1, node.sill)
            gate[name] = 1 if allow else 0
            if allow:
                for pname, p, flow in ins:
                    self._receive(node, flow, events)  # R8; src decremented at probe (LW5)
                    events.append(f"{pname}: {flow} {p.src}->{name}.")
                if node.kind == "xor":
                    events.append(f"Junction {name} passes ({ins[0][0]} sole inlet).")
                elif node.kind == "latch":
                    events.append(f"Latch {name} opens (pool {node.volume} "
                                  f">= level {max(1, node.sill)}).")
                else:
                    events.append(f"Junction {name} sill reached ({len(ins)} inlets).")
            else:
                held_now = sum(flow for _, _, flow in ins)
                # hold the new inflow; pool with anything already held
                for pname, p, flow in ins:
                    self._receive(node, flow, events)  # R8; src decremented at probe (LW5)
                why = (f"{len(ins)} inlets" if node.kind == "xor"
                       else f"{len(ins)} < sill {node.sill}")
                if node.kind == "latch":
                    # THE MEMORY LAW (cycle 5): a below-level latch KEEPS
                    # its pool across dry ticks. No STARVED spill, ever:
                    # the pool is the state a graph carries between reads
                    # (the sill drains its pool on the first dry tick; the
                    # latch is that pin's standing contrast). Below level
                    # with no inflow the latch is silent: no state change,
                    # no event; the pool reads in the snapshot and glass.
                    if held_now > 0:
                        events.append(f"Latch {name} holds pool {node.volume} "
                                      f"below level {max(1, node.sill)}; pooling.")
                    continue
                if held_now > 0:
                    events.append(f"Junction {name} holds {held_now} below gate "
                                  f"({why}); pooling.")
                if node.volume > 0 and held_now == 0:
                    # gate failed again with NO new inflow: previously-pooled
                    # water is now dead weight. Spill it and NAME the starve.
                    # V5 ECONOMY LAW (2026-09-29, Z14 flaw: the STARVED spill
                    # zeroed volume with no destination while its event string
                    # claimed "spilled to waste" — slow starters permanently
                    # lost half the 8-unit economy). Fix: the spill ROUTES to
                    # the first waste node in insertion order, and waste HOLDS
                    # it as a boilable basin (boil from waste -> steam ignores
                    # pipes -> condenses at the highest cold node = recovery).
                    # Evidence: tests/test_water_graph_starvation.py V5 tests
                    # (waste holds, boil-from-waste recovers, conservation).
                    # No waste node in the graph: HOLD at the junction (never
                    # delete); the event names the hold so the sensor stays
                    # honest and the water stays boilable where it sits.
                    spill = node.volume
                    basin = next((n for n in self.nodes.values()
                                  if n.kind == "waste"), None)
                    if basin is not None:
                        self._receive(basin, spill, events)  # R8
                        node.volume = 0
                        events.append(f"Junction {name} STARVED: {spill} pooled units "
                                      f"spilled to waste at {basin.name} ({why}; no inflow "
                                      f"reached the gate; boil {basin.name} to recover them).")
                    else:
                        events.append(f"Junction {name} STARVED: {spill} pooled units "
                                      f"held at the junction ({why}; no inflow reached "
                                      f"the gate; no waste node to receive them).")

        # gated outflow under the gate
        for p in gated_out:
            if not gate.get(p.src):
                continue
            src = self.nodes[p.src]
            dst = self.nodes[p.dst]
            self._move(p, src, dst, events)

        # VORTEX rotor emissions (2026-10-10, mariner cycle 3, receipt
        # watch/inbox/mates_leave_protocol/receipts/receipt_20261010_mariner.md).
        # One outlet per vortex per tick: the LIVE pipe at index rot % k
        # in insertion order; delivery is ordinary _move (head, siphon,
        # fracture, waste-hold laws all apply unchanged); rot advances
        # ONLY when volume left through the chosen pipe, so a blocked or
        # dry outlet parks the rotor while a burst on its tick still
        # turned it (the water left the hub). Runs AFTER gate outflows so
        # a gate's committed delivery can land in the hub this tick
        # before the wheel turns; across vortices the order is first-
        # live-outlet pipe insertion order. Deterministic, zero RNG.
        for name, outlets in vortex_out.items():
            node = self.nodes[name]
            k = len(outlets)
            p = outlets[node.rot % k]
            before = node.volume
            self._move(p, node, self.nodes[p.dst], events)
            if node.volume < before:
                node.rot = (node.rot + 1) % k

        return events

    def _available(self, p: Pipe, src: Node, events: list[str]) -> int:
        """Flow a pipe into a gated junction would carry this tick (no commit)."""
        if src.volume <= 0:
            return 0
        dst = self.nodes[p.dst]
        head_ok = src.elev > dst.elev
        if p.siphon:
            if not p.primed:
                if src.volume >= p.crest and head_ok:
                    p.primed = True
                    events.append(f"Siphon {p.name} primes at crest ({p.crest}).")
                else:
                    return 0
            return min(p.cap, src.volume)
        if not head_ok:
            return 0
        return min(p.cap, src.volume)

    def _fracture(self, p: Pipe, src: Node, dst: Node, flow: int,
                  events: list[str]) -> bool:
        """AC2 pipe-fracture law (2026-09-30), B1 reach retune (2026-09-30).
        Full-bore flow (flow == cap) loads the pipe: stress += flow,
        cumulative VOLUME across ticks (a cap-k pipe wears k units per
        full-bore tick). When stress EXCEEDS 200 + hash(name) % 201 (= [200,
        400] volume — 200-400 ticks of sustained full bore on the all-cap-1
        default Mountain) the pipe bursts — closed forever — and THIS tick's
        flow sprays to the lowest-elevation node other than dst (first-min
        in insertion order; min() keeps the first tie) instead of
        delivering. Returns True when the burst happened (caller returns;
        volumes are already conserved: src -= flow, spray += flow)."""
        if flow != p.cap:
            return False
        p.stress += flow
        if p.stress <= fracture_threshold(p.name):
            return False
        p.fractured = True
        p.open = False
        src.volume -= flow
        spray = min((n for n in self.nodes.values() if n.name != dst.name),
                    key=lambda n: n.elev)
        self._receive(spray, flow, events)  # R8: even a burst's spray saturates
        events.append(f"Pipe {p.name} FRACTURES (stress {p.stress}): "
                      f"spray to {spray.name}.")
        return True

    def _move(self, p: Pipe, src: Node, dst: Node,
              events: list[str]) -> None:
        # Cycle-4 (2026-10-11): the `delivered` dict is gone. It was
        # write-only since the first cut (created, written at the plain
        # and gate-commit sites, never read by any engine or test; the
        # cycle-3 receipt named it a one-deletion reclaim). Event lines
        # carry the same provenance the dict pretended to keep.
        if src.volume <= 0:
            if p.siphon and p.primed:
                p.primed = False
                events.append(f"Siphon {p.name} breaks (intake dry).")
            return
        head_ok = src.elev > dst.elev
        if p.siphon:
            if not p.primed:
                if src.volume >= p.crest and head_ok:
                    p.primed = True
                    events.append(f"Siphon {p.name} primes at crest ({p.crest}).")
                else:
                    return
            flow = min(p.cap, src.volume)
        else:
            if not head_ok:
                return  # check valve: gravity-only, never uphill
            flow = min(p.cap, src.volume)
        if self._fracture(p, src, dst, flow, events):
            return  # AC2: burst — this tick's flow sprayed, not delivered
        src.volume -= flow
        if dst.kind == "waste":
            # V5 ECONOMY LAW (2026-09-29): waste HOLDS what it receives —
            # the old early-return skipped the accumulation, so every unit
            # piped to waste was deleted from the economy. Held waste is
            # boilable (steam ignores pipes, condenses at the cold crown),
            # so the drain is a basin, not a void.
            self._receive(dst, flow, events)  # R8
            events.append(f"{p.name}: {flow} to waste at {dst.name}.")
            return
        self._receive(dst, flow, events)  # R8
        events.append(f"{p.name}: {flow} {p.src}->{p.dst}.")

    # -------------------------------------------------------------- state ----
    def volume(self, node_name: str) -> int:
        return self.nodes[node_name].volume

    def to_spec(self) -> dict[str, Any]:
        # LATCH roundtrip law (2026-10-12, mariner cycle 5, receipt
        # receipt_20261012_mariner.md): to_spec never emitted `sill`, so a
        # bare spec roundtrip (snapshot() included; only the campaign path's
        # _save_graph overlay ever preserved it) silently reverted a latch's
        # LEVEL to 0, whose gate then evaluates at level 1. The level is
        # runtime-essential gate state for kind "latch" (like rot for the
        # vortex), so it rides to_spec under the additive-key family law
        # (steam, then rot, now sill; from_spec already passed it through).
        return {
            "schema": "water_graph.v1",
            "tick": self.tick_count,
            "nodes": {n: {"elev": v.elev, "kind": v.kind, "sill": v.sill,
                          "volume": v.volume, "steam": v.steam, "rot": v.rot}
                      for n, v in self.nodes.items()},
            "pipes": {p: {"src": v.src, "dst": v.dst, "cap": v.cap,
                          "siphon": v.siphon, "crest": v.crest,
                          "primed": v.primed, "open": v.open,
                          "stress": v.stress, "fractured": v.fractured}
                      for p, v in self.pipes.items()},
        }


def from_spec(spec: dict[str, Any]) -> WaterGraph:
    g = WaterGraph()
    for name, n in spec.get("nodes", {}).items():
        # Steam roundtrip fix (2026-10-10, mariner cycle 3, receipt
        # receipt_20261010_mariner.md): to_spec has emitted per-node
        # steam since the steam law landed, but from_spec never passed
        # it, so every roundtrip (estate_water_graph_tick included)
        # silently emptied steam to 0. Third member of the LW5 drop
        # family (primed, then stress/fractured, now steam). Masked in
        # stock play: world mode condenses the same tick it boils, and
        # campaign boils ride to_gas (water_computer), never graph.boil
        # across a save boundary. `rot` rides the same pass (the vortex
        # law's roundtrip half); add_node owns the R8 clamps.
        g.add_node(name, elev=int(n.get("elev", 0)),
                   kind=str(n.get("kind", "plain")),
                   sill=int(n.get("sill", 0)),
                   volume=int(n.get("volume", 0)),
                   steam=int(n.get("steam", 0)),
                   rot=int(n.get("rot", 0)))
    for name, p in spec.get("pipes", {}).items():
        # LW5 (2026-09-29): pass `primed` through — to_spec emitted it but
        # from_spec dropped it, so every spec roundtrip (estate_water_graph_
        # tick included) silently reverted a primed siphon to unprimed.
        # Evidence fixed-on: test_spec_roundtrip_preserves_siphon_primed_state.
        # AC2 (2026-09-30): `stress`/`fractured` ride the same law — a burst
        # pipe must survive the estate roundtrip closed, not resurrect open.
        g.add_pipe(name, src=p["src"], dst=p["dst"], cap=int(p.get("cap", 1)),
                   siphon=bool(p.get("siphon", False)),
                   crest=int(p.get("crest", 2)), open_=bool(p.get("open", True)),
                   primed=bool(p.get("primed", False)),
                   stress=int(p.get("stress", 0)),
                   fractured=bool(p.get("fractured", False)))
    g.tick_count = int(spec.get("tick", 0))
    return g
