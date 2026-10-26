# STEAL — Fish Tank IoT (self-steal) — 2026-10-19

prompt_genome_id: fleet/self_steal@v1 · SUBJECT: Mag's LAN/IoT-facing surfaces · LENS: "the fish tank is the door"

## Verdict
Supported that the story is real (Darktrace 2017). Mag's version of the fish tank is not one device but a **set of wildcard-bound services** (Ollama 11434, sshd 22, portproxy 8765, gstd_beacon 8777, gstd-node 8080) on the same Private LAN as untrusted consumer gear (Roku, phones). Mag already forbids LAN *control* of cast/display. It does not yet treat LAN devices as untrusted peers with a notice/lease/kill path. Smallest hang: an **untrusted-LAN-device NOTICE + lease rule** routed through existing organs (cast_guard probe log, leases, platform_kill). No new brain.

## Evidence tiers
| Tier | Claim | Status |
|---|---|---|
| Post (@Hamzaonchain, 2026-10-19, x.com/Hamzaonchain/status/2112117330100596956) | Casino lost 10GB through a fish tank; homes have the same weakness. Video not watched | Unproven at post tier (it's a repost/hook) |
| Paper/press | Darktrace Global Threat Report 2017, case 6: a North American casino's connected tank (temp/salinity/feeding sensors) sat on its own VPN; 10GB left for a "rare destination" in Finland over an audio/video-type protocol. SecurityWeek 2017-07-26 (Justin Fier): attacker already in the corp net, then brute-forced or used stolen creds to get onto the tank VPN. Contents of the data unknown. CNN 2017-07-19: lateral movement afterward | Supported (vendor report; few technical details, which SecurityWeek points out) |
| Mag bytes | Rows below, cited from files on disk + STEAL_SELF_REPLICATION_DEFENSE_20261017.md live receipts (netstat/firewall dated 2026-10-17) | Supported at file level; live state **Unproven today** (no new port probing this run) |

Note: the casino tank was *isolated by VPN* and still leaked. Lesson: segmentation without egress watching isn't enough. The anomaly was the **egress pattern** (volume + new destination + protocol mismatch), not the breach itself.

## Inventory (paths verified at bytes)
- watch/LIBRARY/STEAL_SELF_REPLICATION_DEFENSE_20261017.md (16653 B): bind table rows 1-12
- mag/cast_server.py (14144 B): default 127.0.0.1:8766, `--lan` opt-in (L13, L26)
- mag/cast_guard.py (5449 B): LAN-only + token control, probe log memory/security/cast_probes.jsonl, IP temp-block, read-only routes fail-open for Roku
- mag/display.py (6035 B): read-only TV payload for Roku/wall clients
- tools/gstd_beacon.py: L37 `SERVE_HOST` default `0.0.0.0` ("the Roku reads the LAN side")
- mag/seat_handshake.py: `MAG_SEAT_HANDSHAKE` default off (L32); scripts/container/mcp_tcp_bridge.py L120 same
- mag/leases.py (22887 B), mag/platform_kill.py (6608 B), scripts/lease.py (3816 B)
- docs/BRAIN_HOSTING.md L201 (handshake modes), L227 (tailscale serve --tcp 8766 advice)

## Provenance
Cast/wearable server and cast_guard came from the operator's 2026-08-11 "keep it LAN only and detect people trying to gate into it" (cast_guard docstring). gstd_beacon v0 was added 2026-10-12 with a deliberate LAN bind so the Roku can read it. The bind audit came from the 2026-10-17 self-replication steal.

## Mag analogs (the fish tanks)
| Surface | Bind (per 10-17 receipt) | Fish-tank role |
|---|---|---|
| Ollama | 0.0.0.0:11434, OLLAMA_HOST=0.0.0.0, firewall Private Any | Unauthenticated compute + /api/pull from any LAN device. The worst analog |
| sshd | 0.0.0.0:22, a third rule allows Any RemoteIP | Credential brute-force target (the casino tank VPN was brute-forced or got stolen creds) |
| portproxy 8765 | 0.0.0.0:8765 -> dashboard; rule came back after the 10-05 "cure" | Dashboard on every interface |
| gstd_beacon | 0.0.0.0:8777 by design | Read surface for the Roku. Its comment says tailnet-only but the bind is all interfaces |
| gstd-node | 0.0.0.0:8080, outside Mag compose | Unowned third-party container. Classic forgotten device |
| warm MCP 8001 / mag-mcp 8766 | 127.0.0.1 (compose) | OK. Handshake off is the latent risk if anything local is compromised |
| cast_server | 127.0.0.1:8766 default, `--lan` opt-in | Guarded (see below). **Note:** 8766 is listed for both mag-mcp (compose) and cast_server (DEFAULT_PORT). Port collision or ambiguity: Unproven which one owns it when `--lan` runs |
| Roku fleet | consumer firmware, read-only consumer of display/beacon | Literally the fish tank: an untrusted IoT box on the same LAN that Mag can't patch |
| Thin-client phones (salon_phone etc.) | LAN/tailnet | Roaming endpoints that join other networks |
| Tailscale Serve | tailnet only, no Funnel | Good fence. Every tailnet node is still trusted |
| Public Drive mirror | one-way out | Egress channel by design. The casino lesson is to watch egress |

## What Mag already forbids
- LAN *control* of cast/display without a private-range client + X-Mag-Token, fail-closed, with probes logged and IPs blocked (cast_guard)
- Display surfaces are read-only by construction (display.py, cast_server "Read-only cast receiver")
- Loopback law for compose publishes (redis/mag/browser on 127.0.0.1); tests/test_bind_policy.py covers the dashboard only
- Public mirror is one-way. Tailscale Funnel is off
- platform_kill gives a one-pass teardown. Seat revocation exists (seat_public returns None when revoked)

## Gaps
1. **Bind addresses:** five wildcard listeners (11434, 22, 8765, 8777, 8080). No bind audit fails the host. Same as the 10-17 gap, still open (Unproven whether anything was fixed since)
2. **Roku/phone exposure:** devices are trusted by default because they share a subnet. No inventory of LAN peers. gstd_beacon serves all interfaces with no cast_guard-style probe log
3. **Cast exposure:** `--lan` mode is guarded. The 8766 double-assignment needs a ruling
4. **Egress blindness:** the casino was caught by egress anomaly. Mag has no notice for unusual outbound volume or new destinations (Drive mirror, gstd_drain ssh)
5. Handshake off on warm MCP: a compromised LAN device that reaches loopback via portproxy-like rules meets no signatures

## Five bones
- Claims: an IoT device can be the door and the exit
- Proofs: Darktrace case 6 + Mag 10-17 netstat receipt
- Assumptions: the home LAN (Private profile) is friendly. **This is the assumption that breaks**
- Forbids: "a read-only display device is harmless." Read-only for Mag doesn't make the device trustworthy on the LAN
- Costs: rebinding to 127.0.0.1/tailnet breaks Roku reads of the beacon unless a narrow route is kept

## Fold — smallest hang (no new brain)
- **Law (shelf):** "Untrusted LAN peer" = any non-tailnet, non-seat device (Roku, phone on Wi-Fi, IoT). It may READ display/beacon routes only, never reach 11434/22/8765/8080
- **Notices:** extend cast_guard's probe log pattern (memory/security/cast_probes.jsonl) to gstd_beacon reads. A NOTICE row when a new LAN IP appears or an untrusted peer touches a non-display port
- **Leases:** a LAN `--lan`/beacon exposure should be a lease (mag/leases.py, scripts/lease.py) with a TTL, not a permanent default bind
- **Kill:** when a lease expires or a notice repeats, use platform_kill / process stop for the exposing service (beacon, cast `--lan`), plus seat revocation for phones
- **Operator gates (proposed, not done):** bind Ollama to 127.0.0.1; drop the portproxy rule; scope sshd to tailnet only; give gstd-node 127.0.0.1 or remove it; extend test_bind_policy to host listeners
- Poetry: "the fish tank is the door"

## Surprise
- gstd_beacon is the closest Mag analog to the fish tank, and it's *intentionally* LAN-wide to serve a consumer IoT device. Its comment says tailnet but the bind is all interfaces
- Port 8766 is claimed by both mag-mcp (compose) and cast_server

## Falsifiability / counters
Proved wrong if a fresh `netstat` shows all five as 127.0.0.1/100.x, or if the LAN has no untrusted peers. FORBIDS: trusting Roku/phones by subnet. PAID RENT ON: cast_guard's existing probe log + leases + platform_kill.

## Receipt
watch/LIBRARY/STEAL_FISH_TANK_IOT_20261019.md: self-steal, report-only, no code/git/secrets/paid calls, no live port probing (relies on the 10-17 receipts).
