# FISH_TANK_REMEDIATE_20261019

Source: STEAL_FISH_TANK_IOT_20261019.md (operator "ok" 2026-10-19). Executor run 2026-10-19 ~17:10 EDT. No git, no secrets, no mag-sovereign restart, no paid calls. Shell was NOT elevated, so the admin-only steps are staged in a script.

## BEFORE (netstat, 2026-10-19 17:07 EDT)
- 0.0.0.0:22 / [::]:22 sshd (pid 4608)
- 0.0.0.0:8080 / [::]:8080 gstd-node via Docker backend (pid 2876)
- 0.0.0.0:8765 portproxy (svchost/iphlpsvc pid 5060). `netsh interface portproxy show all`: 0.0.0.0 8765 -> 127.0.0.1 8765
- 0.0.0.0:11434 / [::]:11434 Ollama (pid 29536), user env OLLAMA_HOST=0.0.0.0
- 127.0.0.1:8766 mag-mcp (compose). 8777 beacon not running.
- Firewall rules: could not be listed (Get-NetFirewallRule access denied, not elevated)

## Applied (live)
- A1 Ollama: User env OLLAMA_HOST 0.0.0.0 -> 127.0.0.1:11434, Ollama app restarted. Now 127.0.0.1:11434 (pid 20128). Container check: mag-sovereign -> host.docker.internal:11434/api/version = {"version":"0.34.3"} (still reachable)

## Staged (needs elevated run): scripts/host_lockdown_fish_tank_20261019.ps1
- A2 netsh portproxy delete 8765 (tried unelevated: "requires elevation"). No repo script or scheduled task re-adds it (searched scripts/ mag/ tools/ configs/ watch/LIBRARY/ + scheduled tasks)
- A3 sshd: disables other inbound allow rules on 22, adds MAG-sshd-tailnet (100.64.0.0/10, fd7a:115c:a1e0::/48, 127.0.0.1). sshd stays running
- A1 belt+braces: disables inbound allow rules on 11434
- A4 gstd-node: its compose project (reference/gstdcoin/gstdbot/docker-compose*.yml) no longer exists on disk, so a rebind means recreating the container by hand. Staged MAG-block-lan-8080 (blocks private ranges inbound to 8080 instead)

## Code (uncommitted)
- configs/restricted_leases.json: new lease resource `expose:lan` (default 3600s, max 14400s)
- mag/cast_guard.py: untrusted-LAN-peer law. Adds peer_class, display_gate (display routes only, deny by default), a NOTICE row `notice:new_lan_peer:*` / `notice:non_display_route:*` in memory/security/cast_probes.jsonl, peers in memory/security/lan_peers.json, lan_lease_live, lan_lease_watchdog
- tools/gstd_beacon.py: defaults to 127.0.0.1. LAN needs GSTD_BEACON_LAN=1 plus a live expose:lan lease, otherwise it refuses. Requests go through display_gate. The server shuts itself down when the lease ends
- mag/cast_server.py: a wildcard bind refuses without the lease and the watchdog shuts it down at expiry. Adds LAN_PORT=8767
- main.py cast: `--lan` with the default 8766 moves to 8767. C ruling: host 127.0.0.1:8766 belongs to compose mag-mcp. Compose is untouched. `lab --with-cast --cast-lan` cast_port is NOT moved yet (remaining wire)
- mag/platform_kill.py: kill_lan_expired() (beacon serve / cast --lan when the lease is not live). CLI `--lan-expired`. kill_all now also reaps LAN exposure
- tests/test_fish_tank_binds.py (new): pins compose publishes to loopback, 8766 ownership, beacon loopback default, Ollama not on 0.0.0.0, the expose:lan lease, peer classes, display-only and notice behavior, the no-lease kill path
- patch applied by watch/inbox/fish_tank_patch_20261019.py

## Tests (MAG_ALLOW_LIVE_WRITES unset)
pytest tests/test_fish_tank_binds.py tests/test_bind_policy.py tests/test_cast_server.py: 18 passed

## AFTER (netstat, 17:12 EDT)
11434 -> 127.0.0.1 only. 22, 8080, 8765 unchanged until the elevated script runs.

## Remaining
1. Operator runs the elevated script, then re-runs `netstat -ano` and `netsh interface portproxy show all`
2. Optional: recreate gstd-node with -p 127.0.0.1:8080:8080 (compose files missing)
3. Nothing runs `platform_kill --lan-expired` on a schedule yet (the watchdog covers live servers). Move cast_port on lab --cast-lan
4. Egress watching (steal gap 4) is not addressed
