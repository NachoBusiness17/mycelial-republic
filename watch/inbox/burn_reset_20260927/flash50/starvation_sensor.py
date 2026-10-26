"""starvation_sensor.v1 -- the STARVED event, generalized to any resource-flow DAG.

Source of truth: mag/water_graph.py (the water engine), read this session.
The sensor carries the water engine's flow laws over 1:1:

  L1 direction    flow only downhill: src.elev > dst.elev (water_graph.py:203,223)
  L2 capacity     flow = min(p.cap, src.volume)          (water_graph.py:231,235)
  L3 gating       xor (exactly one inlet) / sill (>= N)  (water_graph.py:156-157)
  L4 hold+spill   under-gate inflow HELDS (:170-174); a pool dying with no new
                  inflow spills and is NAMED -- the STARVED law (:180-186)
  L5 crest        a node with batch_min serves only when buffered that high;
                  the siphon crest law (:204-211)
  L6 waste        a sink swallows, but NAMES what it swallows (:237-239)
  L7 conservation the sensor's own law (NEW, the generalization): every unit
                  removed from a node must surface as a NAMED op. Unnamed
                  loss is silent starvation -- the meta-pattern B2-443
                  measured live (896 model.network.failed events invisible
                  to tools/provider_error_tally.py).

Design doc: watch/inbox/burn_reset_20260927/flash50/deep-starvation-sensor.md
Deterministic, stdlib-only, no subprocesses (so no CREATE_NO_WINDOW needed),
no floats, no RNG. Run: .venv/Scripts/python.exe <this file>
"""
from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

# --------------------------------------------------------------- model ----

@dataclass
class FNode:
    name: str
    kind: str = "junction"      # source | junction | demand | sink | cold
    elev: int = 0
    volume: int = 0
    rate: int = 0               # source: units produced per tick
    demand_rate: int = 0        # demand: units served per tick once batch_min met
    batch_min: int = 0          # L5 crest: serve only when buffered this high
    gate: str = "none"          # L3: none | xor | sill
    sill: int = 0
    oob_to: str | None = None   # L6 steam: out-of-band lift target
    oob_rate: int = 0
    silent_spill: bool = False  # pre-law gate: spills pools WITHOUT naming (L4 violation)


@dataclass
class FEdge:
    name: str
    src: str
    dst: str
    cap: int = 1                # L2


@dataclass
class Op:
    """One volume-changing operation. named=False ops are what the sensor hunts."""
    node: str
    delta: int
    kind: str                   # produce|move_in|move_out|serve|spill|oob_lift|oob_land
    named: bool = True
    detail: str = ""


