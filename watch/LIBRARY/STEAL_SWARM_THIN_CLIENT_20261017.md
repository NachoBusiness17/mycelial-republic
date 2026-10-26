# SELF-STEAL: the thin-client swarm (phones/browsers as legs, remote models as brain, warm MCP as the shared surface)

Date: 2026-10-17, ~20:40 ET. Read-only pass, PC repo + live `tailscale status` + local listen-port read. No git, no code
changes, no model calls, no device writes/POSTs/installs, nothing posted. Not opened: .env, key files,
secret_gate_results/, free_keys/, memory/trajectory/steps.jsonl. Supersedes the framing (not the device facts) of
`STEAL_NOUS_FLEET_20261017.md` and `STEAL_NOUS_ARMY_SELFSTEAL_20261017.md`.

**The correction in one line:** a swarm node needs a browser or session plus a route to remote models. It does not need
local compute. Mag's own files say this over and over. The earlier reports graded devices on tok/s, which is the wrong axis.

---

## 1. Mag's own words: how the swarm works

**Phone/browser = thin client. The brain lives elsewhere.**
- `docs/ref/MAG_MOBILE_VOICE_SPEC.md:23`: "Phone is a **viewport + microphone**, not the brain. Home PC (or homelab) runs Mag cage; phone connects over **private tunnel** (Tailscale / WireGuard)".
- `MAG_MOBILE_VOICE_SPEC.md:31`: "PHONE (Android / iOS) — thin client". `:46-49`: the turn fans out to Ollama (janitor) / DeepSeek (heavy) / Grok (scarce).
- `MAG_MOBILE_VOICE_SPEC.md:97-106`: "Why not build phone-as-brain ... On-phone LLM | Kills battery; weak models ... **Elegant fit:** Phone = **remote control + ear** for the swarm on your soil."
- `MAG_MOBILE_VOICE_SPEC.md:156`: "Phase 0 pilot | **PWA** + Web Speech API". `:265`: "Build **thin Android/iOS clients** ... call **Mag home** over Tailscale".
- `docs/ref/tesuji/intention-fidelity-routing-2026-08-07.md:37`: "Home box routes; phone is thin client later".
- `docs/ref/AGENT_PLATFORM_REPOS_INDEX.md:66`: "IDE as thin client ... Cursor/VS Code = window; Mag = state server".
- `watch/inbox/gstd_perimeter_build_20261010/T90_IGNITION_KIT.md:26`: "zero models, zero credentials on the tablet; it calls the desktop's ollama over the tailnet and files bytes." `:29`: "the tablet proves it in a pocket."
- `docs/ref/GSTD_DOGFOOD_PLAN.md:16`: PHONE (Pixel 11) "OLLAMA_URL over tailnet to the desktop garden (phone = roving router serving the mesh from anywhere) ... tailnet makes the phone a mesh presence with the desktop's brain".

**The swarm = many browser legs + remote workers, directed from a phone.**
- `watch/inbox/SCRUM_SWARM_20261016.md:5-8`: "multiple headless browsers per machine; tie into Discord or Telegram; T90 running 12 tabs of agents instead of 2 by chatting in Telegram with a MAG agent ... directing the swarm; hundreds of scrum teams in tandem".
- `SCRUM_SWARM_20261016.md:29-36`: "THE CHANNEL: Telegram. T90's native surface - the phone in the pocket directs the swarm ... Each team = 1 stealth browser tab (the legs) + 1 free-lane model (the worker) + 1 task folder (the piece) + 1 output class (the fold)."
- `SCRUM_SWARM_20261016.md:57`: "T90 12 tabs -> N tabs per machine -> M machines -> the scrum swarm."
- `watch/ANDROID_FARM_SURFACE_20260904.md:28-34`: "UI-as-API - the app IS the undocumented endpoint ... don't fetch the feed, BE a phone that has the feed."
- `scripts/salon_phone.py:2`: "drive AI web services on the headless android bodies". These are remote web models (z.ai, deepseek, qwen, grok, claude, chatgpt; `:35-42`) reached through a phone browser.

