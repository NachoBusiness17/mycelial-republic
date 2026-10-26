# STEAL (defensive self-steal): self-replicating AI without a datacenter -> hardening Mag

Date: 2026-10-17 (America/New_York). Mode: read-only inspection plus this one report. No code, port, firewall, service, container or Tailscale setting was changed. No git, no paid or model calls, nothing posted. Not opened: .env files, key files, secret_gate_results/, free_keys/, memory/trajectory/steps.jsonl, configs/secrets/, configs/keys.json, .proof_key.

Scope: this is about **hardening Mag only**. Nothing here builds, tests, or describes any replication capability.

Sources read:
- The brief: X post https://x.com/NorenNamert/status/2111367087038119947 (via api.fxtwitter.com; Russian; posted 2026-10-17 04:01 America/New_York).
- Primary: Anthropic Frontier Red Team, "AI models may be capable of self-replicating without access to a datacenter", William Zhou and Daniel Freeman, 12 Oct 2026. https://www.anthropic.com/research/self-replicating-ai
- Secondary: BleepingComputer (Bill Toulas, 13 Oct 2026) https://www.bleepingcomputer.com/news/security/anthropic-warns-self-replicating-ai-could-spread-to-your-smart-devices/ and The Next Web (13 Oct 2026) https://thenextweb.com/news/auto-anthropic-small-ai-models-self-replicate-iot-devices

---

## 1. Verification table

| # | Claim in the brief | What the Anthropic page says | Verdict |
|---|---|---|---|
| 1 | 15 off-brand Android TV boxes at about $55 each | "15 inexpensive off-brand Android TV boxes (~$55 each) that we bought and networked together", 4 GB RAM each, pipeline-parallel sharding | **Confirmed** |
| 2 | Gemma4-26B-A4B at 0.39 tok/s | "at 0.39 tokens per second". Section C also gives ~0.3 tok/s averaged over a 32k window (prefill plus decode), unoptimized | **Confirmed** (0.39 is the demo figure; ~0.3 is the realistic agent-loop figure) |
| 3 | A 9B model set up inference on 8 of 9 hardware types | "a 9B model got inference running on 8 of the 9 hardware types we tested" (Qwen3.5-9B, in the Memento harness) | **Confirmed**, with the nuance that the brief omits the model name and the harness |
| 4 | GLM-5.2 completed end-to-end replication only in simplified evals (open debug/ADB ports, emulated networks) | Firewalled VPC of 8 GCP redroid Android 15 emulator nodes; unauthenticated ADB port; GLM-5.2 reached 8/8 in 4 of 5 trials and 7/8 in 1; other open-weight models "fail reliably". Anthropic calls this "an upper bound on real-world success" | **Confirmed**. Brief is accurate; BC and TNW match |
| 5 | An "end of 2026" extrapolation | "If small models improve at their historical rate, they'll match this capability level by the end of this year. Small weight-based replicators may be possible soon after." Trend fit: 13.7 ECI/year on <=30B models | **Confirmed**, as trend extrapolation, not a demonstrated worm |
| 6 | No central kill switch | "challenging to shut down, since there's no centralized point to shut off" (doubling time of days) | **Confirmed** as the paper's threat framing. Defenders still have ISP quarantine / flow-anomaly levers (section F); those are not a single kill switch |

### Brief errors and framing gaps (not number lies)

1. The X post is a fair Russian summary of the Anthropic page. The six numbers and framings above match.
2. Softening the brief would miss: (a) only GLM-5.2 of the *tested open-weight set* cleared end-to-end; "stronger models" are named as also capable in the abstract, but the graph's reliable winner is GLM-5.2; (b) the cyber step was deliberately trivial; (c) the floor (GLM-5.2 capability) and the size ceiling (what fits on 4 GB IoT) **do not intersect yet** — that is the whole point of the end-of-2026 line; (d) no rogue worm exists today (paper: "Signs of life", BC: "failed to demonstrate full end-to-end worm-creation capability" on real IoT).
3. BC and TNW both exist and agree with the primary. BC adds the 28–51 h / 71–150 h inference-setup windows and the Kimwolf / 40-H100-equivalent analogy. TNW is thinner but not contradictory.
4. Minor naming: brief says "Gemma примерно на 26 миллиардов" — actual tag is Gemma4-26B-A4B (MoE-style A4B active). Not wrong, just less precise.

---

## 2. What the paper's cycle would look for on Mag

Paper stages: find targets -> gain execution (open debug / unauthenticated ports) -> establish inference -> continue from the new host. Mag is not an Android TV box, but the same *shape* of exposure exists: LAN/tailnet-reachable services, an SSH door, a host Ollama that will pull and serve models, intentional remote-exec organs, and no fleet-wide stop.