@dataclass
class FlowNet:
    nodes: dict[str, FNode] = field(default_factory=dict)
    edges: dict[str, FEdge] = field(default_factory=dict)
    tick_count: int = 0

    def node(self, name: str, **kw) -> FNode:
        n = FNode(name=name, **kw)
        self.nodes[name] = n
        return n

    def edge(self, name: str, src: str, dst: str, cap: int = 1) -> FEdge:
        for x in (src, dst):
            if x not in self.nodes:
                raise KeyError(f"unknown node {x!r}")
        e = FEdge(name=name, src=src, dst=dst, cap=cap)
        self.edges[name] = e
        return e

    def snapshot(self) -> dict[str, int]:
        return {n: v.volume for n, v in self.nodes.items()}

    def tick(self) -> tuple[list[str], list[Op]]:
        """One physics tick, same three-phase structure as water_graph.tick()
        (condense/defer/gate). Returns (event lines, op ledger)."""
        self.tick_count += 1
        t = self.tick_count
        events: list[str] = []
        ops: list[Op] = []
        gated = ("xor", "sill")

        def is_gated(n: FNode) -> bool:
            return n.gate in gated

        # 1. sources produce (L2: production is capped by nothing but rate)
        for n in self.nodes.values():
            if n.kind == "source" and n.rate > 0:
                n.volume += n.rate
                ops.append(Op(n.name, +n.rate, "produce"))
                events.append(f"t{t} {n.name} produces +{n.rate}.")

        # 2. out-of-band lifts (L6): units leave the metered DAG
        for n in self.nodes.values():
            if n.oob_rate > 0 and n.volume > 0:
                lift = min(n.oob_rate, n.volume)
                n.volume -= lift
                ops.append(Op(n.name, -lift, "oob_lift"))
                target = self.nodes.get(n.oob_to) if n.oob_to else None
                if target is not None and target.kind in ("cold", "sink"):
                    target.volume += lift
                    ops.append(Op(target.name, +lift, "oob_land"))
                    events.append(f"t{t} {n.name} lifts {lift} out-of-band to {target.name}.")
                else:
                    n.volume += lift  # no condenser: falls back (water_graph.py:21-22)
                    ops.append(Op(n.name, +lift, "oob_land", detail="fallback"))
                    events.append(f"t{t} {n.name} lift {lift} returns (no condenser).")

        # 3. plain edges + deferred inflows into gated nodes
        gated_out: list[FEdge] = []
        deferred_in: dict[str, list[tuple[FEdge, int]]] = {}
        for e in self.edges.values():
            src, dst = self.nodes[e.src], self.nodes[e.dst]
            if is_gated(src):
                gated_out.append(e)
                continue
            if src.volume <= 0:
                continue                       # intake dry (water_graph.py:200-201)
            if e.src == e.dst or not (src.elev > dst.elev):
                continue                       # L1 check valve: never uphill
            flow = min(e.cap, src.volume)      # L2
            if is_gated(dst):
                if flow:
                    # reserve at read time: a shared source must not be
                    # double-spent by N deferred pipes (water_graph commits at
                    # gate time instead, water_graph.py:172-174 -- latent
                    # over-drain there when 2+ pipes share one source)
                    src.volume -= flow
                    deferred_in.setdefault(dst.name, []).append((e, flow))
                    ops.append(Op(e.src, -flow, "move_out", detail="reserved"))
                continue
            if flow:
                src.volume -= flow
                dst.volume += flow
                ops.append(Op(e.src, -flow, "move_out"))
                ops.append(Op(e.dst, +flow, "move_in"))
                events.append(f"t{t} {e.name}: {flow} {e.src}->{e.dst}.")

        # 4. gate evaluation: commit or hold (L3/L4)
        gate: dict[str, int] = {}
        for name, nd in self.nodes.items():
            if not is_gated(nd):
                continue
            ins = deferred_in.get(name, [])
            allow = (len(ins) == 1) if nd.gate == "xor" else (
                len(ins) >= max(1, nd.sill))
            gate[name] = 1 if allow else 0
            if allow:
                for e, flow in ins:
                    nd.volume += flow          # src already paid at reservation
                    ops.append(Op(name, +flow, "move_in"))
                    events.append(f"t{t} {e.name}: {flow} {e.src}->{name} (gate open).")
            else:
                held_now = 0
                for e, flow in ins:
                    nd.volume += flow          # HOLD, not spill (water_graph.py:170-174)
                    held_now += flow
                    ops.append(Op(name, +flow, "move_in", detail="held"))
                if held_now > 0:
                    events.append(f"t{t} {name} holds {held_now} below gate "
                                  f"({nd.gate}); pooling.")
                if nd.volume > 0 and not ins:
                    spill = nd.volume          # pool dying with no inflow: L4 verdict
                    nd.volume = 0
                    if nd.silent_spill:
                        ops.append(Op(name, -spill, "spill", named=False))
                        # NO event line: the pre-law behavior the STARVED law killed
                    else:
                        ops.append(Op(name, -spill, "spill"))
                        events.append(f"t{t} {name} STARVED: {spill} pooled units "
                                      f"spilled ({nd.gate}).")

        # 5. gated outflow under the gate
        for e in gated_out:
            if not gate.get(e.src):
                continue
            src, dst = self.nodes[e.src], self.nodes[e.dst]
            flow = min(e.cap, src.volume)
            if flow and src.elev > dst.elev:
                src.volume -= flow
                dst.volume += flow
                ops.append(Op(e.src, -flow, "move_out"))
                ops.append(Op(e.dst, +flow, "move_in"))
                events.append(f"t{t} {e.name}: {flow} {e.src}->{e.dst} (gated).")

        # 6. demand consumption: the receipt
        for nd in self.nodes.values():
            if nd.kind == "demand" and nd.volume >= nd.batch_min and nd.volume > 0:
                serve = min(nd.demand_rate, nd.volume)
                nd.volume -= serve
                ops.append(Op(nd.name, -serve, "serve"))
                events.append(f"t{t} {nd.name} serves {serve} (receipt).")

        return events, ops


