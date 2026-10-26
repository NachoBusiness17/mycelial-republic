# Shared surface: client config snippets (2026-10-17)

One MCP door for every seat: the warm pack (live chain tip, warm state, latest
notes, LIBRARY index, rule/invariant cards, per-seat preamble) as fixed
`mag://warm/*` resources, plus one write-back tool. Plan and inventory:
`watch/LIBRARY/SHARED_SURFACE_SELFSTEAL_20261017.md`. Code: `mag/warm_surface.py`,
`mag/mcp_server.py` (resources + `warm` profile), `mag/estate_bridge.py`
(`shared_receipt_append`), `scripts/mcp_stdio_shim.py`.

These are EXAMPLES. Nothing here was written into any client's real config.
No secrets appear below; the HTTP door's key is referenced by env var name only.

## What a seat gets

| Surface | What |
|---|---|
| `resources/list` | `mag://warm/tip`, `mag://warm/state`, `mag://warm/zknot`, `mag://warm/laws`, `mag://warm/library-index` (when present), `mag://warm/preamble/<seat>` for grok, gemini, deepseek, zcode, hermes, codex, cursor, claude, free |
| `resources/read` | the body for one of those URIs; redacted; unknown URI = JSON-RPC error -32002 |
| tool `estate_warm_read(uri)` | same bodies, for clients that only call tools |
| tool `estate_chain_verify()` | dry-run chain verify (read-only) |
| tool `estate_shared_receipt(seat, body, model?, title?)` | writes ONE new `watch/receipts/seat_<utc>_<seat>_<sha12>.json`; server stamps ts + sha256; 64 KiB cap; no path argument |

Boot ritual for any seat: read `mag://warm/preamble/<your seat>` (or call
`estate_warm_read` with that URI), work, then file the outcome with
`estate_shared_receipt`.

## Three doors (pick one per client)

Repo: `C:\Users\foste\Documents\projects\local_sovereign_agent` (below: `<REPO>`).
Python: `<REPO>\.venv\Scripts\python.exe` (never bare `python`: that is Hermes on this host).

- **A. Local stdio, `warm` profile (recommended; works now, no container change).**
  The client spawns `python -m mag.mcp_server --profile warm` with
  `PYTHONPATH=<REPO>`. Serves resources + the 3 warm tools; receipts land in
  the host `watch/receipts/`.
- **B. Container via the shim (always-on `mag-mcp`, 127.0.0.1:8766).** The client
  spawns `python <REPO>\scripts\mcp_stdio_shim.py`, which pipes stdio to the TCP
  bridge. The container bind-mounts `./mag` and `./tools`, so each new connection
  runs the current code: resources are served now. The service runs
  `--profile archivist`, so `estate_shared_receipt` is NOT on this door until the
  operator flips the compose `--profile` to `warm` and applies the compose change
  (see the bottom of this file).
- **C. HTTP `POST http://127.0.0.1:8001/mcp`** (`mag/mcp_http.py` on `mag/api_server.py`).
  Gated by the `X-API-Key` header; the key is read from env `MAG_API_KEY` on both
  sides. Serves the `full` profile + resources. Not listening at 2026-10-17
  survey time; use A or B until it is up.

## Gemini CLI: `%USERPROFILE%\.gemini\settings.json` (merge into `mcpServers`)

```json
{
  "mcpServers": {
    "mag-warm": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mag.mcp_server", "--profile", "warm"],
      "env": { "PYTHONPATH": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent" },
      "timeout": 60000,
      "trust": false
    },
    "mag-container": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\scripts\\mcp_stdio_shim.py"]
    },
    "mag-http": {
      "httpUrl": "http://127.0.0.1:8001/mcp",
      "headers": { "X-API-Key": "$MAG_API_KEY" }
    }
  }
}
```

## Codex: `%USERPROFILE%\.codex\config.toml`

