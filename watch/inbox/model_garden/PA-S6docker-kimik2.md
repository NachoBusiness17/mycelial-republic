# PA-S6docker-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

## STRANGER AUDIT: Mag Container Surface

### (1) LAN Attacker, 3 Moves

**Move 1:** Scan 0.0.0.0:8765 on any host interface (docker-proxy binds 0.0.0.0:8765→container:8765 per 00__docker-compose.yml:44).

**Move 2:** POST to /api/v1/verdicts or any unauthenticated route (dashboard server.py GPS_LEDGER_DB surface at 00__docker-compose.yml:58 comment; no auth middleware visible in compose).

**Move 3:** Write to overmounted paths: `./memory:/app/memory`, `./state:/app/state`, `./queue:/app/queue` (00__docker-compose.yml:48-53) — host directories become attacker-controlled if container process is compromised.

**Verdict:** Full read/write on mag_net services (redis:6379 unauthenticated inside bridge), arbitrary file write to host via volume escapes, probable code execution via healthcheck python -c injection if attacker can influence environment (unverified: entrypoint.sh not provided).

---

### (2) Secrets Handling

| Mechanism | Finding | Citation |
|-----------|---------|----------|
| .env file | `env_file: - .env` (00__docker-compose.yml:13) — **host file, container sees all keys** | 00__docker-compose.yml:13 |
| BIONIC_BASE_URL | `${BIONIC_BASE_URL:-...}` default leaks host.docker.internal to container | 00__docker-compose.yml:28 |
| TS_AUTHKEY | `${TS_AUTHKEY:-}` empty-default in retired-openclaw profile | 00__docker-compose.yml:159 |
| ZAI_CODING_KEY_* | Passed raw to autoclaw in 02__docker-compose.yml:6-7 |

**Overmounts (host→container, read-write unless noted):**
- `./memory`, `./state`, `./queue`, `./jobs`, `./logs` — **RW** (00__docker-compose.yml:48-52)
- `./tools/gps_mcp` — **RW, sqlite ledger shared with host X11 feed** (00__docker-compose.yml:58-61 comment)
- `./configs:ro`, `./tests:ro`, `./main.py:ro` — **read-only** (correct)

**Critical:** `read_only: false` on mcp service (00__docker-compose.yml:242) despite archivist profile; no `tmpfs` for `/tmp`.

---

### (3) Cheapest Hardening (Not Theater)

| Fix | Cost | Falsifier |
|-----|------|-----------|
| `MAG_BIND_HOST: "127.0.0.1"` + remove 0.0.0.0 port publish | One line | `curl http://$(hostname -I):8765` from LAN host still connects |
| `read_only: true` on mag + `tmpfs: /tmp:rw,noexec,nosuid,size=100m` | Two lines | Container fails to write logs/queue/state (proves overmounts wrong) |
| Drop `./memory`, `./state` from mag if not needed by runtime | Audit + removal | `docker exec mag-sovereign ls /app/memory` succeeds after patch |
| Redis `requirepass` + network isolation (not mag_net bridge to all) | One secret, one network key | `redis-cli -h redis ping` from browser container still works |
| `cap_drop: ALL` already set — add `seccomp: ./mag-seccomp.json` | One file | `strace -f docker run ...` shows blocked syscalls (openat, connect, etc.) |

**Not theater:** seccomp-bpf with errno default (blocks ~300 syscalls, costs 50KB JSON). **Is theater:** `security_opt: no-new-privileges` when container already runs as root (Dockerfile lacks USER).

---

### Deliverable: 3-Line Patch

```diff
--- a/00__docker-compose.yml
+++ b/00__docker-compose.yml
@@ -15,7 +15,7 @@ services:
       PYTHONUTF8: "1"
-      MAG_BIND_HOST: "0.0.0.0"
+      MAG_BIND_HOST: "127.0.0.1"
       MAG_CONTAINER: "1"
@@ -42,7 +42,7 @@ services:
       - redis
     ports:
-      - "8765:8765"
+      - "127.0.0.1:8765:8765"
       - "127.0.0.1:8000:8000"
@@ -47,6 +47,9 @@ services:
       - ./jobs:/app/jobs
       - ./configs:/app/configs:ro
+    read_only: true
+    tmpfs:
+      - /tmp:rw,noexec,nosuid,size=100m
     security_opt:
       - no-new-privileges:true
```

**Falsifier:** `nmap -p8765 <docker-host-ip>` from adjacent LAN host shows port filtered (not open) after `docker compose up`.