# -------------------------------------------------------------- sensor ----

@dataclass
class Finding:
    tick: int
    pattern: str                # STARVED|CREST_SPLIT|SUPPLY_CUT|COLLISION_LOSS|
                                # UNNAMED_LOSS|BUDGET_EXPIRED|OOB_DRAIN|STATIC
    node: str
    units: int
    detail: str

    def line(self) -> str:
        return (f"[t{self.tick}] {self.pattern:14s} node={self.node} "
                f"units={self.units} :: {self.detail}")


class StarvationSensor:
    """Observer over any FlowNet. Emits classified findings; every finding
    names the node, the units, and the tick (water_graph.py:149-150: 'the
    sensor the spec lacked')."""

    def __init__(self, net: FlowNet, split_patience: int = 3,
                 cut_patience: int = 3, deadline: int = 6):
        self.net = net
        self.split_patience = split_patience
        self.cut_patience = cut_patience
        self.deadline = deadline
        self.findings: list[Finding] = []
        self.split_strikes: dict[str, int] = defaultdict(int)
        self.split_base: dict[str, int] = {}     # volume when the current strike began
        self.unmet: dict[str, int] = defaultdict(int)
        self.src_dry: int = 0
        self.seen: set[str] = set()

    def _emit(self, t: int, pattern: str, node: str, units: int, detail: str,
              once: bool = True) -> None:
        key = f"{pattern}:{node}"
        if once and key in self.seen:
            return
        self.seen.add(key)
        self.findings.append(Finding(t, pattern, node, units, detail))

    def observe(self, before: dict[str, int], ops: list[Op]) -> list[Finding]:
        t = self.net.tick_count
        net = self.net

        # L7 conservation audit: every unit accounted, every loss NAMED
        for name, nd in net.nodes.items():
            delta = sum(o.delta for o in ops if o.node == name)
            actual = nd.volume - before[name]
            if delta != actual:
                self._emit(t, "ENGINE_BUG", name, delta - actual,
                           "ledger does not match volume delta")
            unnamed = sum(-o.delta for o in ops
                          if o.node == name and not o.named and o.delta < 0)
            if unnamed > 0:
                self._emit(t, "UNNAMED_LOSS", name, unnamed,
                           "units removed with no named event "
                           "(silent starvation witness)")

        per_node_in = defaultdict(int)
        per_node_served = defaultdict(int)
        for o in ops:
            if o.kind == "move_in":
                per_node_in[o.node] += o.delta
            elif o.kind == "serve":
                per_node_served[o.node] += -o.delta

        # demand deadline: a receipt this tick is proof of health even though
        # the serve empties the buffer back below batch_min
        for name, nd in net.nodes.items():
            if nd.kind == "demand":
                if per_node_served.get(name, 0) > 0:
                    self.unmet[name] = 0
                elif nd.volume >= nd.batch_min and (nd.volume > 0 or nd.batch_min == 0):
                    self.unmet[name] = 0
                else:
                    self.unmet[name] += 1
                    if self.unmet[name] == self.deadline:
                        pools = sorted(((v.volume, k) for k, v in net.nodes.items()
                                        if k != name and v.volume > 0), reverse=True)
                        where = (f"largest pool: {pools[0][1]} ({pools[0][0]})"
                                 if pools else "no resource anywhere")
                        self._emit(t, "BUDGET_EXPIRED", name, self.unmet[name],
                                   f"unmet {self.deadline} ticks; {where}")

        # crest split: fed but the threshold is provably unreachable -- volume
        # flat-or-falling across the whole strike window. Fed AND rising is
        # delay, not starvation; the strike resets on any progress.
        for name, nd in net.nodes.items():
            if nd.batch_min > 0:
                fed = per_node_in.get(name, 0) > 0
                below = nd.volume < nd.batch_min
                if fed and below:
                    base = self.split_base.get(name)
                    if base is None:
                        self.split_base[name] = nd.volume
                    elif nd.volume > base:     # progress: rising toward the crest
                        self.split_strikes[name] = 0
                        self.split_base[name] = nd.volume
                    self.split_strikes[name] += 1
                    if self.split_strikes[name] >= self.split_patience:
                        self._emit(t, "CREST_SPLIT", name, nd.volume,
                                   f"fed {self.split_strikes[name]} ticks, volume "
                                   f"never rises toward batch_min {nd.batch_min}")
                else:
                    self.split_strikes[name] = 0
                    self.split_base.pop(name, None)

        # supply cut: a live demand set with a dead source
        sources_alive = [n for n in net.nodes.values()
                         if n.kind == "source" and n.volume > 0]
        unmet_any = any(self.unmet[k] > 0 for k, v in net.nodes.items()
                        if v.kind == "demand")
        if unmet_any and not sources_alive:
            self.src_dry += 1
            if self.src_dry >= self.cut_patience:
                self._emit(t, "SUPPLY_CUT", "*", self.src_dry,
                           "all sources dry while demand unmet")
        else:
            self.src_dry = 0

        # out-of-band drain: lifts landing on a sink = swallowed off-DAG
        for nd in net.nodes.values():
            tgt = net.nodes.get(nd.oob_to) if nd.oob_to else None
            if tgt is not None and tgt.kind == "sink" and nd.oob_rate > 0:
                self._emit(t, "OOB_DRAIN", nd.name, nd.oob_rate,
                           f"out-of-band lane lands on sink {tgt.name}; "
                           f"downstream demand sees none of it")

        return [f for f in self.findings if f.tick == t]


