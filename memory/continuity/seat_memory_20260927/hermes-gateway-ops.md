---
name: hermes-gateway-ops
description: Hermes gateway ops knobs — context_file_max_chars pin (20k-floor
  gotcha truncated AGENTS.md even on a 262k model), context_length_cache.yaml,
  40-60s cold-start, sqlite hosted_room wart, reusable %TEMP% probes
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

Hermes gateway (`%LOCALAPPDATA%\hermes\`) operational knobs, learned fixing Mag's first live Discord answer on 2026-09-15 (see [[discord-hermes-bot-wiring]]):

- **Context-file cap:** `context_file_max_chars` is a top-level key in `config.yaml`; explicit value wins over the dynamic cap (agent/prompt_builder.py ~L1022-1044: dynamic = context_length × 4 chars/token × 0.06, clamped [20k floor, 500k ceiling]). **Gotcha:** when the model's context length is unknown at prompt-build, the cap falls to the 20,000-char floor — Mag's first Discord reply led with "⚠️ Context file AGENTS.md TRUNCATED: 21262 chars exceeds limit of 20000" despite a 262k model. Fixed by pinning `context_file_max_chars: 40000` (backup `config.yaml.bak-20260915`, YAML validated with the hermes venv python, gateway recycled).
- **AGENTS.md is 21,262 chars** — any Hermes context-file cap must stay ≥ that. Config.yaml ends in comment lines, so appending a top-level key at column 0 is safe.
- **Model windows** cached in `%LOCALAPPDATA%\hermes\context_length_cache.yaml` (key = model@endpoint): ling-3.0-flash-sante:free = 262,144 · deepseek-v4-flash-vision-exp = 1,048,576 · gpt-6-astra = 1,050,000 · gemma4 = 131,072 · gemma:2b = 8,192.
- **Restart:** `hermes.exe gateway stop` (drains cleanly) → `powershell Start-Process -WindowStyle Minimized -FilePath '…venv\Scripts\hermes.exe' -ArgumentList 'gateway','run'`. Cold start takes **~40-60s** before `[Discord] Connected as Mag#2124` + `✓ discord connected` appear in the canonical log `%LOCALAPPDATA%\hermes\logs\gateway.log` — grep with line TIMESTAMPS, stale tracebacks live there forever.
- **Known wart (non-blocking):** supervised `hosted_room_worker` dies on `sqlite3.OperationalError: database is locked`; supervisor gives up after 5 rapid restarts; messaging platforms unaffected. Pre-existing, unfixed.
- **Reusable probes** in `%LOCALAPPDATA%\Temp\`: `discord_state_probe_20260915.py` (identity/guilds/test-post), `discord_perm_probe_20260915.py` (member roles → guild roles → channel overwrites → effective perms), `discord_dm_link_20260915.py` (bot→owner DM delivery), `discord_token_land.py` (clipboard → .env → identity, masked). All SSRF-hardened to pass the Mimosa write-guard.
- Full setup receipt + addendum: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md`.
