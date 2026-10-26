# B7 - MAG-SOVEREIGN HEALTHCHECK: the 8h unhealthy lie (2026-09-30)

Date: 2026-09-30 (machine-clock bytes; dir stamp) · Lane: B7 (ZCode subagent)
Ownership: docker-compose.yml (mag service healthcheck) + Dockerfile (HEALTHCHECK)
Receipt: this file.

## Incident (tablet root cause #2)

`mag-sovereign` sat **UNHEALTHY for 8h** while the app served fine the whole
time. Nobody was paged because the probe itself was wrong.

## Root cause (diagnosed from live bytes, not guesses)

Old check (inherited from the image Dockerfile; compose `mag` had none):

```
CMD-SHELL python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/api/v1/health', timeout=15)"
```

Diagnosis steps and findings:

1. `docker inspect mag-sovereign --format '{{json .Config.Healthcheck}}'` → the
   urllib CMD above, interval 30s / timeout 20s / start_period 90s / retries 3.
2. Health log: every probe died with `urllib.error.HTTPError: HTTP Error 500`
   — NOT a connection refused, NOT `No module named ...`. Python exists
   (python:3.12-slim base); the port is live; the URL answered.
3. In-container probes: `/` → **200**; `/api/v1/health` → **500** with body
   `powershell.exe not resolvable: PATH carries no WindowsPowerShell
   directory and the System32 candidates are absent (B2-375)`.
4. Why: on :8765 the DASHBOARD serves that route via `h_health`
   (dashboard/rest.py:105) → `mag.health.sanity()` — the deep CAGE_DOCTOR
   sweep, whose B2-375 PowerShell resolution is host-Windows-only and can
   NEVER pass inside a Linux container. The /api/v1/health route that the
   check was presumably patterned after belongs to the GHOST daemon on
   :9000 (mag/ghost.py:1844), a different service.

So the check conflated liveness with a deep, OS-specific sanity sweep: the
container was up, serving 200s on `/`, and reporting unhealthy forever.

## Fix (probe the liveness surface)

Both owning files now probe `http://127.0.0.1:8765/` — the same URL
mag_launch.py itself gates dashboard health on — via python urllib
(`curl`/`wget` are ABSENT from python:3.12-slim; verified with
`command -v` in-container; python IS in-image, the sanctioned fallback):

- `Dockerfile` HEALTHCHECK: `--interval=15s --timeout=5s --start-period=30s
  --retries=3`, CMD probes `/` with timeout=4.
- `docker-compose.yml` mag service: explicit `healthcheck:` block (compose
  overrides the image default, so the fix is live without an image rebuild),
  same shape, with the fix-comment carrying this receipt.

Deep-sweep health stays reachable at `/api/v1/loop/health` and the sanity
route itself — untouched, outside this lane's ownership.

## Verification (bytes)

```
docker compose up -d --no-build --force-recreate mag   → Recreated/Started
docker inspect .Config.Healthcheck  → CMD python -c "...urlopen('http://127.0.0.1:8765/'..."
docker ps   → "Up About a minute (healthy)"  × 3 consecutive polls
              (healthy inside the FIRST 15s interval, well under 3 intervals)
State.Health.Log → exit codes: 0 0 0 0 0
host curl http://127.0.0.1:8765/ → 200
```

Port bindings after recreate (8765 broad binding KEPT, not reverted — the
prior landing stands; everything else stays loopback):

```
8000/tcp -> 127.0.0.1:8000      9000/tcp -> 127.0.0.1:9000
8001/tcp -> 127.0.0.1:8001      8765/tcp -> 0.0.0.0:8765 + [::]
```

## Findings for the operator (not this lane's call)

- **Image rebuild deferred.** `docker compose up -d --build` was attempted
  twice; the build context carries `corpus/` (8.2 GB, NOT in .dockerignore)
  → a 24-minute 1.68 GB context transfer that the engine then canceled
  (`http2: server: error reading preface ... file already closed`). The
  compose override is authoritative at runtime, so the container is healthy
  NOW; the Dockerfile fix lands in the image at the next natural rebuild.
  Dockerignoring `corpus/` would cut the context by ~5x but changes baked
  image contents — operator decision, not mine.
- No Python tree changed (compose + Dockerfile only) → no pytest numbers
  claimed here; nothing for the census to move.
