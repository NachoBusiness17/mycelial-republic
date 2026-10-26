# W6 — K8S AS WATER, v0 LANDED (2026-09-30, lane W6)

WD's hydraulic mapping (`watch/inbox/water_engineering_20260930/WD_K8S_AS_WATER.md`)
made executable on `mag/water_graph.py` with ZERO engine changes. $0, stdlib,
no cluster. No commit (mission order).

## Files (owned)

- `tools/k8s_water_sim.py` — `k8s_scenario(spec)` maps the spec onto a
  WaterGraph; `simulate()` runs the valve loop + gravity ticks + live
  invariants; `workload_from_ledger()` reads `tools/gps_mcp/gps_ledger.db3`
  verdict_log as a real workload; `render_trace()`; CLI `--demo`/`--json`.
- `tests/test_k8s_water.py` — 9 tests (mission properties pinned).

## Mapping as implemented

| k8s thing | water_graph primitive |
|---|---|
| pod | `Node pod:<name>`, elev = PriorityClass, volume = pending |
| ResourceQuota | `baseline` pipe cap (mux -> served) |
| per-pod limit | `svc:<pod>` pipe cap (pod -> dispatch) |
| priority ladder | class elevations strictly descending; scheduler opens ONE class lane per tick (svc + lane valves together), highest class with work first |
| load shedding | `sill` junction per class: below-threshold inflow HELD, then STARVED to waste (eviction) |
| autoscaler | `burst` siphon mux->served: primes at mux backlog >= crest, drains burst cap, breaks on dry intake (scale-in) |
| escalation/retry | `boil` waste -> steam condenses at `escalation_tier` (highest cold) -> always-open top-tier lane back to mux |

The operator lens holds: the loop only sets valves (priority plugin) and the
boil budget; gravity, caps, sills and crests do all dispatch. Live per-tick
invariants: no node ever negative; economy never leaks (V5 law, future
arrivals accounted).

## Real trace (gps_ledger verdict_log: 10 events, glm-5.3-prime critical,
mountain-world-v0 burstable sill=2, quota 2, burst cap 2 crest 2, budget 1)

```
tick  lane         admitted           srvd mux held shed esc wste  pending
   1  critical     z-ai-glm-5.3-prime=2    0   3    0    0   1    0  glm=3
   2  critical     z-ai-glm-5.3-prime=2    3   2    0    0   0    0  glm=1,mountain=1
   3  critical     z-ai-glm-5.3-prime=1    2   1    0    0   0    0  mountain=4
   4  burstable    -                     1   0    2    0   0    0  mountain=2
   5  burstable    -                     0   0    2    0   0    0  -
   6  burstable    -                     0   0    0    4   0    4  -
   7  -            -                     0   1    0    0   1    3  -
   8  -            -                     1   1    0    0   1    2  -
   9  -            -                     1   1    0    0   1    1  -
  10  -            -                     1   1    0    0   1    0  -
  11  -            -                     1   0    0    0   0    0  -
accounting: served 10/10 injected | waste 0 | mux 0 | 11 ticks
```

Story on real bytes: critical drains t1-t3 (burst siphon primed at t2,
served 3 > quota 2); the single-pod burstable batch is held below sill 2
(t4-t5), STARVED to waste at t6, then boiled back 1/tick through the cold
crown and re-served t7-t11. The failed-verdict seed (waste 1 at t0) rides the
same escalation lane at t1. Determinism: two runs byte-identical.

## Tests (instrument named, per census law)

- `pytest tests/test_k8s_water.py -q` -> 9 passed (0.65s).
- Water family executed: `pytest tests/test_k8s_water.py
  tests/test_water_graph.py tests/test_water_graph_campaign.py
  tests/test_water_graph_starvation.py tests/test_water_computer.py
  tests/test_water_swarm.py -q` -> 48 passed (47.71s).
- Fresh collect (`pytest --collect-only -q --continue-on-collection-errors`,
  2026-09-30): 3,211 tests tree-wide, 1 collection error. My file collects 9.

Mission properties all pinned: priority ordering (crit admission ticks 1-3
strictly before burstable 4+; low starts only once crit pod empty); quota
caps (per-tick served <= quota with burst off; per-pod limit holds); shed =
sill threshold (1 pod < sill 2 held then STARVED to waste; 2 pods >= sill
admitted and served); no negative volume + conservation every tick (17-unit
adversarial scenario with mid-run arrivals, burst, shed and escalation ends
served 17 / waste 0).

## v0 honesty notes

- Waiting classes hold pending AT THE POD (svc valved with the lane); a class
  dispatch that pools and then stops receiving starves to waste = idle queues
  are evicted, not parked forever. Escalation is the recovery path.
- Per-tick service is attributed via svc/lane commits; strict one-lane ticks
  keep identity exact (mux is a plain pool).
- Trunk insertion order [burst, baseline, esc_lane]: the siphon sees the
  backlog before the baseline drains.

## Incident flag (not this lane's file)

`tests/test_behavioral_awareness.py` has a committed SyntaxError (unmodified
vs HEAD; last touched in the ff1c02822 V-WAVE tree) — it breaks whole-tree
`pytest --collect-only` (3,211 collected, 1 error, 2026-09-30). The B2-246
daily census patrol needs a clean collect; whoever owns that file should fix
or the patrol will cannot-verify.
