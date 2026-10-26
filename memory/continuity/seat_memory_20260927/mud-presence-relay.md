---
name: mud-presence-relay
description: The second lantern — dashboard/mud_relay.py, stdlib presence server on :8766; two+ browsers see each other's lanterns in MUD (verified); OPTIONS/CORS preflight required; must be RUNNING for multi-lantern play
metadata:
  node_type: memory
  type: project
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

Shipped 2026-09-14 — the salon's decisive experiment ("two clients, one room, one torch") at the presence layer. **Verified live:** P1's lantern sees the second browser at its coordinates.

- **Run:** `./.venv/Scripts/python.exe dashboard/mud_relay.py` (defaults :8766 @ 127.0.0.1; args [port] [bind]). Currently running as background task exec_6a45434a — it dies with the session; relaunch to restore multi-lantern play.
- **API:** POST `/mud/seen` {id,name,x,y,hp,max_hp,state} · GET `/mud/others?id=X` (excludes self) · GET `/mud/ping`. 6s expiry, reap at 4×. CORS `*` on everything.
- **Critical lesson:** cross-origin POST (page :8765 → relay :8766) fires an OPTIONS preflight — without a `do_OPTIONS` handler returning ACAO headers, fetch throws "Failed to fetch" silently. First relay died to this.
- **Client layer (mud.html):** `RELAY/ME/LANTERN_NAME` consts (`?name=` query param names your lantern), `mudOthers` array, `relayTick()` on 250ms setInterval (never reassign the array — mutate it, see the bonfire rule). Draw: bodies + name tags inside torch radius, pulsing embers beyond it, culled to screen.
- **v1 is presence-only** — each client's world is its own; the relay is the shared room, not an authority. Next stone per the architecture witness: server-side sim (authoritative relay), then Durable Object rooms for off-LAN.
- **Bind guard:** relay refuses non-loopback binds unless explicitly 0.0.0.0 (LAN-only intent, same perimeter as dashboard, no auth).

- **Update 2026-09-28 (FW-37 ws spike):** the relay grew a push socket — `GET /mud/ws` (RFC6455, stdlib hand-rolled: `_recvn/_ws_read_frame/_ws_send_frame`, one broadcaster thread at 8Hz). Client (mud.html) is WS-first: presence goes out as ws text frames, `others` arrive broadcast (`{"ok":true,"type":"others",...}`); 3 connect/close strikes → v1 HTTP poll until reload; headless harnesses (no `WebSocket` global) stay on HTTP via the typeof guard. Socket close drops the lantern immediately (no 6s ghost). Verified by `watch/inbox/burn_reset_20260927/queue/Q_037_ws_probe.py` 5/5 (handshake/accept, broadcast with self excluded, instant drop on close, HTTP path intact, plain GET → 400) + mud replay 41/41 + mud fifty 63/63 after the client edit. Receipt: `watch/inbox/burn_reset_20260927/queue/Q-027.md` §FW-37.