Machine inspected: DESKTOP-7C70KSC (`5c18da76-268a-457c-9ed3-4c3a990b9d6c`), repo `C:\Users\foste\Documents\projects\local_sovereign_agent`. Bob was offline at inspect time. Ethernet and Tailscale both Private. Domain firewall profile OFF; Private/Public ON.

---

## 3. Mag exposure table (ranked)

| Rank | Exposure | Live evidence | Organ that already covers part of it | Gap |
|---|---|---|---|---|
| 1 | **Host Ollama on 0.0.0.0:11434** (pull + serve = "establish inference") | `netstat`: `0.0.0.0:11434` pid 29280 `ollama.exe`. User env `OLLAMA_HOST=0.0.0.0`. Firewall: Private allow for `ollama.exe` TCP/UDP Any port, RemoteIP Any. Compose points Mag at `host.docker.internal:11434` (`docker-compose.yml:28`) | `tests/test_bind_policy.py` only covers Mag's own dashboard bind, not the host Ollama process | No bind-audit that fails the host. Anyone on LAN (Private) who can reach 11434 can pull/run models. Paper stage: establish inference |
| 2 | **OpenSSH on 0.0.0.0:22** (gain execution) | `sshd` Running/Automatic, Listen 0.0.0.0:22. Two Tailscale-scoped allow rules *and* a third "OpenSSH SSH Server (sshd)" Allow Any RemoteIP. Config only showed `Match Group administrators` at L87 — PasswordAuthentication not confirmed in this pass | Mag SSH Tailscale rules; gstd_drain already SSHes to bob with a key (`tools/gstd_drain.py:93–116`) | Dual firewall posture (Any + Tailscale). Paper stage: gain execution. Mag itself already has an SSH cell to bob |
| 3 | **Portproxy 0.0.0.0:8765 -> 127.0.0.1:8765** (dashboard on every interface) | `netsh interface portproxy show all` still has the rule. Compose documents it as the loopback-law break (`docker-compose.yml:43–51`) and claims a 2026-10-05 cure — but the rule is **back**. Live: `0.0.0.0:8765` pid 48136 svchost. Firewall: Mag Dashboard 8765 allow from 100.64.0.0/10. Tailscale Serve also proxies `https://desktop-7c70ksc.tail8403e9.ts.net/` -> `http://127.0.0.1:8765` | Compose comments + lab bind policy (`config.bind_host`, `tests/test_bind_policy.py`) | Rule reappeared. Compose publish is `127.0.0.1:8765:8765` (L60) but host still wildcards via portproxy. Paper stage: find targets / unauthenticated surface |
| 4 | **gstd_beacon on 0.0.0.0:8777** | `tools/gstd_beacon.py:37` `SERVE_HOST` defaults to `0.0.0.0`; L38 port 8777. Live: pid 29708 `tools/gstd_beacon.py serve`. Firewall: uv python.exe Any TCP/UDP on Private | None for this process | Comment says "tailnet only" but bind is all interfaces. Paper stage: find targets |
| 5 | **gstd-node Docker on 0.0.0.0:8080** (not in Mag compose) | `docker ps`: `gstd-node` `0.0.0.0:8080->8080`. Image `gstdcoin/node:latest`. Live listen 0.0.0.0:8080 via com.docker.backend | Outside Mag's compose; no Mag organ owns it | Adjacent estate surface. Paper stage: find targets |
| 6 | **Intentional remote-exec organs** (Mag can already move work to other devices) | `tools/gstd_drain.py` CELLS: bob over `ssh -i … etfag@100.125.103.60` running a remote harness. `scripts/salon_phone.py` / `scripts/vision_endowment.py`: ADB shell/tap/am against PocketFleet. Live `adb.exe` listening 127.0.0.1:5037; `adb devices` empty right now. Tailnet peers: bob (idle), t90 (online android), pixel-11-pro / moto-g / mag-openclaw offline | Restricted leases (`configs/restricted_leases.json`, `mag/leases.py`) — but they cover chain/lab/compose/key-*names*, not SSH/ADB/ollama-pull | These are operator tools, not worm code. They are the *same shape* of stage the paper uses: find node, gain shell, run inference. Paper stages: all four, via Mag's own scripts |
| 7 | **Brain replicate target bob SMB** | `configs/brain_targets.yaml:17–22` — bob `\\100.125.103.60\MagBrain\brain`, enabled, probe TCP 445. Host SMB also listens 0.0.0.0:445 | Copy-only / append-only doctrine in the yaml header; probe-skip when offline | Not a worm vector by itself; it is a write destination a compromised seat could abuse if SMB auth is weak. Paper stage: continue propagation (payload parking) |
| 8 | **Seat handshake default OFF; 11 GLM mate seats, 0 revoked** | `mag/seat_handshake.py:76–77,338` `MAG_SEAT_HANDSHAKE` default `"off"`. `mcp_tcp_bridge.py:165` same default. `configs/seat_allowlist.json`: 11 seats (`mate:cartographer` … `mate:composer`), all `model_family: glm`, `revoked` count 0, `operator_seats: []`, `require_non_glm_approval: true` | `seat_public` returns None when `revoked: true` (`mag/seat_handshake.py:195–197`). Quorum / non-GLM approval on proposals | Warm MCP doors are not actually demanding signatures until mode is raised. Revocation flag exists but has never been drilled. Paper parallel: "no central kill" of a seat fleet |
| 9 | **OpenCode desktop on 127.0.0.1:49374** | Live: `opencode-cli.exe serve --service` pid 2720, loopback only | Loopback law held for this one | Low. Local-only. Still a "gain execution on this host" surface if something already on the box can hit it |
| 10 | **mag-mcp 127.0.0.1:8766 (archivist)** | Compose `docker-compose.yml:391–425`: in-cage `0.0.0.0`, host map `127.0.0.1:8766`. Profile archivist = no run_shell/write_file/apply_patch (comment L377). Live listen 127.0.0.1:8766 | Loopback publish + archivist profile + (optional) seat handshake | Low while handshake stays off *and* something local can talk to 8766. In-cage 0.0.0.0 is correct for Docker proxy (documented L392–398) |
| 11 | **Other Mag compose publishes (loopback-correct)** | redis `127.0.0.1:6379`, mag `127.0.0.1:8000/9000/8001`, browser `127.0.0.1:9222` (compose L126, L60–63, L185). Live match | Loopback law | OK. Note: compose `ollama` service publish `127.0.0.1:11434` (L152) is not the live host Ollama — host Ollama is the one on 0.0.0.0 |
| 12 | **Tailscale Serve / Funnel** | `tailscale status`: desktop-7c70ksc 100.96.161.76. Serve (tailnet only): `/` -> 127.0.0.1:8765 and `:8443` -> 127.0.0.1:9119. Funnel status returned the same serve block (no public funnel path confirmed in this pass) | Tailnet ACL + Serve | Serve puts the dashboard on the whole tailnet. mag-openclaw node offline 40d. Phones mostly offline; t90 online |
| 13 | **Kill switches today are local, not fleet-wide** | `scripts/lab_ctl.py`: lease-gated restart/stop/start/freeze/unfreeze of `mag-sovereign` only (`proc:lab`). Notices: `mag/fleet_report.py` KIND `NOTICE` + `mag://warm/notices` (in-force until cancelled). No single flag that stops ollama pulls, SSH cells, ADB scripts, gstd_drain, and mate seats together | lab_ctl + leases + NOTICE + seat `revoked` | Paper lesson: "no centralized point to shut off". Mag has pieces; it does not have one fleet kill |