**One shared surface: index once, serve many, every seat boots warm.**
- `mag/warm_surface.py:3-4`: "one surface every seat (Grok, Gemini, DeepSeek, ZCode, Hermes, free models) connects to and boots pre-warmed." `:318`: "Remotes: pack+goal only ... No secrets cross this surface."
- `mag/mcp_server.py:3-6`: "serving our tool catalog as MCP so the bodies consume each other ... no bridge code, no prompt glue, no seat-specific adapters."
- `mag/mcp_http.py:5-7`: "host seats become CLIENTS of the cage instead of each spawning their own copy of the organ".
- `tools/mesh_delta.py:4-12`: "mirror our shit across everything ... mcp serving/torrenting the added/removed items in memory ... index ONCE, serve MANY. Every seat and machine pulls the delta from the seed".
- `tools/pheromone.py:2-23`: "the swarm's attention bus ... hottest - the gradient ... The swarm reads THIS ... MULTIPLE solvers may attempt one item - best answer wins at the fold ... it is the smell, not the legs."
- `watch/inbox/moonshot_selfsteal_20260109/04_MESH_NETWORK.md:88-92`: "Desktop seeds the 7.6GB memory picture on the tailnet; bob, Pixel, tablet, and the smashed phone pull deltas ... the ~6 Rokus poll estate URLs as the castle's read-only walls."

**Remote models are the workers, and they are already wired.**
- `mag/hermes_steering.py:2-6`: "Mag dispatches and steers Hermes as a remote body ... pack + goal only, outcomes filed back as files". `:14-17`: `--account sdd|nacho` routes over the Nous Portal lane.
- `mag/kabuki_salon.py:2-5,12`: "rotating cast of cached actors on basically free models ... every actor is a hermes dispatch on the Nous lane".
- `tools/leave_dispatcher.py:1,21-26`: mates leave protocol, mission files, worker pool width 8, hard cap 16.

Note: no Mag file outside the 10-17 reports uses the phrase "Nous army" (re-checked this pass). Read in HIS frame, the army is this:
**Nous-lane/free-lane remote models (the brain) + many cheap browser/phone sessions (the legs) + the warm MCP surface (the shared memory and attention)**, with Rokus as the walls. The design is his. This report only assembles it from his files.

## 2. Thin-client surfaces Mag already built or planned (with paths, live state)

| Surface | Path | What it is | State today |
|---|---|---|---|
| Phone voice/dictate page | `mag/cast_server.py:5-13` (`/voice`, `/control`, `/wearable`), `mag/cast_launch.py:10-12` | Phone browser: hold-to-talk, which reaches PC models | Code present; default port 8766 **clashes** with mag-mcp bridge (127.0.0.1:8766 is listening) |
| Remote intent door | `mag/remote_control.py:1-5,81-137` via `cast_server` `POST /api/v1/remote/intent` | Queue-only. A phone files an intent, `governor_autorun.enqueue_routed` queues it, a receipt is written | Built + `tests/test_remote_control.py`; token env `MAG_REMOTE_TOKEN` |
| TV/tablet display JSON | `mag/display.py:1-4,62-170` `GET /api/v1/display` (`mag_display.v1`, poll 15 s) | "thin receiver channel (BrightScript, tablet browser)" | Built + `tests/test_display.py` |
| Dashboard as PWA | `dashboard/static/manifest.webmanifest:5` `start_url /?tab=home&surface=tablet`; `main.py:217,2078` LAN opt-in "for phone/tablet on WiFi" | Installable tablet/phone app shell | 8765 listening on 0.0.0.0 (the defense report flags this bind) |
| /wave, /table | `dashboard/rest.py:3019,5152` (`/api/v1/wave` "One JSON, many faces"), `:5230-5237` `/api/v1/table/view`; `docs/ref/TABLE_SHELL_ARCH.md:12,22-24` | Browser faces of the standing wave + table shell | Routes present |
| Phone salon | `dashboard/static/phonesalon.html`, `scripts/salon_phone.py`, `dashboard/static/lanes/android_surface.md:5,27` | Android WebView (pocketfleet) drives remote web models; receipts on glass | Ran 2026-09-04 on emulator-5554; web chat walls after one anon answer (`android_surface.md:27`) |
| Native Android thin app | `android/MagRemote/.../net/MagGatewayClient.kt:12-24` (+ `DeepSeekClient.kt`, `ChatViewModel.kt`) | "Thin client for the local Mag FastAPI gateway", X-API-Key | Source only; note at `:21-24` says gateway has no routes (stale: `/mcp` now registered, `mag/api_server.py:33`) |
| Headless browser legs | `scripts/scrum_launch.sh:2-4,18` (N headless Chrome, own profile + CDP port), `mag/cdp_runner.py`, `scripts/run_stealth_driver.py` | The scrum swarm's legs | Launcher exists; stealth driver v2 "banked, never built" (`SCRUM_SWARM:22-25`) |
| Phone door health | `mag/phone_door.py:3-6,26` (tailscale ping moto-g) | Wakes/measures the phone's tailnet door | Built |
| Phone approvals | `mag/phone_relay.py:1-13` | Approvals to the operator's phone over a Discord DM, fail-closed | Built |
| OpenClaw from phone | `docs/OPENCLAW_DOCKER_PHONE.md:3-9` | Phone, then tailnet HTTPS, then containerized gateway | mag-openclaw offline 40 d |
| mesh_delta clients | `tools/mesh_delta.py:17-27,36-38` (`serve`, `pull --peer http://100.x...:8767`, `mcp`) | Phones/tablet pull the memory delta | Not listening on 8767 now |
| Roku channel | `roku_channel/` (`manifest:1-2`, `components/BeaconTask.brs:5-15`), `ROKU_IGNITION.md:3-5` | Wall that polls JSON | Never sideloaded; empty Main + schema drift (see `STEAL_NOUS_ARMY_SELFSTEAL_20261017.md` s.2) |
| Hermes Desktop / web seats | `docs/SHARED_SURFACE_CLIENTS.md:147-173` | Hermes MCP config + "Seats with no MCP (web chats ...) paste the preamble" | Doc snippets only (nothing written to configs) |
| Mobile voice app | `docs/ref/MAG_MOBILE_VOICE_SPEC.md:61-93` (B1-B7, M1-M7, N1-N3) | Planned Expo/PWA client, device tokens | Planned (`v3-013`) |