# ------------------------------------------------------- static mode (M1) --

def static_check(net: FlowNet) -> list[Finding]:
    """M1: prove starvation possible-by-construction before any tick runs.
    Liveness checks stay dynamic (see the design doc, section 2)."""
    out: list[Finding] = []
    live: dict[str, list[str]] = defaultdict(list)
    for e in net.edges.values():
        src, dst = net.nodes[e.src], net.nodes[e.dst]
        if src.elev > dst.elev:                # L1: only downhill edges are live
            live[e.src].append(e.dst)
    sources = [n.name for n in net.nodes.values() if n.kind == "source"]
    reach: set[str] = set()
    stack = list(sources)
    while stack:
        x = stack.pop()
        if x in reach:
            continue
        reach.add(x)
        stack.extend(live[x])
    for nd in net.nodes.values():
        if nd.kind == "demand" and nd.name not in reach:
            out.append(Finding(0, "STATIC", nd.name, 0,
                               "no live (downhill) route from any source: "
                               "starvation by construction"))
        if nd.gate == "xor":
            ins = [e for e in net.edges.values() if e.dst == nd.name
                   and net.nodes[e.src].elev > nd.elev]
            if len(ins) > 1:
                out.append(Finding(0, "STATIC", nd.name, len(ins),
                                   f"xor gate fed by {len(ins)} live inlets: "
                                   f"collision-loss possible (water_graph.py:15-17)"))
    return out


# ----------------------------------------------------------------- demo ----

def run(net: FlowNet, sensor: StarvationSensor, ticks: int,
        mutate=None) -> list[str]:
    """Shared loop: snapshot -> tick -> observe -> collect lines."""
    log: list[str] = []
    for i in range(ticks):
        if mutate:
            mutate(i)
        before = net.snapshot()
        evs, ops = net.tick()
        sensor.observe(before, ops)
        log += evs if evs else [f"t{net.tick_count} (no movement)"]
        for f in sensor.findings:
            if f.tick == net.tick_count:
                log.append(f.line())
    return log


def case_a_starve() -> str:
    """The water_graph starvation test shape (tests/test_water_graph_starvation.py:20-30),
    rebuilt on the generic engine: sill junction pools 4, then the pool dies."""
    net = FlowNet()
    net.node("src", kind="source", elev=6, volume=8)
    net.node("mid", kind="source", elev=5, volume=8)
    net.node("jx", elev=3, gate="sill", sill=2)
    net.node("out", kind="demand", elev=1, demand_rate=99)
    net.node("waste", kind="sink", elev=0)
    net.edge("a", "src", "jx", cap=4)
    net.edge("b", "mid", "jx", cap=4)
    net.edge("j", "jx", "out", cap=8)
    sensor = StarvationSensor(net)

    def step(i: int) -> None:
        if i == 0:
            net.edges["b"].cap = 0        # starve the second inlet
        if i == 1:                        # both sources dry: the pool dies
            net.nodes["src"].volume = 0
            net.nodes["mid"].volume = 0
    return "\n".join(run(net, sensor, 3, mutate=step))


