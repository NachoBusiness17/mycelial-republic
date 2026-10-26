"""hydrology tests -- rung 1 of the WF_SYNTHESIS ladder (2026-09-30).

Each test pins one law of the Watershed: node geometry (cross_section
-> depth -> head), conservation, graded flow (bigger drop = bigger
flow), backwater (a filling pool raises its own head), equalization,
the cap, determinism (byte-identical), and the bridge law that the
boolean engine it extends still passes its own suite untouched.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.hydrology import HydrologyGraph, from_spec  # noqa: E402
from mag.water_graph import WaterGraph, fracture_threshold  # noqa: E402


def _pair(src_elev: int, dst_preload: int = 0, cap: int = 1000) -> HydrologyGraph:
    """Two same-shape pools, one pipe, linear regime (cap far above flow)."""
    g = HydrologyGraph()
    g.add_node("src", elev=src_elev, volume=100)
    g.add_node("dst", elev=2, volume=dst_preload)
    g.add_pipe("p", "src", "dst", cap=cap)
    return g


# ------------------------------------------------------------ geometry ----
def test_node_geometry_depth_and_head():
    g = HydrologyGraph()
    n = g.add_node("tank", elev=3, volume=250, cross_section=500)
    assert n.cross_section == 500
    assert n.depth == 250 * 1000 // 500 == 500, "depth = volume*1000//cross_section"
    assert n.head == 3 * 256 + 500, "head = elev*256 + depth"
    assert g.depth("tank") == 500 and g.head("tank") == 1268


def test_cross_section_must_be_positive():
    g = HydrologyGraph()
    try:
        g.add_node("bad", cross_section=0)
    except ValueError:
        pass
    else:
        raise AssertionError("cross_section 0 must be rejected (integer divide)")


# ------------------------------------------------------- conservation ----
def test_conservation_total_volume_unchanged_through_ticks():
    g = HydrologyGraph()
    g.add_node("spring", elev=9, volume=500, cross_section=750)
    g.add_node("mid", elev=5, cross_section=500)
    g.add_node("low", elev=1, cross_section=1250)
    g.add_node("cold", elev=8, kind="cold")
    g.add_pipe("sip", "spring", "mid", cap=9, siphon=True, crest=3)
    g.add_pipe("run", "mid", "low", cap=11)
    g.boil("spring", 40)  # steam rides the tick too: volume + steam must hold
    total = sum(n.volume for n in g.nodes.values()) + sum(n.steam for n in g.nodes.values())
    for _ in range(60):
        g.tick()
        now = sum(n.volume for n in g.nodes.values()) + sum(n.steam for n in g.nodes.values())
        assert now == total, f"tick {g.tick_count}: water appeared or vanished ({now} != {total})"


# ----------------------------------------------------------- grading ----
def test_graded_flow_bigger_drop_bigger_flow():
    hi = _pair(src_elev=8)   # dHead = (2048+100) - 512 = 1636 -> flow 51
    lo = _pair(src_elev=4)   # dHead = (1024+100) - 512 =  612 -> flow 19
    hi.tick()
    lo.tick()
    f_hi, f_lo = hi.volume("dst"), lo.volume("dst")
    assert f_lo == 19 and f_hi == 51, (f_lo, f_hi)
    assert f_hi > f_lo > 0, "bigger drop must move more water (linear regime)"
    assert hi.volume("src") == 100 - f_hi, "what arrived must have left"


def test_depth_backwater_reduces_flow():
    empty = _pair(src_elev=4)            # dst empty: flow 19
    fuller = _pair(src_elev=4, dst_preload=200)  # dst head +200: flow 12
    empty.tick()
    fuller.tick()
    assert empty.volume("dst") == 19
    assert fuller.volume("dst") - 200 == 12
    assert fuller.volume("dst") - 200 < empty.volume("dst"), (
        "a filling pool raises its own head and throttles the pipe (backwater)")


def test_flow_capped_by_pipe_capacity():
    g = HydrologyGraph()
    g.add_node("dam", elev=20, volume=5000)
    g.add_node("valley", elev=0)
    g.add_pipe("spill", "dam", "valley", cap=7)
    g.tick()
    assert g.volume("valley") == 7, "huge dHead still saturates at the cap"


def test_no_uphill_flow_ever():
    g = HydrologyGraph()
    g.add_node("low", elev=0, volume=100)
    g.add_node("high", elev=5)
    g.add_pipe("up", "low", "high", cap=50)
    g.tick()
    assert g.volume("high") == 0, "check valve: never uphill on elevation"
    # same elevation, dst already deeper: its head is higher, still no flow
    g2 = HydrologyGraph()
    g2.add_node("shallow", elev=5, volume=100)
    g2.add_node("deep_full", elev=5, volume=300)
    g2.add_pipe("p", "shallow", "deep_full", cap=50)
    g2.tick()
    assert g2.volume("deep_full") == 300, "no flow into the higher-head pool"


def test_equal_heads_do_not_move():
    g = HydrologyGraph()
    g.add_node("a", elev=5, volume=200)
    g.add_node("b", elev=5, volume=200)
    g.add_pipe("level", "a", "b", cap=50)
    g.tick()
    assert g.volume("a") == 200 and g.volume("b") == 200, "equal heads = no flow"


def test_pools_equalize_and_settle():
    g = HydrologyGraph()
    g.add_node("a", elev=5, volume=400)
    g.add_node("b", elev=5, volume=0)
    g.add_pipe("w", "a", "b", cap=100)
    prev_a = 400
    for _ in range(100):
        g.tick()
        assert g.volume("a") + g.volume("b") == 400, "equalization conserves water"
        assert g.volume("a") >= g.volume("b"), "never overshoots past equal heads"
        assert g.volume("a") <= prev_a, "one-way pipe: no sloshing back"
        prev_a = g.volume("a")
    delta = g.volume("a") - g.volume("b")
    assert 0 <= delta <= 31, f"pools must settle near level (residual {delta})"
    assert g.volume("b") > 150, "the lower pool actually filled"
    settled = (g.volume("a"), g.volume("b"))
    g.tick()
    assert (g.volume("a"), g.volume("b")) == settled, "once settled, stays settled"


# --------------------------------------------------------- determinism ----
def test_deterministic_same_inputs_byte_identical():
    def run():
        g = _pair(src_elev=6, dst_preload=17, cap=13)
        g.add_node("sip_t", elev=4, volume=3)
        g.add_node("well", elev=0)
        g.add_pipe("sip", "sip_t", "well", cap=2, siphon=True, crest=2)
        log = []
        for _ in range(12):
            log.extend(g.tick())
        return json.dumps(g.to_spec(), sort_keys=True), tuple(log)
    a_spec, a_log = run()
    b_spec, b_log = run()
    assert a_spec == b_spec, "same inputs must produce byte-identical state"
    assert a_log == b_log, "same inputs must produce identical event logs"


# --------------------------------------------------------- spec bridge ----
def test_spec_roundtrip_and_water_graph_inheritance():
    g = _pair(src_elev=7)
    g.tick()
    spec = g.to_spec()
    assert spec["schema"] == "hydrology.v1"
    assert isinstance(g, WaterGraph), "the Watershed extends the verdict layer"
    g2 = from_spec(spec)
    assert g2.to_spec() == spec, "spec roundtrip must be exact"
    g2.tick()
    g.tick()
    assert g2.to_spec() == g.to_spec(), "roundtripped graph keeps evolving identically"


def test_boolean_engine_still_passes_its_own_tests():
    """The rung-1 change must not touch water_graph: load and run the
    boolean engine's own suite in-process (tests/test_water_graph.py)."""
    path = ROOT / "tests" / "test_water_graph.py"
    spec = importlib.util.spec_from_file_location("legacy_test_water_graph", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ran = 0
    for name in sorted(vars(mod)):
        if name.startswith("test_") and callable(getattr(mod, name)):
            getattr(mod, name)()
            ran += 1
    assert ran >= 7, f"expected the legacy suite's tests to run, got {ran}"


# ---- AF2 pipe-fracture law under graded heads (2026-09-30) ---------------
# The AC2 law (water_graph, spec watch/inbox/last_mile_20260930/AD1_FRACTURE.md)
# now fires from hydrology's `_move` via the INHERITED `_fracture` hook: a
# stressed pipe does not care which head law computed its flow. Receipt:
# watch/inbox/last_mile_20260930/AF2_HYDROLOGY_FRACTURE.md.


def test_graded_full_bore_stresses_partial_does_not():
    """flow == cap under the GRADED law still loads the pipe; a graded
    partial flow (dHead- or volume-limited below cap) loads nothing."""
    g = HydrologyGraph()
    g.add_node("tank", elev=20, volume=5000)   # huge dHead: flow saturates at cap
    g.add_node("pool", elev=2)
    g.add_node("sump", elev=0)
    g.add_pipe("p_main", "tank", "pool", cap=3)
    g.tick()
    assert g.pipes["p_main"].stress == 3, "graded full-bore flow must stress"
    assert not g.pipes["p_main"].fractured
    g.nodes["tank"].volume = 2                 # volume-limited: flow 2 < cap 3
    g.tick()
    assert g.pipes["p_main"].stress == 3, "graded partial flow must not stress"


def test_fracture_fires_identically_to_boolean_engine():
    """Same pipe name, same shape, cap 1: the graded-head engine must burst
    at the same tick with the same stress, the same spray, and a
    byte-identical event log as the boolean engine — one law, two heads."""
    def build(engine):
        g = engine()
        g.add_node("tank", elev=9, volume=10_000)
        g.add_node("pool", elev=5)
        g.add_node("sump", elev=0)
        g.add_pipe("burst", "tank", "pool", cap=1)
        return g

    graphs = {"boolean": build(WaterGraph), "graded": build(HydrologyGraph)}
    logs: dict[str, list[str]] = {"boolean": [], "graded": []}
    burst_line: dict[str, str] = {}
    for key, g in graphs.items():
        for _ in range(400):
            events = g.tick()
            logs[key].extend(events)
            hit = [e for e in events if "FRACTURES" in e]
            if hit:
                burst_line[key] = hit[0]
                break
    t = fracture_threshold("burst")
    assert burst_line["graded"] == burst_line["boolean"] == (
        f"Pipe burst FRACTURES (stress {t + 1}): spray to sump.")
    for key, g in graphs.items():
        p = g.pipes["burst"]
        assert p.fractured and not p.open, key
        assert p.stress == t + 1, key
        assert g.volume("pool") == t, f"{key}: burst tick must not deliver"
        assert g.volume("sump") == 1, f"{key}: the sprayed unit must land"
        assert g.volume("tank") == 10_000 - (t + 1), key
    assert logs["graded"] == logs["boolean"], (
        "same name + full bore every tick: the two head laws must log identically")


def test_hydrology_spec_roundtrip_preserves_stress_and_fractured():
    """hydrology.v1 roundtrip carries the AC2 fields (via the base to_spec
    and the AF2 from_spec fix): partial stress survives, and a burst pipe
    stays closed through the roundtrip instead of resurrecting open."""
    g = HydrologyGraph()
    g.add_node("tank", elev=20, volume=5000)
    g.add_node("pool", elev=2)
    g.add_node("sump", elev=0)
    g.add_pipe("carry", "tank", "pool", cap=2)
    g.tick()
    g.tick()
    assert g.pipes["carry"].stress == 4
    g2 = from_spec(g.to_spec())
    assert g2.pipes["carry"].stress == 4
    assert g2.pipes["carry"].fractured is g.pipes["carry"].fractured is False
    burst = HydrologyGraph()
    # volume 10_000: graded flow (dHead*8>>8 = 432) saturates at cap, so the
    # pipe runs full bore on tick 1 and bursts instantly.
    burst.add_node("tank", elev=20, volume=10_000)
    burst.add_node("pool", elev=5)
    burst.add_node("sump", elev=0)
    burst.add_pipe("one_shot", "tank", "pool",
                   cap=fracture_threshold("one_shot") + 1)
    burst.tick()                               # full bore tick 1: instant burst
    assert burst.pipes["one_shot"].fractured
    b2 = from_spec(burst.to_spec())
    assert b2.pipes["one_shot"].fractured and not b2.pipes["one_shot"].open
    b2.open("one_shot")                        # valve verb path: refused
    b2.tick()
    assert not b2.pipes["one_shot"].open
    assert b2.volume("pool") == 0, "a roundtripped burst pipe must stay dead"
