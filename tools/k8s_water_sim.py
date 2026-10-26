"""k8s_water_sim — the water_graph as a k8s scheduler simulator (v0, 2026-09-30).

Design owner: watch/inbox/water_engineering_20260930/WD_K8S_AS_WATER.md —
WD's hydraulic mapping made executable on mag/water_graph.py with ZERO
changes to the engine. $0, stdlib, no cluster.

Mapping (WD's lens, executable):

  k8s thing                      water_graph primitive
  -----------------------------  ------------------------------------------
  pod                            Node ``pod:<name>``, elev = PriorityClass,
                                 volume = pending requests
  ResourceQuota                  pipe cap ``baseline`` (mux -> served)
  per-pod limit                  pipe cap ``svc:<pod>`` (pod -> dispatch)
  priority ladder                class elevations, strictly descending; the
                                 scheduler loop opens ONE class lane per tick
                                 (its svc + lane valves together), highest
                                 class with work first (kube's priority
                                 plugin = valves; gravity + caps dispatch —
                                 the operator lens: the AI sets elevations,
                                 sills and crests, physics moves)
  load shedding                  ``sill`` junction per class: inflow below the
                                 batch threshold is HELD, then STARVED by the
                                 engine into the waste basin (eviction)
  autoscaler (burst-then-drain)  ``burst`` siphon mux -> served: primes when
                                 the mux backlog >= crest, drains burst cap
                                 until the mux runs dry, then breaks (the
                                 burst pool scales in)
  escalation / retry             boil() the waste basin -> steam condenses at
                                 the highest cold node (``escalation_tier``),
                                 which feeds the mux on an ALWAYS-OPEN lane:
                                 retries jump the valve ladder to top tier
  scheduling trace               per-tick rows parsed from the engine's own
                                 event lines (which svc pipes committed, what
                                 served, what shed, siphon state)

v0 semantics notes (honesty):
  - The mux is a plain pool; per-tick service is attributed through the
    svc/lane commits of that tick. Strict one-lane ticks keep the
    attribution exact (only one class is in flight per tick).
  - A class dispatch holding pooled volume that receives NO new inflow for a
    tick is STARVED by the engine into waste: idle queues are evicted, not
    parked forever. Escalation (boil) is the recovery path — nothing is
    deleted (V5 economy law).
  - Trunk insertion order is [burst, baseline, esc_lane]: the autoscaler
    siphon evaluates the mux backlog before the baseline drain.

Workload feed: tools/gps_mcp/gps_ledger.db3 verdict_log (real routing
receipts) -> arrivals schedule; verdict=0 rows seed the waste basin as
already-shed work awaiting escalation.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402

MUX_ELEV = 5
SERVED_ELEV = 0
WASTE_ELEV = 0
ESC_ELEV = 200
DISPATCH_DROP = 5  # dispatch:<class> sits this far below its pods

DEFAULT_CLASSES: list[dict[str, int]] = [
    {"name": "critical", "elev": 60, "sill": 1},
    {"name": "burstable", "elev": 40, "sill": 1},
    {"name": "best-effort", "elev": 20, "sill": 1},
]


@dataclass
class Scenario:
    """A k8s spec mapped onto a WaterGraph (k8s_scenario() builds this)."""

    graph: WaterGraph
    spec: dict[str, Any]
    classes: list[dict[str, Any]] = field(default_factory=list)
    pod_class: dict[str, str] = field(default_factory=dict)
    lane_pipes: dict[str, str] = field(default_factory=dict)   # class -> lane pipe
    svc_pipes: dict[str, list[str]] = field(default_factory=dict)  # class -> svc pipes
    quota: int = 1
    lane_cap: int = 1
    escalation_budget: int = 0


def k8s_scenario(spec: dict[str, Any]) -> Scenario:
    """Map a k8s scheduling spec onto a WaterGraph.

    spec = {
      "quota": 2,                          # ResourceQuota: units/tick baseline
      "burst": {"cap": 2, "crest": 3},     # autoscaler siphon (optional)
      "classes": [                         # priority ladder, first = highest
         {"name": "critical", "elev": 60, "sill": 1}, ...
      ],
      "pods": [
         {"name": "glm-prime", "class": "critical", "pending": 5, "limit": 2},
      ],
      "escalation": {"tier_elev": 200, "budget": 1},   # boil retries/tick
      "ticks": 24,                          # max scheduling ticks
    }
    """
    classes = spec.get("classes") or DEFAULT_CLASSES
    names = [str(c["name"]) for c in classes]
    if not classes or len(set(names)) != len(names):
        raise ValueError("classes must be a non-empty list of unique names")
    elevs = [int(c["elev"]) for c in classes]
    if any(b >= a for a, b in zip(elevs, elevs[1:])):
        raise ValueError(f"class elevations must strictly descend: {elevs}")
    if min(elevs) <= MUX_ELEV + DISPATCH_DROP:
        raise ValueError("lowest class elevation must clear the mux + dispatch drop")
    if any(int(c.get("sill", 1)) < 1 for c in classes):
        raise ValueError("sill thresholds must be >= 1")

    quota = int(spec.get("quota", 1))
    if quota < 1:
        raise ValueError("quota must be >= 1")
    burst = spec.get("burst") or None
    if burst and int(burst.get("cap", 0)) < 1:
        raise ValueError("burst cap must be >= 1")
    lane_cap = quota + (int(burst["cap"]) if burst else 0)

    esc = spec.get("escalation") or {}
    esc_elev = int(esc.get("tier_elev", ESC_ELEV))
    if esc_elev <= max(elevs):
        raise ValueError("escalation tier must sit above every class elevation")
    budget = int(esc.get("budget", 0))

    g = WaterGraph()
    g.add_node("mux", elev=MUX_ELEV)
    g.add_node("served", elev=SERVED_ELEV)
    g.add_node("waste", elev=WASTE_ELEV, kind="waste")
    g.add_node("escalation_tier", elev=esc_elev, kind="cold")
    # trunk order matters: burst siphon sees the backlog before baseline drains
    if burst:
        g.add_pipe("burst", "mux", "served", cap=int(burst["cap"]),
                   siphon=True, crest=int(burst.get("crest", 2)))
    g.add_pipe("baseline", "mux", "served", cap=quota)
    g.add_pipe("esc_lane", "escalation_tier", "mux", cap=quota)

    for c in classes:
        g.add_node(f"dispatch:{c['name']}", elev=int(c["elev"]) - DISPATCH_DROP,
                   kind="sill", sill=int(c.get("sill", 1)))

    seen: set[str] = set()
    for pod in spec.get("pods", []):
        name = str(pod["name"])
        if name in seen:
            raise ValueError(f"duplicate pod {name!r}")
        seen.add(name)
        cls = str(pod["class"])
        if cls not in names:
            raise ValueError(f"pod {name!r} references unknown class {cls!r}")
        pending, limit = int(pod.get("pending", 0)), int(pod.get("limit", 1))
        if pending < 0 or limit < 1:
            raise ValueError(f"pod {name!r}: pending >= 0 and limit >= 1 required")
        g.add_node(f"pod:{name}", elev=dict(zip(names, elevs))[cls], volume=pending)
        g.add_pipe(f"svc:{name}", f"pod:{name}", f"dispatch:{cls}", cap=limit)

    for c in classes:
        g.add_pipe(f"lane:{c['name']}", f"dispatch:{c['name']}", "mux", cap=lane_cap)

    svc_pipes: dict[str, list[str]] = {str(c["name"]): [] for c in classes}
    for pod_name, cls in ((str(p["name"]), str(p["class"])) for p in spec.get("pods", [])):
        svc_pipes[cls].append(f"svc:{pod_name}")
    return Scenario(graph=g, spec=spec, classes=classes,
                    pod_class={str(p["name"]): str(p["class"]) for p in spec.get("pods", [])},
                    lane_pipes={str(c["name"]): f"lane:{c['name']}" for c in classes},
                    svc_pipes=svc_pipes,
                    quota=quota, lane_cap=lane_cap, escalation_budget=budget)


# --------------------------------------------------------------- parsing ----

_SVC_RE = re.compile(r"^svc:(.+): (\d+) ")
_HOLD_RE = re.compile(r"^Junction dispatch:\S+ holds (\d+) below gate")


def _parse_admitted(events: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for ev in events:
        m = _SVC_RE.match(ev)
        if m:
            out[m.group(1)] = out.get(m.group(1), 0) + int(m.group(2))
    return out


def _parse_held(events: list[str]) -> int:
    return sum(int(m.group(1)) for ev in events
               if (m := _HOLD_RE.match(ev)))


def _pressure(sc: Scenario, cls: str) -> int:
    """Work waiting in a class: pod pending + pooled dispatch volume."""
    total = sc.graph.volume(f"dispatch:{cls}")
    for pod, c in sc.pod_class.items():
        if c == cls:
            total += sc.graph.volume(f"pod:{pod}")
    return total


def _idle(sc: Scenario, by_tick: dict[int, list], tick: int) -> bool:
    if any(t > tick for t in by_tick):
        return False
    if any(p.primed for p in sc.graph.pipes.values()):
        return False  # a primed siphon (burst pool still up) is not quiescent:
        # it must run one more tick to break on its dry intake (scale-in)
    for name, n in sc.graph.nodes.items():
        if name == "served":
            continue
        if n.volume or n.steam:
            if name == "waste" and sc.escalation_budget == 0:
                continue  # unrecoverable without a boil budget: park it
            return False
    return True


def _check_invariants(g: WaterGraph, expected: int, tick: int) -> None:
    """Live shed/starvation properties: volumes never go negative and the
    economy never leaks (V5: deletion is theft). `expected` = units that have
    actually arrived on the graph so far (future arrivals excluded)."""
    total = 0
    for n in g.nodes.values():
        assert n.volume >= 0, f"tick {tick}: negative volume at {n.name}"
        assert n.steam >= 0, f"tick {tick}: negative steam at {n.name}"
        total += n.volume + n.steam
    assert total == expected, f"tick {tick}: economy leak {total} != {expected}"


# --------------------------------------------------------------- simulate ----

def simulate(spec: dict[str, Any], arrivals: list[dict[str, Any]] | None = None,
             waste_seed: int | None = None, check_invariants: bool = True) -> dict[str, Any]:
    """Run the scheduler: gravity ticks + the priority valve loop.

    Per tick: (1) arrivals land on pods; (2) the highest class with work gets
    its lane valve opened, all others closed; (3) the escalation budget boils
    shed work out of waste (steam -> cold crown -> top-tier lane); (4) one
    engine tick — sills admit/hold, lanes flow, trunk + siphon drain, starves
    spill; (5) the trace row is parsed from the engine's own events.
    """
    sc = k8s_scenario(spec)
    g = sc.graph
    if arrivals is None:
        arrivals = spec.get("arrivals") or []
    if waste_seed is None:
        waste_seed = int(spec.get("waste_seed", 0))
    by_tick: dict[int, list] = {}
    for a in arrivals:
        by_tick.setdefault(int(a["tick"]), []).append(a)
    g.nodes["waste"].volume += waste_seed

    injected = (sum(int(p.get("pending", 0)) for p in spec.get("pods", []))
                + sum(int(a["units"]) for a in arrivals) + waste_seed)
    max_ticks = int(spec.get("ticks", 64))

    trace: list[dict[str, Any]] = []
    tick = 0
    # units that should be on the graph right now: initial pending + waste
    # seed are placed before tick 1; arrivals join their tick's expected total
    expected = sum(int(p.get("pending", 0)) for p in spec.get("pods", [])) + waste_seed
    while tick < max_ticks:
        tick += 1
        for a in by_tick.get(tick, []):
            g.nodes[f"pod:{a['pod']}"].volume += int(a["units"])
            expected += int(a["units"])
        # priority plugin = valves: ONE class lane per tick, top first. The
        # whole lane valves together (svc pipes + lane pipe) so a waiting
        # class holds its pending AT THE POD instead of pooling at its
        # dispatch and starving while a higher class runs.
        lane = next((c["name"] for c in sc.classes if _pressure(sc, c["name"]) > 0), None)
        for cls_name in sc.lane_pipes:
            active = cls_name == lane
            (g.open if active else g.close)(sc.lane_pipes[cls_name])
            for pipe in sc.svc_pipes.get(cls_name, []):
                (g.open if active else g.close)(pipe)
        # escalation: boil shed work out of the waste basin (top-tier retry)
        escalated = g.boil("waste", sc.escalation_budget) if sc.escalation_budget else 0
        served0, waste0 = g.volume("served"), g.volume("waste")
        events = g.tick()
        trace.append({
            "tick": tick, "lane": lane,
            "admitted": _parse_admitted(events), "held": _parse_held(events),
            "served": g.volume("served") - served0,
            "mux": g.volume("mux"), "shed": g.volume("waste") - waste0,
            "escalated": escalated, "waste": g.volume("waste"),
            "pending": {p: g.volume(f"pod:{p}") for p in sc.pod_class},
            "events": events,
        })
        if check_invariants:
            _check_invariants(g, expected, tick)
        if _idle(sc, by_tick, tick):
            break

    return {
        "trace": trace, "ticks_used": tick,
        "served": g.volume("served"), "waste": g.volume("waste"),
        "mux": g.volume("mux"), "escalation_tier": g.volume("escalation_tier"),
        "total": injected, "graph": g, "scenario": sc,
    }


def render_trace(res: dict[str, Any]) -> str:
    head = (f"{'tick':>4}  {'lane':<12} {'admitted':<18} {'srvd':>4} {'mux':>3} "
            f"{'held':>4} {'shed':>4} {'esc':>3} {'wste':>4}  pending")
    lines = [head]
    for r in res["trace"]:
        adm = ",".join(f"{p}={u}" for p, u in r["admitted"].items()) or "-"
        pend = ",".join(f"{p}={v}" for p, v in r["pending"].items() if v) or "-"
        lines.append(f"{r['tick']:>4}  {str(r['lane'] or '-'):<12} {adm:<18} "
                     f"{r['served']:>4} {r['mux']:>3} {r['held']:>4} {r['shed']:>4} "
                     f"{r['escalated']:>3} {r['waste']:>4}  {pend}")
    return "\n".join(lines)


# --------------------------------------------------------------- workload ----

def workload_from_ledger(db_path: str | Path | None = None,
                         class_map: dict[str, str] | None = None) -> dict[str, Any]:
    """Read gps_mcp's verdict_log as a workload: each row = one request unit.

    model_id -> pod, task_shape -> priority class (class_map), verdict=1 ->
    an arrival unit at its ts's tick, verdict=0 -> one unit of pre-shed work
    seeded into the waste basin (recoverable via escalation).
    """
    db_path = Path(db_path or (ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"))
    if not db_path.exists():
        raise FileNotFoundError(f"ledger not found: {db_path}")
    class_map = class_map or {"night-judgment": "critical", "world-tick": "burstable"}
    con = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT ts, model_id, task_shape, verdict FROM verdict_log ORDER BY ts, rowid"
        ).fetchall()
    finally:
        con.close()

    ticks: dict[str, int] = {}
    pods: dict[str, dict[str, Any]] = {}
    arrivals: list[dict[str, Any]] = []
    waste_seed = 0
    for ts, model_id, task_shape, verdict in rows:
        pod = re.sub(r"[^A-Za-z0-9._-]", "-", str(model_id))
        if pod not in pods:
            pods[pod] = {"name": pod, "class": class_map.get(str(task_shape)),
                         "pending": 0, "limit": 2, "model_id": str(model_id),
                         "task_shape": str(task_shape)}
        tick = ticks.setdefault(str(ts), len(ticks) + 1)
        if int(verdict):
            arrivals.append({"tick": tick, "pod": pod, "units": 1})
        else:
            waste_seed += 1
    return {"pods": list(pods.values()), "arrivals": arrivals, "waste_seed": waste_seed,
            "meta": {"events": len(rows), "ticks": len(ticks), "db": str(db_path)}}


def spec_from_workload(wl: dict[str, Any], classes: list[dict[str, Any]] | None = None,
                       quota: int = 2, burst: dict[str, int] | None = None,
                       budget: int = 1, ticks: int = 40) -> dict[str, Any]:
    """Lift a workload_from_ledger() result into a simulate()-able spec."""
    classes = classes or DEFAULT_CLASSES
    names = [str(c["name"]) for c in classes]
    lowest = names[-1]
    pods = [{"name": p["name"],
             "class": p["class"] if p["class"] in names else lowest,
             "pending": int(p.get("pending", 0)), "limit": int(p.get("limit", 2))}
            for p in wl["pods"]]
    return {"quota": quota, "burst": burst, "classes": classes, "pods": pods,
            "escalation": {"tier_elev": ESC_ELEV, "budget": budget}, "ticks": ticks,
            "arrivals": wl["arrivals"], "waste_seed": wl["waste_seed"],
            "workload_meta": wl["meta"]}


# ------------------------------------------------------------------- cli ----

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="water_graph as a k8s scheduler simulator")
    ap.add_argument("--demo", action="store_true", help="run the gps_ledger-fed demo")
    ap.add_argument("--db", default=None, help="path to gps_ledger.db3")
    ap.add_argument("--json", action="store_true", help="dump the trace as JSON")
    args = ap.parse_args(argv)

    wl = workload_from_ledger(args.db)
    spec = spec_from_workload(
        wl,
        classes=[{"name": "critical", "elev": 60, "sill": 1},
                 {"name": "burstable", "elev": 40, "sill": 2}],
        quota=2, burst={"cap": 2, "crest": 2}, budget=1, ticks=24,
    )
    res = simulate(spec)
    if args.json:
        print(json.dumps({k: v for k, v in res.items() if k not in ("graph", "scenario")},
                         indent=1))
        return 0
    meta = spec["workload_meta"]
    print(f"workload: {meta['events']} verdict_log events over {meta['ticks']} arrival "
          f"ticks from {meta['db']}")
    for p in spec["pods"]:
        print(f"  pod {p['name']:<22} class={p['class']:<10} limit={p['limit']}")
    print(f"quota={spec['quota']}/tick  burst={spec['burst']}  "
          f"escalation budget={spec['escalation']['budget']}/tick  "
          f"waste seed={spec['waste_seed']}")
    print()
    print(render_trace(res))
    print()
    print(f"accounting: served {res['served']}/{res['total']} injected | waste {res['waste']} "
          f"| mux {res['mux']} | escalation_tier {res['escalation_tier']} "
          f"| {res['ticks_used']} ticks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
