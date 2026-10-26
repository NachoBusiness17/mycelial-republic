# SELF-STEAL (corrective): the 4 Rokus and the "Nous army", from Mag's own records + the devices themselves

Date: 2026-10-17, ~20:30 ET. Read-only pass. Corrects `STEAL_NOUS_FLEET_20261017.md` (not edited).
Method: rg over the repo + Desktop/Downloads/Documents\projects; `tailscale status`; `arp -a`; Roku ECP **GET only**
(`/query/device-info`, `/query/active-app`, `/query/apps`) on LAN hosts. No POSTs, no keypresses, no installs, no git,
no model calls, no code changes. Not opened: .env, key files, configs/keys.json, secret_gate_results/, free_keys/,
memory/trajectory/steps.jsonl.

---

## 1. Device facts (live ECP device-info, 2026-10-17 ~20:25 ET)

The ARP table on 192.168.86.0/24 has 8 neighbours. Four of them answer Roku ECP on :8060. The other four (.26 .28 .36 .37) time out on :8060.

| IP | model-name / model-number | user-device-name / location | software-version (build) | developer-enabled | net | ui-res | uptime | active-app at probe |
|---|---|---|---|---|---|---|---|---|
| 192.168.86.52 | Roku Ultra / 4660X | "Roku Ultra Waneta LR" / Living room | 15.3.4 (2402) | **false** | ethernet | 1080p | 43.0 d | Home (Roku Dynamic Menu), Aquatic Life screensaver |
| 192.168.86.53 | Roku Premiere+ / 4630X | "Roku Premiere+" / Map Room | 16.0.4 (834) | **false** | ethernet | 1080p | 3.9 d | Disney Plus |
| 192.168.86.85 | Roku Stick / 3500X (is-stick=true) | *(blank)* / *(blank)* | 11.0.0 (4195) | **false** | wifi | 720p | 38.0 d | Featured Free, Roku City screensaver |
| 192.168.86.149 | Roku Ultra / 4660X | "Roku Ultra Australia" / Family room | 16.0.4 (834) | **false** | wifi | 1080p | 3.8 d | Home, Aquatic Life screensaver |

- All four report `is-tv=false` (they are external boxes/sticks, not Roku TVs) and an empty `keyed-developer-id`.
- `/query/apps` returned 403 on .52/.53/.149 (ECP limited mode). The .85 Stick listed 32 store channels (Netflix, Hulu, YouTube, Disney Plus, Spectrum TV, ...). **None is a dev channel.**
- **Tailnet:** no Roku is on it. The nodes are desktop-7c70ksc, bob, mag-openclaw (offline 40 d), moto-g-5g (offline 14 d), pixel-11-pro (offline 19 h) and t90. The T90 is the Android **tablet**, not a TV box (`watch/inbox/gstd_perimeter_build_20261010/T90_IGNITION_KIT.md:3`).

**Bottom line: Mag runs nothing on any of the 4 Rokus today.** Developer mode is off on all four, so the channel was never sideloaded. They are ordinary household streaming boxes in active family use.

## 2. What Mag's own files say about the Rokus

| Claim | Evidence |
|---|---|
| The operator's count changed over time: "half dozen" on 10-07, then "3 rokus, one never used" on 10-12 | `memory/zknot/2026-10-06_sess_7318df04....md:37` ("i have a tablet an old phone with a smashed screen and a half dozen rokus"); `memory/zknot/2026-10-11_sess_133c7902....md:11` ("also we have 3 rokus one of which is never used. might want to use that as a fun device to test because if we can get this shit running on rokus we...") |
| Mag knew 3 by IP and model | `watch/inbox/gstd_perimeter_build_20261010/ROKU_IGNITION.md:11`: "Ultra .52, Premiere+ .53, Stick .85". **The 4th (.149, Ultra "Australia", Family room) appears in no Mag file.** |
| Mag's own verdict: terminal, not node | `ROKU_IGNITION.md:5`: "a Roku is a TERMINAL, not a node. BrightScript sandbox, no shell, no python - the harness will never run on it", plus the distribution-surface thesis ("every Roku on earth is one Channel Store approval away from showing the swarm") |
| The planned role is a DISPLAY FLEET | `docs/ref/GSTD_DOGFOOD_PLAN.md:85`: "~6x ROKU / DISPLAY FLEET (read-only spiders; locked OS, no compute join) / six always-on estate viewports: smith chart, pheromone gradient, gauntlet register, memory-wave city, dawn report, estate walk"; `:87-91`: display nodes "consume, they do not earn ... even a locked streaming stick joins as an eye". Echoed in `watch/inbox/moonshot_selfsteal_20260109/04_MESH_NETWORK.md:17,27,92` (Rokus = "the castle's read-only walls") |
| What was built | `roku_channel/` (10-12 09:24-09:27) and `republic_channel.zip` (2652 B, 10-12 09:29, same 7 files). Manifest `title=The Distributed Republic` / `subtitle=GSTD beacon - live lattice` (`manifest:1-2`). `BeaconTask.brs:5-15` GETs a URL with roUrlTransfer. `MainScene.brs:4` hardcodes `http://192.168.86.35:8777/beacon.json`, `MainScene.xml:32-35` refreshes every 60 s, and `MainScene.brs:23-34` paints lattice cells (rep, ton) plus artifact rows (type, name, price_gstd) |
| How it was to be deployed (never done) | `ROKU_IGNITION.md:9-16`: operator's remote code Home x3, Up x2, R, L, R, U, R, then "Enable installer", web password, then `curl --user rokudev:... /plugin_install`. No receipt of an install exists anywhere; ECP `developer-enabled=false` on all four confirms it never happened |
| Operator deferred it | zknot 10-11 session `:12`, 10-12 09:46: "not gonna shelf that till i get permission but lets treat it as a future project" |
| Other Roku-aimed organs already built (desk side) | `mag/display.py:1-3` (TV-safe `mag_display.v1`, "Poll GET /api/v1/display from a thin receiver channel (BrightScript ...)"); `mag/cast_server.py:2-13` ("Spotify-to-Roku style" cast receiver, :8766, `/api/v1/display` JSON, `/voice` phone voice UI, local faster-whisper STT); `dashboard/rest.py:3063,4709,5238`; `main.py:2098,2113`; `mag/stack.py:3` ("payload for UI/Roku/brain"); `tools/gstd_beacon.py:37` (bind 0.0.0.0 "the Roku reads the LAN side") |

