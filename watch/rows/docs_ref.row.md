ROW
pointer: /mag/docs/ref/SURFACES.md
claim: <matches observable board state, with one port divergence (SURFACES A says OpenClaw UI 127.0.0.1:18789; probed gateway is mag-sovereign:8001)>
type: probe
confidence: M
status: VERIFIED
evidence: (1) /board/room.jsonl live, 2944 lines, seat:"claw" dispatch incl. this subagent thread; (2) /board/WARM_PACK.json (warm_pack.v1 law+spine+shape_hash) + PACK_* files == OPERATOR_CARD LOAD-pack; (3) probe_mag_gateway.md: /seats grok Idle, /room 80 lines, /queue 10 jobs — gateway+seat real, but 8001≠18789 port; (4) MEMORY_RIB.jsonl (ObjectBegin law.soul/agent/memory, sha256 bounds) + active_session.json == stateless-seat boundary/agent_state; (5) docker_watchdog.ps1/.vbs + CAMPAIGN_MAP "mag-worker unhealthy" == SURFACES C container host row.
