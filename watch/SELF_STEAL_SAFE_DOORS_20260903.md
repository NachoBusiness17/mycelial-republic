# SELF STEAL — SAFE DOORS (2026-09-03, morning)

Trigger: operator's internet went sideways; he killed the Cloudflare thing; then:
"self steal and help me figure out the best way to do all of this as safely as possible."

## VERDICT (one line)
WARP was dead weight with a built-in failure mode — kill it forever. The safe
architecture ALREADY EXISTS on this box: the loopback law held on every fleet
surface, and the phone door is one Tailscale app install away.

## WHY WARP WAS USELESS TO OUR ENDS
WARP is a consumer VPN for the HOST's outbound traffic — everything routes through
Cloudflare's edge. Against our three actual needs:
1. **Phone → fleet**: needs the desktop reachable from his phone = Tailscale's exact
   job. WARP cannot do it at all (it tunnels outbound, it doesn't expose surfaces).
2. **Privacy of API traffic**: already TLS end-to-end; keys stay local. WARP just adds
   a middleman that sees all traffic and can flap — and when it flaps, it takes DNS
   and routing down with it. That was this morning's tuition.
3. **Public surfaces** (the public turn, recruiting external agents): that's a
   DIFFERENT Cloudflare product — cloudflared tunnel + Access — scoped, not host-wide.
Cost of keeping it: two network layers fighting, whole-line flaps. Zero benefit.

## THE DOORS INVENTORY (measured 09:05–09:15Z 2026-09-03)
- **Fleet surfaces — ALL loopback (SUPPORTED)**: 11434/12434 (ollama), 18789 (hermes
  gateway, node under AppData\Local\hermes), 6379 (redis), 8000/8001/8765/9000
  (mag-sovereign: room/board/API), 9222 (Chrome CDP), 55344 (control-plane).
  netstat + docker ps publish lists agree. The loopback law held.
- **0.0.0.0 listeners = Windows core only (SUPPORTED, per-PID)**: svchost/lsass/
  wininit/services/spoolsv on 135/445/5357/5040/7680/49664-8/62892. LAN-only behind
  home NAT. Normal house noise, not fleet debt.
- **Tailnet (SUPPORTED)**: node `mag-openclaw` 100.122.55.63 lives in
  mag-openclaw-tailscale. `RouteAll: false`, `AdvertiseRoutes: null` — it is ONE node,
  not a subnet router. Least-exposure posture already correct.
- **Phone door ALREADY WIRED (SUPPORTED)**: `tailscale serve` inside the container
  publishes `https://mag-openclaw.tail8403e9.ts.net` (tailnet only) → proxy to
  172.19.0.3:18789 = the openclaw gateway (shares netns with the tailscale container —
  inferred from docker inspect: mag-openclaw shows no separate IP).
- **WARP remnants (SUPPORTED)**: warp-svc.exe running (disconnected/idle — routes
  nothing), app installed at `C:\Program Files\Cloudflare\Cloudflare WARP`,
  warp-cli on PATH.
- **Secrets**: repo `.env` exists (existence noted only, never echoed).

## THE ARCHITECTURE (recommendation)
**One private door, one scoped public door, loopback default everywhere else.**

1. **PRIVATE DOOR = the tailnet.** Operator phone: install the Tailscale app, sign in
   with the same account, open `https://mag-openclaw.tail8403e9.ts.net`. Zero router
   port-forwards, WireGuard-encrypted, device-level tailnet auth. When the room
   (127.0.0.1:8765/room) should ride the phone too, add one serve route in the
   tailscale container (cmd in GOS). Still tailnet-only.
2. **PUBLIC DOOR (operator GO only, for the public turn)**: cloudflared tunnel →
   Cloudflare Access in front → read-only mirror of the board, rate-limited. Never
   `docker -p 0.0.0.0`, never router forwards. THIS is the only shape in which
   Cloudflare earns a place in the fleet.
3. **LOOPBACK LAW stays default**: every fleet surface binds 127.0.0.1; exposure is a
   named exception with a reason on file.
4. **WARP dies**: uninstall app + service (cmds below). The flap class dies with it.

## HOOKS (prose fails, hooks hold — candidates, GO-gated)
- `loopback_gate`: periodic netstat assert that no fleet-known port binds non-loopback
  (full-chord law: assert every port, or print "partial").
- After WARP uninstall, the two-VPN-flap failure class is extinct, no hook needed.

## GOS AWAITING OPERATOR (one-word triggers)
- **GO "KILL"** — uninstall WARP: `warp-cli --help` for the uninstall verb, or
  Settings → Apps → Cloudflare WARP; verify `warp-svc.exe` gone from tasklist.
- **GO "PHONE"** — add the room to the phone door:
  `docker exec mag-openclaw-tailscale tailscale serve --bg --set-path=/room http://host.docker.internal:8765`
  (must verify host.docker.internal resolves from that container's netns; fallback =
  host bridge IP 172.19.0.1). Verify from the phone.
- **GO "PUBLIC"** — design pass on the scoped public door (Access policy, read-only
  board mirror, rate limits, kill-switch).

## HONEST GAPS (tri-state)
- **UNPROVEN**: whether any cloudflared tunnel config ever landed on this box (no
  `~/.cloudflared`, no process) — the "phone surface via Cloudflare tunnel" build
  order looks like it never got past the login gate.
- **UNPROVEN**: app-level auth on the openclaw gateway surface (18789). Tailnet
  membership is the device-level auth; verify app-level before this URL is ever
  shared past his own devices.
- **UNPROVEN**: host.docker.internal resolution inside the tailscale container netns
  (blocks nothing until PHONE GO).
- **INFERRED, not receipt**: mag-openclaw shares netns with mag-openclaw-tailscale.

## STATE OF THE WATCH
Line healthy (0% loss, ~38ms to 8.8.8.8, HTTPS 200s to google/cloudflare/api.z.ai).
Fleet 8/8 containers healthy, all surfaces loopback. WARP daemon idle but installed.
Phone door live tailnet-side, waiting for the phone app. Nothing exposed to the
public internet today.

Decision: escalate to operator — re-surface 2 open GOs (WARP uninstall, phone door); fold into security posture card (ZERO_BACKREF_TRIAGE_20260905)

RESOLVED 2026-09-06 (operator: warp was useless, confirmed kill): WARP verified ALREADY GONE — no winget package, no install paths (the kill resolved itself in an earlier sweep; the audit mattered because nobody had noticed). Phone door: LIVE (tailscale serve, tailnet-only). Both GOs settled. POSSESSION-AUDIT law minted from this finding (LAW_CANDIDATES_059_060_20260906). Cites: LAW_CANDIDATES_059_060_20260906