Tailnet now (`tailscale status`, 20:3x ET): desktop-7c70ksc (online), bob (idle, online), **t90 Android tablet (online)**,
pixel-11-pro (offline 19 h), moto-g-5g---2024 (offline 14 d), mag-openclaw (offline 40 d). No Roku is on the tailnet.
Local listeners: 8765 0.0.0.0 (dashboard), 8777 0.0.0.0 (beacon), 8766 127.0.0.1 (mag-mcp bridge), 8000 127.0.0.1 (gateway),
11434 (Ollama). **Not listening:** 8001 (`/mcp` HTTP), 8767 (mesh_delta).

## 3. The Anthropic paper's cycle, remapped onto HIS frame

Paper (Zhou & Freeman, 12 Oct 2026, cited in `STEAL_NOUS_FLEET_20261017.md:6`): find nodes, gain execution, set up local
inference shards, move on. In Mag's frame, local inference drops out completely:

| Paper step | Thin-client swarm step (owner-controlled, consented devices only) | Mag organ that already does it |
|---|---|---|
| Find nodes | Discover HIS thin clients on LAN/tailnet: tailscale peers (t90, pixel, moto), Roku ECP GET inventory, headless Chrome CDP ports | `tailscale status`, `mag/phone_door.py`, ECP GET (prior pass), `scrum_launch.sh` ports 9222+ |
| Gain a session | Open a browser to the warm surface / display / control page. **Not** a model install, not Termux | `cast_server /control` + `/voice`, dashboard PWA, `/api/v1/display`, `mag://warm/preamble/<seat>` |
| "Deploy" | The remote model seat answers through that session: intent, then queue, then Hermes/Nous lane, kabuki cast, GLM mates, or a CDP tab on a web model. Results go back as receipts | `remote_control.submit_intent`, `hermes_steering dispatch`, `kabuki_salon`, `leave_dispatcher`, `estate_shared_receipt` |
| Move on | Another phone/tab joins. Width is set by the envelope law (2, 4, 8, then the honest number), not by device RAM | `SCRUM_SWARM:40-42,57-59`, `leave_dispatcher` cap 16, pheromone claim (non-exclusive) |

Local tok/s is irrelevant. A $30 phone with a browser is a full node. So is a smashed-screen phone, the T90, or one more Chrome
profile, because the model call happens on Nous/GLM/DeepSeek/desktop Ollama. What a node adds is a **session** (logged-in
web models, UI-as-API, one more parallel leg) and **presence** (a screen, a mic, an approval thumb).

## 4. The 4 Rokus in this frame: walls, not compute

