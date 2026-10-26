# Charter Scribe — pointer registry & gate (MOONSHOT_CHARTER_20260831)

8 pointers extracted. Per-pointer verdict below.

1. **water_windows v2 (12 reservoirs)** — §5/K5, §1 | **WRONG-SPAN**. No `water_windows*` file exists at /mag,/board,/patches. "12 reservoirs" rests on ledger text only (SWARM_RESEARCH_LEDGER:155, CODEX_CONVERGENCE:"water clock—12 reservoirs"). Cited receipt environments.json shows **7 containers, not 10 seats**, no desktop lanes. Count not byte-verifiable.

2. **CODEX_CONVERGENCE_20260831.md** — §1/M2 | **OK**. Exists; lists exactly the 5 donated tests (bypass, capability-attenuation, noisy-neighbor, replay, confused-deputy). (Note: its "43 tools" line is stale; charter corrected.)

3. **moiche.md §1 Ladder** — M3 | **OK**. Sections 1 Ladder (8×8/16×16/32×32) + Self-attack ("only ½ multipliers receipted") present, match X citations.

4. **freescale.md** — K4 | **OK**. "deref-heavy session (100%) drops it to ~3.4×" matches "honest floor 3.4×"; §1 groq 200K+cerebras 1M = 1.2M remote tok/day.

5. **ask_router_row0.json** — M1 | **OK**. Exists (202 B); schema: lane, ok, cost_usd, latency_s, task (marker first_light_2). No `kind` field but valid staged payload for the M1 gate.

6. **mcp_server.py + tools/__init__.py TOOL_MAP=20** — M1 | **OK**. mcp_server.py exists; `from tools import TOOL_MAP` resolves to `/mag/tools/__init__.py` (charter typed `/mag/mag/tools/__init__.py` — path off). Counted **exactly 20 distinct top-level keys**; "43 was a grep artifact" confirmed.

7. **switchboard.py v3-014 28KB** — M2/T2 | **OK**. Header v3-014; 28,162 B ≈ 28KB.

8. **patches 6a/6b** — M1 | **OK**. `/patches/applied/fix_ask_router_record_outcome.json` = PATCH 6a/6b; `fix_spawn_outcome_memory.json` = PATCH 6b/6b. Staged, present.

**Verdict:** 8 pointers, 7 OK, 1 WRONG-SPAN (water_windows/12-reservoir + environments.json). #5/#6 minor path/stale-text notes, non-blocking.
