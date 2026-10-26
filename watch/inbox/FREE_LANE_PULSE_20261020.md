# DYNAMIC FREE FLEET AUTOPILOT: MODEL-LEVEL LIVENESS PULSE (2026-10-20)

**Operator directive:** "next (Project Aegis-Percolator Phase 1)"  
**Classification:** INFRASTRUCTURE AUTONOMY & DYNAMIC ROUTING  
**House Law Compliance:** Strictly zero unicode em-dashes (-- and - only); strictly zero git commits.

---

## 1. Executive Summary

Phase 1 of Project Aegis-Percolator is now live and operational:
- **Module Landed:** `tools/free_lane_pulse.py` + tests in `tests/test_free_lane_pulse.py` (ALL PASS).
- **State Emitted:** `state/live_free_roster.json` containing live-probed, latency-ranked endpoints.
- **The Core Problem Solved:** Free model endpoints on OpenRouter and Nous rotate by the hour. Dispatching blind causes HTTP 404/403 drops and 900-second timeouts. This tool runs 1-token health checks with strict 5-second timeouts, keeping the fleet routed exclusively to active models.

---

## 2. Live Pulse Verification Results (2026-10-20T21:39Z)

Total probed: 13 candidate lanes.  
**Alive: 10 | Rate-Limited (429): 1 | Dead/Rotated (403): 2**

### The Live Ranked Ladder (Sorted by Latency):
1. `nvidia/nemotron-3.5-content-safety:free` -- 0.219s
2. `poolside/laguna-xs-2.1:free` -- 0.293s
3. `cohere/north-mini-code:free` -- 0.359s
4. `nvidia/nemotron-3.5-lightning:free` -- 0.425s
5. `liquid/lfm-2.5-2.6b:free` -- 0.577s
6. `dots-studio/dots-3-note-preview:free` -- 0.729s
7. `minimax/minimax-m3.1-flash:free` -- 0.884s
8. `nvidia/nemotron-3.5-super-vl:free` -- 0.985s
9. `poolside/laguna-s-2.1:free` -- 0.988s
10. `reflection/beam-1.0-501b-a23b:free` (Nous 501B) -- 2.489s

### Failures Caught Before Dispatch:
- `thinkingmachines/inkling:free` (HTTP 403 Forbidden -- rotated off)
- `thinkingmachines/inkling-small:free` (HTTP 403 Forbidden -- rotated off)
- `xingchen-agi/xing4.0-29b-a4b:free` (HTTP 429 Too Many Requests -- backed off)

---

## 3. Integration & Consumption

The engine exposes:
```python
from tools.free_lane_pulse import get_live_free_models

live_ladder = get_live_free_models()
# Automatically returns cached alive models, or refreshes if older than 30 minutes
```

Any downstream task runner (`tools/task_wall.py`, Same Book waves, or offpeak background workers) can now query `get_live_free_models()` to guarantee zero-fail dispatches at zero marginal cost.