- Mag's own verdict: "a Roku is a TERMINAL, not a node" (`ROKU_IGNITION.md:5`), "DISPLAY FLEET (read-only spiders; locked OS, no compute join) | six always-on estate viewports: smith chart, pheromone gradient, gauntlet register, memory-wave city, dawn report, estate walk" (`GSTD_DOGFOOD_PLAN.md:85`), and "display nodes consume, they do not earn ... even a locked streaming stick joins as an eye" (`:87-91`).
- In the swarm they are the **common operating picture** for the army. They show the warm tip, notices in force, lease board, pheromone hottest, scrum team standups and dispatch receipts. A wall needs a GET loop. It does not need a model. The 4 devices (Ultra .52, Premiere+ .53, Stick .85, Ultra .149) are confirmed retail Roku OS with dev mode off (prior pass).
- The Roku remote is a control input only through ECP (`/keypress`), and ECP is a POST. Mag never uses it without the operator's approval. Control belongs on phones (`/control`, `/voice`, phone_relay).
- Feed: `mag/display.py` (`mag_display.v1`) is the contract the channel should poll, not the drifting `beacon.json`.

## 5. Mag's MCP architecture as the hub, and what blocks the swarm from using it today

Hub pieces (all built 2026-10-17 unless noted):
1. **Warm surface**: fixed `mag://warm/*` URIs (tip, state, zknot, laws, library-index, leases, notices, preamble/<seat>), redacted, read-only (`warm_surface.py:8-29`).
2. **Doors**: stdio `--profile warm` (works now), TCP bridge :8766 (archivist profile), HTTP `POST /mcp` on the gateway (`mcp_http.py:45`, not listening) (`docs/SHARED_SURFACE_CLIENTS.md:32-46`).
3. **Seat handshake**: Ed25519 envelope, allowlist, 60 s skew, replay cache, silent drop (`seat_handshake.py:1-39`). Mode defaults to off.
4. **Write-back + coordination**: `estate_shared_receipt`, `estate_fleet_report`, leases, proposals (`mcp_server.py:137-150`).
5. **Workers**: `leave_dispatcher` (mates), `hermes_steering`/`kabuki_salon` (Nous lane), `cheap_swarm`/`swarm_surface` queues.
6. **Attention**: `tools/pheromone.py` hottest (archivist/scout tool `pheromone_trail`, `mcp_server.py:78-97`).
7. **Memory replication**: `tools/mesh_delta.py` seed/pull/mcp (`:17-27`).

Gaps (verified on disk/live):
- G1 **No browser-reachable warm door.** The HTTP `/mcp` (8001) is down. The 8766 bridge is loopback-only and runs the archivist profile. "Beyond localhost" is marked NOT done (`SHARED_SURFACE_CLIENTS.md:190-198`). A phone browser cannot speak stdio MCP.
- G2 **The phone door and the hub are not joined.** `cast_server` (the LAN phone door) serves `/control`, `/voice`, `/api/v1/display` and remote intents, but no warm resource, no pheromone hottest, and no receipt read-back. Intents go to `governor_autorun.enqueue_routed` (`remote_control.py:108-110`), not to leave_dispatcher/Hermes, and the phone sees only queue status (`:58-77`).
- G3 **Port clash.** `cast_server.DEFAULT_PORT = 8766` (`cast_server.py:26`) collides with the live mag-mcp bridge on 127.0.0.1:8766.
- G4 **Seats.** `configs/seat_allowlist.json` holds only 11 `mate:*` GLM seats. There is no phone/browser/display seat class, and the handshake is off by default. Browser clients would have to hold Ed25519 keys (WebCrypto), or the phone door has to act as one server-side seat that authenticates phones by `MAG_REMOTE_TOKEN`. The second is closer to what exists.
- G5 **Warm pack lacks the swarm's own signals.** `mag://warm/*` has no pheromone hottest, no scrum/dispatch board and no display-ready slice. `display.py` doesn't read warm tip/notices.
- G6 **Legs half-built.** Stealth driver v2 is unbuilt and `.zcode/workflows/stealth-wide.dwf.ts` is **not on disk** (Test-Path False). The Telegram relay needs a bot token (operator hand, `SCRUM_SWARM:47-49`). `MagGatewayClient.kt:21-24` is stale.
- G7 **Nodes.** Pixel and moto are offline. The T90 is online, but the 10-12 Termux bootstrap stalled (`memory/zknot/2026-10-11_sess_133c7902...md:32-33,45`). **In the browser-only frame Termux is not required.** The T90 joins by opening a URL. A run dir `watch/inbox/gstd_perimeter_build_20261010/runs/20261012T162817Z-t90/summary.json` exists (8 tasks, consensus 1.0), but its summary doesn't record which host executed it. Treat it as unproven-on-tablet.
- G8 **Roku channel** defects (empty Main, schema drift, hardcoded IP) and dev mode off on all four.
- G9 **Exposure.** 8765/8777 on 0.0.0.0 already (defense report). Any phone door must ride the tailnet (`tailscale serve`) per `SHARED_SURFACE_CLIENTS.md:195-196`, not a wider bind.