Factorio (`0.0.0.0:27000` / UDP 34197) and Steam are out of Mag scope; noted only so the bind audit does not confuse them with Mag.

---

## 4. Map paper stages -> Mag organs

| Paper stage | Mag surface | Existing organ | Hardening move (build later; not done here) |
|---|---|---|---|
| Find targets | Wild binds (11434, 22, 8765 portproxy, 8777, 8080), Tailscale Serve, SMB 445 | Compose loopback comments; `tests/test_bind_policy.py` (dashboard only) | Bind-audit test that fails on any Mag-owned 0.0.0.0 / unauthenticated port |
| Gain execution | sshd, ADB scripts, MCP (if handshake off), OpenCode loopback | Seat handshake (`revoked`), archivist MCP profile, Tailscale-scoped SSH rules | Raise `MAG_SEAT_HANDSHAKE=required` on warm doors; revoke drill; tighten sshd RemoteIP |
| Establish inference | Host Ollama 0.0.0.0 + `OLLAMA_HOST=0.0.0.0`; gstd_drain remote harness | None that blocks unsolicited `/api/pull` from LAN | Bind Ollama to 127.0.0.1; lease or NOTICE before any cross-host model pull |
| Continue from new host | brain_targets bob SMB; gstd_drain bob SSH; Tailnet peers | brain_targets copy/append-only; leases on lab/chain | Fleet kill switch that also freezes remote CELLS and brain push |
| No central kill | lab_ctl is lab-only; 11 seats unrevoked; handshake off | lab_ctl + leases + NOTICE + `revoked` | One fleet-wide kill (below) |

