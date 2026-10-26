# PA-S6docker-grok47 (grok-4.7 @ xai, turn 1, channel: content)

**Stranger audit, compose surface only.** Instrument: pasted `S6docker/00__docker-compose.yml` plus `01__Dockerfile` and `02__docker-compose.yml`. Moment: file bytes as shown (00 truncated mid-openclaw; tail of worker/mcp seen). Assumption: default `docker compose up` (no `--profile`). Auth on `:8765` is **UNVERIFIED** (no server.py in this packet).

### (1) LAN, 3 moves
Only non-loopback publish is mag `8765:8765` (no `127.0.0.1:` prefix). Redis `6379`, mag `8000/9000/8001`, mcp `8766`, browser `9222`, retired ollama `11434` are loopback-mapped. OpenClaw has no host port (`network_mode: service:tailscale-openclaw`) and is profile `retired-openclaw`, so it is down unless resurrected.

1. Connect to `<lan-ip>:8765`. In-container `MAG_BIND_HOST=0.0.0.0` is what the proxy dials; the host mapping is what puts it on the LAN. Comment "Public ingress is intentionally absent" is false for this one port.
2. `GET /` is a live 200 (healthcheck uses that URL). Dashboard, verdicts (`/api/v1/verdicts`), and the shared gps ledger are on that process. Whether routes require auth: **UNVERIFIED**.
3. That process has writable host trees: `./memory`, `./watch`, `./logs`, `./state`, `./queue`, `./jobs`, `./mag` (not `:ro`), `./dashboard`, `./tools/gps_mcp`, `./models`. A write the app accepts lands on the host. `extra_hosts: host-gateway` lets the container reach host Ollama `:11434` and Bionic `:1234`. Not proven RCE. Proven: one LAN socket plus a fat rw bind set.

NAME != SERVICE: service `mag`, container `mag-sovereign`. Probe the service publish, not the name.

### (2) Secrets and overmounts
`env_file: .env` on `mag` and (if profile up) `openclaw` injects the whole file into process env. OpenClaw also interpolates `COHERE_API_KEY_PAID` and `CEREBAS_API_KEY`. Dockerfile `COPY . .` can bake `.env` into image layers if `.dockerignore` does not exclude it: **UNVERIFIED**.

Overmounts (image copy shadowed): `./mag:/app/mag` rw, `./dashboard`, `./main.py:ro`, `./mag_launch.py:ro`, `./tools/gps_mcp`. OpenClaw, if up: `./:/mag:ro` plus writable `./watch:/board` and `./queue/handoff/openclaw/PATCHES:/patches` (host apply path). Retired ollama bind: `C:/Users/foste/.ollama/models`. `02` autoclaw is profile `manual`; keys in env; `./board` and `./workspace` rw. Not the default fleet.

### (3) Cheapest real hardening
One line. Do not flip in-container bind to `127.0.0.1` (mcp comment: proxy dials container IP, loopback-in-cage is a blackhole).

```yaml
ports:
  - "127.0.0.1:8765:8765"
```

Same shape as `8000/9000/8001`. That removes the LAN socket. Theater would be another `cap_drop` comment while `8765` stays `0.0.0.0`.

**Falsifier:** after recreate, `docker port mag-sovereign 8765` must show `127.0.0.1:8765` only. A second host on the LAN must get connection refused. If it still shows `0.0.0.0:8765`, the patch did not land.

Negative: publishing `8765:8765` "because MAG_BIND_HOST is 0.0.0.0". Positive: keep `0.0.0.0` inside, pin the host side to loopback, same as mcp `8766`.
