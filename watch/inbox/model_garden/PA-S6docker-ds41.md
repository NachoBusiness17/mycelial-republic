# PA-S6docker-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

## Stranger audit: mag container surface

**Scope.** All claims cite `00__docker-compose.yml` (the live stack). The `02__` file is a three-line sibling project, not this fleet.

### 1. LAN attacker, three moves

Move 1: scan `8765` on the host. Line 40 publishes `"8765:8765"` on **0.0.0.0**, and `MAG_BIND_HOST: "0.0.0.0"` (line 17) means the app also listens on all interfaces inside the cage. Every other port (8000, 9000, 8001, 6379, 8766, 9222, 11434) is bound to `127.0.0.1`. 8765 is the only door. The header comment "Public ingress is intentionally absent" (line 2) is falsified by line 40.

Move 2: fetch `/`. The dashboard mounts `./dashboard`, `./mag`, `./configs`, and `./watch` as bind mounts (lines 47-56). Whatever the app serves is live host source. No auth is configured in this file.

Move 3: hit any write surface the app exposes. `MAG_RUNTIME_ROLE: "authoritative"` (line 20) plus `./queue`, `./jobs`, `./state`, `./memory`, `./watch` writable (lines 45-52) means app-level write RCE lands in files the host later reads and applies.

**Falsifier for move 3:** if `mag/` enforces auth before any mutating route, the third move downgrades to read-only exfiltration. That check is outside this file. Marked UNVERIFIED.

### 2. Secrets into containers

`.env` is read by `mag` (line 15) and `openclaw` (retired profile). Every var in `.env` enters both processes. There is no `env_file` scoping, no `secrets:` block. `COHERE_API_KEY_PAID` is remapped to `COHERE_API_KEY` for openclaw (line ~"COHERE_API_KEY") - a naming trick, not isolation.

**Overmounts.** `./mag:/app/mag` (line 47) is rw and covers the shipped code with host code. `./tools/gps_mcp:/app/tools/gps_mcp` (line 66) is rw and carries a sqlite ledger the panel reads. `./tests:ro` and the two `:ro` main.py bindings (lines 68-71) are the only ro source mounts. `mcp` service is properly `:ro` throughout (lines ~"mcp" block). `./watch` is mounted into mag rw (line 47) **and** into openclaw as `/board` rw - one directory, two writers, cross-service.

### 3. Cheapest non-theater hardening

Change line 40 from `"8765:8765"` to `"127.0.0.1:8765:8765"`. Same one-line pattern already used on 8000/9000/8001/6379/8766/9222 (lines 41-44, 79, ~"mcp"). This closes the LAN door without touching app code, without TLS theater, without a reverse proxy.

Then: flip `./mag` and `./tools/gps_mcp` to `:ro` (lines 47, 66) and stop overwriting shipped code from the host. If mag needs to write, it already has `./state`, `./logs`, `./memory`.

**What is theater here:** adding `cap_drop`/`no-new-privileges` (already present, lines 57-59), or a firewall rule, while line 40 stays open.

**Deliverable falsifier:** if `mag` serves a public-facing health/ingest endpoint that an external Tailscale peer is contractually promised, loopback-only breaks that promise. No such peer is named in this file.
