# T1W2_S6_docker (anthropic/claude-opus-5.5, turn 1, channel: content)

# STRANGER AUDIT: mag container surface

**Measurement conditions.** This is a static read of `docker-compose.yml` and the `Dockerfile` as pasted, at audit time. I ran no scan. Line numbers come from counting the evidence. The host is Docker Desktop on Windows (`C:/Users/foste`). Windows Firewall state is **UNVERIFIED**.

## (1) LAN attacker, 3 moves

1. **Find the port.** Compose line 41 reads `- "8765:8765"`. It has no host IP, so the port publishes on `0.0.0.0` of the host and is reachable from the LAN. This contradicts compose line 6 (`http://127.0.0.1:8765/`) and Dockerfile line 3 (`Host exposes only localhost ports`). Every other port is `127.0.0.1`-prefixed (lines 42-44).
2. **Hit the dashboard.** Dockerfile line 2 says `Agent tools, backend, and subprocesses run inside this cage`. Whether auth exists is **UNVERIFIED** because server.py is not in the evidence. There is no `USER` line in the Dockerfile, so the process runs as root in-container. `cap_drop: ALL` (lines 69-70) limits escape, not data access.
3. **Harvest.** Several things open up from inside the cage:
   - `/proc/self/environ` holds every `.env` key (`env_file: - .env`, lines 16-17).
   - Redis on `mag_net` has no `requirepass` set anywhere.
   - `host.docker.internal:11434` and `:1234` reach the host LLMs (lines 28, 35, 73).

## (2) Secrets and mounts

- **Writable code overmount.** Line 53 reads `- ./mag:/app/mag`, with no `:ro`. This mount shadows the image's `COPY . .` (Dockerfile line 21), and the container can rewrite host source. The worker gets the same code `:ro`, and host-shell Python imports it too (`mag/lm_studio.py`, per line 32). A compromise of the cage therefore becomes persistence on the host.
- **Possible baked secrets.** `COPY . .` may bake `.env` into the image. This is **UNVERIFIED** because no `.dockerignore` is in the evidence.
- **Retired openclaw (dormant until resurrected).**
  - `- ./:/mag:ro` mounts the whole repo, `.env` included.
  - `- ./watch:/board` is writable, and mag reads `./watch` (line 47). That is a prompt-injection lane.
  - Line numbers are **UNVERIFIED**.
- **Contrast case: mcp.** It has no `env_file` and all of its mounts are `:ro`. That is the correct pattern.

## (3) Cheapest real hardening

**Patch (apply as-is):**
```diff
-      - "8765:8765"
+      - "127.0.0.1:8765:8765"
-      - ./mag:/app/mag
+      - ./mag:/app/mag:ro
```

**Why each change is not theater:**

| Change | Effect |
|---|---|
| `127.0.0.1:8765:8765` | Removes move 1, which is the only LAN-reachable socket. |
| `./mag:/app/mag:ro` | Severs the container-to-host code write path. |

**Theater, do not count these as fixes:**

- Rotating API keys while 8765 stays on `0.0.0.0`. The new keys leak the same way.
- Adding `read_only: true` to mcp. It already mounts everything `:ro`.
- Setting a Redis password. Redis is already loopback-only on the host (`127.0.0.1:6379`), and the attacker reaches it from inside mag anyway.
- Relying on the "Public ingress is intentionally absent" comment (line 2). A comment is not a bind.

**Falsifiers:**

- **Bind fix.** From a second LAN machine, run `curl http://<host-LAN-IP>:8765/`. Before the patch it returns 200 (unless the firewall blocks it). After the patch it is refused. If it is refused before the patch, the firewall was already the real control and move 1 was overstated.
- **`:ro` fix.** If mag logs `Read-only file system` under `/app/mag` after the patch, it writes its own code at runtime. Find that writer before landing the change.