def case_b_crest_split() -> str:
    """L5 starved by dribble: a demand needing 5 buffered gets 1/tick while a
    side edge leaks the same 1/tick to waste: batch never crosses."""
    net = FlowNet()
    net.node("src", kind="source", elev=9, volume=99, rate=1)
    net.node("bat", elev=7)
    net.node("out", kind="demand", elev=2, demand_rate=99, batch_min=5)
    net.node("leak", kind="sink", elev=0)
    net.edge("feed", "src", "bat", cap=1)
    net.edge("serve", "bat", "out", cap=9)
    net.edge("drip", "out", "leak", cap=1)     # side lane steals the inflow
    sensor = StarvationSensor(net, split_patience=3, deadline=5)
    return "\n".join(run(net, sensor, 6))


def case_c_api_storm(silent: bool) -> str:
    """The B2-443 shape: one funded account fans out to 5 workflow children
    (maxAttempts 0, six units of budget); the window decays (source dries);
    the held asks spill. silent=True replays the pre-STARVED-law gate (the
    tally blind spot the census measured)."""
    net = FlowNet()
    net.node("account", kind="source", elev=10, volume=6, rate=0)
    for i in range(1, 6):
        name = f"child_{i}"
        net.node(name, elev=5, gate="sill", sill=2, silent_spill=silent)
        net.edge(f"ask_{i}", "account", name, cap=1)
        net.node(f"{name}.done", kind="demand", elev=1, demand_rate=2)
        net.edge(f"{name}.work", name, f"{name}.done", cap=2)
    sensor = StarvationSensor(net, deadline=4)
    return "\n".join(run(net, sensor, 6))


def case_d_static() -> str:
    net = FlowNet()
    net.node("src", kind="source", elev=2, volume=9, rate=1)
    net.node("mid", elev=3)                       # uphill of src
    net.node("need", kind="demand", elev=1, demand_rate=1)
    net.edge("up", "src", "mid", cap=5)           # dead by L1
    net.edge("down", "mid", "need", cap=5)
    net.node("x", elev=0, gate="xor")
    net.node("s1", kind="source", elev=4, volume=9, rate=1)
    net.node("s2", kind="source", elev=4, volume=9, rate=1)
    net.edge("x1", "s1", "x", cap=1)              # xor fed by TWO live inlets
    net.edge("x2", "s2", "x", cap=1)
    return "\n".join(f.line() for f in static_check(net))


def cross_check_real_engine() -> str:
    """Same scenario through mag/water_graph.WaterGraph: the estate engine must
    name the same starve the generic sensor names."""
    from mag.water_graph import WaterGraph
    g = WaterGraph()
    g.add_node("src", elev=6, volume=8)
    g.add_node("mid", elev=5, volume=8)
    g.add_node("jx", elev=3, kind="sill", sill=2)
    g.add_node("out", elev=1)
    g.add_node("waste", elev=0, kind="waste")
    g.add_pipe("a", "src", "jx", cap=4)
    g.add_pipe("b", "mid", "jx", cap=4)
    g.add_pipe("j", "jx", "out", cap=8)
    g.close("b")
    g.tick()
    g.nodes["src"].volume = 0
    evs = g.tick()
    joined = " | ".join(evs)
    ok = "STARVED" in joined and "4 pooled units" in joined
    return f"cross-check vs mag.water_graph.WaterGraph: {'PASS' if ok else 'FAIL'} :: {joined}"


if __name__ == "__main__":
    print("=== CASE A: gate starvation (sill pools 4, pool dies) ===")
    print(case_a_starve())
    print()
    print("=== CASE B: crest split (batch_min never crossed under a drip-leak) ===")
    print(case_b_crest_split())
    print()
    print("=== CASE C1: API-budget storm, pre-law gate (silent spill) ===")
    print(case_c_api_storm(silent=True))
    print()
    print("=== CASE C2: API-budget storm, STARVED-law gate (named spill) ===")
    print(case_c_api_storm(silent=False))
    print()
    print("=== CASE D: static mode (starvation by construction, zero ticks) ===")
    print(case_d_static())
    print()
    print("=== CROSS-CHECK: the real estate engine names the same starve ===")
    print(cross_check_real_engine())
