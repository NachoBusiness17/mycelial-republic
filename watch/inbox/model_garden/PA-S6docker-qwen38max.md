# PA-S6docker-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## 1. LAN Attacker in 3 Moves

**Claim:** Port 8765 is the only published port without a loopback bind restriction.
**Source:** `00__docker-compose.yml`, mag service `ports` block:
`- "8765:8765"` (no `127.0.0.1:` prefix).
All sibling ports use the prefix: `"127.0.0.1:8000:8000"`, `"127.0.0.1:9000:9000"`, `"127.0.0.1:8001:8001"`.

**Claim:** The container binds all interfaces internally.
**Source:** `00__docker-compose.yml`, mag service environment: `MAG_BIND_HOST: "0.0.0.0"`.
**Source:** `01__Dockerfile`, ENV block: `MAG_BIND_HOST=0.0.0.0`.

**Claim:** The service answers HTTP on `/` and exposes API routes.
**Source:** `00__docker-compose.yml`, mag healthcheck: probes `http://127.0.0.1:8765/`.
**Source:** `00__docker-compose.yml`, AC13 comment names `/api/v1/verdicts` as a served route.

**3 moves:**
1. ARP scan or port sweep finds 8765 open on the Docker host.
2. GET `/` returns the dashboard (200 confirmed by healthcheck).
3. Enumerate `/api/v1/*` routes; any write or execution endpoint is the pivot. No auth layer is declared in the compose or Dockerfile.

## 2. Secrets into Containers

**Claim:** The entire `.env` file is injected into the mag container.
**Source:** `00__docker-compose.yml`, mag service: `env_file: - .env`.

**Claim:** The openclaw service (retired but defined) mounts the full project root read-only.
**Source:** `00__docker-compose.yml`, openclaw service volumes: `- ./:/mag:ro`.
This exposes `.env`, all source, all state to any process inside that container.

**Claim:** The mag source directory is mounted read-write into the running container.
**Source:** `00__docker-compose.yml`, mag volumes: `- ./mag:/app/mag`.
A compromised process inside the container can modify its own code on the host filesystem.

**Claim:** The retired ollama service mounts a host user directory by absolute path.
**Source:** `00__docker-compose.yml`, ollama volumes: `- C:/Users/foste/.ollama/models:/root/.ollama/models`.

## 3. Cheapest Real Hardening

| Fix | Effort | Effect |
|-----|--------|--------|
| Change `"8765:8765"` to `"127.0.0.1:8765:8765"` | 1 line | Closes the only LAN-reachable surface |
| Replace `env_file: .env` with explicit `environment:` keys listing only what mag needs | ~5 lines | Stops leaking unrelated secrets (COHERE, CEREBRAS, TS_AUTHKEY) into the container |
| Change `./mag:/app/mag` to `:ro` | 1 token | Prevents container-side code mutation of host source |

**Falsifier for this deliverable:** if Tailscale or a reverse proxy intentionally requires 8765 on a non-loopback interface for tailnet ingress, the loopback bind breaks the design. The compose header says "Tailscale sidecars provide tailnet-only access," which implies the sidecar should be the ingress path, not a raw port. If that is true, the fix stands.