```toml
[mcp_servers.mag_warm]
command = 'C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe'
args = ['-m', 'mag.mcp_server', '--profile', 'warm']
startup_timeout_sec = 60

[mcp_servers.mag_warm.env]
PYTHONPATH = 'C:\Users\foste\Documents\projects\local_sovereign_agent'

# Container door via the shim:
# [mcp_servers.mag_container]
# command = 'C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe'
# args = ['C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\mcp_stdio_shim.py']
```

(Codex HTTP servers take `url = "http://127.0.0.1:8001/mcp"` plus an env-sourced
header; check the field name for your Codex version, e.g.
`env_http_headers = { "X-API-Key" = "MAG_API_KEY" }`.)

## Cursor: `%USERPROFILE%\.cursor\mcp.json` (or `<REPO>\.cursor\mcp.json`)

```json
{
  "mcpServers": {
    "mag-warm": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mag.mcp_server", "--profile", "warm"],
      "env": { "PYTHONPATH": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent" }
    },
    "mag-http": {
      "url": "http://127.0.0.1:8001/mcp",
      "headers": { "X-API-Key": "${env:MAG_API_KEY}" }
    }
  }
}
```

## Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mag-warm": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mag.mcp_server", "--profile", "warm"],
      "env": { "PYTHONPATH": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent" }
    },
    "mag-container": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\scripts\\mcp_stdio_shim.py"]
    }
  }
}
```

## ZCode: MCP settings (standard `mcpServers` JSON)

ZCode keeps no MCP file in this repo (`.zcode/` has only extensions/launch/settings/tasks
JSON). Add it through ZCode's MCP settings using the standard shape below. The
exact file location depends on the ZCode build, so it is not verified here.

```json
{
  "mcpServers": {
    "mag-warm": {
      "command": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mag.mcp_server", "--profile", "warm"],
      "env": { "PYTHONPATH": "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent" }
    }
  }
}
```

## Hermes: `%USERPROFILE%\.hermes\config.yaml` (`mcp_servers:` block)

```yaml
mcp_servers:
  mag_warm:
    command: "C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe"
    args: ["-m", "mag.mcp_server", "--profile", "warm"]
    env:
      PYTHONPATH: "C:/Users/foste/Documents/projects/local_sovereign_agent"
  # container door:
  # mag_container:
  #   command: "C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe"
  #   args: ["C:/Users/foste/Documents/projects/local_sovereign_agent/scripts/mcp_stdio_shim.py"]
```

(Check the key names against `hermes --version`; `watch/hermes_wings/` is the
local study copy of Hermes' own MCP code.)

## Seats with no MCP (web chats, free models without tool calls)

Paste the preamble by hand. It's the same redacted body the resource serves:

```text
<REPO>\.venv\Scripts\python.exe -c "from mag.warm_surface import read_resource; print(read_resource('mag://warm/preamble/deepseek')['text'])"
```

(`scripts/gemini_warm_pack.ps1` stays the richer paste pack for the web Gemini seat.)

## Applying the compose change (operator / git window; NOT done by the agent)

`docker-compose.yml` now gives the `mcp` service one writable bind mount,
`./watch/receipts:/app/watch/receipts:rw`. `./watch` and `./memory` stay `:ro`.
It takes effect only when the service is recreated:

```text
cd C:\Users\foste\Documents\projects\local_sovereign_agent
docker compose up -d --no-deps mcp
```

To serve the receipt tool on the container door too, first change the service's
`--profile` argument from `archivist` to `warm` (docker-compose.yml, `mcp`
entrypoint), then run the same command.

## Later: beyond localhost (NOT done; design notes only)

- Serve only `--profile warm` off-box: fixed resources, dry verify, receipts. Never `full`/`builder`.
- Every body already passes `estate_bridge._redact` + `warm_surface.redact_text`
  (token shapes, private-key blocks, KEY=value lines, tailnet IPs, absolute home/repo paths).
- Transport: tailnet first (`tailscale serve` with the 127.0.0.1 origin), public only through
  a named cloudflared tunnel + Cloudflare Access. Never the `0.0.0.0` portproxy pattern.
- Before any exposure: replace the default gateway key, add per-seat keys and a receipt rate
  limit, and treat `watch/receipts/` as untrusted input until a local seat promotes it.