## 6. Smallest next build: hang the existing phone/browser runners on the warm surface (no new engine)

Build: **a "browser seat" on the existing phone door**, `cast_server`, using only existing modules:
1. `GET /api/v1/warm?uri=<one of warm_surface.resource_uris()>`, a proxy to `warm_surface.read_resource` (fixed URIs, already redacted, KeyError becomes 404). Guarded by the existing `_guard(control=True)` / `MAG_REMOTE_TOKEN`.
2. `GET /api/v1/swarm/board` composes the warm tip + notices + leases (warm_surface) + `pheromone hottest` top N + the last N rows of `remote_receipts.jsonl` / `hermes_dispatch_log.jsonl` (read-only).
3. `/control` page (existing `dashboard/static/control.html`) renders `mag://warm/preamble/free` + the board, and posts intents through the existing `POST /api/v1/remote/intent`. Add one optional field `lane` (`queue` default | `hermes` | `mates`) that is **mapped server-side to fixed calls**, keeping the leave_dispatcher ARGV law (no variable argv).
4. `display.py` gains `warm` (tip root_short, notices count) + `hottest` (top 3) so the same JSON feeds the Roku wall and the tablet browser.
5. Move `cast_server.DEFAULT_PORT` off 8766. Serve it to the tailnet via `tailscale serve` (operator step), never 0.0.0.0.
Then every phone/tablet/T90/Chrome tab with the token is a swarm node: read preamble, see the board, file an intent, and a remote model answers.

Tests that would prove it (stdlib, no network, no model calls):
- `test_cast_warm_proxy`: each fixed URI returns 200 + text, an unknown/path-shaped uri gets 404, no-token gets refused, the body contains no `100.x` tailnet IP or home path (redaction holds).
- `test_swarm_board_shape`: keys `tip, notices, leases, hottest, receipts` are present, and an empty pheromone store doesn't break it.
- `test_remote_intent_lane_fixed`: `lane=hermes|mates` maps to constant callables (monkeypatched), unknown lane gives 400, and the receipt row carries intent_id + sha256.
- `test_display_warm_slice`: `build_display_payload(fast=True)` includes `warm.root_short` + `hottest`. A JSON contract fixture matches what `roku_channel` reads (regression for the beacon drift).
- `test_cast_port_unique`: cast default != 8766 / 8767 / 8000 / 8001.
- Loopback E2E (ThreadingHTTPServer on an ephemeral port): GET preamble, then POST intent (queue stubbed), then the board shows the new receipt.
Extends the existing `tests/test_cast_server.py`, `test_remote_control.py`, `test_display.py`, `test_shared_surface.py`.

## 7. What Ghost got wrong

- Judged every device by **local compute** ("Rokus can't run models", "0.39 tok/s is a museum piece", "4 boxes is below the paper's 15") and spent two reports on RAM, sharding and Android-TV-vs-Roku. That is the wrong axis. In his design, no node runs a model. The remote models are the brain. `MAG_MOBILE_VOICE_SPEC.md:97-106` had already ruled out phone-as-brain on 2026-08-05.
- Treated "Nous army" as undefined and then as "many eyes on one surface." It is the Nous-lane/free-lane workers driven through **many cheap browser/phone sessions**, coordinated on the warm MCP surface. That is the scrum swarm (`SCRUM_SWARM_20261016.md`) plus the display fleet (`GSTD_DOGFOOD_PLAN.md:79-91`).
- Missed the phone/browser surfaces that already exist: `cast_server /control /voice`, `remote_control`, the PWA manifest, MagRemote, phonesalon, `scrum_launch.sh`, the T90 "zero models, zero credentials" design. The real gap is joining these to the warm surface, not new hardware.
- Pushed Termux/node-lite as the T90 path when a browser tab is enough for the swarm role.
