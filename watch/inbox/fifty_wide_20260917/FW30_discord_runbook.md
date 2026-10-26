# FW-30 — Discord two-click runbook (operator gate packet)

- Board item: `watch/inbox/FIFTY_WIDE_BOARD_20260917.md:56` — "the two clicks (token rotation + #game-c-overview 403 grant) as a one-page card"
- Source: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md` (setup-state receipt); `watch/inbox/wave_20260916/receipts/D20_BONES_ADAPTER.md` (adapter + gates)
- Packet filed: 2026-09-28, Q-025 queue gopher. Adapter dry-run re-executed 2026-09-28 (see section 4).

## The one-page card

### CLICK 1 — rotate the Discord bot token (hygiene, ~3 clicks)

Why: the current token passed through chat twice (operator pasted it during setup;
HERMES_DISCORD_SETUP_20260915.md:41-42, and OPERATOR_ASK_20260916.md:40-41 ask #10).

1. Discord Developer Portal -> your bot application -> Bot -> Reset Token.
2. Copy the new token to clipboard ONLY (do not paste it into any chat).
3. Land it: `python %TEMP%\discord_token_land.py` (the lander HERMES_DISCORD_SETUP_20260915.md:42
   references; it writes `%LOCALAPPDATA%\hermes\.env` var `DISCORD_BOT_TOKEN` and prints only
   length + last 4, e.g. `WROTE replaced=1 len=72 last4=…`).
4. Recycle the gateway so both old-token sessions die: `hermes gateway stop`, then relaunch
   (`Hermes_Gateway.vbs` or `hermes gateway run`). Expect `Connected as Mag#2124` in gateway.log.

Note: live /bones boots read the token from `%LOCALAPPDATA%\hermes\.env` at process start
(D20_BONES_ADAPTER.md law 2); the token value is never printed or copied into files.

### CLICK 2 — grant #game-c-overview (unlocks the channel, ~2 clicks)

Why: posting to channel `1050760558883913780` returns `403 Missing Access (50001)`; a
channel-level permission overwrite beats the bot role (view/send/embed/attach), and the bot
cannot self-elevate (no MANAGE_ROLES) (HERMES_DISCORD_SETUP_20260915.md:20-23).

Either fix ends it (owner account only) (HERMES_DISCORD_SETUP_20260915.md:25-29):

- **Option A:** click the re-authorize link sitting in nachoquixotic's Discord DMs from Mag
  (admin re-invite, guild pre-pinned; DM_SENT id=1549428979495206943) — bypasses all channel locks.
- **Option B:** Discord app -> NT-ACv2 -> #game-c-overview -> Edit Channel (gear) -> Permissions ->
  add role **Mag** -> allow **View Channel** + **Send Messages**.

## Verify (30 seconds, after either click)

Channel check: type anything in #game-c-overview; the Mag gateway should respond natively
(no watcher). Deeper probes, run with `hermes-agent\venv\Scripts\python.exe`
(HERMES_DISCORD_SETUP_20260915.md:32-35):
`%LOCALAPPDATA%\Temp\discord_state_probe_20260915.py` (identity/guilds/post) and
`discord_perm_probe_20260915.py` (role + overwrite diagnosis).

Adapter check (repo venv, dry-run, no token read) — executed 2026-09-28 by this packet, EXIT=0:

```
.venv\Scripts\python.exe -m mag.bones_adapter --check
[bones-adapter] guild 799817554549800982 (NT-ACv2), channel 1050760558883913780 (#game-c-overview)
  /bones start | /bones move | /bones status | /bones receipt | /bones verbs
[bones-adapter] 5 subcommands registered; connect skipped (--check)
```

## Then the referee goes on air (what the clicks unlock)

```
.venv\Scripts\python.exe -m mag.bones_adapter
```

Live boot syncs the five /bones subcommands to guild NT-ACv2 `799817554549800982` and answers
only in #game-c-overview `1050760558883913780` (D20_BONES_ADAPTER.md "Exact launch commands").
The adapter refuses to be useful before both gates clear — that is by design (D20 gates section:
"Token rotation pending" + "403 permission click pending", both still unchecked).

Order law: do CLICK 1 before the live boot (the D20 gate list names rotation first; the token in
.env predates the setup note). CLICK 2 can happen any time before or after CLICK 1.

## Known non-blockers (do not re-debug these)

WebAuthn desktop-app trap, code-grant flag (already flipped OFF 09-15), wrong-account browser,
AGENTS.md context truncation (fixed, pinned 40000 chars) — all closed in the 09-15 receipt
addendum. `hosted_room_worker` sqlite lock stays a known pre-existing wart, messaging unaffected
(HERMES_DISCORD_SETUP_20260915.md:43-58; separately tracked as FW-44).

## What this packet did NOT do

No portal click, no token touched, no DM opened, no live gateway boot. The dry-run --check was
the only execution (read-only, no token read, no connect). Both clicks stay operator-gated.

Receipt: `watch/inbox/burn_reset_20260927/queue/Q-025.md` (FW-30 section).