### Defects found in the never-deployed channel (static read, Mag's files)
1. **`source/main.brs:1-3` is an empty `Main`** (comment only). A SceneGraph channel's Main has to create an `roSGScreen`, call `CreateScene("MainScene")`, `show()` it and run a message loop. As written, the channel would install and exit straight back to Home. The ROKU_IGNITION falsifier (`:23-25`, "installer rejects package") would never catch this.
2. **Schema drift:** the live beacon (`GET 127.0.0.1:8777/beacon.json`, 3188 B) has keys `beacon_version, updated_at, swarm, settlement, anon_model, law, artifacts` and **no `lattice_snapshot`**. `MainScene.brs:23` calls `.Lookup("cells")` on `invalid`, which is a BrightScript runtime crash.
3. `MainScene.brs:28` passes a float (`int(ton*100)/100.0`) to `itToStr(v as integer)` (`:40`), which is likely a type mismatch.
4. The IP is hardcoded. The Rokus can't join the tailnet, so the channel depends on the 0.0.0.0 beacon bind that the defense report flags.

## 3. What "Nous army" means in Mag's own files

**No Mag file outside my own 10-17 report contains "Nous army", "army of Nous", "Roku army" or any Nous-to-Roku link.** I searched the repo (excluding corpora), Desktop, Downloads and the sibling projects. The phrase's only occurrences are `watch/LIBRARY/STEAL_NOUS_FLEET_20261017.md` and its INDEX line, which paraphrase the operator's chat ask. I can't quote Mag's definition because Mag's files don't contain one.

What Mag's files *do* define, and what the phrase most plausibly composes from (labelled as **inference**):
- **"Nous" in Mag = the Nous Portal lane that Hermes runs over.** `mag/hermes_steering.py:2-4` says Hermes is "a gopher body of the fleet", dispatched by Mag with pack + goal, outcomes filed back. `:14-17` covers `--account sdd|nacho`, which routes over the Nous Portal lane (`provider nous-api`). `mag/kabuki_salon.py:2,12` describes "the rotating-cast bench, staged on Hermes over the Nous lane ... every actor is a hermes dispatch on the Nous lane". `harness/hermes_cli.py:1` is the Nous Research Hermes Agent headless one-shot. Nous rescue lanes are in `mag/fuel_feed.py:491-505` and `mag/free_tier.py:86`.
- **The swarm vision:** `watch/inbox/SCRUM_SWARM_20261016.md:5-8,27-39,57` covers "hundreds of scrum teams in tandem" directed from the T90 over Telegram, with a MAG director agent dispatching teams (browser leg + free-lane worker + task folder + fold).
- **The Rokus' place in it:** `GSTD_DOGFOOD_PLAN.md:85-91` makes them the read-only viewports/"walls" where that swarm becomes visible in the room.

So, inferred: the **army is the Hermes/Nous-lane cast plus mates (the workers on the desk, bob and cloud lanes), and the 4 Rokus are its walls**, i.e. viewports onto pheromones, gauntlet, leases, notices and the beacon. Mag's own files give the Rokus **no** compute, agent-host or Hermes front-end role. A voice/remote surface exists (`cast_server /voice`), but it is aimed at the **phone**, not the Roku.

## 4. Architecture fit (grounded) and the paper