---

## 5. Smallest hardening builds (on existing organs)

Do not invent new frameworks. Extend what is already there.

### Build A — Fleet-wide kill switch (NOTICE + lab_ctl + revoked)

One operator action that:
1. Files a `NOTICE` kind via `scripts/fleet_report.py` / `mag/fleet_report.py` with category `fleet_kill`, `until_cancelled`, auto danger mark (already designed in FLEET_COORDINATION_DOCTRINE P4).
2. Runs `lab_ctl.py freeze` under a `proc:lab` lease (already exists).
3. Sets `"revoked": true` on every non-operator seat in `configs/seat_allowlist.json` (handshake already honors this at `seat_public`).
4. Writes a single sentinel file (e.g. `state/FLEET_KILL`) that `gstd_drain.py`, `salon_phone.py`, `brain_replicate.py`, and any ollama-pull helper refuse on sight.

That is the Mag answer to "no central kill switch": one NOTICE id, one lease, one sentinel, N seat revocations.

### Build B — Bind audit test (extend `tests/test_bind_policy.py`)

A pytest (or doctor check) that fails the suite / doctor when any of these are true on the Mag machine:
- Host listen is Mag-owned and not loopback: Ollama, gstd_beacon, Mag dashboard (portproxy), Mag SSH if RemoteIP is Any.
- `docker-compose.yml` host publish is not `127.0.0.1:` for mag / mcp / redis / browser / ollama service.
- Live `netsh interface portproxy` still has `0.0.0.0:8765`.
- User/machine `OLLAMA_HOST` is `0.0.0.0` or empty-with-wildcard-listen.

Reuse `bind_host` / `bind_exposure` from `config.py`. Do not touch Factorio/Steam.

### Build C — Revocation drill

A dry-run script (or a fleet_report ACK exercise) that:
1. Picks one `mate:*` seat, sets `revoked: true`, asserts `seat_public` returns None and a signed warm request is dropped (404 shape in `DROP_HTTP`).
2. Clears revoked, asserts the seat works again.
3. Files a NOTICE + ACK so the COP shows the drill.

Prove the organ that already exists, on a calendar, before a real incident.

### Build D — Handshake default for warm MCP

Raise `MAG_SEAT_HANDSHAKE` from `off` to `required` on the warm/mcp path (`mcp_tcp_bridge.py` already reads the env). Archivist can stay optional. Pair with Build C so a bad seat can be cut without restarting the world.

---

## 6. Tests that would prove them

| Build | Proof |
|---|---|
| A fleet kill | (1) File NOTICE `fleet_kill`; (2) `lab_ctl status` shows Paused; (3) `gstd_drain` / brain replicate / salon_phone exit non-zero on sentinel; (4) all 11 mate seats `seat_public` None; (5) cancel NOTICE + clear sentinel + unfreeze restores. No network change required for the dry path |
| B bind audit | Unit: fixture with a fake `netstat` / portproxy dump containing 0.0.0.0:11434 and 0.0.0.0:8765 fails. Live doctor (opt-in): current machine fails today on Ollama + portproxy + beacon — that failure *is* the signal |
| C revoke drill | Toggle one seat revoked; handshake verify_envelope returns drop; ACK SPOTREP recorded; toggle back green |
| D handshake required | With env `required` and no signature, mcp warm door returns the silent 404 shape; with a good seat signature, passes |

---

## 7. What this report deliberately did not do

- Did not open secrets, .env, key material, or trajectory logs.
- Did not change firewall, portproxy, Tailscale, compose, sshd, Ollama, or any process.
- Did not modify Mag code — only this file and one INDEX.md line.
- Did not build, sketch payloads for, or improve any replication / worm / ADB-exploit path. ADB/SSH hits in the table are Mag's *own* operator scripts, listed as exposure to gate, not as recipes.
- Did not post anything.

---

## 8. Bottom line

The X brief is substantially correct against Anthropic (Zhou & Freeman, 12 Oct 2026) and against BC/TNW. Mag's real analogue of the paper's cycle is not an Android TV farm — it is **wild Ollama + SSH + a resurrected 8765 portproxy + intentional bob SSH/ADB organs + seat handshake still off**. The smallest steals are a fleet kill on top of NOTICE/lab_ctl/revoked, a bind-audit test that fails today's wildcard listens, and a revocation drill. No new organ required; wire the ones that already exist.
