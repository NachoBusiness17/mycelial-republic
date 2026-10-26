# B2-81 Ollama gap ground truth (2026-09-26)

## Verdict

Detection, not absence. The 89 lifecycle_gap:ollama rows are dominated by
detection misses against a live daemon; the start policy (on when
fleet_running>0 or queue_depth>0, mag/lifecycle.py:498-502) is correct and
the probe session shows it aligning when the probe can actually reach the
daemon. The old `_ollama_up()` was a bare `urllib.urlopen(timeout=0.6)` that
inherits env/registry proxies: with `http_proxy` set it times out against a
LIVE daemon at 0.61s and no request ever reaches the server (reproduced
pre-fix on this machine). Row-by-row: 20 of the 21 rows verifiable against
Ollama server logs carry a `/api/tags` HTTP 200 within 0-14 seconds of the
gap observation; the 21st (2026-09-26T04:53:18Z) was observed 59 minutes
after a manual `ollama serve` (PID 11112, created 2026-09-26T03:54:32Z per
wmic) had taken 127.0.0.1:11434. Only 3 rows are true absences between
tray-app sessions (2026-09-20T17:52:33Z, 2026-09-21T06:05:53Z,
2026-09-21T18:21:49Z). Fix landed in `_ollama_up()`: ProxyHandler({}) opener
so proxies never intercept loopback, 2.0s timeout x2 tries, a raw
socket-connect fallback, and a cause-naming detail (refused=daemon absent vs
unreachable) so future rows carry their own verdict. Policy text unchanged.

## Evidence

- Gap log bytes: memory/training/loop_gaps.jsonl has 313 rows, exactly 89
  with name `lifecycle_gap:ollama` (28.4 pct now; the brief's 29.3 pct
  matches 89/304 before 9 later rows landed). Rows land on a metronomic
  ~12h12m cadence, which is the gap-tracking dedupe window
  (mag/temperature_stack.py `dedupe_hours` 12), so the gap condition was
  CHRONIC in the observing process, not sporadic.
- Server logs cross-correlation (LOCALAPPDATA/Ollama server.log,
  server-1.log 302MB, server-2/3/4/5.log): all 89 row timestamps tested
  against every GIN `/api/tags` line. 20 rows have a 200 within 0-14s
  (2026-09-13T01:47:30Z, 09-13T14:06:07Z, 09-14T02:07:43Z, 09-14T14:43:06Z,
  09-15T03:00:04Z, 09-15T15:15:12Z, 09-16T03:15:48Z, 09-16T15:50:03Z,
  09-17T04:03:03Z, 09-17T16:30:23Z, 09-18T04:53:20Z, 09-18T17:07:22Z,
  09-19T05:24:56Z, 09-19T17:34:37Z, 09-20T05:35:34Z, 09-22T06:40:28Z,
  09-23T12:10:55Z, 09-24T00:33:26Z, 09-24T12:49:07Z, 09-25T01:11:08Z); in
  the server-1 era the server answered those probes in 4-12ms. A GIN line
  requires the server alive, so `actual=False` at those moments is a
  detection miss, and the failed probe left NO GIN line, meaning the probe
  request never reached the server (connection-level failure, not latency).
- Timeout is not the chronic cause: only 11 of 6,758 GIN /api/tags samples
  exceeded the 600ms timeout (0.16 pct), max 1,137ms.
- Reproduction (pre-fix): `http_proxy=http://127.0.0.1:9` against the live
  daemon returns URLError timeout after 0.61s; server-side GIN shows nothing.
  Post-fix, same env: `(True, '11434')`.
- Live probe session with queue work live: `spawn_task` t89fd1bad11
  (provider ollama, tag [test]); while it ran (queue_depth=1, fleet_running=1)
  the lifecycle ollama piece read should=on / actual=on / state=aligned /
  detail=11434 on 3 consecutive samples. Probes:
  watch/inbox/burn_wave_20260926/B2_81_probe_livework.json (live-work
  samples) and B2_81_probe_results.json (8 idle samples).
- Adjacent live datapoint, recorded honestly: the spawned janitor agent
  itself died with `[Errno 11001] getaddrinfo failed`
  (logs/orchestrator/t89fd1bad11.out.log) while numeric-IP probes succeeded,
  so this host's child-process name resolution is environment-fragile too;
  same disease family as the proxy interception, different mechanism, not
  claimed as the historical cause.
- Adjacent observation, not fixed in this lane: `_queue_depth()` and
  `_fleet_running()` count task REGISTRY records only, so queued-but-never-
  spawned entries in memory/runs/orchestrator/queue/ are invisible to the
  policy input (2 such entries existed at probe time, including this lane's
  own probe entry, vacated after sampling).

## Work done

- mag/lifecycle.py: added `OLLAMA_TAGS_URL` constant; rewrote `_ollama_up()`
  to return (up, cause) with a ProxyHandler({}) opener, 2.0s timeout x2
  tries, socket-connect fallback, and refusal-vs-unreachable cause strings;
  `_actual_process("ollama")` now reports that cause as the piece detail.
- tests/test_lifecycle.py: 3 new pins (test_ollama_probe_ignores_proxy_env,
  test_ollama_probe_socket_fallback_when_http_wedged,
  test_ollama_probe_absent_names_refusal).
- Probe artifacts registered: B2_81_probe_results.json,
  B2_81_probe_livework.json.
- Cleanup: this lane's queued probe entry q80f303dff8 vacated through the
  store writer (status failed, detail names the cleanup); task t89fd1bad11
  left as its own terminal record (failed, non-zero exit 1) as evidence.
- Gates: tests/test_lifecycle.py + tests/test_loop_death_guards.py 35
  passed; tests/test_temperature_stack.py + tests/test_improve_off_on.py +
  tests/test_doctor_scheduled_tasks.py 30 passed; ratchet
  `tools/violation_ratchet.py check --changed` PASS (NEW=0).

## Falsifier

Set `http_proxy` to a dead proxy in any process and run the OLD probe
against a live daemon: it returned False while the server answered (the 20
GIN-correlated rows are the historical proof). Under the NEW probe the same
env returns (True, '11434') on this machine, and
test_ollama_probe_ignores_proxy_env re-proves it hermetically with a local
HTTP server, so any regression that re-introduces proxy inheritance or
drops the socket fallback fails pytest. The refusal pin keeps the absent
case honest: if nothing listens, the detail must say refused, never
silently False.

## Bibliography closed

- mag/lifecycle.py:355-372 (old `_ollama_up`), 407-415 (old
  `_actual_process` ollama branch), 498-502 (start policy, unchanged)
- mag/temperature_stack.py:33 (GAPS_LOG), 381-430 (track_loop_gap, 12h
  dedupe), 485-510 (track_lifecycle_into_improve)
- mag/orchestrator.py:1587-1614 (list_tasks), 341-358 in lifecycle.py
  (_queue_depth/_fleet_running source), 920-990 (enqueue), 625+ (spawn_task)
- %LOCALAPPDATA%/Ollama: app.log, app-1..5.log (tray sessions), server.log,
  server-1..5.log (GIN request history), ollama.pid
- memory/training/loop_gaps.jsonl (the 89 rows)
- configs/providers.yaml:68-76 (ollama base 127.0.0.1:11434/v1,
  OLLAMA_HOST override)
- wmic process record PID 11112 (CreationDate 20260925235432.590813-240)
- watch/inbox/LIVING_HASH_LAW_20260926.md sections 5-6 (board edit shape)
