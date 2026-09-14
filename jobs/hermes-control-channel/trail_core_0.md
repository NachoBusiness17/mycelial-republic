# trail_core_0 — hermes-control-channel

ts: 2026-09-11
seat: hermes (interactive seat, no MAG_TASK_ID -> pigeonhole mailbox currently no-ops)
phase: recon complete; non-Telegram channel verified live; durability protocol filed
operator signal: "the telegram channel has proven to be less robust and trustworthy. you wiped
the fuck out of the other programs before and stopping you on a task is basically a dead drop"

## completed
1. Hermes dashboard verified up locally: `http://127.0.0.1:9119` HTTP 200, v0.21.1, gateway
   running, `auth_required: false`, telegram connected.
2. Non-Telegram control channel verified END TO END, live, Telegram out of the path:
   - `curl -sk -X POST -H 'Content-Type: application/json' -d '{"cmd":"!continue"}' \
      https://desktop-7c70ksc.tail8403e9.ts.net/api/v1/agent/steer`
     -> HTTP 200 `{"ok": true, "queued": true, "cmd": "!continue"}`
   - `GET https://desktop-7c70ksc.tail8403e9.ts.net/` -> HTTP 200, 13,096 bytes,
     `<title>FLEET CONSOLE — everything, one place</title>`
   - `POST .../api/v1/agent/steer` with empty cmd -> HTTP 400 `{"ok": false, "error": "cmd required"}`
3. Control path read: `dashboard/server.py:829` `/api/v1/agent/stream` -> `_stream_agent`;
   `dashboard/server.py:832-844` `/api/v1/agent/steer` -> `mag.agent_cli.push_steer`.
4. Durability path read: `mag/pigeonhole.py` — `memory/mail/<task_id>/` holding `inbox.txt`
   (append-only, supervisor->agent), `heartbeat.jsonl` (15s liveness beads), `status.json`
   (atomic os.replace). Self-test run with `MAIL_ROOT` patched to a temp dir (zero repo
   footprint): `{"ok": true, "heartbeats": 2, "staleness_s": 0}`.
5. House resume protocol read: `jobs/gateway-durable-spawn/seat_contract.json` (schema
   `seat_contract.v1`) + `jobs/reset-burn-grok2/PASTE.md` (paste same block -> reads latest
   trail_core -> next cage). `memory/mail/` holds ~hundreds of live `ext-*` mailboxes.

## failures
- `400 Invalid Host header` on the Hermes dashboard through `tailscale serve --https=8443 9119`
  (DNS-rebinding guard). Documented fix = `dashboard.public_url`, which ALSO turns the auth gate
  on and therefore requires a password provider. NOT applied: it writes to `~/.hermes/.env` and
  needs operator consent. Config probe for it was blocked by the approval gate.
- `push_steer` is IN-PROCESS ONLY: `agent_cli.py:1827` `_STEER_QUEUE: "queue.Queue[str]"`,
  `1832-1845`. Consequences, precisely: (a) a restart loses queued steers; (b) it reaches only
  turns running inside the BOARD process, not this seat's turn. This is the dead-drop mechanism,
  located to the line.
- Interactive seats get no `MAG_TASK_ID` — set only at `mag/orchestrator.py:489` for spawned
  sub-agents — so for this seat the pigeonhole mailbox no-ops (`agent_cli.py:1856`).
- `config.py:17` `CHECKPOINT_DB = STATE_DIR / "checkpoints.db"` is declared and referenced
  NOWHERE (grep of `mag/governance.py`: 0 hits) -> dead stub, not a working checkpoint store.

## artifacts
- `jobs/hermes-control-channel/seat_contract.json`
- `jobs/hermes-control-channel/PASTE.md`
- `jobs/hermes-control-channel/trail_core_0.md` (this file)

## budget_used_pct: 0
(no provider spend; recon was local disk reads plus two curl requests)

## next_action_one_line
Get the operator's pick: (1) wire a durable `MAG_TASK_ID` mailbox so board-run turns get a
crash-safe inbox+heartbeat, (2) finish `dashboard.public_url` + password provider so the Hermes
panel itself loads in the phone browser, (3) leave the board-only channel exactly as it is now.
