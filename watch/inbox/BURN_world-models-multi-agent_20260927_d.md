## Verdict

steal

## Evidence

Seat: research (pass c used builder; independent second seat, most active: 2,085 trail rows, last_run today, all three artifacts present).

Artifact 1, trail (dashboard/static/trails/research.jsonl, read 2026-09-27): row 1 `{"ts": "2026-09-04T15:34:55Z", "actor": "zcode-manager", "event": "TRAIL_OPENED", "detail": "append-only verbose lane trail. Every action gets a row: ts/actor/event/detail/artifacts."}`; row 2 `"actor": "research", "event": "shift_start", "detail": "relaunch #2 research lane agent online; task: digest ~40 undigested deepseek sessions"`; last row `"ts": "2026-09-27T15:59:57Z", "actor": "research-cage", "event": "MONITOR"`. Identity carried: actor, ts, activity; two actor strings name one seat.

Artifact 2, registry (queue/lanes/research/): manifest.md titles the seat Research, `"state: ARMED-PENDING"`, `"purpose: The ONLY lane that clicks. Live web research: browser-use + kernel."`, `"mcp_whitelist: mag, browser_use, node_repl"`. runner_state.json: `"last_run": "2026-09-27T15:59:57.962369+00:00"`, `"last_result": "monitor rc=0, drops gated=0"`, `"inbox_offset": 14`. No seat field anywhere in the file.

Artifact 3, pack (mag/context_pack.py): build mode sets `"include_trail": True` (line 56); layered pack docstring (line 949): "Layered pack: policy → bonds → trail cores → task → heat (drop heat first)". Bonds load from memory/bonds_active.json via mag/bonds.py; seat values today: five `"local"`, one `"grok_tui"`, zero for research. Trail layer: mag/run_trail.py `trail_pack_excerpt` (line 930) keys on run_id, "only open runs auto-surface in pack"; run-scoped, not seat-scoped.

WebSearch 2026-09-27, same query: thin for agent identity rehydration. Closest hits are security forensics, not NPC=SEAT: [Entro ML identity glossary](https://entro.security/glossary/machine-learning-identity), 2025 browser-history forensics profiling (Preprints.org, Rzayeva), IAM identity unification. No 2026 work on cold-context seat rehydration from a trail/registry/pack triple.

## Steal or Vacuous

What holds: artifacts 1 and 2 rehydrate identity today. Name (trail actor + manifest title), role (purpose, mcp_whitelist, laws), state (ARMED-PENDING, last_run/last_result), activity span (2026-09-04 to live 2026-09-27). A cold context given trail + manifest + runner_state rebuilds the research seat unambiguously, verified on a second seat, so pass c's 3/3 grounding is real machinery, not a builder fluke.

What fails: the pack, third artifact in canon, contributes zero seat-specific identity. Its bonds layer is fleet-residual (no row bound to research) and its trail layer keys on run_id, not seat. The single missing field: `"seat"` on bond rows and in runner_state.json, which names itself nowhere (identity is implicit in the directory path). With it, all three artifacts agree on the seat name and rehydration becomes byte-checkable instead of path-inferred. Fleet canon: residual bonds are fleet DNA, not seat DNA; seat DNA lives only in trail prose and manifest markdown.

## Falsifier

Pre-registered. Build: write `"seat": "<lane>"` into runner_state.json and bond rows at ingest (mag/bonds.py); filter pack bonds by seat. Test (binds research): a cold context receives research trail head+tail, manifest.md, runner_state.json, one seat-filtered pack; it must emit name/state/purpose/last_result matching a second independent reader, and every bond it cites must carry seat=research. Falsified on any anchor divergence or any seatless cited bond.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260927_c.md (read 2026-09-27)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (read 2026-09-27)
- dashboard/static/trails/research.jsonl, first+last 5 rows (read 2026-09-27)
- queue/lanes/research/manifest.md, queue/lanes/research/runner_state.json, queue/lanes/research/trail.jsonl (read 2026-09-27)
- mag/context_pack.py, mag/bonds.py, mag/run_trail.py, memory/bonds_active.json (read 2026-09-27)
- WebSearch "identity reconstruction from logs agent", 2026-09-27: [entro.security ML identity](https://entro.security/glossary/machine-learning-identity), Preprints.org 2025 browser-history forensics; snippet-level