| Mag organ | Role for the 4 Rokus | File |
|---|---|---|
| `mag/display.py` `build_display_payload` (`:62`, schema `mag_display.v1` `:145`) / `cast_server` `/api/v1/display` | **The JSON a fixed channel should poll** (built for "thin receiver channel (BrightScript)") instead of the drifting beacon schema | `mag/display.py:1-3`, `mag/cast_server.py:8,189` |
| `mag/warm_surface.py` `mag://warm/tip, notices, leases, laws` (`:8-20`) | Source of the wall content: tip, notices in force, lease board, fleet-kill banner | `mag/warm_surface.py:8-20,48` |
| `tools/pheromone.py hottest` ("The swarm reads THIS", `:16`) | One of the six planned viewports ("pheromone gradient") | `GSTD_DOGFOOD_PLAN.md:85` |
| Hermes steering / kabuki salon / `tools/leave_dispatcher.py` | **The army itself**: dispatch on desk/cloud; the walls show dispatch receipts (`memory/runs/hermes_dispatch_log.jsonl` per `hermes_steering.py:11-13`) | as cited |
| `mag/seat_handshake.py` (mode env `MAG_SEAT_HANDSHAKE`, default off, `:32,76`) | Rokus aren't seats; they hold no keys and do read-only GETs. Gate on the **server side** instead: bind the display endpoint narrowly, with no write routes | `seat_handshake.py:32,76` |
| `tools/mesh_delta.py` ("index ONCE, serve MANY", `:11-12`) | For bob/phones/T90 only. A Roku can't consume a torrent; at most it displays a delta summary | `tools/mesh_delta.py:1-12` |
| ECP :8060 | **Legit read-only fleet-inventory/liveness probe** (exactly what this pass did): model, OS, dev-mode, active-app per wall. Any `launch`/`keypress` is a POST and stays operator-gated | live ECP results above |

**The paper (Zhou & Freeman, 12 Oct 2026), mapped onto these devices:**
- *Find nodes*: ECP/SSDP is the analogue. Here it only yields inventory, which is useful as a wall-health organ.
- *Gain execution*: the paper's route was open debug ports on Android TV boxes. These Rokus have dev mode **off**, and turning it on needs the physical remote sequence plus a password (`ROKU_IGNITION.md:9-10`). Even then the only payload is one BrightScript channel (Mag's own words, `ROKU_IGNITION.md:5`).
- *Establish inference / continue from the new host*: **not applicable.** No shell or native runtime per Mag's own verdict. The 26B-across-15-boxes and 9B-on-8-of-9-hardware results concern Android/Linux-class boxes, not this fleet.
- The paper's legitimate yield for Mag is (a) the defense invariants already filed and (b) a **coordination picture made visible**. The walls show the army; they are not the army.

## 5. Smallest next step (needs operator hands for step 3 only)
1. On the desk side, fix `roku_channel` in a staging copy: real `Main` (roSGScreen, scene, port loop), guard against missing keys, float formatting. Repoint it to `mag_display.v1` (or a COP JSON composed from warm tip/notices + pheromone hottest), with the host URL as a manifest/registry value instead of a hardcoded one.
2. Unit-check the JSON shape against what the channel reads (the drift in §2.2 is the regression to test).
3. The operator picks **one** wall and enables dev mode with the remote. Mag's files call one Roku "never used" but don't say which. The .85 Stick has a blank name/location and the oldest OS (11.0.0), which is consistent with being unused, but that's an inference.
4. Sideload, then verify with ECP GET `/query/active-app` (dev channel id) as the receipt. Only after that does it become the six-viewport plan.

## 6. Where my earlier report (`STEAL_NOUS_FLEET_20261017.md`) was wrong
- It **hedged on the platform** ("Confirm the OS", case b Android TV) when Mag already had the answer by IP and model (`ROKU_IGNITION.md:11,21`). The devices are confirmed retail Roku OS: 2x Ultra 4660X, Premiere+ 4630X, Stick 3500X. **Case (b) was moot.**
- It said Mag "already treats them as a thin display client" and that "each Roku keeps a sideloaded channel". **False: nothing was ever sideloaded.** Dev mode is off on all 4, and the channel as written would exit (empty Main) and crash (schema drift) if it were installed.
- It argued from generic Roku spec pages (RAM ranges, forum threads) instead of Mag's own `ROKU_IGNITION.md`, the `GSTD_DOGFOOD_PLAN.md:79-91` display-fleet roster, `mag/display.py` and `mag/cast_server.py`. It missed the six named viewports and the fact that the 4th Roku (.149) is undocumented.
- It treated "Nous army" as if it had a defined meaning (COP of "many eyes"). Mag's files define no such term. "Nous" in Mag means the Hermes/Nous Portal lane (workers), which my earlier report barely connected.
- It recommended display seats with keypairs (`display:roku-N` allowlist rows). Rokus can't hold seat keys or join the tailnet. Gating belongs server-side.
- Its seat/warm/pheromone/handshake line references and the defense invariants still stand.
