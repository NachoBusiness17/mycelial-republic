# RESTART FLIP RECEIPT — 2026-09-12 (box clock 2026-09-11T21:38Z)

**THE POINT: old PID 24140 -> new PID 13088; /healthz is LIVE (did not exist before tonight) — semantic health endpoint + http-seam failure logging now hold the wire.**

## Activation
- Activation time (UTC): **2026-09-11T21:38:36Z** (box clock; operator-date 09-12)
- Old process: PID **24140** (started ~20:2xZ, OLD module) — `taskkill //PID 24140 //F` SUCCESS
- Relaunch: `powershell Start-Process python -ArgumentList '-m','backend.server'` hidden/detached, cwd repo root
- New process: PID **13088** — `127.0.0.1:8000 LISTENING` verified after 8s sleep

## Activation proof — GET /healthz (HTTP 200, endpoint is new tonight)
```json
{"ok":true,"tool_error_rate_1h":null,"tool_fail_1h":82,"critical_failure_recent":false,"http_tool_fail_1h":0,"last_failure_ts":"2026-09-11T21:17:11.857034+00:00","window":{"hours":1,"critical_minutes":15,"tail_bytes":2097152}}
```

## GET /health — semantic pointer field confirmed (HTTP 200)
- `"semantic": "/healthz"` present; service `mag-backend`, version `1.0.0`, 24 tools listed.

## http_tool_fail rows in logs/failure_kb.jsonl (75,877 total lines)
- **Count: 3**, all `"kind": "http_tool_fail"`, `"phase": "http_dispatch"`, sigs
  `run_shell:21236404fc6f` (x2, "command not allowlisted: exit") + `run_shell:2a7bbe12f9d6` ("'dict' object has no attribute 'strip'")
- **All 3 timestamped 2026-09-11T15:24:49Z — PRE-restart** (seam code exercised in an earlier window). **0 new rows since the 21:38Z flip**; /healthz corroborates: `http_tool_fail_1h: 0`.

## Notes
- No failures in the flip: kill clean, port handoff clean, both probes 200 on first try.
- `tool_fail_1h: 82` is the pre-existing log-tail scanner count (lane_scheduler stalled-6 warnings, last_failure_ts 21:17:11Z), not a new breach; `tool_error_rate_1h: null` (no critical in window).

— C1-LANE 1 (THE RESTART FLIP), 9-wide wave 2026-09-12
