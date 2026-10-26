# PA-S6docker-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

**Stranger audit: mag container surface**
Assumptions: Docker Desktop on Windows, LAN attacker (same subnet, no creds), compose as shipped, all profiles default-off (only mag/redis/mcp/worker start).

**(1) LAN attacker, 3 moves**
- Move 1: port-scan; find 8765. `ports: - "8765:8765"` has no host-IP prefix (00, mag service), unlike its siblings `127.0.0.1:8000` etc. Docker Desktop forwards unprefixed publishes to 0.0.0.0 on Windows, so the dashboard is LAN-reachable. Move 2: fingerprint `/` and probe unauthenticated API routes (`/api/v1/verdicts`, verdicts panel referenced at AC13 comment). Move 3: read memory/ and watch/ contents if any read endpoint backs them; those dirs are rw-mounted into the container (`./memory:/app/memory`).
- Negative example (correct shape, sibling): `127.0.0.1:9222:9222` (browser) and `127.0.0.1:8766:8766` (mcp) are LAN-safe by construction.
- Redis is safe: `127.0.0.1:6379:6379`. Redis also lacks cap_drop/no-new-privileges, but it is not LAN-exposed.

**(2) Secrets into containers**
- `env_file: - .env` pulls the WHOLE .env into mag's process environment (00, mag). Any RCE or `GET /env`-style debug route in the app reads every secret at once.
- `CEREBRAS_API_KEY: "${CEREBAS_API_KEY:-}"` (00, openclaw, retired): key name typo. The real `CEREBRAS_API_KEY` silently resolves empty. UNVERIFIED: whether .env holds that spelling.
- Overmounts (blast radius if mag is popped): `./mag:/app/mag` rw (attacker rewrites own code), `./tools/gps_mcp`, `./models`, `./watch` rw. Positive counterexample: `./configs:/app/configs:ro`, `./main.py:/app/main.py:ro`.
- Autoclaw (02) passes `ZAI_CODING_KEY_1/2` as raw env; profile-gated `manual`, so not running.

**(3) Cheapest real hardening (patch, apply as-is)**

```yaml
    ports:
      - "127.0.0.1:8765:8765"
      - "127.0.0.1:8000:8000"
```

One line. Same pattern already proven by the 9222/8766 entries. Cuts the LAN surface to zero without touching auth, TLS, or the healthcheck (which probes 127.0.0.1 in-cage, unaffected).

Not theater / actually skip: cap_drop ALL + no-new-privileges on mag (already present); pinning redis minor; adding read_only to mag (breaks rw state mounts).

**Falsifier:** after the patch, `docker port mag-sovereign` shows only 127.0.0.1 bindings, and a LAN host gets connection-refused on :8765. If Windows still exposes 8765 (e.g. firewall port-forward), the patch is falsified and the surface is Docker-VM-level, not compose-level.
