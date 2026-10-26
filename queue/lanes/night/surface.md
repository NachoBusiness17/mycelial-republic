# NIGHT LANE SURFACE - env door landed, march leg re-fire pending

Register row: corpus/steal/MASTER_READ_ESTATE.md section 9, r05#2 ("28 rc=1
composites ... mount .env read-only into the cage compose or pass the two ZAI
keys through the sanctioned env door, rerun the march leg, and bank the rc=0
receipt"). Executed 2026-10-05 by lane e10-env-door. Cause named 2026-10-04 in
watch/inbox/night_shift_20261004/night_march_cured.md (compose delivered .env
as env vars only; /app/.env absent in cage; march_228.py key is FILE-ONLY by
operator law).

## 1. The env door (EXECUTED, byte-verified)

docker-compose.yml, mag service volumes, landed this lane:

    - ./.env:/app/.env:ro

with the cause+receipt comment block above it (night march crash lineage,
2026-10-04 receipt pointer, AC13 file-bind caveat reasoning). Compose
validation: `docker compose config --quiet` exit 0.

Container recreated: `docker compose up -d mag` -> "Container mag-sovereign
Recreated / Starting / Started", then "mag-sovereign Up 8 seconds (healthy)".

In-cage verification (docker inspect + exec, key NAMES only, values never
printed):

    C:\Users\foste\Documents\projects\local_sovereign_agent\.env -> /app/.env (ro)

    exists: True
    total keys: 56
    zai key names: ['ZAI_API_KEY', 'ZAI_API_KEY_2', 'ZAI_API_KEY_3', 'ZAI_API_KEY_Pro']
    march KEY resolves in cage: True
    march ROOT: /app

The door is open: the march module now finds its key inside the cage. This is
the cure for the 28 rc=1 composites (crash class) and the 2026-10-04 rc=2
honest skip (no-key class).

## 2. March leg fired twice in-cage: auth passed, account 429 (DEVIATION)

Exact trigger command (both runs):

    docker exec mag-sovereign python /app/watch/march_228.py

Run 1 (2026-10-05T14:28Z) and run 2 (~14:33Z, after a 4 minute cool-down),
identical outcome:

    MARCH COMPLETE: 8 processed | HALTED: ok-rate 0.00 < 0.90 at tranche 8

signals loaded 1265 (up from the 836 the 2026-10-04 receipt counted); every
call in tranche 8 returned HTTP 429 and the march's own halt gate stopped the
run at width 8, exit code 0 (halt is designed, not a crash). Flight ledger
watch/flight_recorder.jsonl rows 1446-1448 verbatim shape:

    "subsystem": "march", "latency_ms": 1092.6, "status": "error", "error_code": "HTTP429"

Read: the requests LEFT the cage carrying the Pro key (a bad key yields 401,
not 429; latencies ~1.1-1.4s are real round trips). The account is rate
saturated mid-burn: this executor workflow's own sibling lanes run on the same
zai plan. The march rc=0 WITH ok-calls therefore cannot land inside this
sitting; banking it from a 0-ok halt would be a hollow batch (STANDING_RAILS:
empty is not success). Recorded, not faked.

## 3. Full composite trigger: out-of-window (expected)

    2026-10-05T14:28:56Z lane=night result=out-of-window (0.5s)
    night: out-of-window
    LANE_RUNNER_RC=0

The cycle_night in-window guard (mag/lane_runner.py, local hour 23:00-09:00)
held, as designed. Re-fire path: tonight's 23:00 local daemon cycle (once-per-
night gate is open: runner_state.json last_night=2026-10-04) will run monitor
rc=0 + march with the key now present. That composite row is the in-window
confirmation this receipt awaits. Manual re-fire command if needed off-peak:

    docker exec mag-sovereign python /app/watch/march_228.py

(or the full composite: `docker exec mag-sovereign python -m mag.lane_runner
--lane night --once`, which respects the window guard).

## 4. Side effect parked during this lane: host publish 8765 (operator, admin)

Recreating the container hit: "ports are not available: exposing port TCP
127.0.0.1:8765 ... bind: An attempt was made to access a socket in a way
forbidden by its access permissions". Root cause (diagnosed in-session): a
Windows portproxy rule "0.0.0.0:8765 -> 127.0.0.1:8765" served by svchost
iphlpsvc (pid 4972; `netsh interface portproxy show all`) grabbed the wildcard
the moment the old container released the port; docker-first bind had coexisted
with it for the previous 41h, iphlpsvc-first blocks docker. Shell is non-admin
so the rule cannot be deleted here. The 8765 publish line is PARKED (commented,
with cause+operator cure) in docker-compose.yml; the other three publishes
(8000/9000/8001) are live. Operator cure, admin shell:

    netsh interface portproxy delete v4tov4 listenport=8765 listenaddress=0.0.0.0

then uncomment the 8765 publish line in docker-compose.yml and
`docker compose up -d mag` (docker-first bind wins the race, as the 41h
coexistence proved). Until then the dashboard door is dark on the host; no
scheduled host-side poller of 8765 was found (consumers are one-shot probes:
desk_baseline_probe, harness_eval, roadmap_gap_probe).

## 5. Tests (green, this session)

Instrument from the 2026-10-04 cure receipt, `.venv/Scripts/python.exe -m
pytest -q -p no:cacheprovider`:

    tests/test_night_march_cure_20261004.py
    tests/test_lane_runner_cluster.py
    tests/test_monitor_lane_rotation.py
    -> 39 passed in 3.54s

Compose-touching suites (they parse docker-compose.yml):

    tests/test_container_setup.py tests/test_docker_ops.py
    tests/test_reconnect_cage_first.py
    -> 10 passed in 9.09s

## 6. Residuals

1. march rc=0 with ok-calls: re-fires tonight 23:00 local in-window (or manual
   off-peak); blocked tonight-in-this-sitting by account 429 only. The env door
   itself is landed and proven.
2. Host publish 8765: parked, needs the admin portproxy delete above.
3. The composite's march leg timeout is 600s (mag/lane_runner.py _run_script);
   with 1265 open signals the full march may exceed it at width 50. Not this
   lane's fix; flagged for the register (worth a width/tranche-budget look
   after the first clean in-window run).
