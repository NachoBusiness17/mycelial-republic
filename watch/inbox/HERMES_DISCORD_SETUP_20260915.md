# Hermes Discord bot — setup state receipt · 2026-09-15

**Lane:** Hermes seat (Sancho) · Discord messaging gateway
**Status: EVERYTHING DONE except one operator click.** Bot online, token live,
gateway connected — Mag is locked out of exactly one channel by a Discord
channel-permission overwrite, removable only by the account owner.

## Verified done (this window, 2026-09-15 11:00–13:00 local)

| item | evidence |
|---|---|
| New bot token landed in `%LOCALAPPDATA%\hermes\.env` | lander output `WROTE replaced=1 len=72 last4=1CrM` + `/users/@me` 200 → `Mag` id `1543788780270518373` (operator reset the token in-portal ~10:00; old N5UA token invalidated → 4004 at 09:54 in gateway.log) |
| Gateway restarted on the new token | `hermes gateway stop` → PowerShell Start-Process `hermes gateway run`; gateway.log `2026-09-15 10:07:28 [Discord] Connected as Mag#2124` → `✓ discord connected`; Telegram reconnected 10:07:36 |
| `bot_require_code_grant` flipped OFF | public RPC: `bot_require_code_grant: True` before → `False` after operator toggle (this flag caused "integration requires code grant" on every authorize attempt) |
| Bot authorized into guild | probe: `GUILDS: NT-ACv2 (799817554549800982)` (operator switched browser account realsaltybear2741 → nachoquixotic and clicked Authorize) |
| Bot can DM its owner | DM channel opened + message delivered: `DM_SENT id=1549428979495206943` — **the re-authorize link is sitting in nachoquixotic's Discord DMs from Mag** |

## The one remaining blocker

`POST /channels/1050760558883913780/messages` → **403 Missing Access (50001)**.
The bot's role (`Mag`, perms `274878286912`: view/send/embed/attach) is beaten by a
**channel-level permission overwrite on #game-c-overview** — direct channel GET also 403s.
Bot cannot self-elevate (no MANAGE_ROLES anywhere).

## Either fix ends it (operator hands, owner account)

1. **Click the link in Mag's DM** (admin re-invite, guild pre-pinned) — bypasses all channel locks.
2. **Or** Discord app → #game-c-overview → ⚙ Edit Channel → Permissions → add role **Mag** →
   View Channel + Send Messages on.

After either: typing in #game-c-overview gets a gateway response natively
(no watcher needed). Verification harness:
`%LOCALAPPDATA%\Temp\discord_state_probe_20260915.py` (identity/guilds/post) ·
`discord_perm_probe_20260915.py` (role + overwrite diagnosis) — run with
`hermes-agent\venv\Scripts\python.exe`.

## Notes for the next seat

- Gateway autostart: `Hermes_Gateway.vbs` login item installed + desktop app shows "Gateway ready".
- The gateway's Telegram lane was green throughout; Discord adapter healthy (169 slash commands registered).
- Token hygiene: the current token passed through chat twice (operator pasted); rotate clipboard-only
  when convenient (3 clicks + `%TEMP%\discord_token_land.py`).
- Clusterfuck ledger (all Discord-side, zero Hermes-side): WebAuthn login trap in the desktop-app
  webview → code-grant flag → wrong account in default browser → channel overwrite. Four locks, one door.

## Addendum — 2026-09-15 11:53: BOT ANSWERING IN DISCORD + truncation fix

- Operator screenshot: Sofan @Mag in Discord → Mag replied and ran terminal tools.
  Full chain live: Discord → Hermes gateway → agent + tools → reply.
- New fix: AGENTS.md (21,262 chars) was truncated by the context-file cap
  ("TRUNCATED: exceeds limit of 20000"). Root cause: dynamic cap fell to the 20k
  floor (context length unknown at prompt-build) despite the 262k model window.
- Pinned `context_file_max_chars: 40000` in `%LOCALAPPDATA%\hermes\config.yaml`
  (backup `.bak-20260915`; YAML validated), gateway recycled → both platforms
  reconnected 11:51. AGENTS.md now loads whole.
- Known pre-existing wart (not blocking): `hosted_room_worker` dies on
  `sqlite3.OperationalError: database is locked`, supervisor gives up after 5
  fast restarts; messaging platforms unaffected.
