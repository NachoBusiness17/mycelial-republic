# FISH TANK SWEEP REGISTER (2026-10-19 night patrol)

Read-only sweep per the queue row [security] Fish Tank Sweep. Nothing killed,
nothing changed. Trigger: watch/inbox/FISH_TANK_LINK_READ_20261019.md. Full
listener census (TCP+UDP), docker ps, Mag* task states, portproxy rules.

## HEADLINE: the 8765 portproxy ghost is STILL ARMED

- `netsh interface portproxy show all` returns exactly one rule:
  listen 0.0.0.0:8765 -> connect 127.0.0.1:8765, hosted by svchost PID 5060
  (iphlpsvc - the portproxy host service, which is why netstat shows it
  anonymous). BOTH estate tasks that plausibly own 8765 are DISABLED
  (MagLabKit8765, MagPrivateOffice8765). Nothing listens on 127.0.0.1:8765:
  the wildcard forward points at a dead target. This is the residue that left
  sovereign dark 7h on 10-19 and it was never removed - the morning's "fixed"
  covered the portproxy GHOST'S effect, not the rule.
- THE FIX (operator hands, admin, the morning 4Ws block):
  netsh interface portproxy delete v4tov4 listenport=8765 listenaddress=0.0.0.0

## Named-but-unauthorized (confirm-first tier)

- sshd.exe LISTENING 0.0.0.0:22 - OpenSSH Server, not on the estate known-good
  list, exposed on LAN + Tailscale + WSL vNIC. If operator disclaims:
  sc config sshd start=disabled && net stop sshd (admin).
- SharedAccess (Internet Connection Sharing) serving UDP 53 on 0.0.0.0 - a NAT
  resolver that should not normally run on this workstation. If disclaimed:
  sc config SharedAccess start=disabled && net stop SharedAccess (admin; note
  ICS is sometimes deliberate for hotspot tricks).

## Wide-published estate surfaces (named, acceptable, noted)

- gstd-node container: 0.0.0.0:8080 (published wide).
- cluster-factorio_0-1: 0.0.0.0:27000 + udp 34197 (game server, wide).
- All other estate ports (mag-sovereign 8000/8001/9000, mag-mcp 8766,
  mag-browser CDP 9222, mag-redis 6379, ollama 11434, Hermes gateway 7860,
  Tailscale, ZCode app-server) are loopback-only or Tailscale-bound. GOOD.

## Clean bills

- The anonymous-headless-Chrome debug-port class is ABSENT (no chrome.exe
  listener anywhere; only stock chrome mDNS UDP 5353).
- Docker estate: 7 containers Up 10-23h, healthy, every published port named.
- 32 Mag* scheduled tasks: 28 Ready, 4 Disabled (BoxBurnNightly, LabKit8765,
  PrivateOffice8765, ProbeCadence), no anomalies.
- WSL relay mirrors docker ports via wslrelay.exe (127.0.0.1:8080) - content
  unnameable read-only, loopback-only, noted.
- Windows-system listeners (RPC, SMB, CDP, DoSvc, SSDP, kernel http.sys
  loopbacks) all named and stock.

## Falsifier

The sweep is done when no listener exists without a named owner in this
register. Today: 1 orphan (the portproxy), 2 confirm-first (sshd, ICS). Rerun
after the operator's admin block; exit condition is an empty kill-candidate
list.
