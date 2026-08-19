# STEAL — Hermes Desktop (2026-08-14)

Operator: steal hermes desktop. Bytes from this machine + Nous apps/desktop README+DESIGN (Herald v0.20, 2026-08-03) + Mag desk census.

## What it is (not rumor)

Hermes Desktop is a **surface**, not a second agent. Same skills, same memory, same sessions as CLI and gateway. Electron shell + React chat + headless hermes serve (	ui_gateway JSON-RPC/WebSocket). pps/shared is the transport used by **desktop and the browser dashboard**. Three boundaries. Model is interchangeable. The relation is the agent core.

On this machine: %LOCALAPPDATA%\hermes exists. hermes-agent checkout includes pps/desktop + pps/shared. Skills dirs present. logs/desktop.log does **not**. The workbench was installed as CLI/home, not lived in as the GUI. Mag orientation (2026-07-25): Hermes is optional L2; Mag owns the brief; private residual never routes to Hermes. harness/hermes_cli.py remains. No mag/*hermes*.

Herald (v0.20): desktop became a **workbench** — versioned artifacts with sandboxed right-rail preview, plugin SDK (Kanban founding), global quick-entry, multi-window. Chat is the home surface. Durable pages: Chat, Skills, Messaging, Artifacts. Overlays: settings, cron, profiles. Panes: preview, files, terminal — working context, not navigation. A2A v1.0 is in the **agent**, not the chrome.

DESIGN steal (invariants, not CSS):
- Flat, not boxed. Tokens, not literals. One primitive per concern.
- Intent before automation: a tool result must not auto-open a pane or steal focus.
- Direct manipulation paints first; disk reconciles after; rollback visible.
- One action, one home. Projects own cwd. Soft workspace switch, not cold boot.
- Navigation must not replace the foreground transcript when a background session finishes.

## Mag desk (the castle we already have)

Twelve HTML faces in dashboard/static, none of them the core:

| page | title now |
|---|---|
| index.html (100k) + app.js (339k) | MAG · マグ · 勾玉 |
| table.html | Mag Table — the lantern |
| lattice.html | Conspiracy lattice |
| seat.html | SEAT · ghost surface |
| agents.html | sub-agent fleet |
| feed.html | Mycelial Republic · Feed |
| control.html | Direct Mag |
| cast-voice.html | Mag Voice |
| wearable.html | Swarm HUD |
| sovereign_shell.html | Sovereign Shell |
| index.clear-ui.html | Local office |
| cast.html | Mag Cast |

These are Hermes-without-the-rule: many surfaces, **not** one 	ui_gateway. Table was a second world until hung on game_world today. Index is the sky. 
est.py is the unused shared.

## Soil (repurpose)

1. **One JSON gateway.** Mag GET /api/v1/wave = Hermes 	ui_gateway. Verkle tip, party_subchain head, game_world root, lantern view, doctrine one-liner, seats as records. Every HTML face reads that. No face invents a world.
2. **Chat is home; lantern is a pane.** Table.html becomes the right-rail / working context (world_rib field + talk), not a product. Index chat stays the transcript.
3. **Durable nouns:** Wave, Table, Seats, Doctrine. Feed/lattice/agents become panes or overlays. Wearable/cast-voice = voice overlay. Control/sovereign_shell = settings overlay. Do not hide party_subchain inside chat sludge.
4. **Artifacts rail:** steal files + subchain leaves + world_rib ASCII render as sandboxed cards. Intent before automation — do not auto-open on curveball.
5. **apps/shared pattern:** one dashboard/static client module for wave JSON, reused by index and table. Stop forking fetch in each html.
6. **Soft switch:** stop power stop/start as the only way a face sees new organs. Read live modules; faces subscribe.

## Glory (do not steal)

- Electron. Mag desk is already :8765.
- Hermes as Mag's router or SOUL.md residual (never).
- Auto-created skills, Honcho user model, 40 providers.
- A2A **wire**. Already stolen as local contract (participant metadata, transcript, durable artifact).
- Their BrandMark, i18n four-locale tax, assistant-ui fork.
- Calling wow_manifest() per turn.

## Cut

Hermes Desktop is the standing wave as a **workbench over one serve**. Mag already has the serve (world core + subchain + RIB). Mag's front is twelve castles. The newer Mag front is not a Hermes skin. It is one wave JSON, chat as home, lantern as pane, orphans as overlays.

The relation persists. The model is interchangeable. The chain is the ground truth.
