# WINDOWS 10 LAPTOP + MESH SECURITY BASELINE (2026-10-10, the perimeter's coldest vertex)

Operator order: "my laptop is windows 10 but could probablty use some securty tuning
same for the whole mesh." This is the join-the-perimeter baseline: a box that runs
consensus_harness.py and files receipts must be trustworthy before it touches the fleet.
Every item is checkable; run the audit as admin PowerShell where noted.

## 1. Join-day checks (the laptop)

1. BITLOCKER ON (or device encryption if Home): `Get-BitLockerVolume C:` - status
   FullyEncrypted or ask why not. A mesh node holds receipts and .env-shaped files.
2. FIREWALL ON, inbound DEFAULT BLOCK. The harness needs NO inbound ports. If a
   tailnet joins later, Tailscale manages its own interface rule - never open broad
   inbound for it.
3. RDP OFF unless actively used: `Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server -Name fDenyTSConnections` - want 1.
4. AUTO-LOGIN OFF; guest account OFF; local admin count known and named.
5. DEFENDER REAL-SCAN ON. Exclusions are SCOPED, never system-wide: only the repo
   tree and docker data paths, and only if measured interference (the estate's AV
   fights were scoped, documented, and reversible).
6. UPDATE LVL: patch level within 30 days. W10 EOL is 2025-10-14 per Microsoft's
   original schedule - check ESU status; an unpatched EOL box joining a perimeter
   is a liability, note it honestly if so.
7. SCHEDULED TASK + STARTUP AUDIT (the two-registry sweep law): export and eyeball
   tasks + Run keys; the estate's own disease was crons outliving shutdowns.
8. .ENV LAW: the laptop's copy of estate secrets never leaves it; never in commits
   (his precommit mesh enforces this at his repos; ours via secret gates + the
   GOOGLE-OAQ class detectors).

## 2. Mesh-level (all boxes, desktop included)

1. INVENTORY: which services listen on which interfaces (netstat -ano | findstr
   LISTENING) vs the docker map: 8080 gstd-node (published 0.0.0.0 - candidate for
   tightening to LAN-only once the platform needs are known), 8765/9000/8000-8001/
   8766 bound 127.0.0.1 (good), 11434 Ollama (check binding: if 0.0.0.0, it is LAN
   reachable - fine for the perimeter, must be firewalled from WAN).
2. THE KEY LAW: no seed phrases, no API keys in chat/repo/logs. Public payout
   addresses are paste-safe; anything else = red flag by definition.
3. PERIMETER EGRESS: the harness enforces loopback/LAN/tailnet-only hosts (the SSRF
   guard, Mimosa-caught 2026-10-10). Same posture for any new perimeter tool: a
   closed-perimeter tool that can reach the internet is not closed.
4. TAILNET IF USED: key expiry on, device approval on, no funnel/exit nodes for the
   perimeter boxes.
5. RECEIPTS: every join-day check above that passes or fails gets a line in the
   box's join receipt (watch/inbox/gstd_perimeter_build_20261010/laptop_join.md
   when the operator runs it on the machine).

## 3. What this baseline deliberately does not do

No hardening theater (no random port renaming, no AV stacking): the threats that
matter here are unpatched EOL, open RDP, overbroad firewall holes, secrets in the
wrong place, and orphaned crons. Those five carry the weight; the rest is costume.

## 4. EOL ASSESSMENT (2026-10-11, measured on the desktop)

- OS: Windows 10 Home 22H2, build 19045. Official EOL was 2025-10-14.
- BUT: KB5126256 installed 2026-09-11 — a patch landed WITHIN THE LAST MONTH,
  a year past the official EOL date. Microsoft is still shipping fixes to this
  build (ESU-class servicing is active on this machine, whether enrolled or
  via the extended-coverage channel).
- Read: the box is NOT unpatched-EOL. It is receiving security updates. The
  EOL clock is a watch item (verify monthly that KBs keep landing), not an
  incident. The laptop (also W10) needs the same check on its join day.
- Fleet posture unchanged: the perimeter surfaces are tailnet-scoped, Ollama
  sits behind the tailnet-only firewall intent, and no inbound ports face the
  public internet. EOL risk on an offline-facing-perimeter box is mostly the
  browser/attack-surface class, not the fleet class.
