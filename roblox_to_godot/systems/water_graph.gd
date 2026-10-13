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
    var kind: String = "plain"  # plain | xor | sill | cold | waste
    var sill: int = 0
    var volume: int = 0
    var steam: int = 0


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


func add_node(node_name: String, elev: int = 0, kind: String = "plain", sill: int = 0, volume: int = 0, cross_section: int = DEFAULT_CROSS_SECTION) -> void:
    # Z10: every node carries geometry (HydroNode); which head law reads it is
    # the `hydrology` flag, flippable mid-run. mag/hydrology.py raises
    # ValueError on cross_section < 1; the assert mirrors add_pipe's idiom.
    # R8 INT DOMAIN LAW: ingestion clamps into the declared domain (volume
    # <= VOLUME_SAT, |elev| <= ELEV_SAT) so the depth product can never wrap
    # this engine's int64. Construction-time saturation is silent BY DESIGN
    # — no event stream exists yet; the runtime sensor fires in _receive().
    assert(cross_section >= 1, "cross_section must be >= 1, got " + str(cross_section))
    var n = HydroNode.new()
    n.name = node_name
    n.elev = clampi(elev, -ELEV_SAT, ELEV_SAT)
    n.kind = kind
    n.sill = sill
    n.volume = mini(volume, VOLUME_SAT)
    n.cross_section = cross_section
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

    var gated_kinds := ["xor", "sill"]
    var deferred_in: Dictionary = {}  # node_name -> [{pipe, src, flow}]
    var gated_out: Array[WPipe] = []
    var delivered: Dictionary = {}  # node_name -> [pipe_names]

    for p: WPipe in pipes.values():
        if p.fractured or not p.open:
            continue
        var src: WNode = nodes[p.src]
        var dst: WNode = nodes[p.dst]
        if src.kind in gated_kinds:
            gated_out.append(p)
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
        _move(p, src, dst, delivered, events)

    # Junction gates
    var gate: Dictionary = {}
    for node_name: String in nodes:
        var node: WNode = nodes[node_name]
        if not (node.kind in gated_kinds):
            continue
        var ins = deferred_in.get(node_name, [])
        var allow: bool = (ins.size() == 1) if node.kind == "xor" else (ins.size() >= maxi(1, node.sill))
        gate[node_name] = 1 if allow else 0
        if allow:
            for entry in ins:
                # volume already reserved at probe time (D1 parity port);
                # the gate only DELIVERS it onward now. R8: saturating.
                _receive(node, entry.flow, events)
                if not delivered.has(node_name):
                    delivered[node_name] = []
                delivered[node_name].append(entry.pipe)
                events.append("%s: %d %s->%s." % [entry.pipe, entry.flow, entry.src, node_name])
            if node.kind == "xor":
                events.append("Junction %s passes (%s sole inlet)." % [node_name, ins[0].pipe])
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
        _move(p, nodes[p.src], nodes[p.dst], delivered, events)

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


func _move(p: WPipe, src: WNode, dst: WNode, delivered: Dictionary, events: Array[String]) -> void:
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
        if not delivered.has(dst.name):
            delivered[dst.name] = []
        delivered[dst.name].append(p.name)
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
        result["nodes"][name] = {"elev": n.elev, "kind": n.kind, "volume": n.volume, "steam": n.steam, "cross_section": n.cross_section, "depth": n.depth, "head": n.head}
    for name: String in pipes:
        var p: WPipe = pipes[name]
        result["pipes"][name] = {"src": p.src, "dst": p.dst, "cap": p.cap, "open": p.open, "primed": p.primed, "siphon": p.siphon, "stress": p.stress, "fractured": p.fractured} # B1.0 fix 2026-09-29: siphon was missing (game.gd _draw reads it); AC2 2026-09-30: stress/fractured mirror the engine's to_spec keys
    return result
